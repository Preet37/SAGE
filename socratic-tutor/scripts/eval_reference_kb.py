#!/usr/bin/env python3
"""
Reference KB quality evaluator — Option B (LLM-as-judge).

Compares the OLD reference KB stored in the DB against a freshly generated
one using the current prompt. Scores both on a tutoring-specific rubric and
prints a side-by-side markdown report.

Usage:
    python3 scripts/eval_reference_kb.py                         # auto-pick 3 lessons
    python3 scripts/eval_reference_kb.py attention-mechanism     # specific lesson slug
    python3 scripts/eval_reference_kb.py slug1 slug2 slug3       # multiple slugs
    python3 scripts/eval_reference_kb.py --list                  # show lessons with KB

Outputs:
    scripts/eval_kb_report.md   — full side-by-side comparison + scores

Environment:
    LLM_API_KEY, LLM_BASE_URL, LLM_MODEL — read from backend/.env if present
"""

import asyncio
import json
import os
import sys
import textwrap
from pathlib import Path
from datetime import datetime

REPO_ROOT = Path(__file__).parent.parent
BACKEND_ENV = REPO_ROOT / "backend" / ".env"
BACKEND_SETTINGS = REPO_ROOT / "backend" / "settings.yaml"
REPORT_PATH = Path(__file__).parent / "eval_kb_report.md"

# ---------------------------------------------------------------------------
# Bootstrap: load env and add backend to sys.path
# ---------------------------------------------------------------------------

def _load_env() -> None:
    if BACKEND_ENV.exists():
        for line in BACKEND_ENV.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                os.environ.setdefault(k.strip(), v.strip())


def _load_llm_settings() -> dict:
    try:
        import yaml
        with open(BACKEND_SETTINGS) as f:
            cfg = yaml.safe_load(f)
        return {
            "base_url": cfg.get("llm", {}).get("base_url", "https://inference-api.nvidia.com"),
            "model": cfg.get("models", {}).get("tutor", {}).get("model_id", "openai/openai/gpt-5.2"),
        }
    except Exception:
        return {
            "base_url": "https://inference-api.nvidia.com",
            "model": "openai/openai/gpt-5.2",
        }


_load_env()
sys.path.insert(0, str(REPO_ROOT / "backend"))

# ---------------------------------------------------------------------------
# LLM client
# ---------------------------------------------------------------------------

def _make_client():
    from openai import OpenAI
    settings = _load_llm_settings()
    api_key = os.environ.get("LLM_API_KEY", "")
    if not api_key:
        print("ERROR: LLM_API_KEY not set.", file=sys.stderr)
        sys.exit(1)
    return OpenAI(api_key=api_key, base_url=settings["base_url"]), settings["model"]


def _llm_call(client, model: str, prompt: str, max_tokens: int = 6000) -> str:
    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
        temperature=0.3,
    )
    return resp.choices[0].message.content or ""

# ---------------------------------------------------------------------------
# DB access — fetch lessons with reference_kb
# ---------------------------------------------------------------------------

