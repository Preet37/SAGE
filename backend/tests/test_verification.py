from app.core.verification import claim_support, split_claims, verify


def test_split_claims_basic():
    text = "Photosynthesis uses light. Chlorophyll absorbs it. Plants then make sugar!"
    assert split_claims(text) == [
        "Photosynthesis uses light.",
        "Chlorophyll absorbs it.",
        "Plants then make sugar!",
    ]


def test_split_claims_empty():
    assert split_claims("   ") == []


def test_claim_support_high_overlap_grounded():
    sources = ["Chlorophyll absorbs light during photosynthesis in plant cells."]
    score, idx = claim_support("Chlorophyll absorbs light in plants.", sources, threshold=0.4)
    assert idx == 0
    assert score >= 0.4


def test_claim_support_low_overlap_ungrounded():
    sources = ["The French Revolution began in 1789 in Paris."]
    score, idx = claim_support("Mitochondria produce ATP through respiration.", sources)
    assert idx is None
    assert score < 0.4


def test_verify_all_grounded():
    sources = [
        "Photosynthesis converts light energy into chemical energy.",
        "Chlorophyll is the pigment that absorbs light in plants.",
    ]
    answer = "Photosynthesis converts light energy. Chlorophyll absorbs light in plants."
    report = verify(answer, sources)
    assert report.grounded is True
    assert report.score > 0.5
    assert all(c.grounded for c in report.claims)


def test_verify_partial_hallucination():
    sources = ["Photosynthesis converts light energy into chemical energy."]
    answer = "Photosynthesis converts light energy. Napoleon invaded Russia in 1812."
    report = verify(answer, sources)
    assert report.grounded is False
    grounded_flags = [c.grounded for c in report.claims]
    assert grounded_flags.count(True) == 1
    assert grounded_flags.count(False) == 1


def test_verify_empty_answer_is_grounded_trivially():
    report = verify("", ["any source"])
    assert report.grounded is True
    assert report.score == 1.0
    assert report.claims == []


def test_verify_payload_shape():
    report = verify("Plants use chlorophyll.", ["Plants use chlorophyll for photosynthesis."])
    payload = report.to_payload()
    assert set(payload.keys()) == {"score", "grounded", "claims"}
    assert set(payload["claims"][0].keys()) == {"claim", "score", "grounded", "source_index"}
