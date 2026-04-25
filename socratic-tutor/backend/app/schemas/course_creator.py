from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel


class CreateDraftRequest(BaseModel):
    title: str
    source_type: str = "prompt"
    source_text: str = ""
    source_url: Optional[str] = None


class UpdateOutlineRequest(BaseModel):
    outline: dict


class UpdateContentRequest(BaseModel):
    lessons: List[dict]


class UpdateCleanupRequest(BaseModel):
    lessons: List[dict]


class UpdateReferenceKbDraftsRequest(BaseModel):
    reference_kb_drafts: dict


class UpdateQARequest(BaseModel):
    approved: List[dict]
    rejected: List[dict]


class ChatMessage(BaseModel):
    role: str
    content: str


class DraftChatRequest(BaseModel):
    message: str
    history: List[ChatMessage] = []


class DraftSummaryResponse(BaseModel):
    id: str
    title: str
    slug: str
    source_type: str
    phase: str
    stage: str
    created_at: datetime
    updated_at: datetime


class DraftDetailResponse(BaseModel):
    id: str
    title: str
    slug: str
    source_type: str
    phase: str
    stage: str
    data: dict
    created_at: datetime
    updated_at: datetime
