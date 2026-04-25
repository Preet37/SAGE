#!/usr/bin/env python3
"""
Regenerate all lessons in a course using the wiki-first pipeline, then
update course.json and optionally seed the database.

Reads the existing course.json for its outline (module/lesson structure),
regenerates each lesson's student notes + reference KB via
generate_lesson_bundle with full pedagogy + reference track wiki context,
merges results back into course.json, writes enrichment KB files, and
optionally runs seed.py.

With --enrich, first runs assess_wiki_coverage + enrichment (search,
curate, download) for any lessons with thin or missing wiki coverage
before regenerating content.

Usage:
    cd backend && python -m scripts.regenerate_and_publish ml-engineering-foundations
    cd backend && python -m scripts.regenerate_and_publish --all
    cd backend && python -m scripts.regenerate_and_publish ml-engineering-foundations --enrich
    cd backend && python -m scripts.regenerate_and_publish ml-engineering-foundations --dry-run
    cd backend && python -m scripts.regenerate_and_publish ml-engineering-foundations --lesson "word-*"
    cd backend && python -m scripts.regenerate_and_publish ml-engineering-foundations --no-seed
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import shutil
import subprocess
import sys
import time
from fnmatch import fnmatch
from pathlib import Path

BACKEND = Path(__file__).resolve().parent.parent
ROOT = BACKEND.parent
CONTENT_DIR = Path(os.environ.get("CONTENT_DIR", str(ROOT / "content"))).resolve()
sys.path.insert(0, str(BACKEND))

from app.services.course_generator import (
    ensure_wiki_coverage,
    generate_lesson_bundle,
    load_wiki_context,
    resolve_topics_llm,
)

def _discover_courses() -> list[str]:
    """Discover course slugs from content directory."""
    return sorted(
        p.parent.name for p in CONTENT_DIR.glob("*/course.json")
        if not p.parent.name.startswith("private-")
    )

COURSE_SLUGS = _discover_courses()


def load_course(slug: str) -> dict:
    path = CONTENT_DIR / slug / "course.json"
    if not path.exists():
        print(f"[!] No course.json found at {path}")
        sys.exit(1)
    return json.loads(path.read_text())


def backup_course(slug: str) -> Path:
    src = CONTENT_DIR / slug / "course.json"
    dst = CONTENT_DIR / slug / "course.json.bak"
    shutil.copy2(src, dst)
    return dst


async def regenerate_course(
    slug: str,
    lesson_filter: str | None = None,
    dry_run: bool = False,
    enrich: bool = False,
) -> dict[str, dict]:
    """Regenerate lessons and return {slug: lesson_out} for successful ones."""
    course = load_course(slug)
    all_lessons = []
    for mod in course["modules"]:
        for les in mod["lessons"]:
            all_lessons.append(les)

    if lesson_filter:
        all_lessons = [l for l in all_lessons if fnmatch(l["slug"], lesson_filter)]
        print(f"  Filtered to {len(all_lessons)} lessons matching '{lesson_filter}'")

    print(f"\n{'='*60}")
    print(f"  Course: {course['title']} ({slug})")
    print(f"  Lessons: {len(all_lessons)}")
    if enrich:
        print(f"  Mode: ENRICH (will assess + enrich wiki before generating)")
    if dry_run:
        print(f"  Mode: DRY RUN (will not update course.json)")
    print(f"{'='*60}\n")

    # --- Enrichment phase (optional) ---
    assessment_map: dict[str, dict] = {}
    if enrich:
        print("  Phase 1: Assessing wiki coverage + enriching gaps...\n")
        assessment = await ensure_wiki_coverage(
            all_lessons,
            course_description=course.get("description", ""),
            enrich=True,
        )
        for bucket in ("fully_covered", "needs_research"):
            for entry in assessment.get(bucket, []):
                les_slug = entry["lesson"].get("slug", "")
                if les_slug:
                    assessment_map[les_slug] = entry
        fc = len(assessment.get("fully_covered", []))
        nr = len(assessment.get("needs_research", []))
        nm = len(assessment.get("no_match", []))
        print(f"\n  Coverage: {fc} fully covered, {nr} enriched, {nm} bootstrapped")
        print(f"\n  Phase 2: Generating content from enriched wiki...\n")

    # --- Generation phase ---
    results: dict[str, dict] = {}
    total_start = time.time()

    for i, lesson in enumerate(all_lessons, 1):
        lesson_slug = lesson["slug"]
        title = lesson["title"]
        concepts = lesson.get("concepts", [])

        print(f"  [{i}/{len(all_lessons)}] {title} ({lesson_slug})")
        start = time.time()

        entry = assessment_map.get(lesson_slug)
        if entry and entry.get("resolved_topics"):
            topic_slugs = entry["resolved_topics"]
            if isinstance(topic_slugs, set):
                topic_slugs = topic_slugs
        else:
            resolved = await resolve_topics_llm(
                concepts, lesson_title=title,
                lesson_summary=lesson.get("summary", ""),
            )
            topic_slugs = resolved["topic_slugs"]

        print(f"    Topics: {sorted(topic_slugs)}")

        wiki_ctx = load_wiki_context(concepts, topic_slugs=topic_slugs)
        ref_ctx = load_wiki_context(concepts, topic_slugs=topic_slugs, track="reference")
        source_count = sum(len(v) for v in wiki_ctx.get("source_content", {}).values())
        ref_count = sum(len(v) for v in ref_ctx.get("source_content", {}).values())
        image_count = sum(len(v) for v in wiki_ctx.get("images", {}).values())
        print(f"    Wiki: {source_count} ped + {ref_count} ref sources, {image_count} images")

        ref_kwarg = ref_ctx if ref_ctx.get("source_content") else None

        try:
            bundle = await generate_lesson_bundle(lesson, wiki_ctx, reference_ctx=ref_kwarg)
        except Exception as e:
            print(f"    [!] FAILED: {e}")
            results[lesson_slug] = {"error": str(e)}
            continue

        content_data = bundle.get("content", {})
        kb_text = bundle.get("reference_kb", "")
        wiki_meta = bundle.get("wiki_meta", {})
        lesson_images = bundle.get("image_metadata", [])

        notes_text = content_data.get("content", "")
        notes_wc = len(notes_text.split())
        kb_wc = len(kb_text.split())

        lesson_out = {
            "content": notes_text,
            "summary": content_data.get("summary", lesson.get("summary", "")),
            "concepts": content_data.get("concepts", concepts),
            "reference_kb": kb_text,
            "sources_used": content_data.get("sources_used", []),
            "image_metadata": lesson_images,
            "youtube_id": content_data.get("youtube_id") or wiki_meta.get("youtube_id"),
            "video_title": content_data.get("video_title") or wiki_meta.get("video_title"),
        }

        results[lesson_slug] = lesson_out
        elapsed = time.time() - start
        print(f"    Done: {notes_wc}w notes, {kb_wc}w KB, "
              f"{len(lesson_out['sources_used'])} sources, "
              f"{len(lesson_images)} images ({elapsed:.1f}s)")

    total_elapsed = time.time() - total_start
    successful = sum(1 for v in results.values() if "error" not in v)
    failed = sum(1 for v in results.values() if "error" in v)
    print(f"\n  Regeneration: {successful} OK, {failed} failed, {total_elapsed:.0f}s total")

    if successful > 0:
        avg_notes = sum(
            len(v.get("content", "").split())
            for v in results.values() if "error" not in v
        ) / successful
        avg_kb = sum(
            len(v.get("reference_kb", "").split())
            for v in results.values() if "error" not in v
        ) / successful
        print(f"  Averages: {avg_notes:.0f}w notes, {avg_kb:.0f}w KB")

    return results


def merge_into_course(slug: str, results: dict[str, dict]) -> dict:
    """Merge regenerated lesson data back into course.json structure."""
    course = load_course(slug)
    merged = 0

    for mod in course["modules"]:
        for lesson in mod["lessons"]:
            regen = results.get(lesson["slug"])
            if not regen or "error" in regen:
                continue

            lesson["content"] = regen["content"]
            lesson["summary"] = regen["summary"]
            lesson["concepts"] = regen["concepts"]
            lesson["sources_used"] = regen["sources_used"]
            lesson["image_metadata"] = regen["image_metadata"]

            if regen.get("youtube_id"):
                lesson["youtube_id"] = regen["youtube_id"]
            if regen.get("video_title"):
                lesson["video_title"] = regen["video_title"]

            merged += 1

    print(f"  Merged {merged} lessons into course.json")
    return course


def write_enrichment_kbs(slug: str, results: dict[str, dict]) -> int:
    """Write reference KB markdown files to the enrichment directory."""
    enrichment_dir = CONTENT_DIR / slug / "enrichment"
    enrichment_dir.mkdir(exist_ok=True)
    written = 0

    for lesson_slug, data in results.items():
        if "error" in data:
            continue
        kb = data.get("reference_kb", "")
        if not kb:
            continue
        kb_path = enrichment_dir / f"{lesson_slug}_reference_kb.md"
        kb_path.write_text(kb)
        written += 1

    print(f"  Wrote {written} enrichment KB files to {enrichment_dir.relative_to(ROOT)}")
    return written


def save_course(slug: str, course: dict) -> None:
    path = CONTENT_DIR / slug / "course.json"
    path.write_text(json.dumps(course, indent=2, ensure_ascii=False) + "\n")
    print(f"  Saved {path.relative_to(ROOT)}")


def run_seed() -> None:
    print("\n  Running seed.py...")
    result = subprocess.run(
        [sys.executable, "seed.py"],
        cwd=str(BACKEND),
        capture_output=True,
        text=True,
    )
    print(result.stdout)
    if result.returncode != 0:
        print(f"  [!] seed.py failed:\n{result.stderr}")


async def process_course(
    slug: str,
    lesson_filter: str | None = None,
    dry_run: bool = False,
    enrich: bool = False,
) -> dict[str, dict]:
    results = await regenerate_course(slug, lesson_filter, dry_run, enrich)

    successful = {k: v for k, v in results.items() if "error" not in v}
    if not successful:
        print(f"\n  No lessons regenerated successfully for {slug} — skipping merge.")
        return results

    if not dry_run:
        backup_course(slug)
        course = merge_into_course(slug, results)
        save_course(slug, course)

    write_enrichment_kbs(slug, results)
    return results


async def main_async(args: argparse.Namespace) -> None:
    available = _discover_courses()
    if args.all:
        slugs = available
    else:
        slugs = [args.course]

    for slug in slugs:
        course_json = CONTENT_DIR / slug / "course.json"
        if not course_json.exists():
            print(f"[!] No course.json found for: {slug}")
            print(f"    Available: {', '.join(available)}")
            sys.exit(1)

    all_results = {}
    for slug in slugs:
        results = await process_course(slug, args.lesson, args.dry_run, args.enrich)
        all_results[slug] = results

    if not args.dry_run and not args.no_seed:
        run_seed()

    total_ok = sum(
        1 for r in all_results.values()
        for v in r.values() if "error" not in v
    )
    total_fail = sum(
        1 for r in all_results.values()
        for v in r.values() if "error" in v
    )
    print(f"\n{'='*60}")
    print(f"  All done: {total_ok} lessons regenerated, {total_fail} failed")
    if args.dry_run:
        print(f"  (dry run — no course.json files were updated)")
    print(f"{'='*60}")


def main():
    parser = argparse.ArgumentParser(
        description="Regenerate course lessons with wiki-first pipeline and update course.json"
    )
    parser.add_argument("course", nargs="?", default=None,
                        help="Course slug (discovered from content directory)")
    parser.add_argument("--all", action="store_true",
                        help="Regenerate all courses")
    parser.add_argument("--enrich", action="store_true",
                        help="Assess wiki coverage and enrich gaps before generating")
    parser.add_argument("--lesson", type=str, default=None,
                        help="Glob pattern to filter lessons (e.g. 'word-*')")
    parser.add_argument("--dry-run", action="store_true",
                        help="Regenerate but don't update course.json")
    parser.add_argument("--no-seed", action="store_true",
                        help="Skip running seed.py after updating")
    args = parser.parse_args()

    if not args.course and not args.all:
        parser.error("Provide a course slug or use --all")

    asyncio.run(main_async(args))


if __name__ == "__main__":
    main()
