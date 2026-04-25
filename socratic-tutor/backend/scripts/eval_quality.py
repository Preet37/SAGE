#!/usr/bin/env python3
"""
Quality evaluation for pipeline output.

Three tiers:
  Tier 1 — Structural checks (fast, no LLM, always runs)
  Tier 2 — Grounding verification (checks note claims against wiki sources)
  Tier 3 — LLM-based rubric scoring (opt-in with --llm)

Usage:
    python -m scripts.eval_quality                          # Tier 1+2 only
    python -m scripts.eval_quality --llm                    # All tiers
    python -m scripts.eval_quality --lesson bahdanau*       # Single lesson
    python -m scripts.eval_quality --output-dir /some/path  # Custom output
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import re
import sys
from dataclasses import dataclass, field
from fnmatch import fnmatch
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

# ── Paths ────────────────────────────────────────────────────────────────
BACKEND = Path(__file__).resolve().parent.parent
OUTPUT = BACKEND / "content" / "pipeline-output"
CHECKPOINTS = OUTPUT / "checkpoints"
NOTES_DIR = OUTPUT / "notes"
KB_DIR = OUTPUT / "reference-kb"
WIKI_DIR = Path(os.environ.get("CONTENT_DIR", str(BACKEND.parent / "content"))).resolve() / "pedagogy-wiki"


# ── Data classes ─────────────────────────────────────────────────────────
@dataclass
class Check:
    name: str
    passed: bool
    detail: str = ""
    severity: str = "error"  # "error" | "warning" | "info"


@dataclass
class LessonEval:
    slug: str
    title: str
    notes_checks: list[Check] = field(default_factory=list)
    kb_checks: list[Check] = field(default_factory=list)
    grounding_checks: list[Check] = field(default_factory=list)
    image_checks: list[Check] = field(default_factory=list)
    citation_checks: list[Check] = field(default_factory=list)
    rubric_scores: dict[str, Any] = field(default_factory=dict)


@dataclass
class CourseEval:
    outline_checks: list[Check] = field(default_factory=list)
    lessons: list[LessonEval] = field(default_factory=list)
    summary: dict[str, int] = field(default_factory=dict)


# ── Tier 1: Structural checks ───────────────────────────────────────────
NOTES_REQUIRED_SECTIONS = ["Intro", "Summary", "Recommended Reading"]
KB_REQUIRED_SECTIONS = [
    "Key Facts & Definitions",
    "Technical Details",
    "How It Works",
    "Comparisons & Trade-offs",
    "Common Misconceptions",
    "Key Sources",
]

NOTES_WORD_RANGE = (250, 1500)
KB_WORD_RANGE = (800, 8000)


def _extract_sections(md_text: str) -> list[str]:
    """Return all ## headings from markdown."""
    return re.findall(r"^## (.+)$", md_text, re.MULTILINE)


def _word_count(md_text: str) -> int:
    cleaned = re.sub(r"```[\s\S]*?```", "", md_text)
    cleaned = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", cleaned)
    return len(cleaned.split())


def _extract_urls(md_text: str) -> list[str]:
    return re.findall(r"https?://[^\s)>\]\"]+", md_text)


def _has_latex(md_text: str) -> bool:
    return bool(re.search(r"\\\[.*?\\\]|\\\(.*?\\\)", md_text, re.DOTALL))


def _check_balanced_latex(md_text: str) -> bool:
    opens_block = len(re.findall(r"\\\[", md_text))
    closes_block = len(re.findall(r"\\\]", md_text))
    opens_inline = len(re.findall(r"\\\(", md_text))
    closes_inline = len(re.findall(r"\\\)", md_text))
    return opens_block == closes_block and opens_inline == closes_inline


def _check_code_blocks(md_text: str) -> bool:
    return md_text.count("```") % 2 == 0


