# Card: MoReS (LLaVA Steering) — VLM PEFT with extreme parameter reduction
**Source:** https://aclanthology.org/2025.acl-long.739.pdf  
**Role:** paper | **Need:** EMPIRICAL_DATA  
**Anchor:** VLM-specific PEFT results/ablations: where to add steering modules, parameter counts, benchmark impacts in LLaVA-style visual instruction tuning

## Key Content
- **Autoregressive conditioning (Eq. 1, Sec. 3):**  
  \(p(\hat{y})=\prod_{i=1}^{L} p(\hat{y}_i \mid \hat{y}_{<i}, R_{\text{text}}, R_{\text{image}}, R_{\text{sys}})\).  
  \(\hat{y}_i\): i-th output token; \(R_{\text{text}}\), \(R_{\text{image}}\): text/vision representations; \(R_{\text{sys}}\): system context; \(L\): output length.
- **Modality balance metric LMAR (Eq. 2, Sec. 3):**  
  \(\text{LMAR}_l=\frac{1}{N}\sum_{i=1}^{N}\frac{\alpha^{l}_{\text{image},i}}{\alpha^{l}_{\text{text},i}}\).  
  \(\alpha^{l}_{\text{image},i}\), \(\alpha^{l}_{\text{text},i}\): *mean per-token* attention to visual/text tokens at layer \(l\) for sample \(i\); \(N\): samples. LMAR≈1 implies balanced per-token attention (important because vision tokens can be ~576 vs dozens of text tokens).
- **MoReS steering (Eqs. 3–4, Sec. 4):** freeze LLM; **insert per-layer linear steering on visual tokens** in a low-dim subspace.  
  \(\text{MoReS}(h)=W_{\text{up}}\cdot \phi(h)\); \(\phi(h)=\text{Linear}(h)-W_{\text{down}}h\).  
  \(h\in\mathbb{R}^D\), \(W_{\text{down}}\in\mathbb{R}^{d\times D}\), \(W_{\text{up}}\in\mathbb{R}^{D\times d}\), \(d<D\); constraint \(W_{\text{down}}W_{\text{up}}^{T}=I_D\).
- **Training procedure defaults (Sec. 5):** LLaVA-1.5 recipe; visual instruction tuning on **LLaVA-665k**; apply MoReS in **each LLM layer** but only to **1% of visual tokens** (sparse steering).
- **Multi-task SFT results (Table 1, LLaVA Steering-3B):**  
  Trainable params in LLM (TP*): **FT 2.78B**, Adapter **83M**, LoRA **188.7M**, OFT **39.3M**, IA3 **0.49M**, **MoReS-B 0.164M**, **MoReS-L 0.328M**, **MoReS-H 0.655M**.  
  MoReS-H: **POPE 88.2**, **MMMU 35.8**, SciQA-IMG **71.9**, MM-Vet **31.1**; achieves **287–1150× fewer TP than LoRA** (depending on setup).
- **Hallucination mitigation (Table 6):** MoReS best: **POPE Acc 88.2** (vs Full 87.2; LoRA 86.7); HallucinationBench **Hard Acc 42.6** (vs IA3 39.3; Full 37.4).
- **Ablations (Sec. 5.7):**
  - **Subspace rank (Table 7):** rank=**1** best avg **81.8** across 4 tasks with **0.164M** TP (rank 2: 0.328M; rank 4: 0.655M; rank 8: 1.340M).
  - **Steered visual token ratio (Table 8):** **1%** best overall (e.g., SciQA-IMG 89.7, IconQA-blank 94.1); dense 100% hurts (SciQA-IMG 85.8, IconQA-txt 67.7).

## When to surface
Use when students ask where to place LoRA/adapters in LLaVA-like VLMs, how many trainable parameters different PEFT methods use, or what ablations (rank, token steering ratio) most affect VLM instruction-tuning performance and hallucinations.