"""Document ingestion endpoint.

Accepts uploads of PDF, DOCX, PPTX, TXT, MD, and video/audio files.
Parses text from each, chunks it, and stores in semantic memory so the
tutor can recall the contents in future sessions.

Endpoints:
  POST /documents/upload        — multipart file upload, returns document record
  GET  /documents               — list all uploaded documents for the user
  GET  /documents/{id}          — get a single document + its memory chunks
  DELETE /documents/{id}        — remove document and its memory entries
"""

from __future__ import annotations

import io
import json
import logging
import mimetypes
import os
import re
import tempfile
from datetime import datetime
from typing import Optional

from cuid2 import Cuid as _Cuid
_cuid_gen = _Cuid()
def cuid() -> str:
    return _cuid_gen.generate()
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from pydantic import BaseModel
from sqlmodel import Session, select

from ..db import get_session
from ..deps import get_current_user
from ..models.memory import MemoryRecord
from ..models.user import User
from ..services.semantic_memory import _heuristic_importance as compute_importance

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/documents", tags=["documents"])

# ── Max sizes ────────────────────────────────────────────────────────────────
MAX_BYTES = 50 * 1024 * 1024   # 50 MB hard limit
CHUNK_SIZE = 1200               # characters per memory chunk
CHUNK_OVERLAP = 200             # overlap between adjacent chunks

# ── Supported MIME types ─────────────────────────────────────────────────────
_PDF_TYPES   = {"application/pdf"}
_DOCX_TYPES  = {"application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/msword"}
_PPTX_TYPES  = {
    "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    "application/vnd.ms-powerpoint",
}
_TEXT_TYPES  = {"text/plain", "text/markdown", "text/csv", "application/json"}
_VIDEO_TYPES = {"video/mp4", "video/mpeg", "video/webm", "video/ogg", "video/quicktime"}
_AUDIO_TYPES = {"audio/mpeg", "audio/wav", "audio/ogg", "audio/mp4", "audio/webm"}

ALL_ACCEPTED = _PDF_TYPES | _DOCX_TYPES | _PPTX_TYPES | _TEXT_TYPES | _VIDEO_TYPES | _AUDIO_TYPES

# ── Parsers ───────────────────────────────────────────────────────────────────

def _parse_pdf(data: bytes) -> str:
    from pypdf import PdfReader
    reader = PdfReader(io.BytesIO(data))
    parts: list[str] = []
    for page in reader.pages:
        text = page.extract_text() or ""
        parts.append(text.strip())
    return "\n\n".join(p for p in parts if p)


def _parse_docx(data: bytes) -> str:
    from docx import Document  # type: ignore
    doc = Document(io.BytesIO(data))
    paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
    # Also extract tables
    for table in doc.tables:
        for row in table.rows:
            cell_texts = [c.text.strip() for c in row.cells if c.text.strip()]
            if cell_texts:
                paragraphs.append(" | ".join(cell_texts))
    return "\n\n".join(paragraphs)


def _parse_pptx(data: bytes) -> str:
    from pptx import Presentation  # type: ignore
    prs = Presentation(io.BytesIO(data))
    slides_text: list[str] = []
    for i, slide in enumerate(prs.slides, 1):
        texts: list[str] = []
        for shape in slide.shapes:
            if not shape.has_text_frame:
                continue
            for para in shape.text_frame.paragraphs:
                line = " ".join(run.text for run in para.runs).strip()
                if line:
                    texts.append(line)
        if texts:
            slides_text.append(f"[Slide {i}]\n" + "\n".join(texts))
    return "\n\n".join(slides_text)


def _parse_text(data: bytes) -> str:
    for enc in ("utf-8", "latin-1", "cp1252"):
        try:
            return data.decode(enc)
        except UnicodeDecodeError:
            continue
    return data.decode("utf-8", errors="replace")


def _parse_video_audio(data: bytes, filename: str) -> str:
    """Best-effort: extract metadata. Full transcription requires Whisper (optional)."""
    size_mb = len(data) / 1024 / 1024
    name = os.path.basename(filename)
    return (
        f"[Video/audio file: {name}]\n"
        f"Size: {size_mb:.1f} MB\n"
        "Note: Full speech-to-text transcription is not yet enabled. "
        "The file has been stored in your documents for reference. "
        "To enable automatic transcription, add a Whisper API key to your environment."
    )


def _extract_text(data: bytes, mime: str, filename: str) -> str:
    try:
        if mime in _PDF_TYPES:
            return _parse_pdf(data)
        if mime in _DOCX_TYPES:
            return _parse_docx(data)
        if mime in _PPTX_TYPES:
            return _parse_pptx(data)
        if mime in _TEXT_TYPES:
            return _parse_text(data)
        if mime in (_VIDEO_TYPES | _AUDIO_TYPES):
            return _parse_video_audio(data, filename)
    except Exception as exc:
        logger.warning("Parse failed for %s (%s): %s", filename, mime, exc)
        return f"[Could not fully parse {filename}: {exc}]"
    return f"[Unsupported file type: {mime}]"


