# Card: Self-Consistency for Chain-of-Thought (ICLR 2023)
**Source:** http://arxiv.org/pdf/2203.11171v4.pdf  
**Role:** paper | **Need:** EMPIRICAL_DATA  
**Anchor:** Benchmark tables/ablations comparing self-consistency vs greedy CoT across reasoning datasets + sampling settings + accuracy gains.

## Key Content
- **Method (Self-Consistency; “sample-and-marginalize”, Sec. 2):**
  1) Prompt LM with **CoT exemplars**.  
  2) **Sample** \(m\) diverse outputs \((r_i, a_i)\) from decoder (reasoning path \(r_i\), final answer \(a_i \in \mathcal{A}\)).  
  3) **Aggregate** by marginalizing out \(r_i\): majority vote  
     \[
     a^*=\arg\max_{a\in\mathcal{A}}\sum_{i=1}^{m}\mathbf{1}(a_i=a)
     \]
- **Optional probability-weighted aggregation (Eq. 1, length-normalized):**
  \[
  P(r_i,a_i\mid \text{prompt},q)=\exp\Big(\frac{1}{K}\sum_{k=1}^{K}\log P(t_k\mid \text{prompt},q,t_{<k})\Big)
  \]
  where \(t_k\) are output tokens, \(K\)=#tokens in \((r_i,a_i)\). Finding: **majority vote ≈ normalized weighted sum**; unnormalized weighting performs worse.
- **Sampling defaults (Sec. 3.1):** typically **40 samples**, averaged over **10 runs**.  
  - UL2-20B & LaMDA-137B: temperature \(T=0.5\), top-\(k=40\)  
  - PaLM-540B: \(T=0.7\), top-\(k=40\)  
  - GPT-3: \(T=0.7\), **no top-\(k\)**
- **Key empirical gains (Tables 2–3; absolute accuracy):**
  - **PaLM-540B:** GSM8K **56.5→74.4 (+17.9)**; SVAMP **79.0→86.6 (+7.6)**; AQuA **35.8→48.3 (+12.5)**; ARC-c **85.2→88.7 (+3.5)**; StrategyQA **75.3→81.6 (+6.3)**.
  - **GPT-3 code-davinci-002:** GSM8K **60.1→78.0 (+17.9)**; SVAMP **75.8→86.8 (+11.0)**; AQuA **39.8→52.0 (+12.2)**; StrategyQA **73.4→79.8 (+6.4)**; ARC-c **83.6→87.5 (+3.9)**.
- **Ablations/Comparisons:** More sampled paths improves accuracy (Fig. 2). Self-consistency **beats sample-and-rank** (Fig. 3) and **beam search** (Table 6); beam search reduces diversity.

## When to surface
Use when students ask why **sampling multiple CoT solutions + voting** can outperform greedy decoding, or when they want **concrete benchmark gains** and **recommended sampling parameters** for self-consistency.