"""Response verification — judges tutor output for groundedness against the lesson KB.

Run after the tutor finishes streaming. Uses the fast/judge model so it adds
minimal latency. Emits a structured score the frontend renders as a confidence chip.
"""

from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass
from typing import Optional

from openai import AsyncOpenAI

from ..config import get_settings

logger = logging.getLogger(__name__)


@dataclass
class VerificationResult:
    score: float                  # 0.0–1.0 groundedness score
    label: str                    # "grounded" | "partial" | "unverified"
    grounded_claims: list[str]    # claims supported by the KB
    unsupported_claims: list[str] # claims not found in KB / lesson
    rationale: str

    def to_dict(self) -> dict:
        return {
            "score": round(self.score, 2),
            "label": self.label,
            "grounded_claims": self.grounded_claims,
            "unsupported_claims": self.unsupported_claims,
            "rationale": self.rationale,
        }


_JUDGE_PROMPT = """You are a strict groundedness judge for an educational tutor.

You will receive (1) a tutor response and (2) the authoritative lesson material
(content + reference KB). Your job: rate whether each substantive factual claim
in the tutor response is supported by the material.

Return STRICT JSON only — no prose, no markdown fences:

{{
  "score": <float 0.0–1.0, fraction of substantive claims supported>,
  "grounded_claims": [<short paraphrase of each supported claim, max 5>],
  "unsupported_claims": [<short paraphrase of each unsupported / unverifiable claim, max 5>],
  "rationale": "<one sentence explaining the score>"
}}

Rules:
- Pedagogical questions, restated prompts, and Socratic prompts are NOT claims — ignore them.
- Generic background knowledge widely known in the field counts as supported.
- A factual claim with a specific number, name, paper, or result MUST appear in
  the lesson material to count as grounded.
- If the response is mostly questions or scaffolding (Socratic), score 1.0.
- If material is empty or response makes no factual claims, score 1.0.

LESSON TITLE: {title}

LESSON MATERIAL:
\"\"\"
{material}
\"\"\"

TUTOR RESPONSE:
\"\"\"
{response}
\"\"\"
"""


def _strip_tags(text: str) -> str:
    """Remove rendered tags (<quiz>, <resource>, etc.) so the judge sees prose only."""
    text = re.sub(r"<(quiz|resource|image|flow|architecture)\b[^>]*>.*?</\1>", " ", text, flags=re.DOTALL)
    text = re.sub(r"<(quiz|resource|image|flow|architecture)\b[^>]*/?>", " ", text)
    text = re.sub(r"```mermaid.*?```", " ", text, flags=re.DOTALL)
    return text.strip()


_judge_client: Optional[AsyncOpenAI] = None


def _get_client() -> AsyncOpenAI:
    global _judge_client
    if _judge_client is None:
        s = get_settings()
        _judge_client = AsyncOpenAI(api_key=s.llm_api_key, base_url=s.llm_base_url)
    return _judge_client


async def verify_response(
    response_text: str,
    lesson_title: str,
    lesson_content: str,
    reference_kb: str,
) -> Optional[VerificationResult]:
    """Score `response_text` for groundedness. Returns None on failure (best-effort)."""
    settings = get_settings()
    if not settings.feature_verification:
        return None

    cleaned = _strip_tags(response_text)
    # Skip near-empty or pure-question responses — nothing to verify.
    if len(cleaned) < 80 or cleaned.count("?") >= max(1, len(cleaned) // 200):
        return VerificationResult(
            score=1.0,
            label="grounded",
            grounded_claims=[],
            unsupported_claims=[],
            rationale="No substantive factual claims to verify.",
        )

    material = ((lesson_content or "") + "\n\n---\n\n" + (reference_kb or "")).strip()
    if not material:
        return None

    # Judge model: prefer dedicated `judge` if available, else fast, else tutor.
    model = settings.fast_llm_model or settings.llm_model

    prompt = _JUDGE_PROMPT.format(
        title=lesson_title or "(untitled)",
        material=material[:12000],     # cap to keep judge cheap
        response=cleaned[:6000],
    )

    try:
        client = _get_client()
        completion = await client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You output strict JSON only."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=512,
            temperature=0.0,
            stream=False,
        )
        raw = (completion.choices[0].message.content or "").strip()
    except Exception as e:
        logger.warning("Verifier LLM call failed: %s", e)
        return None

    # Strip any stray markdown fences before parsing.
    raw = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw.strip(), flags=re.MULTILINE)
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", raw, re.DOTALL)
        if not match:
            logger.warning("Verifier returned non-JSON output: %s", raw[:200])
            return None
        try:
            data = json.loads(match.group(0))
        except json.JSONDecodeError:
            return None

    score = float(data.get("score", 0.5) or 0.5)
    score = max(0.0, min(1.0, score))
    label = "grounded" if score >= 0.85 else ("partial" if score >= 0.5 else "unverified")

    return VerificationResult(
        score=score,
        label=label,
        grounded_claims=[str(x)[:200] for x in (data.get("grounded_claims") or [])][:5],
        unsupported_claims=[str(x)[:200] for x in (data.get("unsupported_claims") or [])][:5],
        rationale=str(data.get("rationale", ""))[:300],
    )
