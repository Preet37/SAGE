---
title: "LoRA & PEFT"
subject: "Large Language Models"
date: 2026-04-06
tags:
  - "subject/large-language-models"
  - "level/intermediate"
  - "level/advanced"
  - "educator/andrej-karpathy"
  - "educator/sebastian-raschka"
  - "educator/lilian-weng"
  - "educator/hugging-face"
  - "resource/video"
  - "resource/blog"
  - "resource/deep-dive"
  - "resource/paper"
  - "resource/code"
educators:
  - "Andrej Karpathy"
  - "Sebastian Raschka"
  - "Lilian Weng"
  - "Hugging Face"
levels:
  - "intermediate"
  - "advanced"
resources:
  - "video"
  - "blog"
  - "deep-dive"
  - "paper"
  - "code"
---

# Lora Peft

## Video (best)
- **Andrej Karpathy** — "State of GPT" (covers fine-tuning landscape including LoRA/PEFT in context)
- **Watch:** [YouTube](https://www.youtube.com/watch?v=CRFON_RPa_E)
- Why: Karpathy provides authoritative, intuitive framing of why parameter-efficient fine-tuning matters and where LoRA fits in the modern LLM training pipeline. Accessible to practitioners without sacrificing technical depth.
- Level: intermediate

> **Note:** A more directly focused alternative is Sebastian Raschka's dedicated LoRA explainer videos on YouTube — search "Sebastian Raschka LoRA" to verify current best candidate. No single canonical 3Blue1Brown/Karpathy video exists that is *exclusively* about LoRA.

## Blog / Written explainer (best)
- **Sebastian Raschka** — "Parameter-Efficient LLM Fine-Tuning With Low-Rank Adaptation (LoRA)"
- **Link:** [https://magazine.sebastianraschka.com/p/practical-tips-for-finetuning-llms](https://magazine.sebastianraschka.com/p/practical-tips-for-finetuning-llms)
- Why: Raschka systematically explains the mathematical intuition behind low-rank decomposition, compares LoRA to other PEFT methods (prefix tuning, adapters), and includes practical guidance. His writing bridges theory and implementation better than most sources for this specific topic.
- Level: intermediate

## Deep dive
- **Lilian Weng** — "Parameter-Efficient Transfer Learning"
- **Link:** [https://lilianweng.github.io/posts/2023-01-27-the-transformer-family-v2/](https://lilianweng.github.io/posts/2023-01-27-the-transformer-family-v2/)
- Why: Weng's blog posts are the gold standard for comprehensive, well-cited technical surveys. Her coverage of adapter methods, prompt tuning, and LoRA variants provides the broadest and most rigorous reference for understanding the full PEFT landscape including QLoRA and multi-modal extensions.
- Level: advanced

> **Better candidate:** https://lilianweng.github.io/posts/2023-01-27-the-transformer-family-v2/ may not be the exact post — her PEFT-specific post should be verified. Search lilianweng.github.io for "fine-tuning" or "PEFT". [NOT VERIFIED]

## Original paper
- **Hu et al. (2021)** — "LoRA: Low-Rank Adaptation of Large Language Models"
- **Link:** [https://arxiv.org/abs/2106.09685](https://arxiv.org/abs/2106.09685)
- Why: This is the seminal, clearly written paper that introduced LoRA. The authors provide strong motivation, clean mathematical formulation (W = W₀ + BA where B and A are low-rank matrices), and empirical results across GPT-2/3 and RoBERTa. Unusually readable for a systems paper. QLoRA (arxiv.org/abs/2305.14314) is the essential follow-on for quantization-aware fine-tuning.
- Level: intermediate

## Code walkthrough
- **Hugging Face** — PEFT library documentation and LoRA fine-tuning notebook
- **Link:** [https://github.com/huggingface/peft](https://github.com/huggingface/peft)
- Why: The official PEFT library by Hugging Face is the de facto implementation standard. Their example notebooks cover LoRA, QLoRA, and multi-modal fine-tuning (including LLaVA-style VLMs) with working code. Directly maps to how practitioners implement these methods in production. The `examples/` directory includes causal LM and sequence classification walkthroughs.
- Level: intermediate

> **Supplementary code resource:** Tim Dettmers' QLoRA repository (github.com/artidoro/qlora) is the canonical reference for quantized LoRA implementation.

---

## Coverage notes
- **Strong:** Core LoRA mathematics, PEFT comparison, QLoRA, LLM fine-tuning workflows — well covered across the resources above
- **Weak:** LoRA specifically for Vision-Language Models (VLMs) and multi-modal fine-tuning — fewer dedicated tutorials exist; most resources treat this as an extension of LLM LoRA
- **Gap:** No single excellent YouTube video exists that covers *both* LoRA fundamentals AND its application to VLMs (lora-for-vlms, visual instruction tuning) in one place. The multi-modal fine-tuning angle (relevant to `intro-to-multimodal`) requires piecing together LLaVA paper + PEFT docs. No 3Blue1Brown or Yannic Kilcher video is exclusively dedicated to LoRA/PEFT as of knowledge cutoff.

---

## Cross-validation
This topic appears in 2 courses: **intro-to-llms**, **intro-to-multimodal**

- For `intro-to-llms`: The LoRA paper + Raschka blog + PEFT code walkthrough form a complete unit covering adapter methods, low-rank adaptation, and QLoRA.
- For `intro-to-multimodal`: Additional coverage of visual instruction tuning and LoRA-for-VLMs is needed. The LLaVA paper (arxiv.org/abs/2304.08485) and InstructBLIP serve as companion readings for the multi-modal fine-tuning angle. The PEFT library's multimodal examples are the best available code resource for this gap.

---

---

## Additional Resources for Tutor Depth

> **10 sources** — papers, official docs, working code, benchmarks, and deep explainers that give the AI tutor precision on this topic.

### 📄 LoRAServe—rank-aware distributed serving for heterogeneous LoRA
**Paper** · [source](https://www.arxiv.org/pdf/2511.22880.pdf)

*Cluster-level design to serve many LoRA adapters with heterogeneous ranks; quantifies rank interference + dynamic placement/routing + RDMA-based remote adapter access.*

<details>
<summary>Key content</summary>

- **Problem (rank heterogeneity interference):** Multi-tenant LoRA kernels (Punica BGMV, S-LoRA MBGMV) size compute tiles/pipelines to the **maximum rank in the batch**, so low-rank requests “pay” for high-rank ones → tail latency skew. Example (Sec. I/III-A5, Fig.1): co-serving **rank-8 + rank-128** on Llama-7B increases **P95 TTFT of rank-8 by 84%** vs serving only rank-8.
- **SLO impact:** Common SLO cited: **P95 TTFT < 10s** (Sec. III-A4). Under a **4 RPS Poisson** workload with **P95 TTFT SLO=20s**, **ranks 64/128 violate SLO** while smaller ranks do not (Fig.6).
- **Scaling effects:** Rank heterogeneity penalty grows with model size: up to **45% degradation on Llama-70B** (Sec. III-A2). Tensor parallelism reduces but doesn’t remove it: with **TP=8**, rank-128 still causes **~20% TTFT increase** vs rank-8 on Llama-7B (Sec. III-A3).
- **Memory pressure numbers:** For a **200B** model quantized to **8-bit**, base size ≈ **200GB**; LoRA adapters ≈ **1%** of model → **~2GB/adapter**; **500 adapters ≈ 1TB** if replicated per server (Sec. I).
- **LoRAServe architecture (Sec. IV):** Cluster orchestrator maintains routing table with tuples **(adapter a, servers S, probabilities p)**; route to server *s* with probability **p_s**, with **∑_{s∈S} p_s = 1**. If adapter absent locally, fetch from remote server via **GPUDirect RDMA over InfiniBand**, then cache in host memory.
- **Placement algorithm (Alg.1, Sec. IV-A):** Per timestep: (1) estimate **TPS demand per adapter**; (2) compute per-rank server budget using profiled **rank operating points under SLO** (max TPS per rank); (3) **fractional bin packing** for ranks with budget; (4) place remaining adapters on servers with higher max-rank capacity; (5) **permute to minimize deviation** from previous placement; (6) update routing + metadata.
- **Empirical gains (Abstract/Sec. V-F):** On Company X traces: up to **2× throughput**, up to **9× lower TTFT**, and up to **50% fewer GPUs** vs SOTA; reduces per-server adapter storage footprint up to **16×** vs Toppings.

</details>

### 📄 MoReS (LLaVA Steering) — VLM PEFT with extreme parameter reduction
**Paper** · [source](https://aclanthology.org/2025.acl-long.739.pdf)

*VLM-specific PEFT results/ablations: where to add steering modules, parameter counts, benchmark impacts in LLaVA-style visual instruction tuning*

<details>
<summary>Key content</summary>

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

</details>

### 📄 MobileVLM training + LoRA insertion points in VLM stacks
**Paper** · [source](https://arxiv.org/pdf/2312.16886.pdf)

*Reproducible VLM pipeline (frozen vision encoder + projector + LLM) + 2-step VLM training and LoRA results for PEFT discussion.*

<details>
<summary>Key content</summary>

- **Architecture (Sec. 3.1):** 3 parts: (1) vision encoder, (2) LLM (MobileLLaMA), (3) efficient projector (LDP) aligning vision→text embedding space.
- **Eq. (1) (Sec. 3.1):** Projector maps visual embeddings to LLM word-embedding dimension:  
  - Input visual tokens: \(Z \in \mathbb{R}^{N \times D_v}\) (N patches/tokens, \(D_v\) vision hidden size).  
  - Output image tokens: \(V \in \mathbb{R}^{M \times D_t}\) (M visual tokens after compression/alignment, \(D_t\) LLM embedding size).
- **Eq. (2):** Autoregressive generation conditioned on multimodal tokens (image tokens + text tokens) to produce output length \(L\).
- **Projector rationale (Sec. 3.4):** Q-Former can lose spatial info + slow convergence + inefficient on edge; plain MLP keeps spatial info but injects many useless/background tokens → slows inference. LDP uses **depthwise conv** and **stride-2 downsampling** to reduce tokens while preserving spatial structure.
- **Token reduction & quality (Sec. 5.1):** LDP reduces visual tokens **576 → 144 (−75%)** with **equivalent or sometimes better** benchmark performance vs baseline.
- **Resolution vs token strategy (Sec. 5.3, Table 11):** Keeping 144 tokens via LDP beats reducing input resolution (RIR):  
  - **LDP:** GQA 56.1, SQA 54.7, VQA 41.5, POPE 84.5, MME 1196.2, MMB 53.2  
  - **RIR:** GQA 53.9, SQA 53.1, VQA 37.1, POPE 81.5, MME 1072.5, MMB 46.7
- **VLM training procedure (Sec. 4.1):** Two-step multimodal training (like LLaVA/mPLUG style):  
  1) **Pre-train:** freeze **vision encoder + LLM**, train **projector only** on **CC-595K** for **1 epoch**, lr **2e-3**, batch **256**.  
  2) **Instruction tuning:** fine-tune **projector + LLM** on **LLaVA-Instruct-158K** for **1 epoch**, lr **2e-5**, batch **128**. Optimizer AdamW, **no weight decay**, cosine LR, **3% warmup**.
- **LoRA PEFT result (Sec. 4.4):** During visual instruction tuning, freeze all LLM params except LoRA; trainable params are **8.87% (1.4B)** and **7.41% (2.7B)** of full LLM; LoRA config **r=128**, **α=256**; achieves **comparable** performance to full finetuning on **6 benchmarks**.

</details>

### 📄 PEFT A2Z — PEFT taxonomy + core fine-tuning equations
**Paper** · [source](https://arxiv.org/html/2504.14117)

*Broad PEFT survey spanning LLMs/VLMs; taxonomy + mechanisms (LoRA, adapters, prefix/prompt, BitFit) and efficiency motivations.*

<details>
<summary>Key content</summary>

- **Scaled dot-product attention (Eq. 2, Sec. 3.1):**  
  Given token embeddings \(X\), projections \(Q=XW_Q,\ K=XW_K,\ V=XW_V\) (Eq. 1).  
  \[
  \text{Attn}(Q,K,V)=\text{softmax}\!\left(\frac{QK^\top}{\sqrt{d_k}}\right)V
  \]
  where \(d_k\) is key/query head dimension; scaling stabilizes softmax.
- **Multi-head attention (Sec. 3.3):** per-head attention computed independently then concatenated and projected:  
  \[
  \text{MHA}(X)=\text{Concat}(\text{head}_1,\dots,\text{head}_h)W_O
  \]
- **FFN (Sec. 3.4):** position-wise two-layer MLP: \( \text{FFN}(x)=\sigma(xW_1+b_1)W_2+b_2\).
- **Full fine-tuning objective (Eq. 12, Sec. 3.6):**  
  \[
  \theta^\*=\arg\min_\theta \sum_{(x,y)\in D}\mathcal{L}(f_\theta(x),y)
  \]
  **Gradient update (Eq. 13):** \(\theta_{t+1}=\theta_t-\eta\nabla_\theta \mathcal{L}\), learning rate \(\eta\).
- **LM pretraining losses (Sec. 3.5):** MLM loss (Eq. 10) predicts masked token \(x_i\) from \(x_{\setminus i}\); AR loss (Eq. 11) predicts \(x_i\) from prefix \(x_{<i}\).
- **Design rationale for PEFT (Intro/Sec. 3.7):** full FT updates all parameters → high memory for parameters+gradients+optimizer states; prone to overfitting on small data + catastrophic forgetting; PEFT updates a small structured subset (e.g., adapters/LoRA/BitFit/prefix/prompt) to reduce compute/storage and act as implicit regularization.
- **Taxonomy (Sec. 5):** five families—**additive**, **selective**, **reparameterized**, **hybrid**, **MoE-based/unified**—to compare trade-offs (efficiency vs. performance vs. complexity).
- **Efficiency procedures (Sec. 4):** precision-aware quantization (e.g., 2/4-bit for less critical params; 8/16-bit for sensitive layers), activation checkpointing, gradient offloading, reversible fine-tuning, KV-cache optimization (hierarchical storage; entropy-based pruning), structured pruning (layer-wise adapter pruning; channel-wise LoRA pruning).

</details>

### 📄 QLoRA core procedure + key numbers
**Paper** · [source](https://proceedings.neurips.cc/paper_files/paper/2023/file/1feb87871436031bdc0f2beaa62a049b-Paper-Conference.pdf)

*Core QLoRA procedure (NF4 + double quantization + paged optimizers), key equations, and benchmark tradeoffs (quality vs memory)*

<details>
<summary>Key content</summary>

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

</details>

### 📄 S-LoRA multi-tenant LoRA serving (Unified Paging + heterogeneous batching)
**Paper** · [source](https://arxiv.org/pdf/2311.03285.pdf)

*System design + empirical scaling claims for serving thousands of concurrent LoRA adapters (memory pool, batching, kernels, multi-GPU TP).*

<details>
<summary>Key content</summary>

- **LoRA math (Section 2, Eq. 1–2):** For pretrained weight matrix \(W\), LoRA adds update \(\Delta W = BA\) where \(B\in\mathbb{R}^{d\times r}\), \(A\in\mathbb{R}^{r\times k}\), rank \(r\). Base forward \(h = xW\). With LoRA: \(h = xW + xBA\) (compute on-the-fly rather than merging for multi-adapter serving).
- **Design rationale (Section 4):** Merging adapters into base weights eliminates per-request overhead for *one* adapter, but for *many* adapters it causes weight duplication or serial adapter swapping → missed batching + GPU underutilization. S-LoRA separates batchable base-model compute from per-request LoRA compute and batches LoRA via custom kernels (avoid padding inefficiency from heterogeneous ranks/seq lengths).
- **Unified Paging (Section 5.1):** Extends vLLM PagedAttention to a **unified GPU memory pool** jointly managing **KV cache** and **adapter weights** to reduce fragmentation. Pool is a large static buffer using GPU space not occupied by base weights/temporary activations. Storage is paged; **each page is a vector of length \(h\)** (hidden size). KV cache with seq len \(s\) uses \(s\) pages; LoRA weight with rank \(r\) uses \(r\) pages; KV + adapters interleaved, non-contiguous.
- **Prefetching (Section 5.2):** Predict adapters needed for next decoding batch from waiting queue; prefetch to overlap I/O with compute.
- **Custom kernels (Section 5.3):** MBGMM (prefill, matrix-matrix) in Triton; MBGMV (decode, matrix-vector) implemented via modified Punica kernels to support non-contiguous memory + multiple ranks.
- **Multi-GPU TP (Section 6):** Align LoRA partitions with Megatron-LM TP; schedule comms on small LoRA intermediates and fuse with base-model comms. Base comm cost: one all-reduce \(O(th)\). Added LoRA comm: \(O(tr)\) (3 all-gathers for Q/K/V + 1 all-reduce for output), negligible since \(r\ll h\). No replicated weights (partitioned across devices).
- **Empirical results (Section 7.2, Table 3):**
  - S-LoRA serves **2,000 adapters** simultaneously with stable throughput once adapters ≥ ~100 (active adapters per batch bounded by GPU mem).
  - **vLLM-packed** (merged copies) can serve **<5 adapters** before OOM.
  - Throughput: up to **4×** higher than vLLM-packed (small adapter counts) and up to **30×** higher than HuggingFace PEFT; “several orders of magnitude” more adapters than naive vLLM LoRA support.
- **Eval defaults (Section 7.1–7.2):** Models: Llama-7B/13B/30B/70B. Example adapter ranks: S1 {8}; S2 {64,32,16,8}; S4 {64,32,16}; S5 {32}; S6 {64}. Hardware: A10G 24GB; A100 40/80GB; host RAM 64–670GB. SLO attainment metric: % requests with **first token ≤ 6s**. Synthetic trace: total rate \(\lambda\) req/s; input/output lengths uniform **[8,512]** tokens.

</details>

### 📄 UniPELT adapters + Prompt Tuning on RoBERTa (parameter counts & benchmark deltas)
**Paper** · [source](https://arxiv.org/html/2405.05493)

*Concrete PEFT adapter comparisons (UniPELT variants), trainable-parameter budgets, and benchmark tables (GLUE/domain/SQuAD)*

<details>
<summary>Key content</summary>

- **Design rationale**
  - Goal: match DAPT/TAPT or full fine-tuning performance while training far fewer parameters (keep most pretrained weights frozen).
  - Uses **UniPELT** (unifies **LoRA + Prefix Tuning + SeqBn/bottleneck adapters** with **gating** to regulate submodule activation); explores stacking and swapping submodules.
  - Adds **Prompt Tuning (PT)** on top of UniPELT to test whether stacking adapters improves feature capture with minimal parameter increase.
- **Mechanism detail (IA3 vs LoRA)**
  - **IA3**: “three learned vectors” rescale **keys and values** in attention layers (vector scaling) vs **LoRA**’s decomposed low-rank matrices.
- **Training procedure / defaults**
  - Model: **RoBERTa-Base**.
  - Batch size **16**, input length **128**, dropout **0.1**, epochs **50** with **early stopping patience=10** (SQuAD: omit early stopping).
  - Loss: **Cross-Entropy** for classification.
  - Learning rates tuned: **2e-4** and **5e-4** (reported best).
  - Tooling: **Adapters** library + Hugging Face Transformers.
- **Empirical results (GLUE avg + key tasks)**
  - Fine-tuning avg **86.35** vs UniPELT (Adapter Lib) **85.15**; PT+UniPELT (Adapter Lib) **85.66**.
  - Best per-task examples: CoLA **66.14** (PT+UniPELT Adapter Lib), MRPC **90.90** (PT+UniPELT Adapter Lib), RTE **78.00** (full FT), QNLI **93.12** (PT+UniPELT Paper).
- **Trainable parameter budgets (RoBERTa-base total 124,645,632 = 100%)**
  - UniPELT **11,083,376 (8.892%)**
  - PT+UniPELT **11,091,056 (8.898%)** (negligible +0.006%)
  - IA3+Prefix+SeqBn **10,852,988 (8.707%)**
  - UniPELT Stack-3 **33,250,128 (26.68%)** (≈3× params; not consistently better)
- **Domain tasks (selected deltas)**
  - CS gains with PT+UniPELT: **ACL-ARC 63.0 → 82.10**, **SCIERC 77.3 → 86.81** (small datasets: 1,688 / 3,219).
  - Vocabulary overlap with RoBERTa pretraining: News **54.1%**, Reviews **34.5%**, BioMed **27.3%**, CS **19.2%** (lower overlap → larger adapter benefit).
- **SQuAD 1.1 (QA)**
  - Fine-tuning **F1 94.6 / EM 88.9**
  - UniPELT (Paper) **90.23 / 82.37**
  - PT+UniPELT (Paper) **88.70 / 80.74** (PT hurts vs UniPELT by ~1.5 F1)

</details>

### 📊 PEFT Taxonomy + Method-by-Method Numbers (Adapters, Prompts, BitFit, IA3, LoRA, QLoRA)
**Benchmark** · [source](https://arxiv.org/html/2303.15647v2)

*Taxonomy + comparative breakdown of where PEFT injects/updates params and efficiency tradeoffs.*

<details>
<summary>Key content</summary>

- **PEFT taxonomy (Section 3):**  
  - **Addition-based:** add new modules; train only added params (Adapters, Soft/Prompt/Prefix).  
  - **Selection-based:** tune subset of existing params (BitFit biases; sparse masks; layer subsets).  
  - **Reparametrization-based:** low-rank update parameterization (LoRA, KronA, Intrinsic SAID).  
  - **Hybrid:** combine (e.g., UniPELT = LoRA + Prefix + Adapters with gates).
- **Memory rationale (Section 3.1 “Why add parameters?”):** with **Adam**, per byte of trainable parameter: **+1 byte gradient +2 bytes optimizer moments**; overall training often **12–20×** model-weight memory. Freezing most weights saves optimizer/grad memory; can also quantize frozen weights.
- **LoRA update (Section 9.2):** for weight matrix \(W\), learn low-rank update  
  \(\Delta W = B A\) (rank \(r\)); effective weight \(W' = W + \alpha/r \cdot BA\). Train only \(A,B\); merge after training by adding \(\Delta W\) into \(W\). Typically applied to attention projections (often \(Q,V\)); best performance when applied to **all** weight matrices (cites Dettmers et al. 2023).
- **(IA)³ (Section 7.2):** learn vectors that **rescale** activations: key, value, and FFN hidden activations; minimal inference overhead (can fold scaling into linear layers; only one vector remains as overhead).
- **Key empirical parameter ranges (Table 2 excerpt):**  
  - **Adapters:** **0.1–6%** trainable.  
  - **BitFit:** **0.05–0.1%** trainable; underperforms on >1B models; note **bias-less** architectures (T5 mostly no biases; LLaMA none).  
  - **Prompt tuning:** **0.1%**; inference overhead from longer sequence.  
  - **Prefix-tuning:** **0.1–4%**.  
  - **LoRA:** **0.01–0.5% trainable**, but **~30% “changed parameters”** (update affects many weights when merged).  
  - **(IA)³:** **0.02%** trainable; reported to beat LoRA with **16×** more trainable params on T0-3B.  
- **QLoRA (Section 9.8):** memory savings via **4-bit NF4 quantization**, **double quantization** (quantize quant constants), and **CPU↔GPU paging** for optimizer-state spikes.

</details>

### 📖 bitsandbytes 4-bit Linear Layers (QLoRA)
**Reference Doc** · [source](https://github.com/bitsandbytes-foundation/bitsandbytes/blob/main/docs/source/reference/nn/linear4bit.mdx)

*Exact API surface for bitsandbytes 4-bit layers used in QLoRA-style finetuning: `Linear4bit`, `LinearFP4`, `LinearNF4`, and `Params4bit` (all via autodoc of their `__init__`).*

<details>
<summary>Key content</summary>

- **QLoRA procedure (high-level workflow):**  
  1) **Quantize** a pretrained model’s weights to **4-bit**.  
  2) **Add LoRA** (low-rank adaptation) weights.  
  3) **Finetune LoRA parameters** “through the quantized weights” (i.e., base weights remain quantized while adapters are trained).  
  *(Section: “4-bit quantization”)*

- **4-bit layer/data-type options (design rationale):**
  - Introduces **two 4-bit quantization data types** for linear layers:  
    - **Float4** via `LinearFP4` (“standard Float4 data type”).  
    - **NormalFloat 4-bit** via `LinearNF4` (“4-bit NormalFloat”).  
  - **Rationale for NF4:** `LinearNF4` is “a quantization data type for **normally distributed data**” and **can improve performance** vs standard Float4.  
  *(Section: “4-bit quantization”)*

- **API entry points (consult autodoc for exact parameters/defaults):**
  - `bitsandbytes.nn.Linear4bit.__init__`
  - `bitsandbytes.nn.LinearFP4.__init__`
  - `bitsandbytes.nn.LinearNF4.__init__`
  - `bitsandbytes.nn.Params4bit.__init__`
  *(Sections: Linear4bit / LinearFP4 / LinearNF4 / Params4bit)*

</details>

### 🔍 S-LoRA serving thousands of concurrent LoRA adapters
**Explainer** · [source](https://lmsys.org/blog/2023-11-15-slora/)

*Step-by-step operational explanation of S-LoRA’s serving approach (adapter storage/loading, routing, batching strategy)*

<details>
<summary>Key content</summary>

- **LoRA equations (Section “Low-Rank Adaptation”)**
  - For base weight \(W\in\mathbb{R}^{h\times d}\): **Eq.(1)** \(W' = W + AB\), where \(A\in\mathbb{R}^{h\times r}\), \(B\in\mathbb{R}^{r\times d}\), rank \(r \ll \min(h,d)\).
  - If base forward is \(h=xW\), then with LoRA: **Eq.(2)** \(h=xW' = x(W+AB)=xW + xAB\).
  - Rationale: merging adapters into \(W\) is fast for **one** adapter, but switching/merge per batch causes GPU under-utilization and throughput collapse with **>2 adapters**; separating base compute (batchable) from per-adapter LoRA compute scales better.
- **Unified Paging memory design (Section “Reserved Memory v.s. Unified Memory”)**
  - Avoid fixed “reserved adapter memory” because it (1) wastes memory when adapters < reserved (reduces KV cache → smaller batch size → lower throughput) and (2) caps active adapters (hurts continuous batching).
  - Put **KV cache + adapter weights** into **one paged pool** (extends vLLM paged KV cache).
  - KV cache per layer tensor shape \((S,H)\) (sequence length \(S\)); LoRA weights shape \((R,H)\) (rank \(R\)); choose **page size = \(H\)** to reduce fragmentation (common factor).
- **Non-contiguous layout → custom kernels (Section “Non-contiguous Memory Layout”)**
  - Interleaved, non-contiguous KV/adapter pages break standard contiguous ops (PyTorch/xFormers/CUTLASS grouped GEMM assumptions).
  - Prefill: Triton tiled kernel gathers adapter weights of varying ranks from pool.
  - Decode: modified Punica BGMV kernel supports **multiple ranks in a batch** + fine-grained gathers aligned to pool.
- **Multi-GPU scaling: S-LoRA TP (Section “Tensor Parallelism”)**
  - Align LoRA partitioning with Megatron-LM TP; minimize comms by avoiding unnecessary comms and fusing some comms; overhead from LoRA comms is “small” vs compute; scaling from **2→4 GPUs** yields **>2× throughput** (memory-bound, superlinear).
- **Empirical throughput (A100 80GB, Table “Throughput”)**
  - **S1 (Llama-7B, rank {8})**: \(n=5\) adapters **8.05 req/s** (vLLM-packed 2.04, PEFT 0.88); \(n=100\) **7.99** (vLLM-packed OOM, PEFT 0.25); \(n=2000\) **7.61**.
  - **S2 (Llama-7B, ranks {64,32,16,8})**: \(n=5\) **7.48**; \(n=2000\) **6.71** (vLLM-packed OOM at 100).
  - **S4 (Llama-13B, ranks {64,32,16})**: \(n=2\) **4.49** (vLLM-packed 3.83, PEFT 0.54); \(n=1000\) **3.96**.
  - Claim: serves **2,000 adapters** with minimal overhead; up to **4×** throughput vs vLLM-packed (small \(n\)), up to **30×** vs PEFT.

</details>

---

## Related Topics

- [[topics/pre-training|Pre-Training]]
- [[topics/domain-adaptation|Domain Adaptation]]
- [[topics/inference-optimization|Inference Optimization]]
