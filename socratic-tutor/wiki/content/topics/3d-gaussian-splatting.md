---
title: "3D Gaussian Splatting"
subject: "3D & Scene Understanding"
date: 2025-04-06
tags:
  - "subject/3d-and-scene-understanding"
  - "level/beginner"
  - "level/intermediate"
  - "level/advanced"
  - "educator/yannic-kilcher"
  - "resource/video"
  - "resource/blog"
  - "resource/deep-dive"
  - "resource/paper"
  - "resource/code"
educators:
  - "Yannic Kilcher"
levels:
  - "beginner"
  - "intermediate"
  - "advanced"
resources:
  - "video"
  - "blog"
  - "deep-dive"
  - "paper"
  - "code"
---

# 3D Gaussian Splatting

## Video (best)
- **Yannic Kilcher** — "3D Gaussian Splatting for Real-Time Radiance Field Rendering (Paper Explained)"
- **Watch:** [YouTube](https://www.youtube.com/watch?v=T_kXY43VZnk)
- Why: Yannic's paper walkthrough style is ideal for understanding the mathematical intuition behind Gaussian primitives, the differentiable rasterization pipeline, and why this approach outperforms NeRF for real-time rendering. He connects theory to implementation clearly.
- Level: intermediate/advanced

> An alternative well-known explainer by Bilawal Sidhu on YouTube covers 3D Gaussian Splatting; the Computerphile video on 3D Gaussian Splatting has youtube_id VkIJbpdTujE.

## Blog / Written explainer (best)
- **Hugging Face / Maxime Labonne** — None from the preferred list (Jay Alammar, Lilian Weng, etc.) have published a dedicated 3DGS explainer as of my knowledge cutoff.
- **Recommended alternative:** The official INRIA project blog / supplementary site at `https://repo-sam.inria.fr/fungraph/3d-gaussian-splatting/`
- Why: Written by the original authors, it provides accessible visual explanations of the core concepts (Gaussian representation, splatting, tile-based rasterization) alongside interactive comparisons — making it the clearest written introduction directly tied to the source material.
- Level: beginner/intermediate

## Deep dive
- **Author:** Leonid Keselman
- **Title:** "A Gentle Introduction to 3D Gaussian Splatting"
- url: `https://leonidk.com/fmb-plus/` [NOT VERIFIED]
- Why: Provides a thorough technical walkthrough of the full pipeline including covariance matrix parameterization, spherical harmonics for view-dependent color, and the adaptive density control mechanism — going deeper than most blog posts while remaining pedagogically structured.
- Level: advanced

> ⚠️ I have moderate confidence in this URL. If unavailable, the GitHub repository README at `https://github.com/graphdeco-inria/gaussian-splatting` serves as an excellent technical reference.

## Original paper
- **Authors:** Kerbl, Kopanas, Leimkühler, Drettakis (2023)
- **Title:** "3D Gaussian Splatting for Real-Time Radiance Field Rendering"
- url: `https://arxiv.org/abs/2308.04079`
- Why: This is the clear seminal paper for this topic. It is unusually readable for a SIGGRAPH paper — the authors explain the motivation for each design choice (why Gaussians, why tile-based rasterization, why adaptive densification), making it suitable as a primary teaching reference rather than just a citation.
- Level: advanced

## Code walkthrough
- **Resource:** Official INRIA implementation with documented training pipeline
- url: `https://github.com/graphdeco-inria/gaussian-splatting`
- Why: The official codebase is well-structured with clear separation between the Gaussian representation, rasterization CUDA kernels, and training loop. It is the reference implementation that all downstream work builds on, making it the most pedagogically honest starting point for hands-on learning.
- Level: intermediate/advanced

> **Alternative:** The `nerfstudio` integration (`https://docs.nerf.studio/nerfology/methods/splat.html`) provides a more beginner-friendly entry point with cleaner abstractions for learners not ready for raw CUDA.

---

## Coverage notes
- **Strong:** The original paper (arxiv) is excellent and genuinely readable. The official GitHub repo is well-documented. The INRIA project page has strong visuals.
- **Weak:** No tier-1 educator (3Blue1Brown, Jay Alammar, Lilian Weng) has produced a dedicated explainer for 3DGS as of early 2025. The mathematical foundations (covariance matrices, spherical harmonics, EWA splatting) are underserved in beginner-friendly formats.
- **Gap:** No high-quality video exists from the preferred educator list. The connection between 3DGS and downstream applications (digital twins, NVIDIA Omniverse, USD pipelines, synthetic data generation) is almost entirely uncovered in public educational content — learners in `intro-to-physical-ai` will need custom-created bridging material.
- **Gap:** No distill.pub or equivalent interactive explainer exists for the mathematical core (Gaussian projection, 2D covariance derivation).

---

## Cross-validation
This topic appears in 2 courses: **intro-to-multimodal**, **intro-to-physical-ai**

- In `intro-to-multimodal`: 3DGS is relevant as a 3D scene representation that bridges vision and geometry — connecting to topics like NeRF, novel view synthesis, and multimodal scene understanding.
- In `intro-to-physical-ai`: 3DGS is directly relevant to digital twin creation, synthetic data generation for robot training, and integration with NVIDIA Omniverse/USD pipelines. The gap in coverage of these applied connections is the most significant pedagogical risk for this course.

---

---

## Additional Resources for Tutor Depth

> **10 sources** — papers, official docs, working code, benchmarks, and deep explainers that give the AI tutor precision on this topic.

### 📄 3DGS vs NeRF for Real-Time SLAM + Telepresence (latency/streaming)
**Paper** · [source](https://arxiv.org/html/2509.23555v1)

*System/architecture requirements + latency/streaming constraints; how 3DGS fits SLAM + telepresence pipelines (taxonomy + design rationale)*

<details>
<summary>Key content</summary>

- **NeRF definition & rendering (Sec. III-B):** NeRF is a function \(F_\theta(\mathbf{x},\mathbf{d})\to(\mathbf{c},\sigma)\) where \(\mathbf{x}\)=3D point, \(\mathbf{d}\)=view dir, \(\mathbf{c}\)=RGB, \(\sigma\)=density. Rendering uses **alpha compositing along a ray** with transmittance \(T\); approximated by stratified sampling with step \(\delta\). Optimized with **photometric loss** between predicted and GT pixels.
- **3DGS primitive & rasterization (Sec. III-C):** Scene is explicit anisotropic Gaussians with **center** \(\mu\), **covariance** \(\Sigma\succeq0\), **opacity** \(\alpha\), **color** \(\mathbf{c}\) (often view-dependent via spherical harmonics). Projection linearizes camera mapping with Jacobian \(J\) and world-to-camera transform \(T\). Pixels rendered by **ordered alpha compositing** with effective opacity. Covariance kept valid via reparameterization; **densification/pruning**: clone/split/prune Gaussians based on gradient magnitude & coverage.
- **Design rationale:** NeRF ray marching + slow convergence → poor for interactive/low-latency systems; 3DGS uses differentiable **rasterization** → real-time rendering, modular integration into hybrid pipelines; tradeoff: **higher memory** (millions of primitives).
- **Empirical speed comparisons (Sec. IV):**
  - Dense-prediction SLAM: **6–20 FPS** throughput.
  - NeRF-SLAM: **3–15 FPS**.
  - 3DGS-SLAM: **3–30 FPS end-to-end**, but **rendering >100 FPS (up to 1000 FPS)**.
  - Examples: MonoGS ~**3 FPS** end-to-end; RTG-SLAM **17.9 FPS** end-to-end; SplaTAM ~**400 FPS rendering**; Photo-SLAM **up to 1000 FPS rendering**; GS-ICP-SLAM **107 FPS rendering**.
- **Telepresence requirement checklist (Sec. V-A):** (1) multi-user life-sized immersive visualization, (2) accurate dynamic geometry, (3) real-time scanning/updates with minimized latency, (4) photorealistic output.
- **TeleAloha telepresence pipeline + numbers (Sec. V-B):** 4 sparse RGB cams + consumer GPU + autostereoscopic screen; **2048×2048 @ 30 FPS**, **end-to-end latency <150 ms**. Uses cascaded disparity for geometry + **Gaussian-splat neural rasterizer** + weighted blending to refine output.

</details>

### 📄 GrowSplat temporal plant digital twins w/ 3D Gaussian Splats
**Paper** · [source](https://arxiv.org/html/2505.10923v1)

*Digital-twin-oriented pipeline for temporal capture + update/alignment of evolving plant scenes using 3D Gaussian Splatting.*

<details>
<summary>Key content</summary>

- **System framing (4D digital twin):** Build per-time-step 3D Gaussian Splat reconstructions from multi-view images, then **temporally register** them into a consistent global plant frame to obtain a discrete-time 4D model (Sections I, V).
- **Capture setup (Maxi-Marvin, Sec. III-A):** 15 static calibrated cameras arranged in **3 layers × 5 cameras**; each time step yields **15 images + calibrated poses** (intrinsics + distortion).
- **Preprocess for Nerfstudio (Sec. III-B):** Maxi-Marvin uses **division distortion model** (single radial coefficient). Nerfstudio expects **6 distortion params**; convert to **K1, K2, P1=0, P2=0**, with **K3=0, K4=0** (defaults).
- **Temporal registration formulation (Sec. IV-C):** For point cloud \(P_t\) at time \(t\), align to reference \(P_{\text{ref}}\) via transformation  
  **Eq. (1):** \(T(P_t)=R(P_t)+D(P_t;\theta)\)  
  where \(R(\cdot)\) is **global rigid alignment** and \(D(\cdot;\theta)\) is a **non-rigid deformation field** capturing growth.
- **Registration pipeline (Sec. V-B):**
  1) **Downsample/filter GS points** to reduce outliers/overhead: filter by **log-scale range**, **scale ratio** (remove elongated splats), and **quaternion norm** (rotation validity).  
  2) Estimate normals → compute **FPFH** features.  
  3) **Coarse alignment:** FPFH matching + **RANSAC** outlier rejection + **Fast Global Registration (FGR)** robust optimization.  
  4) **Fine alignment:** **ICP**, improved with **Colored ICP** (adds photometric/color consistency).
