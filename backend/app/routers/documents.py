"""Document ingestion — Cloudinary-powered.

Every uploaded file goes through:
  1. Upload to Cloudinary (storage + CDN)
  2. Cloudinary transformations for images:
       - Auto-enhance  : e_improve,e_sharpen,e_auto_contrast
       - Background removal : e_background_removal
       - Thumbnail     : c_thumb,w_300,h_300,g_auto
  3. Text extraction (Cloudinary OCR for images, local parsers for docs)
  4. LLM classification → doc_type / subject / summary / key_topics
  5. Text chunked into MemoryRecord rows (semantic memory)

Endpoints:
  POST /documents/upload
  GET  /documents
  GET  /documents/{id}
  DELETE /documents/{id}
"""

from __future__ import annotations

import io
import json
import logging
import mimetypes
import os
import re
from datetime import datetime
from typing import Optional

import cloudinary
import cloudinary.uploader
import cloudinary.api
from cuid2 import Cuid as _Cuid

_cuid_gen = _Cuid()
def cuid() -> str:
    return _cuid_gen.generate()

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from pydantic import BaseModel
from sqlmodel import Session, select

from ..agent.agent_loop import get_async_client
from ..config import get_settings
from ..db import get_session
from ..deps import get_current_user
from ..models.memory import MemoryRecord
from ..models.user import User
from ..services.semantic_memory import _heuristic_importance as compute_importance

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/documents", tags=["documents"])

# ── Cloudinary config ─────────────────────────────────────────────────────────

def _init_cloudinary() -> None:
    """Configure Cloudinary from env / CLOUDINARY_URL."""
    url = os.getenv("CLOUDINARY_URL", "")
    if url.startswith("cloudinary://"):
        cloudinary.config(cloudinary_url=url)
    else:
        settings = get_settings()
        if settings.cloudinary_cloud_name and settings.cloudinary_api_key:
            cloudinary.config(
                cloud_name=settings.cloudinary_cloud_name,
                api_key=settings.cloudinary_api_key,
                api_secret=settings.cloudinary_api_secret,
                secure=True,
            )

_init_cloudinary()

# ── Limits ────────────────────────────────────────────────────────────────────
MAX_BYTES    = 50 * 1024 * 1024
CHUNK_SIZE   = 1200
CHUNK_OVERLAP = 200

# ── MIME sets ─────────────────────────────────────────────────────────────────
_PDF_TYPES   = {"application/pdf"}
_DOCX_TYPES  = {
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/msword",
}
_PPTX_TYPES  = {
    "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    "application/vnd.ms-powerpoint",
}
_TEXT_TYPES  = {"text/plain", "text/markdown", "text/csv", "application/json"}
_IMAGE_TYPES = {
    "image/png", "image/jpeg", "image/jpg", "image/webp",
    "image/bmp", "image/gif", "image/tiff",
}
_VIDEO_TYPES = {"video/mp4", "video/mpeg", "video/webm", "video/ogg", "video/quicktime"}
_AUDIO_TYPES = {"audio/mpeg", "audio/wav", "audio/ogg", "audio/mp4", "audio/webm"}
_RAW_TYPES   = _PDF_TYPES | _DOCX_TYPES | _PPTX_TYPES | _TEXT_TYPES

ALL_ACCEPTED = _RAW_TYPES | _IMAGE_TYPES | _VIDEO_TYPES | _AUDIO_TYPES


# ── Cloudinary upload helpers ─────────────────────────────────────────────────

def _cld_resource_type(mime: str) -> str:
    if mime in _IMAGE_TYPES: return "image"
    if mime in _VIDEO_TYPES | _AUDIO_TYPES: return "video"
    return "raw"


def _upload_to_cloudinary(data: bytes, filename: str, mime: str, folder: str) -> dict:
    """Upload bytes to Cloudinary and return the upload response dict."""
    resource_type = _cld_resource_type(mime)
    result = cloudinary.uploader.upload(
        data,
        resource_type=resource_type,
        folder=folder,
        use_filename=True,
        unique_filename=True,
        overwrite=False,
        # Request Cloudinary OCR for images (if the add-on is enabled)
        ocr="adv_ocr" if resource_type == "image" else None,
    )
    return result  # type: ignore[return-value]