def eval_notes_structural(slug: str, notes_text: str) -> list[Check]:
    checks = []
    sections = _extract_sections(notes_text)

    for req in NOTES_REQUIRED_SECTIONS:
        found = any(req.lower() in s.lower() for s in sections)
        if not found and req == "Intro":
            body = notes_text.split("---", 1)[-1] if "---" in notes_text else notes_text
            first_section = re.split(r"^## ", body, maxsplit=1, flags=re.MULTILINE)[0]
            has_inline_intro = len(first_section.strip().split()) >= 20
            found = has_inline_intro
            detail = "Inline intro (no ## Intro heading)" if found else "No intro content found"
        else:
            detail = f"Missing required section '## {req}'" if not found else ""
        checks.append(Check(
            f"section:{req}",
            found,
            detail,
            severity="warning" if not found and req == "Intro" else "error",
        ))

    wc = _word_count(notes_text)
    lo, hi = NOTES_WORD_RANGE
    in_range = lo <= wc <= hi
    checks.append(Check(
        "word_count",
        in_range,
        f"{wc} words (expected {lo}-{hi})",
        severity="warning" if not in_range else "info",
    ))

    has_sources = bool(re.search(r"\*\*Sources?:\*\*", notes_text))
    checks.append(Check("sources_header", has_sources, "Missing **Sources:** header" if not has_sources else ""))

    urls = _extract_urls(notes_text)
    valid_urls = all(urlparse(u).scheme in ("http", "https") for u in urls)
    checks.append(Check("valid_urls", valid_urls, f"{len(urls)} URLs found" if valid_urls else "Malformed URLs"))

    rec_section = notes_text.split("## Recommended Reading")[-1] if "## Recommended Reading" in notes_text else ""
    rec_links = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", rec_section)
    checks.append(Check(
        "recommended_reading_links",
        len(rec_links) >= 2,
        f"{len(rec_links)} links in Recommended Reading",
        severity="warning" if len(rec_links) < 2 else "info",
    ))

    if _has_latex(notes_text):
        balanced = _check_balanced_latex(notes_text)
        checks.append(Check("latex_balanced", balanced, "Unbalanced LaTeX delimiters" if not balanced else ""))

    code_ok = _check_code_blocks(notes_text)
    checks.append(Check("code_blocks", code_ok, "Unmatched ``` fences" if not code_ok else ""))

    dup_title = notes_text.count(f"# {slug.replace('-', ' ').title()}")
    has_dup_h1 = len(re.findall(r"^# .+$", notes_text, re.MULTILINE)) > 1
    checks.append(Check(
        "no_duplicate_h1",
        not has_dup_h1 or dup_title <= 1,
        "Duplicate H1 title" if has_dup_h1 else "",
        severity="warning",
    ))

    return checks


def eval_kb_structural(slug: str, kb_text: str) -> list[Check]:
    checks = []
    sections = _extract_sections(kb_text)

    for req in KB_REQUIRED_SECTIONS:
        found = any(req.lower() in s.lower() for s in sections)
        checks.append(Check(
            f"section:{req}",
            found,
            f"Missing required section '## {req}'" if not found else "",
        ))

    wc = _word_count(kb_text)
    lo, hi = KB_WORD_RANGE
    in_range = lo <= wc <= hi
    checks.append(Check(
        "word_count",
        in_range,
        f"{wc} words (expected {lo}-{hi})",
        severity="warning" if not in_range else "info",
    ))

    source_citations = re.findall(r"\[([^\]]+)\]\(https?://[^)]+\)", kb_text)
    checks.append(Check(
        "has_citations",
        len(source_citations) >= 3,
        f"{len(source_citations)} inline citations",
        severity="warning" if len(source_citations) < 3 else "info",
    ))

    key_sources_section = kb_text.split("## Key Sources")[-1] if "## Key Sources" in kb_text else ""
    ks_links = re.findall(r"\[([^\]]+)\]\(https?://[^)]+\)", key_sources_section)
    checks.append(Check(
        "key_sources_list",
        len(ks_links) >= 1,
        f"{len(ks_links)} sources listed" if ks_links else "Empty Key Sources section",
    ))

    code_ok = _check_code_blocks(kb_text)
    checks.append(Check("code_blocks", code_ok, "Unmatched ``` fences" if not code_ok else ""))

    return checks


