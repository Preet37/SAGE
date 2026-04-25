# Card: Completions API — output budgeting & determinism knobs
**Source:** https://platform.openai.com/docs/api-reference/completions/create  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Endpoint-specific schema for request/response fields and parameter semantics needed to implement memory-carryover and output budgeting in production.

## Key Content
- **Endpoint:** `POST /v1/completions` → returns a **Completion object** (or a sequence if streamed). Streamed and non-streamed responses share the **same shape**.
- **Core budgeting constraint (Eq. 1):**  
  **tokens(prompt) + max_tokens ≤ model_context_length**  
  - `max_tokens` = maximum tokens generated in the completion (min 0).
- **Prompt formats:** `prompt` can be **string**, **array of strings**, **array of tokens (numbers)**, or **array of token arrays**. `<|endoftext|>` acts as a document separator; if no prompt, model generates from start of a new document.
- **Candidate generation controls:**
  - `n` (min 1, max 128): number of completions per prompt.
  - `best_of` (min 0, max 20): generates `best_of` candidates server-side and returns the single best by **highest logprob per token**. **Cannot be streamed.** If used with `n`: **best_of > n**. Token quota can rise quickly → pair with reasonable `max_tokens` and `stop`.
- **Stopping:** `stop` = string or array (up to **4** sequences); returned text **excludes** stop sequence. **Not supported with reasoning models `o3` and `o4-mini`.**
- **Sampling knobs:** `temperature` ∈ [0,2]; `top_p` ∈ [0,1]; recommendation: adjust **one**, not both.
- **Penalties:** `frequency_penalty`, `presence_penalty` ∈ [-2, 2].
- **Determinism:** `seed` (int64) → best-effort deterministic; monitor backend changes via `system_fingerprint` in response.
- **Logprobs:** `logprobs` max **5**; response may include up to **logprobs+1** tokens (always includes sampled token).
- **Logit bias:** map token_id → bias [-100,100]; e.g., `{"50256": -100}` bans `<|endoftext|>`.
- **Streaming:** `stream: true` uses SSE; terminates with `data: [DONE]`. `stream_options` only when streaming.
- **Response usage accounting:** `usage = {prompt_tokens, completion_tokens, total_tokens}`.

## When to surface
Use when students ask how to **cap output length**, **trim/fit conversation history into context**, **stop generation**, **stream tokens**, or **make outputs repeatable** (seed/system_fingerprint) with the Completions endpoint.