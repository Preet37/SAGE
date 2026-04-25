from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session as OrmSession

from app.db import get_db
from app.models import Lesson, User
from app.schemas import LessonCreate, LessonOut
from app.security import get_current_user

router = APIRouter(prefix="/courses", tags=["courses"])


@router.get("", response_model=list[LessonOut])
def list_courses(db: OrmSession = Depends(get_db), user: User = Depends(get_current_user)):
    return db.query(Lesson).filter(Lesson.owner_id == user.id).all()


@router.post("", response_model=LessonOut, status_code=201)
def create_course(
    payload: LessonCreate,
    db: OrmSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    lesson = Lesson(owner_id=user.id, **payload.model_dump())
    db.add(lesson)
    db.commit()
    db.refresh(lesson)
    return lesson


@router.get("/{course_id}", response_model=LessonOut)
def get_course(
    course_id: int,
    db: OrmSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    lesson = db.query(Lesson).filter(Lesson.id == course_id, Lesson.owner_id == user.id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Course not found")
    return lesson


@router.delete("/{course_id}", status_code=204)
def delete_course(
    course_id: int,
    db: OrmSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    lesson = db.query(Lesson).filter(Lesson.id == course_id, Lesson.owner_id == user.id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Course not found")
    db.delete(lesson)
    db.commit()
