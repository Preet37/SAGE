# Card: Perspective-projected EWA Gaussian splat footprint (screen-space conic)
**Source:** https://www.cs.umd.edu/~zwicker/publications/EWASplatting-TVCG02.pdf  
**Role:** paper | **Need:** FORMULA_SOURCE  
**Anchor:** Derivation of perspective-projected elliptical Gaussian footprint (screen-space quadratic/conic) + EWA resampling (reconstruction ⊗ low-pass) equations.

## Key Content
- **Reconstruction in source space (Eq. 1):**  
  \(f_c(u)=\sum_k w_k\, r_k(u)\). Rendering treated as **projection + prefilter + sampling** (Sec. 3.3).
- **Ideal resampling kernel (Eq. 6):**  
  \(g'_c(x)=\sum_k w_k\,\varphi_k(x)\), with \(\varphi_k(x)=(p_k*h)(x)\), \(p_k=P\,r_k\).
- **Elliptical Gaussian definitions (Eqs. 19–20):**  
  \(G^3_V(x-p)=\frac{1}{(2\pi)^{3/2}|V|^{1/2}}\exp\!\left(-\tfrac12(x-p)^T V^{-1}(x-p)\right)\).  
  \(G^2_V(x-p)=\frac{1}{2\pi|V|^{1/2}}\exp\!\left(-\tfrac12(x-p)^T V^{-1}(x-p)\right)\).
- **Gaussian properties used (Eqs. 21–23):** affine map \(u=Mx+c\):  
  \(G^n_V(\phi^{-1}(u)-p)=\frac{1}{|M^{-1}|}G^n_{MVM^T}(u-\phi(p))\).  
  Convolution: \(G_V*G_Y=G_{V+Y}\).  
  Integrate 3D→2D: \(\int G^3_V\,dx_2 = G^2_{\hat V}\) where \(\hat V\) is \(V\) with 3rd row/col removed (Eq. 24).
- **Perspective to ray space (Eqs. 26–29):**  
  \(x=\Psi(t)=(t_0/t_2,\ t_1/t_2,\ \|t\|)^T\). Use **local affine approximation** at \(t_k\):  
  \(\Psi_k(t)=x_k+J_k(t-t_k)\), \(J_k=\partial\Psi/\partial t|_{t_k}\) (Eq. 29).
- **Projected 3D kernel variance in ray space (Eq. 31):**  
  \(V'_k = J_k\,W\,V_k\,W^T\,J_k^T\) (view rotation \(W\)).  
  **Footprint (Eq. 32):** \(q_k(x)=\frac{1}{|W^{-1}J_k^{-1}|}\,G^2_{\hat V'_k}(x-x_k)\).
- **EWA volume resampling filter / splat (Eq. 33):** choose low-pass \(h(x)=G_{V_h}(x)\) (typically \(V_h=I_{2\times2}\)):  
  \(\varphi_k(x)=c_k o_k \frac{1}{|W^{-1}J_k^{-1}|}\,G^2_{\hat V'_k+V_h}(x-x_k)\).
- **Rasterization (Sec. 7.1.2):** conic \(Q=(\hat V'_k+V_h)^{-1}\); radial index \(r(\Delta x)=\Delta x^T Q \Delta x\). Use LUT for \(\exp(-\tfrac12 r)\); evaluate within threshold **\(r<c\), typically \(c=4\)**; finite differencing (biquadratic → 2 adds/pixel).
- **Empirical comparison (Sec. 8):** EWA vs uniform scaling [Swan18] on anisotropic kernels (major:minor **2:1** and **4:1**)—EWA “crisper” without aliasing; uniform scaling overly blurry. Reported render times: ~**6 s/frame** (zebra test) and ~**11 s/frame** (CT head/engine/foot) on **866 MHz PIII**.

## When to surface
Use when students ask how 3D Gaussians become **screen-space ellipses/conics under perspective**, or how **EWA splatting** combines reconstruction + low-pass filtering to avoid aliasing (including the exact variance/conic formulas and rasterization threshold).