# Card: GNMT (2016) — Deep LSTM seq2seq w/ attention, residuals, wordpieces, and throughput tricks
**Source:** https://arxiv.org/pdf/1609.08144.pdf  
**Role:** paper | **Need:** COMPARISON_DATA  
**Anchor:** System-level comparison details for pre-Transformer improvements (stacked LSTMs, residual connections, bidirectional encoders, attention) with quality results + computational cost/throughput.

## Key Content
- **Seq2seq + attention equations (Section 3):**  
  - Encoder outputs per source token: \(\mathbf{x}_1,\dots,\mathbf{x}_M=\text{EncoderRNN}(x_1,\dots,x_M)\) (Eq. 1).  
  - Autoregressive factorization: \(P(Y|X)=\prod_{i=1}^{N} P(y_i|y_{0:i-1}; \mathbf{x}_{1:M})\) (Eq. 2–3).  
  - Attention (decoder state \(\mathbf{y}_{i-1}\), encoder vectors \(\mathbf{x}_t\)):  
    \(s_t=\text{AttnFn}(\mathbf{y}_{i-1},\mathbf{x}_t)\); \(p_t=\exp(s_t)/\sum_{t=1}^M \exp(s_t)\); \(\mathbf{a}_i=\sum_{t=1}^M p_t \mathbf{x}_t\) (Eq. 4).
- **Residual LSTM stack (Section 3.1):** between layer \(i\) and \(i{+}1\): \(\mathbf{x}_t^{i}=\mathbf{m}_t^{i}+\mathbf{x}_t^{i-1}\) (Eq. 6). Rationale: improves gradient flow; plain stacking works well to ~4 layers, barely 6, “very poorly beyond 8” without residuals.
- **Architecture/parallelism rationale (Sections 3.2–3.3):** 8-layer encoder + 8-layer decoder; only **bottom encoder layer bidirectional** (others uni) to preserve model-parallel throughput. Attention connects **bottom decoder layer → top encoder layer** to keep decoder-layer parallelism.
- **Wordpieces (Section 4.1):** shared source/target WPM; typical vocab **8k–32k** balances BLEU + speed; helps rare words and avoids long character sequences.
- **Beam search scoring (Section 7, Eq. 14):**  
  \(s(Y,X)=\log P(Y|X)/lp(Y)+cp(X;Y)\); \(lp(Y)=\frac{(5+|Y|)^\alpha}{(5+1)^\alpha}\); \(cp(X;Y)=\beta\sum_{i=1}^{|X|}\log(\min(\sum_{j=1}^{|Y|}p_{i,j},1.0))\). Defaults: \(\alpha=0.2,\beta=0.2\); beam typically 8–12 (4 or 2 only slight BLEU drop).
- **Key empirical results (Tables 4–9):**  
  - WMT’14 En→Fr single: **WPM-32K 38.95 BLEU**, CPU decode **0.2118 s/sent**; Word 37.90 (0.2226), Char 38.01 (1.0530) (Table 4).  
  - WMT’14 En→De single: **WPM-32K 24.61 BLEU**, CPU decode **0.1882 s/sent**; Word 23.12 (0.2972) (Table 5).  
  - RL refinement (Table 6): En→Fr **38.95→39.92**; En→De **24.67→24.60**.  
  - Ensemble 8 models: En→Fr **40.35**, RL-refined **41.16** (Table 7); En→De **26.20**, RL-refined **26.30** (Table 8).  
  - Human SxS (En→Fr): PBMT score **3.87**, NMT ensemble **4.46**, RL ensemble **4.44**, Human ref **4.82** (Table 9).
- **Training pipeline defaults (Section 8.3):** 12 async replicas; batch **128**; init \([-0.04,0.04]\); grad clip norm **5.0**; Adam lr **0.0002** for **60k** steps then SGD lr **0.5**; En→Fr anneal after **1.2M** steps, halve every **200k** for **800k**; dropout **0.2** (En→Fr), **0.3** (En→De).
- **Quantized inference throughput (Section 6, Table 1):** En→Fr dev decode time: CPU **1322s**, GPU **3028s**, TPU **384s**; BLEU ~**31.20–31.21** (no BLEU loss), log perplexity CPU **1.4553** vs TPU **1.4626**.

## When to surface
Use when students ask how classic (pre-Transformer) seq2seq systems addressed the **context bottleneck/long-range dependencies** (attention), trained **very deep LSTMs** (residuals), handled **rare words** (wordpieces), or balanced **quality vs decoding speed** (beam scoring, parallelism, quantized inference).