#!/usr/bin/env python3
"""
Evaluate image-based tutoring flows end-to-end.

Runs a battery of simulated student messages through the tutor agent loop
and checks whether the image tool is used correctly, <image> blocks are
well-formed, image paths resolve to real files, and the tutor integrates
images contextually rather than dumping them.

Three tiers (mirrors eval_quality.py structure):
  Tier 1 — Tool plumbing  (no LLM, always runs)
  Tier 2 — Agent flows     (live LLM, opt-in with --llm)
  Tier 3 — Quality rubric  (LLM-judged, opt-in with --rubric)

Usage:
    python -m scripts.eval_image_tutoring               # Tier 1 only
    python -m scripts.eval_image_tutoring --llm         # Tier 1 + 2
    python -m scripts.eval_image_tutoring --llm --rubric  # All tiers
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import re
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

BACKEND = Path(__file__).resolve().parent.parent
WIKI_DIR = Path(os.environ.get("CONTENT_DIR", str(BACKEND.parent / "content"))).resolve() / "pedagogy-wiki"
sys.path.insert(0, str(BACKEND))

from app.agent.context import TutorContext
from app.agent.tool_handlers import _get_relevant_images
from app.agent.tools import TUTOR_TOOLS

PASS = "\033[92m✓\033[0m"
FAIL = "\033[91m✗\033[0m"
WARN = "\033[93m⚠\033[0m"
INFO = "\033[94mℹ\033[0m"

IMAGE_TAG_RE = re.compile(r"<image>\s*(\{.*?\})\s*</image>", re.DOTALL)


# ── Data ──────────────────────────────────────────────────────────────────

@dataclass
class Check:
    name: str
    passed: bool
    detail: str = ""
    severity: str = "error"


@dataclass
class ScenarioResult:
    name: str
    student_message: str
    expect_images: bool
    checks: list[Check] = field(default_factory=list)
    tool_calls: list[str] = field(default_factory=list)
    image_blocks: list[dict] = field(default_factory=list)
    response_text: str = ""
    rubric_scores: dict[str, Any] = field(default_factory=dict)
    elapsed_s: float = 0.0


# Each scenario: (name, student_msg, concepts_for_context, expect_images)
SCENARIOS = [
    {
        "name": "explicit_diagram_request",
        "student": "Can you show me a diagram of how Bahdanau attention works?",
        "concepts": ["attention mechanism", "bahdanau attention", "alignment scores"],
        "lesson_title": "Attention Mechanism",
        "expect_images": True,
    },
    {
        "name": "visual_learner_hint",
        "student": "I'm a visual learner — is there a picture that shows how the attention weights are computed?",
        "concepts": ["attention mechanism", "attention weights"],
        "lesson_title": "Attention Mechanism",
        "expect_images": True,
    },
    {
        "name": "conceptual_question_no_image",
        "student": "What is the difference between hard and soft attention?",
        "concepts": ["attention mechanism", "bahdanau attention"],
        "lesson_title": "Attention Mechanism",
        "expect_images": False,  # might still show one, but shouldn't be forced
    },
    {
        "name": "self_attention_architecture",
        "student": "Can you show me the self-attention architecture diagram?",
        "concepts": ["self-attention", "multi-head attention"],
        "lesson_title": "Self-Attention",
        "expect_images": True,
    },
    {
        "name": "no_images_available",
        "student": "Show me a diagram of how softmax temperature scaling works.",
        "concepts": ["softmax", "temperature"],
        "lesson_title": "Softmax and Temperature",
        "expect_images": False,  # no images in wiki for these concepts
    },
]


# ── Tier 1: Tool plumbing ────────────────────────────────────────────────

def eval_tool_plumbing() -> list[Check]:
    checks = []

    # 1. Tool registered
    names = [t["function"]["name"] for t in TUTOR_TOOLS]
    checks.append(Check(
        "tool_registered",
        "get_relevant_images" in names,
        "get_relevant_images in TUTOR_TOOLS",
    ))

    # 2. Tool schema well-formed
    tool = next((t for t in TUTOR_TOOLS if t["function"]["name"] == "get_relevant_images"), None)
    if tool:
        params = tool["function"].get("parameters", {})
        has_concepts = "concepts" in params.get("properties", {})
        checks.append(Check("tool_schema_concepts", has_concepts, "concepts param exists"))
        is_required = "concepts" in params.get("required", [])
        checks.append(Check("tool_schema_required", is_required, "concepts is required"))

    # 3. Direct call with matching concepts
    result = _get_relevant_images(["attention mechanism", "bahdanau attention"])
    count = result.get("image_count", 0)
    checks.append(Check("direct_call_match", count > 0, f"{count} images returned"))

    if count > 0:
        img = result["images"][0]
        checks.append(Check(
            "image_has_path",
            img.get("path", "").startswith("/api/wiki-images/"),
            f"path={img.get('path', '')[:60]}",
        ))
        checks.append(Check(
            "image_has_caption",
            bool(img.get("caption")),
            f"caption={'yes' if img.get('caption') else 'missing'}",
            severity="warning",
        ))
        checks.append(Check(
            "image_has_when_to_show",
            bool(img.get("when_to_show")),
            f"when_to_show={'yes' if img.get('when_to_show') else 'missing'}",
            severity="warning",
        ))

        # Verify the image file actually exists on disk
        rel_path = img["path"].replace("/api/wiki-images/", "")
        disk_path = WIKI_DIR / "resources" / "by-topic" / rel_path
        checks.append(Check(
            "image_file_exists",
            disk_path.exists(),
            f"{'found' if disk_path.exists() else 'MISSING'}: {disk_path.name}",
        ))

    # 4. Max count respected
    result_big = _get_relevant_images(["attention mechanism"])
    checks.append(Check(
        "max_count_respected",
        result_big.get("image_count", 0) <= 6,
        f"{result_big.get('image_count', 0)} <= 6",
    ))

    # 5. Empty concepts returns error
    result_empty = _get_relevant_images([])
    checks.append(Check("empty_concepts_error", "error" in result_empty, "returns error key"))

    # 6. Unrelated concepts returns 0
    result_miss = _get_relevant_images(["quantum entanglement", "string theory"])
    checks.append(Check(
        "no_match_returns_zero",
        result_miss.get("image_count", 0) == 0,
        f"{result_miss.get('image_count', 0)} images",
    ))

    return checks


# ── Tier 2: Agent flow scenarios ─────────────────────────────────────────

async def run_scenario(scenario: dict) -> ScenarioResult:
    from app.agent.agent_loop import run_tutor_agent_loop

    sr = ScenarioResult(
        name=scenario["name"],
        student_message=scenario["student"],
        expect_images=scenario["expect_images"],
    )

    context = TutorContext(
        lesson_id=f"eval-{scenario['name']}",
        lesson_title=scenario["lesson_title"],
        lesson_summary=f"Understanding {scenario['lesson_title'].lower()}",
        concepts=scenario["concepts"],
        completed_lesson_titles=[],
        lesson_content=f"This lesson covers {', '.join(scenario['concepts'])}.",
        reference_kb="",
    )

    messages = [{"role": "user", "content": scenario["student"]}]
    text_parts: list[str] = []

    t0 = time.monotonic()
    try:
        async for event_str in run_tutor_agent_loop(messages, context):
            if not event_str.startswith("data: "):
                continue
            raw = event_str[6:].strip()
            if not raw:
                continue
            event = json.loads(raw)

            if event["type"] == "tool_call":
                sr.tool_calls.append(event["name"])
            elif event["type"] == "text":
                text_parts.append(event.get("delta", ""))
            elif event["type"] == "done":
                break
    except Exception as e:
        sr.checks.append(Check("agent_no_crash", False, str(e)))
        return sr

    sr.elapsed_s = time.monotonic() - t0
    sr.response_text = "".join(text_parts)

    # Parse <image> blocks
    for m in IMAGE_TAG_RE.finditer(sr.response_text):
        try:
            sr.image_blocks.append(json.loads(m.group(1)))
        except json.JSONDecodeError:
            sr.checks.append(Check("image_json_valid", False, f"Bad JSON: {m.group(1)[:60]}"))

    # -- Checks --

    sr.checks.append(Check(
        "agent_no_crash", True,
        f"completed in {sr.elapsed_s:.1f}s",
        severity="info",
    ))

    used_image_tool = "get_relevant_images" in sr.tool_calls
    if scenario["expect_images"]:
        sr.checks.append(Check(
            "used_image_tool",
            used_image_tool,
            f"tool calls: {sr.tool_calls or 'none'}",
            severity="warning",
        ))

        has_image_block = len(sr.image_blocks) > 0
        has_inline_image = "![" in sr.response_text
        shows_image = has_image_block or has_inline_image
        sr.checks.append(Check(
            "shows_image",
            shows_image,
            f"<image> blocks: {len(sr.image_blocks)}, inline ![]: {has_inline_image}",
        ))

        # Validate image block structure
        for i, img in enumerate(sr.image_blocks):
            has_path = isinstance(img.get("path"), str) and img["path"].startswith("/api/wiki-images/")
            sr.checks.append(Check(
                f"block_{i}_valid_path",
                has_path,
                img.get("path", "missing")[:60],
            ))
            has_caption = bool(img.get("caption"))
            sr.checks.append(Check(
                f"block_{i}_has_caption",
                has_caption,
                "present" if has_caption else "missing",
                severity="warning",
            ))

            # Check file exists on disk
            if has_path:
                rel = img["path"].replace("/api/wiki-images/", "")
                exists = (WIKI_DIR / "resources" / "by-topic" / rel).exists()
                sr.checks.append(Check(
                    f"block_{i}_file_exists",
                    exists,
                    f"{'found' if exists else 'MISSING'} on disk",
                ))

        # Contextual introduction — tutor should say something before the image
        if has_image_block:
            first_tag_pos = sr.response_text.index("<image>")
            text_before = sr.response_text[:first_tag_pos].strip()
            has_intro = len(text_before.split()) >= 5
            sr.checks.append(Check(
                "contextual_intro",
                has_intro,
                f"{len(text_before.split())} words before first <image>",
                severity="warning",
            ))
    else:
        # For "no images expected" scenarios, it's okay either way —
        # but the tutor should not crash or hallucinate image paths
        if sr.image_blocks:
            for i, img in enumerate(sr.image_blocks):
                if img.get("path"):
                    rel = img["path"].replace("/api/wiki-images/", "")
                    exists = (WIKI_DIR / "resources" / "by-topic" / rel).exists()
                    sr.checks.append(Check(
                        f"optional_block_{i}_file_exists",
                        exists,
                        f"{'found' if exists else 'HALLUCINATED'} on disk",
                    ))

        sr.checks.append(Check(
            "response_not_empty",
            len(sr.response_text.strip()) > 20,
            f"{len(sr.response_text)} chars",
        ))

    return sr


# ── Tier 3: LLM rubric for image integration quality ────────────────────

RUBRIC_PROMPT = """\
You are evaluating how well an AI tutor integrated visual images into its response.