# ── Tier 2: Grounding verification ──────────────────────────────────────
def eval_grounding(slug: str, notes_text: str, outline_lesson: dict, assessment_entry: dict | None) -> list[Check]:
    checks = []

    concepts = outline_lesson.get("concepts", [])
    notes_lower = notes_text.lower()
    found = sum(1 for c in concepts if c.lower() in notes_lower)
    ratio = found / len(concepts) if concepts else 1.0
    checks.append(Check(
        "concept_coverage",
        ratio >= 0.5,
        f"{found}/{len(concepts)} outline concepts mentioned ({ratio:.0%})",
        severity="warning" if ratio < 0.5 else "info",
    ))

    if assessment_entry:
        gaps = assessment_entry.get("research_topics", [])
        if gaps:
            gap_found = sum(1 for g in gaps if any(
                kw.lower() in notes_lower
                for kw in re.findall(r"\w{4,}", g)[:3]
            ))
            gap_ratio = gap_found / len(gaps) if gaps else 1.0
            checks.append(Check(
                "gap_addressed",
                gap_ratio >= 0.4,
                f"{gap_found}/{len(gaps)} research gaps addressed ({gap_ratio:.0%})",
                severity="warning" if gap_ratio < 0.4 else "info",
            ))

    sources_match = re.search(r"\*\*Sources?:\*\*\s*(.+?)(?:\n|$)", notes_text)
    if sources_match:
        source_urls = [u.strip() for u in sources_match.group(1).split(",")]
        rec_section = notes_text.split("## Recommended Reading")[-1] if "## Recommended Reading" in notes_text else ""
        rec_urls = set(_extract_urls(rec_section))
        source_set = set(source_urls)
        overlap = source_set & rec_urls
        checks.append(Check(
            "sources_in_reading",
            len(overlap) >= 1,
            f"{len(overlap)}/{len(source_set)} header sources appear in Recommended Reading",
            severity="warning" if len(overlap) < 1 else "info",
        ))

    return checks


# ── Tier 2b: Image checks ───────────────────────────────────────────────
def _load_topic_images(topic_slugs: list[str]) -> dict[str, list[dict]]:
    """Load images.json for each topic slug."""
    images: dict[str, list[dict]] = {}
    for slug in topic_slugs:
        json_path = WIKI_DIR / "resources" / "by-topic" / slug / "images" / "images.json"
        if json_path.exists():
            try:
                entries = json.loads(json_path.read_text())
                if entries:
                    images[slug] = entries
            except (json.JSONDecodeError, OSError):
                pass
    return images


def eval_images(
    slug: str, notes_text: str, kb_text: str,
    outline_lesson: dict, assessment_entry: dict | None,
) -> list[Check]:
    checks = []

    topic_slugs = []
    if assessment_entry:
        topic_slugs = assessment_entry.get("topics", [])
    if not topic_slugs:
        topic_slugs = assessment_entry.get("resolved_topics", []) if assessment_entry else []

    topic_images = _load_topic_images(topic_slugs)
    total_images = sum(len(v) for v in topic_images.values())

    if total_images == 0:
        return checks

    lesson_concepts = {c.lower() for c in outline_lesson.get("concepts", [])}
    relevant = []
    for imgs in topic_images.values():
        for img in imgs:
            img_concepts = {c.lower() for c in img.get("concepts", [])}
            if img_concepts & lesson_concepts:
                relevant.append(img)

    if not relevant:
        checks.append(Check(
            "images_available",
            True,
            f"{total_images} wiki images, 0 match lesson concepts",
            severity="info",
        ))
        return checks

    notes_has_images = bool(re.search(r"!\[", notes_text))
    checks.append(Check(
        "notes_image_refs",
        notes_has_images,
        f"{len(relevant)} relevant images available; {'included' if notes_has_images else 'not referenced'} in notes",
        severity="warning" if not notes_has_images else "info",
    ))

    kb_has_images = bool(re.search(r"!\[|Visual Aids", kb_text))
    checks.append(Check(
        "kb_image_refs",
        kb_has_images,
        f"{'Has' if kb_has_images else 'Missing'} image references or Visual Aids section in KB",
        severity="warning" if not kb_has_images else "info",
    ))

    img_refs = re.findall(r"!\[[^\]]*\]\(([^)]+)\)", notes_text + "\n" + kb_text)
    for ref_path in img_refs:
        if ref_path.startswith("/api/wiki-images/"):
            rel = ref_path.replace("/api/wiki-images/", "")
            disk_path = WIKI_DIR / "resources" / "by-topic" / rel
            exists = disk_path.exists()
            checks.append(Check(
                "image_file_exists",
                exists,
                f"{'Found' if exists else 'Missing'}: {ref_path}",
                severity="error" if not exists else "info",
            ))

    return checks


