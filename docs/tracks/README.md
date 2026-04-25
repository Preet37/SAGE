# SAGE × Hackathon Tracks — Judging Index

SAGE is a Socratic AI tutor for technical courses (FastAPI + Next.js + Groq
llama-3.3-70b). For this hackathon we shipped five track-specific surfaces,
each behind a feature flag in `backend/settings.yaml` so the core tutor
keeps working untouched when external credentials are missing.

This folder contains a detailed judging pitch per track — **what** we
shipped, **where** it lives in the codebase, and **why** it scores 10/10
against the track's stated criteria.

| # | Track | Pitch | Surface in app |
|---|-------|-------|----------------|
| 1 | [Fetch.ai — Agentverse](01-fetchai.md) | SAGE Tutor as a Chat-Protocol uAgent on Agentverse, with multi-agent quiz delegation + Payment Protocol stub | `python -m app.agents.sage_uagent` + `/fetchai/info` |
| 2 | [Cognition — Augment the Agent](02-cognition.md) | Verification chip on every reply + cross-session semantic memory + MCP server exposing SAGE's KB to any agent | confidence chip on tutor messages, `/memory`, `mcp_server.py` |
| 3 | [ZETIC — On-device AI](03-zetic.md) | `/pocket` — full tutor running on the user's GPU via WebGPU + WebLLM; Melange recipe for the mobile (CPU/GPU/NPU) path | `/pocket` page + `docs/MELANGE-DEPLOYMENT.md` |
| 4 | [Cloudinary — React AI Starter Kit](04-cloudinary.md) | Sketch Studio: signed direct uploads + chained AI transforms + sketch-to-concept LLM explainer integrated into a Socratic learning loop | `/sketch` page |
| 5 | [Arista Networks — Connect the Dots](05-arista.md) | Live peer presence (REST + WebSocket pub/sub) + a unified resource router that aggregates arXiv + GitHub + YouTube and reranks locally | `/network` page |

## Cross-cutting design choices

- **Feature flags everywhere** — `features.{verification, semantic_memory, mcp_server, peer_network, resource_router, cloudinary, fetchai_agent, on_device}` in `backend/settings.yaml`. Judges can disable any track and the rest still works.
- **Graceful degradation** — every track surface checks for missing credentials and returns a clear, recoverable error instead of crashing the app (e.g., `/sketch` shows "Cloudinary not configured" rather than 500).
- **Reusing the existing tutor loop** — every track ties back into the *same* Socratic tutor (`backend/app/agent/agent_loop.py`). The Fetch.ai uAgent, the Sketch Explainer, and the on-device Pocket Tutor all share one pedagogical brain.
- **Zero changes to existing routes** — all five tracks added new routers (`/cognition`, `/network`, `/media`, `/fetchai`) and new frontend pages. The `/tutor`, `/learn`, `/quiz`, `/explore` flows are unmodified except for additive metadata (verification scores).
