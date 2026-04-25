from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session as OrmSession

from app.db import get_db
from app.models import Concept, User
from app.schemas import ConceptOut
from app.security import get_current_user

router = APIRouter(prefix="/concept-map", tags=["concept-map"])


@router.get("/{session_id}", response_model=list[ConceptOut])
def get_map(
    session_id: int,
    db: OrmSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    return db.query(Concept).filter(Concept.session_id == session_id).all()