# ── Tier 2c: Citation validation ────────────────────────────────────────
def _normalize_url(url: str) -> str:
    """Normalize a URL for comparison."""
    url = url.strip().rstrip("/").split("#")[0]
    parsed = urlparse(url)
    host = parsed.hostname or ""
    if host.startswith("www."):
        host = host[4:]
    return f"{parsed.scheme}://{host}{parsed.path}".rstrip("/")


def build_wiki_url_index() -> dict[str, list[dict]]:
    """Scan wiki topic dirs for # Source: headers; returns {normalized_url: [entries]}."""
    topics_dir = WIKI_DIR / "resources" / "by-topic"
    if not topics_dir.is_dir():
        return {}
    index: dict[str, list[dict]] = {}
    for topic_dir in sorted(topics_dir.iterdir()):
        if not topic_dir.is_dir():
            continue
        slug = topic_dir.name
        for md_file in sorted(topic_dir.glob("*.md")):
            if md_file.name in ("curation-report.md",):
                continue
            try:
                text = md_file.read_text(errors="ignore")
                lines = text.split("\n", 5)
                url = ""
                for line in lines[:5]:
                    if line.startswith("# Source:"):
                        url = line.replace("# Source:", "").strip()
                    elif line.startswith("# Transcript:"):
                        url = line.replace("# Transcript:", "").strip()
                if url:
                    norm = _normalize_url(url)
                    index.setdefault(norm, []).append({"topic": slug, "file": md_file.name})
            except Exception:
                pass
    return index


def eval_citations(
    slug: str,
    notes_text: str,
    kb_text: str,
    wiki_url_index: dict[str, list[dict]],
    assessment_entry: dict | None,
) -> list[Check]:
    """Cross-check cited URLs in notes and KB against wiki ground truth."""
    checks = []

    all_urls = set(_extract_urls(kb_text)) | set(_extract_urls(notes_text))
    if not all_urls:
        checks.append(Check("citations_present", False, "No URLs found in notes or KB", severity="warning"))
        return checks

    normalized = {_normalize_url(u) for u in all_urls}
    video_hosts = {"youtube.com", "youtu.be", "vimeo.com"}
    non_video = {u for u in normalized if not any(h in (urlparse(u).hostname or "") for h in video_hosts)}

    verified = {u for u in non_video if u in wiki_url_index}
    unverified = non_video - verified

    checks.append(Check(
        "verified_citations",
        len(verified) >= 2,
        f"{len(verified)}/{len(non_video)} cited URLs found in wiki sources",
        severity="warning" if len(verified) < 2 else "info",
    ))

    if unverified:
        checks.append(Check(
            "unverified_citations",
            len(unverified) <= len(non_video) * 0.7,
            f"{len(unverified)} URLs not in wiki (may be external references or hallucinated)",
            severity="warning" if len(unverified) > len(non_video) * 0.7 else "info",
        ))

    topic_slugs = []
    if assessment_entry:
        topic_slugs = assessment_entry.get("topics", []) or assessment_entry.get("resolved_topics", [])
    if topic_slugs:
        topic_urls: set[str] = set()
        for norm_url, entries in wiki_url_index.items():
            if any(e["topic"] in topic_slugs for e in entries):
                topic_urls.add(norm_url)
        if topic_urls:
            cited_from_topic = verified & topic_urls
            coverage = len(cited_from_topic) / len(topic_urls)
            checks.append(Check(
                "wiki_source_coverage",
                coverage >= 0.05,
                f"{len(cited_from_topic)}/{len(topic_urls)} topic wiki sources cited ({coverage:.0%})",
                severity="info",
            ))

    return checks


