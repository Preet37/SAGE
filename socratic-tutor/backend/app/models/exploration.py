from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from cuid2 import cuid_wrapper

cuid = cuid_wrapper()


class ExplorationSession(SQLModel, table=True):
    __tablename__ = "explorationsession"

    id: str = Field(default_factory=cuid, primary_key=True)
    user_id: str = Field(foreign_key="user.id", index=True)
    title: str = "Untitled exploration"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    messages: List["ExplorationMessage"] = Relationship(back_populates="session")


class ExplorationMessage(SQLModel, table=True):
    __tablename__ = "explorationmessage"

    id: str = Field(default_factory=cuid, primary_key=True)
    session_id: str = Field(foreign_key="explorationsession.id", index=True)
    role: str  # "user" | "assistant"
    content: str
    message_meta: Optional[str] = None  # JSON: {tools_used: [...], modalities: [...], ...}
    created_at: datetime = Field(default_factory=datetime.utcnow)

    session: Optional[ExplorationSession] = Relationship(back_populates="messages")
