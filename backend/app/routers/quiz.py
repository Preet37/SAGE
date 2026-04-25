import asyncio
import json
import logging
import random
from fastapi import APIRouter, Depends, HTTPException
from openai import AsyncOpenAI
from sqlmodel import Session, select, col

from ..db import get_session, engine
from ..deps import get_current_user
from ..models.user import User
from ..models.learning import Lesson, Module, LearningPath
from ..models.quiz import QuizSession, QuizQuestion, QuizAnswer
from ..schemas.quiz import (
    QuizGenerateRequest,
    QuizAnswerRequest,
    QuizQuestionResponse,
    QuizAnswerResponse,
    QuizSessionResponse,
    QuizSessionSummary,
    QuizTopicResponse,
    OptionResponse,
)
from ..agent.system_prompt_quiz import build_quiz_prompt
from ..config import get_settings

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/quiz", tags=["quiz"])

_async_client: AsyncOpenAI | None = None


def _get_client() -> AsyncOpenAI:
    global _async_client
    if _async_client is None:
        settings = get_settings()
        _async_client = AsyncOpenAI(
            api_key=settings.llm_api_key,
            base_url=settings.llm_base_url,
        )
    return _async_client


def _parse_options(options_json: str) -> list[OptionResponse]:
    try:
        return [OptionResponse(**o) for o in json.loads(options_json)]
    except Exception:
        return []


def _question_to_response(q: QuizQuestion) -> QuizQuestionResponse:
    return QuizQuestionResponse(
        id=q.id,
        order_index=q.order_index,
        difficulty=q.difficulty,
        question_type=q.question_type,
        question_text=q.question_text,
        options=_parse_options(q.options),
        hint=q.hint,
    )


async def _call_llm_for_questions(
    lesson_title: str,
    lesson_summary: str,
    lesson_content: str,
    concepts: list[str],
    reference_kb: str,
    difficulty: str,
    num_questions: int,
) -> list[dict]:
    """Call the LLM and return parsed question dicts."""
    prompt = build_quiz_prompt(
        lesson_title=lesson_title,
        lesson_summary=lesson_summary,
        lesson_content=lesson_content,
        concepts=concepts,
        reference_kb=reference_kb,
        difficulty=difficulty,
        num_questions=num_questions,
    )

    client = _get_client()
    settings = get_settings()

    response = await client.chat.completions.create(
        model=settings.llm_model,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": "Generate the quiz now."},
        ],
        max_tokens=4096,
        temperature=0.7,
    )

    raw = (response.choices[0].message.content or "").strip()
    if raw.startswith("```"):
        lines = raw.split("\n")
        lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        raw = "\n".join(lines)

    data = json.loads(raw)
    return data.get("questions", [])


def _shuffle_options(q: dict) -> dict:
    """Shuffle option positions so the correct answer isn't always in the same slot."""
    options = q.get("options", [])
    correct_id = q.get("correct_option_id", "")
    if len(options) != 4:
        return q

    correct_text = next((o["text"] for o in options if o["id"] == correct_id), None)
    if not correct_text:
        return q

    texts = [o["text"] for o in options]
    random.shuffle(texts)

    slot_ids = ["a", "b", "c", "d"]
    new_options = [{"id": sid, "text": t} for sid, t in zip(slot_ids, texts)]
    new_correct = next(sid for sid, t in zip(slot_ids, texts) if t == correct_text)

    return {**q, "options": new_options, "correct_option_id": new_correct}


def _save_questions(session_id: str, questions_data: list[dict], start_index: int) -> list[QuizQuestion]:
    """Save question dicts to the DB. Runs in its own session (safe for background tasks)."""
    db_questions = []
    with Session(engine) as db:
        for idx, q in enumerate(questions_data):
            q = _shuffle_options(q)
            question = QuizQuestion(
                session_id=session_id,
                order_index=start_index + idx,
                difficulty=q.get("difficulty", "medium"),
                question_type="multiple_choice",
                question_text=q["question_text"],
                options=json.dumps(q["options"]),
                correct_option_id=q["correct_option_id"],
                hint=q.get("hint", ""),
                explanation=q.get("explanation", ""),
            )
            db.add(question)
            db_questions.append(question)
        db.commit()
        for q in db_questions:
            db.refresh(q)
    return db_questions


