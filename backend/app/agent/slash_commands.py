"""Slash command parsing and behavioral instructions.

Slash commands let the learner invoke a specific tutor behavior with a single
keystroke (e.g. `/quiz` to request a knowledge check, `/simpler` to ask for an
ELI5 reframing of the previous turn). Detection is purely string-based — no
new endpoints. The router strips the command from the visible message and
injects a behavioral hint into the system prompt for that turn.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SlashCommand:
    name: str
    description: str
    instruction: str


_COMMANDS: dict[str, SlashCommand] = {
    "quiz": SlashCommand(
        name="quiz",
        description="Generate a knowledge check on the current concept",
        instruction=(
            "The learner explicitly requested a knowledge check. Respond with a "
            "single <quiz> card targeting the concept under discussion. Keep any "
            "lead-in text to one sentence."
        ),
    ),
    "hint": SlashCommand(
        name="hint",
        description="Get a small nudge without spoiling the answer",
        instruction=(
            "The learner asked for a hint. Give a small, non-spoiling nudge — "
            "the smallest piece of information that unblocks them — and end with a "
            "Socratic question that points toward the next step. Do not reveal the "
            "full answer."
        ),
    ),
    "simpler": SlashCommand(
        name="simpler",
        description="Re-explain the previous answer in simpler terms",
        instruction=(
            "The learner found the previous explanation too dense. Re-explain the "
            "same concept in dramatically simpler terms: lead with a vivid everyday "
            "analogy, avoid jargon, and use shorter sentences. Aim for clarity over "
            "completeness."
        ),
    ),
    "deeper": SlashCommand(
        name="deeper",
        description="Go deeper on the current topic with rigor",
        instruction=(
            "The learner wants a deeper, more rigorous treatment of the current "
            "topic. Go into the mathematical or theoretical detail you held back: "
            "derivations, edge cases, why the standard approach is the standard. "
            "Still use Socratic structure where natural."
        ),
    ),
    "feedback": SlashCommand(
        name="feedback",
        description="Get feedback on the learner's understanding so far",
        instruction=(
            "The learner asked for feedback on their understanding. Review the "
            "conversation so far and give an honest, specific assessment: what "
            "they've grasped solidly, what's shaky, and the single most useful "
            "next step. Be direct but encouraging — vague praise is unhelpful."
        ),
    ),
}


def list_commands() -> list[dict]:
    """Return the catalog (used by the frontend autocomplete)."""
    return [
        {"name": c.name, "description": c.description}
        for c in _COMMANDS.values()
    ]


def parse_slash_command(text: str) -> tuple[SlashCommand | None, str]:
    """Detect a leading slash command in the user message.

    Returns ``(command, remaining_text)``. If no command matched, the first
    element is ``None`` and the original text is returned unchanged.
    """
    if not text or not text.startswith("/"):
        return None, text
    head, _, tail = text[1:].partition(" ")
    head = head.strip().lower()
    cmd = _COMMANDS.get(head)
    if cmd is None:
        return None, text
    return cmd, tail.strip()
