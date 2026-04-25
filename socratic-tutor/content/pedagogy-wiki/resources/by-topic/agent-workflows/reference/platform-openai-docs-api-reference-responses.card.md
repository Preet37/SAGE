# Card: Responses API — tool calls, streaming events, execution controls
**Source:** https://platform.openai.com/docs/api-reference/responses  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Exact request/response schema for tool calls, streaming events, and fields controlling execution (tool_choice, parallel tool calls where supported, truncation/limits) that determine what a supervisor can delegate and how results are returned

## Key Content
- **Core endpoints (Responses):**
  - Create: `POST /responses`
  - Get: `GET /responses/{response_id}`
  - Delete: `DELETE /responses/{response_id}`
  - Cancel: `POST /responses/{response_id}/cancel`
  - Compact: `POST /responses/compact`
  - List input items: `GET /responses/{response_id}/input_items`
  - Input token counts: `POST /responses/input_tokens`
- **Instruction hierarchy (input messages):** `EasyInputMessage {role, content, ...}` where **developer/system instructions override user**; `assistant` role is treated as prior model output.
- **Tool execution control (`tool_choice`):**
  - `ToolChoiceOptions`: `"none" | "auto" | "required"`
    - `none`: model **will not** call tools; generates a message.
    - `auto`: model may choose message vs tool call(s).
    - `required`: model **must** call ≥1 tool.
  - Forcing specific tools (objects): `ToolChoiceFunction {name}`, `ToolChoiceCustom {name}`, `ToolChoiceMcp {server_label, name}`, `ToolChoiceShell {type}`, `ToolChoiceApplyPatch {type}`, `ToolChoiceAllowed {mode, tools}` (constrain to a set).
- **Response lifecycle status (`ResponseStatus`):** `"queued" | "in_progress" | "completed" | "failed" | "cancelled" | "incomplete"`.
- **Streaming/event model:** server emits typed events including `ResponseCreatedEvent`, `ResponseInProgressEvent`, `ResponseCompletedEvent`, `ResponseFailedEvent`, `ResponseIncompleteEvent`, plus granular deltas/done events for text/audio/refusals and tool calls (e.g., `ResponseFunctionCallArgumentsDelta/Done`, `ResponseMcpCall...`, `ResponseWebSearchCall...`, `ResponseFileSearchCall...`, `ResponseCodeInterpreterCall...`).
- **Including extra tool/output data (`include[]`: `ResponseIncludable`):**
  - `web_search_call.action.sources`, `file_search_call.results`, `web_search_call.results`
  - `code_interpreter_call.outputs`
  - `computer_call_output.output.image_url`
  - `message.input_image.image_url`
  - `message.output_text.logprobs`
  - `reasoning.encrypted_content`
- **Output formatting:** `text.format` supports `{type:"text"}` (default), `{type:"json_schema"}` (Structured Outputs), `{type:"json_object"}` (older JSON mode; “not recommended for gpt-4o and newer”).

## When to surface
Use when students ask how a supervisor agent should force/allow tool (agent) calls, interpret streaming tool-call events, manage cancellation/status, or request extra included fields (sources, results, logprobs, encrypted reasoning) in multi-agent orchestration.