def _cld_transformation_url(public_id: str, resource_type: str, transformation: str) -> str:
    """Build a Cloudinary transformation delivery URL."""
    settings = get_settings()
    cloud = settings.cloudinary_cloud_name or os.getenv("CLOUDINARY_CLOUD_NAME", "")
    return (
        f"https://res.cloudinary.com/{cloud}/{resource_type}/upload/"
        f"{transformation}/{public_id}"
    )


def _build_image_urls(public_id: str) -> tuple[str, str, str]:
    """
    Returns (thumbnail_url, enhanced_url, nobg_url) as Cloudinary delivery URLs.
    These are on-the-fly transformations — no extra API calls needed.
    """
    thumb    = _cld_transformation_url(public_id, "image", "c_thumb,w_300,h_300,g_auto,f_auto,q_auto")
    enhanced = _cld_transformation_url(public_id, "image", "e_improve,e_sharpen:80,e_auto_contrast,f_auto,q_auto")
    nobg     = _cld_transformation_url(public_id, "image", "e_background_removal,f_png")
    return thumb, enhanced, nobg


# ── Local text parsers (for document types Cloudinary can't parse) ────────────

def _parse_pdf(data: bytes) -> str:
    from pypdf import PdfReader
    reader = PdfReader(io.BytesIO(data))
    return "\n\n".join((p.extract_text() or "").strip() for p in reader.pages).strip()


def _parse_docx(data: bytes) -> str:
    from docx import Document  # type: ignore
    doc = Document(io.BytesIO(data))
    parts = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
    for table in doc.tables:
        for row in table.rows:
            cells = [c.text.strip() for c in row.cells if c.text.strip()]
            if cells: parts.append(" | ".join(cells))
    return "\n\n".join(parts)


def _parse_pptx(data: bytes) -> str:
    from pptx import Presentation  # type: ignore
    prs = Presentation(io.BytesIO(data))
    slides: list[str] = []
    for i, slide in enumerate(prs.slides, 1):
        texts = [
            " ".join(run.text for run in para.runs).strip()
            for shape in slide.shapes if shape.has_text_frame
            for para in shape.text_frame.paragraphs
        ]
        texts = [t for t in texts if t]
        if texts:
            slides.append(f"[Slide {i}]\n" + "\n".join(texts))
    return "\n\n".join(slides)


def _parse_text(data: bytes) -> str:
    for enc in ("utf-8", "latin-1", "cp1252"):
        try: return data.decode(enc)
        except UnicodeDecodeError: continue
    return data.decode("utf-8", errors="replace")


def _extract_text_from_cloudinary_ocr(upload_result: dict) -> str:
    """Pull OCR text from Cloudinary's adv_ocr response if available."""
    try:
        ocr_data = upload_result.get("info", {}).get("ocr", {})
        adv = ocr_data.get("adv_ocr", {}) or ocr_data.get("adv_ocr", {})
        status = adv.get("status", "")
        if status == "complete":
            data = adv.get("data", [])
            all_text: list[str] = []
            for page in data:
                for annotation in page.get("textAnnotations", []):
                    text = annotation.get("description", "")
                    if text: all_text.append(text); break  # first annotation = full page text
            return "\n\n".join(all_text).strip()
    except Exception as exc:
        logger.debug("OCR extraction failed: %s", exc)
    return ""


