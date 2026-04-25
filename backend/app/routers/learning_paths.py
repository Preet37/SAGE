import json
import secrets
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select, or_

from ..db import get_session
from ..deps import get_current_user
from ..models.user import User
from ..models.learning import LearningPath, Module, Lesson, CourseShare
from ..schemas.learning import (
    LearningPathResponse,
    LearningPathSummary,
    ModuleResponse,
    LessonResponse,
    ShareEntry,
)

router = APIRouter(prefix="/learning-paths", tags=["learning"])


def _can_access(path: LearningPath, user: User, session: Session) -> bool:
    if path.visibility == "public":
        return True
    if path.created_by == user.id:
        return True
    shared = session.exec(
        select(CourseShare)
        .where(CourseShare.learning_path_id == path.id, CourseShare.user_id == user.id)
    ).first()
    return shared is not None


def _shared_path_ids(user_id: str, session: Session) -> set[str]:
    rows = session.exec(
        select(CourseShare.learning_path_id).where(CourseShare.user_id == user_id)
    ).all()
    return set(rows)


def lesson_to_schema(lesson: Lesson) -> LessonResponse:
    try:
        concepts = json.loads(lesson.concepts)
    except (json.JSONDecodeError, TypeError):
        concepts = []

    try:
        image_metadata = json.loads(lesson.image_metadata) if lesson.image_metadata else []
    except (json.JSONDecodeError, TypeError):
        image_metadata = []

    try:
        sources_raw = json.loads(lesson.sources_used) if lesson.sources_used else []
    except (json.JSONDecodeError, TypeError):
        sources_raw = []
    sources_used = [
        (s["url"] if isinstance(s, dict) and "url" in s else str(s))
        for s in sources_raw
    ]

    return LessonResponse(
        id=lesson.id,
        title=lesson.title,
        slug=lesson.slug,
        content=lesson.content,
        summary=lesson.summary,
        concepts=concepts,
        order_index=lesson.order_index,
        youtube_id=lesson.youtube_id,
        video_title=lesson.video_title,
        vimeo_url=lesson.vimeo_url,
        module_id=lesson.module_id,
        image_metadata=image_metadata,
        sources_used=sources_used,
        reference_kb=lesson.reference_kb,
    )


def module_to_schema(module: Module, session: Session) -> ModuleResponse:
    lessons = session.exec(
        select(Lesson).where(Lesson.module_id == module.id).order_by(Lesson.order_index)
    ).all()
    return ModuleResponse(
        id=module.id,
        title=module.title,
        order_index=module.order_index,
        lessons=[lesson_to_schema(l) for l in lessons],
    )


@router.get("", response_model=List[LearningPathSummary])
def list_learning_paths(
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    shared_ids = _shared_path_ids(user.id, session)

    paths = session.exec(
        select(LearningPath)
        .where(
            or_(
                LearningPath.visibility == "public",
                LearningPath.created_by == user.id,
                LearningPath.id.in_(shared_ids) if shared_ids else False,  # type: ignore[union-attr]
            )
        )
        .order_by(LearningPath.order_index)
    ).all()

    return [
        LearningPathSummary(
            id=p.id,
            slug=p.slug,
            title=p.title,
            description=p.description,
            level=p.level,
            visibility=p.visibility,
            is_mine=p.created_by == user.id,
        )
        for p in paths
    ]


@router.get("/{slug}", response_model=LearningPathResponse)
def get_learning_path(
    slug: str,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    path = session.exec(select(LearningPath).where(LearningPath.slug == slug)).first()
    if not path or not _can_access(path, user, session):
        raise HTTPException(status_code=404, detail="Learning path not found")

    modules = session.exec(
        select(Module)
        .where(Module.learning_path_id == path.id)
        .order_by(Module.order_index)
    ).all()

    return LearningPathResponse(
        id=path.id,
        slug=path.slug,
        title=path.title,
        description=path.description,
        level=path.level,
        visibility=path.visibility,
        is_mine=path.created_by == user.id,
        modules=[module_to_schema(m, session) for m in modules],
    )


@router.get("/lessons/{lesson_id}", response_model=LessonResponse)
def get_lesson(
    lesson_id: str,
    session: Session = Depends(get_session),
    _user: User = Depends(get_current_user),
):
    lesson = session.get(Lesson, lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return lesson_to_schema(lesson)


# ---------------------------------------------------------------------------
# Sharing
# ---------------------------------------------------------------------------

class ShareRequest(BaseModel):
    email: str


@router.post("/{slug}/share")
def share_course(
    slug: str,
    req: ShareRequest,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    path = session.exec(select(LearningPath).where(LearningPath.slug == slug)).first()
    if not path or path.created_by != user.id:
        raise HTTPException(status_code=404, detail="Course not found")

    target = session.exec(select(User).where(User.email == req.email)).first()
    if not target:
        raise HTTPException(status_code=404, detail="User not found")
    if target.id == user.id:
        raise HTTPException(status_code=400, detail="Cannot share with yourself")

    existing = session.exec(
        select(CourseShare)
        .where(CourseShare.learning_path_id == path.id, CourseShare.user_id == target.id)
    ).first()
    if existing:
        return {"status": "already_shared", "email": req.email}

    session.add(CourseShare(learning_path_id=path.id, user_id=target.id))
    session.commit()
    return {"status": "shared", "email": req.email}


@router.delete("/{slug}/share/{target_user_id}")
def unshare_course(
    slug: str,
    target_user_id: str,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    path = session.exec(select(LearningPath).where(LearningPath.slug == slug)).first()
    if not path or path.created_by != user.id:
        raise HTTPException(status_code=404, detail="Course not found")

    share = session.exec(
        select(CourseShare)
        .where(CourseShare.learning_path_id == path.id, CourseShare.user_id == target_user_id)
    ).first()
    if not share:
        return {"status": "not_shared"}

    session.delete(share)
    session.commit()
    return {"status": "unshared"}


@router.get("/{slug}/shares", response_model=List[ShareEntry])
def list_shares(
    slug: str,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    path = session.exec(select(LearningPath).where(LearningPath.slug == slug)).first()
    if not path or path.created_by != user.id:
        raise HTTPException(status_code=404, detail="Course not found")

    shares = session.exec(
        select(CourseShare).where(CourseShare.learning_path_id == path.id)
    ).all()

    entries = []
    for s in shares:
        u = session.get(User, s.user_id)
        if u:
            entries.append(ShareEntry(user_id=u.id, email=u.email, username=u.username))
    return entries


@router.post("/{slug}/share-link")
def get_share_link(
    slug: str,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    path = session.exec(select(LearningPath).where(LearningPath.slug == slug)).first()
    if not path or path.created_by != user.id:
        raise HTTPException(status_code=404, detail="Course not found")

    if not path.share_token:
        path.share_token = secrets.token_urlsafe(16)
        session.add(path)
        session.commit()

    return {"share_token": path.share_token, "slug": slug}


@router.post("/join/{share_token}")
def join_via_link(
    share_token: str,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    path = session.exec(
        select(LearningPath).where(LearningPath.share_token == share_token)
    ).first()
    if not path:
        raise HTTPException(status_code=404, detail="Invalid share link")

    if path.created_by == user.id:
        return {"status": "owner", "slug": path.slug}

    existing = session.exec(
        select(CourseShare)
        .where(CourseShare.learning_path_id == path.id, CourseShare.user_id == user.id)
    ).first()
    if existing:
        return {"status": "already_shared", "slug": path.slug}

    session.add(CourseShare(learning_path_id=path.id, user_id=user.id))
    session.commit()
    return {"status": "joined", "slug": path.slug}
