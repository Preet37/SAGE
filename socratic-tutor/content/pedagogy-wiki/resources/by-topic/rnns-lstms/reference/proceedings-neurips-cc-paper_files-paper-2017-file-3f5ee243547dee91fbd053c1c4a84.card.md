# Card: Transformer Attention (Scaled Dot-Product vs Additive; Multi-Head)
**Source:** https://proceedings.neurips.cc/paper_files/paper/2017/file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf  
**Role:** paper | **Need:** PROCESS/ARCHITECTURE  
**Anchor:** Exact equations + architectural procedure for scaled dot-product attention and multi-head attention; contrasts with additive (Bahdanau) attention and gives rationale.

## Key Content
- **Attention definition (Section 3.2):** maps **query** and **key–value pairs** to an output; output is weighted sum of values; weights from a compatibility function between query and keys.
- **Scaled Dot-Product Attention (Eq. 1, Section 3.2.1):**  
  \[
  \text{Attention}(Q,K,V)=\text{softmax}\left(\frac{QK^\top}{\sqrt{d_k}}\right)V
  \]  
  where \(Q\) (queries), \(K\) (keys) have dimension \(d_k\); \(V\) (values) has dimension \(d_v\).
- **Rationale for scaling (Section 3.2.1, footnote 4):** if components of \(q,k\) are i.i.d. mean 0 var 1, then \(\mathrm{Var}(q\cdot k)=d_k\); large dot products push softmax into tiny-gradient regions → scale by \(1/\sqrt{d_k}\).
- **Additive vs dot-product (Section 3.2.1):** additive attention uses a 1-hidden-layer FFN for compatibility; similar theoretical complexity, but dot-product is faster/more space-efficient via matrix multiplies; additive can outperform **unscaled** dot-product for large \(d_k\).
- **Multi-Head Attention (Section 3.2.2):**  
  \[
  \text{MultiHead}(Q,K,V)=\text{Concat}(\text{head}_1,\dots,\text{head}_h)W^O
  \]
  \[
  \text{head}_i=\text{Attention}(QW_i^Q,KW_i^K,VW_i^V)
  \]
  with \(W_i^Q,W_i^K\in\mathbb{R}^{d_{model}\times d_k}\), \(W_i^V\in\mathbb{R}^{d_{model}\times d_v}\), \(W^O\in\mathbb{R}^{hd_v\times d_{model}}\). Default: \(h=8\), \(d_{model}=512\), \(d_k=d_v=64\).
- **Empirical (Table 3A):** single-head \(h=1\) gives **BLEU 24.9** vs base **25.8** (EN-DE dev); too many heads also drops (e.g., \(h=32\) → **25.4**).
- **Applications (Section 3.2.3):** encoder self-attn; decoder masked self-attn (mask illegal future positions by setting softmax inputs to \(-\infty\)); encoder–decoder attention (decoder queries attend to encoder keys/values).

## When to surface
Use when students ask for the *exact* attention equations, why the \(\sqrt{d_k}\) scaling exists, how multi-head projections are defined, or how this contrasts with additive/Bahdanau attention and masking in decoders.