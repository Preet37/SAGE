# SocraticTutor — Decision Log

Chronological record of design decisions, iterations, and implementation details. For the concise reference doc, see [PROJECT.md](PROJECT.md).

---

## Wiki-First Cleanup

Removed all source-first discovery pipeline remnants (dead endpoints, unused imports, stale code paths in `chat_actions.py`, `course_creator.py` router). Renamed `_resolve_topics_exact` to `resolve_topics_exact` (public API). Full pytest suite passing after cleanup.

---

## Static Files Security Fix

**Problem**: Generic `StaticFiles` mount at `/api/wiki-images/` exposed markdown, proposals, and other non-image wiki content.

**Fix**: Custom secure endpoint `GET /api/wiki-images/{topic_slug}/images/{filename}` — only serves image files (`.png`, `.jpg`, `.jpeg`, `.gif`, `.svg`, `.webp`), includes path traversal protection.

---

## Image Metadata in Tutor System Prompt

Added `available_images: list[dict]` to `TutorContext`. System prompt now includes `AVAILABLE IMAGES FOR THIS LESSON` (up to 15 images with path, caption, concepts, when_to_show). Tutor can emit `<image>` tags directly; `get_relevant_images` tool still available for cross-lesson lookups.

---

## Source-to-Lesson Mapping

Added `sources_used` and `image_metadata` fields to `Lesson` SQLModel. `select_lesson_images()` filters images by matching `source_page` URLs against `lesson.sources_used` — tight lesson->source->image chain. `course_validator.py` persists both fields when publishing. Tutor router reads `lesson.image_metadata` first, falls back to disk for older lessons.

---

## Citation Validation Tooling

`backend/scripts/validate_citations.py` — offline citation validator. `build_wiki_url_index()` scans wiki source files for `# Source:` headers to build ground-truth URL map. Cross-checks lesson content/KB URLs, classifies as verified/unverified/video, computes topic_coverage. Integrated into `eval_quality.py` as Tier 2c.

---

## Wiki-First Regeneration Experiment

**Scripts**: `regenerate_course.py` (regenerates via wiki-first `generate_lesson_bundle`) + `compare_generations.py` (structural + grounding + citation metrics, HTML report).

**Experiment**: 12-lesson "Introduction to LLMs" course, old vs wiki-first. Results: wiki-first improved source grounding, structural adherence, and image integration. Student notes were initially too citation-heavy — needed prompt tuning.

---

## Reference KB Prompt Rewrite (v2)

**Problem**: Original KB prompt was structured like a textbook chapter. A tutor consulting mid-conversation needs lookup-oriented structure.

**Approach**: Side-by-side comparison on `alignment-rlhf`. Old prompt had exact formulas and specific numbers; new prompt had teaching approaches, misconceptions, and Socratic questions.

**Changes to `REFERENCE_KB_FROM_WIKI_PROMPT`**:
- Rewrote persona to be organized around tutoring tasks
- New sections: Teaching Approaches, Common Misconceptions (required), Prerequisite Connections, Socratic Question Bank, Available Resources
- Re-added old strengths: Key Formulas & Empirical Results, Likely Student Questions
- Word count target: 2000-3500 words
- Rule: "When source material contains formulas, benchmarks, or specific defaults — include them"

**Resource metadata enrichment**: New `_build_resource_summary()` extracts YouTube IDs and reading from `wiki_ctx`. Injected as `{resource_summary}` into prompt.

**Eval results** (7 lessons):

| Lesson | Old | New | Winner |
|--------|-----|-----|--------|
| attention-breakthrough | 12/25 | 14/25 | New |
| self-attention | 15/25 | 14/25 | Old |
| word-embeddings | 10/25 | 14/25 | New |
| from-digital-to-physical | 11/25 | 11/25 | Tie |
| agent-frameworks-sdks | 11/25 | 11/25 | Tie |
| rag-retrieval | 11/25 | 13/25 | New |
| alignment-rlhf | 9/25 | 13/25 | New |

**4 new wins, 1 old win, 2 ties**. Old wins on precision-heavy topics; new wins on conceptual topics.

---

## Student Notes Prompt Tuning (v1 -> v2 -> v3)

- **v1**: Over-constrained — "ground every claim", cite educators by name
- **v2**: Added narrative persona (Karpathy/3Blue1Brown/Alammar), hooks, analogies — but too formulaic ("Imagine you're...")
- **v3** (current): Relaxed structural prescriptions. "Write naturally — vary your openings." Analogies only when they genuinely clarify. Comparison tables encouraged for tradeoffs. Citation rules separated: no inline citations in prose, attribution in captions/footnotes, Recommended Reading at end.

