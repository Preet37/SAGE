# Card: Schema-Constrained Decoding (Structured Outputs)
**Source:** https://openai.com/index/introducing-structured-outputs-in-the-api/  
**Role:** reference_doc | **Need:** DEPLOYMENT_CASE  
**Anchor:** Design rationale + mechanism for schema-constrained decoding vs JSON mode (guarantees/limits)

## Key Content
- **JSON mode vs Structured Outputs**
  - JSON mode: improves validity of JSON but **does not guarantee conformance to a specific schema**.
  - **Structured Outputs:** designed to ensure outputs **exactly match developer-supplied JSON Schemas**.
- **How to enable (2 paths)**
  1. **Function calling:** set `strict: true` inside the tool/function definition → outputs match the supplied tool schema.
  2. **response_format:** set `response_format: { type: "json_schema", json_schema: { strict: true, schema: ... } }` → outputs match schema (supported on `gpt-4o-2024-08-06`, `gpt-4o-mini-2024-07-18`).
- **Reliability / empirical results**
  - On complex JSON schema-following evals: `gpt-4o-2024-08-06` + Structured Outputs scores **100%**; `gpt-4-0613` scores **<40%**.
  - Model training alone reached **93%** on benchmark; deterministic constrained decoding used to reach **100%** reliability.
- **Mechanism: constrained decoding (dynamic token masking)**
  - Convert JSON Schema → **context-free grammar (CFG)**.
  - During sampling, after **every token**, compute valid next tokens from CFG and **mask** invalid tokens (probability → **0**).
  - First request with a new schema incurs preprocessing latency; artifacts are cached for reuse.
- **Why CFG (vs FSM/regex)**
  - CFGs express broader languages; better for **nested/recursive** schemas (e.g., `$ref: "#"`) where FSMs struggle.
- **Operational limits**
  - Can still fail schema if **refusal**, **`max_tokens`/stop** truncation, or **parallel tool calls** (set `parallel_tool_calls: false`).
  - Structured Outputs ensures structure, **not correctness of values** (e.g., math step may be wrong).
  - First-schema latency: typical **<10s**, complex up to **~1 min**.
  - Refusals surfaced via `message.refusal` string; if no refusal and not interrupted (`finish_reason`), output matches schema.

## When to surface
Use when students ask how to *guarantee* JSON/schema adherence, why JSON mode isn’t enough, how constrained decoding works (CFG/token masking), or what failure modes/parameters (`strict`, `max_tokens`, `parallel_tool_calls`) matter in deployment.