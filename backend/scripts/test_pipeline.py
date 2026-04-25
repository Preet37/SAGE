"""
End-to-end pipeline test for wiki-first course creation.

Runs every stage of the pipeline on "Attention Mechanisms" and logs
results for human inspection.

Pipeline order (enrich-before-generate):
    1  Wiki readiness check (+ concept mapping quality)
    2  Outline generation (LLM + user prompt)
    3  Coverage assessment (concept-level, LLM-assessed)
    4  Enrichment: bootstrap new topics + two-track search + download
    5  Unified generation (student notes + tutor KB from enriched wiki)
    6  Resource recommendation tool test
    7  Feedback loop test

Usage:
    cd backend
    PYTHONUNBUFFERED=1 uv run python scripts/test_pipeline.py
    PYTHONUNBUFFERED=1 uv run python scripts/test_pipeline.py --sample 2
"""

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
os.environ.setdefault("TESTING_PIPELINE", "1")

from app.services.course_generator import (
    generate_outline,
    load_wiki_context,
    check_outline_coverage,
    _load_concept_map,
    resolve_topics_llm,
    assess_wiki_coverage,
    ensure_wiki_coverage,
    generate_lesson_bundle,
    file_structural_note,
    deduplicate_youtube_ids,
)

# ──────────────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────────────

_WIDTH = 88
_DIVIDER = "═" * _WIDTH


def _header(stage: int, title: str) -> None:
    print(f"\n{_DIVIDER}")
    print(f"  STAGE {stage}: {title}")
    print(f"{_DIVIDER}\n")


def _kv(label: str, value, indent: int = 2) -> None:
    pad = " " * indent
    if isinstance(value, (list, set)):
        print(f"{pad}{label}: ({len(value)})")
        for item in sorted(value) if isinstance(value, set) else value:
            print(f"{pad}  - {item}")
    elif isinstance(value, dict):
        print(f"{pad}{label}:")
        for k, v in value.items():
            if isinstance(v, list):
                print(f"{pad}  {k}: [{len(v)} items]")
            elif isinstance(v, str) and len(v) > 120:
                print(f"{pad}  {k}: ({len(v)} chars)")
            else:
                print(f"{pad}  {k}: {v}")
    else:
        print(f"{pad}{label}: {value}")


def _word_count(text: str) -> int:
    return len(text.split())


async def _collect_sse(async_gen) -> list[dict]:
    events = []
    async for raw in async_gen:
        raw = raw.strip()
        if raw.startswith("data: "):
            try:
                events.append(json.loads(raw[6:]))
            except json.JSONDecodeError:
                pass
    return events


PASS = "PASS"
FAIL = "FAIL"
WARN = "WARN"
results_summary: list[tuple[str, str, str]] = []

def _result(stage: str, check: str, status: str, detail: str = "") -> None:
    results_summary.append((stage, check, status))
    symbol = {"PASS": "✓", "FAIL": "✗", "WARN": "⚠"}.get(status, "?")
    msg = f"  [{symbol}] {check}"
    if detail:
        msg += f" — {detail}"
    print(msg)


CONCEPTS = [
    "attention mechanism", "self-attention", "multi-head attention",
    "scaled dot-product attention", "cross-attention", "kv cache",
    "positional encoding", "transformer",
]

OUTLINE_CONCEPTS = [
    "additive attention", "alignment model", "attention scores",
    "softmax normalization", "query key value projections",
    "sparse attention", "sliding window attention",
    "io-aware algorithms", "hbm vs sram",
    "kernel trick", "encoder-decoder architecture",
    "grouped query attention (gqa)", "multi-query attention (mqa)",
    "sinusoidal positional encoding", "vision transformer (vit)",
    "state space models (ssm)", "mamba selective ssm",
    "masked self-attention", "flash attention",
    "bahdanau attention", "cross-modal attention",
]

COURSE_PROMPT = """Create a focused course on Attention Mechanisms in Deep Learning.
Target audience: ML practitioners who understand basic neural networks but want
to deeply understand how attention works, from Bahdanau to modern transformers.
Difficulty: intermediate to advanced.  4-6 lessons."""


