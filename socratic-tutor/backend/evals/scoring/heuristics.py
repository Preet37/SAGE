"""Layer 1: Deterministic heuristic checks on tutor responses.

Two categories:
  - Safety checks (quiz JSON validity, fabricated URLs, notation consistency)
  - Format-compliance checks (quiz card vs plaintext, resource URL presence,
    duplicate resources, response length, mermaid format)

Each check function returns a float in [0, 1]. Higher is better.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from statistics import median


QUIZ_BLOCK_PATTERN = re.compile(r"<quiz>([\s\S]*?)</quiz>")
RESOURCE_BLOCK_PATTERN = re.compile(r"<resource>([\s\S]*?)</resource>")
MERMAID_FENCED_PATTERN = re.compile(r"```mermaid\s*\n[\s\S]*?```")
FLOW_BLOCK_PATTERN = re.compile(r"<flow>([\s\S]*?)</flow>")
ARCHITECTURE_BLOCK_PATTERN = re.compile(r"<architecture>([\s\S]*?)</architecture>")
URL_PATTERN = re.compile(r"https?://[^\s)\]]+")

# Matches lines like "A. Option text", "(a) option text", "A) Option text"
# Requires at least two such options within a region to count as a choice list
PLAINTEXT_OPTION_PATTERN = re.compile(
    r"(?:^|\n)\s*(?:\(?[A-Da-d]\)|[A-Da-d][\.\)])\s+\S",
)

SUPERSCRIPT_MAP = {
    'ᵃ': 'a', 'ᵇ': 'b', 'ᵈ': 'd', 'ᵏ': 'k', 'ⁿ': 'n',
    'ʳ': 'r', 'ˣ': 'x',
}


@dataclass
class HeuristicScores:
    """Scores for a single tutor response (format safety only).

    Behavioral checks (quiz_card_used, resource_has_url, tool_diversity)
    have moved to scoring/behavioral.py.
    """
    quiz_format_valid: float | None = None
    no_fabricated_urls: float = 1.0
    structured_output_valid: float | None = None  # None = no structured blocks
    response_length: int = 0                       # raw char count (not a 0-1 score)

    def as_dict(self) -> dict:
        d: dict = {"no_fabricated_urls": self.no_fabricated_urls}
        if self.quiz_format_valid is not None:
            d["quiz_format_valid"] = self.quiz_format_valid
        if self.structured_output_valid is not None:
            d["structured_output_valid"] = self.structured_output_valid
        d["response_length"] = self.response_length
        return d

    @property
    def mean_score(self) -> float:
        vals = [self.no_fabricated_urls]
        if self.quiz_format_valid is not None:
            vals.append(self.quiz_format_valid)
        if self.structured_output_valid is not None:
            vals.append(self.structured_output_valid)
        return sum(vals) / len(vals)


@dataclass
class ConversationHeuristicScores:
    """Aggregate heuristic scores for an entire conversation.

    tool_diversity has moved to scoring/behavioral.py.
    """
    per_response: list[HeuristicScores] = field(default_factory=list)
    notation_consistency: float = 1.0
    no_duplicate_resources: float = 1.0
    median_response_length: float = 0.0

    def as_dict(self) -> dict:
        return {
            "per_response": [s.as_dict() for s in self.per_response],
            "notation_consistency": self.notation_consistency,
            "no_duplicate_resources": self.no_duplicate_resources,
            "median_response_length": self.median_response_length,
            "mean_per_response": self.mean_per_response,
            "overall": self.overall,
        }

    @property
    def mean_per_response(self) -> float:
        if not self.per_response:
            return 1.0
        return sum(s.mean_score for s in self.per_response) / len(self.per_response)

    @property
    def overall(self) -> float:
        scores = [self.mean_per_response, self.notation_consistency,
                  self.no_duplicate_resources]
        return sum(scores) / len(scores)


# ---------------------------------------------------------------------------
# Individual check functions
# ---------------------------------------------------------------------------

def check_quiz_valid(content: str) -> float | None:
    """If a <quiz> block is present, is it well-formed JSON with required keys?
    Returns None if no quiz block exists (not penalized)."""
    matches = QUIZ_BLOCK_PATTERN.findall(content)
    if not matches:
        return None

    valid = 0
    for match in matches:
        try:
            data = json.loads(match.strip())
            required = {"question", "options", "correct", "explanation"}
            if required.issubset(data.keys()):
                if isinstance(data["options"], list) and len(data["options"]) >= 2:
                    valid += 1
        except (json.JSONDecodeError, TypeError):
            pass

    return valid / len(matches)


def check_no_fabricated_urls(content: str, search_tool_used: bool = False) -> float:
    """Response should not contain URLs unless search_web was called."""
    urls = URL_PATTERN.findall(content)
    if not urls:
        return 1.0
    if search_tool_used:
        return 1.0
    return 0.0


def check_quiz_card_used(content: str) -> float | None:
    """Detect when the tutor presents multiple-choice options as plain text
    instead of using a <quiz> card. Returns None if no options are detected,
    1.0 if options are properly wrapped in <quiz>, 0.0 if plain-text options
    appear without a card."""
    has_quiz_block = bool(QUIZ_BLOCK_PATTERN.search(content))

    # Strip out quiz blocks before checking for plaintext options
    stripped = QUIZ_BLOCK_PATTERN.sub("", content)
    plaintext_options = PLAINTEXT_OPTION_PATTERN.findall(stripped)
    has_plaintext_options = len(plaintext_options) >= 2

    if not has_quiz_block and not has_plaintext_options:
        return None  # no options at all — not penalized
    if has_quiz_block and not has_plaintext_options:
        return 1.0   # properly used card
    if has_plaintext_options:
        return 0.0   # options in prose without a card
    return 1.0


def check_resource_has_url(content: str) -> float | None:
    """If <resource> blocks exist, verify they contain a url field.
    Returns None if no resource blocks present."""
    matches = RESOURCE_BLOCK_PATTERN.findall(content)
    if not matches:
        return None

    valid = 0
    for match in matches:
        try:
            data = json.loads(match.strip())
            if data.get("url"):
                valid += 1
        except (json.JSONDecodeError, TypeError):
            pass

    return valid / len(matches)


def check_no_duplicate_resources(messages: list[dict]) -> float:
    """Track resource titles/URLs across the conversation; penalize repeats.
    Returns 1.0 if all unique, scales down with duplicates."""
    seen_keys: set[str] = set()
    total = 0
    unique = 0

    for msg in messages:
        if msg.get("role") != "assistant":
            continue
        content = msg.get("content") or ""
        for match in RESOURCE_BLOCK_PATTERN.findall(content):
            try:
                data = json.loads(match.strip())
            except (json.JSONDecodeError, TypeError):
                continue
            total += 1
            key = data.get("url") or data.get("title") or match.strip()
            if key not in seen_keys:
                seen_keys.add(key)
                unique += 1

    if total == 0:
        return 1.0
    return unique / total


def check_tool_diversity(messages: list[dict]) -> float:
    """Check if the conversation used any tools at all.

    Returns 1.0 if at least one tool was used, 0.0 if no tools.
    Flags conversations where the tutor relied purely on its base knowledge
    without using search, KB lookup, or other tools.
    """
    tools_used: set[str] = set()

    for msg in messages:
        if msg.get("tool_used"):
            tools_used.add(msg["tool_used"])
        if msg.get("message_meta"):
            try:
                meta = json.loads(msg["message_meta"]) if isinstance(msg["message_meta"], str) else msg["message_meta"]
                for tool in meta.get("tools_used", []):
                    tools_used.add(tool)
            except (json.JSONDecodeError, TypeError):
                pass

    return 1.0 if tools_used else 0.0


def check_structured_output_valid(content: str) -> float | None:
    """Validate that structured output blocks (mermaid, flow, architecture) are well-formed.

    Returns None if no structured blocks present.
    Returns 1.0 if all blocks are valid, 0.0-1.0 based on validity ratio.
    """
    total = 0
    valid = 0

    # Check mermaid blocks
    mermaid_matches = MERMAID_FENCED_PATTERN.findall(content)
    for match in mermaid_matches:
        total += 1
        inner = match.replace("```mermaid", "").replace("```", "").strip()
        if inner and len(inner) > 10:
            if any(kw in inner.lower() for kw in ["graph", "flowchart", "sequencediagram", "classDiagram", "stateDiagram", "pie", "gantt", "-->", "---"]):
                valid += 1

    # Check <flow> blocks
    flow_matches = FLOW_BLOCK_PATTERN.findall(content)
    for match in flow_matches:
        total += 1
        try:
            data = json.loads(match.strip())
            if isinstance(data, dict) and ("steps" in data or "nodes" in data or "flow" in data):
                valid += 1
            elif isinstance(data, list) and len(data) > 0:
                valid += 1
        except (json.JSONDecodeError, TypeError):
            pass

    # Check <architecture> blocks
    arch_matches = ARCHITECTURE_BLOCK_PATTERN.findall(content)
    for match in arch_matches:
        total += 1
        try:
            data = json.loads(match.strip())
            if isinstance(data, dict) and ("components" in data or "layers" in data or "nodes" in data):
                valid += 1
            elif isinstance(data, list) and len(data) > 0:
                valid += 1
        except (json.JSONDecodeError, TypeError):
            pass

    if total == 0:
        return None
    return valid / total


# ---------------------------------------------------------------------------
# Notation consistency helpers
# ---------------------------------------------------------------------------

def _normalize_superscripts(text: str) -> str:
    """Replace Unicode superscript letters with ASCII equivalents."""
    for sup, normal in SUPERSCRIPT_MAP.items():
        text = text.replace(sup, normal)
    return text


def _extract_product_orders(text: str) -> set[str]:
    """Extract matrix product orderings (AB vs BA) for delta-W decomposition."""
    orders: set[str] = set()
    normalized = _normalize_superscripts(text)
    patterns = [
        r'(?:ΔW\s*=|W[₀0]?\s*\+)\s*([AB])\s*[·\*×⋅.]?\s*([AB])',
        r'\(\s*([AB])\s*[·\*×⋅.]?\s*([AB])\s*\)',
    ]
    for pat in patterns:
        for m in re.finditer(pat, normalized):
            first, second = m.group(1).upper(), m.group(2).upper()
            if first != second:
                orders.add(first + second)
    return orders


def _extract_matrix_shapes(text: str) -> dict[str, str]:
    """Extract shape assignments for matrices A and B.

    Returns dict like {'A': 'dxr', 'B': 'rxk'} with normalized dimensions.
    """
    normalized = _normalize_superscripts(text)
    shapes: dict[str, str] = {}
    patterns = [
        r'(?:^|\W)([AB])\W[^A-Za-z]{0,20}\(?([drk])\s*[×x]\s*([drk])\)?',
        r'\b([AB])\b.{0,30}?(?:shape|:)\s*\(?([drk])\s*[×x]\s*([drk])\)?',
        r'\b([AB])\s*[∈∊]\s*ℝ([drk])x([drk])',
    ]
    for pat in patterns:
        for m in re.finditer(pat, normalized, re.MULTILINE):
            name = m.group(1).upper()
            if name not in shapes:
                shapes[name] = f"{m.group(2).lower()}x{m.group(3).lower()}"
    return shapes


def check_notation_consistency(messages: list[dict], lesson_content: str) -> float:
    """Check if the tutor's mathematical notation matches the lesson conventions.

    Compares matrix product ordering and shape assignments against ground truth.
    Returns 1.0 for consistent, 0.0 for contradictory, 0.5 if indeterminate.
    """
    if not lesson_content:
        return 1.0

    lesson_orders = _extract_product_orders(lesson_content)
    lesson_shapes = _extract_matrix_shapes(lesson_content)

    if not lesson_orders and not lesson_shapes:
        return 1.0

    tutor_text = " ".join(
        (msg.get("content") or "") for msg in messages if msg.get("role") == "assistant"
    )
    tutor_orders = _extract_product_orders(tutor_text)
    tutor_shapes = _extract_matrix_shapes(tutor_text)

    scores: list[float] = []

    if lesson_orders and tutor_orders:
        if tutor_orders == lesson_orders:
            scores.append(1.0)
        elif tutor_orders & lesson_orders:
            scores.append(0.5)
        else:
            scores.append(0.0)

    if lesson_shapes and tutor_shapes:
        common_keys = set(tutor_shapes) & set(lesson_shapes)
        if common_keys:
            matching = sum(
                1 for k in common_keys if tutor_shapes[k] == lesson_shapes[k]
            )
            scores.append(matching / len(common_keys))

    return sum(scores) / len(scores) if scores else 1.0


# ---------------------------------------------------------------------------
# Main scoring entry points
# ---------------------------------------------------------------------------

def score_response(
    content: str,
    search_tool_used: bool = False,
    **_kwargs,
) -> HeuristicScores:
    """Score a single tutor response on safety + format-compliance heuristics."""
    return HeuristicScores(
        quiz_format_valid=check_quiz_valid(content),
        no_fabricated_urls=check_no_fabricated_urls(content, search_tool_used),
        structured_output_valid=check_structured_output_valid(content),
        response_length=len(content),
    )


def score_conversation(
    messages: list[dict],
    lesson_content: str = "",
    **_kwargs,
) -> ConversationHeuristicScores:
    """Score an entire conversation transcript.

    `messages` is a list of dicts with 'role' and 'content' keys,
    optionally 'search_tool_used' (bool).
    """
    result = ConversationHeuristicScores()

    for msg in messages:
        if msg.get("role") != "assistant":
            continue

        content = msg.get("content") or ""
        search_used = msg.get("search_tool_used", False)
        scores = score_response(content, search_used)
        result.per_response.append(scores)

    result.notation_consistency = check_notation_consistency(messages, lesson_content)
    result.no_duplicate_resources = check_no_duplicate_resources(messages)

    lengths = [s.response_length for s in result.per_response if s.response_length > 0]
    result.median_response_length = median(lengths) if lengths else 0.0

    return result
