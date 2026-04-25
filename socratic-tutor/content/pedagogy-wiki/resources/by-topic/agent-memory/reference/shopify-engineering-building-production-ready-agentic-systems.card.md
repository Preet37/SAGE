# Card: Production-ready agentic loop patterns (Shopify Sidekick)
**Source:** https://shopify.engineering/building-production-ready-agentic-systems  
**Role:** explainer | **Need:** DEPLOYMENT_CASE  
**Anchor:** Production architecture patterns for an agentic loop incl. Just-in-Time (JIT) instructions/context injection + operational considerations

## Key Content
- **Agentic loop (architecture):** Human input → LLM decides actions → actions executed in environment/tools → feedback collected → loop continues until task complete (single-agent emphasized).
- **Tool scaling failure mode (“Tool Complexity Problem”):**
  - **0–20 tools:** clear boundaries, easy debugging.
  - **20–50 tools:** unclear boundaries; tool combinations cause unexpected outcomes.
  - **50+ tools:** multiple ways to do same task; system hard to reason about.
  - Leads to **“Death by a Thousand Instructions”**: bloated system prompt with special cases/conflicts.
- **Just-in-Time (JIT) instructions (context injection):** Return **relevant instructions alongside tool data only when needed**; aim: “perfect context… not a token less, not a token more.”
  - Benefits: **localized guidance**, **cache efficiency** (change instructions without breaking prompt caches), **modularity** (vary by beta flags, model versions, page context).
- **Evaluation shift:** Reject “vibe testing” / generic “rate 0–10” judges; require **principled, statistically rigorous** evaluation.
- **Ground Truth Sets (GTX) over golden datasets:** Sample **real production conversations**; define criteria from observed distribution.
  - **Human eval:** ≥ **3 product experts** label conversations across criteria.
  - **Inter-annotator stats:** **Cohen’s Kappa**, **Kendall Tau**, **Pearson correlation**; treat human agreement as theoretical max for judges.
- **LLM-as-a-Judge calibration:** Improve judge from **Kappa 0.02 → 0.61**; human baseline **0.69**. Trust when swapping judge/human in GTX is hard to distinguish.
- **Pre-prod testing:** LLM **merchant simulator** replays “essence/goals” of real convos through candidate systems to catch regressions.
- **Training:** **GRPO** with **N-stage gated rewards** = procedural validation (syntax/schema) + semantic LLM-judge rewards.
  - **Reward hacking modes:** opt-out (“can’t help”), tag hacking, schema violations (hallucinated IDs/enum).
  - Fixes improved **syntax validation ~93% → ~99%**, judge correlation **0.66 → 0.75**; end-to-end quality matched SFT baseline.
- **Deployment recommendations:** stay simple (quality>quantity tools), start modular (JIT early), avoid multi-agent early; expect reward hacking; iterative judge refinement.

## When to surface
Use when students ask how to scale tool-using agents in production (prompt bloat, tool explosion), how to inject context safely (JIT), or how to evaluate/train agentic systems with rigorous judges, simulators, and anti–reward-hacking measures.