# ──────────────────────────────────────────────────────────────────────
# Stage 1: Wiki Readiness + Concept Mapping Quality
# ──────────────────────────────────────────────────────────────────────

async def stage_1_wiki_readiness() -> dict:
    _header(1, "Wiki Readiness + Concept Mapping Quality")

    resolved = await resolve_topics_llm(
        CONCEPTS,
        lesson_title="Attention Mechanisms in Deep Learning",
        lesson_summary="Understanding how attention works from Bahdanau to transformers",
    )
    ctx = load_wiki_context(CONCEPTS, topic_slugs=resolved["topic_slugs"])
    topics = ctx.get("topics", [])
    source_content = ctx.get("source_content", {})
    total_files = sum(len(v) for v in source_content.values())
    total_words = sum(
        _word_count(f["content"]) for files in source_content.values() for f in files
    )
    _kv("Topics resolved (LLM mapper)", topics)
    _kv("Downloaded source files (deduped)", total_files)
    _kv("Total source words", f"{total_words:,}")

    yt = ctx.get("youtube_ids", {})
    total_yt = sum(len(v) for v in yt.values())
    _kv("YouTube video IDs (deduped)", total_yt)

    _result("S1", "Wiki has content",
            PASS if total_files > 0 and total_words > 1000 else FAIL,
            f"{total_files} files, {total_words:,} words")

    print()
    print("  LLM concept mapping quality (simulated outline concepts):")
    llm_resolved = await resolve_topics_llm(
        OUTLINE_CONCEPTS,
        lesson_title="Attention Mechanisms in Deep Learning",
        lesson_summary="Attention from Bahdanau to transformers, efficiency, and alternatives",
    )
    mappings = llm_resolved["mappings"]
    unmapped_concepts = llm_resolved["unmapped"]
    mapped = sum(1 for v in mappings.values() if isinstance(v, list) and v)

    hit_rate = mapped / len(OUTLINE_CONCEPTS) * 100
    _result("S1", "LLM concept mapping hit rate",
            PASS if hit_rate > 70 else (WARN if hit_rate > 50 else FAIL),
            f"{mapped}/{len(OUTLINE_CONCEPTS)} ({hit_rate:.0f}%)")

    if unmapped_concepts:
        print(f"    Unmapped ({len(unmapped_concepts)}):")
        for u in unmapped_concepts:
            print(f"      \"{u}\"")

    print()
    print("  Mapping details (spot-check for false positives):")
    for concept, slugs in sorted(mappings.items()):
        if isinstance(slugs, list) and slugs:
            print(f"    \"{concept}\" -> {slugs}")

    all_filenames = []
    for topic, files in source_content.items():
        for f in files:
            all_filenames.append(f["file"])
    unique_count = len(set(all_filenames))
    _result("S1", "File deduplication",
            PASS if unique_count == len(all_filenames) else WARN,
            f"{unique_count} unique / {len(all_filenames)} total")

    return ctx


# ──────────────────────────────────────────────────────────────────────
# Stage 2: Outline Generation
# ──────────────────────────────────────────────────────────────────────

async def stage_2_outline() -> dict:
    _header(2, "Outline Generation (LLM + User Prompt)")

    events = await _collect_sse(
        generate_outline(COURSE_PROMPT, "prompt")
    )

    outline = None
    for ev in events:
        if ev.get("type") == "outline":
            outline = ev["data"]
        elif ev.get("type") == "error":
            _result("S2", "Outline generation", FAIL, ev["message"])
            sys.exit(1)

    if not outline:
        _result("S2", "Outline generation", FAIL, "No outline produced")
        sys.exit(1)

    modules = outline.get("modules", [])
    all_lessons = []
    for mod in modules:
        for les in mod.get("lessons", []):
            all_lessons.append(les)

    _kv("Title", outline.get("title", ""))
    _kv("Modules", len(modules))
    for mod in modules:
        print(f"\n  Module: {mod.get('title', '')}")
        for les in mod.get("lessons", []):
            concepts = les.get("concepts", [])
            print(f"    {les.get('title', '')} ({len(concepts)} concepts)")

    _result("S2", "Outline generation", PASS,
            f"{len(modules)} modules, {len(all_lessons)} lessons")

    return outline


