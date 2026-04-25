"""
Cloudinary media router — signed uploads, OCR ingestion, diagram fetching.
Track 4: Cloudinary.
"""
import logging
import os
from datetime import datetime

import cloudinary
import cloudinary.api
import cloudinary.uploader
import cloudinary.utils
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.routers.auth import get_current_user
from app.models.user import User

log = logging.getLogger("sage.media")
router = APIRouter(prefix="/media", tags=["media"])

cloudinary.config(
    cloud_name=os.environ.get("CLOUDINARY_CLOUD_NAME", ""),
    api_key=os.environ.get("CLOUDINARY_API_KEY", ""),
    api_secret=os.environ.get("CLOUDINARY_API_SECRET", ""),
    secure=True,
)


class SignedUploadResponse(BaseModel):
    signature: str
    timestamp: int
    cloud_name: str
    api_key: str
    folder: str


class OcrIngestionRequest(BaseModel):
    image_url: str
    public_id: str = ""
    lesson_id: int = 0
    extracted_text: str = ""


class DiagramResponse(BaseModel):
    url: str
    public_id: str
    format: str


@router.get("/upload-signed")
async def get_signed_upload_params(
    lesson_id: int = 0,
    user: User = Depends(get_current_user),
) -> SignedUploadResponse:
    """Generate signed upload parameters for direct browser→Cloudinary upload."""
    folder = f"sage/lessons/{lesson_id}/user_{user.id}"
    timestamp = int(datetime.utcnow().timestamp())

    params_to_sign = {
        "folder": folder,
        "timestamp": timestamp,
        "eager": "c_crop,g_auto|e_auto_brightness|e_sharpen",
        "eager_async": True,
    }

    signature = cloudinary.utils.api_sign_request(
        params_to_sign,
        os.environ.get("CLOUDINARY_API_SECRET", ""),
    )

    return SignedUploadResponse(
        signature=signature,
        timestamp=timestamp,
        cloud_name=os.environ.get("CLOUDINARY_CLOUD_NAME", ""),
        api_key=os.environ.get("CLOUDINARY_API_KEY", ""),
        folder=folder,
    )


@router.post("/ocr")
async def ingest_ocr_result(
    req: OcrIngestionRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """
    Try Cloudinary adv_ocr on the uploaded image.
    Falls back gracefully if the OCR add-on is not enabled.
    """
    extracted_text = req.extracted_text

    if not extracted_text and req.public_id:
        try:
            result = cloudinary.api.resource(
                req.public_id,
                ocr="adv_ocr",
            )
            ocr_data = result.get("info", {}).get("ocr", {}).get("adv_ocr", {})
            text_blocks = ocr_data.get("data", [{}])[0].get("textAnnotations", [])
            if text_blocks:
                extracted_text = text_blocks[0].get("description", "")
        except Exception as e:
            log.debug(f"OCR addon unavailable: {e}")

    log.info(f"OCR result: url={req.image_url}, chars={len(extracted_text)}")
    return {
        "status": "ok",
        "extracted_text": extracted_text,
        "extracted_chars": len(extracted_text),
    }


@router.get("/materials/{lesson_id}")
async def get_lesson_materials(
    lesson_id: int,
    user: User = Depends(get_current_user),
) -> dict:
    """Fetch all media uploaded for this lesson by this user from Cloudinary."""
    folder = f"sage/lessons/{lesson_id}/user_{user.id}"
    try:
        result = cloudinary.api.resources(
            type="upload",
            prefix=folder,
            max_results=50,
            resource_type="image",
        )
        resources = result.get("resources", [])
        return {
            "materials": [
                {
                    "public_id": r["public_id"],
                    "secure_url": r["secure_url"],
                    "format": r.get("format", ""),
                    "created_at": r.get("created_at", ""),
                    "bytes": r.get("bytes", 0),
                    "width": r.get("width"),
                    "height": r.get("height"),
                }
                for r in resources
            ]
        }
    except Exception as e:
        log.warning(f"Cloudinary materials fetch failed: {e}")
        return {"materials": []}


@router.get("/diagram/{course_id}/{lesson_id}/{concept_slug}")
async def get_lesson_diagram(
    course_id: int,
    lesson_id: int,
    concept_slug: str,
    width: int = 800,
    user: User = Depends(get_current_user),
) -> DiagramResponse:
    """Fetch a pre-uploaded lesson diagram from Cloudinary with responsive transform."""
    public_id = f"sage/courses/{course_id}/{lesson_id}/{concept_slug}"
    try:
        url = cloudinary.utils.cloudinary_url(
            public_id,
            width=width,
            crop="scale",
            format="auto",
            quality="auto:good",
            fetch_format="auto",
        )[0]
        return DiagramResponse(url=url, public_id=public_id, format="auto")
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Diagram not found: {e}")
