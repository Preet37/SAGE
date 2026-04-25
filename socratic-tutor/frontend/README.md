# SocraticTutor Frontend

Next.js 16 (App Router) frontend for the SocraticTutor platform. See the [project README](../README.md) for full documentation.

## Setup

```bash
cp .env.local.example .env.local   # then edit if backend is not on localhost:8000
npm install
npm run dev
```

Runs at [http://localhost:3000](http://localhost:3000). Requires the backend to be running.

## Key Files

- `app/learn/[pathId]/[lessonId]/page.tsx` — Main lesson page with chat + content panels
- `components/tutor/TutorPanel.tsx` — Chat interface with streaming, quizzes, and diagrams
- `lib/useTutorStream.ts` — SSE streaming hook that connects to the backend tutor endpoint
- `lib/api.ts` — Typed API client for all REST endpoints
