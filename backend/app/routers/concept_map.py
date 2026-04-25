from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session as OrmSession

from app.db import get_db
from app.models import Concept
from app.models import Session as TutorSession
from app.models import User
from app.schemas import ConceptOut, MasteryUpdate
from app.security import get_current_user

router = APIRouter(prefix="/concept-map", tags=["concept-map"])


def _own_session(db: OrmSession, session_id: int, user: User) -> TutorSession:
    s = (
        db.query(TutorSession)
        .filter(TutorSession.id == session_id, TutorSession.user_id == user.id)
        .first()
    )
    if not s:
        raise HTTPException(status_code=404, detail="Session not found")
    return s


@router.get("/{session_id}", response_model=list[ConceptOut])
def get_map(
    session_id: int,
    db: OrmSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    _own_session(db, session_id, user)
    return db.query(Concept).filter(Concept.session_id == session_id).all()


@router.patch("/{session_id}/concepts/{concept_id}/mastery", response_model=ConceptOut)
def bump_mastery(
    session_id: int,
    concept_id: int,
    payload: MasteryUpdate,
    db: OrmSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    _own_session(db, session_id, user)
    c = (
        db.query(Concept)
        .filter(Concept.id == concept_id, Concept.session_id == session_id)
        .first()
    )
    if not c:
        raise HTTPException(status_code=404, detail="Concept not found")
    c.mastery = max(0.0, min(1.0, (c.mastery or 0.0) + payload.delta))
    db.commit()
    db.refresh(c)
    return c


@router.get("/{session_id}/next", response_model=list[ConceptOut])
def next_concepts(
    session_id: int,
    db: OrmSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Top 3 concepts the learner is weakest at — what to study next."""
    _own_session(db, session_id, user)
    rows = (
        db.query(Concept)
        .filter(Concept.session_id == session_id, Concept.mastery < 0.8)
        .order_by(Concept.mastery.asc())
        .limit(3)
        .all()
    )
    return rows
