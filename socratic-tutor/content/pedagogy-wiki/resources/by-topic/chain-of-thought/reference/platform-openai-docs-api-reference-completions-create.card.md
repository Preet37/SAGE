# Card: Completions API — decoding controls & reproducibility
**Source:** https://platform.openai.com/docs/api-reference/completions/create  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Parameter-level semantics for multi-sample decoding + reproducibility controls (n, best_of, logprobs, temperature, top_p, max_tokens, stop, seed)

## Key Content
- **Endpoint:** `POST /completions` creates a completion for provided `prompt` + parameters; returns a **Completion object** (or a sequence if streamed).
- **Model (`model`)**: string ID (examples listed: `"gpt-3.5-turbo-instruct"`, `"davinci-002"`, `"babbage-002"`).
- **Prompt (`prompt`) types:** string | array of strings | array of token IDs (numbers) | array of token arrays. If omitted, model generates as from start of new document; `<|endoftext|>` is training-time document separator.
- **Multi-sample decoding:**
  - `n` (min **1**, max **128**): number of completions to generate **per prompt**; increases token usage.
  - `best_of` (min **0**, max **20**): generates `best_of` candidates **server-side** and returns the **single best** by **highest log probability per token**. **Cannot be streamed.**
  - Constraint: when used together, **`best_of` must be > `n`**; `best_of` = candidates, `n` = returned.
- **Token/probability controls:**
  - `max_tokens` (min **0**): max generated tokens; **prompt_tokens + max_tokens ≤ model context length**.
  - `temperature` range **[0, 2]**; higher = more random, lower = more deterministic. Recommendation: change **temperature OR top_p**, not both.
  - `top_p` range **[0, 1]** nucleus sampling: consider tokens within top_p probability mass (e.g., **0.1 → top 10% mass**).
  - `logprobs` (min **0**, max **5**): return logprobs for **logprobs most likely tokens** plus the chosen token (up to **logprobs+1** entries).
- **Stopping:** `stop` string or array (up to **4** sequences); returned text **excludes** stop sequence. **Not supported with reasoning models `o3` and `o4-mini`.**
- **Reproducibility:** `seed` (int64): best-effort deterministic sampling with same seed+params; not guaranteed—monitor `system_fingerprint`.
- **Streaming:** `stream: true` sends SSE token events; terminates with `data: [DONE]`. `best_of` disables streaming.

## When to surface
Use when students ask how to control randomness, generate multiple candidates (n/best_of), inspect token probabilities (logprobs), enforce stopping, manage token limits, or reproduce outputs with seeds/system_fingerprint.