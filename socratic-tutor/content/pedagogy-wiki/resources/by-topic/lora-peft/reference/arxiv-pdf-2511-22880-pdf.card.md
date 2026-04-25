# Card: LoRAServe—rank-aware distributed serving for heterogeneous LoRA
**Source:** https://www.arxiv.org/pdf/2511.22880.pdf  
**Role:** paper | **Need:** DEPLOYMENT_CASE  
**Anchor:** Cluster-level design to serve many LoRA adapters with heterogeneous ranks; quantifies rank interference + dynamic placement/routing + RDMA-based remote adapter access.

## Key Content
- **Problem (rank heterogeneity interference):** Multi-tenant LoRA kernels (Punica BGMV, S-LoRA MBGMV) size compute tiles/pipelines to the **maximum rank in the batch**, so low-rank requests “pay” for high-rank ones → tail latency skew. Example (Sec. I/III-A5, Fig.1): co-serving **rank-8 + rank-128** on Llama-7B increases **P95 TTFT of rank-8 by 84%** vs serving only rank-8.
- **SLO impact:** Common SLO cited: **P95 TTFT < 10s** (Sec. III-A4). Under a **4 RPS Poisson** workload with **P95 TTFT SLO=20s**, **ranks 64/128 violate SLO** while smaller ranks do not (Fig.6).
- **Scaling effects:** Rank heterogeneity penalty grows with model size: up to **45% degradation on Llama-70B** (Sec. III-A2). Tensor parallelism reduces but doesn’t remove it: with **TP=8**, rank-128 still causes **~20% TTFT increase** vs rank-8 on Llama-7B (Sec. III-A3).
- **Memory pressure numbers:** For a **200B** model quantized to **8-bit**, base size ≈ **200GB**; LoRA adapters ≈ **1%** of model → **~2GB/adapter**; **500 adapters ≈ 1TB** if replicated per server (Sec. I).
- **LoRAServe architecture (Sec. IV):** Cluster orchestrator maintains routing table with tuples **(adapter a, servers S, probabilities p)**; route to server *s* with probability **p_s**, with **∑_{s∈S} p_s = 1**. If adapter absent locally, fetch from remote server via **GPUDirect RDMA over InfiniBand**, then cache in host memory.
- **Placement algorithm (Alg.1, Sec. IV-A):** Per timestep: (1) estimate **TPS demand per adapter**; (2) compute per-rank server budget using profiled **rank operating points under SLO** (max TPS per rank); (3) **fractional bin packing** for ranks with budget; (4) place remaining adapters on servers with higher max-rank capacity; (5) **permute to minimize deviation** from previous placement; (6) update routing + metadata.
- **Empirical gains (Abstract/Sec. V-F):** On Company X traces: up to **2× throughput**, up to **9× lower TTFT**, and up to **50% fewer GPUs** vs SOTA; reduces per-server adapter storage footprint up to **16×** vs Toppings.

## When to surface
Use for questions about **serving many LoRA adapters in production**, especially **why heterogeneous ranks hurt latency/throughput**, and **how to place/route/migrate adapters across a GPU cluster under TTFT SLOs**.