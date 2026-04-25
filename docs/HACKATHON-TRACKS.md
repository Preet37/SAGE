# SAGE — Hackathon Track Integrations

SAGE ships with five track-specific surfaces. Each one is opt-in via a
`features.*` flag in `backend/settings.yaml` and degrades gracefully when
external credentials are missing — so the core tutor keeps working even
if a track's API key isn't configured.

| Track | Surface | Backend | Frontend |
|---|---|---|---|
| **Fetch.ai** — Agentverse-discoverable tutor | `python -m app.agents.sage_uagent` + `/fetchai/*` | `app/agents/sage_uagent.py`, `app/agents/quiz_uagent.py`, `app/routers/fetchai_bridge.py` | bridge proxy in admin |
| **Cognition** — Verification + memory + MCP | `/cognition/*` + `mcp_server.py` | `app/agent/verifier.py`, `app/services/semantic_memory.py`, `app/routers/cognition.py`, `mcp_server.py` | confidence chip on every tutor message, `/memory` page |
| **ZETIC** — On-device Pocket Tutor | client-side WebGPU + WebLLM | (none — pure frontend) | `/pocket` page, `lib/onDeviceLLM.ts`; `docs/MELANGE-DEPLOYMENT.md` for the mobile path |
| **Cloudinary** — Sketch Studio + media | `/media/*` | `app/routers/media.py`, `app/models/media.py` | `/sketch` page, `lib/cloudinary.ts` |
| **Arista** — Connect the Dots | `/network/*` (REST + WebSocket) | `app/routers/network.py`, `app/models/network.py` | `/network` page, `lib/usePresence.ts` |

## Track 1 — Fetch.ai

The SAGE tutor is exposed as a uAgent that implements the **Chat Protocol**
(mandatory) and a **Payment Protocol** stub (optional). It also delegates
quiz requests to a sibling `quiz_uagent`, demonstrating multi-agent
orchestration.

```bash
# 1. Set a stable seed in .env so the agent address persists.
export FETCHAI_AGENT_SEED="<24+ chars, anything stable>"

# 2. Start both agents (separate terminals).
cd backend
python -m app.agents.sage_uagent
python -m app.agents.quiz_uagent  # prints address; copy into the tutor's env

# 3. Wire the tutor to delegate to the quiz agent.
export SAGE_QUIZ_AGENT_ADDRESS=agent1q...   # from the quiz agent's startup log

# 4. Register on Agentverse (manual or programmatic).
export AGENTVERSE_API_KEY=<your key>
python scripts/register_uagents.py
```

The web UI's `/fetchai/info` endpoint surfaces the registration link, agent
address, and payment SKUs.

## Track 2 — Cognition

Three deliverables under one track:

1. **Response verification** — every tutor reply is scored against the
   lesson's reference KB by a fast judge model. The frontend renders a
   green / amber / red confidence chip with the supported and unsupported
   claims spelled out.

2. **Semantic memory** — significant turns are persisted as TF-IDF token
   bags per user. The next time they ask something related, the top-3
   relevant past memories are injected into the system prompt so the tutor
   has continuity across sessions. Browsable + searchable at `/memory`.

3. **MCP server** — `backend/mcp_server.py` is a stdlib-only JSON-RPC stdio
   server that exposes SAGE's KB to any external agent (Claude Code,
   Cursor, custom Agent SDK code). Tools: `sage.lesson.search`,
   `sage.lesson.get`, `sage.concept.lookup`, `sage.verify`,
   `sage.memory.recall`. Set up in `mcp.json`:

   ```json
   {
     "mcpServers": {
       "sage": {
         "command": "python",
         "args": ["/abs/path/to/SAGE/backend/mcp_server.py"],
         "env": {
           "SAGE_API_URL": "http://localhost:8000",
           "SAGE_AUTH_TOKEN": "<jwt>"
         }
       }
     }
   }
   ```

## Track 3 — ZETIC

`/pocket` runs Llama-3.2-1B / 3B or Phi-3.5-mini **entirely on the
student's device** via WebGPU + WebLLM. Zero tokens leave the browser. The
UI labels what's local and what would hit the cloud, and exposes live
tokens/sec metrics so judges can verify it's really running locally.

For the mobile (CPU/GPU/NPU) path via Zetic Melange, see
`docs/MELANGE-DEPLOYMENT.md` — that's the recipe to take SAGE's distilled
tutor weights → ONNX → Melange bundle → iOS/Android.

```bash
cd frontend
npm install        # picks up @mlc-ai/web-llm
npm run dev
# open http://localhost:3000/pocket
```

## Track 4 — Cloudinary

The **Sketch Studio** at `/sketch` lets students upload hand-drawn diagrams,
equations, or paper screenshots. Cloudinary AI cleans them up
(`e_background_removal`, `c_thumb,g_auto`, `e_improve:outdoor`) and the
tutor explains what they show, returning detected concepts and a suggested
follow-up question for the main tutor chat.

```bash
# Cloudinary credentials in .env (see .env.example).
# Create an unsigned upload preset named 'sage_unsigned' in your Cloudinary
# console (or change the name in settings.yaml -> cloudinary.upload_preset).
```

Backend signs every upload server-side, browser uploads directly to
Cloudinary, and `/media/assets` records the result. `/media/transform`
builds chained transformation URLs on demand.

## Track 5 — Arista

`/network` shows live peer presence: who is studying which lesson right
now, who is "looking for a study buddy", and surfaces a one-click "nudge"
to ping someone. Built on a FastAPI WebSocket pub/sub (`/network/ws`)
with REST heartbeat fallback.

The same page exposes the **resource router** that pulls related papers
(arXiv), repos (GitHub), and videos (YouTube — optional, requires API
key) for any query, reranks them locally against your focus terms, and
caches results for 12h to stay polite. One click to one unified feed
instead of three tabs.
