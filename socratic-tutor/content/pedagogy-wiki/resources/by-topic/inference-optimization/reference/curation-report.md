# Curation Report: Inference Optimization
**Topic:** `inference-optimization` | **Date:** 2026-04-09 18:36
**Library:** 3 existing → 14 sources (11 added, 8 downloaded)
**Candidates evaluated:** 60
**Reviewer verdict:** needs_additions

## Added (11)
- **[reference_doc]** [Model Configuration#](https://docs.nvidia.com/deeplearning/triton-inference-server/archives/triton-inference-server-2540/user-guide/docs/tensorrtllm_backend/docs/model_config.html)
  This is official NVIDIA documentation that the tutor can cite for exact configuration knobs and defaults used in production Triton + TensorRT-LLM deployments.
- **[paper]** [Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads](https://arxiv.org/abs/2401.10774)
  Provides an authoritative, citable description of a speculative decoding variant beyond standard draft/verify, including the concrete algorithmic workflow needed for teaching correctness and implementation details.
- **[paper]** [[PDF] A Theoretical Perspective for Speculative Decoding Algorithm - NIPS](https://proceedings.neurips.cc/paper_files/paper/2024/file/e7349e785900b93d8b4971a3f2c1cefe-Paper-Conference.pdf)
  Adds rigorous theory the tutor can use to explain why acceptance/rejection works and what governs speedups, beyond purely procedural blog-level explanations.
- **[paper]** [SmoothQuant: Accurate and Efficient Post-Training Quantization for Large Language Models](https://arxiv.org/abs/2211.10438)
  Serves as a primary, widely-cited baseline for PTQ comparisons (vs 4-bit methods like GPTQ/AWQ/NF4 and FP8), with concrete methodology and empirical tables.
- **[paper]** [[PDF] Which Quantization Should I Use? A Unified Evaluation of llama.cpp ...](https://arxiv.org/pdf/2601.14277.pdf)
  Helps the tutor teach deployment-format tradeoffs (GGUF-centric toolchains) with both format-level specifics and comparative evaluation context.
- **[paper]** [GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers](https://arxiv.org/abs/2210.17323)
  This is the primary GPTQ source and directly fills the stated need for derivations and update rules; it’s too central to omit when teaching inference quantization tradeoffs and implementation details.
- **[paper]** [AWQ: Activation-aware Weight Quantization for LLM Compression and Acceleration](https://arxiv.org/abs/2306.00978)
  This is the canonical AWQ reference and contains the specific selection/scaling/clipping rules the tutor needs to explain and justify AWQ beyond high-level summaries.
- **[paper]** [SmoothQuant: Accurate and Efficient Post-Training Quantization for Large Language Models](https://arxiv.org/pdf/2211.10438.pdf)
  Even if arXiv is already present, the PDF is often easier to cite precisely (page-stable tables/figures) for a tutor that needs to quote exact numbers and reproduce methodology.
- **[paper]** [GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers](https://arxiv.org/abs/2210.17323) *(promoted by reviewer)*
  This is the primary GPTQ source and directly fills the stated need for derivations and update rules; it’s too central to omit when teaching inference quantization tradeoffs and implementation details.
- **[paper]** [AWQ: Activation-aware Weight Quantization for LLM Compression and Acceleration](https://arxiv.org/abs/2306.00978) *(promoted by reviewer)*
  This is the canonical AWQ reference and contains the specific selection/scaling/clipping rules the tutor needs to explain and justify AWQ beyond high-level summaries.
- **[paper]** [SmoothQuant: Accurate and Efficient Post-Training Quantization for Large Language Models](https://arxiv.org/pdf/2211.10438.pdf) *(promoted by reviewer)*
  Even if arXiv is already present, the PDF is often easier to cite precisely (page-stable tables/figures) for a tutor that needs to quote exact numbers and reproduce methodology.

## Near-Misses (3) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **Which Quantization Should I Use? A Unified Evaluation of lla** — [Which Quantization Should I Use? A Unified Evaluation of llama.cpp ...](https://arxiv.org/html/2601.14277v1)
  _Skipped because:_ HTML version is less stable for citation and precise extraction than the PDF for format specs and tables.
- **SmoothQuant: Accurate and Efficient Post-Training Quantizati** — [SmoothQuant: Accurate and Efficient Post-Training Quantization for ...](https://proceedings.mlr.press/v202/xiao23c.html)
  _Skipped because:_ Redundant with the arXiv entry; arXiv is the canonical evolving version with the latest revisions.
- **Paged Attention Meets FlexAttention: Unlocking Long ...** — [Paged Attention Meets FlexAttention: Unlocking Long ...](https://arxiv.org/html/2506.07311v1)
  _Skipped because:_ Likely useful for paging/attention-kernel design discussion, but it does not clearly promise the requested head-to-head cross-engine benchmark tables (vLLM vs TensorRT-LLM vs Triton) with fixed-model memory/latency breakdowns.

## Reasoning
**Curator:** Selections prioritize authoritative primary papers and official NVIDIA docs that provide citable algorithms, defaults, and theory; thin or non-authoritative benchmark/blog candidates were avoided to keep the library high-signal.
**Reviewer:** The curator’s additions are strong for speculative decoding and SmoothQuant, but the library still misses the two seminal PTQ formula sources (GPTQ and AWQ) explicitly required for teaching quantization objectives and update rules with precision.
