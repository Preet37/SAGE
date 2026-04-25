# Card: o3-mini empirical evals + compute/latency tradeoffs (benchmarks)
**Source:** https://cdn.openai.com/o3-mini-system-card-feb10.pdf  
**Role:** explainer | **Need:** [EMPIRICAL_DATA]  
**Anchor:** o3-mini-specific benchmark tables; reasoning behavior vs latency/cost via tool scaffolds + test-time attempts

## Key Content
- **Reasoning model training (Section 2):** o-series trained with **large-scale reinforcement learning** to “think before answering” (chain-of-thought), learning to refine strategies and recognize mistakes; includes **deliberative alignment** (explicitly reason through safety specs before answering).
- **Evaluation defaults / test-time compute:**
  - **CTF eval (Sec. 5.3):** headless Kali Linux; **up to 60 rounds of tool use per attempt**; **12 attempts per task**. Results (post-mitigation): **61%** high-school, **21%** collegiate, **21%** professional CTFs.
  - **SWE-bench Verified N=477 (Sec. 5.7.2):**
    - *Agentless 1.0 scaffold:* **5 tries** to generate patch; metric **pass@1** computed by averaging per-instance pass rates over valid patches.
    - *o3-mini (tools) internal scaffold:* efficient iterative editing/debugging; **4 tries per instance**; **pass@1 = 61%** (non-final checkpoint).
    - *o3-mini launch candidate (Agentless):* **39%**; **o1: 48%**. (Shows tool scaffold/test-time procedure materially changes performance.)
- **Safety/jailbreak robustness (Sec. 4):**
  - StrongReject goodness@0.1: **GPT-4o 0.37**, **o1-mini 0.72**, **o3-mini 0.73**.
  - Gray Swan Arena attack success rate: **o3-mini 3.6%**, **o1-mini 3.7%**, **gpt-4o 4.0%**, **o1 1.9%**.
- **Hallucination (PersonQA, Table 3):** accuracy **o3-mini 21.7%**; hallucination rate **14.8%** (vs **GPT-4o-mini 52.4%**, **o1-mini 27.4%**).
- **Model autonomy indicator (Sec. 5.7):** interview coding **92% pass@1**; multiple-choice matches o1 (cons@32).

## When to surface
Use when students ask for **concrete benchmark numbers**, or how **more test-time compute / more tries / tool scaffolds** change reasoning performance, latency, and cost tradeoffs (e.g., SWE-bench “tools” vs agentless).