# Card: QLoRA core procedure + key numbers
**Source:** https://proceedings.neurips.cc/paper_files/paper/2023/file/1feb87871436031bdc0f2beaa62a049b-Paper-Conference.pdf  
**Role:** paper | **Need:** COMPARISON_DATA  
**Anchor:** Core QLoRA procedure (NF4 + double quantization + paged optimizers), key equations, and benchmark tradeoffs (quality vs memory)

## Key Content
- **LoRA equation (Eq. 3):** For linear projection \(Y=XW\), LoRA uses  
  \[
  Y = XW + s X L_1 L_2
  \]
  where \(X\in\mathbb{R}^{b\times h}\), \(W\in\mathbb{R}^{h\times o}\), \(L_1\in\mathbb{R}^{h\times r}\), \(L_2\in\mathbb{R}^{r\times o}\), \(s\)=scalar, \(r\)=rank.
- **Blockwise quantization (Eq. 1–2):**  
  \(X_{\text{Int8}}=\text{round}\big(\frac{127}{\text{absmax}(X_{\text{FP32}})}X_{\text{FP32}}\big)=\text{round}(c\cdot X_{\text{FP32}})\); dequant: \(X_{\text{FP32}}=X_{\text{Int8}}/c\).
- **QLoRA forward (Eq. 5–6, Sec. 3):** store base weights in 4-bit (NF4), compute in BF16:  
  \[
  Y_{\text{BF16}} = X_{\text{BF16}}\;\text{doubleDequant}(c^{(1)}_{\text{FP32}}, c^{(2)}_{k\text{-bit}}, W_{k\text{-bit}}) + X_{\text{BF16}}L^{(1)}_{\text{BF16}}L^{(2)}_{\text{BF16}}
  \]
  with \(\text{doubleDequant}=\text{dequant}(\text{dequant}(c^{(1)},c^{(2)}),W)\Rightarrow W_{\text{BF16}}\). **Only LoRA params get gradients** (base \(W\) frozen).
- **NF4 rationale (Sec. 3):** weights ~ \(N(0,\sigma)\); NFk uses theoretical normal quantiles (Eq. 4) normalized to \([-1,1]\); asymmetric construction ensures exact zero.
- **Double Quantization defaults (Sec. 3):** quantize quantization constants: first-level blocksize **64** for \(W\); second-level uses **FP8**, blocksize **256** for constants. Memory for constants drops from **0.5 bits/param** (32/64) to **0.127 bits/param** (8/64 + 32/(64·256)), saving **0.373 bits/param (~3GB for 65B)**.
- **Paged optimizers (Sec. 3):** use NVIDIA Unified Memory paging to avoid OOM spikes during gradient checkpointing; reported same speed as regular optimizers for **65B, batch size 16**.
- **Empirical comparisons:**
  - **Pile Common Crawl PPL (Table 2):** Int4 **34.34**, FP4(E2M1) **31.07**, FP4(E3M0) **29.48**, **NF4+DQ 27.41** (best).
  - **MMLU 5-shot mean (Table 3):** BF16 **53.0**, Float4 **52.2**, **NF4+DQ 53.1** (matches BF16; FP4 ~1 pt behind).
  - **Vicuna benchmark vs ChatGPT (Table 4, memory):** Guanaco **65B 4-bit 41GB: 99.3% ±4.4**; Guanaco **33B 4-bit 21GB: 97.8% ±4.4**; Vicuna **13B 16-bit 26GB: 94.9% ±4.5**; Guanaco **13B 4-bit 10GB: 90.4% ±5.2**; Guanaco **7B 4-bit 5GB: 87.0% ±5.4**.
  - **Elo (Table 1, GPT-4 judge):** Guanaco 65B **1022±1**, 33B **992±1**, ChatGPT **966±1**, Vicuna 13B **974±1**.
- **Hyperparam scaling rule (Sec. 5.1):** 7B settings generalize; for **33B/65B halve learning rate and double batch size**.

## When to surface
Use when students ask how QLoRA works mathematically (NF4, DQ, paged optimizers), what defaults to use (block sizes, FP8 constants), or how 4-bit adapter tuning compares to BF16/FP4 on MMLU/perplexity and chatbot benchmarks vs memory.