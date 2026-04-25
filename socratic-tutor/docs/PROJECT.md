# SocraticTutor — Project Overview

A **wiki-first, LLM-powered Socratic tutoring platform**. The pipeline creates courses by:
1. Building a pedagogy wiki (curated knowledge base of sources, educators, topics)
2. Assessing wiki coverage per lesson concept
3. Enriching gaps via targeted web search + LLM-driven curation
4. Generating student-facing content and tutor-facing reference KBs from wiki sources
5. Serving an interactive tutor agent that uses the wiki for grounded, cited responses

**Stack**: Python 3.11+ / FastAPI backend, Next.js 16 / React 19 frontend, SQLite + SQLModel, Quartz static wiki
**Models**: GPT-5.2 (primary + fallback), GPT-4.1-mini (fast/card extraction)
**Wiki**: 51 topics, 466+ reference sources, 9 subjects, 11 educators, ~517 concepts, 1499+ images
**Courses**: 6 platform courses, 74 lessons total

For detailed iteration history and design decisions, see [decision-log.md](decision-log.md). For architecture deep-dives, see [ARCHITECTURE-TUTOR.md](ARCHITECTURE-TUTOR.md) and [ARCHITECTURE-COURSE-CREATOR.md](ARCHITECTURE-COURSE-CREATOR.md). For product vision and principles, see [VISION.md](VISION.md).

---

## Architecture

```
content/pedagogy-wiki/
  authors.md                    # Unified author registry (76 entries, 107 domains)
  concept-map.md                # Topic -> Subtopic -> Concept hierarchy
  educators/                    # 15 canonical educator profiles
  resources/by-topic/{slug}/
    {slug}.md                   # Topic overview page
    {source}.md                 # Downloaded source (with # Author: header)
    proposals.json              # Curation decisions
    curation-report.md          # Human-reviewable near-misses
    images/images.json          # Image metadata index (binaries gitignored)
    reference/                  # Precision-first reference track
      {source}.md               # Full reference source
      {source}.card.md          # LLM-extracted ~200-300w summary card
      proposals.json, curation-report.md, ramps.json

content/{course-slug}/
  course.json                   # Outline + lesson content (notes, concepts, sources_used, image_metadata)
  enrichment/                   # Tutor reference KBs per lesson

backend/app/
  services/
    course_generator.py         # Content + KB generation, wiki context, ensure_wiki_coverage()
    course_enricher.py          # Coverage assessment, search, curation, audit
    course_validator.py         # QA generation, publishing
    chat_actions.py             # Chat-driven lesson regeneration
    wiki_downloader.py          # Source fetching, card extraction, resource page generation
    wiki_images.py              # Image extraction + annotation pipeline
    wiki_authors.py             # Author registry
  agent/
    system_prompt_v2.py         # Lesson tutor prompt
    system_prompt_explore.py    # Explore mode prompt
    agent_loop.py               # ReAct-style agent loop (up to 5 tool steps, temp=0.7)
    tool_handlers.py            # 7 tools: search_web, get_lesson_context, get_lesson_transcript,
                                #   get_lesson_reference_kb, get_curated_resources,
                                #   get_relevant_images, get_user_progress
    tools.py                    # Tool schemas for LLM
    context.py                  # TutorContext dataclass
  models/learning.py            # LearningPath, CourseShare, Module, Lesson, Project
  routers/
    tutor.py                    # Chat endpoint
    course_creator.py           # Draft CRUD, SSE streams, co-pilot chat
    learning_paths.py           # Course listing, sharing, visibility

backend/evals/                  # 4-layer tutor prompt evaluation
  run_eval.py                   # CLI orchestrator
  run_ablation.py               # Prompt section removal testing
  runner.py                     # Multi-turn simulation
  student_simulator.py          # Scripted + LLM student personas
  scoring/
    heuristics.py               # Layer 0: behavioral metrics (deterministic)
    prompt_alignment.py         # Layer 2: LLM prompt-alignment judge (6 dimensions)
    llm_judge.py                # Layer 3: LLM outcome judge (5 dimensions)
  scenarios/*.yaml              # Per-lesson test scenarios

scripts/
  topic_to_quartz.py            # Wiki -> Quartz pages
  wiki_curator.py               # Automated source quality audit + fix
  update_wiki.py                # Auto-classify topics + rebuild Quartz

backend/scripts/
  test_pipeline.py              # 7-stage pipeline test with checkpointing
  regenerate_and_publish.py     # Batch course regeneration (--enrich, --no-seed)
  eval_quality.py               # 3-tier content quality eval
  eval_image_tutoring.py        # Image tutoring flow eval
  validate_citations.py         # Citation validation against wiki
  bootstrap_wiki.py             # Wiki bootstrapping (--consolidate, --download)
  backfill_reference_track.py   # Batch reference track enrichment
  batch_extract_images.py       # Image extraction + --rehydrate

frontend/components/
  AppHeader.tsx                 # Shared nav bar
  tutor/MessageBubble.tsx       # Chat renderer (quiz/resource/flow/image/mermaid blocks)
  tutor/MermaidBlock.tsx        # Theme-aware Mermaid diagrams
  tutor/InlineQuiz.tsx          # Interactive quiz cards
  tutor/TutorPanel.tsx          # Chat panel (smart scroll, empty/messages state)
  create/ResearchView.tsx       # KB coverage assessment + enrichment log
  create/EnrichmentView.tsx     # Enrichment progress (per-lesson tracking)
  ShareDialog.tsx               # Course sharing (email, link)

backend/tests/test_pipeline/    # 3-tier test suite (unit, mocked integration, real LLM)
  test_*.py                     # 7 pipeline stage tests + images + visibility
```

