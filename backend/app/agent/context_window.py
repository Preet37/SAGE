"""Conversation history budgeting.

The tutor system prompt is large (lesson content, reference KB, image catalog,
curriculum index). Long conversations occasionally bumped against the model's
context limit and the provider would either truncate silently or return a
length-finished response. This module keeps the most recent turns under a
configurable token budget without disturbing the system message or the
in-flight user turn.

Token estimation is intentionally cheap — a 4-chars-per-token heuristic is
within ~10% of true tokenization for English chat traffic and avoids pulling
in a per-model tokenizer at runtime.
"""

from __future__ import annotations

from typing import Iterable

# 4 chars per token is the standard rule of thumb for English chat with BPE
# tokenizers. Code-heavy turns trend higher, but we only need a usable upper
# bound for trimming decisions.
_CHARS_PER_TOKEN = 4


def estimate_tokens(text: str) -> int:
    if not text:
        return 0
    return max(1, len(text) // _CHARS_PER_TOKEN)


def _content_text(content) -> str:
    """Best-effort flatten of OpenAI-style message content into a string."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: list[str] = []
        for block in content:
            if isinstance(block, dict):
                # tool_result blocks have a "content" field; text blocks have "text"
                if "text" in block and isinstance(block["text"], str):
                    parts.append(block["text"])
                elif "content" in block and isinstance(block["content"], str):
                    parts.append(block["content"])
        return " ".join(parts)
    return ""


def _message_tokens(msg: dict) -> int:
    """Estimate tokens for a single chat message including role overhead."""
    text = _content_text(msg.get("content", ""))
    # Tool calls carry their JSON arguments — count those too.
    for tc in msg.get("tool_calls", []) or []:
        fn = tc.get("function", {}) if isinstance(tc, dict) else {}
        text += fn.get("name", "") + fn.get("arguments", "")
    # 4 tokens of role/format overhead per message in OpenAI-style protocols.
    return estimate_tokens(text) + 4


def trim_messages_to_budget(
    messages: Iterable[dict],
    budget_tokens: int,
    *,
    keep_system: bool = True,
) -> list[dict]:
    """Drop the oldest turns until the running total fits under ``budget_tokens``.

    The most recent message is always kept (that's the user's current turn).
    The system message is preserved when ``keep_system`` is set, since callers
    typically inject lesson content there. Tool-call/tool-result pairs are kept
    contiguous: if a ``tool`` message is the oldest survivor, we also drop its
    preceding ``assistant`` message so the surviving history stays valid.
    """
    msgs = list(messages)
    if not msgs:
        return msgs
    if budget_tokens <= 0:
        return msgs

    head: list[dict] = []
    if keep_system and msgs and msgs[0].get("role") == "system":
        head.append(msgs[0])
        msgs = msgs[1:]

    if not msgs:
        return head

    # Reserve at least the final user turn — never drop it.
    final = msgs[-1]
    rest = msgs[:-1]

    head_cost = sum(_message_tokens(m) for m in head)
    final_cost = _message_tokens(final)
    remaining = max(0, budget_tokens - head_cost - final_cost)

    kept_reversed: list[dict] = []
    for msg in reversed(rest):
        cost = _message_tokens(msg)
        if cost > remaining:
            break
        kept_reversed.append(msg)
        remaining -= cost

    kept = list(reversed(kept_reversed))

    # If the surviving history begins with an orphan ``tool`` reply (no matching
    # assistant tool_call ahead of it), drop it — the API rejects unmatched tool
    # messages.
    while kept and kept[0].get("role") == "tool":
        kept.pop(0)

    return head + kept + [final]
