# Curation Report: Vision-Language Models
**Topic:** `vision-language-models` | **Date:** 2026-04-09 16:39
**Library:** 6 existing → 20 sources (14 added, 10 downloaded)
**Candidates evaluated:** 47
**Reviewer verdict:** needs_additions

## Added (14)
- **[paper]** [[PDF] Flamingo: a Visual Language Model for Few-Shot Learning](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/tackling-multiple-tasks-with-a-single-visual-language-model/flamingo.pdf)
  This is the primary-source Flamingo paper PDF (DeepMind-hosted) with the most authoritative architectural equations and module-level details needed for precise Socratic explanations.
- **[paper]** [[PDF] BLIP-2: Bootstrapping Language-Image Pre-training with Frozen ...](https://proceedings.mlr.press/v202/li23q/li23q.pdf)
  The PMLR camera-ready BLIP-2 paper is the most citable source for the exact Q-Former objective/loss definitions and the precise training setup beyond blog-level summaries.
- **[benchmark]** [🦩Flamingo: a Visual Language Model](https://proceedings.neurips.cc/paper_files/paper/2022/file/960a172bc7fbf0177ccccbb411a7d800-Supplemental-Conference.pdf)
  The supplemental contains the densest set of concrete numbers and ablations (often omitted from summaries), which the tutor can quote when students ask for exact performance comparisons.
- **[reference_doc]** [Images and vision - OpenAI API](https://platform.openai.com/docs/guides/images-vision)
  This is the authoritative OpenAI platform guide for vision inputs and is the best candidate here for production-facing API specifics and defaults that can be cited.
- **[paper]** [arXiv:2305.19924v2 [cs.CV] 1 Jun 2023](https://arxiv.org/pdf/2305.19924.pdf)
  Among the candidates, this provides the most directly usable compute/throughput-vs-accuracy comparison material for visual tokenization/summarization strategies.
- **[paper]** [Perceiver-VL: Efficient Vision-and-Language Modeling ...](https://openaccess.thecvf.com/content/WACV2023/papers/Tang_Perceiver-VL_Efficient_Vision-and-Language_Modeling_With_Iterative_Latent_Attention_WACV_2023_paper.pdf)
  This adds an alternative, well-documented fusion/token-bottleneck design with empirical comparisons that help the tutor explain why resampling/latent bottlenecks can be more efficient.
- **[reference_doc]** [OpenAI API Reference (Images)](https://platform.openai.com/docs/api-reference/images)
  Even if “thin,” the API reference is the canonical place for precise field names and behaviors that a Socratic tutor must cite when students ask implementation-specific questions.
- **[reference_doc]** [Vision fine-tuning (OpenAI Docs)](https://platform.openai.com/docs/guides/vision-fine-tuning)
  This directly addresses the “authoritative recipes” gap (even if vendor-specific) and provides concrete procedural guidance beyond architecture papers.
- **[paper]** [Flamingo: a Visual Language Model for Few-Shot Learning (ar5iv HTML)](https://ar5iv.labs.arxiv.org/html/2204.14198)
  Not redundant with the PDF in practice: the HTML rendering is far easier to quote precisely in tutoring contexts and to locate exact module definitions quickly.
- **[paper]** [BLIP-2: Bootstrapping Language-Image Pre-training with Frozen Image Encoders and Large Language Models (arXiv PDF)](https://arxiv.org/pdf/2312.16886.pdf)
  If the PMLR PDF link ever breaks or is paywalled/unstable in some environments, the arXiv PDF is the most robust fallback for the same equations and training objective definitions.
- **[reference_doc]** [OpenAI API Reference (Images)](https://platform.openai.com/docs/api-reference/images) *(promoted by reviewer)*
  Even if “thin,” the API reference is the canonical place for precise field names and behaviors that a Socratic tutor must cite when students ask implementation-specific questions.
- **[reference_doc]** [Vision fine-tuning (OpenAI Docs)](https://platform.openai.com/docs/guides/vision-fine-tuning) *(promoted by reviewer)*
  This directly addresses the “authoritative recipes” gap (even if vendor-specific) and provides concrete procedural guidance beyond architecture papers.
- **[paper]** [Flamingo: a Visual Language Model for Few-Shot Learning (ar5iv HTML)](https://ar5iv.labs.arxiv.org/html/2204.14198) *(promoted by reviewer)*
  Not redundant with the PDF in practice: the HTML rendering is far easier to quote precisely in tutoring contexts and to locate exact module definitions quickly.
- **[paper]** [BLIP-2: Bootstrapping Language-Image Pre-training with Frozen Image Encoders and Large Language Models (arXiv PDF)](https://arxiv.org/pdf/2312.16886.pdf) *(promoted by reviewer)*
  If the PMLR PDF link ever breaks or is paywalled/unstable in some environments, the arXiv PDF is the most robust fallback for the same equations and training objective definitions.

## Near-Misses (3) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **BLIP-2: Bootstrapping Language-Image Pre-training with Froze** — [BLIP-2: Bootstrapping Language-Image Pre-training with Frozen Image Encoders and Large Language Models](https://arxiv.org/html/2301.12597)
  _Skipped because:_ Close to the PMLR PDF, but the camera-ready proceedings version is the most stable/citable for exact equations and loss definitions.
- **🦩Flamingo: a Visual Language Model** — [🦩Flamingo: a Visual Language Model](https://proceedings.neurips.cc/paper_files/paper/2022/file/960a172bc7fbf0177ccccbb411a7d800-Paper-Conference.pdf)
  _Skipped because:_ Selected the DeepMind-hosted PDF as the primary formula anchor and the NeurIPS supplemental for dense tables; adding the main NeurIPS PDF would be redundant under the 6-source cap.
- **OpenAI Platform** — [OpenAI Platform](https://platform.openai.com/docs/guides/vision/faq)
  _Skipped because:_ Useful clarifications, but the main Images/Vision guide is the better single anchor for API usage patterns and constraints.

## Reasoning
**Curator:** Selections prioritize primary-source PDFs for exact architectural equations/losses (Flamingo, BLIP-2), dense empirical tables/ablations (Flamingo supplement), official production API documentation (OpenAI vision guide), and quantitative efficiency/compute tradeoff comparisons for visual token strategies (token summarization + Perceiver-style bottlenecks).
**Reviewer:** The curator’s core paper choices are strong, but they should add at least one canonical API reference page (and optionally a procedural fine-tuning guide) because “thin” docs and step-by-step workflows are exactly what students ask for when moving from concepts to implementation.
