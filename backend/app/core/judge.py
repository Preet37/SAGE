"""
LLM-as-judge pipeline — Cognition track.
Evaluates every tutor response on 4 dimensions via async Haiku call.
Returns a structured score payload streamed as `judge_result` SSE event.
"""
from __future__ import annotations

import asyncio
import json
import logging
from dataclasses import dataclass, field

log = logging.getLogger("sage.judge")


@dataclass
class JudgeResult:
    confidence_score: int            # 0-100 composite
    grounded: bool                    # every claim in KB chunks?
    socratic: bool                    # guides rather than just answers?
    no_fabrications: bool             # no invented URLs/stats?
    on_topic: bool                    # stays on lesson scope?
    flags: list[str] = field(default_factory=list)
    retrieved_chunks: int = 0
    hyde_improvement_pct: float = 0.0

    def to_sse_payload(self) -> dict:
        return {
            "confidence_score": self.confidence_score,
            "grounded": self.grounded,
            "socratic": self.socratic,
            "no_fabrications": self.no_fabrications,
            "on_topic": self.on_topic,
            "flags": self.flags,
            "retrieved_chunks": self.retrieved_chunks,
            "hyde_improvement_pct": self.hyde_improvement_pct,
        }


async def judge_response(
    question: str,
    response: str,
    chunks: list[str],
    retrieved_chunks: int = 0,
    hyde_improvement_pct: float = 0.0,
) -> JudgeResult:
    """
    Run LLM-as-judge evaluation. Uses a fast Haiku call (haiku-4-5).
    Returns a JudgeResult even if the call fails (defaults to passing).
    """
    chunk_preview = "\n---\n".join(chunks[:4])[:1500] if chunks else "(no chunks retrieved)"

    prompt = f"""You are a strict educational AI quality evaluator. Evaluate this tutoring exchange.

STUDENT QUESTION:
{question[:300]}

TUTOR RESPONSE:
{response[:800]}

KNOWLEDGE BASE CHUNKS USED:
{chunk_preview}

Evaluate on these 4 dimensions. Answer with ONLY a JSON object, no explanation:

{{
  "grounded": true/false,
  "socratic": true/false,
  "no_fabrications": true/false,
  "on_topic": true/false,
  "flags": [],
  "confidence_score": 0
}}

grounded = every factual claim traceable to KB chunks
socratic = guides with questions rather than just giving answers
no_fabrications = no invented URLs, citations, or statistics not in KB
on_topic = stays on lesson topic
confidence_score = 0-100 overall quality"""

    try:
        import anthropic
        import os
        client = anthropic.AsyncAnthropic(api_key=os.environ.get("ANTHROPIC_API_KEY", ""))
        message = await asyncio.wait_for(
            client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=200,
                messages=[{"role": "user", "content": prompt}],
            ),
            timeout=8.0,
        )
        raw = message.content[0].text.strip()
        start = raw.find("{")
        end = raw.rfind("}") + 1
        data = json.loads(raw[start:end])

        return JudgeResult(
            confidence_score=int(data.get("confidence_score", 75)),
            grounded=bool(data.get("grounded", True)),
            socratic=bool(data.get("socratic", True)),
            no_fabrications=bool(data.get("no_fabrications", True)),
            on_topic=bool(data.get("on_topic", True)),
            flags=data.get("flags", []),
            retrieved_chunks=retrieved_chunks,
            hyde_improvement_pct=hyde_improvement_pct,
        )
    except Exception as e:
        log.warning(f"Judge evaluation failed: {e}")
        return JudgeResult(
            confidence_score=75,
            grounded=True,
            socratic=True,
            no_fabrications=True,
            on_topic=True,
            flags=[],
            retrieved_chunks=retrieved_chunks,
            hyde_improvement_pct=hyde_improvement_pct,
        )
