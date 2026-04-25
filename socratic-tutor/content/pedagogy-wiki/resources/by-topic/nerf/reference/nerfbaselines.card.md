# Card: NerfBaselines (consistent NeRF/NVS benchmarking)
**Source:** https://nerfbaselines.github.io  
**Role:** benchmark | **Need:** EMPIRICAL_DATA  
**Anchor:** Standardized benchmark tables across methods with PSNR/SSIM/LPIPS (+ some runtime notes) under consistent evaluation protocols.

## Key Content
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

## When to surface
Use when students ask “Which NeRF/NVS method is better on dataset X?” or when resolving **metric/protocol mismatches** (downscaling, background color, half-image evaluation, tau settings) that affect PSNR/SSIM/LPIPS comparisons.