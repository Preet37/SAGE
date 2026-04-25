# Card: Gemini Function/Tool Calling (Compositional + Parallel)
**Source:** https://ai.google.dev/gemini-api/docs/function-calling  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Gemini function/tool calling request/response schema + execution loop (functionDeclarations → model functionCall parts → app executes → return functionResponse with matching `id`), incl. modes and compositional/parallel calling.

## Key Content
- **Core workflow (4-step loop):**
  1) **Declare tools**: send `tools: [{ functionDeclarations: [ {name, description, parameters(OpenAPI-subset)} ] }]`.  
  2) **Model decides** (AUTO/VALIDATED) whether to emit **text** or a structured **`functionCall`** with `{id, name, args}`. *(Gemini 3 always returns a unique `id` for each functionCall.)*  
  3) **App executes** the named function using `args` (model never executes tools).  
  4) **Return result** in next turn as **`functionResponse`** including the **exact same `id`** so the API maps results to calls; model then produces final user-facing text.
- **Function declaration schema (OpenAPI subset):** `name` (no spaces/special chars), `description` (specific), `parameters: {type:"object", properties:{...}, required:[...]}`; use `enum` for fixed choices; strong typing reduces errors.
- **Parallel calling:** model may emit multiple `functionCall`s in one turn; results can be returned **in any order** because mapping uses `id`.
- **Compositional (sequential) calling:** model chains calls (e.g., `get_weather_forecast(location)` → `set_thermostat_temperature(temperature)`), repeating the loop until no more calls.
- **Function calling modes (`tool_config.function_calling_config.mode`):**
  - `AUTO`: model chooses text vs call (default when only function tools enabled).
  - `VALIDATED`: constrains to text or valid calls; better schema adherence (default when combining tools/structured output).
  - `ANY`: **always** call a function; optional `allowed_function_names`.
  - `NONE`: prohibit function calls.
- **Critical parsing note:** don’t assume `functionCall` is last in `parts`; iterate all parts (esp. when mixing built-in tools).
- **Best-practice defaults:** keep active tools ~**10–20**; use low temperature (e.g., **0**) for reliable calls; validate high-stakes actions with user.

## When to surface
Use when students ask how ReAct/tool-calling loops are represented in Gemini API JSON, how to execute/return tool results correctly (especially `id` mapping), or how to force/disable tool use (modes, parallel vs compositional).