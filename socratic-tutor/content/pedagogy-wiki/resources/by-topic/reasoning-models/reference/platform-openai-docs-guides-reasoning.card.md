# Card: Reasoning models via Responses API (effort, tokens, summaries)
**Source:** https://platform.openai.com/docs/guides/reasoning  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** How to use reasoning models with the Responses API; parameters to control reasoning behavior and how to request/suppress reasoning outputs.

## Key Content
- **Model guidance (selection):** Start with `gpt-5.4` for most reasoning workloads; use `gpt-5.4-pro` for highest intelligence (more latency); `gpt-5-mini` / `gpt-5-nano` for lower cost/latency. Reasoning models “work better” with **Responses API** vs Chat Completions.
- **Core control knob:** `reasoning: {"effort": <level>}` guides how many **reasoning tokens** are generated before visible output. Supported values (model-dependent): `none`, `minimal`, `low`, `medium`, `high`, `xhigh`.  
  - Table (start here when…):  
    - `none`: lowest latency for extraction/routing/simple transforms  
    - `low`: small extra thinking improves reliability  
    - `medium`/`high`: planning, coding, synthesis, harder reasoning  
    - `xhigh`: only if evals justify extra latency/cost  
  - Defaults are model-dependent: `gpt-5.4` defaults to `none`; older GPT‑5 models default to `medium`.
- **Token accounting & context:** Reasoning tokens are **discarded from context after** the response, but still **consume context window** and are **billed as output tokens**. Usage shows reasoning tokens at:  
  `usage.output_tokens_details.reasoning_tokens` (example: `reasoning_tokens: 1024`).
- **Cost/length limit:** `max_output_tokens` caps **(reasoning + final output)** tokens.
- **Incomplete handling:** If context limit or `max_output_tokens` hit → `status: "incomplete"` and `incomplete_details.reason: "max_output_tokens"`. Can happen **before any visible output** (cost incurred for input + reasoning).
- **Practical buffer:** Recommend reserving **≥ 25,000 tokens** for reasoning+outputs when experimenting.
- **Function calling continuity:** Pass back **reasoning items** (plus tool call + tool outputs) across turns; easiest via `previous_response_id` or replaying prior `output` items.
- **Stateless/ZDR:** Include `"reasoning.encrypted_content"` in `include` to receive encrypted reasoning items for reuse.
- **Reasoning summaries (not raw traces):** Opt-in via `reasoning.summary` (e.g., `"auto"`). Summary appears in an output item of type `"reasoning"` under `summary[]`.

## When to surface
Use when students ask how to control “thinking”/latency/cost in OpenAI reasoning models, interpret reasoning token usage, handle incomplete responses, or request reasoning summaries/encrypted reasoning items in the Responses API.