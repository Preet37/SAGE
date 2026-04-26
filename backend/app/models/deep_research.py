from datetime import datetime
from typing import Optional

from cuid2 import cuid_wrapper
from sqlmodel import Field, SQLModel

cuid = cuid_wrapper()


class ResearchRun(SQLModel, table=True):
    id: str = Field(default_factory=cuid, primary_key=True)
    user_id: str = Field(index=True, foreign_key="users.id")
    topic: str
    status: str = "running"  # running | ready_for_outreach | error | done
    # Snapshot of the live state — JSON-encoded to keep schema simple.
    graph_json: Optional[str] = None
    validation_json: Optional[str] = None
    experts_json: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class OutreachLog(SQLModel, table=True):
    id: str = Field(default_factory=cuid, primary_key=True)
    run_id: str = Field(index=True, foreign_key="researchrun.id")
    expert_id: str
    expert_name: str
    expert_email: str
    subject: str
    body: str
    sent: bool = False
    status_code: Optional[int] = None
    error: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
