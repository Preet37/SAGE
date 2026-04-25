"""
HyDE — Hypothetical Document Embedding.
Generates a hypothetical ideal answer to a question, embeds it,
then compares retrieval quality against the baseline (raw question embedding).
"""
from __future__ import annotations

import logging
from dataclasses import dataclass

from app.agents.base import asi1_complete

log = logging.getLogger("sage.hyde")


@dataclass
class HydeResult:
    hypothesis: str
    hyde_score: float       # avg cosine similarity of top chunks to hypothesis
    baseline_score: float   # avg cosine similarity of top chunks to raw question
    improvement_pct: float  # (hyde - baseline) / baseline * 100, clamped to [0, 999]


async def generate_hypothesis(question: str, lesson_context: str = "") -> str:
    """Generate a hypothetical ideal answer to embed instead of the raw question."""
    prompt = (
        f"Write a short, authoritative 2-3 sentence answer to this question as if you "
        f"were an expert tutor. Do not hedge. This answer will be used only for document "
        f"retrieval — precision matters more than safety.\n\n"
        f"Question: {question}\n\n"
        f"Context (lesson topic): {lesson_context[:200] if lesson_context else 'general ML/AI'}\n\n"
        f"Hypothetical Answer:"
    )
    try:
        hypothesis = await asi1_complete(prompt, max_tokens=150)
        return hypothesis.strip()
    except Exception as e:
        log.warning(f"HyDE hypothesis generation failed: {e}")
        return question  # fall back to raw question


def compute_hyde_result(
    hypothesis: str,
    question: str,
    hyde_chunk_scores: list[float],
    baseline_chunk_scores: list[float],
) -> HydeResult:
    """Compute improvement metrics given pre-computed similarity scores."""
    hyde_avg = sum(hyde_chunk_scores) / len(hyde_chunk_scores) if hyde_chunk_scores else 0.0
    base_avg = sum(baseline_chunk_scores) / len(baseline_chunk_scores) if baseline_chunk_scores else 0.0

    if base_avg > 0:
        improvement = (hyde_avg - base_avg) / base_avg * 100
    else:
        improvement = 0.0

    improvement = max(0.0, min(improvement, 999.0))

    return HydeResult(
        hypothesis=hypothesis,
        hyde_score=round(hyde_avg, 4),
        baseline_score=round(base_avg, 4),
        improvement_pct=round(improvement, 1),
    )
