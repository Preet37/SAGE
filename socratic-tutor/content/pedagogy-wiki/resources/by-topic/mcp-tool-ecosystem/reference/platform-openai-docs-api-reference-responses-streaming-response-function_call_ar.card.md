# Card: Streaming tool args — `response.function_call_arguments`
**Source:** https://platform.openai.com/docs/api-reference/responses-streaming/response/function_call_arguments  
**Role:** reference_doc | **Need:** WORKING_EXAMPLE  
**Anchor:** Exact streaming field name(s) and payload shape used to reconstruct tool/function call arguments

## Key Content
- **Endpoint:** `POST /v1/responses` creates a model response; supports **streaming** via Server-Sent Events (SSE) when `stream: true`.
- **Streaming control (request):**
  - `stream: boolean` — if `true`, response data is streamed as generated (SSE).
  - `stream_options: { include_obfuscation }` — only set when `stream: true`.
- **Tool/function calling configuration (request):**
  - `tools: [...]` — list of tools the model may call (built-in tools, MCP tools, or **function calls/custom tools** with typed args).
  - `tool_choice` — controls how the model selects tools (e.g., `"auto"`).
  - `parallel_tool_calls: boolean` — whether tool calls may run in parallel.
  - `max_tool_calls: number` — maximum total built-in tool calls processed in a response (across all built-in tools).
- **Include extra tool-related outputs (request `include: [...]`):**
  - `web_search_call.action.sources`
  - `code_interpreter_call.outputs`
  - `computer_call_output.output.image_url`
  - `file_search_call.results`
  - `message.input_image.image_url`
  - `message.output_text.logprobs`
  - `reasoning.encrypted_content`
- **Non-streamed response shape example (for orientation):**
  - Top-level `Response` includes `id`, `object:"response"`, `status`, `output:[...]`, `tools:[]`, `tool_choice`, `parallel_tool_calls`, `usage`, etc.
  - Assistant text appears under `output[].type:"message" → content[].type:"output_text" → text`.

## When to surface
Use when a student asks how to **stream** Responses API outputs and how to configure/collect **tool/function calling** data—especially reconstructing tool arguments from streaming events like `response.function_call_arguments`.