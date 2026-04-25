"""
Cognition track — advanced retrieval + LLM-as-judge.

Three layers on top of the baseline cosine retrieval:

  1. HyDE  — generate a hypothetical answer with a small LLM, embed *that*,
            and use it as the retrieval query. Catches the case where the
            student's question and the source material don't share vocabulary.

  2. Cross-encoder rerank — re-rank the top-N candidates with a cross-encoder
            (ms-marco-MiniLM-L-6-v2). Cosine over MiniLM embeddings is a coarse
            filter; the cross-encoder reads each (query, chunk) pair jointly.

  3. LLM-as-judge — after the tutor produces an answer, run a parallel call
            that returns a JSON ScoreCard with `score`, `grounded`, `reasoning`,
            and `citations[]`. Streamed to the client as a `judge_result` SSE.

Each layer degrades gracefully: if the rerank model isn't installed, we keep
the cosine ranking; if HyDE fails, we fall back to the raw question; if the
judge errors, we emit a `score=0, grounded=false` result with the error message
in `reasoning`.
"""
from __future__ import annotations

import asyncio
import json
import logging
import re
import time
from dataclasses import dataclass, field
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.agents.base import asi1_complete

log = logging.getLogger("sage.cognition")


@dataclass(frozen=True)
class RetrievedChunk:
    id: str
    text: str
    cosine: float
    rerank: Optional[float] = None


@dataclass(frozen=True)
class JudgeResult:
    score: float          # 0.0 to 1.0
    grounded: bool
    reasoning: str
    citations: list[int]  # indices into the retrieved chunk list


@dataclass(frozen=True)
class CognitionTrace:
    hyde_query: str
    retrieved: list[RetrievedChunk]
    rerank_used: bool
    latency_ms: int

    def to_payload(self) -> dict:
        return {
            "hyde_query": self.hyde_query,
            "retrieved": [
                {
                    "id": c.id,
                    "preview": c.text[:160],
                    "cosine": round(c.cosine, 4),
                    "rerank": round(c.rerank, 4) if c.rerank is not None else None,
                }
                for c in self.retrieved
            ],
            "rerank_used": self.rerank_used,
            "latency_ms": self.latency_ms,
        }


# ─── HyDE ──────────────────────────────────────────────────────────

HYDE_PROMPT = """You are helping a student learn. Without using outside knowledge,
write the *kind* of paragraph an ideal textbook would produce in answer to this
question. Two to four sentences. Plain prose, no bullet points.

Question: {question}

Answer:"""


async def hyde_expand(question: str) -> str:
    """Generate a hypothetical answer to use as the embedding query."""
    try:
        result = await asyncio.wait_for(
            asi1_complete(HYDE_PROMPT.format(question=question), max_tokens=200),
            timeout=4.0,
        )
        result = result.strip()
        if not result or result.lower().startswith("agent llm error"):
            return question
        # If the model fell back to a stub, the original question is still better.
        if result.startswith("[stub:"):
            return question
        return f"{question}\n\n{result}"
    except Exception as e:
        log.debug("HyDE expand failed: %s", e)
        return question


# ─── Cross-encoder reranker ────────────────────────────────────────

_reranker = None
_reranker_unavailable = False


def _get_reranker():
    """Lazy-load the cross-encoder. Cache None if unavailable."""
    global _reranker, _reranker_unavailable
    if _reranker is not None or _reranker_unavailable:
        return _reranker
    try:
        from sentence_transformers import CrossEncoder
        _reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2", max_length=512)
        return _reranker
    except Exception as e:
        log.info("Cross-encoder unavailable, falling back to cosine: %s", e)
        _reranker_unavailable = True
        return None


def rerank(query: str, chunks: list[RetrievedChunk], top_k: int = 4) -> tuple[list[RetrievedChunk], bool]:
    """Return top-k chunks reranked by cross-encoder. Returns (chunks, rerank_used)."""
    if not chunks:
        return chunks, False
    model = _get_reranker()
    if model is None:
        return chunks[:top_k], False
    try:
        pairs = [(query, c.text) for c in chunks]
        scores = model.predict(pairs)
        ranked = [
            RetrievedChunk(id=c.id, text=c.text, cosine=c.cosine, rerank=float(s))
            for c, s in zip(chunks, scores)
        ]
        ranked.sort(key=lambda c: c.rerank or 0.0, reverse=True)
        return ranked[:top_k], True
    except Exception as e:
        log.warning("Rerank failed, using cosine order: %s", e)
        return chunks[:top_k], False


# ─── End-to-end pipeline ───────────────────────────────────────────

