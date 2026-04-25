from datetime import datetime
from typing import Optional
from sqlalchemy import String, DateTime, Boolean, JSON
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    username: Mapped[str] = mapped_column(String, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String)
    display_name: Mapped[str] = mapped_column(String, default="")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    preferred_language: Mapped[str] = mapped_column(String, default="en")
    teaching_mode: Mapped[str] = mapped_column(String, default="default")
    accessibility_profile: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    subscription_tier: Mapped[str] = mapped_column(String, default="free")  # free | pro | expert
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
