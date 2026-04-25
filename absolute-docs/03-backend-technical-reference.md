# 03 - Backend Technical Reference

## 1. Stack and Entry Point

- Framework: FastAPI
- ORM: SQLAlchemy async engine/session
- Auth: JWT (`python-jose`) + OAuth2 password form
- DB: SQLite (async driver `aiosqlite`)
- LLM Clients:
  - Anthropic async stream client
  - OpenAI-compatible async client (OpenAI, Groq, ASI1)
- API composition file: `backend/app/main.py`

Application startup behavior:

- Lifespan hook runs `create_tables()` at boot.
- CORS allow-origins includes `settings.frontend_url` plus localhost 3000/3001/3002.
- Routers mounted:
  - `/auth`
  - `/courses`
  - `/tutor`
  - `/concept-map`
  - `/network`
  - `/replay`
  - `/accessibility`
  - `/dashboard`
  - `/notes`

## 2. Configuration Model

## 2.1 Runtime Settings (`app/config.py`)

`Settings` values are read from `.env`:

- LLM: `llm_api_key`, `llm_provider`
- Fetch.ai: `agentverse_api_key`, `asi1_api_key`
- Auth: `jwt_secret`, `jwt_algorithm`
- DB: `database_url`
- Voice: `elevenlabs_api_key`, `elevenlabs_voice_id`
- Server: `frontend_url`, `backend_port`, `content_dir`

## 2.2 YAML Settings (`backend/settings.yaml`)

Used for:

- Provider base URLs
- Provider/model mapping for tutor and judge
- Retrieval defaults (`top_k`, chunk sizing)
- Verification and voice settings metadata

Practical rule:

- Provider selection is controlled by env `LLM_PROVIDER`.
- Actual model names are looked up from yaml map based on provider.

## 3. Authentication and Authorization

## 3.1 Token Issue

- Register: `POST /auth/register` (JSON payload)
- Login: `POST /auth/token` (form-url-encoded; username=email)

Both return:

```json
{
  "access_token": "<jwt>",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "...",
    "username": "...",
    "display_name": "...",
    "teaching_mode": "default"
  }
}
```

## 3.2 Current User Dependency

All protected endpoints use `get_current_user`:

- Reads bearer token via OAuth2 scheme
- Decodes JWT `sub`
- Fetches user row
- Returns 401 on any decode/lookup failure

## 3.3 Auth Endpoints

- `POST /auth/register`
  - Body: `email`, `username`, `password`, optional `display_name`
  - 400 if email exists
- `POST /auth/token`
  - Form fields: `username` (email), `password`
  - 400 on invalid credentials
- `GET /auth/me`
  - Returns current user
- `PATCH /auth/me/mode?mode=<mode>`
  - Valid values: `default|eli5|analogy|code|deep_dive`

## 4. API Surface by Router

## 4.1 Courses (`/courses`)

Public endpoints:

- `GET /courses/` -> list all courses
- `GET /courses/{course_slug}` -> course details
- `GET /courses/{course_slug}/lessons` -> lesson list for course
- `GET /courses/{course_slug}/lessons/{lesson_slug}` -> lesson details

Response models expose lesson metadata but not full server internals.

## 4.2 Tutor (`/tutor`)

### 4.2.1 Session Creation

- `POST /tutor/session`
- Body:

```json
{
  "lesson_id": 1,
  "teaching_mode": "default"
}
```

- Response:

```json
{ "session_id": 123 }
```

### 4.2.2 Chat Streaming

- `POST /tutor/chat`
- Returns `text/event-stream`

Request body:

```json
{
  "lesson_id": 1,
  "message": "Explain backprop",
  "history": [
    { "role": "user", "content": "..." },
    { "role": "assistant", "content": "..." }
  ],
  "session_id": 123,
  "teaching_mode": "code",
  "voice_enabled": false
}
```

SSE events emitted by current implementation:

1. `agent_event` with content retrieval metadata
2. `agent_event` with pedagogy mode metadata
3. repeated `token` events
4. one `verification` event
5. optional `audio` event (base64 MP3)
6. final `done` event
7. `error` event on exception

Example event frames:

```text
event: agent_event
data: {"type":"content_retrieved","chunks":4}

event: token
data: {"content":"Backpropagation "}

event: verification
data: {"passed":true,"flags":[],"score":0.87}

event: done
data: {"response":"...","agent_trace":{...}}
```

Persistence behavior:

- If `session_id` is present, both user and assistant messages are inserted into `tutor_messages`.
- `retrieved_chunks` preview and verification flags are stored per message.

Provider routing logic:

- `anthropic` -> `_stream_anthropic(...)`
- all others -> `_stream_openai(...)` with provider-specific `base_url` and model mapping

## 4.3 Concept Map (`/concept-map`)

- `GET /concept-map/{course_id}`
  - Returns `{ nodes, edges }` with mastery overlay per node
- `POST /concept-map/mastery`
  - Body: `concept_id`, `score`
  - Upserts `student_mastery`, increments attempts, sets `is_mastered` if score >= 0.8
- `GET /concept-map/next/{course_id}`
  - Returns top 3 recommended concepts (note: current implementation returns first 3 due permissive filter)

## 4.4 Network (`/network`)

