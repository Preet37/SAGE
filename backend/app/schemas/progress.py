from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel


class ProgressResponse(BaseModel):
    lesson_id: str
    completed: bool
    completed_at: Optional[datetime]


class MarkCompleteRequest(BaseModel):
    lesson_id: str


class ChatMessageResponse(BaseModel):
    id: str
    role: str
    content: str
    created_at: datetime
    message_meta: Optional[str] = None


class ChatRequest(BaseModel):
    messages: List[dict]
    lesson_id: str
    mode: str = "default"
    session_id: Optional[str] = None


class TutorSessionResponse(BaseModel):
    id: str
    lesson_id: str
    created_at: datetime
    updated_at: datetime
