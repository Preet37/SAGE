from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session as OrmSession

from app.db import get_db
from app.models import Concept
from app.models import Session as TutorSession
from app.models import TutorMessage, User
from app.schemas import ConceptOut, ReplaySessionOut, SessionOut, TutorMessageOut
from app.security import get_current_user

router = APIRouter(prefix="/replay", tags=["replay"])


@router.get("", response_model=list[SessionOut])
def list_replays(
    db: OrmSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return (
        db.query(TutorSession)
        .filter(TutorSession.user_id == user.id)
        .order_by(TutorSession.started_at.desc())
        .all()
    )


@router.get("/{session_id}", response_model=ReplaySessionOut)
def replay_session(
    session_id: int,
    limit: int = Query(200, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    db: OrmSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    s = (
        db.query(TutorSession)
        .filter(TutorSession.id == session_id, TutorSession.user_id == user.id)
        .first()
    )
    if not s:
        raise HTTPException(status_code=404, detail="Session not found")
    concepts = db.query(Concept).filter(Concept.session_id == s.id).all()
    messages = (
        db.query(TutorMessage)
        .filter(TutorMessage.session_id == s.id)
        .order_by(TutorMessage.created_at.asc(), TutorMessage.id.asc())
        .offset(offset)
        .limit(limit)
        .all()
    )
    return ReplaySessionOut(
        session_id=s.id,
        lesson_id=s.lesson_id,
        status=s.status,
        started_at=s.started_at,
        ended_at=s.ended_at,
        transcript=s.transcript or "",
        concepts=[ConceptOut.model_validate(c) for c in concepts],
        messages=[TutorMessageOut.model_validate(m) for m in messages],
    )