- `POST /network/peer-match`
  - Body: `concept_id`, `lesson_id`
  - If partner waiting: marks active peer session and returns room token
  - Otherwise: enqueues requester and returns waiting state
- `WS /network/peer-session/{room_token}`
  - Accepts JSON messages and broadcasts to peers in same room token
- `GET /network/status`
  - Returns:
    - active students waiting
    - hot concepts
    - live peer session count

Important runtime detail:

- Waiting room and websocket connection maps are in-memory, per-process.
- Horizontal scaling requires external shared state (Redis/pubsub) to preserve behavior.

## 4.5 Replay (`/replay`)

- `GET /replay/sessions`
  - Lists user sessions, newest first
- `GET /replay/sessions/{session_id}`
  - Returns full ordered turn list with:
    - message role/content
    - timestamp
    - verification pass/flags
    - agent trace
    - chunk previews

## 4.6 Accessibility (`/accessibility`)

- `GET /accessibility/profiles`
  - Enumerates disability and strength profiles
- `GET /accessibility/me`
  - Returns user profile plus generated `prompt_modifier` and `ui_hints`
- `POST /accessibility/me`
  - Saves profile and returns active adaptation summary

Prompt generation source:

- `get_user_accessibility_modifier(user)` is invoked in tutor prompt assembly.

## 4.7 Dashboard (`/dashboard`)

- `GET /dashboard/overview`
  - Aggregated 30-day and global stats
  - Mastery segmentation
  - Verification metrics
  - Recent sessions and active courses
- `GET /dashboard/course/{course_id}`
  - Course-specific concept breakdown and next recommendations

## 4.8 Notes (`/notes`)

- `POST /notes/revise`
  - AI rewrites and analyzes student notes
  - Returns revised markdown + gaps + misconceptions + suggestions
- `POST /notes/generate-plan?lesson_id=...`
  - Generates study guide markdown and downloadable filename

Modeling detail:

- Both routes currently call `asi1_complete(...)` helper from `app/agents/base.py`.
- JSON parsing fallback is implemented for malformed model response.

## 5. Core Modules

## 5.1 Retrieval (`app/core/retrieval.py`)

Functions:

- `chunk_text(text, chunk_size=512, overlap=64)`
- `embed_texts(texts)`
- `get_relevant_chunks(question, lesson_id, db, top_k=4)`

Current behavior notes:

- Uses local `sentence-transformers` model `all-MiniLM-L6-v2`.
- If module import fails, retrieval falls back to full chunk list.
- Seed currently stores chunks but does not precompute embeddings; retrieval scores default to 0.0 unless embeddings are populated later.

## 5.2 Verification (`app/core/verification.py`)

Checks implemented:

- URL fabrication (if no search tool call)
- Quiz JSON validity in `<quiz>...</quiz>` blocks
- Grounding score via keyword overlap with KB chunks
- Max length guard (8000 chars)
- Matched `$$` math delimiters

Output:

```python
VerificationResult(passed: bool, flags: list[str], score: float)
```

## 5.3 Voice (`app/core/voice.py`)

- Uses ElevenLabs text-to-speech endpoint if API key set.
- Sanitizes markdown/code before synthesis.
- Returns raw MP3 bytes or `None` on failure.

## 6. Agent Modules

## 6.1 `app/agents/base.py`

- `get_agent_client()` selects ASI1, Groq, or OpenAI-compatible client.
- `asi1_complete(prompt, ...)` is generic short completion utility.

## 6.2 `app/agents/orchestrator.py`

- Defines six specialized agent task methods.
- Uses `asyncio.gather` for parallel execution.
- Returns a dict of per-agent outputs.

Current status:

- This orchestrator is scaffolded but not currently integrated into `/tutor/chat` streaming pipeline.

## 6.3 `app/agents/uagents_runner.py`

- Defines six uAgents and optional message handlers.
- Intended run command:

```bash
python -m app.agents.uagents_runner
```

Prerequisite: valid `uagents` install and Agentverse credentials.

## 7. Error Handling and Status Codes

Common patterns:

- 400 for invalid credentials/validation enum failures
- 401 for auth token failures
- 404 for missing lesson/course/session/concept
- 200 for most business responses (including waiting states)
- Streaming errors emitted as SSE `error` event instead of HTTP error once stream started

## 8. Extension Playbooks

## 8.1 Add a New Router

1. Create new router under `app/routers/`.
2. Register in `app/main.py` via `app.include_router(...)`.
3. Add auth dependency where needed.
4. Add typed client wrapper in frontend `lib/api.ts`.
5. Update docs in this file + frontend reference.

## 8.2 Add New Teaching Mode

1. Add mode entry in `TEACHING_MODE_PROMPTS` in tutor router.
2. Permit mode in `/auth/me/mode` validator.
3. Add mode button in lesson page mode selector.
4. Verify mode appears in `agent_trace` and prompt output.

## 8.3 Add Verification Rule

1. Implement rule in `verify_response(...)`.
2. Add deterministic unit test for false-positive/false-negative boundaries.
3. Update dashboard metric interpretation if needed.

## 9. Backend Observability Minimum

Recommended immediate additions for productionization:

- Structured request logging with correlation/session id
- Metrics for:
  - tutor stream latency
  - token throughput
  - verification fail-rate
  - peer match wait time
- Explicit timeout/retry policy around external LLM APIs
- Stream cancellation handling when clients disconnect
