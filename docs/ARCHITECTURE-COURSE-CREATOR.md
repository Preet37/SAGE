# Course Creator: Architecture & Design Decisions

## Overview

The Course Creator lets users describe what they want to learn, then builds a fully structured, wiki-grounded curriculum. The pipeline assesses what the pedagogy wiki already knows, enriches gaps via targeted web search, generates student-facing content and tutor-facing reference KBs, and publishes the result as a live course.

This document covers the creator pipeline end-to-end. For the tutor agent and learner-facing architecture, see [ARCHITECTURE-TUTOR.md](ARCHITECTURE-TUTOR.md).

---

## The Pipeline

```
Phase 1: Outline       → Phase 2: Research       → Phase 3: Enrich        → Phase 4: Build         → Phase 5: Review      → Phase 6: Publish
━━━━━━━━━━━━━━━━━━━━━    ━━━━━━━━━━━━━━━━━━━━━━    ━━━━━━━━━━━━━━━━━━━━━    ━━━━━━━━━━━━━━━━━━━━━    ━━━━━━━━━━━━━━━━━━━    ━━━━━━━━━━━━━━━━━━━
• LLM generates outline  • Per-lesson wiki        • Web search for gaps    • Generate Reference KB  • Quality gate checks  • Publish to database
• Chat-based editing       coverage assessment    • LLM curator selects    • Generate Student Notes • QA pair generation   • Course goes live
• Approve structure      • Concept-level verdicts    best sources           • Per-lesson streaming   • Human review         • Private by default
                           (covered/thin/missing)  • Download + card        • Resume on interruption
                                                     extraction
```

### Why wiki-first?

The original approach ran web searches per lesson and generated content directly. This produced wide but shallow content. The wiki-first approach:

1. **Grounds content in curated sources** — every lesson is backed by the pedagogy wiki's reviewed material
2. **Identifies real gaps** — LLM-based coverage assessment knows exactly which concepts need research
3. **Accumulates knowledge** — enrichment grows the wiki, so future courses benefit automatically
4. **Two-track depth** — pedagogy sources for teaching context + reference sources for precision (formulas, benchmarks, APIs)

### Why KB before content?

The pipeline generates a **tutor-facing Reference KB** first, then derives **student-facing Lesson Notes** from it:
- The KB is a comprehensive, fact-dense markdown document (~2K-4K words) designed for the tutor's real-time grounding
- Student notes are a more focused, pedagogically structured narrative (~600-700 words)
- Human reviewers can inspect and edit the KB before content generation

---

## Data Model

### Draft storage

Each course-in-progress is a `CourseDraft` row with a `data` JSON blob:

```json
{
  "outline": {
    "title": "AI Agents Masterclass",
    "description": "...",
    "level": "intermediate",
    "modules": [
      { "title": "Foundations", "order_index": 0, "lesson_slugs": ["what-is-an-ai-agent", "why-use-a-framework"] }
    ]
  },
  "lessons": {
    "what-is-an-ai-agent": {
      "title": "What Is an AI Agent?",
      "slug": "what-is-an-ai-agent",
      "summary": "Introduces the concept of AI agents...",
      "concepts": ["perception-reasoning-action loop", "tool use"],
      "status": "content_done",
      "research": { "queries": [...], "search_results": [...], "evaluations": [...], "curated_sources": [...] },
      "reference_kb": "# What Is an AI Agent?\n\n...",
      "content": "## Understanding AI Agents\n\n..."
    }
  },
  "coverage_assessment": { ... },
  "enrichment_log": [ ... ],
  "course_profile": { "audience": "practitioner", "tone": "conversational", ... }
}
```

**Key design decisions:**

- **Modules are grouping containers only** — they store `lesson_slugs` arrays, not nested lesson objects. All lesson data lives in the flat `lessons` dictionary.
- **Status is per-lesson** — `outline` -> `researched` -> `kb_done` -> `content_done`. Enables resume after interruption.
- **Draft-level phase is computed** — `_compute_draft_phase()` derives the wizard phase from the aggregate of lesson statuses. No separate phase field to fall out of sync.
- **Incremental persistence** — every streaming endpoint saves results to DB as each lesson completes, not after the batch finishes. Protects against browser tab closure, network interruptions, and server restarts.

