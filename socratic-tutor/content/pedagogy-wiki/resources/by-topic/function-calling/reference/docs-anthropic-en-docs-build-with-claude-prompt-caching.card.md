# Card: Prompt caching (Claude API) — cost/latency control for iterative loops
**Source:** https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching  
**Role:** reference_doc | **Need:** DEPLOYMENT_CASE  
**Anchor:** Cacheable prompt prefixes + billing/TTL implications for multi-step agent/ReAct/tool loops

## Key Content
- **Mechanism (prefix caching):** Caches the **entire prompt prefix** in order **tools → system → messages**, up to and including the block marked with `cache_control`. Cache hits require **100% identical** content (incl. images) through the breakpoint.
- **Two enablement modes:**
  - **Automatic caching:** top-level `"cache_control": {"type":"ephemeral"}`; breakpoint auto-moves to **last cacheable block** as conversation grows.
  - **Explicit breakpoints:** put `cache_control` on specific content blocks; up to **4 breakpoints**.
- **Core algorithm (explicit) (Section “How automatic prefix checking works”):**
  1) **Write only at breakpoints** (one cache entry = hash of prefix ending at breakpoint).  
  2) **Read by lookback:** if no hit at breakpoint, walk backward **1 block at a time** to find a prior **write**.  
  3) **Lookback window = 20 blocks** (breakpoint counts as 1st checked). If last write is >20 blocks back, no hit unless you add another breakpoint earlier.
- **Common pitfall:** placing breakpoint on a **changing block** (timestamp/per-request suffix) yields repeated **cache writes** and **no reads**; move breakpoint to last **stable** block.
- **Defaults/params:**
  - Cache type: `"ephemeral"` only.
  - **TTL default = 5 minutes**; optional `"ttl":"1h"` (higher cost). Cache refreshed at no extra cost on use.
- **Pricing multipliers (all models):** 5m **writes = 1.25×** base input; 1h **writes = 2×** base input; **reads = 0.1×** base input. Example row: **Claude Opus 4.6** base input **$5/MTok**, 5m writes **$6.25/MTok**, 1h writes **$10/MTok**, reads **$0.50/MTok**, output **$25/MTok**.
- **Token accounting (Eq. 1):**  
  `total_input_tokens = cache_read_input_tokens + cache_creation_input_tokens + input_tokens`  
  where `input_tokens` = tokens **after last breakpoint**.
- **Minimum cacheable length:** Opus 4.6/4.5 **4096** tokens; Sonnet 4.6 **2048**; many others **1024** (silent no-cache if below).
- **Thinking blocks:** cannot be directly marked cacheable; can be cached when included in prior assistant turns; **count as input tokens when read**. Non-tool-result user content can strip prior thinking blocks.

## When to surface
Use when students ask how to reduce **latency/cost** in long multi-turn or tool-using ReAct agents, how to place cache breakpoints, or how caching affects **billing/token counts/TTL**.