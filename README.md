# SocraticTutor

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)

Socratic AI tutor for technical courses. Learners work in conversation, not a wall of slides—the tutor asks, nudges, and can use live search when you configure an API key. Who this is for and how grounding works: [`docs/VISION.md`](docs/VISION.md).

**Docs:** [Vision](docs/VISION.md) · [Tutor architecture](docs/ARCHITECTURE-TUTOR.md) · [Course Creator architecture](docs/ARCHITECTURE-COURSE-CREATOR.md)

## What's in the repo

| Part | What it does |
|------|----------------|
| `frontend/` | Learner app: courses, lessons, tutor chat, quizzes, concepts, capstone **Projects**, assessments. |
| `course-creator/` | Optional **wizard** that turns research and sources into reference KBs and lesson content (same backend). Details: `docs/ARCHITECTURE-COURSE-CREATOR.md`. |
| `backend/` | FastAPI: auth, tutor agent and tools, course-creator APIs, SQLite + `seed.py`, evaluation runners. |
| `content/` | Course **packages** (manifest + markdown). Treated as data—you can swap curricula without rewriting the app. |

**License:** Apache 2.0. **Models:** any OpenAI-compatible API via `settings.yaml` + `LLM_API_KEY` in `.env`. **Search:** optional (e.g. Perplexity) when `SEARCH_API_KEY` is set.

## Design (why it is shaped this way)

- **Grounding** — Lessons use **reference KB** text (and optional web search in-session) so answers lean on sourced material, not improvisation as fact.
- **Engine vs. curriculum** — Application code stays separate from `content/`; you publish new material from files or from the course creator into the DB.
- **Regression testing** — The **eval** framework simulates students across personas so you can compare prompts and models on the same lessons.
- **Authoring** — **Browser wizard** for research-first course creation, or **git-friendly packs** under `content/` for manual edits.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  Frontend (Next.js 16 / React 19)                          │
│  ┌──────────┐  ┌──────────────┐  ┌───────────────────────┐ │
│  │ Auth     │  │ Course       │  │ Lesson Page           │ │
│  │ Pages    │  │ browser      │  │ ┌───────┐ ┌─────────┐ │ │
│  └──────────┘  └──────────────┘  │ │ Tutor │ │ Content │ │ │
│                                  │ │ Chat  │ │ Panel   │ │ │
│                                  │ └───────┘ └─────────┘ │ │
│                                  └───────────────────────┘ │
└──────────────────────┬──────────────────────────────────────┘
                       │ SSE streaming
┌──────────────────────▼──────────────────────────────────────┐
│  Backend (FastAPI)                                          │
│  ┌─────────────────────────────────────────────────┐       │
│  │ Agent Loop                                       │       │
│  │  System Prompt + Lesson Content + Reference KB   │       │
│  │  ┌──────────┐  ┌──────────┐  ┌───────────────┐  │       │
│  │  │ search   │  │ get      │  │ get_lesson    │  │       │
│  │  │ _web     │  │ _context │  │ _transcript   │  │       │
│  │  └────┬─────┘  └──────────┘  └───────────────┘  │       │
│  │       │                                          │       │
│  └───────┼──────────────────────────────────────────┘       │
│          │                                                  │
│  ┌───────▼──────────┐  ┌──────────┐  ┌───────────────────┐ │
│  │ Perplexity       │  │ SQLite   │  │ Eval Framework    │ │
│  │ Search API       │  │ (tutor   │  │ (scenarios,       │ │
│  │ (optional)       │  │  .db)    │  │  LLM judge)       │ │
│  └──────────────────┘  └──────────┘  └───────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## Courses

Example paths shipped with the seed data (you can add your own under `content/`):

| Course | Lessons | Description |
|--------|---------|-------------|
| ML/AI Foundations | 8 | Neural networks through LoRA/PEFT, with video lectures |
| Intro to Agentic AI / others | varies | Additional seeded topics (e.g. agents, multimodal, physical AI) — see `content/` after `seed.py` |

Each lesson has curated content, a summary, key concepts, and a reference knowledge base (where enriched) so the tutor can stay grounded in prepared material.

## Quick Start

### Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (fast Python package manager)
- Node.js 20+
- An API key for any OpenAI-compatible LLM provider (OpenAI, NVIDIA, Azure, Together, etc.)

### Backend

```bash
cd backend
uv sync
cp .env.example .env   # edit with your LLM_API_KEY and JWT_SECRET
uv run python seed.py
uv run uvicorn app.main:app --reload --port 8000
```

