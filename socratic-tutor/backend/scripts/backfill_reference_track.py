#!/usr/bin/env python3
"""Backfill the reference track for all wiki topics.

Reads the concept map, identifies topics that don't yet have reference/
subdirectories (or have fewer than N sources), then runs
enrich_reference_track() for each.

Usage:
    cd backend
    PYTHONUNBUFFERED=1 uv run python scripts/backfill_reference_track.py
    PYTHONUNBUFFERED=1 uv run python scripts/backfill_reference_track.py --dry-run
    PYTHONUNBUFFERED=1 uv run python scripts/backfill_reference_track.py --topics attention-mechanism,cnns
    PYTHONUNBUFFERED=1 uv run python scripts/backfill_reference_track.py --concurrency 3
    PYTHONUNBUFFERED=1 uv run python scripts/backfill_reference_track.py --min-sources 5  # re-enrich topics with <5 ref sources
"""

import argparse
import asyncio
import os
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.services.course_enricher import enrich_reference_track

_WIKI_DIR = Path(os.environ.get("CONTENT_DIR", str(Path(__file__).resolve().parent.parent.parent / "content"))).resolve() / "pedagogy-wiki"
_TOPICS_DIR = _WIKI_DIR / "resources" / "by-topic"


def parse_concept_map() -> list[dict]:
    """Parse concept-map.md into a list of {slug, title, concepts}."""
    concept_map_path = _WIKI_DIR / "concept-map.md"
    if not concept_map_path.exists():
        print(f"ERROR: concept-map.md not found at {concept_map_path}")
        sys.exit(1)

    text = concept_map_path.read_text()
    topics: list[dict] = []
    current: dict | None = None

    for line in text.split("\n"):
        line = line.strip()
        if line.startswith("# ") and not line.startswith("# Concept"):
            if current and current["concepts"]:
                topics.append(current)
            current = {"slug": line[2:].strip(), "title": "", "concepts": []}
        elif line.startswith("**") and current:
            m = re.match(r"\*\*(.+?)\*\*", line)
            if m:
                current["title"] = m.group(1)
        elif line.startswith("- ") and current:
            current["concepts"].append(line[2:].strip())

    if current and current["concepts"]:
        topics.append(current)

    return topics


def count_reference_sources(topic_slug: str) -> tuple[int, int]:
    """Return (source_count, card_count) for a topic's reference/ dir."""
    ref_dir = _TOPICS_DIR / topic_slug / "reference"
    if not ref_dir.is_dir():
        return 0, 0

    sources = 0
    cards = 0
    for f in ref_dir.iterdir():
        if f.suffix != ".md":
            continue
        if f.name == "curation-report.md":
            continue
        if f.name.endswith(".card.md"):
            cards += 1
        else:
            sources += 1
    return sources, cards


async def backfill_one(
    topic: dict,
    *,
    sem: asyncio.Semaphore,
    dry_run: bool = False,
) -> dict:
    """Run reference enrichment + card extraction for one topic."""
    slug = topic["slug"]
    title = topic["title"] or slug
    concepts = topic["concepts"]

    src_before, cards_before = count_reference_sources(slug)

    if dry_run:
        print(f"  [DRY RUN] {slug}: \"{title}\" — {len(concepts)} concepts, "
              f"{src_before} existing ref sources")
        return {"slug": slug, "status": "dry_run", "sources_before": src_before}

    async with sem:
        t0 = time.time()
        print(f"\n{'─' * 70}")
        print(f"  {slug}: \"{title}\" ({len(concepts)} concepts)")
        print(f"  Existing reference sources: {src_before}")

        try:
            result = await enrich_reference_track(
                title, slug, concepts,
                lesson_summary=f"Reference material for {title}",
            )

            picks = result.get("picks", 0)
            downloads = result.get("downloads", 0)
            ramps = len(result.get("unfilled_needs", []))

            print(f"  Needs: {result.get('needs', 0)} | "
                  f"Queries: {result.get('queries', 0)} | "
                  f"Searches: {result.get('searches', 0)}")
            print(f"  Picks: {picks} + {result.get('promotions', 0)} promotions | "
                  f"Downloads: {downloads}")

            if ramps:
                print(f"  Ramps (unfilled): {ramps}")
                for ramp in result.get("unfilled_needs", [])[:3]:
                    print(f"    → [{ramp.get('need_type', '?')}] "
                          f"{ramp.get('description', '')[:60]}")

            cards_extracted = result.get("cards_extracted", 0)
            cards_skipped = result.get("cards_skipped", 0)

            src_after, cards_after = count_reference_sources(slug)
            elapsed = time.time() - t0

            print(f"  Cards: {cards_extracted} extracted")
            print(f"  Final: {src_after} sources, {cards_after} cards ({elapsed:.1f}s)")

            return {
                "slug": slug,
                "status": "ok",
                "sources_before": src_before,
                "sources_after": src_after,
                "cards_after": cards_after,
                "picks": picks,
                "downloads": downloads,
                "ramps": ramps,
                "elapsed": elapsed,
            }

        except Exception as e:
            elapsed = time.time() - t0
            print(f"  ERROR: {type(e).__name__}: {e} ({elapsed:.1f}s)")
            return {
                "slug": slug,
                "status": "error",
                "error": str(e),
                "elapsed": elapsed,
            }


