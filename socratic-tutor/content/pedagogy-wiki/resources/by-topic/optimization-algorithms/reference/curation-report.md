# Curation Report: Optimization Algorithms
**Topic:** `optimization-algorithms` | **Date:** 2026-04-09 16:26
**Library:** 6 existing → 19 sources (13 added, 9 downloaded)
**Candidates evaluated:** 50
**Reviewer verdict:** needs_additions

## Added (13)
- **[reference_doc]** [DistributedDataParallel — PyTorch 2.11 documentation](https://docs.pytorch.org/docs/stable/generated/torch.nn.parallel.DistributedDataParallel.html)
  This is the authoritative spec for DDP behavior and defaults the tutor can quote when students ask about reducer buckets, sync points, and how DDP interacts with unused params and mixed precision.
- **[paper]** [[1710.03740] Mixed Precision Training - arXiv](https://arxiv.org/abs/1710.03740)
  Provides the canonical mixed-precision methodology (master weights + loss scaling) plus concrete experimental results and failure-mode mitigation (overflow/underflow) that students commonly ask about.
- **[benchmark]** [A Study of BFLOAT16 for Deep Learning Training](https://arxiv.org/abs/1905.12322)
  Adds BF16-specific empirical evidence and practical guidance (range/overflow behavior) that complements FP16-focused mixed-precision sources.
- **[paper]** [Megatron-LM: Training Multi-Billion Parameter Language Models ...](https://arxiv.org/abs/1909.08053)
  Gives a concrete, teachable blueprint for tensor parallelism and the exact collectives involved, enabling the tutor to explain why/where communication happens and how parallelism strategies compose.
- **[benchmark]** [Model Details](https://pytorch.org/blog/maximizing-training/)
  Provides real-world distributed training outcomes with concrete throughput and utilization metrics plus practical lessons, which are essential for teaching deployment tradeoffs beyond toy examples.
- **[reference_doc]** [Automatic Mixed Precision package - torch.amp (PyTorch docs)](https://docs.pytorch.org/docs/stable/amp.html)
  The library currently has mixed-precision papers but lacks the authoritative API contract students will ask about (what GradScaler actually does, default hyperparameters, and when it is enabled/disabled).
- **[reference_doc]** [Automatic Mixed Precision examples — PyTorch documentation](https://docs.pytorch.org/docs/stable/notes/amp_examples.html)
  Even if 'thin', these examples are the quickest way to resolve common student failure modes (wrong step/update order, accumulation with scaling) with an official reference.
- **[benchmark]** [A Study of BFLOAT16 for Deep Learning Training](https://arxiv.org/pdf/1905.12322.pdf)
  This is the concrete, numbers-first BF16 evidence the tutor can cite; it directly supports the BF16 claims students question (accuracy parity, stability, when scaling is unnecessary).
- **[benchmark]** [Supercharging Training using float8 and FSDP2 - PyTorch Blog](https://pytorch.org/blog/training-using-float8-fsdp2/)
  The curator already referenced 'Model Details' for FSDP scaling; this is the primary source with the quoted numbers and adds practical FSDP2/precision pipeline details useful for teaching deployment tradeoffs.
- **[reference_doc]** [Automatic Mixed Precision package - torch.amp (PyTorch docs)](https://docs.pytorch.org/docs/stable/amp.html) *(promoted by reviewer)*
  The library currently has mixed-precision papers but lacks the authoritative API contract students will ask about (what GradScaler actually does, default hyperparameters, and when it is enabled/disabled).
- **[reference_doc]** [Automatic Mixed Precision examples — PyTorch documentation](https://docs.pytorch.org/docs/stable/notes/amp_examples.html) *(promoted by reviewer)*
  Even if 'thin', these examples are the quickest way to resolve common student failure modes (wrong step/update order, accumulation with scaling) with an official reference.
- **[benchmark]** [A Study of BFLOAT16 for Deep Learning Training](https://arxiv.org/pdf/1905.12322.pdf) *(promoted by reviewer)*
  This is the concrete, numbers-first BF16 evidence the tutor can cite; it directly supports the BF16 claims students question (accuracy parity, stability, when scaling is unnecessary).
- **[benchmark]** [Supercharging Training using float8 and FSDP2 - PyTorch Blog](https://pytorch.org/blog/training-using-float8-fsdp2/) *(promoted by reviewer)*
  The curator already referenced 'Model Details' for FSDP scaling; this is the primary source with the quoted numbers and adds practical FSDP2/precision pipeline details useful for teaching deployment tradeoffs.

## Near-Misses (2) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **ZeRO++: Extremely Efficient Collective Communication for ...** — [ZeRO++: Extremely Efficient Collective Communication for ...](https://arxiv.org/pdf/2306.10209.pdf)
  _Skipped because:_ Excellent for advanced ZeRO communication-volume reductions, but less directly aligned with the requested step-by-step baseline explanation of DP vs tensor/model parallel communication patterns.
- **Highly Scalable Deep Learning Training System with Mixed-Pre** — [Highly Scalable Deep Learning Training System with Mixed-Precision: Training ImageNet in Four Minutes](https://arxiv.org/pdf/1807.11205.pdf)
  _Skipped because:_ Strong system/throughput case study, but overlaps with the mixed-precision paper pick while being less directly focused on BF16/overflow-rate and loss-scaling behavior details requested.

## Reasoning
**Curator:** Selections prioritize authoritative specs (PyTorch DDP docs) and seminal/empirical sources (mixed precision + BF16 studies) plus one concrete parallelism explainer (Megatron-LM) and one real-world scaling case (PyTorch FSDP blog). Remaining gaps require original optimization-method derivations and official AMP/FSDP API references not present in the candidate list.
**Reviewer:** The additions are strong for DDP/mixed precision/parallelism, but the library still needs official AMP/GradScaler references (and the BF16 benchmark PDF) to cover missing API semantics and citeable empirical tables.
