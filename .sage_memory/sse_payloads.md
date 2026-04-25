# SAGE `/tutor/chat` SSE Payload Contract

**Endpoint:** `GET /tutor/chat?session_id={int}&message={string}`
**Auth:** `Authorization: Bearer <jwt>` (EventSource: pass via query proxy or use `fetch` + ReadableStream)
**Content-Type:** `text/event-stream`

## Event sequence (per turn)
1. `agent_event` (orchestrator start)
2. `agent_event` (retriever retrieved)
3. `agent_event` (socratic generating)
4. `token` × N
5. `verification`
6. `done`

## Event payloads

### `agent_event`
```json
{ "agent": "orchestrator" | "retriever" | "socratic" | "verifier",
  "phase": "start" | "retrieved" | "generating" | "verifying",
  "session_id"?: number,
  "k"?: number,
  "scores"?: number[],
  "system_prompt_chars"?: number }
```

### `token`
```json
{ "agent": "socratic", "text": "string-with-trailing-space " }
```
Concatenate `text` values in arrival order to reconstruct the answer.

### `verification`
```json
{ "score": 0.0,           // float in [0,1], aggregate groundedness
  "grounded": true,
  "claims": [
    { "claim": "string",
      "score": 0.0,        // overlap fraction with best source
      "grounded": true,    // score >= threshold (0.4)
      "source_index": 0    // null if not grounded
    }
  ] }
```

### `done`
```json
{ "session_id": 1, "ok": true, "grounded": true }
```

## Frontend reference
```ts
const es = new EventSource(`/api/tutor/chat?session_id=${id}&message=${q}`);
es.addEventListener("agent_event", e => onAgent(JSON.parse(e.data)));
es.addEventListener("token",       e => appendToken(JSON.parse(e.data).text));
es.addEventListener("verification",e => showVerification(JSON.parse(e.data)));
es.addEventListener("done",        e => { es.close(); finalize(JSON.parse(e.data)); });
```

## Implementation pointers
- Generator: `backend/app/routers/tutor.py::chat`
- Retrieval: `app.core.retrieval.CosineRetriever` (cosine over hashing embedder)
- Verification: `app.core.verification.verify` (token-overlap, threshold 0.4)
- Prompt: `app.core.prompt_builder.build_system_prompt(a11y, mastery, sources, objective)`
