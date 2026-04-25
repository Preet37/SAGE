"""Cloudinary track — media uploads, AI transforms, and 'sketch-to-concept'.

Surfaces:
- POST /media/sign            — server-signed upload params for direct browser upload
- POST /media/assets          — record a Cloudinary asset for the user/lesson
- GET  /media/assets          — list the user's assets
- DELETE /media/assets/{id}   — remove an asset record
- POST /media/sketch-explain  — given an uploaded sketch, ask the tutor to interpret it
- GET  /media/transform       — proxy that builds a Cloudinary transformation URL
"""

from __future__ import annotations

import hashlib
import hmac
import json
import logging
import time
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select

from ..agent.agent_loop import get_async_client
from ..config import get_settings
from ..db import get_session
from ..deps import get_current_user
from ..models.learning import Lesson
from ..models.media import MediaAsset
from ..models.user import User

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/media", tags=["media"])


# ── Signed upload (browser uploads directly to Cloudinary) ─────

class SignRequest(BaseModel):
    folder: Optional[str] = None
    public_id: Optional[str] = None
    upload_preset: Optional[str] = None
    tags: list[str] = []
    eager: Optional[str] = None


class SignResponse(BaseModel):
    cloud_name: str
    api_key: str
    timestamp: int
    folder: str
    upload_preset: str
    signature: str
    tags: str
    eager: Optional[str] = None


def _sign(params: dict, api_secret: str) -> str:
    """Cloudinary signature: sorted (k=v&...) string + secret, sha1 hex."""
    parts = [f"{k}={v}" for k, v in sorted(params.items()) if v not in (None, "")]
    to_sign = "&".join(parts) + api_secret
    return hashlib.sha1(to_sign.encode()).hexdigest()


@router.post("/sign", response_model=SignResponse)
def sign_upload(
    req: SignRequest,
    user: User = Depends(get_current_user),
) -> SignResponse:
    settings = get_settings()
    if not settings.feature_cloudinary:
        raise HTTPException(status_code=400, detail="Cloudinary feature disabled")
    if not (settings.cloudinary_cloud_name and settings.cloudinary_api_key and settings.cloudinary_api_secret):
        raise HTTPException(
            status_code=400,
            detail="Cloudinary credentials not configured. Set CLOUDINARY_CLOUD_NAME / CLOUDINARY_API_KEY / CLOUDINARY_API_SECRET.",
        )

    folder = (req.folder or f"{settings.cloudinary_folder}/users/{user.id}")[:120]
    upload_preset = req.upload_preset or settings.cloudinary_upload_preset
    tags = ",".join([t for t in req.tags if t][:6])
    timestamp = int(time.time())

    params: dict = {
        "folder": folder,
        "timestamp": timestamp,
        "upload_preset": upload_preset,
    }
    if tags:
        params["tags"] = tags
    if req.public_id:
        params["public_id"] = req.public_id
    if req.eager:
        params["eager"] = req.eager

    signature = _sign(params, settings.cloudinary_api_secret)

    return SignResponse(
        cloud_name=settings.cloudinary_cloud_name,
        api_key=settings.cloudinary_api_key,
        timestamp=timestamp,
        folder=folder,
        upload_preset=upload_preset,
        tags=tags,
        signature=signature,
        eager=req.eager,
    )


# ── Asset bookkeeping ──────────────────────────────────────────

class CloudinaryUploadResult(BaseModel):
    public_id: str
    secure_url: str
    resource_type: str = "image"
    format: str = ""
    width: int = 0
    height: int = 0
    bytes: int = 0
    folder: str = ""
    tags: list[str] = []
    lesson_id: Optional[str] = None
    kind: str = "upload"
    asset_meta: Optional[dict] = None


class AssetOut(BaseModel):
    id: str
    public_id: str
    secure_url: str
    resource_type: str
    format: str
    width: int
    height: int
    bytes: int
    folder: str
    kind: str
    lesson_id: Optional[str]
    asset_meta: Optional[dict]
    created_at: datetime


def _to_out(a: MediaAsset) -> AssetOut:
    meta: Optional[dict] = None
    if a.asset_meta:
        try:
            meta = json.loads(a.asset_meta)
        except json.JSONDecodeError:
            meta = None
    return AssetOut(
        id=a.id, public_id=a.public_id, secure_url=a.secure_url,
        resource_type=a.resource_type, format=a.format,
        width=a.width, height=a.height, bytes=a.bytes, folder=a.folder,
        kind=a.kind, lesson_id=a.lesson_id, asset_meta=meta, created_at=a.created_at,
    )


@router.post("/assets", response_model=AssetOut)
def record_asset(
    req: CloudinaryUploadResult,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
) -> AssetOut:
    asset = MediaAsset(
        user_id=user.id, lesson_id=req.lesson_id,
        public_id=req.public_id, secure_url=req.secure_url,
        resource_type=req.resource_type, format=req.format,
        width=req.width, height=req.height, bytes=req.bytes,
        folder=req.folder, kind=req.kind,
        asset_meta=json.dumps({**(req.asset_meta or {}), "tags": req.tags}) if (req.asset_meta or req.tags) else None,
    )
    session.add(asset)
    session.commit()
    session.refresh(asset)
    return _to_out(asset)


