"""Lightweight semantic memory using TF-IDF cosine similarity (pure stdlib).

Why TF-IDF instead of dense embeddings: SAGE's LLM provider (Groq) doesn't
expose an embedding endpoint, and we want zero external deps for this feature.
For the volumes we expect (a few hundred turns per user) TF-IDF gives strong
enough recall for "did I see this concept before?" lookups without latency.

API:
    record_memory(user_id, role, content, ...)
    recall_memories(user_id, query, k=3) -> list[dict]
"""

from __future__ import annotations

import json
import logging
import math
import re
from collections import Counter
from datetime import datetime
from typing import Optional

from sqlmodel import Session, select

from ..db import engine
from ..models.memory import MemoryRecord

logger = logging.getLogger(__name__)


_STOPWORDS = {
    "the", "a", "an", "and", "or", "but", "if", "then", "is", "are", "was",
    "were", "be", "been", "being", "to", "of", "in", "on", "for", "with", "by",
    "as", "at", "this", "that", "these", "those", "it", "its", "i", "you",
    "we", "they", "he", "she", "them", "us", "our", "your", "my", "me",
    "do", "does", "did", "have", "has", "had", "will", "would", "can",
    "could", "should", "may", "might", "must", "what", "when", "where",
    "why", "how", "which", "who", "whom", "so", "not", "no", "yes",
    "from", "into", "than", "also", "just", "only", "very", "much", "some",
    "any", "all", "each", "more", "most", "few", "such", "like", "about",
}

_TOKEN_RE = re.compile(r"[a-z][a-z0-9_]+")


def tokenize(text: str) -> list[str]:
    return [t for t in _TOKEN_RE.findall((text or "").lower()) if t not in _STOPWORDS and len(t) > 2]


def _cosine(a: dict[str, float], b: dict[str, float]) -> float:
    if not a or not b:
        return 0.0
    common = set(a) & set(b)
    if not common:
        return 0.0
    dot = sum(a[t] * b[t] for t in common)
    na = math.sqrt(sum(v * v for v in a.values()))
    nb = math.sqrt(sum(v * v for v in b.values()))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


def _tfidf(tokens: list[str], doc_freqs: dict[str, int], n_docs: int) -> dict[str, float]:
    if not tokens:
        return {}
    counts = Counter(tokens)
    max_tf = max(counts.values())
    out: dict[str, float] = {}
    for term, tf in counts.items():
        idf = math.log((1 + n_docs) / (1 + doc_freqs.get(term, 0))) + 1.0
        out[term] = (tf / max_tf) * idf
    return out


def _heuristic_importance(content: str) -> float:
    """Cheap importance score so we don't store every trivial turn forever."""
    if not content:
        return 0.0
    length = min(len(content), 1500) / 1500
    has_question = 0.2 if "?" in content else 0.0
    has_specifics = 0.2 if re.search(r"\b\d+\b|paper|formula|equation|theorem|definition", content.lower()) else 0.0
    return min(1.0, 0.3 + 0.4 * length + has_question + has_specifics)


def record_memory(
    user_id: str,
    role: str,
    content: str,
    *,
    lesson_id: Optional[str] = None,
    session_id: Optional[str] = None,
    importance: Optional[float] = None,
) -> Optional[MemoryRecord]:
    """Store a memory record. Returns None if skipped (too short / disabled)."""
    if not content or len(content.strip()) < 40:
        return None
    tokens = tokenize(content)
    if not tokens:
        return None
    record = MemoryRecord(
        user_id=user_id,
        lesson_id=lesson_id,
        session_id=session_id,
        role=role,
        content=content[:4000],
        tokens=" ".join(tokens[:400]),
        importance=importance if importance is not None else _heuristic_importance(content),
    )
    try:
        with Session(engine) as db:
            db.add(record)
            db.commit()
            db.refresh(record)
            return record
    except Exception as e:
        logger.warning("Failed to record memory: %s", e)
        return None


def recall_memories(
    user_id: str,
    query: str,
    *,
    k: int = 3,
    lesson_id: Optional[str] = None,
    exclude_session_id: Optional[str] = None,
    min_score: float = 0.05,
    same_lesson_only: bool = False,
) -> list[dict]:
    """Return top-k past memories most similar to `query` for this user."""
    q_tokens = tokenize(query)
    if not q_tokens:
        return []

    with Session(engine) as db:
        stmt = select(MemoryRecord).where(MemoryRecord.user_id == user_id)
        if same_lesson_only and lesson_id:
            stmt = stmt.where(MemoryRecord.lesson_id == lesson_id)
        stmt = stmt.order_by(MemoryRecord.created_at.desc()).limit(500)
        records: list[MemoryRecord] = list(db.exec(stmt))

    if not records:
        return []

    if exclude_session_id:
        records = [r for r in records if r.session_id != exclude_session_id]

    # Build IDF over the candidate window (small N — recompute each call).
    doc_freqs: dict[str, int] = {}
    tokenized: list[list[str]] = []
    for r in records:
        toks = r.tokens.split() if r.tokens else tokenize(r.content)
        tokenized.append(toks)
        for term in set(toks):
            doc_freqs[term] = doc_freqs.get(term, 0) + 1
    n = len(records)

    q_vec = _tfidf(q_tokens, doc_freqs, n)
    scored: list[tuple[float, MemoryRecord]] = []
    for r, toks in zip(records, tokenized):
        d_vec = _tfidf(toks, doc_freqs, n)
        sim = _cosine(q_vec, d_vec)
        # Boost by importance and lesson match.
        sim *= (0.6 + 0.4 * (r.importance or 0.5))
        if lesson_id and r.lesson_id == lesson_id:
            sim *= 1.15
        if sim >= min_score:
            scored.append((sim, r))

    scored.sort(key=lambda x: x[0], reverse=True)
    out: list[dict] = []
    for sim, r in scored[:k]:
        out.append({
            "id": r.id,
            "role": r.role,
            "content": r.content,
            "lesson_id": r.lesson_id,
            "session_id": r.session_id,
            "score": round(sim, 3),
            "created_at": r.created_at.isoformat() if r.created_at else None,
        })
    return out


def memory_block_for_prompt(user_id: str, query: str, lesson_id: Optional[str], current_session_id: Optional[str]) -> str:
    """Format a 'past memory' block for injection into the system prompt.
    Returns empty string when no relevant memories exist.
    """
    hits = recall_memories(
        user_id=user_id,
        query=query,
        k=3,
        lesson_id=lesson_id,
        exclude_session_id=current_session_id,
    )
    if not hits:
        return ""
    lines = ["You previously discussed these related items with this learner:"]
    for h in hits:
        when = (h.get("created_at") or "").split("T")[0]
        snippet = h["content"].strip().replace("\n", " ")[:240]
        role = "they said" if h["role"] == "user" else "you said"
        lines.append(f"- [{when}] {role}: \"{snippet}\"")
    lines.append(
        "Use this as background context — only reference it when it actually helps. "
        "Do not parrot it back."
    )
    return "\n".join(lines)
