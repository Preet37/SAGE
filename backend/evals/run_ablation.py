#!/usr/bin/env python3
"""Systematic ablation testing for system prompt sections.

Removes one instruction section at a time and runs the eval suite to
measure impact.  Zero changes to existing files — uses monkey-patching.

Usage:
    # Full ablation (all sections, all scenarios)
    python -m evals.run_ablation --lesson lora

    # Fast mode: one scenario only (~40 min)
    python -m evals.run_ablation --lesson lora --scenario curious_beginner

    # Test specific sections only
    python -m evals.run_ablation --lesson lora --sections socratic_rules analogy_guidelines

    # List available section IDs
    python -m evals.run_ablation --list-sections
"""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import evals.runner as runner_module
from evals.config import EvalConfig, TUTOR_BASELINE
from evals.runner import run_eval, save_results

logger = logging.getLogger(__name__)

# ── Section definitions ───────────────────────────────────────────────────────
# Maps a human-readable ID to the exact header text in the generated prompt.

ABLATION_SECTIONS = {
    "teaching_principles":  "TEACHING PRINCIPLES:",
    "reference_material":   "REFERENCE MATERIAL:",
    "detailed_reference":   "DETAILED REFERENCE KNOWLEDGE",
    "curriculum_index":     "CURRICULUM INDEX",
    "available_images":     "AVAILABLE IMAGES FOR THIS LESSON",
    "tools_available":      "TOOLS AVAILABLE:",
    "quiz_format":          "KNOWLEDGE CHECK",
    "resource_format":      "RESOURCE RECOMMENDATION",
    "image_rules":          "IMAGE (when showing a curated diagram",
    "diagrams":             "DIAGRAMS:",
    "flow_diagrams":        "INTERACTIVE FLOW DIAGRAMS",
    "architecture_diagrams": "INTERACTIVE ARCHITECTURE DIAGRAMS",
    "factual_accuracy":     "FACTUAL ACCURACY",
}

_ALL_HEADERS = list(ABLATION_SECTIONS.values()) + ["You are a guide, not a lecturer."]

_original_build = runner_module.build_system_prompt

# ── Section stripping ─────────────────────────────────────────────────────────


def _strip_section(prompt: str, target_header: str) -> str:
    """Remove a section from the prompt text.

    Finds *target_header*, then removes everything from there up to
    (but not including) the next known section header or the footer.
    """
    header_pos = prompt.find(target_header)
    if header_pos == -1:
        return prompt

    start = header_pos
    while start > 0 and prompt[start - 1] == "\n":
        start -= 1

    search_from = header_pos + len(target_header)
    end = len(prompt)
    for header in _ALL_HEADERS:
        if header == target_header:
            continue
        pos = prompt.find(header, search_from)
        if pos != -1 and pos < end:
            end = pos

    result = prompt[:start] + prompt[end:]
    while "\n\n\n" in result:
        result = result.replace("\n\n\n", "\n\n")
    return result.strip()


def _make_patched(section_header: str):
    """Return a replacement ``build_system_prompt`` that strips one section."""
    def patched(context):
        prompt = _original_build(context)
        return _strip_section(prompt, section_header)
    return patched


# ── Score extraction & classification ─────────────────────────────────────────

LOAD_BEARING_JUDGE_THRESHOLD = -0.3
LOAD_BEARING_HEURISTIC_THRESHOLD = -0.05
COUNTERPRODUCTIVE_JUDGE_THRESHOLD = 0.15


def _extract_scores(result_data: dict) -> dict:
    agg = result_data["aggregate"]
    dimensions: dict[str, float] = {}
    all_judge = [
        s["judge_scores"]
        for s in result_data["scenarios"]
        if s.get("judge_scores")
    ]
    if all_judge:
        for dim in all_judge[0]:
            scores = [j[dim]["score"] for j in all_judge if dim in j]
            dimensions[dim] = round(sum(scores) / len(scores), 4) if scores else 0

    return {
        "judge_mean": agg.get("judge_mean"),
        "heuristic_mean": agg.get("heuristic_mean"),
        "dimensions": dimensions,
    }


