# Curation Report: Long Context Models
**Topic:** `long-context` | **Date:** 2026-04-09 18:38
**Library:** 7 existing → 21 sources (14 added, 10 downloaded)
**Candidates evaluated:** 46
**Reviewer verdict:** needs_additions

## Added (14)
- **[paper]** [Extending Context Window of Large Language Models via Positional Interpolation](https://arxiv.org/abs/2306.15595)
  This is the primary, citable source for PI with explicit equations and a concrete recipe for extending RoPE-based models’ context windows.
- **[paper]** [YaRN: Efficient Context Window Extension of Large Language Models](https://arxiv.org/abs/2309.00071)
  YaRN is a widely used long-context extension method; the paper provides the exact scaling schedule and training procedure details needed for precise teaching and implementation.
- **[benchmark]** [Lost in the Middle: How Language Models Use Long Contexts](https://cs.stanford.edu/~nfliu/papers/lost-in-the-middle.arxiv2023.pdf)
  Provides concrete, citable empirical evidence and methodology for context utilization failures that a tutor can reference when explaining why longer context windows don’t automatically yield better use of information.
- **[benchmark]** [NoLiMa: Long-Context Evaluation Beyond Literal Matching](https://arxiv.org/html/2502.05167v2)
  Adds a more robust NIAH-style benchmark with tables/ablations that better reflect real long-context understanding rather than string matching.
- **[benchmark]** [LaRA: Benchmarking Retrieval-Augmented Generation and Long-Context LLMs -- No Silver Bullet for LC or RAG Routing](https://arxiv.org/abs/2502.09977)
  Directly fills the need for empirical, criteria-driven comparisons between RAG and true long-context usage, enabling the tutor to discuss tradeoffs with data.
- **[reference_doc]** [Engine Arguments](https://docs.vllm.ai/en/v0.6.1/models/engine_args.html)
  Gives concrete, quotable configuration surface and defaults for deploying long-context models efficiently in a major inference stack.
- **[benchmark]** [Lost in the Middle: How Language Models Use Long Contexts](https://arxiv.org/abs/2307.03172)
  If the library entry is only a placeholder, the actual paper link should be included explicitly because the figures/tables and methodology are the teachable, citable content.
- **[benchmark]** [Lost in the Middle: How Language Models Use Long Contexts (TACL 2024 version)](https://aclanthology.org/2024.tacl-1.9/)
  For a reference library, the archival venue link is often more stable and citable than arXiv alone; it also reduces ambiguity about versions.
- **[code]** [YaRN: Efficient Context Window Extension of Large Language Models (official repo + paper landing page)](https://arxiv.org/html/2309.00071v3)
  The curator added the YaRN paper for formulas, but the repo is exactly the missing reproducible pipeline/example needed for teaching and for students to run.
- **[benchmark]** [Multimodal Needle in a Haystack: Benchmarking Long-Context Capability of Multimodal Large Language Models](https://arxiv.org/abs/2406.11230)
  Even if the lesson is primarily text LLMs, this paper adds hard numbers at extreme context lengths and clarifies how NIAH-style tests are constructed and stress-tested.
- **[benchmark]** [Lost in the Middle: How Language Models Use Long Contexts](https://arxiv.org/abs/2307.03172) *(promoted by reviewer)*
  If the library entry is only a placeholder, the actual paper link should be included explicitly because the figures/tables and methodology are the teachable, citable content.
- **[benchmark]** [Lost in the Middle: How Language Models Use Long Contexts (TACL 2024 version)](https://aclanthology.org/2024.tacl-1.9/) *(promoted by reviewer)*
  For a reference library, the archival venue link is often more stable and citable than arXiv alone; it also reduces ambiguity about versions.
- **[code]** [YaRN: Efficient Context Window Extension of Large Language Models (official repo + paper landing page)](https://arxiv.org/html/2309.00071v3) *(promoted by reviewer)*
  The curator added the YaRN paper for formulas, but the repo is exactly the missing reproducible pipeline/example needed for teaching and for students to run.
- **[benchmark]** [Multimodal Needle in a Haystack: Benchmarking Long-Context Capability of Multimodal Large Language Models](https://arxiv.org/abs/2406.11230) *(promoted by reviewer)*
  Even if the lesson is primarily text LLMs, this paper adds hard numbers at extreme context lengths and clarifies how NIAH-style tests are constructed and stress-tested.

## Near-Misses (4) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **vllm.v1.kv_cache_interface** — [vllm.v1.kv_cache_interface](https://docs.vllm.ai/en/v0.9.0.1/api/vllm/v1/kv_cache_interface.html)
  _Skipped because:_ Useful for KV-cache internals, but less directly actionable for 'defaults and limits' than the engine-args reference.
- **[PDF] arXiv:2410.00161v2 [cs.CL] 7 Oct 2024** — [[PDF] arXiv:2410.00161v2 [cs.CL] 7 Oct 2024](https://arxiv.org/pdf/2410.00161.pdf)
  _Skipped because:_ Appears to include vLLM CLI usage text, but it’s not clearly an official stable documentation page for parameter defaults/limits.
- **Rope Factor issues with meta-llama/Meta-Llama-3.1-70B** — [Rope Factor issues with meta-llama/Meta-Llama-3.1-70B](https://discuss.huggingface.co/t/rope-factor-issues-with-meta-llama-meta-llama-3-1-70b/104638)
  _Skipped because:_ Helpful troubleshooting, but forum posts are not authoritative API references and can be version-specific/confusing.
- **Position Interpolation Improves ALiBi Extrapolation** — [Position Interpolation Improves ALiBi Extrapolation](https://arxiv.org/abs/2310.13017)
  _Skipped because:_ Relevant to interpolation ideas, but it targets ALiBi rather than being the primary RoPE PI formulation the tutor needs.

## Reasoning
**Curator:** Selections prioritize primary-method papers for exact RoPE/PI/YaRN equations, canonical and improved long-context benchmarks for measurable behavior, a dedicated RAG-vs-LC comparison benchmark, and an official inference-stack parameter reference with quotable defaults and flags.
**Reviewer:** The core paper choices are strong, but the library should add the archival Lost-in-the-Middle entry and at least one reproducible YaRN implementation source; the multimodal NIAH paper is also a high-signal benchmark with concrete long-window numbers.
