---
title: "Optimization Algorithms"
subject: "Foundational AI"
date: 2025-01-01
tags:
  - "subject/foundational-ai"
  - "level/beginner"
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

# Optimization Algorithms

## Video (best)
- **Andrej Karpathy** — "Let's build micrograd" (covers SGD, momentum, backprop foundations)
- **Watch:** [YouTube](https://www.youtube.com/watch?v=VMj-3S1tku0)
- Why: Karpathy builds a neural network optimizer from scratch, making SGD and gradient-based optimization viscerally concrete. Learners see exactly why momentum helps and how learning rate affects convergence — not just conceptually but in running code. Ideal for the intro-to-llms audience.
- Level: beginner/intermediate

## Blog / Written explainer (best)
- **Sebastian Ruder** — "An overview of gradient descent optimization algorithms"
- **Link:** [https://www.ruder.io/optimizing-gradient-descent/](https://www.ruder.io/optimizing-gradient-descent/)
- Why: This is the canonical written survey of SGD, momentum, RMSProp, Adam, and learning rate schedules in one place. Ruder provides intuitive explanations, mathematical formulations, and visual comparisons. Widely used in university courses precisely because it bridges intuition and rigor without requiring a paper-reading background.
- Level: intermediate

## Deep dive
- **Lilian Weng** — "Learning Rate Schedules and Adaptive Learning Rate Methods"
- url: https://lilianweng.github.io/posts/2022-04-15-data-gen/ — **Note: Weng's optimizer post is at** https://lilianweng.github.io/posts/2023-01-27-the-transformer-family-v2/ — **Correct URL:** https://lilianweng.github.io/lil-log/2019-01-11-meta-learning.html [NOT VERIFIED]
- **Preferred alternative (high confidence):** Lilian Weng's blog at `lilianweng.github.io` covers optimizers; the specific optimizer deep-dive post URL requires verification. Use Sebastian Ruder's PhD thesis overview instead:
- **Link:** [https://arxiv.org/abs/1609.04747](https://arxiv.org/abs/1609.04747)
- Why: Ruder's arxiv survey (the paper form of his blog) is the most comprehensive single technical reference covering all major first-order optimizers, convergence properties, and practical recommendations. It is cited thousands of times and used as a reference in ml-engineering-foundations style courses.
- Level: advanced

## Original paper
- **Diederik Kingma & Jimmy Ba** — "Adam: A Method for Stochastic Optimization"
- **Link:** [https://arxiv.org/abs/1412.6980](https://arxiv.org/abs/1412.6980)
- Why: Adam is the dominant optimizer in modern deep learning and LLM training. This paper is unusually readable for a seminal work — the algorithm is presented in a clear pseudocode box, the motivation from moment estimation is well-explained, and the bias-correction derivation is accessible. Directly relevant to both adam and momentum concepts in the related concepts list.
- Level: intermediate/advanced

## Code walkthrough
- **Andrej Karpathy** — "micrograd" repository / "The spelled-out intro to neural networks and backpropagation"
- youtube_id: VMj-3S1tku0 (same video as above, but the accompanying repo is the code walkthrough)
- **Link:** [https://github.com/karpathy/micrograd](https://github.com/karpathy/micrograd)
- Why: The micrograd repo implements SGD and the backward pass from scratch in ~150 lines of Python. Learners can directly experiment with learning rate, momentum, and see loss curves change. For mixed precision and Adam specifically, the `nanoGPT` repo by the same author shows practical AdamW + bf16 usage in a real LLM context.
- Supplementary code: https://github.com/karpathy/nanoGPT
- Level: beginner→intermediate

---

## Coverage notes
- **Strong:** SGD, momentum, Adam — all three have excellent video, written, and paper resources. The Karpathy + Ruder combination covers these comprehensively.
- **Strong:** Learning rate schedules — Ruder's survey and nanoGPT both demonstrate cosine/warmup schedules in context.
- **Weak:** Mixed precision (bf16, fp16) and tensor/data parallelism — these are engineering-heavy topics that sit at the intersection of optimization and systems. Ruder's survey does not cover them. The best resources shift toward Hugging Face documentation and PyTorch docs rather than pedagogical explainers.
- **Gap:** No single excellent YouTube video exists specifically for **mixed precision training (bf16/fp16)** at an introductory level. The topic is covered in passing in Karpathy's nanoGPT walkthrough but not as a standalone explainer.
- **Gap:** **Tensor parallelism and data parallelism** as optimization-adjacent topics lack a strong standalone pedagogical video. Chip Huyen's blog and the Megatron-LM paper are the best references but are not beginner-friendly.
- **Gap:** **AdamW** (the weight-decay corrected variant used in virtually all LLM training) does not have a dedicated best-in-class video explainer separate from general Adam content.

---

## Cross-validation
This topic appears in 2 courses: **intro-to-llms** and **ml-engineering-foundations**

- For **intro-to-llms**: Prioritize the Karpathy video + Ruder blog. Focus on SGD → Adam progression and intuition for learning rate schedules. The Adam paper is accessible enough to assign.
- For **ml-engineering-foundations**: The Adam paper + nanoGPT codebase are essential. Supplement with PyTorch's official mixed precision tutorial (https://pytorch.org/tutorials/recipes/recipes/amp_recipe.html) for bf16/mixed precision coverage, and the Hugging Face `accelerate` documentation for data parallelism patterns.

---

---

## Additional Resources for Tutor Depth

> **9 sources** — papers, official docs, working code, benchmarks, and deep explainers that give the AI tutor precision on this topic.

### 📄 Megatron-LM Tensor (Intra-layer) Parallelism + Data Parallel Composition
**Paper** · [source](https://arxiv.org/abs/1909.08053)

*Step-by-step tensor model parallelism (partitioned linear layers) + comms (all-reduce/all-gather) + composition with data parallelism*

<details>
<summary>Key content</summary>

- **Tensor model parallelism (intra-layer) for Transformer MLP (Fig. 4/5):**
  - Split first MLP weight **A** (shape \(H \times 4H\)) **column-wise** across \(t\) GPUs → each GPU computes partial \(X A_i\); apply GeLU locally.
  - Split second MLP weight **B** (shape \(4H \times H\)) **row-wise** across \(t\) GPUs so each GPU consumes its local activation shard; outputs are partials that must be **all-reduced** to form the full \(H\)-dim output.
  - Communication pattern: **1 all-reduce in forward** for the MLP block output and **1 all-reduce in backward** (paper notes arranging splits to minimize comm; “two all-reduces in forward path and two in backward path” for a transformer layer when accounting for attention+MLP).
- **Self-attention tensor parallelism (Sec. 3 / Fig. 5):**
  - Partition **Q, K, V** projections column-parallel; output projection row-parallel; output linear can operate on partitioned attention output; requires similar all-reduce synchronization.
- **Embedding / vocab-parallel logits:**
  - Parallelize embedding matrix \(E_{H\times v}\) along vocab (column-wise). Naive all-gather of logits costs \(b \times s \times v\); Megatron **fuses parallel output with cross-entropy** so communication reduces to **\(b \times s\)** (loss scalars) instead of full logits.
- **Compose with data parallelism:**
  - Use tensor model-parallel groups of size \(t\) and data-parallel groups of size \(d\) with \(n=t\cdot d\) (and in 3D setups \(n=p\cdot t\cdot d\)).
- **Communication volume formula (Sec. 3):**
  - Per layer, tensor-parallel all-reduce communicates total size \(\approx 8\,b\,s\,h\) elements (microbatch \(b\), seq \(s\), hidden \(h\)); “twice each in forward and backward.”
- **Empirical scaling/results:**
  - 1.2B params on 1×V100 32GB: **39 TFLOP/s** sustained (~**30%** peak).
  - 8.3B params on **512 GPUs** with **8-way tensor model parallelism**: **15.1 PFLOP/s**, **76%** scaling efficiency vs single-GPU baseline; ~**74%** scaling vs linear at 512 GPUs.
- **Training hyperparams (GPT-2-like):**
  - Mixed precision + **dynamic loss scaling**; init \(W\sim\mathcal{N}(0,0.02)\); scale weights before residual by \(1/\sqrt{2N}\) (N transformer layers).
  - **AdamW**: weight decay \(\lambda=0.01\); LR **1.5e-4**, **3k** warmup iters, **single-cycle cosine decay** over remaining **297k** iters to min LR **1e-5**.

</details>

### 📄 Mixed Precision Training (FP16) + Loss Scaling (Dynamic)
**Paper** · [source](https://arxiv.org/abs/1710.03740)

*Loss scaling procedure (incl. dynamic) + evidence FP16 mixed precision matches FP32 accuracy while improving memory/throughput on NVIDIA GPUs*

<details>
<summary>Key content</summary>

- **FP16 numeric limits (motivation for scaling)**: FP16 max normalized = **65,504**; min normalized = **2^-14 ≈ 6.10e-5**; min denormal = **2^-24 ≈ 5.96e-8**. Normalized exponent range centered at **[-14, 15]**; gradients often have small magnitudes → underflow to 0. (Sec. 3.2)
- **Core mixed-precision design (Sec. 3):**
  - Store **weights/activations/gradients in FP16**, but keep **FP32 master weights** for optimizer updates (prevents updates becoming 0 due to FP16 mantissa/exponent limits; e.g., update can vanish when weight magnitude ≥ **2048×** update magnitude). (Sec. 3.1)
  - Use **FP16 math with FP32 accumulation** for dot-products / GEMMs / convs; convert back to FP16 for storage. (Sec. 3.3)
- **Loss scaling (Sec. 3.2):**
  - Scale loss by **S** before backprop: \(L' = S \cdot L\).
  - Backprop yields scaled grads: \(g' = \partial L'/\partial w = S \cdot g\).
  - **Unscale before update**: \(g = g'/S\) (do this **after backward, before** clipping/weight decay to avoid retuning hyperparams).
  - **Choosing S (constant):** pick S so \(S \cdot \max|g| < 65504\). Empirically used **S ∈ [8, 32K]**; many nets need none.
  - **Dynamic loss scaling:** start with large S; if **Inf/NaN** in weight grads → **reduce S**, **skip update**; if no overflow for **N iterations (e.g., N=2000)** → **increase S**. Example multipliers: **×2 up**, **×0.5 down**.
- **Empirical results (object detection, VOC07 test mAP; Table 2):**
  - Faster R-CNN: **FP32 69.1%**, MP no scaling **68.6%**, MP + scaling **69.7%**.
  - Multibox SSD: **FP32 76.9%**, MP no scaling **does not train**, MP + scaling (**S=8**) **77.1%**.
- **Throughput/memory rationale:** FP16 halves storage/bandwidth; recent GPUs have **2×–8×** higher FP16 throughput; overall training memory ~**2× lower** (activations dominate). (Intro/Abstract)

</details>

### 📊 BFLOAT16 mixed-precision training matches FP32 (empirical)
**Benchmark** · [source](https://arxiv.org/abs/1905.12322)

*Cross-task BF16 vs FP32 training results (accuracy/convergence) + why BF16 avoids FP16 loss scaling (FP32 exponent/range)*

<details>
<summary>Key content</summary>

- **BFLOAT16 numeric rationale (Section 3):**
  - BFLOAT16 keeps **FP32-like dynamic range** (same exponent range as FP32) while using fewer mantissa bits (described as “truncated full precision… with 8 bits of mantissa”), so it can represent **small gradients** without FP16-style loss scaling.
  - **FP16 mixed precision often needs loss scaling** to prevent gradient underflow; BFLOAT16 can **avoid loss scaling** due to wider range.
- **Mixed-precision workflow (Figure 1 / Section 3):**
  - Core compute (GEMM/FMA): **BF16 inputs, FP32 accumulation/output**.
  - Maintain **FP32 master weights** for updates (SGD/Adam update in FP32).
  - Convert tensors FP32→BF16 using Quantlib: **zero lower 16 bits + RNE (round-to-nearest-even)** before BF16-intended ops; outputs then quantized for next layer.
  - Non-GEMM ops (e.g., BatchNorm, activations like ReLU/tanh/sigmoid) accept **BF16 inputs**; **bias kept FP32**.
- **Empirical parity with FP32 (Section 4):**
  - **AlexNet (ImageNet):** FP32 **57.4% top-1 / 80.7% top-5** vs BF16 **57.2% top-1 / 80.1% top-5** (global minibatch 1024, 16 nodes, 88 epochs).
  - **ResNet-50 (ImageNet):** baseline FP32 **74.7% top-1 / 92.0% top-5**; BF16 “same top-1/top-5”. Fully trained BF16: **75.7% top-1 test** (global sample stats), matching FP32.
  - **GNMT BLEU (Table 2):** **DE→EN WMT’16:** FP32 **29.3**, BF16 **29.3**.
  - **DC-GAN (Table 3):** Inception **1.97±0.054 (FP32)** vs **2.06±0.055 (BF16)**; MS-SSIM **0.262 (FP32)** vs **0.217 (BF16)**.
  - **ResNet-50 with AVX512BF16 path:** Top-1 **75.62%**, matches SOTA.

</details>

### 📊 BFLOAT16 training parity vs FP32 (empirical)
**Benchmark** · [source](https://arxiv.org/pdf/1905.12322.pdf)

*Cross-task BF16 vs FP32 convergence/accuracy; BF16’s FP32-like exponent range often removes need for loss scaling*

<details>
<summary>Key content</summary>

- **Numeric format (Table 1):**  
  - FP32: (sign,exp,mant) = (1,8,23); max normal **3.40e38**; min normal **1.17e−38**; min subnormal **1.40e−45**  
  - FP16: (1,5,10); max normal **6.55e4**; min normal **6.10e−5**; min subnormal **5.96e−8**  
  - **BFLOAT16:** (1,8,7); max normal **3.38e38**; min normal **1.17e−38**; **no subnormals**  
  - **Rationale (Sec. 3):** BF16 keeps FP32 exponent range ⇒ fewer over/underflows in backprop gradients; avoids FP16-style **loss scaling** hyperparameter tuning.
- **Mixed-precision workflow (Fig. 1, Sec. 3):**
  - GEMMs take **BF16 inputs** (weights/activations/gradients) and **accumulate to FP32 outputs**.
  - A **FP32 master copy of weights** is used for the optimizer update step (e.g., SGD) to preserve accuracy.
  - “Quantlib” emulation: convert FP32→BF16 by **zeroing low 16 bits** with **RNE (round-to-nearest-even)**; applied before ops intended to run in BF16.
  - Bias tensors kept **FP32**; non-GEMM ops (BN, ReLU/tanh/sigmoid) accept BF16 inputs.
- **Empirical parity (Sec. 4):**
  - **AlexNet ImageNet-1K:** FP32 **57.4/80.7** (top1/top5) vs BF16 **57.2/80.1**; global minibatch **1024**, data-parallel **16 nodes**, **88 epochs**.
  - **ResNet-50 ImageNet-1K:** FP32 **74.7/92.0** vs BF16 **74.7/92.0**; global minibatch **1024**, **32 nodes**, **SGD + Nesterov**, **90 epochs**, LR warmup **5 epochs**.
  - **GNMT BLEU (Table 2):** DE→EN **29.3 vs 29.3**; VI→EN(+attention) **17.1 vs 18.3** (FP32 vs BF16).
  - **Recsys logloss (Table 5; lower is better):** Deep&Cross **0.44372 vs 0.44372** (BF16 RND); DNN recsys **0.12520 vs 0.12520** (BF16 RND). Truncation slightly worse (e.g., **0.44393**, **0.12537**).

</details>

### 📊 Float8 + FSDP2 throughput scaling (LLaMA3, H100)
**Benchmark** · [source](https://pytorch.org/blog/training-using-float8-fsdp2/)

*Concrete tokens/sec/GPU gains (wps), scaling to 512 H100s, and operational recipe: FSDP2 + DTensor + torch.compile + torchao float8 (+ float8 all_gather)*

<details>
<summary>Key content</summary>

- **Metric / formula (Eq. 1):**  
  **wps = tokens / second / GPU** (reported as “tokens/sec/GPU (wps)”; seq length fixed at **8K** for measurements).
- **Core recipe / workflow:**
  - Use **FSDP2** + **DTensor** (for very large models; **405B uses tensor parallelism TP=4** with FSDP2).
  - Enable **torch.compile** (used for both bf16 and float8 baselines).
  - Use **torchao float8 linear layers** for compute (matmul/linear updates in float8).
  - Use **float8 all_gather** for **weight communication** (recent PyTorch nightlies) to reduce comm overhead.
  - **Attention computed in bf16** via **SDPA** (work ongoing to move attention to float8).
  - Float8 scaling choice: **per-tensor (tensorwise) scaling**, not rowwise.
- **Empirical throughput gains (Table 1, seq=8K):**
  - **1.8B:** bf16 **29K** wps → float8 **35K** (**+18%**)
  - **8B:** **8K** → **10K** (**+28%**)
  - **70B:** **956** → **1430** (**+50%**)
  - **405B (TP4):** **149** → **227** (**+52%**)
  - Adding **float8 all_gather** yields **~+5%** beyond float8 compute alone.
- **512 H100 scale results (Table 3):**
  - **70B:** **960** → **1448** (**+51%**)
  - **405B (TP4):** **152** → **217** (**+43%**)
- **Quality checks:** loss parity shown for **8B (2k steps)** and **70B (1k steps)** across multiple H100 clusters; 3B trained to **1T tokens** (FineWeb-edu) with eval table (avg **0.59 float8 vs 0.60 bf16**; e.g., **MMLU 0.26 vs 0.29**).

</details>

### 📊 Production FSDP scaling + throughput/MFU/HFU (Llama2-7B)
**Benchmark** · [source](https://pytorch.org/blog/maximizing-training/)

*Production-style FSDP scaling metrics + techniques to reach 3,700 tok/s/GPU and near-linear scaling to 512 GPUs*

<details>
<summary>Key content</summary>

- **Headline benchmark (7B, A100):** FSDP pretraining exemplar (Meta Llama 2 7B architecture) trained to **2T tokens** with **3,700 tokens/sec/GPU** on **128× A100 80GB**, ≈ **40B tokens/day**. Reported **MFU = 57%**, **HFU = 57%**.
- **Scaling claim:** Observed **near-linear scaling to 512 GPUs**; extrapolated **<2 weeks** to train 7B to **2T tokens** on **512 GPUs**.
- **Infrastructure:** **400Gbps** interconnect + **GPU Direct RDMA** (A100 run). H100 cluster referenced: **96× H100 80GB**, **800Gbps** interconnect.
- **Core throughput levers (FSDP stack):**
  - **SDPA FlashAttention v2** (fused attention kernels).
  - **Compute/communication overlap** (forward prefetch gather + backward overlap); practical overlap ceiling ≈ **90%** (first fwd + last bwd can’t overlap).
  - **Selective activation checkpointing (AC):** checkpoint every *n* blocks (vs every block) to trade memory vs recompute; **~10% throughput boost** beyond out-of-box FSDP. For **7B**, **no AC** needed; turning AC off enabled larger batch and **~10% higher throughput** vs using AC.
- **Training hyperparameters (7B run):**
  - **Mixed precision:** **bf16**.
  - **Optimizer:** **AdamW (32-bit)**, **β1=0.9**, **β2=0.95**, **weight decay=0.1**.
  - **LR schedule:** warmup to **3e-4**, cosine decay to **3e-5** over **2T tokens** (ending LR **3e-5**).
  - **Batching:** **~1M tokens/batch** on 128 GPUs; table uses **batch size=2 per GPU** to mimic 4k seq-length and stay ≤ **4M tokens** global batch up to 512 GPUs; beyond that needs **tensor/sequence parallelism**.
- **Empirical table (tokens/sec/GPU, MFU/HFU):**
  - **A100:** 7B **3700 (0.57/0.57)**; 13B **1800 (0.51/0.59)**; 34B **700 (0.47/0.64)**; 70B **370 (0.50/0.67)**.
  - **H100:** 7B **7500 (0.37/0.37)**; 13B **3800 (0.35/0.40)**; 34B **1550 (0.32/0.44)**; 70B **800 (0.34/0.45)**.
- **MFU/HFU computation (procedure):**
  - **HFU:** PyTorch FLOP counter + theoretical **bf16** peak of GPU.
  - **MFU:** methodology from **NanoGPT** and **PaLM**.
- **Design rationale notes:**
  - On **A100**, activation recomputation tends to **decrease MFU** but **increase HFU**.
  - On **H100**, MFU/HFU lower; profiling shows ~**10%** gap from network “peeking”; hypothesis: **HBM bandwidth** limits (H100 compute ~**989 TFLOPS** vs A100 **312 TFLOPS**, but bandwidth <2×).

</details>

### 📖 PyTorch AMP (autocast + GradScaler) essentials
**Reference Doc** · [source](https://docs.pytorch.org/docs/stable/amp.html)

*Exact semantics/defaults for `torch.amp.autocast` + gradient scaling; fp16 vs bf16 behavior and device defaults*

<details>
<summary>Key content</summary>

- **Mixed precision goal/rationale:** Run some ops in `float32` (range/stability, e.g., reductions) and others in lower precision (`lower_precision_fp`: `float16` or `bfloat16`) for speed (e.g., linear/conv).
- **Autocast API:** `torch.autocast(device_type, dtype=None, enabled=True, cache_enabled=None)`
  - **Defaults:** `enabled=True`, `cache_enabled=True`.
  - **dtype default if `None`:** from `get_autocast_dtype()` → **CUDA:** `torch.float16`; **CPU:** `torch.bfloat16`.
  - **Procedure:** Wrap **only forward + loss** in autocast; **do not** run backward under autocast (“Backward passes under autocast are not recommended”; backward runs in same dtype used by corresponding forward ops).
  - **Do not manually call** `.half()` / `.bfloat16()` on model/inputs when using autocast.
  - **Nesting:** `autocast(enabled=False)` subregions allowed; cast incoming tensors (e.g., `e_float16.float()`) to force `float32` execution.
  - **Thread-local state:** must enable autocast per thread; impacts multi-GPU per process (e.g., `DataParallel`, `DistributedDataParallel`).
- **Gradient scaling rationale:** fp16 backward can underflow (small grads flush to 0). Scale loss to amplify grads, then **unscale before optimizer step**.
  - **Equation (Eq. 1):** `L_scaled = s * L`; backprop on `L_scaled`; before update use `g = (∂L_scaled/∂w) / s`.
  - **Important note:** AMP/fp16 may fail for bf16-pretrained models due to fp16 max **65504** → overflow/NaNs; `GradScaler` scale may decrease **below 1** (not guaranteed >1).
- **Deprecations:** `torch.cuda.amp.autocast` / `torch.cpu.amp.autocast` and corresponding `GradScaler` are deprecated → use `torch.amp.autocast("cuda"/"cpu", ...)`, `torch.amp.GradScaler("cuda"/"cpu", ...)`.
- **Loss function pitfall:** `binary_cross_entropy` / `BCELoss` error under autocast; prefer `binary_cross_entropy_with_logits` / `BCEWithLogitsLoss` (safe).

</details>

### 📖 PyTorch AMP canonical training-loop order (GradScaler/autocast)
**Reference Doc** · [source](https://docs.pytorch.org/docs/stable/notes/amp_examples.html)

*Correct AMP training recipes incl. gradient accumulation/clipping + multi-optimizer ordering*

<details>
<summary>Key content</summary>

- **Core AMP components**
  - Use `torch.autocast(device_type='cuda', dtype=torch.float16)` for forward/loss regions.
  - Use `torch.amp.GradScaler()` once at start to scale losses and manage inf/NaN checks + dynamic scale updates.
  - Rationale: scaling mitigates **float16 gradient underflow**; autocast chooses op precision for speed while maintaining accuracy.

- **Canonical step ordering (Typical Mixed Precision Training)**
  1. `optimizer.zero_grad()`
  2. `with autocast(...): output = model(input); loss = loss_fn(output, target)`
  3. `scaler.scale(loss).backward()`  
     - Note: **Backward under autocast not recommended**; backward ops run in dtype chosen for corresponding forward ops.
  4. `scaler.step(optimizer)`  
     - Internally **unscales** grads for optimizer params; if grads contain **inf/NaN**, `optimizer.step()` is **skipped**.
  5. `scaler.update()` (updates scale for next iteration)

- **Unscaled-gradient operations (e.g., clipping)**
  - Must unscale before inspecting/modifying `.grad` (else thresholds are effectively scaled).
  - Procedure: after backward → `scaler.unscale_(optimizer)` → `torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm)` → `scaler.step(optimizer)` → `scaler.update()`.
  - Constraint: `unscale_` **only once per optimizer per step**, and **only after all grads are accumulated**; calling twice triggers `RuntimeError`.

- **Gradient accumulation (effective batch)**
  - Effective batch size: **Eq. 1** `B_eff = batch_per_iter * iters_to_accumulate * num_procs` (if distributed).
  - Loss scaling for accumulation: **Eq. 2** `loss = loss / iters_to_accumulate`.
  - Keep grads **scaled** and scale factor **constant** across accumulation; call `step/update/zero_grad` only when `(i+1) % iters_to_accumulate == 0`. Unscale (for clipping) **just before** `step`.

- **Multiple losses/optimizers**
  - Call `scaler.scale(loss_k)` **for each loss**.
  - Call `scaler.step(optimizer_j)` **for each optimizer**; call `scaler.update()` **once after all steps**.
  - Each optimizer independently skips step on inf/NaN.

</details>

### 📖 PyTorch DistributedDataParallel (DDP) constructor semantics & key knobs
**Reference Doc** · [source](https://docs.pytorch.org/docs/stable/generated/torch.nn.parallel.DistributedDataParallel.html)

*DDP defaults/semantics: bucket sizing, buffer/param sync, unused params, bucket views, static graph, mixed precision surface*

<details>
<summary>Key content</summary>

- **What DDP does (core procedure):** Wraps a `torch.nn.Module` to do *data parallelism* by **all-reducing gradients** across replicas in a `process_group` (default: world). **Does not shard inputs**; user must shard (e.g., `DistributedSampler`). Requires `torch.distributed.init_process_group()` before construction.
- **Process/GPU setup (single-node N GPUs):** Spawn **N processes**, each bound to one GPU (`torch.cuda.set_device(i)` or `torch.accelerator.set_device_index(i)`), then `DDP(model, device_ids=[i], output_device=i)`. Alternative init: `torch.distributed.init_process_group(device_id=i)`.
- **Sync semantics & rationale:**
  - **Parameters are never broadcast each iteration**; DDP assumes optimizers update params identically on all ranks after gradient all-reduce.
  - **Buffers** (e.g., BatchNorm stats) are **broadcast from rank 0 each iteration** if `broadcast_buffers=True` (default).
  - `init_sync=True` (default) **verifies param shapes and broadcasts parameters and buffers at init**; if `False`, user must ensure identical weights across ranks.
- **Gradient bucketing (overlap comm/compute):** DDP buckets params so bucket all-reduce can overlap backward compute. `bucket_cap_mb` controls bucket size in **MiB**; default **25 MiB** when `None`.
- **Unused params handling:** `find_unused_parameters=False` (default). If `True`, DDP traverses autograd graph from `forward` outputs; params not receiving grads are pre-marked “ready” for reduction.
- **Memory/perf knobs:**
  - `gradient_as_bucket_view=False` (default). If `True`, `.grad` becomes a **view into all-reduce buckets**, saving peak memory ≈ **total gradient size** and avoiding copies; cannot call `detach_()` on grads.
  - `static_graph=False` (default). If `True`, graph/used-params set is constant; enables reentrant backwards, multiple checkpointing, unused params with checkpointing, params outside `forward`, and avoids per-iter unused-param search. Check via `ddp._get_ddp_logging_data()["can_set_static_graph"]`.
- **Uneven inputs workflow:** Use `with model.join(...):` to prevent hangs when ranks exhaust data at different times. `divide_by_initial_world_size=True` (default) vs divide by effective world size.
- **Gradient accumulation:** `with ddp.no_sync(): ...` disables sync inside context; sync occurs on first backward after exiting.
- **Mixed precision:** DDP supports mixed parameter dtypes (e.g., fp16/fp32); constructor includes `mixed_precision=` argument.

</details>

---

## Related Topics

- [[topics/neural-networks|Neural Networks]]
- [[topics/pre-training|Pre-Training]]
- [[topics/scaling-laws|Scaling Laws]]
- [[topics/inference-optimization|Inference Optimization]]
