# Card: Responses API SSE Streaming Events (event types + payload fields)
**Source:** https://platform.openai.com/docs/api-reference/responses-streaming  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Exact streaming (SSE/WebSocket) event names + object fields for incremental output, tool-call deltas, and lifecycle/error events in the Responses API.

## Key Content
- **Streaming model:** server emits a sequence of **ResponseStreamEvent** objects (also called **ResponsesServerEvent** for WebSocket). Each event includes:
  - `type` (event name discriminator)
  - often `sequence_number`
  - often `output_index`, `item_id`, and sometimes `content_index` for locating the delta within the response.
- **Lifecycle/status events (ResponseStatus):** `queued`, `in_progress`, `completed`, `failed`, `cancelled`, `incomplete`.
  - `response.created`: **ResponseCreatedEvent** `{ type, sequence_number, response }`
  - `response.queued`: **ResponseQueuedEvent** `{ type, sequence_number, response }`
  - `response.in_progress`: **ResponseInProgressEvent** `{ type, sequence_number, response }`
  - `response.completed`: **ResponseCompletedEvent** `{ type, sequence_number, response }`
  - `response.failed`: **ResponseFailedEvent** `{ type, sequence_number, response }`
  - `response.incomplete`: **ResponseIncompleteEvent** `{ type, sequence_number, response }`
  - `response.error`: **ResponseErrorEvent** `{ type, code, message, param, … }`
- **Incremental text output:**
  - `response.output_text.delta`: **ResponseTextDeltaEvent** `{ type, sequence_number, output_index, item_id, content_index, delta }`
  - `response.output_text.done`: **ResponseTextDoneEvent** `{ type, sequence_number, output_index, item_id, content_index, logprobs, … }`
  - Content-part boundaries: **ResponseContentPartAddedEvent**, **ResponseContentPartDoneEvent** (include `output_index`, `item_id`, `content_index`, …).
  - Output-item boundaries: **ResponseOutputItemAddedEvent**, **ResponseOutputItemDoneEvent** `{ type, sequence_number, output_index, item }`.
- **Tool-call streaming (arguments/code/input deltas + done):**
  - Function calls: **ResponseFunctionCallArgumentsDeltaEvent** `{ delta, item_id, output_index, … }`; **…DoneEvent** `{ arguments, name, item_id, output_index, … }`
  - Custom tool input: **ResponseCustomToolCallInputDeltaEvent** / **…DoneEvent** (`delta` → final `input`)
  - MCP tool args: **ResponseMcpCallArgumentsDeltaEvent** / **…DoneEvent** (`delta` → final `arguments`)
  - Code interpreter code: **ResponseCodeInterpreterCallCodeDeltaEvent** / **…DoneEvent** (`delta` → final `code`) plus state events: **…InProgress**, **…Interpreting**, **…Completed**
  - Search tools: web/file search state events **…InProgress**, **…Searching**, **…Completed**
  - Image generation: **…InProgress**, **…Generating**, **…PartialImage** (`partial_image_b64`), **…Completed**
- **Audio streaming:** **ResponseAudioDeltaEvent** (`delta`), **ResponseAudioDoneEvent**; transcript: **ResponseAudioTranscriptDeltaEvent** (`delta`), **…DoneEvent**.
- **Refusals & reasoning summaries:** refusal delta/done (**ResponseRefusalDeltaEvent**, **ResponseRefusalDoneEvent**); reasoning summary part/text delta/done events.
- **Include extra data via `include[]` (ResponseIncludable):**
  - `web_search_call.action.sources`, `web_search_call.results`, `file_search_call.results`,
  - `code_interpreter_call.outputs`, `computer_call_output.output.image_url`,
  - `message.input_image.image_url`, `message.output_text.logprobs`,
  - `reasoning.encrypted_content`.
- **Text output formatting defaults:** `ResponseTextConfig.format` default is `{ "type": "text" }`. Structured Outputs via `{ "type": "json_schema" }` (preferred over `{ "type": "json_object" }` for newer models).

## When to surface
Use when students ask how to implement **streaming UI**, **reconstruct final text from deltas**, **track tool-call arguments/code incrementally**, or **handle lifecycle/error events** for production-grade Responses API clients.