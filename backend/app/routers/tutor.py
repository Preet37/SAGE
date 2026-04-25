import json
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlmodel import Session, select

from ..db import get_session, engine
from ..deps import get_current_user, enforce_usage_limit
from ..models.user import User
from ..models.learning import Lesson, Module, LearningPath
from ..models.progress import UserLessonProgress, ChatMessage, TutorSession
from ..agent.agent_loop import run_tutor_agent_loop
from ..agent.context import TutorContext
from ..schemas.progress import ChatRequest

router = APIRouter(prefix="/tutor", tags=["tutor"])


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


async def _stream_with_save(
    generator, user_id: str, lesson_id: str, session_id: str, user_content: str,
):
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

    with Session(engine) as db:
        db.add(ChatMessage(
            user_id=user_id, lesson_id=lesson_id, session_id=session_id,
            role="user", content=user_content,
        ))
        if assistant_text:
            modalities = _extract_modalities(assistant_text)
            metadata = json.dumps({
                "tools_used": tools_used,
                "modalities": modalities,
            }) if (tools_used or modalities) else None

            db.add(ChatMessage(
                user_id=user_id, lesson_id=lesson_id, session_id=session_id,
                role="assistant", content=assistant_text, message_meta=metadata,
            ))
        tutor_session = db.get(TutorSession, session_id)
        if tutor_session:
            tutor_session.updated_at = datetime.utcnow()
        db.commit()


@router.post("/chat")
async def chat(
    req: ChatRequest,
    session: Session = Depends(get_session),
    user: User = Depends(enforce_usage_limit),
):
    lesson = session.get(Lesson, req.lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    if req.session_id:
        tutor_session = session.get(TutorSession, req.session_id)
        if not tutor_session or tutor_session.user_id != user.id:
            raise HTTPException(status_code=404, detail="Session not found")
    else:
        tutor_session = TutorSession(user_id=user.id, lesson_id=lesson.id)
        session.add(tutor_session)
        session.commit()
        session.refresh(tutor_session)

    completed = await _get_completed_lesson_titles(user.id, session)

    try:
        concepts = json.loads(lesson.concepts)
    except (json.JSONDecodeError, TypeError):
        concepts = []

    domain = "technical"
    module = session.get(Module, lesson.module_id)
    if module:
        lp = session.get(LearningPath, module.learning_path_id)
        if lp:
            domain = lp.title
        all_lessons = session.exec(
            select(Lesson)
            .join(Module, Module.id == Lesson.module_id)
            .where(Module.learning_path_id == module.learning_path_id)
            .order_by(Lesson.order_index)
        ).all()
    else:
        all_lessons = session.exec(select(Lesson)).all()

    curriculum_index = [
        {
            "slug": l.slug,
            "title": l.title,
            "concepts": json.loads(l.concepts) if l.concepts else [],
        }
        for l in all_lessons
    ]

    # Load image metadata: prefer stored (from generation), fall back to disk
    available_images: list[dict] = []
    if lesson.image_metadata:
        try:
            available_images = json.loads(lesson.image_metadata)
        except (json.JSONDecodeError, TypeError):
            pass
    if not available_images and concepts:
        from ..services.course_generator import select_lesson_images, load_wiki_context
        wiki_ctx = load_wiki_context(concepts)
        src_urls = None
        if lesson.sources_used:
            try:
                src_data = json.loads(lesson.sources_used)
                src_urls = [s["url"] if isinstance(s, dict) else s for s in src_data]
            except (json.JSONDecodeError, TypeError):
                pass
        available_images = select_lesson_images(
            wiki_ctx, concepts, source_urls=src_urls, max_images=15,
        )

    context = TutorContext(
        lesson_id=lesson.id,
        lesson_title=lesson.title,
        lesson_summary=lesson.summary,
        concepts=concepts,
        completed_lesson_titles=completed,
        mode=req.mode,
        lesson_content=lesson.content,
        reference_kb=lesson.reference_kb or "",
        curriculum_index=curriculum_index,
        domain=domain,
        available_images=available_images,
    )

    # Extract the plain-text portion of the latest user message for DB storage.
    # Content can be a string or a list of content blocks (e.g. tool_result dicts).
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
        _stream_with_save(generator, user.id, lesson.id, tutor_session.id, user_message),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
            "X-Session-Id": tutor_session.id,
        },
    )
