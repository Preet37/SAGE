---
title: "Inference Optimization"
subject: "Large Language Models"
date: 2026-04-09
tags:
  - "subject/large-language-models"
  - "level/intermediate"
  - "level/advanced"
  - "educator/andrej-karpathy"
  - "resource/video"
  - "resource/blog"
  - "resource/deep-dive"
  - "resource/paper"
  - "resource/code"
educators:
  - "Andrej Karpathy"
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

# Inference Optimization

## Video (best)
- **Andrej Karpathy** — "State of GPT"
- **Watch:** [YouTube](https://www.youtube.com/watch?v=jkrNMKz9pWU)
- Why: Clear, systems-aware overview of how inference works in practice (latency/throughput constraints, KV cache, batching, serving considerations) from an LLM practitioner perspective.
- Level: Intermediate

## Blog / Written explainer (best)
- **Hugging Face (Blog)** — "Speculative Decoding"
- Why: Practical, readable explanation of speculative decoding with intuition, algorithm sketch, and why it improves throughput without changing model quality.
- Level: Intermediate
- **Link:** [https://huggingface.co/docs/transformers/assisted_decoding](https://huggingface.co/docs/transformers/assisted_decoding)
## Deep dive
- **vLLM (Project Docs)** — "PagedAttention and vLLM"
- Why: Primary reference for paged attention and KV-cache memory management in a modern high-throughput serving engine; directly relevant to continuous batching and KV cache optimization.
- Level: Advanced
- url: https://docs.vllm.ai/ [VERIFY] (navigate to PagedAttention / architecture sections)

## Original paper
- **Kwon et al.** — "Efficient Memory Management for Large Language Model Serving with PagedAttention"
- Why: Foundational paper behind vLLM’s paged attention approach; key for understanding KV cache optimization and high-throughput serving.
- Level: Advanced
- **Link:** [https://arxiv.org/abs/2309.06180](https://arxiv.org/abs/2309.06180)
## Code walkthrough
- **vLLM (GitHub)** — "vLLM: a high-throughput and memory-efficient inference and serving engine for LLMs"
- Why: Best “read-the-source” entry point for continuous batching, KV cache management, and paged attention in a production-grade serving system.
- Level: Advanced
- **Link:** [https://github.com/vllm-project/vllm](https://github.com/vllm-project/vllm)
## Coverage notes
- Strong: vLLM + paged attention; KV cache optimization concepts; speculative decoding overview.
- Weak: Quantization methods (GPTQ/AWQ/GGUF) consolidated “best” explainer; TensorRT-LLM and Triton Inference Server deep, beginner-friendly walkthroughs.
- Gap: Medusa decoding (and other multi-token decoding variants) and a single, high-quality comparative guide across GPTQ vs AWQ vs GGUF with inference tradeoffs.

---

## Additional Resources for Tutor Depth

> **8 sources** — papers, official docs, working code, benchmarks, and deep explainers that give the AI tutor precision on this topic.

### 📄 AWQ scaling + clipping criteria for W4A16 LLM quantization
**Paper** · [source](https://arxiv.org/abs/2306.00978)

*Activation-aware scaling (from activation stats) + AWQ procedure to preserve salient channels under 4-bit weight-only quantization*

<details>
<summary>Key content</summary>

- **Observation (Sec. 3.1):** Only a tiny fraction of weights/channels are “salient” (≈0.1%–1%). Selecting salient channels **by activation magnitude** is far better than by weight norm or random. Example (Table 1, INT3): OPT-6.7B PPL **RTN 23.54** → keeping **1% FP16 based on activations: 11.39** (vs **1% FP16 based on weights: 23.41**, random ≈23.5).
- **Quantization definition (Eq. 1):** For weight group/block \(W\), quantize elementwise  
  \[
  Q(W)=\Delta\cdot \mathrm{Round}(W/\Delta),\quad \Delta=\frac{\max(|W|)}{2^{b-1}-1}
  \]
  where \(b\)=#bits (INT3/INT4), \(\Delta\)=scale from abs-max in the group.
- **Activation-aware scaling trick (Eq. 2–3):** Scale salient **input channels** by \(s\) before quantization and inversely scale activations so the layer output is unchanged in FP16, but quantization error on scaled weights is reduced. Error ratio becomes \(\approx 1/s\) for scaled (salient) weights when group max unchanged.
- **Choosing scales via activation stats (Eq. 4–5):** Optimize per-input-channel scale \(s\) to minimize output mismatch on cached calibration inputs \(X\):  
  \[
  \min_{s}\ \|XW - X\,Q(W\cdot \mathrm{diag}(s))\cdot \mathrm{diag}(s)^{-1}\|
  \]
  Search space (Eq. 5): \(s = (\mathbb{E}|x|)^{\alpha}\) per channel; grid search \(\alpha\in[0,1]\) (20-point grid). Calibration: small set from **Pile**.
- **Weight clipping:** After scaling, apply **weight clipping** to minimize quantization MSE (used in AWQ pipeline).
- **Empirical scaling effect (Table 2):** OPT-6.7B INT3: RTN **23.54** → scaling salient 1% with \(s=2\): **12.87**; \(s=4\): **12.48**; \(s=8\): **11.92** (best); too-large \(s\) hurts non-salient channels.
- **Defaults:** grouped weight-only quantization, **group size 128**, focus on **INT4/INT3**, no backprop/reconstruction.

</details>

### 📄 Choosing llama.cpp GGUF quantization (Llama-3.1-8B-Instruct)
**Paper** · [source](https://arxiv.org/pdf/2601.14277.pdf)

*Unified downstream + throughput evaluation of llama.cpp GGUF quantization choices; GGML/GGUF block-wise (and K-quant hierarchical) quantized-tensor storage concepts.*

<details>
<summary>Key content</summary>

- **Quantization math (Section 2.1):**
  - **Eq. (1) affine quantizer:** \(w \approx s\,(q - z)\) where \(w\)=real weight, \(q\)=integer code, \(s\)=scale, \(z\)=zero-point/offset. In GGML-style PTQ, \(s,z\) are stored **per block** (not per tensor).
  - **Eq. (2) Q4_1-style dequant:** \(w \approx s\,q + m\) where \(m\)=stored per-block offset/min (asymmetric/affine).
  - **Eq. (3) high-resolution error model:** for symmetric \(b\)-bit uniform quantizer, step \(\Delta\) implies quantization error variance \(\approx \Delta^2/12\); +1 bit \(\Rightarrow\) ~4× lower modeled variance (subject to clipping/heavy tails).
- **Format design (Section 2.2):**
  - Legacy: Q4_0 (symmetric), Q4_1 (affine), Q5_0/Q5_1, Q8_0 (symmetric 8-bit).
  - **K-quants:** hierarchical **super-blocks of 256 weights**, split into sub-blocks with additional (often quantized) scale/min metadata; suffixes _S/_M/_L trade compression vs fidelity.
- **Procedure (Section 3):**
  - Quantize from the same FP16 GGUF via: `./llama-quantize <f16.gguf> <out.gguf> <SCHEME>`.
  - Benchmarks: GSM8K (5-shot), HellaSwag (0-shot), IFEval (0-shot), MMLU (0-shot), TruthfulQA (0-shot), plus WikiText-2 perplexity.
  - Throughput measured with **pp=512** (prefill) and **tg=128** (decode).
- **Key empirical results (Table 2, Llama-3.1-8B-Instruct):**
  - **F16:** Avg 69.47, PPL 7.32.
  - **Q5_0:** size reduction **65.19%**, Avg **69.92** (highest), PPL **7.43**.
  - **Q4_K_S:** reduction **70.83%**, Avg **69.17**, PPL **7.62**.
  - **Q3_K_S (most compressed):** reduction **77.23%**, Avg **65.49**, PPL **8.96**; GSM8K drops **77.63 → 68.31**.
- **Throughput (Table 3, tokens/s):**
  - **F16:** pp512 79.57, tg128 2.83.
  - **Q3_K_S:** pp512 57.39, tg128 **9.91** (fastest decode).
  - **Q4_K_S:** pp512 92.52, tg128 4.65.
  - **Q5_0:** pp512 61.44, tg128 6.66.
- **Pareto guidance (Section 4.3):** Non-dominated set highlighted: **Q5_0** (best AvgLoss with strong compression), then **Q4_K_S**, then **Q3_K_L / Q3_K_M**, with **Q3_K_S** only when footprint dominates.

</details>

### 📄 GPTQ objective + sequential error-compensated quantization
**Paper** · [source](https://arxiv.org/abs/2210.17323)

*Exact GPTQ objective (2nd-order/Hessian-based), blockwise/columnwise update rule, sequential quantization w/ error compensation*

<details>
<summary>Key content</summary>

- **Layer reconstruction objective (Section 3, Eq. 1):** for linear layer weights \(W_\ell\) and calibration inputs \(X_\ell\) (m samples), choose quantized weights \(\widehat W\) to minimize squared output error:  
  \[
  \min_{\widehat W}\ \|W_\ell X_\ell - \widehat W X_\ell\|_2^2
  \]
- **OBQ/GPTQ per-row quadratic view:** objective decomposes over rows \(w\). For remaining (unquantized) weights set \(F\), Hessian is  
  \[
  H_F = 2 X_F X_F^\top
  \]
  (depends only on inputs, not weights).
- **Multi-weight/block update (GPTQ Step 2, Eq. 4–5):** quantize a set of indices \(Q\) (e.g., a block of columns), with \(\text{quant}(\cdot)\) = rounding to nearest grid point. Error-compensating update to remaining weights:
  \[
  \delta_F = -(w_Q-\text{quant}(w_Q))\big([\!H_F^{-1}\!]_{QQ}\big)^{-1}(H_F^{-1})_{:,Q}
  \]
  Inverse update after removing \(Q\):
  \[
  H_{-Q}^{-1}=\Big(H^{-1}-H^{-1}_{:,Q}\big([\!H^{-1}\!]_{QQ}\big)^{-1}H^{-1}_{Q,:}\Big)_{-Q}
  \]
- **Key design rationale:** quantizing all rows in the **same fixed column order** makes \(H_F^{-1}\) shared across rows ⇒ update \(H^{-1}\) only \(d_{\text{col}}\) times (not \(d_{\text{row}}d_{\text{col}}\)). Use **block size \(B=128\) columns** for efficiency.
- **Numerical stability (Step 3):** repeated inverse updates can make \(H_F^{-1}\) indefinite; mitigate with **dampening** \(\lambda\) added to diag(\(H\)), chosen as **1% of average diagonal**, and a **Cholesky-based reformulation** to precompute needed rows more stably.
- **Calibration/defaults:** **128 random 2048-token segments** from **C4**; **uniform per-row asymmetric min–max** quantization grid; supports grouping (e.g., group-size **1024** improves perplexity ~**0.2**, group-size **128** adds ~**0.1** more).
- **Empirical runtime/quality:** quantizes **OPT-175B/BLOOM-176B in ~4 GPU hours**, enabling **3–4 bit** weights with negligible perplexity increase; reported end-to-end inference speedups **~3.25× (A100)** and **~4.5× (A6000)** vs FP16.

</details>

### 📄 Medusa multi-head draft + tree verification + acceptance
**Paper** · [source](https://arxiv.org/abs/2401.10774)

*Medusa multi-head draft decoding algorithm: multi-token proposals per step + base-model verification (tree attention) + acceptance (rejection or typical)*

<details>
<summary>Key content</summary>

- **Problem/Rationale (Intro):** AR decoding is **memory-bandwidth-bound**; each step moves full params from HBM → cache but yields **1 token**. Speedup comes from **reducing decoding steps** and increasing arithmetic intensity.
- **Medusa heads (Sec. 2.1.1):** Add \(K\) lightweight decoding heads on top of backbone last hidden state \(h_t\). Head \(i\) predicts token at offset \(i\) in the next \(K\) tokens; backbone LM head predicts offset 0. Each head is a **1-layer FFN + residual**; initialized to match LM head (weights copied; bias zero) to align distributions and avoid draft-model shift.
- **Tree attention verification (Sec. 2.1.2):**
  - For head \(i\), take **top-\(k\)** tokens; build candidate continuations via **Cartesian product** across heads → a token **tree**.
  - Use a **tree-structured attention mask**: a token attends only to its **predecessors on the same branch**; set positional indices accordingly. This verifies many candidates in one forward pass without expanding batch. Total new nodes \(\sum_{i=1}^{K} k^i\).
- **Acceptance (Sec. 2):** After verification logits from backbone, accept a prefix via **(a) rejection sampling** (lossless, speculative-decoding style) or **(b) typical acceptance** (Sec. 2.3.1): accept tokens that are “typical” under backbone using probability threshold based on entropy \(H(\cdot)\): accept if \(p(x_t\mid \text{context}) \ge \min(\epsilon,\ \exp(-H)\cdot \delta)\) (hard threshold \(\epsilon\), entropy-dependent threshold \(\delta\)). First token is **greedy + always accepted**; choose **longest accepted prefix** among candidates.
- **Training losses:**
  - **Medusa-1 frozen backbone (Eq. 1):** weighted sum of head cross-entropies  
    \(\mathcal{L}_{\text{Medusa}}=\sum_{i=1}^{K} w_i\,\mathcal{L}_i\), with \(w_i=c^i\) (e.g., \(c=0.8\)).
  - **Medusa-2 joint training (Eq. 2):** add backbone CE loss + weight; use **differential LRs** and **2-stage warmup** (train heads first, then joint).
- **Defaults/heuristics:** “**5 heads** are sufficient at most” (Sec. 2.2.3); can ignore redundant heads at inference.
- **Empirical results (Abstract/Sec. 3):**
  - Medusa-1: **>2.2×** speedup, no quality loss; Medusa-2: **2.3–2.8×**.
  - Vicuna-13B: Medusa-1 **2.33×**; Vicuna-7B Medusa-2 **2.83×**. Category speedups: **Coding 3.29×**, **Extraction 3.62×**.
  - Ablation (Table 3): heads only **1.5×** → +tree attention **1.9×** → optimized tree **2.2×** → Medusa-2 training **2.8×**.

</details>

### 📄 SmoothQuant (W8A8 PTQ via activation smoothing)
**Paper** · [source](https://arxiv.org/pdf/2211.10438.pdf)

*Exact smoothing formulation (α) + calibration protocol + W8A8 accuracy/latency/memory tables*

<details>
<summary>Key content</summary>

- **Uniform INT8 quantization (Eq. 1):** quantize float tensor \(x\) to INT8 \(\hat{x}\) with step size \(\Delta\): \(\hat{x}=\mathrm{round}(x/\Delta)\) (symmetric; asymmetric adds zero-point). \(\Delta\) typically set from max-abs (static via calibration or dynamic at runtime).  
- **Hardware constraint (Sec. 3, Eq. 2):** per-channel activation scaling is hard to fuse into INT8 GEMM; scaling is feasible only along outer GEMM dims and applied after matmul.
- **SmoothQuant smoothing transform (Eq. 3):** for linear \(Y=XW\), choose per-input-channel scale \(s\) and rewrite equivalently:  
  \[
  Y=(X\operatorname{diag}(s)^{-1})(\operatorname{diag}(s)W)
  \]
  Smooth activations by dividing each input channel by \(s\); compensate by scaling corresponding weight rows/cols (mathematically equivalent).
- **Choosing \(s\) with migration strength \(\alpha\) (Eq. 4):** split quantization difficulty between activations and weights:  
  \[
  s_j=\frac{\left(\max|X_j|\right)^{\alpha}}{\left(\max|W_j|\right)^{1-\alpha}}
  \]
  where \(j\) indexes input channels; \(\max|X_j|\) estimated from calibration samples; \(\alpha\in[0,1]\). Sweet spot for OPT/BLOOM: \(\alpha\approx0.5\); ablation shows good region \(\alpha\in[0.4,0.6]\). For heavier outliers (e.g., GLM-130B), use larger \(\alpha\) (e.g., 0.75).
- **Calibration protocol (Sec. 5.1):** compute smoothing factors + static quant steps once using **512 random sentences from The Pile**; reuse same quantized model for all downstream tasks. For GLM-130B static steps, **clip top 2% tokens** during calibration.
- **Accuracy (Table 3, OPT-175B avg):** FP16 **66.9%**; naive W8A8 **35.5%**; LLM.int8() **66.7%**; SmoothQuant O1/O2/O3 **66.5/66.4/66.8%** (WikiText PPL FP16 **10.99** vs SQ-O3 **11.17**; naive W8A8 **93080**).
- **Latency/memory (Table 8, decoding):** OPT-30B (1 GPU) BS1 Seq512: FP16 **422ms, 57GB** vs SQ **314ms, 30GB** (speedup **1.35×**, saving **1.91×**). OPT-175B (8 GPUs) BS16 Seq512: FP16 **2212ms, 50GB** vs SQ **1628ms, 30GB** (speedup **1.36×**, saving **1.67×**).  
- **Quantization schemes (Table 2):** SmoothQuant O1 = W per-tensor, A per-token dynamic; O2 = W per-tensor, A per-tensor dynamic; O3 = W per-tensor, A per-tensor static (coarser ⇒ lower latency).

</details>

### 📄 SmoothQuant (W8A8 PTQ via activation–weight smoothing)
**Paper** · [source](https://arxiv.org/abs/2211.10438)

*SmoothQuant objective/procedure: per-channel smoothing factor (α) migrates quantization difficulty from activations to weights; calibration + accuracy/latency results for W8A8.*

<details>
<summary>Key content</summary>

- **Uniform INT8 quantization (Eq. 1):** quantize float tensor \(X\) to INT8 \(\hat X\) with step size \(\Delta\):  
  \(\hat X = \mathrm{round}(X/\Delta)\) (symmetric around 0; asymmetric uses zero-point). \(\Delta\) typically from max-abs (static via calibration or dynamic at runtime).
- **Problem (Sec. 3):** activation outliers persist in fixed channels; per-tensor/per-token activation quantization fails for large LLMs; simulated **per-channel activation** quantization restores accuracy but is **hardware-unfriendly** for INT8 GEMM.
  - OPT average accuracy (WinoGrande/HellaSwag/PIQA/LAMBADA): FP16 **71.6%** (175B) vs INT8 per-tensor **32.3%**; INT8 per-channel **71.4%** (Table 1).
- **Smoothing transform (Eq. 3):** for linear \(Y=XW\), choose per-input-channel smoothing vector \(s\):  
  \(Y=(X \operatorname{diag}(s)^{-1})(\operatorname{diag}(s)W)\). This reduces activation channel range; scaling can be **fused offline** into preceding layers (no extra kernel), residual branch may need extra scaling.
- **Choosing \(s\) with migration strength \(\alpha\) (Eq. 4):** split difficulty between activations and weights:  
  \(s_j = \left(\frac{\max|X_j|}{\max|W_j|}\right)^{\alpha}\) (channel \(j\)); \(\alpha\approx 0.5\) works well for OPT/BLOOM; larger (e.g., **0.75**) for harder activations (GLM-130B). Sweet spot **0.4–0.6** (Fig. 10).
- **Procedure:** calibrate \(s\) (and static \(\Delta\) if used) once using **512** random Pile sentences; grid-search \(\alpha\). Quantize compute-heavy ops (linear + attention BMM) to INT8; keep elementwise ops (Softmax/LN/ReLU) in FP16.
- **Key empirical results (OPT-175B, Table 3):** FP16 avg **66.9%**, WikiText ppl **10.99**. Naive W8A8 avg **35.5%**, ppl **93080**. **SmoothQuant-O3** avg **66.8%**, ppl **11.17** (near-lossless).
- **Speed/memory:** integrated into FasterTransformer: up to **1.56×** latency speedup and ~**2×** memory reduction vs FP16; decoding speedup up to **1.42×** (Table 8). Enables serving **530B** within one **8×A100-80GB** node (half GPUs vs FP16).

</details>

### 📄 Speculative Decoding—Expected Rejections & Optimality (TV-distance)
**Paper** · [source](https://proceedings.neurips.cc/paper_files/paper/2024/file/e7349e785900b93d8b4971a3f2c1cefe-Paper-Conference.pdf)

*Formal correctness + optimality for speculative decoding; exact expected rejections formula in terms of draft/target distributions (TV distance).*

<details>
<summary>Key content</summary>

- **Speculative Decoding acceptance/rejection (Alg. 1):** draft token \(\tilde x_t \sim p_t(\cdot\mid x_{1:n-1},\tilde x_{n:t-1})\). Accept with  
  \[
  b_t(\tilde x_t)=\min\left\{1,\frac{q_t(\tilde x_t)}{p_t(\tilde x_t)}\right\}
  \]
  If rejected, sample \(x_n \sim r(q_t-p_t)_+(\cdot)\), i.e. normalized \(\max(0,q-p)\).
- **Runtime proxy:** under Assumption 1 (draft cost negligible; one parallel “oracle call” for target logits costs \(O(1)\)), **#oracle calls = #rejections**, so **acceleration** \(\approx T/\#\text{rejections}\).
- **Exact expected rejections (Thm. 1, Sec. 3):** with \(R_n\in\{0,1\}\) rejection indicator and \(N_{\text{rej}}=\sum_{n=1}^T R_n\),
  \[
  \mathbb E[N_{\text{rej}}]=\sum_{n=1}^T \mathbb E_{x_{1:n-1}\sim q}\Big[\mathrm{TV}\big(p_n(\cdot\mid x_{1:n-1}),\,q_n(\cdot\mid x_{1:n-1})\big)\Big].
  \]
  Implications: if TV=0 always ⇒ accel \(=T\); if TV=1 always ⇒ accel \(=1\).
- **Correctness/unbiasedness (Thm. 1):** output joint distribution matches target: \(P_{\text{SD}}(x_{1:T})=q(x_{1:T})\).
- **Optimality among unbiased rejection-based decoders (Thm. 2):**
  \[
  \inf_{A\in\mathcal F}\mathbb E_A[N_{\text{rej}}]\ \ge\ \sum_{n=1}^T \mathbb E_{x_{1:n-1}\sim q}[\mathrm{TV}(p_n,q_n)],
  \]
  matching SD’s value ⇒ cannot reduce rejections by changing \(b_t,P_t\) without bias/extra info.
- **Empirical check (Fig. 2a):** nonstationary Markov-chain sim, \(T=50\): theoretical \(\mathbb E[N_{\text{rej}}]=16.41\); observed converges to 16.41; accel \(50/16.41=3.05\).

</details>

### 📖 Triton TensorRT‑LLM backend — model config essentials
**Reference Doc** · [source](https://docs.nvidia.com/deeplearning/triton-inference-server/archives/triton-inference-server-2540/user-guide/docs/tensorrtllm_backend/docs/model_config.html)

*Triton TensorRT‑LLM backend `config.pbtxt` fields, defaults, and performance-tuning notes (batching, KV cache, speculative decoding, removed fields)*

<details>
<summary>Key content</summary>

- **Template editing procedure:** Config fields are filled via `tools/fill_template.py`. For comma-valued fields (e.g., `gpu_device_ids`, `participant_ids`), **escape commas**:  
  `python3 fill_template.py -i config.pbtxt "gpu_device_ids:0\,1"`.
- **tensorrt_llm mandatory config highlights:**  
  `backend` (set to TensorRT‑LLM backend), `max_batch_size`, `decoupled_mode` (**must be true**), `max_queue_delay_microseconds` (>0 can improve co-batching of close arrivals), `max_queue_size` (reject beyond), `engine_dir`, batching strategy (set to inflight batching), input dtype, logits dtype.
- **KV-cache parameters & defaults (KV cache section):**
  - `max_tokens_in_paged_kv_cache`: max KV tokens; if unspecified interpreted as **infinite**.  
    **Allocation rule (Eq. 1):** `KV_alloc = min(max_tokens_in_paged_kv_cache, KV_from_mem_fraction)`  
    where `KV_from_mem_fraction` is derived from `kv_cache_free_gpu_mem_fraction`.
  - `kv_cache_free_gpu_mem_fraction` default **0.9** (fraction of post-model-load GPU mem usable for KV).
  - `cross_kv_cache_fraction` default **0.5** (encoder-decoder only; rest for self-attn).
  - Note: `enable_trt_overlap` **removed**; overlapping micro-batches didn’t help after CPU overhead reductions.
- **LoRA cache defaults:** `lora_cache_optimal_adapter_size` **8**; `lora_cache_gpu_mem_fraction` **0.05** (after engine + KV cache); host LoRA cache size default **1G**.
- **Speculative decoding (tensorrt_llm_bls):** set `tensorrt_llm_model_name` (target) and `tensorrt_llm_draft_model_name` (draft); request sets `num_draft_tokens`; optional `use_draft_logits`. Not supported with `return_generation_logits`/`return_context_logits`; **batch size > 1 not supported**.
- **Empirical tuning tips (Some tips section):**
  - `instance_count` ideally ≈ engine max batch size; **5** worked well in experiments; too small (e.g., **1**) is discouraged.
  - Inflight batching: keep **#requests < max_batch_size** and **total tokens < max_num_tokens** (engine build-time via `trtllm-build`).

</details>

---

## Related Topics

- [[topics/scaling-laws|Scaling Laws]]
- [[topics/lora-peft|LoRA & PEFT]]
- [[topics/mixture-of-experts|Mixture of Experts]]
- [[topics/long-context|Long Context Models]]
- [[topics/optimization-algorithms|Optimization Algorithms]]
