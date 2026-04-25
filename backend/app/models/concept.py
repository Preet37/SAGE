from datetime import datetime
from typing import Optional
from sqlalchemy import String, Text, DateTime, Integer, JSON, ForeignKey, Float, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class ConceptNode(Base):
    __tablename__ = "concept_nodes"

    id: Mapped[int] = mapped_column(primary_key=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"))
    lesson_id: Mapped[Optional[int]] = mapped_column(ForeignKey("lessons.id"), nullable=True)
    label: Mapped[str] = mapped_column(String, index=True)
    description: Mapped[str] = mapped_column(Text, default="")
    node_type: Mapped[str] = mapped_column(String, default="concept")  # concept | skill | prereq
    x_pos: Mapped[float] = mapped_column(Float, default=0.0)
    y_pos: Mapped[float] = mapped_column(Float, default=0.0)


class ConceptEdge(Base):
    __tablename__ = "concept_edges"

    id: Mapped[int] = mapped_column(primary_key=True)
    source_id: Mapped[int] = mapped_column(ForeignKey("concept_nodes.id"))
    target_id: Mapped[int] = mapped_column(ForeignKey("concept_nodes.id"))
    edge_type: Mapped[str] = mapped_column(String, default="requires")  # requires | extends | relates
    weight: Mapped[float] = mapped_column(Float, default=1.0)


class StudentMastery(Base):
    __tablename__ = "student_mastery"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    concept_id: Mapped[int] = mapped_column(ForeignKey("concept_nodes.id"))
    score: Mapped[float] = mapped_column(Float, default=0.0)  # 0.0 - 1.0
    attempts: Mapped[int] = mapped_column(Integer, default=0)
    last_seen: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    is_mastered: Mapped[bool] = mapped_column(Boolean, default=False)
