#!/usr/bin/env python3
"""
Dump old (stored) and new (regenerated) KB for a lesson to side-by-side markdown files.

Usage:
    python3 scripts/dump_kb_comparison.py <lesson-slug>

Writes:
    scripts/kb_compare_old.md   — what the tutor currently has
    scripts/kb_compare_new.md   — regenerated with the current prompt
"""

import asyncio
import json
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
BACKEND_ENV = REPO_ROOT / "backend" / ".env"
OLD_PATH = Path(__file__).parent / "kb_compare_old.md"
NEW_PATH = Path(__file__).parent / "kb_compare_new.md"


def _load_env():
    if BACKEND_ENV.exists():
        for line in BACKEND_ENV.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                os.environ.setdefault(k.strip(), v.strip())


_load_env()
sys.path.insert(0, str(REPO_ROOT / "backend"))


def _fetch_lesson(slug: str):
    from sqlmodel import Session, select
    from app.db import engine
    from app.models.learning import Lesson
    with Session(engine) as session:
        stmt = select(Lesson).where(Lesson.slug == slug)
        return session.exec(stmt).first()


async def _regenerate(lesson) -> str:
    from app.services.course_generator import generate_reference_kb_from_wiki
    lesson_dict = {
        "title": lesson.title,
        "slug": lesson.slug,
        "summary": lesson.summary or "",
        "concepts": json.loads(lesson.concepts) if isinstance(lesson.concepts, str) else (lesson.concepts or []),
    }
    new_kb = ""
    async for event_str in generate_reference_kb_from_wiki([lesson_dict], existing_kb={}):
        if not event_str.strip().startswith("data: "):
            continue
        try:
            evt = json.loads(event_str.strip()[6:])
            if evt.get("type") == "reference_kb":
                new_kb = evt.get("data", {}).get(lesson.slug, "")
        except (json.JSONDecodeError, KeyError):
            pass
    return new_kb


def _dump_sources(slug: str, lesson) -> str:
    """Build a source breakdown section for the comparison."""
    from app.services.course_generator import load_wiki_context, resolve_topics_llm

    concepts = json.loads(lesson.concepts) if isinstance(lesson.concepts, str) else (lesson.concepts or [])
    if not concepts:
        return "(no concepts)\n"

    try:
        resolved = asyncio.get_event_loop().run_until_complete(
            resolve_topics_llm(concepts, lesson_title=lesson.title,
                               lesson_summary=lesson.summary or "")
        )
        topic_slugs = resolved["topic_slugs"]
    except Exception:
        from app.services.course_generator import resolve_topics_exact
        topic_slugs = resolve_topics_exact(concepts)["topic_slugs"]

    lines = ["## Source Breakdown\n"]

    ped_ctx = load_wiki_context(concepts, topic_slugs=topic_slugs)
    ref_ctx = load_wiki_context(concepts, topic_slugs=topic_slugs, track="reference")

    ped_sources = []
    for slug_sources in ped_ctx.get("source_content", {}).values():
        for src in slug_sources:
            first_lines = src["content"].split("\n", 5)
            source_line = next(
                (l for l in first_lines if l.startswith("# Source:")),
                src["file"],
            )
            ped_sources.append(source_line.replace("# Source: ", ""))

    ref_sources = []
    for slug_sources in ref_ctx.get("source_content", {}).values():
        for src in slug_sources:
            first_lines = src["content"].split("\n", 5)
            source_line = next(
                (l for l in first_lines if l.startswith("# Source:")),
                src["file"],
            )
            ref_sources.append(source_line.replace("# Source: ", ""))

    has_ref = bool(ref_sources)
    mode = "Blended (reference + pedagogy)" if has_ref else "Pedagogy-only fallback"
    lines.append(f"**Mode:** {mode}\n")

    lines.append(f"### Pedagogy sources ({len(ped_sources)})")
    for s in ped_sources:
        lines.append(f"- {s}")
    lines.append("")

    if ref_sources:
        lines.append(f"### Reference sources ({len(ref_sources)})")
        for s in ref_sources:
            lines.append(f"- {s}")
        lines.append("")

    # Check for ramps
    wiki_dir = Path(os.environ.get("CONTENT_DIR", str(Path(__file__).parent.parent / "content"))).resolve() / "pedagogy-wiki" / "resources" / "by-topic"
    for ts in topic_slugs:
        ramps_path = wiki_dir / ts / "reference" / "ramps.json"
        if ramps_path.exists():
            try:
                ramps = json.loads(ramps_path.read_text())
                if ramps:
                    lines.append(f"### Ramps (unfilled needs → runtime search)")
                    for r in ramps:
                        lines.append(f"- [{r.get('need_type', '?')}] "
                                     f"{r.get('description', '')} — "
                                     f"search: \"{r.get('search_hint', '')}\"")
                    lines.append("")
            except (json.JSONDecodeError, ValueError):
                pass

    return "\n".join(lines)


async def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = [a for a in sys.argv[1:] if a.startswith("--")]
    with_sources = "--with-sources" in flags

    if not args:
        print("Usage: python3 scripts/dump_kb_comparison.py <lesson-slug> [--with-sources]")
        sys.exit(1)

    slug = args[0]
    print(f"Fetching '{slug}' from DB...")
    lesson = _fetch_lesson(slug)
    if not lesson:
        print(f"ERROR: lesson '{slug}' not found.")
        sys.exit(1)

    old_kb = lesson.reference_kb or ""
    if not old_kb:
        print("WARNING: no stored KB for this lesson.")

    header = f"# {lesson.title}\n*Slug: `{slug}`*\n\n"

    source_section = ""
    if with_sources:
        print("Building source breakdown...")
        source_section = _dump_sources(slug, lesson) + "\n---\n\n"

    OLD_PATH.write_text(header + source_section + "---\n\n" + old_kb)
    print(f"Old KB written → {OLD_PATH}  ({len(old_kb.split())} words)")

    print("Regenerating with new prompt (this takes ~60s)...")
    new_kb = await _regenerate(lesson)
    if not new_kb:
        print("ERROR: new KB came back empty — no wiki source material for this lesson?")
        sys.exit(1)

    NEW_PATH.write_text(header + source_section + "---\n\n" + new_kb)
    print(f"New KB written → {NEW_PATH}  ({len(new_kb.split())} words)")
    if with_sources:
        print("(Source breakdown included in both files)")
    print("\nOpen both files side by side and compare!")


if __name__ == "__main__":
    asyncio.run(main())
