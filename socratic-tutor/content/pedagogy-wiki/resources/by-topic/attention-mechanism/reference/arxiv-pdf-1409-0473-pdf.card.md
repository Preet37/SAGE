# Card: Attention vs Fixed-Vector Bottleneck in Seq2Seq (Bahdanau et al., 2015)
**Source:** https://arxiv.org/pdf/1409.0473.pdf  
**Role:** benchmark | **Need:** EMPIRICAL_DATA  
**Anchor:** Empirical comparison showing fixed-length context bottleneck vs attention; BLEU vs sentence length degradation for non-attentional encoder–decoder.

## Key Content
- **Baseline encoder–decoder (fixed context)** (Sec. 2.1): encoder RNN hidden states  
  **Eq. (1)**: \(h_t=f(x_t,h_{t-1})\); context \(c=q(\{h_1,\dots,h_{T_x}\})\) (often \(c=h_{T_x}\)).  
  Decoder factorization **Eq. (2)**: \(p(y|x)=\prod_{t=1}^{T_y} p(y_t|y_{<t},c)\).  
  Conditional **Eq. (3)**: \(p(y_t|y_{<t},c)=g(y_{t-1}, s_t, c)\).
- **Attention / “RNNsearch”** (Sec. 3): distinct context per target word.  
  **Eq. (4)**: \(p(y_i|y_{<i},x)=g(y_{i-1}, s_i, c_i)\), with \(s_i=f(s_{i-1},y_{i-1},c_i)\).  
  **Eq. (5)**: \(c_i=\sum_{j=1}^{T_x}\alpha_{ij} h_j\).  
  **Eq. (6)**: \(\alpha_{ij}=\frac{\exp(e_{ij})}{\sum_k \exp(e_{ik})}\), \(e_{ij}=a(s_{i-1},h_j)\) (alignment MLP; soft alignment).
- **Encoder choice**: bidirectional RNN annotations \(h_j=[\overrightarrow{h_j};\overleftarrow{h_j}]\) (Sec. 3.2) to summarize both left/right context.
- **Empirical results (WMT’14 En→Fr)** (Table 1): BLEU (All / No-UNK)  
  - RNNencdec-30: **13.93 / 24.19**  
  - RNNsearch-30: **21.50 / 31.44**  
  - RNNencdec-50: **17.82 / 26.71**  
  - RNNsearch-50: **26.75 / 34.16** (trained longer: **28.45 / 36.15**)  
  - Moses: **33.30 / 35.63**
- **Length robustness** (Fig. 2): RNNencdec BLEU **drops sharply** with longer sentences; RNNsearch (esp. -50) shows **no deterioration at length ≥50**.
- **Training/config** (Sec. 4.2, Appx A/B): vocab shortlist **30k** each; train with max sentence length **30 or 50**; hidden units **1000**, embeddings **620**, maxout layer **500**, alignment hidden **1000**; minibatch **80**; optimizer **Adadelta** (\(\rho=0.95,\epsilon=10^{-6}\)); gradient norm clip **1**; beam search decoding.

## When to surface
Use when students ask why classic seq2seq with a single context vector fails on long sequences, or want concrete evidence (BLEU vs length) that attention alleviates the fixed-length bottleneck.