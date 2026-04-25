# SAGE — Foundational Architecture Memory

> AgentMemory bootstrap. Update with the project breakdown when provided.

## Stack
- **Backend:** FastAPI (Python), 9 routers
- **Frontend:** Next.js 15 (App Router) + Tailwind v4
- **Agents:** 6-agent swarm

## Routers (`backend/app/routers/`)
1. `auth` — register / login (JWT) / me
2. `courses` — Lesson CRUD
3. `tutor` — start session, list, take turn
4. `concept_map` — `/concept-map/{session_id}`
5. `network` — peer/social discovery (stub)
6. `replay` — session transcript replay
7. `accessibility` — per-user a11y prefs
8. `dashboard` — aggregate stats
9. `notes` — synthesized study notes
(Plus `GET /health` on root app.)

## Models (`backend/app/models/`)
`User`, `Lesson`, `Session` (tutor_sessions), `Concept` — see `db_schema.md`.

## Auth
Bcrypt (passlib) + HS256 JWT (python-jose). OAuth2 password flow at `/auth/login`.
`get_current_user` dependency guards every non-auth route.

## Agent Swarm (`backend/app/agents/`)
1. `socratic` — guiding questions
2. `explainer` — grounded explanations
3. `concept_mapper` — builds concept graphs
4. `note_taker` — session note synthesis
5. `quiz_master` — generates assessments
6. `orchestrator` — routes between agents

## UI Layout
3-column dashboard: Chat | Concept Map | Notes

## Design System
Persisted at `design-system/sage/MASTER.md` (UI-UX Pro Max).
Primary `#2563EB`, accent `#EC4899`, secondary `#F59E0B`.

## Pending
- Foundational project breakdown from user (paste here when provided).