@router.get("/assets", response_model=list[AssetOut])
def list_assets(
    lesson_id: Optional[str] = None,
    kind: Optional[str] = None,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
) -> list[AssetOut]:
    stmt = select(MediaAsset).where(MediaAsset.user_id == user.id)
    if lesson_id:
        stmt = stmt.where(MediaAsset.lesson_id == lesson_id)
    if kind:
        stmt = stmt.where(MediaAsset.kind == kind)
    stmt = stmt.order_by(MediaAsset.created_at.desc()).limit(200)
    rows = list(session.exec(stmt))
    return [_to_out(a) for a in rows]


@router.delete("/assets/{asset_id}")
def delete_asset(
    asset_id: str,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
) -> dict:
    asset = session.get(MediaAsset, asset_id)
    if not asset or asset.user_id != user.id:
        raise HTTPException(status_code=404, detail="Asset not found")
    session.delete(asset)
    session.commit()
    return {"ok": True}


# ── Cloudinary transform helper ────────────────────────────────

class TransformRequest(BaseModel):
    public_id: str
    transformations: list[str]   # e.g. ["c_thumb,w_400,g_auto", "e_background_removal", "f_auto"]
    resource_type: str = "image"


@router.post("/transform")
def build_transform_url(
    req: TransformRequest,
    user: User = Depends(get_current_user),
) -> dict:
    settings = get_settings()
    if not settings.cloudinary_cloud_name:
        raise HTTPException(status_code=400, detail="Cloudinary not configured")
    chain = "/".join(t.strip("/") for t in req.transformations if t.strip())
    base = f"https://res.cloudinary.com/{settings.cloudinary_cloud_name}/{req.resource_type}/upload"
    url = f"{base}/{chain}/{req.public_id}" if chain else f"{base}/{req.public_id}"
    return {"url": url}


# ── Sketch-to-concept (LLM interprets a student-uploaded image) ─

class SketchExplainRequest(BaseModel):
    asset_id: str
    note: Optional[str] = None         # what the student wants to know
    lesson_id: Optional[str] = None    # optional grounding


class SketchExplainResponse(BaseModel):
    explanation: str
    detected_concepts: list[str]
    suggested_prompt: str               # user can hand this to the tutor


_SKETCH_PROMPT = """You are SAGE's sketch interpretation assistant.

A student has uploaded an image (a hand-drawn diagram, equation, or
screenshot of a paper) at the URL below. Their question or note is also
included. Use the URL to open the image (assume the model has
multimodal access; if not, infer from the metadata).

Return STRICT JSON with this shape:

{
  "explanation": "<3–6 sentence explanation of what the image likely shows>",
  "detected_concepts": ["<concept>", "<concept>", ...],
  "suggested_prompt": "<a single follow-up question the student should
    ask the SAGE tutor next, phrased in their voice>"
}

Image URL: {image_url}
Image dimensions: {dims}
Lesson context: {lesson_title}
Student's note: {note}
"""


@router.post("/sketch-explain", response_model=SketchExplainResponse)
async def sketch_explain(
    req: SketchExplainRequest,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
) -> SketchExplainResponse:
    settings = get_settings()
    asset = session.get(MediaAsset, req.asset_id)
    if not asset or asset.user_id != user.id:
        raise HTTPException(status_code=404, detail="Asset not found")
    lesson_title = ""
    if req.lesson_id:
        lesson = session.get(Lesson, req.lesson_id)
        if lesson:
            lesson_title = lesson.title

    prompt = _SKETCH_PROMPT.format(
        image_url=asset.secure_url,
        dims=f"{asset.width}x{asset.height}",
        lesson_title=lesson_title or "(none)",
        note=(req.note or "(no note)")[:300],
    )

    client = get_async_client()
    try:
        completion = await client.chat.completions.create(
            model=settings.vision_llm_model or settings.llm_model,
            messages=[
                {"role": "system", "content": "You output strict JSON only."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=600,
            temperature=0.3,
            stream=False,
        )
        raw = (completion.choices[0].message.content or "").strip()
    except Exception as e:
        logger.warning("Sketch explain failed: %s", e)
        raise HTTPException(status_code=502, detail="LLM call failed")

    # Strip code fences if any.
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        # Best-effort fallback so the user still sees something useful.
        data = {
            "explanation": raw[:800] or "Couldn't parse the model output.",
            "detected_concepts": [],
            "suggested_prompt": "Walk me through this image step by step.",
        }
    return SketchExplainResponse(
        explanation=str(data.get("explanation", ""))[:1500],
        detected_concepts=[str(c)[:80] for c in (data.get("detected_concepts") or [])][:8],
        suggested_prompt=str(data.get("suggested_prompt", "Walk me through this image step by step."))[:300],
    )
