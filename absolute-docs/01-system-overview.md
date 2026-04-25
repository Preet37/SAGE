# 01 - System Overview

## 1. Product Purpose

SAGE is a multi-agent tutoring platform that teaches using Socratic dialogue.
The system combines:

- Guided chat tutoring (streamed token-by-token)
- Concept mastery graph and progress tracking
- Accessibility-aware prompting
- Note revision and offline lesson-plan generation
- Peer matching (network-inspired)
- Optional on-device AI assistant in browser (ZETIC track)

## 2. Runtime Architecture

## 2.1 High-Level

- Frontend: Next.js 14 app on port `3000`
- Backend: FastAPI app on port `8000`
- Database: SQLite (`backend/sage.db`) via async SQLAlchemy
- External AI providers:
  - Anthropic (default path in tutor stream)
  - OpenAI-compatible providers (OpenAI, Groq, ASI1)
- Optional services:
  - ElevenLabs for TTS
  - Fetch.ai uAgents (deployed separately)

## 2.2 Boundary Model

- Browser never talks directly to database.
- Browser calls backend REST endpoints, plus receives SSE stream for tutor responses.
- Browser can open WebSocket for peer-session room messaging.
- Backend owns auth, persistence, retrieval, verification, and orchestration metadata.

## 3. Major Subsystems

## 3.1 Tutor Engine

Primary endpoint: `POST /tutor/chat`

Core pipeline per user message:

1. Validate lesson and user.
2. Resolve teaching mode.
3. Retrieve relevant lesson chunks (`top_k=4`).
4. Inject accessibility modifier from user profile.
5. Build system prompt with course/lesson/mastery context.
6. Stream LLM output as SSE token events.
7. Verify output (grounding, quiz format, URL fabrication checks).
8. Optionally synthesize voice bytes.
9. Persist user + assistant turn to `tutor_messages` (if `session_id` provided).

## 3.2 Learning Graph and Progress

- Concept map: `GET /concept-map/{course_id}`
- Mastery updates: `POST /concept-map/mastery`
- Dashboard aggregation: `/dashboard/*`

Mastery state is persisted in `student_mastery` and overlaid on static concept graph nodes/edges.

## 3.3 Network / Peer Matching

- Match request: `POST /network/peer-match`
- Real-time peer room: `WS /network/peer-session/{room_token}`
- Status panel feed: `GET /network/status`

The matching queue is in-memory for active process runtime and is also mirrored into `peer_sessions` rows.

## 3.4 Accessibility Adaptation

- Profiles: `GET /accessibility/profiles`
- User profile read/write: `GET/POST /accessibility/me`

Prompt modifier strings are generated per profile and embedded into tutor system prompt.

## 3.5 Notes and Study Artifacts

- Note revision: `POST /notes/revise`
- Study plan generation: `POST /notes/generate-plan?lesson_id=...`

Both are currently backed by `asi1_complete(...)` in `app/agents/base.py`.

## 3.6 Replay and Audit

- Session list: `GET /replay/sessions`
- Session replay: `GET /replay/sessions/{session_id}`

Each stored turn includes verification result and lightweight agent trace metadata.

## 4. Frontend Surface Areas

- Landing + auth pages
- Course/lesson explorer
- Lesson workspace with 3-column layout:
  - Left: agent activity panel
  - Center: chat/map/network/notes/replay tabs
  - Right: voice, key concepts, ZETIC panel
- Dashboard analytics page

## 5. Data Ownership by Layer

- Backend owns:
  - Auth identity and JWT validation
  - All persistence and calculations
  - Prompt assembly and LLM invocation
  - Verification rules
- Frontend owns:
  - Local auth token and user store (Zustand persisted)
  - Streaming event rendering and UX state
  - Interactive concept graph behavior
  - Local note cache/download actions

## 6. Hackathon-Track Mapping (as implemented)

- Fetch.ai
  - Agent scaffolding exists in `backend/app/agents/uagents_runner.py`
  - Main tutor runtime currently uses internal trace metadata, not live uAgent orchestration.
- Cognition
  - Retrieval + verification + replay fully wired in live chat path.
- Arista
  - Peer matching/status endpoints live; full frontend WebSocket peer-chat UI is not implemented yet.
- ZETIC
  - On-device inference component exists and is browser-capability gated.
- Light the Way
  - Accessibility profiles and adaptive prompting are wired into tutor prompt creation.

## 7. End-to-End Sequence (Current)

1. User logs in and opens lesson page.
2. Frontend creates tutor session.
3. User sends prompt.
4. Frontend opens `POST /tutor/chat` and parses SSE events.
5. Backend streams `agent_event` + `token` + `verification` + `done` events.
6. Frontend appends tokens to assistant bubble and updates agent panel + verification chip.
7. Backend commits conversation rows for replay/dashboard stats.

## 8. Key Engineering Realities

- Local DB is SQLite; no migration workflow is enforced yet.
- Some advanced track features are partially scaffolded and need production-hardening.
- Settings are split between `.env` and `settings.yaml`; runtime behavior depends on both.

For setup and operations details, continue to `02-local-development.md`.