Tested on 5 diverse lessons — confirmed varied openings, natural tables, strong readability.

---

## Pipeline Architecture (7-stage)

- Checkpointed pipeline (`--resume-from` any stage): wiki readiness, outline, coverage assessment, enrichment (search + curation + download), content generation, resource recommendation, feedback loop
- LLM-based concept mapper (`resolve_topics_llm`) maps lesson concepts to wiki topic slugs
- Three-tier coverage assessment: covered / thin / missing
- Curator + Reviewer pattern: LLM curator selects sources, LLM reviewer audits and promotes near-misses
- Human-reviewable curation report showing only near-misses
- Unified content generation (`generate_lesson_bundle`): student notes (streamable) + reference KB (backgroundable)
- YouTube deduplication and relaxed video assignment
- Fallback LLM model — `_call_llm()` retries with `settings.fallback_llm_model` on error
- Primary model: GPT-5.2 (resolved gateway timeouts and JSON truncation from Claude Sonnet)

---

## Wiki Expansion — 37 to 51 Topics

14 new topics across 4 themes:
- **Agentic Coding & Tools**: `agentic-coding`, `mcp-tool-ecosystem`
- **Deeper Multimodal**: `audio-speech-models`, `document-understanding`, `image-generation`, `video-understanding`
- **Newer ML/AI**: `mixture-of-experts`, `reasoning-models`, `inference-optimization`, `long-context`, `synthetic-data`
- **Extended Agents**: `agent-workflows`, `knowledge-graphs`
- **3D**: `graph-attention-networks-and-structured-data`

Pipeline: concept-map.md -> wiki_config.json -> bootstrap --consolidate -> bootstrap --download (57 sources) -> backfill_reference_track (119 sources, 118 cards, zero errors).

New educators: Simon Willison (MCP), Anthropic (Claude Code).

Final wiki stats: 51 topics, 466+ ref sources, 9 subjects, 11 educators, ~517 concepts, 144 subtopics, 1499+ images.

---

## Unified Enrichment Pipeline — `ensure_wiki_coverage()`

**Problem**: Assess-enrich pipeline existed only inline in `test_pipeline.py`. Regeneration script skipped coverage/enrichment. `chat_actions.py` dropped reference KB on regeneration.

**Solution**: Extracted to single reusable function in `course_generator.py`:
1. `assess_wiki_coverage` — LLM concept-level coverage
2. `bootstrap_new_wiki_topic` — new topic pages for unmapped concepts
3. Search + curate + download (pedagogy track)
4. Reference track enrichment
5. Structural notes for thin concepts

All paths now use the same pipeline:
| Path | File |
|------|------|
| Regeneration (batch) | `regenerate_and_publish.py` (`--enrich`) |
| Pipeline test | `test_pipeline.py` (stages 3-4) |
| Chat action | `chat_actions.py` (fixed to persist `reference_kb`) |
| Course Creator UI | `course_generator.py` |

Also: `resolve_topics_llm` everywhere (replaced exact), `seed.py` syncs all lesson fields.

---

## Full Course Regeneration — 6 Courses, 74 Lessons

All courses regenerated with v3 notes + v2 KB + reference track context.

| Course | Lessons | Avg Notes | Avg KB | Mode |
|--------|---------|-----------|--------|------|
| ML Engineering Foundations | 8 | ~600w | ~3,200w | Direct |
| Intro to LLMs | 12 | ~650w | ~3,100w | Direct |
| Intro to Agentic AI | 13 | ~630w | ~3,000w | Direct |
| Intro to Multi-Modal AI | 12 | ~640w | ~3,200w | Direct |
| Intro to Physical AI | 12 | ~620w | ~3,100w | Direct |
| Agentic AI Frameworks | 17 | 668w | 3,370w | Enriched |

0 failures, all seeded to DB. Agentic AI Frameworks used `--enrich` to deepen 7 wiki topics before generation.

---

## Wiki URL Cleanup — 30 Issues Fixed

Ran `wiki_curator.py` on 9 enriched topics. Fixed 30/33 issues (3 remaining are LangGraph SPA false positives). Fixes included: wrong youtube_ids, dead links (LangGraph, NeMo Guardrails, AutoGen), hallucinated URLs (Lilian Weng), duplicate URLs, casing normalization. Rebuilt all 51 Quartz pages.

