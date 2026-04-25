from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from ..db import get_session
from ..deps import get_current_user
from ..models.user import User
from ..models.progress import UserLessonProgress, ChatMessage, TutorSession
from ..models.learning import Lesson
from ..schemas.progress import (
    ProgressResponse, MarkCompleteRequest, ChatMessageResponse, TutorSessionResponse,
)

router = APIRouter(prefix="/progress", tags=["progress"])


@router.get("", response_model=List[ProgressResponse])
def get_all_progress(
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    rows = session.exec(
        select(UserLessonProgress).where(UserLessonProgress.user_id == user.id)
    ).all()
    return [
        ProgressResponse(
            lesson_id=r.lesson_id,
            completed=r.completed,
            completed_at=r.completed_at,
        )
        for r in rows
    ]


@router.get("/chat-history/{lesson_id}", response_model=List[ChatMessageResponse])
def get_chat_history(
    lesson_id: str,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    """Return messages from the latest tutor session, or legacy messages with no session."""
    latest = session.exec(
        select(TutorSession)
        .where(TutorSession.user_id == user.id, TutorSession.lesson_id == lesson_id)
        .order_by(TutorSession.updated_at.desc())
    ).first()

    if latest:
        messages = session.exec(
            select(ChatMessage)
            .where(ChatMessage.session_id == latest.id)
            .order_by(ChatMessage.created_at)
        ).all()
    else:
        messages = session.exec(
            select(ChatMessage)
            .where(
                ChatMessage.user_id == user.id,
                ChatMessage.lesson_id == lesson_id,
                ChatMessage.session_id == None,  # noqa: E711
            )
            .order_by(ChatMessage.created_at)
        ).all()

    return [
        ChatMessageResponse(id=m.id, role=m.role, content=m.content, created_at=m.created_at, message_meta=m.message_meta)
        for m in messages
    ]


@router.get("/sessions/{lesson_id}", response_model=List[TutorSessionResponse])
def list_tutor_sessions(
    lesson_id: str,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    sessions = session.exec(
        select(TutorSession)
        .where(TutorSession.user_id == user.id, TutorSession.lesson_id == lesson_id)
        .order_by(TutorSession.updated_at.desc())
    ).all()
    return sessions


@router.get("/sessions/{lesson_id}/{session_id}/history", response_model=List[ChatMessageResponse])
def get_session_history(
    lesson_id: str,
    session_id: str,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    tutor_session = session.get(TutorSession, session_id)
    if not tutor_session or tutor_session.user_id != user.id or tutor_session.lesson_id != lesson_id:
        raise HTTPException(status_code=404, detail="Session not found")

    messages = session.exec(
        select(ChatMessage)
        .where(ChatMessage.session_id == session_id)
        .order_by(ChatMessage.created_at)
    ).all()
    return [
        ChatMessageResponse(id=m.id, role=m.role, content=m.content, created_at=m.created_at, message_meta=m.message_meta)
        for m in messages
    ]


@router.delete("/sessions/{lesson_id}/{session_id}")
def delete_tutor_session(
    lesson_id: str,
    session_id: str,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    tutor_session = session.get(TutorSession, session_id)
    if not tutor_session or tutor_session.user_id != user.id or tutor_session.lesson_id != lesson_id:
        raise HTTPException(status_code=404, detail="Session not found")

    messages = session.exec(
        select(ChatMessage).where(ChatMessage.session_id == session_id)
    ).all()
    for m in messages:
        session.delete(m)
    session.delete(tutor_session)
    session.commit()
    return {"ok": True}


@router.get("/{lesson_id}", response_model=ProgressResponse)
def get_lesson_progress(
    lesson_id: str,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    row = session.exec(
        select(UserLessonProgress)
        .where(UserLessonProgress.user_id == user.id)
        .where(UserLessonProgress.lesson_id == lesson_id)
    ).first()
    if not row:
        return ProgressResponse(lesson_id=lesson_id, completed=False, completed_at=None)
    return ProgressResponse(lesson_id=row.lesson_id, completed=row.completed, completed_at=row.completed_at)


@router.post("", response_model=ProgressResponse)
def mark_complete(
    req: MarkCompleteRequest,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    lesson = session.get(Lesson, req.lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    row = session.exec(
        select(UserLessonProgress)
        .where(UserLessonProgress.user_id == user.id)
        .where(UserLessonProgress.lesson_id == req.lesson_id)
    ).first()

    if row:
        row.completed = True
        row.completed_at = datetime.utcnow()
    else:
        row = UserLessonProgress(
            user_id=user.id,
            lesson_id=req.lesson_id,
            completed=True,
            completed_at=datetime.utcnow(),
        )
        session.add(row)

    session.commit()
    session.refresh(row)
    return ProgressResponse(lesson_id=row.lesson_id, completed=row.completed, completed_at=row.completed_at)
