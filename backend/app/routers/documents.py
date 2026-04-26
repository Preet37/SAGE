"""My Documents — per-user Cloudinary-backed file storage.

Free-tier features (always on):
  - Direct upload to Cloudinary via signed params
  - HLS adaptive streaming for videos
  - Smart-crop (g_auto, c_fill) on video posters
  - Multi-page PDF rendering as images
  - Text watermark overlay (l_text) showing the category
  - Filename search

Add-on features (opt-in via /enhance — return 402 from Cloudinary if not enabled):
  - Generative background removal, generative fill, generative recolor, AI upscale
  - Semantic search (falls back to filename search if 4xx)
"""
from __future__ import annotations

import json
import os
import time
import urllib.parse
from typing import List, Literal, Optional

import cloudinary
import cloudinary.api
import cloudinary.uploader
import cloudinary.utils
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlmodel import Session, select

from ..db import get_session
from ..deps import get_current_user
from ..models.document import Document
from ..models.user import User

DEFAULT_CATEGORY = "Document"

router = APIRouter(prefix="/documents", tags=["documents"])


def _derive_category(tags: list[str], resource_type: str = "image") -> str:
    """Pick a watermark label from the AI-generated tags.

    Cloudinary's Imagga/Google taggers return tags ranked by confidence. The
    top tag is usually a strong content descriptor (e.g. "hat", "whiteboard",
    "document"). We title-case it and use it as the category.
    """
    for t in tags or []:
        cleaned = (t or "").strip()
        if cleaned and len(cleaned) >= 3:
            return cleaned.title()
    if resource_type == "video":
        return "Video"
    return DEFAULT_CATEGORY


def _ensure_configured() -> None:
    if not os.getenv("CLOUDINARY_URL") and not os.getenv("CLOUDINARY_CLOUD_NAME"):
        raise HTTPException(status_code=500, detail="Cloudinary not configured")
    # cloudinary auto-reads CLOUDINARY_URL from env on import
    cloudinary.config(secure=True)


def _user_folder(user_id: str) -> str:
    return f"sage/users/{user_id}"


def _ensure_image_source(user_id: str, doc) -> str:
    """Return a public_id that image add-ons (Pixelz, VIESUS, OCR) can process.

    Cloudinary add-ons that operate on raster pixels won't run when the source
    is a PDF — chaining `pg_1,f_jpg` in the URL doesn't help because they look
    at the source asset, not the transformed bytes. So for PDFs we lazily
    upload page 1 as a JPG derivative and reuse it.
    """
    if (doc.format or "").lower() != "pdf":
        return doc.public_id

    derivative_id = f"sage/users/{user_id}/_pages/{doc.id}_p1"

    try:
        cloudinary.api.resource(derivative_id, resource_type="image")
        return derivative_id
    except Exception:
        pass

    rendered_url, _ = cloudinary.utils.cloudinary_url(
        doc.public_id,
        resource_type="image",
        secure=True,
        format="jpg",
        page=1,
        transformation=[{"width": 2000, "crop": "limit"}],
    )
    cloudinary.uploader.upload(
        rendered_url,
        public_id=derivative_id,
        resource_type="image",
        overwrite=False,
    )
    return derivative_id


def _safe_prompt(text: str) -> str:
    """URL-encode a prompt for Cloudinary's `prompt_(...)` syntax.

    Strips characters that would break the transformation grammar
    (commas, semicolons, parentheses) and percent-encodes the rest.
    """
    cleaned = (text or "").replace(",", " ").replace(";", " ").replace("(", "").replace(")", "")
    return urllib.parse.quote(cleaned.strip(), safe="")


def _watermark_transform(category: str) -> str:
    """Bottom-left text overlay tagging the category.

    Black text at 50% opacity, no background — sits softly on any document.
    """
    safe = urllib.parse.quote(category, safe="")
    return (
        f"l_text:Arial_24_bold:{safe},"
        f"co_rgb:000000,o_50,"
        f"g_south_west,x_18,y_18"
    )


def _video_url(public_id: str, category: str) -> str:
    base, _ = cloudinary.utils.cloudinary_url(
        public_id,
        resource_type="video",
        format="m3u8",
        streaming_profile="auto",
        secure=True,
    )
    return base


def _video_poster_url(public_id: str, category: str) -> str:
    base, _ = cloudinary.utils.cloudinary_url(
        public_id,
        resource_type="video",
        format="jpg",
        transformation=[
            {"width": 1280, "height": 720, "crop": "fill", "gravity": "auto"},
            {"raw_transformation": _watermark_transform(category)},
        ],
        secure=True,
    )
    return base


