# Card: NeRF Volume Rendering (MIT Vision Book Ch.45)
**Source:** https://visionbook.mit.edu/nerf.html  
**Role:** explainer | **Need:** FORMULA_SOURCE  
**Anchor:** Clean derivation + discretization of radiance-field image formation (radiance, density, transmittance)

## Key Content
- **Radiance field definition (Sec. 45.2):**  
  \(L: (X,Y,Z,\psi,\phi)\rightarrow (r,g,b,\sigma)\).  
  Subcomponents: \(L^c:(X,Y,Z,\psi,\phi)\rightarrow (r,g,b)\), \(L^\sigma:(X,Y,Z,\psi,\phi)\rightarrow \sigma\).  
  Modeling choice: **color depends on view direction**, density typically **direction-independent**.
- **Volume rendering equation (Eq. 45.1):**  
  \[
  \ell(r)=\int_{t_n}^{t_f}\alpha(t)\,L^\sigma(r(t))\,L^c(r(t),\mathbf D)\,dt
  \]
  \[
  \alpha(t)=\exp\!\Big(-\int_{t_n}^{t} L^\sigma(r(s))\,ds\Big)
  \]
  where \(r(t)\) is the 3D point at distance \(t\) along ray \(r\), \(\mathbf D\) is unit ray direction, \(t_n,t_f\) near/far bounds. \(\alpha(t)\) is **transmittance** (probability ray hasn’t hit density up to \(t\)).
- **Discrete quadrature approximation (Sec. 45.4.1):**  
  \[
  \ell(r)\approx \sum_{i=1}^{T}\alpha_i\,(1-e^{-L^\sigma(\mathbf R_i)\delta_i})\,L^c(\mathbf R_i,\mathbf D)
  \]
  \[
  \alpha_i=\exp\!\Big(-\sum_{j=1}^{i-1}L^\sigma(\mathbf R_j)\delta_j\Big),\quad \delta_i=t_{i+1}-t_i
  \]
  with samples \(\mathbf R_i=r(t_i)\).
- **Sampling along ray (Sec. 45.4.1):** for ray origin \(\mathbf O\), direction \(\mathbf D\):  
  \(\mathbf R_i=\mathbf O+t_i\mathbf D\),  
  \(t_i\sim \mathcal U[i\!-\!1,i]\cdot\frac{t_f-t_n}{T}+t_n\) (uniform within each of \(T\) bins).
- **Rendering/training pipeline (Sec. 45.4–45.5):** pixel \(\rightarrow\) ray (\(\mathbf O_{\text{cam}},\mathbf K_{\text{cam}}\)) \(\rightarrow\) sample points \(\rightarrow\) query \(L_\theta\) \(\rightarrow\) quadrature sum \(\rightarrow\) pixel RGB; optimize \(\theta\) by minimizing reconstruction error between rendered and observed images.
- **Design rationale:** volume rendering generalizes ray casting; gives **smooth, nonzero gradients** vs. hard ray casting, enabling gradient-based fitting.

## When to surface
Use when students ask how NeRF forms an image from \((\sigma,\text{color})\) along rays, what “transmittance/opacity” means, or how the continuous integral becomes the standard discrete NeRF weights.