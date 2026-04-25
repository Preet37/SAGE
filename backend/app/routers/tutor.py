"""
Main Socratic tutor endpoint with SSE streaming.
Integrates: semantic retrieval (Cognition), output verification (Cognition),
agent orchestration (Fetch.ai), voice synthesis, session replay.
"""
import json
import asyncio
from datetime import datetime
from typing import AsyncGenerator, Optional
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from app.database import get_db
from app.models.user import User
from app.models.lesson import Lesson, Course
from app.models.session import TutorSession, TutorMessage
from app.models.concept import ConceptNode, StudentMastery
from app.routers.auth import get_current_user
from app.core.retrieval import get_relevant_chunks
from app.core.verification import verify_response
from app.core.voice import synthesize_speech
from app.config import get_settings, load_yaml_config
from app.routers.accessibility import get_user_accessibility_modifier
import httpx

router = APIRouter(prefix="/tutor", tags=["tutor"])
settings = get_settings()
yaml_cfg = load_yaml_config()

TEACHING_MODE_PROMPTS = {
    "default": "Use the Socratic method: ask guiding questions, build on the student's reasoning. Never just give the answer.",
    "eli5": "Explain everything using simple everyday language and concrete examples a 10-year-old would understand.",
    "analogy": "Always use real-world analogies and comparisons to build intuition before technical details.",
    "code": "Prioritize code examples. Show working code first, then explain the concepts.",
    "deep_dive": "Go deep into mathematical foundations, formal notation, and edge cases. Assume strong technical background.",
}

SYSTEM_PROMPT_TEMPLATE = """You are SAGE, an expert Socratic AI tutor for technical subjects.

## Your Teaching Approach
{mode_instruction}

{accessibility_section}

## Current Lesson
**Course:** {course_title}
**Lesson:** {lesson_title}
**Key Concepts:** {key_concepts}

## Reference Knowledge Base (use this as your primary source)
{kb_context}

## Rules
1. NEVER fabricate URLs or citations. Only include links if a search tool returned them.
2. Build on what the student already knows — ask before you tell.
3. When generating a quiz, use this exact format: <quiz>{{"question": "...", "options": ["A", "B", "C", "D"], "answer": "A", "explanation": "..."}}</quiz>
4. Keep responses focused — 150-300 words unless the student asks for depth.
5. If you don't know something from the KB, say so clearly.
6. Celebrate progress genuinely, but don't be sycophantic.

## Student Progress
Concepts mastered: {mastered_concepts}
Current teaching mode: {teaching_mode}
"""


class ChatMessage(BaseModel):
    role: str
    content: str


class TutorRequest(BaseModel):
    lesson_id: int
    message: str
    history: list[ChatMessage] = []
    session_id: Optional[int] = None
    teaching_mode: Optional[str] = None
    voice_enabled: bool = False


class SessionCreateRequest(BaseModel):
    lesson_id: int
    teaching_mode: str = "default"


