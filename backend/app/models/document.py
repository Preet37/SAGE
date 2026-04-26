from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field
from cuid2 import cuid_wrapper

cuid = cuid_wrapper()


class Document(SQLModel, table=True):
    id: str = Field(default_factory=cuid, primary_key=True)
    user_id: str = Field(index=True, foreign_key="user.id")
    public_id: str = Field(index=True)
    resource_type: str  # "image" | "video" | "raw"
    format: Optional[str] = None
    bytes: int = 0
    pages: Optional[int] = None
    duration: Optional[float] = None
    category: str = "Notes"  # "Notes" | "Textbook" | "Exam" | "Lecture"
    original_filename: str
    # JSON-encoded list of AI-generated tags (Imagga / Google / Cloudinary AI
    # Vision). Populated by Cloudinary at upload time when auto_tagging is set.
    tags_json: Optional[str] = None
    # Text extracted from the asset (OCR for images/PDFs, transcripts for
    # videos). Searched alongside filename + tags for content-based discovery.
    content_text: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
