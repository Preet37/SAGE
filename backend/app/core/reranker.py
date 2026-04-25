"""
Cross-encoder reranking layer — Cognition track.
Loads cross-encoder/ms-marco-MiniLM-L-6-v2 on first use (via sentence-transformers).
Reranks retrieved chunks by scoring (query, chunk) pairs directly.
"""
from __future__ import annotations

import logging
from functools import lru_cache
from dataclasses import dataclass

log = logging.getLogger("sage.reranker")


@dataclass
class RankedChunk:
    text: str
    chunk_id: str
    cross_score: float  # raw cross-encoder logit (higher = more relevant)


@lru_cache(maxsize=1)
def _load_model():
    """Lazy-load cross-encoder. Cached so it loads once per process."""
    from sentence_transformers import CrossEncoder
    log.info("Loading cross-encoder/ms-marco-MiniLM-L-6-v2 (first use, ~80MB)...")
    model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
    log.info("Cross-encoder loaded.")
    return model


def rerank(query: str, chunks: list[tuple[str, str]], top_k: int = 4) -> list[RankedChunk]:
    """
    Rerank chunks against query using the cross-encoder.

    Args:
        query: The original student question.
        chunks: List of (chunk_id, chunk_text) tuples.
        top_k: Number of top chunks to return after reranking.

    Returns:
        List of RankedChunk sorted by descending cross_score, length <= top_k.
    """
    if not chunks:
        return []

    try:
        model = _load_model()
        pairs = [[query, text] for _, text in chunks]
        scores = model.predict(pairs)

        ranked = [
            RankedChunk(text=text, chunk_id=chunk_id, cross_score=float(score))
            for (chunk_id, text), score in zip(chunks, scores)
        ]
        ranked.sort(key=lambda r: r.cross_score, reverse=True)
        return ranked[:top_k]
    except Exception as e:
        log.warning(f"Cross-encoder reranking failed, returning original order: {e}")
        return [
            RankedChunk(text=text, chunk_id=chunk_id, cross_score=0.0)
            for chunk_id, text in chunks[:top_k]
        ]
