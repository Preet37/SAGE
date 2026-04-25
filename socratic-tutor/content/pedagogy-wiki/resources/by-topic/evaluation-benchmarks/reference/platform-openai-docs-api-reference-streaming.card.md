# Card: OpenAI API Streaming (Responses + Events)
**Source:** https://platform.openai.com/docs/api-reference/streaming  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Parameter-level reference for enabling streaming + event framing/lifecycle

## Key Content
- **Default behavior:** API returns the model’s **entire output in one HTTP response** (non-streaming). Streaming reduces perceived latency by sending partial output as it’s generated.
- **Enable streaming (Responses endpoint):** set **`stream: true`** (JS) / **`stream=True`** (Python) in `client.responses.create(...)`.  
  **Procedure:**  
  1) Call `responses.create(..., stream=true)`  
  2) Iterate events (`for await (const event of stream)` / `for event in stream`)  
  3) Route by `event.type` (SDK events are typed; `type` property identifies schema).
- **Streaming model:** Responses API streams **semantic, typed events** (type-safe). Example union includes:  
  `response.created`, `response.in_progress`, `response.failed`, `response.completed`,  
  `response.output_text.delta`, `response.text.done`, `error`, plus tool-related deltas (e.g., `response.function_call_arguments.delta/done`, file search and code interpreter progress events).
- **Common text-stream events to listen for:**  
  - `response.created` (once)  
  - `response.output_text.delta` (many; incremental text)  
  - `response.completed` (once; end-of-stream)  
  - `error`
- **Chat Completions streaming:** also supports `stream=True`, returning **data-only SSE chunks**; iterate chunks and read `chunk.choices[0].delta`.
- **Design rationale:** OpenAI recommends **Responses API for streaming** because it’s “designed with streaming in mind” and uses semantic, type-safe events.
- **Production constraint:** **Moderation risk**—streaming partial output is harder to moderate; partial completions may be difficult to evaluate.

## When to surface
Use when students ask how to **turn on streaming**, **parse streamed output**, **handle lifecycle/error events**, or compare **Responses streaming vs Chat Completions SSE** in production agents.