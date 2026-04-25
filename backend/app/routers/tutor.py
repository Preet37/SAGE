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
from app.core.cognition import cognition_retrieve, llm_judge, CognitionTrace
from app.core.verification import verify_response
from app.core.voice import synthesize_speech
from app.config import get_settings, load_yaml_config
from app.routers.accessibility import get_user_accessibility_modifier
from app.agents.orchestrator import AgentOrchestrator
from app.agents.director_agent import director_badge_payload, DEEP_DIVE_COST_MICRO_ASI
import httpx
import secrets

router = APIRouter(prefix="/tutor", tags=["tutor"])
settings = get_settings()
yaml_cfg = load_yaml_config()

# ---------------------------------------------------------------------------
# Language instructions — injected into system prompt when a non-English
# language is detected. The LLM will respond entirely in the target language.
# ---------------------------------------------------------------------------

LANGUAGE_INSTRUCTIONS: dict[str, str] = {
    "ar": "Respond ENTIRELY in Arabic (العربية). All explanations, questions, and feedback must be in Arabic.",
    "hi": "Respond ENTIRELY in Hindi (हिन्दी). All explanations, questions, and feedback must be in Hindi.",
    "sw": "Respond ENTIRELY in Swahili (Kiswahili). All explanations, questions, and feedback must in Swahili.",
    "tl": "Respond ENTIRELY in Tagalog. All explanations, questions, and feedback must be in Tagalog.",
    "es": "Respond ENTIRELY in Spanish (Español).",
    "fr": "Respond ENTIRELY in French (Français).",
    "zh": "Respond ENTIRELY in Chinese (中文).",
    "pt": "Respond ENTIRELY in Portuguese (Português).",
    "ur": "Respond ENTIRELY in Urdu (اردو).",
    "bn": "Respond ENTIRELY in Bengali (বাংলা).",
}

# Crisis keywords across multiple languages — triggers trauma-informed mode
CRISIS_KEYWORDS: frozenset[str] = frozenset({
    "displaced", "refugee", "fled", "camp", "shelter", "bombs", "war", "conflict",
    "can't stay", "lost my home", "no school", "left school", "not safe",
    "hunger", "no food", "no water", "evacuat",
    # Arabic
    "مخيم", "لاجئ", "مهاجر", "نازح",
    # Hindi
    "शरणार्थी", "विस्थापित",
    # Swahili
    "mkimbizi", "kambi", "wakimbizi",
})

CRISIS_SUPPORT_SECTION = """## Crisis-Aware Teaching Mode
This student may be experiencing displacement or conflict. Apply trauma-informed pedagogy:
- Keep responses SHORT (under 100 words)
- Begin with a warm, human acknowledgement
- Focus on ONE small concept at a time
- Never reference equipment, resources, or things they may not have
- Be gentle, patient, and affirming
- End with: "📚 Free learning: [Khan Academy Lite](https://lite.khanacademy.org) | [UNHCR Education](https://www.unhcr.org/what-we-do/build-better-futures/education)"
"""

LOW_DATA_SECTION = """## Data-Saving Mode (2G / Limited Bandwidth)
The student has very limited mobile data. Strict rules:
- Maximum 80 words per response
- No markdown tables, no code blocks longer than 5 lines
- No image or diagram references
- Ask ONLY one question per response
- Use the simplest possible vocabulary
"""

READING_LEVEL_SECTION = """## Reading Level Auto-Calibration
Detect the student's apparent reading level from their vocabulary and sentence structure:
- Very basic / young child → Grade 3-4 language (short sentences, everyday words only)
- Middle school → Grade 6-8 language
- High school / adult → Grade 9-12 language
- Advanced → college level language
Silently match your response complexity to the student's apparent level without mentioning it.
"""

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

{language_section}

{accessibility_section}

{crisis_section}

{low_data_section}

{reading_level_section}

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
    image_url: Optional[str] = None
    extracted_text: Optional[str] = None
    deep_dive_token: Optional[str] = None
    # Accessibility / context overrides
    language: str = ""          # BCP-47 code e.g. "ar", "hi", "sw"; "" = use user profile
    low_data_mode: bool = False  # Enable 2G / data-saving constraints
    crisis_mode: bool = False   # Manually activate trauma-informed mode


