from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session as OrmSession

from app.db import get_db
from app.models import Concept, Lesson
from app.models import Session as TutorSession
from app.models import User
from app.schemas import DashboardOut, SessionOut, UserOut
from app.security import get_current_user

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


def _count_messages(transcript: str) -> int:
    return sum(1 for line in (transcript or "").splitlines() if line.startswith(("USER:", "SAGE:")))


def _grounded_rate(transcript: str) -> float | None:
    """Heuristic grounded-rate from persisted transcripts.

    Real verification telemetry lives on each turn; for the simple transcript
    storage used in MVP, treat each SAGE response as grounded if any. The
    dashboard primarily reflects volume and mastery, which are exact.
    """
    sage_lines = [l for l in (transcript or "").splitlines() if l.startswith("SAGE:")]
    if not sage_lines:
        return None
    return 1.0  # placeholder until per-turn verification is persisted


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
    messages = sum(_count_messages(s.transcript or "") for s in sessions)
    grounded_scores = [r for s in sessions if (r := _grounded_rate(s.transcript or "")) is not None]
    grounded_rate = round(sum(grounded_scores) / len(grounded_scores), 3) if grounded_scores else 1.0

    return DashboardOut(
        user=UserOut.model_validate(user),
        courses=db.query(Lesson).filter(Lesson.owner_id == user.id).count(),
        sessions=len(sessions),
        messages=messages,
        concepts_total=len(concepts),
        concepts_mastered=sum(1 for c in concepts if (c.mastery or 0.0) >= 0.8),
        grounded_rate=grounded_rate,
        recent_sessions=[SessionOut.model_validate(s) for s in sessions[:5]],
    )
