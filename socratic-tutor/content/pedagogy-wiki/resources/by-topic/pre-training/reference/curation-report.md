# Curation Report: Pre-Training
**Topic:** `pre-training` | **Date:** 2026-04-09 16:29
**Library:** 8 existing → 18 sources (10 added, 7 downloaded)
**Candidates evaluated:** 34
**Reviewer verdict:** needs_additions

## Added (10)
- **[paper]** [[2001.08361] Scaling Laws for Neural Language Models](https://arxiv.org/abs/2001.08361)
  Seminal primary source for concrete scaling-law numbers and the loss/compute/data tradeoffs a tutor can cite when students ask “how much data/compute do I need for X loss?”
- **[paper]** [Training Compute-Optimal Large Language Models](https://arxiv.org/abs/2203.15556)
  Provides the most actionable, modern compute/data/model-size tradeoff results with concrete experimental sweeps and recommendations used widely in practice.
- **[paper]** [LAION-5B: An open large-scale dataset for training next generation language-vision models](https://arxiv.org/abs/2210.08402)
  Authoritative reference for large-scale image-text data curation and documentation, directly addressing how LAION-5B was built and filtered.
- **[reference_doc]** [Optimization — transformers 3.0.2 documentation - Hugging Face](https://www.huggingface.co/transformers/v3.0.2/main_classes/optimizer_schedules.html)
  Gives citable, versioned defaults and optimizer/scheduler configuration details commonly referenced in pre-training stacks using HF Transformers.
- **[paper]** [Language Models Are Better Than Humans at Next-token Prediction](https://arxiv.org/html/2212.11281v2)
  Even if the snippet looks basic, it directly fills the library’s missing primary-source-style explanation of perplexity vs cross-entropy and log-base dependence, which students routinely ask about.
- **[reference_doc]** [How can I use evaluate's perplexity metric on a model that's already loaded?](https://discuss.huggingface.co/t/how-can-i-use-evaluates-perplexity-metric-on-a-model-thats-already-loaded/48564)
  While not “official docs,” it is a high-signal, implementation-specific reference that addresses an unfilled need: how perplexity is actually computed/used in common HF workflows and where defaults/behavior surprise users.
- **[reference_doc]** [Using Cosine LR scheduler via TrainingArguments in Trainer](https://discuss.huggingface.co/t/using-cosine-lr-scheduler-via-trainingarguments-in-trainer/14783/8)
  Thin forum answers are still valuable as a reference track because they pin down the exact parameter names and wiring in Trainer—precisely the kind of API detail students need when reproducing pre-training setups.
- **[paper]** [Language Models Are Better Than Humans at Next-token Prediction](https://arxiv.org/html/2212.11281v2) *(promoted by reviewer)*
  Even if the snippet looks basic, it directly fills the library’s missing primary-source-style explanation of perplexity vs cross-entropy and log-base dependence, which students routinely ask about.
- **[reference_doc]** [How can I use evaluate's perplexity metric on a model that's already loaded?](https://discuss.huggingface.co/t/how-can-i-use-evaluates-perplexity-metric-on-a-model-thats-already-loaded/48564) *(promoted by reviewer)*
  While not “official docs,” it is a high-signal, implementation-specific reference that addresses an unfilled need: how perplexity is actually computed/used in common HF workflows and where defaults/behavior surprise users.
- **[reference_doc]** [Using Cosine LR scheduler via TrainingArguments in Trainer](https://discuss.huggingface.co/t/using-cosine-lr-scheduler-via-trainingarguments-in-trainer/14783/8) *(promoted by reviewer)*
  Thin forum answers are still valuable as a reference track because they pin down the exact parameter names and wiring in Trainer—precisely the kind of API detail students need when reproducing pre-training setups.

## Near-Misses (2) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **LAION-5B: An open large-scale dataset for training next gene** — [LAION-5B: An open large-scale dataset for training next generation ...proceedings.neurips.cc › paper_files › paper › file](https://proceedings.neurips.cc/paper_files/paper/2022/file/a1859debfb3b59d094f3504d5ebb6c25-Paper-Datasets_and_Benchmarks.pdf)
  _Skipped because:_ Essentially duplicates the arXiv paper; kept only one canonical entry to conserve library slots.
- **Using perplexity as metric during training - Hugging Face Fo** — [Using perplexity as metric during training - Hugging Face Forums](https://discuss.huggingface.co/t/using-perplexity-as-metric-during-training/42354)
  _Skipped because:_ Useful code snippet (exp(eval_loss)) but not authoritative API documentation for tokenizer-dependent PPL computation or evaluate defaults.

## Reasoning
**Curator:** Selections prioritize primary, citable sources that directly supply either (a) concrete scaling/compute tradeoff numbers or (b) authoritative, documented pipelines/defaults. Several candidate items were forum/blog-level or off-target for the missing formula and multimodal-architecture needs, so those gaps are left explicitly unfilled with targeted search hints.
**Reviewer:** The curator’s core paper choices are strong, but the library still lacks citable perplexity/cross-entropy formula coverage and practical HF perplexity/scheduler API references that students commonly need during pre-training reproduction.
