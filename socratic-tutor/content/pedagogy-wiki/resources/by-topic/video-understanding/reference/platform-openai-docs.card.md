# Card: OpenAI Responses API — request schema quickstart (multimodal entry point)
**Source:** https://platform.openai.com/docs  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Platform docs index + canonical “Responses API” entry point and quickstart request/response pattern (used for multimodal inputs via `input`).

## Key Content
- **Primary endpoint (procedure):** Create model outputs via **Responses API**  
  - HTTP: `POST https://api.openai.com/v1/responses`  
  - Headers:  
    - `Content-Type: application/json`  
    - `Authorization: Bearer $OPENAI_API_KEY`
- **Minimal request schema (defaults shown by example):**  
  - JSON body fields used in docs quickstart:  
    - `model` (string): example `"gpt-5.4"`  
    - `input` (string): example `"Write a short bedtime story about a unicorn."`
- **SDK procedure (JavaScript):**
  1. `import OpenAI from "openai"; const client = new OpenAI();`
  2. `await client.responses.create({ model: "gpt-5.4", input: "..." })`
  3. Read text via `response.output_text`
- **SDK procedure (Python):**
  1. `from openai import OpenAI; client = OpenAI()`
  2. `client.responses.create(model="gpt-5.4", input="...")`
  3. Read text via `response.output_text`
- **SDK procedure (C#):**
  - `new OpenAIResponseClient(model: "gpt-5.4", apiKey: envVar)` then `CreateResponse("...")`, read via `GetOutputText()`.
- **Model selection guidance (design rationale):**
  - Use **`gpt-5.4`** for “complex reasoning and coding”; **`gpt-5.4-mini`** / **`gpt-5.4-nano`** for “lower-latency, lower-cost workloads.”

## When to surface
Use when students ask how to structure an OpenAI API call for generation (and where multimodal requests start: `responses.create` with `model` + `input`), or how to retrieve the returned text (`output_text`).