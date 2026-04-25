# Card: Function-calling evals (BFCL vs NFCL) + practical pitfalls
**Source:** https://www.databricks.com/blog/unpacking-function-calling-eval  
**Role:** explainer | **Need:** EMPIRICAL_DATA  
**Anchor:** Practical evaluation breakdown for function calling: metrics to track, failure modes, and why leaderboard scores can mislead (with concrete benchmark setups).

## Key Content
- **Function calling requirements (Section 1):** model must (1) interpret request, (2) decide whether tools are needed, (3) emit a **correctly formatted call** with correct arguments (typically via **JSON schema**).
- **BFCL taxonomy (Section 2):**
  - *Simple Function* (1 tool; generate args), *Multiple Function* (choose among 2–4 tools + args), *Parallel Function* (same tool invoked multiple times), *Parallel Multiple Function* (multiple tools, multiple invocations), *Relevance Detection* (none relevant → **no call**).
  - **Scoring:** AST-based matching (parse call → extract args → compare to ground truth). Authors found AST accuracy correlates with executable eval; they used AST only.
  - **Pitfall:** Relevance Detection can be gamed—if a model never calls tools, it can score **100%** on this subset.
- **NFCL taxonomy (Section 2):** categories by API source; implemented as **static dummy Python functions** with real API-like signatures.
  - NVD (2 APIs, ~**30 args** each), VirusTotal (**12** APIs), OTX (**9** simple APIs; easiest), Places (nested calls up to **7** deep), Climate (parallel + nested), VirusTotal Nested, NVD Nested (very hard; **no model >10%** in authors’ tests).
  - **Scoring:** exact string match of final call (rare false positives; can cause false negatives).
- **Empirical sensitivity (Section 3):** BFCL accuracy can vary by **~10%** depending on decoding; **Temperature 0.0** usually best for programmatic tool calling. Public BFCL used **T=0.7** and bespoke parsing for DBRX → unfair comparisons.
- **Prompting/protocol that improved results (Section 4):**
  - Put tool definitions in **system prompt** (token savings in multi-turn).
  - Enforce strict output: tool list inside `<tools>`; tool calls as **valid JSON list** between `{tool_call_start}`…`{tool_call_end}` with keys `"name"` and `"arguments"`.
  - Guiding rules: don’t hallucinate tools; don’t call irrelevant tools; **never call same function twice with same args**; user executes tools and returns results next turn.
  - Few-shot “check each tool for relevance” improved BFCL Relevance Detection: **Llama3-70b 63.75%→75.41%**, **Llama3-8b 19.58%→78.33%**; **DBRX 84.58%→77.08%** (because flawed outputs previously inflated relevance score).
- **Design rationale (Section 4–5):** no single leaderboard is sufficient; combine BFCL+NFCL; interpret scores holistically; consider **structured generation / constrained decoding** (Outlines, Guidance, SGlang) for schema guarantees.

## When to surface
Use when students ask how to **evaluate tool/function-calling**, why **leaderboard scores disagree**, what **failure modes** to watch (relevance detection, nesting/parallelism), or what **decoding/prompt defaults** improve reliability.