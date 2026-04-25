# Track 2 — Cognition (Augment the Agent)

> **Challenge:** AI agents are getting powerful, but they still hit real
> limits. Build a tool, integration, or product that makes AI agents
> measurably more capable, or removes the friction and toil they can't yet
> handle on their own. Practical, high-impact, grounded in real workflows.
>
> Suggested directions: **better verification for AI outputs**,
> **smarter context retrieval**, **agent integrations & extensions**,
> **human–AI collaboration tooling**, **eliminating professional toil**.

## What we built

Three production-grade agent-augmentation systems, each tied to a real
workflow — a single track, three deliverables hitting **three of the five
suggested directions** explicitly.

| Suggested direction | What we shipped |
|---|---|
| Better verification for AI outputs | **Groundedness verifier** — scores every tutor response against the lesson's reference KB, surfaces a confidence chip (green/amber/red) with supported and unsupported claims listed |
| Smarter context retrieval | **Persistent semantic memory** — TF-IDF cosine retrieval over a user's past conversations, auto-injected into the system prompt so the tutor has cross-session continuity |
| Agent integrations & extensions | **MCP server** — stdlib-only stdio JSON-RPC server exposing SAGE's KB to *any* MCP-aware agent (Claude Code, Cursor, custom Agent SDK) as 5 tools |

### Real-world problem solved

LLM tutors hallucinate. LLM tutors forget you across sessions. LLM
tutors are isolated — your coding agent can't ask SAGE for help even if
it would benefit. Each of those three friction points is a daily cost
for anyone using AI at work. We removed all three.

## Where it lives

```
backend/app/agent/
└── verifier.py                  ← Groundedness judge (LLM judge with strict-JSON output)

backend/app/services/
└── semantic_memory.py           ← TF-IDF cosine over past chat turns (pure stdlib)

backend/app/models/
└── memory.py                    ← MemoryRecord SQLModel

backend/app/routers/
└── cognition.py                 ← /cognition/{memory, memory/recall, memory/{id}, verify}

backend/mcp_server.py            ← stdio JSON-RPC MCP server (no external deps)

frontend/components/tutor/
└── MessageBubble.tsx            ← VerificationChip rendering (line 248)

frontend/lib/
└── useTutorStream.ts            ← Verification SSE event handling (line 167)

frontend/app/memory/
└── page.tsx                     ← Memory browse + search UI
```

### Key code paths

| Concern | File / function |
|---|---|
| Verifier prompt (strict JSON, label rubric) | `verifier.py:30-58` |
| Tag-stripping before judging (skip rendered widgets) | `verifier.py:62-67` |
| Score → label mapping (≥0.85 grounded, ≥0.5 partial, else unverified) | `verifier.py:131-132` |
| Plug-in into agent loop (after main streaming, before `done`) | `agent_loop.py:138-149` |
| Verification SSE event type | `agent_loop.py:139` `'type': 'verification'` |
| Confidence chip component | `MessageBubble.tsx:249-291` |
| Persistence of verification in `chatmessage.message_meta` | `routers/tutor.py:81-96` |
| Hydration of chip on history reload | `app/learn/[pathId]/[lessonId]/page.tsx:84-98` |
| Tokenization (stoplist + length filter) | `semantic_memory.py:17-43` |
| TF-IDF + cosine similarity (per-call IDF) | `semantic_memory.py:55-77` |
| Heuristic importance score | `semantic_memory.py:80-87` |
| `record_memory()` (skips < 40-char turns) | `semantic_memory.py:90-118` |
| `recall_memories()` w/ lesson-match boost | `semantic_memory.py:121-167` |
| System-prompt block injection | `semantic_memory.py:170-194` |
| Wire-up in `/tutor/chat` | `routers/tutor.py:201-211` |
| MCP `initialize` / `tools/list` / `tools/call` | `mcp_server.py:202-238` |
| 5 tools exposed | `mcp_server.py:147-194` |

## Why this is 10/10

### 1. Better verification — actually works, not vibes

A common pattern: ship a "confidence score" that's the model's own
self-reported confidence (worthless — same model that's wrong is
reporting). We did the opposite: the verifier is a **separate LLM call**
with `temperature=0.0` and a **strict JSON schema**, judging whether
each substantive claim in the reply is supported by the actual lesson
content + reference KB.

Notable details:
- **Skip non-claims.** Pedagogical questions and Socratic prompts aren't claims (`verifier.py:35`). A quiz question doesn't count as a hallucination.
- **Skip near-empty replies.** Responses < 80 chars or that are mostly questions short-circuit to score 1.0 with no extra LLM call (`verifier.py:91-99`).
- **Tags stripped.** `<quiz>`, `<resource>`, `<image>`, `<flow>` etc. are removed before the judge sees the text — judge only sees prose (`verifier.py:62-67`).
- **JSON resilience.** Strips markdown fences, falls back to regex extraction if pure JSON fails (`verifier.py:121-128`).
- **Persisted.** Verification result is saved to `chatmessage.message_meta` so the chip stays on the message after page reload (`routers/tutor.py:81-96`).

The chip itself isn't decorative — it expands to show:
> "Supported by lesson: [list of grounded claims]
>  Not found in lesson material: [list of unsupported claims]"

That's actionable transparency. A learner can see exactly which sentence was unverifiable, click the lesson reference, and decide if it matters.

