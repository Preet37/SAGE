# Card: Structured Outputs (JSON Schema) — OpenAI Responses API
**Source:** https://platform.openai.com/docs/guides/structured-outputs/  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Exact request/response patterns + guarantees/limits for Structured Outputs (`client.responses.parse(...)`, schema subset, refusals, streaming, supported models)

## Key Content
- **Guarantee (Structured Outputs):** Model output **always adheres to supplied JSON Schema** (type-safety; no missing required keys; no invalid enum values). Distinct from JSON mode which guarantees **valid JSON only**, not schema adherence.
- **Enable Structured Outputs (Responses API):**
  - SDK pattern (Python/Pydantic):  
    `response = client.responses.parse(model=..., input=[...], text_format=MyPydanticModel)` → parsed object at `response.output_parsed`.
  - REST/format equivalent: `text: { format: { type: "json_schema", strict: true, schema: ... } }`
- **Supported models (json_schema):** `gpt-4o-mini`, `gpt-4o-mini-2024-07-18`, `gpt-4o-2024-08-06` **and later**. Older models use **JSON mode**.
- **JSON mode enable:** `text: { format: { type: "json_object" } }`
  - Must explicitly instruct to output JSON; API errors if **“JSON”** not present in context. Risk: endless whitespace stream if not instructed.
- **Refusals:** If safety refusal occurs, response includes **`refusal`** content (programmatically detectable) rather than matching schema.
- **Streaming:** Use `client.responses.stream(..., text_format=Schema)`; handle events like `response.output_text.delta`, `response.refusal.delta`, `response.completed`. SDK recommended for parsing.
- **Schema subset + hard limits:**
  - Types: string, number, boolean, integer, object, array, enum, anyOf.
  - Root schema **must be object** (not anyOf). **All fields required**; emulate optional via union with `null` (e.g., `"type": ["string","null"]`).
  - Objects must set **`additionalProperties: false`**.
  - Limits: **≤5000** total object properties; **≤10** nesting levels; total schema string length **≤120,000** chars; **≤1000** enum values overall; per enum property string total **≤15,000** chars when >250 values.
  - Key ordering: output keys follow schema order.

## When to surface
Use when students ask how to force reliable JSON/schema outputs, choose between Structured Outputs vs JSON mode/function calling, handle refusals/streaming, or debug schema errors/limits.