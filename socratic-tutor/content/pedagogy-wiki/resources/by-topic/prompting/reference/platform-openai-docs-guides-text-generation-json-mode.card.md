# Card: Structured Outputs & JSON Mode (OpenAI API)
**Source:** https://platform.openai.com/docs/guides/text-generation/json-mode  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Concrete SDK pattern `client.responses.parse(...)` / `client.chat.completions.parse(...)` with typed schemas + documented constraints/behavior of Structured Outputs vs JSON mode.

## Key Content
- **Structured Outputs (SO)**: guarantees **valid JSON + schema adherence** to supplied **JSON Schema** (`strict: true`), preventing missing required keys / invalid enums. Recommended over JSON mode when supported.
- **SDK parsing workflow (Python/Pydantic)**:
  - Chat Completions: `client.chat.completions.parse(..., response_format=MyModel)` → `completion.choices[0].message.parsed`
  - Responses API: `client.responses.parse(..., text_format=MyModel)` → `response.output_parsed`
- **When to use**:
  - **Function calling**: bridge model ↔ tools/functions/data.
  - **response_format / text.format**: structure the assistant’s *user-facing* response (e.g., tutoring UI sections).
- **Model support**:
  - SO via `response_format: {type:"json_schema", json_schema:{strict:true, schema:...}}` supported on **gpt-4o-mini**, **gpt-4o-mini-2024-07-18**, **gpt-4o-2024-08-06** and later snapshots.
  - **JSON mode**: `response_format: {type:"json_object"}` (Chat Completions) or `text.format: {type:"json_object"}` (Responses).
- **Refusals**: if safety refusal occurs, API includes a **refusal** field/content (programmatically detectable) rather than schema output.
- **Schema constraints (SO subset)**:
  - Root schema **must be an object** (not top-level `anyOf`).
  - **All fields must be required**; emulate optional via union with `null` (e.g., `"type": ["string","null"]`).
  - Objects must set **`additionalProperties: false`**.
  - Limits: **≤5000** total object properties, **≤10** nesting levels; total schema string length **≤120,000** chars; **≤1000** enum values overall.
  - Key ordering in output follows schema key order.
- **JSON mode gotcha**: must explicitly instruct output as **JSON**; API errors if “JSON” absent; otherwise model may emit endless whitespace.

## When to surface
Use when students ask how to force reliable JSON/typed outputs, choose between JSON mode vs schema-validated outputs, handle refusals, or implement `parse(...)` patterns and schema constraints/limits.