#!/usr/bin/env python3
"""
Transform pedagogy-wiki topic .md files into Quartz-compatible pages.

Reads config from: wiki_config.json  (subject taxonomy, related topics, etc.)
Reads topics from: content/pedagogy-wiki/resources/by-topic/*.md
Writes to:         wiki/content/  (topics/, educators/, subjects/, levels/, index.md)

Run this after any topic is added or wiki_config.json is updated:
    python3 scripts/topic_to_quartz.py
"""

import os
import re
import sys
import json
from pathlib import Path
from collections import defaultdict

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).parent.parent
_CONTENT = Path(os.environ.get("CONTENT_DIR", str(REPO_ROOT / "content"))).resolve()
SOURCE_DIR = _CONTENT / "pedagogy-wiki" / "resources" / "by-topic"
WIKI_CONTENT = Path(os.environ.get("WIKI_OUTPUT_DIR", str(REPO_ROOT / "wiki" / "content"))).resolve()
CONFIG_PATH = REPO_ROOT / "wiki_config.json"

TOPICS_DIR = WIKI_CONTENT / "topics"
EDUCATORS_DIR = WIKI_CONTENT / "educators"
SUBJECTS_DIR = WIKI_CONTENT / "subjects"
LEVELS_DIR = WIKI_CONTENT / "levels"

# ---------------------------------------------------------------------------
# Load config
# ---------------------------------------------------------------------------

def load_config() -> dict:
    if not CONFIG_PATH.exists():
        print(f"ERROR: {CONFIG_PATH} not found. Run update_wiki.py first.", file=sys.stderr)
        sys.exit(1)
    with open(CONFIG_PATH) as f:
        return json.load(f)

# ---------------------------------------------------------------------------
# Resource section markers
# ---------------------------------------------------------------------------
RESOURCE_SECTION_PATTERNS = {
    "video": r"^##\s+Video",
    "blog": r"^##\s+Blog",
    "deep-dive": r"^##\s+Deep dive",
    "paper": r"^##\s+Original paper",
    "code": r"^##\s+Code",
}

# ---------------------------------------------------------------------------
# Body cleaning helpers
# ---------------------------------------------------------------------------

_ENRICHMENT_BLOCKQUOTE = re.compile(
    r"(?:^>[ \t]*\*(?:Why|Confidence|Found)\*.*\n?)+"
    r"(?:^>[ \t]+.*\n?)*",
    re.MULTILINE,
)
_STRUCTURAL_NOTE_BLOCK = re.compile(
    r"(?:^>[ \t]*\*\*\[Structural note\]\*\*.*\n)"
    r"(?:^>.*\n?)*",
    re.MULTILINE,
)
_LAST_VERIFIED_SECTION = re.compile(
    r"^## Last Verified\n(?:.*\n?)*", re.MULTILINE
)
_FOUND_DATE = re.compile(r"\*Found\*:\s*([\d-]+)")
_VERIFIED_DATE = re.compile(r"^## Last Verified\n([\d-]+)", re.MULTILINE)

_URL_LINE = re.compile(r"^-\s+(?:url|URL):\s+(https?://\S+)\s*$", re.MULTILINE)
_YOUTUBE_LINE = re.compile(r"^-\s+youtube_id:\s+(\S+)\s*$", re.MULTILINE)
_YOUTUBE_NONE = re.compile(r"^-\s+youtube_id:\s+None\b.*$\n?", re.MULTILINE)


def _clean_body(text: str) -> tuple[str, str | None]:
    """Strip enrichment metadata and linkify plain URLs.

    Returns (cleaned_body, latest_date_string_or_None).
    """
    dates: list[str] = _FOUND_DATE.findall(text)
    m = _VERIFIED_DATE.search(text)
    if m:
        dates.append(m.group(1))

    latest_date = max(dates) if dates else None

    text = _STRUCTURAL_NOTE_BLOCK.sub("", text)
    text = _ENRICHMENT_BLOCKQUOTE.sub("", text)
    text = _LAST_VERIFIED_SECTION.sub("", text)

    text = _YOUTUBE_NONE.sub("", text)
    text = _URL_LINE.sub(r"- **Link:** [\1](\1)", text)
    text = _YOUTUBE_LINE.sub(
        r"- **Watch:** [YouTube](https://www.youtube.com/watch?v=\1)", text
    )

    text = re.sub(r"\n{3,}", "\n\n", text)

    return text, latest_date


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------

