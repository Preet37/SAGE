# Card: True Temporal Super-Resolution via Deep Internal Learning
**Source:** https://ar5iv.labs.arxiv.org/html/2003.08872  
**Role:** paper | **Need:** CONCEPT_EXPLAINER  
**Anchor:** Temporal SR (beyond interpolation) + internal, video-specific training; coarse-to-fine temporal×2 with spatial/temporal back-projection.

## Key Content
- **TSR vs interpolation (Abstract/Intro):** True Temporal Super-Resolution (TSR) recovers **high temporal frequencies beyond the input Nyquist limit**, resolving **motion blur + motion aliasing**; frame interpolation cannot undo either (it “adds new blurry frames” and preserves aliased motion).
- **Forward model (Intro):** Low-temporal-resolution (LTR) video relates to high-temporal-resolution (HTR) via **temporal blur + subsampling**:  
  **LTR = (HTR ⊛ₜ h) ↓ₜ**  
  where **h** is a **rectangular temporal blur kernel** induced by exposure time; paper often assumes **exposure time ≈ inter-frame time**.
- **Key observation (Sec. 2):** Small **space-time (ST) patches** recur not only **across scales** but also **across dimensions** by **swapping spatial and temporal axes** (x–t, y–t slices). Fast motion makes x–t/y–t slices look like **temporally downscaled** versions of x–y frames → x–y frames provide internal supervision for temporal upsampling.
- **Internal training set (Sec. 3):**
  - **Within-dimension pairs:** build a spatio-temporal pyramid; **downscale space+time by same factor** to preserve motion/blur statistics; create LTR by **temporal blur (frame averaging) + subsample**.
  - **Across-dimension pairs:** rotate 3D volume (swap x↔t or y↔t), apply “temporal” downscaling along the new time axis; use as extra training pairs.
  - Augmentations: mirror flips, **90° rotations**, time reversal.
- **Network & optimization (Sec. 4.1):** **8-layer 3D CNN**, 128 channels each, ReLU; mix of **3×3×3** and **1×3×3** kernels, stride 1; input is **cubic temporally interpolated** video; network predicts **residual** to HTR. Training crops: **36×36×16** ST crop, sampled proportional to mean gradient magnitude. Loss: **L1**. Optimizer: **Adam**. LR starts **1e-3**, decreased per ZSSR schedule until **1e-6** stop.
- **Coarse-to-fine (Sec. 4.2):** Train on spatially downscaled video (typically **¼**, or **½** for small videos). Apply TSR×2, then **spatio-temporal back-projection** to raise spatial res ×2 while enforcing **bicubic spatial consistency** and **rect temporal consistency**; iterate up the diagonal to target.
- **Runtime (Sec. 4.1):** ~**2 hours/video** training on **single Nvidia V100**; inference at **720×1280** takes ~**1 minute**.
- **Empirical (Sec. 5, Table 2 ablation at coarse scale):**  
  - Only within: **PSNR 33.96**, **SSIM 0.962**  
  - Only across: **PSNR 34.25 (+0.28)**, **SSIM 0.964 (+0.002)**  
  - Best config: **PSNR 34.33 (+0.37)**, **SSIM 0.965 (+0.003)**  
  Cross-dimension examples often more informative; preferences vary by video.

## When to surface
Use when students ask why “temporal SR” is different from frame interpolation, how TSR can correct aliasing/blur, or how internal/self-supervised video-specific training and coarse-to-fine temporal×2 pipelines work.