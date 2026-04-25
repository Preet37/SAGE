"""
Merge pending wiki changes into the canonical tracked wiki.

Usage:
    uv run python scripts/merge_wiki_pending.py              # dry-run (list pending)
    uv run python scripts/merge_wiki_pending.py --apply       # apply all
    uv run python scripts/merge_wiki_pending.py --interactive  # review one by one
"""

import argparse
import json
import re
import shutil
import sys
from pathlib import Path

WIKI_DIR = Path(__file__).resolve().parent.parent.parent / "content" / "pedagogy-wiki"
PENDING_DIR = WIKI_DIR / ".pending"
APPLIED_DIR = PENDING_DIR / "applied"
CONCEPT_MAP_PATH = WIKI_DIR / "concept-map.md"
TOPICS_DIR = WIKI_DIR / "resources" / "by-topic"


def _load_pending() -> list[tuple[Path, dict]]:
    if not PENDING_DIR.exists():
        return []
    items = []
    for f in sorted(PENDING_DIR.glob("*.json")):
        try:
            items.append((f, json.loads(f.read_text())))
        except (json.JSONDecodeError, OSError) as e:
            print(f"  [warn] Skipping {f.name}: {e}")
    return items


def _apply_new_topic(item: dict) -> None:
    data = item["data"]
    slug = item["topic_slug"]
    page_path = TOPICS_DIR / f"{slug}.md"

    TOPICS_DIR.mkdir(parents=True, exist_ok=True)

    if page_path.exists():
        print(f"  Page already exists: {slug}.md — skipping page write")
    else:
        page_path.write_text(data["page_content"])
        print(f"  Created: {page_path.relative_to(WIKI_DIR)}")

    (TOPICS_DIR / slug).mkdir(exist_ok=True)

    if CONCEPT_MAP_PATH.exists():
        cm_text = CONCEPT_MAP_PATH.read_text()
    else:
        cm_text = "# Concept → Topic Map\n\n"

    if f"# {slug}" not in cm_text:
        cm_text += data["concept_map_entry"]
        CONCEPT_MAP_PATH.write_text(cm_text)
        n_concepts = len(data.get("concepts", []))
        print(f"  Updated concept-map.md with {slug} ({n_concepts} concepts)")
    else:
        print(f"  Concept map already contains {slug} — skipping")

    sentinel = WIKI_DIR / ".needs-rebuild"
    sentinel.touch()


def _apply_structural_note(item: dict) -> None:
    data = item["data"]
    slug = item["topic_slug"]
    page_path = TOPICS_DIR / f"{slug}.md"

    if not page_path.exists():
        print(f"  [warn] No page for topic {slug!r} — cannot apply structural note")
        return

    content = page_path.read_text()
    note_text = data["note_text"]

    if note_text.strip() in content:
        print(f"  Note already present on {slug}.md — skipping")
        return

    if "## Last Verified" in content:
        content = content.replace("## Last Verified", f"{note_text}\n## Last Verified")
    else:
        content += note_text

    page_path.write_text(content)
    print(f"  Appended structural note to {slug}.md")


def _apply_resource_page(item: dict) -> None:
    data = item["data"]
    slug = item["topic_slug"]
    page_path = TOPICS_DIR / f"{slug}.md"

    if page_path.exists():
        old_len = len(page_path.read_text())
        new_len = len(data["page_content"])
        print(f"  Replacing {slug}.md ({old_len} → {new_len} chars, {data.get('source_count', '?')} sources)")
    else:
        print(f"  Creating {slug}.md ({data.get('source_count', '?')} sources)")

    TOPICS_DIR.mkdir(parents=True, exist_ok=True)
    page_path.write_text(data["page_content"])


_APPLIERS = {
    "new_topic": _apply_new_topic,
    "structural_note": _apply_structural_note,
    "resource_page": _apply_resource_page,
}


def _describe(item: dict) -> str:
    """One-line description of a pending item."""
    item_type = item["type"]
    slug = item["topic_slug"]
    course = item.get("course", "")
    ts = item.get("timestamp", "?")
    course_part = f" (course: {course})" if course else ""
    if item_type == "new_topic":
        n = len(item["data"].get("concepts", []))
        return f"[new_topic] {slug} — {n} concepts{course_part} @ {ts}"
    elif item_type == "structural_note":
        concept = item["data"].get("concept", "?")
        return f"[structural_note] {slug} — \"{concept}\"{course_part} @ {ts}"
    elif item_type == "resource_page":
        n = item["data"].get("source_count", "?")
        return f"[resource_page] {slug} — {n} sources{course_part} @ {ts}"
    return f"[{item_type}] {slug}{course_part} @ {ts}"


def _move_to_applied(file_path: Path) -> None:
    APPLIED_DIR.mkdir(parents=True, exist_ok=True)
    dest = APPLIED_DIR / file_path.name
    shutil.move(str(file_path), str(dest))


def run_dry_run(items: list[tuple[Path, dict]]) -> None:
    print(f"\n{len(items)} pending item(s):\n")
    for path, item in items:
        print(f"  {_describe(item)}")
        print(f"    file: {path.name}")
    print()


def run_apply(items: list[tuple[Path, dict]]) -> None:
    applied = 0
    for path, item in items:
        item_type = item["type"]
        print(f"\nApplying: {_describe(item)}")
        applier = _APPLIERS.get(item_type)
        if not applier:
            print(f"  [warn] Unknown type {item_type!r} — skipping")
            continue
        try:
            applier(item)
            _move_to_applied(path)
            applied += 1
        except Exception as e:
            print(f"  [error] Failed: {e}")
    print(f"\nDone: {applied}/{len(items)} applied.")


def run_interactive(items: list[tuple[Path, dict]]) -> None:
    applied = 0
    skipped = 0
    for i, (path, item) in enumerate(items, 1):
        print(f"\n--- [{i}/{len(items)}] {_describe(item)} ---")

        if item["type"] == "resource_page":
            preview = item["data"]["page_content"][:300]
            print(f"  Preview:\n{preview}...")
        elif item["type"] == "new_topic":
            concepts = item["data"].get("concepts", [])
            print(f"  Concepts: {', '.join(concepts[:8])}")
        elif item["type"] == "structural_note":
            print(f"  Note: {item['data'].get('note_text', '').strip()[:200]}")

        while True:
            choice = input("\n  [a]pply / [s]kip / [q]uit > ").strip().lower()
            if choice in ("a", "apply"):
                applier = _APPLIERS.get(item["type"])
                if applier:
                    try:
                        applier(item)
                        _move_to_applied(path)
                        applied += 1
                    except Exception as e:
                        print(f"  [error] {e}")
                break
            elif choice in ("s", "skip"):
                skipped += 1
                break
            elif choice in ("q", "quit"):
                print(f"\nStopped. Applied: {applied}, Skipped: {skipped + len(items) - i}")
                return
            else:
                print("  Invalid choice. Use a/s/q.")

    print(f"\nDone. Applied: {applied}, Skipped: {skipped}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Merge pending wiki changes")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--apply", action="store_true", help="Apply all pending items")
    group.add_argument("--interactive", action="store_true", help="Review one by one")
    args = parser.parse_args()

    items = _load_pending()
    if not items:
        print("No pending wiki items.")
        return

    if args.apply:
        run_apply(items)
    elif args.interactive:
        run_interactive(items)
    else:
        run_dry_run(items)


if __name__ == "__main__":
    main()
