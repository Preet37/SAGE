# Card: FlashAttention benchmarks & IO-aware exact attention
**Source:** https://proceedings.neurips.cc/paper_files/paper/2022/file/67d57c32e20fd0a7a302cb81d36e40d5-Paper-Conference.pdf  
**Role:** benchmark | **Need:** EMPIRICAL_DATA  
**Anchor:** Benchmark tables/figures with exact speedups + memory savings vs standard attention; ablations tied to IO-aware tiling.

## Key Content
- **Standard attention equations (Section 2.2):**  
  \(Q,K,V\in\mathbb{R}^{N\times d}\).  
  \(S=QK^\top\in\mathbb{R}^{N\times N}\); \(P=\mathrm{softmax}(S)\) (row-wise); \(O=PV\in\mathbb{R}^{N\times d}\).  
  Standard implementations materialize \(S,P\) in HBM → \(O(N^2)\) memory.
- **FlashAttention design (Section 3.1, Alg. 1):** IO-aware **tiling** + **recomputation**; fuse matmul→softmax(+mask/dropout)→matmul in one CUDA kernel; avoid writing \(N\times N\) attention matrix to HBM. Stores output \(O\) and softmax stats \((m,\ell)\) for backward recomputation (selective checkpointing).
- **Softmax block aggregation (Section 3.1):** track per-row \(m(x)=\max_i x_i\), \(\ell(x)=\sum_i e^{x_i-m(x)}\) to combine blocks exactly.
- **IO complexity (Theorem 2):** with SRAM size \(M\), head dim \(d\):  
  Standard attention HBM accesses \(\Theta(Nd+N^2)\).  
  FlashAttention HBM accesses \(\Theta(N^2 d^2 / M)\).  
  Lower bound: no exact algorithm can do \(o(N^2 d^2/M)\) HBM accesses for all \(M\in[d,Nd]\) (Prop. 3).
- **Concrete benchmark (Fig. 2 left, A100; \(N{=}1024,d{=}64\), 16 heads, batch 64):**  
  Standard: **66.6 GFLOPs**, **35.3 GB HBM R/W**, **35.1 ms** (fwd+bwd).  
  FlashAttention: **75.2 GFLOPs**, **4.4 GB HBM R/W**, **11.7 ms**.
- **End-to-end training results:**  
  **BERT-large, seq 512 (Table 1, 8×A100):** 20.0±1.5 min (NVIDIA MLPerf 1.1) vs **17.4±1.4 min** (FlashAttention) → **15% faster**.  
  **GPT-2 small/medium, seq 1K (Table 2, 8×A100):** small **9.5d→2.7d (3.5×)** vs HF; medium **21.0d→6.9d (3.0×)**; same ppl (18.2 / 14.2).  
  **Long-Range Arena (Table 3):** FlashAttention avg **59.8** with **2.4×** speedup; block-sparse FlashAttention **2.8×**.
- **Long-context quality (Table 4):** GPT-2 small FlashAttention: context **4K** ppl **17.2**, **3.6d (1.3×)** vs Megatron 1K ppl 18.2, 4.7d; reported **0.7 ppl** improvement.
- **Memory scaling (Fig. 3 right):** FlashAttention memory footprint **linear in \(N\)**; up to **20×** more memory-efficient than exact attention baselines; at 64K still **2×** more efficient than Linformer.

## When to surface
Use for questions about *why FlashAttention is faster*, *HBM/IO vs FLOPs*, and for *exact numeric speed/memory comparisons* across sequence lengths, GPUs (A100), and training benchmarks (BERT, GPT-2, LRA).