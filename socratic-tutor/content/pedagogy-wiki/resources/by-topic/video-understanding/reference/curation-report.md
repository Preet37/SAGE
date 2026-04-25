# Curation Report: Video Understanding
**Topic:** `video-understanding` | **Date:** 2026-04-09 18:35
**Library:** 6 existing → 20 sources (14 added, 9 downloaded)
**Candidates evaluated:** 50
**Reviewer verdict:** needs_additions

## Added (14)
- **[paper]** [VideoCLIP: Contrastive Pre-training for Zero-shot Video-Text Understanding](https://arxiv.org/pdf/2109.14084.pdf)
  Gives a concrete, citable end-to-end recipe for modern video-language pretraining (sampling/alignment/objective), which the tutor can use to explain why contrastive learning and temporal overlap matter for video understanding.
- **[benchmark]** [Video-MME: The First-Ever Comprehensive Evaluation ...](https://arxiv.org/html/2405.21075v3)
  Directly supplies long-form video understanding numbers and structured breakdowns that support Socratic discussions about temporal context, frame budgets, and the impact of auxiliary modalities like subtitles.
- **[benchmark]** [EgoSchema: A Diagnostic Benchmark for Very Long-form Video Language Understanding](https://proceedings.neurips.cc/paper_files/paper/2023/file/90ce332aff156b910b002ce4e6880dec-Paper-Datasets_and_Benchmarks.pdf)
  Adds an authoritative long-video QA benchmark with clear task framing and baseline performance, useful for teaching what makes long-form video understanding hard and how evaluation is structured.
- **[explainer]** [Video Understanding with Large Language Models: A Survey](https://arxiv.org/html/2312.17432v5)
  Provides a structured map of model families and design choices the tutor can use to compare action recognition vs captioning vs video-language chat, and to justify why certain architectures suit certain tasks.
- **[reference_doc]** [GPT-4o (OpenAI model overview)](https://openai.com/index/gpt-4o/)
  It was treated as pricing-adjacent in the near-miss notes, but official model pages are often the only stable, citable place that states supported modalities and high-level constraints—useful as a reference spine even if details live in platform docs.
- **[reference_doc]** [OpenAI API Documentation (Platform docs)](https://platform.openai.com/docs)
  The library already includes this, but the stated unfilled need is exactly what platform docs are for; the fix is to explicitly include the most specific subpages/sections for video inputs rather than rejecting docs as 'thin'.
- **[reference_doc]** [Gemini (Google DeepMind product/technology page)](https://deepmind.google/technologies/gemini/)
  Similarly, even if high-level, this is the canonical Google-owned reference that can be cited for modality support and used to route learners to the exact parameter docs.
- **[paper]** [Text-Conditioned Resampler for Long Form Video Understanding](https://arxiv.org/abs/2312.11897)
  The current additions emphasize benchmarks and contrastive pretraining, but there is no dedicated source explaining a modern long-form frame selection/resampling mechanism—this paper provides an actionable procedure and design rationale.
- **[benchmark]** [Open-vocabulary Video Question Answering: A New Benchmark for Evaluating the Generalizability of Video Question Answering Models](https://arxiv.org/pdf/2308.09363.pdf)
  The library is heavy on long-form context benchmarks (Video-MME/EgoSchema) but lacks a benchmark explicitly targeting open-vocabulary/generalization; this adds specific evaluation numbers for that core concept.
- **[reference_doc]** [GPT-4o (OpenAI model overview)](https://openai.com/index/gpt-4o/) *(promoted by reviewer)*
  It was treated as pricing-adjacent in the near-miss notes, but official model pages are often the only stable, citable place that states supported modalities and high-level constraints—useful as a reference spine even if details live in platform docs.
- **[reference_doc]** [OpenAI API Documentation (Platform docs)](https://platform.openai.com/docs) *(promoted by reviewer)*
  The library already includes this, but the stated unfilled need is exactly what platform docs are for; the fix is to explicitly include the most specific subpages/sections for video inputs rather than rejecting docs as 'thin'.
- **[reference_doc]** [Gemini (Google DeepMind product/technology page)](https://deepmind.google/technologies/gemini/) *(promoted by reviewer)*
  Similarly, even if high-level, this is the canonical Google-owned reference that can be cited for modality support and used to route learners to the exact parameter docs.
- **[paper]** [Text-Conditioned Resampler for Long Form Video Understanding](https://arxiv.org/abs/2312.11897) *(promoted by reviewer)*
  The current additions emphasize benchmarks and contrastive pretraining, but there is no dedicated source explaining a modern long-form frame selection/resampling mechanism—this paper provides an actionable procedure and design rationale.
- **[benchmark]** [Open-vocabulary Video Question Answering: A New Benchmark for Evaluating the Generalizability of Video Question Answering Models](https://arxiv.org/pdf/2308.09363.pdf) *(promoted by reviewer)*
  The library is heavy on long-form context benchmarks (Video-MME/EgoSchema) but lacks a benchmark explicitly targeting open-vocabulary/generalization; this adds specific evaluation numbers for that core concept.

## Near-Misses (4) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **Video-Language Understanding: A Survey from Model ...** — [Video-Language Understanding: A Survey from Model ...](https://arxiv.org/html/2406.05615v2)
  _Skipped because:_ Another strong survey, but adding both surveys would be redundant versus using one slot for additional benchmarks/API specs that are currently missing.
- **GPT-4o Model | OpenAI API** — [GPT-4o Model | OpenAI API](https://platform.openai.com/docs/models/gpt-4o)
  _Skipped because:_ Useful for model overview, but the provided candidate snippet is pricing-focused and does not clearly anchor parameter-level video input limits/defaults (formats, max duration/frames, sampling behavior, token accounting).
- **Pricing | OpenAI API** — [Pricing | OpenAI API](https://platform.openai.com/docs/pricing)
  _Skipped because:_ Has concrete cost numbers, but it does not satisfy the requested video-input API parameter reference (formats, duration/frame caps, sampling defaults, latency limits).
- **🦩Flamingo: a Visual Language Model** — [🦩Flamingo: a Visual Language Model](https://proceedings.neurips.cc/paper_files/paper/2022/file/960a172bc7fbf0177ccccbb411a7d800-Paper-Conference.pdf)
  _Skipped because:_ Seminal for multimodal in-context learning, but it is not specifically video-focused and would not directly provide the frame sampling/temporal modeling pipeline details requested for modern video-language models.

## Reasoning
**Curator:** Selections prioritize (1) concrete training/inference pipeline detail (VideoCLIP), (2) long-form benchmark tables with length/frame breakdowns (Video-MME, EgoSchema), and (3) a survey that supports structured family-level comparisons. API-level video specs and runnable pipelines were not adequately covered by the provided candidates.
**Reviewer:** The curator’s benchmark/survey picks are strong, but the library still needs at least one authoritative long-video architecture/procedure source and should explicitly include the official API reference entry points (even if thin) plus a complementary benchmark targeting generalization beyond long-context.
