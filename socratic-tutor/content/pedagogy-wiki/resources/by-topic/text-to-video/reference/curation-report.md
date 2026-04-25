# Curation Report: Text-to-Video Generation
**Topic:** `text-to-video` | **Date:** 2026-04-09 16:36
**Library:** 6 existing → 18 sources (12 added, 9 downloaded)
**Candidates evaluated:** 40
**Reviewer verdict:** needs_additions

## Added (12)
- **[paper]** [Video Diffusion Models - NeurIPS](https://proceedings.neurips.cc/paper_files/paper/2022/file/39235c56aef13fb05a6adc95eb9d8d66-Paper-Conference.pdf)
  This is a primary, peer-reviewed source with concrete training and sampling procedures for video diffusion, suitable for step-by-step explanations beyond blog-level summaries.
- **[paper]** [Temporal Super-Resolution using Deep Internal Learning - ar5iv](https://ar5iv.labs.arxiv.org/html/2003.08872)
  Provides an authoritative end-to-end large-scale text-to-video pipeline blueprint (cascades, SR stages, scaling rationale) that tutors can use to explain modern production-grade designs.
- **[benchmark]** [VBench++: Comprehensive and Versatile Benchmark Suite for Video Generative Models](https://arxiv.org/html/2411.13503)
  Directly fills the need for concrete, standardized evaluation numbers and metric breakdowns that can be cited when students ask 'how do we measure video generation quality?'.
- **[benchmark]** [[CVPR2024 Highlight] VBench - We Evaluate Video Generation](https://github.com/Vchitect/VBench)
  Complements the paper with executable evaluation code, which is crucial for teaching how metrics are actually computed and for reproducing benchmark tables.
- **[reference_doc]** [OpenAI Platform](https://platform.openai.com/docs/api-reference/whisper/create)
  Official API reference is the most citable source for exact parameter names, constraints, and default behaviors in speech-to-text pipelines that often accompany text-to-video systems.
- **[paper]** [VALL-E 2: Neural Codec Language Models are](http://arxiv.org/pdf/2406.05370.pdf)
  Adds a primary-source, modern speech-to-speech/TTS formulation centered on discrete codec tokens, enabling precise answers about how audio is represented and generated in VALL-E-style systems.
- **[reference_doc]** [Video generation with Sora | OpenAI API](https://platform.openai.com/docs/guides/video-generation)
  This is the exact “thin but authoritative” page that answers parameter-name/constraint questions students ask when moving from papers to production usage; it directly fills the still-unfilled API-reference need.
- **[reference_doc]** [Models - OpenAI API](https://platform.openai.com/docs/models)
  Even if brief, this is the canonical place to cite model-level constraints and selection guidance; it complements the Sora guide and prevents hand-wavy answers about “which model supports video.”
- **[paper]** [Video Diffusion Models](https://arxiv.org/abs/2204.03458)
  This is the seminal VDM paper itself (not just a mention); it contains the concrete factorization and algorithmic procedure needed for step-by-step tutoring and should be in the core library.
- **[reference_doc]** [Video generation with Sora | OpenAI API](https://platform.openai.com/docs/guides/video-generation) *(promoted by reviewer)*
  This is the exact “thin but authoritative” page that answers parameter-name/constraint questions students ask when moving from papers to production usage; it directly fills the still-unfilled API-reference need.
- **[reference_doc]** [Models - OpenAI API](https://platform.openai.com/docs/models) *(promoted by reviewer)*
  Even if brief, this is the canonical place to cite model-level constraints and selection guidance; it complements the Sora guide and prevents hand-wavy answers about “which model supports video.”
- **[paper]** [Video Diffusion Models](https://arxiv.org/abs/2204.03458) *(promoted by reviewer)*
  This is the seminal VDM paper itself (not just a mention); it contains the concrete factorization and algorithmic procedure needed for step-by-step tutoring and should be in the core library.

## Near-Misses (3) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **Client Secrets | OpenAI API Reference** — [Client Secrets | OpenAI API Reference](https://platform.openai.com/docs/api-reference/realtime-sessions)
  _Skipped because:_ Useful for realtime session setup, but it does not provide the core production text-to-video model parameter defaults/constraints the need calls out.
- **Speech to text - OpenAI API** — [Speech to text - OpenAI API](https://platform.openai.com/docs/guides/speech-to-text/supported-languages%5C)
  _Skipped because:_ Good operational detail (languages), but less central than the endpoint reference for precise parameter/default questions.
- **Tacotron2 — Torchaudio 2.9.0 documentation** — [Tacotron2 — Torchaudio 2.9.0 documentation](https://docs.pytorch.org/audio/stable/generated/torchaudio.models.Tacotron2.html)
  _Skipped because:_ Provides model hyperparameters but not the primary signal-processing equations (STFT/mel filterbank) or vocoder likelihood/objectives requested.

## Reasoning
**Curator:** Selections prioritize authoritative primary sources that add either (a) reproducible benchmark numbers/code (VBench) or (b) concrete system/training procedures (Video Diffusion Models, Imagen Video cascade) plus official API specs (Whisper) and a modern discrete-codec TTS formulation (VALL-E 2). Key gaps remain for DiT-style video transformer equations and official production text-to-video API defaults.
**Reviewer:** The curator’s additions are mostly strong, but they missed two key official OpenAI docs that directly satisfy the unfilled production API-parameter need, and they should explicitly include the seminal Video Diffusion Models paper URL as a primary procedural reference.
