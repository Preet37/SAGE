# Card: Scaling laws (Kaplan et al. 2020) — loss vs N/D/compute
**Source:** https://arxiv.org/pdf/2001.08361.pdf  
**Role:** paper | **Need:** FORMULA_SOURCE  
**Anchor:** Primary fitted scaling-law functional forms for loss vs model size/data/compute (power laws + compute-efficient frontier), plus fitting methodology/constants.

## Key Content
- **Notation (Sec. 1.3):**  
  - *L* = cross-entropy loss (nats/token).  
  - *N* = **non-embedding** parameter count.  
  - *D* = dataset size (tokens).  
  - *B* = batch size (tokens); *S* = optimizer steps.  
  - Training compute: **C ≈ 6 N B S** FLOPs (non-embedding); 1 PF-day = 8.64×10¹⁹ FLOPs.
- **Single-factor scaling (Sec. 1.2, Eq. 1.1–1.3):**  
  - **Model-limited (converged, large D):** \(L(N)=(N_c/N)^{\alpha_N}\), with **αN≈0.076**, **Nc≈8.8×10¹³**.  
  - **Data-limited (early-stopped, large N):** \(L(D)=(D_c/D)^{\alpha_D}\), with **αD≈0.095**, **Dc≈5.4×10¹³** tokens.  
  - **Compute-efficient frontier:** \(L(C_{min})=(C^c_{min}/C_{min})^{\alpha^C_{min}}\), with **α≈0.050**, **C^c≈3.1×10⁸ PF-days**.
- **Joint overfitting law (Eq. 1.5 / 4.1):**  
  \[
  L(N,D)=\Big[(N_c/N)^{\alpha_N/\alpha_D}+D_c/D\Big]^{\alpha_D}
  \]
  Overfitting depends on ratio \(N^{\alpha_N/\alpha_D}/D\); implies **D ∝ N^(αN/αD) ≈ N^0.74** to avoid penalty.
- **Learning curve fit (Eq. 1.6 / 5.6):**  
  \(L(N,S_{min})=(N_c/N)^{\alpha_N}+(S_c/S_{min})^{\alpha_S}\) with **αS≈0.76**, **Sc≈2.1×10³**, **αN≈0.077**, **Nc≈6.5×10¹³** (Table 3).
- **Batch-size/critical batch (Eq. 1.4, 5.1–5.5):**  
  - \(B_{crit}(L)=B^* L^{1/\alpha_B}\), **B*≈2×10⁸ tokens**, **αB≈0.21**.  
  - Step/epoch tradeoff at fixed L: \((S/S_{min}-1)(E/E_{min}-1)=1\), \(E=BS\).  
  - Adjustments: \(S_{min}=S/(1+B_{crit}/B)\); \(C_{min}=C/(1+B/B_{crit})\).
- **Compute-optimal allocations (Eq. 1.7–1.8; Sec. 6):**  
  - \( \alpha^C_{min}=1/(1/\alpha_S+1/\alpha_B+1/\alpha_N)\) ≈ **0.054** (Eq. 6.4).  
  - Empirical: **N ∝ Cmin^0.73**, **B ∝ Cmin^0.24**, **S ∝ Cmin^0.03** (Sec. 1.2, Fig. 14).

## When to surface
Use when students ask “how does loss scale with parameters/data/compute?”, “what’s the compute-optimal model/data tradeoff?”, or “how to adjust for batch size / critical batch in scaling-law fits.”