# Curation Report: Mixture of Experts
**Topic:** `mixture-of-experts` | **Date:** 2026-04-09 18:35
**Library:** 4 existing → 18 sources (14 added, 10 downloaded)
**Candidates evaluated:** 48
**Reviewer verdict:** needs_additions

## Added (14)
- **[paper]** [[PDF] GShard: Scaling Giant Models with Conditional Computation ... - arXiv](https://arxiv.org/pdf/2006.16668.pdf)
  Primary-source, implementation-oriented MoE math and training details that later Switch-style routers build on; gives citable equations and the intended training-time routing behavior.
- **[paper]** [The Sparsely-Gated Mixture-of-Experts Layer - arXiv](https://arxiv.org/abs/1701.06538)
  Seminal formulation that defines the canonical router + auxiliary-loss toolkit; useful for quoting exact loss terms and explaining why imbalance happens and how the losses address it.
- **[paper]** [DeepSeek-V2: A Strong, Economical, and Efficient Mixture-of ... - arXiv](https://arxiv.org/html/2405.04434v5)
  Modern open MoE LLM paper with concrete design tradeoffs and measured results; directly addresses routing and balancing choices beyond older Switch/GShard-era studies.
- **[reference_doc]** [Mixture of Experts (MoE)](https://deepspeed.readthedocs.io/en/latest/moe.html)
  Provides citable parameter definitions and default values in a major training stack, enabling precise answers about practical MoE knobs and their intended behavior.
- **[code]** [Source code for deepspeed.moe.layer](https://deepspeed.readthedocs.io/en/stable/_modules/deepspeed/moe/layer.html)
  Even without a full training script, the source is a runnable ground-truth for how a widely used MoE layer actually performs routing, capacity enforcement, and expert-parallel communication.
- **[benchmark]** [Achieving High Mixtral 8x7B Performance with NVIDIA H100 Tensor ...](https://developer.nvidia.com/blog/achieving-high-mixtral-8x7b-performance-with-nvidia-h100-tensor-core-gpus-and-tensorrt-llm/)
  Adds real deployment metrics and architecture constraints from an authoritative vendor stack, helping the tutor explain inference-time routing overheads, batching constraints, and performance tuning.
- **[benchmark]** [MoE-Inference-Bench: Performance Evaluation of Mixture of Expert Large Language and Vision Models](https://arxiv.org/html/2508.17467v1)
  It directly targets the library’s biggest gap (inference tradeoff numbers) and is more systematic than a single vendor case study; even if not “production,” it provides concrete, citable performance data.
- **[benchmark]** [MoE-Inference-Bench: Performance Evaluation of Mixture of Expert Large Language and Vision Models (PDF)](https://www.arxiv.org/pdf/2508.17467.pdf)
  The PDF is the most stable citation target for specific numbers and tables; keeping it alongside the HTML improves long-term reference reliability.
- **[code]** [DeepSpeedExamples: cifar10_deepspeed.py (includes MoE layer specification and runnable training scaffold)](https://github.com/deepspeedai/DeepSpeedExamples/blob/master/training/cifar/cifar10_deepspeed.py)
  The curator noted the docs lack an end-to-end recipe; this fills that gap with an executable example that concretely wires MoE into a training loop and config.
- **[reference_doc]** [DeepSpeed 文档：专家混合(MoE) / Mixture of Experts (MoE)](https://docs.deepspeed.org.cn/en/latest/moe.html)
  Thin API docs are exactly what the reference track needs; this mirror can be useful when the primary site is blocked/slow and still provides authoritative parameter specs.
- **[benchmark]** [MoE-Inference-Bench: Performance Evaluation of Mixture of Expert Large Language and Vision Models](https://arxiv.org/html/2508.17467v1) *(promoted by reviewer)*
  It directly targets the library’s biggest gap (inference tradeoff numbers) and is more systematic than a single vendor case study; even if not “production,” it provides concrete, citable performance data.
- **[benchmark]** [MoE-Inference-Bench: Performance Evaluation of Mixture of Expert Large Language and Vision Models (PDF)](https://www.arxiv.org/pdf/2508.17467.pdf) *(promoted by reviewer)*
  The PDF is the most stable citation target for specific numbers and tables; keeping it alongside the HTML improves long-term reference reliability.
- **[code]** [DeepSpeedExamples: cifar10_deepspeed.py (includes MoE layer specification and runnable training scaffold)](https://github.com/deepspeedai/DeepSpeedExamples/blob/master/training/cifar/cifar10_deepspeed.py) *(promoted by reviewer)*
  The curator noted the docs lack an end-to-end recipe; this fills that gap with an executable example that concretely wires MoE into a training loop and config.
- **[reference_doc]** [DeepSpeed 文档：专家混合(MoE) / Mixture of Experts (MoE)](https://docs.deepspeed.org.cn/en/latest/moe.html) *(promoted by reviewer)*
  Thin API docs are exactly what the reference track needs; this mirror can be useful when the primary site is blocked/slow and still provides authoritative parameter specs.

## Near-Misses (3) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **DeepSpeed/deepspeed/moe/layer.py at master · deepspeedai/Dee** — [DeepSpeed/deepspeed/moe/layer.py at master · deepspeedai/DeepSpeed](https://github.com/microsoft/DeepSpeed/blob/master/deepspeed/moe/layer.py)
  _Skipped because:_ Redundant with the rendered module source link; kept the docs + rendered source as the more stable, readable pair.
- **[PDF] MoE-Inference-Bench: Performance Evaluation of Mixture** — [[PDF] MoE-Inference-Bench: Performance Evaluation of Mixture of Expert ...](https://arxiv.org/pdf/2508.17467.pdf)
  _Skipped because:_ Looks promising for inference benchmarking, but it is not a production case study and may be less directly actionable for serving architecture than the NVIDIA TensorRT-LLM writeup.
- **Mixture of Experts (MoE)** — [Mixture of Experts (MoE)](https://deepspeed.readthedocs.io/en/latest/moe.html)
  _Skipped because:_ Does not by itself provide an end-to-end training recipe with scripts/configs; it is primarily API reference.

## Reasoning
**Curator:** Selections prioritize primary-source formulations (Shazeer MoE, GShard) for exact equations and losses, plus authoritative stack documentation (DeepSpeed) and a vendor deployment benchmark (NVIDIA TensorRT-LLM) to cover practical defaults and real inference metrics. Remaining gaps are mainly broader stack coverage (Megatron/vLLM) and truly end-to-end training cookbooks with scripts/configs.
**Reviewer:** Core seminal/formula sources are well covered, but the library still needs at least one dedicated inference benchmark with tables and at least one runnable end-to-end training example; the MoE-Inference-Bench and DeepSpeedExamples script are the highest-value additions from the candidates.
