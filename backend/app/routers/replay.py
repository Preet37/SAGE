"""Session replay API — Cognition track. Every agent decision logged and replayable."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import Optional
from app.database import get_db
from app.models.user import User
from app.models.session import TutorSession, TutorMessage
from app.routers.auth import get_current_user

router = APIRouter(prefix="/replay", tags=["replay"])


@router.get("/sessions")
async def list_sessions(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(TutorSession).where(TutorSession.user_id == user.id).order_by(TutorSession.started_at.desc())
    )
    sessions = result.scalars().all()
    return [
        {
            "id": s.id,
            "lesson_id": s.lesson_id,
            "teaching_mode": s.teaching_mode,
            "started_at": s.started_at.isoformat(),
            "ended_at": s.ended_at.isoformat() if s.ended_at else None,
        }
        for s in sessions
    ]


@router.get("/sessions/{session_id}")
async def get_session_replay(
    session_id: int,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Full session replay with agent decisions at each turn."""
    session_result = await db.execute(
        select(TutorSession).where(
            TutorSession.id == session_id,
            TutorSession.user_id == user.id,
        )
    )
    session = session_result.scalar_one_or_none()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    messages_result = await db.execute(
        select(TutorMessage)
        .where(TutorMessage.session_id == session_id)
        .order_by(TutorMessage.created_at)
    )
    messages = messages_result.scalars().all()

    turns = []
    for msg in messages:
        turns.append({
            "role": msg.role,
            "content": msg.content,
            "created_at": msg.created_at.isoformat(),
            "agent_trace": msg.agent_trace,
            "verification": {
                "passed": msg.verification_passed,
                "flags": msg.verification_flags,
            },
            "retrieved_chunks_preview": msg.retrieved_chunks[:2] if msg.retrieved_chunks else [],
        })

    return {
        "session_id": session_id,
        "teaching_mode": session.teaching_mode,
        "started_at": session.started_at.isoformat(),
        "turns": turns,
        "agent_decisions": session.agent_decisions,
    }
