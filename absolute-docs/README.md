# SAGE Absolute Technical Documentation

This directory is the engineering handoff package for SAGE (Socratic Agent for Guided Education).
It is written to let a new engineer run, debug, extend, and deploy the system without additional tribal context.

## Audience

- Backend engineers (FastAPI, SQLAlchemy, SSE/WebSocket)
- Frontend engineers (Next.js, Zustand, D3, streaming UI)
- Platform/devops engineers (env, deployment, observability)
- QA engineers validating end-to-end behavior

## How To Use This Documentation

1. Start with `01-system-overview.md` to understand boundaries and runtime behavior.
2. Follow `02-local-development.md` to get a working local stack.
3. Use `03-backend-technical-reference.md` and `04-frontend-technical-reference.md` while implementing features.
4. Use `05-data-model-and-seeding.md` for schema and seed-data changes.
5. Use `06-operations-deployment-and-handoff.md` for deployment, ops, and final handoff checks.

## Document Map

- `01-system-overview.md`
  - Product architecture, component boundaries, user/request lifecycle.
- `02-local-development.md`
  - Exact local setup, env configuration, startup, reset, and daily workflow.
- `03-backend-technical-reference.md`
  - Router-by-router API contract, SSE/WebSocket protocol, agent/core internals.
- `04-frontend-technical-reference.md`
  - App route map, state model, component responsibilities, backend integration.
- `05-data-model-and-seeding.md`
  - Full schema inventory, relationships, seed content, migration guidance.
- `06-operations-deployment-and-handoff.md`
  - Deployment patterns, reliability/security checklist, known gaps, release checklist.

## Repository Scope

The docs in this folder cover the code currently in:

- `backend/`
- `frontend/`
- `scripts/setup.sh`
- `docs.txt`

## Fast Start

Use this only if you already understand the architecture.

```bash
# From repo root
bash scripts/setup.sh

# Terminal 1
cd backend
uvicorn app.main:app --reload --port 8000

# Terminal 2
cd frontend
npm run dev
```

Then open:

- Frontend: http://localhost:3000
- Backend docs: http://localhost:8000/docs

Demo credentials (seeded):

- Email: `demo@sage.ai`
- Password: `demo1234`

## Source-Of-Truth Rule

When docs and implementation differ, implementation wins.
This pack calls out known mismatches explicitly in `06-operations-deployment-and-handoff.md`.
