#!/usr/bin/env python3
"""Head-to-head comparison of prompt versions (v1 prescriptive vs v2 lean).

Runs the same scenarios with both prompt versions, then presents both
conversations (anonymized) to the judge for a direct preference comparison.

Usage:
    # Compare v1 vs v2 on all scenarios
    python -m evals.run_comparison --lesson lora

    # Single scenario, fast iteration
    python -m evals.run_comparison --lesson lora --scenario curious_beginner

    # With verbose logging
    python -m evals.run_comparison --lesson lora -v
"""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import random
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from evals.config import EvalConfig, RESULTS_DIR, get_openai_client
from evals.runner import run_eval, save_results, EvalRunResult

logger = logging.getLogger(__name__)


H2H_JUDGE_SYSTEM_PROMPT = """You are an expert evaluator comparing two AI tutoring conversations side by side.

Both conversations are between a TUTOR and the same type of STUDENT on the same topic. The tutors may use different teaching strategies.

Your job is to decide which conversation would produce BETTER LEARNING OUTCOMES. Do not focus on style preferences — focus on:

1. LEARNING ARC: In which conversation does the student's understanding grow more?
2. NATURALNESS: Which conversation feels more like talking to a brilliant mentor vs. a chatbot?
3. ENGAGEMENT: In which conversation would a real student be more motivated to continue learning?
4. ACCURACY: Is one tutor more technically accurate than the other?
5. ADAPTIVENESS: Which tutor better reads and responds to the student's signals?

IMPORTANT:
- The conversations are labeled "Conversation A" and "Conversation B" — do NOT assume any ordering preference.
- If both are equally good, say so. Do not force a winner.
- Be specific about WHY one is better, with examples from the conversations.

Respond in EXACTLY this JSON format (no markdown, no extra text):
{
  "winner": "A" | "B" | "tie",
  "confidence": "high" | "medium" | "low",
  "reasoning": "<2-4 sentences explaining why, with specific examples>",
  "dimension_notes": {
    "learning_arc": "<which is better and why>",
    "naturalness": "<which is better and why>",
    "engagement": "<which is better and why>",
    "accuracy": "<which is better and why>",
    "adaptiveness": "<which is better and why>"
  }
}"""


def _format_h2h_user_prompt(
    conv_a: list[dict],
    conv_b: list[dict],
    lesson_title: str,
    student_persona: str,
) -> str:
    """Build the user prompt for head-to-head judging."""

    def _fmt(messages: list[dict]) -> str:
        lines = []
        for msg in messages:
            role = msg.get("role", "unknown")
            content = msg.get("content", "")
            if role == "user":
                lines.append(f"STUDENT: {content}")
            elif role == "assistant":
                lines.append(f"TUTOR: {content}")
        return "\n\n---\n\n".join(lines)

    return f"""## Topic: {lesson_title}

## Student Profile
{student_persona}

---

## Conversation A

{_fmt(conv_a)}

---

## Conversation B

{_fmt(conv_b)}

---

Compare these two tutoring conversations. Which one would produce better learning outcomes for this student? Respond with ONLY valid JSON."""


@dataclass
class H2HResult:
    scenario_id: str
    scenario_title: str
    winner: str  # "A", "B", or "tie"
    confidence: str
    reasoning: str
    dimension_notes: dict[str, str] = field(default_factory=dict)
    label_a: str = ""  # "v1" or "v2" (revealed after judging)
    label_b: str = ""
    error: str | None = None

    def as_dict(self) -> dict:
        d = {
            "scenario_id": self.scenario_id,
            "scenario_title": self.scenario_title,
            "winner": self.winner,
            "winner_version": self._winner_version(),
            "confidence": self.confidence,
            "reasoning": self.reasoning,
            "dimension_notes": self.dimension_notes,
            "label_a": self.label_a,
            "label_b": self.label_b,
        }
        if self.error:
            d["error"] = self.error
        return d

    def _winner_version(self) -> str:
        if self.winner == "A":
            return self.label_a
        elif self.winner == "B":
            return self.label_b
        return "tie"