def parse_topic(path: Path, cfg: dict) -> dict:
    """Parse a topic .md file and extract structured metadata."""
    raw_text = path.read_text(encoding="utf-8")
    text, latest_date = _clean_body(raw_text)
    lines = text.splitlines()

    slug = path.stem

    # Title: use override first, then H1, then slug fallback
    title = slug.replace("-", " ").title()
    for line in lines:
        if line.startswith("# "):
            title = line[2:].strip()
            break
    if slug in cfg.get("title_overrides", {}):
        title = cfg["title_overrides"][slug]

    # Educators: lines like "- **Name** —"
    educator_pattern = re.compile(r"-\s+\*\*([^*]+)\*\*\s+—")
    tracked = set(cfg.get("educator_slugs", {}).keys())
    found_educators = []
    for line in lines:
        m = educator_pattern.search(line)
        if m:
            name = m.group(1).strip()
            if name in tracked and name not in found_educators:
                found_educators.append(name)

    # Levels: lines like "- Level: beginner/intermediate"
    level_pattern = re.compile(r"-\s+Level:\s+(.+)", re.IGNORECASE)
    raw_levels = set()
    for line in lines:
        m = level_pattern.search(line)
        if m:
            raw = m.group(1).strip().lower()
            for part in re.split(r"[/\-–,]", raw):
                part = part.strip()
                if part in ("beginner", "intermediate", "advanced"):
                    raw_levels.add(part)
    levels = sorted(raw_levels, key=lambda x: ["beginner", "intermediate", "advanced"].index(x))
    if not levels:
        levels = ["intermediate"]

    # Resource types present
    resources = [k for k, pat in RESOURCE_SECTION_PATTERNS.items()
                 if re.search(pat, text, re.MULTILINE)]

    subject = cfg["subject_map"].get(slug, "Foundational AI")
    subject_slug = cfg["subject_slugs"].get(subject, "foundational-ai")

    # Related topics — only include slugs that actually exist as source files
    existing_slugs = {p.stem for p in SOURCE_DIR.glob("*.md")}
    related = [r for r in cfg.get("related_topics", {}).get(slug, [])
               if r in existing_slugs]

    return {
        "slug": slug,
        "title": title,
        "educators": found_educators,
        "levels": levels,
        "resources": resources,
        "subject": subject,
        "subject_slug": subject_slug,
        "related": related,
        "body": text,
        "date": latest_date,
    }


def build_frontmatter(meta: dict, cfg: dict) -> str:
    """Generate YAML frontmatter string for a topic page."""
    tags = [f"subject/{meta['subject_slug']}"]
    for level in meta["levels"]:
        tags.append(f"level/{level}")
    for edu in meta["educators"]:
        slug = cfg["educator_slugs"].get(edu, edu.lower().replace(" ", "-"))
        tags.append(f"educator/{slug}")
    for res in meta["resources"]:
        tags.append(f"resource/{res}")

    tags_yaml = "\n".join(f'  - "{t}"' for t in tags)
    educators_yaml = "\n".join(f'  - "{e}"' for e in meta["educators"])
    levels_yaml = "\n".join(f'  - "{l}"' for l in meta["levels"])
    resources_yaml = "\n".join(f'  - "{r}"' for r in meta["resources"])

    date_line = f'\ndate: {meta["date"]}' if meta.get("date") else ""

    return f"""---
title: "{meta['title']}"
subject: "{meta['subject']}"{date_line}
tags:
{tags_yaml}
educators:
{educators_yaml if meta['educators'] else '  []'}
levels:
{levels_yaml}
resources:
{resources_yaml if meta['resources'] else '  []'}
---"""


def build_related_section(meta: dict, all_meta: dict) -> str:
    """Build the ## Related Topics wikilink section."""
    if not meta["related"]:
        return ""
    lines = ["\n---\n", "## Related Topics\n"]
    for slug in meta["related"]:
        rel = all_meta.get(slug)
        rel_title = rel["title"] if rel else slug.replace("-", " ").title()
        lines.append(f"- [[topics/{slug}|{rel_title}]]")
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Reference library
# ---------------------------------------------------------------------------

