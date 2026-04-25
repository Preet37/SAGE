# Card: MoE-Inference-Bench (MoE inference performance + routing/imbalance effects)
**Source:** https://www.arxiv.org/pdf/2508.17467.pdf  
**Role:** benchmark | **Need:** EMPIRICAL_DATA  
**Anchor:** Stable benchmark figures/tables on routing (Top‑k/active experts), imbalance, and end‑to‑end inference performance (H100, vLLM)

## Key Content
- **Metrics & formulas (Section 3.4):**
  - **TTFT**: time from prompt receipt to first generated token (measured by setting max output length = 1).
  - **ITL (Eq. 1)**: average time between consecutive generated tokens (per-token decode latency).
  - **Throughput (Eq. 2)**: tokens/sec computed from end-to-end latency:  
    \[
    \text{Throughput}=\frac{\text{#input tokens}+\text{#output tokens}}{\text{end-to-end latency (s)}}
    \]
  - **VLM metric:** samples/sec (image+text samples processed per second).
- **Experimental defaults (Sections 3.2–3.3):** input/output lengths ∈ {128, 256, 512, 1024, 2048}; batch sizes ∈ {1, 16, 32, 64}. Hardware: **NVIDIA H100 SXM5 80GB**, framework **vLLM**.
- **Model architecture table (Table 1 examples):**
  - **Mixtral‑8×7B:** 32 layers, d_model 4096, FFN 14336, **8 experts**, **Top‑k=2**, total params **47B**, active params **12.9B**.
  - **Qwen3‑30B‑A3B:** 48 layers, **128 experts**, **Top‑k=8**, total **30.5B**, active **3.3B**.
  - **OLMoE‑1B‑7B:** 16 layers, **64 experts**, **Top‑k=8**, total **7.2B**, active **1.3B**.
- **Empirical routing/Top‑k effects (Figure 5):** throughput **decreases as active experts increase**; for **DeepSeek‑V2‑Lite**, active experts 1→32 causes ~**15–20%** throughput drop at large batches (64/128) vs **5–8%** at small batches (1/16). **Qwen1.5‑MoE‑A2.7B**: ~**12–18%** (large) vs **4–7%** (small).
- **Sequence length effects (Figure 6):** at large batches, length **128** yields up to **~30%** higher throughput than **2048**; long lengths (1024–2048) degrade throughput **>20%** (DeepSeek‑V2‑Lite).
- **Hyperparameter scaling (Section 5):**
  - **FFN dim 1792→14336**: throughput drops **~50% avg** (Figure 7); at FFN=14336, **1 vs 8 active experts** gap ~**60%**.
  - **Active experts 1→8**: **50–80%** higher throughput for single-expert vs 8-expert configs (Figure 9), especially at large FFNs.
- **Optimization results:**
  - **FP8 vs FP16 (Figure 10):** FP8 gives **~20–25%** throughput gain across lengths; up to **~25–30%** at highest batch size.
  - **Fused MoE (Figure 14):** **~15–20%** higher throughput when scaling batch size; **~12–18%** across sequence lengths.
- **Load balancing evidence (Figure 15):** DeepSeek‑VL2 shows **uniform expert activation**; MolmoE‑1B shows skew (peaks **~1M** activations vs DeepSeek‑VL2 peak **~290K**). DeepSeek‑V2 uses an **auxiliary loss** to balance expert utilization.

## When to surface
Use for questions about how **Top‑k/active experts, FFN size, batch/sequence length** affect MoE inference throughput/latency, and for concrete **H100+vLLM** gains from **FP8** and **Fused MoE**, plus evidence of **expert imbalance vs balanced routing**.