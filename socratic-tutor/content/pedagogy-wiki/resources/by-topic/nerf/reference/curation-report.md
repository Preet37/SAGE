# Curation Report: Neural Radiance Fields
**Topic:** `nerf` | **Date:** 2026-04-09 16:25
**Library:** 5 existing → 19 sources (14 added, 10 downloaded)
**Candidates evaluated:** 48
**Reviewer verdict:** needs_additions

## Added (14)
- **[explainer]** [[2101.05204] Neural Volume Rendering: NeRF and Beyond - ar5iv](https://ar5iv.labs.arxiv.org/html/2101.05204)
  This survey-style writeup consolidates and derives the core NeRF rendering math and sampling procedure with clearer notation than many implementations, making it easy to quote exact equations and explain why they work.
- **[benchmark]** [NerfBaselines](https://nerfbaselines.github.io)
  Provides a centralized, method-comparable set of quantitative results beyond the original NeRF paper, useful for answering “how much better/faster is X than Y?” with citable numbers.
- **[paper]** [Volume Rendering of Neural Implicit Surfaces](https://proceedings.neurips.cc/paper_files/paper/2021/file/25e2a30f44898b9f3e978b1786dcd85c-Paper.pdf)
  Gives a principled comparison point between NeRF-style volumetric fields and SDF-based methods, including criteria around geometry extraction and rendering behavior.
- **[reference_doc]** [Source code for nerfstudio.model_components.ray_samplers](https://docs.nerf.studio/_modules/nerfstudio/model_components/ray_samplers.html)
  Direct source-level documentation is the most reliable way to answer questions about actual defaults and how sampling is performed in a widely used toolkit.
- **[reference_doc]** [Cameras - nerfstudio](https://docs.nerf.studio/reference/api/cameras.html)
  Helps the tutor precisely explain dataset/camera conventions and avoid common pitfalls when students move from papers to real toolchains.
- **[paper]** [Depth-supervised NeRF: Fewer Views and Faster Training for Free](https://openaccess.thecvf.com/content/CVPR2022/papers/Deng_Depth-Supervised_NeRF_Fewer_Views_and_Faster_Training_for_Free_CVPR_2022_paper.pdf)
  Connects NeRF training to depth/point-cloud supervision with a concrete, step-by-step method and explicit loss terms—useful for explaining multi-sensor reconstruction and geometry stabilization.
- **[explainer]** [Radiance Fields (MIT Vision Book, Chapter 45)](https://visionbook.mit.edu/nerf.html)
  This is an authoritative, pedagogy-first source that often gets overlooked because it’s “just a chapter,” but it’s ideal for step-by-step teaching and for pinning down conventions/notation.
- **[explainer]** [Volume Rendering Digest (for NeRF)](https://arxiv.org/abs/2209.02417)
  Even if the library already has a NeRF survey, this digest is narrowly focused on the rendering math and is highly quotable for a Socratic tutor when students ask “where does this equation come from?”
- **[explainer]** [NeRF: Neural Radiance Field in 3D Vision: A Comprehensive Review](https://arxiv.org/html/2210.00379v6)
  The unfilled needs call for cross-method numbers; this review is one of the few single sources that aggregates many results in one place, even if hardware/runtime reporting is imperfect.
- **[paper]** [Improved Direct Voxel Grid Optimization for Radiance Fields Reconstruction (DVGOv2)](https://arxiv.org/pdf/2206.05085.pdf)
  The library is missing primary sources for major accelerations; this paper provides both a reproducible pipeline and specific quantitative comparisons that help teach why voxel/grid methods train faster.
- **[explainer]** [Radiance Fields (MIT Vision Book, Chapter 45)](https://visionbook.mit.edu/nerf.html) *(promoted by reviewer)*
  This is an authoritative, pedagogy-first source that often gets overlooked because it’s “just a chapter,” but it’s ideal for step-by-step teaching and for pinning down conventions/notation.
- **[explainer]** [Volume Rendering Digest (for NeRF)](https://arxiv.org/abs/2209.02417) *(promoted by reviewer)*
  Even if the library already has a NeRF survey, this digest is narrowly focused on the rendering math and is highly quotable for a Socratic tutor when students ask “where does this equation come from?”
- **[explainer]** [NeRF: Neural Radiance Field in 3D Vision: A Comprehensive Review](https://arxiv.org/html/2210.00379v6) *(promoted by reviewer)*
  The unfilled needs call for cross-method numbers; this review is one of the few single sources that aggregates many results in one place, even if hardware/runtime reporting is imperfect.
- **[paper]** [Improved Direct Voxel Grid Optimization for Radiance Fields Reconstruction (DVGOv2)](https://arxiv.org/pdf/2206.05085.pdf) *(promoted by reviewer)*
  The library is missing primary sources for major accelerations; this paper provides both a reproducible pipeline and specific quantitative comparisons that help teach why voxel/grid methods train faster.

## Near-Misses (3) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **DataManagers - nerfstudio** — [DataManagers - nerfstudio](https://docs.nerf.studio/developer_guides/pipelines/datamanagers.html)
  _Skipped because:_ Useful for dataset plumbing, but less directly anchored to the specific defaults (near/far, sampling thresholds) and camera conventions the tutor most needs to cite.
- **Models** — [Models](https://docs.nerf.studio/reference/api/models.html)
  _Skipped because:_ Good API surface overview, but the ray sampler module and camera reference are more directly tied to the concrete parameter defaults and conventions students ask about.
- **Evaluate Geometry of Radiance Fields with Low-frequency ...** — [Evaluate Geometry of Radiance Fields with Low-frequency ...](https://arxiv.org/html/2304.04351v2)
  _Skipped because:_ Strong for geometry evaluation metrics, but it is narrower than the selected implicit-surface rendering paper for broad NeRF-vs-surface representation comparison.

## Reasoning
**Curator:** Selections prioritize (1) authoritative equations/derivations for NeRF rendering and sampling, (2) a centralized benchmark hub for concrete metrics, (3) a principled NeRF-to-SDF comparison paper, and (4) source-of-truth toolkit docs for defaults and conventions, while leaving gaps only where the provided candidates did not directly contain the requested cross-method speed/memory or instant-ngp/nerfacc default specs.
**Reviewer:** The curator’s core picks are strong, but adding a pedagogy-grade formula chapter plus a rendering-math digest and a couple of sources with compiled/primary quantitative comparisons would materially improve teachability and coverage of the stated unfilled needs.
