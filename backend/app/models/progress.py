from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, UniqueConstraint
from cuid2 import cuid_wrapper

cuid = cuid_wrapper()


class UserLessonProgress(SQLModel, table=True):
    __tablename__ = "userlessonprogress"
    __table_args__ = (UniqueConstraint("user_id", "lesson_id"),)

    id: str = Field(default_factory=cuid, primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    lesson_id: str = Field(foreign_key="lesson.id", index=True)
    completed: bool = False
    completed_at: Optional[datetime] = None


class TutorSession(SQLModel, table=True):
    __tablename__ = "tutorsession"

    id: str = Field(default_factory=cuid, primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    lesson_id: str = Field(foreign_key="lesson.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class ChatMessage(SQLModel, table=True):
    __tablename__ = "chatmessage"

    id: str = Field(default_factory=cuid, primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    lesson_id: str = Field(foreign_key="lesson.id", index=True)
    session_id: Optional[str] = Field(default=None, foreign_key="tutorsession.id", index=True)
    role: str              # "user" | "assistant"
    content: str
    message_meta: Optional[str] = None  # JSON: {tools_used: [...], modalities: [...], ...}
    created_at: datetime = Field(default_factory=datetime.utcnow)
