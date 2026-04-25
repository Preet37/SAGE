#!/usr/bin/env python3
"""Identify non-educator authors worth promoting to canonical educator.

Uses wiki signals (source count, topic spread) + LLM assessment to:
- Auto-promote obvious candidates (strong signals + LLM agrees)
- Surface near-misses with reasoning for human review
- Skip authors with thin evidence

Usage:
    uv run python scripts/promote_authors.py                  # scan + assess
    uv run python scripts/promote_authors.py --dry-run        # scan only, no LLM
    uv run python scripts/promote_authors.py --apply          # auto-apply promotions
    uv run python scripts/promote_authors.py --threshold 3    # min sources to consider
"""

import argparse
import asyncio
import json
import os
import re
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import httpx

from app.config import get_settings
from app.services.wiki_authors import (
    load_authors,
    get_author_by_slug,
    invalidate_cache,
    _AUTHORS_PATH,
)

_WIKI_DIR = Path(os.environ.get("CONTENT_DIR", str(Path(__file__).resolve().parent.parent.parent / "content"))).resolve() / "pedagogy-wiki"
_REPORT_PATH = _WIKI_DIR / "educator-promotion-report.md"

_HEADER_AUTHOR_SLUG_RE = re.compile(r"^#\s*Author Slug:\s*(\S+)", re.MULTILINE)
_HEADER_SOURCE_RE = re.compile(r"^#\s*Source:\s*(https?://\S+)", re.MULTILINE)

_AUTO_PROMOTE_THRESHOLD = {"sources": 8, "topics": 4}
_CONSIDERATION_THRESHOLD = {"sources": 3, "topics": 2}

# ---------------------------------------------------------------------------
# LLM helper (same pattern as the rest of the codebase)
# ---------------------------------------------------------------------------

_llm_semaphore = asyncio.Semaphore(3)


async def _call_llm(prompt: str, *, max_tokens: int = 2048, temperature: float = 0.3) -> str:
    settings = get_settings()
    headers = {
        "Authorization": f"Bearer {settings.llm_api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": settings.llm_model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": temperature,
    }
    async with _llm_semaphore:
        t0 = time.monotonic()
        async with httpx.AsyncClient(timeout=120.0) as client:
            resp = await client.post(
                f"{settings.llm_base_url}/chat/completions",
                headers=headers,
                json=payload,
            )
            resp.raise_for_status()
            content = resp.json()["choices"][0]["message"]["content"].strip()
            elapsed = time.monotonic() - t0
            print(f"  LLM call: {elapsed:.1f}s ({len(content)} chars)")
            return content


async def _call_llm_json(prompt: str, **kwargs) -> dict:
    raw = await _call_llm(prompt, **kwargs)
    text = raw.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[-1]
        if text.endswith("```"):
            text = text[:-3]
        text = text.strip()
    return json.loads(text)


# ---------------------------------------------------------------------------
# Wiki signal collection
# ---------------------------------------------------------------------------

def scan_author_signals() -> dict[str, dict]:
    """Scan all source .md files and compute per-author wiki signals.

    Returns {slug: {name, sources, topics, source_list}} for non-educator authors.
    """
    source_dir = _WIKI_DIR / "resources" / "by-topic"
    slug_sources: dict[str, list[dict]] = defaultdict(list)

    for topic_dir in sorted(source_dir.iterdir()):
        if not topic_dir.is_dir():
            continue
        topic = topic_dir.name
        for f in sorted(topic_dir.glob("*.md")):
            if f.name.startswith("_") or f.name == "curation-report.md":
                continue
            head = f.read_text(errors="replace")[:500]
            m_slug = _HEADER_AUTHOR_SLUG_RE.search(head)
            m_source = _HEADER_SOURCE_RE.search(head)
            if m_slug and m_source:
                slug_sources[m_slug.group(1)].append({
                    "topic": topic,
                    "url": m_source.group(1),
                    "file": str(f.relative_to(_WIKI_DIR)),
                })

    authors = load_authors()
    educator_slugs = {a["slug"] for a in authors if a.get("canonical_educator")}

    signals: dict[str, dict] = {}
    for slug, sources in slug_sources.items():
        if slug in educator_slugs:
            continue
        author = get_author_by_slug(slug)
        topics = sorted(set(s["topic"] for s in sources))
        signals[slug] = {
            "name": author["name"] if author else slug,
            "slug": slug,
            "type": author.get("type", "unknown") if author else "unknown",
            "sources": len(sources),
            "topics": len(topics),
            "topic_list": topics,
            "source_list": sources,
        }

    return dict(sorted(signals.items(), key=lambda x: -x[1]["sources"]))