def _chunk(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """Split text into overlapping chunks."""
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    if not text:
        return []
    chunks: list[str] = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        if end == len(text):
            break
        start = end - overlap
    return chunks


# ── DB model (stored in MemoryRecord with role="document") ───────────────────
# We re-use MemoryRecord with role="document" and store doc metadata in the
# content field as JSON preamble. A separate meta record marks the doc header.

def _doc_meta_content(filename: str, mime: str, size_bytes: int, chunk_count: int) -> str:
    return json.dumps({
        "_doc_meta": True,
        "filename": filename,
        "mime": mime,
        "size_bytes": size_bytes,
        "chunk_count": chunk_count,
    })


# ── Response models ───────────────────────────────────────────────────────────

class DocumentOut(BaseModel):
    id: str
    filename: str
    mime: str
    size_bytes: int
    chunk_count: int
    preview: str
    created_at: datetime


class DocumentDetail(DocumentOut):
    chunks: list[str]


def _meta_to_out(record: MemoryRecord) -> Optional[DocumentOut]:
    try:
        meta = json.loads(record.content)
        if not meta.get("_doc_meta"):
            return None
        return DocumentOut(
            id=record.id,
            filename=meta.get("filename", "unknown"),
            mime=meta.get("mime", ""),
            size_bytes=meta.get("size_bytes", 0),
            chunk_count=meta.get("chunk_count", 0),
            preview=meta.get("preview", ""),
            created_at=record.created_at,
        )
    except Exception:
        return None


# ── Endpoints ─────────────────────────────────────────────────────────────────

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

    # Normalise common aliases
    if filename.lower().endswith(".md"):
        mime = "text/markdown"
    if filename.lower().endswith(".csv"):
        mime = "text/csv"

    if mime not in ALL_ACCEPTED:
        raise HTTPException(
            status_code=415,
            detail=f"Unsupported file type '{mime}'. Accepted: PDF, DOCX, PPTX, TXT, MD, CSV, MP4, and other common video/audio.",
        )

    text = _extract_text(data, mime, filename)
    chunks = _chunk(text)
    if not chunks:
        chunks = [f"[Empty document: {filename}]"]

    doc_id = cuid()
    preview = text[:300].replace("\n", " ").strip()

    # Store meta record (role="document", session_id=doc_id marks the group)
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
        }),
        importance=0.9,
    )
    session.add(meta_record)

    # Store each chunk
    for i, chunk in enumerate(chunks):
        importance = compute_importance(chunk)
        chunk_record = MemoryRecord(
            id=cuid(),
            user_id=user.id,
            role="document",
            session_id=doc_id,
            content=f"[From document '{filename}', part {i+1}/{len(chunks)}]\n{chunk}",
            importance=importance,
        )
        session.add(chunk_record)

    session.commit()
    session.refresh(meta_record)

    return DocumentOut(
        id=doc_id,
        filename=filename,
        mime=mime,
        size_bytes=len(data),
        chunk_count=len(chunks),
        preview=preview,
        created_at=meta_record.created_at,
    )


@router.get("", response_model=list[DocumentOut])
def list_documents(
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
) -> list[DocumentOut]:
    stmt = (
        select(MemoryRecord)
        .where(MemoryRecord.user_id == user.id)
        .where(MemoryRecord.role == "document")
        .order_by(MemoryRecord.created_at.desc())
    )
    rows = list(session.exec(stmt))
    docs: list[DocumentOut] = []
    seen_ids: set[str] = set()
    for r in rows:
        if r.session_id and r.session_id not in seen_ids:
            out = _meta_to_out(r)
            if out:
                seen_ids.add(r.session_id)
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

    chunk_stmt = (
        select(MemoryRecord)
        .where(MemoryRecord.user_id == user.id)
        .where(MemoryRecord.session_id == doc_id)
        .where(MemoryRecord.id != doc_id)
        .order_by(MemoryRecord.created_at)
    )
    chunks = [r.content for r in session.exec(chunk_stmt)]
    return DocumentDetail(**out.model_dump(), chunks=chunks)


@router.delete("/{doc_id}")
def delete_document(
    doc_id: str,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
) -> dict:
    stmt = (
        select(MemoryRecord)
        .where(MemoryRecord.user_id == user.id)
        .where(MemoryRecord.session_id == doc_id)
    )
    rows = list(session.exec(stmt))
    if not rows:
        raise HTTPException(status_code=404, detail="Document not found")
    for r in rows:
        session.delete(r)
    session.commit()
    return {"ok": True, "deleted": len(rows)}
