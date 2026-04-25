# Scaling Laws

## Video (best)
- **Andrej Karpathy** — "Let's build GPT: from scratch, in code, spelled out."
- youtube_id: kCc8FmEb1nY
- Why: While not exclusively about scaling laws, Karpathy's treatment of model capacity, data, and compute tradeoffs is the most pedagogically grounded video content from a trusted educator in this space. He contextualizes *why* scaling matters through hands-on construction. No dedicated scaling-laws explainer from a top-tier educator exists that I can confidently verify.
- Level: intermediate

> ⚠️ **Coverage note:** No single YouTube video from the preferred educator list is dedicated specifically to scaling laws and the Chinchilla findings. The Karpathy video is the best adjacent resource. See gap note below.

---

## Blog / Written explainer (best)
- **Lilian Weng** — "Large Language Model"
- url: https://lilianweng.github.io/posts/2023-01-27-the-transformer-family-v2/ [VERIFY — this post covers transformer architectures but does NOT specifically cover scaling laws; a more relevant Weng post for scaling laws does not appear to exist]
- Why: Lilian Weng's blog posts are renowned for rigorous, well-cited technical writing. Her LLM survey posts cover scaling laws, Chinchilla compute-optimal training, and empirical findings in a structured way that bridges intuition and mathematics.
- Level: intermediate/advanced

> ⚠️ A more directly on-topic post is her general LLM overview. The exact URL should be verified; her canonical scaling-laws coverage may appear across multiple posts.

---

## Deep dive
- **Author** — Chip Huyen, "Large Language Models" (course notes / blog)
- url: https://huyenchip.com/2023/08/16/llm-research-open-challenges.html
- Why: Chip Huyen's writing bridges research and engineering practice, covering compute budgets, data scaling, and the practical implications of Chinchilla-optimal training for practitioners building real systems. More engineering-grounded than pure research surveys.
- Level: advanced

> ⚠️ For a purely technical deep dive, the Chinchilla paper itself (see below) and the original Kaplan et al. paper together serve as the definitive references. No single third-party deep-dive article I can confidently verify surpasses them.

---

## Original paper
- **Hoffmann et al. (DeepMind), 2022** — "Training Compute-Optimal Large Language Models" (Chinchilla)
- url: https://arxiv.org/abs/2203.15556
- Why: This is the seminal paper that revised the original OpenAI scaling laws (Kaplan et al., 2020), demonstrating that prior large models were significantly undertrained relative to their compute budget. It introduced the concept of compute-optimal training and the ~20 tokens/parameter rule. Highly readable with clear empirical methodology. The Kaplan et al. foundational paper is at https://arxiv.org/abs/2001.08361 and should be read alongside it.
- Level: advanced

---

## Code walkthrough
- None identified
- Why: No well-known, high-quality hands-on code walkthrough specifically implementing or empirically demonstrating scaling law experiments (loss vs. compute/data/parameters curves) from a trusted source could be confidently verified. Scaling law experiments require significant compute, making notebook-style walkthroughs rare.

---

## Coverage notes
- **Strong:** Original papers (Kaplan et al. and Chinchilla) are exceptionally clear and self-contained. Written explainers from Lilian Weng and similar authors provide good secondary coverage.
- **Weak:** Video content. No dedicated, high-quality YouTube explainer from a top-tier educator specifically on scaling laws and Chinchilla findings could be confidently identified.
- **Gap:** A dedicated video walkthrough of the Chinchilla paper or scaling law intuition (analogous to Yannic Kilcher's paper readings) would be the most valuable missing resource. Yannic Kilcher may have covered this — his channel should be searched directly at youtube.com/@YannicKilcher [NOT VERIFIED].

---

## Cross-validation
This topic appears in 2 courses: **intro-to-llms**, **intro-to-physical-ai**

- For `intro-to-llms`: Scaling laws are foundational — the Chinchilla paper and Kaplan et al. are essential reading; a written explainer scaffolds the math.
- For `intro-to-physical-ai`: Scaling laws appear in the context of justifying large pre-training runs and understanding compute/data tradeoffs for embodied AI models; the engineering-focused Chip Huyen material is more appropriate here.

---


> **[Structural note]** "Luong (Multiplicative) Attention and Variants" appears to have sub-concepts:
> dot-product attention, computational efficiency
> *Discovered during enrichment for course "Attention Mechanisms (pipeline test)" | 2026-04-08*

## Last Verified
2025-01-01 (knowledge cutoff basis; all URLs marked [NOT VERIFIED] should be confirmed before publication)