from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel


class ExploreRequest(BaseModel):
    messages: List[dict]
    mode: str = "default"
    session_id: Optional[str] = None


class ExplorationSessionResponse(BaseModel):
    id: str
    title: str
    created_at: datetime
    updated_at: datetime


class ExplorationMessageResponse(BaseModel):
    id: str
    role: str
    content: str
    created_at: datetime
