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
) -> list[str]:
    """Return the top-k most semantically relevant KB chunks for a question."""
    try:
        from sentence_transformers import SentenceTransformer
        model = _get_embedding_model()
        q_embedding = model.encode(question, normalize_embeddings=True)
    except ImportError:
        # Fallback: return all chunks if sentence-transformers not available
        return await _get_all_chunks(lesson_id, db)

    result = await db.execute(
        select(LessonChunk).where(LessonChunk.lesson_id == lesson_id)
    )
    chunks = result.scalars().all()

    if not chunks:
        lesson_result = await db.execute(select(Lesson).where(Lesson.id == lesson_id))
        lesson = lesson_result.scalar_one_or_none()
        return [lesson.content_md[:3000]] if lesson else []

    scored = []
    for chunk in chunks:
        if chunk.embedding:
            try:
                chunk_vec = np.array(json.loads(chunk.embedding))
                score = float(np.dot(q_embedding, chunk_vec))
                scored.append((score, chunk.text))
            except Exception:
                scored.append((0.0, chunk.text))
        else:
            scored.append((0.0, chunk.text))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [text for _, text in scored[:top_k]]


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
