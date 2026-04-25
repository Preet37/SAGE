# Curation Report: 3D Gaussian Splatting
**Topic:** `3d-gaussian-splatting` | **Date:** 2026-04-09 16:11
**Library:** 3 existing → 18 sources (15 added, 10 downloaded)
**Candidates evaluated:** 45
**Reviewer verdict:** needs_additions

## Added (15)
- **[paper]** [[PDF] EWA Splatting - UMD Department of Computer Science](https://www.cs.umd.edu/~zwicker/publications/EWASplatting-TVCG02.pdf)
  This is the canonical, fully mathematical reference for EWA splatting, including the covariance/footprint computation under projection and the exact elliptical Gaussian evaluation needed to explain 3DGS-style rasterization rigorously.
- **[benchmark]** [NerfBaselines: Consistent and Reproducible Evaluation of ...](https://arxiv.org/html/2406.17345v1)
  An independent benchmarking framework is the most reliable way to obtain citable, reproducible numbers and to teach students how to evaluate 3DGS vs NeRF variants consistently.
- **[reference_doc]** [API — omni_replicator 1.4.4 documentation](https://docs.omniverse.nvidia.com/py/replicator/1.4.4/source/extensions/omni.replicator.core/docs/API.html)
  This is official NVIDIA documentation with concrete callable signatures and defaults the tutor can quote when teaching Omniverse Replicator-based dataset generation for 3DGS training.
- **[explainer]** [Building Gaussian Splatting Pipelines for Spatial Intelligence With NVIDIA Omniverse](https://www.youtube.com/watch?v=KZqv3Z5rRg8)
  Provides an authoritative, runnable workflow narrative for getting 3DGS into Omniverse, which is exactly what students need when moving from theory to a working digital-twin visualization pipeline.
- **[paper]** [Constructing Temporal Digital Twins of Plants with Gaussian Splats](https://arxiv.org/html/2505.10923v1)
  Among the candidates, this is the closest to a real digital-twin deployment context (not just NVS benchmarks), helping the tutor discuss system architecture and update/temporal aspects relevant to production.
- **[reference_doc]** [Omniverse Replicator Core API (v1.4.0) — omni.replicator.core](https://docs.omniverse.nvidia.com/py/replicator/1.4.0/source/extensions/omni.replicator.core/docs/API.html)
  Even if “thin,” this is precisely the kind of authoritative parameter/default reference a tutor needs; it also complements the curator’s 1.4.4 doc by providing a stable, citable API page and versioned behavior notes.
- **[reference_doc]** [Generate Synthetic Data — Omniverse Workflows (Defect Detection)](https://docs.omniverse.nvidia.com/workflows/latest/defect-detection/generate_data.html)
  This is an official, runnable workflow-style guide (not just API surface) that can be adapted into a “generate data → train 3DGS” teaching pipeline, directly addressing the missing authoritative working example.
- **[explainer]** [Isaac Sim Replicator Tutorial — Scene Based Synthetic Dataset Generation](https://docs.omniverse.nvidia.com/isaacsim/latest/replicator_tutorials/tutorial_replicator_scene_based_sdg.html?highlight=COCO)
  It’s an official tutorial with actionable code patterns and dataset-writing details that are typically missing from high-level blogs—useful for teaching how to actually produce training data for 3DGS pipelines.
- **[paper]** [From Fields to Splats: A Cross-Domain Survey of Real-Time Neural Rendering (incl. 3DGS for SLAM/telepresence)](https://arxiv.org/html/2509.23555v1)
  Even without being a single deployment report, this survey consolidates operational considerations and pipeline architectures across robotics/telepresence—exactly the missing “how it’s used in systems” context for a Socratic tutor.
- **[paper]** [Mon3tr: Monocular 3D Telepresence with Pre-built Gaussian ...](https://arxiv.org/html/2601.07518v1)
  This is closer to the requested production-style case study than many NVS-only papers: it frames 3DGS in an end-to-end telepresence system with measurable runtime constraints.
- **[reference_doc]** [Omniverse Replicator Core API (v1.4.0) — omni.replicator.core](https://docs.omniverse.nvidia.com/py/replicator/1.4.0/source/extensions/omni.replicator.core/docs/API.html) *(promoted by reviewer)*
  Even if “thin,” this is precisely the kind of authoritative parameter/default reference a tutor needs; it also complements the curator’s 1.4.4 doc by providing a stable, citable API page and versioned behavior notes.
- **[reference_doc]** [Generate Synthetic Data — Omniverse Workflows (Defect Detection)](https://docs.omniverse.nvidia.com/workflows/latest/defect-detection/generate_data.html) *(promoted by reviewer)*
  This is an official, runnable workflow-style guide (not just API surface) that can be adapted into a “generate data → train 3DGS” teaching pipeline, directly addressing the missing authoritative working example.
- **[explainer]** [Isaac Sim Replicator Tutorial — Scene Based Synthetic Dataset Generation](https://docs.omniverse.nvidia.com/isaacsim/latest/replicator_tutorials/tutorial_replicator_scene_based_sdg.html?highlight=COCO) *(promoted by reviewer)*
  It’s an official tutorial with actionable code patterns and dataset-writing details that are typically missing from high-level blogs—useful for teaching how to actually produce training data for 3DGS pipelines.
- **[paper]** [From Fields to Splats: A Cross-Domain Survey of Real-Time Neural Rendering (incl. 3DGS for SLAM/telepresence)](https://arxiv.org/html/2509.23555v1) *(promoted by reviewer)*
  Even without being a single deployment report, this survey consolidates operational considerations and pipeline architectures across robotics/telepresence—exactly the missing “how it’s used in systems” context for a Socratic tutor.
- **[paper]** [Mon3tr: Monocular 3D Telepresence with Pre-built Gaussian ...](https://arxiv.org/html/2601.07518v1) *(promoted by reviewer)*
  This is closer to the requested production-style case study than many NVS-only papers: it frames 3DGS in an end-to-end telepresence system with measurable runtime constraints.

## Near-Misses (3) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **Shapes** — [Shapes](https://docs.omniverse.nvidia.com/py/replicator/1.11.35/source/extensions/omni.replicator.core/docs/API.html)
  _Skipped because:_ Likely newer, but the candidate snippet is too thin/ambiguous (appears mis-titled) to justify preferring it over the clearly identified 1.4.4 API reference.
- **[PDF] Generalizable Pixel-wise 3D Gaussian Splatting for Rea** — [[PDF] Generalizable Pixel-wise 3D Gaussian Splatting for Real-time ...](https://openaccess.thecvf.com/content/CVPR2024/papers/Zheng_GPS-Gaussian_Generalizable_Pixel-wise_3D_Gaussian_Splatting_for_Real-time_Human_Novel_CVPR_2024_paper.pdf)
  _Skipped because:_ Strong experiments/ablations, but it is focused on a specific generalizable human setting rather than broad, independent 3DGS-vs-NeRF benchmarking across the standard datasets requested.
- **Accelerating 3D Gaussian Splatting with Spherical ...** — [Accelerating 3D Gaussian Splatting with Spherical ...](https://arxiv.org/html/2501.00342v1)
  _Skipped because:_ Contains useful speed/memory experiments, but it is method-specific and not as generally reusable for standardized cross-method comparisons as a dedicated benchmarking framework.

## Reasoning
**Curator:** Selections prioritize (1) the seminal EWA splatting derivation for exact rasterization math, (2) an independent reproducible benchmarking framework for trustworthy numbers, and (3) official Omniverse Replicator API docs plus the most directly relevant Omniverse pipeline walkthrough and a digital-twin-oriented paper for deployment context.
**Reviewer:** The core 3DGS + EWA math and benchmarking choices are solid, but the library should add the official Omniverse workflow/tutorial docs for runnable SDG pipelines and at least one systems/telepresence-oriented 3DGS source to cover deployment architecture and operational constraints.
