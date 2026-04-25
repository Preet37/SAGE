# Card: Structured Outputs / JSON mode — doc index (404 snapshot)
**Source:** https://platform.openai.com/docs/guides/structured-outputs/json-mode?context=without_parse  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Intended to cover exact request/response fields + behavioral guarantees for JSON mode vs Structured Outputs; fetched content is a “Page not found” snapshot plus docs navigation.

## Key Content
- **HTTP result:** Target URL returned **404: Not Found** (“Page not found”).
- **No API semantics present:** The fetched page contains **no** concrete details about:
  - `response_format` fields, JSON mode invocation, or Structured Outputs guarantees
  - request/response schemas, tool/function calling payloads, streaming event shapes
  - defaults/parameters, error-handling procedures, or comparisons between modes
- **Navigation pointers (relevant alternative docs to consult):**
  - Core concepts: **Structured output** (`/api/docs/guides/structured-outputs`)
  - Core concepts: **Function calling** (`/api/docs/guides/function-calling`)
  - Core concepts: **Using tools** (`/api/docs/guides/tools`)
  - Run & scale: **Streaming** (`/api/docs/guides/streaming-responses`)
  - Suggested search terms shown on page: `response_format`, `reasoning_effort`, `streaming`, `tools`

## When to surface
Use this card when a student asks for the **exact JSON mode vs Structured Outputs guarantees or fields** and you need to confirm the authoritative doc—this snapshot indicates the specific URL is **not available** and you should pivot to the linked **Structured outputs** and **Function calling** guides in the docs navigation.