# Card: Self-Consistency (Sample-and-Marginalize) for CoT Decoding
**Source:** http://webdocs.cs.ualberta.ca/~dale/papers/iclr23b.pdf  
**Role:** paper | **Need:** FORMULA_SOURCE  
**Anchor:** Self-consistency selection objective: marginalize/aggregate over sampled rationales → majority-vote (or weighted) answer selection; explicit decoding procedure + notation.

## Key Content
- **Core procedure (Figure 1; Section 2):**
  1) Prompt LM with **chain-of-thought exemplars**.  
  2) **Sample** a diverse set of outputs (reasoning paths) from the decoder (not greedy).  
  3) **Marginalize out reasoning paths** and **aggregate final answers** to pick the most consistent answer.
- **Notation (Section 2):** sample \(m\) candidate outputs indexed by \(i=1,\dots,m\).  
  - Final answers \(a_i \in \mathcal{A}\) (fixed answer set).  
  - Latent reasoning path \(r_i\) (token sequence) leading to \(a_i\) (reasoning optional: \(r_i \rightarrow a_i\)).
- **Self-consistency objective (majority vote; Section 2):**
  \[
  \hat a=\arg\max_{a}\sum_{i=1}^{m}\mathbf{1}(a_i=a)
  \]
- **Optional probability-weighted aggregation (Eq. 1, length-normalized):**
  \[
  P(r_i,a_i\mid \text{prompt},q)=\exp\left(\frac{1}{K}\sum_{k=1}^{K}\log P(t_k\mid \text{prompt},q,t_{1:k-1})\right)
  \]
  where \(t_k\) is the \(k\)-th token in \((r_i,a_i)\), \(K\)=#tokens.
- **Empirical aggregation comparison (Table 1, PaLM-540B):** majority vote (“Unweighted sum”) strong: GSM8K **74.4**, MultiArith **99.3**, AQuA **48.3**, SVAMP **86.6**, CSQA **80.7**, ARC-c **88.7**.
- **Main gains vs greedy CoT (Tables 2–3):** PaLM-540B GSM8K **56.5→74.4 (+17.9)**; AQuA **35.8→48.3 (+12.5)**; SVAMP **79.0→86.6 (+7.6)**; StrategyQA **75.3→81.6 (+6.3)**; ARC-c **85.2→88.7 (+3.5)**.
- **Defaults (Section 3.1):** typically **40 sampled outputs** per run; sampling: UL2/LaMDA \(T=0.5, k=40\); PaLM \(T=0.7, k=40\); GPT-3 \(T=0.7\) (no top-k).

## When to surface
Use when students ask how to **choose an answer from multiple CoT samples**, why **majority vote over rationales** works, or want the **exact self-consistency formula / decoding steps / sampling defaults**.