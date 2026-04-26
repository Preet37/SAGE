"""Learner profile — durable personalization signals for the tutor.

Distinct from semantic memory (`MemoryRecord`), which retrieves specific past
turns. This is a small structured record the learner edits explicitly: their
self-described expertise level, preferred explanation style, interests, and
goals. The agent loop folds a short summary into the system prompt so the
tutor adapts even on the first turn of a new session.
"""

from datetime import datetime

from sqlmodel import Field, SQLModel


class LearnerProfile(SQLModel, table=True):
    __tablename__ = "learnerprofile"

    # One profile per user — user_id is both PK and FK.
    user_id: str = Field(foreign_key="user.id", primary_key=True)
    # Free-form values, but the UI offers a fixed list:
    #   beginner | intermediate | advanced | unspecified
    expertise_level: str = "unspecified"
    # default | eli5 | analogy | code | deep_dive
    preferred_style: str = "default"
    # JSON array of short tags (e.g. ["transformers", "rl", "systems"]).
    interests: str = "[]"
    # Free-text goal statement ("I'm preparing for a graduate ML class").
    goals: str = ""
    updated_at: datetime = Field(default_factory=datetime.utcnow)
