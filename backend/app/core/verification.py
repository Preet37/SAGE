"""Hallucination / groundedness checking.

A claim is considered grounded if it has substantial token-overlap with at least
one retrieved source. This is intentionally lightweight (no external model call)
so it is safe to run on every streamed sentence.

`verify(answer, sources)` returns a `VerificationReport` with per-claim verdicts
plus an aggregate score in [0, 1].
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from app.core.retrieval import tokenize

_SENT_SPLIT = re.compile(r"(?<=[.!?])\s+(?=[A-Z(])")
_STOP = {
    "the", "a", "an", "of", "to", "in", "is", "it", "and", "or", "for", "on",
    "with", "as", "by", "that", "this", "are", "be", "was", "were", "at",
    "from", "but", "if", "then", "so", "we", "you", "i", "he", "she", "they",
}


def split_claims(text: str) -> list[str]:
    text = text.strip()
    if not text:
        return []
    return [c.strip() for c in _SENT_SPLIT.split(text) if c.strip()]


def _content_tokens(s: str) -> set[str]:
    return {t for t in tokenize(s) if t not in _STOP and len(t) > 1}


def claim_support(claim: str, sources: list[str], threshold: float = 0.4) -> tuple[float, int | None]:
    claim_toks = _content_tokens(claim)
    if not claim_toks:
        return 1.0, None
    best = 0.0
    best_idx: int | None = None
    for i, src in enumerate(sources):
        src_toks = _content_tokens(src)
        if not src_toks:
            continue
        overlap = len(claim_toks & src_toks) / len(claim_toks)
        if overlap > best:
            best = overlap
            best_idx = i
    return best, (best_idx if best >= threshold else None)


@dataclass
class ClaimVerdict:
    claim: str
    score: float
    grounded: bool
    source_index: int | None


@dataclass
class VerificationReport:
    claims: list[ClaimVerdict] = field(default_factory=list)
    score: float = 1.0
    grounded: bool = True

    def to_payload(self) -> dict:
        return {
            "score": round(self.score, 3),
            "grounded": self.grounded,
            "claims": [
                {
                    "claim": c.claim,
                    "score": round(c.score, 3),
                    "grounded": c.grounded,
                    "source_index": c.source_index,
                }
                for c in self.claims
            ],
        }


def verify(answer: str, sources: list[str], threshold: float = 0.4) -> VerificationReport:
    claims = split_claims(answer)
    if not claims:
        return VerificationReport(claims=[], score=1.0, grounded=True)

    verdicts: list[ClaimVerdict] = []
    for claim in claims:
        score, src_idx = claim_support(claim, sources, threshold)
        verdicts.append(
            ClaimVerdict(
                claim=claim,
                score=score,
                grounded=src_idx is not None,
                source_index=src_idx,
            )
        )
    agg = sum(v.score for v in verdicts) / len(verdicts)
    return VerificationReport(
        claims=verdicts,
        score=agg,
        grounded=all(v.grounded for v in verdicts),
    )