@dataclass
class ComparisonResult:
    timestamp: str
    lesson_slug: str
    model_name: str
    model_id: str
    comparisons: list[H2HResult] = field(default_factory=list)
    v1_result: EvalRunResult | None = None
    v2_result: EvalRunResult | None = None

    def as_dict(self) -> dict:
        v1_wins = sum(1 for c in self.comparisons if c._winner_version() == "v1")
        v2_wins = sum(1 for c in self.comparisons if c._winner_version() == "v2")
        ties = sum(1 for c in self.comparisons if c._winner_version() == "tie")
        errors = sum(1 for c in self.comparisons if c.error)

        v1_data = self.v1_result.as_dict() if self.v1_result else None
        v2_data = self.v2_result.as_dict() if self.v2_result else None

        return {
            "timestamp": self.timestamp,
            "lesson_slug": self.lesson_slug,
            "model_name": self.model_name,
            "model_id": self.model_id,
            "summary": {
                "v1_wins": v1_wins,
                "v2_wins": v2_wins,
                "ties": ties,
                "errors": errors,
                "total": len(self.comparisons),
            },
            "v1_judge_mean": v1_data["aggregate"]["judge_mean"] if v1_data else None,
            "v2_judge_mean": v2_data["aggregate"]["judge_mean"] if v2_data else None,
            "v1_heuristic_mean": v1_data["aggregate"]["heuristic_mean"] if v1_data else None,
            "v2_heuristic_mean": v2_data["aggregate"]["heuristic_mean"] if v2_data else None,
            "comparisons": [c.as_dict() for c in self.comparisons],
        }