def _fetch_lessons(slugs: list[str] | None = None) -> list[dict]:
    """Return lessons from the DB. If slugs given, fetch those; else auto-pick."""
    from sqlmodel import Session, select
    from app.db import engine
    from app.models.learning import Lesson

    with Session(engine) as session:
        if slugs:
            results = []
            for slug in slugs:
                stmt = select(Lesson).where(Lesson.slug == slug)
                lesson = session.exec(stmt).first()
                if lesson:
                    results.append(lesson)
                else:
                    print(f"WARNING: no lesson found for slug '{slug}'", file=sys.stderr)
            return results
        else:
            # Auto-pick: lessons that have both reference_kb and summary
            stmt = select(Lesson).where(
                Lesson.reference_kb.isnot(None),  # type: ignore[attr-defined]
                Lesson.summary.isnot(None),       # type: ignore[attr-defined]
            )
            all_lessons = session.exec(stmt).all()
            # Filter to those with substantive KB (>300 words) and prefer variety
            with_kb = [l for l in all_lessons if l.reference_kb and len(l.reference_kb.split()) > 300]
            if not with_kb:
                print("No lessons with reference KB found in the database.", file=sys.stderr)
                sys.exit(1)
            # Pick up to 3: spread across different lengths to test variety
            with_kb.sort(key=lambda l: len(l.reference_kb or ""), reverse=True)
            picks = [with_kb[0]]  # longest
            if len(with_kb) > 2:
                picks.append(with_kb[len(with_kb) // 2])  # median
            if len(with_kb) > 1:
                picks.append(with_kb[-1])  # shortest
            return picks[:3]


def _list_lessons_with_kb() -> None:
    from sqlmodel import Session, select
    from app.db import engine
    from app.models.learning import Lesson

    with Session(engine) as session:
        stmt = select(Lesson).where(Lesson.reference_kb.isnot(None))  # type: ignore[attr-defined]
        lessons = session.exec(stmt).all()
    rows = [(l.slug, len((l.reference_kb or "").split())) for l in lessons if l.reference_kb]
    rows.sort(key=lambda x: x[1], reverse=True)
    print(f"\n{'Slug':<45} {'KB words':>10}")
    print("-" * 57)
    for slug, words in rows:
        print(f"{slug:<45} {words:>10,}")
    print(f"\nTotal: {len(rows)} lessons with reference KB\n")

# ---------------------------------------------------------------------------
# Regenerate KB with current prompt
# ---------------------------------------------------------------------------

async def _regenerate_kb(lesson) -> str:
    """Regenerate the reference KB for a lesson using the current prompt."""
    from app.services.course_generator import generate_reference_kb_from_wiki

    lesson_dict = {
        "title": lesson.title,
        "slug": lesson.slug,
        "summary": lesson.summary or "",
        "concepts": json.loads(lesson.concepts) if isinstance(lesson.concepts, str) else (lesson.concepts or []),
    }

    new_kb = ""
    async for event_str in generate_reference_kb_from_wiki([lesson_dict], existing_kb={}):
        if not event_str.strip().startswith("data: "):
            continue
        try:
            evt = json.loads(event_str.strip()[6:])
            if evt.get("type") == "reference_kb":
                new_kb = evt.get("data", {}).get(lesson.slug, "")
        except (json.JSONDecodeError, KeyError):
            pass
    return new_kb

# ---------------------------------------------------------------------------
# Judge prompt
# ---------------------------------------------------------------------------

JUDGE_PROMPT = """\
You are evaluating two reference knowledge documents for an AI Socratic tutor. \
Both documents are for the same lesson. Document A is the OLD version; \
Document B is the NEW version generated with a revised prompt.

LESSON: {title}

---
DOCUMENT A (old):
{doc_a}

---
DOCUMENT B (new):
{doc_b}

---
Score each document on these five dimensions (1-5 scale each):

1. **Definition Precision** — Are key terms defined precisely enough for the \
tutor to quote directly? (1=vague/missing, 5=exact, quotable)

2. **Explanation Diversity** — Does the document offer multiple ways to explain \
the concept (intuitive, technical, analogy)? (1=one approach only, 5=clearly \
multiple angles)

3. **Misconception Coverage** — Does it name specific things students get wrong \
and explain the correction? (1=none, 5=3+ specific misconceptions with corrections)

4. **Teaching Utility** — Does it include Socratic questions, worked examples, \
or prerequisite connections that a tutor would actually use? \
(1=none, 5=all three present and specific)

5. **Resource Inventory** — Does it list available videos/articles with guidance \
on when to surface them? (1=no resources listed, 5=clear catalog with "when to show")

Respond ONLY with valid JSON in this exact format:
{{
  "doc_a": {{
    "definition_precision": <1-5>,
    "explanation_diversity": <1-5>,
    "misconception_coverage": <1-5>,
    "teaching_utility": <1-5>,
    "resource_inventory": <1-5>,
    "total": <sum of above>,
    "strengths": "<one sentence>",
    "weaknesses": "<one sentence>"
  }},
  "doc_b": {{
    "definition_precision": <1-5>,
    "explanation_diversity": <1-5>,
    "misconception_coverage": <1-5>,
    "teaching_utility": <1-5>,
    "resource_inventory": <1-5>,
    "total": <sum of above>,
    "strengths": "<one sentence>",
    "weaknesses": "<one sentence>"
  }},
  "verdict": "A" | "B" | "tie",
  "verdict_reason": "<one sentence explaining the outcome>"
}}
"""

# ---------------------------------------------------------------------------
# Report builder
# ---------------------------------------------------------------------------

SCORE_DIMS = [
    ("definition_precision", "Definition Precision"),
    ("explanation_diversity", "Explanation Diversity"),
    ("misconception_coverage", "Misconception Coverage"),
    ("teaching_utility", "Teaching Utility"),
    ("resource_inventory", "Resource Inventory"),
]


def _format_scores(scores: dict) -> str:
    rows = []
    for key, label in SCORE_DIMS:
        a = scores["doc_a"].get(key, "?")
        b = scores["doc_b"].get(key, "?")
        delta = ""
        if isinstance(a, int) and isinstance(b, int):
            if b > a:
                delta = f" ▲+{b-a}"
            elif b < a:
                delta = f" ▼{b-a}"
        rows.append(f"| {label} | {a}/5 | {b}/5{delta} |")
    total_a = scores["doc_a"].get("total", "?")
    total_b = scores["doc_b"].get("total", "?")
    total_delta = ""
    if isinstance(total_a, int) and isinstance(total_b, int):
        diff = total_b - total_a
        total_delta = f" ({'▲+' if diff >= 0 else '▼'}{abs(diff)})" if diff != 0 else " (tie)"
    rows.append(f"| **TOTAL** | **{total_a}/25** | **{total_b}/25{total_delta}** |")
    header = "| Dimension | Old (A) | New (B) |\n|---|---|---|"
    return header + "\n" + "\n".join(rows)


def _build_report(results: list[dict]) -> str:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [
        f"# Reference KB Eval Report",
        f"*Generated {ts}*\n",
        "Comparing **old stored KB (A)** vs **new prompt KB (B)** for "
        f"{len(results)} lesson(s).\n",
        "---\n",
    ]

    wins = {"A": 0, "B": 0, "tie": 0}
    for r in results:
        lines.append(f"## {r['title']}")
        lines.append(f"*Slug: `{r['slug']}`*\n")

        # Source breakdown
        bd = r.get("source_breakdown", {})
        if bd:
            mode_label = {
                "blended": "Blended (reference + pedagogy)",
                "pedagogy_only": "Pedagogy-only fallback",
            }.get(bd.get("mode", ""), bd.get("mode", ""))
            lines.append(
                f"**Sources:** {bd.get('pedagogy', '?')} pedagogy, "
                f"{bd.get('reference', '?')} reference — *{mode_label}*\n"
            )

        if r.get("error"):
            lines.append(f"> **Error:** {r['error']}\n")
            continue

        scores = r.get("scores", {})
        if scores:
            lines.append(_format_scores(scores))
            lines.append("")
            verdict = scores.get("verdict", "?")
            wins[verdict] = wins.get(verdict, 0) + 1
            verdict_label = {"A": "Old wins", "B": "New wins", "tie": "Tie"}.get(verdict, verdict)
            lines.append(f"**Verdict: {verdict_label}** — {scores.get('verdict_reason', '')}\n")
            lines.append(f"- Old strengths: {scores['doc_a'].get('strengths', '')}")
            lines.append(f"- Old weaknesses: {scores['doc_a'].get('weaknesses', '')}")
            lines.append(f"- New strengths: {scores['doc_b'].get('strengths', '')}")
            lines.append(f"- New weaknesses: {scores['doc_b'].get('weaknesses', '')}")
            lines.append("")

        if r.get("new_kb"):
            lines.append("<details><summary>New KB (B) — click to expand</summary>\n")
            lines.append("```markdown")
            lines.append(r["new_kb"][:4000] + (" [truncated...]" if len(r["new_kb"]) > 4000 else ""))
            lines.append("```\n</details>\n")

        lines.append("---\n")

    lines.append("## Summary")
    lines.append(f"- New wins: **{wins.get('B', 0)}**")
    lines.append(f"- Old wins: **{wins.get('A', 0)}**")
    lines.append(f"- Ties: **{wins.get('tie', 0)}**")

    return "\n".join(lines)

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def _get_source_breakdown(lesson) -> dict:
    """Count pedagogy vs reference sources available for a lesson."""
    from app.services.course_generator import load_wiki_context, resolve_topics_llm

    concepts = json.loads(lesson.concepts) if isinstance(lesson.concepts, str) else (lesson.concepts or [])
    if not concepts:
        return {"pedagogy": 0, "reference": 0, "mode": "no_concepts"}

    try:
        import asyncio
        resolved = asyncio.get_event_loop().run_until_complete(
            resolve_topics_llm(
                concepts, lesson_title=lesson.title,
                lesson_summary=lesson.summary or "",
            )
        )
        topic_slugs = resolved["topic_slugs"]
    except Exception:
        from app.services.course_generator import resolve_topics_exact
        topic_slugs = resolve_topics_exact(concepts)["topic_slugs"]

    ped_ctx = load_wiki_context(concepts, topic_slugs=topic_slugs)
    ref_ctx = load_wiki_context(concepts, topic_slugs=topic_slugs, track="reference")

    ped_count = sum(len(v) for v in ped_ctx.get("source_content", {}).values())
    ref_count = sum(len(v) for v in ref_ctx.get("source_content", {}).values())

    if ref_count > 0:
        mode = "blended"
    else:
        mode = "pedagogy_only"

    return {"pedagogy": ped_count, "reference": ref_count, "mode": mode}


async def _run(slugs: list[str] | None) -> None:
    client, model = _make_client()

    print("Fetching lessons from database...")
    lessons = _fetch_lessons(slugs)
    print(f"Found {len(lessons)} lesson(s) to evaluate: {[l.slug for l in lessons]}\n")

    results = []
    for lesson in lessons:
        # Report source breakdown
        breakdown = _get_source_breakdown(lesson)
        mode_label = {
            "blended": "BLENDED (ref+ped)",
            "pedagogy_only": "FALLBACK (pedagogy only)",
            "no_concepts": "N/A",
        }.get(breakdown["mode"], breakdown["mode"])
        print(f"[{lesson.slug}] Sources: {breakdown['pedagogy']} pedagogy, "
              f"{breakdown['reference']} reference — mode: {mode_label}")

        print(f"  Regenerating KB with new prompt...")
        try:
            new_kb = await _regenerate_kb(lesson)
        except Exception as e:
            print(f"  ERROR regenerating KB: {e}")
            results.append({"slug": lesson.slug, "title": lesson.title, "error": str(e)})
            continue

        if not new_kb:
            print(f"  WARNING: new KB came back empty (no wiki source material?)")
            results.append({
                "slug": lesson.slug,
                "title": lesson.title,
                "error": "New KB generation returned empty — likely no wiki downloads for this lesson's concepts.",
            })
            continue

        old_kb = lesson.reference_kb or ""
        old_words = len(old_kb.split())
        new_words = len(new_kb.split())
        print(f"  Old KB: {old_words:,} words | New KB: {new_words:,} words")

        print(f"  Scoring with LLM judge...")
        judge_prompt = JUDGE_PROMPT.format(
            title=lesson.title,
            doc_a=old_kb[:6000],
            doc_b=new_kb[:6000],
        )
        try:
            raw = _llm_call(client, model, judge_prompt, max_tokens=1000)
            # Strip markdown code fences if present
            raw = raw.strip()
            if raw.startswith("```"):
                raw = raw.split("```", 2)[1]
                if raw.startswith("json"):
                    raw = raw[4:]
            scores = json.loads(raw.strip())
        except Exception as e:
            print(f"  ERROR parsing judge response: {e}")
            scores = {}

        verdict = scores.get("verdict", "?")
        total_a = scores.get("doc_a", {}).get("total", "?")
        total_b = scores.get("doc_b", {}).get("total", "?")
        print(f"  Verdict: {verdict} | Old={total_a}/25 | New={total_b}/25\n")

        results.append({
            "slug": lesson.slug,
            "title": lesson.title,
            "scores": scores,
            "new_kb": new_kb,
            "source_breakdown": breakdown,
        })

    report = _build_report(results)
    REPORT_PATH.write_text(report)
    print(f"Report written to: {REPORT_PATH}")
    print("\n--- Summary ---")
    verdicts = [r.get("scores", {}).get("verdict") for r in results if r.get("scores")]
    wins_b = verdicts.count("B")
    wins_a = verdicts.count("A")
    ties = verdicts.count("tie")
    print(f"New wins: {wins_b} | Old wins: {wins_a} | Ties: {ties}")

    # Report source mode breakdown
    blended = sum(1 for r in results if r.get("source_breakdown", {}).get("mode") == "blended")
    fallback = sum(1 for r in results if r.get("source_breakdown", {}).get("mode") == "pedagogy_only")
    if blended or fallback:
        print(f"Source modes: {blended} blended (ref+ped), {fallback} pedagogy-only fallback")


def main() -> None:
    args = sys.argv[1:]

    if "--list" in args:
        _list_lessons_with_kb()
        return

    slugs = [a for a in args if not a.startswith("--")] or None
    asyncio.run(_run(slugs))


if __name__ == "__main__":
    main()
