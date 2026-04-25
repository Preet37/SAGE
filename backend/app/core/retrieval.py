"""Cosine-similarity RAG over an in-memory document store.

Embeddings are pluggable: pass any `Embedder` callable that maps `str -> list[float]`.
Default is a deterministic hashing embedder so tests are stable without API calls.
"""

from __future__ import annotations

import hashlib
import math
import re
from dataclasses import dataclass, field
from typing import Callable, Iterable

Vector = list[float]
Embedder = Callable[[str], Vector]


_TOKEN_RE = re.compile(r"[A-Za-z0-9']+")


def tokenize(text: str) -> list[str]:
    return [t.lower() for t in _TOKEN_RE.findall(text)]


def hashing_embedder(dim: int = 256) -> Embedder:
    """Deterministic bag-of-tokens hashing embedder. No external deps."""

    def embed(text: str) -> Vector:
        vec = [0.0] * dim
        for tok in tokenize(text):
            h = int.from_bytes(hashlib.blake2b(tok.encode(), digest_size=8).digest(), "big")
            vec[h % dim] += 1.0
        return vec

    return embed


def cosine(a: Vector, b: Vector) -> float:
    if len(a) != len(b):
        raise ValueError("vector dim mismatch")
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    if na == 0.0 or nb == 0.0:
        return 0.0
    return dot / (na * nb)


@dataclass
class Document:
    id: str
    text: str
    meta: dict = field(default_factory=dict)


@dataclass
class Retrieved:
    doc: Document
    score: float


class CosineRetriever:
    def __init__(self, embedder: Embedder | None = None):
        self.embedder: Embedder = embedder or hashing_embedder()
        self._docs: list[Document] = []
        self._vecs: list[Vector] = []

    def add(self, docs: Iterable[Document]) -> None:
        for d in docs:
            self._docs.append(d)
            self._vecs.append(self.embedder(d.text))

    def __len__(self) -> int:
        return len(self._docs)

    def search(self, query: str, k: int = 4, min_score: float = 0.0) -> list[Retrieved]:
        if not self._docs:
            return []
        qv = self.embedder(query)
        scored = [Retrieved(d, cosine(qv, v)) for d, v in zip(self._docs, self._vecs)]
        scored.sort(key=lambda r: r.score, reverse=True)
        out = [r for r in scored if r.score >= min_score]
        return out[:k]
