"""
End-to-end smoke test for the audience-aware enrichment pipeline.

Generates an outline for a practical, non-developer topic (Claude Skills),
verifies the course_profile is extracted correctly, runs enrichment on
1-2 lessons, and checks that:
  - Multimedia queries are generated
  - Audience-appropriate sources are found (deeplearning.ai, Anthropic docs, etc.)
  - Wiki staging writes go to .pending/ (not directly to tracked files)

Usage:
    cd backend
    PYTHONUNBUFFERED=1 uv run python scripts/test_staging_e2e.py
"""

import asyncio
import json
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
os.environ.setdefault("TESTING_PIPELINE", "1")

from app.services.course_generator import (
    generate_outline,
    ensure_wiki_coverage,
)
from app.services.wiki_downloader import _PENDING_DIR
from app.config import WIKI_DIR

W = 80
DIV = "=" * W

COURSE_PROMPT = """\
Create a short course on Claude Skills — how to create, configure, and use \
skills in Cursor IDE with Claude. Target audience: non-developer power users \
and knowledge workers who want to get the most out of Claude as a coding \
assistant. They are NOT ML engineers — they are people who use Claude daily \
for writing, analysis, and automation. Focus on practical, hands-on guidance \
with real examples. 2-3 modules, 2-3 lessons each."""


async def collect_sse(async_gen) -> list[dict]:
    events = []
    async for raw in async_gen:
        raw = raw.strip()
        if raw.startswith("data: "):
            try:
                events.append(json.loads(raw[6:]))
            except json.JSONDecodeError:
                pass
    return events