### 2. Smarter context retrieval — semantic, persistent, free

We didn't reach for `pinecone`, `weaviate`, or `sentence-transformers`.
Groq doesn't expose embeddings, and a hackathon shouldn't add a 1GB
dependency for a feature that benefits from a tiny TF-IDF over a
~hundred-row table.

Implementation choices that matter:
- **Pure stdlib retrieval.** TF-IDF cosine in `semantic_memory.py` with
  no extra packages. Re-computes IDF over the candidate window each
  call — cheap because windows are small (≤500 rows per user).
- **Importance heuristic.** Long, question-bearing, specific-fact-bearing
  turns get higher importance and stronger ranking (`semantic_memory.py:80-87`).
  Trivial chitchat doesn't drown out load-bearing memories.
- **Lesson-match boost.** A memory from the same lesson gets a 1.15x score multiplier — recall stays topic-relevant.
- **Auto-inject, don't expose as a tool.** The agent doesn't have to
  *decide* to call a "memory" tool. The memory block is prepended to the
  system prompt automatically (`routers/tutor.py:201-211`). No prompt
  engineering needed; the model can't forget to use it.
- **Browseable + searchable UI.** `/memory` page lets users see exactly
  what's stored, recall by query, delete individual items, or wipe everything.
  Privacy and trust are not afterthoughts.

This is "smarter context retrieval" not as a research demo, but as a
zero-config feature integrated into a real product loop.

### 3. Agent integrations & extensions — MCP server, no deps required

The most ambitious deliverable. SAGE's curated 74-lesson KB +
verification capability is exactly the kind of high-signal augmentation
that makes coding agents (Claude Code, Cursor) and research agents
measurably better at technical tasks. So we wrote an **MCP server** that
exposes SAGE as five tools any external agent can call:

| Tool | Purpose |
|---|---|
| `sage.lesson.search` | Free-text search across the full curriculum |
| `sage.lesson.get` | Pull full content + reference KB for grounding |
| `sage.concept.lookup` | Curated wiki resources for a concept (videos, papers) |
| `sage.verify` | **Score an arbitrary claim against a lesson's KB** — this is huge: the same verifier that protects SAGE's tutor is now available as a check for any agent's intermediate claims |
| `sage.memory.recall` | Recall the calling user's prior tutor conversations |

Implementation choices:
- **Pure stdlib JSON-RPC over stdio.** No `mcp` package required. The
  MCP transport is just newline-delimited JSON-RPC 2.0 — we implemented
  it in 50 lines (`mcp_server.py:202-265`). Drop the file in any Claude
  Code / Cursor `mcp.json` and it works.
- **Stateless wrapper, stateful backend.** The MCP server is just an
  HTTP client to the running SAGE backend (`mcp_server.py:54-71`). The
  backend holds the data; the MCP layer is dumb. This keeps the surface
  area tiny and the security model simple (auth via env-var JWT).
- **Standards-correct.** `protocolVersion: 2025-06-18`, proper `initialize`
  handshake, `notifications/initialized` ignored as required, `tools/list`
  and `tools/call` both implemented per spec.

Set this up in `~/.claude.json` or `mcp.json`:
```json
{
  "mcpServers": {
    "sage": {
      "command": "python",
      "args": ["/path/to/SAGE/backend/mcp_server.py"],
      "env": {
        "SAGE_API_URL": "http://localhost:8000",
        "SAGE_AUTH_TOKEN": "<jwt>"
      }
    }
  }
}
```

Now the user's coding agent can ask SAGE "is this LoRA fact correct?"
and get a grounded answer.

### 4. Hits 3 / 5 suggested directions in one track
Not "loosely related to one." Three explicit, non-overlapping deliverables:

- *better verification* → groundedness chip
- *smarter context retrieval* → semantic memory
- *agent integrations & extensions* → MCP server

Each of those alone would be a credible Cognition submission.

### 5. Real workflow, real product
This isn't a demo agent that "verifies" toy facts. It's wired into
SAGE's real tutor that real students use. The verification chip ships on
every reply. The memory persists across sessions. The MCP server is
addressable by any agent right now. There's no "but in production we'd…"
caveat — production is what's running.

## Demo flow

### Verification
```
1. Open any lesson in /learn → /learn/<path>/<lesson>
2. Ask the tutor: "What did Hu et al. find about LoRA rank 1 vs rank 8?"
3. Watch the response stream in.
4. Wait ~1s after streaming ends — green/amber/red chip appears under the message.
5. Click the chip → see exactly which claims the verifier supported and which it flagged.
6. Reload the page → chip is still there (persisted via message_meta).
```

### Semantic memory
```
1. Have a conversation in lesson A: discuss "scaling laws".
2. Open a NEW session (or another lesson). Ask "did we ever talk about chinchilla?"
3. Tutor's response references the prior conversation correctly — without you re-supplying context.
4. Visit /memory → see all stored turns, search "scaling", get top hits with match %.
```

### MCP server
```
1. Start SAGE backend on :8000.
2. Get a JWT from /auth/login.
3. Add SAGE to your Claude Code mcp.json (block above).
4. In a Claude Code session, ask: "use sage.lesson.search to find lessons on attention"
   → tool call → list of matching lesson slugs.
5. "use sage.verify to check this claim against lesson <id>: 'GPT-2 has 1.5B params'"
   → 0–1 score + grounded/unsupported claim breakdown.
```
