## Core Definitions

**LiDAR (Light Detection and Ranging).** An active depth sensor that emits near-infrared light and measures **time-of-flight (ToF)** of the returned reflection to estimate range; performance depends on returned reflected light along the emitted beam path (arXiv:2309.10504, Sec. II).

**Depth camera (stereo IR depth).** A depth camera like the Intel D455 estimates depth by **stereo disparity** using an IR stereo pair; depth is computed from focal length, baseline, and disparity (arXiv:2309.10504, Sec. II).

**Point cloud.** A set of 3D points representing sampled surface/scene geometry (often with attributes like color or normals). In 3D Gaussian Splatting pipelines, a sparse point cloud from **Structure-from-Motion (SfM)/COLMAP** is used as initialization (Hugging Face Gaussian Splatting blog; graphdeco-inria/gaussian-splatting README).

**Sensor fusion.** Combining multiple sensor measurements (e.g., LiDAR + radar + depth camera) into a single estimate for downstream tasks; in practice often implemented with Bayesian filtering (Bayes filter → Kalman/EKF/UKF) as in *Probabilistic Robotics* and KF/EKF/UKF implementations (ProbabilisticRobotics.pdf; TheGreatGalaxy/sensor-fusion repo).

**Belief (state estimate) in Bayes filtering.** The posterior distribution over state given all measurements and controls up to time \(t\):  
\(bel(x_t)=p(x_t\mid z_{1:t},u_{1:t})\) (ProbabilisticRobotics.pdf, Eq. 2.35).

**NeRF (Neural Radiance Field).** A scene representation as a learned 5D function mapping 3D position and viewing direction to color and density:  
\(F_\theta(\mathbf{x},\mathbf{d})\rightarrow(\mathbf{c},\sigma)\) (arXiv:2210.00379v6; arXiv:2509.23555, Sec. III-B; Mildenhall et al. NeRF project/paper).

**Volumetric rendering / alpha compositing (NeRF-style).** Rendering a pixel by integrating color contributions along a ray, weighted by transmittance and density; discretized as a weighted sum with \(\alpha_i=1-\exp(-\sigma_i\delta_i)\) and \(w_i=T_i\alpha_i\) (MIT Vision Book Ch.45; arXiv:2210.00379v6; arXiv:2209.02417).

**3D Gaussian Splatting (3DGS).** An explicit scene representation using many anisotropic 3D Gaussians with parameters such as **center \(\mu\)**, **covariance \(\Sigma\)**, **opacity \(\alpha\)**, and **color \(\mathbf{c}\)** (often view-dependent via spherical harmonics), rendered via differentiable rasterization and ordered alpha compositing (arXiv:2509.23555, Sec. III-C; Hugging Face Gaussian Splatting blog; graphdeco-inria/gaussian-splatting README).

**EWA splatting (elliptical weighted average).** A rendering/resampling approach where a 3D Gaussian kernel projects under perspective to a **screen-space ellipse/conic**, and splatting uses a Gaussian low-pass filter to avoid aliasing; the footprint is computed from projected covariance and rasterized within a threshold (Zwicker et al., EWASplatting-TVCG02).

**Tactile sensing.** Sensing via physical contact (force/pressure/contact events). In Isaac Sim, “contact sensors” are among the simulated sensors used for robotics development and digital twins (Isaac Sim Replicator tutorial card).

---

## Key Formulas & Empirical Results

### Depth camera stereo geometry (depth from disparity)
From arXiv:2309.10504 (Sec. II), Intel D455 depth:
\[
Z = \frac{f\,b}{d}
\]
- \(Z\): depth  
- \(f\): focal length  
- \(b\): stereo baseline  
- \(d\): disparity  
**Supports:** why depth error grows with distance (disparity shrinks as \(Z\) increases).