Student message: {student_message}
Tutor response:
---
{response}
---

Score each dimension 1-5:

1. **relevance**: Did the tutor pick images that match what the student asked about? (5 = perfect match, 1 = unrelated)
2. **contextual_framing**: Did the tutor explain what the image shows and what to look for, rather than just dropping it in? (5 = excellent setup, 1 = no explanation)
3. **pedagogical_timing**: Was the image placed at the right point in the explanation? (5 = perfect placement, 1 = awkward/disruptive)
4. **restraint**: Did the tutor show an appropriate number of images (usually 1-2), or dump too many? (5 = just right, 1 = image overload or zero when one was needed)

Return ONLY a JSON object: {{"relevance": N, "contextual_framing": N, "pedagogical_timing": N, "restraint": N, "notes": "brief comment"}}"""


async def eval_rubric(sr: ScenarioResult) -> dict[str, Any]:
    if not sr.image_blocks and not sr.expect_images:
        return {}

    from app.services.course_generator import _call_llm_json

    prompt = RUBRIC_PROMPT.format(
        student_message=sr.student_message,
        response=sr.response_text[:4000],
    )
    try:
        return await _call_llm_json(prompt, max_tokens=256)
    except Exception as e:
        return {"error": str(e)}


# ── Reporting ─────────────────────────────────────────────────────────────

def _icon(check: Check) -> str:
    if check.passed:
        return PASS if check.severity != "info" else INFO
    return FAIL if check.severity == "error" else WARN


def print_report(
    plumbing: list[Check],
    scenarios: list[ScenarioResult],
) -> int:
    print("\n" + "=" * 64)
    print("IMAGE TUTORING EVAL")
    print("=" * 64)

    total_pass = total_fail = total_warn = 0

    # Tier 1
    print("\n  Tier 1 — Tool Plumbing\n")
    for c in plumbing:
        print(f"    {_icon(c)} {c.name}: {c.detail}")
        if c.passed:
            total_pass += 1
        elif c.severity == "error":
            total_fail += 1
        else:
            total_warn += 1

    # Tier 2
    if scenarios:
        print(f"\n  Tier 2 — Agent Flow Scenarios ({len(scenarios)})\n")
        for sr in scenarios:
            expects = "expects images" if sr.expect_images else "no images expected"
            print(f"    ── {sr.name} ({expects}, {sr.elapsed_s:.1f}s) ──")
            print(f"       Student: \"{sr.student_message[:70]}\"")
            print(f"       Tools used: {sr.tool_calls or ['none']}")
            print(f"       <image> blocks: {len(sr.image_blocks)}")

            for c in sr.checks:
                print(f"       {_icon(c)} {c.name}: {c.detail}")
                if c.passed:
                    total_pass += 1
                elif c.severity == "error":
                    total_fail += 1
                else:
                    total_warn += 1

            # Response preview
            preview = sr.response_text[:200].replace("\n", " ")
            print(f"       Response: {preview}...")

            # Rubric scores
            if sr.rubric_scores and "error" not in sr.rubric_scores:
                scores = {k: v for k, v in sr.rubric_scores.items() if k != "notes"}
                avg = sum(v for v in scores.values() if isinstance(v, (int, float))) / max(len(scores), 1)
                print(f"       Rubric: {scores}  (avg {avg:.1f}/5)")
                if sr.rubric_scores.get("notes"):
                    print(f"       Notes: {sr.rubric_scores['notes']}")

            print()

    # Summary
    print("  " + "-" * 60)
    print(f"  Total: {total_pass} passed, {total_warn} warnings, {total_fail} failed")
    print("=" * 64)

    return 1 if total_fail > 0 else 0


# ── Main ──────────────────────────────────────────────────────────────────

async def main():
    parser = argparse.ArgumentParser(description="Image tutoring flow evaluation")
    parser.add_argument("--llm", action="store_true", help="Run Tier 2 agent flow scenarios (requires LLM)")
    parser.add_argument("--rubric", action="store_true", help="Run Tier 3 LLM rubric scoring (implies --llm)")
    parser.add_argument("--scenario", type=str, default=None, help="Run a single scenario by name")
    args = parser.parse_args()

    if args.rubric:
        args.llm = True

    # Tier 1
    plumbing = eval_tool_plumbing()

    # Tier 2
    scenarios: list[ScenarioResult] = []
    if args.llm:
        run_list = SCENARIOS
        if args.scenario:
            run_list = [s for s in SCENARIOS if s["name"] == args.scenario]
            if not run_list:
                print(f"[!] Unknown scenario '{args.scenario}'")
                print(f"    Available: {[s['name'] for s in SCENARIOS]}")
                sys.exit(1)

        for s in run_list:
            print(f"  Running scenario: {s['name']}...")
            sr = await run_scenario(s)

            # Tier 3 rubric (only for scenarios that expect images)
            if args.rubric and sr.expect_images and sr.image_blocks:
                print(f"    Scoring with LLM rubric...")
                sr.rubric_scores = await eval_rubric(sr)

            scenarios.append(sr)

    exit_code = print_report(plumbing, scenarios)
    sys.exit(exit_code)


if __name__ == "__main__":
    asyncio.run(main())
