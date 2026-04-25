# Card: S-LoRA serving thousands of concurrent LoRA adapters
**Source:** https://lmsys.org/blog/2023-11-15-slora/  
**Role:** explainer | **Need:** DEPLOYMENT_CASE  
**Anchor:** Step-by-step operational explanation of S-LoRA’s serving approach (adapter storage/loading, routing, batching strategy)

## Key Content
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

## When to surface
Use when students ask how to **serve many LoRA adapters concurrently** (memory layout, paging, batching across ranks, avoiding merge/swap) or want **concrete throughput/memory tradeoffs** vs PEFT/vLLM.