# Card: Float8 + FSDP2 throughput scaling (LLaMA3, H100)
**Source:** https://pytorch.org/blog/training-using-float8-fsdp2/  
**Role:** benchmark | **Need:** API_REFERENCE / DEPLOYMENT_CASE  
**Anchor:** Concrete tokens/sec/GPU gains (wps), scaling to 512 H100s, and operational recipe: FSDP2 + DTensor + torch.compile + torchao float8 (+ float8 all_gather)

## Key Content
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

## When to surface
Use when students ask for **real throughput/MFU-style evidence** of float8 benefits, or how to **combine float8 with FSDP2/DTensor/torch.compile** (including comm via **float8 all_gather**) and what speedups to expect at **70B–405B** and **512-GPU** scale.