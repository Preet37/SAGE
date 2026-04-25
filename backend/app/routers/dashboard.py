from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session as OrmSession

from app.db import get_db
from app.models import Lesson
from app.models import Session as TutorSession
from app.models import User
from app.security import get_current_user

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("")
def dashboard(db: OrmSession = Depends(get_db), user: User = Depends(get_current_user)):
    return {
        "user": {"id": user.id, "name": user.name, "email": user.email},
        "courses": db.query(Lesson).filter(Lesson.owner_id == user.id).count(),
        "sessions": db.query(TutorSession).filter(TutorSession.user_id == user.id).count(),
    }
