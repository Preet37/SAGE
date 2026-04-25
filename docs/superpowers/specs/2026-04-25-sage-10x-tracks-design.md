# SAGE 10/10 Track Implementation Design

**Date:** 2026-04-25  
**Status:** Approved  
**Scope:** Deep implementation of all 5 LA Hacks sponsor tracks into SAGE

---

## Overview

SAGE (Socratic Agent for Guided Education) is augmented to achieve 10/10 depth on all 5 sponsor tracks simultaneously. Each track maps naturally to a layer of the tutoring experience. A single demo session shows all 5 in action. Every UI component that uses a sponsor's technology carries a visible **track badge** so judges immediately know what they're evaluating.

### The Layered Story

```
Student Question
      │
      ▼
┌─────────────────────────────────────────────────────┐
│  ZETIC Layer (Track 3)                              │
│  On-device inference via Melange — question never   │
│  leaves the device in Privacy Mode                  │
└──────────────────┬──────────────────────────────────┘
                   │ (if cloud mode)
                   ▼
┌─────────────────────────────────────────────────────┐
│  Fetch.ai Layer (Track 1)                           │
│  uAgents Bureau routes question to 6 specialist     │
│  agents via Agentverse Chat Protocol                │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│  Cognition Layer (Track 2)                          │
│  HyDE retrieval → cross-encoder reranking →         │
│  LLM-as-judge verification → Cognition Score        │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│  Cloudinary Layer (Track 4)                         │
│  Visual uploads processed, OCR extracted,           │
│  diagrams served via CDN with AI transforms         │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│  Arista Layer (Track 5)                             │
│  SAGE Routing Protocol finds optimal peer,          │
│  live network topology, concept graph routing       │
└─────────────────────────────────────────────────────┘
```

### Team Assignment
- **Person 1 → Track 1: Fetch.ai**
- **Person 2 → Track 2: Cognition**
- **Person 3 → Track 3: ZETIC**
- **Person 4 → Track 4: Cloudinary**
- **Person 5 → Track 5: Arista**

### Track Badge System
Every sponsor-powered UI component carries a colored pill badge:
- `fetch.ai` — teal
- `cognition` — purple
- `zetic` — blue
- `cloudinary` — orange
- `arista` — green

Clicking a badge links to the sponsor's platform page or the agent's Agentverse inspection URL.

---

## Track 1: Fetch.ai / Agentverse

### Goal
All 6 SAGE agents run as real uAgents registered on Agentverse, discoverable via ASI:One. The orchestrator routes through the Bureau using actual inter-agent messaging. Chat Protocol is fully implemented. Payment Protocol gates Deep Dive mode.

### Architecture

#### A. Bureau Background Thread
A `bureau.py` module starts 7 uAgents in a background thread (within the same FastAPI process) when the server starts via the lifespan hook:

| Agent | Port | Role |
|-------|------|------|
| Director | 8007 | Public entry point, discoverable on ASI:One |
| Pedagogy | 8001 | Teaching strategy selection |
| Content | 8002 | KB relevance analysis |
| ConceptMap | 8003 | Concept node identification |
| Assessment | 8004 | Quiz generation decisions |
| PeerMatch | 8005 | Peer recommendation |
| Progress | 8006 | Learning trajectory assessment |

Each agent uses a deterministic seed (`sage_agent_seed_{name}`) so its `agent1q...` address is stable across restarts. All addresses are logged at startup:

```
[SAGE] Director Agent:  agent1qxyz... → https://agentverse.ai/agents/agent1qxyz
[SAGE] Pedagogy Agent:  agent1qabc...
```

#### B. Real Inter-Agent Messaging
The `AgentOrchestrator` is refactored to send `ChatRequest` uAgent messages to each specialist agent's address and collect `ChatResponse` results, replacing direct `asi1_complete()` calls. The Director Agent fans out to all 6 specialists in parallel via `asyncio.gather` over uAgent messaging.

The FastAPI tutor endpoint sends a `TutorRequest` to the Director's local Bureau address. The Director assembles all specialist responses and returns a `TutorResponse`. The SSE stream remains unchanged from the student's perspective.