# ---------------------------------------------------------------------------
# LLM assessment
# ---------------------------------------------------------------------------

_ASSESS_PROMPT = """\
You are assessing whether an author/organization should be promoted to \
"canonical educator" in a Socratic tutoring platform's knowledge base.

A canonical educator is someone whose content is consistently high-quality, \
pedagogically valuable, and worth recommending to learners by name. They have \
a distinct teaching style and cover topics with depth.

AUTHOR: {name}
TYPE: {type}
WIKI EVIDENCE:
- {sources} source documents across {topics} topics
- Topics covered: {topic_list}
- Sample URLs:
{sample_urls}

Based on your knowledge of this author/organization AND the wiki evidence above, \
assess their suitability as a canonical educator.

Return a JSON object:
{{
  "recommendation": "promote" | "near_miss" | "skip",
  "confidence": 0.0-1.0,
  "reasoning": "2-3 sentence explanation of your recommendation",
  "level": "beginner" | "beginner-intermediate" | "intermediate" | "intermediate-advanced" | "advanced",
  "style": "one-line teaching style description",
  "best_topics": ["topic-slug-1", "topic-slug-2", ...],
  "pairs_with": ["educator-slug-1", "educator-slug-2", ...]
}}

For "skip": set level/style/best_topics/pairs_with to null.
For "near_miss": fill in all fields — the human reviewer needs them.
For "promote": fill in all fields confidently.

Only return the JSON object, no other text.
"""


async def assess_candidate(signal: dict) -> dict:
    """Ask the LLM to assess a single promotion candidate."""
    sample_urls = "\n".join(
        f"  - {s['url']}" for s in signal["source_list"][:8]
    )
    prompt = _ASSESS_PROMPT.format(
        name=signal["name"],
        type=signal["type"],
        sources=signal["sources"],
        topics=signal["topics"],
        topic_list=", ".join(signal["topic_list"]),
        sample_urls=sample_urls,
    )
    try:
        result = await _call_llm_json(prompt)
        result["slug"] = signal["slug"]
        result["name"] = signal["name"]
        result["wiki_sources"] = signal["sources"]
        result["wiki_topics"] = signal["topics"]
        return result
    except Exception as e:
        return {
            "slug": signal["slug"],
            "name": signal["name"],
            "recommendation": "error",
            "reasoning": str(e),
        }


# ---------------------------------------------------------------------------
# Apply promotions to authors.md
# ---------------------------------------------------------------------------

def apply_promotion(assessment: dict) -> bool:
    """Write educator fields into the author's block in authors.md."""
    slug = assessment["slug"]
    text = _AUTHORS_PATH.read_text(encoding="utf-8")

    blocks = re.split(r"(\n## )", text)
    updated = False

    for i, block in enumerate(blocks):
        if f"- Slug: {slug}" in block and "- Canonical Educator:" not in block:
            new_lines = []
            if assessment.get("style"):
                new_lines.append(f"- Canonical Educator: yes")
                new_lines.append(f"- Level: {assessment['level']}")
                topics = ", ".join(assessment.get("best_topics") or [])
                new_lines.append(f"- Best Topics: {topics}")
                new_lines.append(f"- Style: {assessment['style']}")
                pairs = ", ".join(assessment.get("pairs_with") or [])
                new_lines.append(f"- Pairs With: {pairs}")

            if new_lines:
                block_lines = block.rstrip().split("\n")
                block_lines.extend(new_lines)
                blocks[i] = "\n".join(block_lines) + "\n"
                updated = True
            break

    if updated:
        _AUTHORS_PATH.write_text("".join(blocks), encoding="utf-8")
        invalidate_cache()
        print(f"  ✓ Promoted {assessment['name']} to canonical educator")
    return updated


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------