def parse_reference_card(path: Path) -> dict | None:
    """Parse a .card.md file into structured metadata."""
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines:
        return None

    title = lines[0].replace("# Card: ", "").strip()

    source = ""
    role = ""
    need = ""
    anchor = ""
    key_content_lines: list[str] = []
    when_lines: list[str] = []
    in_key = False
    in_when = False

    for line in lines[1:]:
        if line.startswith("**Source:**"):
            source = line.replace("**Source:**", "").strip()
        elif line.startswith("**Role:**"):
            parts = line.split("|")
            for p in parts:
                p = p.strip()
                if p.startswith("**Role:**"):
                    role = p.replace("**Role:**", "").strip()
                elif p.startswith("**Need:**"):
                    need = p.replace("**Need:**", "").strip()
        elif line.startswith("**Anchor:**"):
            anchor = line.replace("**Anchor:**", "").strip()
        elif line.startswith("## Key Content"):
            in_key = True
            in_when = False
        elif line.startswith("## When to surface"):
            in_when = True
            in_key = False
        elif in_key:
            key_content_lines.append(line)
        elif in_when:
            when_lines.append(line)

    return {
        "title": title,
        "source": source,
        "role": role,
        "need": need,
        "anchor": anchor,
        "key_content": "\n".join(key_content_lines).strip(),
        "when_to_surface": "\n".join(when_lines).strip(),
    }


def load_reference_cards(slug: str) -> list[dict]:
    """Load all reference cards for a topic, sorted by role."""
    ref_dir = SOURCE_DIR / slug / "reference"
    if not ref_dir.is_dir():
        return []

    cards = []
    for f in sorted(ref_dir.iterdir()):
        if f.suffix == ".md" and f.name.endswith(".card.md"):
            card = parse_reference_card(f)
            if card:
                cards.append(card)

    role_order = {"paper": 0, "benchmark": 1, "reference_doc": 2, "": 3}
    cards.sort(key=lambda c: (role_order.get(c["role"], 3), c["title"]))
    return cards


def _role_emoji(role: str) -> str:
    return {
        "paper": "📄", "benchmark": "📊", "reference_doc": "📖",
        "working_example": "💻", "deployment_case": "🏭",
        "comparison": "⚖️", "explainer": "🔍",
    }.get(role, "📋")


def build_reference_section(slug: str) -> str:
    """Build the Additional Resources section for a topic page."""
    cards = load_reference_cards(slug)
    if not cards:
        return ""

    ped_dir = SOURCE_DIR / slug
    ped_sources = sum(1 for f in ped_dir.iterdir()
                      if f.suffix == ".md" and not f.name.startswith("_")
                      and f.name != "curation-report.md"
                      and "reference" not in str(f)) if ped_dir.is_dir() else 0

    lines = [
        "\n---\n",
        "## Additional Resources for Tutor Depth\n",
        f"> **{len(cards)} sources** — papers, official docs, working code, "
        f"benchmarks, and deep explainers that give the AI tutor precision "
        f"on this topic.\n",
    ]

    for card in cards:
        emoji = _role_emoji(card["role"])
        role_label = card["role"].replace("_", " ").title() if card["role"] else "Source"
        source_link = f"[source]({card['source']})" if card["source"] else ""

        lines.append(f"### {emoji} {card['title']}")
        lines.append(f"**{role_label}** · {source_link}\n")

        if card["anchor"]:
            lines.append(f"*{card['anchor']}*\n")

        if card["key_content"]:
            lines.append("<details>")
            lines.append("<summary>Key content</summary>\n")
            lines.append(card["key_content"])
            lines.append("\n</details>\n")

    return "\n".join(lines)


def write_topic_page(meta: dict, all_meta: dict, cfg: dict) -> None:
    """Write a transformed topic page to wiki/content/topics/."""
    frontmatter = build_frontmatter(meta, cfg)
    related_section = build_related_section(meta, all_meta)
    reference_section = build_reference_section(meta["slug"])

    body = meta["body"]
    if body.startswith("---"):
        end = body.find("---", 3)
        if end != -1:
            body = body[end + 3:].lstrip("\n")

    content = frontmatter + "\n\n" + body
    if reference_section:
        content = content.rstrip() + "\n" + reference_section
    if related_section:
        content = content.rstrip() + "\n" + related_section

    ref_cards = load_reference_cards(meta["slug"])
    ref_info = f" ref={len(ref_cards)}" if ref_cards else ""

    out_path = TOPICS_DIR / f"{meta['slug']}.md"
    out_path.write_text(content, encoding="utf-8")
    print(f"  [topic] {meta['slug']}.md  educators={len(meta['educators'])} levels={meta['levels']}{ref_info}")


