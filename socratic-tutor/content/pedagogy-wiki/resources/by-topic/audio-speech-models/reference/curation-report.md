# Curation Report: Audio and Speech Models
**Topic:** `audio-speech-models` | **Date:** 2026-04-09 18:31
**Library:** 5 existing → 14 sources (9 added, 6 downloaded)
**Candidates evaluated:** 49
**Reviewer verdict:** needs_additions

## Added (9)
- **[reference_doc]** [Customize voice and sound with SSML](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/speech-synthesis-markup-voice)
  Official Microsoft documentation that the tutor can cite for production-grade TTS control parameters and constraints, including what is required vs optional in SSML and how to specify voice/style.
- **[benchmark]** [[PDF] Robust Speech Recognition via Large-Scale Weak Supervision](https://cdn.openai.com/papers/whisper.pdf)
  This is the authoritative source for Whisper’s reported WER results and evaluation methodology, suitable for quoting exact benchmark numbers and the conditions under which they were obtained.
- **[paper]** [[2301.02111] Neural Codec Language Models are Zero-Shot Text to Speech Synthesizers](https://arxiv.org/abs/2301.02111)
  Primary technical report for VALL-E-style voice cloning; provides the design rationale for treating TTS as conditional language modeling over codec tokens and describes training/inference flow.
- **[paper]** [SoundStream: An End-to-End Neural Audio Codec](https://arxiv.org/pdf/2107.03312.pdf)
  This is a canonical neural audio codec paper with the quantization math and training procedure the library is currently missing; it complements EnCodec by providing the foundational equations and design rationale.
- **[paper]** [Building Accurate Low Latency ASR for Streaming Voice](https://aclanthology.org/2023.acl-industry.26.pdf)
  It directly fills the deployment-case gap with an industry-style, end-to-end streaming ASR description and measurable outcomes—more citable and structured than blog posts or GitHub discussions.
- **[paper]** [SCDiar: a streaming diarization system based on speaker change detection](https://arxiv.org/pdf/2501.16641.pdf)
  Diarization is a common real-world ASR adjunct (meeting transcription, call centers) and this paper provides a concrete streaming architecture and metrics, which the current library lacks.
- **[paper]** [SoundStream: An End-to-End Neural Audio Codec](https://arxiv.org/pdf/2107.03312.pdf) *(promoted by reviewer)*
  This is a canonical neural audio codec paper with the quantization math and training procedure the library is currently missing; it complements EnCodec by providing the foundational equations and design rationale.
- **[paper]** [Building Accurate Low Latency ASR for Streaming Voice](https://aclanthology.org/2023.acl-industry.26.pdf) *(promoted by reviewer)*
  It directly fills the deployment-case gap with an industry-style, end-to-end streaming ASR description and measurable outcomes—more citable and structured than blog posts or GitHub discussions.
- **[paper]** [SCDiar: a streaming diarization system based on speaker change detection](https://arxiv.org/pdf/2501.16641.pdf) *(promoted by reviewer)*
  Diarization is a common real-world ASR adjunct (meeting transcription, call centers) and this paper provides a concrete streaming architecture and metrics, which the current library lacks.

## Near-Misses (3) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **VALL-E R: Robust and Efficient Zero-Shot Text-to-Speech ...** — [VALL-E R: Robust and Efficient Zero-Shot Text-to-Speech ...](https://arxiv.org/html/2406.07855v1)
  _Skipped because:_ Useful follow-on work, but the original VALL-E report is the more canonical reference for the core step-by-step pipeline and rationale.
- **Replicating WER on FLEURS · openai whisper · Discussion #207** — [Replicating WER on FLEURS · openai whisper · Discussion #2076](https://github.com/openai/whisper/discussions/2076)
  _Skipped because:_ Potentially helpful for reproduction details, but it is not as stable/authoritative or comprehensive as the official paper for citable benchmark numbers.
- **Whisper Deployment Decisions: Part I — Evaluating Latency, C** — [Whisper Deployment Decisions: Part I — Evaluating Latency, Costs ...](https://www.ml6.eu/en/blog/whisper-deployment-decisions-part-i-evaluating-latency-costs-and-performance-metrics)
  _Skipped because:_ Practical, but it is a third-party blog (not a formal case study/paper) and may not provide sufficiently rigorous, broadly citable deployment metrics across settings.

## Reasoning
**Curator:** Selections prioritize authoritative, citable sources that directly provide (1) official API surfaces/defaults and (2) primary-paper benchmark numbers and system design descriptions. Candidates that were derivative, unstable, or insufficiently rigorous were kept as near-misses rather than added.
**Reviewer:** The curator’s core picks are solid, but the library still needs at least one canonical neural-codec math source (SoundStream) and one or two real-world streaming system papers with concrete latency/architecture details (ACL Industry streaming ASR, SCDiar).
