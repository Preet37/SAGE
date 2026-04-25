# Card: Structured Outputs (JSON Schema enforcement)
**Source:** https://platform.openai.com/docs/guides/structured-outputs?api-mode=chat  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** JSON schema-based structured output constraints + enforcement behavior via `response_format` / `text.format`

## Key Content
- **What it guarantees:** Structured Outputs ensures the model output **adheres to your supplied JSON Schema** (not just valid JSON). Prevents missing required keys and invalid enum values.
- **How to enable (Responses API):** set `text: { format: { type: "json_schema", strict: true, schema: {...} } }` or use SDK helpers (`responses.parse` with Pydantic / Zod).
- **When to use which:**
  - **Function calling**: when connecting model to tools/functions/data in your system.
  - **`response_format` / `text.format` schema**: when you want the assistant’s **user-facing response** structured for UI, tutoring steps, extraction, etc.
- **Structured Outputs vs JSON mode (table facts):**
  - Valid JSON: both **Yes**
  - Schema adherence: Structured Outputs **Yes**; JSON mode **No**
  - Structured Outputs compatible models: **gpt-4o-mini**, **gpt-4o-mini-2024-07-18**, **gpt-4o-2024-08-06** and later (JSON mode works on broader set incl. `gpt-3.5-turbo`, `gpt-4-*`, `gpt-4o-*`).
  - JSON mode enable: `text: { format: { type: "json_object" } }`
- **Refusals:** If the model refuses for safety, output may not match schema; API includes a **`refusal`** content item/field so refusals are programmatically detectable.
- **Schema rules/limits (enforced):**
  - Root schema **must be an object** (cannot be top-level `anyOf`).
  - **All fields must be required**; emulate optional via union with `null` (e.g., `"type": ["string","null"]`).
  - Objects must set **`additionalProperties: false`**.
  - Limits: **≤5000** total object properties, **≤10** nesting levels; total string size **≤120,000** chars; **≤1000** enum values overall.
  - Key ordering: output keys follow schema key order.
- **Supported JSON Schema subset:** types `string, number, boolean, integer, object, array, enum, anyOf`; supports `$defs` and recursion (`$ref: "#"`, etc.). Unsupported keywords include `allOf`, `not`, `if/then/else`, etc.

## When to surface
Use when students ask how an agent/tutor can **output plans, steps, or UI-ready fields reliably**, how to **enforce required subgoals**, or how to **detect refusals/validation constraints** in structured agent planning outputs.