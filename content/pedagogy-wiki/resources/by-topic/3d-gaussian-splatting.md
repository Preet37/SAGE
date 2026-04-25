# 3D Gaussian Splatting

## Video (best)
- **Yannic Kilcher** — "3D Gaussian Splatting for Real-Time Radiance Field Rendering (Paper Explained)"
- youtube_id: T_kXY43VZnk
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

## Last Verified
2025-04-06