# Card: DS-NeRF depth-supervised ray termination loss
**Source:** https://openaccess.thecvf.com/content/CVPR2022/papers/Deng_Depth-Supervised_NeRF_Fewer_Views_and_Faster_Training_for_Free_CVPR_2022_paper.pdf  
**Role:** paper | **Need:** CONCEPT_EXPLAINER  
**Anchor:** Depth-supervision pipeline + loss: use sparse depth priors (SfM point clouds) to regularize NeRF ray termination/opacity distribution

## Key Content
- **Volumetric rendering (Eq. 1–2, Sec. 3.1):** NeRF predicts density and color:  
  \(f(\mathbf{x},\mathbf{d})=(\sigma,\mathbf{c})\). Ray \( \mathbf{r}(t)=\mathbf{o}+t\mathbf{d}\).  
  Rendered color: \(\hat{\mathbf{C}}=\int_0^\infty T(t)\sigma(t)\mathbf{c}(t)\,dt\), where \(T(t)=\exp(-\int_0^t \sigma(s)\,ds)\).  
  Color loss: \(L_{\text{Color}}=\mathbb{E}_{r\in R(P)}\|\hat{\mathbf{C}}(r)-\mathbf{C}(r)\|_2^2\).
- **Ray termination distribution (Sec. 3.1):** define \(h(t)=T(t)\sigma(t)\) (a probability distribution over termination depth). Ideal for opaque surfaces at depth \(D\): \(\delta(t-D)\). NeRF implementations assume near/far bounds \((t_n,t_f)\) and treat \(t_f\) as an opaque wall to normalize.
- **Depth supervision from SfM (Sec. 3.2):** Run COLMAP/SfM to get camera poses + sparse 3D keypoints \(\{\mathbf{x}_i\}\) and per-point mean reprojection error \(\hat{\sigma}_i\). For camera \(j\), project visible keypoint \(\mathbf{x}_i\) to get depth \(D_{ij}\).
- **Probabilistic depth model + loss (Sec. 3.2):** model true surface depth as \( \mathcal{N}(D_{ij},\hat{\sigma}_i)\). Minimize KL between depth distribution and rendered termination distribution:  
  \(L_{\text{Depth}}=\mathbb{E}_{\mathbf{x}_i\in X_j}\int \log h(t)\exp\!\left(-\frac{(t-D_{ij})^2}{2\hat{\sigma}_i^2}\right)dt\)  
  Discrete approx: \(\sum_k \log h_k \exp(-\frac{(t_k-D_{ij})^2}{2\hat{\sigma}_i^2})\Delta t_k\).  
  Total loss: \(L=L_{\text{Color}}+\lambda_D L_{\text{Depth}}\).
- **Empirical results:**  
  - **NeRF Real, 2-view PSNR:** NeRF 13.5 vs **DS-NeRF (KL)** 20.2 (Table 1).  
  - **Depth error (lower better), NeRF Real 2-view:** NeRF 20.32 vs **DS-NeRF** 10.41 (Table 4).  
  - **Training speed:** reaches NeRF peak PSNR in **2–3× fewer iterations**; per-iter time ~362.4ms (DS) vs 359.8ms (NeRF); in 5-view case ~**13 hours faster** to reach NeRF peak (Sec. 4.5, Fig. 7).  
  - KL-based depth loss yields fewer artifacts than MSE depth loss (Fig. 6).

## When to surface
Use when students ask how to incorporate depth/point-cloud priors into NeRF training, why ray termination distributions matter, or how sparse SfM depth can reduce few-view overfitting and speed up convergence.