---

## Quartz Wiki Integration

Updated `topic_to_quartz.py` to render reference track content:
- "Additional Resources for Tutor Depth" section with expandable reference cards
- Cards sorted by role (papers -> benchmarks -> reference docs)
- Body cleanup: strips enrichment blockquotes, structural notes, `## Last Verified`; converts url/youtube_id lines to clickable links

Wiki theme: sage-green light mode matching the app, warm olive dark mode.

---

## Wiki Curator Script

`scripts/wiki_curator.py` — automated source quality auditing (7 check types) + auto-fix (5 fix types) + link validation (HTTP + YouTube oEmbed, cached 7-day TTL).

Initial run: 153 issues fixed across 51 topics. 38 dead links and 37 title mismatches caught.

**Root cause**: Many hallucinated URLs were generated during `bootstrap_wiki.py` Phase B (LLM resource curation). They exist in listing files, not downloaded sources. The download pipeline works correctly; the curation step generated fake URLs.

Integrated into job runner (`curate-wiki`, 24h cycle).

---

## Author Registry

**Problem**: Author info fragmented across 5 hardcoded locations.

**Solution**: Unified registry in `content/pedagogy-wiki/authors.md` (76 authors, 107 domains, 15 educators, 5 venues). Core module `wiki_authors.py` with resolve/extract/validate. Download integration writes `# Author:` headers automatically. Backfill scripts for domain-based (213 files) and arXiv API-based (62 papers) attribution. 245/245 source files attributed (100%).

---

## Reference Track Pipeline

**Decision**: Two separate tracks. Pedagogy track (unchanged, teaching resources) + reference track (new, precision technical sources).

**Key design choices**:
- **Needs-driven**: LLM outputs 3-5 typed precision needs (FORMULA_SOURCE, EMPIRICAL_DATA, API_REFERENCE, WORKING_EXAMPLE, etc.) with queries. Adapts to topic nature.
- **Small library**: 3-6 sources per topic (tutor has web search for everything else)
- **Ramps over gaps**: unfilled needs produce `search_hint` for runtime lookup (`ramps.json`)
- **Source cards**: full sources distilled to ~200-300w cards by LLM. Cards (not raw sources) feed KB generation.
- **Parallel card extraction**: `asyncio.gather` with `Semaphore(5)`
- **Two-pass context packing**: (1) guarantee one source per concept, (2) fill by relevance. Word-based budgets (500w/source cap).
- **Blended generation context**: reference first (10K words) + pedagogy (5K words). Fallback to pedagogy-only (15K) when no reference sources exist.

**Bugs found and fixed**:
1. Download EXISTS check too permissive — now checks cleaned word count
2. Arxiv boilerplate inflating word counts — added boilerplate regex patterns
3. Card extraction on boilerplate-inflated sources — applies cleaning before threshold check
4. Context packing dropping niche concepts — two-pass guarantees one source per concept
5. Silent empty KB on LLM failures — retry up to 3 times if <50 words

**Test results** (`alignment-rlhf`, 6 concepts): enrichment ~137s, KB ~100s -> 3,472 words, all concepts covered. Constitutional AI properly defined (was broken by packing bug).

---

## Frontend UX

**Resizable sidebar**: Replaced `react-resizable-panels` (type errors, state loss) with custom drag handler.

**Syntax highlighting**: `rehype-highlight` + `highlight.js` across all markdown renderers. Dark/light mode colors in `globals.css`.

**Chat UX overhaul**:
- Gemini-style empty state (centered input + prompts, moves to sticky bottom on messages)
- Auto-scroll only on new question (not during streaming)
- `h-dvh` for accurate viewport height
- Lesson page: 60/40 chat/content split, content visible by default

**Mermaid diagrams**: Fixed rendering (rehype-highlight changed class format). Theme-aware (MutationObserver re-renders on toggle).

**Resource cards**: Clickable with auto-constructed YouTube URLs. **Quiz cards**: Fixed light mode colors.

---

## Unified AppHeader

`frontend/components/AppHeader.tsx` — shared nav across all authenticated pages (Learn, Explore, Quiz, Concepts, Projects, Create, Wiki). Flexible `leftSlot` prop. Replaced per-page custom headers in 8 files.

---

## Tutor Agent Prompt Tuning

