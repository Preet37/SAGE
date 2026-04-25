from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field
from cuid2 import cuid_wrapper

cuid = cuid_wrapper()


class SkillAssessment(SQLModel, table=True):
    __tablename__ = "skillassessment"

    id: str = Field(default_factory=cuid, primary_key=True)
    user_id: str = Field(foreign_key="user.id", index=True)
    background_text: str = ""
    overall_level: str = "beginner"
    overall_summary: str = ""
    skill_dimensions: str = "[]"  # JSON array of {name, level, score, max_score, description}
    strengths: str = "[]"  # JSON array of strings
    gaps: str = "[]"  # JSON array of strings
    recommended_module_id: Optional[str] = Field(default=None, foreign_key="module.id")
    recommendation_text: str = ""
    created_at: datetime = Field(default_factory=datetime.utcnow)