#### C. Chat Protocol (Mandatory)
The Director Agent implements the Agentverse Chat Protocol spec. Any ASI:One user can message `agent1q[director]` directly and receive tutoring — no SAGE website required. The Director handles `ChatMessage` → runs the specialist pipeline → returns `ChatMessage` response in structured format.

#### D. Payment Protocol (Differentiator)
Deep Dive teaching mode is gated behind a micropayment:
- Frontend shows payment prompt when student selects Deep Dive: *"Deep Dive costs 0.001 ASI per session"*
- Director Agent checks for `PaymentConfirmation` before routing to the `deep_dive` prompt modifier
- Uses `uagents.protocols.payments` — `fund_agent_if_low` called at startup
- Successful payment → session created with `deep_dive` mode unlocked

### New Files
- `backend/app/agents/bureau.py` — Bureau background thread startup, agent registration
- `backend/app/agents/director.py` — SAGE Director Agent (Chat + Payment Protocol)
- `backend/app/agents/protocols/chat.py` — Chat Protocol message models
- `backend/app/agents/protocols/payment.py` — Payment Protocol handler
- Updates: `backend/app/main.py` — lifespan starts Bureau in background thread
- Updates: `backend/app/routers/tutor.py` — routes through Director via Bureau messaging
- Updates: `backend/app/agents/orchestrator.py` — uses uAgent messages not asi1_complete

### Integration Points
- Tutor endpoint sends `TutorRequest` to Director address
- Director fans out to 6 specialists, collects results, returns assembled context
- Each specialist still responds with same data shape as before (backwards compatible)
- Payment check is async and non-blocking — falls back gracefully if payment service unavailable