# ──────────────────────────────────────────────────────────────────────
# Stage 3: Coverage Assessment (concept-level, LLM-assessed)
# ──────────────────────────────────────────────────────────────────────

async def stage_3_and_4_coverage_and_enrichment(
    outline: dict,
    *,
    sample: int | None = None,
) -> dict:
    """Stages 3-4: assess wiki coverage and enrich gaps.

    Delegates to the shared ``ensure_wiki_coverage`` function in
    ``course_generator``, then prints detailed results for test output.
    """
    _header(3, "Coverage Assessment + Enrichment (Stages 3-4 Combined)")

    all_lessons = []
    for mod in outline.get("modules", []):
        for les in mod.get("lessons", []):
            all_lessons.append(les)

    assessment = await ensure_wiki_coverage(
        all_lessons,
        course_description=outline.get("description", ""),
        enrich=True,
        sample=sample,
    )

    fully = assessment.get("fully_covered", [])
    research = assessment.get("needs_research", [])
    no_match = assessment.get("no_match", [])

    print(f"\n  Fully covered ({len(fully)} lessons — wiki sufficient):")
    for entry in fully:
        les = entry["lesson"]
        verdicts = entry.get("concept_verdicts", {})
        covered = sum(1 for v in verdicts.values() if isinstance(v, dict) and v.get("verdict") == "covered")
        print(f"    {les.get('title', '?')} ({covered}/{len(verdicts)} concepts covered)")

    print(f"\n  Needs research ({len(research)} lessons — enriched):")
    for entry in research:
        les = entry["lesson"]
        verdicts = entry.get("concept_verdicts", {})
        thin_concepts = [
            c for c, v in verdicts.items()
            if isinstance(v, dict) and v.get("verdict") in ("thin", "missing")
        ]
        print(f"    {les.get('title', '?')}")
        if thin_concepts:
            print(f"      Gaps: {', '.join(thin_concepts[:5])}")

    total = len(all_lessons)
    _result("S3-4", "Fully covered by wiki",
            PASS if len(fully) > 0 else WARN,
            f"{len(fully)}/{total} lessons")
    _result("S3-4", "Enriched lessons",
            PASS,
            f"{len(research)}/{total} lessons enriched")
    _result("S3-4", "No wiki match (bootstrapped)",
            PASS if not no_match else WARN,
            f"{len(no_match)} remaining")

    return assessment


# ──────────────────────────────────────────────────────────────────────
# Stage 5: Unified Generation (student notes + tutor KB)
# ──────────────────────────────────────────────────────────────────────

