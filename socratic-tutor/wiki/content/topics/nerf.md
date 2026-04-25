---
title: "NeRF"
subject: "3D & Scene Understanding"
date: 2026-04-06
tags:
  - "subject/3d-and-scene-understanding"
  - "level/intermediate"
  - "level/advanced"
  - "educator/yannic-kilcher"
  - "educator/lilian-weng"
  - "resource/video"
  - "resource/blog"
  - "resource/deep-dive"
  - "resource/paper"
  - "resource/code"
educators:
  - "Yannic Kilcher"
  - "Lilian Weng"
levels:
  - "intermediate"
  - "advanced"
resources:
  - "video"
  - "blog"
  - "deep-dive"
  - "paper"
  - "code"
---

# Nerf

## Video (best)
- **Yannic Kilcher** — "NeRF: Representing Scenes as Neural Radiance Fields for View Synthesis (Paper Explained)"
- **Watch:** [YouTube](https://www.youtube.com/watch?v=CRlN-cYFxTk)
- Why: Yannic walks through the original NeRF paper methodically, explaining the volume rendering equation, positional encoding, and the MLP architecture. He balances mathematical rigor with intuition, making it ideal for learners who want to understand *why* each design choice was made, not just what NeRF does.
- Level: intermediate

## Blog / Written explainer (best)
- **Lilian Weng** — "Neural Radiance Field (NeRF): A Review"
- **Link:** [https://arxiv.org/abs/2003.08934](https://arxiv.org/abs/2003.08934)
- Why: Lilian Weng's posts are known for comprehensive yet accessible coverage. This post situates NeRF within the broader landscape of neural scene representations, covers the core volume rendering math, and surveys key follow-up works (NeRF-W, Instant-NGP, etc.), giving learners both depth and context.
- Level: intermediate/advanced

## Deep dive
- **Matthew Tancik et al. (NeRF project page + supplementary)**
- **Link:** [https://www.matthewtancik.com/nerf](https://www.matthewtancik.com/nerf)
- Why: The official project page aggregates the paper, video results, and code in one place. For a technical deep dive, it provides the canonical reference point including the full rendering pipeline, training details, and qualitative comparisons that are essential for implementation-level understanding.
- Level: advanced

## Original paper
- **Mildenhall et al.** — "NeRF: Representing Scenes as Neural Radiance Fields for View Synthesis" (ECCV 2020)
- **Link:** [https://arxiv.org/abs/2003.08934](https://arxiv.org/abs/2003.08934)
- Why: This is the clear seminal paper for the topic. It is unusually readable for a graphics/vision paper — the volume rendering derivation is self-contained, the ablations are instructive, and the writing is accessible enough for ML practitioners without a graphics background.
- Level: advanced

## Code walkthrough
- **bmild/nerf (official TensorFlow implementation)**
- **Link:** [https://github.com/bmild/nerf](https://github.com/bmild/nerf)
- Why: The official implementation by the original authors is the most trustworthy reference for understanding how the hierarchical sampling, positional encoding, and coarse-to-fine network are actually coded. The README and notebook (`tiny_nerf.ipynb`) provide a minimal working example that strips NeRF down to its essentials — ideal for hands-on learners.
- Level: intermediate/advanced

## Coverage notes
- **Strong:** Core NeRF concept (implicit neural scene representation, volume rendering, view synthesis), original paper walkthrough, official code
- **Weak:** Connection to **point clouds** as an alternative/complementary 3D representation is not well-covered by any single resource that bridges both; learners in intro-to-physical-ai may need a separate point cloud primer
- **Gap:** No excellent beginner-friendly video exists that jointly covers NeRF *and* point clouds in the context of physical AI / robotics perception. A 3Blue1Brown-style visual explainer of volume rendering from scratch does not yet exist. Resources covering newer real-time variants (Gaussian Splatting as a NeRF successor) are sparse in structured tutorial form.

## Cross-validation
This topic appears in 2 courses: **intro-to-multimodal** (where NeRF is relevant as a 3D scene understanding method feeding into multimodal models) and **intro-to-physical-ai** (where NeRF and point clouds are used for robot perception and scene reconstruction). The original paper and Yannic Kilcher video serve both courses well; the point-cloud connection is a gap that may require supplementary material specific to each course's framing.

---

## Additional Resources for Tutor Depth

> **10 sources** — papers, official docs, working code, benchmarks, and deep explainers that give the AI tutor precision on this topic.

### 📄 DS-NeRF depth-supervised ray termination loss
**Paper** · [source](https://openaccess.thecvf.com/content/CVPR2022/papers/Deng_Depth-Supervised_NeRF_Fewer_Views_and_Faster_Training_for_Free_CVPR_2022_paper.pdf)

*Depth-supervision pipeline + loss: use sparse depth priors (SfM point clouds) to regularize NeRF ray termination/opacity distribution*

<details>
<summary>Key content</summary>

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

</details>

### 📄 DVGOv2 speed/quality + efficient regularizers for voxel-grid NeRF
**Paper** · [source](https://arxiv.org/pdf/2206.05085.pdf)

*concrete speed/quality tradeoffs + training procedure for DVGO-style dense voxel radiance fields*

<details>
<summary>Key content</summary>

- **Why explicit grids are fast (Intro):** MLP NeRF point query cost example: 8-layer, 256-hidden MLP ≈ **520k FLOPs/point**; typical iteration **8192 rays × 256 samples** ⇒ **>1T FLOPs**. Explicit grids give constant-time queries; occupancy masks skip low-density space.
- **Efficient distortion loss (Sec. 2, Eq. 1–3):**  
  Distortion loss for a ray with **N** intervals:
  \[
  L_{dist}(s,w)=\sum_{i}\sum_{j} w_i w_j \left|\frac{s_i+s_{i+1}}{2}-\frac{s_j+s_{j+1}}{2}\right|+\frac{1}{3}\sum_i w_i^2(s_{i+1}-s_i)
  \]
  where \(m_i=(s_i+s_{i+1})/2\), interval length \((s_{i+1}-s_i)\), \(s\) normalized to \([0,1]\). Naive first term is **O(N²)**; DVGOv2 rewrites using **prefix sums of \(w\) and \(w\odot m\)** to compute in **O(N)** (Eq. 2) and gradients in **O(N)** using prefix/suffix sums (Eq. 3). Implemented as CUDA extension; supports uneven samples/ray.
- **Efficient TV loss (Sec. 2, Listing 1):** Huber loss to 6-neighbors; fused CUDA kernel; **add gradients after backward**:
  `total_loss.backward(); total_variation_add_grad(tv_weight, dense_mode=(step<10000)); optimizer.step()`. TV computed densely for **first 10k iters**, then only on voxels with non-zero grads.
- **CUDA speedups (Sec. 3, Tab. 3; RTX 2080Ti, 160³ grid):**  
  Baseline times: lego **11.5m**, mic **9.3m**, ship **14.6m**.  
  + fused Adam: lego **8.7m (1.3×)**, mic **6.4m (1.5×)**, ship **12.1m (1.2×)**.  
  + Adam+rendering CUDA: lego **4.8m (2.4×)**, mic **3.4m (2.7×)**, ship **7.1m (2.1×)**.  
  Rendering details: sample per-ray bbox intersection (bounded scenes); fuse density→alpha ops; stop ray when transmittance < **1e−3**.
- **Speed/quality tradeoffs (Sec. 5):**
  - **Synthetic-NeRF (Tab. 4a, avg 8 scenes, 2080Ti):** DVGOv2(S, **160³**) **4.9m**, PSNR **31.91**; DVGOv2(L, **256³**) **6.8m**, PSNR **32.76**. DVGO baseline **14.2m**, PSNR **31.95**.
  - **LLFF forward-facing (Tab. 5):** DVGOv2 **10.9m**, PSNR **26.34** vs DVGOv2 w/o \(L_{dist}\) **13.9m**, PSNR **26.24** (distortion improves speed+quality). Forward-facing params: **D=256**, **XZ=384²**, step **s=1.0** layer; TV weights density **1e−5**, feature **1e−6**; distortion weight **1e−2**.
  - **Unbounded inward-facing (Sec. 5.4, Eq. 4 contraction):** grid **320³**, \(\alpha_{init}=1e{-4}\), step **0.5 voxel**; TV weights density **1e−6**, feature **1e−7**; distortion **1e−2**. Contracted-space mapping (Eq. 4) with hyperparam **b>0**; try **p=2** vs **p=∞** (cuboid) — on mip-NeRF-360 (Tab. 7) PSNR improves from **24.80 (p=2)** to **25.24 (p=∞)**; longer schedule **25.42**.

</details>

### 📄 VolSDF—Bridge NeRF Volume Rendering ↔ SDF Surfaces
**Paper** · [source](https://proceedings.neurips.cc/paper_files/paper/2021/file/25e2a30f44898b9f3e978b1786dcd85c-Paper.pdf)

*Differentiable volume rendering where density is a transformed SDF (explicit surface + better sampling + disentanglement)*

<details>
<summary>Key content</summary>

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

</details>

### 📊 NerfBaselines (consistent NeRF/NVS benchmarking)
**Benchmark** · [source](https://nerfbaselines.github.io)

*Standardized benchmark tables across methods with PSNR/SSIM/LPIPS (+ some runtime notes) under consistent evaluation protocols.*

<details>
<summary>Key content</summary>

- **Purpose / workflow:** NerfBaselines wraps **official implementations** (does not reimplement) to run methods via a **unified interface** with **consistent dataset loaders, evaluation protocols, and metrics** to make comparisons meaningful.
- **Core metrics reported (per dataset/method):**
  - **PSNR** (dB), **SSIM**, **LPIPS** (often **LPIPS (VGG)**).  
  - (No explicit formulas in excerpt; metrics are used as standardized outputs.)
- **Dataset protocol notes (important for fair comparisons):**
  - **Mip-NeRF 360:** 4 indoor + 5 outdoor object-centric scenes; camera trajectory is an **orbit** with fixed elevation/radius; **test set = every n-th frame**.
  - **Mip-NeRF 360 evaluation detail:** Some papers evaluate on **larger images then downscale** (avoids JPEG artifacts), which can **increase PSNR by ~0.5 dB** (noted via 3DGS paper discussion).
  - **Blender (nerf-synthetic):** 8 synthetic scenes; cameras on a **semi-sphere**; default background is **white**. Instant-NGP and some others reported as trained/evaluated on **black background** (not directly comparable to white-default).
  - **Photo Tourism:** Official protocol (NeRF-W style) optimizes appearance embedding on **left half** of test image; metrics computed on **right half** → yields **lower** numbers than papers that use full image.
  - **H3DGS dataset:** paper varies **tau ∈ {0,3,6,15}**; NerfBaselines chooses **tau=6** as quality/speed trade-off.
- **Concrete example “paper” numbers shown in excerpt (use as anchors when checking tables):**
  - **Mip-NeRF 360:** PSNR values listed include **27.04, 27.26, 27.29, 27.20, 27.79, 27.69, 28.54**; SSIM includes **0.805, 0.810, 0.815, 0.827, 0.792, 0.828**; LPIPS(VGG) includes **0.214, 0.203, 0.237, 0.189**.
  - **Blender:** PSNR includes **31.00, 32.52, 33.18, 33.68, 33.14, 33.31, 33.88, 33.80, 33.09**; SSIM includes **0.947, 0.982, 0.963, 0.970, 0.971**; LPIPS(VGG) includes **0.081, 0.047, 0.031**.
  - **LLFF:** PSNR **26.73**, SSIM **0.839**, LPIPS(VGG) **0.204**.
  - **Photo Tourism:** PSNR **24.70**, SSIM **0.865**, LPIPS **0.124**.
  - **H3DGS:** PSNR **25.39**, SSIM **0.806** (tau choice note above).

</details>

### 📖 Nerfstudio Ray Samplers (defaults + algorithms)
**Reference Doc** · [source](https://docs.nerf.studio/_modules/nerfstudio/model_components/ray_samplers.html)

*authoritative defaults and parameter meanings for ray sampling + proposal/PDF/occupancy sampling implementation in nerfstudio*

<details>
<summary>Key content</summary>

- **SpacedSampler (core spacing → euclidean bins)**  
  - Create normalized bin edges: `bins = linspace(0,1,num_samples+1)[None,:]`.  
  - **Stratified jitter (train only):** if `train_stratified and training`: jitter within each bin using `t_rand ~ U(0,1)`; if `single_jitter=True`, one jitter per ray (`[num_rays,1]`), else per edge (`[num_rays,num_samples+1]`).  
  - Map near/far through spacing: `s_near = spacing_fn(near)`, `s_far = spacing_fn(far)`.  
  - **Eq.1 (spacing→euclidean):** `t = spacing_fn_inv(x*s_far + (1-x)*s_near)` where `x∈[0,1]` are `bins`.  
  - Output `RaySamples` with `bin_starts=t[..., :-1]`, `bin_ends=t[..., 1:]` plus stored `spacing_*` and `spacing_to_euclidean_fn`.

- **Built-in spacings (all default `train_stratified=True`)**
  - `UniformSampler`: `spacing_fn(x)=x`.  
  - `LinearDisparitySampler`: `spacing_fn(x)=1/x`.  
  - `SqrtSampler`: `spacing_fn=sqrt`, inverse `x^2`.  
  - `LogSampler`: `spacing_fn=log`, inverse `exp`.  
  - `UniformLinDispPiecewiseSampler`: `spacing_fn(x)=where(x<1, x/2, 1-1/(2x))`; inverse `where(x<0.5, 2x, 1/(2-2x))`.

- **PDFSampler (hierarchical resampling from weights)**
  - Defaults: `train_stratified=True`, `include_original=True`, `histogram_padding=0.01`, `single_jitter=False`.  
  - **Eq.2 (PDF/CDF):** `w = weights[...,0] + histogram_padding`; normalize `pdf=w/sum(w)`; `cdf=[0, cumsum(pdf)]` clamped to ≤1.  
  - Sample `u` in `[0,1)` with `num_bins=num_samples+1`: stratified (train) or centered (eval). Invert CDF via `searchsorted`, linear interpolate bins; optionally concatenate+sort with original bins; `bins` are `detach()`’d.

- **VolumetricSampler (Instant-NGP-style occupancy sampling)**
  - Uses `OccGridEstimator.sampling(..., stratified=training, alpha_thre=0.01, near_plane=0.0, far_plane=1e10 if None, cone_angle=0.0)`.  
  - Optional **sigma_fn** (train only): density at midpoint `pos = o + d*(t_start+t_end)/2`.

- **ProposalNetworkSampler (proposal → NeRF sampling loop)**
  - Defaults: `num_proposal_samples_per_ray=(64,)`, `num_nerf_samples_per_ray=32`, `num_proposal_network_iterations=2`, `update_sched=lambda step:1`.  
  - Default samplers: initial `UniformLinDispPiecewiseSampler`; later `PDFSampler(include_original=False)`.  
  - Update logic: `updated = steps_since_update > update_sched(step) or step < 10`; proposal densities computed with grad if updated else `no_grad`.  
  - Anneal: resample with `annealed_weights = weights ** _anneal`.

- **NeuSSampler defaults**
  - `num_samples=64`, `num_samples_importance=64`, `num_samples_outside=32`, `num_upsample_steps=4`, `base_variance=64`, `single_jitter=True`.  
  - Upsampling uses fixed `inv_s = base_variance * 2**iter` and PDF resampling with `histogram_padding=1e-5`, `include_original=False`.

</details>

### 📖 nerfstudio Cameras & Rays API (intrinsics/extrinsics, distortion, ray gen)
**Reference Doc** · [source](https://docs.nerf.studio/reference/api/cameras.html)

*Camera model conventions + core API fields for intrinsics/extrinsics, distortion handling, ray generation, pose optimization.*

<details>
<summary>Key content</summary>

- **Cameras dataclass (per-image camera model):**  
  `Cameras(camera_to_worlds[* 3×4], fx, fy, cx, cy, width, height, distortion_params[* 6], camera_type, times[num_cameras], metadata)`  
  - `camera_to_worlds`: per-image **c2w** matrices in **[R | t]** (3×4).  
  - Intrinsics scalars/tensors: `fx, fy` (focal lengths), `cx, cy` (principal point). Single values are **broadcast** to all cameras.  
  - `distortion_params`: **6 params** in OpenCV order **[k1, k2, k3, k4, p1, p2]** (radial + tangential; also mentions OpenCV “6 radial” / “6-2-4 … thin-prism for Fisheye624”).  
  - `camera_type`: int enum (default **CameraType.PERSPECTIVE**).  
  - `metadata`: broadcast to generated rays / RaySamples for interpolation or conditioning.
- **Intrinsics matrix (pinhole):** `get_intrinsics_matrices() -> K[* 3×3]` built from `(fx, fy, cx, cy)` (standard pinhole K).
- **Pixel coordinate grid:** `get_image_coords(pixel_offset=0.5)` returns `[H, W, 2]` coords; default offset **0.5** = pixel centers.
- **Ray generation workflow:** `generate_rays(camera_indices, coords=None, ..., disable_distortion=False, aabb_box=None, obb_box=None)`  
  - Handles 4 broadcasting cases for `(camera_indices, coords)`; if `coords=None`, renders full image.  
  - **Jagged cameras** (varying H/W): if `coords=None`, coordinate maps can’t stack → **flatten & concatenate** rays.  
  - Optional `aabb_box` computes `nears/fars` via box intersection.
- **Undistortion procedure:** `radial_and_tangential_undistort(coords, distortion_params, eps=0.001, max_iterations=10)` iterative undistort (MultiNeRF-adapted).
- **Pose optimization config:** `CameraOptimizerConfig(mode ∈ {'off','SO3xR3','SE3'} default 'off', trans_l2_penalty=0.01, rot_l2_penalty=0.001)`; recommendation: **SO3xR3**.
- **Ray structures:**  
  - `RayBundle(origins[* 3], directions[* 3] unit, pixel_area[* 1], camera_indices, nears, fars, times, metadata)`  
  - `RaySamples.get_weights(densities)` and `get_weights_and_transmittance_from_alphas(alphas)` for volumetric rendering weights.

</details>

### 🔍 NeRF Volume Rendering (MIT Vision Book Ch.45)
**Explainer** · [source](https://visionbook.mit.edu/nerf.html)

*Clean derivation + discretization of radiance-field image formation (radiance, density, transmittance)*

<details>
<summary>Key content</summary>

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

</details>

### 🔍 NeRF Volume Rendering Equations (weights, transmittance, sampling)
**Explainer** · [source](https://arxiv.org/abs/2209.02417)

*consolidated continuous + discrete NeRF rendering equations; clarifies discretization (weights/transmittance) and sampling; notes piecewise-linear opacity alternative*

<details>
<summary>Key content</summary>

- **Ray color as expectation / integral (Sec. 3; Eq. 7 in excerpted VolSDF review, consistent with NeRF):**  
  \[
  \hat{y}=\mathbb{E}_{s\sim p(s)}[c(s)]=\int_{0}^{\infty} p(s)\,c(s)\,ds
  \]
  with **PDF** \(p(s)=\tau(s)T(s)\), **transmittance**  
  \[
  T(t)=\exp\!\left(-\int_{0}^{t}\sigma(x(u))\,du\right)
  \]
  **opacity** \(O(t)=1-T(t)\), and  
  \[
  \tau(t)=\frac{dO}{dt}=\sigma(x(t))T(t)
  \]
- **Standard NeRF discrete quadrature / alpha-compositing (NeRF Eq. 3):** sample depths \(t_i\), intervals \(\delta_i=t_{i+1}-t_i\), network outputs \((\sigma_i,c_i)\).  
  \[
  \hat{C}(\mathbf{r})=\sum_{i=1}^{N} w_i c_i,\quad
  w_i=T_i\alpha_i,\quad
  \alpha_i=1-\exp(-\sigma_i\delta_i),\quad
  T_i=\exp\!\left(-\sum_{j<i}\sigma_j\delta_j\right)=\prod_{j<i}(1-\alpha_j)
  \]
- **Sampling procedure (NeRF Sec. 5.2):** stratified samples: partition \([t_n,t_f]\) into \(N\) bins, draw one uniform sample per bin. Hierarchical sampling: use coarse weights \(w_i\) to form a piecewise-constant PDF along the ray; draw \(N_f\) additional samples via inverse-CDF; render with union of samples.
- **Defaults (NeRF Sec. 5.3):** batch size **4096 rays**; **\(N_c=64\)** coarse samples + **\(N_f=128\)** fine samples; Adam LR **5e-4 → 5e-5** exponential decay.
- **Design rationale (Digest focus):** piecewise-constant opacity causes **“quadrature instability”** (rendering sensitive to sample placement; non-invertible CDF → surrogate for importance sampling). Proposed fix: **piecewise-linear opacity** yields closed-form/invertible CDF and more stable rendering/sampling.

</details>

### 🔍 NeRF core equations + benchmark anchor (PSNR/SSIM/LPIPS, speed)
**Explainer** · [source](https://arxiv.org/html/2210.00379v6)

*compiled quantitative comparisons across NeRF families/datasets (tables with PSNR/SSIM/LPIPS + training/inference speed)*

<details>
<summary>Key content</summary>

- **Radiance field definition (Eq. 1):** NeRF models a 5D function  
  \(F_\theta(\mathbf{x},\mathbf{d}) \rightarrow (\mathbf{c},\sigma)\) where \(\mathbf{x}\) is 3D position, \(\mathbf{d}\) is viewing direction (often a 3D unit vector), \(\mathbf{c}\) is RGB color, \(\sigma\) is volume density. Density is constrained **view-independent**; color depends on \((\mathbf{x},\mathbf{d})\) via a 2-stage MLP (feature vector size **256** in original NeRF).
- **Volume rendering (Eq. 2–5):** Ray color  
  \(C(\mathbf{r})=\int T(t)\,\sigma(\mathbf{r}(t))\,\mathbf{c}(\mathbf{r}(t),\mathbf{d})\,dt\), with transmittance  
  \(T(t)=\exp(-\int \sigma(\mathbf{r}(s))ds)\) (Eq. 3). Discrete approximation (Eq. 4):  
  \(\hat{C}(\mathbf{r})=\sum_i T_i\,\alpha_i\,\mathbf{c}_i\), \(\alpha_i=1-\exp(-\sigma_i\delta_i)\) (Eq. 5).
- **Expected depth (Eq. 6–7):** \(\mathbb{E}[t]=\int T(t)\sigma(t)t\,dt \approx \sum_i T_i\alpha_i t_i\). Used for depth regularization/supervision.
- **Training loss (Eq. 8):** photometric MSE over rays \( \sum_{\mathbf{r}\in\mathcal{R}}\|\hat{C}(\mathbf{r})-C^{gt}(\mathbf{r})\|_2^2\).
- **Positional encoding (Eq. 9):** apply sin/cos at multiple frequencies to each component of \(\mathbf{x}\in[-1,1]\) and \(\mathbf{d}\). Original NeRF uses **\(N=10\)** for \(\mathbf{x}\), **\(N=4\)** for \(\mathbf{d}\).
- **Dataset defaults:** NeRF Synthetic (8 objects: hotdog/materials/ficus/lego/mic/drums/chair/ship), images **800×800**, **100 train / 200 test** views.
- **Speed/quality comparisons (survey claims):** Gaussian Splatting typically **more photorealistic**, trains **2–3 orders of magnitude faster**, and renders **orders of magnitude faster** than fully implicit NeRF; NeRF often **lower storage** and better fits **implicit-representation pipelines**.
- **Concrete speedups (Sec. III-B1):** “baked” methods like **SNeRG** and **PlenOctree** report ~**3000×** faster inference vs original NeRF; **PointNeRF** reports ~**3×** speedup by skipping empty space via point-cloud features.

</details>

### 🔍 NeRF overview + why volume rendering helps optimization
**Explainer** · [source](https://ar5iv.labs.arxiv.org/html/2101.05204)

*NeRF-style volumetric rendering intuition; positional encoding/Fourier features motivation; stratified sampling mention; pointers to related work*

<details>
<summary>Key content</summary>

- **Neural volume rendering definition (Intro):** render by tracing a ray and taking an **integral along the ray**; an MLP maps **3D coordinates (and often view direction)** to **density + color**, which are integrated to yield pixel color.
- **NeRF core representation (Sec. 3.2):** “brutal simplicity”: an **MLP** takes a **5D coordinate** (3D position + 2D view direction) and outputs **density** and **color**; trained from **many posed images**; novel views rendered by integrating predictions along rays.
- **Numerical integration (Sec. 3.2):** NeRF uses an “easily differentiable” **numerical integration method** approximating volumetric rendering by sampling points along each ray and accumulating contributions.
- **Positional encoding / Fourier features rationale (Sec. 3.2):** NeRF achieves high detail by encoding inputs with **periodic activation functions (Fourier Features)**; later generalized to **SIREN** (sinusoidal representation networks).
- **Why volume rendering can optimize well (Sec. 3.1, Neural Volumes quote):** semi-transparent density/opacity “**disperses gradient information along the ray of integration**,” widening the basin of convergence and helping find good solutions.
- **Stratified sampling (Sec. 10):** original NeRF’s **stratified sampling scheme** is framed as a step toward discovering/guessing surfaces after convergence.
- **Concrete limitations/opportunities (Sec. 3.2):** vanilla NeRF is **slow** (training/rendering), **static-only**, **bakes in lighting**, and **does not generalize** across scenes.

</details>

---

## Related Topics

- [[topics/3d-gaussian-splatting|3D Gaussian Splatting]]
