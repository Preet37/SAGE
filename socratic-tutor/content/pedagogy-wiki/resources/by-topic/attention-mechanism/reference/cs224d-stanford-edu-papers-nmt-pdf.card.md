# Card: Seq2Seq Encoder–Decoder & Fixed-Vector Bottleneck (pre-attention baseline)
**Source:** https://cs224d.stanford.edu/papers/nmt.pdf  
**Role:** explainer | **Need:** CONCEPT_EXPLAINER  
**Anchor:** Step-by-step encoder→fixed vector *c/z*→decoder pipeline; why single-vector context is a bottleneck; baseline before attention + teacher-forcing-style conditional factorization.

## Key Content
- **Seq2Seq objective (Sec.2):** translation as \(\arg\max_y p(y\mid x)\). Decoder factorization (Eq.2):  
  \[
  p(y)=\prod_{t=1}^{T_y} p(y_t \mid y_{<t}, c)
  \]
- **Encoder (Eq.1):** reads source \(x=(x_1,\dots,x_{T_x})\) with RNN hidden states  
  \[
  h_t=f(x_t,h_{t-1})
  \]
  and produces **fixed-length context** \(c=q(\{h_1,\dots,h_{T_x}\})\). Example choice: \(q(\cdot)=h_{T_x}\) (Sutskever et al.).
- **Decoder conditional (Eq.3):**  
  \[
  p(y_t\mid y_{<t},c)=g(y_{t-1}, s_t, c)
  \]
  where \(s_t\) is decoder RNN state.
- **Design rationale / bottleneck (Intro, Sec.2):** compressing *all* source info into a single fixed-length vector \(c\) makes long sentences hard; performance of basic encoder–decoder **deteriorates rapidly with input length** (cited Cho et al. 2014b).
- **Attention-style fix (Sec.3, contrast to baseline):** replace single \(c\) with per-step \(c_i\) (Eq.4–6):  
  \[
  p(y_i\mid y_{<i},x)=g(y_{i-1}, s_i, c_i),\quad c_i=\sum_{j=1}^{T_x}\alpha_{ij}h_j
  \]
  \(\alpha_{ij}=\text{softmax}(e_{ij})\), \(e_{ij}=a(s_{i-1},h_j)\). Frees model from single-vector bottleneck.
- **Empirical numbers (Table 1, BLEU):**  
  - RNNencdec-30: **13.93** (All), **24.19** (No UNK)  
  - RNNsearch-50: **26.75** (All), **34.16** (No UNK)  
  - Moses: **33.30** (All), **35.63** (No UNK)  
  Fig.2: RNNencdec BLEU drops sharply with sentence length; RNNsearch-50 shows **no deterioration** at length ≥50.
- **Training defaults (Sec.4, Appx B):** shortlist vocab **30k** each side; minibatch **80**; Adadelta \(\rho=0.95,\ \epsilon=10^{-6}\); gradient norm clip **1**; beam search decoding.

## When to surface
Use when students ask how classic seq2seq works (encoder→single context vector→decoder), why fixed-length context causes an information bottleneck/long-range dependency issues, or how attention changes the conditioning and improves long-sentence performance.