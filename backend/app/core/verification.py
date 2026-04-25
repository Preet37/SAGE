"""
Output verification layer — Cognition track.
Checks LLM responses for hallucinations, fabricated URLs,
quiz format validity, and sourcing before the student sees them.
"""
import re
import json
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class VerificationResult:
    passed: bool
    flags: list[str] = field(default_factory=list)
    score: float = 1.0


@dataclass
class ClaimReport:
    claim: str
    score: float
    grounded: bool
    source_index: Optional[int]


@dataclass
class VerificationReport:
    score: float
    grounded: bool
    claims: list[ClaimReport]

    def to_payload(self) -> dict:
        return {
            "score": self.score,
            "grounded": self.grounded,
            "claims": [
                {
                    "claim": c.claim,
                    "score": c.score,
                    "grounded": c.grounded,
                    "source_index": c.source_index,
                }
                for c in self.claims
            ],
        }


URL_PATTERN = re.compile(r"https?://\S+")
QUIZ_PATTERN = re.compile(r"<quiz>(.*?)</quiz>", re.DOTALL)


def split_claims(text: str) -> list[str]:
    text = text.strip()
    if not text:
        return []
    return [m.group(0).strip() for m in re.finditer(r"[^.!?]+[.!?]", text) if m.group(0).strip()]


def _keywords(text: str) -> set[str]:
    return set(re.findall(r"\b\w{4,}\b", text.lower()))


def claim_support(claim: str, sources: list[str], threshold: float = 0.4) -> tuple[float, Optional[int]]:
    claim_words = _keywords(claim)
    if not claim_words or not sources:
        return (1.0 if not claim_words else 0.0), None
    best_score = 0.0
    best_idx: Optional[int] = None
    for idx, source in enumerate(sources):
        source_words = _keywords(source)
        score = len(claim_words & source_words) / len(claim_words)
        if score > best_score:
            best_score = score
            best_idx = idx
    return best_score, best_idx if best_score >= threshold else None


def verify(answer: str, sources: list[str], threshold: float = 0.4) -> VerificationReport:
    claims = split_claims(answer)
    if not claims:
        return VerificationReport(score=1.0, grounded=True, claims=[])
    reports = []
    for claim in claims:
        score, idx = claim_support(claim, sources, threshold=threshold)
        reports.append(ClaimReport(claim=claim, score=score, grounded=idx is not None, source_index=idx))
    avg_score = sum(r.score for r in reports) / len(reports)
    return VerificationReport(
        score=avg_score,
        grounded=all(r.grounded for r in reports),
        claims=reports,
    )


def verify_response(
    response: str,
    context_chunks: list[str],
    search_was_called: bool = False,
) -> VerificationResult:
    """
    Run all verification checks on a tutor response.
    Returns VerificationResult with pass/fail and any flags.
    """
    flags = []

    # 1. URL fabrication check
    urls_in_response = URL_PATTERN.findall(response)
    if urls_in_response and not search_was_called:
        flags.append(f"URL_FABRICATION: Found {len(urls_in_response)} URL(s) without search tool call")

    # 2. Quiz format validation
    quiz_matches = QUIZ_PATTERN.findall(response)
    for quiz_json in quiz_matches:
        try:
            quiz = json.loads(quiz_json.strip())
            if not isinstance(quiz, dict):
                flags.append("QUIZ_FORMAT: Quiz is not a JSON object")
            elif "question" not in quiz or "options" not in quiz:
                flags.append("QUIZ_FORMAT: Quiz missing required fields (question, options)")
        except json.JSONDecodeError:
            flags.append("QUIZ_FORMAT: Invalid JSON in <quiz> block")

    # 3. Grounding check — key claims should appear in context
    if context_chunks:
        grounding_score = _check_grounding(response, context_chunks)
        if grounding_score < 0.15:
            flags.append(f"LOW_GROUNDING: Response may not be grounded in KB (score: {grounding_score:.2f})")
    else:
        grounding_score = 1.0

    # 4. Length sanity
    if len(response) > 8000:
        flags.append("RESPONSE_TOO_LONG: Response exceeds 8000 characters")

    # 5. Markdown math consistency
    if "$$" in response:
        open_count = response.count("$$")
        if open_count % 2 != 0:
            flags.append("MATH_NOTATION: Unmatched $$ delimiters")

    passed = len([f for f in flags if "FABRICATION" in f or "QUIZ_FORMAT" in f]) == 0
    score = max(0.0, 1.0 - (len(flags) * 0.15))

    return VerificationResult(passed=passed, flags=flags, score=score)


def _check_grounding(response: str, chunks: list[str]) -> float:
    """
    Simple keyword overlap grounding check.
    Returns a score 0-1 indicating how grounded the response is.
    """
    if not chunks:
        return 1.0

    response_words = set(re.findall(r"\b\w{4,}\b", response.lower()))
    context_words = set()
    for chunk in chunks:
        context_words.update(re.findall(r"\b\w{4,}\b", chunk.lower()))

    if not response_words:
        return 0.0

    overlap = response_words.intersection(context_words)
    return len(overlap) / len(response_words)


def extract_quiz_from_response(response: str) -> Optional[dict]:
    """Extract and parse a quiz block from a tutor response."""
    match = QUIZ_PATTERN.search(response)
    if match:
        try:
            return json.loads(match.group(1).strip())
        except json.JSONDecodeError:
            return None
    return None


def strip_quiz_from_response(response: str) -> str:
    """Remove <quiz>...</quiz> blocks for display purposes."""
    return QUIZ_PATTERN.sub("", response).strip()
