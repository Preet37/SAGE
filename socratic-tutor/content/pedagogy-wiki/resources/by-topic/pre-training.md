# PRE-TRAINING

## Video (best)
- **Andrej Karpathy** — "Intro to Large Language Models"
- youtube_id: zjkBMFhNj_g
- Why: Karpathy provides an exceptionally clear mental model of pre-training as the foundational "compression of the internet" step — covering next-token prediction, autoregressive generation, and the intuition behind perplexity in a way that is accessible yet technically honest. Already validated in the existing curated list.
- Level: beginner/intermediate

---

## Blog / Written explainer (best)
- **Lilian Weng** — "Large Language Model Pre-training"
- url: https://lilianweng.github.io/posts/2023-01-27-the-transformer-family-v2/
- Why: Lilian Weng's blog posts are the gold standard for structured, citation-backed written explainers in ML. Her coverage of training objectives, data curation (including LAION-5B context), and architectural choices bridges theory and practice better than most written resources. The exact post slug should be verified.
- Level: intermediate/advanced

---

## Deep dive
- **Sebastian Raschka** — "Pre-Training LLMs from Scratch" (Magazine/Substack series)
- url: https://magazine.sebastianraschka.com/p/new-llm-pre-training-and-post-training [VERIFY — Raschka's Substack at magazine.sebastianraschka.com is confirmed real; exact slug needs verification]
- Why: Raschka's writing uniquely combines rigorous mathematical grounding with practical implementation notes. His pre-training coverage explicitly addresses data pipelines, tokenization, training stability, and evaluation via perplexity — making it the most complete written deep dive for practitioners building intuition before touching code.
- Level: advanced

---

## Original paper
- **Brown et al. (2020)** — "Language Models are Few-Shot Learners" (GPT-3)
- url: https://arxiv.org/abs/2005.14165
- Why: This is the most widely cited and pedagogically readable paper establishing the modern pre-training paradigm at scale. It clearly articulates the next-token prediction objective, training data composition, and emergent capabilities — making it the canonical reference for what "pre-training" means in the LLM era. For multi-modal pre-training specifically, the CLIP paper (arxiv.org/abs/2103.00020) is the contrastive pre-training counterpart. [NOT VERIFIED]
- Level: intermediate/advanced

---

## Code walkthrough
- **Andrej Karpathy** — "Let's build GPT: from scratch, in code, spelled out"
- youtube_id: kCc8FmEb1nY
- Why: This is arguably the best hands-on pre-training walkthrough in existence. Karpathy implements autoregressive language model pre-training from scratch in ~2 hours, covering the training loop, next-token prediction loss, and perplexity evaluation with minimal abstraction. The associated GitHub repo (github.com/karpathy/ng-video-lecture) provides runnable code.
- Level: intermediate

---

## Coverage notes
- **Strong:** Unimodal LLM pre-training (next-token prediction, autoregressive generation, perplexity, scale) — Karpathy's video and code walkthrough cover this exceptionally well.
- **Weak:** Multi-modal pre-training specifics (interleaved training, natively multi-modal architectures, LAION-5B data curation) — no single curated video covers this with the same depth as the LLM-only case.
- **Gap:** No excellent standalone YouTube video exists specifically for **contrastive pre-training** (CLIP-style) or **interleaved multi-modal pre-training** (Flamingo/Gemini-style) at a beginner-friendly level. The intro-to-multimodal course will need supplementary resources for these sub-topics. Consider Yannic Kilcher's CLIP paper walkthrough (youtube_id: `T9XSU0pKX2E`) [NOT VERIFIED] as a candidate for contrastive pre-training.

---

## Cross-validation
This topic appears in **2 courses**: `intro-to-llms`, `intro-to-multimodal`
- The Karpathy video (`zjkBMFhNj_g`) is already curated 4× for `intro-to-llms/how-language-models-work` — **deduplication recommended** in the platform's content index.
- The `intro-to-multimodal` course will require additional resources specifically addressing LAION-5B, contrastive pre-training, and natively multi-modal objectives not covered by the LLM-focused resources above.

---

## Last Verified
2025-04-06