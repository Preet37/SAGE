from sqlalchemy import Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class Concept(Base):
    __tablename__ = "concepts"

    id: Mapped[int] = mapped_column(primary_key=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("tutor_sessions.id"), index=True)
    label: Mapped[str] = mapped_column(String(200))
    summary: Mapped[str] = mapped_column(Text, default="")
    mastery: Mapped[float] = mapped_column(Float, default=0.0)
    parent_id: Mapped[int | None] = mapped_column(ForeignKey("concepts.id"), nullable=True)

    session: Mapped["Session"] = relationship(back_populates="concepts")  # noqa: F821