async def cognition_retrieve(
    question: str,
    lesson_id: int,
    db: AsyncSession,
    top_k: int = 4,
    candidate_pool: int = 12,
) -> CognitionTrace:
    """
    Full Cognition retrieval: HyDE → cosine top-N → rerank → top-k.
    Returns a trace usable by the SSE stream and the score card.
    """
    start = time.monotonic()
    from app.models.lesson import LessonChunk, Lesson
    from app.core.retrieval import _get_embedding_model

    expanded = await hyde_expand(question)

    # Cosine prefilter
    try:
        model = _get_embedding_model()
        q_vec = model.encode(expanded, normalize_embeddings=True)
    except Exception:
        # No embeddings available — fall back to whole-lesson stub
        result = await db.execute(select(Lesson).where(Lesson.id == lesson_id))
        lesson = result.scalar_one_or_none()
        text = (lesson.content_md[:3000] if lesson else "")
        return CognitionTrace(
            hyde_query=expanded,
            retrieved=[RetrievedChunk(id="lesson", text=text, cosine=1.0)] if text else [],
            rerank_used=False,
            latency_ms=int((time.monotonic() - start) * 1000),
        )

    result = await db.execute(
        select(LessonChunk).where(LessonChunk.lesson_id == lesson_id)
    )
    chunks = result.scalars().all()
    if not chunks:
        lesson_res = await db.execute(select(Lesson).where(Lesson.id == lesson_id))
        lesson = lesson_res.scalar_one_or_none()
        text = (lesson.content_md[:3000] if lesson else "")
        return CognitionTrace(
            hyde_query=expanded,
            retrieved=[RetrievedChunk(id="lesson", text=text, cosine=1.0)] if text else [],
            rerank_used=False,
            latency_ms=int((time.monotonic() - start) * 1000),
        )

    import numpy as np
    scored: list[RetrievedChunk] = []
    for chunk in chunks:
        if not chunk.embedding:
            scored.append(RetrievedChunk(id=str(chunk.id), text=chunk.text, cosine=0.0))
            continue
        try:
            chunk_vec = np.array(json.loads(chunk.embedding))
            score = float(np.dot(q_vec, chunk_vec))
            scored.append(RetrievedChunk(id=str(chunk.id), text=chunk.text, cosine=score))
        except Exception:
            scored.append(RetrievedChunk(id=str(chunk.id), text=chunk.text, cosine=0.0))

    scored.sort(key=lambda c: c.cosine, reverse=True)
    pool = scored[:candidate_pool]

    # Rerank with cross-encoder
    final, rerank_used = rerank(question, pool, top_k=top_k)
    return CognitionTrace(
        hyde_query=expanded,
        retrieved=final,
        rerank_used=rerank_used,
        latency_ms=int((time.monotonic() - start) * 1000),
    )


# ─── LLM-as-judge ──────────────────────────────────────────────────

JUDGE_PROMPT = """You are an output verifier. Score whether the SAGE Tutor's
answer is grounded in the retrieved sources. Return ONLY a JSON object with
this shape:

{{
  "score": 0.0-1.0,
  "grounded": true|false,
  "reasoning": "one sentence explaining your score",
  "citations": [list of source indices that the answer actually relies on]
}}

A "grounded" answer makes only claims that can be inferred from the sources.
Hallucinated facts, fabricated URLs, or fabricated quotes mean grounded=false.
A Socratic counter-question that does not assert facts should score 1.0
grounded=true.

Question:
{question}

Tutor answer:
{answer}

Sources:
{sources}

JSON:"""


def _strip_json(raw: str) -> Optional[dict]:
    """Best-effort extract a JSON object from the model output."""
    match = re.search(r"\{[\s\S]*\}", raw)
    if not match:
        return None
    payload = match.group(0)
    try:
        return json.loads(payload)
    except json.JSONDecodeError:
        cleaned = re.sub(r",\s*([}\]])", r"\1", payload)
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            return None


async def llm_judge(
    question: str,
    answer: str,
    sources: list[RetrievedChunk],
) -> JudgeResult:
    """Run the LLM-as-judge. Falls back to a permissive result on error."""
    if not answer.strip():
        return JudgeResult(
            score=0.0, grounded=False,
            reasoning="empty answer", citations=[],
        )

    sources_text = "\n\n".join(
        f"[{i}] {c.text[:600]}" for i, c in enumerate(sources)
    ) or "(no sources retrieved)"

    prompt = JUDGE_PROMPT.format(
        question=question[:600],
        answer=answer[:1500],
        sources=sources_text,
    )

    try:
        raw = await asyncio.wait_for(asi1_complete(prompt, max_tokens=300), timeout=8.0)
    except asyncio.TimeoutError:
        return JudgeResult(
            score=0.5, grounded=False,
            reasoning="judge timed out", citations=[],
        )
    except Exception as e:
        return JudgeResult(
            score=0.5, grounded=False,
            reasoning=f"judge error: {e}", citations=[],
        )

    parsed = _strip_json(raw)
    if not parsed:
        return JudgeResult(
            score=0.5, grounded=False,
            reasoning="judge returned non-JSON", citations=[],
        )

    return JudgeResult(
        score=float(parsed.get("score", 0.5)),
        grounded=bool(parsed.get("grounded", False)),
        reasoning=str(parsed.get("reasoning", "")),
        citations=[int(i) for i in parsed.get("citations", []) if isinstance(i, (int, float))],
    )