---

## Backend Services

### `course_generator.py` — Orchestration

The central service that coordinates assessment, enrichment, and content generation.

**Coverage assessment:**
- `_assess_one_lesson(lesson)` — resolves concepts to wiki topics via `resolve_topics_llm`, loads wiki snippets, LLM scores each concept as `covered`/`thin`/`missing`. Returns verdict: `fully_covered`, `needs_research`, or `no_match`.
- `assess_wiki_coverage_stream(lessons)` — runs assessments concurrently via `as_completed`, yielding SSE events per lesson.

**Enrichment:**
- `ensure_wiki_coverage_stream(lessons, ...)` — full pipeline: assess -> bootstrap missing topics -> generate gap-driven queries -> search -> curate sources -> audit curation -> download to wiki -> reference track enrichment -> structural notes -> regenerate resource pages. Yields step-by-step SSE events.
- `_format_course_profile(profile)` — formats the audience/tone/vendor profile as a prompt block, threaded through all generation calls.

**Content generation:**
- `generate_content(outline, ...)` — walks lessons, skips already-completed ones (resume support). For each lesson: resolve wiki topics, load context (pedagogy + reference track), generate via `generate_lesson_bundle`. SSE: `progress`, `content`, `done`.
- `generate_reference_kb_from_wiki(lessons, ...)` — per-lesson KB generation from blended wiki context (reference track first at 10K words, pedagogy at 5K words; fallback to pedagogy-only at 15K). SSE: `progress`, `reference_kb`, `done`.

**Context packing:**
- Two-pass `_build_wiki_source_context()`: (1) guarantee at least one source per lesson concept, (2) fill remaining budget by relevance. Word-based budgets with 500-word per-source cap.
- Audience affinity scoring (`_extract_audience_tag`, `_AUDIENCE_AFFINITY`) boosts sources matching the course profile.

### `course_enricher.py` — Search & Curation

**Search strategies** (`QUERY_STRATEGIES`):
- `natural_question`, `specific_lookup` — general discovery
- `comparative` — alternatives and tradeoffs
- `failure_edge_case` — pitfalls and debugging
- `multimedia` — YouTube tutorials from recognized educators, interactive demos

When wiki coverage data is available, the enricher short-circuits to gap-driven queries + multimedia only (skips generic strategies).

**Reference track** (`enrich_reference_track`):
- `assess_reference_needs` — LLM proposes typed needs (FORMULA_SOURCE, EMPIRICAL_DATA, API_REFERENCE, WORKING_EXAMPLE, DEPLOYMENT_CASE, COMPARISON_DATA, CONCEPT_EXPLAINER) with search queries
- Per-need search -> `curate_reference_sources` -> `audit_reference_curation` -> download -> card extraction
- Unfilled needs produce `ramps.json` (search hints for runtime lookup)

**Search routing** (`_search`):
- Inference API (Perplexity endpoint) when only `LLM_API_KEY` is set
- Direct Perplexity API when `SEARCH_API_KEY` is configured separately

### `wiki_downloader.py` — Source Acquisition

**Download cascade** (`download_url`):
1. Trafilatura (including arXiv HTML variants)
2. Playwright browser fallback (for JS-heavy sites)
3. Jina Reader
4. Search-augmented summary fallback

Each result is checked for thin content (< 500 words cleaned). The best non-thin result wins.

**Source processing:**
- `download_source` — writes markdown files with `# Source`, `# Author`, `# Audience` headers. Supports both pedagogy and reference tracks.
- `curate_best_sources` / `audit_curation` — LLM curator selects from candidates, reviewer audits for overlooked near-misses
- `extract_reference_card` — distills full sources into ~200-300 word precision cards (formulas, results, procedures). Cards feed KB generation instead of raw text.
- `regenerate_resource_page` — auto-generates structured topic pages from downloaded sources

### `course_validator.py` — QA & Publishing

- `publish_course` — creates `LearningPath` + `Module` + `Lesson` rows from draft data. Persists `sources_used`, `image_metadata`, `reference_kb`. User-created courses get `visibility="private"`.
- `generate_qa` / `evaluate_qa` — SSE-streamed QA pair generation and evaluation

