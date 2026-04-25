# Curation Report: Tokenization
**Topic:** `tokenization` | **Date:** 2026-04-09 16:37
**Library:** 5 existing → 15 sources (10 added, 7 downloaded)
**Candidates evaluated:** 44
**Reviewer verdict:** needs_additions

## Added (10)
- **[paper]** [[PDF] High Fidelity Neural Audio Compression - arXiv.org](https://arxiv.org/pdf/2210.13438.pdf)
  This is the primary EnCodec paper and the most authoritative place to cite the exact RVQ math and training objective as used in EnCodec, including how multiple quantizers are stacked and optimized.
- **[paper]** [[2210.13438] High Fidelity Neural Audio Compression - arXiv](https://arxiv.org/abs/2210.13438)
  The paper provides the step-by-step system design narrative (not just equations), which is what a tutor needs to explain how speech tokenization via EnCodec works and why the design choices were made.
- **[benchmark]** [SoundStream: An End-to-End Neural Audio Codec](https://arxiv.org/pdf/2107.03312.pdf)
  Even though it is SoundStream (not EnCodec), it is a seminal neural codec paper with concrete empirical results and ablations that are directly useful for teaching bitrate–quality tradeoffs and quantizer-stack effects.
- **[benchmark]** [A Comparative Analysis of Subword Tokenization Methods - arXiv.org](https://arxiv.org/html/2411.17669v1)
  This directly targets the missing structured comparison need and is more likely than informal sources to provide citable, organized contrasts and evaluation dimensions for teaching tokenization choices.
- **[paper]** [Residual Quantization with Implicit Neural Codebooks](https://arxiv.org/pdf/2401.14732.pdf)
  Even if not EnCodec-specific, it is a recent, equation-heavy RVQ paper that strengthens the tutor’s ability to teach RVQ precisely (and contrast classical RVQ vs newer implicit-codebook training).
- **[reference_doc]** [torchaudio.save_with_torchcodec — PyTorch/TorchAudio API Reference](https://docs.pytorch.org/audio/stable/generated/torchaudio.save_with_torchcodec.html)
  This is precisely the kind of “thin but authoritative” page needed to pin down parameter names/defaults; it directly addresses the unfilled API-defaults need better than forum threads.
- **[reference_doc]** [TorchCodec audio_encoding.ipynb (official example notebook)](https://docs.pytorch.org/torchcodec/0.5/_downloads/11ef1d93158a89ea05a303d1d7c2cc02/audio_encoding.ipynb)
  Example notebooks often contain the missing operational details (recommended settings, typical workflows) that API pages omit; it’s an official source and helps teach the practical pipeline.
- **[paper]** [Residual Quantization with Implicit Neural Codebooks](https://arxiv.org/pdf/2401.14732.pdf) *(promoted by reviewer)*
  Even if not EnCodec-specific, it is a recent, equation-heavy RVQ paper that strengthens the tutor’s ability to teach RVQ precisely (and contrast classical RVQ vs newer implicit-codebook training).
- **[reference_doc]** [torchaudio.save_with_torchcodec — PyTorch/TorchAudio API Reference](https://docs.pytorch.org/audio/stable/generated/torchaudio.save_with_torchcodec.html) *(promoted by reviewer)*
  This is precisely the kind of “thin but authoritative” page needed to pin down parameter names/defaults; it directly addresses the unfilled API-defaults need better than forum threads.
- **[reference_doc]** [TorchCodec audio_encoding.ipynb (official example notebook)](https://docs.pytorch.org/torchcodec/0.5/_downloads/11ef1d93158a89ea05a303d1d7c2cc02/audio_encoding.ipynb) *(promoted by reviewer)*
  Example notebooks often contain the missing operational details (recommended settings, typical workflows) that API pages omit; it’s an official source and helps teach the practical pipeline.

## Near-Misses (2) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **Residual Vector Quantization - Scott H. Hawley** — [Residual Vector Quantization - Scott H. Hawley](https://drscotthawley.github.io/blog/posts/2023-06-12-RVQ.html)
  _Skipped because:_ Clear and pedagogical, but it is not a primary/official source for EnCodec’s exact objective, losses, and architectural integration.
- **`add_prefix_space=True` option for the BPE tokenizer** — [`add_prefix_space=True` option for the BPE tokenizer](https://discuss.huggingface.co/t/add-prefix-space-true-option-for-the-bpe-tokenizer/1633)
  _Skipped because:_ Useful practical detail, but forum posts are not authoritative API references for defaults/specs compared to official docs or source code.

## Reasoning
**Curator:** Selections prioritize primary/seminal papers that contain the exact RVQ formulation and the full EnCodec pipeline description, plus one strong empirical codec benchmark and one structured text-tokenizer comparison; forum posts and non-authoritative explainers were kept as near-misses rather than core references.
**Reviewer:** The curator’s core paper choices are strong, but the library still needs at least one official TorchAudio/TorchCodec reference/example for exact parameter defaults and a stronger RVQ-formula backup source beyond EnCodec itself.
