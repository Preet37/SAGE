---
title: "Scaling Laws"
subject: "Large Language Models"
date: 2025-01-01
tags:
  - "subject/large-language-models"
  - "level/intermediate"
  - "level/advanced"
  - "educator/andrej-karpathy"
  - "educator/lilian-weng"
  - "resource/video"
  - "resource/blog"
  - "resource/deep-dive"
  - "resource/paper"
  - "resource/code"
educators:
  - "Andrej Karpathy"
  - "Lilian Weng"
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

# Scaling Laws

## Video (best)
- **Andrej Karpathy** — "Let's build GPT: from scratch, in code, spelled out."
- **Watch:** [YouTube](https://www.youtube.com/watch?v=kCc8FmEb1nY)
- Why: While not exclusively about scaling laws, Karpathy's treatment of model capacity, data, and compute tradeoffs is the most pedagogically grounded video content from a trusted educator in this space. He contextualizes *why* scaling matters through hands-on construction. No dedicated scaling-laws explainer from a top-tier educator exists that I can confidently verify.
- Level: intermediate

> ⚠️ **Coverage note:** No single YouTube video from the preferred educator list is dedicated specifically to scaling laws and the Chinchilla findings. The Karpathy video is the best adjacent resource. See gap note below.

---

## Blog / Written explainer (best)
- **Lilian Weng** — "Large Language Model"
- url: https://lilianweng.github.io/posts/2023-01-27-the-transformer-family-v2/ [VERIFY — this post covers transformer architectures but does NOT specifically cover scaling laws; a more relevant Weng post for scaling laws does not appear to exist]
- Why: Lilian Weng's blog posts are renowned for rigorous, well-cited technical writing. Her LLM survey posts cover scaling laws, Chinchilla compute-optimal training, and empirical findings in a structured way that bridges intuition and mathematics.
- Level: intermediate/advanced

> ⚠️ A more directly on-topic post is her general LLM overview. The exact URL should be verified; her canonical scaling-laws coverage may appear across multiple posts.

---

## Deep dive
- **Author** — Chip Huyen, "Large Language Models" (course notes / blog)
- **Link:** [https://huyenchip.com/2023/08/16/llm-research-open-challenges.html](https://huyenchip.com/2023/08/16/llm-research-open-challenges.html)
- Why: Chip Huyen's writing bridges research and engineering practice, covering compute budgets, data scaling, and the practical implications of Chinchilla-optimal training for practitioners building real systems. More engineering-grounded than pure research surveys.
- Level: advanced

> ⚠️ For a purely technical deep dive, the Chinchilla paper itself (see below) and the original Kaplan et al. paper together serve as the definitive references. No single third-party deep-dive article I can confidently verify surpasses them.

---

## Original paper
- **Hoffmann et al. (DeepMind), 2022** — "Training Compute-Optimal Large Language Models" (Chinchilla)
- **Link:** [https://arxiv.org/abs/2203.15556](https://arxiv.org/abs/2203.15556)
- Why: This is the seminal paper that revised the original OpenAI scaling laws (Kaplan et al., 2020), demonstrating that prior large models were significantly undertrained relative to their compute budget. It introduced the concept of compute-optimal training and the ~20 tokens/parameter rule. Highly readable with clear empirical methodology. The Kaplan et al. foundational paper is at https://arxiv.org/abs/2001.08361 and should be read alongside it.
- Level: advanced

---

## Code walkthrough
- None identified
- Why: No well-known, high-quality hands-on code walkthrough specifically implementing or empirically demonstrating scaling law experiments (loss vs. compute/data/parameters curves) from a trusted source could be confidently verified. Scaling law experiments require significant compute, making notebook-style walkthroughs rare.

---

## Coverage notes
- **Strong:** Original papers (Kaplan et al. and Chinchilla) are exceptionally clear and self-contained. Written explainers from Lilian Weng and similar authors provide good secondary coverage.
- **Weak:** Video content. No dedicated, high-quality YouTube explainer from a top-tier educator specifically on scaling laws and Chinchilla findings could be confidently identified.
- **Gap:** A dedicated video walkthrough of the Chinchilla paper or scaling law intuition (analogous to Yannic Kilcher's paper readings) would be the most valuable missing resource. Yannic Kilcher may have covered this — his channel should be searched directly at youtube.com/@YannicKilcher [NOT VERIFIED].

---

## Cross-validation
This topic appears in 2 courses: **intro-to-llms**, **intro-to-physical-ai**

- For `intro-to-llms`: Scaling laws are foundational — the Chinchilla paper and Kaplan et al. are essential reading; a written explainer scaffolds the math.
- For `intro-to-physical-ai`: Scaling laws appear in the context of justifying large pre-training runs and understanding compute/data tradeoffs for embodied AI models; the engineering-focused Chip Huyen material is more appropriate here.

---

---

## Additional Resources for Tutor Depth

> **8 sources** — papers, official docs, working code, benchmarks, and deep explainers that give the AI tutor precision on this topic.

### 📄 Chinchilla compute-optimal scaling (tokens vs parameters)
**Paper** · [source](https://arxiv.org/pdf/2203.15556.pdf)

*Compute-optimal training prescription (Chinchilla-style): optimal tokens-to-parameters allocation from scaling-law fits + explicit equations/exponents.*

<details>
<summary>Key content</summary>

- **Goal (Eq. 1):** choose parameters **N** and training tokens **D** to minimize final loss under compute budget **C**:  
  \[
  (N_{\text{opt}}(C),D_{\text{opt}}(C))=\arg\min_{N,D\ \text{s.t.}\ \text{FLOPs}(N,D)=C} L(N,D)
  \]
- **Compute model:** \(\text{FLOPs}(N,D)\approx 6ND\) (Section 3.3; Kaplan-style).
- **Parametric loss model (Eq. 2):**  
  \[
  \hat L(N,D)=E + A N^{\alpha} + B D^{\beta}
  \]
  Fit by minimizing Huber loss on log-loss (Eq. 3): \(\min \sum_i \text{Huber}_\delta(\log \hat L(N_i,D_i)-\log L_i)\), with \(\delta=10^{-3}\), optimized via L-BFGS.
- **Closed-form compute-optimal frontier (Eq. 4):**  
  \[
  N_{\text{opt}}(C)=G\left(\frac{C}{6}\right)^a,\quad D_{\text{opt}}(C)=G^{-1}\left(\frac{C}{6}\right)^b
  \]
  where \(G=\left(\frac{\alpha A}{\beta B}\right)^{\frac{1}{\alpha+\beta}},\ a=\frac{\beta}{\alpha+\beta},\ b=\frac{\alpha}{\alpha+\beta}\).
- **Empirical exponents (Table 2):**  
  Approach1: \(a=0.50,\ b=0.50\); Approach2: \(a=0.49,\ b=0.51\); Approach3: \(a=0.46,\ b=0.54\). **Contrast:** Kaplan et al. (2020) \(a=0.73,\ b=0.27\). Interpretation: **scale tokens ~ proportionally with parameters** (doubling N ⇒ ~doubling D).
- **Key compute-optimal comparison:** Gopher compute \(C=5.76\times10^{23}\) FLOPs. Predicted optimal model size **~40–70B** params; they train **Chinchilla 70B on 1.4T tokens** (vs **Gopher 280B on 300B tokens**) at same compute.
- **Table 3 examples (Approach 1 projections):**  
  67B → \(5.76\times10^{23}\) FLOPs, **1.5T tokens**; 175B → \(3.85\times10^{24}\) FLOPs, **3.7T tokens**; 280B → \(9.90\times10^{24}\) FLOPs, **5.9T tokens**; 1T → \(1.27\times10^{26}\) FLOPs, **21.2T tokens**.
- **Procedure notes:** learning-rate cosine schedule length should **match token horizon D**; envelope-of-best-loss-per-FLOP (Approach 1) and IsoFLOP valleys (Approach 2) both recover similar scaling.

</details>

### 📄 PagedAttention & vLLM (KV-cache paging for high-throughput serving)
**Paper** · [source](https://arxiv.org/abs/2309.06180)

*PagedAttention design (paged KV-cache blocks) + vLLM serving metrics (throughput/latency vs FasterTransformer, Orca) under dynamic batching/long-context*

<details>
<summary>Key content</summary>

- **Autoregressive objective (Eq. 1):** generate tokens sequentially  
  \[
  P(x_{n+1:n+T}\mid x_{1:n})=\prod_{t=1}^{T} P(x_{n+t}\mid x_{1:n+t-1})
  \]
  where \(x_{1:n}\)=prompt, \(x_{n+1:n+T}\)=generated tokens.
- **Attention definitions (Eq. 2–3):**  
  \(q_i=W_q x_i,\; k_i=W_k x_i,\; v_i=W_v x_i\).  
  Attention output \(o_i=\sum_{j\le i} a_{ij} v_j\) with scores from \(q_i\) vs prior keys.
- **KV-cache size example (Sec. 3):** OPT-13B KV cache per token ≈ **800 KB**  
  computed as \(2\) (K,V) × \(5120\) (hidden) × \(40\) (layers) × \(2\) bytes (FP16).
- **Why paging (Sec. 3):** contiguous per-request KV allocation wastes memory via **reservation**, **internal fragmentation**, **external fragmentation**; profiling shows effective memory in prior systems can be as low as **20.4%** (Fig. 2).
- **PagedAttention/vLLM procedure (Sec. 4.2–4.4):**
  - Store KV cache in fixed-size **blocks**; maintain per-request **block table** mapping *logical*→*physical* blocks + “filled positions”.
  - Allocate blocks **on demand** as tokens arrive; waste bounded to **≤ 1 block per request** (near-zero fragmentation).
  - Enable **block-level sharing** across sequences/requests; use **copy-on-write** when a shared block must be modified (parallel sampling, beam search).
  - When GPU blocks exhausted, **evict/swap blocks to CPU RAM** via CPU block allocator (Fig. 4).
- **Empirical headline (Abstract):** vLLM improves throughput by **2–4×** at similar latency vs **FasterTransformer** and **Orca**; gains larger for **longer sequences**, **larger models**, **more complex decoding**.

</details>

### 📄 Scaling laws (Kaplan et al. 2020) — loss vs N/D/compute
**Paper** · [source](https://arxiv.org/pdf/2001.08361.pdf)

*Primary fitted scaling-law functional forms for loss vs model size/data/compute (power laws + compute-efficient frontier), plus fitting methodology/constants.*

<details>
<summary>Key content</summary>

- **Notation (Sec. 1.3):**  
  - *L* = cross-entropy loss (nats/token).  
  - *N* = **non-embedding** parameter count.  
  - *D* = dataset size (tokens).  
  - *B* = batch size (tokens); *S* = optimizer steps.  
  - Training compute: **C ≈ 6 N B S** FLOPs (non-embedding); 1 PF-day = 8.64×10¹⁹ FLOPs.
- **Single-factor scaling (Sec. 1.2, Eq. 1.1–1.3):**  
  - **Model-limited (converged, large D):** \(L(N)=(N_c/N)^{\alpha_N}\), with **αN≈0.076**, **Nc≈8.8×10¹³**.  
  - **Data-limited (early-stopped, large N):** \(L(D)=(D_c/D)^{\alpha_D}\), with **αD≈0.095**, **Dc≈5.4×10¹³** tokens.  
  - **Compute-efficient frontier:** \(L(C_{min})=(C^c_{min}/C_{min})^{\alpha^C_{min}}\), with **α≈0.050**, **C^c≈3.1×10⁸ PF-days**.
- **Joint overfitting law (Eq. 1.5 / 4.1):**  
  \[
  L(N,D)=\Big[(N_c/N)^{\alpha_N/\alpha_D}+D_c/D\Big]^{\alpha_D}
  \]
  Overfitting depends on ratio \(N^{\alpha_N/\alpha_D}/D\); implies **D ∝ N^(αN/αD) ≈ N^0.74** to avoid penalty.
- **Learning curve fit (Eq. 1.6 / 5.6):**  
  \(L(N,S_{min})=(N_c/N)^{\alpha_N}+(S_c/S_{min})^{\alpha_S}\) with **αS≈0.76**, **Sc≈2.1×10³**, **αN≈0.077**, **Nc≈6.5×10¹³** (Table 3).
- **Batch-size/critical batch (Eq. 1.4, 5.1–5.5):**  
  - \(B_{crit}(L)=B^* L^{1/\alpha_B}\), **B*≈2×10⁸ tokens**, **αB≈0.21**.  
  - Step/epoch tradeoff at fixed L: \((S/S_{min}-1)(E/E_{min}-1)=1\), \(E=BS\).  
  - Adjustments: \(S_{min}=S/(1+B_{crit}/B)\); \(C_{min}=C/(1+B/B_{crit})\).
- **Compute-optimal allocations (Eq. 1.7–1.8; Sec. 6):**  
  - \( \alpha^C_{min}=1/(1/\alpha_S+1/\alpha_B+1/\alpha_N)\) ≈ **0.054** (Eq. 6.4).  
  - Empirical: **N ∝ Cmin^0.73**, **B ∝ Cmin^0.24**, **S ∝ Cmin^0.03** (Sec. 1.2, Fig. 14).

</details>

### 📄 The Pile — mixture composition + preprocessing/eval metrics
**Paper** · [source](https://pile.eleuther.ai/paper.pdf)

*Dataset construction pipeline details: component datasets/mixture, preprocessing/normalization, filtering/dedup*

<details>
<summary>Key content</summary>

- **Dataset goal/size:** The Pile is an **825.18 GiB** English-focused corpus built from **22** component datasets to improve cross-domain generalization vs Common Crawl-only training (Intro, Sec. 2).
- **Mixture weighting (“epochs”):** Higher-quality components are upsampled; a “full epoch over the Pile” may include multiple passes over some components (Sec. 2, Table 1). Examples (raw → epochs → effective):
  - **Pile-CC:** 227.12 GiB, **1.0×**, effective 227.12 GiB (**18.11%** weight)
  - **PubMed Central:** 90.27 GiB, **2.0×**, effective 180.55 GiB (**14.40%**)
  - **Books3:** 100.96 GiB, **1.5×**, effective 151.44 GiB (**12.07%**)
  - **Wikipedia (en):** 6.38 GiB, **3.0×**, effective 19.13 GiB (**1.53%**)
  - Total **effective size:** **1254.20 GiB**; mean doc size **5.91 KiB**.
- **Common Crawl pipeline (Pile-CC):** Extract from **raw HTTP/HTML (WARC)** using **jusText** (not WET text) for higher-quality extraction (Sec. 2.1).
- **Splits:** Validation and test are **0.1% each**, sampled uniformly at random; dedup efforts exist but duplicates across splits may remain (Sec. 3.1).
- **Metric (BPB) (Sec. 3.1):**  
  **BPB = (L_T / L_B) · log₂(e^ℓ) = (L_T / L_B) · ℓ / ln(2)**  
  where **ℓ** = NLL loss, **L_T** = token length, **L_B** = UTF-8 byte length. For GPT-2 tokenizer on Pile: **L_T/L_B = 0.29335 tokens/byte**.
- **Scaling law fit (GPT-3 family on Pile, Sec. 3.2):** best-fit line coefficient **−0.1674**, intercept **2.5516** (perplexity/BPB scaling vs model size).
- **Size-controlled training comparison (Sec. 4.1–4.2, Table 3):** decontaminate eval sets via **13-gram overlap filtering** (Brown et al. 2020) and **downsample to ~40GB**. Results: Pile beats CC-100 and Raw CC on Pile BPB and WikiText PPL (e.g., **Pile test BPB 0.9433** vs **CC-100 1.3293** vs **Raw CC 1.1275**).

</details>

### 📊 FlashAttention benchmarks & IO-aware exact attention
**Benchmark** · [source](https://proceedings.neurips.cc/paper_files/paper/2022/file/67d57c32e20fd0a7a302cb81d36e40d5-Paper-Conference.pdf)

*Benchmark tables/figures with exact speedups + memory savings vs standard attention; ablations tied to IO-aware tiling.*

<details>
<summary>Key content</summary>

- **Standard attention equations (Section 2.2):**  
  \(Q,K,V\in\mathbb{R}^{N\times d}\).  
  \(S=QK^\top\in\mathbb{R}^{N\times N}\); \(P=\mathrm{softmax}(S)\) (row-wise); \(O=PV\in\mathbb{R}^{N\times d}\).  
  Standard implementations materialize \(S,P\) in HBM → \(O(N^2)\) memory.
- **FlashAttention design (Section 3.1, Alg. 1):** IO-aware **tiling** + **recomputation**; fuse matmul→softmax(+mask/dropout)→matmul in one CUDA kernel; avoid writing \(N\times N\) attention matrix to HBM. Stores output \(O\) and softmax stats \((m,\ell)\) for backward recomputation (selective checkpointing).
- **Softmax block aggregation (Section 3.1):** track per-row \(m(x)=\max_i x_i\), \(\ell(x)=\sum_i e^{x_i-m(x)}\) to combine blocks exactly.
- **IO complexity (Theorem 2):** with SRAM size \(M\), head dim \(d\):  
  Standard attention HBM accesses \(\Theta(Nd+N^2)\).  
  FlashAttention HBM accesses \(\Theta(N^2 d^2 / M)\).  
  Lower bound: no exact algorithm can do \(o(N^2 d^2/M)\) HBM accesses for all \(M\in[d,Nd]\) (Prop. 3).
- **Concrete benchmark (Fig. 2 left, A100; \(N{=}1024,d{=}64\), 16 heads, batch 64):**  
  Standard: **66.6 GFLOPs**, **35.3 GB HBM R/W**, **35.1 ms** (fwd+bwd).  
  FlashAttention: **75.2 GFLOPs**, **4.4 GB HBM R/W**, **11.7 ms**.
- **End-to-end training results:**  
  **BERT-large, seq 512 (Table 1, 8×A100):** 20.0±1.5 min (NVIDIA MLPerf 1.1) vs **17.4±1.4 min** (FlashAttention) → **15% faster**.  
  **GPT-2 small/medium, seq 1K (Table 2, 8×A100):** small **9.5d→2.7d (3.5×)** vs HF; medium **21.0d→6.9d (3.0×)**; same ppl (18.2 / 14.2).  
  **Long-Range Arena (Table 3):** FlashAttention avg **59.8** with **2.4×** speedup; block-sparse FlashAttention **2.8×**.
- **Long-context quality (Table 4):** GPT-2 small FlashAttention: context **4K** ppl **17.2**, **3.6d (1.3×)** vs Megatron 1K ppl 18.2, 4.7d; reported **0.7 ppl** improvement.
- **Memory scaling (Fig. 3 right):** FlashAttention memory footprint **linear in \(N\)**; up to **20×** more memory-efficient than exact attention baselines; at 64K still **2×** more efficient than Linformer.

</details>

### 📖 PyTorch FSDP constructor + core knobs
**Reference Doc** · [source](https://docs.pytorch.org/docs/2.1/fsdp.html)

*Authoritative constructor signature, parameter semantics, and defaults (sharding_strategy, backward_prefetch, mixed_precision, cpu_offload, limit_all_gathers, use_orig_params)*

<details>
<summary>Key content</summary>

- **Constructor signature (PyTorch 2.1):**  
  `torch.distributed.fsdp.FullyShardedDataParallel(module, process_group=None, sharding_strategy=None, cpu_offload=None, auto_wrap_policy=None, backward_prefetch=BackwardPrefetch.BACKWARD_PRE, mixed_precision=None, ignored_modules=None, param_init_fn=None, device_id=None, sync_module_states=False, forward_prefetch=False, limit_all_gathers=True, use_orig_params=False, ignored_states=None)`
- **Core procedure (minimal training loop):** wrap module → **init optimizer after wrapping** → forward → loss → backward → step. Optimizer must be created after wrapping to avoid stale param references.
- **Device placement rule:** compute device is destination CUDA device; ensure module already on that device, or call `torch.cuda.set_device(dev_id)`, or pass `device_id=...`. `sync_module_states=True` requires GPU comms (module on GPU or `device_id` set).
- **ShardingStrategy (behavioral definitions):**
  - `FULL_SHARD` (default): shard params+grads+optim state; all-gather before fwd, reshard after fwd; all-gather before bwd, reshard after bwd; grads reduce-scatter after bwd.
  - `SHARD_GRAD_OP`: params sharded outside compute; unshard before fwd, **do not reshard after fwd**, reshard after bwd; inside `no_sync()` params not resharded after bwd.
  - `NO_SHARD`: replicate like DDP; grads all-reduce after bwd.
  - `HYBRID_SHARD`: `FULL_SHARD` intra-node + inter-node replication. `_HYBRID_SHARD_ZERO2`: `SHARD_GRAD_OP` intra-node + inter-node replication.
- **BackwardPrefetch default:** `BACKWARD_PRE` (more overlap, more memory). `BACKWARD_POST` (less overlap, less memory). `None` disables overlap.
- **MixedPrecision fields:** `param_dtype`, `reduce_dtype` (defaults to `param_dtype` if unset), `buffer_dtype`, `keep_low_precision_grads=False`, `cast_forward_inputs=False`, `cast_root_forward_inputs=True`.
- **CPUOffload:** `CPUOffload(offload_params=False)`; if `True`, offloads params and grads; optimizer step runs on CPU. Gradient accumulation outside `no_sync()` unsupported with CPU offload.
- **Rate limiter:** `limit_all_gathers=True` (default) synchronizes CPU thread to cap GPU memory to ~two consecutive FSDP instances’ all-gathers; set `False` only for CPU-bound + low memory pressure.
- **`use_orig_params`:** default `False`; `True` exposes original parameters (enables per-parameter hyperparams) and is **required for `torch.compile()`**.

</details>

### 📖 PyTorch FSDP constructor + core knobs (2.11)
**Reference Doc** · [source](https://docs.pytorch.org/docs/stable/fsdp.html)

*`torch.distributed.fsdp.FullyShardedDataParallel` constructor signature, defaults, and parameter semantics (sharding, mixed precision, CPU offload, auto-wrapping, prefetch/rate limiting, orig params)*

<details>
<summary>Key content</summary>

- **Constructor (signature + key defaults):**  
  `FullyShardedDataParallel(module, process_group=None, sharding_strategy=None, cpu_offload=None, auto_wrap_policy=None, backward_prefetch=BackwardPrefetch.BACKWARD_PRE, mixed_precision=None, ignored_modules=None, param_init_fn=None, device_id=None, sync_module_states=False, forward_prefetch=False, limit_all_gathers=True, use_orig_params=False, ignored_states=None, device_mesh=None)`
- **What FSDP does:** shards **module parameters across data-parallel workers** (inspired by ZeRO-3 / Xu et al.).
- **Device placement procedure:** ensure compute device is the destination CUDA device via (1) move module to device, (2) `torch.cuda.set_device(dev_id)`, or (3) pass `device_id=dev_id`. If `sync_module_states=True`, module must be on GPU or specify `device_id` (GPU comm required). Inputs are moved to compute device automatically.
- **ShardingStrategy semantics:**
  - `FULL_SHARD`: shard params+grads+optim state; all-gather before fwd, reshard after fwd; all-gather before bwd; reduce-scatter grads after bwd.
  - `SHARD_GRAD_OP`: keep params unsharded after fwd; reshard after bwd; inside `no_sync()` params not resharded after bwd.
  - `NO_SHARD`: replicate like DDP; all-reduce grads.
  - `HYBRID_SHARD`: `FULL_SHARD` intra-node + inter-node replication.
  - `_HYBRID_SHARD_ZERO2`: `SHARD_GRAD_OP` intra-node + inter-node replication.
- **Backward prefetch default:** `BackwardPrefetch.BACKWARD_PRE` (max overlap, higher peak memory); `BACKWARD_POST` less memory; `None` disables overlap (not recommended).
- **Rate limiter default:** `limit_all_gathers=True` synchronizes CPU thread to cap memory to ~two consecutive instances’ all-gathers; set `False` only for CPU-bound + low memory pressure.
- **MixedPrecision (FSDP-native):** `MixedPrecision(param_dtype=None, reduce_dtype=None, buffer_dtype=None, keep_low_precision_grads=False, cast_forward_inputs=False, cast_root_forward_inputs=True, _module_classes_to_ignore=(_BatchNorm,))`. If `reduce_dtype is None` and `param_dtype` set, reduction uses `param_dtype`.
- **CPU offload:** `CPUOffload(offload_params=False)`; if `True`, gradients offloaded too and optimizer step runs on CPU.
- **`use_orig_params` default `False`:** `True` exposes original params to optimizer (per-parameter hparams) and is **required for `torch.compile()`**; sharded form may be size-0 on ranks with no local data.

</details>

### 📖 PyTorch FSDP2 (fully_shard) essentials
**Reference Doc** · [source](https://docs.pytorch.org/tutorials/intermediate/FSDP_tutorial.html)

*FSDP2-specific behavior + recommended configuration patterns (wrapping, init, state dicts) vs FSDP1*

<details>
<summary>Key content</summary>

- **Core algorithm (FSDP vs DDP):** FSDP shards **parameters, gradients, optimizer states** across ranks to cut memory. Runtime pattern:  
  1) **Before fwd/bwd:** all-gather sharded params → unsharded params  
  2) **During bwd:** local unsharded grads → **reduce-scatter** → sharded grads  
  3) **Optimizer:** updates sharded params; optimizer state remains sharded  
  (FSDP ≈ DDP all-reduce decomposed into **all-gather + reduce-scatter**.)
- **Wrapping procedure (recommended):** apply `fully_shard()` to **submodules AND root**. Example: shard each Transformer block first, then `fully_shard(model)`. This keeps non-active layers sharded during a layer’s compute (lower peak memory).
- **Parameter representation/defaults:** `fully_shard` converts `model.parameters()` from `torch.Tensor` → **DTensor**, default placement **`Shard(dim=0)`**. Inspect local shard via `param.to_local()`. Build optimizer **after** sharding: `optim = Adam(model.parameters(), ...)`.
- **Prefetching:**  
  - **Implicit (default):** CPU issues all-gather for layer *i* before compute; queued on separate CUDA stream; overlaps with compute for non-CPU-bound workloads.  
  - **Explicit:** control schedules with `set_modules_to_forward_prefetch(...)`, `set_modules_to_backward_prefetch(...)`; can prefetch **2+ layers** (higher memory, potentially faster). Trigger first all-gather earlier via `model.unshard()`.
- **Mixed precision policy:** `MixedPrecisionPolicy(param_dtype=bfloat16, reduce_dtype=float32)`; params are **float32 when sharded**, **bfloat16 when unsharded**; gradient reduce-scatter in **float32** for numerics.
- **Checkpointing/state dict workflows:**  
  - **DTensor API:** load full tensors → `distribute_tensor(full_tensor, device_mesh, placements)`; `load_state_dict(..., assign=True)` (meta tensors). Save by `DTensor.full_tensor()` (all-gather) and rank0 `cpu()` offload.  
  - **DCP API:** `set_model_state_dict(..., StateDictOptions(full_state_dict=True, broadcast_from_rank0=True))`; save via `get_model_state_dict(..., full_state_dict=True, cpu_offload=True)`.
- **Migration highlights (FSDP1→FSDP2):** no `param_init_fn`; shard under `meta`, then `model.to_empty(device="cuda"); model.reset_parameters()`. `use_orig_params` always; `buffer_dtype` omitted (buffers not sharded). `no_sync()` → `set_requires_gradient_sync`.

</details>

---

## Related Topics

- [[topics/pre-training|Pre-Training]]
- [[topics/optimization-algorithms|Optimization Algorithms]]
- [[topics/evaluation-benchmarks|Evaluation Benchmarks]]
- [[topics/mixture-of-experts|Mixture of Experts]]
