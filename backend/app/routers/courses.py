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

    sources_used: list = []
    try:
        raw_sources = row[12] if len(row) > 12 else None
        if raw_sources:
            sources_used = json.loads(raw_sources)
    except Exception:
        pass

    image_metadata: list = []
    try:
        raw_images = row[13] if len(row) > 13 else None
        if raw_images:
            image_metadata = json.loads(raw_images)
    except Exception:
        pass

    # Build video_url from youtube_id or vimeo_url
    youtube_id = row[9] if len(row) > 9 else None
    vimeo_url = row[11] if len(row) > 11 else None
    legacy_video_url = row[7] if len(row) > 7 else None
    video_url = legacy_video_url
    if youtube_id and not video_url:
        video_url = f"https://www.youtube.com/watch?v={youtube_id}"

    return {
        "id": row[0],          # CUID from new lesson table
        "slug": row[1],
        "title": row[2],
        "order": row[3],
        "summary": row[4],
        "key_concepts": key_concepts or [],
        "estimated_minutes": row[6] if row[6] else 20,
        "video_url": video_url,
        # Rich fields
        "content": row[8] if len(row) > 8 else None,
        "youtube_id": youtube_id,
        "video_title": row[10] if len(row) > 10 else None,
        "vimeo_url": vimeo_url,
        "reference_kb": row[14] if len(row) > 14 else None,
        "sources_used": sources_used,
        "image_metadata": image_metadata,
    }


_LESSON_SELECT = """
    SELECT l.id, l.slug, l.title, l.order_index, l.summary, l.concepts,
           ll.estimated_minutes, ll.video_url,
           l.content, l.youtube_id, l.video_title, l.vimeo_url,
           l.sources_used, l.image_metadata, l.reference_kb
    FROM lesson l
    JOIN module m ON m.id = l.module_id
    JOIN learningpath lp ON lp.id = m.learning_path_id
    LEFT JOIN lessons ll ON ll.slug = l.slug
"""


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
        rows = conn.execute(
            text(f"{_LESSON_SELECT} WHERE lp.slug = :course_slug ORDER BY l.order_index"),
            {"course_slug": slug},
        ).fetchall()
    if not rows:
        raise HTTPException(status_code=404, detail="Course not found")
    return [_row_to_lesson(r) for r in rows]


@router.get("/{slug}/lessons/{lesson_slug}")
def get_lesson(slug: str, lesson_slug: str, _user: User = Depends(get_current_user)):
    with engine.connect() as conn:
        row = conn.execute(
            text(f"{_LESSON_SELECT} WHERE lp.slug = :course_slug AND l.slug = :lesson_slug"),
            {"course_slug": slug, "lesson_slug": lesson_slug},
        ).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return _row_to_lesson(row)
