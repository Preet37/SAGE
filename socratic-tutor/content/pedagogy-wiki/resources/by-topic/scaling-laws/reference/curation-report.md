# Curation Report: Scaling Laws
**Topic:** `scaling-laws` | **Date:** 2026-04-09 16:35
**Library:** 12 existing → 24 sources (12 added, 8 downloaded)
**Candidates evaluated:** 48
**Reviewer verdict:** needs_additions

## Added (12)
- **[reference_doc]** [FullyShardedDataParallel — PyTorch 2.11 documentation](https://docs.pytorch.org/docs/stable/fsdp.html)
  Gives authoritative, citable API-level defaults and meanings for a widely used distributed-training primitive, enabling the tutor to answer precise questions about configuration and behavior.
- **[paper]** [[PDF] An 800GB Dataset of Diverse Text for Language Modeling - The Pile](https://pile.eleuther.ai/paper.pdf)
  Provides an end-to-end, step-by-step data curation reference that the tutor can use to explain how large pretraining corpora are assembled and why mixture diversity matters for scaling.
- **[paper]** [Efficient Memory Management for Large Language Model Serving ...](https://arxiv.org/abs/2309.06180)
  Connects scaling-driven inference constraints (KV-cache growth, batching limits) to concrete system design choices and measured serving outcomes.
- **[benchmark]** [FLASHATTENTION: Fast and](https://proceedings.neurips.cc/paper_files/paper/2022/file/67d57c32e20fd0a7a302cb81d36e40d5-Paper-Conference.pdf)
  Supplies concrete, citable performance numbers and the algorithmic rationale needed to teach why attention becomes an IO bottleneck at scale and how FlashAttention changes the scaling behavior.
- **[paper]** [Scaling Laws for Neural Language Models](https://arxiv.org/pdf/2001.08361.pdf)
  This is the seminal primary source for modern neural scaling laws; the equations and fit procedure are exactly what the library is currently missing, and the existing entry is only a bare arXiv pointer without anchoring the formulas.
- **[paper]** [Training Compute-Optimal Large Language Models](https://arxiv.org/pdf/2203.15556.pdf)
  This is the other cornerstone scaling-law paper (compute-optimal frontier) and provides the derivations/constants needed to teach why “more data” can beat “more parameters” at fixed compute.
- **[reference_doc]** [FullyShardedDataParallel — PyTorch Documentation](https://docs.pytorch.org/docs/2.1/fsdp.html)
  Even if “thin,” this is the canonical API reference page that is easiest to cite for exact defaults/meanings; tutorials are not a substitute for definitive parameter documentation.
- **[reference_doc]** [Getting Started with Fully Sharded Data Parallel (FSDP2)](https://docs.pytorch.org/tutorials/intermediate/FSDP_tutorial.html)
  The library already wants precise distributed-training configuration guidance; this tutorial is the closest official companion to the API docs for explaining how the knobs are used in practice (especially for FSDP2).
- **[paper]** [Scaling Laws for Neural Language Models](https://arxiv.org/pdf/2001.08361.pdf) *(promoted by reviewer)*
  This is the seminal primary source for modern neural scaling laws; the equations and fit procedure are exactly what the library is currently missing, and the existing entry is only a bare arXiv pointer without anchoring the formulas.
- **[paper]** [Training Compute-Optimal Large Language Models](https://arxiv.org/pdf/2203.15556.pdf) *(promoted by reviewer)*
  This is the other cornerstone scaling-law paper (compute-optimal frontier) and provides the derivations/constants needed to teach why “more data” can beat “more parameters” at fixed compute.
- **[reference_doc]** [FullyShardedDataParallel — PyTorch Documentation](https://docs.pytorch.org/docs/2.1/fsdp.html) *(promoted by reviewer)*
  Even if “thin,” this is the canonical API reference page that is easiest to cite for exact defaults/meanings; tutorials are not a substitute for definitive parameter documentation.
- **[reference_doc]** [Getting Started with Fully Sharded Data Parallel (FSDP2)](https://docs.pytorch.org/tutorials/intermediate/FSDP_tutorial.html) *(promoted by reviewer)*
  The library already wants precise distributed-training configuration guidance; this tutorial is the closest official companion to the API docs for explaining how the knobs are used in practice (especially for FSDP2).

## Near-Misses (3) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **Advanced Model Training with Fully Sharded Data Parallel (FS** — [Advanced Model Training with Fully Sharded Data Parallel (FSDP)](https://docs.pytorch.org/tutorials/intermediate/FSDP_advanced_tutorial.html)
  _Skipped because:_ Useful recipes, but less authoritative for exact defaults/parameter semantics than the API reference page, and overlaps heavily with it.
- **FlashAttention-3: Fast and Accurate Attention with ...** — [FlashAttention-3: Fast and Accurate Attention with ...](https://arxiv.org/html/2407.08608v2)
  _Skipped because:_ Excellent newer results, but adding both FA2 and FA3 would crowd the limited budget; FA2 is the more established baseline reference for core FlashAttention benchmarks.
- **Optimization — NVIDIA Triton Inference Server** — [Optimization — NVIDIA Triton Inference Server](https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/user_guide/optimization.html)
  _Skipped because:_ Provides strong serving optimization methodology and example p95/throughput outputs, but is not LLM/KV-cache-specific compared to the vLLM/PagedAttention paper.

## Reasoning
**Curator:** Selections prioritize authoritative sources that directly supply (1) citable defaults/specs (PyTorch FSDP), (2) concrete benchmark tables for scaling-critical kernels (FlashAttention), and (3) end-to-end pipeline/system designs with measured outcomes (The Pile for data curation; vLLM/PagedAttention for serving). Key gaps remain for primary scaling-law formula papers and for KV-cache/GQA/MQA-specific benchmarks and API docs.
**Reviewer:** The curation is strong on systems (FSDP, vLLM, FlashAttention) and data (Pile), but it still needs the two seminal scaling-law papers as primary formula sources and should include the canonical PyTorch FSDP docs (and FSDP2 tutorial) for authoritative defaults and semantics.