### Badge Placement
- Agent Panel header: `fetch.ai ↗` teal pill (links to Director's Agentverse page)
- Each agent event card: small teal dot
- Deep Dive payment gate: `fetch.ai Payment Protocol` label

---

## Track 2: Cognition / Augment the Agent

### Goal
Measurably improve AI agent capability through HyDE retrieval, cross-encoder reranking, LLM-as-judge verification, and real peer matching. Every improvement is visible and quantified.

### Architecture

#### A. HyDE Retrieval (Hypothetical Document Embedding)
Before fetching KB chunks, a fast LLM call generates a hypothetical perfect answer:

**Flow:** `question → generate_hypothesis(question) → embed(hypothesis) → retrieve(top_8) → rerank(top_4) → tutor_context`

The hypothesis is in the same semantic space as actual KB chunks, dramatically improving retrieval relevance vs embedding the short raw question.

Every retrieval logs:
- `hyde_score`: similarity of retrieved chunks to hypothesis embedding
- `baseline_score`: similarity using raw question embedding  
- `improvement_pct`: `(hyde_score - baseline_score) / baseline_score × 100`

This delta is displayed in the Cognition Score card.

#### B. Cross-Encoder Reranking
After HyDE retrieval returns top-8 chunks, `cross-encoder/ms-marco-MiniLM-L-6-v2` scores each chunk against the original question directly (not via embedding similarity). Cross-encoders see query+document together, making them significantly more accurate than bi-encoder similarity for relevance scoring. Top-4 reranked chunks are passed to the tutor.

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2` (fast, ~80MB, runs on CPU)

#### C. LLM-as-Judge Verification
After every tutor response is generated, a parallel async Haiku call evaluates 4 dimensions:

1. **Grounding** — every claim supported by the KB chunks provided?
2. **Socratic adherence** — guides rather than just answers?
3. **Fabrication** — any invented URLs, citations, statistics?
4. **Scope** — stays on-topic for the lesson?

Returns `confidence_score` (0–100) and `flags[]`. Streams as a new `judge_result` SSE event.

Frontend renders a **Cognition Score card** on every message:
```
◈ Cognition Score: 94/100                    [cognition]
  ✓ Grounded in KB  ✓ Socratic  ✓ No fabrications  ✓ On-topic
  Retrieved 4 chunks · HyDE improved relevance +31%
```
Score < 60 → card turns amber, shows which check failed.

#### D. Real Peer Matching
`PeerMatchAgent` queries `StudentMastery` table for real users matching criteria:
- Mastery score ≥ 0.75 on current concept
- Active in last 7 days
- Not previously matched with this student (novelty bonus)

Returns ranked real `user_id`, `username`, `mastery_score`, `last_active`. No more `f"peer-{i}"` synthetic IDs.

#### E. Adaptive Chunking
Content-aware chunk sizing in `retrieval.py`:
- Code blocks: 100 words per chunk (preserve syntax context)
- Math/equations: kept as single atomic chunks
- Prose: 300 words per chunk
- Overlap: 20% of chunk size

### New Files
- `backend/app/core/hyde.py` — HyDE hypothesis generation + baseline comparison
- `backend/app/core/reranker.py` — cross-encoder reranking layer
- `backend/app/core/judge.py` — LLM-as-judge pipeline, `judge_result` SSE event
- Updates: `backend/app/core/retrieval.py` — wires HyDE → rerank pipeline, adaptive chunking
- Updates: `backend/app/agents/peer_match.py` — real DB queries replacing fake peers
- Frontend: `components/cognition/CognitionScoreCard.tsx` — per-message score display

### Integration Points
- `get_relevant_chunks()` signature unchanged — HyDE + rerank are internal
- New SSE event type `judge_result` added to stream (frontend handles it gracefully if absent)
- PeerMatchAgent now requires DB session — injected via context

### Badge Placement
- Cognition Score card header: `cognition ↗` purple pill
- Verification chip (existing): add purple dot
- Retrieval stats in agent panel: purple label

---

## Track 3: ZETIC / On-Device AI

### Goal
Replace `@mlc-ai/web-llm` with actual ZETIC Melange SDK in a dedicated Expo React Native companion app. All tutoring inference runs on-device via Melange. Privacy Mode proves no data leaves the device.

### Architecture

#### On-Device vs Cloud Split

| Responsibility | Where | Rationale |
|---|---|---|
| Tutoring inference | **On-device (ZETIC Melange)** | Student questions never leave phone |
| Quiz generation | **On-device (ZETIC Melange)** | Low-latency, privacy-first |
| Local RAG retrieval | **On-device (Melange)** | Cached lesson chunks, offline capable |
| Knowledge base seeding | Cloud (SAGE backend) | One-time, heavy computation |
| Concept map persistence | Cloud (SAGE backend) | Shared across devices |
| Multi-agent orchestration | Cloud (SAGE backend) | Requires Agentverse network |
| Peer matching | Cloud (SAGE backend) | Needs real user database |

#### A. Expo React Native App (`sage-mobile/`)
A new `sage-mobile/` directory contains the Expo React Native app. It connects to the same SAGE backend for knowledge base and concept maps, but all inference runs locally via Melange.

**Core screens:**
- `LessonScreen` — full tutoring experience mirroring web app
- `ModelManagerScreen` — Melange model catalog + benchmarking
- `PrivacyScreen` — network monitor proving zero outbound requests

#### B. ZETIC Melange Integration
```typescript
import { MelangeEngine } from '@zetic/melange-rn';

const engine = new MelangeEngine({
  modelId: selectedModel.id,  // from Melange catalog
  device: 'auto',             // auto-selects CPU / GPU / NPU
  onProgress: (pct) => setDownloadProgress(pct),
});

await engine.load();           // downloads, compiles, caches to device
const stream = engine.stream(systemPrompt + userQuestion);
for await (const token of stream) appendToken(token);
```

#### C. Privacy Mode
Toggle in app header. When ON:
- All inference routes to Melange engine (local)
- Network traffic interceptor shows zero outbound requests during tutoring
- Indicator: *"Your questions never leave this device"*

When OFF:
- Requests go to SAGE cloud backend
- Network monitor shows request/response cycle

Both modes are demonstrable in real-time — the most convincing proof of on-device inference possible.

#### D. Model Benchmarking UI (`ModelManagerScreen`)
Browse Melange's model catalog with specs. Tap "Benchmark" to run a live test:
- Generate 10 tokens, measure latency
- Display: model name, size, tokens/sec, quality rating, compute unit (CPU/GPU/NPU)
- User selects preferred model — persisted in device storage

#### E. Performance Dashboard
Live metrics card on every response:
```
⚡ On-Device Performance                   [zetic]
  Compute: NPU (Neural Engine)
  First token: 41ms
  Throughput: 67 tok/s
  vs Cloud: 3.2× faster
  Model: Phi-3.5-mini · 2.4GB · NPU
```

NPU/GPU/CPU detected via Melange's device capability API. NPU (available on modern iPhones, Pixel phones) shows the most dramatic speed advantage.

#### F. Offline-First
After model download, zero connectivity needed:
- Lesson content cached via existing `lessonCache`
- Inference via Melange (fully local)
- Concept map read from local SQLite cache
- On reconnect: sync mastery updates and session history to SAGE backend

### New Directory & Files
- `sage-mobile/` — Expo React Native project
- `sage-mobile/screens/LessonScreen.tsx`
- `sage-mobile/screens/ModelManagerScreen.tsx`
- `sage-mobile/screens/PrivacyScreen.tsx`
- `sage-mobile/components/PerformanceDashboard.tsx`
- `sage-mobile/components/PrivacyModeToggle.tsx`
- `sage-mobile/lib/melange.ts` — Melange engine wrapper + streaming adapter

### Badge Placement
- Privacy mode toggle: `zetic ↗` blue pill
- Performance dashboard card header: `zetic` blue pill
- Model manager screen header: `zetic` blue pill

---

## Track 4: Cloudinary

### Goal
SAGE becomes a visual tutor. Students photograph handwritten notes, textbook pages, and whiteboard diagrams. Cloudinary processes every image before the tutor sees it. All lesson media is served via Cloudinary CDN with AI transformations.

### Architecture

#### A. Visual Upload in Chat (Core Feature)
Camera/upload button in `TutorChat` input bar opens `CldUploadWidget`. On upload, Cloudinary runs a server-side transformation pipeline:

1. Auto-crop to content (remove whitespace/borders)
2. Background removal (clean up desk clutter)
3. Enhance + upscale (sharpen phone captures)
4. OCR extraction (extract all text from image)

Both the optimized image URL and extracted text are sent to the tutor endpoint as additional context. Claude's vision API receives the image URL; the extracted text is injected into the system prompt as `## Visual Context`. Chat bubble renders the image inline via `CldImage` (automatic WebP/AVIF, responsive sizing).

**Student flow:** *"I don't understand this derivation"* + [photo of textbook page] → tutor explains the page content step by step.

#### B. Lesson Diagram Library
Tutor responses can include structured diagram descriptors:
```json
{ "diagram": "neural_network_forward_pass", "style": "annotated" }
```

Backend fetches corresponding diagram from Cloudinary folder `sage/courses/{course}/{lesson}/`, applies real-time transformations (resize, annotation overlays, contrast adjustment), returns optimized `CldImage` URL. All lesson diagrams are organized by `course/lesson/concept` in Cloudinary media library and served via CDN with automatic format negotiation and caching.

#### C. Study Material Gallery (New Tab)
**Materials** tab in the lesson workspace shows all media uploaded across sessions for this lesson:
- `CldImage` thumbnail grid with lazy loading
- Click any material → re-opens in tutor context ("Let's revisit this diagram")
- Powered by Cloudinary search API (filter by lesson, date, tag)
- Materials persist across devices (stored in Cloudinary, not localStorage)

#### D. AI Transformations for Pedagogy
- **Generative fill:** Student uploads incomplete diagram → Cloudinary fills in the missing parts → tutor asks "Does the completed diagram match what you were thinking?"
- **Annotation overlays:** Tutor response references specific image regions → backend adds text overlay annotations via Cloudinary transformation URL parameters, highlighting relevant area before returning to student
- **Before/After viewer:** Shows original photo alongside Cloudinary-processed version with split slider — demonstrates the processing pipeline visually for judges

#### E. Video Lesson Support
`CldUploadWidget` in video mode for lecture uploads:
- Adaptive streaming (HLS) via Cloudinary Video Player
- Auto-generated thumbnails at key timestamps
- Tutor answers questions about video using Cloudinary video URL + transcript as context

### New Files
- `frontend/components/cloudinary/VisualUpload.tsx` — `CldUploadWidget` + upload pipeline
- `frontend/components/cloudinary/DiagramLibrary.tsx` — lesson diagram gallery
- `frontend/components/cloudinary/MaterialsGallery.tsx` — study material history tab
- `frontend/components/cloudinary/BeforeAfter.tsx` — split-slider image comparison
- `frontend/lib/cloudinary.ts` — transformation URL builder, OCR result helper
- `backend/app/routers/media.py` — signed upload endpoint, OCR result handler, diagram fetcher
- Updates: `frontend/components/tutor/TutorChat.tsx` — upload button, inline `CldImage`
- Updates: `backend/app/routers/tutor.py` — accepts `image_url` + `extracted_text` in request

### New Environment Variables
```
NEXT_PUBLIC_CLOUDINARY_CLOUD_NAME=...
CLOUDINARY_API_KEY=...
CLOUDINARY_API_SECRET=...
```

### Badge Placement
- Every `CldImage` component: `cloudinary` orange pill (small, bottom-right of image)
- Upload widget button: `cloudinary ↗` orange pill
- Materials tab header: `cloudinary` orange pill
- Video player: `cloudinary` orange pill

---

## Track 5: Arista Networks / Connect the Dots

### Goal
Replace FIFO peer matching and fake simulated activity with the SAGE Routing Protocol (SRP) — a BGP-inspired multi-factor routing algorithm with concept graph traversal, live network topology visualization, and a full analytics dashboard.

### Architecture

#### A. Remove All Fake Data (Immediate)
Delete all `rng.randint` simulated students from `network.py`. Status endpoint returns real numbers only. Fake `f"peer-{i}"` data in `PeerMatchAgent` replaced with real DB queries.

#### B. SAGE Routing Protocol (SRP)
Multi-factor peer scoring algorithm replacing FIFO:

```
SRP Score = (mastery_delta   × 0.40)
          + (recency_score   × 0.20)
          + (style_compat    × 0.20)
          + (novelty_score   × 0.20)
```

- **mastery_delta:** `peer_mastery - student_mastery` — higher gap means better tutor
- **recency_score:** Exponential decay — studied 2h ago = 0.95, studied 7 days ago = 0.30
- **style_compatibility:** Same preferred teaching mode → 1.0 bonus
- **novelty_score:** Never matched = 1.0 / matched once = 0.6 / matched twice = 0.3

Match result includes full SRP score breakdown so students see *why* they were paired.

#### C. Concept Graph Routing
If no peer available for exact concept, SRP runs BFS on `ConceptEdge` table following `"requires"` edges:

```
Student needs: "Transformer"   → 0 peers available
SRP checks:    "Self-Attention" → 1 peer available ✓

Result: "No direct peer for Transformer.
         SRP routed via next-hop: Self-Attention.
         Peer mastered Self-Attention 3h ago."
```

The routing path is highlighted as a trail through the concept map visualization.

This is the Arista metaphor made literal: BGP-style path selection when there's no direct route.

#### D. Live Network Topology Visualization
Replaces the existing `NetworkPanel` with a D3 force-directed graph:

- **Nodes:** Active students (anonymized as `Learner #4`) sized by mastery score
- **Edges:** Active peer sessions (pulsing green) / pending queue (dashed yellow)
- **Concept clusters:** Nodes visually group around their current study concept
- **Real-time updates:** WebSocket pushes topology diffs every 3s — new matches flash briefly
- **Routing table panel:** Beside the graph, shows each concept as a "route entry" with available peers, avg wait time, session success rate

This is the demo centerpiece — Arista judges will immediately recognize the network topology metaphor.

#### E. Persistent Peer Sessions + Quality Ratings
New `PeerMessage` DB model stores all peer chat messages (session_id, sender_id, content, timestamp). Post-session rating prompt: 1–5 stars + optional note. Sessions appear in Replay tab. Session quality feeds back into SRP scores — high-rated tutors get routing preference boost.

#### F. Network Analytics Dashboard
```
SRP Routing Table                                    [arista]
  Concept              Peers   Avg Wait   Sessions   Δ Mastery
  ─────────────────────────────────────────────────────────────
  Self-Attention         3      0m 42s       47        +18%
  Backpropagation        1      2m 10s       31        +12%
  Transformer            0       —           12        +21%
  LoRA                   2      0m 18s        8         +9%

Network Health
  Active: 4    Queue: 2    Throughput: 6 matches/hr
```

### New Files
- `backend/app/core/srp.py` — SRP scoring algorithm + concept graph BFS routing
- `backend/app/models/peer.py` — `PeerMessage`, `PeerSessionRating` models
- Updates: `backend/app/routers/network.py` — SRP matching, analytics endpoint, remove fake data
- `frontend/components/network/NetworkTopology.tsx` — D3 force-directed live graph
- `frontend/components/network/RoutingTable.tsx` — SRP analytics panel
- `frontend/components/network/PeerChat.tsx` — persistent peer chat with replay
- New Alembic migration: `PeerMessage` + `PeerSessionRating` tables

### Badge Placement
- Network topology graph header: `arista ↗` green pill
- Routing table header: `arista` green pill
- Every peer match notification: `arista` green pill
- Network analytics panel: `arista` green pill

---

## Integration Contracts

### New SSE Event Types
| Event | Producer | Consumer |
|---|---|---|
| `agent_event` | Fetch.ai Director | AgentPanel (existing) |
| `judge_result` | Cognition judge.py | CognitionScoreCard (new) |
| `zetic_metrics` | ZETIC mobile app (local) | PerformanceDashboard (new) |
| `topology_update` | Arista network.py | NetworkTopology (new) |

### New API Endpoints
| Endpoint | Track | Purpose |
|---|---|---|
| `POST /media/upload-signed` | Cloudinary | Signed upload URL generation |
| `POST /media/ocr` | Cloudinary | OCR result ingestion |
| `GET /media/materials/{lesson_id}` | Cloudinary | Study material gallery |
| `GET /network/analytics` | Arista | SRP routing table + health |
| `POST /network/peer-sessions/{id}/rate` | Arista | Post-session quality rating |
| `GET /metrics` | All | Existing — extended with per-track stats |

### Tutor Request Body Extensions
```python
class TutorRequest(BaseModel):
    lesson_id: int
    message: str
    history: list[ChatMessage] = []
    session_id: Optional[int] = None
    teaching_mode: Optional[str] = None
    voice_enabled: bool = False
    # New fields:
    image_url: Optional[str] = None       # Cloudinary
    extracted_text: Optional[str] = None  # Cloudinary OCR
```

---

## Demo Flow (All 5 Tracks in One Session)

1. **Open SAGE mobile app** (ZETIC) → Performance Dashboard shows NPU inference active
2. **Toggle Privacy Mode ON** (ZETIC) → network monitor shows zero outbound requests
3. **Ask a question** (Fetch.ai) → Agent Panel shows 6 real uAgent events firing
4. **See Cognition Score card** (Cognition) → 94/100, HyDE improved retrieval +31%
5. **Upload a photo of a textbook diagram** (Cloudinary) → tutor explains the image
6. **Switch to Network tab** (Arista) → live topology shows active learners, routing table
7. **Request a peer match** (Arista) → SRP finds peer via concept graph, shows routing path
8. **Select Deep Dive mode** (Fetch.ai) → Payment Protocol prompt appears, 0.001 ASI

---

## Dependencies to Add

### Backend
```
# requirements.txt additions
uagents>=0.24.2          # already present — verify Bureau usage
sentence-transformers>=2.7.0  # already present; cross-encoder loaded via this package
cloudinary>=1.36.0
```
Note: The cross-encoder model (`cross-encoder/ms-marco-MiniLM-L-6-v2`) is downloaded via `sentence-transformers` at first use — no separate pip package required.

### Frontend
```
# package.json additions
next-cloudinary          # CldImage, CldUploadWidget, CldVideoPlayer
@cloudinary/url-gen      # URL transformation builder
```

### Mobile
```
# sage-mobile/package.json
expo
@zetic/melange-rn        # verify exact package name at melange.zetic.ai/docs
expo-sqlite              # local concept map cache
```
Note: Confirm the exact React Native package name from ZETIC Melange docs before initialising the project — it may be `@zetic.ai/melange` or similar.

---

## Success Criteria Per Track

| Track | Judge Will See |
|---|---|
| Fetch.ai | 7 real agent addresses in logs, ASI:One can message Director, Deep Dive payment gate works |
| Cognition | Cognition Score card on every message, HyDE improvement % shown, real peer suggestions |
| ZETIC | Privacy Mode with zero outbound requests, NPU badge, latency vs cloud comparison |
| Cloudinary | Photo upload → OCR extraction → tutor explains image, Materials gallery, CldImage everywhere |
| Arista | Live network topology graph, SRP score breakdown on match, concept graph routing path shown |
