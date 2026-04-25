#!/usr/bin/env python3
"""CLI entry point for running tutor evaluations.

Usage:
    # Run all scenarios against default tutor model (uses prompt v2)
    python -m evals.run_eval --lesson lora

    # Run with legacy prescriptive prompt v1
    python -m evals.run_eval --lesson lora --prompt-version v1

    # Run with exploration-mode prompt
    python -m evals.run_eval --lesson lora --prompt-version v2-explore

    # Run against a specific model
    python -m evals.run_eval --lesson lora --tutor-model openai/openai/gpt-5.2

    # Run a single scenario (e.g. format probe for quiz cards)
    python -m evals.run_eval --lesson lora --scenario format_probe_quiz

    # Compare two models side-by-side
    python -m evals.run_eval --lesson lora --compare aws/anthropic/bedrock-claude-sonnet-4-6 openai/openai/gpt-5.2

    # Limit conversation turns
    python -m evals.run_eval --lesson lora --max-turns 6

    # Run multiple times for stability testing (reports mean/stddev)
    python -m evals.run_eval --lesson lora --runs 5
"""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import sys
from pathlib import Path
from statistics import mean, stdev

# Ensure backend root is on path for app module imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from evals.config import EvalConfig, ModelConfig, TUTOR_BASELINE
from evals.runner import run_eval, save_results


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run SocraticTutor evaluation suite",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--lesson", default="lora",
        help="Lesson slug to evaluate (default: lora)",
    )
    parser.add_argument(
        "--scenario", default=None,
        help="Run a specific scenario by ID (e.g., curious_beginner)",
    )
    parser.add_argument(
        "--tutor-model", default=None,
        help="Model ID for the tutor (e.g., openai/openai/gpt-5.2). Defaults to Claude Sonnet 4.6.",
    )
    parser.add_argument(
        "--tutor-name", default=None,
        help="Human-friendly name for the tutor model (used in output filenames)",
    )
    parser.add_argument(
        "--max-turns", type=int, default=10,
        help="Maximum conversation turns per scenario (default: 10)",
    )
    parser.add_argument(
        "--compare", nargs="+", metavar="MODEL_ID",
        help="Compare multiple tutor models. Provide 2+ model IDs.",
    )
    parser.add_argument(
        "--prompt-version", default="v2",
        choices=["v1", "v2", "v2-explore"],
        help="System prompt version: v1 (prescriptive), v2 (lean), "
             "v2-explore (exploration mode). Default: v2",
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true",
        help="Enable verbose logging",
    )
    parser.add_argument(
        "--runs", type=int, default=1,
        help="Number of runs for stability testing (default: 1). Reports mean/stddev when >1.",
    )
    return parser.parse_args()


def _model_name_from_id(model_id: str) -> str:
    """Derive a short name from a model ID like 'openai/openai/gpt-5.2'."""
    return model_id.rsplit("/", 1)[-1]


