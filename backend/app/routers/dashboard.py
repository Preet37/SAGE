from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session as OrmSession

from app.db import get_db
from app.models import Concept, Lesson
from app.models import Session as TutorSession
from app.models import TutorMessage, User
from app.schemas import (
    ConceptOut,
    CourseDashboardOut,
    DashboardOut,
    LessonOut,
    SessionOut,
    UserOut,
)
from app.security import get_current_user

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


def _grounded_rate_from_messages(messages: list[TutorMessage]) -> float:
    rated = [m for m in messages if m.role == "assistant"]
    if not rated:
        return 1.0
    return round(sum(1 for m in rated if m.verification_passed) / len(rated), 3)


def _count_messages_in_transcript(t: str) -> int:
    return sum(1 for line in (t or "").splitlines() if line.startswith(("USER:", "SAGE:")))


@router.get("", response_model=DashboardOut)
def dashboard(
    db: OrmSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    sessions = (
        db.query(TutorSession)
        .filter(TutorSession.user_id == user.id)
        .order_by(TutorSession.started_at.desc())
        .all()
    )
    session_ids = [s.id for s in sessions]
    concepts = (
        db.query(Concept).filter(Concept.session_id.in_(session_ids)).all() if session_ids else []
    )
    messages = (
        db.query(TutorMessage).filter(TutorMessage.session_id.in_(session_ids)).all()
        if session_ids
        else []
    )
    persisted_msgs = len(messages)
    transcript_msgs = sum(_count_messages_in_transcript(s.transcript or "") for s in sessions)

    return DashboardOut(
        user=UserOut.model_validate(user),
        courses=db.query(Lesson).count(),
        sessions=len(sessions),
        # Prefer persisted message count; fall back to transcript scan for legacy sessions.
        messages=persisted_msgs or transcript_msgs,
        concepts_total=len(concepts),
        concepts_mastered=sum(1 for c in concepts if (c.mastery or 0.0) >= 0.8),
        grounded_rate=_grounded_rate_from_messages(messages) if messages else 1.0,
        recent_sessions=[SessionOut.model_validate(s) for s in sessions[:5]],
    )


@router.get("/course/{course_id}", response_model=CourseDashboardOut)
def course_dashboard(
    course_id: int,
    db: OrmSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    lesson = db.query(Lesson).filter(Lesson.id == course_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Course not found")

    sessions = (
        db.query(TutorSession)
        .filter(TutorSession.user_id == user.id, TutorSession.lesson_id == course_id)
        .all()
    )
    session_ids = [s.id for s in sessions]
    concepts = (
        db.query(Concept).filter(Concept.session_id.in_(session_ids)).all()
        if session_ids
        else []
    )
    messages = (
        db.query(TutorMessage).filter(TutorMessage.session_id.in_(session_ids)).count()
        if session_ids
        else 0
    )
    weakest = sorted(concepts, key=lambda c: c.mastery or 0.0)[:5]
    next_concepts = [c for c in weakest if (c.mastery or 0.0) < 0.8][:3]

    return CourseDashboardOut(
        course=LessonOut.model_validate(lesson),
        sessions=len(sessions),
        messages=messages,
        concepts_total=len(concepts),
        concepts_mastered=sum(1 for c in concepts if (c.mastery or 0.0) >= 0.8),
        weakest=[ConceptOut.model_validate(c) for c in weakest],
        next_concepts=[ConceptOut.model_validate(c) for c in next_concepts],
    )
