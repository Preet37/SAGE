#!/usr/bin/env python3
"""Backfill ``- Audience:`` tags into existing wiki resource pages.

Scans hand-curated resource pages (those with ``## Video (best)`` etc.)
and adds ``- Audience: <tag>`` lines to resource entries that have
``- Level:`` but no ``- Audience:``.

Uses simple heuristics based on the resource type/section and level:
  - Papers (arxiv, proceedings) -> technical
  - API docs, official docs -> practitioner
  - Tutorial videos, getting-started -> practitioner or general
  - Blog posts -> depends on level (advanced = technical, else practitioner)
  - Code walkthroughs -> practitioner
  - General overviews -> all

Usage:
    uv run python scripts/backfill_audience_tags.py              # dry run
    uv run python scripts/backfill_audience_tags.py --apply      # write files
    uv run python scripts/backfill_audience_tags.py --stats      # show stats only
"""

import argparse
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

_WIKI_DIR = (
    Path(
        os.environ.get(
            "CONTENT_DIR",
            str(Path(__file__).resolve().parent.parent.parent / "content"),
        )
    ).resolve()
    / "pedagogy-wiki"
)

_LEVEL_RE = re.compile(r"^- Level:\s*(.+)$", re.MULTILINE)
_AUDIENCE_RE = re.compile(r"^- Audience:\s*(.+)$", re.MULTILINE)
_SECTION_RE = re.compile(r"^## (.+)$", re.MULTILINE)
_URL_RE = re.compile(r"^- url:\s*(.+)$", re.MULTILINE)
_YT_RE = re.compile(r"^- youtube_id:\s*(.+)$", re.MULTILINE)


def _infer_audience(section: str, level: str, url: str = "") -> str:
    """Infer audience tag from section header, level, and URL."""
    section_lower = section.lower()
    level_lower = level.lower()

    if "paper" in section_lower or "arxiv" in url:
        return "technical"

    if "video" in section_lower:
        if "advanced" in level_lower:
            return "technical"
        return "practitioner"

    if "code" in section_lower:
        return "practitioner"

    if "doc" in section_lower or "reference" in section_lower:
        return "practitioner"

    if "deep dive" in section_lower:
        if "advanced" in level_lower:
            return "technical"
        return "practitioner"

    if "blog" in section_lower or "written" in section_lower:
        if "advanced" in level_lower:
            return "technical"
        if "beginner" in level_lower:
            return "general"
        return "practitioner"

    if "tutorial" in section_lower or "getting started" in section_lower:
        return "general"

    return "all"


def find_resource_pages() -> list[Path]:
    """Find hand-curated resource pages (those with standard section headers)."""
    base = _WIKI_DIR / "resources" / "by-topic"
    if not base.is_dir():
        return []
    pages = []
    markers = ("## Video (best)", "## Blog / Written explainer", "## Deep dive",
               "## Original paper", "## Code walkthrough")
    for f in sorted(base.glob("*.md")):
        text = f.read_text(errors="replace")
        if any(m in text for m in markers):
            pages.append(f)
    return pages


def backfill_page(page: Path, apply: bool = False) -> dict:
    """Add Audience tags to a single resource page.

    Returns stats dict with counts.
    """
    text = page.read_text(errors="replace")
    lines = text.split("\n")
    new_lines = []
    current_section = ""
    added = 0
    already_has = 0

    i = 0
    while i < len(lines):
        line = lines[i]

        section_match = _SECTION_RE.match(line)
        if section_match:
            current_section = section_match.group(1)

        new_lines.append(line)

        if line.startswith("- Level:"):
            level_val = line.replace("- Level:", "").strip()

            next_idx = i + 1
            while next_idx < len(lines) and not lines[next_idx].strip():
                next_idx += 1

            if next_idx < len(lines) and lines[next_idx].startswith("- Audience:"):
                already_has += 1
            else:
                url = ""
                for back in range(max(0, i - 5), i):
                    if lines[back].startswith("- url:"):
                        url = lines[back].replace("- url:", "").strip()
                        break

                audience = _infer_audience(current_section, level_val, url)
                new_lines.append(f"- Audience: {audience}")
                added += 1

        i += 1

    result = {
        "file": page.name,
        "added": added,
        "already_has": already_has,
    }

    if apply and added > 0:
        page.write_text("\n".join(new_lines))
        result["written"] = True

    return result


def main():
    parser = argparse.ArgumentParser(description="Backfill audience tags on wiki resource pages")
    parser.add_argument("--apply", action="store_true", help="Actually write changes (default: dry run)")
    parser.add_argument("--stats", action="store_true", help="Only show aggregate stats")
    args = parser.parse_args()

    pages = find_resource_pages()
    print(f"Found {len(pages)} hand-curated resource pages\n")

    if not pages:
        return

    total_added = 0
    total_existing = 0
    results = []

    for page in pages:
        result = backfill_page(page, apply=args.apply)
        results.append(result)
        total_added += result["added"]
        total_existing += result["already_has"]

        if not args.stats and result["added"] > 0:
            status = "WRITTEN" if result.get("written") else "DRY RUN"
            print(f"  [{status}] {result['file']}: +{result['added']} audience tags "
                  f"({result['already_has']} already had)")

    print(f"\n{'=' * 50}")
    print(f"Total pages: {len(pages)}")
    print(f"Tags added: {total_added}")
    print(f"Already had tags: {total_existing}")
    pages_changed = sum(1 for r in results if r["added"] > 0)
    print(f"Pages {'updated' if args.apply else 'to update'}: {pages_changed}")

    if not args.apply and total_added > 0:
        print(f"\nDry run — re-run with --apply to write changes")


if __name__ == "__main__":
    main()
