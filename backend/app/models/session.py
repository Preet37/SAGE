from datetime import datetime
from typing import Optional
from sqlalchemy import String, Text, DateTime, Integer, JSON, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class TutorSession(Base):
    __tablename__ = "tutor_sessions"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    lesson_id: Mapped[int] = mapped_column(ForeignKey("lessons.id"))
    teaching_mode: Mapped[str] = mapped_column(String, default="default")
    started_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    ended_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    agent_decisions: Mapped[list] = mapped_column(JSON, default=list)  # Cognition: session replay

    messages: Mapped[list["TutorMessage"]] = relationship("TutorMessage", back_populates="session")


class TutorMessage(Base):
    __tablename__ = "tutor_messages"

    id: Mapped[int] = mapped_column(primary_key=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("tutor_sessions.id"))
    role: Mapped[str] = mapped_column(String)  # user | assistant
    content: Mapped[str] = mapped_column(Text)
    retrieved_chunks: Mapped[list] = mapped_column(JSON, default=list)
    verification_passed: Mapped[bool] = mapped_column(Boolean, default=True)
    verification_flags: Mapped[list] = mapped_column(JSON, default=list)
    agent_trace: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    session: Mapped["TutorSession"] = relationship("TutorSession", back_populates="messages")


class PeerSession(Base):
    __tablename__ = "peer_sessions"

    id: Mapped[int] = mapped_column(primary_key=True)
    concept_id: Mapped[Optional[int]] = mapped_column(ForeignKey("concept_nodes.id"), nullable=True)
    initiator_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    partner_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True)
    room_token: Mapped[str] = mapped_column(String, unique=True)
    status: Mapped[str] = mapped_column(String, default="waiting")  # waiting | active | ended
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