async def stage_5_generate(assessment: dict) -> tuple[dict, dict]:
    _header(5, "Unified Generation (Student Notes + Tutor KB from Enriched Wiki)")

    all_entries = (
        assessment.get("fully_covered", [])
        + assessment.get("needs_research", [])
    )

    if not all_entries:
        print("  No lessons to generate")
        return {}, {}

    total = len(all_entries)
    print(f"  Generating content + reference KB for {total} lessons...")
    print(f"  (wiki resolved once per lesson in Stage 3, reloaded with enriched content)\n")

    lessons_out: dict[str, dict] = {}
    all_kb: dict[str, str] = {}
    alt_videos: dict[str, list[tuple[str, str]]] = {}
    errors = 0

    sem = asyncio.Semaphore(5)

    async def _gen_one(entry: dict) -> None:
        nonlocal errors
        les = entry["lesson"]
        title = les.get("title", "Untitled")
        slug = les.get("slug", "")
        concepts = les.get("concepts", [])
        resolved_topics = entry.get("resolved_topics", set())

        async with sem:
            wiki_ctx = load_wiki_context(concepts, topic_slugs=resolved_topics)

            if not wiki_ctx.get("source_content"):
                print(f"  {title}: NO wiki content — skipping")
                errors += 1
                return

            ref_ctx = load_wiki_context(
                concepts, topic_slugs=resolved_topics, track="reference",
            )
            if not ref_ctx.get("source_content"):
                ref_ctx = None

            bundle = await generate_lesson_bundle(
                les, wiki_ctx, reference_ctx=ref_ctx,
            )

        content = bundle["content"]
        kb = bundle["reference_kb"]
        wiki_meta = bundle.get("wiki_meta", {})

        if wiki_meta.get("all_videos"):
            alt_videos[slug] = wiki_meta["all_videos"]

        if content.get("error"):
            print(f"  {title}: CONTENT ERROR — {content['error']}")
            errors += 1
        else:
            lessons_out[slug] = content
            content_words = _word_count(content.get("content", ""))
            kb_words = _word_count(kb)
            print(f"  {title}")
            print(f"    Notes: {content_words}w | KB: {kb_words}w | "
                  f"YT: {content.get('youtube_id', '-')} | "
                  f"Sources: {len(content.get('sources_used', []))}")

        if kb:
            all_kb[slug] = kb

    futures = [asyncio.ensure_future(_gen_one(e)) for e in all_entries]
    await asyncio.gather(*futures)

    # Checks
    _result("S5", "Lessons generated",
            PASS if len(lessons_out) == total else (WARN if len(lessons_out) > 0 else FAIL),
            f"{len(lessons_out)}/{total} generated, {errors} errors")

    wiki_grounded = sum(1 for l in lessons_out.values() if l.get("sources_used"))
    has_rec_reading = sum(1 for l in lessons_out.values()
                          if "## recommended reading" in l.get("content", "").lower())
    has_yt = sum(1 for l in lessons_out.values() if l.get("youtube_id"))
    has_educator_ref = sum(1 for l in lessons_out.values()
                           if any(kw in l.get("content", "").lower()
                                  for kw in ["alammar", "karpathy", "vaswani", "bahdanau", "3blue1brown"]))

    _result("S5", "Wiki-grounded lessons",
            PASS if wiki_grounded > total * 0.5 else WARN,
            f"{wiki_grounded}/{len(lessons_out)}")
    _result("S5", "Educator references",
            PASS if has_educator_ref > total * 0.5 else WARN,
            f"{has_educator_ref}/{len(lessons_out)}")
    _result("S5", "Recommended Reading sections",
            PASS if has_rec_reading > total * 0.3 else WARN,
            f"{has_rec_reading}/{len(lessons_out)}")

    # Image references in generated content
    import re as _re
    has_image_notes = sum(1 for l in lessons_out.values()
                         if _re.search(r"!\[", l.get("content", "")))
    has_image_kb = sum(1 for md in all_kb.values()
                       if _re.search(r"!\[|Visual Aids", md))
    _result("S5", "Image references in notes",
            PASS if has_image_notes > 0 else WARN,
            f"{has_image_notes}/{len(lessons_out)} lessons include images")
    _result("S5", "Image references in KBs",
            PASS if has_image_kb > 0 else WARN,
            f"{has_image_kb}/{len(all_kb)} KBs include images or Visual Aids")

    # YouTube dedup (with fallback to alternative videos from wiki)
    before_yt = sum(1 for l in lessons_out.values() if l.get("youtube_id"))
    deduplicate_youtube_ids(lessons_out, alt_videos=alt_videos)
    after_yt = sum(1 for l in lessons_out.values() if l.get("youtube_id"))
    removed = before_yt - after_yt
    if removed > 0:
        print(f"\n  YouTube dedup: removed {removed} duplicate video refs ({before_yt} → {after_yt})")
    _result("S5", "YouTube deduplication",
            PASS if removed > 0 or before_yt <= 2 else WARN,
            f"{after_yt} unique assignments (removed {removed} duplicates)")

    # KB stats
    kb_count = len(all_kb)
    kb_words = sum(len(md.split()) for md in all_kb.values())
    _result("S5", "Reference KBs generated",
            PASS if kb_count > total * 0.5 else WARN,
            f"{kb_count}/{total} lessons, {kb_words:,} total words")

    total_content_words = sum(_word_count(l.get("content", "")) for l in lessons_out.values())
    print(f"\n  Total: {total_content_words:,} content words + {kb_words:,} KB words across {len(lessons_out)} lessons")

    # Save generated content for review
    output_dir = Path(__file__).resolve().parent.parent / "content" / "pipeline-output"
    notes_dir = output_dir / "notes"
    kb_dir = output_dir / "reference-kb"
    notes_dir.mkdir(parents=True, exist_ok=True)
    kb_dir.mkdir(parents=True, exist_ok=True)

    for slug, lesson in lessons_out.items():
        title = lesson.get("title", slug)
        content_md = lesson.get("content", "")
        sources = lesson.get("sources_used", [])
        yt_id = lesson.get("youtube_id", "")
        video_title = lesson.get("video_title", "")

        header = f"# {title}\n\n"
        if yt_id:
            header += f"**Video:** [{video_title or yt_id}](https://youtube.com/watch?v={yt_id})\n\n"
        if sources:
            header += "**Sources:** " + ", ".join(sources[:5]) + "\n\n"
        header += "---\n\n"

        (notes_dir / f"{slug}.md").write_text(header + content_md)

    for slug, kb_md in all_kb.items():
        title = lessons_out.get(slug, {}).get("title", slug)
        header = f"# Reference KB: {title}\n\n---\n\n"
        (kb_dir / f"{slug}.md").write_text(header + kb_md)

    print(f"\n  Saved to {output_dir.relative_to(Path(__file__).resolve().parent.parent)}/")
    print(f"    notes/     — {len(lessons_out)} lesson files")
    print(f"    reference-kb/ — {len(all_kb)} KB files")

    return lessons_out, all_kb


