# Audio Speech Models

## Video (best)
- **Andrej Karpathy** — "Let's build GPT: from scratch, in code, spelled out."
- youtube_id: kCc8FmEb1nY
- Why: Clear, practical introduction to transformer language models; transfers well to *audio language models* and *audio tokenization* concepts even though the demo is text.
- Level: Intermediate

## Blog / Written explainer (best)
- **Jay Alammar** — "The Illustrated Transformer"
- url: https://jalammar.github.io/illustrated-transformer/
- Why: Best high-level visual explanation of transformers; foundational for understanding Whisper-style ASR, TTS models, and audio LMs.
- Level: Beginner → Intermediate

## Deep dive
- **OpenAI** — "Whisper" (model + paper + usage)
- Why: Canonical reference for modern automatic speech recognition (speech-to-text) with a practical repo and paper.
- Level: Intermediate  
- url: https://github.com/openai/whisper

- **Meta AI** — "Audiocraft" (MusicGen and audio generation tooling)
- Why: Practical deep dive into *music generation* and audio generation pipelines; useful for understanding audio tokenization + generation stacks.
- Level: Intermediate  
- url: https://github.com/facebookresearch/audiocraft

## Original paper
- **Radford et al. (OpenAI)** — "Robust Speech Recognition via Large-Scale Weak Supervision" (Whisper)
- Why: Foundational ASR paper for Whisper; covers training setup, data, robustness, and evaluation.
- Level: Intermediate → Advanced  
- url: https://arxiv.org/abs/2212.04356

- **Défossez et al. (Meta AI)** — "High Fidelity Neural Audio Compression" (EnCodec)
- Why: Core reference for *audio tokenization* via neural audio codecs; widely used in downstream audio language models.
- Level: Advanced  
- url: https://arxiv.org/abs/2210.13438

## Code walkthrough
- **OpenAI** — Whisper repository (reference implementation)
- Why: Straightforward codebase to study end-to-end ASR inference (feature extraction, decoding, timestamps).
- Level: Intermediate  
- url: https://github.com/openai/whisper

- **Meta AI** — EnCodec repository
- Why: Practical implementation of neural audio compression/tokenization; useful for understanding discrete audio representations.
- Level: Advanced  
- url: https://github.com/facebookresearch/encodec

## Coverage notes
- Strong: Whisper / automatic speech recognition (speech-to-text); transformer foundations; EnCodec-style audio tokenization; music generation tooling (MusicGen via Audiocraft).
- Weak: Text-to-speech systems (especially VALL-E, Bark) and voice cloning—high-quality, stable, primary resources are less consistently available in canonical “teaching” formats.
- Gap: A single, educator-grade walkthrough that connects *audio tokenization → audio language model → TTS/voice cloning* end-to-end (with modern discrete codec tokens and practical training details).

## Last Verified
2026-04-09