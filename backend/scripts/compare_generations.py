#!/usr/bin/env python3
"""
Compare old vs new course generation: structural, grounding, and citation metrics.

Reads per-lesson JSON files from two experiment directories (old and new),
computes metrics side by side, and outputs a summary table + HTML report.

Usage:
    python -m scripts.compare_generations \
        --old content/experiments/intro-to-llms-old \
        --new content/experiments/intro-to-llms-new
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import urlparse

BACKEND = Path(__file__).resolve().parent.parent
WIKI_DIR = Path(os.environ.get("CONTENT_DIR", str(BACKEND.parent / "content"))).resolve() / "pedagogy-wiki"


# ── Shared utilities ─────────────────────────────────────────────────────

def _extract_urls(md_text: str) -> list[str]:
    return re.findall(r"https?://[^\s)>\]\"]+", md_text)


def _extract_markdown_links(md_text: str) -> list[tuple[str, str]]:
    return re.findall(r"\[([^\]]+)\]\((https?://[^)]+)\)", md_text)


def _word_count(md_text: str) -> int:
    cleaned = re.sub(r"```[\s\S]*?```", "", md_text)
    cleaned = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", cleaned)
    return len(cleaned.split())


def _extract_sections(md_text: str) -> list[str]:
    return re.findall(r"^## (.+)$", md_text, re.MULTILINE)


def _normalize_url(url: str) -> str:
    url = url.strip().rstrip("/").split("#")[0]
    parsed = urlparse(url)
    host = parsed.hostname or ""
    if host.startswith("www."):
        host = host[4:]
    return f"{parsed.scheme}://{host}{parsed.path}".rstrip("/")


def _build_wiki_url_index() -> dict[str, list[dict]]:
    topics_dir = WIKI_DIR / "resources" / "by-topic"
    if not topics_dir.is_dir():
        return {}
    index: dict[str, list[dict]] = {}
    for topic_dir in sorted(topics_dir.iterdir()):
        if not topic_dir.is_dir():
            continue
        for md_file in sorted(topic_dir.glob("*.md")):
            try:
                lines = md_file.read_text(errors="ignore").split("\n", 5)
                url = ""
                for line in lines[:5]:
                    if line.startswith("# Source:"):
                        url = line.replace("# Source:", "").strip()
                    elif line.startswith("# Transcript:"):
                        url = line.replace("# Transcript:", "").strip()
                if url:
                    norm = _normalize_url(url)
                    index.setdefault(norm, []).append({"topic": topic_dir.name, "file": md_file.name})
            except Exception:
                pass
    return index


# ── Per-lesson metrics ───────────────────────────────────────────────────

@dataclass
class LessonMetrics:
    slug: str
    title: str
    notes_words: int = 0
    kb_words: int = 0
    notes_sections: list[str] = field(default_factory=list)
    kb_sections: list[str] = field(default_factory=list)
    has_recommended_reading: bool = False
    has_key_sources: bool = False
    has_sources_header: bool = False
    inline_citations: int = 0
    total_urls: int = 0
    verified_urls: int = 0
    unverified_urls: int = 0
    sources_used_count: int = 0
    image_metadata_count: int = 0
    notes_image_refs: int = 0
    kb_image_refs: int = 0
    has_code_blocks: bool = False
    has_latex: bool = False
    educator_mentions: int = 0


def compute_metrics(lesson_data: dict, wiki_url_index: dict) -> LessonMetrics:
    m = LessonMetrics(slug=lesson_data.get("slug", ""), title=lesson_data.get("title", ""))

    notes = lesson_data.get("content", "")
    kb = lesson_data.get("reference_kb", "")

    m.notes_words = _word_count(notes)
    m.kb_words = _word_count(kb)
    m.notes_sections = _extract_sections(notes)
    m.kb_sections = _extract_sections(kb)
    m.has_recommended_reading = "## Recommended Reading" in notes
    m.has_key_sources = "## Key Sources" in kb
    m.has_sources_header = bool(re.search(r"\*\*Sources?:\*\*", notes))

    m.inline_citations = len(_extract_markdown_links(kb))

    all_urls = set(_extract_urls(notes + "\n" + kb))
    video_hosts = {"youtube.com", "youtu.be", "vimeo.com"}
    non_video = {_normalize_url(u) for u in all_urls
                 if not any(h in (urlparse(u).hostname or "") for h in video_hosts)}
    m.total_urls = len(non_video)
    m.verified_urls = sum(1 for u in non_video if u in wiki_url_index)
    m.unverified_urls = m.total_urls - m.verified_urls

    m.sources_used_count = len(lesson_data.get("sources_used", []) or [])
    m.image_metadata_count = len(lesson_data.get("image_metadata", []) or [])

    m.notes_image_refs = len(re.findall(r"!\[", notes))
    m.kb_image_refs = len(re.findall(r"!\[", kb))

    m.has_code_blocks = "```" in notes or "```" in kb
    m.has_latex = bool(re.search(r"\\\[|\\\(", notes + kb))

    educator_pattern = r"(?:As|According to)\s+[A-Z][a-z]+(?:\s+(?:et al\.|[A-Z][a-z]+))?"
    m.educator_mentions = len(re.findall(educator_pattern, notes + "\n" + kb))

    return m


# ── Loading ──────────────────────────────────────────────────────────────

def load_experiment(exp_dir: Path) -> list[dict]:
    lessons = []
    outline_path = exp_dir / "outline.json"
    if not outline_path.exists():
        outline_path = exp_dir / "checkpoints" / "stage2_outline.json"
    if not outline_path.exists():
        print(f"  [!] No outline found in {exp_dir}")
        return lessons

    outline = json.loads(outline_path.read_text())
    notes_dir = exp_dir / "notes"
    kb_dir = exp_dir / "reference-kb"

    for mod in outline.get("modules", []):
        for les in mod.get("lessons", []):
            slug = les["slug"]
            lesson_json = exp_dir / f"{slug}.json"
            if lesson_json.exists():
                data = json.loads(lesson_json.read_text())
            else:
                data = dict(les)
                notes_path = notes_dir / f"{slug}.md"
                if notes_path.exists():
                    data["content"] = notes_path.read_text()
                kb_path = kb_dir / f"{slug}.md"
                if kb_path.exists():
                    data["reference_kb"] = kb_path.read_text()
            lessons.append(data)
    return lessons


# ── Console report ───────────────────────────────────────────────────────

def print_comparison(old_metrics: list[LessonMetrics], new_metrics: list[LessonMetrics]):
    print()
    print("=" * 100)
    print("  WIKI-FIRST REGENERATION COMPARISON")
    print("=" * 100)

    header = f"  {'Lesson':<35} {'Notes(w)':>10} {'KB(w)':>10} {'Citations':>10} {'Verified':>10} {'Images':>8}"
    divider = f"  {'-'*35} {'-'*10} {'-'*10} {'-'*10} {'-'*10} {'-'*8}"

    print(f"\n  OLD PIPELINE:")
    print(header)
    print(divider)
    for m in old_metrics:
        grounding = f"{m.verified_urls}/{m.total_urls}" if m.total_urls else "0/0"
        print(f"  {m.title[:35]:<35} {m.notes_words:>10} {m.kb_words:>10} "
              f"{m.inline_citations:>10} {grounding:>10} {m.image_metadata_count:>8}")

    print(f"\n  NEW (WIKI-FIRST) PIPELINE:")
    print(header)
    print(divider)
    for m in new_metrics:
        grounding = f"{m.verified_urls}/{m.total_urls}" if m.total_urls else "0/0"
        print(f"  {m.title[:35]:<35} {m.notes_words:>10} {m.kb_words:>10} "
              f"{m.inline_citations:>10} {grounding:>10} {m.image_metadata_count:>8}")

    # Aggregated comparison
    print(f"\n  AGGREGATED COMPARISON:")
    print(f"  {'-'*60}")

    def avg(vals):
        return sum(vals) / len(vals) if vals else 0

    old_nw = avg([m.notes_words for m in old_metrics])
    new_nw = avg([m.notes_words for m in new_metrics])
    old_kw = avg([m.kb_words for m in old_metrics])
    new_kw = avg([m.kb_words for m in new_metrics])
    old_cit = avg([m.inline_citations for m in old_metrics])
    new_cit = avg([m.inline_citations for m in new_metrics])
    old_ver = sum(m.verified_urls for m in old_metrics)
    new_ver = sum(m.verified_urls for m in new_metrics)
    old_tot = sum(m.total_urls for m in old_metrics)
    new_tot = sum(m.total_urls for m in new_metrics)
    old_img = sum(m.image_metadata_count for m in old_metrics)
    new_img = sum(m.image_metadata_count for m in new_metrics)
    old_edu = avg([m.educator_mentions for m in old_metrics])
    new_edu = avg([m.educator_mentions for m in new_metrics])
    old_rec = sum(1 for m in old_metrics if m.has_recommended_reading)
    new_rec = sum(1 for m in new_metrics if m.has_recommended_reading)
    old_ks = sum(1 for m in old_metrics if m.has_key_sources)
    new_ks = sum(1 for m in new_metrics if m.has_key_sources)

    def delta(old, new, fmt=".0f"):
        d = new - old
        sign = "+" if d > 0 else ""
        return f"{sign}{d:{fmt}}"

    rows = [
        ("Avg notes words", f"{old_nw:.0f}", f"{new_nw:.0f}", delta(old_nw, new_nw)),
        ("Avg KB words", f"{old_kw:.0f}", f"{new_kw:.0f}", delta(old_kw, new_kw)),
        ("Avg inline citations (KB)", f"{old_cit:.0f}", f"{new_cit:.0f}", delta(old_cit, new_cit)),
        ("Total verified URLs", str(old_ver), str(new_ver), delta(old_ver, new_ver)),
        ("Total URLs", str(old_tot), str(new_tot), delta(old_tot, new_tot)),
        ("Grounding %", f"{old_ver/old_tot:.0%}" if old_tot else "n/a",
         f"{new_ver/new_tot:.0%}" if new_tot else "n/a", ""),
        ("Total images attached", str(old_img), str(new_img), delta(old_img, new_img)),
        ("Avg educator mentions", f"{old_edu:.1f}", f"{new_edu:.1f}", delta(old_edu, new_edu, ".1f")),
        ("Has Recommended Reading", f"{old_rec}/{len(old_metrics)}", f"{new_rec}/{len(new_metrics)}", ""),
        ("Has Key Sources (KB)", f"{old_ks}/{len(old_metrics)}", f"{new_ks}/{len(new_metrics)}", ""),
    ]

    print(f"  {'Metric':<30} {'Old':>12} {'New':>12} {'Delta':>10}")
    print(f"  {'-'*30} {'-'*12} {'-'*12} {'-'*10}")
    for name, old_v, new_v, d in rows:
        print(f"  {name:<30} {old_v:>12} {new_v:>12} {d:>10}")

    print("=" * 100)


# ── HTML report ──────────────────────────────────────────────────────────

def generate_html_report(
    old_metrics: list[LessonMetrics],
    new_metrics: list[LessonMetrics],
    old_lessons: list[dict],
    new_lessons: list[dict],
    output_path: Path,
):
    report = None

    if report is None:
        _generate_plain_html(old_metrics, new_metrics, old_lessons, new_lessons, output_path)
        return

    def avg(vals):
        return sum(vals) / len(vals) if vals else 0

    old_ver = sum(m.verified_urls for m in old_metrics)
    new_ver = sum(m.verified_urls for m in new_metrics)
    old_tot = sum(m.total_urls for m in old_metrics)
    new_tot = sum(m.total_urls for m in new_metrics)

    report.add_executive_summary(f"""
        Regenerated **{len(new_metrics)} lessons** from "Introduction to Large Language Models"
        using the wiki-first pipeline. Same outline, same concepts — only the generation method changed.

        **Key improvements:**
        - Grounding: **{old_ver}/{old_tot} ({old_ver/old_tot:.0%})** old → **{new_ver}/{new_tot} ({new_ver/new_tot:.0%})** new verified URLs
        - Avg KB inline citations: **{avg([m.inline_citations for m in old_metrics]):.0f}** → **{avg([m.inline_citations for m in new_metrics]):.0f}**
        - Images attached: **{sum(m.image_metadata_count for m in old_metrics)}** → **{sum(m.image_metadata_count for m in new_metrics)}**
        - Educator attributions: **{avg([m.educator_mentions for m in old_metrics]):.1f}** → **{avg([m.educator_mentions for m in new_metrics]):.1f}** per lesson
    """)

    # Aggregated metrics table
    table_md = "| Metric | Old | New | Delta |\n|--------|-----|-----|-------|\n"
    comparisons = [
        ("Avg notes words",
         f"{avg([m.notes_words for m in old_metrics]):.0f}",
         f"{avg([m.notes_words for m in new_metrics]):.0f}"),
        ("Avg KB words",
         f"{avg([m.kb_words for m in old_metrics]):.0f}",
         f"{avg([m.kb_words for m in new_metrics]):.0f}"),
        ("Avg inline citations",
         f"{avg([m.inline_citations for m in old_metrics]):.0f}",
         f"{avg([m.inline_citations for m in new_metrics]):.0f}"),
        ("Grounding %",
         f"{old_ver/old_tot:.0%}" if old_tot else "n/a",
         f"{new_ver/new_tot:.0%}" if new_tot else "n/a"),
        ("Total images",
         str(sum(m.image_metadata_count for m in old_metrics)),
         str(sum(m.image_metadata_count for m in new_metrics))),
        ("Avg educator mentions",
         f"{avg([m.educator_mentions for m in old_metrics]):.1f}",
         f"{avg([m.educator_mentions for m in new_metrics]):.1f}"),
    ]
    for name, old_v, new_v in comparisons:
        table_md += f"| {name} | {old_v} | {new_v} | |\n"

    report.add_section("Aggregated Metrics", table_md)

    # Per-lesson comparison
    per_lesson_md = "| Lesson | Notes (old→new) | KB (old→new) | Citations (old→new) | Grounding (old→new) |\n"
    per_lesson_md += "|--------|-----------------|--------------|---------------------|--------------------|\n"

    for om, nm in zip(old_metrics, new_metrics):
        og = f"{om.verified_urls}/{om.total_urls}" if om.total_urls else "0"
        ng = f"{nm.verified_urls}/{nm.total_urls}" if nm.total_urls else "0"
        per_lesson_md += (
            f"| {om.title[:40]} | {om.notes_words}→{nm.notes_words} | "
            f"{om.kb_words}→{nm.kb_words} | {om.inline_citations}→{nm.inline_citations} | "
            f"{og}→{ng} |\n"
        )

    report.add_section("Per-Lesson Comparison", per_lesson_md)

    # Side-by-side diffs for a few lessons
    for old_l, new_l, om, nm in zip(old_lessons[:3], new_lessons[:3], old_metrics[:3], new_metrics[:3]):
        old_rec = ""
        if "## Recommended Reading" in old_l.get("content", ""):
            old_rec = old_l["content"].split("## Recommended Reading")[-1][:500]
        new_rec = ""
        if "## Recommended Reading" in new_l.get("content", ""):
            new_rec = new_l["content"].split("## Recommended Reading")[-1][:500]

        diff_md = f"""**Notes:** {om.notes_words}w → {nm.notes_words}w | **KB:** {om.kb_words}w → {nm.kb_words}w
