import json
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlmodel import Session, select

from ..db import get_session, engine
from ..deps import get_current_user, enforce_usage_limit
from ..models.user import User
from ..models.learning import Lesson, Module, LearningPath
from ..models.progress import UserLessonProgress
from ..models.exploration import ExplorationSession, ExplorationMessage
from ..agent.agent_loop import run_tutor_agent_loop
from ..agent.context import TutorContext
from ..schemas.explore import (
    ExploreRequest,
    ExplorationSessionResponse,
    ExplorationMessageResponse,
)

router = APIRouter(prefix="/explore", tags=["explore"])


def _build_available_courses(session: Session) -> list[dict]:
    """Load all courses with their lessons into a compact structure for the prompt."""
    paths = session.exec(
        select(LearningPath).order_by(LearningPath.title)
    ).all()

    courses = []
    for lp in paths:
        modules = session.exec(
            select(Module)
            .where(Module.learning_path_id == lp.id)
            .order_by(Module.order_index)
        ).all()

        lessons_data = []
        for mod in modules:
            lessons = session.exec(
                select(Lesson)
                .where(Lesson.module_id == mod.id)
                .order_by(Lesson.order_index)
            ).all()
            for lesson in lessons:
                try:
                    concepts = json.loads(lesson.concepts)
                except (json.JSONDecodeError, TypeError):
                    concepts = []
                lessons_data.append({
                    "slug": lesson.slug,
                    "title": lesson.title,
                    "summary": lesson.summary,
                    "concepts": concepts,
                })

        courses.append({
            "title": lp.title,
            "description": lp.description,
            "level": lp.level,
            "lessons": lessons_data,
        })
    return courses


def _build_curriculum_index(courses: list[dict]) -> list[dict]:
    """Flatten courses into a single curriculum index for tool lookups."""
    index = []
    for course in courses:
        for lesson in course.get("lessons", []):
            index.append({
                "slug": lesson["slug"],
                "title": lesson["title"],
                "concepts": lesson.get("concepts", []),
            })
    return index


async def _get_completed_lesson_titles(user_id: str, session: Session) -> list[str]:
    rows = session.exec(
        select(Lesson.title)
        .join(UserLessonProgress, UserLessonProgress.lesson_id == Lesson.id)
        .where(UserLessonProgress.user_id == user_id)
        .where(UserLessonProgress.completed == True)
    ).all()
    return list(rows)


def _extract_modalities(text: str) -> list[str]:
    """Detect output modalities present in assistant response."""
    import re
    modalities = []
    if re.search(r"<quiz>", text):
        modalities.append("quiz")
    if re.search(r"<resource>", text):
        modalities.append("resource")
    if re.search(r"<image>", text):
        modalities.append("image")
    if re.search(r"```mermaid", text):
        modalities.append("mermaid")
    if re.search(r"<flow>", text):
        modalities.append("flow")
    if re.search(r"<architecture>", text):
        modalities.append("architecture")
    if re.search(r"```(?:python|javascript|typescript|bash|sql)", text):
        modalities.append("code")
    if re.search(r"\$\$.*?\$\$|\\\[.*?\\\]", text, re.DOTALL):
        modalities.append("math")
    return modalities


async def _stream_with_save(generator, user_id: str, session_id: str, user_content: str):
    """Wrap the agent generator to collect assistant text, tools, and modalities."""
    assistant_text = ""
    tools_used: list[str] = []

    async for chunk in generator:
        yield chunk
        try:
            data = chunk.removeprefix("data: ").strip()
            if data:
                event = json.loads(data)
                if event.get("type") == "text":
                    assistant_text += event.get("delta", "")
                elif event.get("type") == "tool_call":
                    tool_name = event.get("name", "")
                    if tool_name and tool_name not in tools_used:
                        tools_used.append(tool_name)
        except Exception:
            pass

    with Session(engine) as session:
        session.add(ExplorationMessage(
            session_id=session_id, role="user", content=user_content,
        ))
        if assistant_text:
            modalities = _extract_modalities(assistant_text)
            metadata = json.dumps({
                "tools_used": tools_used,
                "modalities": modalities,
            }) if (tools_used or modalities) else None

            session.add(ExplorationMessage(
                session_id=session_id, role="assistant", content=assistant_text,
                message_meta=metadata,
            ))
        # Update session timestamp
        explore_session = session.get(ExplorationSession, session_id)
        if explore_session:
            explore_session.updated_at = datetime.utcnow()
        session.commit()


@router.post("/chat")
async def explore_chat(
    req: ExploreRequest,
    session: Session = Depends(get_session),
    user: User = Depends(enforce_usage_limit),
):
    # Create or continue a session
    if req.session_id:
        explore_session = session.get(ExplorationSession, req.session_id)
        if not explore_session or explore_session.user_id != user.id:
            raise HTTPException(status_code=404, detail="Session not found")
    else:
        explore_session = ExplorationSession(user_id=user.id)
        session.add(explore_session)
        session.commit()
        session.refresh(explore_session)

    completed = await _get_completed_lesson_titles(user.id, session)
    available_courses = _build_available_courses(session)
    curriculum_index = _build_curriculum_index(available_courses)

    context = TutorContext(
        lesson_id="",
        lesson_title="",
        lesson_summary="",
        concepts=[],
        completed_lesson_titles=completed,
        mode=req.mode,
        curriculum_index=curriculum_index,
        exploration_mode=True,
        available_courses=available_courses,
    )

    user_message = ""
    for msg in reversed(req.messages):
        if msg.get("role") == "user":
            content = msg.get("content", "")
            if isinstance(content, str):
                user_message = content
            elif isinstance(content, list):
                text_parts = [
                    block.get("text", "")
                    for block in content
                    if isinstance(block, dict) and block.get("type") == "text"
                ]
                user_message = " ".join(text_parts) if text_parts else ""
            break

    generator = run_tutor_agent_loop(req.messages, context)

    return StreamingResponse(
        _stream_with_save(generator, user.id, explore_session.id, user_message),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
            "X-Session-Id": explore_session.id,
        },
    )


@router.get("/sessions", response_model=list[ExplorationSessionResponse])
async def list_sessions(
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    sessions = session.exec(
        select(ExplorationSession)
        .where(ExplorationSession.user_id == user.id)
        .order_by(ExplorationSession.updated_at.desc())
    ).all()
    return sessions


@router.get("/sessions/{session_id}/history", response_model=list[ExplorationMessageResponse])
async def get_session_history(
    session_id: str,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    explore_session = session.get(ExplorationSession, session_id)
    if not explore_session or explore_session.user_id != user.id:
        raise HTTPException(status_code=404, detail="Session not found")

    messages = session.exec(
        select(ExplorationMessage)
        .where(ExplorationMessage.session_id == session_id)
        .order_by(ExplorationMessage.created_at)
    ).all()
    return messages


@router.delete("/sessions/{session_id}")
async def delete_session(
    session_id: str,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    explore_session = session.get(ExplorationSession, session_id)
    if not explore_session or explore_session.user_id != user.id:
        raise HTTPException(status_code=404, detail="Session not found")

    # Delete messages first, then session
    messages = session.exec(
        select(ExplorationMessage)
        .where(ExplorationMessage.session_id == session_id)
    ).all()
    for msg in messages:
        session.delete(msg)
    session.delete(explore_session)
    session.commit()
    return {"ok": True}