class SessionCreateRequest(BaseModel):
    lesson_id: int
    teaching_mode: str = "default"


@router.post("/session")
async def create_session(
    req: SessionCreateRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    lesson_result = await db.execute(select(Lesson).where(Lesson.id == req.lesson_id))
    if not lesson_result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Lesson not found")

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

    # Cognition track — HyDE + cosine + cross-encoder rerank
    cognition_trace = await cognition_retrieve(req.message, req.lesson_id, db, top_k=4)
    kb_chunks = [c.text for c in cognition_trace.retrieved]
    if not kb_chunks:
        kb_chunks = await get_relevant_chunks(req.message, req.lesson_id, db, top_k=4)
    kb_context = "\n\n---\n\n".join(kb_chunks) if kb_chunks else lesson.content_md[:2000]

    # If the student attached an image and we OCR'd it, prepend that text to
    # the KB context so the tutor sees it without us shipping the image bytes
    # to a vision model.
    if req.extracted_text:
        kb_context = (
            f"## Student-Uploaded Image (OCR text)\n{req.extracted_text[:1200]}\n\n"
            + kb_context
        )

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

    # ── Language section ────────────────────────────────────────────────────
    lang_code = req.language or getattr(user, "preferred_language", "en") or "en"
    # Normalise: "en-US" → "en", "ar-SA" → "ar"
    lang_code = lang_code.split("-")[0].lower()
    lang_instruction = LANGUAGE_INSTRUCTIONS.get(lang_code, "")
    language_section = f"## Language\n{lang_instruction}" if lang_instruction else ""

    # ── Crisis detection ────────────────────────────────────────────────────
    all_text = " ".join(
        [req.message] + [m.content for m in req.history[-4:]]
    ).lower()
    crisis_detected = req.crisis_mode or any(kw in all_text for kw in CRISIS_KEYWORDS)
    crisis_section = CRISIS_SUPPORT_SECTION if crisis_detected else ""

    # ── Low-data mode ───────────────────────────────────────────────────────
    low_data_section = LOW_DATA_SECTION if req.low_data_mode else ""

    # ── Reading level ───────────────────────────────────────────────────────
    # Always inject — the LLM auto-calibrates silently
    reading_level_section = READING_LEVEL_SECTION

    system_prompt = SYSTEM_PROMPT_TEMPLATE.format(
        mode_instruction=mode_instruction,
        language_section=language_section,
        accessibility_section=accessibility_section,
        crisis_section=crisis_section,
        low_data_section=low_data_section,
        reading_level_section=reading_level_section,
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
        "events": [],
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
            cognition_trace=cognition_trace,
            agent_trace=agent_trace,
            voice_enabled=req.voice_enabled,
            crisis_detected=crisis_detected,
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
    cognition_trace: CognitionTrace,
    agent_trace: dict,
    voice_enabled: bool,
    crisis_detected: bool,
    db: AsyncSession,
) -> AsyncGenerator[str, None]:
    full_response = ""
    search_was_called = False

    try:
        try:
            orchestrator_result = await asyncio.wait_for(
                AgentOrchestrator(
                    user_id=user.id,
                    lesson_id=lesson.id,
                    question=messages[-1]["content"],
                    history=messages[:-1],
                ).run(),
                timeout=8.0,
            )
            pedagogy = orchestrator_result.get("pedagogy", {})
            content = orchestrator_result.get("content", {})
            concept_map = orchestrator_result.get("concept_map", {})
            assessment = orchestrator_result.get("assessment", {})
            peer_match = orchestrator_result.get("peer_match", {})
            progress = orchestrator_result.get("progress", {})
            agent_events = [
                {
                    "type": "pedagogy_applied",
                    "mode": pedagogy.get("recommended_mode", agent_trace["pedagogy"]),
                    "engagement": pedagogy.get("engagement_level"),
                    "misconception": pedagogy.get("misconception_detected"),
                },
                {
                    "type": "content_retrieved",
                    "chunks": len(kb_chunks),
                    "key_terms": content.get("key_terms", []),
                    "focus": content.get("content_focus"),
                },
                {
                    "type": "concept_map_updated",
                    "lesson_id": lesson.id,
                    "concepts_touched": concept_map.get("concepts_touched", []),
                    "mastery_delta": concept_map.get("suggested_mastery_update", 0.0),
                },
                {
                    "type": "assessment_check",
                    "should_quiz": assessment.get("should_quiz", False),
                    "difficulty": assessment.get("difficulty"),
                    "concept": assessment.get("concept_to_test"),
                },
                {
                    "type": "peer_match_check",
                    "recommended": peer_match.get("peer_match_recommended", False),
                    "reasoning": peer_match.get("reasoning"),
                },
                {
                    "type": "progress_updated",
                    "signal": progress.get("progress_signal"),
                    "mastered_concepts": agent_trace.get("mastered_concepts", 0),
                    "encouragement": progress.get("encouragement"),
                },
            ]
        except Exception as _orch_err:
            import logging
            logging.getLogger(__name__).warning(
                "AgentOrchestrator failed, using static fallback: %s", _orch_err
            )
            agent_events = [
                {"type": "content_retrieved", "chunks": len(kb_chunks)},
                {"type": "pedagogy_applied", "mode": agent_trace["pedagogy"]},
                {
                    "type": "concept_map_updated",
                    "lesson_id": lesson.id,
                    "concepts": lesson.key_concepts[:6],
                },
                {
                    "type": "assessment_check",
                    "quiz": "eligible" if len(messages) >= 3 else "not_yet",
                },
                {"type": "peer_match_check", "recommended": len(kb_chunks) == 0},
                {
                    "type": "progress_updated",
                    "mastered_concepts": agent_trace.get("mastered_concepts", 0),
                },
            ]
        agent_trace["events"] = agent_events
        for event in agent_events:
            yield _sse("agent_event", event)

        # Fetch.ai Bureau badge — proves agents are real, not just labels
        badge = director_badge_payload()
        if agent_trace["pedagogy"] == "deep_dive":
            badge["payment"] = {
                "amount_micro_asi": DEEP_DIVE_COST_MICRO_ASI,
                "token": secrets.token_urlsafe(8),
                "ts": datetime.utcnow().isoformat(),
            }
        yield _sse("fetchai_badge", badge)

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

        # Cognition track — LLM-as-judge runs after the answer is finalized.
        # Streamed in parallel with TTS so it doesn't block voice playback.
        try:
            judge = await llm_judge(
                question=messages[-1]["content"],
                answer=full_response,
                sources=cognition_trace.retrieved,
            )
            agent_trace["judge"] = {
                "score": judge.score,
                "grounded": judge.grounded,
                "reasoning": judge.reasoning,
                "citations": judge.citations,
            }
            yield _sse("judge_result", {
                **cognition_trace.to_payload(),
                "judge": agent_trace["judge"],
            })
        except Exception as _judge_err:
            yield _sse("judge_result", {
                **cognition_trace.to_payload(),
                "judge": {
                    "score": 0.5,
                    "grounded": False,
                    "reasoning": f"judge error: {_judge_err}",
                    "citations": [],
                },
            })

        if voice_enabled and settings.elevenlabs_api_key:
            audio_bytes = await synthesize_speech(full_response)
            if audio_bytes:
                import base64
                yield _sse("audio", {"data": base64.b64encode(audio_bytes).decode()})

        if session_id:
            session = await db.get(TutorSession, session_id)
            if session and session.user_id == user.id:
                decisions = list(session.agent_decisions or [])
                decisions.append(agent_trace)
                session.agent_decisions = decisions
                db.add(session)
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

        yield _sse("done", {
            "response": full_response,
            "agent_trace": agent_trace,
            "crisis_detected": crisis_detected,
        })

    except Exception as e:
        yield _sse("error", {"message": str(e)})


async def _stream_anthropic(system_prompt: str, messages: list[dict]) -> AsyncGenerator[str, None]:
    import anthropic as anth
    client = anth.AsyncAnthropic(api_key=settings.llm_api_key, timeout=30.0, max_retries=2)
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

    client = AsyncOpenAI(base_url=base_url, api_key=api_key, timeout=30.0, max_retries=2)
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
