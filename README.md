# SAGE — Socratic Agent for Guided Education

> Multi-agent AI tutor powered by Fetch.ai · Built for LA Hacks 2026

![Light the Way](https://img.shields.io/badge/track-Light%20the%20Way-green)
![Fetch.ai](https://img.shields.io/badge/sponsor-Fetch.ai-blue)
![Cognition](https://img.shields.io/badge/sponsor-Cognition-purple)
![Arista](https://img.shields.io/badge/sponsor-Arista-orange)

SAGE transforms passive reading into an active Socratic dialogue. Six Fetch.ai uAgents
coordinate in real-time to deliver personalized tutoring, live concept maps, voice interaction,
verified outputs, and peer learning — all in one unified interface.

## Architecture

```
Frontend (Next.js 14)
  ├── TutorChat      — Streaming SSE chat with markdown + math rendering
  ├── ConceptMap     — Live D3 force-directed knowledge graph
  ├── VoiceAgent     — Web Speech API voice input + ElevenLabs output
  ├── AgentPanel     — Real-time Fetch.ai agent activity feed
  └── NetworkPanel   — Arista-style peer routing dashboard

Backend (FastAPI + Python 3.11)
  ├── /tutor/chat    — SSE-streamed Socratic responses (Anthropic / ASI1-Mini)
  ├── /concept-map   — Student mastery graph
  ├── /network       — WebSocket peer matching (Arista track)
  └── /replay        — Full session replay with agent decisions (Cognition track)

Fetch.ai Agents (6 uAgents on Agentverse)
  ├── Pedagogy Agent      — Selects optimal teaching mode per student
  ├── Content Agent       — Semantic KB retrieval (RAG)
  ├── Concept Map Agent   — Updates knowledge graph nodes
  ├── Assessment Agent    — Generates adaptive quizzes
  ├── Peer Match Agent    — Routes students to peers
  └── Progress Agent      — Tracks mastery + recommends next steps
```

## Hackathon Tracks

| Track | Implementation |
|-------|----------------|
| **Fetch.ai** | 6 uAgents registered on Agentverse, ASI1-Mini LLM, Chat Protocol |
| **Cognition** | Output verification layer, semantic retrieval, session replay |
| **Arista Networks** | Peer routing dashboard, WebSocket peer sessions, network visualization |
| **Light the Way** | Socratic pedagogy, voice interface, concept mastery tracking |

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 20+
- `uv` (recommended): `curl -LsSf https://astral.sh/uv/install.sh | sh`

### 1. Backend

```bash
cd backend
cp .env.example .env
# Edit .env — add LLM_API_KEY (Anthropic or OpenAI) at minimum

# Install dependencies
pip install -r requirements.txt

# Seed the database with courses and a demo user
python seed.py

# Start the API server
uvicorn app.main:app --reload --port 8000
```

### 2. Frontend

```bash
cd frontend
cp .env.local.example .env.local
npm install
npm run dev
# → http://localhost:3000
```

### 3. Fetch.ai Agents (optional — enhances agent panel)

```bash
cd backend
# Add AGENTVERSE_API_KEY to .env first
python -m app.agents.uagents_runner
```

## Demo Credentials

```
Email:    demo@sage.ai
Password: demo1234
```

## Environment Variables

### Backend (`.env`)
```
LLM_API_KEY=sk-ant-...         # Anthropic or OpenAI key
LLM_PROVIDER=anthropic          # anthropic | openai | asi1
AGENTVERSE_API_KEY=...          # Fetch.ai Agentverse key
ASI1_API_KEY=...                # ASI1-Mini key (same as agentverse usually)
JWT_SECRET=your-secret-here
ELEVENLABS_API_KEY=...          # Optional: voice synthesis
```

### Frontend (`.env.local`)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Key Features

### Socratic Tutoring Engine
- Five teaching modes: Socratic (default), ELI5, Analogy, Code-first, Deep Dive
- Streaming responses via SSE
- Markdown + LaTeX math rendering
- Embedded adaptive quizzes in `<quiz>` blocks

### Fetch.ai Agent Swarm (6 Agents)
Every student message fires all 6 agents concurrently via `asyncio.gather`:
- **Pedagogy Agent** — detects misconceptions, recommends teaching mode
- **Content Agent** — semantic retrieval (finds relevant KB chunks via cosine similarity)
- **Concept Map Agent** — identifies concept nodes touched by the question
- **Assessment Agent** — decides when to insert a quiz
- **Peer Match Agent** — flags when peer learning would help
- **Progress Agent** — updates mastery scores, suggests next topics

### Output Verification (Cognition Track)
Every LLM response passes through `core/verification.py`:
- URL fabrication detection (blocks hallucinated links)
- Quiz format validation (JSON schema check)
- Grounding score (keyword overlap with KB)
- Math notation consistency (unmatched `$$` detection)

### Peer Network (Arista Track)
- Concept-similarity routing: students matched by current learning node
- "Mastered" peers preferred as tutors over co-learners
- Real-time WebSocket room for peer sessions
- Network dashboard: active students, hot concepts, live pairs

### Session Replay (Cognition Track)
Every turn stores: retrieved chunks, verification result, agent decisions, timestamps.
The `/replay` endpoint makes every decision auditable and explainable.
