#!/usr/bin/env python3
"""
Targeted reference track test — run the full reference pipeline for a
single lesson, then regenerate the KB and compare old vs new.

Usage:
    cd backend
    PYTHONUNBUFFERED=1 python3 ../scripts/test_reference_track.py alignment-rlhf
    PYTHONUNBUFFERED=1 python3 ../scripts/test_reference_track.py self-attention
    PYTHONUNBUFFERED=1 python3 ../scripts/test_reference_track.py --list

What it does:
    1. Fetches the lesson from DB (needs existing lesson with KB)
    2. Resolves topic slugs for the lesson's concepts
    3. Runs the reference track: needs analysis → search → curate → audit → download
    4. Regenerates the KB (now with blended ref+ped sources)
    5. Dumps old KB and new KB to scripts/kb_compare_old.md / kb_compare_new.md
    6. Prints a summary of what changed

No student notes, no full pipeline — just reference enrichment + KB regen.
"""

import asyncio
import json
import os
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
BACKEND_DIR = REPO_ROOT / "backend"
BACKEND_ENV = BACKEND_DIR / ".env"
SCRIPTS_DIR = Path(__file__).parent

OLD_PATH = SCRIPTS_DIR / "kb_compare_old.md"
NEW_PATH = SCRIPTS_DIR / "kb_compare_new.md"

# Bootstrap
def _load_env():
    if BACKEND_ENV.exists():
        for line in BACKEND_ENV.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                os.environ.setdefault(k.strip(), v.strip())


_load_env()
sys.path.insert(0, str(BACKEND_DIR))

# Configure logging so all pipeline logger.info() calls are visible
import logging
logging.basicConfig(
    level=logging.INFO,
    format="  %(name)s | %(message)s",
    stream=sys.stdout,
)
# Quiet down noisy libraries
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)
logging.getLogger("openai").setLevel(logging.WARNING)

LOG_PATH = SCRIPTS_DIR / "reference_track_log.md"


def _fetch_lesson(slug: str):
    from sqlmodel import Session, select
    from app.db import engine
    from app.models.learning import Lesson
    with Session(engine) as session:
        stmt = select(Lesson).where(Lesson.slug == slug)
        return session.exec(stmt).first()


def _list_lessons():
    from sqlmodel import Session, select
    from app.db import engine
    from app.models.learning import Lesson
    with Session(engine) as session:
        stmt = select(Lesson).where(Lesson.reference_kb.isnot(None))  # type: ignore
        lessons = session.exec(stmt).all()
    rows = [(l.slug, len((l.reference_kb or "").split())) for l in lessons if l.reference_kb]
    rows.sort(key=lambda x: x[1], reverse=True)
    print(f"\n{'Slug':<45} {'KB words':>10}")
    print("-" * 57)
    for slug, words in rows:
        print(f"{slug:<45} {words:>10,}")
    print(f"\nTotal: {len(rows)} lessons with reference KB")
    print("\nSuggested test targets: alignment-rlhf, self-attention, rag-retrieval\n")


