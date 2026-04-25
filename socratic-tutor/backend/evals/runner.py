"""Eval runner: orchestrates multi-turn conversations and scoring.

Reuses the real system prompt, tools, and tool handlers from the app,
but with its own OpenAI client for clean model control.
"""

from __future__ import annotations

import asyncio
import json
import logging
import sys
import os
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

# Ensure backend app modules are importable
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.agent.system_prompt import build_system_prompt as build_system_prompt_v1
from app.agent.system_prompt_v2 import build_system_prompt_v2
from app.agent.system_prompt_explore import build_exploration_prompt
from app.agent.context import TutorContext
from app.agent.tools import TUTOR_TOOLS
from app.agent.tool_handlers import execute_tool

from .config import EvalConfig, ModelConfig, RESULTS_DIR, get_openai_client
from .student_simulator import Scenario, StudentSimulator
from .scoring.heuristics import score_conversation, ConversationHeuristicScores
from .scoring.behavioral import score_behavioral, BehavioralScores
from .scoring.llm_judge import judge_conversation, JudgeScores
from .scoring.prompt_alignment import judge_prompt_alignment, AlignmentScores

PROMPT_BUILDERS = {
    "v1": build_system_prompt_v1,
    "v2": build_system_prompt_v2,
    "v2-explore": build_exploration_prompt,
}

# Module-level default; can be overridden by callers or monkey-patching
build_system_prompt = build_system_prompt_v2

logger = logging.getLogger(__name__)

MAX_TOOL_STEPS = 5

def _load_eval_curriculum() -> list[dict]:
    """Build curriculum index from DB. Falls back to empty list if no lessons."""
    try:
        from sqlmodel import Session, select
        from app.db import engine
        from app.models.learning import Lesson
        with Session(engine) as session:
            lessons = session.exec(select(Lesson)).all()
            if not lessons:
                logger.warning("No lessons in DB — run seed.py first")
                return []
            return [
                {
                    "slug": lesson.slug,
                    "title": lesson.title,
                    "concepts": [c.strip() for c in (lesson.concepts or "").split(",") if c.strip()],
                }
                for lesson in lessons
            ]
    except Exception as e:
        logger.warning("Could not load curriculum from DB: %s", e)
        return []

EVAL_CURRICULUM_INDEX = _load_eval_curriculum()


def _get_lesson_content(lesson_slug: str) -> tuple[str, str, str, list[str], str, str, list[dict]]:
    """Load lesson metadata for eval context from the database.

    Returns (lesson_id, title, summary, concepts, content, reference_kb, available_images).
    """
    from sqlmodel import Session, select
    from app.db import engine
    from app.models.learning import Lesson

    with Session(engine) as session:
        lesson = session.exec(
            select(Lesson).where(Lesson.slug == lesson_slug)
        ).first()
        if lesson:
            concepts = json.loads(lesson.concepts) if lesson.concepts else []
            images: list[dict] = []
            if lesson.image_metadata:
                try:
                    images = json.loads(lesson.image_metadata)
                except (json.JSONDecodeError, TypeError):
                    pass
            return (
                lesson.id,
                lesson.title,
                lesson.summary,
                concepts,
                lesson.content,
                lesson.reference_kb or "",
                images,
            )

    raise ValueError(
        f"Lesson '{lesson_slug}' not found in database. "
        f"Run seed.py first or use a valid lesson slug."
    )


@dataclass
class TutorTurnResult:
    text: str
    search_used: bool
    tool_messages: list[dict]


async def run_tutor_turn(
    messages: list[dict],
    context: TutorContext,
    model: ModelConfig,
) -> TutorTurnResult:
    """Run a single tutor turn (may include tool calls).

    Returns a TutorTurnResult with the final text, search flag,
    and all intermediate tool-call / tool-result messages so the
    judge can verify claims against actual search evidence.
    """
    client = get_openai_client()
    system_msg = {"role": "system", "content": build_system_prompt(context)}
    api_messages = [system_msg] + messages

    search_used = False
    tool_messages: list[dict] = []
    steps = 0

    while steps < MAX_TOOL_STEPS:
        steps += 1
        response = await client.chat.completions.create(
            model=model.model_id,
            messages=api_messages,
            tools=TUTOR_TOOLS,
            max_tokens=model.max_tokens,
            temperature=model.temperature,
        )

        choice = response.choices[0]
        finish_reason = choice.finish_reason

        if finish_reason in ("stop", "length", None):
            return TutorTurnResult(choice.message.content or "", search_used, tool_messages)

        if finish_reason == "tool_calls" and choice.message.tool_calls:
            assistant_msg = {
                "role": "assistant",
                "content": choice.message.content,
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments,
                        },
                    }
                    for tc in choice.message.tool_calls
                ],
            }
            api_messages.append(assistant_msg)
            tool_messages.append(assistant_msg)

            for tc in choice.message.tool_calls:
                if tc.function.name == "search_web":
                    search_used = True
                try:
                    tool_input = json.loads(tc.function.arguments)
                except json.JSONDecodeError:
                    tool_input = {}

                result = await execute_tool(tc.function.name, tool_input, context)
                tool_result_msg = {
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "name": tc.function.name,
                    "content": json.dumps(result),
                }
                api_messages.append(tool_result_msg)
                tool_messages.append(tool_result_msg)

    return TutorTurnResult(choice.message.content or "", search_used, tool_messages)


