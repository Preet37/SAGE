# Video Understanding

## Video (best)
- **Andrej Karpathy** — "Deep Dive into LLMs like ChatGPT" (context for multimodal/video LLMs; not video-specific)
- youtube_id: "None identified"
- Why: Clear mental models for transformer-based language models that underpin modern video-language models (Video-LLMs).
- Level: Intermediate

## Blog / Written explainer (best)
- **Lilian Weng (OpenAI)** — "Prompt Engineering"
- url: https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/
- Why: Practical prompting patterns that transfer directly to video QA/captioning workflows when using video-capable models (e.g., Gemini, GPT-4o).
- Level: Beginner–Intermediate

## Deep dive
- **OpenAI** — "GPT-4o" (system card / announcement + technical overview)
- Why: Primary-source description of a natively multimodal model family relevant to video understanding applications and evaluation framing.
- Level: Intermediate  
- url: https://openai.com/blog/hello-gpt-4o
- **Google DeepMind** — "Gemini 1.5" (long-context multimodal; relevant to long-form video understanding)
- Why: Primary-source overview of long-context multimodal modeling, a key enabler for long-form video comprehension.
- Level: Intermediate  
- url: https://deepmind.google/technologies/gemini/

## Original paper
- **A. Vaswani et al.** — "Attention Is All You Need"
- Why: Foundational transformer architecture used by modern video-language models and many video understanding systems.
- Level: Intermediate–Advanced  
- url: https://arxiv.org/abs/1706.03762
- **A. Radford et al. (OpenAI)** — "Learning Transferable Visual Models From Natural Language Supervision" (CLIP)
- Why: Core vision-language pretraining approach widely used as a component in video retrieval/search and as a building block for video-language systems.
- Level: Intermediate  
- url: https://arxiv.org/abs/2103.00020

## Code walkthrough
- **Hugging Face** — Transformers documentation (multimodal + video-related model support varies by release)
- Why: Most common practical entry point for running and adapting open multimodal models; useful for implementing video captioning/QA pipelines when supported.
- Level: Intermediate  
- url: https://huggingface.co/docs/transformers/index
- **OpenAI** — API docs (multimodal usage patterns; video support depends on current API capabilities)
- Why: Canonical reference for building video understanding applications with OpenAI models where available.
- Level: Intermediate  
- url: https://platform.openai.com/docs

## Coverage notes
- Strong: Transformer foundations; general multimodal model overviews (GPT-4o, Gemini); practical tooling entry points (HF Transformers).
- Weak: Single, educator-grade “Video Understanding 101” video that cleanly covers video QA, captioning, long-form understanding, and evaluation end-to-end.
- Gap: High-confidence, stable, video-specific deep-dive resources (especially for Video-LLMs, long-form video benchmarks, and action recognition) with clearly identifiable canonical videos/IDs.

## Last Verified
2026-04-09