async def _run(slug: str) -> None:
    print(f"\n{'=' * 70}")
    print(f"  REFERENCE TRACK TEST: {slug}")
    print(f"{'=' * 70}\n")

    # Step 1: Fetch lesson
    print("Step 1: Fetching lesson from DB...")
    lesson = _fetch_lesson(slug)
    if not lesson:
        print(f"ERROR: lesson '{slug}' not found. Use --list to see available lessons.")
        sys.exit(1)

    concepts = json.loads(lesson.concepts) if isinstance(lesson.concepts, str) else (lesson.concepts or [])
    old_kb = lesson.reference_kb or ""
    print(f"  Title: {lesson.title}")
    print(f"  Concepts: {concepts}")
    print(f"  Existing KB: {len(old_kb.split())} words")

    # Step 2: Resolve topic slugs
    print("\nStep 2: Resolving topic slugs...")
    from app.services.course_generator import resolve_topics_llm, load_wiki_context

    resolved = await resolve_topics_llm(
        concepts, lesson_title=lesson.title,
        lesson_summary=lesson.summary or "",
    )
    topic_slugs = resolved["topic_slugs"]
    print(f"  Topics: {sorted(topic_slugs)}")

    # Show existing pedagogy sources
    ped_ctx = load_wiki_context(concepts, topic_slugs=topic_slugs)
    ped_count = sum(len(v) for v in ped_ctx.get("source_content", {}).values())
    print(f"  Pedagogy sources: {ped_count}")

    # Show existing reference sources (before enrichment)
    ref_ctx_before = load_wiki_context(concepts, topic_slugs=topic_slugs, track="reference")
    ref_count_before = sum(len(v) for v in ref_ctx_before.get("source_content", {}).values())
    print(f"  Reference sources (before): {ref_count_before}")

    # Step 3: Run reference track enrichment — broken into substeps for auditing
    print(f"\n{'─' * 70}")
    print("Step 3: Running reference track enrichment...")
    print(f"{'─' * 70}")

    from app.services.course_enricher import assess_reference_needs, _search
    from app.services.wiki_downloader import (
        curate_reference_sources, audit_reference_curation,
        _get_existing_source_details, get_existing_source_urls,
        enrich_wiki_topic, save_proposals, save_curation_report,
    )

    target_topic = sorted(topic_slugs)[0] if topic_slugs else slug
    t0 = time.time()
    audit_log: list[str] = []
    audit_log.append(f"# Reference Track Audit Log: {lesson.title}")
    audit_log.append(f"*Slug: `{slug}` | Topic: `{target_topic}` | "
                     f"Date: {time.strftime('%Y-%m-%d %H:%M')}*\n")

    # 3a: Assess reference needs
    print("\n  3a. Assessing reference needs (LLM call)...")
    needs_result = await assess_reference_needs(
        target_topic, lesson.title, concepts,
        lesson_summary=lesson.summary or "",
    )
    typed_needs = needs_result["needs"]
    all_queries = needs_result["all_queries"]

    print(f"      Identified {len(typed_needs)} needs, {len(all_queries)} queries")
    audit_log.append("## Step 3a: Reference Needs Analysis")
    audit_log.append(f"**Reasoning:** {needs_result.get('reasoning', '')}\n")
    for i, need in enumerate(typed_needs, 1):
        print(f"      [{need['need_type']}] {need.get('description', '')[:70]}")
        for q in need.get("search_queries", []):
            print(f"        → query: \"{q}\"")
        audit_log.append(f"### Need {i}: {need['need_type']}")
        audit_log.append(f"**Description:** {need.get('description', '')}")
        audit_log.append(f"**Queries:** {', '.join(need.get('search_queries', []))}\n")

    if not typed_needs:
        print("      No needs identified — nothing to search for.")
        ref_result = {
            "needs": 0, "queries": 0, "searches": 0,
            "picks": 0, "promotions": 0, "downloads": 0,
            "unfilled_needs": [],
        }
    else:
        # 3b: Run searches
        print(f"\n  3b. Running {len(all_queries)} searches...")
        search_results_by_need: dict[str, list[dict]] = {}
        total_searches = 0
        total_citations = 0
        audit_log.append("## Step 3b: Search Results")
        for need in typed_needs:
            need_type = need["need_type"]
            need_results: list[dict] = []
            for query in need.get("search_queries", []):
                result = await _search(query)
                need_results.append(result)
                total_searches += 1
                n_citations = len(result.get("citations", []))
                total_citations += n_citations
                print(f"      [{need_type}] \"{query[:50]}\" → {n_citations} citations")
                audit_log.append(f"- **[{need_type}]** `{query}` → {n_citations} citations")
                if result.get("error"):
                    print(f"        ERROR: {result['error']}")
                    audit_log.append(f"  - ERROR: {result['error']}")
            search_results_by_need[need_type] = need_results

        print(f"      Total: {total_searches} searches, {total_citations} citations")
        audit_log.append(f"\n**Total:** {total_searches} searches, {total_citations} citations\n")

        # 3c: Curate
        print(f"\n  3c. Curating reference sources (LLM call)...")
        existing_urls = get_existing_source_urls(target_topic)
        curation = await curate_reference_sources(
            lesson.title, typed_needs, search_results_by_need,
            existing_urls, topic_slug=target_topic,
        )

        picks = curation["picks"]
        near_misses = curation.get("near_misses", [])
        unfilled_needs = curation.get("unfilled_needs", [])
        all_candidates = curation["all_candidates"]

        print(f"      Picks: {len(picks)} | Near-misses: {len(near_misses)} | "
              f"Unfilled: {len(unfilled_needs)} | Candidates: {len(all_candidates)}")

        audit_log.append("## Step 3c: Curation Decisions")
        audit_log.append(f"**Reasoning:** {curation.get('reasoning', '')}\n")
        if picks:
            audit_log.append("### Picks")
            for p in picks:
                print(f"      ADD [{p.get('role', '?')}] {p['url'][:65]}")
                print(f"          anchor: {p.get('anchor', '?')[:80]}")
                audit_log.append(f"- **[{p.get('role', '?')}]** [{p.get('title', 'Untitled')}]({p['url']})")
                audit_log.append(f"  - Need: {p.get('need_type', '?')}")
                audit_log.append(f"  - Anchor: {p.get('anchor', '?')}")
                audit_log.append(f"  - Why: {p.get('why', '')}")
        if near_misses:
            audit_log.append("\n### Near-Misses")
            for nm in near_misses:
                print(f"      NEAR-MISS: {nm.get('title', nm.get('url', '?'))[:55]}")
                print(f"          reason: {nm.get('why_not', '')[:80]}")
                audit_log.append(f"- {nm.get('title', nm.get('url', '?'))}: {nm.get('why_not', '')}")
        if unfilled_needs:
            audit_log.append("\n### Unfilled Needs (→ Ramps)")
            for un in unfilled_needs:
                print(f"      UNFILLED [{un.get('need_type', '?')}] {un.get('description', '')[:55]}")
                if un.get("search_hint"):
                    print(f"          ramp: \"{un['search_hint']}\"")
                audit_log.append(f"- [{un.get('need_type', '?')}] {un.get('description', '')}")
                if un.get("search_hint"):
                    audit_log.append(f"  - Search hint: `{un['search_hint']}`")
        audit_log.append("")

        # 3d: Audit
        print(f"\n  3d. Reviewer audit (LLM call)...")
        existing_details = _get_existing_source_details(target_topic)

        candidates_by_url: dict[str, dict] = {}
        for need_type, results in search_results_by_need.items():
            for r in results:
                snippet = r.get("content", "")[:1200]
                for c in r.get("citations", []):
                    url = c.get("url", "") if isinstance(c, dict) else str(c)
                    t = c.get("title", "") if isinstance(c, dict) else ""
                    if url and url not in existing_urls and url not in candidates_by_url:
                        candidates_by_url[url] = {
                            "url": url, "title": t,
                            "snippet": snippet, "needs": [need_type],
                        }
                    elif url in candidates_by_url:
                        if need_type not in candidates_by_url[url].get("needs", []):
                            candidates_by_url[url]["needs"].append(need_type)

        audit = await audit_reference_curation(
            lesson.title, curation, candidates_by_url, existing_details,
        )

        promotions = audit.get("promotions", [])
        verdict = audit.get("verdict", "good")
        summary = audit.get("summary", "")
        print(f"      Verdict: {verdict} — {summary[:100]}")

        audit_log.append("## Step 3d: Reviewer Audit")
        audit_log.append(f"**Verdict:** {verdict}")
        audit_log.append(f"**Summary:** {summary}\n")
        if promotions:
            print(f"      Promotions: {len(promotions)}")
            for promo in promotions:
                print(f"      PROMOTE [{promo.get('role', '?')}] {promo['url'][:65]}")
                print(f"              anchor: {promo.get('anchor', '?')[:80]}")
                audit_log.append(f"- PROMOTE [{promo.get('role', '?')}] "
                                 f"[{promo.get('title', 'Untitled')}]({promo['url']})")
                audit_log.append(f"  - Anchor: {promo.get('anchor', '?')}")
                audit_log.append(f"  - Why: {promo.get('why', '')}")
            picks.extend(promotions)
        audit_log.append("")

        # 3e: Download
        print(f"\n  3e. Downloading {len(picks)} sources to reference/...")
        dl_result = None
        downloads = 0
        if picks:
            sources_to_dl = [{"url": p["url"], "title": p.get("title", "")} for p in picks]
            dl_result = await enrich_wiki_topic(
                target_topic, sources_to_dl, extract_images=False, track="reference",
            )
            downloads = dl_result.get("saved", 0)
            print(f"      Saved: {dl_result.get('saved', 0)} | "
                  f"Skipped: {dl_result.get('skipped', 0)} | "
                  f"Failed: {dl_result.get('failed', 0)}")
            audit_log.append("## Step 3e: Downloads")
            audit_log.append(f"Saved: {dl_result.get('saved', 0)}, "
                             f"Skipped: {dl_result.get('skipped', 0)}, "
                             f"Failed: {dl_result.get('failed', 0)}\n")
            for d in dl_result.get("details", []):
                status = "SAVED" if d.get("saved") else ("EXISTS" if d.get("reason") == "already exists" else "FAILED")
                audit_log.append(f"- [{status}] {d.get('path', d.get('url', '?'))[:80]}")
        else:
            print("      No sources to download.")
            audit_log.append("## Step 3e: Downloads\nNo sources to download.\n")

        # 3f: Save audit trail
        print(f"\n  3f. Saving proposals + curation report...")
        if all_candidates:
            save_proposals(
                target_topic,
                [{"url": c.get("url", ""), "title": c.get("title", ""),
                  "need_type": c.get("need_type", "")} for c in all_candidates],
                run_label=f"reference-track:{lesson.title}",
                track="reference",
            )
        save_curation_report(
            target_topic, lesson.title,
            curation=curation, audit=audit,
            existing_details=existing_details,
            download_result=dl_result,
            track="reference",
        )

        # Save ramps
        if unfilled_needs:
            wiki_dir = Path(os.environ.get("CONTENT_DIR", str(REPO_ROOT / "content"))).resolve() / "pedagogy-wiki" / "resources" / "by-topic"
            ramps_dir = wiki_dir / target_topic / "reference"
            ramps_dir.mkdir(parents=True, exist_ok=True)
            ramps_path = ramps_dir / "ramps.json"
            ramps_path.write_text(json.dumps(unfilled_needs, indent=2))
            print(f"      Saved {len(unfilled_needs)} ramps to {ramps_path}")

        # 3g: Extract reference cards
        print(f"\n  3g. Extracting reference cards...")
        from app.services.wiki_downloader import extract_cards_for_sources

        cards_result = await extract_cards_for_sources(
            target_topic, picks,
            lesson_title=lesson.title,
            concepts=concepts,
        )
        cards_extracted = cards_result.get("extracted", 0)
        cards_skipped = cards_result.get("skipped", 0)
        cards_failed = cards_result.get("failed", 0)
        print(f"      Extracted: {cards_extracted} | Skipped: {cards_skipped} | "
              f"Failed: {cards_failed}")

        audit_log.append("## Step 3g: Card Extraction\n")
        audit_log.append(f"Extracted: {cards_extracted}, Skipped: {cards_skipped}, "
                         f"Failed: {cards_failed}\n")

        ref_result = {
            "needs": len(typed_needs),
            "queries": len(all_queries),
            "searches": total_searches,
            "picks": len(curation["picks"]),
            "promotions": len(promotions),
            "downloads": downloads,
            "cards_extracted": cards_extracted,
            "unfilled_needs": unfilled_needs,
            "reasoning": needs_result.get("reasoning", ""),
        }

    elapsed = time.time() - t0
    print(f"\n  Enrichment completed in {elapsed:.1f}s")

    # Show reference sources after enrichment (cards preferred over raw)
    ref_ctx_after = load_wiki_context(concepts, topic_slugs=topic_slugs, track="reference")
    ref_count_after = sum(len(v) for v in ref_ctx_after.get("source_content", {}).values())
    print(f"\n  Reference sources (after): {ref_count_after} "
          f"(+{ref_count_after - ref_count_before} new)")

    # List the reference sources (showing cards vs raw)
    if ref_ctx_after.get("source_content"):
        print("\n  Reference library:")
        for topic_sources in ref_ctx_after.get("source_content", {}).values():
            for src in topic_sources:
                is_card = src["file"].endswith(".card.md")
                tag = "CARD" if is_card else "RAW"
                first_lines = src["content"].split("\n", 5)
                source_line = next(
                    (l for l in first_lines if l.startswith("# Source:") or l.startswith("# Card:")),
                    src["file"],
                )
                words = len(src["content"].split())
                print(f"    [{tag}] {source_line.replace('# Source: ', '').replace('# Card: ', '')} ({words}w)")

    # Step 4: Regenerate KB with blended sources
    print(f"\n{'─' * 70}")
    print("Step 4: Regenerating reference KB (with blended sources)...")
    print(f"{'─' * 70}\n")

    from app.services.course_generator import generate_reference_kb_from_wiki

    lesson_dict = {
        "title": lesson.title,
        "slug": lesson.slug,
        "summary": lesson.summary or "",
        "concepts": concepts,
    }

    max_attempts = 2
    for attempt_num in range(1, max_attempts + 1):
        t1 = time.time()
        new_kb = ""
        async for event_str in generate_reference_kb_from_wiki([lesson_dict], existing_kb={}):
            if not event_str.strip().startswith("data: "):
                continue
            try:
                evt = json.loads(event_str.strip()[6:])
                etype = evt.get("type", "")
                if etype == "progress":
                    print(f"    [SSE] progress: status={evt.get('status')} words={evt.get('word_count')}")
                elif etype == "wiki_kb_complete":
                    print(f"    [SSE] complete: total_words={evt.get('total_words')} gaps={len(evt.get('gaps', []))}")
                elif etype == "reference_kb":
                    kb_data = evt.get("data", {})
                    print(f"    [SSE] reference_kb: keys={list(kb_data.keys())} looking_for={lesson.slug}")
                    new_kb = kb_data.get(lesson.slug, "")
            except (json.JSONDecodeError, KeyError) as e:
                print(f"    [SSE] PARSE ERROR: {type(e).__name__}: {e}")

        elapsed_kb = time.time() - t1
        print(f"  KB regenerated in {elapsed_kb:.1f}s")
        print(f"  New KB: {len(new_kb.split())} words")

        if new_kb:
            break
        if attempt_num < max_attempts:
            print(f"  WARNING: KB empty on attempt {attempt_num}, retrying...")
        else:
            print("  WARNING: new KB came back empty after all attempts!")
            return

    # Step 5: Dump comparison files
    print(f"\n{'─' * 70}")
    print("Step 5: Writing comparison files...")
    print(f"{'─' * 70}\n")

    mode = "blended (ref+ped)" if ref_count_after > 0 else "pedagogy-only fallback"
    header = (
        f"# {lesson.title}\n"
        f"*Slug: `{slug}`*\n\n"
        f"**Sources:** {ped_count} pedagogy, {ref_count_after} reference — *{mode}*\n\n"
    )

    OLD_PATH.write_text(header + "---\n\n" + old_kb)
    NEW_PATH.write_text(header + "---\n\n" + new_kb)

    print(f"  Old KB → {OLD_PATH}  ({len(old_kb.split())} words)")
    print(f"  New KB → {NEW_PATH}  ({len(new_kb.split())} words)")

    # Step 6: Write audit log
    print(f"\n{'─' * 70}")
    print("Step 6: Writing audit log...")
    print(f"{'─' * 70}\n")

    audit_log.append("## Step 4: KB Regeneration")
    audit_log.append(f"- Old KB: {len(old_kb.split())} words")
    audit_log.append(f"- New KB: {len(new_kb.split())} words")
    audit_log.append(f"- Context mode: {mode}")
    audit_log.append(f"- Pedagogy sources: {ped_count}")
    audit_log.append(f"- Reference sources: {ref_count_before} → {ref_count_after}\n")

    if ref_ctx_after.get("source_content"):
        audit_log.append("### Reference Sources Used")
        for topic_sources in ref_ctx_after.get("source_content", {}).values():
            for src in topic_sources:
                first_lines = src["content"].split("\n", 5)
                source_line = next(
                    (l for l in first_lines if l.startswith("# Source:")), src["file"],
                )
                words = len(src["content"].split())
                audit_log.append(f"- {source_line.replace('# Source: ', '')} ({words}w)")
        audit_log.append("")

    audit_log.append(f"---\n*Total time: {time.time() - t0:.1f}s*")

    LOG_PATH.write_text("\n".join(audit_log))
    print(f"  Audit log → {LOG_PATH}")

    # Summary
    print(f"\n{'=' * 70}")
    print("  SUMMARY")
    print(f"{'=' * 70}\n")
    print(f"  Lesson:             {lesson.title}")
    print(f"  Pedagogy sources:   {ped_count}")
    print(f"  Reference sources:  {ref_count_before} → {ref_count_after} "
          f"(+{ref_count_after - ref_count_before})")
    print(f"  Old KB words:       {len(old_kb.split())}")
    print(f"  New KB words:       {len(new_kb.split())}")
    print(f"  Context mode:       {mode}")
    print(f"  Total time:         {time.time() - t0:.1f}s")
    print(f"\n  Output files:")
    print(f"    {OLD_PATH.name}              — old KB (from DB)")
    print(f"    {NEW_PATH.name}              — new KB (with reference sources)")
    print(f"    {LOG_PATH.name}   — full audit trail of every decision")
    print()


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = [a for a in sys.argv[1:] if a.startswith("--")]

    if "--list" in flags:
        _list_lessons()
        return

    if not args:
        print("Usage: python3 scripts/test_reference_track.py <lesson-slug>")
        print("       python3 scripts/test_reference_track.py --list")
        sys.exit(1)

    asyncio.run(_run(args[0]))


if __name__ == "__main__":
    main()
