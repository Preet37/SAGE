# Card: Tool/Function Calling Schema & Control Knobs (OpenAI Responses API)
**Source:** https://platform.openai.com/docs/guides/function-calling?api-mode=chat  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Tool-calling request/response schema (tool definitions, tool_choice behavior, tool call arguments), plus planning-loop-relevant fields like `parallel_tool_calls`

## Key Content
- **Tool-calling workflow (5 steps):**  
  1) Request model with `tools` available → 2) Model returns tool call(s) → 3) App executes tool(s) → 4) App sends tool outputs back → 5) Model returns final answer or more tool calls.
- **Tool definition schema (function tools):**  
  `{"type":"function","name":..., "description":..., "parameters": JSONSchema, "strict": bool}`.  
  Example includes `additionalProperties:false` and `required:[...]`.
- **Tool call item (model → app):** response `output` array contains items with:  
  `type:"function_call"`, `call_id`, `name`, `arguments` (JSON-encoded string). Multiple calls may appear in one turn.
- **Tool output item (app → model):** append to next request input:  
  `{"type":"function_call_output","call_id": <from tool call>, "output": <string | array of image/file objects>}`.
- **Reasoning-model constraint:** for GPT-5 / o4-mini, **any reasoning items returned alongside tool calls must be passed back** with tool outputs in the next request.
- **`tool_choice` behaviors (defaults & forcing):**  
  - Default: `"auto"` (0, 1, or many tool calls)  
  - `"required"` (must call ≥1 tool)  
  - Force one tool: `{"type":"function","name":"get_weather"}`  
  - Restrict without changing `tools`: `{"type":"allowed_tools","mode":"auto","tools":[...]}`
  - `"none"` imitates passing no tools.
- **Parallelism control:** `parallel_tool_calls:false` ⇒ model can call **exactly 0 or 1** tool per turn. (Parallel calling not possible with built-in tools.)
- **Strict mode requirements (Structured Outputs):** if `strict:true`: every object must set `additionalProperties:false` and **all** `properties` must be in `required`; optional fields use union types like `["string","null"]`.

## When to surface
Use when students ask how an agent decides to call tools, how to structure tool schemas/messages, or how to control/sequence multi-step plans (force tools, restrict tools, disable parallel calls, enforce strict arguments).