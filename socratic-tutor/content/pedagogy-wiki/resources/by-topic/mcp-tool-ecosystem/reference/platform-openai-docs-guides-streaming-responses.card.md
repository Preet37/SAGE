# Card: Streaming Responses API — event sequence & assembly
**Source:** https://platform.openai.com/docs/guides/streaming-responses?api-mode=responses  
**Role:** reference_doc | **Need:** WORKING_EXAMPLE  
**Anchor:** Streaming event sequence + ordering/termination semantics (incl. tool/function-call argument deltas)

## Key Content
- **Enable streaming (Responses API):** set `stream: true` / `stream=True` in `client.responses.create(...)`. Iterate events (`for await ... of stream` in JS; `for event in stream` in Python).
- **Core lifecycle events (text):**  
  - `response.created` → start boundary (contains `response.id`)  
  - `response.output_text.delta` → incremental token in `delta`  
  - `response.completed` → end boundary (contains full `response`)  
  - `error` / `response.error` → failure handling
- **Event typing:** each streamed object has `type` (schema-defined). Useful types include:  
  `response.output_item.added/done`, `response.content_part.added/done`, `response.output_text.delta`, `response.text.done`, plus tool-related: `response.function_call_arguments.delta` and `response.function_call_arguments.done`.
- **Text assembly procedure (message-per-token):**
  1. On `response.output_item.added`, note `output_index` and `item.id` when `item.type === "message"`.
  2. On `response.content_part.added`, note `content_index` for the message item.
  3. Append each `response.output_text.delta.delta` **only when** `(event.item_id, output_index, content_index)` match the target message content part.
  4. Treat `response.content_part.done` / `response.output_item.done` as “part/item fully generated”; `response.completed` as final completion boundary.
- **Tool/function-call argument assembly (streaming):**
  - Accumulate `response.function_call_arguments.delta` chunks in order for a given call (correlate by the event’s identifiers); finalize when `response.function_call_arguments.done` arrives, then parse the completed arguments string (e.g., JSON) before executing the tool.
- **Design rationale:** Responses API streaming uses **semantic, type-safe events** (preferred over legacy chunked streaming) to let apps listen only to relevant events and reliably reconstruct outputs.

## When to surface
Use when students ask how to stream model output, reconstruct text from deltas, or correctly assemble streamed tool/function-call arguments and know when a stream is truly finished.