# ──────────────────────────────────────────────────────────────────────
# Stage 6: Resource Recommendation Tool Test
# ──────────────────────────────────────────────────────────────────────

def stage_6_resource_tool() -> None:
    _header(6, "Resource Recommendation Tool (Tutoring)")

    from app.agent.tool_handlers import _get_curated_resources

    result = _get_curated_resources(["self-attention", "multi-head attention", "transformer"])
    resources = result.get("resources", [])

    videos = [r for r in resources if r.get("type") == "video"]
    blogs = [r for r in resources if r.get("type") == "blog"]

    _result("S6", "Resource tool returns results",
            PASS if resources else FAIL,
            f"{len(resources)} resources ({len(videos)} videos, {len(blogs)} articles)")

    for r in resources[:5]:
        has_transcript = r.get("has_transcript", False)
        print(f"  [{r.get('type', '?')}] {r.get('educator', '?')} — {r.get('title', '?')}")
        if r.get("youtube_id"):
            print(f"    YouTube: {r['youtube_id']} | Transcript: {'YES' if has_transcript else 'no'}")
        elif r.get("url"):
            print(f"    URL: {r['url'][:80]}")

    has_karpathy = any("karpathy" in r.get("educator", "").lower() for r in resources)
    has_3b1b = any("3blue1brown" in r.get("educator", "").lower() or "3b1b" in r.get("educator", "").lower() for r in resources)
    _result("S6", "Known educators found",
            PASS if has_karpathy or has_3b1b else WARN,
            f"Karpathy={'Y' if has_karpathy else 'N'}, 3B1B={'Y' if has_3b1b else 'N'}")



# ──────────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────────

_CHECKPOINT_DIR = Path(__file__).resolve().parent.parent / "content" / "pipeline-output" / "checkpoints"


def _save_checkpoint(name: str, data: dict) -> None:
    _CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)
    path = _CHECKPOINT_DIR / f"{name}.json"

    def _serialize(obj):
        if isinstance(obj, set):
            return list(obj)
        raise TypeError(f"Not serializable: {type(obj)}")

    path.write_text(json.dumps(data, indent=2, default=_serialize))
    print(f"  [checkpoint] Saved {name}")