- Teaching toolkit instruction: "Lean into your full teaching toolkit: analogies, diagrams, curated images, code examples, tables, knowledge-check quizzes, and curated resources"
- Quiz format: renamed to "QUICK KNOWLEDGE CHECK", explicit `<quiz>` card instruction
- Resource recommendations: balanced frequency, never same resource twice, `url` field required
- Temperature fix: 0.7 was loaded but never sent to API — now actually passed

---

## Systematic Prompt Evaluation Framework

4-layer evaluation in `backend/evals/`:

**Layer 0 — Behavioral metrics** (deterministic): question_ratio, modality_count, image_proactive_count, tool_call_count, backward_reference_count

**Layer 1 — Format safety** (heuristics): quiz card usage, resource URL presence, no duplicate resources, response length tracking

**Layer 2 — Prompt alignment judge** (LLM): socratic_method, multimodal_teaching, compound_analogies, factual_grounding, adaptive_mode, image_discipline. Retry logic (up to 2 retries with backoff). Known-pattern rubric notes for compound_analogies and image_discipline in code-heavy scenarios.

**Layer 3 — Outcome judge** (LLM): learning_arc, conversational_craft, technical_accuracy, intellectual_engagement, adaptive_responsiveness

Format-probe scenarios: quiz cards, resource cards, visual diagrams.

Baseline results (GPT-5.2 + prompt v2): all format probes passing. Full 40-scenario baseline run completed.

---

## Creator Chat Context Enrichment

**Problem**: Course design co-pilot had no awareness of app workflow or terminology — told users enrichment was a "manual 20-45 minute task" when it's one-click automated.

**Solution**: Enriched `DRAFT_CHAT_SYSTEM` prompt with app workflow (6-step pipeline with phases), features & terminology (all 6 tabs, key terms, learner experience), and live coverage context injection (`_build_chat_context` parses coverage_assessment data from draft). No additional LLM calls.

---

## KB Research Visibility — Course Creator

**Problem**: KB matching and enrichment happened invisibly after "Build Course" click.

**Solution**: New "Research" phase/tab between outline and content generation. Backend: `_assess_one_lesson()` shared helper, `assess_wiki_coverage_stream()` (SSE per lesson), `ensure_wiki_coverage_stream()` (full enrichment pipeline). Frontend: `ResearchView.tsx` with coverage %, expandable lesson cards (green/amber/red), concept verdicts, enrichment log. Two-step flow: "Prepare Content" -> review -> "Build Course".

---

## Course Visibility and Sharing

**Design decision**: AI-first Socratic learning — no community/marketplace (encourages passive browsing over active prompting). Private by default, share by email or link. Platform courses stay public.

Model: `LearningPath` with `created_by`, `visibility`, `share_token`. `CourseShare` table for per-user shares. Backend: scoped listing, sharing endpoints, share link generation/joining. Frontend: My Courses / Shared / Platform sections, ShareDialog. 10 new tests, 114 total passing.

---

## Audience-Aware Enrichment Pipeline

**Problem**: Enrichment was audience-blind — practical courses got academic-heavy sources.

**Solution**: `course_profile` dict (audience, tone, source_types, deprioritize, vendor) extracted at outline time. Threaded through: enrichment queries, source curation, content generation, KB generation.

Added: multimedia search strategy (YouTube tutorials from recognized educators), audience affinity scoring (_extract_audience_tag, _AUDIENCE_AFFINITY), auto-generated wiki resource pages.

---

## Wiki Metadata Version Control

**Problem**: Entire `content/` was gitignored including valuable wiki metadata.

**Solution**: Selective `.gitignore` — track wiki metadata (resource pages, concept-map, authors, educators), ignore bulk downloads (500MB+):
```
content/*
!content/pedagogy-wiki/
content/pedagogy-wiki/resources/by-topic/*/
```

---

## Reference Track Backfill

`backfill_reference_track.py` — batch enrichment for all topics. Configurable: `--dry-run`, `--topics`, `--concurrency`, `--min-sources`. Full backfill: 50 topics, 466 sources, 465 cards, ~11 minutes.

---

## Image Pipeline

Two-tier extraction (HTML parsing + heuristic filtering + batched LLM annotation, optional multimodal enhancement). Image metadata in `images.json`. Cross-topic deduplication (saved 224 downloads / 430 MB). Git-friendly: binaries gitignored, `--rehydrate` downloads from metadata. Browser fallback (Playwright) for JS-heavy sites.

---

## Pipeline Pytest Suite