The API docs are available at [http://localhost:8000/docs](http://localhost:8000/docs) (interactive Swagger UI).

### Frontend

```bash
cd frontend
cp .env.local.example .env.local    # edit if backend is not on localhost:8000
npm install
npm run dev
```

The app runs at [http://localhost:3000](http://localhost:3000). Register an account and start learning.

### Course creator (optional)

Requires the backend running (same `JWT` / API as the main app).

```bash
cd course-creator
npm install
npm run dev   # http://localhost:3001
```

If the API is not at `http://localhost:8000`, set `NEXT_PUBLIC_API_URL` for the course creator (see `course-creator/lib/api.ts`).

## Configuration

Non-secret settings live in `backend/settings.yaml`:

- **LLM Provider** — `llm.base_url` points at any OpenAI-compatible API
- **Models** — tutor, judge, rerank, and student simulator model IDs are configured in `models:` (default: Claude Sonnet via NVIDIA inference API)
- **Search** — optional Perplexity web search (enabled when `SEARCH_API_KEY` is set)
- **Auth** — JWT algorithm, expiry (7 days)
- **Database** — SQLite path

Secrets (`LLM_API_KEY`, `JWT_SECRET`, optional `SEARCH_API_KEY`) stay in `backend/.env` and are never committed.

### Using a Different LLM Provider

SocraticTutor works with any OpenAI-compatible API. To switch providers, update two things:

1. **`backend/settings.yaml`** — change `llm.base_url` and the `model_id` values
2. **`backend/.env`** — set `LLM_API_KEY` to your provider's API key

For example, to use NVIDIA's inference API:

```yaml
llm:
  base_url: "https://inference-api.nvidia.com"

models:
  tutor:
    model_id: "aws/anthropic/bedrock-claude-sonnet-4-6"
```

## How the Tutor Works

1. The student selects a lesson and types a question.
2. The backend builds a system prompt with the lesson content, reference KB, curriculum index, and student progress.
3. The LLM generates a response in a Socratic style — asking questions, using analogies, building on the student's reasoning.
4. If the LLM needs external evidence and search is configured, it calls `search_web` (Perplexity) and incorporates the results with citations.
5. Responses stream to the frontend via SSE, with inline rendering of markdown, Mermaid diagrams, and interactive quizzes.

### Teaching Modes

Students can switch modes to change how the tutor explains concepts:

| Mode | Behavior |
|------|----------|
| Default | Balanced Socratic approach |
| ELI5 | Simple language and everyday analogies |
| Analogy | Real-world comparisons |
| Code | Code-first examples |
| Deep Dive | Mathematical depth and formal notation |

### Tools Available to the Tutor

| Tool | Purpose |
|------|---------|
| `search_web` | Live web search via Perplexity for current facts, papers, benchmarks (requires `SEARCH_API_KEY`) |
| `get_lesson_context` | Retrieve content from other lessons in the curriculum |
| `get_lesson_transcript` | Access video transcripts when students reference the video |
| `get_user_progress` | Check which lessons the student has completed |

## Evaluation Framework

The eval system tests tutor quality with simulated multi-turn conversations:

```bash
cd backend

# Run all scenarios for the LoRA lesson
uv run python -m evals.run_eval --lesson lora

# Run a single persona
uv run python -m evals.run_eval --lesson lora --scenario curious_beginner

# Compare models side-by-side (use full model_id values from settings.yaml)
uv run python -m evals.run_eval --lesson lora --compare aws/anthropic/bedrock-claude-sonnet-4-6 openai/openai/gpt-4.1

# Use the v2 system prompt
uv run python -m evals.run_eval --lesson lora --prompt-version v2
```

### Scoring

**Layer 1 — Heuristic checks** (automated):
- No fabricated URLs (URLs only appear when `search_web` was called)
- Quiz format validity (JSON structure inside `<quiz>` tags)
- Mathematical notation consistency

**Layer 2 — LLM judge** (scores 1-5 on each dimension using the configured judge model):
- **Learning Arc** — Does the student's understanding grow across the conversation?
- **Conversational Craft** — Does it feel like a dialogue with a mentor, not a chatbot?
- **Technical Accuracy** — Are facts, formulas, and citations correct?
- **Intellectual Engagement** — Would a real learner stay engaged?
- **Adaptive Responsiveness** — Does the tutor read the student's signals?

### Student Personas

| Persona | Tests |
|---------|-------|
| Curious Beginner | Intuition-first teaching, avoids premature formulas |
| Sharp Intermediate | Depth handling, technical precision |
| Factual Probe | Accuracy under scrutiny, proper sourcing |
| Demands Answer | Balancing direct answers with guided discovery |
| Wrong Intuition | Misconception detection and correction |
| Visual Learner | Diagram and visual tool usage |
| Cross Topic | Connecting concepts across lessons |

## Content Pipeline

There are two ways to add a course:

1. **Course Creator wizard** (recommended) — Run the Course Creator frontend at `http://localhost:3001`. It walks you through a 4-phase pipeline: outline generation, content creation, web-search enrichment, and QA validation — with human review gates at every step. See [Course Creator architecture](docs/ARCHITECTURE-COURSE-CREATOR.md).

2. **Manual** — Create a `content/<slug>/course.json` following the [content schema](content/README.md), then run `python seed.py` from `backend/` to load it into the database.

## Project Structure

```
SocraticTutor/
├── backend/
│   ├── app/
│   │   ├── agent/          # Tutor LLM loop, system prompts, tool handlers
│   │   ├── models/         # SQLModel data models (User, Lesson, Progress)
│   │   ├── routers/        # auth, tutor, paths, progress, projects, course_creator, …
│   │   └── schemas/        # Pydantic request/response schemas
│   ├── evals/
│   │   ├── scenarios/      # YAML persona definitions with scripted turns
│   │   └── scoring/        # Heuristic checks + LLM judge rubric
│   ├── scripts/            # Concept preloading
│   ├── seed.py             # Database seeding
│   └── settings.yaml       # Non-secret configuration
├── frontend/
│   ├── app/                # Next.js App Router pages
│   ├── components/
│   │   ├── tutor/          # Chat panel, message bubbles, quizzes, diagrams
│   │   ├── content/        # Lesson content viewer, video player
│   │   └── ui/             # shadcn/ui base components
│   └── lib/                # API client, auth, SSE streaming hook
└── course-creator/         # Next.js wizard for AI-assisted course authoring (optional)
```
