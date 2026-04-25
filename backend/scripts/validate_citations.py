#!/usr/bin/env python3
"""
Offline citation validation: cross-checks URLs in generated lesson content
against the wiki's ground-truth source files.

For each lesson, extracts all cited URLs from:
  - sources_used (JSON array from generation)
  - reference_kb (inline [Title](url) citations)
  - student notes (## Recommended Reading + **Sources:** header)

Then checks which URLs actually exist in the wiki as downloaded sources
(# Source: headers in by-topic/<slug>/*.md files).

Usage:
    python -m scripts.validate_citations                        # All courses
    python -m scripts.validate_citations --course intro-to-llms # One course
    python -m scripts.validate_citations --pipeline-output      # Pipeline output dir
    python -m scripts.validate_citations --verbose              # Show per-lesson detail
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
CONTENT_DIR = Path(os.environ.get("CONTENT_DIR", str(BACKEND.parent / "content"))).resolve()
WIKI_DIR = CONTENT_DIR / "pedagogy-wiki"
PIPELINE_OUTPUT = BACKEND / "content" / "pipeline-output"


# ── URL normalization ────────────────────────────────────────────────────

def _normalize_url(url: str) -> str:
    """Normalize a URL for comparison: strip trailing slash, fragment, www."""
    url = url.strip().rstrip("/").split("#")[0]
    parsed = urlparse(url)
    host = parsed.hostname or ""
    if host.startswith("www."):
        host = host[4:]
    normalized = f"{parsed.scheme}://{host}{parsed.path}".rstrip("/")
    return normalized


# ── Ground truth: scan all wiki source files ────────────────────────────

def build_wiki_url_index() -> dict[str, list[dict]]:
    """Scan all wiki topic directories and build URL -> source file mapping.

    Returns: {normalized_url: [{"topic": slug, "file": filename, "title": str, "url": raw_url}, ...]}
    """
    topics_dir = WIKI_DIR / "resources" / "by-topic"
    if not topics_dir.is_dir():
        return {}

    index: dict[str, list[dict]] = {}
    for topic_dir in sorted(topics_dir.iterdir()):
        if not topic_dir.is_dir():
            continue
        slug = topic_dir.name
        for md_file in sorted(topic_dir.glob("*.md")):
            if md_file.name in ("curation-report.md", "proposals.json"):
                continue
            try:
                text = md_file.read_text(errors="ignore")
                lines = text.split("\n", 5)
                url = ""
                title = ""
                for line in lines[:5]:
                    if line.startswith("# Source:"):
                        url = line.replace("# Source:", "").strip()
                    elif line.startswith("# Transcript:"):
                        url = line.replace("# Transcript:", "").strip()
                    elif line.startswith("# Title:"):
                        title = line.replace("# Title:", "").strip()
                if url:
                    norm = _normalize_url(url)
                    entry = {
                        "topic": slug,
                        "file": md_file.name,
                        "title": title or md_file.stem,
                        "url": url,
                    }
                    index.setdefault(norm, []).append(entry)
            except Exception:
                pass
    return index


def build_topic_url_sets(url_index: dict[str, list[dict]]) -> dict[str, set[str]]:
    """Build per-topic sets of normalized URLs for coverage checks."""
    topic_urls: dict[str, set[str]] = {}
    for norm_url, entries in url_index.items():
        for entry in entries:
            topic_urls.setdefault(entry["topic"], set()).add(norm_url)
    return topic_urls


# ── URL extraction from markdown ────────────────────────────────────────

def extract_urls(md_text: str) -> list[str]:
    """Extract all HTTP(S) URLs from markdown text."""
    return re.findall(r"https?://[^\s)>\]\"]+", md_text)


def extract_markdown_link_urls(md_text: str) -> list[tuple[str, str]]:
    """Extract (title, url) pairs from markdown links."""
    return re.findall(r"\[([^\]]+)\]\((https?://[^)]+)\)", md_text)


# ── Lesson data loading ────────────────────────────────────────────────

@dataclass
class LessonData:
    slug: str
    title: str
    topics: list[str] = field(default_factory=list)
    sources_used: list[str] = field(default_factory=list)
    notes_text: str = ""
    kb_text: str = ""


def load_course_lessons(course_dir: Path) -> list[LessonData]:
    """Load lessons from a course.json file."""
    course_json = course_dir / "course.json"
    if not course_json.exists():
        return []

    data = json.loads(course_json.read_text())
    enrichment_dir = course_dir / "enrichment"
    lessons = []

    for mod in data.get("modules", []):
        for les in mod.get("lessons", []):
            slug = les.get("slug", "")
            ld = LessonData(
                slug=slug,
                title=les.get("title", slug),
                notes_text=les.get("content", ""),
                sources_used=les.get("sources_used", []) or [],
            )
            kb_path = enrichment_dir / f"{slug}_reference_kb.md"
            if kb_path.exists():
                ld.kb_text = kb_path.read_text()
            elif les.get("reference_kb"):
                ld.kb_text = les["reference_kb"]

            lessons.append(ld)

    return lessons


def load_pipeline_lessons(output_dir: Path) -> list[LessonData]:
    """Load lessons from pipeline output (notes/ + reference-kb/ + checkpoints/)."""
    notes_dir = output_dir / "notes"
    kb_dir = output_dir / "reference-kb"
    checkpoints = output_dir / "checkpoints"

    outline_path = checkpoints / "stage2_outline.json"
    assessment_path = checkpoints / "stage3_assessment.json"

    outline = json.loads(outline_path.read_text()) if outline_path.exists() else {}
    assessment = json.loads(assessment_path.read_text()) if assessment_path.exists() else {}

    topic_map: dict[str, list[str]] = {}
    for entry in assessment.get("needs_research", []) + assessment.get("fully_covered", []):
        slug = entry.get("lesson", {}).get("slug", "")
        if slug:
            topic_map[slug] = entry.get("topics", []) or entry.get("resolved_topics", [])

    lessons = []
    all_lessons = [l for m in outline.get("modules", []) for l in m.get("lessons", [])]
    for les in all_lessons:
        slug = les.get("slug", "")
        ld = LessonData(
            slug=slug,
            title=les.get("title", slug),
            topics=topic_map.get(slug, []),
        )
        notes_path = notes_dir / f"{slug}.md"
        if notes_path.exists():
            ld.notes_text = notes_path.read_text()
        kb_path = kb_dir / f"{slug}.md"
        if kb_path.exists():
            ld.kb_text = kb_path.read_text()
        lessons.append(ld)

    return lessons


# ── Validation logic ───────────────────────────────────────────────────

@dataclass
class CitationReport:
    slug: str
    title: str
    verified: list[dict] = field(default_factory=list)
    unverified: list[dict] = field(default_factory=list)
    topic_coverage: float = 0.0
    total_wiki_sources: int = 0
    cited_wiki_sources: int = 0


def validate_lesson(
    lesson: LessonData,
    url_index: dict[str, list[dict]],
    topic_url_sets: dict[str, set[str]],
) -> CitationReport:
    """Validate all citations in a single lesson."""
    report = CitationReport(slug=lesson.slug, title=lesson.title)

    all_urls: dict[str, str] = {}

    for url in lesson.sources_used:
        raw = url["url"] if isinstance(url, dict) else url
        all_urls[_normalize_url(raw)] = "sources_used"

    if lesson.kb_text:
        for url in extract_urls(lesson.kb_text):
            norm = _normalize_url(url)
            if norm not in all_urls:
                all_urls[norm] = "reference_kb"

    if lesson.notes_text:
        for url in extract_urls(lesson.notes_text):
            norm = _normalize_url(url)
            if norm not in all_urls:
                all_urls[norm] = "notes"

    for norm_url, source_location in all_urls.items():
        wiki_entries = url_index.get(norm_url, [])
        if wiki_entries:
            report.verified.append({
                "url": norm_url,
                "found_in": source_location,
                "wiki_topics": [e["topic"] for e in wiki_entries],
                "wiki_files": [e["file"] for e in wiki_entries],
                "title": wiki_entries[0].get("title", ""),
            })
        else:
            parsed = urlparse(norm_url)
            host = parsed.hostname or ""
            is_video = "youtube.com" in host or "youtu.be" in host or "vimeo.com" in host
            report.unverified.append({
                "url": norm_url,
                "found_in": source_location,
                "type": "video" if is_video else "external",
            })

    if lesson.topics:
        all_topic_urls: set[str] = set()
        for topic in lesson.topics:
            all_topic_urls |= topic_url_sets.get(topic, set())
        report.total_wiki_sources = len(all_topic_urls)
        cited_norm = set(all_urls.keys())
        report.cited_wiki_sources = len(cited_norm & all_topic_urls)
        report.topic_coverage = (
            report.cited_wiki_sources / report.total_wiki_sources
            if report.total_wiki_sources > 0 else 1.0
        )

    return report


# ── Reporting ──────────────────────────────────────────────────────────

def print_summary(reports: list[CitationReport], verbose: bool = False) -> int:
    print()
    print("=" * 80)
    print("  CITATION VALIDATION REPORT")
    print("=" * 80)

    total_verified = 0
    total_unverified = 0
    total_lessons = len(reports)
    lessons_with_issues = 0

    for r in reports:
        total_verified += len(r.verified)
        total_unverified += len(r.unverified)

        has_issues = any(
            u["type"] != "video" and u["found_in"] == "sources_used"
            for u in r.unverified
        )
        if has_issues:
            lessons_with_issues += 1

        if verbose:
            print(f"\n  -- {r.title} ({r.slug}) --")
            print(f"     Verified: {len(r.verified)}  |  Unverified: {len(r.unverified)}")
            if r.total_wiki_sources > 0:
                print(f"     Wiki coverage: {r.cited_wiki_sources}/{r.total_wiki_sources} "
                      f"({r.topic_coverage:.0%})")

            if r.verified and verbose:
                for v in r.verified[:5]:
                    print(f"       [ok] {v['url'][:70]}")
                    print(f"            wiki: {', '.join(v['wiki_files'][:2])}")
                if len(r.verified) > 5:
                    print(f"       ... and {len(r.verified) - 5} more verified")

            for u in r.unverified:
                tag = "video" if u["type"] == "video" else "EXTERNAL"
                print(f"       [{tag}] {u['url'][:70]}  (from {u['found_in']})")

    # Summary table
    print()
    print("-" * 80)
    print(f"  Lessons analyzed:        {total_lessons}")
    print(f"  Total verified URLs:     {total_verified}")
    print(f"  Total unverified URLs:   {total_unverified}")
    print(f"  Lessons with unverified sources_used: {lessons_with_issues}")

    if any(r.total_wiki_sources > 0 for r in reports):
        coverages = [r.topic_coverage for r in reports if r.total_wiki_sources > 0]
        avg_coverage = sum(coverages) / len(coverages) if coverages else 0
        print(f"  Average wiki source coverage: {avg_coverage:.0%}")

    print("=" * 80)

    # Per-lesson compact table
    print(f"\n  {'Lesson':<50} {'Verified':>8} {'Unverif':>8} {'Coverage':>9}")
    print(f"  {'-'*50} {'-'*8} {'-'*8} {'-'*9}")
    for r in reports:
        cov = f"{r.topic_coverage:.0%}" if r.total_wiki_sources > 0 else "n/a"
        print(f"  {r.title[:50]:<50} {len(r.verified):>8} {len(r.unverified):>8} {cov:>9}")

    print()
    return 1 if lessons_with_issues > 0 else 0


def export_json(reports: list[CitationReport], output_path: Path) -> None:
    """Export validation results as JSON for downstream use."""
    data = []
    for r in reports:
        data.append({
            "slug": r.slug,
            "title": r.title,
            "verified_count": len(r.verified),
            "unverified_count": len(r.unverified),
            "topic_coverage": round(r.topic_coverage, 3),
            "total_wiki_sources": r.total_wiki_sources,
            "cited_wiki_sources": r.cited_wiki_sources,
            "verified": r.verified,
            "unverified": r.unverified,
        })
    output_path.write_text(json.dumps(data, indent=2))
    print(f"  Exported detailed results to {output_path}")


# ── Main ───────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Validate citations against wiki sources")
    parser.add_argument("--course", type=str, default=None,
                        help="Course slug to validate (e.g. intro-to-llms)")
    parser.add_argument("--pipeline-output", action="store_true",
                        help="Validate pipeline output directory instead of course.json")
    parser.add_argument("--output-dir", type=str, default=None,
                        help="Custom pipeline output directory")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Show per-lesson citation details")
    parser.add_argument("--export", type=str, default=None,
                        help="Export results as JSON to this path")
    args = parser.parse_args()

    print("\n  Building wiki URL index...")
    url_index = build_wiki_url_index()
    topic_url_sets = build_topic_url_sets(url_index)
    total_sources = sum(len(v) for v in url_index.values())
    print(f"  Found {len(url_index)} unique source URLs across {len(topic_url_sets)} topics "
          f"({total_sources} total entries including cross-topic duplicates)")

    lessons: list[LessonData] = []

    if args.pipeline_output:
        output_dir = Path(args.output_dir) if args.output_dir else PIPELINE_OUTPUT
        print(f"  Loading from pipeline output: {output_dir}")
        lessons = load_pipeline_lessons(output_dir)
    elif args.course:
        course_dir = CONTENT_DIR / args.course
        if not course_dir.exists():
            print(f"  [!] Course directory not found: {course_dir}")
            sys.exit(1)
        print(f"  Loading course: {args.course}")
        lessons = load_course_lessons(course_dir)
    else:
        for course_dir in sorted(CONTENT_DIR.iterdir()):
            course_json = course_dir / "course.json"
            if course_json.exists():
                print(f"  Loading course: {course_dir.name}")
                lessons.extend(load_course_lessons(course_dir))

    if not lessons:
        print("  [!] No lessons found")
        sys.exit(1)

    print(f"  Validating {len(lessons)} lessons...\n")

    reports = []
    for lesson in lessons:
        report = validate_lesson(lesson, url_index, topic_url_sets)
        reports.append(report)

    exit_code = print_summary(reports, verbose=args.verbose)

    if args.export:
        export_json(reports, Path(args.export))

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