async def run_h2h_judge(
    conv_a: list[dict],
    conv_b: list[dict],
    lesson_title: str,
    student_persona: str,
    config: EvalConfig,
) -> dict:
    """Present both conversations to the judge and get a preference."""
    client = get_openai_client()
    user_prompt = _format_h2h_user_prompt(conv_a, conv_b, lesson_title, student_persona)

    try:
        response = await client.chat.completions.create(
            model=config.judge_model.model_id,
            messages=[
                {"role": "system", "content": H2H_JUDGE_SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=config.judge_model.max_tokens,
            temperature=0.3,
        )

        raw = response.choices[0].message.content or ""
        cleaned = raw.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.split("\n", 1)[1] if "\n" in cleaned else cleaned[3:]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
            cleaned = cleaned.strip()

        return json.loads(cleaned)

    except json.JSONDecodeError as e:
        logger.error("H2H judge returned invalid JSON: %s\nRaw: %s", e, raw)
        return {"winner": "tie", "confidence": "low", "reasoning": f"Parse error: {e}", "dimension_notes": {}}
    except Exception as e:
        logger.error("H2H judge API call failed: %s", e)
        return {"winner": "tie", "confidence": "low", "reasoning": f"API error: {e}", "dimension_notes": {}}


async def run_comparison(
    config: EvalConfig,
    scenario_filter: str | None = None,
) -> ComparisonResult:
    """Run v1 and v2 prompts on all scenarios, then do head-to-head judging."""

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    comparison = ComparisonResult(
        timestamp=timestamp,
        lesson_slug=config.lesson_slug,
        model_name=config.tutor_model.name,
        model_id=config.tutor_model.model_id,
    )

    # Run both prompt versions
    print("\n[Phase 1/3] Running v1 (prescriptive prompt)...")
    v1_result = await run_eval(config, scenario_filter=scenario_filter, prompt_version="v1")
    comparison.v1_result = v1_result
    save_results(v1_result)

    print("\n[Phase 2/3] Running v2 (lean prompt)...")
    v2_result = await run_eval(config, scenario_filter=scenario_filter, prompt_version="v2")
    comparison.v2_result = v2_result
    save_results(v2_result)

    # Head-to-head judging
    print("\n[Phase 3/3] Head-to-head judging...")

    from evals.runner import _get_lesson_content
    _, lesson_title, _, _, _ = _get_lesson_content(config.lesson_slug)

    for v1_scenario, v2_scenario in zip(v1_result.scenarios, v2_result.scenarios):
        if v1_scenario.error or v2_scenario.error:
            comparison.comparisons.append(H2HResult(
                scenario_id=v1_scenario.scenario_id,
                scenario_title=v1_scenario.scenario_title,
                winner="tie",
                confidence="low",
                reasoning="One or both scenarios had errors.",
                error=v1_scenario.error or v2_scenario.error,
            ))
            continue

        # Randomize A/B assignment to avoid position bias
        if random.random() < 0.5:
            conv_a, conv_b = v1_scenario.messages, v2_scenario.messages
            label_a, label_b = "v1", "v2"
        else:
            conv_a, conv_b = v2_scenario.messages, v1_scenario.messages
            label_a, label_b = "v2", "v1"

        # Get persona from v1 scenario (same scenario, same persona)
        from evals.student_simulator import Scenario
        scenarios = Scenario.load_all(config.lesson_slug)
        persona = ""
        for s in scenarios:
            if s.id == v1_scenario.scenario_id:
                persona = s.persona
                break

        logger.info("  H2H judging: %s (A=%s, B=%s)", v1_scenario.scenario_title, label_a, label_b)
        judge_result = await run_h2h_judge(conv_a, conv_b, lesson_title, persona, config)

        h2h = H2HResult(
            scenario_id=v1_scenario.scenario_id,
            scenario_title=v1_scenario.scenario_title,
            winner=judge_result.get("winner", "tie"),
            confidence=judge_result.get("confidence", "low"),
            reasoning=judge_result.get("reasoning", ""),
            dimension_notes=judge_result.get("dimension_notes", {}),
            label_a=label_a,
            label_b=label_b,
        )
        comparison.comparisons.append(h2h)

        winner_ver = h2h._winner_version()
        logger.info("    Winner: %s (%s confidence)", winner_ver, h2h.confidence)

    return comparison


def print_comparison_summary(result: ComparisonResult) -> None:
    """Print a formatted summary of the head-to-head comparison."""
    data = result.as_dict()
    summary = data["summary"]

    print("\n" + "=" * 75)
    print("  HEAD-TO-HEAD COMPARISON: v1 (prescriptive) vs v2 (lean)")
    print(f"  Model: {data['model_name']} | Lesson: {data['lesson_slug']}")
    print("=" * 75)

    print(f"\n  Overall: v1 wins {summary['v1_wins']} | v2 wins {summary['v2_wins']} | ties {summary['ties']}")

    if data["v1_judge_mean"] is not None and data["v2_judge_mean"] is not None:
        print(f"\n  Quality Judge Scores (independent, per-version):")
        print(f"    v1 mean: {data['v1_judge_mean']:.2f} / 5.00")
        print(f"    v2 mean: {data['v2_judge_mean']:.2f} / 5.00")
        delta = data['v2_judge_mean'] - data['v1_judge_mean']
        print(f"    delta:   {delta:+.2f}")

    if data["v1_heuristic_mean"] is not None and data["v2_heuristic_mean"] is not None:
        print(f"\n  Safety Heuristic Scores:")
        print(f"    v1 mean: {data['v1_heuristic_mean']:.2f} / 1.00")
        print(f"    v2 mean: {data['v2_heuristic_mean']:.2f} / 1.00")

    print(f"\n  {'Scenario':<28} {'Winner':>8} {'Conf':>8}  Reasoning")
    print(f"  {'-'*28} {'-'*8} {'-'*8}  {'-'*40}")

    for c in data["comparisons"]:
        winner = c.get("winner_version", "?")
        conf = c.get("confidence", "?")
        reasoning = c.get("reasoning", "")[:60]
        err = " [ERROR]" if c.get("error") else ""
        print(f"  {c['scenario_title']:<28} {winner:>8} {conf:>8}  {reasoning}{err}")

    # Dimension-level breakdown
    print(f"\n  Dimension-Level Notes (first 3 scenarios):")
    for c in data["comparisons"][:3]:
        print(f"\n  --- {c['scenario_title']} (winner: {c.get('winner_version', '?')}) ---")
        for dim, note in c.get("dimension_notes", {}).items():
            print(f"    {dim}: {note[:80]}")

    print()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Head-to-head comparison of prompt v1 (prescriptive) vs v2 (lean)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--lesson", default="lora",
                        help="Lesson slug to evaluate (default: lora)")
    parser.add_argument("--scenario", default=None,
                        help="Run only one scenario for fast iteration")
    parser.add_argument("--max-turns", type=int, default=10,
                        help="Max conversation turns per scenario (default: 10)")
    parser.add_argument("-v", "--verbose", action="store_true")
    return parser.parse_args()


async def main() -> None:
    args = parse_args()

    level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )

    config = EvalConfig(
        max_turns=args.max_turns,
        lesson_slug=args.lesson,
    )

    result = run_comparison(config, scenario_filter=args.scenario)
    if asyncio.iscoroutine(result):
        result = await result

    print_comparison_summary(result)

    # Save full report
    report_path = RESULTS_DIR / f"comparison_{args.lesson}_{result.timestamp}.json"
    with open(report_path, "w") as f:
        json.dump(result.as_dict(), f, indent=2, default=str)
    print(f"Full report saved to: {report_path}")


if __name__ == "__main__":
    asyncio.run(main())
