"""Lesson plan generator — turns a topic into a structured lesson + quiz.

Uses Gemini when `GEMINI_API_KEY` is set, otherwise falls back to the shared
`LLM.from_env()` (Anthropic → ASI1 → stub). The endpoint is intentionally
unauthenticated so the landing-page → first-lesson flow works without a
sign-in step.
"""

from __future__ import annotations

import json
import os
import re
from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.agents.base import LLM

router = APIRouter(prefix="/lesson", tags=["lesson"])


class LessonRequest(BaseModel):
    topic: str = Field(min_length=1, max_length=200)


SYSTEM_PROMPT = """You design short, interactive lessons for learners.
Output STRICT JSON only — no markdown fences, no commentary.

Schema:
{
  "topic": string,
  "summary": string (1 sentence),
  "steps": [
    { "title": string, "content": string (2-4 sentences, plain prose) }
  ],   // exactly 4 steps, ordered from intuition to formal
  "quiz": [
    {
      "question": string,
      "options": [string, string, string, string],
      "correct_index": 0|1|2|3,
      "explanation": string
    }
  ]    // exactly 3 questions
}
"""


def _fallback_lesson(topic: str) -> dict[str, Any]:
    return {
        "topic": topic,
        "summary": f"A short guided lesson on {topic}.",
        "steps": [
            {"title": f"What is {topic}?", "content": f"Begin with the intuition behind {topic}. Why does it matter and where does it show up?"},
            {"title": "Core idea", "content": f"The central principle of {topic} can be summarized in one mental model. Try to picture it."},
            {"title": "Worked example", "content": f"Trace through a concrete example of {topic} step by step. Notice which variables drive the outcome."},
            {"title": "Connections", "content": f"How does {topic} connect to ideas you already know? What does it generalize, and what generalizes it?"},
        ],
        "quiz": [
            {
                "question": f"Which best describes {topic}?",
                "options": ["A foundational concept", "An unrelated detail", "A historical figure", "A measurement unit"],
                "correct_index": 0,
                "explanation": f"{topic} is treated here as a foundational concept worth mastering.",
            },
            {
                "question": f"Why does understanding {topic} matter?",
                "options": ["It rarely applies", "It builds on earlier ideas and unlocks later ones", "It is purely decorative", "It only matters for exams"],
                "correct_index": 1,
                "explanation": "Foundational topics serve as bridges between simpler and more advanced ideas.",
            },
            {
                "question": f"What is the best way to deepen mastery of {topic}?",
                "options": ["Memorize one definition", "Skip examples", "Work through examples and connect to other concepts", "Avoid practice"],
                "correct_index": 2,
                "explanation": "Active practice plus connection-building beats rote recall.",
            },
        ],
    }


def _extract_json(text: str) -> dict[str, Any] | None:
    if not text:
        return None
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        m = re.search(r"\{[\s\S]*\}", text)
        if not m:
            return None
        try:
            return json.loads(m.group(0))
        except json.JSONDecodeError:
            return None


def _validate(payload: dict[str, Any], topic: str) -> dict[str, Any] | None:
    try:
        steps = payload.get("steps") or []
        quiz = payload.get("quiz") or []
        if not (3 <= len(steps) <= 6) or not (2 <= len(quiz) <= 5):
            return None
        for s in steps:
            if not isinstance(s.get("title"), str) or not isinstance(s.get("content"), str):
                return None
        for q in quiz:
            opts = q.get("options")
            if not isinstance(opts, list) or len(opts) != 4:
                return None
            ci = q.get("correct_index")
            if not isinstance(ci, int) or ci < 0 or ci > 3:
                return None
        payload["topic"] = payload.get("topic") or topic
        payload.setdefault("summary", f"A short guided lesson on {topic}.")
        return payload
    except (TypeError, AttributeError):
        return None


async def _generate_with_gemini(topic: str) -> dict[str, Any] | None:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None
    try:
        from google import genai
        client = genai.Client()
        prompt = f"{SYSTEM_PROMPT}\n\nTopic: {topic}\n\nReturn the JSON now."
        resp = client.models.generate_content(model="gemini-1.5-flash", contents=prompt)
        return _extract_json(resp.text or "")
    except Exception:
        return None


async def _generate_with_llm(topic: str) -> dict[str, Any] | None:
    try:
        llm = LLM.from_env()
        text = await llm.complete(SYSTEM_PROMPT, f"Topic: {topic}\n\nReturn the JSON now.", max_tokens=1400)
        return _extract_json(text)
    except Exception:
        return None


@router.post("/generate")
async def generate_lesson(req: LessonRequest) -> dict[str, Any]:
    topic = req.topic.strip()
    payload = await _generate_with_gemini(topic)
    if payload is None:
        payload = await _generate_with_llm(topic)
    if payload is not None:
        validated = _validate(payload, topic)
        if validated is not None:
            return validated
    return _fallback_lesson(topic)
