# Card: Joint Adaptive Representations (efficient image–language fusion)
**Source:** https://arxiv.org/pdf/2305.19924.pdf  
**Role:** paper | **Need:** COMPARISON_DATA  
**Anchor:** Quantitative compute/accuracy tradeoffs from reducing/reshaping visual tokens; efficient fusion vs concatenation/cross-attn/Perceiver/co-tokenization.

## Key Content
- **Problem/rationale (Sec. 2, Fig. 2–3):**
  - Concatenation increases sequence length by **H·W** visual tokens → attention cost grows quadratically; scales poorly with image/model size.
  - Standard cross-attention “squeezes” many visual tokens (e.g., **14×14=196** at 224²) into few text tokens (e.g., **~10** in VQA) → information bottleneck.
  - Goal: **reduce tokens first**, then **iteratively fuse** with low FLOPs; expensive tokenization over full inputs done **once** (unlike Perceiver/co-tokenization).

- **Core equations (Sec. 2):**
  - **Eq. 1 (visual projection):** \(P(X_{im}) = W_1 X_{im}\), where \(X_{im}\in\mathbb{R}^{H\times W\times C}\), \(P(X_{im})\in\mathbb{R}^{H\!*\!W\times D}\).
  - **Eq. 2 (latent token resampling, DETR-style learnable tokens):** learn \(X_N\in\mathbb{R}^{N\times D}\); \(f_N = W_2\,\Phi(X_N, P(X_{im}))\). Similarly produce \(t_N\) from \(X_{text}\in\mathbb{R}^{L\times D}\). \(N\) is **not tied** to text length.
  - **Eq. 3 (gated fusion):**
    - \(P_{cr}(t_N,f_N)=Ln(t_N)+\tanh(\alpha)\Phi(Ln(t_N),Ln(f_N))\)
    - \(F(t_N,f_N)=P_{cr}+\tanh(\beta)MLP(P_{cr})\)
  - **Eq. 4 (iterative refinement):** replace \(t_N\) with \(F_i+t_N\); compute \(F_{i+1}\) via Eq. 3 then transformer layer \(T(\cdot)\).

- **Key empirical results (Tables 1–4):**
  - **Concat baseline vs Ours (Table 3):** **58.4→38.9 GFLOPs** (~**33%** less; **1.5× fewer FLOPs**) and **GQA 78.9→79.1**, **SNLI-VE 77.4→77.9**. Memory **15GB→9GB** (~40% reduction).
  - **Vs Perceiver/CoTokenization (Table 2, base):** Perceiver **40.3 GF** (GQA **78.2**), CoToken **43.8 GF** (GQA **78.5**), **Ours 38.9 GF** (GQA **79.1**, SNLI-VE **77.9**).
  - **Ablations (Table 4):**
    - Iterations: **1/2/4/8** → **34.2/35.5/38.9/42.5 GF**, GQA **78.3/78.8/79.1/79.2** (diminishing returns).
    - Tokens \(N\): **16/32/64/128** → **18.5/28.4/38.9/72.9 GF**, GQA **76.5/78.3/79.1/79.2**.
    - Resampling: **Latent** better than **Spatial** (GQA **79.1 vs 78.9**, **38.9 vs 42.5 GF**).
    - Iterative combination: **Weighted** best (GQA **79.1**) vs **Residual 78.7**, **None 78.1** at same **38.9 GF**.
    - Fusion module layers: **32 layers** best among shown (**38.9 GF**, GQA **79.1**) vs **16 layers 30.5 GF, 78.3**; very deep (**822.4 GF**) hurts (**76.7**).

## When to surface
Use when students ask how VLMs reduce visual tokens / improve throughput (GFLOPs, memory) and what accuracy tradeoffs occur vs concatenation, cross-attention, Perceiver-style resampling, or iterative co-tokenization.