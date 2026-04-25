import math

import pytest

from app.core.retrieval import (
    CosineRetriever,
    Document,
    cosine,
    hashing_embedder,
    tokenize,
)


def test_tokenize_lowercases_and_splits():
    assert tokenize("Hello, World! It's 2026.") == ["hello", "world", "it's", "2026"]


def test_cosine_identical_is_one():
    e = hashing_embedder()
    v = e("photosynthesis converts light to chemical energy")
    assert cosine(v, v) == pytest.approx(1.0)


def test_cosine_orthogonal_disjoint_vocab():
    e = hashing_embedder(dim=4096)
    a = e("alpha bravo charlie")
    b = e("xenon yttrium zirconium")
    assert cosine(a, b) == pytest.approx(0.0, abs=1e-9)


def test_cosine_dim_mismatch_raises():
    with pytest.raises(ValueError):
        cosine([1.0, 0.0], [1.0, 0.0, 0.0])


def test_cosine_zero_vector_returns_zero():
    assert cosine([0.0, 0.0], [1.0, 1.0]) == 0.0


def test_retriever_returns_top_k_in_order():
    r = CosineRetriever()
    r.add([
        Document("a", "Photosynthesis converts light into chemical energy in plants."),
        Document("b", "Mitochondria are the powerhouse of the cell."),
        Document("c", "Chlorophyll absorbs light during photosynthesis."),
        Document("d", "The French Revolution began in 1789."),
    ])
    hits = r.search("how does photosynthesis use light", k=2)
    assert len(hits) == 2
    assert hits[0].doc.id in {"a", "c"}
    assert hits[0].score >= hits[1].score
    assert hits[0].score > 0.0


def test_retriever_min_score_filters():
    r = CosineRetriever()
    r.add([Document("a", "Totally unrelated content about cooking pasta.")])
    hits = r.search("quantum chromodynamics", k=4, min_score=0.5)
    assert hits == []


def test_retriever_empty_store_returns_empty():
    r = CosineRetriever()
    assert r.search("anything", k=4) == []


def test_retriever_len_tracks_adds():
    r = CosineRetriever()
    assert len(r) == 0
    r.add([Document("x", "one"), Document("y", "two")])
    assert len(r) == 2


def test_hashing_embedder_is_deterministic():
    e = hashing_embedder(dim=128)
    assert e("the cat sat") == e("the cat sat")
    assert math.isclose(sum(e("a b c d")), 4.0)
