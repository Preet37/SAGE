from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session as OrmSession

from app.db import get_db
from app.models import Concept
from app.models import Session as TutorSession
from app.models import User
from app.schemas import ConceptOut, ReplaySessionOut, SessionOut
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
    return ReplaySessionOut(
        session_id=s.id,
        lesson_id=s.lesson_id,
        status=s.status,
        started_at=s.started_at,
        ended_at=s.ended_at,
        transcript=s.transcript or "",
        concepts=[ConceptOut.model_validate(c) for c in concepts],
    )
