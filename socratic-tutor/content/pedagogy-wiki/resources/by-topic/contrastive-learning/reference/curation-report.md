# Curation Report: Contrastive Learning
**Topic:** `contrastive-learning` | **Date:** 2026-04-09 16:16
**Library:** 4 existing → 13 sources (9 added, 6 downloaded)
**Candidates evaluated:** 43
**Reviewer verdict:** needs_additions

## Added (9)
- **[code]** [open_clip/README.md at main · mlfoundations/open_clip](https://github.com/mlfoundations/open_clip/blob/main/README.md)
  This is the most authoritative, widely used OpenCLIP reference for practical defaults and configuration surfaces, and it directly points to the exact code paths a tutor can cite for preprocessing and training/inference settings.
- **[paper]** [Sigmoid Loss for Language Image Pre-Training - arXiv.org](https://arxiv.org/abs/2303.15343)
  Primary source for SigLIP’s design rationale and training pipeline; it gives the tutor the exact objective and the motivation for why sigmoid changes the role of negatives and batch-size scaling.
- **[benchmark]** [[PDF] arXiv:2303.15343v3 [cs.CV] 4 May 2023 - OpenReview](https://arxiv.org/pdf/2303.15343v3.pdf)
  Provides concrete, citable benchmark numbers and ablations tied directly to SigLIP’s claims about batch-size scaling and performance, which are central to the missing empirical comparisons.
- **[paper]** [Learning Transferable Visual Models From Natural Language Supervision (CLIP)](https://arxiv.org/abs/2103.00020)
  This is the canonical source for the exact dual-encoder contrastive objective and training setup; it directly fills the missing primary formula/derivation need better than secondary temperature-tuning papers.
- **[paper]** [LiT: Zero-Shot Transfer with Locked-image Text Tuning](https://arxiv.org/pdf/2212.01758.pdf)
  Even if the snippet looked like a discussion, the paper is a strong empirical and procedural reference for CLIP-family training variants and provides citable numbers that help contextualize CLIP/OpenCLIP/SigLIP-style objectives.
- **[paper]** [Interpreting and Analyzing CLIP's Zero-Shot Image Classification via ...](https://arxiv.org/html/2410.13016v1)
  This fills a gap in concept/process coverage: how CLIP-style contrastive pretraining translates into the zero-shot classifier and what drives its behavior, which is valuable for Socratic teaching beyond just objectives and benchmarks.
- **[paper]** [Learning Transferable Visual Models From Natural Language Supervision (CLIP)](https://arxiv.org/abs/2103.00020) *(promoted by reviewer)*
  This is the canonical source for the exact dual-encoder contrastive objective and training setup; it directly fills the missing primary formula/derivation need better than secondary temperature-tuning papers.
- **[paper]** [LiT: Zero-Shot Transfer with Locked-image Text Tuning](https://arxiv.org/pdf/2212.01758.pdf) *(promoted by reviewer)*
  Even if the snippet looked like a discussion, the paper is a strong empirical and procedural reference for CLIP-family training variants and provides citable numbers that help contextualize CLIP/OpenCLIP/SigLIP-style objectives.
- **[paper]** [Interpreting and Analyzing CLIP's Zero-Shot Image Classification via ...](https://arxiv.org/html/2410.13016v1) *(promoted by reviewer)*
  This fills a gap in concept/process coverage: how CLIP-style contrastive pretraining translates into the zero-shot classifier and what drives its behavior, which is valuable for Socratic teaching beyond just objectives and benchmarks.

## Near-Misses (2) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **SigLIP 2: Multilingual Vision-Language Encoders with ...** — [SigLIP 2: Multilingual Vision-Language Encoders with ...](https://arxiv.org/pdf/2502.14786.pdf)
  _Skipped because:_ Likely valuable for updated recipes and multilingual extensions, but it is SigLIP2 (not the requested SigLIP baseline) and may complicate CLIP-vs-OpenCLIP-vs-SigLIP comparisons for an introductory reference set.
- **Proper way to handle non-square images with CLIP? - Models** — [Proper way to handle non-square images with CLIP? - Models](https://discuss.huggingface.co/t/proper-way-to-handle-non-square-images-with-clip/32813)
  _Skipped because:_ Community forum guidance is not authoritative API documentation and is less citable than official library docs/repos for preprocessing defaults.

## Reasoning
**Curator:** Selections prioritize primary sources (SigLIP paper/PDF) for objective + rationale + citable results, and the OpenCLIP README as the most authoritative entry point to real-world defaults and runnable code paths. Several needs remain unfilled because the provided candidates did not include the original CLIP paper/API docs or official end-to-end example notebooks/scripts.
**Reviewer:** The curator’s SigLIP/OpenCLIP additions are strong, but the library still needs the canonical CLIP paper as the explicit formula source plus at least one CLIP-family benchmark/procedure paper and one authoritative analysis of the zero-shot pipeline.
