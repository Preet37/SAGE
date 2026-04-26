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
from ..agent.slash_commands import parse_slash_command, list_commands
from ..config import get_settings
from ..schemas.progress import ChatRequest
from ..services.semantic_memory import (
    memory_block_for_prompt,
    record_memory,
)
from ..services.learner_profile import profile_summary_for_prompt

router = APIRouter(prefix="/tutor", tags=["tutor"])


@router.get("/slash-commands")
def slash_command_catalog():
    """Public catalog used by the frontend autocomplete."""
    return {"commands": list_commands()}


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
    if re.search(r"<artifact>", text):
        modalities.append("artifact")
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
    verification: dict | None = None

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
                elif event.get("type") == "verification":
                    verification = event.get("result")
        except Exception:
            pass

    with Session(engine) as db:
        db.add(ChatMessage(
            user_id=user_id, lesson_id=lesson_id, session_id=session_id,
            role="user", content=user_content,
        ))
        if assistant_text:
            modalities = _extract_modalities(assistant_text)
            meta_payload: dict = {}
            if tools_used:
                meta_payload["tools_used"] = tools_used
            if modalities:
                meta_payload["modalities"] = modalities
            if verification:
                meta_payload["verification"] = verification
            metadata = json.dumps(meta_payload) if meta_payload else None

            db.add(ChatMessage(
                user_id=user_id, lesson_id=lesson_id, session_id=session_id,
                role="assistant", content=assistant_text, message_meta=metadata,
            ))
        tutor_session = db.get(TutorSession, session_id)
        if tutor_session:
            tutor_session.updated_at = datetime.utcnow()
        db.commit()

    # Persist to semantic memory (best-effort, async-safe).
    settings = get_settings()
    if settings.feature_semantic_memory:
        if user_content:
            record_memory(
                user_id=user_id, role="user", content=user_content,
                lesson_id=lesson_id, session_id=session_id,
            )
        if assistant_text:
            record_memory(
                user_id=user_id, role="assistant", content=assistant_text,
                lesson_id=lesson_id, session_id=session_id,
            )


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
        user_id=user.id,
        session_id=tutor_session.id,
        slash_instruction=cmd.instruction if cmd else "",
        learner_profile=profile_summary_for_prompt(user.id),
    )

    # Extract the plain-text portion of the latest user message for DB storage.
    # Content can be a string or a list of content blocks (e.g. tool_result dicts).
    user_message = ""
    last_user_idx: int | None = None
    for i in range(len(req.messages) - 1, -1, -1):
        msg = req.messages[i]
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
            last_user_idx = i
            break

    # Slash-command detection — strip the command from the visible message and
    # pass the behavioral instruction through TutorContext.
    cmd, remainder = parse_slash_command(user_message)
    if cmd is not None and last_user_idx is not None:
        context_message = remainder or f"(/{cmd.name})"
        # Persist the cleaned message for DB storage and inject it into the
        # outgoing API messages so the LLM doesn't see the literal slash.
        user_message = context_message
        target = req.messages[last_user_idx]
        if isinstance(target.get("content"), str):
            target["content"] = context_message
        elif isinstance(target.get("content"), list):
            for block in target["content"]:
                if isinstance(block, dict) and block.get("type") == "text":
                    block["text"] = context_message
                    break

    settings = get_settings()
    if settings.feature_semantic_memory and user_message:
        context.memory_block = memory_block_for_prompt(
            user_id=user.id,
            query=user_message,
            lesson_id=lesson.id,
            current_session_id=tutor_session.id,
        )

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


# ── Voice intent detection ────────────────────────────────────────────────────
import re as _re
from openai import AsyncOpenAI as _AsyncOpenAI
from pydantic import BaseModel as _BaseModel
from typing import Optional as _Optional

class VoiceIntentRequest(_BaseModel):
    transcript: str
    page_type: _Optional[str] = None
    page_title: _Optional[str] = None
    topic: _Optional[str] = None

class VoiceIntentResponse(_BaseModel):
    action: str   # "navigate"|"open_graph"|"add_note"|"open_quiz"|"open_chat"|"mark_complete"|"none"
    path: _Optional[str] = None
    note_content: _Optional[str] = None
    explanation: _Optional[str] = None

_INTENT_PROMPT = """You are an intent classifier for an AI tutoring app called SAGE.
Given a student's voice message, determine what UI action (if any) the agent should take.

Available pages (for navigate):
- /learn — learning paths dashboard
- /explore — explore topics/concepts
- /network — real-time learner network
- /pocket — on-device AI pocket tutor
- /galaxy — knowledge galaxy ranking
- /documents — my uploaded documents
- /create — create a new course

Available actions:
- navigate: go to a page
- open_graph: open the interactive simulation/graph for the current lesson
- add_note: add a written note (provide note_content)
- open_quiz: switch to the quiz tab
- open_chat: switch to the tutor chat tab
- mark_complete: mark current lesson complete
- none: no UI action needed, just speak

Current context: page={page_type}, title="{page_title}", topic="{topic}"

Respond with a single JSON object:
{{
  "action": "<action>",
  "path": "<path or null>",
  "note_content": "<note text or null>",
  "explanation": "<brief reason>"
}}

Student message: "{transcript}"
"""

@router.post("/voice-intent", response_model=VoiceIntentResponse)
async def detect_voice_intent(req: VoiceIntentRequest):
    """Detect and return the UI action implied by a voice message."""
    settings = get_settings()
    client = _AsyncOpenAI(api_key=settings.llm_api_key, base_url=settings.llm_base_url)
    prompt = _INTENT_PROMPT.format(
        page_type=req.page_type or "unknown",
        page_title=req.page_title or "",
        topic=req.topic or "",
        transcript=req.transcript,
    )
    try:
        resp = await client.chat.completions.create(
            model=settings.llm_model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            max_tokens=200,
        )
        raw = resp.choices[0].message.content or ""
        # Extract JSON block
        m = _re.search(r'\{.*\}', raw, _re.DOTALL)
        if m:
            data = json.loads(m.group())
            return VoiceIntentResponse(
                action=data.get("action", "none"),
                path=data.get("path"),
                note_content=data.get("note_content"),
                explanation=data.get("explanation"),
            )
    except Exception:
        pass
    return VoiceIntentResponse(action="none")
