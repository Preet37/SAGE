# Card: FlashAttention for long sequences — speed/memory + scaling rationale
**Source:** https://hazyresearch.stanford.edu/blog/2023-01-12-flashattention-long-sequences  
**Role:** benchmark | **Need:** EMPIRICAL_DATA  
**Anchor:** Concrete speed/throughput numbers at 8K context + system-level explanation (IO-aware tiling + parallelism changes practical scaling)

## Key Content
- **Quadratic baseline scaling (motivation):** Standard attention runtime and memory scale as **O(L²)** in sequence length **L**; doubling **L** ⇒ ~**4×** runtime and memory.
- **FlashAttention core idea (exact, no approximation):** Reorders attention computation to be **IO-aware**:
  - **Tiling:** load blocks of **Q, K, V** from GPU **HBM** (main memory) into **SRAM** (fast cache), compute attention for that tile, write output back.
  - **Recomputation:** trades some compute to avoid storing large intermediates; reduces memory footprint from **quadratic to linear in L** (activation memory).
  - Reported typical speedups from reduced HBM reads/writes: **~2–4×** (general regime).
- **Parallelism change for long sequences (small batch/heads):**
  - v1 parallelized over **batch_size × num_heads** (1 CUDA thread block per head). Efficient when **batch_size × num_heads ≥ ~80** (A100 has **108 SMs**).
  - For long sequences (often **batch size ~1** with pipeline parallelism; **~8–12 heads** with tensor parallelism), add **parallelism over sequence length**:
    - **Forward:** multiple workers per head, each handles a **block of rows** of attention matrix (rows independent → no worker communication).
    - **Backward:** workers handle **blocks of columns**; need to aggregate **∂L/∂Q** via **atomic operations**. Column-parallel chosen because it reduces communication vs row-parallel (which would aggregate **∂L/∂K, ∂L/∂V**).
- **Attention-layer benchmark (A100 40GB):** heads **=12**, head dim **=128**; measure **forward+backward** time while increasing **L** and decreasing batch to keep tokens constant. At **L=8K**, FlashAttention is **2.2–2.7× faster** than (a) standard PyTorch attention and (b) Megatron-LM optimized attention.
- **End-to-end training benchmark (8K context):**
  - Train Transformers up to **2.7B** params on **8K** sequences: **up to 175 TFLOPs/s per A100** (~**56%** model FLOPs efficiency), **no activation checkpointing**.
  - **2.2× faster** than Megatron-LM end-to-end.
  - Efficiency drop going **2K → 8K**: FlashAttention **~7%** less efficient; Megatron-LM drops by **1.9×**.

## When to surface
Use when students ask why long-context training is slow/memory-heavy, how IO-aware attention changes real GPU scaling, or for concrete speed/throughput comparisons (PyTorch vs Megatron-LM vs FlashAttention at 8K).