### Bayes filter belief definitions (sensor fusion foundation)
From *Probabilistic Robotics* (ProbabilisticRobotics.pdf):
- Posterior belief (Eq. 2.35): \(bel(x_t)=p(x_t\mid z_{1:t},u_{1:t})\)  
- Prediction belief (Eq. 2.36): \(\overline{bel}(x_t)=p(x_t\mid z_{1:t-1},u_{1:t})\)  
- Markov assumptions (Eq. 2.33–2.34): transition depends on \((x_{t-1},u_t)\); measurement depends only on \(x_t\).  
**Supports:** recursive predict→update structure used by KF/EKF/UKF.

### NeRF volumetric rendering (continuous + discrete)
From arXiv:2210.00379v6 and MIT Vision Book Ch.45:
- Continuous (ray integral):
\[
C(\mathbf{r})=\int T(t)\,\sigma(\mathbf{r}(t))\,\mathbf{c}(\mathbf{r}(t),\mathbf{d})\,dt,\quad
T(t)=\exp\!\left(-\int \sigma(\mathbf{r}(s))ds\right)
\]
- Discrete alpha compositing:
\[
\hat{C}(\mathbf{r})=\sum_i T_i\,\alpha_i\,\mathbf{c}_i,\quad
\alpha_i=1-\exp(-\sigma_i\delta_i)
\]
From arXiv:2209.02417 (discrete weights):
\[
w_i=T_i\alpha_i,\quad
T_i=\exp\!\left(-\sum_{j<i}\sigma_j\delta_j\right)=\prod_{j<i}(1-\alpha_j)
\]
**Supports:** where NeRF “weights” come from; how density becomes opacity.

### Expected depth from NeRF weights
From arXiv:2210.00379v6 (Eq. 6–7):
\[
\mathbb{E}[t]\approx \sum_i T_i\alpha_i t_i
\]
**Supports:** extracting depth-like signals from volumetric rendering.

### DS-NeRF depth supervision loss (sparse depth priors)
From Deng et al. (CVPR 2022) DS-NeRF:
- Define termination distribution \(h(t)=T(t)\sigma(t)\).  
- Depth supervision via KL-style objective (Sec. 3.2):
\[
L_{\text{Depth}}=\mathbb{E}_{\mathbf{x}_i\in X_j}\int \log h(t)\exp\!\left(-\frac{(t-D_{ij})^2}{2\hat{\sigma}_i^2}\right)dt
\]
Total loss: \(L=L_{\text{Color}}+\lambda_D L_{\text{Depth}}\).  
**Empirical anchors:** NeRF Real 2-view PSNR: NeRF 13.5 vs DS-NeRF(KL) 20.2; depth error 20.32 vs 10.41 (paper tables cited in card).  
**Supports:** how sparse SfM depth can regularize NeRF.

### Nerfstudio ray sampling defaults (implementation reference)
From nerfstudio ray samplers module:
- `ProposalNetworkSampler` defaults:  
  `num_proposal_samples_per_ray=(64,)`, `num_nerf_samples_per_ray=32`, `num_proposal_network_iterations=2`.  
- `PDFSampler` defaults: `histogram_padding=0.01`, `include_original=True`, `train_stratified=True`.  
- `VolumetricSampler` occupancy sampling uses `alpha_thre=0.01` (Instant-NGP-style).  
**Supports:** answering “how many samples / what does stratified mean / what thresholds are used?”

### Nerfstudio camera model & distortion parameterization
From nerfstudio Cameras API:
- `distortion_params` are 6 params in OpenCV order: **[k1, k2, k3, k4, p1, p2]**.  
- `camera_to_worlds` are per-image **c2w** 3×4 matrices \([R|t]\).  
**Supports:** practical questions about intrinsics/extrinsics and distortion handling.