def _image_url(
    public_id: str,
    category: str,
    page: Optional[int] = None,
    is_pdf: bool = False,
) -> str:
    transform = [
        {"width": 1600, "crop": "limit"},
        {"raw_transformation": _watermark_transform(category)},
    ]
    kwargs: dict = dict(
        resource_type="image",
        secure=True,
        transformation=transform,
    )
    if is_pdf:
        # PDFs uploaded as image need explicit page + image format to render in <img>.
        kwargs["format"] = "jpg"
        kwargs["page"] = page or 1
    elif page is not None:
        kwargs["page"] = page
    base, _ = cloudinary.utils.cloudinary_url(public_id, **kwargs)
    return base


def _raw_url(public_id: str) -> str:
    base, _ = cloudinary.utils.cloudinary_url(public_id, resource_type="raw", secure=True)
    return base


# ───────────── Schemas ─────────────


class SignParams(BaseModel):
    resource_type: Literal["image", "video", "raw"]


class SignResponse(BaseModel):
    cloud_name: str
    api_key: str
    timestamp: int
    folder: str
    signature: str
    resource_type: str
    # Extra params the browser must include in the upload form, exactly as
    # they were signed. Tagging add-ons run during upload — these enable
    # them automatically.
    extra_params: dict[str, str]


class ImportPayload(BaseModel):
    public_id: str
    resource_type: Literal["image", "video", "raw"]
    format: Optional[str] = None
    bytes: int = 0
    pages: Optional[int] = None
    duration: Optional[float] = None
    # Optional override; if absent we derive the category from AI tags.
    category: Optional[str] = None
    original_filename: str
    tags: List[str] = []


class UpdateCategoryPayload(BaseModel):
    category: str


class DocumentOut(BaseModel):
    id: str
    public_id: str
    resource_type: str
    format: Optional[str]
    bytes: int
    pages: Optional[int]
    duration: Optional[float]
    category: str
    original_filename: str
    tags: List[str] = []
    preview_url: str
    download_url: str
    streaming_url: Optional[str] = None


class EnhanceRequest(BaseModel):
    document_id: str
    op: Literal["bg_remove", "auto_enhance", "gen_remove", "gen_fill", "gen_recolor", "upscale"]
    prompt: Optional[str] = None  # for gen_remove / gen_fill / gen_recolor


class EnhanceResponse(BaseModel):
    url: str
    enabled: bool
    note: Optional[str] = None


# ───────────── Endpoints ─────────────


@router.post("/sign", response_model=SignResponse)
def sign_upload(
    params: SignParams,
    user: User = Depends(get_current_user),
):
    """Return signed params so the browser can upload direct-to-Cloudinary.

    Tagging add-ons (Imagga, Google Auto Tagging, Cloudinary AI Vision) run
    during upload when the right params are signed in. Their output tags
    populate `result.tags` on the upload response and become searchable.
    """
    _ensure_configured()
    cfg = cloudinary.config()
    folder = _user_folder(user.id)
    timestamp = int(time.time())

    # auto_tagging: keeps any tag with confidence >= 0.6 from the categorizers.
    # categorization: which AI taggers to run. Imagga is image-only; google
    # works on both images and video keyframes.
    # Lower threshold = more tags = better content-based recall in search.
    extra: dict[str, str] = {
        "categorization": "google_tagging,imagga_tagging",
        "auto_tagging": "0.4",
    }

    to_sign: dict = {"folder": folder, "timestamp": timestamp, **extra}
    signature = cloudinary.utils.api_sign_request(to_sign, cfg.api_secret)
    return SignResponse(
        cloud_name=cfg.cloud_name,
        api_key=cfg.api_key,
        timestamp=timestamp,
        folder=folder,
        signature=signature,
        resource_type=params.resource_type,
        extra_params=extra,
    )


