from datetime import datetime
from typing import Any

from sqlalchemy import JSON, Boolean, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class TutorMessage(Base):
    """One persisted turn in a session, with verification + agent trace.

    `agent_trace` mirrors the orchestrator output (plan, retrieved chunks
    summary, concept_map_delta, assessment, peers, progress_delta) so the
    replay UI can reconstruct what every agent decided.
    """

    __tablename__ = "tutor_messages"

    id: Mapped[int] = mapped_column(primary_key=True)
    session_id: Mapped[int] = mapped_column(
        ForeignKey("tutor_sessions.id"), index=True
    )
    role: Mapped[str] = mapped_column(String(16))  # "user" | "assistant"
    content: Mapped[str] = mapped_column(Text, default="")
    verification_passed: Mapped[bool] = mapped_column(Boolean, default=True)
    verification_score: Mapped[float] = mapped_column(default=1.0)
    verification_flags: Mapped[list[Any]] = mapped_column(JSON, default=list)
    agent_trace: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    retrieved_chunks: Mapped[list[Any]] = mapped_column(JSON, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    session: Mapped["Session"] = relationship()  # noqa: F821
