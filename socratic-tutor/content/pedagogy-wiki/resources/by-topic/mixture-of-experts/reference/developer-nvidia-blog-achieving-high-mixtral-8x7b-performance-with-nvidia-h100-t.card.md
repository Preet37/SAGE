# Card: Mixtral 8x7B inference on H100 + TensorRT-LLM (throughput/latency, FP8, batching)
**Source:** https://developer.nvidia.com/blog/achieving-high-mixtral-8x7b-performance-with-nvidia-h100-tensor-core-gpus-and-tensorrt-llm/  
**Role:** benchmark | **Need:** DEPLOYMENT_CASE  
**Anchor:** Production-oriented Mixtral 8x7B serving results + system optimizations (TensorRT-LLM on 2× H100 SXM), with FP16 vs FP8 comparisons.

## Key Content
- **MoE routing (Mixtral 8x7B, quoted from paper):** Each layer has **8 experts (FFN blocks)**; for **every token at each layer**, a **router selects top-2 experts** and **combines outputs** (weighted).  
  - **Capacity vs active params:** token has access to **47B parameters**, but uses **13B active parameters** during inference (due to sparse top-2 routing).
- **Serving workflow / design choices:**
  - **In-flight batching:** during serving, **completed requests are replaced with new requests** to improve throughput under latency targets.
  - **Deployment tuning rationale:** choose a **response-time budget** by examining the **throughput–latency curve**; production targets often sit in a “steep” region where **small latency increases yield large throughput gains**.
- **Benchmark configuration (key defaults):**
  - **Hardware/software:** **2× NVIDIA H100 SXM**, **TensorRT-LLM v0.10**, **CUDA 12.4 (12.4.131)**.
  - **Parallelism:** **Tensor Parallel (TP)=2**.
  - **Online test lengths:** **Avg ISL=573**, **Avg OSL=50**.
  - **Offline test lengths:** **ISL=128**, **OSL=128**; batch sizes swept up to **1024**.
- **Empirical results (specific numbers):**
  - **FP8 benefit (online):** **~50% more throughput** than FP16 **within a 0.5 s response limit** (H100 FP8 vs FP16).
  - **Streaming mode point:** at **mean time/output token = 0.016 s** (~**>60 tok/s** per user), **2×H100 FP8** achieves **38.4 requests/s**.
  - **Offline peak:** at **batch size 1024**, throughput reaches **~21,000 tokens/s** with **FP8**.
- **Why FP8:** H100 **4th-gen Tensor Cores** support **FP8 at ~2× peak compute** vs FP16/BF16; FP8 also **reduces memory footprint**, enabling larger batches.

## When to surface
Use when students ask how MoE (Mixtral) affects inference cost/latency, how to pick latency targets vs throughput, or what concrete H100+TensorRT-LLM FP8 serving numbers/configs look like (streaming, batching, offline throughput).