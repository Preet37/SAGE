"""Courses (modeled as Lesson rows in the simplified MVP schema).

Catalog is shared across authenticated users so that seeded demo content is
visible to anyone who registers. Mutation (create/delete) is owner-scoped.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import Optional
from app.database import get_db
from app.models.lesson import Course, Lesson
from app.models.user import User
from app.routers.auth import get_current_user

router = APIRouter(prefix="/courses", tags=["courses"])


class CourseOut(BaseModel):
    id: int
    slug: str
    title: str
    description: str
    level: str
    tags: list
    thumbnail_url: Optional[str]

    class Config:
        from_attributes = True


class LessonOut(BaseModel):
    id: int
    slug: str
    title: str
    order: int
    summary: str
    key_concepts: list
    estimated_minutes: int
    video_url: Optional[str]

    class Config:
        from_attributes = True


@router.get("/", response_model=list[CourseOut])
async def list_courses(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Course).order_by(Course.id))
    return result.scalars().all()


@router.get("/{course_slug}", response_model=CourseOut)
async def get_course(course_slug: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Course).where(Course.slug == course_slug))
    course = result.scalar_one_or_none()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


@router.get("/{course_slug}/lessons", response_model=list[LessonOut])
async def list_lessons(course_slug: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Course).where(Course.slug == course_slug))
    course = result.scalar_one_or_none()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    lessons_result = await db.execute(
        select(Lesson).where(Lesson.course_id == course.id).order_by(Lesson.order)
    )
    return lessons_result.scalars().all()


@router.get("/{course_slug}/lessons/{lesson_slug}", response_model=LessonOut)
async def get_lesson(course_slug: str, lesson_slug: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Course).where(Course.slug == course_slug))
    course = result.scalar_one_or_none()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    lesson_result = await db.execute(
        select(Lesson).where(Lesson.course_id == course.id, Lesson.slug == lesson_slug)
    )
    lesson = lesson_result.scalar_one_or_none()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return lesson
