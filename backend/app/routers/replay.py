from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session as OrmSession

from app.db import get_db
from app.models import Session as TutorSession
from app.models import User
from app.security import get_current_user

router = APIRouter(prefix="/replay", tags=["replay"])


@router.get("/{session_id}")
def replay_session(
    session_id: int,
    db: OrmSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    s = db.query(TutorSession).filter(
        TutorSession.id == session_id, TutorSession.user_id == user.id
    ).first()
    if not s:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"session_id": s.id, "transcript": s.transcript, "started_at": s.started_at}
