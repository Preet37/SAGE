# Card: Latency-aware parallel orchestration via critical path (LAMaS)
**Source:** https://arxiv.org/pdf/2601.10560.pdf  
**Role:** benchmark | **Need:** EMPIRICAL_DATA  
**Anchor:** Experimental tables + equations showing latency (critical path) vs cost/accuracy for parallel DAG orchestration; ablations on latency reward + critical-path credit assignment.

## Key Content
- **Parallel latency vs cost distinction (Section 3.3):**  
  - **Latency (critical path), Eq. 1:** \(L=\sum_{l\in \mathcal{L}} \max_{o\in \mathcal{O}_l} t(o)\)  
    - \(\mathcal{L}\): layers; \(\mathcal{O}_l\): operators executed in parallel at layer \(l\); \(t(o)\): operator time.  
  - **Cost, Eq. 2:** \(C=\sum_{l\in \mathcal{L}} \sum_{o\in \mathcal{O}_l} c(o)\) (token/$ cost accumulates additively).
- **Controller sampling (Eq. 4):** threshold-based subset selection per layer: pick highest-scoring operators until cumulative confidence exceeds threshold \(\tau\); EarlyExit ends generation.
- **Reward (Eq. 5):** global reward combines task score \(S\), cost penalty, and **latency proxy** penalty.  
- **Critical-path-aware credit assignment (Eq. 6–7):** identify per-layer critical operator \(o_l^\*\!=\arg\max_{o\in \mathcal{O}_l}\hat{t}(o)\); apply latency penalty **only** to bottleneck operators to avoid credit assignment error under parallelism.
- **Latency proxy metric (Eq. 9):** CP length (CP len) sums, per layer, the max of (output tokens + scaled tool time). Tool scaling: **1 sec = 50 virtual tokens**.
- **Key results vs MaAS (Table 2):**  
  - GSM8K: **93.37%** score, **CP 913.5** vs MaAS 93.13%, CP 1474.6 (**-38.0%**).  
  - HumanEval: **92.11%**, **CP 1042.7** vs 93.00%, CP 1810.8 (**-42.4%**).  
  - MATH: **52.26%**, **CP 1195.8** vs 51.23%, CP 2218.5 (**-46.1%**).
- **Fixed baselines tradeoffs (Table 3 examples):** GSM8K Generate CP 405.2 (92.80%, cost 0.31) vs LAMaS CP 913.5 (93.37%, cost 0.88); CoT*5+SC cost **1.96** with CP 488.3 (92.99%).
- **Ablations (Table 4):**  
  - **w/o latency weight:** GSM8K CP **1215.9** (vs 913.5) and cost **1.73** (vs 0.88). HumanEval CP **1629.3** (vs 1042.7).  
  - **w/o CP credit (HumanEval):** CP **1197.5** (vs 1042.7), score 91.60 (vs 92.11).
- **Defaults (Section 4.1):** LLM **gpt-4o-mini-0718**, temperature **1**; layers \(=5\); sampling times \(=5\); activation threshold \(\tau=0.8\); latency weight \(\lambda_L=0.5\) (normalized by 50); cost penalty \(\lambda_C=0.1\).

## When to surface
Use when students ask how to orchestrate multi-agent subgraphs in **parallel** and why optimizing **token cost** doesn’t minimize **latency**; or when they need concrete latency/accuracy/cost comparisons and ablation evidence for critical-path supervision.