async def main():
    print(f"\n{DIV}")
    print("  AUDIENCE-AWARE PIPELINE SMOKE TEST")
    print(f"  Topic: Claude Skills (practical, non-developer)")
    print(f"{DIV}\n")

    # ------------------------------------------------------------------
    # Stage 1: Generate outline — verify course_profile extraction
    # ------------------------------------------------------------------
    print(f"{'─' * W}")
    print("  STAGE 1: Outline Generation + course_profile Extraction")
    print(f"{'─' * W}\n")

    t0 = time.time()
    events = await collect_sse(generate_outline(COURSE_PROMPT, "prompt"))
    elapsed = time.time() - t0

    outline = None
    for ev in events:
        if ev.get("type") == "outline":
            outline = ev["data"]
        elif ev.get("type") == "error":
            print(f"  [FAIL] Outline generation error: {ev['message']}")
            sys.exit(1)

    if not outline:
        print("  [FAIL] No outline produced")
        sys.exit(1)

    profile = outline.get("course_profile", {})
    modules = outline.get("modules", [])
    all_lessons = []
    for mod in modules:
        for les in mod.get("lessons", []):
            all_lessons.append(les)

    print(f"  Title: {outline.get('title', '?')}")
    print(f"  Level: {outline.get('level', '?')}")
    print(f"  Modules: {len(modules)}, Lessons: {len(all_lessons)}")
    print(f"  Time: {elapsed:.1f}s")
    print()
    print(f"  course_profile:")
    print(f"    audience: {profile.get('audience', '(missing)')}")
    print(f"    tone: {profile.get('tone', '(missing)')}")
    print(f"    source_types: {profile.get('source_types', '(missing)')}")
    print(f"    deprioritize: {profile.get('deprioritize', '(missing)')}")
    print(f"    vendor: {profile.get('vendor', '(missing)')}")
    print()

    # Checks
    checks_passed = 0
    checks_total = 0

    def check(name, condition, detail=""):
        nonlocal checks_passed, checks_total
        checks_total += 1
        sym = "✓" if condition else "✗"
        status = "PASS" if condition else "FAIL"
        msg = f"  [{sym}] {name}"
        if detail:
            msg += f" — {detail}"
        print(msg)
        if condition:
            checks_passed += 1

    check("course_profile extracted", bool(profile))
    check("audience is non-developer/practical",
          profile.get("audience") and any(
              kw in profile.get("audience", "").lower()
              for kw in ("non-developer", "power user", "knowledge worker",
                         "non-technical", "practical", "business", "daily")
          ),
          profile.get("audience", "")[:80])
    check("tone is practical",
          profile.get("tone") in ("practical-hands-on",),
          profile.get("tone", ""))
    check("vendor is Anthropic or Claude-related",
          profile.get("vendor") and any(
              kw in profile.get("vendor", "").lower()
              for kw in ("anthropic", "claude", "cursor")
          ),
          profile.get("vendor", ""))
    check("source_types includes tutorials or videos",
          any(s in (profile.get("source_types") or [])
              for s in ("tutorials", "videos", "official-docs")),
          str(profile.get("source_types", [])))
    check("deprioritizes papers",
          "papers" in (profile.get("deprioritize") or []),
          str(profile.get("deprioritize", [])))

    print()
    print("  Outline structure:")
    for mod in modules:
        print(f"    {mod.get('title', '?')}")
        for les in mod.get("lessons", []):
            concepts = les.get("concepts", [])
            print(f"      - {les.get('title', '?')} ({len(concepts)} concepts: {', '.join(concepts[:4])}...)")
    print()

    # ------------------------------------------------------------------
    # Stage 2: Enrichment on first 2 lessons — verify queries + sources
    # ------------------------------------------------------------------
    print(f"{'─' * W}")
    print("  STAGE 2: Coverage Assessment + Enrichment (2 lessons)")
    print(f"{'─' * W}\n")

    test_lessons = all_lessons[:2]
    print(f"  Testing {len(test_lessons)} lessons:")
    for les in test_lessons:
        print(f"    - {les.get('title', '?')}")
    print()

    # Clear any existing pending items for clean test
    existing_pending = list(_PENDING_DIR.glob("*.json")) if _PENDING_DIR.exists() else []

    t0 = time.time()
    assessment = await ensure_wiki_coverage(
        test_lessons,
        course_description=outline.get("description", ""),
        enrich=True,
        course_profile=profile,
    )
    elapsed = time.time() - t0

    fully = assessment.get("fully_covered", [])
    research = assessment.get("needs_research", [])
    no_match = assessment.get("no_match", [])

    print(f"  Enrichment completed in {elapsed:.1f}s")
    print(f"  Fully covered: {len(fully)}")
    print(f"  Needs research (enriched): {len(research)}")
    print(f"  No match (bootstrapped): {len(no_match)}")
    print()

    # Show enrichment details
    for entry in research + no_match:
        les = entry["lesson"]
        topics = entry.get("topics", entry.get("resolved_topics", []))
        verdicts = entry.get("concept_verdicts", {})
        thin = [c for c, v in verdicts.items()
                if isinstance(v, dict) and v.get("verdict") in ("thin", "missing")]
        print(f"  Lesson: {les.get('title', '?')}")
        print(f"    Topics resolved: {list(topics) if isinstance(topics, set) else topics}")
        if thin:
            print(f"    Gaps: {', '.join(thin[:5])}")
        print()

    # Check pending items
    new_pending = []
    if _PENDING_DIR.exists():
        all_now = set(f.name for f in _PENDING_DIR.glob("*.json"))
        old_names = set(f.name for f in existing_pending)
        new_pending = sorted(all_now - old_names)

    print(f"  New pending items: {len(new_pending)}")
    for name in new_pending:
        item = json.loads((_PENDING_DIR / name).read_text())
        print(f"    [{item['type']}] {item['topic_slug']}")
        if item["type"] == "new_topic":
            print(f"      concepts: {item['data'].get('concepts', [])}")
        elif item["type"] == "resource_page":
            print(f"      sources: {item['data'].get('source_count', '?')}")
        elif item["type"] == "structural_note":
            print(f"      concept: {item['data'].get('concept', '?')}")
    print()

    check("Enrichment completed", len(research) + len(no_match) + len(fully) > 0)
    check("Pending items created (not direct writes)",
          len(new_pending) > 0 or len(fully) == len(test_lessons),
          f"{len(new_pending)} pending items")

    # Check what sources were downloaded to topic directories
    topics_dir = WIKI_DIR / "resources" / "by-topic"
    print()
    print("  Downloaded sources (checking for audience-appropriate content):")
    multimedia_found = False
    video_stubs_found = 0
    video_stubs_with_transcript = 0
    practitioner_sources = []
    for entry in research + no_match:
        topics = entry.get("resolved_topics", entry.get("topics", set()))
        if isinstance(topics, list):
            topics = set(topics)
        for topic in topics:
            topic_dir = topics_dir / topic
            if topic_dir.is_dir():
                source_files = list(topic_dir.glob("*.md"))
                print(f"\n    Topic: {topic} ({len(source_files)} source files)")
                for sf in source_files[:12]:
                    text = sf.read_text(errors="ignore")
                    lines = text.split("\n")[:12]
                    url = title = audience = src_type = yt_id = via = ""
                    for line in lines:
                        if line.startswith("# Source:"):
                            url = line.replace("# Source:", "").strip()
                        elif line.startswith("# Title:"):
                            title = line.replace("# Title:", "").strip()
                        elif line.startswith("# Audience:"):
                            audience = line.replace("# Audience:", "").strip()
                        elif line.startswith("# Type:"):
                            src_type = line.replace("# Type:", "").strip()
                        elif line.startswith("# youtube_id:"):
                            yt_id = line.replace("# youtube_id:", "").strip()
                        elif line.startswith("# Via:"):
                            via = line.replace("# Via:", "").strip()
                    short_url = url[:60] + "..." if len(url) > 60 else url
                    print(f"      {sf.name}")
                    print(f"        URL: {short_url}")
                    if title:
                        print(f"        Title: {title[:60]}")
                    if src_type:
                        print(f"        Type: {src_type}")
                    if yt_id:
                        print(f"        youtube_id: {yt_id}")
                    if via:
                        print(f"        Via: {via}")
                    if audience:
                        print(f"        Audience: {audience}")

                    # Video stub detection
                    if src_type == "video" or via == "video-metadata":
                        video_stubs_found += 1
                        has_transcript = "## Transcript" in text
                        if has_transcript:
                            video_stubs_with_transcript += 1
                            word_count = len(text.split())
                            print(f"        Transcript: YES ({word_count} words)")
                        else:
                            print(f"        Transcript: NO")

                    if any(kw in url.lower() for kw in (
                        "youtube.com", "youtu.be", "deeplearning.ai",
                        "video", "tutorial"
                    )):
                        multimedia_found = True
                    if any(kw in url.lower() for kw in (
                        "anthropic", "claude", "cursor", "deeplearning",
                        "docs.", "tutorial"
                    )):
                        practitioner_sources.append(url)

    print()
    check("Multimedia/video sources discovered", multimedia_found,
          "YouTube or deeplearning.ai content found" if multimedia_found
          else "No multimedia sources found")
    check("Video stubs created (metadata path)",
          video_stubs_found > 0,
          f"{video_stubs_found} video stubs ({video_stubs_with_transcript} with transcript)")
    check("Practitioner-relevant sources found",
          len(practitioner_sources) > 0,
          f"{len(practitioner_sources)} sources from Anthropic/Claude/deeplearning/tutorials")

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    print(f"\n{DIV}")
    print(f"  RESULTS: {checks_passed}/{checks_total} checks passed")
    print(f"{DIV}\n")

    if checks_passed < checks_total:
        failed = checks_total - checks_passed
        print(f"  {failed} check(s) need attention — review output above.\n")
    else:
        print("  All checks passed!\n")


if __name__ == "__main__":
    asyncio.run(main())
