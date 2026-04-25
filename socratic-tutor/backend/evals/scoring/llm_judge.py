"""Layer 2: LLM-as-judge scoring via the configured judge model.

v2: Uses 5 outcome-focused dimensions instead of 8 prescriptive ones.
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field

from ..config import EvalConfig, get_openai_client
from .rubric import DIMENSIONS, JUDGE_SYSTEM_PROMPT, build_judge_user_prompt

logger = logging.getLogger(__name__)


@dataclass
class DimensionScore:
    score: int
    justification: str

    def as_dict(self) -> dict:
        return {"score": self.score, "justification": self.justification}


@dataclass
class JudgeScores:
    learning_arc: DimensionScore = field(default_factory=lambda: DimensionScore(0, ""))
    conversational_craft: DimensionScore = field(default_factory=lambda: DimensionScore(0, ""))
    technical_accuracy: DimensionScore = field(default_factory=lambda: DimensionScore(0, ""))
    intellectual_engagement: DimensionScore = field(default_factory=lambda: DimensionScore(0, ""))
    adaptive_responsiveness: DimensionScore = field(default_factory=lambda: DimensionScore(0, ""))

    def as_dict(self) -> dict:
        return {
            dim: getattr(self, dim).as_dict()
            for dim in DIMENSIONS
        }

    @property
    def mean_score(self) -> float:
        scores = [getattr(self, dim).score for dim in DIMENSIONS]
        return sum(scores) / len(scores)


def _format_transcript(messages: list[dict]) -> str:
    """Format messages list into a readable transcript.

    Includes tool calls and tool results so the judge can verify
    whether the tutor's factual claims are backed by actual search evidence.
    """
    lines = []
    for msg in messages:
        role = msg.get("role", "unknown")
        content = msg.get("content", "")

        if role == "user":
            lines.append(f"### STUDENT\n\n{content}\n")
        elif role == "assistant":
            tool_calls = msg.get("tool_calls", [])
            if tool_calls:
                tc_lines = []
                for tc in tool_calls:
                    fn = tc.get("function", {})
                    name = fn.get("name", "unknown_tool")
                    args = fn.get("arguments", "")
                    tc_lines.append(f"  - **{name}**({args})")
                tool_section = "\n".join(tc_lines)
                if content:
                    lines.append(f"### TUTOR\n\n{content}\n\n*Tool calls:*\n{tool_section}\n")
                else:
                    lines.append(f"### TUTOR (tool use)\n\n*Tool calls:*\n{tool_section}\n")
            elif content:
                lines.append(f"### TUTOR\n\n{content}\n")
        elif role == "tool":
            tool_name = msg.get("name", "tool")
            lines.append(f"### TOOL RESULT ({tool_name})\n\n{content}\n")

    return "\n---\n\n".join(lines)


async def judge_conversation(
    messages: list[dict],
    lesson_content: str,
    lesson_title: str,
    config: EvalConfig,
    student_persona: str = "",
    teaching_mode: str = "default",
    reference_kb: str = "",
) -> JudgeScores:
    """Send the full conversation to the judge model for rubric-based scoring."""
    client = get_openai_client()

    transcript = _format_transcript(messages)
    user_prompt = build_judge_user_prompt(
        transcript, lesson_content, lesson_title,
        student_persona=student_persona,
        teaching_mode=teaching_mode,
        reference_kb=reference_kb,
    )

    try:
        response = await client.chat.completions.create(
            model=config.judge_model.model_id,
            messages=[
                {"role": "system", "content": JUDGE_SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=config.judge_model.max_tokens,
            temperature=config.judge_model.temperature,
        )

        raw = response.choices[0].message.content or ""
        cleaned = raw.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.split("\n", 1)[1] if "\n" in cleaned else cleaned[3:]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
            cleaned = cleaned.strip()

        data = json.loads(cleaned)
        scores = JudgeScores()
        for dim in DIMENSIONS:
            if dim in data:
                entry = data[dim]
                setattr(scores, dim, DimensionScore(
                    score=int(entry.get("score", 0)),
                    justification=str(entry.get("justification", "")),
                ))
        return scores

    except json.JSONDecodeError as e:
        logger.error("Judge returned invalid JSON: %s\nRaw: %s", e, raw)
        return JudgeScores()
    except Exception as e:
        logger.error("Judge API call failed: %s", e)
        return JudgeScores()
