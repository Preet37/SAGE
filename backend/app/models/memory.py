"""Persistent semantic memory for the tutor — stores significant turns and
retrieves them across sessions via TF-IDF cosine similarity (pure stdlib).
"""

from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field
from cuid2 import cuid_wrapper

cuid = cuid_wrapper()


class MemoryRecord(SQLModel, table=True):
    __tablename__ = "memoryrecord"

    id: str = Field(default_factory=cuid, primary_key=True)
    user_id: str = Field(foreign_key="user.id", index=True)
    lesson_id: Optional[str] = Field(default=None, foreign_key="lesson.id", index=True)
    session_id: Optional[str] = Field(default=None, index=True)
    role: str                           # "user" | "assistant" | "summary"
    content: str
    tokens: str = ""                    # space-separated lowercase tokens for retrieval
    importance: float = 0.5             # 0–1 — used to prune low-value memories
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
