#!/usr/bin/env python3
"""
Regenerate a course using the wiki-first pipeline, keeping the same outline.

Takes an existing outline (from a baseline experiment directory or course.json)
and regenerates each lesson's notes + reference KB using generate_lesson_bundle
with full wiki context. Saves output alongside the baseline for comparison.

Usage:
    python -m scripts.regenerate_course --baseline content/experiments/intro-to-llms-old
    python -m scripts.regenerate_course --baseline content/experiments/intro-to-llms-old --lesson self-attention
"""
from __future__ import annotations

import argparse
import asyncio
import json
import sys
import time
from fnmatch import fnmatch
from pathlib import Path

BACKEND = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BACKEND))

from app.services.course_generator import (
    generate_lesson_bundle,
    load_wiki_context,
    resolve_topics_exact,
    select_lesson_images,
)


async def regenerate(baseline_dir: Path, output_dir: Path, lesson_filter: str | None = None):
    outline_path = baseline_dir / "outline.json"
    if not outline_path.exists():
        print(f"[!] No outline.json found in {baseline_dir}")
        sys.exit(1)

    outline = json.loads(outline_path.read_text())

    output_dir.mkdir(parents=True, exist_ok=True)
    notes_dir = output_dir / "notes"
    notes_dir.mkdir(exist_ok=True)
    kb_dir = output_dir / "reference-kb"
    kb_dir.mkdir(exist_ok=True)
    ckpt_dir = output_dir / "checkpoints"
    ckpt_dir.mkdir(exist_ok=True)

    (ckpt_dir / "stage2_outline.json").write_text(json.dumps(outline, indent=2))

    all_lessons = []
    for mod in outline["modules"]:
        for les in mod["lessons"]:
            all_lessons.append(les)

    if lesson_filter:
        all_lessons = [l for l in all_lessons if fnmatch(l["slug"], lesson_filter)]
        print(f"  Filtered to {len(all_lessons)} lessons matching '{lesson_filter}'")

    print(f"\n  Regenerating {len(all_lessons)} lessons from {outline['title']}")
    print(f"  Output: {output_dir}\n")

    results: dict[str, dict] = {}
    assessment_entries = []
    total_start = time.time()

    for i, lesson in enumerate(all_lessons, 1):
        slug = lesson["slug"]
        title = lesson["title"]
        concepts = lesson.get("concepts", [])

        print(f"  [{i}/{len(all_lessons)}] {title}")
        start = time.time()

        resolved = resolve_topics_exact(concepts)
        topic_slugs = resolved["topic_slugs"]
        print(f"    Topics: {sorted(topic_slugs)}")

        wiki_ctx = load_wiki_context(concepts, topic_slugs=topic_slugs)
        ref_ctx = load_wiki_context(concepts, topic_slugs=topic_slugs, track="reference")
        source_count = sum(len(v) for v in wiki_ctx.get("source_content", {}).values())
        ref_count = sum(len(v) for v in ref_ctx.get("source_content", {}).values())
        image_count = sum(len(v) for v in wiki_ctx.get("images", {}).values())
        print(f"    Wiki context: {source_count} ped + {ref_count} ref sources, {image_count} images")

        ref_kwarg = ref_ctx if ref_ctx.get("source_content") else None

        try:
            bundle = await generate_lesson_bundle(lesson, wiki_ctx, reference_ctx=ref_kwarg)
        except Exception as e:
            print(f"    [!] Failed: {e}")
            results[slug] = {"error": str(e)}
            continue

        content_data = bundle.get("content", {})
        kb_text = bundle.get("reference_kb", "")
        wiki_meta = bundle.get("wiki_meta", {})
        lesson_images = bundle.get("image_metadata", [])

        notes_text = content_data.get("content", "")
        notes_wc = len(notes_text.split())
        kb_wc = len(kb_text.split())

        lesson_out = {
            "title": title,
            "slug": slug,
            "order_index": lesson.get("order_index", 0),
            "summary": content_data.get("summary", lesson.get("summary", "")),
            "concepts": content_data.get("concepts", concepts),
            "content": notes_text,
            "reference_kb": kb_text,
            "sources_used": content_data.get("sources_used", []),
            "image_metadata": lesson_images,
            "youtube_id": content_data.get("youtube_id", wiki_meta.get("youtube_id")),
            "video_title": content_data.get("video_title", wiki_meta.get("video_title")),
        }

        (output_dir / f"{slug}.json").write_text(json.dumps(lesson_out, indent=2))
        (notes_dir / f"{slug}.md").write_text(notes_text)
        if kb_text:
            (kb_dir / f"{slug}.md").write_text(kb_text)

        results[slug] = lesson_out
        elapsed = time.time() - start
        print(f"    Done: {notes_wc}w notes, {kb_wc}w KB, "
              f"{len(lesson_out['sources_used'])} sources, "
              f"{len(lesson_images)} images ({elapsed:.1f}s)")

        assessment_entries.append({
            "lesson": {
                "title": title,
                "slug": slug,
                "order_index": lesson.get("order_index", 0),
                "summary": lesson.get("summary", ""),
                "concepts": concepts,
            },
            "topics": sorted(topic_slugs),
            "resolved_topics": sorted(topic_slugs),
        })

    assessment = {"needs_research": [], "fully_covered": assessment_entries}
    (ckpt_dir / "stage3_assessment.json").write_text(json.dumps(assessment, indent=2))

    total_elapsed = time.time() - total_start
    successful = sum(1 for v in results.values() if "error" not in v)
    print(f"\n  Regeneration complete: {successful}/{len(all_lessons)} lessons "
          f"in {total_elapsed:.0f}s")

    if successful > 0:
        avg_notes = sum(
            len(v.get("content", "").split())
            for v in results.values() if "error" not in v
        ) / successful
        avg_kb = sum(
            len(v.get("reference_kb", "").split())
            for v in results.values() if "error" not in v
        ) / successful
        avg_sources = sum(
            len(v.get("sources_used", []))
            for v in results.values() if "error" not in v
        ) / successful
        avg_images = sum(
            len(v.get("image_metadata", []))
            for v in results.values() if "error" not in v
        ) / successful
        print(f"  Averages: {avg_notes:.0f}w notes, {avg_kb:.0f}w KB, "
              f"{avg_sources:.1f} sources, {avg_images:.1f} images")


def main():
    parser = argparse.ArgumentParser(description="Regenerate course with wiki-first pipeline")
    parser.add_argument("--baseline", type=str, required=True,
                        help="Path to baseline experiment directory (relative to backend/)")
    parser.add_argument("--output", type=str, default=None,
                        help="Output directory (default: baseline path with -old replaced by -new)")
    parser.add_argument("--lesson", type=str, default=None,
                        help="Glob pattern to filter lessons (e.g. 'self-attention')")
    args = parser.parse_args()

    baseline_dir = BACKEND / args.baseline
    if not baseline_dir.exists():
        baseline_dir = Path(args.baseline)
    if not baseline_dir.exists():
        print(f"[!] Baseline directory not found: {args.baseline}")
        sys.exit(1)

    if args.output:
        output_dir = BACKEND / args.output
    else:
        output_dir = Path(str(baseline_dir).replace("-old", "-new"))

    asyncio.run(regenerate(baseline_dir, output_dir, args.lesson))


if __name__ == "__main__":
    main()