---

## API Endpoints

All under prefix `/course-creator`.

### Draft CRUD

| Method | Path | Purpose |
|--------|------|---------|
| POST | `/drafts` | Create draft from title + source type |
| GET | `/drafts` | List user's drafts |
| GET | `/drafts/{id}` | Get draft with migrated data |
| DELETE | `/drafts/{id}` | Delete draft |
| PATCH | `/drafts/{id}/patch` | Merge keys into draft data |
| GET | `/drafts/{id}/export` | Export as JSON (schema v2.0) |

### Pipeline (SSE streams)

| Method | Path | SSE events | What it does |
|--------|------|------------|--------------|
| POST | `/drafts/{id}/generate-outline` | `status`, `partial_outline`, `outline`, `done` | LLM generates course structure |
| POST | `/drafts/{id}/assess-coverage` | `status`, `lesson_assessed`, `assessment_complete`, `done` | Per-lesson wiki coverage assessment |
| POST | `/drafts/{id}/enrich-coverage` | `status`, `bootstrap`, `queries`, `search_result`, `curation`, `download`, `reference_enrichment`, `enrich_complete`, `done` | Full enrichment pipeline |
| POST | `/drafts/{id}/wiki-reference-kb` | `status`, `progress`, `wiki_kb_complete`, `reference_kb`, `done` | Generate reference KBs from wiki |
| POST | `/drafts/{id}/generate-content` | `progress`, `content`, `done` | Generate student notes (supports resume) |
| POST | `/drafts/{id}/generate-qa` | `progress`, `qa`, `done` | Generate QA pairs |
| POST | `/drafts/{id}/evaluate-qa` | `progress`, `evaluation`, `done` | Evaluate QA quality |

### Content management

| Method | Path | Purpose |
|--------|------|---------|
| PUT | `/drafts/{id}/outline` | Save edited outline |
| PUT | `/drafts/{id}/content` | Save edited lesson content |
| PUT | `/drafts/{id}/reference-kb-drafts` | Save edited reference KBs |
| POST | `/drafts/{id}/promote-source` | Download a near-miss source into wiki |
| GET | `/drafts/{id}/quality-gate` | Run quality checks |
| GET | `/drafts/{id}/final-dashboard` | Aggregated publish stats |
| POST | `/drafts/{id}/publish` | Publish to database |

### Chat co-pilot

`POST /drafts/{id}/chat` — SSE stream with `token` and `draft_actions` events.

The chat system prompt includes:
- Full pipeline description (6 phases with labels)
- All UI tab descriptions and terminology
- Live coverage assessment data (concept-level stats per lesson)
- Available actions: `research_topic`, `modify_outline`, `edit_lesson_content`, `regenerate_lesson`

---

## Frontend Components

### Layout

`CreateCanvas.tsx` — full-screen shell with horizontal resizable split: `ChatPanel` (co-pilot) | `ArtifactPanel` (tabbed workspace).

### Tabs (`ArtifactPanel.tsx`)

| Tab | Component | What it shows |
|-----|-----------|---------------|
| Outline | `OutlineView.tsx` | Editable outline tree, module/lesson reorder, "Prepare Content" / "Build" buttons |
| Research | `ResearchView.tsx` | Coverage assessment results — per-lesson cards (green/amber/red), concept verdicts, "Enrich" action |
| Enrich | `EnrichmentView.tsx` | Live enrichment log — per-lesson cards with queries, curation picks, near-misses (promotable), downloads, reference status |
| Build | `ProgressView.tsx` | Content generation progress bars, per-lesson status, cancel/resume |
| Lessons | `LessonsView.tsx` | Lesson picker with Notes vs Reference KB sub-views |
| Publish | `PublishView.tsx` | Quality gate, dashboard stats, QA flows, publish CTA |

### Supporting components

| Component | Purpose |
|-----------|---------|
| `ChatPanel.tsx` | Course assistant chat — markdown rendering, action card approval/skip |
| `DraftList.tsx` | Lists drafts with phase badge, relative time, delete |
| `GoalInput.tsx` | Landing textarea for new course description |

