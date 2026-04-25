# Card: Production FSDP scaling + throughput/MFU/HFU (Llama2-7B)
**Source:** https://pytorch.org/blog/maximizing-training/  
**Role:** benchmark | **Need:** DEPLOYMENT_CASE  
**Anchor:** Production-style FSDP scaling metrics + techniques to reach 3,700 tok/s/GPU and near-linear scaling to 512 GPUs

## Key Content
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

## When to surface
Use when students ask how to **measure/interpret MFU vs HFU**, how to reach **production-grade FSDP throughput**, or what **specific knobs (FlashAttention, overlap, activation checkpointing, batch sizing, LR/AdamW settings)** enabled near-linear scaling to hundreds of GPUs.