# ── Tier 3: LLM rubric scoring ──────────────────────────────────────────
RUBRIC_PROMPT = """\
You are a senior instructional designer evaluating auto-generated educational content.

LESSON TITLE: {title}
LESSON SUMMARY (from outline): {summary}

--- STUDENT NOTES ---
{notes}

--- REFERENCE KB ---
{kb}

Score each dimension 1-5 (1=poor, 5=excellent). Return ONLY valid JSON:
{{
  "factual_accuracy": {{"score": <int>, "rationale": "<1 sentence>"}},
  "pedagogical_flow": {{"score": <int>, "rationale": "<1 sentence>"}},
  "concept_coverage": {{"score": <int>, "rationale": "<1 sentence>"}},
  "source_grounding": {{"score": <int>, "rationale": "<1 sentence>"}},
  "notes_kb_alignment": {{"score": <int>, "rationale": "<1 sentence>"}},
  "student_friendliness": {{"score": <int>, "rationale": "<1 sentence>"}}
}}

Scoring guide:
- factual_accuracy: Are claims correct? Any hallucinations?
- pedagogical_flow: Does the lesson build concepts in logical order?
- concept_coverage: Are the outline concepts adequately covered?
- source_grounding: Are claims traced to sources (especially in KB)?
- notes_kb_alignment: Do notes and KB complement each other without contradiction?
- student_friendliness: Is the notes text clear for the target audience?
"""


async def eval_rubric(lesson: dict, notes_text: str, kb_text: str) -> dict[str, Any]:
    """Score a lesson using an LLM judge. Returns rubric dict or empty on failure."""
    try:
        sys.path.insert(0, str(BACKEND))
        from app.services.course_generator import _call_llm_json
    except ImportError:
        print("  [!] Cannot import LLM client — skipping rubric scoring")
        return {}

    prompt = RUBRIC_PROMPT.format(
        title=lesson.get("title", ""),
        summary=lesson.get("summary", ""),
        notes=notes_text[:6000],
        kb=kb_text[:6000],
    )
    try:
        result = await _call_llm_json(prompt, max_tokens=1024)
        return result
    except Exception as e:
        print(f"  [!] LLM rubric failed: {e}")
        return {}


# ── Outline-level checks ────────────────────────────────────────────────
def eval_outline(outline: dict) -> list[Check]:
    checks = []
    modules = outline.get("modules", [])
    checks.append(Check("has_modules", len(modules) >= 2, f"{len(modules)} modules"))

    all_lessons = [l for m in modules for l in m.get("lessons", [])]
    checks.append(Check("has_lessons", len(all_lessons) >= 4, f"{len(all_lessons)} total lessons"))

    slugs = [l.get("slug", "") for l in all_lessons]
    checks.append(Check("unique_slugs", len(slugs) == len(set(slugs)), f"{len(set(slugs))}/{len(slugs)} unique slugs"))

    for les in all_lessons:
        has_concepts = len(les.get("concepts", [])) >= 2
        if not has_concepts:
            checks.append(Check(
                f"concepts:{les.get('slug', '?')}",
                False,
                f"Lesson '{les.get('title', '?')}' has <2 concepts",
                severity="warning",
            ))

    notes_on_disk = {f.stem for f in NOTES_DIR.glob("*.md")} if NOTES_DIR.exists() else set()
    slug_set = set(slugs)
    generated = slug_set & notes_on_disk
    missing = slug_set - notes_on_disk
    checks.append(Check(
        "all_lessons_generated",
        len(missing) == 0,
        f"{len(generated)}/{len(slug_set)} lessons have notes on disk"
        + (f" — missing: {', '.join(sorted(missing)[:5])}" if missing else ""),
    ))

    kb_on_disk = {f.stem for f in KB_DIR.glob("*.md")} if KB_DIR.exists() else set()
    kb_missing = slug_set - kb_on_disk
    checks.append(Check(
        "all_kbs_generated",
        len(kb_missing) == 0,
        f"{len(slug_set - kb_missing)}/{len(slug_set)} lessons have reference KBs"
        + (f" — missing: {', '.join(sorted(kb_missing)[:5])}" if kb_missing else ""),
    ))

    return checks


