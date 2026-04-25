# SAGE Agent Swarm Contract

## Topology
```
                ┌──────────────┐
                │ Orchestrator │
                └──────┬───────┘
       ┌──────────┬────┼────┬─────────┬──────────┐
       ▼          ▼    ▼    ▼         ▼          ▼
   Pedagogy → Content → ConceptMap → Assessment ∥ PeerMatch ∥ Progress
                  │
                  └─→ verify() (deterministic, app/core/verification.py)
```

Sequential phases: **Pedagogy → Content → verify → ConceptMap**.
Parallel fan-out: **Assessment ∥ PeerMatch ∥ Progress** via `asyncio.gather`.

## Inter-agent communication
Agents are **stateless functions over a shared `AgentContext`**. The
orchestrator is the only sequencer. Agents do not import each other.
Every read/write is recorded in `ctx.trace` as an `AgentMessage`
(`sender`, `recipient`, `intent`, `payload`).

### `AgentContext` fields written
| field | written by | shape |
|---|---|---|
| `plan` | pedagogy | `{strategy, depth, ask_one_question, weak_concepts}` |
| `answer` | content | `str` |
| `verification` | orchestrator (via `verify()`) | see `sse_payloads.md` |
| `concept_map_delta` | concept_map | `[{label, summary, mastery, parent_label}]` |
| `assessment` | assessment | `{question, concept, kind, skip}` |
| `peers` | peer_match | `[{peer_id, complements, score}]` |
| `progress_delta` | progress | `{bump, by_concept: {label: delta}}` |
| `trace` | all | `[AgentMessage]` |

## LLM provider chain
`app.agents.base.LLM.from_env()` resolves in order:
1. **Primary:** `ANTHROPIC_API_KEY` → Claude (`AnthropicProvider`)
2. **Fallback:** `ASI1_API_KEY` → `ASI1MiniProvider` (Fetch.ai ASI1-Mini)
3. **Offline:** `StubProvider` (deterministic, used in tests)

`LLM.complete()` automatically falls back to ASI1-Mini if the primary raises.

## Fetch.ai Agentverse deployment
Module: `app/agents/uagents_runner.py`
Models: `TutorRequest` / `TutorResponse` (uagents `Model`)
Protocol: `sage-tutor` v0.1.0
Run:
```bash
AGENT_SEED="..." ASI1_API_KEY="..." python -m app.agents.uagents_runner
```
Address is printed on startup. Publish manifest is enabled so the agent
appears in Agentverse search.

## Streaming
`Orchestrator.stream_turn(ctx)` yields `(event_name, payload)` tuples
already shaped to match the `/tutor/chat` SSE contract in
`.sage_memory/sse_payloads.md`. The router can wrap each tuple with
`{"event": name, "data": json.dumps(payload)}`.
