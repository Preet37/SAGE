# 06 - Operations, Deployment, and Handoff

## 1. Deployment Architecture Recommendations

## 1.1 Minimum Production Topology

- Frontend: Next.js deployment (Vercel or containerized Node runtime)
- Backend: FastAPI served by Uvicorn/Gunicorn behind reverse proxy
- Database: Postgres (replace SQLite for durability/concurrency)
- Optional workers:
  - background job for embedding generation
  - async queue for long-running note-plan generation

## 1.2 Suggested Process Layout

- `frontend` service
- `backend-api` service
- `db` service
- optional `redis` service (if scaling peer matching and websocket fanout)

## 2. Environment Matrix

## 2.1 Required in All Environments

- `LLM_PROVIDER`
- `LLM_API_KEY` (or provider-specific equivalent)
- `JWT_SECRET`
- `DATABASE_URL`
- `FRONTEND_URL`

## 2.2 Optional / Feature-Gated

- `ELEVENLABS_API_KEY`, `ELEVENLABS_VOICE_ID` (voice output)
- `AGENTVERSE_API_KEY`, `ASI1_API_KEY` (Fetch.ai tracks)
- `SEARCH_API_KEY` (reserved; currently not wired into tutor flow)

## 2.3 Consistency Rule

Keep `.env.example`, deployment secrets, and docs synchronized on every env change.

## 3. Startup and Health

## 3.1 Startup Commands

Backend:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Frontend:

```bash
npm run build
npm run start
```

## 3.2 Health Endpoints

- `GET /health` for liveliness
- `GET /` for service metadata sanity check

## 4. Observability Requirements

Minimum recommended telemetry in production:

- Request logs with request id and user/session id where available
- Tutor stream metrics:
  - time-to-first-token
  - full response latency
  - stream error rate
- Verification metrics:
  - pass/fail count
  - top verification flags
- Network metrics:
  - waiting queue size
  - peer match latency
- Dashboard aggregation latency

## 5. Security Checklist

Required before production handoff:

1. Rotate `JWT_SECRET` away from default and store in secret manager.
2. Restrict CORS origins to trusted frontend domains only.
3. Enforce HTTPS and secure cookie/token storage strategy.
4. Add rate limiting for auth and chat endpoints.
5. Add payload size constraints for note submissions and chat history.
6. Validate and sanitize all user-generated markdown before display/export if untrusted contexts are added.

## 6. Performance and Scaling Considerations

## 6.1 Tutor Stream

- External LLM latency dominates end-user response time.
- Introduce retry/backoff with bounded timeout for provider calls.
- Consider provider abstraction with fallback sequence on failures.

## 6.2 Retrieval

- Semantic retrieval quality is limited until embeddings are populated.
- Add async embedding job on lesson ingest and persist vectors.

## 6.3 Peer Matching / WebSocket

- Current waiting queue and websocket maps are in-memory.
- For multi-instance scaling, move these to shared infra (Redis + pubsub).

## 6.4 Database

- SQLite limits concurrent write throughput.
- Migrate to Postgres for production workloads.

## 7. Known Gaps and Mismatches (Current Codebase)

These are important handoff notes for incoming engineers.

1. `backend/.env.example` mentions `nvidia` provider option, but provider branches implemented are `anthropic|openai|groq|asi1`.
2. `AgentOrchestrator` exists but is not currently invoked in live tutor stream path.
3. Frontend `AgentPanel` expects six distinct event types; backend currently emits two (`content_retrieved`, `pedagogy_applied`).
4. Lesson page currently creates a first session using `lesson_id=0` before creating actual session.
5. Lesson page concept map fetch is hardcoded to `courseId=1` (demo shortcut).
6. `GET /concept-map/next/{course_id}` currently returns first three nodes due permissive condition.
7. Retrieval chunks are seeded without embeddings, limiting semantic ranking quality.
8. Frontend network panel displays match status but does not connect to websocket room for live peer chat.
9. ZETIC component relies on CDN-loaded WebLLM global; browser support and runtime loading can vary.

## 8. Recommended Immediate Backlog (Priority Order)

1. Wire live tutor flow to orchestrator outputs and emit full agent event set.
2. Remove dummy session creation and enforce valid lesson id in session API.
3. Fix concept-map next recommendation logic and add tests.
4. Add embedding generation pipeline and backfill existing lessons.
5. Implement websocket peer chat client UI and reconnection logic.
6. Introduce migration workflow and move prod DB to Postgres.

## 9. QA Acceptance Test Matrix

Before release, verify:

1. Auth: register/login/me/mode update all pass.
2. Tutor: stream produces token + verification + done events.
3. Replay: completed session appears with turns and traces.
4. Concept map: node click updates mastery and dashboard reflects it.
5. Accessibility: profile update changes subsequent tutor response style.
6. Notes: revise and study-plan generation succeed.
7. Dashboard: aggregates sessions/messages/mastery correctly.
8. Network: peer-match waiting and matched responses are correct.
9. Voice: transcript ingestion works on supported browser.
10. ZETIC: model load and local inference succeeds on WebGPU-capable hardware.

## 10. Final Engineer Handoff Checklist

Use this as signoff criteria.

1. Environment and secrets documented and provisioned.
2. Local bootstrap validated on a clean machine.
3. Core API contracts confirmed against implementation.
4. Frontend panels mapped to endpoint contracts.
5. Known gaps explicitly accepted or ticketed.
6. Rollback plan and monitoring dashboard defined.
7. On-call/debug owner assigned for first production week.

## 11. Ownership Boundaries for New Team

- Backend owner:
  - API contracts, auth, prompting, retrieval, verification, persistence.
- Frontend owner:
  - streaming UX, panel interactions, accessibility UX, browser features.
- Platform owner:
  - deployment, secrets, observability, scale and resilience.

When onboarding a new engineer, give them this folder plus direct code access; no additional tribal notes should be required for first contribution.
