#!/usr/bin/env python3
"""Backfill # Author: / # Author Slug: headers into existing source .md files.

Uses the author registry (authors.md) for domain-based resolution.
Does NOT modify files that already have an # Author: header.

Usage:
    uv run python scripts/backfill_authors.py              # dry run (default)
    uv run python scripts/backfill_authors.py --apply      # actually write files
    uv run python scripts/backfill_authors.py --stats      # just show domain stats
"""

import argparse
import os
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.services.wiki_authors import resolve_author, load_authors

_WIKI_DIR = Path(os.environ.get("CONTENT_DIR", str(Path(__file__).resolve().parent.parent.parent / "content"))).resolve() / "pedagogy-wiki"
_SOURCE_RE = re.compile(r"^#\s*Source:\s*(https?://\S+)")
_AUTHOR_RE = re.compile(r"^#\s*Author:", re.MULTILINE)


def find_source_files() -> list[Path]:
    base = _WIKI_DIR / "resources" / "by-topic"
    files = []
    for f in sorted(base.rglob("*.md")):
        if f.name.startswith("_") or f.name == "curation-report.md":
            continue
        text = f.read_text(errors="replace")[:200]
        if text.startswith("# Source:"):
            files.append(f)
    return files


def backfill_file(path: Path, *, apply: bool = False) -> dict:
    """Add author headers to a single source file.

    Returns a result dict with status: 'updated', 'already_has_author',
    'no_match', or 'error'.
    """
    text = path.read_text(errors="replace")

    if _AUTHOR_RE.search(text[:500]):
        return {"status": "already_has_author", "path": str(path)}

    m = _SOURCE_RE.match(text.splitlines()[0])
    if not m:
        return {"status": "error", "path": str(path), "reason": "no Source: header"}

    url = m.group(1)
    author = resolve_author(url)
    if not author:
        return {"status": "no_match", "path": str(path), "url": url}

    name = author.get("name", "")
    slug = author.get("slug", "")

    lines = text.splitlines(keepends=True)
    insert_lines = []
    if name:
        insert_lines.append(f"# Author: {name}\n")
    if slug:
        insert_lines.append(f"# Author Slug: {slug}\n")

    # Insert after the # Source: line
    new_lines = [lines[0]] + insert_lines + lines[1:]
    new_text = "".join(new_lines)

    if apply:
        path.write_text(new_text)

    return {
        "status": "updated",
        "path": str(path),
        "author": name,
        "slug": slug,
        "url": url,
    }


def show_stats(files: list[Path]) -> None:
    """Show domain frequency for unmatched files."""
    from urllib.parse import urlparse

    unmatched_domains: Counter = Counter()
    matched_domains: Counter = Counter()

    for f in files:
        text = f.read_text(errors="replace")
        if _AUTHOR_RE.search(text[:500]):
            continue
        m = _SOURCE_RE.match(text.splitlines()[0])
        if not m:
            continue
        url = m.group(1)
        domain = urlparse(url).netloc.replace("www.", "")
        author = resolve_author(url)
        if author:
            matched_domains[domain] += 1
        else:
            unmatched_domains[domain] += 1

    authors = load_authors()
    print(f"\nRegistry: {len(authors)} authors, "
          f"{sum(len(a.get('domains', [])) for a in authors)} domains")

    print(f"\n✓ Matched domains ({sum(matched_domains.values())} files):")
    for d, c in matched_domains.most_common(20):
        author = resolve_author(f"https://{d}/")
        name = author["name"] if author else "?"
        print(f"  {c:4d}  {d:<40s}  → {name}")

    print(f"\n✗ Unmatched domains ({sum(unmatched_domains.values())} files):")
    for d, c in unmatched_domains.most_common(20):
        print(f"  {c:4d}  {d}")


def main():
    parser = argparse.ArgumentParser(description="Backfill author headers into source .md files")
    parser.add_argument("--apply", action="store_true", help="Actually write files (default is dry run)")
    parser.add_argument("--stats", action="store_true", help="Show domain match/miss stats only")
    args = parser.parse_args()

    files = find_source_files()
    print(f"Found {len(files)} source .md files")

    if args.stats:
        show_stats(files)
        return

    results = Counter()
    updated = []

    for f in files:
        r = backfill_file(f, apply=args.apply)
        results[r["status"]] += 1
        if r["status"] == "updated":
            updated.append(r)

    mode = "APPLIED" if args.apply else "DRY RUN"
    print(f"\n--- {mode} ---")
    print(f"  Updated:            {results['updated']}")
    print(f"  Already has author: {results['already_has_author']}")
    print(f"  No match (unknown): {results['no_match']}")
    print(f"  Errors:             {results['error']}")

    if updated and not args.apply:
        print(f"\nWould update {len(updated)} files. Examples:")
        for r in updated[:10]:
            rel = Path(r["path"]).relative_to(_WIKI_DIR)
            print(f"  {rel}  → {r['author']}")
        if len(updated) > 10:
            print(f"  ... and {len(updated) - 10} more")
        print("\nRe-run with --apply to write changes.")


if __name__ == "__main__":
    main()
