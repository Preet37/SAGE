"""Simulated student for multi-turn eval conversations.

Supports two modes:
  - Scripted: plays back pre-defined turns from the scenario YAML.
  - LLM-driven: uses a lightweight model with a persona prompt to generate
    realistic student responses after scripted turns are exhausted.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any

import yaml
from pathlib import Path

from .config import EvalConfig, SCENARIOS_DIR, get_openai_client

logger = logging.getLogger(__name__)


@dataclass
class Scenario:
    id: str
    title: str
    lesson_slug: str
    description: str
    persona: str
    mode: str
    scripted_turns: list[dict[str, str]]
    expected_behaviors: list[str]
    diagram_expected: bool = False

    @classmethod
    def from_yaml(cls, path: Path) -> "Scenario":
        with open(path) as f:
            data = yaml.safe_load(f)
        return cls(
            id=data["id"],
            title=data["title"],
            lesson_slug=data["lesson_slug"],
            description=data.get("description", ""),
            persona=data.get("persona", ""),
            mode=data.get("mode", "default"),
            scripted_turns=data.get("scripted_turns", []),
            expected_behaviors=data.get("expected_behaviors", []),
            diagram_expected=data.get("diagram_expected", False),
        )

    @classmethod
    def load_all(cls, lesson_slug: str = "lora") -> list["Scenario"]:
        scenarios = []
        for path in sorted(SCENARIOS_DIR.glob(f"{lesson_slug}_*.yaml")):
            try:
                scenarios.append(cls.from_yaml(path))
            except Exception as e:
                logger.warning("Failed to load scenario %s: %s", path.name, e)
        return scenarios


STUDENT_SYSTEM_PROMPT_TEMPLATE = """You are a student in a tutoring session about ML/AI topics.

PERSONA:
{persona}

RULES:
- Stay in character as described in the persona above.
- Respond naturally to the tutor's questions and explanations.
- Keep responses concise (2-4 sentences typically).
- If the tutor asks you a question, TRY TO ANSWER IT based on your persona's knowledge level — even if your answer is wrong or partial. A real student would attempt an answer, not just say "I don't know."
- If you're supposed to have a misconception, hold onto it until the tutor convincingly corrects it.
- Do NOT break character or mention that you are a simulated student.
- Do NOT use markdown headers or formatting. Write plain conversational text.

HOW TO EXPRESS CONFUSION (IMPORTANT):
- NEVER just say "I'm not sure" or "can you explain more?" — that is too vague and unhelpful.
- Instead, be SPECIFIC about what confuses you. Real students say things like:
  - "I get the freezing part, but I don't understand why we need TWO matrices instead of one"
  - "Wait, so the rank r controls how expressive the update is? What happens if r is too small?"
  - "I think I follow the analogy but I'm lost on how that maps to the actual math"
  - "So you're saying the original weights don't change at all? Then how does the model actually learn anything new?"
  - "Could you show me a concrete example with actual numbers? The abstract notation is hard to follow"
- If the tutor explains something well, ACKNOWLEDGE what clicked and then ask a follow-up that goes deeper or connects to something else.
- Show your reasoning process — say what you THINK the answer might be, even if uncertain."""


class StudentSimulator:
    """Generates student messages, first from scripted turns, then via LLM."""

    def __init__(self, scenario: Scenario, config: EvalConfig):
        self.scenario = scenario
        self.config = config
        self._scripted_index = 0

    @property
    def has_scripted_turn(self) -> bool:
        return self._scripted_index < len(self.scenario.scripted_turns)

    def next_scripted(self) -> str | None:
        if not self.has_scripted_turn:
            return None
        turn = self.scenario.scripted_turns[self._scripted_index]
        self._scripted_index += 1
        content = turn.get("content", "")
        return content.strip()

    async def generate_response(self, conversation: list[dict]) -> str:
        """Generate the next student message.

        Uses scripted turns first, then falls back to LLM generation.
        """
        scripted = self.next_scripted()
        if scripted is not None:
            return scripted

        return await self._llm_response(conversation)

    async def _llm_response(self, conversation: list[dict]) -> str:
        """Use the student sim model to generate a persona-driven response."""
        client = get_openai_client()

        system = STUDENT_SYSTEM_PROMPT_TEMPLATE.format(persona=self.scenario.persona)

        # Build the conversation as a single user prompt with clear formatting.
        # Role-swapping confuses smaller models, so we present the full
        # transcript and ask for the next student reply.
        transcript_lines = []
        for msg in conversation:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            if role == "assistant":
                transcript_lines.append(f"TUTOR: {content}")
            elif role == "user":
                transcript_lines.append(f"YOU (student): {content}")

        transcript = "\n\n".join(transcript_lines)

        user_prompt = (
            f"Here is the conversation so far:\n\n{transcript}\n\n"
            "---\n"
            "Write your next reply as the student. Remember:\n"
            "- Be SPECIFIC about what you understand and what confuses you\n"
            "- If the tutor asked you a question, ATTEMPT to answer it (even if your answer is wrong or uncertain)\n"
            "- Do NOT just say 'I'm not sure' or 'can you explain more' — say WHAT specifically is unclear\n"
            "- Keep it to 2-4 sentences, plain conversational text, no markdown\n\n"
            "Your reply:"
        )

        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": user_prompt},
        ]

        try:
            response = await client.chat.completions.create(
                model=self.config.student_model.model_id,
                messages=messages,
                max_tokens=self.config.student_model.max_tokens,
                temperature=self.config.student_model.temperature,
            )
            reply = (response.choices[0].message.content or "").strip()
            if not reply or reply.lower() in ("i'm not sure", "i'm not sure, can you explain more?"):
                return "I think I follow the high-level idea, but I'm lost on how the math works. Can you show me with a small concrete example?"
            return reply
        except Exception as e:
            logger.error("Student LLM generation failed: %s", e)
            return "I get the general concept, but could you walk me through a specific numerical example? That would help me see how it works."
