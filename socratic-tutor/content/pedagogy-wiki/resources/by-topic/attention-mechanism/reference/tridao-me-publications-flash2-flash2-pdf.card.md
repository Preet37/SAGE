# Card: FlashAttention-2 (exact IO-aware attention via tiling + online softmax)
**Source:** https://tridao.me/publications/flash2/flash2.pdf  
**Role:** paper | **Need:** FORMULA_SOURCE  
**Anchor:** Block/tiling scheme for exact attention; online softmax with running \((m,\ell)\) / logsumexp \(L\); recomputation to avoid materializing \(N\times N\) attention.

## Key Content
- **Standard attention (Sec. 2.2):** Given \(Q,K,V\in\mathbb{R}^{N\times d}\):  
  \(S=QK^\top\in\mathbb{R}^{N\times N}\), \(P=\mathrm{softmax}(S)\) (row-wise), \(O=PV\in\mathbb{R}^{N\times d}\).  
  Backward: \(dV=P^\top dO\); \(dP=dOV^\top\); \(dS=\mathrm{dsoftmax}(dP)\); \(dQ=dSK\); \(dK=QdS^\top\).
- **FlashAttention-2 forward algorithm (Alg. 1, Sec. 3.1.1):** Tile rows/cols: \(T_r=\lceil N/B_r\rceil\), \(T_c=\lceil N/B_c\rceil\). For each row block \(Q_i\): init on-chip \(O_i^{(0)}=0\), \(\ell_i^{(0)}=0\), \(m_i^{(0)}=-\infty\). For each col block \(K_j,V_j\):  
  \(S_{ij}=Q_iK_j^\top\). Update running row-wise max and exp-sum:  
  \(m_i^{(j)}=\max(m_i^{(j-1)}, \mathrm{rowmax}(S_{ij}))\); \(\tilde P_{ij}=\exp(S_{ij}-m_i^{(j)})\);  
  \(\ell_i^{(j)}=\exp(m_i^{(j-1)}-m_i^{(j)})\ell_i^{(j-1)}+\mathrm{rowsum}(\tilde P_{ij})\).  
  Update unnormalized output: \(O_i^{(j)}=\mathrm{diag}(\exp(m_i^{(j-1)}-m_i^{(j)}))O_i^{(j-1)}+\tilde P_{ij}V_j\).  
  Final: \(O_i=\mathrm{diag}((\ell_i^{(T_c)})^{-1})O_i^{(T_c)}\); store \(L_i=m_i^{(T_c)}+\log(\ell_i^{(T_c)})\) (logsumexp).
- **Rationale (Sec. 3.1):** Reduce expensive non-matmul FLOPs (A100: 312 TFLOPs/s FP16/BF16 matmul vs 19.5 TFLOPs/s FP32 non-matmul; ~16× gap). Keep \(O\) unscaled until end; store only \(L\) (not both \(m,\ell\)).
- **Memory/compute:** Exact output (no approximation); avoids materializing \(S,P\) in HBM; **extra memory \(O(N)\)** (store \(L\)); FLOPs \(O(N^2 d)\) (Sec. 3.1.1).
- **Causal mask (Sec. 3.1.1):** Skip blocks entirely above diagonal (~half blocks) → ~**1.7–1.8×** speedup vs non-causal; per row apply mask to only ~1 block (square blocks).
- **Parallelism/work partitioning (Secs. 3.2–3.3):** Forward parallelize over row blocks (sequence length) + batch + heads; backward parallelize over column blocks; atomic adds for \(dQ\). Avoid “split-K”: FlashAttn-2 splits **Q across warps** (K,V shared) to reduce shared-memory traffic.
- **Empirical (A100 80GB, Sec. 4.1):** FlashAttention-2 **1.7–3.0×** faster than FlashAttention; **3–10×** faster than PyTorch attention; forward reaches **up to 73%** of theoretical peak; end-to-end training up to **225 TFLOPs/s per A100** (72% MFU) (Table 1).

## When to surface
Use when students ask how FlashAttention computes **exact** attention with **linear memory**, how **online softmax/logsumexp** enables tiling, or what concrete speedups/throughput FlashAttention-2 achieves vs baselines.