### LiDAR vs RADAR vs depth camera robustness (measured)
From arXiv:2309.10504:
- White surface baseline max range: LiDAR **10 m**, RADAR **7 m**, depth camera **6 m**.  
- Ill-reflective black surface: LiDAR max **3 m** (**33%** of baseline); RADAR max **7.5 m**; depth camera remains **6 m**.  
- Static ranging MAE: LiDAR **<5 cm up to 8.5 m** (white); RADAR ~**10–15 cm**; depth camera MAE **61 cm at 6 m** (white).  
- Dynamic lap times (fusion impact): LiDAR+Depth **7.686 s** best; LiDAR-only **7.729 s**; LiDAR+RADAR **8.011 s**.  
**Supports:** concrete fusion justification and failure modes on dark/ill-reflective materials.

### 3DGS vs NeRF for real-time systems (FPS/latency anchors)
From arXiv:2509.23555:
- 3DGS-SLAM end-to-end **3–30 FPS**, rendering often **>100 FPS (up to 1000 FPS)**; NeRF-SLAM **3–15 FPS**.  
**Supports:** why 3DGS is favored for interactive SLAM/telepresence.

### EWA splatting: projected footprint and rasterization threshold
From Zwicker et al.:
- 3D Gaussian:
\[
G^3_V(x-p)=\frac{1}{(2\pi)^{3/2}|V|^{1/2}}\exp\!\left(-\tfrac12(x-p)^T V^{-1}(x-p)\right)
\]
- Projected variance (Eq. 31): \(V'_k = J_k\,W\,V_k\,W^T\,J_k^T\)  
- Screen-space conic uses \(Q=(\hat V'_k+V_h)^{-1}\); evaluate within \(r(\Delta x)=\Delta x^T Q \Delta x < c\), typically **\(c=4\)**.  
**Supports:** how 3D Gaussians become 2D ellipses and how rasterization is bounded.

---

## How It Works

### A. Typical robot perception → 3D understanding pipeline (multi-sensor)
1. **Acquire raw measurements**  
   - Cameras: RGB images.  
   - LiDAR: ToF returns → ranges along beams (arXiv:2309.10504).  
   - IMU/tactile: not deeply specified in sources here, but tactile/contact sensors appear in Isaac Sim context.
2. **Calibrate & synchronize**  
   - Estimate intrinsics/extrinsics; for camera pipelines, store per-image `camera_to_worlds` and intrinsics (nerfstudio Cameras API).
3. **Build geometric primitives**  
   - Depth camera: compute depth via \(Z=fb/d\) (arXiv:2309.10504).  
   - LiDAR: assemble 3D points in sensor frame; transform to world frame.  
   - Multi-view RGB: run SfM/COLMAP to get sparse point cloud + camera poses (Hugging Face 3DGS blog; DS-NeRF uses COLMAP too).
4. **Fuse / filter** (state estimation)  
   - Maintain belief \(bel(x_t)=p(x_t\mid z_{1:t},u_{1:t})\) and update recursively (ProbabilisticRobotics.pdf).  
   - Practical implementations: KF/EKF/UKF with radar/lidar measurement models (TheGreatGalaxy/sensor-fusion repo).
5. **Choose a 3D scene representation for downstream tasks**  
   - **Point cloud** for geometry and registration.  
   - **NeRF** for implicit radiance field + novel view synthesis (NeRF sources).  
   - **3DGS** for explicit primitives + fast rasterization (arXiv:2509.23555; graphdeco-inria/gaussian-splatting).

### B. NeRF training & rendering (mechanics)
1. **Inputs:** posed images (camera intrinsics/extrinsics).  
2. **For each training step:** sample rays/pixels; sample points along each ray (stratified bins).  
3. **Query network:** \(F_\theta(\mathbf{x},\mathbf{d})\to(\mathbf{c},\sigma)\).  
4. **Render:** compute \(\alpha_i=1-\exp(-\sigma_i\delta_i)\), transmittance \(T_i\), and sum \(\hat C=\sum_i T_i\alpha_i c_i\).  
5. **Loss:** photometric MSE (arXiv:2210.00379v6).  
6. **(Optional) Hierarchical sampling:** build PDF from coarse weights and resample (arXiv:2209.02417; nerfstudio PDFSampler/ProposalNetworkSampler).

### C. 3D Gaussian Splatting (3DGS) pipeline (mechanics)
1. **Initialize from SfM:** run COLMAP/SfM to obtain sparse point cloud + camera poses (Hugging Face 3DGS blog; graphdeco-inria/gaussian-splatting README).  
2. **Convert points → Gaussians:** each point becomes a Gaussian primitive with position and initial attributes.  
3. **Differentiable rasterization:** project Gaussians to screen-space ellipses (EWA theory gives the covariance-to-conic mapping; Zwicker et al.).  
4. **Alpha compositing:** order contributions and composite to render an image (arXiv:2509.23555, Sec. III-C).  
5. **Optimize Gaussian parameters:** minimize image reconstruction loss; update \(\mu,\Sigma,\alpha,\mathbf{c}\) (graphdeco-inria/gaussian-splatting README describes interleaved optimization + density control).  
6. **Densification/pruning:** clone/split/prune Gaussians based on gradient magnitude and coverage (arXiv:2509.23555, Sec. III-C; Hugging Face blog).

### D. Temporal digital twin with 3DGS (GrowSplat example)
From arXiv:2505.10923:
1. Capture per time step: **15 calibrated cameras** (3 layers × 5 cameras) → 15 images + poses.  
2. Train per-time-step 3DGS (Nerfstudio Splatfacto-MCMC); use segmentation masks and initial point clouds to stabilize with few views.  
3. Filter GS points (log-scale range, scale ratio, quaternion norm).  
4. Compute normals → FPFH features.  
5. Coarse alignment: FPFH matching + RANSAC + Fast Global Registration (FGR).  
6. Fine alignment: ICP, improved with Colored ICP.  
7. Registration model: \(T(P_t)=R(P_t)+D(P_t;\theta)\) (rigid + non-rigid deformation field).

---

## Teaching Approaches

### Intuitive (no math): “What does the robot *know* about 3D?”
- LiDAR/depth cameras give **direct distance samples** (sparse but metric).  
- Cameras give **appearance**; with multiple views you can infer 3D by matching features (SfM) or by learning a renderer (NeRF/3DGS).  
- Fusion is about **not trusting any single sensor**: when LiDAR fails on black surfaces, radar or stereo may still work (arXiv:2309.10504).

### Technical (with math): “Rendering as weighted accumulation”
- NeRF: pixel color is a **weighted sum** along a ray where weights \(w_i=T_i\alpha_i\) come from density \(\sigma_i\) and spacing \(\delta_i\) (arXiv:2209.02417).  
- Depth supervision (DS-NeRF): encourage the termination distribution \(h(t)=T(t)\sigma(t)\) to concentrate near known depths \(D_{ij}\) (DS-NeRF).

### Analogy-based: “Triangles vs Gaussians”
- Classic graphics draws **triangles** via rasterization; 3DGS draws **Gaussians** via rasterization (Hugging Face 3DGS blog).  
- NeRF is like storing the scene in a **function you query repeatedly** (ray marching); 3DGS is like storing the scene in **many explicit blobs** you can draw quickly (arXiv:2509.23555).

---

## Common Misconceptions

1. **“A point cloud is the same thing as a 3D Gaussian Splat model.”**  
   - **Why wrong:** a point cloud is just discrete points; 3DGS attaches **covariance/opacity/color** and is rendered via **differentiable rasterization + alpha compositing** (arXiv:2509.23555).  
   - **Correct model:** point clouds are often *initialization* (SfM) or geometry; 3DGS is an optimized set of anisotropic volumetric primitives.

2. **“NeRF depth is a single surface intersection like ray casting.”**  
   - **Why wrong:** NeRF uses **volumetric rendering**; contributions come from many samples with weights \(w_i=T_i\alpha_i\), and depth is often an **expectation** \(\sum_i w_i t_i\) (arXiv:2210.00379v6).  
   - **Correct model:** NeRF represents a *distribution of opacity along the ray*, not a hard surface unless the learned density collapses.

3. **“LiDAR always works better than cameras for depth.”**  
   - **Why wrong:** LiDAR can fail badly on **ill-reflective black surfaces** (max range drops from 10 m to 3 m in the cited setup), while stereo depth camera kept 6 m max range (arXiv:2309.10504).  
   - **Correct model:** each modality has material/lighting failure modes; fusion is often justified empirically.

4. **“Sensor fusion just means averaging measurements.”**  
   - **Why wrong:** Bayes filtering defines belief updates using transition and measurement models under Markov assumptions (ProbabilisticRobotics.pdf).  
   - **Correct model:** fusion is probabilistic inference: predict with dynamics, update with sensor likelihoods.

5. **“Reported PSNR/SSIM numbers across NeRF/3DGS papers are directly comparable.”**  
   - **Why wrong:** evaluation protocol differences (downscaling source, JPEG artifacts, background color, SSIM params, LPIPS backbone) can shift metrics materially (NerfBaselines arXiv:2406.17345; nerfbaselines site notes).  
   - **Correct model:** comparisons require standardized protocols (NerfBaselines harness).

---

## Worked Examples

### 1) Quick modality robustness “decision” example (using cited numbers)
**Scenario:** mobile robot must detect obstacles up to ~6–8 m; environment includes dark/ill-reflective objects.

**Use the arXiv:2309.10504 results as a lookup:**
- On white: LiDAR MAE **<5 cm up to 8.5 m**; depth camera MAE grows to **61 cm at 6 m**.  
- On black: LiDAR max range drops to **3 m**, while depth camera still reaches **6 m**, radar **7.5 m**.

**Tutor move (mid-conversation): ask student to choose a fusion strategy**
- If you need accurate mid-range geometry on normal surfaces: prioritize **LiDAR**.  
- If you must handle black/ill-reflective obstacles beyond 3 m: ensure **depth camera and/or radar** can take over when LiDAR returns drop out.  
- Tie to downstream impact: LiDAR+Depth had best lap time **7.686 s** vs LiDAR-only **7.729 s** and LiDAR+RADAR **8.011 s** in that study.

### 2) Nerfstudio camera distortion parameter mapping (GrowSplat deployment detail)
From arXiv:2505.10923 (Sec. III-B):
- Maxi-Marvin uses a **division distortion model** (single radial coefficient).  
- Nerfstudio expects **6 distortion params**: \([k1,k2,k3,k4,p1,p2]\).  
- Their conversion: set **K1, K2**, and **P1=P2=0**, with **K3=K4=0** as defaults.

**Tutor use:** when a student asks “why does my Nerfstudio import want 6 distortion params?”, you can cite this exact workaround pattern.

---

## Comparisons & Trade-offs

| Topic | LiDAR | Depth camera (IR stereo, e.g., D455) | FMCW RADAR |
|---|---|---|---|
| Principle | Active ToF NIR (arXiv:2309.10504) | Disparity \(Z=fb/d\) (arXiv:2309.10504) | Beat frequency for range; phase across chirps for velocity (arXiv:2309.10504) |
| White-surface max range (study setup) | 10 m | 6 m | 7 m |
| Black/ill-reflective max range | 3 m (33% of baseline) | 6 m | 7.5 m |
| Typical static MAE (study) | <5 cm up to 8.5 m (white) | 61 cm at 6 m (white) | ~10–15 cm |
| Common failure mode highlighted | Low reflectivity → dropouts | Error increases with distance (small disparity) | More false positives at short range |

| Topic | NeRF | 3D Gaussian Splatting (3DGS) |
|---|---|---|
| Representation | Implicit function \(F_\theta(\mathbf{x},\mathbf{d})\to(\mathbf{c},\sigma)\) (arXiv:2509.23555) | Explicit Gaussians \(\mu,\Sigma,\alpha,\mathbf{c}\) (arXiv:2509.23555) |
| Rendering | Ray marching + volumetric compositing (MIT Vision Book; arXiv:2209.02417) | Rasterization + ordered alpha compositing (arXiv:2509.23555) |
| Real-time suitability (surveyed) | NeRF-SLAM 3–15 FPS (arXiv:2509.23555) | 3DGS-SLAM 3–30 FPS end-to-end; rendering often >100 FPS up to 1000 FPS (arXiv:2509.23555) |
| Practical pitfall | Slow convergence / sampling cost | Higher memory (many primitives) (arXiv:2509.23555) |

**When to choose:**  
- Choose **LiDAR** when you need accurate metric depth on typical materials and can tolerate reflectivity failures via redundancy.  
- Choose **3DGS** over NeRF when interactive rendering/telepresence/SLAM latency is critical (arXiv:2509.23555).  
- Choose **NeRF** when you want an implicit field with standard volumetric rendering math and can afford slower training/rendering (NeRF sources).

---

## Prerequisite Connections

- **Coordinate frames & camera geometry.** Needed to interpret `camera_to_worlds`, intrinsics, and ray generation (nerfstudio Cameras API).  
- **Probability & Bayes rule.** Needed to understand belief updates and why fusion is inference, not averaging (ProbabilisticRobotics.pdf).  
- **Ray-based rendering intuition.** Needed to understand NeRF’s integral/discretization and why weights sum to a pixel color (MIT Vision Book Ch.45).  
- **Basic optimization (gradient descent).** Needed to understand training of NeRF/3DGS as minimizing photometric loss with differentiable rendering (NeRF sources; 3DGS sources).

---

## Socratic Question Bank

1. **If LiDAR max range collapses on a black surface, what property of the sensing principle is being violated?**  
   *Good answer:* LiDAR depends on returned reflected NIR; low reflectivity reduces returns (arXiv:2309.10504).

2. **In NeRF’s discrete rendering, what does \(T_i\) represent physically, and how is it computed from earlier samples?**  
   *Good answer:* transmittance/probability ray hasn’t “hit” density; \(T_i=\prod_{j<i}(1-\alpha_j)\) (arXiv:2209.02417).

3. **Why does stereo depth error tend to increase with distance, using \(Z=fb/d\)?**  
   *Good answer:* disparity \(d\) shrinks with distance; small disparity errors cause large depth errors (arXiv:2309.10504).

4. **What is the difference between a point cloud from SfM and a trained 3DGS model?**  
   *Good answer:* SfM gives sparse points/poses; 3DGS optimizes Gaussian covariances/opacities/colors for rendering (Hugging Face blog; arXiv:2509.23555).

5. **If two papers report different PSNR for “the same method,” what protocol differences could explain it?**  
   *Good answer:* downscaling source (JPEG artifacts), background color, SSIM/LPIPS settings; need standardized harness (arXiv:2406.17345; nerfbaselines site).

6. **How does DS-NeRF use sparse SfM depth to change what NeRF learns along a ray?**  
   *Good answer:* adds depth loss encouraging termination distribution \(h(t)\) to concentrate near \(D_{ij}\) (DS-NeRF).

7. **Why might 3DGS be preferred for telepresence/SLAM rendering even if both can produce photorealistic views?**  
   *Good answer:* rasterization enables very high rendering FPS; NeRF ray marching is slower (arXiv:2509.23555).

8. **In Bayes filtering terms, what’s the difference between \(\overline{bel}(x_t)\) and \(bel(x_t)\)?**  
   *Good answer:* predicted belief before incorporating \(z_t\) vs posterior after measurement update (ProbabilisticRobotics.pdf).

---

## Likely Student Questions

**Q: What’s the exact depth-from-disparity equation for a stereo depth camera?**  
→ **A:** \(Z=\frac{f\,b}{d}\), where \(f\) is focal length, \(b\) baseline, \(d\) disparity (arXiv:2309.10504, Sec. II).

**Q: Where do NeRF’s rendering weights \(w_i\) come from?**  
→ **A:** \(w_i=T_i\alpha_i\), with \(\alpha_i=1-\exp(-\sigma_i\delta_i)\) and \(T_i=\exp(-\sum_{j<i}\sigma_j\delta_j)=\prod_{j<i}(1-\alpha_j)\) (arXiv:2209.02417; arXiv:2210.00379v6).

**Q: How can NeRF produce a depth map if it’s volumetric?**  
→ **A:** Use expected termination depth \(\mathbb{E}[t]\approx\sum_i T_i\alpha_i t_i\) (arXiv:2210.00379v6).

**Q: What are the measured failure modes of LiDAR on dark surfaces?**  
→ **A:** In the cited study, LiDAR max range dropped from **10 m (white)** to **3 m (black)**; reflectivity differences were quantified (e.g., black matt p-pol reflectivity 0.3%) (arXiv:2309.10504).

**Q: What distortion parameter format does Nerfstudio expect?**  
→ **A:** `distortion_params` has 6 OpenCV-ordered params **[k1, k2, k3, k4, p1, p2]** (nerfstudio Cameras API). GrowSplat notes converting a division model to this by setting tangential to 0 and unused radial terms to 0 (arXiv:2505.10923).

**Q: What are Nerfstudio’s default ray sampling counts for proposal sampling?**  
→ **A:** `ProposalNetworkSampler` defaults include `num_proposal_samples_per_ray=(64,)` and `num_nerf_samples_per_ray=32`, with `num_proposal_network_iterations=2` (nerfstudio ray samplers module).

**Q: Why are PSNR numbers for 3DGS vs NeRF sometimes “unfair”?**  
→ **A:** NerfBaselines reports that downscaling from originals vs using released downscaled JPEGs can change PSNR (notably outdoors), and other protocol differences (background color, metric settings) also matter; hence standardized evaluation harnesses (arXiv:2406.17345; nerfbaselines site).

**Q: What FPS ranges are reported for 3DGS-SLAM vs NeRF-SLAM?**  
→ **A:** Surveyed ranges: NeRF-SLAM **3–15 FPS**; 3DGS-SLAM **3–30 FPS end-to-end**, with rendering often **>100 FPS up to 1000 FPS** (arXiv:2509.23555).

---

## Available Resources

### Videos
- [3D Gaussian Splatting for Real-Time Radiance Field Rendering (Paper Explained)](https://youtube.com/watch?v=T_kXY43VZnk) — Surface when: student asks “how does 3DGS actually rasterize and train?” or wants math/implementation intuition.
- [3D Gaussian Splatting overview video](https://youtube.com/watch?v=VkIJbpdTujE) — Surface when: student wants a quick, non-mathy intuition for why splats feel “instant” vs NeRF.
- [NeRF: Representing Scenes as Neural Radiance Fields for View Synthesis (Paper Explained)](https://youtube.com/watch?v=CRlN-cYFxTk) — Surface when: student asks for a careful walkthrough of NeRF’s volume rendering and positional encoding.

### Articles & Tutorials
- [Mildenhall et al. — NeRF (paper)](https://arxiv.org/abs/2003.08934) — Surface when: student wants the canonical definition and original method details.
- [Matthew Tancik — NeRF project page](https://www.matthewtancik.com/nerf) — Surface when: student wants the official pipeline description and qualitative results context.
- [bmild/nerf (official code)](https://github.com/bmild/nerf) — Surface when: student asks “what does the reference implementation look like?”
- [graphdeco-inria/gaussian-splatting (official 3DGS repo)](https://github.com/graphdeco-inria/gaussian-splatting) — Surface when: student asks about the practical 3DGS training loop, densification/pruning, or official artifacts.
- [NerfBaselines paper (reproducible benchmarking)](https://arxiv.org/html/2406.17345v1) — Surface when: student asks why metrics differ across papers or how to benchmark fairly.
- [NerfBaselines site](https://nerfbaselines.github.io) — Surface when: student asks “which method is best on dataset X?” and you need protocol notes.
- [Nerfstudio Cameras API](https://docs.nerf.studio/reference/api/cameras.html) — Surface when: student asks about intrinsics/extrinsics/distortion or ray generation conventions.
- [Nerfstudio ray samplers module](https://docs.nerf.studio/_modules/nerfstudio/model_components/ray_samplers.html) — Surface when: student asks about stratified/PDF/proposal sampling defaults.
- [Isaac Sim Replicator tutorial (scene-based SDG)](https://docs.omniverse.nvidia.com/isaacsim/latest/replicator_tutorials/tutorial_replicator_scene_based_sdg.html?highlight=COCO) — Surface when: student asks how to generate synthetic multi-sensor data/digital twins in Omniverse.

---

## Visual Aids

![Triangle rasterization: the classical primitive analogous to Gaussian splatting. (Source: HuggingFace Blog)](/api/wiki-images/3d-gaussian-splatting/images/huggingface-co-blog-gaussian-splatting_001.png)  
**Show when:** student needs the “triangles vs Gaussians” rasterization analogy before 3DGS details.

![A single rasterized Gaussian with border — the core rendering primitive. (Source: HuggingFace Blog)](/api/wiki-images/3d-gaussian-splatting/images/huggingface-co-blog-gaussian-splatting_002.png)  
**Show when:** student asks “what is a Gaussian splat visually / what parameters does it have?”

![Three composited Gaussians — building blocks of a full 3DGS scene. (Source: HuggingFace Blog)](/api/wiki-images/3d-gaussian-splatting/images/huggingface-co-blog-gaussian-splatting_003.png)  
**Show when:** student asks how multiple splats combine (alpha compositing intuition).

![3D Gaussian ellipsoids in space before projection onto the image plane. (Source: HuggingFace Blog)](/api/wiki-images/3d-gaussian-splatting/images/huggingface-co-blog-gaussian-splatting_005.png)  
**Show when:** student is confused about 3D covariance/ellipsoids vs 2D screen-space ellipses.

![SfM point cloud from COLMAP — the initialization for 3D Gaussian Splatting training. (Source: HuggingFace Blog)](/api/wiki-images/3d-gaussian-splatting/images/huggingface-co-blog-gaussian-splatting_006.png)  
**Show when:** student asks “where do the initial Gaussians come from?”

![NeRF: Representing scenes as continuous volumetric functions. (Mildenhall et al.)](/api/wiki-images/nerf/images/matthewtancik-nerf_001.png)  
**Show when:** student needs the high-level NeRF concept (implicit volumetric function).

![NeRF pipeline: 5D coordinates → MLP → density & color → rendered image. (Mildenhall et al.)](/api/wiki-images/nerf/images/matthewtancik-nerf_002.svg)  
**Show when:** student asks for the exact NeRF pipeline stages (ray → samples → MLP → compositing).

---

## Key Sources

- [NeRF: Representing Scenes as Neural Radiance Fields for View Synthesis](https://arxiv.org/abs/2003.08934) — canonical NeRF definition and posed-image-to-rendered-view pipeline.
- [MIT Vision Book Ch.45: NeRF volume rendering](https://visionbook.mit.edu/nerf.html) — clean derivation of transmittance/opacity and discrete quadrature.
- [3D Gaussian Splatting for Real-Time Radiance Field Rendering (official repo)](https://github.com/graphdeco-inria/gaussian-splatting) — authoritative implementation framing (SfM init, optimization, densification/pruning).
- [Robustness of LiDAR vs RADAR vs Depth Camera on ill-reflective surfaces](https://arxiv.org/html/2309.10504) — concrete measured modality failure modes and fusion impact numbers.
- [NerfBaselines — Reproducible NeRF/3DGS Benchmarking](https://arxiv.org/html/2406.17345v1) — protocol standardization and why reported metrics differ across papers.