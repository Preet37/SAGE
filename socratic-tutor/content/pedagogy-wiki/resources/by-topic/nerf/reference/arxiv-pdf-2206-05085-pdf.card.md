# Card: DVGOv2 speed/quality + efficient regularizers for voxel-grid NeRF
**Source:** https://arxiv.org/pdf/2206.05085.pdf  
**Role:** paper | **Need:** EMPIRICAL_DATA  
**Anchor:** concrete speed/quality tradeoffs + training procedure for DVGO-style dense voxel radiance fields

## Key Content
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

## When to surface
Use when students ask about **DVGO/DVGOv2 training steps**, **CUDA/occupancy-based NeRF acceleration**, or need **specific speed vs PSNR/SSIM/LPIPS numbers** and **distortion/TV regularization details** for voxel-grid radiance fields.