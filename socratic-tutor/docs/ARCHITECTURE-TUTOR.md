# Tutor Platform: Architecture & Design Decisions

## Overview

The tutoring platform is the core product: learners pick a lesson, open a chat, and study through guided conversation. The tutor asks before it answers, uses diagrams and quizzes inline, and can search the web for evidence. There is also an open-ended Explore mode where learners can ask anything without a fixed lesson context.

This document covers **everything except the course creator** (see [ARCHITECTURE-COURSE-CREATOR.md](ARCHITECTURE-COURSE-CREATOR.md)). For the project-wide reference, see [PROJECT.md](PROJECT.md).

---

## How a tutor conversation works

```
  User sends message
         │
         ▼
  POST /tutor/chat  (SSE streaming response)
         │
         ├── Load lesson, progress, sessions from DB
         ├── Build TutorContext (lesson content, reference_kb, images, curriculum)
         ├── Select system prompt (v2 for lessons, explore for open-ended)
         │
         ▼
  ┌──────────────────────────────────────────────────────────┐
  │  Agent Loop  (up to 5 tool-call rounds)                  │
  │                                                          │
  │  LLM streams tokens ──► SSE text deltas                  │
  │       │                                                  │
  │       ├── finish_reason: stop → done                     │
  │       ├── finish_reason: length → truncation notice      │
  │       └── finish_reason: tool_calls                      │
  │              │                                           │
  │              ▼                                           │
  │         execute_tool()                                   │
  │         ┌──────────────────────────────────────────────┐ │
  │         │ search_web              (Perplexity)         │ │
  │         │ get_lesson_context      (DB)                 │ │
  │         │ get_lesson_transcript   (DB)                 │ │
  │         │ get_lesson_reference_kb (DB)                 │ │
  │         │ get_curated_resources   (wiki)               │ │
  │         │ get_relevant_images     (wiki)               │ │
  │         │ get_user_progress       (context)            │ │
  │         └──────────────────────────────────────────────┘ │
  │         append tool result → next LLM call               │
  └──────────────────────────────────────────────────────────┘
         │
         ▼
  _stream_with_save: persist user + assistant messages
  Update TutorSession.updated_at
```

### SSE event types

The response is a streaming HTTP body (`text/event-stream`). Each frame is `data: {json}\n\n`.

| Event | Payload | When |
|-------|---------|------|
| `text` | `{"delta": "..."}` | Each streamed LLM token |
| `tool_call` | `{"name": "search_web"}` | Before tool execution |
| `tool_result` | `{"name": "...", "result": {...}}` | After tool returns |
| `error` | `{"message": "..."}` | API or stream failure |
| `done` | `{}` | End of response |

The response header `X-Session-Id` carries the session ID so the client can continue the same thread.

---

## Agent loop

`backend/app/agent/agent_loop.py`

- **`MAX_STEPS = 5`** — outer loop cap on LLM rounds. Each round ends in `stop`, `length`, or `tool_calls`.
- **Prompt selection**: `build_exploration_prompt(context)` when `context.exploration_mode` is true, otherwise `build_system_prompt_v2(context)`.
- **Tool gating**: full `TUTOR_TOOLS` list unless `settings.search_enabled` is false, in which case `search_web` is stripped.
- **API call**: `client.chat.completions.create(stream=True)` with `model=settings.llm_model`, `max_tokens=settings.llm_max_tokens`, `temperature=settings.llm_temperature`.
- **Tool call assembly**: tool call fragments are reassembled by `index` from streamed chunks, then each tool is executed and its result appended as a `role: tool` message before the next LLM call.

---

## Tools

Seven tools are available to the agent:

| Tool | What it does | Notes |
|------|-------------|-------|
| `search_web` | Web search via inference API (Perplexity endpoint) or direct Perplexity API | Delegates to `course_enricher._search` for API routing; results capped to 5; arXiv URLs rewritten to ar5iv |
| `get_lesson_context` | Fetches content, summary, and concepts for any lesson by slug | For cross-lesson references |
| `get_lesson_transcript` | Returns video transcript for current or specified lesson | Defaults to current lesson if no ID given |
| `get_lesson_reference_kb` | Returns the reference KB text for any lesson | The grounding article |
| `get_curated_resources` | Finds matching resources from the pedagogy wiki by concept overlap | Returns up to 8 entries with URLs, descriptions, and why-relevant |
| `get_relevant_images` | Concept-matched image lookup from wiki image metadata | Returns top 6 with paths, captions, and teaching guidance |
| `get_user_progress` | Returns completed lesson titles and counts | Reads from TutorContext built at request time, no DB call |