@router.post("/session")
async def create_session(
    req: SessionCreateRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    session = TutorSession(
        user_id=user.id,
        lesson_id=req.lesson_id,
        teaching_mode=req.teaching_mode,
    )
    db.add(session)
    await db.commit()
    await db.refresh(session)
    return {"session_id": session.id}


@router.post("/chat")
async def chat(
    req: TutorRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Main Socratic chat endpoint. Returns SSE stream."""
    lesson_result = await db.execute(select(Lesson).where(Lesson.id == req.lesson_id))
    lesson = lesson_result.scalar_one_or_none()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    course_result = await db.execute(select(Course).where(Course.id == lesson.course_id))
    course = course_result.scalar_one_or_none()

    teaching_mode = req.teaching_mode or user.teaching_mode or "default"
    mode_instruction = TEACHING_MODE_PROMPTS.get(teaching_mode, TEACHING_MODE_PROMPTS["default"])

    kb_chunks = await get_relevant_chunks(req.message, req.lesson_id, db, top_k=4)
    kb_context = "\n\n---\n\n".join(kb_chunks) if kb_chunks else lesson.content_md[:2000]

    mastery_result = await db.execute(
        select(ConceptNode, StudentMastery)
        .join(StudentMastery, ConceptNode.id == StudentMastery.concept_id, isouter=True)
        .where(ConceptNode.course_id == lesson.course_id)
        .where(StudentMastery.user_id == user.id)
        .where(StudentMastery.is_mastered == True)
    )
    mastered = [row[0].label for row in mastery_result.all()]

    accessibility_modifier = get_user_accessibility_modifier(user)
    accessibility_section = (
        f"## Accessibility Requirements\n{accessibility_modifier}"
        if accessibility_modifier
        else ""
    )

    system_prompt = SYSTEM_PROMPT_TEMPLATE.format(
        mode_instruction=mode_instruction,
        accessibility_section=accessibility_section,
        course_title=course.title if course else "",
        lesson_title=lesson.title,
        key_concepts=", ".join(lesson.key_concepts),
        kb_context=kb_context[:3000],
        mastered_concepts=", ".join(mastered) if mastered else "None yet",
        teaching_mode=teaching_mode,
    )

    messages = [{"role": m.role, "content": m.content} for m in req.history]
    messages.append({"role": "user", "content": req.message})

    agent_trace = {
        "pedagogy": teaching_mode,
        "retrieved_chunks": len(kb_chunks),
        "mastered_concepts": len(mastered),
        "timestamp": datetime.utcnow().isoformat(),
    }

    return StreamingResponse(
        _stream_response(
            system_prompt=system_prompt,
            messages=messages,
            user=user,
            lesson=lesson,
            session_id=req.session_id,
            kb_chunks=kb_chunks,
            agent_trace=agent_trace,
            voice_enabled=req.voice_enabled,
            db=db,
        ),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


async def _stream_response(
    system_prompt: str,
    messages: list[dict],
    user: User,
    lesson: Lesson,
    session_id: Optional[int],
    kb_chunks: list[str],
    agent_trace: dict,
    voice_enabled: bool,
    db: AsyncSession,
) -> AsyncGenerator[str, None]:
    full_response = ""
    search_was_called = False

    try:
        yield _sse("agent_event", {"type": "content_retrieved", "chunks": len(kb_chunks)})
        yield _sse("agent_event", {"type": "pedagogy_applied", "mode": agent_trace["pedagogy"]})

        if settings.llm_provider == "anthropic":
            async for chunk in _stream_anthropic(system_prompt, messages):
                full_response += chunk
                yield _sse("token", {"content": chunk})
        else:
            async for chunk in _stream_openai(system_prompt, messages):
                full_response += chunk
                yield _sse("token", {"content": chunk})

        verification = verify_response(full_response, kb_chunks, search_was_called)
        agent_trace["verification"] = {
            "passed": verification.passed,
            "flags": verification.flags,
            "score": verification.score,
        }

        yield _sse("verification", {
            "passed": verification.passed,
            "flags": verification.flags,
            "score": verification.score,
        })

        if voice_enabled and settings.elevenlabs_api_key:
            audio_bytes = await synthesize_speech(full_response)
            if audio_bytes:
                import base64
                yield _sse("audio", {"data": base64.b64encode(audio_bytes).decode()})

        if session_id:
            msg = TutorMessage(
                session_id=session_id,
                role="user",
                content=messages[-1]["content"],
                retrieved_chunks=[c[:200] for c in kb_chunks],
                verification_passed=verification.passed,
                verification_flags=verification.flags,
                agent_trace=agent_trace,
            )
            db.add(msg)
            reply_msg = TutorMessage(
                session_id=session_id,
                role="assistant",
                content=full_response,
                verification_passed=verification.passed,
                verification_flags=verification.flags,
                agent_trace=agent_trace,
            )
            db.add(reply_msg)
            await db.commit()

        yield _sse("done", {"response": full_response, "agent_trace": agent_trace})

    except Exception as e:
        yield _sse("error", {"message": str(e)})


async def _stream_anthropic(system_prompt: str, messages: list[dict]) -> AsyncGenerator[str, None]:
    import anthropic as anth
    client = anth.AsyncAnthropic(api_key=settings.llm_api_key)
    model = yaml_cfg.get("models", {}).get("tutor", {}).get("anthropic", "claude-sonnet-4-5")

    async with client.messages.stream(
        model=model,
        max_tokens=1024,
        system=system_prompt,
        messages=messages,
    ) as stream:
        async for text in stream.text_stream:
            yield text


async def _stream_openai(system_prompt: str, messages: list[dict]) -> AsyncGenerator[str, None]:
    from openai import AsyncOpenAI
    provider = settings.llm_provider
    if provider == "asi1":
        base_url = yaml_cfg["llm"]["asi1_base"]
        api_key = settings.asi1_api_key
        model = yaml_cfg.get("models", {}).get("tutor", {}).get("asi1", "asi1-mini")
    elif provider == "groq":
        base_url = yaml_cfg["llm"]["groq_base"]
        api_key = settings.llm_api_key
        model = yaml_cfg.get("models", {}).get("tutor", {}).get("groq", "llama-3.3-70b-versatile")
    else:
        base_url = yaml_cfg["llm"]["openai_base"]
        api_key = settings.llm_api_key
        model = yaml_cfg.get("models", {}).get("tutor", {}).get("openai", "gpt-4o")

    client = AsyncOpenAI(base_url=base_url, api_key=api_key)
    all_messages = [{"role": "system", "content": system_prompt}] + messages

    stream = await client.chat.completions.create(
        model=model,
        messages=all_messages,
        max_tokens=1024,
        stream=True,
    )
    async for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            yield delta


def _sse(event: str, data: dict) -> str:
    return f"event: {event}\ndata: {json.dumps(data)}\n\n"
