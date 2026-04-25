#!/usr/bin/env python3
"""Backfill real paper authors into venue-attributed source files.

Replaces "# Author: arXiv" with the actual paper authors fetched from
the arXiv API. Handles rate limiting (3 req/sec per arXiv policy).

Usage:
    uv run python scripts/backfill_paper_authors.py              # dry run
    uv run python scripts/backfill_paper_authors.py --apply      # write files
"""

import argparse
import asyncio
import os
import re
import sys
import time
from functools import partial
from pathlib import Path

print = partial(print, flush=True)

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.wiki_authors import (
    extract_arxiv_authors,
    format_paper_authors,
    is_venue,
    parse_arxiv_id,
)

_WIKI_DIR = Path(os.environ.get("CONTENT_DIR", str(Path(__file__).resolve().parent.parent.parent / "content"))).resolve() / "pedagogy-wiki"
_SOURCE_DIR = _WIKI_DIR / "resources" / "by-topic"

_HEADER_RE = re.compile(
    r"^(# Source:\s*(https?://\S+)\n)"
    r"(# Author:\s*.+\n)"
    r"(# Author Slug:\s*.+\n)?",
    re.MULTILINE,
)
_AUTHOR_SLUG_RE = re.compile(r"^# Author Slug:\s*(\S+)", re.MULTILINE)


def find_venue_files() -> list[tuple[Path, str, str]]:
    """Find source files currently attributed to a venue.

    Returns [(path, url, slug), ...].
    """
    results = []
    for f in sorted(_SOURCE_DIR.rglob("*.md")):
        if f.name.startswith("_") or f.name == "curation-report.md":
            continue
        head = f.read_text(errors="replace")[:500]
        m = _AUTHOR_SLUG_RE.search(head)
        if m and is_venue(m.group(1)):
            source_m = re.match(r"^# Source:\s*(https?://\S+)", head)
            if source_m:
                results.append((f, source_m.group(1), m.group(1)))
    return results


async def process_arxiv_file(
    path: Path, url: str, *, apply: bool = False
) -> dict:
    """Fetch real authors for an arXiv paper and optionally update the file."""
    arxiv_id = parse_arxiv_id(url)
    if not arxiv_id:
        return {"status": "skip", "path": str(path), "reason": "no arXiv ID parsed"}

    authors = None
    for attempt in range(3):
        try:
            authors = await extract_arxiv_authors(arxiv_id)
            break
        except Exception as e:
            if "429" in str(e) and attempt < 2:
                await asyncio.sleep(3 * (attempt + 1))
                continue
            return {"status": "error", "path": str(path), "error": str(e)}

    if not authors:
        return {"status": "skip", "path": str(path), "reason": "no authors from API"}

    author_str = format_paper_authors(authors)

    text = path.read_text(errors="replace")
    m = _HEADER_RE.search(text)
    if not m:
        return {"status": "skip", "path": str(path), "reason": "header not matched"}

    source_line = m.group(1)
    new_header = f"{source_line}# Author: {author_str}\n"

    new_text = text[:m.start()] + new_header + text[m.end():]

    if apply:
        path.write_text(new_text)

    return {
        "status": "updated",
        "path": str(path),
        "authors": author_str,
        "arxiv_id": arxiv_id,
        "author_count": len(authors),
    }


async def main():
    parser = argparse.ArgumentParser(description="Backfill real paper authors")
    parser.add_argument("--apply", action="store_true", help="Write changes to files")
    args = parser.parse_args()

    files = find_venue_files()
    print(f"Found {len(files)} venue-attributed source files")

    arxiv_files = [(p, u) for p, u, slug in files if slug == "arxiv"]
    other_files = [(p, u, slug) for p, u, slug in files if slug != "arxiv"]

    print(f"  arXiv papers: {len(arxiv_files)}")
    print(f"  Other venues: {len(other_files)}")

    if other_files:
        print("\n  Non-arXiv venue files (skipped for now):")
        for p, u, slug in other_files:
            print(f"    [{slug}] {p.relative_to(_WIKI_DIR)}")

    if not arxiv_files:
        print("\nNo arXiv papers to process.")
        return

    mode = "APPLYING" if args.apply else "DRY RUN"
    print(f"\nProcessing {len(arxiv_files)} arXiv papers ({mode})...")

    updated = 0
    errors = 0
    skipped = 0

    for i, (path, url) in enumerate(arxiv_files):
        result = await process_arxiv_file(path, url, apply=args.apply)

        if result["status"] == "updated":
            updated += 1
            rel = path.relative_to(_WIKI_DIR)
            print(f"  [{i+1}/{len(arxiv_files)}] {rel}")
            print(f"    → {result['authors']}")
        elif result["status"] == "error":
            errors += 1
            print(f"  [{i+1}/{len(arxiv_files)}] ERROR: {result['error']}")
        else:
            skipped += 1
            print(f"  [{i+1}/{len(arxiv_files)}] skip: {result.get('reason', '?')}")

        if i < len(arxiv_files) - 1:
            await asyncio.sleep(1.0)

    print(f"\n--- {'APPLIED' if args.apply else 'DRY RUN'} ---")
    print(f"  Updated: {updated}")
    print(f"  Skipped: {skipped}")
    print(f"  Errors:  {errors}")

    if not args.apply and updated > 0:
        print("\nRe-run with --apply to write changes.")


if __name__ == "__main__":
    asyncio.run(main())
