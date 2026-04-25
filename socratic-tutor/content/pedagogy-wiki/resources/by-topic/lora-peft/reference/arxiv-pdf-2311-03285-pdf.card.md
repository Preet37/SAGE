# Card: S-LoRA multi-tenant LoRA serving (Unified Paging + heterogeneous batching)
**Source:** https://arxiv.org/pdf/2311.03285.pdf  
**Role:** paper | **Need:** DEPLOYMENT_CASE  
**Anchor:** System design + empirical scaling claims for serving thousands of concurrent LoRA adapters (memory pool, batching, kernels, multi-GPU TP).

## Key Content
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

## When to surface
Use when students ask how to **serve many LoRA adapters concurrently**, how to avoid **GPU memory fragmentation** with KV cache + adapters, or how batching/parallelism changes when adapters have **heterogeneous ranks/sequence lengths**.