# Card: GPT-3 Few-/One-/Zero-shot In-Context Learning (NeurIPS 2020 record)
**Source:** https://proceedings.neurips.cc/paper/2020/hash/6b493230205f780e1bc26945df7481e5-Abstract.html  
**Role:** paper | **Need:** FORMULA_SOURCE  
**Anchor:** NeurIPS 2020 canonical publication record (as captured here) for GPT-3-style in-context learning settings, evaluation defaults, and scaling setup.

## Key Content
- **Model scale & setting (Section 2):**
  - GPT-3 is a **175B-parameter** autoregressive Transformer (same architecture family as GPT-2), evaluated primarily in **few-shot** settings **without gradient updates / fine-tuning**.
- **In-context learning modes (Section 2 “Approach”):**
  - **Fine-Tuning (FT):** update weights using thousands of labeled examples per task.
  - **Few-Shot (FS):** provide **K demonstrations** in the prompt; **no weight updates**.
  - **One-Shot (1S):** FS with **K = 1**.
  - **Zero-Shot (0S):** provide **natural-language task description** (no examples).
  - **Typical K range:** **10–100**, constrained by context window **nctx = 2048 tokens**.
- **Evaluation procedure defaults (Section 2.4):**
  - For each evaluation example, **randomly draw K training examples** as prompt conditioning; delimiter is **1–2 newlines** depending on task.
  - For free-form generation tasks: **beam search** with **beam width = 4** and **length penalty α = 0.6**.
  - Example: on **SuperGLUE**, few-shot uses **32 examples** for all tasks.
- **Training data pipeline (Section 2.2):**
  1) Filter CommonCrawl by similarity to high-quality corpora  
  2) **Fuzzy deduplicate at document level** (within/across datasets)  
  3) Mix in curated corpora (e.g., WebText-like, Books, Wikipedia).

## When to surface
Use when students ask how **few-/one-/zero-shot prompting** is defined/evaluated, what **K** and **context window** constraints are, or what **decoding defaults (beam=4, α=0.6)** were used in the NeurIPS 2020 GPT-3 record.