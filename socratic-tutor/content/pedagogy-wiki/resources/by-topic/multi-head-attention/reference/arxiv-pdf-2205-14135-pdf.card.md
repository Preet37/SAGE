# Card: FlashAttention (IO-aware exact attention via tiling)
**Source:** https://arxiv.org/pdf/2205.14135.pdf  
**Role:** paper | **Need:** DEPLOYMENT_CASE  
**Anchor:** IO-aware attention algorithm (tiling/blocking) that avoids materializing the \(N\times N\) attention matrix; measured speedups + linear-memory attention.

## Key Content
- **Standard attention equations (Section 2.2):**  
  \(S = QK^\top \in \mathbb{R}^{N\times N}\), \(P=\mathrm{softmax}(S)\) (row-wise), \(O=PV \in \mathbb{R}^{N\times d}\), with \(Q,K,V\in\mathbb{R}^{N\times d}\). Standard implementations **materialize** \(S\) and \(P\) in HBM \(\Rightarrow O(N^2)\) memory.
- **Why IO-aware (Section 1–2):** attention is often **memory-bandwidth-bound** (HBM much slower than on-chip SRAM). Example A100: HBM \(\sim 1.5\!-\!2.0\) TB/s vs SRAM bandwidth \(\sim 19\) TB/s; SRAM is tiny (per-SM 192KB; figure also notes ~20MB total SRAM).
- **FlashAttention algorithm (Algorithm 1, Section 3.1):**  
  Tile \(Q\) into \(T_r=\lceil N/B_r\rceil\) blocks and \(K,V\) into \(T_c=\lceil N/B_c\rceil\) blocks. Outer loop over \(K_j,V_j\) blocks loaded to SRAM; inner loop over \(Q_i\) blocks. Compute block scores \(S_{ij}=Q_iK_j^\top\), then **online softmax** using per-row stats: rowmax \(\tilde m_{ij}\), rowsum \(\tilde \ell_{ij}\); update running \(m_i,\ell_i\) and accumulate \(O_i\) with correct renormalization. Store only \(O\) and \((m,\ell)\) for backward; **recompute** attention blocks on-chip in backward (selective checkpointing).
  Block sizes: \(B_c=\lceil M/(4d)\rceil\), \(B_r=\min(\lceil M/(4d)\rceil, d)\) where \(M\)=SRAM size.
- **Complexity (Theorem 2):**  
  Standard attention HBM accesses: \(\Theta(Nd + N^2)\).  
  FlashAttention HBM accesses: \(\Theta(N^2 d^2 / M)\).  
  Lower bound: no exact attention can do \(o(N^2 d^2/M)\) HBM accesses for all \(M\in[d,Nd]\) (Proposition 3).
- **Empirical speed/memory (Figures/Tables):**
  - GPT-2 medium attention (N=1024, d=64, 16 heads, batch 64, A100): **HBM R/W 40.3GB → 4.4GB**, runtime **41.7ms → 7.3ms** (Fig. 2 left).  
  - Reported attention-kernel speedup up to **7.6×** vs PyTorch on GPT-2 attention compute (Fig. 1 right).  
  - End-to-end training: **BERT-large (seq 512) 20.0±1.5 min → 17.4±1.4 min** (15% faster than MLPerf 1.1 record, Table 1).  
  - GPT-2 medium training on 8×A100: HuggingFace **21.0 days** vs FlashAttention **6.9 days (3.0×)** (Table 2).  
  - Memory footprint scales **linearly** in \(N\); up to **20×** more memory-efficient than exact attention baselines (Fig. 3 right).

## When to surface
Use when students ask why attention is slow on GPUs, why “quadratic” attention can still be bandwidth-bound, or how FlashAttention achieves exact attention faster/with linear memory (tiling + online softmax + recomputation).