def _classify(delta_judge: float, delta_heuristic: float) -> str:
    if delta_judge <= LOAD_BEARING_JUDGE_THRESHOLD:
        return "load_bearing"
    if delta_heuristic <= LOAD_BEARING_HEURISTIC_THRESHOLD:
        return "load_bearing"
    if delta_judge >= COUNTERPRODUCTIVE_JUDGE_THRESHOLD:
        return "counterproductive"
    return "ignored"


# ── Reporting ─────────────────────────────────────────────────────────────────


def print_ablation_summary(report: dict) -> None:
    baseline = report["baseline"]
    bj = baseline["judge_mean"]
    bh = baseline["heuristic_mean"]

    print("\n" + "=" * 85)
    print("  PROMPT ABLATION RESULTS")
    print(f"  Baseline: judge={bj:.2f}  heuristic={bh:.2f}")
    print(f"  Model: {report['model']} | Lesson: {report['lesson_slug']}"
          + (f" | Scenario: {report['scenario_filter']}" if report.get("scenario_filter") else ""))
    print("=" * 85)

    header = f"  {'Section Removed':<28} {'Judge':>7} {'Delta':>7} {'Heuristic':>10} {'Delta':>7}  {'Class'}"
    print(f"\n{header}")
    print(f"  {'-'*28} {'-'*7} {'-'*7} {'-'*10} {'-'*7}  {'-'*16}")

    ablations = sorted(
        report["ablations"],
        key=lambda a: a.get("delta_judge") or 0,
    )

    for a in ablations:
        if a.get("error"):
            print(f"  {a['removed_section']:<28} {'ERROR':>7} {'':>7} {'':>10} {'':>7}  {a['error'][:16]}")
            continue
        j = f"{a['judge_mean']:.2f}" if a.get("judge_mean") is not None else "N/A"
        dj = f"{a['delta_judge']:+.2f}" if a.get("delta_judge") is not None else "N/A"
        h = f"{a['heuristic_mean']:.2f}" if a.get("heuristic_mean") is not None else "N/A"
        dh = f"{a['delta_heuristic']:+.2f}" if a.get("delta_heuristic") is not None else "N/A"
        cls = a["classification"].upper().replace("_", "-")
        print(f"  {a['removed_section']:<28} {j:>7} {dj:>7} {h:>10} {dh:>7}  {cls}")

    summary = report["summary"]
    print()
    if summary["load_bearing"]:
        print(f"  Load-bearing: {', '.join(summary['load_bearing'])}")
    if summary["counterproductive"]:
        print(f"  Counterproductive: {', '.join(summary['counterproductive'])}")
    if summary["ignored"]:
        print(f"  Ignored: {', '.join(summary['ignored'])}")
    print()


# ── CLI ───────────────────────────────────────────────────────────────────────


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Systematic ablation testing for system prompt sections",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--lesson", default="lora",
                        help="Lesson slug to evaluate (default: lora)")
    parser.add_argument("--scenario", default=None,
                        help="Run only one scenario for fast iteration")
    parser.add_argument("--sections", nargs="+", metavar="ID",
                        help="Only ablate these sections (default: all)")
    parser.add_argument("--list-sections", action="store_true",
                        help="List available section IDs and exit")
    parser.add_argument("-v", "--verbose", action="store_true")
    return parser.parse_args()


# ── Main ──────────────────────────────────────────────────────────────────────


