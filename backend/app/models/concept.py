from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field
from cuid2 import cuid_wrapper

cuid = cuid_wrapper()


class ConceptPage(SQLModel, table=True):
    __tablename__ = "conceptpage"

    id: str = Field(default_factory=cuid, primary_key=True)
    topic: str = Field(index=True)
    level: str = "intermediate"
    simple_definition: str = ""
    why_it_matters: str = ""
    detailed_explanation: str = ""
    analogy: str = ""
    real_world_example: str = ""
    misconceptions: str = "[]"  # JSON array of {text, is_correct}
    key_takeaways: str = "[]"  # JSON array of strings
    related_concepts: str = "[]"  # JSON array of strings
    further_reading: str = "[]"  # JSON array of strings
    # Rich enrichment data added in v2 — stored as a single JSON blob for migration safety
    extra_data: Optional[str] = Field(default="{}")
    lesson_id: Optional[str] = Field(default=None, foreign_key="lesson.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
