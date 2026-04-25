# Card: Responses API Streaming Event Types (Server-Sent Events / WS)
**Source:** https://platform.openai.com/docs/api-reference/responses-streaming  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Enumerated Responses streaming event types + payload shapes (delta vs done, lifecycle/termination, tool-call streaming)

## Key Content
- **Response lifecycle status values (`ResponseStatus`):** `"queued"`, `"in_progress"`, `"completed"`, `"failed"`, `"cancelled"`, `"incomplete"`.
- **Top-level termination/lifecycle events (each includes `type`, `sequence_number`, and often `response`):**
  - `ResponseCreatedEvent` `{ response, sequence_number, type }`
  - `ResponseQueuedEvent` `{ response, sequence_number, type }`
  - `ResponseInProgressEvent` `{ response, sequence_number, type }`
  - `ResponseCompletedEvent` `{ response, sequence_number, type }`
  - `ResponseFailedEvent` `{ response, sequence_number, type }`
  - `ResponseIncompleteEvent` `{ response, sequence_number, type }`
  - `ResponseErrorEvent` `{ code, message, param, … }` (error during streaming)
- **Output structure events (robust client should handle item/content boundaries):**
  - `ResponseOutputItemAddedEvent` `{ item, output_index, sequence_number, type }`
  - `ResponseOutputItemDoneEvent` `{ item, output_index, sequence_number, type }`
  - `ResponseContentPartAddedEvent` / `ResponseContentPartDoneEvent` `{ content_index, item_id, output_index, … }`
- **Text streaming (delta → done):**
  - `ResponseTextDeltaEvent` `{ content_index, delta, item_id, output_index, … }`
  - `ResponseTextDoneEvent` `{ content_index, item_id, logprobs, … }`
- **Refusal streaming:** `ResponseRefusalDeltaEvent` / `ResponseRefusalDoneEvent` with `{ content_index, delta/refusal, item_id, output_index, … }`.
- **Audio streaming:** `ResponseAudioDeltaEvent` `{ delta, sequence_number, type }` and `ResponseAudioDoneEvent`; transcript equivalents `ResponseAudioTranscriptDeltaEvent` / `Done`.
- **Tool-call streaming patterns (all keyed by `item_id`, `output_index`, `sequence_number`):**
  - Function args: `ResponseFunctionCallArgumentsDeltaEvent` `{ delta, item_id, output_index, … }` → `…DoneEvent` `{ arguments, name, item_id, … }`
  - Code interpreter code: `…CallCodeDeltaEvent` → `…CallCodeDoneEvent` plus `…InProgress/Interpreting/Completed`
  - Web/file search: `…InProgress` → `…Searching` → `…Completed`
  - Image gen: `…InProgress/Generating` → `…PartialImage` → `…Completed`
  - MCP tool calls: args delta/done + in_progress/completed/failed; list-tools in_progress/completed/failed
- **Include-able extra fields (`ResponseIncludable`):** `"file_search_call.results"`, `"web_search_call.results"`, `"web_search_call.action.sources"`, `"code_interpreter_call.outputs"`, `"computer_call_output.output.image_url"`, `"message.input_image.image_url"`, `"message.output_text.logprobs"`, `"reasoning.encrypted_content"`.

## When to surface
Use when students ask how to implement a **robust streaming client** for the Responses API (handling deltas, item boundaries, tool-call progress, and completion/failure), or how Responses streaming differs from simpler “token stream” assumptions.