# Card: Streaming API responses (SSE) — Responses vs Chat Completions
**Source:** https://platform.openai.com/docs/api-reference/streaming  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Central index of streaming behavior across endpoints (SSE framing, event types, lifecycle patterns, and robust client iteration).

## Key Content
- **Default behavior:** API returns the model’s *entire* output in one HTTP response; **streaming** lets clients process output incrementally while generation continues.
- **Enable streaming (Responses API):** set **`stream: true`** (JS) / **`stream=True`** (Python) in `client.responses.create(...)`, then iterate events (`for await ...` / `for event in stream`).
- **Transport:** HTTP streaming uses **Server-Sent Events (SSE)** with **semantic, typed events** (type-safe schemas).  
  - Persistent alternative: **WebSocket mode** (incremental inputs via **`previous_response_id`**) is referenced separately.
- **Common lifecycle events (Responses streaming):**
  - `response.created`
  - `response.output_text.delta`
  - `response.completed`
  - `error`
- **Event typing (examples from union list):** `ResponseCreatedEvent`, `ResponseInProgressEvent`, `ResponseCompletedEvent`, `ResponseOutputTextDelta`, `ResponseFunctionCallArgumentsDelta/Done`, tool-call progress events (file search, code interpreter), plus `Error`.
- **Chat Completions streaming:** set **`stream: true`** / **`stream=True`** on `chat.completions.create(...)`. Stream returns **data-only SSE chunks**.
  - Key parsing rule: streamed chunks use **`choices[0].delta`** (not `message`).  
    - `delta` may contain a **role token**, **content token**, or **nothing** (example shows `{}` at end).
  - To print only text: write `chunk.choices[0]?.delta?.content || ""` (JS) or check `delta.content is not None` (Python).
- **Design rationale:** OpenAI recommends **Responses API for streaming** because it’s “designed with streaming in mind” and uses **semantic events**.
- **Moderation risk:** streaming partial outputs makes moderation harder; may affect approved usage.

## When to surface
Use when students ask how to implement streaming output, interpret SSE event/chunk structure (`delta` vs `message`), handle lifecycle/error events, or compare Responses streaming with Chat Completions streaming.