# ---------------------------------------------------------------------------
# Hub pages
# ---------------------------------------------------------------------------

def write_educator_pages(all_meta: dict, cfg: dict) -> None:
    educator_slugs = cfg["educator_slugs"]
    educator_bios = cfg.get("educator_bios", {})
    tracked = list(educator_slugs.keys())

    edu_topics: dict[str, list[dict]] = defaultdict(list)
    for meta in all_meta.values():
        for edu in meta["educators"]:
            if edu in tracked:
                edu_topics[edu].append(meta)

    for edu in tracked:
        topics = edu_topics.get(edu, [])
        slug = educator_slugs[edu]
        bio = educator_bios.get(edu, "")

        by_subject: dict[str, list[dict]] = defaultdict(list)
        for t in topics:
            by_subject[t["subject"]].append(t)

        subject_sections = []
        for subj, subj_topics in sorted(by_subject.items()):
            links = "\n".join(f"- [[topics/{t['slug']}|{t['title']}]]" for t in subj_topics)
            subject_sections.append(f"### {subj}\n\n{links}")

        topics_content = "\n\n".join(subject_sections) if subject_sections else "_No topics indexed yet._"

        content = f"""---
title: "{edu}"
tags:
  - "educator/{slug}"
---

# {edu}

{bio}

## Topics ({len(topics)})

{topics_content}
"""
        out_path = EDUCATORS_DIR / f"{slug}.md"
        out_path.write_text(content, encoding="utf-8")
        print(f"  [educator] {slug}.md  ({len(topics)} topics)")


def write_subject_pages(all_meta: dict, cfg: dict) -> None:
    subject_slugs = cfg["subject_slugs"]
    subject_descriptions = cfg.get("subject_descriptions", {})

    by_subject: dict[str, list[dict]] = defaultdict(list)
    for meta in all_meta.values():
        by_subject[meta["subject"]].append(meta)

    for subject, slug in subject_slugs.items():
        topics = by_subject.get(subject, [])
        description = subject_descriptions.get(subject, "")

        by_level: dict[str, list[dict]] = defaultdict(list)
        for t in topics:
            primary_level = t["levels"][0] if t["levels"] else "intermediate"
            by_level[primary_level].append(t)

        level_sections = []
        for level in ["beginner", "intermediate", "advanced"]:
            level_topics = by_level.get(level, [])
            if level_topics:
                links = "\n".join(f"- [[topics/{t['slug']}|{t['title']}]]" for t in level_topics)
                level_sections.append(f"### {level.title()}\n\n{links}")

        all_links = "\n".join(f"- [[topics/{t['slug']}|{t['title']}]]" for t in topics)
        levels_content = "\n\n".join(level_sections) if level_sections else all_links

        content = f"""---
title: "{subject}"
tags:
  - "subject/{slug}"
---

# {subject}

{description}

## Topics ({len(topics)})

{levels_content}
"""
        out_path = SUBJECTS_DIR / f"{slug}.md"
        out_path.write_text(content, encoding="utf-8")
        print(f"  [subject] {slug}.md  ({len(topics)} topics)")


def write_level_pages(all_meta: dict) -> None:
    LEVEL_DESCRIPTIONS = {
        "beginner": "No prior ML experience required. These topics build intuition through visuals, analogies, and hands-on code before introducing math.",
        "intermediate": "Comfortable with Python and basic ML concepts. These topics go deeper into architecture details, math, and implementation trade-offs.",
        "advanced": "Assumes strong ML foundations. These topics cover research papers, complex derivations, and cutting-edge techniques.",
    }

    by_level: dict[str, list[dict]] = defaultdict(list)
    for meta in all_meta.values():
        for level in meta["levels"]:
            by_level[level].append(meta)

    for level in ["beginner", "intermediate", "advanced"]:
        topics = by_level.get(level, [])
        desc = LEVEL_DESCRIPTIONS[level]

        by_subject: dict[str, list[dict]] = defaultdict(list)
        for t in topics:
            by_subject[t["subject"]].append(t)

        subject_sections = []
        for subj in sorted(by_subject.keys()):
            links = "\n".join(f"- [[topics/{t['slug']}|{t['title']}]]" for t in by_subject[subj])
            subject_sections.append(f"### {subj}\n\n{links}")

        content = f"""---
title: "{level.title()} Topics"
tags:
  - "level/{level}"
---

# {level.title()} Topics

{desc}

## {len(topics)} Topics

{chr(10).join(subject_sections)}
"""
        out_path = LEVELS_DIR / f"{level}.md"
        out_path.write_text(content, encoding="utf-8")
        print(f"  [level] {level}.md  ({len(topics)} topics)")


