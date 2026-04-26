"""Models for the Cloudinary track: persisted media assets uploaded by users."""

from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field
from cuid2 import cuid_wrapper

cuid = cuid_wrapper()


class MediaAsset(SQLModel, table=True):
    __tablename__ = "mediaasset"

    id: str = Field(default_factory=cuid, primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    lesson_id: Optional[str] = Field(default=None, foreign_key="lesson.id", index=True)
    public_id: str                     # Cloudinary public_id
    secure_url: str                    # Direct CDN URL
    resource_type: str = "image"       # "image" | "video" | "raw"
    format: str = ""
    width: int = 0
    height: int = 0
    bytes: int = 0
    folder: str = ""
    kind: str = "upload"               # "upload" | "sketch" | "thumbnail" | "annotation"
    asset_meta: Optional[str] = None   # JSON: tags, AI-derived attributes, parent_id, etc.
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
