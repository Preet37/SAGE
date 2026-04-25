# Card: Structured outputs (JSON outputs + strict tool use)
**Source:** https://platform.claude.com/docs/en/build-with-claude/structured-outputs  
**Role:** reference_doc | **Need:** CONCEPT_EXPLAINER  
**Anchor:** Tool name + tool input schema validation guarantees; how Claude enforces/returns structured outputs

## Key Content
- **Two complementary features**
  - **JSON outputs** via `output_config.format`: constrains *Claude’s response text* to **valid JSON** matching a provided **JSON Schema**; returned in `response.content[0].text`.
  - **Strict tool use** via `tools[].strict: true`: guarantees **schema validation on tool names and tool inputs** (grammar-constrained sampling).
  - Can be used **independently or together** in one request.
- **Why (design rationale):** avoids malformed JSON / schema violations (missing required fields, wrong types). Guarantees schema-compliant outputs via **constrained decoding** → “no JSON.parse() errors,” type-safe required fields, fewer retries.
- **Procedure (JSON outputs quick start)**
  1. Define JSON Schema (`type`, `properties`, `required`, `additionalProperties: false`).
  2. Send request with `output_config.format: { type: "json_schema", schema: ... }`.
  3. Parse JSON from `response.content[0].text`.
- **Property ordering rule:** output object fields ordered as **required first (schema order)**, then **optional (schema order)**.
- **Failure modes (still possible):**
  - `stop_reason: "refusal"` → may not match schema (200 OK; billed).
  - `stop_reason: "max_tokens"` → truncated/incomplete JSON; retry with higher `max_tokens`.
- **Performance/caching defaults**
  - Grammar compilation adds **first-request latency**.
  - Compiled grammars cached **24 hours since last use**.
  - Cache invalidated if **schema structure** changes or **tool set** changes; changing only tool `name`/`description` does **not** invalidate.
- **Schema complexity limits (explicit)**
  - **20** strict tools/request.
  - **24** total optional parameters across all strict schemas.
  - **16** parameters using union types (`anyOf` or `type: [...]`).
  - Too complex → **400** “Schema is too complex for compilation”; compilation timeout **180s**.
- **Compatibility:** works with streaming, batch, token counting; **incompatible with citations** (400) and **message prefilling**.

## When to surface
Use when students ask how to guarantee valid JSON outputs, enforce tool input schemas (`strict: true`), handle refusals/max_tokens truncation, or debug schema complexity/caching/latency issues.