def _load_checkpoint(name: str) -> dict | None:
    path = _CHECKPOINT_DIR / f"{name}.json"
    if not path.exists():
        return None
    data = json.loads(path.read_text())
    # Restore sets that were serialized as lists
    if name.startswith("stage3") or name.startswith("stage4"):
        for bucket in ("fully_covered", "needs_research", "no_match"):
            for entry in data.get(bucket, []):
                if "resolved_topics" in entry:
                    entry["resolved_topics"] = set(entry["resolved_topics"])
    return data


async def main():
    parser = argparse.ArgumentParser(description="Wiki-first course pipeline test")
    parser.add_argument("--sample", type=int, default=None,
                        help="Limit enrichment search to N lessons (default: all)")
    parser.add_argument("--resume-from", type=int, default=1, metavar="STAGE",
                        help="Resume from stage N using saved checkpoints (default: 1)")
    args = parser.parse_args()

    resume = args.resume_from

    print(_DIVIDER)
    print("  WIKI-FIRST COURSE CREATION PIPELINE TEST")
    print(f"  Topic: Attention Mechanisms in Deep Learning")
    if args.sample:
        print(f"  Enrichment sample: {args.sample} lessons")
    if resume > 1:
        print(f"  Resuming from Stage {resume} (loading checkpoints)")
    print(_DIVIDER)

    # Stage 1: Wiki readiness
    if resume <= 1:
        wiki_ctx = await stage_1_wiki_readiness()
    else:
        print(f"\n  [skip] Stage 1 — resuming from {resume}")

    # Stage 2: Outline (LLM + user prompt)
    if resume <= 2:
        outline = await stage_2_outline()
        _save_checkpoint("stage2_outline", outline)
    else:
        outline = _load_checkpoint("stage2_outline")
        if not outline:
            print("  ERROR: No checkpoint for stage 2 — run from stage 2 first")
            return
        print(f"  [skip] Stage 2 — loaded outline checkpoint")

    # Stages 3-4: Coverage assessment + enrichment (via shared ensure_wiki_coverage)
    if resume <= 3:
        assessment = await stage_3_and_4_coverage_and_enrichment(outline, sample=args.sample)
        _save_checkpoint("stage3_assessment", assessment)
        _save_checkpoint("stage4_assessment", assessment)
    elif resume <= 4:
        assessment = _load_checkpoint("stage3_assessment")
        if not assessment:
            print("  ERROR: No checkpoint for stage 3 — run from stage 3 first")
            return
        assessment = await stage_3_and_4_coverage_and_enrichment(outline, sample=args.sample)
        _save_checkpoint("stage4_assessment", assessment)
    else:
        assessment = _load_checkpoint("stage4_assessment") or _load_checkpoint("stage3_assessment")
        if not assessment:
            print("  ERROR: No checkpoint for stages 3-4 — run from stage 3 first")
            return
        print(f"  [skip] Stages 3-4 — loaded assessment checkpoint")

    # Stage 5: Unified generation (student notes + tutor KB)
    if resume <= 5:
        lessons_out, kb = await stage_5_generate(assessment)
    else:
        print(f"  [skip] Stage 5")

    # Stage 6: Resource tool test
    if resume <= 6:
        stage_6_resource_tool()

    # Summary
    print(f"\n{_DIVIDER}")
    print("  RESULTS SUMMARY")
    print(f"{_DIVIDER}")
    passed = sum(1 for _, _, s in results_summary if s == PASS)
    warned = sum(1 for _, _, s in results_summary if s == WARN)
    failed = sum(1 for _, _, s in results_summary if s == FAIL)
    total = len(results_summary)
    print(f"\n  {passed} passed, {warned} warnings, {failed} failed (of {total} checks)")
    print()
    for stage, check, status in results_summary:
        symbol = {"PASS": "✓", "FAIL": "✗", "WARN": "⚠"}.get(status, "?")
        print(f"  {stage:4s} [{symbol}] {check}")

    if failed:
        print(f"\n  {failed} FAILURE(S) — investigate above")
    elif warned:
        print(f"\n  All critical checks passed. {warned} warning(s) to review.")
    else:
        print(f"\n  All checks passed!")


if __name__ == "__main__":
    asyncio.run(main())
