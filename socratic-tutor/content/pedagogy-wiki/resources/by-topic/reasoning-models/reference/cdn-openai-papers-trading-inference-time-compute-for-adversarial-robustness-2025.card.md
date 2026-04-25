# Card: Inference-time compute ↔ adversarial robustness (o1)
**Source:** https://cdn.openai.com/papers/trading-inference-time-compute-for-adversarial-robustness-20250121_1.pdf  
**Role:** paper | **Need:** EMPIRICAL_DATA  
**Anchor:** Quantitative evidence that increasing inference-time compute improves robustness/performance; methods + metrics (e.g., StrongREJECT goodness@0.1), attack/defense scaling curves, and human red-teaming table.

## Key Content
- **Adversarial training objective (context, Intro):**  
  \[
  \min_f \mathbb{E}_{(x,y)\sim D}\left[\max_{t\in T} L(f(t(x)),y)\right]
  \]
  where \(T\) is allowed perturbations; contrasted with this paper’s approach: **no adversarial training**, only **more inference-time compute** (“thinking time”).
- **Core measurement protocol (Sec. 2):** For each prompt \(x\), sample multiple model outputs at varying **defender inference-time compute**; compute **attack success probability** vs (a) attacker resources and (b) defender compute. Models: **o1-preview, o1-mini** (plus **o1-v** for vision).
- **Tasks + attacker goals (Table 1):**
  - Math (2-digit add/mult; MATH): force output **42**, **correct+1**, or **correct×7**.
  - Safety: **StrongREJECT** (60 filtered policy-violating prompts; 35 jailbreaks), **Misuse Prompts**, **Rule Following** (unambiguous internal spec subset).
  - Agentic: **AdvSimpleQA** prompt injection; adversary wants output **“COMPROMISED”**.
  - Vision: ImageNet-A; Attack-Bard (transfer, \(\epsilon=16/255\), \(L_\infty\)); plus Attack-Bard-clean.
- **StrongREJECT metric (Sec. 3.2, Fig. 7):** **goodness@0.1** = for each misuse prompt, apply all jailbreaks; score responses with StrongREJECT grader; take **worst 10%** average; then average over prompts. Robustness **increases nearly monotonically** with compute.
- **Key empirical patterns (Figs. 2,3,12–15):**
  - For **unambiguous tasks** (math, AdvSimpleQA), for fixed attacker resources, attack success **tends toward 0** as compute increases.
  - **Soft-token attack procedure (Sec. 3.4):** optimize soft embeddings on train split to maximize logprob of sampled CoT + adversary answer; evaluate on held-out test; unconstrained norms can grow **>1000×** typical embedding norm → use **norm-capped** projection to average embedding norm every few steps.
- **Human red-teaming (Sec. 3.7, Table 2; o1-preview; 40 red-teamers; 5 compute levels):**
  - Avg attempts needed for success (↑ better): **11.0, 16.8, 15.6, 15.9, 22.6** (levels 1→5).
  - Transfer success on 80 prompts (↓ better): **36%, 30%, 21%, 20%, 19%**.
- **New compute-targeting attacks:** “**Think Less**” reduces model compute (Sec. 3.8); “**Nerd sniping**” shows top **5%** longest-compute traces can have **higher** attack success than median (Sec. 3.9, Fig. 18).

## When to surface
Use when students ask for **evidence/benchmarks** that “more thinking tokens/test-time compute” improves **robustness**, how it’s **measured (goodness@0.1, worst-10%)**, or what **attack/defense scaling** experiments and red-teaming results show.