async def _extract_text(data: bytes, mime: str, filename: str, upload_result: dict) -> str:
    """Extract text from the document, using Cloudinary OCR for images."""
    try:
        if mime in _PDF_TYPES:   return _parse_pdf(data)
        if mime in _DOCX_TYPES:  return _parse_docx(data)
        if mime in _PPTX_TYPES:  return _parse_pptx(data)
        if mime in _TEXT_TYPES:  return _parse_text(data)
        if mime in _IMAGE_TYPES:
            # Try Cloudinary OCR first
            ocr_text = _extract_text_from_cloudinary_ocr(upload_result)
            if ocr_text:
                return ocr_text
            # Fallback: Groq vision
            return await _groq_vision_ocr(data, mime, filename)
        if mime in (_VIDEO_TYPES | _AUDIO_TYPES):
            dur = upload_result.get("duration", "")
            return (
                f"[Media file: {filename}]\n"
                f"Size: {len(data)/1024/1024:.1f} MB"
                + (f"\nDuration: {dur:.1f}s" if dur else "") + "\n"
                "Transcription requires a Whisper API key."
            )
    except Exception as exc:
        logger.warning("Text extraction failed for %s: %s", filename, exc)
        return f"[Parse failed: {exc}]"
    return ""


async def _groq_vision_ocr(data: bytes, mime: str, filename: str) -> str:
    import base64
    try:
        b64 = base64.b64encode(data).decode()
        settings = get_settings()
        client = get_async_client()
        completion = await client.chat.completions.create(
            model=settings.fast_llm_model or settings.llm_model,
            messages=[{
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{b64}"}},
                    {"type": "text", "text":
                        "Extract all visible text from this image verbatim, then briefly describe what it shows.\n"
                        "Format:\nEXTRACTED TEXT:\n<text or 'None'>\n\nDESCRIPTION:\n<description>"},
                ],
            }],
            max_tokens=1024, temperature=0.1,
        )
        return (completion.choices[0].message.content or "").strip()
    except Exception as exc:
        return f"[Image: {filename}. Vision OCR unavailable: {exc}]"


# ── LLM classification ────────────────────────────────────────────────────────

_CLASSIFY_PROMPT = """Classify this document excerpt and return STRICT JSON (no markdown, no fences):

{{
  "doc_type": "<Research Paper|Lecture Notes|Textbook Chapter|Presentation|Study Guide|Code/Technical|Image/Diagram|Video Transcript|General Notes|Other>",
  "subject": "<subject area>",
  "summary": "<2-3 sentence plain-English summary>",
  "key_topics": ["<topic>", "<topic>", "<topic>"]
}}

Excerpt:
{excerpt}"""


async def _classify(text: str) -> dict:
    try:
        settings = get_settings()
        client = get_async_client()
        completion = await client.chat.completions.create(
            model=settings.fast_llm_model or settings.llm_model,
            messages=[
                {"role": "system", "content": "Return strict JSON only."},
                {"role": "user", "content": _CLASSIFY_PROMPT.format(excerpt=text[:1500].strip())},
            ],
            max_tokens=400, temperature=0.1,
        )
        raw = re.sub(r"^```(?:json)?\s*|\s*```$", "", (completion.choices[0].message.content or "").strip())
        return json.loads(raw)
    except Exception as exc:
        logger.warning("Classification failed: %s", exc)
        return {"doc_type": "Other", "subject": "", "summary": "", "key_topics": []}


# ── Chunker ───────────────────────────────────────────────────────────────────

def _chunk(text: str) -> list[str]:
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    if not text: return []
    chunks: list[str] = []
    start = 0
    while start < len(text):
        end = min(start + CHUNK_SIZE, len(text))
        chunks.append(text[start:end])
        if end == len(text): break
        start = end - CHUNK_OVERLAP
    return chunks


# ── Response models ───────────────────────────────────────────────────────────

class DocumentOut(BaseModel):
    id: str
    filename: str
    mime: str
    size_bytes: int
    chunk_count: int
    preview: str
    created_at: datetime
    # Cloudinary
    cld_public_id: str = ""
    cld_secure_url: str = ""
    # Classification
    doc_type: str = "Other"
    subject: str = ""
    summary: str = ""
    key_topics: list[str] = []
    # Image delivery URLs (Cloudinary on-the-fly transformations)
    is_image: bool = False
    thumbnail_url: Optional[str] = None
    enhanced_url: Optional[str] = None
    nobg_url: Optional[str] = None


