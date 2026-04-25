# Card: FlashAttention benchmarks + IO-aware exact attention
**Source:** https://arxiv.org/pdf/2205.14135.pdf  
**Role:** benchmark | **Need:** EMPIRICAL_DATA  
**Anchor:** Benchmark tables/plots (speed, memory) + IO-aware tiling algorithm for exact attention

## Key Content
- **Standard scaled dot-product attention (Section 2.2):**  
  \(Q,K,V\in\mathbb{R}^{N\times d}\) (sequence length \(N\), head dim \(d\)).  
  \(S = QK^\top \in \mathbb{R}^{N\times N}\); \(P=\mathrm{softmax}(S)\) row-wise; \(O=PV\in\mathbb{R}^{N\times d}\).  
  Standard implementations **materialize** \(S\) and \(P\) in HBM → \(O(N^2)\) memory.
- **FlashAttention algorithm (Algorithm 1, Section 3.1):** IO-aware **tiling** to avoid storing \(N\times N\).  
  Block sizes from SRAM \(M\): \(B_c=\lceil M/(4d)\rceil\), \(B_r=\min(\lceil M/(4d)\rceil,d)\).  
  Maintain per-row softmax stats in HBM: \(m\in\mathbb{R}^N\) (max), \(\ell\in\mathbb{R}^N\) (sum of exp).  
  For each KV block \(j\): load \(K_j,V_j\) to SRAM; for each Q block \(i\): load \(Q_i,O_i,\ell_i,m_i\); compute \(S_{ij}=Q_iK_j^\top\); update \(\tilde m,\tilde \ell\); combine with stable update \(m_i^{new}=\max(m_i,\tilde m_{ij})\), \(\ell_i^{new}=e^{m_i-m_i^{new}}\ell_i + e^{\tilde m_{ij}-m_i^{new}}\tilde\ell_{ij}\); update \(O_i\) accordingly; write back \(O,\ell,m\).  
  **Kernel fusion:** matmul + softmax (+ mask/dropout) + matmul in one CUDA kernel.
- **Numerical stability (Section 3.1):** softmax via \(m(x)=\max_i x_i\), \(f_i=e^{x_i-m(x)}\), \(\ell=\sum_i f_i\), \(\mathrm{softmax}(x)=f/\ell\); supports blockwise aggregation by tracking \((m,\ell)\).
- **IO complexity (Theorem 2, Section 3.2):**  
  Standard attention HBM accesses: \(\Theta(Nd + N^2)\).  
  FlashAttention HBM accesses: \(\Theta(N^2 d^2 / M)\) for \(d\le M\le Nd\).  
  Lower bound: no exact algorithm can do \(o(N^2 d^2/M)\) HBM accesses for all \(M\) (Proposition 3).
- **Concrete benchmark (Figure 2, GPT-2 medium, \(N{=}1024,d{=}64\), 16 heads, batch 64, A100):**  
  Standard vs FlashAttention: **HBM R/W 40.3 GB → 4.4 GB**, **runtime 41.7 ms → 7.3 ms** (fwd+bwd), **GFLOPs 66.6 → 75.2** (more FLOPs but faster due to less IO).
- **End-to-end training speedups:**  
  BERT-large seq 512: **20.0±1.5 min (Nvidia MLPerf 1.1) vs 17.4±1.4 min (FlashAttention)** (Table 1, ~15% faster).  
  GPT-2 medium: **21.0 days (HF) vs 6.9 days (FlashAttention)** = **3.0×** (Table 2).  
  LRA avg accuracy similar; FlashAttention **2.4×** speedup (Table 3).
- **Memory scaling (Figure 3):** FlashAttention memory footprint grows **linearly** in \(N\); reported **up to 20×** more memory-efficient than exact attention baselines; enables long contexts up to **64K**.

## When to surface
Use when students ask why attention is memory-bound, how FlashAttention computes **exact** softmax attention without storing \(N\times N\), or when they need **specific speed/memory numbers** comparing standard attention vs FlashAttention across sequence lengths/models.