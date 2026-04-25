"""Courses (modeled as Lesson rows in the simplified MVP schema).

Catalog is shared across authenticated users so that seeded demo content is
visible to anyone who registers. Mutation (create/delete) is owner-scoped.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session as OrmSession

from app.db import get_db
from app.models import Lesson, User
from app.schemas import LessonCreate, LessonOut
from app.security import get_current_user

router = APIRouter(prefix="/courses", tags=["courses"])


@router.get("", response_model=list[LessonOut])
def list_courses(db: OrmSession = Depends(get_db), _: User = Depends(get_current_user)):
    return db.query(Lesson).order_by(Lesson.id.asc()).all()


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
    _: User = Depends(get_current_user),
):
    lesson = db.query(Lesson).filter(Lesson.id == course_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Course not found")
    return lesson


@router.delete("/{course_id}", status_code=204)
def delete_course(
    course_id: int,
    db: OrmSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    lesson = db.query(Lesson).filter(Lesson.id == course_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Course not found")
    if lesson.owner_id != user.id:
        raise HTTPException(status_code=403, detail="Not owner")
    db.delete(lesson)
    db.commit()