class DocumentDetail(DocumentOut):
    chunks: list[str]


def _meta_to_out(record: MemoryRecord) -> Optional[DocumentOut]:
    try:
        meta = json.loads(record.content)
        if not meta.get("_doc_meta"): return None
        return DocumentOut(
            id=record.id,
            filename=meta.get("filename", "unknown"),
            mime=meta.get("mime", ""),
            size_bytes=meta.get("size_bytes", 0),
            chunk_count=meta.get("chunk_count", 0),
            preview=meta.get("preview", ""),
            created_at=record.created_at,
            cld_public_id=meta.get("cld_public_id", ""),
            cld_secure_url=meta.get("cld_secure_url", ""),
            doc_type=meta.get("doc_type", "Other"),
            subject=meta.get("subject", ""),
            summary=meta.get("summary", ""),
            key_topics=meta.get("key_topics", []),
            is_image=meta.get("is_image", False),
            thumbnail_url=meta.get("thumbnail_url"),
            enhanced_url=meta.get("enhanced_url"),
            nobg_url=meta.get("nobg_url"),
        )
    except Exception:
        return None


# ── Upload endpoint ───────────────────────────────────────────────────────────

@router.post("/upload", response_model=DocumentOut)
async def upload_document(
    file: UploadFile = File(...),
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
) -> DocumentOut:
    data = await file.read()
    if len(data) > MAX_BYTES:
        raise HTTPException(status_code=413, detail=f"File too large (max {MAX_BYTES // (1024*1024)} MB)")

    filename = file.filename or "upload"
    mime = file.content_type or mimetypes.guess_type(filename)[0] or "application/octet-stream"

    # Normalise MIME from extension
    ext_lower = filename.lower().rsplit(".", 1)[-1] if "." in filename else ""
    _ext_map = {
        "md": "text/markdown", "csv": "text/csv", "txt": "text/plain",
        "png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg",
        "webp": "image/webp", "bmp": "image/bmp", "gif": "image/gif",
    }
    if ext_lower in _ext_map:
        mime = _ext_map[ext_lower]

    if mime not in ALL_ACCEPTED:
        raise HTTPException(
            status_code=415,
            detail=f"Unsupported type '{mime}'. Accepted: PDF, DOCX, PPTX, TXT, MD, CSV, PNG, JPG, WEBP, MP4, MP3…",
        )

    is_image = mime in _IMAGE_TYPES
    settings = get_settings()
    folder = f"{settings.cloudinary_folder}/docs/user_{user.id}"

    # ── 1. Upload to Cloudinary ───────────────────────────────────────────────
    try:
        upload_result = _upload_to_cloudinary(data, filename, mime, folder)
        cld_public_id  = upload_result.get("public_id", "")
        cld_secure_url = upload_result.get("secure_url", "")
    except Exception as exc:
        logger.error("Cloudinary upload failed: %s", exc)
        raise HTTPException(status_code=502, detail=f"Cloudinary upload failed: {exc}")

    # ── 2. Image transformation URLs (on-the-fly, no extra API call) ──────────
    thumbnail_url: Optional[str] = None
    enhanced_url:  Optional[str] = None
    nobg_url:      Optional[str] = None

    if is_image and cld_public_id:
        thumbnail_url, enhanced_url, nobg_url = _build_image_urls(cld_public_id)

    # ── 3. Extract text ───────────────────────────────────────────────────────
    text = await _extract_text(data, mime, filename, upload_result)
    chunks = _chunk(text) or [f"[Empty document: {filename}]"]

    # ── 4. Classify ───────────────────────────────────────────────────────────
    cls = await _classify(text)

    # ── 5. Persist metadata + chunks in DB ───────────────────────────────────
    doc_id = cuid()
    preview = text[:300].replace("\n", " ").strip()

    meta_record = MemoryRecord(
        id=doc_id,
        user_id=user.id,
        role="document",
        session_id=doc_id,
        content=json.dumps({
            "_doc_meta": True,
            "filename": filename,
            "mime": mime,
            "size_bytes": len(data),
            "chunk_count": len(chunks),
            "preview": preview,
            "cld_public_id": cld_public_id,
            "cld_secure_url": cld_secure_url,
            "doc_type": cls.get("doc_type", "Other"),
            "subject": cls.get("subject", ""),
            "summary": cls.get("summary", ""),
            "key_topics": cls.get("key_topics", []),
            "is_image": is_image,
            "thumbnail_url": thumbnail_url,
            "enhanced_url": enhanced_url,
            "nobg_url": nobg_url,
        }),
        importance=0.9,
    )
    session.add(meta_record)

    for i, chunk in enumerate(chunks):
        session.add(MemoryRecord(
            id=cuid(),
            user_id=user.id,
            role="document",
            session_id=doc_id,
            content=f"[From '{filename}', part {i+1}/{len(chunks)}]\n{chunk}",
            importance=compute_importance(chunk),
        ))

    session.commit()
    session.refresh(meta_record)

    return DocumentOut(
        id=doc_id, filename=filename, mime=mime, size_bytes=len(data),
        chunk_count=len(chunks), preview=preview,
        created_at=meta_record.created_at,
        cld_public_id=cld_public_id, cld_secure_url=cld_secure_url,
        doc_type=cls.get("doc_type", "Other"),
        subject=cls.get("subject", ""),
        summary=cls.get("summary", ""),
        key_topics=cls.get("key_topics", []),
        is_image=is_image,
        thumbnail_url=thumbnail_url,
        enhanced_url=enhanced_url,
        nobg_url=nobg_url,
    )


