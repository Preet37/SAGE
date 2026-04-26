"""
Notes router — AI-powered note revision for students.
Students write notes; AI reviews, enriches, identifies gaps,
and suggests concept connections.
"""
import json
import logging
import re
from fastapi import APIRouter, Depends, HTTPException
from openai import AsyncOpenAI
from pydantic import BaseModel
from sqlmodel import Session, select
from typing import Optional

from ..db import get_session
from ..deps import get_current_user
from ..models.learning import Lesson
from ..models.user import User
from ..config import get_settings

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/notes", tags=["notes"])

_async_client: AsyncOpenAI | None = None


def _get_client() -> AsyncOpenAI:
    global _async_client
    if _async_client is None:
        settings = get_settings()
        if not settings.llm_api_key:
            raise HTTPException(status_code=503, detail="LLM not configured.")
        _async_client = AsyncOpenAI(
            api_key=settings.llm_api_key,
            base_url=settings.llm_base_url,
        )
    return _async_client


class NoteReviseRequest(BaseModel):
    lesson_id: str
    content: str
    lesson_title: Optional[str] = None
    concepts: Optional[list[str]] = None


class NoteRevisionResponse(BaseModel):
    original: str
    revised: str
    gaps_identified: list[str]
    concept_connections: list[dict]
    misconceptions: list[str]
    strength_score: float
    suggestions: list[str]


def _extract_json(raw: str) -> dict:
    raw = raw.strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        pass
    stripped = re.sub(r"^```[a-zA-Z]*\n?", "", raw)
    stripped = re.sub(r"\n?```$", "", stripped.rstrip()).strip()
    try:
        return json.loads(stripped)
    except json.JSONDecodeError:
        pass
    match = re.search(r"\{[\s\S]*\}", stripped)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass
    raise ValueError("Could not extract valid JSON from LLM response")


@router.post("/revise", response_model=NoteRevisionResponse)
async def revise_notes(
    req: NoteReviseRequest,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    """AI reviews student notes and returns enriched revision with analysis."""
    # Try to load lesson context
    lesson = session.get(Lesson, req.lesson_id)
    lesson_title = req.lesson_title or (lesson.title if lesson else "this lesson")
    concepts_str = ", ".join(req.concepts or [])
    if not concepts_str and lesson:
        try:
            concepts_str = ", ".join(json.loads(lesson.concepts or "[]"))
        except Exception:
            pass

    prompt = f"""You are SAGE's Note Revision Agent reviewing a student's notes on "{lesson_title}".
Key concepts in this lesson: {concepts_str or "general concepts"}

Student notes (up to 800 chars shown):
{req.content[:800]}

Review the notes and return ONLY this JSON object — no markdown fences, no commentary:
{{
  "revised": "Improved, enriched markdown version of the student's notes. Fix errors, add missing context, improve clarity. Use $...$ for inline math and $$...$$ for block equations.",
  "gaps_identified": ["Missing concept or topic 1", "Missing concept 2"],
  "concept_connections": [
    {{"from": "term from their notes", "to": "related concept", "relationship": "how they connect"}}
  ],
  "misconceptions": ["Incorrect statement if any"],
  "strength_score": 0.65,
  "suggestions": ["Actionable improvement tip 1", "Actionable tip 2"]
}}

Rules:
- strength_score: 0.0 (very weak) to 1.0 (excellent). Be honest.
- gaps_identified: concepts from the lesson not covered in their notes
- misconceptions: only include if there are actual factual errors
- suggestions: concrete, actionable, specific to their notes
- revised: make it genuinely better — expand explanations, add examples, use correct terminology
"""

    client = _get_client()
    settings = get_settings()

    try:
        response = await client.chat.completions.create(
            model=settings.llm_model,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": "Review my notes and return the JSON."},
            ],
            max_tokens=2048,
            temperature=0.3,
            response_format={"type": "json_object"},
        )
        raw = (response.choices[0].message.content or "").strip()
    except Exception:
        # Retry without json_object mode
        try:
            response = await client.chat.completions.create(
                model=settings.llm_model,
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": "Review my notes and return only the JSON object."},
                ],
                max_tokens=2048,
                temperature=0.3,
            )
            raw = (response.choices[0].message.content or "").strip()
        except Exception as e:
            logger.error("Notes revision LLM failed: %s", e)
            raise HTTPException(status_code=502, detail="Note revision failed. Please try again.")

    try:
        data = _extract_json(raw)
    except ValueError:
        logger.error("Failed to parse notes revision JSON: %s", raw[:400])
        raise HTTPException(status_code=502, detail="Note revision returned invalid format.")

    return NoteRevisionResponse(
        original=req.content,
        revised=data.get("revised", req.content),
        gaps_identified=data.get("gaps_identified", []),
        concept_connections=data.get("concept_connections", []),
        misconceptions=data.get("misconceptions", []),
        strength_score=min(1.0, max(0.0, float(data.get("strength_score", 0.5)))),
        suggestions=data.get("suggestions", []),
    )