def print_summary(result_data: dict) -> None:
    """Print a formatted summary of eval results to stdout."""
    agg = result_data["aggregate"]
    print("\n" + "=" * 70)
    print(f"  MODEL: {result_data['model_name']} ({result_data['model_id']})")
    print(f"  PROMPT: {result_data.get('prompt_version', 'v1')}")
    print(f"  LESSON: {result_data['lesson_slug']}")
    print(f"  TIMESTAMP: {result_data['timestamp']}")
    print("=" * 70)

    # Top-level aggregates
    print(f"\n  {'Metric':<30} {'Score':>10}")
    print(f"  {'-'*30} {'-'*10}")
    if agg.get("judge_mean") is not None:
        print(f"  {'Outcome Judge (L3)':>30} {agg['judge_mean']:>7.2f} / 5")
    if agg.get("alignment_mean") is not None:
        print(f"  {'Prompt Alignment (L2)':>30} {agg['alignment_mean']:>7.2f} / 5")
    if agg.get("heuristic_mean") is not None:
        print(f"  {'Format Safety (L1)':>30} {agg['heuristic_mean']:>7.2f} / 1")
    print(f"  {'Scenarios Run':<30} {agg['scenarios_run']:>10}")
    print(f"  {'Scenarios Errored':<30} {agg['scenarios_errored']:>10}")

    # Per-scenario breakdown
    print(f"\n  Per-Scenario Breakdown:")
    print(f"  {'Scenario':<25} {'Judge':>7} {'Align':>7} {'Safety':>7}")
    print(f"  {'-'*25} {'-'*7} {'-'*7} {'-'*7}")

    for s in result_data["scenarios"]:
        judge = f"{s['judge_mean']:.2f}" if s.get("judge_mean") is not None else "N/A"
        align = f"{s['alignment_mean']:.2f}" if s.get("alignment_mean") is not None else "N/A"
        heur = f"{s['heuristic_overall']:.2f}" if s.get("heuristic_overall") is not None else "N/A"
        err = " [ERR]" if s.get("error") else ""
        print(f"  {s['scenario_title']:<25} {judge:>7} {align:>7} {heur:>7}{err}")

    # Behavioral metrics aggregate
    all_behavioral = [s["behavioral_scores"] for s in result_data["scenarios"] if s.get("behavioral_scores")]
    if all_behavioral:
        print("\n  Behavioral Metrics (Layer 0, deterministic):")

        def _avg(key):
            vals = [b[key] for b in all_behavioral if b.get(key) is not None]
            return sum(vals) / len(vals) if vals else 0

        print(f"    {'Question Ratio':<30} {_avg('question_ratio'):.2f}")
        print(f"    {'Open Question Ratio':<30} {_avg('open_question_ratio'):.2f}")
        print(f"    {'Avg Modalities Used':<30} {_avg('modality_count'):.1f}")
        print(f"    {'Images (proactive)':<30} {_avg('image_proactive_count'):.1f}")
        print(f"    {'Images (reactive)':<30} {_avg('image_reactive_count'):.1f}")
        print(f"    {'Backward References':<30} {_avg('backward_reference_count'):.1f}")
        print(f"    {'Avg Response Length':<30} {_avg('avg_assistant_length'):.0f} words")
        print(f"    {'Tool Calls':<30} {_avg('tool_call_count'):.1f}")

        # Collect all modalities used
        all_modalities: set[str] = set()
        for b in all_behavioral:
            all_modalities.update(b.get("modalities_used", []))
        if all_modalities:
            print(f"    {'Modalities Seen':<30} {', '.join(sorted(all_modalities))}")

    # Format safety breakdown
    all_heur = [s["heuristic_scores"] for s in result_data["scenarios"] if s.get("heuristic_scores")]
    if all_heur:
        print("\n  Format Safety (Layer 1):")
        for key in ("notation_consistency", "no_duplicate_resources", "median_response_length"):
            vals = [h[key] for h in all_heur if key in h]
            if vals:
                avg = sum(vals) / len(vals)
                label = key.replace("_", " ").title()
                if key == "median_response_length":
                    print(f"    {label:<30} {avg:.0f} chars")
                else:
                    print(f"    {label:<30} {avg:.2f}")

    # Prompt alignment dimension breakdown
    all_align = [s["alignment_scores"] for s in result_data["scenarios"] if s.get("alignment_scores")]
    if all_align:
        print("\n  Prompt Alignment Dimensions (Layer 2):")
        dims = list(all_align[0].keys())
        for dim in dims:
            scores = [a[dim]["score"] for a in all_align if dim in a]
            avg = sum(scores) / len(scores) if scores else 0
            print(f"    {dim:<30} {avg:.2f}")

    # Outcome judge dimension breakdown
    all_judge = [s["judge_scores"] for s in result_data["scenarios"] if s.get("judge_scores")]
    if all_judge:
        print("\n  Outcome Judge Dimensions (Layer 3):")
        dims = list(all_judge[0].keys())
        for dim in dims:
            scores = [j[dim]["score"] for j in all_judge if dim in j]
            avg = sum(scores) / len(scores) if scores else 0
            print(f"    {dim:<30} {avg:.2f}")

    print()


def print_comparison(results: list[dict]) -> None:
    """Print a side-by-side comparison of multiple model runs."""
    print("\n" + "=" * 70)
    print("  MODEL COMPARISON")
    print("=" * 70)

    header = f"  {'Metric':<30}"
    for r in results:
        header += f" {r['model_name']:>15}"
    print(header)
    print(f"  {'-'*30}" + f" {'-'*15}" * len(results))

    # Overall scores
    row = f"  {'Judge Mean':<30}"
    for r in results:
        v = r["aggregate"].get("judge_mean")
        row += f" {v:>15.2f}" if v is not None else f" {'N/A':>15}"
    print(row)

    row = f"  {'Heuristic Mean':<30}"
    for r in results:
        v = r["aggregate"].get("heuristic_mean")
        row += f" {v:>15.2f}" if v is not None else f" {'N/A':>15}"
    print(row)

    # Per-dimension comparison
    all_dims = set()
    for r in results:
        for s in r["scenarios"]:
            if s.get("judge_scores"):
                all_dims.update(s["judge_scores"].keys())

    if all_dims:
        print(f"\n  {'Dimension':<30}" + f" {r['model_name']:>15}" * len(results))
        print(f"  {'-'*30}" + f" {'-'*15}" * len(results))

        for dim in sorted(all_dims):
            row = f"  {dim:<30}"
            for r in results:
                scores = []
                for s in r["scenarios"]:
                    if s.get("judge_scores") and dim in s["judge_scores"]:
                        scores.append(s["judge_scores"][dim]["score"])
                avg = sum(scores) / len(scores) if scores else 0
                row += f" {avg:>15.2f}"
            print(row)

    print()


