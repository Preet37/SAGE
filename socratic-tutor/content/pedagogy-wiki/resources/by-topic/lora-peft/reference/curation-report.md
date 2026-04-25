# Curation Report: LoRA and Parameter-Efficient Fine-Tuning
**Topic:** `lora-peft` | **Date:** 2026-04-09 16:21
**Library:** 8 existing → 23 sources (15 added, 10 downloaded)
**Candidates evaluated:** 49
**Reviewer verdict:** needs_additions

## Added (15)
- **[reference_doc]** [bitsandbytes/docs/source/reference/nn/linear4bit.mdx at main · bitsandbytes-foundation/bitsandbytes](https://github.com/bitsandbytes-foundation/bitsandbytes/blob/main/docs/source/reference/nn/linear4bit.mdx)
  This is the most authoritative place to cite bitsandbytes 4-bit module behavior and configuration knobs, which students often ask about when reproducing QLoRA defaults and troubleshooting dtype/precision pitfalls.
- **[benchmark]** [A Guide to Parameter-Efficient Fine-Tuning](https://arxiv.org/html/2303.15647v2)
  Among the candidates, this is the most directly useful structured comparison across PEFT families beyond LoRA, giving the tutor a single citable reference to contrast mechanisms and parameterization choices.
- **[paper]** [S-LoRA: Serving Thousands of Concurrent LoRA Adapters](https://arxiv.org/pdf/2311.03285.pdf)
  This provides concrete, production-oriented mechanisms and measurable serving considerations (memory fragmentation, batching, adapter hot-swapping) that directly answer deployment questions beyond training.
- **[explainer]** [Recipe for Serving Thousands of Concurrent LoRA Adapters](https://lmsys.org/blog/2023-11-15-slora/)
  Pairs with the paper by translating the system into an implementer’s mental model, helping the tutor explain the 'how' of adapter hot-swapping and multi-tenant throughput/latency tradeoffs.
- **[paper]** [arXiv:2312.16886v2 [cs.CV] 30 Dec 2023](https://arxiv.org/pdf/2312.16886.pdf)
  While not a LoRA ablation paper itself, it is a canonical VLM training reference that anchors discussions of module boundaries (vision encoder vs projector vs LLM) needed to interpret LoRA/QLoRA VLM ablations.
- **[paper]** [QLoRA: Efficient Finetuning of Quantized LLMs](https://proceedings.neurips.cc/paper_files/paper/2023/file/1feb87871436031bdc0f2beaa62a049b-Paper-Conference.pdf)
  This is the seminal PEFT+quantization paper and should be in the core library; relying on secondary blogs/docs misses the authoritative algorithm description and the numbers students ask to reproduce.
- **[paper]** [LLaVA Steering: Visual Instruction Tuning with 500× Fewer Parameters](https://aclanthology.org/2025.acl-long.739.pdf)
  It directly targets the currently unfilled VLM LoRA/QLoRA ablation need; even if the snippet looked generic, the paper is likely to contain the concrete module-placement and parameter-efficiency numbers the tutor needs.
- **[paper]** [Serving Heterogeneous LoRA Adapters in Distributed LLM Systems](https://www.arxiv.org/pdf/2511.22880.pdf)
  Since S-LoRA is already included, this is the natural next-step systems reference that broadens deployment coverage to distributed settings and heterogeneous adapters with concrete measurements.
- **[paper]** [Parameter-Efficient Fine-Tuning With Adapters](https://arxiv.org/html/2405.05493)
  The library currently leans LoRA/QLoRA-heavy; this fills concept coverage for adapter-style PEFT with an authoritative, teachable taxonomy even if it’s not purely benchmark-driven.
- **[paper]** [PEFT A2Z: Parameter-Efficient Fine-Tuning Survey for Large Language and Vision Models](https://arxiv.org/html/2504.14117)
  Given the explicit need for cross-method comparison and VLM coverage, a recent survey is a high-leverage index to locate numbers/tables and ensure the tutor doesn’t miss major PEFT variants.
- **[paper]** [QLoRA: Efficient Finetuning of Quantized LLMs](https://proceedings.neurips.cc/paper_files/paper/2023/file/1feb87871436031bdc0f2beaa62a049b-Paper-Conference.pdf) *(promoted by reviewer)*
  This is the seminal PEFT+quantization paper and should be in the core library; relying on secondary blogs/docs misses the authoritative algorithm description and the numbers students ask to reproduce.
- **[paper]** [LLaVA Steering: Visual Instruction Tuning with 500× Fewer Parameters](https://aclanthology.org/2025.acl-long.739.pdf) *(promoted by reviewer)*
  It directly targets the currently unfilled VLM LoRA/QLoRA ablation need; even if the snippet looked generic, the paper is likely to contain the concrete module-placement and parameter-efficiency numbers the tutor needs.
- **[paper]** [Serving Heterogeneous LoRA Adapters in Distributed LLM Systems](https://www.arxiv.org/pdf/2511.22880.pdf) *(promoted by reviewer)*
  Since S-LoRA is already included, this is the natural next-step systems reference that broadens deployment coverage to distributed settings and heterogeneous adapters with concrete measurements.
- **[paper]** [Parameter-Efficient Fine-Tuning With Adapters](https://arxiv.org/html/2405.05493) *(promoted by reviewer)*
  The library currently leans LoRA/QLoRA-heavy; this fills concept coverage for adapter-style PEFT with an authoritative, teachable taxonomy even if it’s not purely benchmark-driven.
- **[paper]** [PEFT A2Z: Parameter-Efficient Fine-Tuning Survey for Large Language and Vision Models](https://arxiv.org/html/2504.14117) *(promoted by reviewer)*
  Given the explicit need for cross-method comparison and VLM coverage, a recent survey is a high-leverage index to locate numbers/tables and ensure the tutor doesn’t miss major PEFT variants.

## Near-Misses (2) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **bitsandbytes/docs/source/fsdp_qlora.md at main · bitsandbyte** — [bitsandbytes/docs/source/fsdp_qlora.md at main · bitsandbytes-foundation/bitsandbytes](https://github.com/bitsandbytes-foundation/bitsandbytes/blob/main/docs/source/fsdp_qlora.md)
  _Skipped because:_ Useful for distributed training recipes, but less definitive than the API reference for exact parameter/default semantics of 4-bit modules.
- **LLaVA Steering: Visual Instruction Tuning with 500x Fewer ..** — [LLaVA Steering: Visual Instruction Tuning with 500x Fewer ... - arXiv](https://arxiv.org/html/2412.12359v2)
  _Skipped because:_ Likely relevant to PEFT on LLaVA, but the candidate snippet does not clearly indicate the depth of LoRA/QLoRA module/rank/data-mixture ablations needed for the specific empirical gap.

## Reasoning
**Curator:** Selections prioritize authoritative specs (bitsandbytes API) and concrete system/benchmark artifacts (S-LoRA paper/blog) while adding one canonical VLM training reference to support module-level reasoning; remaining gaps require targeted benchmark tables and reproducible multimodal training repos not present in the candidates.
**Reviewer:** The curation is strong on LoRA basics and practical tooling, but it should add the seminal QLoRA paper plus at least one VLM-specific PEFT results paper and one broader PEFT taxonomy/survey to cover missing benchmark-backed comparisons and multimodal ablations.
