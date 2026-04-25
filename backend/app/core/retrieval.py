"""
Semantic retrieval layer — Cognition track.
Embeds student questions and finds the most relevant KB chunks
instead of dumping the entire lesson into context.
"""
import json
import hashlib
import math
import re
import numpy as np
from dataclasses import dataclass
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.lesson import LessonChunk, Lesson


def _adaptive_chunk_size(text: str) -> int:
    """Return appropriate chunk size in words based on content type."""
    code_lines = sum(
        1 for line in text.split('\n')
        if line.strip().startswith(('def ', 'class ', '```', '    ', '\t'))
    )
    math_markers = text.count('$$') + text.count('\\[') + text.count('\\(')

    if code_lines > 3:
        return 100    # preserve syntax context
    if math_markers > 1:
        return 9999   # keep as single atomic chunk
    return 300        # prose default


@dataclass(frozen=True)
class Document:
    id: str
    text: str


@dataclass(frozen=True)
class SearchHit:
    doc: Document
    score: float


def tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z0-9']+", text.lower())


def hashing_embedder(dim: int = 512):
    def embed(text: str) -> list[float]:
        vector = [0.0] * dim
        for token in tokenize(text):
            digest = hashlib.sha256(token.encode("utf-8")).digest()
            idx = int.from_bytes(digest[:8], "big") % dim
            vector[idx] += 1.0
        return vector

    return embed


def cosine(a: list[float], b: list[float]) -> float:
    if len(a) != len(b):
        raise ValueError("vectors must have same dimension")
    denom = math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b))
    if denom == 0:
        return 0.0
    return sum(x * y for x, y in zip(a, b)) / denom


class CosineRetriever:
    def __init__(self, embedder=None):
        self.embedder = embedder or hashing_embedder()
        self._docs: list[tuple[Document, list[float]]] = []

    def add(self, docs) -> None:
        for doc in docs:
            self._docs.append((doc, self.embedder(doc.text)))

    def search(self, query: str, k: int = 4, min_score: float = 0.0) -> list[SearchHit]:
        if not self._docs:
            return []
        q = self.embedder(query)
        hits = [
            SearchHit(doc=doc, score=cosine(q, vector))
            for doc, vector in self._docs
        ]
        hits = [hit for hit in hits if hit.score >= min_score]
        hits.sort(key=lambda hit: hit.score, reverse=True)
        return hits[:k]

    def __len__(self) -> int:
        return len(self._docs)


async def get_relevant_chunks(
    question: str,
    lesson_id: int,
    db: AsyncSession,
    top_k: int = 4,
) -> tuple[list[str], dict]:
    """
    Retrieve top-k relevant chunks via HyDE + cross-encoder reranking.
    Returns (chunk_texts, cognition_meta) where cognition_meta carries metrics
    for the Cognition Score card.
    """
    try:
        model = _get_embedding_model()
    except ImportError:
        raw = await _get_all_chunks(lesson_id, db)
        return raw[:top_k], {"hyde_improvement_pct": 0.0, "retrieved_chunks": len(raw[:top_k])}

    result = await db.execute(
        select(LessonChunk).where(LessonChunk.lesson_id == lesson_id)
    )
    all_chunks = result.scalars().all()

    if not all_chunks:
        lesson_result = await db.execute(select(Lesson).where(Lesson.id == lesson_id))
        lesson = lesson_result.scalar_one_or_none()
        fallback = [lesson.content_md[:3000]] if lesson else []
        return fallback, {"hyde_improvement_pct": 0.0, "retrieved_chunks": len(fallback)}

    # Build (chunk_id, text, embedding) list
    chunk_data: list[tuple[str, str, Optional[list[float]]]] = []
    for chunk in all_chunks:
        if chunk.embedding:
            try:
                vec = json.loads(chunk.embedding)
                chunk_data.append((str(chunk.id), chunk.text, vec))
            except Exception:
                chunk_data.append((str(chunk.id), chunk.text, None))
        else:
            chunk_data.append((str(chunk.id), chunk.text, None))

    # Baseline: embed raw question
    q_embedding = model.encode(question, normalize_embeddings=True)

    def _score_chunks(embedding) -> list[tuple[float, str, str]]:
        scored = []
        for cid, text, vec in chunk_data:
            if vec:
                try:
                    chunk_vec = np.array(vec)
                    score = float(np.dot(embedding, chunk_vec))
                    scored.append((score, cid, text))
                except Exception:
                    scored.append((0.0, cid, text))
            else:
                scored.append((0.0, cid, text))
        scored.sort(key=lambda x: x[0], reverse=True)
        return scored

    baseline_scored = _score_chunks(q_embedding)
    baseline_top_scores = [s for s, _, _ in baseline_scored[:8]]

    # HyDE: generate hypothesis and embed it
    try:
        from app.core.hyde import generate_hypothesis, compute_hyde_result
        lesson_result = await db.execute(select(Lesson).where(Lesson.id == lesson_id))
        lesson = lesson_result.scalar_one_or_none()
        lesson_topic = lesson.title if lesson else ""

        hypothesis = await generate_hypothesis(question, lesson_topic)
        h_embedding = model.encode(hypothesis, normalize_embeddings=True)
        hyde_scored = _score_chunks(h_embedding)
        hyde_top_scores = [s for s, _, _ in hyde_scored[:8]]

        hyde_result = compute_hyde_result(hypothesis, question, hyde_top_scores[:top_k], baseline_top_scores[:top_k])
        hyde_improvement_pct = hyde_result.improvement_pct

        # Use HyDE-scored candidates for reranking
        candidates = [(cid, text) for _, cid, text in hyde_scored[:8]]
    except Exception:
        candidates = [(cid, text) for _, cid, text in baseline_scored[:8]]
        hyde_improvement_pct = 0.0

    # Cross-encoder rerank
    try:
        from app.core.reranker import rerank
        reranked = rerank(question, candidates, top_k=top_k)
        final_chunks = [r.text for r in reranked]
    except Exception:
        final_chunks = [text for _, text in candidates[:top_k]]

    cognition_meta = {
        "hyde_improvement_pct": hyde_improvement_pct,
        "retrieved_chunks": len(final_chunks),
    }
    return final_chunks, cognition_meta


async def _get_all_chunks(lesson_id: int, db: AsyncSession) -> list[str]:
    result = await db.execute(
        select(LessonChunk).where(LessonChunk.lesson_id == lesson_id)
    )
    chunks = result.scalars().all()
    return [c.text for c in chunks] if chunks else []


_embedding_model = None


def _get_embedding_model():
    global _embedding_model
    if _embedding_model is None:
        from sentence_transformers import SentenceTransformer
        _embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
    return _embedding_model


def chunk_text(text: str, chunk_size: int = 512, overlap: int = 64) -> list[str]:
    """Split text into overlapping chunks."""
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = " ".join(words[i : i + chunk_size])
        chunks.append(chunk)
        i += chunk_size - overlap
    return chunks


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Embed a list of texts, returns list of float vectors."""
    try:
        model = _get_embedding_model()
        embeddings = model.encode(texts, normalize_embeddings=True)
        return embeddings.tolist()
    except ImportError:
        return [[] for _ in texts]