### State management (`useCreatorState.ts`)

Single hook `useCreatorState(draftId)` manages all creator state:
- `draft`, `outline`, `coverage`, `lessonProgress`, `quality`, `coverageAssessment`, `enrichmentLog`, `dashboard`
- SSE-backed actions: `generateOutline`, `generateContent`, `assessCoverage`, `enrichCoverage`, `sendChat`
- Phase derivation: `shaping` | `researching` | `building` | `reviewing` | `published`
- Hydrates from saved draft on load — restores chat history, coverage assessment, enrichment log

### SSE streaming (`useCreatorStream.ts`)

- `streamSSE(path, body, onEvent, onDone?, onError?)` — POST with Bearer token, ReadableStream reader, incremental JSON parse
- `useCreatorStream` — wraps with AbortController management for cancellation

---

## Audience-Aware Pipeline

The `course_profile` extracted at outline time threads through the entire pipeline:

```
Outline response
  → course_profile: { audience, tone, source_types, deprioritize, vendor }
    │
    ├── Enrichment: generate_queries(), assess_reference_needs()
    │   (multimedia strategy targets YouTube from recognized educators)
    │
    ├── Curation: curate_best_sources()
    │   (audience affinity scoring boosts matching sources)
    │
    ├── Content generation: CONTENT_FROM_WIKI_PROMPT
    │   (tone and audience injected into prompt)
    │
    └── KB generation: REFERENCE_KB_FROM_WIKI_PROMPT
        (depth calibrated to audience level)
```

---

## Two-Track Wiki Architecture

The wiki maintains two independent source tracks per topic:

```
resources/by-topic/{topic-slug}/
  ├── {source}.md              # Pedagogy track: teaching resources (blogs, tutorials, talks)
  ├── proposals.json           # Pedagogy curation decisions
  ├── curation-report.md       # Near-misses for human review
  │
  └── reference/               # Reference track: precision sources (papers, benchmarks, APIs)
      ├── {source}.md          # Full source text
      ├── {source}.card.md     # LLM-extracted ~200-300 word summary card
      ├── proposals.json       # Reference curation decisions
      └── ramps.json           # Unfilled needs → runtime search hints
```

**Pedagogy track** — teaching-oriented sources selected for explanatory clarity. Curator + reviewer audit pattern.

**Reference track** — precision sources for formulas, empirical results, API docs. Needs-driven discovery (LLM proposes typed needs like FORMULA_SOURCE, EMPIRICAL_DATA). Cards (not raw sources) feed KB generation, maximizing source diversity in the context window.

**Blended generation context:**
- Reference KB: reference sources first (10K words) + pedagogy (5K words)
- Student notes: pedagogy primary (15K words), blends reference when pedagogy is thin (< 3 sources)

---

## File Map

| Concern | Path |
|---------|------|
| API endpoints + draft model | `backend/app/routers/course_creator.py` |
| Draft DB model | `backend/app/models/course_draft.py` |
| Pipeline orchestration | `backend/app/services/course_generator.py` |
| Search, curation, reference track | `backend/app/services/course_enricher.py` |
| Source download, card extraction | `backend/app/services/wiki_downloader.py` |
| QA + publishing | `backend/app/services/course_validator.py` |
| Image pipeline | `backend/app/services/wiki_images.py` |
| Author registry | `backend/app/services/wiki_authors.py` |
| Creator canvas | `frontend/components/create/CreateCanvas.tsx` |
| Outline editor | `frontend/components/create/OutlineView.tsx` |
| Coverage assessment | `frontend/components/create/ResearchView.tsx` |
| Enrichment log | `frontend/components/create/EnrichmentView.tsx` |
| Build progress | `frontend/components/create/ProgressView.tsx` |
| Lesson viewer | `frontend/components/create/LessonsView.tsx` |
| Publish flow | `frontend/components/create/PublishView.tsx` |
| Chat co-pilot | `frontend/components/create/ChatPanel.tsx` |
| State management | `frontend/lib/useCreatorState.ts` |
| SSE utilities | `frontend/lib/useCreatorStream.ts` |
