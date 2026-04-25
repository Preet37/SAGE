# Card: Auto Evol-Instruct (Automatic Instruction Evolving)
**Source:** https://aclanthology.org/2024.emnlp-main.397.pdf  
**Role:** paper | **Need:** EMPIRICAL_DATA  
**Anchor:** Empirical comparison/ablation of instruction-evolving strategies (auto-designed evolution rules + selection by failure rate) with downstream benchmark gains.

## Key Content
- **Goal / optimization objective (Eq. 1):** find evolving method \(e^*\) maximizing post-SFT performance on evolved data:  
  \[
  e^*=\arg\max_e Q(X_e)
  \]
  where \(X=\{x_i\}\) is seed instruction-response data, \(X_e\) is evolved dataset under method \(e\), \(Q(\cdot)\) is downstream benchmark score after instruction tuning.
- **Core workflow (Sec. 3; Fig. 1):**
  1) Start with **universal initial evolving method** prompt (Fig. 2): Step1 list methods to increase complexity; Step2 plan; Step3 rewrite adding **10–20 words**; Step4 review for reasonableness.  
  2) Iteratively optimize evolving method using **optimizer LLM** via: **Evol Trajectory Analysis** (prompt Fig. 7) → **Evolving Method Optimization** (Fig. 8).  
  3) **Multiple optimizations (self-consistency):** run optimizer \(m\) times; select method with **lowest evolution failure rate** on dev set \(D\).
- **Failure-rate selection (Eq. 2):**
  \[
  \lambda_{R^{e_i^t}}=\frac{\sum_{r\in R^{e_i^t}}F(r)}{|D|}
  \]
  \(R^{e_i^t}\): responses when answering evolved dev instructions; \(F(r)\in\{0,1\}\) flags evolution failure (Appendix A rules: e.g., “Understood/Thank you … ?”, “Sure … ?”, contains “please provide”).
- **Defaults / setup (Table 1):** seed data sizes: ShareGPT **10K**, GSM8K-train **7K**, Code Alpaca **20K**. Evol+optimizer LLM often **GPT-4**; subset ~**2,000** samples used to optimize method (footnote Sec. 3).
- **Main empirical results (Table 2; large models):**
  - Mixtral-8x7B + **10K evolved ShareGPT**: **MT-Bench 8.09**, **AlpacaEval 91.37** (vs seed 7.65/87.98; Evol-Instruct 7.76/89.50).
  - Mixtral-8x7B + **7K evolved GSM8K**: **GSM8K 82.49** (vs seed 70.60; Evol-Instruct 79.15).
  - DeepSeek-Coder-Base-33B + **20K evolved Code Alpaca**: **HumanEval 77.40** (vs seed 72.00; Evol-Instruct 73.20).
- **Ablations:**
  - Initial evolving method alone improves vs Evol-Instruct (Fig. 3): MT-Bench **6.31→6.60**, HumanEval **61.0→62.2**; Auto Evol-Instruct further to MT-Bench **6.71**, HumanEval **64.0**, GSM8K **64.4**.
  - **#optimizations \(m\)** (Fig. 5a, GSM8K): \(m=1\) → **62.7**, \(m=9\) → **65.0**.
  - **Optimization steps** (Fig. 5b): performance rises early, then **drops after ~12 steps** (over-optimization).
  - **Evol LLM strength** (Table 3, GSM8K): Auto Evol-Instruct with evol LLM **GPT-3.5: 64.4**; with **GPT-4: 70.7**.
- **Contamination check (Sec. 5.6):** GSM8K evolved 7K; only **10** samples show any **13-gram** match.

## When to surface
Use when students ask how “evol-instruct/auto-evolution” is implemented (selection criteria, failure detection, optimization loop) or want concrete benchmark deltas from evolving-method ablations and hyperparameters (m, steps, data sizes, evol LLM choice).