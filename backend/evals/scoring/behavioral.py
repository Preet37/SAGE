"""Layer 0: Deterministic behavioral metrics extracted from conversation transcripts.

Each metric maps directly to a prompt instruction, providing a fast feedback
signal for prompt iteration.  Zero LLM calls — runs in milliseconds.

Metrics are NOT aggregated into a single score.  They are individual signals
that tell you *which specific prompt instruction* is or isn't working.
"""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass, field
from pathlib import Path


# ---------------------------------------------------------------------------
# Patterns
# ---------------------------------------------------------------------------

_QUESTION_END = re.compile(
    r"\?\s*(?:```[\s\S]*?```\s*)*"       # question mark, optionally followed by code blocks
    r"(?:</?(?:quiz|resource|image|flow|architecture)>[\s\S]*?)*"
    r"\s*$",
)

_OPEN_QUESTION = re.compile(
    r"\b(?:what|how|why|when|where|which|in what way|can you explain|"
    r"what do you think|what would happen|how would you|how does|how do|"
    r"what if|why do you think|why is)\b",
    re.IGNORECASE,
)

_CLOSED_QUESTION = re.compile(
    r"(?:right\?|correct\?|make sense\?|does that make sense\?|"
    r"do you follow\?|got it\?|see what I mean\?|fair enough\?|okay\?|"
    r"sound good\?|does that help\?|clear\?|ready to move on\?)",
    re.IGNORECASE,
)

_BACKWARD_REF = re.compile(
    r"\b(?:earlier|as we (?:saw|discussed|covered|mentioned|noted)|"
    r"building on|remember when|recall (?:that|how|when)|"
    r"going back to|from before|in our earlier|as I mentioned|"
    r"like we said|extending (?:the|our) (?:analogy|example|metaphor))\b",
    re.IGNORECASE,
)

_IMAGE_TAG = re.compile(r"<image>\s*(\{.*?\})\s*</image>", re.DOTALL)
_QUIZ_TAG = re.compile(r"<quiz>[\s\S]*?</quiz>")
_RESOURCE_TAG = re.compile(r"<resource>[\s\S]*?</resource>")
_MERMAID_TAG = re.compile(r"```mermaid\s*\n[\s\S]*?```")
_FLOW_TAG = re.compile(r"<flow>[\s\S]*?</flow>")
_ARCH_TAG = re.compile(r"<architecture>[\s\S]*?</architecture>")
_CODE_TAG = re.compile(r"```(?:python|javascript|typescript|bash|sql|java|cpp|c\b)")
_MATH_TAG = re.compile(r"\$\$.*?\$\$|\\\[.*?\\\]", re.DOTALL)

_VISUAL_REQUEST = re.compile(
    r"\b(?:show me|draw|diagram|picture|visual|visualize|image|"
    r"can you (?:draw|show|illustrate)|flowchart|architecture diagram)\b",
    re.IGNORECASE,
)

_IMAGE_PATH = re.compile(r"/api/(?:wiki-images|images)/[^\s\"']+")

_WIKI_DIR = Path(
    os.environ.get("CONTENT_DIR", str(Path(__file__).parent.parent.parent.parent / "content"))
).resolve() / "pedagogy-wiki"


# ---------------------------------------------------------------------------
# Dataclass
# ---------------------------------------------------------------------------

@dataclass
class BehavioralScores:
    """Deterministic behavioral metrics for a single conversation."""

    # Socratic method
    question_ratio: float = 0.0
    open_question_ratio: float = 0.0
    questions_total: int = 0
    questions_open: int = 0
    questions_closed: int = 0

    # Image usage
    image_proactive_count: int = 0
    image_reactive_count: int = 0
    image_total_count: int = 0
    image_latency: int | None = None

    # Modality diversity
    modality_count: int = 0
    modalities_used: list[str] = field(default_factory=list)
    first_modality_turn: int | None = None

    # Toolkit usage counts
    quiz_count: int = 0
    resource_count: int = 0
    mermaid_count: int = 0
    flow_count: int = 0
    architecture_count: int = 0
    code_count: int = 0
    math_count: int = 0

    # Conversation shape
    avg_assistant_length: float = 0.0
    backward_reference_count: int = 0

    # Image path validity
    image_paths_total: int = 0
    image_paths_valid: int = 0
    image_path_valid_ratio: float = 1.0

    # Tool usage
    tools_used: list[str] = field(default_factory=list)
    tool_call_count: int = 0

    def as_dict(self) -> dict:
        return {
            "question_ratio": round(self.question_ratio, 3),
            "open_question_ratio": round(self.open_question_ratio, 3),
            "questions_total": self.questions_total,
            "questions_open": self.questions_open,
            "questions_closed": self.questions_closed,
            "image_proactive_count": self.image_proactive_count,
            "image_reactive_count": self.image_reactive_count,
            "image_total_count": self.image_total_count,
            "image_latency": self.image_latency,
            "modality_count": self.modality_count,
            "modalities_used": self.modalities_used,
            "first_modality_turn": self.first_modality_turn,
            "quiz_count": self.quiz_count,
            "resource_count": self.resource_count,
            "mermaid_count": self.mermaid_count,
            "flow_count": self.flow_count,
            "architecture_count": self.architecture_count,
            "code_count": self.code_count,
            "math_count": self.math_count,
            "avg_assistant_length": round(self.avg_assistant_length, 1),
            "backward_reference_count": self.backward_reference_count,
            "image_paths_total": self.image_paths_total,
            "image_paths_valid": self.image_paths_valid,
            "image_path_valid_ratio": round(self.image_path_valid_ratio, 3),
            "tools_used": self.tools_used,
            "tool_call_count": self.tool_call_count,
        }