def write_index_page(all_meta: dict, cfg: dict) -> None:
    subject_slugs = cfg["subject_slugs"]
    educator_slugs = cfg["educator_slugs"]

    by_subject: dict[str, list[dict]] = defaultdict(list)
    for meta in all_meta.values():
        by_subject[meta["subject"]].append(meta)

    subject_rows = []
    for subject, slug in subject_slugs.items():
        count = len(by_subject.get(subject, []))
        subject_rows.append(f"| [[subjects/{slug}\\|{subject}]] | {count} |")

    educator_links = " · ".join(
        f"[[educators/{slug}\\|{edu}]]" for edu, slug in educator_slugs.items()
    )

    total_ref_cards = sum(len(load_reference_cards(slug)) for slug in all_meta)

    content = f"""---
title: "SocraticTutor Knowledge Base"
tags: []
---

# SocraticTutor Knowledge Base

A curated, interlinked library of AI and machine learning concepts — built by educators, for learners.

Browse **{len(all_meta)} topics** across **{len(subject_slugs)} subjects**, backed by **{total_ref_cards} additional depth sources** (papers, docs, code examples, benchmarks, deployment cases) curated from the best educators and researchers in the field.

---

## Browse by Subject

| Subject | Topics |
|---------|--------|
{chr(10).join(subject_rows)}

---

## Browse by Level

- [[levels/beginner|Beginner]] — Start here if you're new to ML
- [[levels/intermediate|Intermediate]] — Deepen your understanding
- [[levels/advanced|Advanced]] — Research-level depth

---

## Browse by Educator

{educator_links}

---

## How to Navigate

- **Graph view** (bottom right) — explore concept connections visually
- **Search** (top left) — find any topic instantly
- **Tags** — filter by subject, level, educator, or resource type
- **Backlinks** (right sidebar) — see what connects to each concept

---

> This wiki is the knowledge base that powers the [SocraticTutor](/) learning platform.
> Topics are curated from top educators and research papers, verified and enriched by our team.
"""
    out_path = WIKI_CONTENT / "index.md"
    out_path.write_text(content, encoding="utf-8")
    print(f"  [index] index.md")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    if not SOURCE_DIR.exists():
        print(f"ERROR: Source directory not found: {SOURCE_DIR}", file=sys.stderr)
        sys.exit(1)

    cfg = load_config()

    # Ensure output directories exist
    for d in [TOPICS_DIR, EDUCATORS_DIR, SUBJECTS_DIR, LEVELS_DIR]:
        d.mkdir(parents=True, exist_ok=True)

    source_files = sorted(SOURCE_DIR.glob("*.md"))
    print(f"Found {len(source_files)} topic files")

    print("\nParsing topics...")
    all_meta: dict[str, dict] = {}
    for path in source_files:
        meta = parse_topic(path, cfg)
        all_meta[meta["slug"]] = meta

    print(f"\nWriting {len(all_meta)} topic pages...")
    for meta in all_meta.values():
        write_topic_page(meta, all_meta, cfg)

    print(f"\nWriting educator hub pages...")
    write_educator_pages(all_meta, cfg)

    print(f"\nWriting subject hub pages...")
    write_subject_pages(all_meta, cfg)

    print(f"\nWriting level hub pages...")
    write_level_pages(all_meta)

    print(f"\nWriting index page...")
    write_index_page(all_meta, cfg)

    print(f"\nDone. {len(all_meta)} topics · {len(cfg['subject_slugs'])} subjects · {len(cfg['educator_slugs'])} educators")


if __name__ == "__main__":
    main()
