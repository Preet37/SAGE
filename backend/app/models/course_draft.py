from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field
from cuid2 import cuid_wrapper

cuid = cuid_wrapper()


class CourseDraft(SQLModel, table=True):
    __tablename__ = "coursedraft"

    id: str = Field(default_factory=cuid, primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    title: str
    slug: str
    source_type: str = "prompt"
    phase: str = "research"
    stage: str = "generate_outline"
    data: str = "{}"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