async def main():
    parser = argparse.ArgumentParser(description="Backfill reference track for wiki topics")
    parser.add_argument("--dry-run", action="store_true",
                        help="List what would be processed without running enrichment")
    parser.add_argument("--topics", type=str, default="",
                        help="Comma-separated topic slugs to process (default: all)")
    parser.add_argument("--concurrency", type=int, default=2,
                        help="Max topics to enrich in parallel (default: 2)")
    parser.add_argument("--min-sources", type=int, default=1,
                        help="Re-enrich topics with fewer than N reference sources (default: 1, i.e. skip topics with any)")
    args = parser.parse_args()

    all_topics = parse_concept_map()
    print(f"Found {len(all_topics)} topics in concept map\n")

    # Filter to requested topics
    if args.topics:
        requested = {s.strip() for s in args.topics.split(",")}
        all_topics = [t for t in all_topics if t["slug"] in requested]
        print(f"Filtered to {len(all_topics)} requested topics\n")

    # Filter out topics that already have enough reference sources
    needs_backfill = []
    already_done = []
    for t in all_topics:
        src_count, _ = count_reference_sources(t["slug"])
        if src_count < args.min_sources:
            needs_backfill.append(t)
        else:
            already_done.append(t)

    if already_done:
        print(f"Skipping {len(already_done)} topics with >= {args.min_sources} reference sources:")
        for t in already_done:
            src, cards = count_reference_sources(t["slug"])
            print(f"  {t['slug']}: {src} sources, {cards} cards")
        print()

    if not needs_backfill:
        print("Nothing to backfill — all topics have reference content!")
        return

    print(f"Will backfill {len(needs_backfill)} topics "
          f"(concurrency={args.concurrency}):\n")
    for t in needs_backfill:
        print(f"  {t['slug']}: \"{t['title']}\" ({len(t['concepts'])} concepts)")
    print()

    if args.dry_run:
        print("Dry run — no changes made.")
        return

    sem = asyncio.Semaphore(args.concurrency)
    t_start = time.time()

    results = await asyncio.gather(
        *(backfill_one(t, sem=sem) for t in needs_backfill),
        return_exceptions=True,
    )

    # Summary
    elapsed_total = time.time() - t_start
    print(f"\n{'═' * 70}")
    print(f"  BACKFILL SUMMARY")
    print(f"{'═' * 70}\n")

    ok = [r for r in results if isinstance(r, dict) and r.get("status") == "ok"]
    errors = [r for r in results if isinstance(r, dict) and r.get("status") == "error"]
    exceptions = [r for r in results if isinstance(r, Exception)]

    total_sources = sum(r.get("sources_after", 0) for r in ok)
    total_cards = sum(r.get("cards_after", 0) for r in ok)
    total_downloads = sum(r.get("downloads", 0) for r in ok)
    total_ramps = sum(r.get("ramps", 0) for r in ok)

    print(f"  Topics processed: {len(ok)}/{len(needs_backfill)}")
    print(f"  Total reference sources: {total_sources}")
    print(f"  Total reference cards: {total_cards}")
    print(f"  New downloads this run: {total_downloads}")
    print(f"  Unfilled ramps: {total_ramps}")
    print(f"  Errors: {len(errors) + len(exceptions)}")
    print(f"  Total time: {elapsed_total:.0f}s ({elapsed_total/60:.1f}m)")

    if errors:
        print(f"\n  Failed topics:")
        for r in errors:
            print(f"    {r['slug']}: {r.get('error', '?')}")
    if exceptions:
        print(f"\n  Exceptions:")
        for e in exceptions:
            print(f"    {type(e).__name__}: {e}")

    print(f"\n  Per-topic breakdown:")
    for r in sorted(ok, key=lambda x: x.get("elapsed", 0), reverse=True):
        print(f"    {r['slug']}: {r['sources_before']}→{r['sources_after']} sources, "
              f"{r['cards_after']} cards, {r.get('elapsed', 0):.0f}s")


if __name__ == "__main__":
    asyncio.run(main())
