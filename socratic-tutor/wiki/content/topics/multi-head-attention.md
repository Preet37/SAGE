---
title: "Multi-Head Attention"
subject: "Sequence Models & Attention"
date: 2026-04-06
tags:
  - "subject/sequence-models-and-attention"
  - "level/beginner"
  - "level/intermediate"
  - "level/advanced"
  - "educator/3blue1brown"
  - "educator/jay-alammar"
  - "educator/lilian-weng"
  - "educator/andrej-karpathy"
  - "resource/video"
  - "resource/blog"
  - "resource/deep-dive"
  - "resource/paper"
  - "resource/code"
educators:
  - "3Blue1Brown"
  - "Jay Alammar"
  - "Lilian Weng"
  - "Andrej Karpathy"
levels:
  - "beginner"
  - "intermediate"
  - "advanced"
resources:
  - "video"
  - "blog"
  - "deep-dive"
  - "paper"
  - "code"
---

# Multi Head Attention

## Video (best)
- **3Blue1Brown** — "Attention in transformers, visually explained | Chapter 6, Deep Learning"
- **Watch:** [YouTube](https://www.youtube.com/watch?v=eMlx5fFNoYc)
- Why: Exceptional visual intuition for how attention heads carve up representation space, with geometric analogies that make the multi-head mechanism genuinely comprehensible rather than just mechanically described. Part of the "Neural Networks" series which builds context cleanly.
- Level: beginner/intermediate

## Blog / Written explainer (best)
- **Jay Alammar** — "The Illustrated Transformer"
- **Link:** [https://jalammar.github.io/illustrated-transformer/](https://jalammar.github.io/illustrated-transformer/)
- Why: The definitive visual walkthrough of multi-head attention. Alammar's step-by-step diagrams showing Q/K/V projections, the splitting into heads, parallel attention computation, and concatenation/projection are unmatched in clarity. Widely considered the canonical introductory reference for this exact mechanism.
- Level: beginner/intermediate

## Deep dive
- **Lilian Weng** — "Attention? Attention!"
- **Link:** [https://lilianweng.github.io/posts/2018-06-24-attention/](https://lilianweng.github.io/posts/2018-06-24-attention/)
- Why: Comprehensive technical treatment covering the full attention family tree — from Bahdanau through self-attention to multi-head — with precise mathematical notation, architectural variants, and historical context. Weng's posts are research-grade while remaining pedagogically structured.
- Level: intermediate/advanced

## Original paper
- **Vaswani et al.** — "Attention Is All You Need"
- **Link:** [https://arxiv.org/abs/1706.03762](https://arxiv.org/abs/1706.03762)
- Why: The seminal paper introducing multi-head attention as a named, formalized mechanism. Section 3.2 is unusually readable for a foundational ML paper, with clear equations and explicit motivation for why multiple heads are used (attending to information from different representation subspaces).
- Level: intermediate/advanced

## Code walkthrough
- **Andrej Karpathy** — "Let's build GPT: from scratch, in code, spelled out"
- **Watch:** [YouTube](https://www.youtube.com/watch?v=kCc8FmEb1nY)
- Why: Karpathy builds multi-head attention from absolute scratch in PyTorch, narrating every design decision. The progression from single-head to multi-head is explicit and the code is minimal enough to see the structure clearly. Paired with the nanoGPT repo for reference implementation.
- Level: intermediate

## Coverage notes
- **Strong:** Introductory visual explanations (Alammar, 3B1B) are exceptional. The original paper is highly readable. From-scratch code implementation (Karpathy) is best-in-class.
- **Weak:** Cross-attention and gated cross-attention (relevant to `intro-to-multimodal`) are underserved by the resources above, which focus on self-attention in decoder/encoder-only contexts.
- **Gap:** No single excellent resource specifically targets **gated cross-attention** (as used in Flamingo-style multimodal architectures). For `intro-to-multimodal`, instructors should supplement with the Flamingo paper directly (https://arxiv.org/abs/2204.14198) and Weng's multimodal post. No dedicated YouTube explainer for gated cross-attention exists at the quality tier specified.

## Cross-validation
This topic appears in 2 courses: **intro-to-llms**, **intro-to-multimodal**
- For `intro-to-llms`: All resources above apply directly. Karpathy's code walkthrough is especially well-aligned.
- For `intro-to-multimodal`: The self-attention resources provide necessary foundation, but cross-attention and gated cross-attention require supplementary material not covered by the primary resources listed here. Flag this gap for curriculum designers.

---

## Additional Resources for Tutor Depth

> **6 sources** — papers, official docs, working code, benchmarks, and deep explainers that give the AI tutor precision on this topic.

### 📄 ALiBi (Attention with Linear Biases) logits bias + slope schedule
**Paper** · [source](https://arxiv.org/abs/2108.12409)

*ALiBi attention-score modification: add head-specific linear bias proportional to relative distance directly to \(QK^\top\) logits (pre-softmax), incl. slope schedule across heads*

<details>
<summary>Key content</summary>

- **ALiBi attention logits modification (Section 3):** for causal self-attention, for query position \(i\in\{1,\dots,L\}\) with query vector \(q_i\in\mathbb{R}^{1\times d}\) and key matrix \(K\), replace standard logits \(q_iK^\top\) with  
  \[
  \text{softmax}\Big(q_iK^\top \;+\; m\cdot [-(i-1),\ldots,-2,-1,0]\Big)
  \]
  where **\(m\)** is a **head-specific slope** (fixed, non-learned). The bias is a **linear penalty proportional to distance** (more negative for farther keys).  
  **Note:** bias term is **not multiplied by** the usual \(\sqrt{d_k}\) scaling factor (footnote 10).
- **No positional embeddings:** ALiBi **does not add** positional embeddings to token embeddings; it injects position info only via the attention-score bias.
- **Slope defaults (Section 3):**
  - For **8 heads:** geometric sequence \(2^{-1},2^{-2},\ldots,2^{-8}\).
  - For **16 heads:** interpolate by **geometric averaging** consecutive pairs of the 8-head slopes (producing a geometric sequence starting at the smallest slope and using that value as ratio).
- **Implementation procedure:** add the linear biases to the **mask matrix** (easy “few lines of code” change); works naturally with causal masking.
- **Empirical results (Abstract + Results):**
  - **1.3B** model trained with **1024** tokens extrapolates to **2048**, matching perplexity of sinusoidal model trained on 2048 while **11% faster** and **11% less memory**.
  - WikiText-103 example: model trained on **512** tokens gets **19.73** ppl at \(L_{valid}=512\), improves to **18.40** at \(L_{valid}=3072\).

</details>

### 📄 FlashAttention (IO-aware exact attention via tiling)
**Paper** · [source](https://arxiv.org/pdf/2205.14135.pdf)

*IO-aware attention algorithm (tiling/blocking) that avoids materializing the \(N\times N\) attention matrix; measured speedups + linear-memory attention.*

<details>
<summary>Key content</summary>

- **Standard attention equations (Section 2.2):**  
  \(S = QK^\top \in \mathbb{R}^{N\times N}\), \(P=\mathrm{softmax}(S)\) (row-wise), \(O=PV \in \mathbb{R}^{N\times d}\), with \(Q,K,V\in\mathbb{R}^{N\times d}\). Standard implementations **materialize** \(S\) and \(P\) in HBM \(\Rightarrow O(N^2)\) memory.
- **Why IO-aware (Section 1–2):** attention is often **memory-bandwidth-bound** (HBM much slower than on-chip SRAM). Example A100: HBM \(\sim 1.5\!-\!2.0\) TB/s vs SRAM bandwidth \(\sim 19\) TB/s; SRAM is tiny (per-SM 192KB; figure also notes ~20MB total SRAM).
- **FlashAttention algorithm (Algorithm 1, Section 3.1):**  
  Tile \(Q\) into \(T_r=\lceil N/B_r\rceil\) blocks and \(K,V\) into \(T_c=\lceil N/B_c\rceil\) blocks. Outer loop over \(K_j,V_j\) blocks loaded to SRAM; inner loop over \(Q_i\) blocks. Compute block scores \(S_{ij}=Q_iK_j^\top\), then **online softmax** using per-row stats: rowmax \(\tilde m_{ij}\), rowsum \(\tilde \ell_{ij}\); update running \(m_i,\ell_i\) and accumulate \(O_i\) with correct renormalization. Store only \(O\) and \((m,\ell)\) for backward; **recompute** attention blocks on-chip in backward (selective checkpointing).
  Block sizes: \(B_c=\lceil M/(4d)\rceil\), \(B_r=\min(\lceil M/(4d)\rceil, d)\) where \(M\)=SRAM size.
- **Complexity (Theorem 2):**  
  Standard attention HBM accesses: \(\Theta(Nd + N^2)\).  
  FlashAttention HBM accesses: \(\Theta(N^2 d^2 / M)\).  
  Lower bound: no exact attention can do \(o(N^2 d^2/M)\) HBM accesses for all \(M\in[d,Nd]\) (Proposition 3).
- **Empirical speed/memory (Figures/Tables):**
  - GPT-2 medium attention (N=1024, d=64, 16 heads, batch 64, A100): **HBM R/W 40.3GB → 4.4GB**, runtime **41.7ms → 7.3ms** (Fig. 2 left).  
  - Reported attention-kernel speedup up to **7.6×** vs PyTorch on GPT-2 attention compute (Fig. 1 right).  
  - End-to-end training: **BERT-large (seq 512) 20.0±1.5 min → 17.4±1.4 min** (15% faster than MLPerf 1.1 record, Table 1).  
  - GPT-2 medium training on 8×A100: HuggingFace **21.0 days** vs FlashAttention **6.9 days (3.0×)** (Table 2).  
  - Memory footprint scales **linearly** in \(N\); up to **20×** more memory-efficient than exact attention baselines (Fig. 3 right).

</details>

### 📄 RoPE (Rotary Position Embedding) equations for attention
**Paper** · [source](https://arxiv.org/abs/2104.09864)

*RoPE equations: position-dependent 2D rotations applied to Q,K so dot-products encode relative position; even/odd dim pairing*

<details>
<summary>Key content</summary>

- **Self-attention with position-aware Q,K,V (Eq. 1–2):**  
  \( \mathbf{q}_m=f_q(\mathbf{x}_m,m),\ \mathbf{k}_n=f_k(\mathbf{x}_n,n),\ \mathbf{v}_n=f_v(\mathbf{x}_n,n)\).  
  \(a_{m,n}=\frac{\exp(\mathbf{q}_m^\top \mathbf{k}_n/\sqrt d)}{\sum_{j=1}^N \exp(\mathbf{q}_m^\top \mathbf{k}_j/\sqrt d)}\),  
  \(\mathbf{o}_m=\sum_{n=1}^N a_{m,n}\mathbf{v}_n\).
- **Goal (relative-only dependence, Eq. 11):**  
  \(\langle f_q(\mathbf{x}_m,m), f_k(\mathbf{x}_n,n)\rangle = g(\mathbf{x}_m,\mathbf{x}_n,m-n)\).
- **2D RoPE (Section 3.2.1, Eq. 12/13):** treat 2D vectors as complex numbers.  
  \(f_q(\mathbf{x}_m,m)=(\mathbf{W}_q\mathbf{x}_m)e^{im\theta}\),  
  \(f_k(\mathbf{x}_n,n)=(\mathbf{W}_k\mathbf{x}_n)e^{in\theta}\),  
  \(g=\Re\!\left[(\mathbf{W}_q\mathbf{x}_m)(\mathbf{W}_k\mathbf{x}_n)^* e^{i(m-n)\theta}\right]\).  
  Equivalent real form: rotate \((u,v)\) by angle \(m\theta\) using \(\begin{pmatrix}\cos m\theta&-\sin m\theta\\ \sin m\theta&\cos m\theta\end{pmatrix}\).
- **General d-dim RoPE (Section 3.2.2, Eq. 14–16):** for even \(d\), pair dims into \(d/2\) 2D subspaces.  
  \(f_{\{q,k\}}(\mathbf{x}_m,m)=\mathbf{R}^d_{\Theta,m}\mathbf{W}_{\{q,k\}}\mathbf{x}_m\), where \(\mathbf{R}^d_{\Theta,m}\) is block-diagonal with 2×2 rotation blocks using angles \(m\theta_i\).  
  \(\theta_i = 10000^{-2(i-1)/d}\) (pre-defined).  
  Dot-product becomes relative: \((\mathbf{R}_{\Theta,m}\mathbf{W}_q\mathbf{x}_m)^\top(\mathbf{R}_{\Theta,n}\mathbf{W}_k\mathbf{x}_n) = (\mathbf{W}_q\mathbf{x}_m)^\top \mathbf{R}_{\Theta,n-m}(\mathbf{W}_k\mathbf{x}_n)\), with \(\mathbf{R}_{\Theta,n-m}=(\mathbf{R}_{\Theta,m})^\top\mathbf{R}_{\Theta,n}\).  
  \(\mathbf{R}\) is **orthogonal** ⇒ preserves norms/stability.
- **Design rationale (Section 3.3):** multiplicative rotation (not additive) yields explicit **relative position** in attention; choosing \(\theta_i=10000^{-2i/d}\) gives **long-term decay** of inner-product with increasing \(|m-n|\).

</details>

### 📊 Head pruning shows many MHA heads are redundant
**Benchmark** · [source](https://proceedings.neurips.cc/paper_files/paper/2019/file/2c601ad9d2ff9bc8b282670cdd54f69f-Paper.pdf)

*Head-pruning ablations + greedy pruning via gradient-based head-importance*

<details>
<summary>Key content</summary>

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

</details>

### 📖 PyTorch `nn.MultiheadAttention` (API shapes + masks)
**Reference Doc** · [source](https://docs.pytorch.org/docs/stable/generated/torch.nn.MultiheadAttention.html)

*Exact `forward()` tensor shapes, `attn_mask` vs `key_padding_mask`, constructor defaults*

<details>
<summary>Key content</summary>

- **Module purpose (Eq. 1: Multi-Head Attention):** Implements “Attention Is All You Need” multi-head attention; conceptually  
  **MultiHead(Q,K,V) = Concat(head₁,…,head_h) Wᴼ**, where each head attends in a subspace; **embed_dim** is split across **num_heads** (per-head dim = `embed_dim // num_heads`).
- **Constructor signature + defaults:**  
  `MultiheadAttention(embed_dim, num_heads, dropout=0.0, bias=True, add_bias_kv=False, add_zero_attn=False, kdim=None, vdim=None, batch_first=False, ...)`  
  - `kdim=None` ⇒ `kdim=embed_dim`; `vdim=None` ⇒ `vdim=embed_dim`  
  - `dropout` applies to `attn_output_weights` (default **0.0**).
- **Forward signature:**  
  `forward(query, key, value, key_padding_mask=None, need_weights=True, attn_mask=None, average_attn_weights=True, is_causal=False)`
- **Input shapes (batched):**
  - If `batch_first=False` (default): `query (L,N,E)`, `key/value (S,N,Ek/Ev)`
  - If `batch_first=True`: `query (N,L,E)`, `key/value (N,S,Ek/Ev)`
  - Unbatched: `query (L,E)`, `key/value (S,Ek/Ev)`; `batch_first` ignored.
- **Masks:**
  - `key_padding_mask`: shape `(N,S)` (or `(S)` unbatched). **True** (binary) ⇒ ignore that key position; float mask is **added** to corresponding key scores.
  - `attn_mask`: 2D `(L,S)` broadcast across batch, or 3D `(N,L,S)` per batch entry. **True** (binary) ⇒ disallow attending; float mask is **added** to attention weights. If both masks given, their **types must match**.
  - `is_causal=True` applies a causal mask (hint that `attn_mask` is causal).
- **Outputs:**
  - `attn_output`: `(L,N,E)` or `(N,L,E)` (or `(L,E)` unbatched).
  - `attn_output_weights` (if `need_weights=True`):  
    - averaged heads (`average_attn_weights=True`): `(N,L,S)` (or `(L,S)` unbatched)  
    - per-head (`average_attn_weights=False`): `(N,num_heads,L,S)` (or `(num_heads,L,S)` unbatched).
- **Performance note:** Set `need_weights=False` to use optimized `scaled_dot_product_attention()` for best performance.

</details>

### 📖 tf.keras.layers.MultiHeadAttention — constructor, call semantics, masks
**Reference Doc** · [source](https://www.tensorflow.org/api_docs/python/tf/keras/layers/MultiHeadAttention)

*Constructor/forward argument semantics and defaults (num_heads, key_dim/value_dim, attention_axes, dropout, use_bias) plus mask handling and returned attention scores*

<details>
<summary>Key content</summary>

- **Purpose/definition:** Implements multi-head attention (Vaswani et al., 2017). If `query`, `key`, `value` are the same tensor ⇒ **self-attention**; otherwise can be used for **cross-attention**.
- **Core computation (Eq. 1: scaled dot-product attention per head):**  
  - Project inputs into heads:  
    - `Q`: shape `(B, <query dims>, key_dim)`  
    - `K`: shape `(B, <key/value dims>, key_dim)`  
    - `V`: shape `(B, <key/value dims>, value_dim)`  
    (effectively a list of `num_heads` tensors)  
  - Scores: `scores = (Q · K^T) / sqrt(key_dim)`  
  - Probabilities: `P = softmax(scores)`  
  - Head output: `O_head = P · V`  
  - Concatenate heads, then optional final linear projection.
- **Constructor args + defaults:**  
  - `num_heads` (required): number of attention heads  
  - `key_dim` (required): size per head for query/key  
  - `value_dim=None`: size per head for value  
  - `dropout=0.0`: dropout probability (applied in training)  
  - `use_bias=True`: whether dense projections use bias  
  - `output_shape=None`: if `None`, output projects back to **query last-dim**; else projects to `output_shape`  
  - `attention_axes=None`: axes to apply attention over; `None` ⇒ all axes except batch, heads, features
- **Call signature + shapes:**  
  - `query`: `(B, T, dim)`; `value`: `(B, S, dim)`; `key` optional `(B, S, dim)`; if `key` omitted ⇒ `key=value`  
  - `attention_mask`: boolean `(B, T, S)`; `1` allow attention, `0` block; broadcasting allowed over missing batch dims and head dim  
  - `use_causal_mask`: boolean to prevent attending to future tokens  
  - `return_attention_scores=False`: if `True` returns `(attention_output, attention_scores)`
- **Returns:**  
  - `attention_output`: `(B, T, E)` where `E` is query last-dim if `output_shape=None`, else `output_shape`  
  - `attention_scores` (optional): multi-head attention coefficients over attention axes

</details>

---

## Related Topics

- [[topics/attention-mechanism|Attention Mechanism]]
- [[topics/self-attention|Self-Attention]]
- [[topics/transformer-architecture|Transformer Architecture]]