# ── List / Get / Delete ───────────────────────────────────────────────────────

@router.get("", response_model=list[DocumentOut])
def list_documents(
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
) -> list[DocumentOut]:
    rows = list(session.exec(
        select(MemoryRecord)
        .where(MemoryRecord.user_id == user.id)
        .where(MemoryRecord.role == "document")
        .order_by(MemoryRecord.created_at.desc())
    ))
    docs: list[DocumentOut] = []
    seen: set[str] = set()
    for r in rows:
        if r.session_id and r.session_id not in seen:
            out = _meta_to_out(r)
            if out:
                seen.add(r.session_id)
                docs.append(out)
    return docs


@router.get("/{doc_id}", response_model=DocumentDetail)
def get_document(
    doc_id: str,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
) -> DocumentDetail:
    meta_record = session.get(MemoryRecord, doc_id)
    if not meta_record or meta_record.user_id != user.id:
        raise HTTPException(status_code=404, detail="Document not found")
    out = _meta_to_out(meta_record)
    if not out:
        raise HTTPException(status_code=404, detail="Document not found")
    chunks = [r.content for r in session.exec(
        select(MemoryRecord)
        .where(MemoryRecord.user_id == user.id)
        .where(MemoryRecord.session_id == doc_id)
        .where(MemoryRecord.id != doc_id)
        .order_by(MemoryRecord.created_at)
    )]
    return DocumentDetail(**out.model_dump(), chunks=chunks)


@router.delete("/{doc_id}")
def delete_document(
    doc_id: str,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
) -> dict:
    rows = list(session.exec(
        select(MemoryRecord)
        .where(MemoryRecord.user_id == user.id)
        .where(MemoryRecord.session_id == doc_id)
    ))
    if not rows:
        raise HTTPException(status_code=404, detail="Document not found")
    # Also delete from Cloudinary
    meta_record = next((r for r in rows if r.id == doc_id), None)
    if meta_record:
        try:
            meta = json.loads(meta_record.content)
            pub_id = meta.get("cld_public_id", "")
            res_type = _cld_resource_type(meta.get("mime", "raw"))
            if pub_id:
                cloudinary.uploader.destroy(pub_id, resource_type=res_type)
        except Exception as exc:
            logger.warning("Cloudinary delete failed: %s", exc)
    for r in rows:
        session.delete(r)
    session.commit()
    return {"ok": True, "deleted": len(rows)}