Three-tier test architecture: unit (mocked LLMs), mocked integration (canned JSON), opt-in real LLM/wiki. 7 test files covering all pipeline stages + images + visibility. Mini-wiki fixture for isolation. LLM/wiki tests deselected by default.

---

## search_web Tool Fix

**Problem**: `search_web` tool failed with "Illegal header value b'Bearer '" — `SEARCH_API_KEY` not set, causing empty auth header.

**Fix**: Refactored `_search_web` in `tool_handlers.py` to delegate to `course_enricher._search` which handles API key routing (inference API via `LLM_API_KEY` or direct Perplexity via `SEARCH_API_KEY`). Removed redundant LLM-reranking step.

---

## Enrichment Progress UI Fix

**Problem**: Progress bar showed "0 of 19 complete" even though lesson cards showed "Complete". UI appeared stuck after downloads.

**Fix**: `computeStats` in `EnrichmentView.tsx` was counting `enrich_complete` events (emitted once at pipeline end). Changed to count lessons with `status === "done"` from `lessonMap`. Added intermediate `"referencing"` status for reference track enrichment phase.

---

## Eval Scoring Bug Fixes

**alignment-rlhf 0.00 scoring**: Alignment judge was silently returning all-zero scores on LLM failures. Added retry logic (up to 2 retries with backoff), zero-score detection as soft failure, descriptive "SCORING FAILED" justifications. Runner excludes zero-score results from aggregates.

**self-attention explore low score (3.20)**: Scenario asked about RAG pipelines while lesson was self-attention — judge penalized for off-topic teaching. Rewrote scenario to ask about self-attention Q/K/V computation while still probing for diagrams.

**image_discipline and compound_analogies**: Low scores in code-heavy scenarios were accepted behavior (tutor prioritizes code/text). Added KNOWN PATTERN rubric notes instead of prompt changes.

---

## Future: Design Direction — AI-First Learning

**Principle**: Lesson page should prioritize interactive AI engagement over static content consumption.

Planned: Chat-first layout (notes behind toggle). AI content actions: Download Notes, Generate Podcast (NotebookLM-style), Quiz Me, Explain Like I'm..., Flashcard Deck, Study Group Mode, Connect the Dots.

---

## Future: Wiki Staging Workflow

**Problem**: Enrichment directly modifies tracked wiki files.

**Design**: Redirect writes to `.pending/` staging area. `merge_wiki_pending.py` with `--dry-run`, `--apply`, `--interactive` modes. Three functions affected: `bootstrap_new_wiki_topic`, `file_structural_note`, `regenerate_resource_page`.

---

## Future: Wiki Storage for Multi-User

**Problem**: Filesystem wiki doesn't scale for concurrent enrichment.

**Options**: Git batch commits (A), DB-backed (B), object storage (C), write-ahead layer (D). Recommended: Option D — `wiki_writes` DB table buffers enrichment, periodic flush to git. Stepping stone to full DB migration.

---

## Future: Interactive Artifact Visuals

`<artifact>` tag for in-chat HTML/JS interactives (sliders, step-throughs) in sandboxed iframes. Prototyped and rolled back. Key concern: too many output format guides already. Need consolidated VISUALS decision tree. Good first candidates: softmax temperature slider, attention heatmap, gradient descent landscape.

---

## Future: Slash Commands

`/command` system for all chat surfaces. Universal: `/feedback`, `/bug`, `/help`, `/clear`, `/export`. Tutor: `/hint`, `/explain`, `/quiz`, `/sources`, `/simpler`, `/deeper`. Creator: `/status`, `/enrich`, `/build`, `/assess`, `/outline`, `/publish`.

---

## Future: Learner Memory & Personalization

Three-layer memory: structured profile (concepts mastered/struggling), session summaries (100-200w digests), full chat archive. Personal learning wiki (Obsidian-style concept pages). User-uploaded content ("Teach Me This" / "Help Me Study From My Notes"). Build order: profile -> file upload -> summaries -> dashboard -> personal wiki.

---

## Historical: External Deployment (torn down)

Domain: socratictutor.dev. Droplet: 164.92.113.225 (DigitalOcean). Stack: Docker Compose + Caddy. This deployment is no longer active.

---

## Historical: Nightly Enrichment Workflow (pre-hosted)

Designed for the external droplet where datacenter IPs got throttled. Workflow: users create courses on droplet -> pull `tutor.db` nightly -> run enrichment locally (residential IP, better downloads) -> push to git -> pull on droplet. No longer needed with hosted deployment.
