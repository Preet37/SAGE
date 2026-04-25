from datetime import datetime
from sqlmodel import SQLModel, Field
from cuid2 import cuid_wrapper

cuid = cuid_wrapper()


class GeneratedCurriculum(SQLModel, table=True):
    __tablename__ = "generatedcurriculum"

    id: str = Field(default_factory=cuid, primary_key=True)
    user_id: str = Field(foreign_key="user.id", index=True)
    learning_goals: str = ""
    title: str = ""
    level_range: str = ""
    estimated_hours: float = 0
    personalization_note: str = ""
    phases: str = "[]"  # JSON array of phase objects
    gaps: str = "[]"  # JSON array of gap objects
    created_at: datetime = Field(default_factory=datetime.utcnow)