# ---------------------------------------------------------------------------
# Scoring functions
# ---------------------------------------------------------------------------

def _extract_last_question(text: str) -> str | None:
    """Extract the last sentence ending with '?' from assistant text."""
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    for s in reversed(sentences):
        if s.strip().endswith("?"):
            return s.strip()
    return None


def _student_asked_for_visual(messages: list[dict], up_to_index: int) -> bool:
    """Check if any preceding user message asked for a visual."""
    for i in range(up_to_index - 1, -1, -1):
        msg = messages[i]
        if msg.get("role") == "user":
            return bool(_VISUAL_REQUEST.search(msg.get("content", "")))
        if msg.get("role") == "assistant":
            break
    return False


def _check_image_path(path: str) -> bool:
    """Check if an image path resolves to a real file on disk."""
    # /api/wiki-images/{topic}/images/{file}
    m = re.match(r"/api/wiki-images/([^/]+)/images/(.+)", path)
    if m:
        topic, filename = m.group(1), m.group(2)
        file_path = _WIKI_DIR / "resources" / "by-topic" / topic / "images" / filename
        return file_path.is_file()

    # /api/images/{id} — can't resolve without DB, assume valid
    if re.match(r"/api/images/\w+", path):
        return True

    return False


def score_behavioral(messages: list[dict]) -> BehavioralScores:
    """Compute all behavioral metrics from a conversation transcript."""
    result = BehavioralScores()

    assistant_turns = []
    assistant_lengths = []
    modalities: set[str] = set()
    tools: set[str] = set()
    tool_count = 0
    all_image_paths: list[str] = []

    assistant_turn_num = 0
    for i, msg in enumerate(messages):
        role = msg.get("role", "")
        content = msg.get("content", "") or ""

        # Track tool calls
        if role == "assistant" and msg.get("tool_calls"):
            for tc in msg["tool_calls"]:
                fn = tc.get("function", {})
                name = fn.get("name", "")
                if name:
                    tools.add(name)
                    tool_count += 1

        # Track tool results from message_meta
        if role == "assistant" and msg.get("message_meta"):
            try:
                meta = json.loads(msg["message_meta"]) if isinstance(msg["message_meta"], str) else msg["message_meta"]
                for t in meta.get("tools_used", []):
                    tools.add(t)
                    tool_count += 1
            except (json.JSONDecodeError, TypeError):
                pass

        if role != "assistant" or not content:
            continue

        # Skip tool-call-only assistant messages (no text content)
        if msg.get("tool_calls") and not content.strip():
            continue

        assistant_turn_num += 1
        assistant_turns.append(content)
        assistant_lengths.append(len(content.split()))

        # Questions
        last_q = _extract_last_question(content)
        if last_q or _QUESTION_END.search(content):
            result.questions_total += 1
            q_text = last_q or content
            if _OPEN_QUESTION.search(q_text):
                result.questions_open += 1
            elif _CLOSED_QUESTION.search(q_text):
                result.questions_closed += 1
            else:
                result.questions_open += 1

        # Images
        image_matches = _IMAGE_TAG.findall(content)
        if image_matches:
            result.image_total_count += len(image_matches)
            if result.image_latency is None:
                result.image_latency = assistant_turn_num

            is_reactive = _student_asked_for_visual(messages, i)
            if is_reactive:
                result.image_reactive_count += len(image_matches)
            else:
                result.image_proactive_count += len(image_matches)

            for match in image_matches:
                try:
                    data = json.loads(match)
                    path = data.get("path", "")
                    if path:
                        all_image_paths.append(path)
                except (json.JSONDecodeError, TypeError):
                    pass

        # Also check for image paths in raw text
        for path in _IMAGE_PATH.findall(content):
            if path not in [p for p in all_image_paths]:
                all_image_paths.append(path)

        # Modalities
        if _QUIZ_TAG.search(content):
            modalities.add("quiz")
            result.quiz_count += len(_QUIZ_TAG.findall(content))
        if _IMAGE_TAG.search(content):
            modalities.add("image")
        if _MERMAID_TAG.search(content):
            modalities.add("mermaid")
            result.mermaid_count += len(_MERMAID_TAG.findall(content))
        if _FLOW_TAG.search(content):
            modalities.add("flow")
            result.flow_count += len(_FLOW_TAG.findall(content))
        if _ARCH_TAG.search(content):
            modalities.add("architecture")
            result.architecture_count += len(_ARCH_TAG.findall(content))
        if _CODE_TAG.search(content):
            modalities.add("code")
            result.code_count += len(_CODE_TAG.findall(content))
        if _MATH_TAG.search(content):
            modalities.add("math")
            result.math_count += len(_MATH_TAG.findall(content))
        if _RESOURCE_TAG.search(content):
            modalities.add("resource")
            result.resource_count += len(_RESOURCE_TAG.findall(content))

        if modalities and result.first_modality_turn is None:
            result.first_modality_turn = assistant_turn_num

        # Backward references
        result.backward_reference_count += len(_BACKWARD_REF.findall(content))

    # Aggregate
    total_assistant = len(assistant_turns)
    if total_assistant > 0:
        result.question_ratio = result.questions_total / total_assistant
        result.avg_assistant_length = sum(assistant_lengths) / total_assistant

    if result.questions_total > 0:
        result.open_question_ratio = result.questions_open / result.questions_total

    result.modality_count = len(modalities)
    result.modalities_used = sorted(modalities)

    result.tools_used = sorted(tools)
    result.tool_call_count = tool_count

    # Image path validation
    result.image_paths_total = len(all_image_paths)
    valid = sum(1 for p in all_image_paths if _check_image_path(p))
    result.image_paths_valid = valid
    if all_image_paths:
        result.image_path_valid_ratio = valid / len(all_image_paths)

    return result