**Citations:** {om.inline_citations} → {nm.inline_citations} | **Grounding:** {om.verified_urls}/{om.total_urls} → {nm.verified_urls}/{nm.total_urls}

Old Recommended Reading:
```
{old_rec.strip() or '(none)'}
```

New Recommended Reading:
```
{new_rec.strip() or '(none)'}
```
"""
        report.add_section(f"Sample: {om.title[:50]}", diff_md)

    report.save(str(output_path))
    print(f"  HTML report saved to {output_path}")


def _generate_plain_html(old_metrics, new_metrics, old_lessons, new_lessons, output_path):
    """Generate a plain HTML comparison report."""

    def avg(vals):
        return sum(vals) / len(vals) if vals else 0

    old_ver = sum(m.verified_urls for m in old_metrics)
    new_ver = sum(m.verified_urls for m in new_metrics)
    old_tot = sum(m.total_urls for m in old_metrics)
    new_tot = sum(m.total_urls for m in new_metrics)

    rows = ""
    for om, nm in zip(old_metrics, new_metrics):
        og = f"{om.verified_urls}/{om.total_urls}" if om.total_urls else "0"
        ng = f"{nm.verified_urls}/{nm.total_urls}" if nm.total_urls else "0"
        rows += f"""<tr>
            <td>{om.title}</td>
            <td>{om.notes_words} → {nm.notes_words}</td>
            <td>{om.kb_words} → {nm.kb_words}</td>
            <td>{om.inline_citations} → {nm.inline_citations}</td>
            <td>{og} → {ng}</td>
            <td>{om.image_metadata_count} → {nm.image_metadata_count}</td>
        </tr>"""

    html = f"""<!DOCTYPE html>
