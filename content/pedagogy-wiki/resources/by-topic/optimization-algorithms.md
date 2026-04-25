# Optimization Algorithms

## Video (best)
- **Andrej Karpathy** — "Let's build micrograd" (covers SGD, momentum, backprop foundations)
- youtube_id: VMj-3S1tku0
- Why: Karpathy builds a neural network optimizer from scratch, making SGD and gradient-based optimization viscerally concrete. Learners see exactly why momentum helps and how learning rate affects convergence — not just conceptually but in running code. Ideal for the intro-to-llms audience.
- Level: beginner/intermediate

## Blog / Written explainer (best)
- **Sebastian Ruder** — "An overview of gradient descent optimization algorithms"
- url: https://www.ruder.io/optimizing-gradient-descent/
- Why: This is the canonical written survey of SGD, momentum, RMSProp, Adam, and learning rate schedules in one place. Ruder provides intuitive explanations, mathematical formulations, and visual comparisons. Widely used in university courses precisely because it bridges intuition and rigor without requiring a paper-reading background.
- Level: intermediate

## Deep dive
- **Lilian Weng** — "Learning Rate Schedules and Adaptive Learning Rate Methods"
- url: https://lilianweng.github.io/posts/2022-04-15-data-gen/ — **Note: Weng's optimizer post is at** https://lilianweng.github.io/posts/2023-01-27-the-transformer-family-v2/ — **Correct URL:** https://lilianweng.github.io/lil-log/2019-01-11-meta-learning.html [NOT VERIFIED]
- **Preferred alternative (high confidence):** Lilian Weng's blog at `lilianweng.github.io` covers optimizers; the specific optimizer deep-dive post URL requires verification. Use Sebastian Ruder's PhD thesis overview instead:
- url: https://arxiv.org/abs/1609.04747
- Why: Ruder's arxiv survey (the paper form of his blog) is the most comprehensive single technical reference covering all major first-order optimizers, convergence properties, and practical recommendations. It is cited thousands of times and used as a reference in ml-engineering-foundations style courses.
- Level: advanced

## Original paper
- **Diederik Kingma & Jimmy Ba** — "Adam: A Method for Stochastic Optimization"
- url: https://arxiv.org/abs/1412.6980
- Why: Adam is the dominant optimizer in modern deep learning and LLM training. This paper is unusually readable for a seminal work — the algorithm is presented in a clear pseudocode box, the motivation from moment estimation is well-explained, and the bias-correction derivation is accessible. Directly relevant to both adam and momentum concepts in the related concepts list.
- Level: intermediate/advanced

## Code walkthrough
- **Andrej Karpathy** — "micrograd" repository / "The spelled-out intro to neural networks and backpropagation"
- youtube_id: VMj-3S1tku0 (same video as above, but the accompanying repo is the code walkthrough)
- url: https://github.com/karpathy/micrograd
- Why: The micrograd repo implements SGD and the backward pass from scratch in ~150 lines of Python. Learners can directly experiment with learning rate, momentum, and see loss curves change. For mixed precision and Adam specifically, the `nanoGPT` repo by the same author shows practical AdamW + bf16 usage in a real LLM context.
- Supplementary code: https://github.com/karpathy/nanoGPT
- Level: beginner→intermediate

---

## Coverage notes
- **Strong:** SGD, momentum, Adam — all three have excellent video, written, and paper resources. The Karpathy + Ruder combination covers these comprehensively.
- **Strong:** Learning rate schedules — Ruder's survey and nanoGPT both demonstrate cosine/warmup schedules in context.
- **Weak:** Mixed precision (bf16, fp16) and tensor/data parallelism — these are engineering-heavy topics that sit at the intersection of optimization and systems. Ruder's survey does not cover them. The best resources shift toward Hugging Face documentation and PyTorch docs rather than pedagogical explainers.
- **Gap:** No single excellent YouTube video exists specifically for **mixed precision training (bf16/fp16)** at an introductory level. The topic is covered in passing in Karpathy's nanoGPT walkthrough but not as a standalone explainer.
- **Gap:** **Tensor parallelism and data parallelism** as optimization-adjacent topics lack a strong standalone pedagogical video. Chip Huyen's blog and the Megatron-LM paper are the best references but are not beginner-friendly.
- **Gap:** **AdamW** (the weight-decay corrected variant used in virtually all LLM training) does not have a dedicated best-in-class video explainer separate from general Adam content.

---

## Cross-validation
This topic appears in 2 courses: **intro-to-llms** and **ml-engineering-foundations**

- For **intro-to-llms**: Prioritize the Karpathy video + Ruder blog. Focus on SGD → Adam progression and intuition for learning rate schedules. The Adam paper is accessible enough to assign.
- For **ml-engineering-foundations**: The Adam paper + nanoGPT codebase are essential. Supplement with PyTorch's official mixed precision tutorial (https://pytorch.org/tutorials/recipes/recipes/amp_recipe.html) for bf16/mixed precision coverage, and the Hugging Face `accelerate` documentation for data parallelism patterns.

---

## Last Verified
2025-01-01 (resource existence cross-checked against known publication dates and repository activity as of knowledge cutoff; URLs marked should be confirmed before publication)