# Card: OpenAI API Function/Tool Calling (Schemas, tool_choice, outputs)
**Source:** https://platform.openai.com/docs/guides/function-calling  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Exact tool/function JSON schema, tool_choice behavior, and how tool call arguments are returned/parsed

## Key Content
- **Tool calling flow (5 steps):** (1) Request model with `tools` it can call → (2) receive `function_call`(s) → (3) execute app-side code using tool args → (4) send `function_call_output` with results (matched by `call_id`) → (5) receive final model response (or more tool calls).
- **Function tool schema (per tool):**  
  - Fields: `type:"function"`, `name`, `description`, `parameters` (JSON Schema), `strict` (enforce schema).  
  - Example requirements for strict schemas: `additionalProperties:false` on each object; **all** `properties` fields must be in `required`. Optional fields via union types like `"type":["string","null"]`.
- **How tool calls appear in Responses API:** `response.output` is an array; tool calls are items with `type:"function_call"` containing `call_id`, `name`, and **JSON-encoded string** `arguments` (parse with `json.loads(arguments)`).
- **Returning tool results:** append an item:  
  `{"type":"function_call_output","call_id": <call_id>, "output": <string|array-of-image/file-objects>}`. For no-return actions, output e.g. `"success"`.
- **Multiple calls:** assume zero/one/**multiple** tool calls per response; iterate through `response.output`.
- **Reasoning models note:** any reasoning items returned alongside tool calls must also be passed back with tool outputs.
- **`tool_choice` modes:**  
  - `"auto"` (default): zero/one/many calls  
  - `"required"`: one or more calls  
  - `{"type":"function","name":"get_weather"}`: force exactly one specific function  
  - `{"type":"allowed_tools","mode":"auto","tools":[...]}`
  - `"none"`: imitate passing no tools
- **Parallel calls control:** `parallel_tool_calls:false` ⇒ exactly 0 or 1 tool call. (Built-in tools: no parallel calling.)
- **Token/cost rationale:** tool definitions count as input tokens (injected into system message); keep initial tools small (soft suggestion: **<20**) or use tool search (only **gpt-5.4+**).

## When to surface
Use when students ask how an agent “acts” via tools: defining tool schemas, forcing/limiting tool usage (`tool_choice`, `parallel_tool_calls`), and correctly parsing/returning tool call arguments/results in the OpenAI Responses API.