def print_stability_report(all_results: list[dict]) -> None:
    """Print variance report for multiple runs of the same scenario."""
    print("\n" + "=" * 70)
    print("  STABILITY REPORT")
    print(f"  {len(all_results)} runs")
    print("=" * 70)

    # Extract judge scores across runs
    judge_scores = [r["aggregate"].get("judge_mean") for r in all_results if r["aggregate"].get("judge_mean") is not None]
    heuristic_scores = [r["aggregate"].get("heuristic_mean") for r in all_results if r["aggregate"].get("heuristic_mean") is not None]

    if judge_scores:
        j_mean = mean(judge_scores)
        j_std = stdev(judge_scores) if len(judge_scores) > 1 else 0.0
        print(f"\n  Judge Mean:     {j_mean:.3f} ± {j_std:.3f}")
        print(f"  Judge Range:    [{min(judge_scores):.2f}, {max(judge_scores):.2f}]")

    if heuristic_scores:
        h_mean = mean(heuristic_scores)
        h_std = stdev(heuristic_scores) if len(heuristic_scores) > 1 else 0.0
        print(f"\n  Heuristic Mean: {h_mean:.3f} ± {h_std:.3f}")
        print(f"  Heuristic Range:[{min(heuristic_scores):.2f}, {max(heuristic_scores):.2f}]")

    # Per-dimension variance
    all_dims = set()
    for r in all_results:
        for s in r["scenarios"]:
            if s.get("judge_scores"):
                all_dims.update(s["judge_scores"].keys())

    if all_dims:
        print(f"\n  {'Dimension':<30} {'Mean':>8} {'StdDev':>8} {'Range':>15}")
        print(f"  {'-'*30} {'-'*8} {'-'*8} {'-'*15}")

        for dim in sorted(all_dims):
            dim_scores = []
            for r in all_results:
                for s in r["scenarios"]:
                    if s.get("judge_scores") and dim in s["judge_scores"]:
                        dim_scores.append(s["judge_scores"][dim]["score"])
            
            if dim_scores:
                d_mean = mean(dim_scores)
                d_std = stdev(dim_scores) if len(dim_scores) > 1 else 0.0
                d_range = f"[{min(dim_scores):.1f}, {max(dim_scores):.1f}]"
                print(f"  {dim:<30} {d_mean:>8.2f} {d_std:>8.2f} {d_range:>15}")

    # Stability assessment
    print("\n  --- Stability Assessment ---")
    if judge_scores and len(judge_scores) > 1:
        cv = (stdev(judge_scores) / mean(judge_scores)) * 100 if mean(judge_scores) > 0 else 0
        if cv < 5:
            print(f"  Coefficient of Variation: {cv:.1f}% — STABLE")
        elif cv < 15:
            print(f"  Coefficient of Variation: {cv:.1f}% — MODERATE variance")
        else:
            print(f"  Coefficient of Variation: {cv:.1f}% — HIGH variance (investigate)")

    print()


async def main() -> None:
    args = parse_args()

    level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )

    pv = args.prompt_version

    if args.compare:
        # Compare mode: run eval for each model
        all_results = []
        for model_id in args.compare:
            model_name = _model_name_from_id(model_id)
            config = EvalConfig(
                tutor_model=ModelConfig(name=model_name, model_id=model_id),
                max_turns=args.max_turns,
                lesson_slug=args.lesson,
            )
            print(f"\nRunning eval for: {model_name} ({model_id}) [prompt {pv}]")
            result = await run_eval(config, scenario_filter=args.scenario, prompt_version=pv)
            path = save_results(result)
            result_data = result.as_dict()
            print_summary(result_data)
            all_results.append(result_data)

        if len(all_results) > 1:
            print_comparison(all_results)
    elif args.runs > 1:
        # Stability testing mode: run multiple times
        tutor = TUTOR_BASELINE
        if args.tutor_model:
            name = args.tutor_name or _model_name_from_id(args.tutor_model)
            tutor = ModelConfig(name=name, model_id=args.tutor_model)

        config = EvalConfig(
            tutor_model=tutor,
            max_turns=args.max_turns,
            lesson_slug=args.lesson,
        )

        all_results = []
        for i in range(args.runs):
            print(f"\n{'='*60}")
            print(f"  RUN {i+1}/{args.runs}")
            print(f"{'='*60}")
            
            result = await run_eval(config, scenario_filter=args.scenario, prompt_version=pv)
            path = save_results(result)
            result_data = result.as_dict()
            print_summary(result_data)
            all_results.append(result_data)

        print_stability_report(all_results)
        print(f"All results saved to: {path.parent}")
    else:
        # Single model mode
        tutor = TUTOR_BASELINE
        if args.tutor_model:
            name = args.tutor_name or _model_name_from_id(args.tutor_model)
            tutor = ModelConfig(name=name, model_id=args.tutor_model)

        config = EvalConfig(
            tutor_model=tutor,
            max_turns=args.max_turns,
            lesson_slug=args.lesson,
        )

        result = await run_eval(config, scenario_filter=args.scenario, prompt_version=pv)
        path = save_results(result)
        result_data = result.as_dict()
        print_summary(result_data)
        print(f"Full results saved to: {path}")


if __name__ == "__main__":
    asyncio.run(main())
