# Curation Report: Diffusion Models
**Topic:** `diffusion-models` | **Date:** 2026-04-09 16:17
**Library:** 4 existing → 14 sources (10 added, 6 downloaded)
**Candidates evaluated:** 21
**Reviewer verdict:** needs_additions

## Added (10)
- **[paper]** [[PDF] High-Resolution Image Synthesis With Latent Diffusion Models](https://openaccess.thecvf.com/content/CVPR2022/papers/Rombach_High-Resolution_Image_Synthesis_With_Latent_Diffusion_Models_CVPR_2022_paper.pdf)
  This is the primary, citable source for Stable Diffusion’s core design (latent-space diffusion + cross-attention text conditioning) and includes concrete architectural and training-procedure specifics the tutor can walk through step-by-step.
- **[paper]** [Adding Conditional Control to Text-to-Image Diffusion Models](https://openaccess.thecvf.com/content/ICCV2023/papers/Zhang_Adding_Conditional_Control_to_Text-to-Image_Diffusion_Models_ICCV_2023_paper.pdf)
  This is the authoritative ControlNet paper with diagrams and algorithmic description needed to precisely explain how ControlNet adds conditioning while keeping the pretrained diffusion backbone intact.
- **[paper]** [Denoising Diffusion Probabilistic Models](https://arxiv.org/abs/2006.11239)
  This is the canonical source for the exact training/sampling equations the library is explicitly missing; it’s already listed but should be explicitly promoted/anchored as the formula reference rather than relying on secondary explainers.
- **[paper]** [Classifier-Free Diffusion Guidance](https://arxiv.org/abs/2207.12598)
  Classifier-free guidance is a core operational concept for modern text-to-image diffusion, but it’s not covered as an authoritative primary source in the current library; this paper is the definitive reference.
- **[reference_doc]** [Diffusers API Reference: StableDiffusionPipeline](https://huggingface.co/docs/diffusers/api/pipelines/stable_diffusion/stable_diffusion)
  Forum threads drift, but the official API reference is precisely what’s needed for stable parameter semantics and teaching correct usage; even if “thin,” it’s the authoritative source.
- **[reference_doc]** [Diffusers API Reference: ControlNet Pipelines](https://huggingface.co/docs/diffusers/api/pipelines/controlnet)
  The ControlNet paper explains the method, but production tutoring needs the exact pipeline knobs learners will touch; the official docs provide the canonical parameter surface.
- **[paper]** [Denoising Diffusion Probabilistic Models](https://arxiv.org/abs/2006.11239) *(promoted by reviewer)*
  This is the canonical source for the exact training/sampling equations the library is explicitly missing; it’s already listed but should be explicitly promoted/anchored as the formula reference rather than relying on secondary explainers.
- **[paper]** [Classifier-Free Diffusion Guidance](https://arxiv.org/abs/2207.12598) *(promoted by reviewer)*
  Classifier-free guidance is a core operational concept for modern text-to-image diffusion, but it’s not covered as an authoritative primary source in the current library; this paper is the definitive reference.
- **[reference_doc]** [Diffusers API Reference: StableDiffusionPipeline](https://huggingface.co/docs/diffusers/api/pipelines/stable_diffusion/stable_diffusion) *(promoted by reviewer)*
  Forum threads drift, but the official API reference is precisely what’s needed for stable parameter semantics and teaching correct usage; even if “thin,” it’s the authoritative source.
- **[reference_doc]** [Diffusers API Reference: ControlNet Pipelines](https://huggingface.co/docs/diffusers/api/pipelines/controlnet) *(promoted by reviewer)*
  The ControlNet paper explains the method, but production tutoring needs the exact pipeline knobs learners will touch; the official docs provide the canonical parameter surface.

## Near-Misses (3) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **High-Resolution Image Synthesis with Latent Diffusion ...** — [High-Resolution Image Synthesis with Latent Diffusion ...](https://arxiv.org/abs/2112.10752)
  _Skipped because:_ Selected the CVPR PDF version instead because it is the camera-ready paper with stable pagination/figures for citation and teaching.
- **Adding Conditional Control to Text-to-Image Diffusion Models** — [Adding Conditional Control to Text-to-Image Diffusion Models](https://arxiv.org/html/2302.05543)
  _Skipped because:_ Selected the ICCV PDF for consistent formatting and easier citation of figures/algorithms; the HTML is useful but redundant.
- **What is DPMSolverMultistepScheduler for? - Hugging Face Foru** — [What is DPMSolverMultistepScheduler for? - Hugging Face Forums](https://discuss.huggingface.co/t/what-is-dpmsolvermultistepscheduler-for/93548)
  _Skipped because:_ Forum threads are not authoritative API references for defaults/parameter semantics and can drift with library versions.

## Reasoning
**Curator:** Only two candidates were truly primary/authoritative sources that directly fill missing conceptual and algorithmic gaps (LDM/Stable Diffusion pipeline and ControlNet). The remaining needs require seminal papers and official diffusers documentation that are not present among the provided candidates, so they are left unfilled with targeted search hints.
**Reviewer:** The curator’s paper choices are solid for LDM/ControlNet, but the library still needs an authoritative classifier-free guidance paper and official diffusers API reference pages to cover missing core formulas and production parameter semantics.