# ── Cross-lesson checks ─────────────────────────────────────────────────
def eval_cross_lesson(lesson_evals: list[LessonEval]) -> list[Check]:
    checks = []

    all_notes_urls: dict[str, list[str]] = {}
    for le in lesson_evals:
        notes_path = NOTES_DIR / f"{le.slug}.md"
        if notes_path.exists():
            urls = _extract_urls(notes_path.read_text())
            all_notes_urls[le.slug] = urls

    url_to_lessons: dict[str, list[str]] = {}
    for slug, urls in all_notes_urls.items():
        for u in urls:
            url_to_lessons.setdefault(u, []).append(slug)

    over_used = {u: ls for u, ls in url_to_lessons.items() if len(ls) > len(lesson_evals) * 0.7}
    checks.append(Check(
        "source_diversity",
        len(over_used) == 0,
        f"{len(over_used)} URLs appear in >70% of lessons" if over_used else "Good source diversity",
        severity="warning" if over_used else "info",
    ))

    wcs = []
    for le in lesson_evals:
        notes_path = NOTES_DIR / f"{le.slug}.md"
        if notes_path.exists():
            wcs.append(_word_count(notes_path.read_text()))
    if wcs:
        avg = sum(wcs) / len(wcs)
        cv = (max(wcs) - min(wcs)) / avg if avg else 0
        checks.append(Check(
            "word_count_consistency",
            cv < 1.5,
            f"Range {min(wcs)}-{max(wcs)} words, avg {avg:.0f} (CV ratio {cv:.2f})",
            severity="warning" if cv >= 1.5 else "info",
        ))

    return checks


# ── Reporter ─────────────────────────────────────────────────────────────
def print_report(course_eval: CourseEval) -> int:
    total = 0
    passed = 0
    warnings = 0
    failed = 0

    def _print_checks(checks: list[Check], indent: str = "  "):
        nonlocal total, passed, warnings, failed
        for c in checks:
            total += 1
            if c.passed:
                passed += 1
                icon = "[✓]"
            elif c.severity == "warning":
                warnings += 1
                icon = "[⚠]"
            else:
                failed += 1
                icon = "[✗]"
            detail = f" — {c.detail}" if c.detail else ""
            print(f"{indent}{icon} {c.name}{detail}")

    print()
    print("=" * 80)
    print("  PIPELINE OUTPUT QUALITY EVALUATION")
    print("=" * 80)

    if course_eval.outline_checks:
        print("\n  ── Outline ──")
        _print_checks(course_eval.outline_checks)

    for le in course_eval.lessons:
        print(f"\n  ── {le.title} ──")
        if le.notes_checks:
            print("    Notes:")
            _print_checks(le.notes_checks, "      ")
        if le.kb_checks:
            print("    Reference KB:")
            _print_checks(le.kb_checks, "      ")
        if le.grounding_checks:
            print("    Grounding:")
            _print_checks(le.grounding_checks, "      ")
        if le.image_checks:
            print("    Images:")
            _print_checks(le.image_checks, "      ")
        if le.citation_checks:
            print("    Citations:")
            _print_checks(le.citation_checks, "      ")
        if le.rubric_scores:
            print("    LLM Rubric:")
            for dim, val in le.rubric_scores.items():
                score = val.get("score", "?")
                rationale = val.get("rationale", "")
                icon = "✓" if isinstance(score, int) and score >= 4 else ("⚠" if isinstance(score, int) and score >= 3 else "✗")
                print(f"      [{icon}] {dim}: {score}/5 — {rationale}")

    cross = eval_cross_lesson(course_eval.lessons)
    if cross:
        print("\n  ── Cross-lesson ──")
        _print_checks(cross)

    print()
    print("=" * 80)
    print(f"  SUMMARY: {passed} passed, {warnings} warnings, {failed} failed (of {total} checks)")
    print("=" * 80)

    if course_eval.lessons and any(le.rubric_scores for le in course_eval.lessons):
        dims: dict[str, list[int]] = {}
        for le in course_eval.lessons:
            for dim, val in le.rubric_scores.items():
                if isinstance(val.get("score"), int):
                    dims.setdefault(dim, []).append(val["score"])
        if dims:
            print("\n  LLM Rubric Averages:")
            for dim, scores in sorted(dims.items()):
                avg = sum(scores) / len(scores)
                print(f"    {dim}: {avg:.1f}/5 (n={len(scores)})")
            overall = sum(sum(s) for s in dims.values()) / sum(len(s) for s in dims.values())
            print(f"    ── overall: {overall:.1f}/5 ──")
        print()

    return 1 if failed > 0 else 0