@dataclass
class ScenarioResult:
    scenario_id: str
    scenario_title: str
    messages: list[dict] = field(default_factory=list)
    behavioral_scores: BehavioralScores | None = None
    heuristic_scores: ConversationHeuristicScores | None = None
    alignment_scores: AlignmentScores | None = None
    judge_scores: JudgeScores | None = None
    error: str | None = None

    def as_dict(self) -> dict:
        d: dict = {
            "scenario_id": self.scenario_id,
            "scenario_title": self.scenario_title,
            "messages": self.messages,
            "behavioral_scores": self.behavioral_scores.as_dict() if self.behavioral_scores else None,
            "heuristic_scores": self.heuristic_scores.as_dict() if self.heuristic_scores else None,
            "alignment_scores": self.alignment_scores.as_dict() if self.alignment_scores else None,
            "alignment_mean": self.alignment_scores.mean_score if self.alignment_scores else None,
            "judge_scores": self.judge_scores.as_dict() if self.judge_scores else None,
            "judge_mean": self.judge_scores.mean_score if self.judge_scores else None,
            "heuristic_overall": self.heuristic_scores.overall if self.heuristic_scores else None,
        }
        if self.error:
            d["error"] = self.error
        return d


@dataclass
class EvalRunResult:
    model_name: str
    model_id: str
    timestamp: str
    lesson_slug: str
    prompt_version: str = "v1"
    scenarios: list[ScenarioResult] = field(default_factory=list)

    def as_dict(self) -> dict:
        scenario_dicts = [s.as_dict() for s in self.scenarios]
        judge_means = [s.judge_scores.mean_score for s in self.scenarios if s.judge_scores]
        heuristic_means = [s.heuristic_scores.overall for s in self.scenarios if s.heuristic_scores]
        alignment_means = [s.alignment_scores.mean_score for s in self.scenarios if s.alignment_scores and s.alignment_scores.mean_score > 0]
        return {
            "model_name": self.model_name,
            "model_id": self.model_id,
            "prompt_version": self.prompt_version,
            "timestamp": self.timestamp,
            "lesson_slug": self.lesson_slug,
            "aggregate": {
                "judge_mean": sum(judge_means) / len(judge_means) if judge_means else None,
                "alignment_mean": sum(alignment_means) / len(alignment_means) if alignment_means else None,
                "heuristic_mean": sum(heuristic_means) / len(heuristic_means) if heuristic_means else None,
                "scenarios_run": len(self.scenarios),
                "scenarios_errored": sum(1 for s in self.scenarios if s.error),
            },
            "scenarios": scenario_dicts,
        }