async def main() -> None:
    args = parse_args()

    if args.list_sections:
        print("Available sections for ablation:")
        for sid, header in ABLATION_SECTIONS.items():
            print(f"  {sid:<28} → {header}")
        return

    level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )

    config = EvalConfig(tutor_model=TUTOR_BASELINE, lesson_slug=args.lesson)

    if args.sections:
        sections = {k: v for k, v in ABLATION_SECTIONS.items() if k in args.sections}
        unknown = set(args.sections) - set(ABLATION_SECTIONS)
        if unknown:
            print(f"Unknown section IDs: {unknown}")
            print(f"Run with --list-sections to see available IDs.")
            sys.exit(1)
    else:
        sections = ABLATION_SECTIONS

    total_runs = len(sections) + 1
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    # ── 1. Baseline ──────────────────────────────────────────────────────
    print(f"\n[1/{total_runs}] Running baseline (full prompt)...")
    baseline_result = await run_eval(config, scenario_filter=args.scenario)
    baseline_data = baseline_result.as_dict()
    baseline_scores = _extract_scores(baseline_data)
    save_results(baseline_result)
    logger.info(
        "Baseline complete: judge=%.2f, heuristic=%.2f",
        baseline_scores["judge_mean"] or 0,
        baseline_scores["heuristic_mean"] or 0,
    )

    # ── 2. Ablations (sequential to avoid monkey-patch races) ────────────
    ablation_results: list[dict] = []

    for i, (section_id, header) in enumerate(sections.items(), start=2):
        print(f"\n[{i}/{total_runs}] Ablating: {section_id}")

        runner_module.build_system_prompt = _make_patched(header)
        try:
            result = await run_eval(config, scenario_filter=args.scenario)
            result_data = result.as_dict()
            scores = _extract_scores(result_data)

            dj = (
                round(scores["judge_mean"] - baseline_scores["judge_mean"], 4)
                if scores["judge_mean"] is not None and baseline_scores["judge_mean"] is not None
                else None
            )
            dh = (
                round(scores["heuristic_mean"] - baseline_scores["heuristic_mean"], 4)
                if scores["heuristic_mean"] is not None and baseline_scores["heuristic_mean"] is not None
                else None
            )

            entry = {
                "removed_section": section_id,
                "removed_header": header,
                "judge_mean": scores["judge_mean"],
                "heuristic_mean": scores["heuristic_mean"],
                "delta_judge": dj,
                "delta_heuristic": dh,
                "dimensions": scores["dimensions"],
                "classification": _classify(dj or 0, dh or 0),
            }
            ablation_results.append(entry)

            logger.info(
                "  %s: judge=%.2f (Δ%+.2f), heuristic=%.2f (Δ%+.2f) → %s",
                section_id,
                scores["judge_mean"] or 0, dj or 0,
                scores["heuristic_mean"] or 0, dh or 0,
                entry["classification"],
            )

        except Exception as e:
            logger.error("  %s FAILED: %s", section_id, e, exc_info=True)
            ablation_results.append({
                "removed_section": section_id,
                "removed_header": header,
                "error": str(e),
                "classification": "error",
            })
        finally:
            runner_module.build_system_prompt = _original_build

    # ── 3. Build report ──────────────────────────────────────────────────
    report = {
        "timestamp": timestamp,
        "lesson_slug": args.lesson,
        "model": config.tutor_model.name,
        "model_id": config.tutor_model.model_id,
        "scenario_filter": args.scenario,
        "total_sections_tested": len(sections),
        "baseline": baseline_scores,
        "ablations": ablation_results,
        "summary": {
            "load_bearing": [
                a["removed_section"] for a in ablation_results
                if a.get("classification") == "load_bearing"
            ],
            "counterproductive": [
                a["removed_section"] for a in ablation_results
                if a.get("classification") == "counterproductive"
            ],
            "ignored": [
                a["removed_section"] for a in ablation_results
                if a.get("classification") == "ignored"
            ],
        },
    }

    # ── 4. Save & print ──────────────────────────────────────────────────
    results_dir = Path(__file__).parent / "results"
    results_dir.mkdir(exist_ok=True)
    report_path = results_dir / f"ablation_{args.lesson}_{timestamp}.json"
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2, default=str)

    print_ablation_summary(report)
    print(f"Full report saved to: {report_path}")


if __name__ == "__main__":
    asyncio.run(main())
