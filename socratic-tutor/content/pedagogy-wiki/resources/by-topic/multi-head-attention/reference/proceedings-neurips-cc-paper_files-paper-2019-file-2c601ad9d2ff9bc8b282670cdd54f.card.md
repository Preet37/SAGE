# Card: Head pruning shows many MHA heads are redundant
**Source:** https://proceedings.neurips.cc/paper_files/paper/2019/file/2c601ad9d2ff9bc8b282670cdd54f69f-Paper.pdf  
**Role:** benchmark | **Need:** EMPIRICAL_DATA  
**Anchor:** Head-pruning ablations + greedy pruning via gradient-based head-importance

## Key Content
- **Multi-Head Attention (Eq. 1):**  
  \[
  \mathrm{MHAtt}(x,q)=\sum_{h=1}^{N_h}\mathrm{Att}_h(x,q)
  \]
  with head-specific params \(W_k^h,W_q^h,W_v^h\in\mathbb{R}^{d_h\times d}\), \(W_o^h\in\mathbb{R}^{d\times d_h}\). Typically \(d_h=d/N_h\) (keeps params constant; “ensemble of low-rank” attentions).
- **Masking heads (Sec. 2.3):**  
  \[
  \mathrm{MHAtt}(x,q)=\sum_{h=1}^{N_h}\xi_h\,\mathrm{Att}_h(x,q),\quad \xi_h\in\{0,1\}
  \]
  Mask head \(h\) by setting \(\xi_h=0\).
- **Single-head attention (Sec. 2.1):**  
  \[
  \mathrm{Att}(x,q)=W_o\sum_{i=1}^n \alpha_i W_v x_i,\quad
  \alpha_i=\mathrm{softmax}\Big(\frac{q^\top W_q^\top W_k x_i}{\sqrt d}\Big)
  \]
- **Empirical ablations (Sec. 3):**
  - WMT14 En→Fr Transformer-Large (6 layers, **16 heads/layer**, BLEU base **36.05**): only **8/96** encoder self-attn heads cause **significant** BLEU change when individually removed (p<0.01); ~half of those *increase* BLEU.
  - **All-but-one head per layer (Tables 2–3):** many layers can be reduced to **1 head** with minimal loss; but WMT **Enc-Dec layer 6** single-head causes **−13.56 BLEU** (catastrophic).
  - BERT-base (12 layers, **12 heads/layer**) fine-tuned on MNLI: best single-head-per-layer deltas range about **−0.96% to +0.10%**, none significant (p<0.01).
- **Greedy iterative pruning (Sec. 4):** rank heads by importance \(I_h\) and prune lowest first.
  - **Importance score (Eq. 2):**  
    \[
    I_h=\mathbb{E}_{x\sim X}\left|\frac{\partial L(x)}{\partial \xi_h}\right|
    =\mathbb{E}_{x\sim X}\left|\mathrm{Att}_h(x)^\top \frac{\partial L(x)}{\partial \mathrm{Att}_h(x)}\right|
    \]
    Compute via forward+backward pass; normalize scores **per layer** with \(\ell_2\) norm.
  - Can prune **~20%** heads (WMT) and **~40%** heads (BERT) with no noticeable drop; further pruning drops sharply.
- **Efficiency (Table 4):** actually pruning **50%** of BERT heads yields up to **+17.5%** inference speed at larger batch sizes (e.g., batch 64: **124.7→146.6 ex/s**).
- **Design insight (Sec. 5):** WMT **encoder-decoder (cross-)attention** is far more sensitive to pruning than self-attention; pruning >**60%** Enc-Dec heads causes catastrophic BLEU degradation.

## When to surface
Use when students ask whether “more heads are better,” how to measure head importance, or what pruning/ablation evidence says about redundancy—especially differences between self-attention vs encoder-decoder (cross-)attention sensitivity.