# ── Main ─────────────────────────────────────────────────────────────────
async def main():
    parser = argparse.ArgumentParser(description="Evaluate pipeline output quality")
    parser.add_argument("--llm", action="store_true", help="Run Tier 3 LLM rubric scoring")
    parser.add_argument("--lesson", type=str, default=None, help="Glob pattern to filter lessons (e.g. 'bahdanau*')")
    parser.add_argument("--output-dir", type=str, default=None, help="Custom pipeline output directory")
    args = parser.parse_args()

    global OUTPUT, CHECKPOINTS, NOTES_DIR, KB_DIR
    if args.output_dir:
        OUTPUT = Path(args.output_dir)
        CHECKPOINTS = OUTPUT / "checkpoints"
        NOTES_DIR = OUTPUT / "notes"
        KB_DIR = OUTPUT / "reference-kb"

    if not CHECKPOINTS.exists():
        print(f"[!] No checkpoints at {CHECKPOINTS} — run the pipeline first")
        sys.exit(1)

    outline_path = CHECKPOINTS / "stage2_outline.json"
    assessment_path = CHECKPOINTS / "stage3_assessment.json"

    outline = json.loads(outline_path.read_text()) if outline_path.exists() else {}
    assessment = json.loads(assessment_path.read_text()) if assessment_path.exists() else {}

    assessment_by_slug: dict[str, dict] = {}
    for entry in assessment.get("needs_research", []):
        slug = entry.get("lesson", {}).get("slug", "")
        if slug:
            assessment_by_slug[slug] = entry
    for entry in assessment.get("fully_covered", []):
        slug = entry.get("lesson", {}).get("slug", "")
        if slug:
            assessment_by_slug[slug] = entry

    course_eval = CourseEval()

    print("\n  Loading pipeline output...")
    wiki_url_index = build_wiki_url_index()
    print(f"  Wiki URL index: {len(wiki_url_index)} unique source URLs")
    course_eval.outline_checks = eval_outline(outline)

    all_lessons = [l for m in outline.get("modules", []) for l in m.get("lessons", [])]
    if args.lesson:
        all_lessons = [l for l in all_lessons if fnmatch(l.get("slug", ""), args.lesson)]
        print(f"  Filtered to {len(all_lessons)} lessons matching '{args.lesson}'")

    for lesson in all_lessons:
        slug = lesson.get("slug", "")
        title = lesson.get("title", slug)
        le = LessonEval(slug=slug, title=title)

        notes_path = NOTES_DIR / f"{slug}.md"
        kb_path = KB_DIR / f"{slug}.md"

        if notes_path.exists():
            notes_text = notes_path.read_text()
            le.notes_checks = eval_notes_structural(slug, notes_text)
            le.grounding_checks = eval_grounding(slug, notes_text, lesson, assessment_by_slug.get(slug))
        else:
            le.notes_checks = [Check("file_exists", False, f"Notes file not found: {notes_path}")]

        if kb_path.exists():
            kb_text = kb_path.read_text()
            le.kb_checks = eval_kb_structural(slug, kb_text)
        else:
            kb_text = ""
            le.kb_checks = [Check("file_exists", False, f"KB file not found: {kb_path}")]

        if notes_path.exists() and kb_path.exists():
            le.image_checks = eval_images(
                slug, notes_text, kb_text, lesson, assessment_by_slug.get(slug),
            )
            le.citation_checks = eval_citations(
                slug, notes_text, kb_text, wiki_url_index, assessment_by_slug.get(slug),
            )

        if args.llm and notes_path.exists() and kb_path.exists():
            print(f"  Scoring {title}...")
            le.rubric_scores = await eval_rubric(lesson, notes_text, kb_text)

        course_eval.lessons.append(le)

    exit_code = print_report(course_eval)
    sys.exit(exit_code)


if __name__ == "__main__":
    asyncio.run(main())
