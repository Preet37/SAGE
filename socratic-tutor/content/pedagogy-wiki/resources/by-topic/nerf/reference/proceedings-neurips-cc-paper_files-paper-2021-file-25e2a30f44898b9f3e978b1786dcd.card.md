# Card: VolSDF—Bridge NeRF Volume Rendering ↔ SDF Surfaces
**Source:** https://proceedings.neurips.cc/paper_files/paper/2021/file/25e2a30f44898b9f3e978b1786dcd85c-Paper.pdf  
**Role:** paper | **Need:** COMPARISON_DATA  
**Anchor:** Differentiable volume rendering where density is a transformed SDF (explicit surface + better sampling + disentanglement)

## Key Content
- **SDF + density parameterization (Section 3.1):**  
  - Indicator + SDF (Eq. 1): \(1_\Omega(x)\in\{0,1\}\), \(d_\Omega(x)=(-1)^{1_\Omega(x)}\min_{y\in M}\|x-y\|\), \(M=\partial\Omega\).  
  - Density from SDF (Eq. 2–3): \(\sigma(x)=\alpha\,\Psi_\beta(-d_\Omega(x))\), \(\alpha,\beta>0\).  
    Laplace CDF \(\Psi_\beta(s)=\tfrac12 e^{s/\beta}\) if \(s\le0\); else \(1-\tfrac12 e^{-s/\beta}\).  
  - As \(\beta\to0\): \(\sigma\to \alpha 1_\Omega\) away from the surface ⇒ **surface is zero level-set of SDF** (principled extraction vs arbitrary density threshold).
- **Volume rendering equations (Section 3.2):**  
  Ray \(x(t)=c+tv\). Transparency (Eq. 4) \(T(t)=\exp(-\int_0^t \sigma(x(s))ds)\); opacity (Eq. 5) \(O(t)=1-T(t)\).  
  PDF (Eq. 6) \(\tau(t)=\frac{dO}{dt}=\sigma(x(t))T(t)\).  
  Pixel color (Eq. 7): \(I(c,v)=\int_0^\infty L(x(t),n(t),v)\tau(t)\,dt\), with normal \(n(t)=\nabla_x d_\Omega(x(t))\).  
  Quadrature (Eq. 8): \(\hat I_S=\sum_{i=1}^{m-1}\hat\tau_i L_i\).
- **Opacity approximation error bound + sampling (Section 3.3–3.4):**  
  Rectangle rule (Eq. 9–10) defines \(\hat O(t)=1-\exp(-\hat R(t))\).  
  Density derivative bound (Thm 1, Eq. 11): \(|\frac{d}{ds}\sigma(x(s))|\le \frac{\alpha}{2\beta}\exp(-d_i^*/\beta)\) (uses SDF geometry).  
  Error bound (Eq. 12–15) yields uniform bound \(B_{T,\beta}\) on \(|O-\hat O|\).  
  **Algorithm 1:** start uniform \(n=128\) samples \(T_0\); set \(\beta^+>\beta\) via Lemma 2 (Eq. 16) to ensure \(B_{T,\beta^+}\le\epsilon\); iteratively upsample intervals proportional to error; bisection (≤10 iters) to reduce \(\beta^+\to\beta\); max 5 outer iters; then inverse-CDF sample \(m=64\) points from \(\hat O^{-1}\). Typical \(\beta=0.001\), \(\epsilon=0.1\).
- **Training pipeline (Section 3.5):**  
  Two MLPs: geometry \(f_\phi(x)=(d(x),z(x))\in\mathbb R^{1+256}\); radiance \(L_\psi(x,n,v,z)\in\mathbb R^3\). Learn \(\beta\) (implementation sets \(\alpha=\beta^{-1}\)). Positional encoding for \(x,v\).  
  Loss (Eq. 17–18): \(L=L_{\text{RGB}}+\lambda L_{\text{SDF}}\); \(L_{\text{RGB}}=\mathbb E_p\|I_p-\hat I_S(c_p,v_p)\|_1\).  
  Eikonal \(L_{\text{SDF}}=\mathbb E_z(\|\nabla d(z)\|-1)^2\), with \(z\) sampled as (1 uniform 3D point + 1 point from \(S\)) per pixel. Batch=1024 pixels; \(\lambda=0.1\).
- **Empirical comparisons:**  
  **DTU (Table 1):** Mean Chamfer \(l_1\) (mm): VolSDF **0.86**, IDR 0.90, NeRF 1.89, COLMAP 0 1.36, COLMAP 7 0.65. Mean PSNR: NeRF 30.65 vs VolSDF 30.38.  
  **BlendedMVS (Table 2):** Mean Chamfer improvement vs NeRF: **51.8%**; Mean PSNR: NeRF++ 27.55 vs VolSDF 27.08.  
  **Disentanglement (Section 4.2):** swapping radiance fields works for VolSDF; fails for NeRF (even with normal-conditioned radiance).

## When to surface
Use when students ask how to connect NeRF-style volume rendering to **implicit surfaces/SDFs**, how to **extract clean geometry**, or how **sampling/error bounds** improve rendering and disentanglement.