async def run_scenario(
    scenario: Scenario,
    config: EvalConfig,
    lesson_content: str,
    lesson_title: str,
    context: TutorContext,
) -> ScenarioResult:
    """Run a single evaluation scenario: multi-turn conversation + scoring."""
    result = ScenarioResult(
        scenario_id=scenario.id,
        scenario_title=scenario.title,
    )
    simulator = StudentSimulator(scenario, config)
    conversation: list[dict] = []

    try:
        for turn_num in range(config.max_turns):
            # Student turn
            student_msg = await simulator.generate_response(conversation)
            conversation.append({"role": "user", "content": student_msg})
            logger.info(
                "  [Turn %d] Student: %s",
                turn_num + 1,
                student_msg[:80] + ("..." if len(student_msg) > 80 else ""),
            )

            # Tutor turn
            turn_result = await run_tutor_turn(
                conversation, context, config.tutor_model,
            )
            # Include tool call/result messages so the judge can
            # cross-check citations against actual search evidence
            conversation.extend(turn_result.tool_messages)
            conversation.append({
                "role": "assistant",
                "content": turn_result.text,
                "search_tool_used": turn_result.search_used,
            })
            logger.info(
                "  [Turn %d] Tutor: %s",
                turn_num + 1,
                turn_result.text[:80] + ("..." if len(turn_result.text) > 80 else ""),
            )

            # Stop after scripted turns + a few LLM turns
            if not simulator.has_scripted_turn and turn_num >= len(scenario.scripted_turns) + 2:
                break

        result.messages = conversation
        scenario_mode = getattr(scenario, "mode", "default") or "default"

        # Layer 0: Behavioral metrics (deterministic, instant)
        result.behavioral_scores = score_behavioral(conversation)
        logger.info(
            "  Behavioral: q_ratio=%.2f, modalities=%d, images=%d",
            result.behavioral_scores.question_ratio,
            result.behavioral_scores.modality_count,
            result.behavioral_scores.image_total_count,
        )

        # Layer 1: Format safety heuristics
        result.heuristic_scores = score_conversation(
            conversation, lesson_content=lesson_content,
        )
        logger.info(
            "  Heuristics: %.2f", result.heuristic_scores.overall,
        )

        # Layer 2: Prompt-alignment judge (instruction compliance)
        result.alignment_scores = await judge_prompt_alignment(
            conversation, lesson_title, config,
            teaching_mode=scenario_mode,
            available_images=getattr(context, "available_images", None),
        )
        logger.info(
            "  Alignment mean: %.2f", result.alignment_scores.mean_score,
        )

        # Layer 3: Outcome judge (learning quality)
        result.judge_scores = await judge_conversation(
            conversation, lesson_content, lesson_title, config,
            student_persona=scenario.persona,
            teaching_mode=scenario_mode,
            reference_kb=context.reference_kb,
        )
        logger.info(
            "  Judge mean: %.2f", result.judge_scores.mean_score,
        )

    except Exception as e:
        logger.error("Scenario %s failed: %s", scenario.id, e, exc_info=True)
        result.error = str(e)

    return result


async def run_eval(
    config: EvalConfig,
    scenario_filter: str | None = None,
    prompt_version: str = "v2",
) -> EvalRunResult:
    """Run the full evaluation suite for a lesson."""
    global build_system_prompt
    if prompt_version in PROMPT_BUILDERS:
        build_system_prompt = PROMPT_BUILDERS[prompt_version]
    else:
        raise ValueError(
            f"Unknown prompt version: {prompt_version}. "
            f"Available: {', '.join(PROMPT_BUILDERS.keys())}"
        )

    lesson_id, lesson_title, summary, concepts, lesson_content, reference_kb, available_images = (
        _get_lesson_content(config.lesson_slug)
    )

    context = TutorContext(
        lesson_id=lesson_id,
        lesson_title=lesson_title,
        lesson_summary=summary,
        concepts=concepts,
        completed_lesson_titles=[
            "Introduction to Neural Networks",
            "Backpropagation & Gradient Descent",
            "Optimization Algorithms",
            "Regularization & Normalization",
            "Attention Mechanism",
            "Transformer Architecture Deep Dive",
            "Transfer Learning & Fine-tuning",
        ],
        mode="default",
        lesson_content=lesson_content,
        reference_kb=reference_kb,
        available_images=available_images,
        curriculum_index=EVAL_CURRICULUM_INDEX,
        exploration_mode=(prompt_version == "v2-explore"),
    )

    scenarios = Scenario.load_all(config.lesson_slug)
    if scenario_filter:
        scenarios = [s for s in scenarios if s.id == scenario_filter]
        if not scenarios:
            raise ValueError(f"No scenario found with id '{scenario_filter}'")

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_result = EvalRunResult(
        model_name=config.tutor_model.name,
        model_id=config.tutor_model.model_id,
        timestamp=timestamp,
        lesson_slug=config.lesson_slug,
        prompt_version=prompt_version,
    )

    logger.info(
        "Running %d scenarios for lesson '%s' with tutor model '%s' (prompt %s)",
        len(scenarios), config.lesson_slug, config.tutor_model.name, prompt_version,
    )

    for scenario in scenarios:
        logger.info("Scenario: %s (%s)", scenario.title, scenario.id)
        # Use the scenario's mode so the system prompt matches
        context.mode = getattr(scenario, "mode", "default") or "default"
        result = await run_scenario(
            scenario, config, lesson_content, lesson_title, context,
        )
        run_result.scenarios.append(result)

    return run_result


def save_results(result: EvalRunResult) -> Path:
    """Save eval results to a JSON file."""
    filename = f"{result.model_name}_{result.lesson_slug}_{result.prompt_version}_{result.timestamp}.json"
    path = RESULTS_DIR / filename
    with open(path, "w") as f:
        json.dump(result.as_dict(), f, indent=2, default=str)
    logger.info("Results saved to %s", path)
    return path