@router.post("/import", response_model=DocumentOut)
def import_document(
    payload: ImportPayload,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    """Persist a Cloudinary upload result to the user's document list."""
    _ensure_configured()

    folder = _user_folder(user.id)
    if not payload.public_id.startswith(folder + "/"):
        raise HTTPException(status_code=403, detail="public_id outside user folder")

    derived_category = payload.category or _derive_category(
        payload.tags, payload.resource_type
    )
    doc = Document(
        user_id=user.id,
        public_id=payload.public_id,
        resource_type=payload.resource_type,
        format=payload.format,
        bytes=payload.bytes,
        pages=payload.pages,
        duration=payload.duration,
        category=derived_category,
        original_filename=payload.original_filename,
        tags_json=json.dumps(payload.tags) if payload.tags else None,
    )
    session.add(doc)
    session.commit()
    session.refresh(doc)

    # Best-effort: index OCR text for images and PDFs so search can match
    # words inside the document. Videos skip — Cloudinary's OCR add-on doesn't
    # process video; that needs the Video Transcription add-on which is async.
    if doc.resource_type == "image":
        try:
            text, _ = _run_ocr_for_doc(user.id, doc)
            if text:
                doc.content_text = text
                session.add(doc)
                session.commit()
                session.refresh(doc)
        except Exception:
            pass

    return _to_out(doc)


@router.patch("/{doc_id}", response_model=DocumentOut)
def update_document(
    doc_id: str,
    payload: UpdateCategoryPayload,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    _ensure_configured()
    doc = session.get(Document, doc_id)
    if not doc or doc.user_id != user.id:
        raise HTTPException(status_code=404, detail="Document not found")
    doc.category = payload.category
    session.add(doc)
    session.commit()
    session.refresh(doc)
    return _to_out(doc)


@router.get("", response_model=List[DocumentOut])
def list_documents(
    q: Optional[str] = Query(default=None),
    category: Optional[str] = None,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    _ensure_configured()
    stmt = select(Document).where(Document.user_id == user.id)
    if category:
        stmt = stmt.where(Document.category == category)
    if q:
        like = f"%{q.lower()}%"
        stmt = stmt.where(Document.original_filename.ilike(like))
    stmt = stmt.order_by(Document.created_at.desc())
    docs = session.exec(stmt).all()
    return [_to_out(d) for d in docs]


@router.get("/search", response_model=List[DocumentOut])
def search_documents(
    q: str = Query(..., min_length=1),
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    """Try Cloudinary semantic search; fall back to filename match on any error."""
    _ensure_configured()
    folder = _user_folder(user.id)
    public_ids: list[str] = []
    semantic_ok = False
    try:
        # Cloudinary Search API — works only on premium tiers with Visual Search.
        result = cloudinary.search.Search() \
            .expression(f'folder:"{folder}/*" AND ({q})') \
            .max_results(50) \
            .execute()
        public_ids = [r.get("public_id") for r in result.get("resources", []) if r.get("public_id")]
        semantic_ok = True
    except Exception:
        semantic_ok = False

    if semantic_ok and public_ids:
        stmt = select(Document).where(
            Document.user_id == user.id,
            Document.public_id.in_(public_ids),  # type: ignore[attr-defined]
        )
        docs = session.exec(stmt).all()
        return [_to_out(d) for d in docs]

    # Fallback: match filename OR AI-generated tags OR OCR'd content text.
    docs = session.exec(
        select(Document)
        .where(Document.user_id == user.id)
        .order_by(Document.created_at.desc())
    ).all()
    needle = q.lower()
    matched = []
    for d in docs:
        if needle in (d.original_filename or "").lower():
            matched.append(d)
            continue
        if d.content_text and needle in d.content_text.lower():
            matched.append(d)
            continue
        if d.tags_json:
            try:
                tags = [t.lower() for t in json.loads(d.tags_json)]
            except Exception:
                tags = []
            if any(needle in t or t in needle for t in tags):
                matched.append(d)
    return [_to_out(d) for d in matched]


@router.delete("/{doc_id}")
def delete_document(
    doc_id: str,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    _ensure_configured()
    doc = session.get(Document, doc_id)
    if not doc or doc.user_id != user.id:
        raise HTTPException(status_code=404, detail="Document not found")
    try:
        cloudinary.uploader.destroy(doc.public_id, resource_type=doc.resource_type, invalidate=True)
    except Exception:
        pass  # we still want to remove the DB row
    session.delete(doc)
    session.commit()
    return {"deleted": True}


class OcrResponse(BaseModel):
    text: str
    blocks: int


class TranscriptResponse(BaseModel):
    text: str
    status: str  # "ready" | "processing"
    snippets: int


def _run_ocr_for_doc(user_id: str, doc) -> tuple[str, int]:
    """Run OCR on a document and return (text, blocks). Best-effort.

    Re-renders PDFs to JPG first, destroys any cached derivative so the OCR
    add-on actually runs on the upload, then extracts the text annotation.
    """
    is_pdf = (doc.format or "").lower() == "pdf"
    if is_pdf:
        source_url, _ = cloudinary.utils.cloudinary_url(
            doc.public_id, resource_type="image", secure=True, format="jpg",
            page=1, transformation=[{"width": 2000, "crop": "limit"}],
        )
    else:
        source_url, _ = cloudinary.utils.cloudinary_url(
            doc.public_id, resource_type="image", secure=True,
        )
    derivative_id = f"sage/users/{user_id}/_pages/{doc.id}_ocr"
    try:
        cloudinary.uploader.destroy(
            derivative_id, resource_type="image", invalidate=True
        )
    except Exception:
        pass
    result = cloudinary.uploader.upload(
        source_url, public_id=derivative_id, resource_type="image",
        ocr="adv_ocr",
    )
    return _extract_ocr_text(result)


def _extract_ocr_text(result: dict) -> tuple[str, int]:
    info = (result or {}).get("info", {}) or {}
    ocr_block = info.get("ocr", {}) or {}
    adv = ocr_block.get("adv_ocr", {}) or {}
    data = adv.get("data") or []
    full_text = ""
    if data:
        annotation = data[0].get("fullTextAnnotation") or {}
        full_text = annotation.get("text", "") or ""
    return full_text, len(data)


@router.post("/{doc_id}/ocr", response_model=OcrResponse)
def ocr_extract(
    doc_id: str,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    """Run OCR on a document via the OCR Text Detection add-on.

    For PDFs, the source asset doesn't expose text to the OCR add-on, so we
    upload page 1 as a JPG derivative image and OCR that. For image uploads,
    we OCR the asset in place via explicit().

    Requires the OCR Text Detection and Extraction add-on to be enabled.
    """
    _ensure_configured()
    doc = session.get(Document, doc_id)
    if not doc or doc.user_id != user.id:
        raise HTTPException(status_code=404, detail="Document not found")
    if doc.resource_type != "image":
        raise HTTPException(status_code=400, detail="OCR is image/PDF only")

    try:
        text, blocks = _run_ocr_for_doc(user.id, doc)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"OCR add-on error: {e}")

    # Cache for future searches.
    if text and text != doc.content_text:
        doc.content_text = text
        session.add(doc)
        session.commit()

    return OcrResponse(text=text, blocks=blocks)


@router.post("/{doc_id}/transcribe", response_model=TranscriptResponse)
def transcribe_video(
    doc_id: str,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    """Kick off Google AI Video Transcription on a video and return the text.

    Cloudinary processes transcription asynchronously and writes a `.transcript`
    JSON file alongside the original video. We fire the conversion if it
    hasn't run yet, then attempt to fetch the transcript file. If processing
    is still in flight the response is `status: processing` and the user can
    click again in a few seconds.
    """
    _ensure_configured()
    doc = session.get(Document, doc_id)
    if not doc or doc.user_id != user.id:
        raise HTTPException(status_code=404, detail="Document not found")
    if doc.resource_type != "video":
        raise HTTPException(status_code=400, detail="Transcription is video-only")

    # Trigger google_speech on the asset (idempotent — Cloudinary skips if
    # the transcript already exists).
    try:
        cloudinary.uploader.explicit(
            doc.public_id,
            type="upload",
            resource_type="video",
            raw_convert="google_speech",
        )
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Transcription error: {e}")

    # Try to fetch the transcript JSON file. If 404 it's still processing.
    transcript_url, _ = cloudinary.utils.cloudinary_url(
        f"{doc.public_id}.transcript",
        resource_type="raw",
        secure=True,
    )
    import urllib.request
    try:
        with urllib.request.urlopen(transcript_url, timeout=10) as resp:
            data = resp.read().decode("utf-8", errors="replace")
        parsed = json.loads(data)
    except Exception:
        return TranscriptResponse(text="", status="processing", snippets=0)

    # Cloudinary's transcript JSON is a list of snippet objects with
    # `transcript` and timing fields. Some accounts wrap them under a
    # top-level key; handle both shapes.
    snippets_list = parsed if isinstance(parsed, list) else parsed.get("snippets", [])
    text_parts: list[str] = []
    for s in snippets_list:
        if not isinstance(s, dict):
            continue
        text_parts.append(s.get("transcript") or s.get("text") or "")
    full_text = " ".join(p for p in text_parts if p).strip()

    if full_text and full_text != doc.content_text:
        doc.content_text = full_text
        session.add(doc)
        session.commit()

    return TranscriptResponse(
        text=full_text,
        status="ready" if full_text else "processing",
        snippets=len(snippets_list),
    )


@router.post("/enhance", response_model=EnhanceResponse)
def enhance(
    req: EnhanceRequest,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    """Build a Cloudinary URL with the requested generative effect.

    These transforms only render successfully if your Cloudinary account
    has the corresponding add-on enabled. The URL is returned regardless;
    the browser will see a 402/4xx if the add-on is off.
    """
    _ensure_configured()
    doc = session.get(Document, req.document_id)
    if not doc or doc.user_id != user.id:
        raise HTTPException(status_code=404, detail="Document not found")
    if doc.resource_type != "image":
        raise HTTPException(status_code=400, detail="Enhancement is image-only")

    # Effect strings map to specific Cloudinary add-ons. The exact add-on name
    # in your account dashboard must be enabled, otherwise the URL 4xx's.
    if req.op == "bg_remove":
        # "Pixelz - Remove the Background" add-on uses e_bgremoval (NOT
        # e_background_removal — that's a different, separate add-on).
        effect = "e_bgremoval"
    elif req.op == "auto_enhance":
        # "VIESUS Image Enhancement" add-on
        effect = "e_viesus_correct"
    elif req.op == "upscale":
        # Generative Upscale add-on (only fires if Generative AI add-on enabled)
        effect = "e_upscale"
    elif req.op == "gen_remove":
        # Generative Remove — needs a prompt of the object to remove
        prompt = _safe_prompt(req.prompt or "background")
        effect = f"e_gen_remove:prompt_({prompt})"
    elif req.op == "gen_fill":
        # Outpainting: extend the canvas, then b_gen_fill paints the new pixels.
        # Without a prompt the model fills with a natural extension; with one
        # it follows the description.
        prompt = _safe_prompt(req.prompt or "")
        fill = "b_gen_fill" if not prompt else f"b_gen_fill:prompt_({prompt})"
        effect = f"ar_4:3,c_pad,{fill}"
    elif req.op == "gen_recolor":
        # Recolor uses to-color (hyphen) and the prompt in parens.
        prompt = _safe_prompt(req.prompt or "ink")
        effect = f"e_gen_recolor:prompt_({prompt});to-color_000000"
    else:
        raise HTTPException(status_code=400, detail="Unknown op")

    # PDFs need a materialized JPG derivative — chained transforms aren't
    # enough because add-ons read the source asset, not the chained pixels.
    try:
        source_pid = _ensure_image_source(user.id, doc)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Failed to render page: {e}")

    base, _ = cloudinary.utils.cloudinary_url(
        source_pid,
        resource_type="image",
        secure=True,
        sign_url=True,
        format="jpg",
        transformation=[
            {"raw_transformation": effect},
            {"raw_transformation": _watermark_transform(doc.category)},
        ],
    )
    # Cache-buster — the URL signature is identical for the same op+doc, so a
    # browser that previously got a 4xx (e.g. before the add-on was enabled)
    # would keep serving the cached failure. A querystring forces a refetch
    # without invalidating Cloudinary's CDN cache.
    base = f"{base}?_={int(time.time())}"
    return EnhanceResponse(url=base, enabled=True, note=None)


# ───────────── helpers ─────────────


def _to_out(doc: Document) -> DocumentOut:
    if doc.resource_type == "video":
        preview = _video_poster_url(doc.public_id, doc.category)
        streaming = _video_url(doc.public_id, doc.category)
        download, _ = cloudinary.utils.cloudinary_url(doc.public_id, resource_type="video", secure=True)
    elif doc.resource_type == "image":
        is_pdf = (doc.format or "").lower() == "pdf"
        preview = _image_url(doc.public_id, doc.category, is_pdf=is_pdf)
        streaming = None
        download, _ = cloudinary.utils.cloudinary_url(doc.public_id, resource_type="image", secure=True)
    else:
        # raw — usually PDFs are uploaded as resource_type=image so multi-page transforms work.
        preview = _raw_url(doc.public_id)
        streaming = None
        download = preview

    tags: List[str] = []
    if doc.tags_json:
        try:
            tags = json.loads(doc.tags_json)
        except Exception:
            tags = []

    return DocumentOut(
        id=doc.id,
        public_id=doc.public_id,
        resource_type=doc.resource_type,
        format=doc.format,
        bytes=doc.bytes,
        pages=doc.pages,
        duration=doc.duration,
        category=doc.category,
        original_filename=doc.original_filename,
        tags=tags,
        preview_url=preview,
        download_url=download,
        streaming_url=streaming,
    )
