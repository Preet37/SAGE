# Card: FlashAttention — IO-aware exact scaled dot-product attention
**Source:** https://proceedings.neurips.cc/paper_files/paper/2022/file/67d57c32e20fd0a7a302cb81d36e40d5-Paper-Conference.pdf  
**Role:** benchmark | **Need:** EMPIRICAL_DATA  
**Anchor:** Benchmark tables/figures comparing speed & memory vs standard attention; IO-aware tiling algorithm; “exact attention” claim.

## Key Content
- **Standard attention math (Section 2.2):**  
  - Inputs: \(Q,K,V \in \mathbb{R}^{N\times d}\) (sequence length \(N\), head dim \(d\)).  
  - \(S = QK^\top \in \mathbb{R}^{N\times N}\)  
  - \(P = \mathrm{softmax}(S)\) (row-wise)  
  - \(O = PV \in \mathbb{R}^{N\times d}\)  
  - Standard implementations **materialize** \(S\) and \(P\) in HBM ⇒ \(O(N^2)\) memory.
- **Numerically stable softmax + blockwise decomposition (Section 3.1):**  
  - For vector \(x\): \(m(x)=\max_i x_i\); \(f(x)=\exp(x-m(x))\); \(\ell(x)=\sum_i f(x)_i\); \(\mathrm{softmax}(x)=f(x)/\ell(x)\).  
  - For concatenation \(x=[x^{(1)},x^{(2)}]\):  
    \(m(x)=\max(m(x^{(1)}),m(x^{(2)}))\);  
    \(\ell(x)=e^{m(x^{(1)})-m(x)}\ell(x^{(1)})+e^{m(x^{(2)})-m(x)}\ell(x^{(2)})\).  
  - Enables **tiling**: compute softmax incrementally per block while tracking per-row \((m,\ell)\).
- **FlashAttention algorithm (Algorithm 1):**  
  - Choose block sizes: \(B_c=\lceil M/(4d)\rceil\), \(B_r=\min(\lceil M/(4d)\rceil,d)\) where \(M\)=SRAM size.  
  - Loop over \(K_j,V_j\) blocks (outer), then \(Q_i\) blocks (inner); compute \(S_{ij}=Q_iK_j^\top\), rowmax/rowsum stats, update running \((m_i,\ell_i)\), and update \(O_i\) without storing \(N\times N\).
  - **Recomputation rationale:** store only \(O\) and \((m,\ell)\) to recompute attention on-chip in backward, avoiding storing \(S,P\).
- **Exactness + complexity claims:**  
  - **Theorem 1:** returns **exact** \(O=\mathrm{softmax}(QK^\top)V\); FLOPs \(O(N^2d)\); extra memory \(O(N)\) beyond inputs/outputs.  
  - **Theorem 2 (IO):** Standard attention HBM accesses \(\Theta(Nd+N^2)\); FlashAttention \(\Theta(N^2 d^2/M)\).
- **Concrete benchmark numbers (Figure 2, A100, \(N{=}1024,d{=}64\), 16 heads, batch 64, padding mask, no dropout):**  
  - Standard vs FlashAttention: **GFLOPs** 66.6 vs 75.2; **HBM R/W (GB)** 35.3 vs 4.4; **runtime (ms)** 35.1 vs 11.7.
- **End-to-end training results:**  
  - **BERT-large seq 512 (Table 1, 8×A100):** 20.0±1.5 min (Nvidia MLPerf 1.1) vs **17.4±1.4 min** (FlashAttention) ⇒ **15% faster**.  
  - **GPT-2 small/medium seq 1K (Table 2, 8×A100):**  
    - Small: 9.5d (HF) vs 4.7d (Megatron) vs **2.7d (FlashAttention, 3.5×)**; ppl 18.2 all.  
    - Medium: 21.0d (HF) vs 11.5d (Megatron) vs **6.9d (FlashAttention, 3.0×)**; ppl 14.2 all.
- **Long-Range Arena (Table 3):** Avg accuracy 59.3 (Transformer) vs **59.8 (FlashAttention)** with **2.4× speedup**; block-sparse FlashAttention speedup **2.8×**.

## When to surface
Use when students ask why attention is memory/time bottlenecked on GPUs, how to compute **exact** softmax attention without storing \(N\times N\), or want **specific speed/memory benchmarks** comparing FlashAttention to standard attention.