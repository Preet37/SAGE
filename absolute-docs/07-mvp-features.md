# 07 - MVP Feature Requirements

This file defines the full set of features that must be implemented before MVP launch.
If a feature is marked partial or missing, it is a launch blocker until done.

## 1. MVP Definition

MVP for SAGE means:

- A learner can sign in, open a course lesson, chat with the tutor in real time, and see reliable progress updates.
- Tutor outputs are grounded, verified, and replayable.
- Accessibility and collaboration flows are usable in production conditions.
- Core platform reliability, security, and observability are in place.

## 2. Required Feature Set

## 2.1 Core Learning Experience

| ID | Required Feature | Current Status | Definition of Done |
|---|---|---|---|
| MVP-001 | User registration and login with JWT auth | Implemented | Register, login, and protected endpoints pass manual and automated tests. |
| MVP-002 | Protected route enforcement in frontend | Implemented | Unauthenticated users are redirected from protected pages consistently. |
| MVP-003 | Course catalog and lesson navigation | Implemented | All seeded courses and lessons load with correct routing and metadata. |
| MVP-004 | Lesson workspace bootstrap | Partial | Remove dummy session creation and create one valid lesson session only. |
| MVP-005 | Tutor session lifecycle | Implemented | Session create, message persistence, and replay linkage all work end to end. |
| MVP-006 | Real-time streaming tutor responses over SSE | Implemented | Stream delivers token, verification, and done events without parser failures. |
| MVP-007 | Teaching mode selection and persistence | Partial | Mode updates persist and are reflected in tutor prompt and agent trace. |
| MVP-008 | Session replay panel in frontend | Missing | Replay tab renders real replay data and allows viewing prior sessions. |

## 2.2 Tutor Intelligence and Safety

| ID | Required Feature | Current Status | Definition of Done |
|---|---|---|---|
| MVP-020 | Retrieval from lesson chunks | Implemented | Relevant chunks are selected and included in tutor context for each turn. |
| MVP-021 | Embedding generation and storage pipeline | Missing | Lesson chunks have embeddings generated at ingest or via backfill job. |
| MVP-022 | Fallback retrieval behavior | Implemented | Tutor gracefully falls back to lesson content when chunk retrieval is empty. |
| MVP-023 | Verification checks in live stream | Implemented | URL, quiz, grounding, and format checks run per assistant response. |
| MVP-024 | Quiz rendering and grading in chat | Implemented | Quiz blocks are parsed, rendered, and evaluated in UI with feedback. |
| MVP-025 | Provider timeout and retry policy | Missing | Provider failures degrade gracefully with bounded retry and clear errors. |
| MVP-026 | Provider switch support by env | Partial | Anthropic, OpenAI-compatible, Groq, and ASI1 paths are tested and documented. |

## 2.3 Agent and Event System

| ID | Required Feature | Current Status | Definition of Done |
|---|---|---|---|
| MVP-030 | Orchestrator integration into live tutor flow | Missing | Agent orchestrator executes per turn and informs prompt and trace output. |
| MVP-031 | Full agent event emission for all six agents | Missing | Backend emits event types expected by AgentPanel for all agents. |
| MVP-032 | Session-level agent decision persistence | Partial | Session decision history is persisted and visible through replay APIs. |
| MVP-033 | Replay includes complete per-turn agent trace | Partial | Replay payload includes full trace fields needed for debugging and audit. |

## 2.4 Learning Graph and Progress

| ID | Required Feature | Current Status | Definition of Done |
|---|---|---|---|
| MVP-040 | Concept map loads by active course id | Partial | Remove hardcoded course id and use route-derived course consistently. |
| MVP-041 | Mastery updates from concept interactions | Implemented | Node interactions update backend mastery and UI state immediately. |
| MVP-042 | Next concept recommendation correctness | Partial | Fix logic so recommendations do not always return first nodes. |
| MVP-043 | Dashboard overview accuracy | Implemented | Stats match persisted session and mastery data for real users. |
| MVP-044 | Per-course dashboard correctness | Implemented | Course breakdown and next recommendations reflect backend calculations. |

## 2.5 Collaboration and Notes

| ID | Required Feature | Current Status | Definition of Done |
|---|---|---|---|
| MVP-050 | Peer match request and queue behavior | Implemented | Request, waiting, and match transitions are stable and tested. |
| MVP-051 | Peer WebSocket session UI | Missing | Frontend can join room token and exchange real-time peer messages. |
| MVP-052 | Queue timeout and stale-session cleanup | Missing | Waiting users are expired or cleaned to avoid infinite queue artifacts. |
| MVP-053 | Notes AI revision reliability | Partial | Revision output parsing is robust and fallback paths are user-friendly. |
| MVP-054 | Study plan generation and markdown download | Implemented | Plan generation works and downloaded files are valid markdown. |
| MVP-055 | Offline notes restore path | Missing | Previously saved offline notes can be loaded back into notes editor. |

## 2.6 Accessibility, Voice, and On-Device

| ID | Required Feature | Current Status | Definition of Done |
|---|---|---|---|
| MVP-060 | Accessibility profile CRUD and prompt injection | Implemented | Profile changes persist and clearly modify tutor response style. |
| MVP-061 | Accessibility UI-hint application in frontend | Partial | High-value hints are reflected in UI behavior, not only stored metadata. |
| MVP-062 | Voice input with browser fallback | Implemented | Speech input works on supported browsers and fails gracefully otherwise. |
| MVP-063 | Optional ElevenLabs TTS output | Partial | Audio event path is tested and can be toggled from frontend controls. |
| MVP-064 | ZETIC on-device fallback handling | Partial | WebGPU and load failures show clear guidance and never break lesson page. |

## 2.7 Platform, Security, and Quality

| ID | Required Feature | Current Status | Definition of Done |
|---|---|---|---|
| MVP-070 | Alembic migration workflow | Missing | Schema changes are migration-driven with repeatable upgrade path. |
| MVP-071 | Production database move to Postgres | Missing | Production deploy uses Postgres with tested connection and migrations. |
| MVP-072 | Structured logging and request ids | Missing | Backend logs include request and session correlation for debugging. |
| MVP-073 | Rate limiting for auth and tutor endpoints | Missing | Abuse and accidental overload are mitigated by per-route limits. |
| MVP-074 | CORS and secrets hardening | Partial | Production origins and secret handling follow secure defaults. |
| MVP-075 | Automated test suite baseline | Missing | Backend unit/integration and frontend smoke tests run in CI. |
| MVP-076 | CI quality gates | Missing | Lint, type-check, tests, and build run on every PR. |
| MVP-077 | Deployment and rollback runbook | Partial | Deploy, verify, and rollback commands are documented and validated. |
| MVP-078 | Monitoring and alert baseline | Missing | Health, stream errors, latency, and provider failures are monitored. |

## 3. MVP Release Gates

MVP is release-ready only when all conditions below are true:

1. All Missing and Partial items above are completed and verified.
2. End-to-end learner flow passes: login -> lesson -> tutor -> replay -> dashboard.
3. One full regression cycle passes with no P0 or P1 defects.
4. Deployment and rollback are practiced on a staging environment.
5. On-call owner and incident runbook are assigned.

## 4. Tracking Convention

Use this naming convention in tickets:

- Epic: MVP Core, MVP Intelligence, MVP Collaboration, MVP Platform
- Story ID: match table IDs in this file, for example MVP-031