---

## Key Commands

```bash
# --- Course Operations ---
cd backend && uv run python -m scripts.regenerate_and_publish              # Regenerate all courses
cd backend && uv run python -m scripts.regenerate_and_publish intro-to-llms  # Single course
cd backend && uv run python -m scripts.regenerate_and_publish <slug> --enrich  # With wiki enrichment
cd backend && uv run python seed.py                                          # Seed DB from course.json

# --- Pipeline Testing ---
cd backend && python scripts/test_pipeline.py                    # Full 7-stage test
cd backend && python scripts/test_pipeline.py --resume-from stage3  # Resume from stage

# --- Quality Evaluation ---
cd backend && python -m scripts.eval_quality                     # Structural + grounding
cd backend && python -m scripts.eval_quality --llm               # + LLM rubric scoring
cd backend && python -m scripts.validate_citations               # Citation validation

# --- Tutor Prompt Evaluation ---
cd backend && python -m evals.run_eval --lesson self-attention   # All scenarios for lesson
cd backend && python -m evals.run_eval --lesson self-attention --scenario format_probe_quiz
cd backend && python -m evals.run_eval --lesson self-attention --compare model-a model-b

# --- Wiki Management ---
cd backend && uv run python scripts/bootstrap_wiki.py --consolidate
cd backend && uv run python scripts/bootstrap_wiki.py --download --topic topic-slug
cd backend && uv run python scripts/backfill_reference_track.py --topics topic-slug
python3 scripts/topic_to_quartz.py
python scripts/wiki_curator.py --fix --rebuild                   # Audit + fix + rebuild
python scripts/wiki_curator.py --validate-links                  # Check URLs (~2 min)

# --- Image Pipeline ---
cd backend && PYTHONUNBUFFERED=1 python scripts/batch_extract_images.py
cd backend && PYTHONUNBUFFERED=1 python scripts/batch_extract_images.py --rehydrate

# --- Tests ---
cd backend && python -m pytest tests/ -q                         # Unit + integration
cd backend && python -m pytest tests/ -q -m "llm"               # + real LLM tests
```

---

## Current State

### What's Working
- Full wiki-first pipeline: concept mapping -> coverage -> enrichment -> generation -> validation -> publishing
- 6 courses (74 lessons) with v3 notes prompt + v2 KB prompt + reference track context
- Tutor agent with grounded responses, images, Mermaid diagrams, search, quiz, assessment
- Two-track enrichment: pedagogy (teaching resources) + reference (precision sources with card extraction)
- Audience-aware enrichment: `course_profile` threads through entire pipeline
- Unified enrichment via `ensure_wiki_coverage()` across all course creation paths
- Course visibility: private by default, share by email or link, platform courses public
- Course creator with Research tab: per-lesson coverage assessment, enrichment log, two-step build flow
- Creator chat co-pilot with app workflow awareness and live coverage context
- Automated wiki curation (`wiki_curator.py`, 24h job cycle)
- Quartz wiki with reference library sections, theme-matched to app
- Systematic prompt eval: 4-layer scoring (behavioral, format safety, alignment judge, outcome judge)
- Frontend: Gemini-style chat UX, Mermaid diagrams, syntax highlighting, resizable sidebar, quiz/resource/image cards

### What's Not Done
1. **AI-first lesson layout** — flip to chat-only with notes as toggled panel + AI content actions (podcast, flashcards, study group mode, etc.)
2. **Frontend polish** — responsive design, mobile optimization, accessibility audit
3. **Alembic migrations** — schema changes currently require DB wipe
4. **Context window management** — no explicit token budget/truncation
5. **Explore mode eval scenarios** — format probes exist for lesson mode only
6. **Wiki staging workflow** — enrichment writes directly to tracked wiki files; needs `.pending/` staging area
7. **Multi-user wiki storage** — filesystem doesn't scale; needs DB-backed write-ahead layer
8. **Learner memory & personalization** — structured profiles, session summaries, uploaded content support
9. **Interactive artifact visuals** — `<artifact>` tag for in-chat HTML/JS interactives (prototyped, rolled back)
10. **Slash commands** — `/quiz`, `/hint`, `/simpler`, `/deeper`, `/feedback` across all chat surfaces
