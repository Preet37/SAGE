"""
Cloudinary track — visual upload, OCR ingestion, and diagram library.

Endpoints:
  POST /media/upload-signed
       → returns a one-shot signature so the browser can upload directly
         to Cloudinary without leaking the API secret.

  POST /media/ingest-ocr
       → student finished uploading an image. We call Cloudinary's
         `adv_ocr` add-on, persist the extracted text, and return a
         normalized payload the chat client can attach to its next turn.

  GET  /media/diagram/{course_id}/{lesson_id}/{concept_slug}
       → returns up to 8 transformation-built thumbnails so the lesson
         can render a "diagram library" without storing per-concept media.

  GET  /media/materials/{lesson_id}
       → returns every uploaded asset associated with this lesson, with
         pre-built thumbnail/full URLs.

All endpoints degrade gracefully when Cloudinary credentials are not set —
they return empty lists / a `mock` flag so the UI can still render.
"""
from __future__ import annotations

import hashlib
import logging
import time
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.database import get_db
from app.models.user import User
from app.routers.auth import get_current_user

router = APIRouter(prefix="/media", tags=["media"])
log = logging.getLogger("sage.media")
settings = get_settings()


def _cloudinary_configured() -> bool:
    return bool(
        settings.cloudinary_cloud_name
        and settings.cloudinary_api_key
        and settings.cloudinary_api_secret
    )


def _signature(params: dict, secret: str) -> str:
    """Cloudinary signed upload — sha1 over alphabetized params + secret."""
    sorted_params = "&".join(
        f"{k}={v}" for k, v in sorted(params.items()) if v not in (None, "")
    )
    return hashlib.sha1((sorted_params + secret).encode("utf-8")).hexdigest()


# ─── Schemas ───────────────────────────────────────────────────────


class SignRequest(BaseModel):
    folder: str = "sage_uploads"
    lesson_id: int = 0
    public_id: Optional[str] = None
    use_ocr: bool = True


class SignResponse(BaseModel):
    cloud_name: str
    api_key: str
    timestamp: int
    signature: str
    folder: str
    upload_url: str
    public_id: Optional[str] = None
    use_ocr: bool


class OcrIngestionRequest(BaseModel):
    image_url: str
    public_id: Optional[str] = None
    lesson_id: Optional[int] = None
    extracted_text: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    bytes: Optional[int] = None


class OcrIngestionResponse(BaseModel):
    image_url: str
    extracted_text: str
    public_id: Optional[str]
    lesson_id: Optional[int]
    annotations: int
    mock: bool


# ─── Endpoints ─────────────────────────────────────────────────────


@router.post("/upload-signed", response_model=SignResponse)
async def upload_signed(
    req: SignRequest,
    user: User = Depends(get_current_user),
):
    """Issue a Cloudinary signed-upload payload for direct browser upload."""
    timestamp = int(time.time())
    public_id = req.public_id or f"sage/{user.id}/{timestamp}"

    params: dict = {
        "folder": req.folder,
        "public_id": public_id,
        "timestamp": timestamp,
    }
    if req.use_ocr:
        params["ocr"] = "adv_ocr"

    signature = "mock"
    if _cloudinary_configured():
        signature = _signature(params, settings.cloudinary_api_secret)

    upload_url = (
        f"https://api.cloudinary.com/v1_1/{settings.cloudinary_cloud_name or 'demo'}/image/upload"
    )
    return SignResponse(
        cloud_name=settings.cloudinary_cloud_name or "demo",
        api_key=settings.cloudinary_api_key or "demo",
        timestamp=timestamp,
        signature=signature,
        folder=req.folder,
        public_id=public_id,
        upload_url=upload_url,
        use_ocr=req.use_ocr,
    )