def write_report(assessments: list[dict], signals: dict[str, dict]) -> None:
    """Write a human-reviewable promotion report."""
    promotes = [a for a in assessments if a["recommendation"] == "promote"]
    near_misses = [a for a in assessments if a["recommendation"] == "near_miss"]
    skips = [a for a in assessments if a["recommendation"] == "skip"]
    errors = [a for a in assessments if a["recommendation"] == "error"]

    lines = [
        "# Educator Promotion Report",
        f"Generated: {time.strftime('%Y-%m-%d %H:%M')}",
        "",
        f"Candidates assessed: {len(assessments)}",
        f"  Promote: {len(promotes)}  |  Near-miss: {len(near_misses)}  "
        f"|  Skip: {len(skips)}  |  Error: {len(errors)}",
        "",
    ]

    if promotes:
        lines.append("## Auto-Promoted")
        lines.append("")
        for a in promotes:
            lines.append(f"### {a['name']}")
            lines.append(f"- Sources: {a['wiki_sources']} across {a['wiki_topics']} topics")
            lines.append(f"- Confidence: {a.get('confidence', '?')}")
            lines.append(f"- Level: {a.get('level', '?')}")
            lines.append(f"- Style: {a.get('style', '?')}")
            lines.append(f"- Reasoning: {a.get('reasoning', '')}")
            lines.append("")

    if near_misses:
        lines.append("## Near-Misses (Needs Human Review)")
        lines.append("")
        for a in near_misses:
            s = signals.get(a["slug"], {})
            lines.append(f"### {a['name']}")
            lines.append(f"- Sources: {a['wiki_sources']} across {a['wiki_topics']} topics")
            lines.append(f"- Topics: {', '.join(s.get('topic_list', []))}")
            lines.append(f"- Confidence: {a.get('confidence', '?')}")
            lines.append(f"- Level: {a.get('level', '?')}")
            lines.append(f"- Style: {a.get('style', '?')}")
            lines.append(f"- Best Topics: {', '.join(a.get('best_topics') or [])}")
            lines.append(f"- Pairs With: {', '.join(a.get('pairs_with') or [])}")
            lines.append(f"- **Reasoning:** {a.get('reasoning', '')}")
            lines.append("")
            lines.append("  To promote, add to authors.md:")
            lines.append("  ```")
            lines.append(f"  - Canonical Educator: yes")
            lines.append(f"  - Level: {a.get('level', '?')}")
            lines.append(f"  - Best Topics: {', '.join(a.get('best_topics') or [])}")
            lines.append(f"  - Style: {a.get('style', '?')}")
            lines.append(f"  - Pairs With: {', '.join(a.get('pairs_with') or [])}")
            lines.append("  ```")
            lines.append("")

    if skips:
        lines.append("## Skipped")
        lines.append("")
        for a in skips:
            lines.append(f"- **{a['name']}** ({a['wiki_sources']} sources) — {a.get('reasoning', '')}")
        lines.append("")

    _REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nReport written to: {_REPORT_PATH.relative_to(_WIKI_DIR.parent.parent)}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

async def main():
    parser = argparse.ArgumentParser(description="Scan and promote authors to canonical educators")
    parser.add_argument("--dry-run", action="store_true", help="Scan only, no LLM calls")
    parser.add_argument("--apply", action="store_true", help="Auto-apply promotions to authors.md")
    parser.add_argument("--threshold", type=int, default=3, help="Min source count to consider")
    args = parser.parse_args()

    print("Scanning wiki for author signals...")
    signals = scan_author_signals()

    print(f"\nAll non-educator authors with source files: {len(signals)}")
    print(f"{'Name':<35s} {'Sources':>7s} {'Topics':>6s}")
    print("-" * 55)
    for slug, s in signals.items():
        marker = ""
        if s["sources"] >= _AUTO_PROMOTE_THRESHOLD["sources"] and s["topics"] >= _AUTO_PROMOTE_THRESHOLD["topics"]:
            marker = " ★ auto-promote candidate"
        elif s["sources"] >= _CONSIDERATION_THRESHOLD["sources"] or s["topics"] >= _CONSIDERATION_THRESHOLD["topics"]:
            marker = " ◆ consideration"
        print(f"  {s['name']:<33s} {s['sources']:>5d}   {s['topics']:>4d}{marker}")

    candidates = {
        slug: s for slug, s in signals.items()
        if s["sources"] >= args.threshold or s["topics"] >= _CONSIDERATION_THRESHOLD["topics"]
    }

    if not candidates:
        print(f"\nNo candidates above threshold ({args.threshold} sources). Done.")
        return

    print(f"\n{len(candidates)} candidates above threshold")

    if args.dry_run:
        print("Dry run — skipping LLM assessment.")
        return

    print("\nAssessing candidates with LLM...")
    assessments = []
    for slug, s in candidates.items():
        print(f"\n  Assessing: {s['name']} ({s['sources']} sources, {s['topics']} topics)")
        result = await assess_candidate(s)
        assessments.append(result)
        print(f"  → {result.get('recommendation', 'error')}"
              f" (confidence: {result.get('confidence', '?')})")

    promotes = [a for a in assessments if a["recommendation"] == "promote"]
    near_misses = [a for a in assessments if a["recommendation"] == "near_miss"]

    if args.apply and promotes:
        print(f"\nAuto-promoting {len(promotes)} authors...")
        for a in promotes:
            apply_promotion(a)

    write_report(assessments, signals)

    print(f"\nDone. {len(promotes)} promoted, {len(near_misses)} near-misses for review.")


if __name__ == "__main__":
    asyncio.run(main())
