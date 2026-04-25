# Card: Anthropic Messages SSE Streaming Event Semantics
**Source:** https://docs.anthropic.com/en/api/messages-streaming?debug_url=1&debug=1&debug=true  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** SSE streaming message event structure, incremental delivery, tool/thinking deltas, and recovery patterns

## Key Content
- **Enable streaming:** set `"stream": true` on a Messages create request; responses arrive via **Server-Sent Events (SSE)**.
- **Event flow (canonical order):**  
  1) `message_start` → contains a **Message** object with empty `content: []`  
  2) For each content block `i` in final `message.content[i]`:  
     `content_block_start(index=i)` → 1+ `content_block_delta(index=i)` → `content_block_stop(index=i)`  
  3) 1+ `message_delta` (top-level Message changes)  
  4) `message_stop` (final)
- **Usage accounting:** token counts in `message_delta.usage` are **cumulative** (e.g., `{"output_tokens": 15}`).
- **Ping events:** arbitrary number of `ping` events may appear anywhere in the stream.
- **Error events in-stream:** SSE `event: error` with JSON like  
  `{"type":"error","error":{"type":"overloaded_error","message":"Overloaded"}}` (maps to HTTP **529** in non-streaming).
- **Forward compatibility:** new event types may be added; clients should **ignore/handle unknown event types** gracefully.
- **Delta types (content_block_delta.delta.type):**
  - `text_delta`: incremental text, e.g. `"text":"Hello"`.
  - `input_json_delta`: for `tool_use` blocks; provides **partial JSON string** chunks in `partial_json`. Accumulate chunks; parse to an object at `content_block_stop`. (Current models emit **one complete key/value at a time**, so gaps between chunks can occur.)
  - `thinking_delta` + `signature_delta` (extended thinking): thinking streams as deltas; a **signature_delta arrives just before** `content_block_stop`. If `thinking.display: "omitted"`, no thinking deltas—only signature then stop.
- **SDK accumulation pattern:** stream events but return final Message via `.get_final_message()` (Python) / `.finalMessage()` (TS); Go uses `message.Accumulate(event)`; Java `MessageAccumulator.create().accumulate(event)`; Ruby `.accumulated_message`.
- **Recovery:**  
  - Claude **4.5 and earlier**: resume by sending partial assistant content and continue.  
  - Claude **4.6**: add a **user** message: “Your previous response was interrupted and ended with [previous_response]. Continue…”

## When to surface
Use when students ask how to implement/port **streaming LLM responses**, handle **tool-call parameter streaming**, manage **SSE errors/pings**, or design **reliable resume/retry** logic in production agents.