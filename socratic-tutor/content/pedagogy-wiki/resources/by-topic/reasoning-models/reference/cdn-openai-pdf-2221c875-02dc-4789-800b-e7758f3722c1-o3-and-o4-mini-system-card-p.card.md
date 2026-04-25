# Card: o3/o4-mini — test-time compute, long rollouts, and benchmark evidence
**Source:** https://cdn.openai.com/pdf/2221c875-02dc-4789-800b-e7758f3722c1/o3-and-o4-mini-system-card.pdf  
**Role:** explainer | **Need:** EMPIRICAL_DATA  
**Anchor:** Citable PDF tables/figures quantifying reasoning/tool-use gains from longer rollouts (“test-time compute”) + evaluation methodology/metrics.

## Key Content
- **Training / design (Sections 1–2):**
  - o3 and o4-mini are **reasoning models trained with large-scale reinforcement learning on chains of thought**; trained to “think before they answer,” trying strategies and recognizing mistakes.
  - Models can **use tools inside their chain-of-thought** (web browsing, Python, image/file analysis, etc.) to augment reasoning.
- **Test-time compute / long rollouts evidence (Cybersecurity CTF; Section 4.3.1, Fig. 7):**
  - Evaluation uses **16 rollouts per CTF**, reports **pass@12** (“best set of rollouts”).
  - With 12 attempts: **o3** solves **89% high-school**, **68% collegiate**, **59% professional** CTFs; **o4-mini** solves **80%**, **55%**, **41%** respectively.
  - Authors attribute gains vs prior o-series models to **improved tool use + ability to make use of long rollouts**.
  - **No-browsing results plotted** to avoid answer lookup contamination.
- **Agentic cyber range workflow + compute settings (Section 4.3.2):**
  - Two scenarios; run configs: **Normal**, **With Hints**, **With Solver Code**.
  - Trials: online-retailer scenario **30 trials/config**; priv-esc scenario **16 trials/config**.
  - Metrics: **pass@12** (Normal/With Hints), **pass@1** (With Solver Code).
  - Key result: **no model solves either scenario unaided or with hints**; **o3/o4-mini solve with reasonably high accuracy when given solver code**.
- **Evaluation methodology note (Section 4.1):**
  - Evals are **lower bounds**; longer rollouts/scaffolding can elicit more capability.
  - **95% CI for pass@1 via bootstrap** over attempts per problem.

## When to surface
Use when students ask how “reasoning effort,” **longer inference rollouts**, or **tool-augmented reasoning** changes measurable performance (e.g., pass@k, agentic tasks), or how browsing/tool access affects benchmark validity (“contamination”).