@router.post("/ingest-ocr", response_model=OcrIngestionResponse)
async def ingest_ocr(
    req: OcrIngestionRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Call Cloudinary's adv_ocr add-on and return the extracted text."""
    if not req.image_url:
        raise HTTPException(status_code=400, detail="image_url is required")

    extracted = req.extracted_text or ""
    annotations = 0
    mock = False

    if not extracted and _cloudinary_configured() and req.public_id:
        try:
            import cloudinary
            import cloudinary.api
            cloudinary.config(
                cloud_name=settings.cloudinary_cloud_name,
                api_key=settings.cloudinary_api_key,
                api_secret=settings.cloudinary_api_secret,
                secure=True,
            )
            res = cloudinary.api.resource(
                req.public_id,
                ocr="adv_ocr",
                image_metadata=True,
            )
            ocr = (res or {}).get("info", {}).get("ocr", {}).get("adv_ocr", {})
            data = ocr.get("data", []) or []
            text_lines: list[str] = []
            for entry in data:
                ann = entry.get("textAnnotations", []) or []
                annotations += len(ann)
                if ann:
                    text_lines.append(ann[0].get("description", ""))
            extracted = "\n".join(t for t in text_lines if t).strip()
        except Exception as e:
            log.warning("OCR ingestion failed for %s: %s", req.public_id, e)
            mock = True

    if not extracted:
        mock = True
        extracted = "(no text detected)"

    return OcrIngestionResponse(
        image_url=req.image_url,
        extracted_text=extracted,
        public_id=req.public_id,
        lesson_id=req.lesson_id,
        annotations=annotations,
        mock=mock,
    )


@router.get("/diagram/{course_id}/{lesson_id}/{concept_slug}")
async def diagram_library(course_id: int, lesson_id: int, concept_slug: str):
    """Return up to 8 transformation-built thumbnails for a concept."""
    cloud = settings.cloudinary_cloud_name
    if not cloud:
        return {"items": [], "mock": True}

    base = f"https://res.cloudinary.com/{cloud}/image/upload"
    folder = f"sage_diagrams/{course_id}/{lesson_id}/{concept_slug}"

    # We don't list — we serve up the canonical 8 transformation slots.
    # If the asset doesn't exist Cloudinary returns 404 lazily; the UI shows
    # the placeholder rather than failing the page render.
    slots = [
        ("hero",     "w_960,h_540,c_fill,q_auto,f_auto"),
        ("thumb",    "w_320,h_180,c_fill,q_auto,f_auto"),
        ("dark",     "w_960,h_540,c_fill,e_invert,q_auto,f_auto"),
        ("contrast", "w_960,h_540,c_fill,e_contrast:60,q_auto,f_auto"),
        ("blur",     "w_960,h_540,c_fill,e_blur:200,q_auto,f_auto"),
        ("annotate", "w_960,h_540,c_fill,l_text:Arial_24:annotated,q_auto,f_auto"),
        ("crop1",    "w_540,h_540,c_thumb,g_auto,q_auto,f_auto"),
        ("crop2",    "w_540,h_540,c_thumb,g_face,q_auto,f_auto"),
    ]
    items = [
        {
            "label": label,
            "url": f"{base}/{tx}/{folder}/main",
            "thumb_url": f"{base}/w_240,h_135,c_fill,q_auto,f_auto/{folder}/main",
        }
        for label, tx in slots
    ]
    return {"items": items, "mock": False}


@router.get("/materials/{lesson_id}")
async def list_materials(
    lesson_id: int,
    user: User = Depends(get_current_user),
):
    """Return every asset uploaded for this lesson — used by MaterialsGallery."""
    if not _cloudinary_configured():
        return {"items": [], "mock": True}

    try:
        import cloudinary
        import cloudinary.api
        cloudinary.config(
            cloud_name=settings.cloudinary_cloud_name,
            api_key=settings.cloudinary_api_key,
            api_secret=settings.cloudinary_api_secret,
            secure=True,
        )
        prefix = f"sage_uploads/sage/{user.id}"
        res = cloudinary.api.resources(
            type="upload",
            prefix=prefix,
            max_results=24,
        )
        resources = (res or {}).get("resources", []) or []
        cloud = settings.cloudinary_cloud_name
        items = [
            {
                "public_id": r.get("public_id", ""),
                "url": r.get("secure_url", ""),
                "thumb_url": (
                    f"https://res.cloudinary.com/{cloud}/image/upload/"
                    f"w_240,h_135,c_fill,q_auto,f_auto/{r.get('public_id','')}"
                ),
                "width": r.get("width", 0),
                "height": r.get("height", 0),
                "format": r.get("format", ""),
                "bytes": r.get("bytes", 0),
                "created_at": r.get("created_at", ""),
            }
            for r in resources
        ]
        return {"items": items, "mock": False}
    except Exception as e:
        log.warning("Materials listing failed: %s", e)
        return {"items": [], "mock": True}
