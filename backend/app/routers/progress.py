from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from ..db import get_session
from ..deps import get_current_user
from ..models.user import User
from ..models.progress import UserLessonProgress, ChatMessage, TutorSession
from ..models.learning import Lesson
from ..schemas.progress import (
    ProgressResponse, MarkCompleteRequest, ChatMessageResponse, TutorSessionResponse,
)

router = APIRouter(prefix="/progress", tags=["progress"])


@router.get("", response_model=List[ProgressResponse])
def get_all_progress(
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    rows = session.exec(
        select(UserLessonProgress).where(UserLessonProgress.user_id == user.id)
    ).all()
    return [
        ProgressResponse(
            lesson_id=r.lesson_id,
            completed=r.completed,
            completed_at=r.completed_at,
        )
        for r in rows
    ]


@router.get("/chat-history/{lesson_id}", response_model=List[ChatMessageResponse])
def get_chat_history(
    lesson_id: str,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    """Return messages from the latest tutor session, or legacy messages with no session."""
    latest = session.exec(
        select(TutorSession)
        .where(TutorSession.user_id == user.id, TutorSession.lesson_id == lesson_id)
        .order_by(TutorSession.updated_at.desc())
    ).first()

    if latest:
        messages = session.exec(
            select(ChatMessage)
            .where(ChatMessage.session_id == latest.id)
            .order_by(ChatMessage.created_at)
        ).all()
    else:
        messages = session.exec(
            select(ChatMessage)
            .where(
                ChatMessage.user_id == user.id,
                ChatMessage.lesson_id == lesson_id,
                ChatMessage.session_id == None,  # noqa: E711
            )
            .order_by(ChatMessage.created_at)
        ).all()

    return [
        ChatMessageResponse(id=m.id, role=m.role, content=m.content, created_at=m.created_at, message_meta=m.message_meta)
        for m in messages
    ]


@router.get("/sessions/{lesson_id}", response_model=List[TutorSessionResponse])
def list_tutor_sessions(
    lesson_id: str,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    sessions = session.exec(
        select(TutorSession)
        .where(TutorSession.user_id == user.id, TutorSession.lesson_id == lesson_id)
        .order_by(TutorSession.updated_at.desc())
    ).all()
    return sessions


@router.get("/sessions/{lesson_id}/{session_id}/history", response_model=List[ChatMessageResponse])
def get_session_history(
    lesson_id: str,
    session_id: str,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    tutor_session = session.get(TutorSession, session_id)
    if not tutor_session or tutor_session.user_id != user.id or tutor_session.lesson_id != lesson_id:
        raise HTTPException(status_code=404, detail="Session not found")

    messages = session.exec(
        select(ChatMessage)
        .where(ChatMessage.session_id == session_id)
        .order_by(ChatMessage.created_at)
    ).all()
    return [
        ChatMessageResponse(id=m.id, role=m.role, content=m.content, created_at=m.created_at, message_meta=m.message_meta)
        for m in messages
    ]


@router.delete("/sessions/{lesson_id}/{session_id}")
def delete_tutor_session(
    lesson_id: str,
    session_id: str,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    tutor_session = session.get(TutorSession, session_id)
    if not tutor_session or tutor_session.user_id != user.id or tutor_session.lesson_id != lesson_id:
        raise HTTPException(status_code=404, detail="Session not found")

    messages = session.exec(
        select(ChatMessage).where(ChatMessage.session_id == session_id)
    ).all()
    for m in messages:
        session.delete(m)
    session.delete(tutor_session)
    session.commit()
    return {"ok": True}


@router.get("/{lesson_id}", response_model=ProgressResponse)
def get_lesson_progress(
    lesson_id: str,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    row = session.exec(
        select(UserLessonProgress)
        .where(UserLessonProgress.user_id == user.id)
        .where(UserLessonProgress.lesson_id == lesson_id)
    ).first()
    if not row:
        return ProgressResponse(lesson_id=lesson_id, completed=False, completed_at=None)
    return ProgressResponse(lesson_id=row.lesson_id, completed=row.completed, completed_at=row.completed_at)


@router.post("", response_model=ProgressResponse)
def mark_complete(
    req: MarkCompleteRequest,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    lesson = session.get(Lesson, req.lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    row = session.exec(
        select(UserLessonProgress)
        .where(UserLessonProgress.user_id == user.id)
        .where(UserLessonProgress.lesson_id == req.lesson_id)
    ).first()

    if row:
        row.completed = True
        row.completed_at = datetime.utcnow()
    else:
        row = UserLessonProgress(
            user_id=user.id,
            lesson_id=req.lesson_id,
            completed=True,
            completed_at=datetime.utcnow(),
        )
        session.add(row)

    session.commit()
    session.refresh(row)
    return ProgressResponse(lesson_id=row.lesson_id, completed=row.completed, completed_at=row.completed_at)


# ── Knowledge Galaxy endpoint ─────────────────────────────────────────────────
from ..models.learning import LearningPath, Module
from ..models.user import User as _User
from sqlmodel import func as sqlfunc
from pydantic import BaseModel as _BaseModel
from typing import Optional

class GalaxyNode(_BaseModel):
    id: str
    label: str
    module_id: str
    module_name: str
    path_id: str
    path_name: str
    completed: bool
    order_index: int

class GalaxyEdge(_BaseModel):
    source: str
    target: str

class GalaxyRank(_BaseModel):
    rank: int
    total_users: int
    score: int  # completed lessons
    percentile: float

class GalaxyResponse(_BaseModel):
    nodes: list[GalaxyNode]
    edges: list[GalaxyEdge]
    rank: GalaxyRank
    total_lessons: int
    completed_count: int
    streak_days: int


@router.get("/galaxy", response_model=GalaxyResponse)
def get_knowledge_galaxy(
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    """Return the user's knowledge graph for the galaxy visualization."""
    # Fetch all paths → modules → lessons
    paths = session.exec(select(LearningPath)).all()
    modules = session.exec(select(Module)).all()
    lessons = session.exec(select(Lesson)).all()

    # Index for lookup
    path_map = {p.id: p for p in paths}
    module_map = {m.id: m for m in modules}

    # User's completed lessons
    completed_ids = {
        r.lesson_id
        for r in session.exec(
            select(UserLessonProgress)
            .where(UserLessonProgress.user_id == user.id)
            .where(UserLessonProgress.completed == True)  # noqa: E712
        ).all()
    }

    # Build nodes
    nodes: list[GalaxyNode] = []
    for lesson in lessons:
        mod = module_map.get(lesson.module_id)
        if not mod:
            continue
        path = path_map.get(mod.path_id)
        if not path:
            continue
        nodes.append(GalaxyNode(
            id=lesson.id,
            label=lesson.title,
            module_id=mod.id,
            module_name=mod.title,
            path_id=path.id,
            path_name=path.title,
            completed=lesson.id in completed_ids,
            order_index=getattr(lesson, "order_index", 0),
        ))

    # Build edges: connect consecutive lessons within same module
    module_lessons: dict[str, list[GalaxyNode]] = {}
    for node in nodes:
        module_lessons.setdefault(node.module_id, []).append(node)

    edges: list[GalaxyEdge] = []
    for mod_id, mod_nodes in module_lessons.items():
        sorted_nodes = sorted(mod_nodes, key=lambda n: n.order_index)
        for i in range(len(sorted_nodes) - 1):
            edges.append(GalaxyEdge(source=sorted_nodes[i].id, target=sorted_nodes[i + 1].id))

    # Rank: count completed lessons per user, rank current user
    user_scores = session.exec(
        select(UserLessonProgress.user_id, sqlfunc.count(UserLessonProgress.id).label("score"))
        .where(UserLessonProgress.completed == True)  # noqa: E712
        .group_by(UserLessonProgress.user_id)
    ).all()

    score_map = {row[0]: row[1] for row in user_scores}
    my_score = score_map.get(user.id, 0)
    total_users = max(len(score_map), 1)
    users_beaten = sum(1 for s in score_map.values() if s < my_score)
    rank = total_users - users_beaten

    # Streak: consecutive days with chat activity
    recent_days = session.exec(
        select(sqlfunc.date(ChatMessage.created_at).label("day"))
        .where(ChatMessage.user_id == user.id)
        .group_by(sqlfunc.date(ChatMessage.created_at))
        .order_by(sqlfunc.date(ChatMessage.created_at).desc())
    ).all()

    streak = 0
    from datetime import date, timedelta
    today = date.today()
    for i, (day,) in enumerate(recent_days):
        d = date.fromisoformat(str(day))
        if d == today - timedelta(days=i):
            streak += 1
        else:
            break

    return GalaxyResponse(
        nodes=nodes,
        edges=edges,
        rank=GalaxyRank(
            rank=rank,
            total_users=total_users,
            score=my_score,
            percentile=round(users_beaten / total_users * 100, 1),
        ),
        total_lessons=len(nodes),
        completed_count=len(completed_ids),
        streak_days=streak,
    )
