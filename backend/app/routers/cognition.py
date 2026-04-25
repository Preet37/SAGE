"""Cognition track endpoints: semantic memory + ad-hoc verification.

These power the agent-augmentation surface in the SAGE UI:
- /cognition/memory          GET  — list a user's stored memories
- /cognition/memory/recall   POST — query memory with a free-text question
- /cognition/memory/{id}     DELETE — drop a memory
- /cognition/verify          POST — verify an arbitrary claim against a lesson's KB
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlmodel import Session, select

from ..config import get_settings
from ..db import get_session
from ..deps import get_current_user
from ..models.learning import Lesson
from ..models.memory import MemoryRecord
from ..models.user import User
from ..agent.verifier import verify_response
from ..services.semantic_memory import recall_memories

router = APIRouter(prefix="/cognition", tags=["cognition"])


class MemoryItem(BaseModel):
    id: str
    role: str
    content: str
    lesson_id: Optional[str] = None
    session_id: Optional[str] = None
    importance: float
    created_at: datetime


class MemoryListResponse(BaseModel):
    items: list[MemoryItem]
    enabled: bool


class RecallRequest(BaseModel):
    query: str
    k: int = 5
    lesson_id: Optional[str] = None
    same_lesson_only: bool = False


class RecallHit(BaseModel):
    id: str
    role: str
    content: str
    lesson_id: Optional[str] = None
    session_id: Optional[str] = None
    score: float
    created_at: Optional[str] = None


class RecallResponse(BaseModel):
    hits: list[RecallHit]


class VerifyRequest(BaseModel):
    claim: str
    lesson_id: str


class VerifyResponse(BaseModel):
    score: float
    label: str
    grounded_claims: list[str]
    unsupported_claims: list[str]
    rationale: str


@router.get("/memory", response_model=MemoryListResponse)
def list_memory(
    lesson_id: Optional[str] = Query(default=None),
    limit: int = Query(default=50, le=200),
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
) -> MemoryListResponse:
    settings = get_settings()
    stmt = select(MemoryRecord).where(MemoryRecord.user_id == user.id)
    if lesson_id:
        stmt = stmt.where(MemoryRecord.lesson_id == lesson_id)
    stmt = stmt.order_by(MemoryRecord.created_at.desc()).limit(limit)
    rows = list(session.exec(stmt))
    return MemoryListResponse(
        enabled=settings.feature_semantic_memory,
        items=[
            MemoryItem(
                id=r.id, role=r.role, content=r.content,
                lesson_id=r.lesson_id, session_id=r.session_id,
                importance=r.importance, created_at=r.created_at,
            ) for r in rows
        ],
    )


@router.post("/memory/recall", response_model=RecallResponse)
def recall(
    req: RecallRequest,
    user: User = Depends(get_current_user),
) -> RecallResponse:
    if not req.query.strip():
        return RecallResponse(hits=[])
    hits = recall_memories(
        user_id=user.id,
        query=req.query,
        k=max(1, min(20, req.k)),
        lesson_id=req.lesson_id,
        same_lesson_only=req.same_lesson_only,
    )
    return RecallResponse(hits=[RecallHit(**h) for h in hits])


@router.delete("/memory/{memory_id}")
def delete_memory(
    memory_id: str,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
) -> dict:
    record = session.get(MemoryRecord, memory_id)
    if not record or record.user_id != user.id:
        raise HTTPException(status_code=404, detail="Memory not found")
    session.delete(record)
    session.commit()
    return {"ok": True}


@router.delete("/memory")
def clear_memory(
    lesson_id: Optional[str] = Query(default=None),
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
) -> dict:
    stmt = select(MemoryRecord).where(MemoryRecord.user_id == user.id)
    if lesson_id:
        stmt = stmt.where(MemoryRecord.lesson_id == lesson_id)
    rows = list(session.exec(stmt))
    for r in rows:
        session.delete(r)
    session.commit()
    return {"ok": True, "deleted": len(rows)}


@router.post("/verify", response_model=VerifyResponse)
async def verify(
    req: VerifyRequest,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
) -> VerifyResponse:
    settings = get_settings()
    if not settings.feature_verification:
        raise HTTPException(status_code=400, detail="Verification feature disabled")
    lesson = session.get(Lesson, req.lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    result = await verify_response(
        req.claim,
        lesson.title or "",
        lesson.content or "",
        lesson.reference_kb or "",
    )
    if result is None:
        raise HTTPException(status_code=502, detail="Verifier unavailable")
    return VerifyResponse(**result.to_dict())
