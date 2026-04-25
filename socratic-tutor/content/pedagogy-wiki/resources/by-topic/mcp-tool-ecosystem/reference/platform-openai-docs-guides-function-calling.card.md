# Card: Responses API Function/Tool Calling (fields + flow)
**Source:** https://platform.openai.com/docs/guides/function-calling?api-mode=responses  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Exact Responses API tool/function-calling request/response fields, tool_choice behavior, tool call objects/arguments, and returning tool results.

## Key Content
- **Tool-calling workflow (5 steps):** (1) `responses.create(..., tools=..., input=...)` → (2) model returns tool call(s) in `response.output` → (3) app executes tool(s) using provided args → (4) append tool results as `function_call_output` items → (5) call `responses.create` again with updated `input` to get final answer (or more calls).
- **Tool definition (function tool schema):**  
  `tools: [{ "type":"function", "name", "description", "parameters": JSONSchema, "strict": bool }]`
- **Function call item (in `response.output`):**  
  `{ "type":"function_call", "id":"fc_…", "call_id":"call_…", "name":"get_weather", "arguments":"{...JSON string...}" }`  
  `arguments` is **JSON-encoded string**; parse with `json.loads(...)`.
- **Returning tool results to model:** append to next request `input`:  
  `{ "type":"function_call_output", "call_id": <matching call_id>, "output": <string | array of image/file objects> }`
- **Multiple calls:** assume **0/1/many** tool calls per response; iterate `response.output` and handle each `function_call`.
- **Reasoning models requirement:** for GPT-5 / o4-mini, **pass back any reasoning items** from model responses along with tool outputs in the next `input`.
- **tool_choice options (defaults/controls):**
  - Default: `"auto"` (model may call 0/1/many tools)
  - `"required"` (must call ≥1 tool)
  - Force one tool: `{"type":"function","name":"get_weather"}`
  - Restrict without changing `tools`: `{"type":"allowed_tools","mode":"auto","tools":[{"type":"function","name":"get_weather"}, ...]}`
  - `"none"` imitates no tools.
- **Parallel calls:** set `parallel_tool_calls: false` to ensure **exactly 0 or 1** tool call per turn. Not available with built-in tools.
- **Strict mode (recommended):** `strict:true` enforces schema via structured outputs. Requirements: every object has `additionalProperties:false`; **all** `properties` fields listed in `required`; optional via union with `null` (e.g., `"type":["string","null"]`). In **Responses API**, schemas are normalized into strict by default unless `strict:false`.

## When to surface
Use when students ask how to define tools/functions, interpret `response.output` tool call objects, control tool calling (`tool_choice`, parallelism, strict), or correctly return tool outputs in the Responses API.