### search_web routing

The `_search_web` handler delegates to `course_enricher._search()`, which routes based on available API keys:
- **Inference API**: when only `LLM_API_KEY` is configured (sends requests to the Perplexity endpoint via the API gateway)
- **Direct Perplexity**: when `SEARCH_API_KEY` is configured separately

This ensures the tutor agent and the course enricher share identical search infrastructure.

---

## System prompt

The active prompt is `system_prompt_v2.py`. It is a single string assembled at request time from the `TutorContext`:

1. **Role and teaching goal** — Socratic, intuition-first, no premature formulas
2. **Current lesson** — title, summary, key concepts, completed lessons
3. **Teaching mode** — `default`, `eli5`, `analogy`, `code`, `deep_dive` (mode hints change tone)
4. **Teaching principles** — Socratic method, compounding analogies, multimodal toolkit (images, code, quizzes, resources, tables, Mermaid), energy matching, notation rules
5. **Conversation rhythm** — teach / anchor / check / connect pattern, modality diversity target
6. **Reference material** — `lesson_content` markdown (when present)
7. **Detailed reference knowledge** — `reference_kb` markdown (the grounding layer, typically 2K-4K words)
8. **Curriculum index** — slugs, titles, and concepts for other lessons in the same course
9. **Available images** — up to 15 images from wiki with path, caption, concepts, when_to_show
10. **Tools available** — short descriptions of when to use each tool
11. **Output formats** — `<quiz>` JSON schema, `<resource>` JSON schema, `<image>` rules, Mermaid diagrams, `<flow>` / `<architecture>` interactive diagram specs
12. **Factual accuracy tiers** — four levels from reference KB (cite straight) to unsourced (say you're not sure)

### Exploration mode

`system_prompt_explore.py` is used for the Explore surface, where there is no current lesson:
- No embedded lesson body or reference KB
- Receives the full course catalog (`available_courses`) so the model can route questions
- Emphasizes proactive use of `get_lesson_context` and `get_lesson_reference_kb` when a curriculum topic is touched
- Same output format rules (quiz, resource, image, Mermaid, flow, architecture)

---

## TutorContext

`backend/app/agent/context.py`

| Field | Type | Default | Source |
|-------|------|---------|--------|
| `lesson_id` | `str` | `""` | DB |
| `lesson_title` | `str` | `""` | DB |
| `lesson_summary` | `str` | `""` | DB |
| `concepts` | `list[str]` | `[]` | DB (JSON parsed) |
| `lesson_content` | `str` | `""` | DB |
| `reference_kb` | `str` | `""` | DB |
| `completed_lesson_titles` | `list[str]` | `[]` | UserLessonProgress join |
| `curriculum_index` | `list[dict]` | `[]` | All lessons in same course |
| `mode` | `str` | `"default"` | Request body |
| `domain` | `str` | `"technical"` | LearningPath title |
| `available_images` | `list[dict]` | `[]` | lesson.image_metadata or wiki lookup |
| `exploration_mode` | `bool` | `False` | True for /explore |
| `available_courses` | `list[dict]` | `[]` | All courses (explore only) |

---

## Frontend

### Learner app (`frontend/`)

Next.js App Router with a persistent sidebar (course picker, modules, lesson links, progress indicators).

| Route | What it shows |
|-------|---------------|
| `/learn` | Course list — My Courses / Shared with Me / Platform Courses sections |
| `/learn/[pathId]` | Modules and lesson cards with completion state |
| `/learn/[pathId]/[lessonId]` | **Main lesson page**: tutor chat (60%) + resizable lesson content panel (40%) |
| `/explore` | Open-ended chat, no lesson scope (Gemini-style centered empty state) |
| `/quiz` | Pick a topic, LLM-generated quiz with per-question feedback |
| `/concepts` | Browse rich concept pages (LLM-generated on first request, cached) |
| `/projects` | Capstone-style project cards tied to courses |
| `/assess` | Skill assessment from background + progress + quiz scores |
| `/create` | Course creator (see [ARCHITECTURE-COURSE-CREATOR.md](ARCHITECTURE-COURSE-CREATOR.md)) |

### Tutor chat components (`components/tutor/`)

`TutorPanel` is the chat shell. It uses `useTutorStream` — a custom hook that opens a `fetch` request to the chat endpoint, reads the streaming body with `getReader()`, and parses SSE frames.

`MessageBubble` renders:
- **Markdown** via ReactMarkdown + remark-gfm + remark-math + rehype-katex + rehype-highlight
- **Mermaid diagrams** from fenced code blocks — theme-aware rendering (default/dark), re-renders via MutationObserver on theme toggle
- **Inline quizzes** from `<quiz>` XML tags — `InlineQuiz` component with light/dark mode colors
- **Resource cards** from `<resource>` tags — clickable with auto-constructed YouTube URLs, ExternalLink icon
- **Image cards** from `<image>` tags — `ImageCard` with caption, hover-zoom, click-to-expand lightbox
- **Flow diagrams** from `<flow>` tags — `AnimatedFlowBlock` (SVG + framer-motion, step-by-step playback)
- **Architecture diagrams** from `<architecture>` tags — `ArchitectureBlock` (React Flow with drillable nodes)

**Chat UX**:
- Gemini-style empty state: centered input + suggested prompts, moves to sticky bottom bar when messages exist
- Auto-scroll only when user sends a new question (not during AI streaming)
- Teaching mode chips let the user switch modes mid-conversation

---

## Content model

### On disk

```
content/{course-slug}/
  course.json              # Course manifest (slug, title, modules, lessons with content/concepts/sources)
  enrichment/              # Tutor reference KBs ({lesson-slug}_reference_kb.md)
```

### In the database

| Table | Key fields |
|-------|------------|
| `LearningPath` | slug, title, description, level, order_index, `created_by`, `visibility` (public/private), `share_token` |
| `CourseShare` | learning_path_id, user_id (tracks per-user shares) |
| `Module` | learning_path_id, title, order_index |
| `Lesson` | module_id, title, slug, content, summary, concepts (JSON), reference_kb, `sources_used` (JSON URLs), `image_metadata` (JSON), youtube_id, video_title, transcript |
| `UserLessonProgress` | user_id, lesson_id, completed, completed_at |
| `TutorSession` | user_id, lesson_id, created_at, updated_at |
| `ChatMessage` | user_id, lesson_id, session_id, role, content, created_at |
| `ExplorationSession` | user_id, created_at, updated_at |
| `ExplorationMessage` | user_id, session_id, role, content, created_at |
| `Project` | slug, vision, outcomes, challenges, architecture_mermaid, demo/repo URLs |
| `QuizSession / QuizQuestion / QuizAnswer` | Quiz threads, questions, answers |
| `ConceptPage` | topic, rich text, optional lesson_id |

### Seeding

`python seed.py` scans `content/*/course.json`, creates or updates `LearningPath -> Module -> Lesson`, and loads `enrichment/*_reference_kb.md` into `Lesson.reference_kb`. It syncs all lesson fields including `sources_used`, `image_metadata`, `youtube_id`, and `video_title`. Platform courses get `visibility="public"`.

---

## Evaluation framework

The eval system stress-tests tutor quality using **simulated multi-turn conversations** with the real agent loop, real tools, and real system prompt.

### How it works

```
  Scenario YAML (persona + scripted turns + expected behaviors)
         │
         ▼
  StudentSimulator ─────────────────────┐
    (scripted turns first,              │
     then LLM-generated replies)        │
         │                              │
         ▼                              ▼
  run_tutor_turn()                  Scoring Pipeline
    (real agent loop,               ┌──────────────────────────────────┐
     real tools,                    │ Layer 0: Behavioral metrics      │
     non-streaming)                 │ Layer 1: Format safety           │
         │                          │ Layer 2: Prompt alignment judge  │
         ▼                          │ Layer 3: Outcome judge           │
  Conversation transcript           └──────────────────────────────────┘
                                         │
                                         ▼
                                    Results JSON
```

### Scoring — four layers

**Layer 0 — Behavioral metrics** (`scoring/behavioral.py`, deterministic):
- Question ratios (open/closed)
- Image usage (proactive vs reactive)
- Modality diversity (quiz, resource, mermaid, flow, architecture, code, math)
- Tool call counts
- Backward-reference phrases (conversation continuity)

**Layer 1 — Format safety** (`scoring/heuristics.py`, deterministic):
- No fabricated URLs (only when `search_web` was called)
- Quiz JSON validity inside `<quiz>` tags
- Plaintext multiple-choice detected (should be `<quiz>` cards)
- `<resource>` blocks include `url` field
- No duplicate resources across conversation
- Structured block validity (mermaid, flow, architecture)
- Notation consistency with lesson content

**Layer 2 — Prompt alignment judge** (`scoring/prompt_alignment.py`, LLM-based):
- **socratic_method** — questions before answers, guided discovery
- **multimodal_teaching** — uses full toolkit (images, diagrams, code, quizzes)
- **compound_analogies** — builds on analogies across turns
- **factual_grounding** — cites reference KB, searches when unsure
- **adaptive_mode** — matches teaching mode and energy
- **image_discipline** — uses available images appropriately

Includes retry logic (up to 2 retries with backoff) and known-pattern rubric notes for code-heavy scenarios.

**Layer 3 — Outcome judge** (`scoring/llm_judge.py` + `rubric.py`, LLM-based):
- **learning_arc** — does understanding grow across the conversation?
- **conversational_craft** — does it feel like a mentor, not a chatbot?
- **technical_accuracy** — are facts, formulas, and citations correct?
- **intellectual_engagement** — would a real learner stay engaged?
- **adaptive_responsiveness** — does the tutor read the student's signals?

The judge sees the full transcript including tool calls and results.

### Scenarios

40 YAML files in `evals/scenarios/` covering 8 lessons across multiple persona types:

| Lesson | Scenarios | Coverage |
|--------|-----------|----------|
| `lora-parameter-efficient` | 17 | Beginner, intermediate, factual probe, wrong intuition, visual learner, cross-topic, code mode, analogy mode, eli5, deep dive, demands answer, compound analogy, proactive visuals, resource timing, tangent follow, confusion recovery, structured overview |
| `self-attention` | 7 | Format probes (quiz, sources, visual), explore mode probes, compound analogy |
| `building-first-langgraph-agent` | 3 | Beginner, compound analogy, proactive visuals |
| `from-chatbots-to-agents` | 3 | Beginner, compound analogy, proactive visuals |
| `code-execution-retrieval` | 3 | Beginner, compound analogy, proactive visuals |
| `sim-to-real-transfer` | 3 | Beginner, compound analogy, proactive visuals |
| `alignment-rlhf` | 2 | Beginner, technical deep dive |
| `attention-breakthrough` | 2 | Beginner, format probe visual |

### Running evals

```bash
cd backend
python -m evals.run_eval --lesson self-attention                          # All scenarios
python -m evals.run_eval --lesson self-attention --scenario format_probe_quiz  # Single scenario
python -m evals.run_eval --lesson lora --prompt-version v2-explore        # Explore mode
python -m evals.run_eval --lesson lora --compare model-a model-b          # Side-by-side
```

Results are saved as JSON in `evals/results/`.

---

## Configuration

| What | Where | Notes |
|------|-------|-------|
| Non-secret settings | `backend/settings.yaml` | LLM base URL, model IDs (primary, fallback, fast), search URL, usage limits, eval defaults |
| Secrets | `backend/.env` | `LLM_API_KEY`, `JWT_SECRET`, optional `SEARCH_API_KEY` |
| Frontend API URL | `NEXT_PUBLIC_API_URL` env var | Defaults to `http://localhost:8000` |
| Wiki URL | `NEXT_PUBLIC_WIKI_URL` env var | Used in AppHeader wiki link |

The LLM configuration is provider-agnostic: any OpenAI-compatible API works. Change `llm.base_url` and model IDs in `settings.yaml`, set the right key in `.env`.

---

## File map

| Concern | Path |
|---------|------|
| Agent loop | `backend/app/agent/agent_loop.py` |
| System prompt (lesson) | `backend/app/agent/system_prompt_v2.py` |
| System prompt (explore) | `backend/app/agent/system_prompt_explore.py` |
| Tool schemas | `backend/app/agent/tools.py` |
| Tool execution | `backend/app/agent/tool_handlers.py` |
| Context dataclass | `backend/app/agent/context.py` |
| Tutor chat endpoint | `backend/app/routers/tutor.py` |
| Explore chat endpoint | `backend/app/routers/explore.py` |
| Course sharing/visibility | `backend/app/routers/learning_paths.py` |
| DB models | `backend/app/models/learning.py` |
| Config | `backend/app/config.py` + `backend/settings.yaml` |
| Seeding | `backend/seed.py` |
| Eval runner | `backend/evals/runner.py` + `run_eval.py` |
| Eval scoring | `backend/evals/scoring/` (behavioral, heuristics, prompt_alignment, llm_judge, rubric) |
| Eval scenarios | `backend/evals/scenarios/*.yaml` |
| Ablation testing | `backend/evals/run_ablation.py` |
| Frontend chat | `frontend/components/tutor/TutorPanel.tsx` |
| SSE streaming hook | `frontend/lib/useTutorStream.ts` |
| Message rendering | `frontend/components/tutor/MessageBubble.tsx` |
| Mermaid diagrams | `frontend/components/tutor/MermaidBlock.tsx` |
| Quiz cards | `frontend/components/tutor/InlineQuiz.tsx` |
| Navigation | `frontend/components/AppHeader.tsx` |
