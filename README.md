# SAGE — Smart Adaptive Guide for Educators

> **Closing the gap between educators and the people they teach.**

SAGE is a platform built *for teachers* — not just students. It gives educators the tools to deeply understand their own subject matter, create interactive and factually grounded course material, and deliver it to students in a way that is engaging, personalized, and measurably effective.

---

## The Problem

There is a persistent gap between what educators *know* and what students *receive*. Traditional tools force teachers to choose between quality and scale: a hand-crafted lecture reaches 30 students; a recorded video loses nuance; a textbook goes unread. None of these close the gap — they widen it.

---

## What SAGE Does

SAGE gives every educator three core capabilities:

### 1. Learn Content — Deeply

Teachers use the same AI-powered tutor that their students do. Before teaching a topic, an educator can explore it through a Socratic AI conversation, run live simulations, view interactive visualizations, and verify their own understanding — all from a single platform.

- Voice-based AI tutor (ElevenLabs conversational AI)
- Interactive physics/math simulations with real-time parameter controls
- Deep Dive mode — concept cards with linked papers, videos, and figures
- On-device AI (Pocket Tutor) for private, zero-latency learning

### 2. Create Course Material — Publish It

Educators build courses directly inside SAGE. The AI assists with content generation, structure, and accuracy checking. Every lesson is interactive by default.

- AI-assisted course creator with lesson structuring
- Automatic groundedness scoring on every AI response
- Multi-format document ingestion (PDF, DOCX, PPTX, MP4) via Cloudinary
- Image enhancement, OCR, and AI classification for uploaded materials
- QR-code shareable courses

### 3. Monitor Students — Stay Connected

Teachers see exactly where each student is, what they are struggling with, and how their cohort is progressing — without needing a separate LMS.

- Real-time learner presence network (WebSocket peer map)
- Per-student progress tracking across all lessons
- Session history and chat logs per lesson
- Skill assessments and quiz analytics
- Shared courses with visibility controls

---

## Platform Features

| Feature | Description |
|---|---|
| **AI Tutor** | Groq-powered (Llama 3.3 70B) Socratic conversation with streaming responses |
| **Voice Agent** | ElevenLabs real-time speech-to-speech; agent navigates the UI, opens graphs, adds notes on command |
| **Interactive Simulations** | LLM-generated Plotly visualizations with animation, sliders, and real-time parameter control |
| **Code Runner** | Multi-language execution (Python, C, C++, Java, Go, Rust, TypeScript, and more) |
| **Deep Dive** | Rich concept pages linking ArXiv papers, YouTube lectures, GitHub repos |
| **My Documents** | Cloudinary-powered upload, OCR, and semantic memory injection |
| **Pocket Tutor** | WebGPU on-device AI — zero tokens leave the browser |
| **Knowledge Wiki** | Curated interlinked knowledge base of 51 topics across 9 AI/ML subjects |
| **Network** | Real-time peer presence map showing active learners |
| **Multi-agent** | Fetch.ai uAgents for orchestrated, payment-enabled AI delegation |

---

## Hackathon Tracks

| Track | Implementation |
|---|---|
| **Fetch.ai** | uAgents with Chat Protocol + Payment Protocol; multi-agent tutor delegation |
| **Cognition** | LLM groundedness verifier on every tutor response; semantic memory (TF-IDF) |
| **ZETIC** | WebGPU + `@mlc-ai/web-llm` Pocket Tutor — fully on-device inference |
| **Cloudinary** | Document ingestion, AI enhancement, background removal, OCR for My Documents |
| **Arista Networks** | WebSocket pub/sub learner presence network with real-time heartbeats |

---

## Tech Stack

**Frontend:** Next.js 16, React, Tailwind CSS, Plotly.js, `@11labs/client`, `@mlc-ai/web-llm`  
**Backend:** FastAPI, SQLModel, SQLite, Groq API (OpenAI-compatible), Cloudinary SDK  
**AI:** Llama 3.3 70B (tutor), Llama 3.1 8B (fast tasks), ElevenLabs (voice)  
**Infrastructure:** Judge0 CE (code execution), Piston fallback, WebRTC (voice), WebSockets (presence)

---

## Quick Start

```bash
# Backend
cd backend
uv sync
cp .env.example .env   # fill in GROQ_API_KEY, AUTH0_*, CLOUDINARY_*, ELEVENLABS_*
uv run uvicorn app.main:app --reload --port 8000

# Frontend
cd frontend
npm install
cp .env.local.example .env.local  # fill in NEXT_PUBLIC_* keys
npm run dev
```

App runs at `http://localhost:3000`.

---

## Vision

> *"The best teachers are learners first."*

SAGE exists to enrich educator quality by making deep, interactive learning accessible to the people who shape how others learn. When teachers understand their material at a greater depth — and can communicate it through tools that are visual, voice-driven, and factually grounded — the gap between educator and student closes.

**Docs:** [Vision](docs/VISION.md) · [Architecture](docs/ARCHITECTURE-TUTOR.md) · [Course Creator](docs/ARCHITECTURE-COURSE-CREATOR.md)