- **3DGS training rationale (Sec. V-A):** 3DGS chosen for speed vs NeRF; cited comparison: **3 sec** (GS) vs **6 sec** (NeRF) to reach first **100 iterations**. Uses **Nerfstudio Splatfacto-MCMC**; with only 15 images, uses **segmentation masks** (ignore loss outside mask; minimize total rendered opacity), **initial point clouds**, and a **lighting factor** to handle darker images.
- **Empirical dataset scale (Sec. VI):** Sequoia: **40** time steps over **2024-02-13→2024-05-24**, avg \(\Delta t=2.4\) days. Quinoa: **55** time steps over **2022-10-31→2023-01-15**, avg \(\Delta t=1.4\) days; longest series **55 time points over 76 days**.

</details>

### 📄 Mon3tr telepresence pipeline (amortized 3DGS avatar)
**Paper** · [source](https://arxiv.org/html/2601.07518v1)

*Concrete monocular telepresence procedure + real-time deployment numbers (FPS/latency/bandwidth) and design choices*

<details>
<summary>Key content</summary>

- **Core idea (Section 3): amortized computation**
  - **Offline (one-time):** build a **user-specific animatable 3DGS avatar** from **1–2 min multi-view RGB video**; stored on cloud; reported **~33 s per user** for amortization stage (Fig. 3).
  - **Online (live):** sender transmits only compact **motion/expression parameters**; receiver deforms + renders pre-built 3DGS avatar.
- **System architecture (Section 3B/3D):**
  - **Sender:** PC + monocular RGB camera; runs parallel estimators for **body pose** (GVHMR), **hands** (HaMeR), **face** (SMIRK/landmarks) → unified SPMM3 driving params \((\theta,\psi,\phi)\). Compression: **FP16 quantization + LZ4**.
  - **Channel:** **WebRTC reliable data channel**; motion stream **~0.2 Mbps** (also reported **~0.16 Mbps** end-to-end bandwidth).
  - **Receiver (Meta Quest 3):** downloads avatar package: template mesh \(\bar{M}\), baseline Gaussians \(\bar{G}\), ONNX models \((f_m,f_g)\). Runs mesh deformation + Gaussian attribute deformation + optimized 3DGS rasterization at **60 FPS**.
- **Key equations (Section 4):**
  - **Hybrid template topology (Eq. 1):** \(T=\text{Replace}(B',F(\beta),H;\,A_F,A_H)\) (body mesh with FLAME face + MANO hands aligned/attached).
  - **Posed mesh with learned offsets (Eq. 2):** \(M_t=\text{LBS}(T+\Delta V_t,\;J_t,\;W)\).
  - **Gaussian attribute residuals (Eq. 5):** \(\Delta a_i=\sum_{k\in \mathcal{N}(i)} \tilde{m}_{ik}\,p_k\) (weighted “dragging forces” from local controllers).
  - **Hierarchical Gaussian position (Eq. 6):** \(x_t = \Phi(M_t) + \delta x_t\) (coarse mesh-driven + fine residual).
  - **Virtual mass coupling (Eq. 4):** \(m_{ik}\) uses **geodesic distance + skinning-weight similarity** to avoid pseudo-proximity.
- **Empirical results (Abstract/Section 6):**
  - **Latency:** **73.1 ms** end-to-end (also stated **~80 ms**); per-frame comm delay **~22 ms** (Fig. 3).
  - **FPS:** **60 FPS** on Quest 3; **>124 FPS** on PC.
  - **Quality:** **Novel poses PSNR 28.3858 dB** (SSIM **0.9743**, LPIPS **0.0564**, FID **20.3608**); training poses PSNR **32.4037 dB** (SSIM **0.9857**, LPIPS **0.0232**, FID **11.2907**).
  - **Sender extraction throughput:** face **377.08 FPS**, body **73.60 FPS**, hands **71.23 FPS**; integrated pipeline **58.21 FPS**; worker exec **13.78 ms**, join/comm **2.13 ms**, smoothing **1.27 ms**.
  - **Bandwidth reduction:** **~1000×** vs point-cloud/volumetric streaming; comparisons cited: TeleAloha **~100 Mbps**, MetaStream **72.3 Mbps**.
  - **Deployment details:** ONNX Runtime on Android; **static graphs**, **FP16** for networks, **UInt16** for Gaussian sorting; **frame interpolation** (Slerp for rotation, Lerp otherwise) to raise **30→60 FPS**.
  - **Cost/VRAM:** estimated system cost **~$73**; VRAM **3.9 GB** (vs MonoPort **11.2 GB**).

</details>

### 📄 Perspective-projected EWA Gaussian splat footprint (screen-space conic)
**Paper** · [source](https://www.cs.umd.edu/~zwicker/publications/EWASplatting-TVCG02.pdf)

*Derivation of perspective-projected elliptical Gaussian footprint (screen-space quadratic/conic) + EWA resampling (reconstruction ⊗ low-pass) equations.*

<details>
<summary>Key content</summary>

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

</details>

### 📊 NerfBaselines — Reproducible NeRF/3DGS Benchmarking
**Benchmark** · [source](https://arxiv.org/html/2406.17345v1)

*Reproducible evaluation harness + standardized metric reporting (PSNR/SSIM/LPIPS) across datasets for apples-to-apples comparisons and reruns.*

<details>
<summary>Key content</summary>

- **Problem/Rationale (Intro, Sec. 3–4):** Small evaluation-protocol differences (image resolution, downscaling, SSIM params, LPIPS backbone, float vs uint8 metric computation, background color) can materially change reported metrics → motivates strict standardization.
- **Standard metrics (Sec. 4):** Reports **PSNR, SSIM, LPIPS (AlexNet)**; main paper mostly PSNR.
- **Unified Method API (Appx A.1):**
  - `constructor(train_dataset?, checkpoint?)` (at least one provided)
  - `train_iteration()` (one training step)
  - `save(path)` (checkpoint)
  - `render(cameras, embeddings?)` (novel-view rendering)
  - `get_info()`, `get_method_info()`
  - optional `optimize_embeddings(dataset)` for appearance conditioning
- **Reproducibility mechanisms (Sec. 3):**
  - Install each method in **isolated environments**; IPC to communicate.
  - Backends: **Conda, Docker, Apptainer** (Docker best isolation; Apptainer HPC-friendly).
  - Store checkpoints; during evaluation store **checkpoint SHA** and verify match; **fix random seeds**; tests ensure checkpoint reload reproduces outputs.
- **Unified dataloader (Sec. 3):** Standardizes dataset formats + processing; supports COLMAP, NeRF/NerfStudio `transforms.json`, Bundler, LLFF, Tanks&Temples, PhotoTourism splits; consistent camera format.
- **Empirical results (Sec. 4.1):**
  - On **Mip-NeRF 360** and **Blender**, reproduces original paper numbers with **<1% deviation for most scenes**.
  - Larger discrepancies traced to protocol/code evolution (e.g., NerfStudio changes; Instant-NGP black background).
- **Protocol pitfall example (Sec. 4.3, Mip-NeRF 360):**
  - NeRFs evaluate on **released downscaled images** (JPEG-compressed).
  - 3DGS/Mip-Splatting downscale **internally from originals** (no JPEG artifacts) → **higher PSNR**, especially outdoors.
  - Downscale factors: **indoor ×2**, **outdoor ×4**.
- **Compute-cost definition (Sec. 4.2):** computational cost = **training time × GPU memory use**; 3DGS shows higher cost variance due to adaptive capacity.
- **Hardware default (Sec. 4):** Experiments on **NVIDIA A100**; **Mip-NeRF 360 uses 4 GPUs**, others **1 GPU**.

</details>

### 📖 Omniverse Replicator Core API (1.4.4) — layers, creation, distributions, writers
**Reference Doc** · [source](https://docs.omniverse.nvidia.com/py/replicator/1.4.4/source/extensions/omni.replicator.core/docs/API.html)

*Documented Replicator API surface + defaults (e.g., `rep.new_layer()` defaults to layer name **"Replicator"**) and core synthetic-data workflow patterns.*

<details>
<summary>Key content</summary>

- **Layer isolation (authoring context)**
  - `rep.new_layer(name: str=None)`: creates a new authoring layer to contain Replicator changes; if a layer with the same name exists, it is **cleared** before applying new changes.
  - **Default:** if `name` omitted → layer name **"Replicator"**.
  - Pattern: `with rep.new_layer(): ...` (e.g., create 100 cones with random positions).

- **Core synthetic-data workflow (procedure)**
  1. Create camera: `camera = rep.create.camera(...)`
     - Key defaults: `focal_length=24.0`, `focus_distance=400.0`, `f_stop=0.0`, `horizontal_aperture=20.955`, `clipping_range=(1.0, 1000000.0)`, `projection_type='pinhole'`.
  2. Create render product: `render_product = rep.create.render_product(camera, (W,H))` (example uses **(1024,1024)**).
  3. Initialize writer: `writer = rep.WriterRegistry.get("BasicWriter"); writer.initialize(output_dir=..., rgb=True, ...)`
     - `BasicWriter` defaults: `image_output_format='png'`, `frame_padding=4`, `semantic_types=["class"]`.
     - Colorization defaults: `colorize_semantic_segmentation=True`, `colorize_instance_id_segmentation=True`, `colorize_instance_segmentation=True`.
  4. Attach writer: `writer.attach([render_product])`
  5. Run: `rep.orchestrator.run()`; stop via `rep.orchestrator.stop()`.

- **Randomization distributions (parameters)**
  - `rep.distribution.uniform(lower, upper, num_samples=1, seed=None, name=None)`
  - `rep.distribution.normal(mean, std, num_samples=1, seed=None, name=None)`
  - `rep.distribution.choice(choices, weights=None, num_samples=1, seed=None, with_replacements=True, name=None)`
  - **Rationale:** `name` makes distribution values available to the **Writer**.

- **Creation & modification primitives**
  - `rep.create.*` (e.g., `sphere`, `cube`, `cone`, `light`, `from_usd`, `group`, `material_omnipbr`) commonly accept `position/rotation/scale`, `semantics=[("class","label")]`, `count=1`, `visible=True`.
  - `rep.modify.pose(...)`: cannot specify **both** `rotation` and `look_at`; cannot specify **both** `size` and `scale`. Default `rotation_order='XYZ'`.

</details>

### 📖 Omniverse Replicator Core API (v1.4.0) — essentials for reproducible synthetic-data scripts
**Reference Doc** · [source](https://docs.omniverse.nvidia.com/py/replicator/1.4.0/source/extensions/omni.replicator.core/docs/API.html)

*Exact callable signatures + parameter defaults (incl. `new_layer` clearing behavior, writer/creator/distribution defaults)*

<details>
<summary>Key content</summary>

- **Layer isolation (authoring context)**
  - `omni.replicator.core.new_layer(name: str = None)`  
    Creates a new authoring layer context to contain Replicator changes. **If a layer of the same name already exists, it is cleared** before applying new changes. Default name: **"Replicator"**.
- **Basic data-writing pipeline (minimal workflow)**
  1. Create camera: `rep.create.camera(...)`
  2. Create render product: `rep.create.render_product(camera, (W, H))`
  3. Writer: `writer = rep.WriterRegistry.get("BasicWriter")`
  4. `writer.initialize(output_dir=..., rgb=True, ...)`
  5. `writer.attach([render_product])`
  6. `rep.orchestrator.run()`
- **Writer API + defaults**
  - `class omni.replicator.core.BasicWriter(output_dir: str, semantic_types: Optional[List[str]] = None, rgb: bool=False, ... image_output_format: str='png', colorize_semantic_segmentation: bool=True, colorize_instance_id_segmentation: bool=True, colorize_instance_segmentation: bool=True, ...)`
  - `write(data: dict)` called every frame; `Writer.on_final_frame()` runs after final frame.
- **Sampling/distributions (named values can be written)**
  - `rep.distribution.uniform(lower, upper, num_samples: int=1, seed: Optional[int]=None, name: Optional[str]=None)`
  - `rep.distribution.normal(mean, std, num_samples: int=1, seed: Optional[int]=None, name: Optional[str]=None)`
  - `rep.distribution.choice(choices: List[str], weights: List[float]=None, num_samples=1, seed=None, with_replacements: bool=True, name=None)`
- **Camera defaults (useful for 3DGS dataset generation)**
  - `rep.create.camera(... focal_length=24.0, focus_distance=400.0, f_stop=0.0, horizontal_aperture=20.955, clipping_range=(1.0, 1000000.0), projection_type='pinhole', ... count: int=1, parent=None)`

</details>

### 📖 Omniverse Workflows Overview (Defect Detection)
**Reference Doc** · [source](https://docs.omniverse.nvidia.com/workflows/latest/defect-detection/generate_data.html)

*Entry point describing what “Workflows” are in NVIDIA Omniverse Workflows docs (step-by-step pipelines across apps/tools)*

<details>
<summary>Key content</summary>

- **Definition / purpose (Workflows Overview section):**
  - “Workflows are step-by-step instructions” enabling users to utilize the **NVIDIA Omniverse™ platform** within broader projects.
  - Workflows may **weave in and out of multiple Omniverse applications** and can also use **tools outside the Omniverse Platform**.
  - The docs position workflows as a way to go “from planning, design, and development” to get users “from point A to point B.”
  - The set of possible workflows is described as **“virtually unlimited”**; this section focuses on “more common and useful pipelines identified by [NVIDIA’s] engineering team.”
- **Navigation / related procedural content (Table of Contents pointers):**
  - Links onward to **Extension Workflows** (next page) and a set of concrete extension tutorials (e.g., “Make an Extension To Spawn Primitives,” “Create a CSV Reader,” “Reusable Light Panel,” “Viewport Reticle,” etc.).
  - Additional workflow categories listed: **Simulation**, **Variant Workflows**, **Digital Human Real-Time Rendering Setup**, **Data Driven Product Configurators**.
- **No equations, hyperparameters, or numeric empirical results** are provided on this page; it is a conceptual overview and index into detailed workflows elsewhere in the docs.

</details>

### 🔍 Isaac Sim + Omniverse Replicator (Scene-Based SDG) — Core Concepts
**Explainer** · [source](https://docs.omniverse.nvidia.com/isaacsim/latest/replicator_tutorials/tutorial_replicator_scene_based_sdg.html?highlight=COCO)

*Step-by-step scene-based synthetic data generation (SDG) in Isaac Sim/Replicator (triggers, writers, annotations such as COCO) with runnable script patterns.*

<details>
<summary>Key content</summary>

- **What Isaac Sim is (definition):** A reference application built on **NVIDIA Omniverse** for developing, simulating, and testing **AI-driven robots** in **physically-based virtual environments**.
- **Core enabling tech (design rationale):**
  - Uses **Universal Scene Description (USD)** as the *unifying interchange format* for scenes/assets; USD is **open-source**, **extensible**, and widely adopted across VFX, robotics, manufacturing, etc.
  - Simulation uses a **high-fidelity GPU-based PhysX engine**, enabling **industrial-scale** simulation and **multi-sensor RTX rendering**.
  - Direct GPU access supports simulated sensors: **cameras**, **RTX Lidars**, and **contact sensors**—used to build **digital twins** so pipelines can run before deploying on real robots.
- **Synthetic data workflow components (procedure-level pointers):**
  - Synthetic data collection is done with **Replicator** (SDG tooling).
  - Environment orchestration can be done through **Omnigraph**.
  - Physics realism can be tuned via **PhysX simulation parameters** to better match reality (sim-to-real).
- **Integration/deployment context (why it matters):**
  - Omniverse Kit provides plugin-based app infrastructure and a Python interpreter for scripting/extensions.
  - Bridges exist for **ROS 2** and integration with **NVIDIA Isaac ROS** for real robot communication.

</details>

### 🔍 Omniverse end-to-end Gaussian Splatting pipeline (tools + workflow map)
**Explainer** · [source](https://www.youtube.com/watch?v=KZqv3Z5rRg8)

*End-to-end Omniverse pipeline walkthrough (capture/ingest → train splats → visualize/stream in Omniverse), including practical integration steps and tooling choices.*

<details>
<summary>Key content</summary>

- **Use case framing:** Gaussian Splatting positioned as a method for **real-time 3D reconstruction** supporting **spatial intelligence** applications such as **geospatial digital twins** and **media & entertainment** workflows.
- **Pipeline components called out (library/tooling index):**
  - **NVIDIA Omniverse workflows** for:  
    1) **city-scale capture**,  
    2) **virtual production environments**,  
    3) **dynamic scene rendering**.
  - **Key spatial intelligence libraries mentioned for integration:**
    - **Omniverse NuRec**
    - **3DGRUT**
    - **PPISP**
- **Data/scene representation anchor:** Integration is described as **USD-based Omniverse pipelines** (OpenUSD as the scene interchange/assembly layer for bringing reconstructed content into Omniverse for visualization/rendering/streaming).
- **Practical integration emphasis:** The session is explicitly about “**building pipelines**” (not just theory): how Gaussian Splatting fits into Omniverse workflows from reconstruction outputs into **Omniverse visualization and rendering** contexts.

</details>

---

## Related Topics

- [[topics/nerf|NeRF]]