<html><head><title>Wiki-First Comparison</title>
<style>body{{font-family:system-ui;max-width:1200px;margin:auto;padding:2em;background:#1a1a2e;color:#eee}}
table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #333;padding:8px;text-align:left}}
th{{background:#16213e}}h1{{color:#76b900}}</style></head>
<body>
<h1>Wiki-First Regeneration Comparison</h1>
<p>Grounding: <b>{old_ver}/{old_tot} ({old_ver/old_tot:.0%})</b> old →
<b>{new_ver}/{new_tot} ({new_ver/new_tot:.0%})</b> new</p>
<table><tr><th>Lesson</th><th>Notes</th><th>KB</th><th>Citations</th><th>Grounding</th><th>Images</th></tr>
{rows}</table></body></html>"""

    output_path.write_text(html)
    print(f"  HTML report saved to {output_path}")


# ── Main ─────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Compare old vs new course generation")
    parser.add_argument("--old", type=str, required=True, help="Old experiment directory")
    parser.add_argument("--new", type=str, required=True, help="New experiment directory")
    parser.add_argument("--html", type=str, default=None, help="Output HTML report path")
    args = parser.parse_args()

    old_dir = BACKEND / args.old if not Path(args.old).is_absolute() else Path(args.old)
    new_dir = BACKEND / args.new if not Path(args.new).is_absolute() else Path(args.new)

    print("\n  Building wiki URL index...")
    wiki_url_index = _build_wiki_url_index()
    print(f"  {len(wiki_url_index)} unique source URLs")

    print(f"  Loading old: {old_dir}")
    old_lessons = load_experiment(old_dir)
    print(f"  Loading new: {new_dir}")
    new_lessons = load_experiment(new_dir)

    if len(old_lessons) != len(new_lessons):
        print(f"  [!] Lesson count mismatch: old={len(old_lessons)}, new={len(new_lessons)}")

    matched = min(len(old_lessons), len(new_lessons))
    old_metrics = [compute_metrics(l, wiki_url_index) for l in old_lessons[:matched]]
    new_metrics = [compute_metrics(l, wiki_url_index) for l in new_lessons[:matched]]

    print_comparison(old_metrics, new_metrics)

    html_path = Path(args.html) if args.html else (new_dir / "comparison_report.html")
    generate_html_report(old_metrics, new_metrics, old_lessons, new_lessons, html_path)


if __name__ == "__main__":
    main()
