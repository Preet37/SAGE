"""Read-only endpoints for courses — bridges legacy courses/lessons tables with new lesson CUIDs."""
import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from ..db import engine
from ..deps import get_current_user
from ..models.user import User

router = APIRouter(prefix="/courses", tags=["courses"])


def _row_to_course(row) -> dict:
    tags = row[5]
    if isinstance(tags, str):
        try:
            tags = json.loads(tags)
        except Exception:
            tags = []
    return {
        "id": row[0],
        "slug": row[1],
        "title": row[2],
        "description": row[3],
        "level": row[4],
        "tags": tags or [],
        "thumbnail_url": row[6] if len(row) > 6 else None,
    }


def _row_to_lesson(row) -> dict:
    key_concepts = row[5]
    if isinstance(key_concepts, str):
        try:
            key_concepts = json.loads(key_concepts)
        except Exception:
            key_concepts = []
    return {
        "id": row[0],          # CUID from new lesson table
        "slug": row[1],
        "title": row[2],
        "order": row[3],
        "summary": row[4],
        "key_concepts": key_concepts or [],
        "estimated_minutes": row[6] if row[6] else 20,
        "video_url": row[7] if len(row) > 7 else None,
    }


@router.get("/")
def list_courses(_user: User = Depends(get_current_user)):
    with engine.connect() as conn:
        rows = conn.execute(
            text("SELECT id, slug, title, description, level, tags, thumbnail_url FROM courses ORDER BY id")
        ).fetchall()
    return [_row_to_course(r) for r in rows]


@router.get("/{slug}/lessons")
def list_lessons(slug: str, _user: User = Depends(get_current_user)):
    with engine.connect() as conn:
        # Join new lesson table (for CUID) with legacy lessons table (for estimated_minutes/video_url)
        rows = conn.execute(
            text("""
                SELECT l.id, l.slug, l.title, l.order_index, l.summary, l.concepts,
                       ll.estimated_minutes, ll.video_url
                FROM lesson l
                JOIN module m ON m.id = l.module_id
                JOIN learningpath lp ON lp.id = m.learning_path_id
                LEFT JOIN lessons ll ON ll.slug = l.slug
                WHERE lp.slug = :course_slug
                ORDER BY l.order_index
            """),
            {"course_slug": slug},
        ).fetchall()
    if not rows:
        raise HTTPException(status_code=404, detail="Course not found")
    return [_row_to_lesson(r) for r in rows]


@router.get("/{slug}/lessons/{lesson_slug}")
def get_lesson(slug: str, lesson_slug: str, _user: User = Depends(get_current_user)):
    with engine.connect() as conn:
        row = conn.execute(
            text("""
                SELECT l.id, l.slug, l.title, l.order_index, l.summary, l.concepts,
                       ll.estimated_minutes, ll.video_url
                FROM lesson l
                JOIN module m ON m.id = l.module_id
                JOIN learningpath lp ON lp.id = m.learning_path_id
                LEFT JOIN lessons ll ON ll.slug = l.slug
                WHERE lp.slug = :course_slug AND l.slug = :lesson_slug
            """),
            {"course_slug": slug, "lesson_slug": lesson_slug},
        ).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return _row_to_lesson(row)