async def _generate_remaining_questions(
    session_id: str,
    lesson_title: str,
    lesson_summary: str,
    lesson_content: str,
    concepts: list[str],
    reference_kb: str,
    difficulty: str,
    num_remaining: int,
):
    """Background task: generate remaining questions one at a time, saving each immediately."""
    for i in range(num_remaining):
        try:
            questions_data = await _call_llm_for_questions(
                lesson_title=lesson_title,
                lesson_summary=lesson_summary,
                lesson_content=lesson_content,
                concepts=concepts,
                reference_kb=reference_kb,
                difficulty=difficulty,
                num_questions=1,
            )
            if questions_data:
                _save_questions(session_id, questions_data[:1], start_index=1 + i)
                logger.info("Background question %d/%d ready for session %s", i + 1, num_remaining, session_id)
        except Exception:
            logger.exception("Background question %d failed for session %s", i + 1, session_id)

    with Session(engine) as db:
        quiz_session = db.get(QuizSession, session_id)
        if quiz_session:
            actual_count = len(db.exec(
                select(QuizQuestion).where(QuizQuestion.session_id == session_id)
            ).all())
            quiz_session.total_questions = actual_count
            db.commit()


# ── GET /quiz/topics ─────────────────────────────────────────────────────────

@router.get("/topics", response_model=list[QuizTopicResponse])
async def list_topics(
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    lessons = session.exec(
        select(Lesson, Module, LearningPath)
        .join(Module, Lesson.module_id == Module.id)
        .join(LearningPath, Module.learning_path_id == LearningPath.id)
        .order_by(LearningPath.title, Module.order_index, Lesson.order_index)
    ).all()

    results = []
    for lesson, module, path in lessons:
        try:
            concepts = json.loads(lesson.concepts) if lesson.concepts else []
        except (json.JSONDecodeError, TypeError):
            concepts = []
        results.append(QuizTopicResponse(
            lesson_id=lesson.id,
            lesson_title=lesson.title,
            module_title=module.title,
            path_title=path.title,
            level=path.level,
            concepts=concepts,
        ))
    return results


# ── POST /quiz/generate ──────────────────────────────────────────────────────

@router.post("/generate", response_model=QuizSessionResponse)
async def generate_quiz(
    req: QuizGenerateRequest,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    lesson = session.get(Lesson, req.lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    try:
        concepts = json.loads(lesson.concepts) if lesson.concepts else []
    except (json.JSONDecodeError, TypeError):
        concepts = []

    lesson_title = lesson.title
    lesson_summary = lesson.summary
    lesson_content = lesson.content
    reference_kb = lesson.reference_kb or ""

    # Generate only the first question synchronously for fast response
    try:
        first_questions = await _call_llm_for_questions(
            lesson_title=lesson_title,
            lesson_summary=lesson_summary,
            lesson_content=lesson_content,
            concepts=concepts,
            reference_kb=reference_kb,
            difficulty=req.difficulty,
            num_questions=1,
        )
    except json.JSONDecodeError:
        raise HTTPException(status_code=502, detail="Quiz generation returned invalid format. Please try again.")
    except Exception as e:
        logger.error("LLM quiz generation failed: %s", e)
        raise HTTPException(status_code=502, detail="Quiz generation failed. Please try again.")

    if not first_questions:
        raise HTTPException(status_code=502, detail="No questions were generated. Please try again.")

    quiz_session = QuizSession(
        user_id=user.id,
        lesson_id=lesson.id,
        topic=lesson_title,
        difficulty=req.difficulty,
        total_questions=req.num_questions,
    )
    session.add(quiz_session)
    session.commit()
    session.refresh(quiz_session)

    db_questions = _save_questions(quiz_session.id, first_questions[:1], start_index=0)

    # Kick off background generation for the remaining questions
    num_remaining = req.num_questions - 1
    if num_remaining > 0:
        asyncio.create_task(_generate_remaining_questions(
            session_id=quiz_session.id,
            lesson_title=lesson_title,
            lesson_summary=lesson_summary,
            lesson_content=lesson_content,
            concepts=concepts,
            reference_kb=reference_kb,
            difficulty=req.difficulty,
            num_remaining=num_remaining,
        ))

    return QuizSessionResponse(
        id=quiz_session.id,
        topic=quiz_session.topic,
        difficulty=quiz_session.difficulty,
        total_questions=quiz_session.total_questions,
        correct_count=quiz_session.correct_count,
        completed=quiz_session.completed,
        created_at=quiz_session.created_at,
        questions=[_question_to_response(q) for q in db_questions],
    )


# ── GET /quiz/sessions ───────────────────────────────────────────────────────

@router.get("/sessions", response_model=list[QuizSessionSummary])
async def list_sessions(
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    sessions = session.exec(
        select(QuizSession)
        .where(QuizSession.user_id == user.id)
        .order_by(col(QuizSession.created_at).desc())
    ).all()
    return [
        QuizSessionSummary(
            id=s.id,
            topic=s.topic,
            difficulty=s.difficulty,
            total_questions=s.total_questions,
            correct_count=s.correct_count,
            completed=s.completed,
            created_at=s.created_at,
        )
        for s in sessions
    ]


# ── GET /quiz/sessions/{session_id} ──────────────────────────────────────────

@router.get("/sessions/{session_id}", response_model=QuizSessionResponse)
async def get_session_detail(
    session_id: str,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    quiz_session = session.get(QuizSession, session_id)
    if not quiz_session or quiz_session.user_id != user.id:
        raise HTTPException(status_code=404, detail="Quiz session not found")

    questions = session.exec(
        select(QuizQuestion)
        .where(QuizQuestion.session_id == session_id)
        .order_by(QuizQuestion.order_index)
    ).all()

    return QuizSessionResponse(
        id=quiz_session.id,
        topic=quiz_session.topic,
        difficulty=quiz_session.difficulty,
        total_questions=quiz_session.total_questions,
        correct_count=quiz_session.correct_count,
        completed=quiz_session.completed,
        created_at=quiz_session.created_at,
        questions=[_question_to_response(q) for q in questions],
    )


# ── POST /quiz/sessions/{session_id}/answer ──────────────────────────────────

@router.post("/sessions/{session_id}/answer", response_model=QuizAnswerResponse)
async def submit_answer(
    session_id: str,
    req: QuizAnswerRequest,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    quiz_session = session.get(QuizSession, session_id)
    if not quiz_session or quiz_session.user_id != user.id:
        raise HTTPException(status_code=404, detail="Quiz session not found")

    question = session.get(QuizQuestion, req.question_id)
    if not question or question.session_id != session_id:
        raise HTTPException(status_code=404, detail="Question not found in this quiz")

    existing = session.exec(
        select(QuizAnswer)
        .where(QuizAnswer.question_id == req.question_id)
        .where(QuizAnswer.session_id == session_id)
    ).first()
    if existing:
        return QuizAnswerResponse(
            is_correct=existing.is_correct,
            correct_option_id=question.correct_option_id,
            explanation=question.explanation,
            correct_count=quiz_session.correct_count,
            completed=quiz_session.completed,
        )

    is_correct = req.selected_option_id == question.correct_option_id

    answer = QuizAnswer(
        question_id=question.id,
        session_id=session_id,
        selected_option_id=req.selected_option_id,
        is_correct=is_correct,
    )
    session.add(answer)

    if is_correct:
        quiz_session.correct_count += 1

    total_answered = session.exec(
        select(QuizAnswer)
        .where(QuizAnswer.session_id == session_id)
    ).all()
    if len(total_answered) + 1 >= quiz_session.total_questions:
        quiz_session.completed = True

    session.commit()
    session.refresh(quiz_session)

    return QuizAnswerResponse(
        is_correct=is_correct,
        correct_option_id=question.correct_option_id,
        explanation=question.explanation,
        correct_count=quiz_session.correct_count,
        completed=quiz_session.completed,
    )


# ── DELETE /quiz/sessions/{session_id} ────────────────────────────────────────

@router.delete("/sessions/{session_id}")
async def delete_session(
    session_id: str,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    quiz_session = session.get(QuizSession, session_id)
    if not quiz_session or quiz_session.user_id != user.id:
        raise HTTPException(status_code=404, detail="Quiz session not found")

    answers = session.exec(
        select(QuizAnswer).where(QuizAnswer.session_id == session_id)
    ).all()
    for a in answers:
        session.delete(a)

    questions = session.exec(
        select(QuizQuestion).where(QuizQuestion.session_id == session_id)
    ).all()
    for q in questions:
        session.delete(q)

    session.delete(quiz_session)
    session.commit()
    return {"ok": True}
