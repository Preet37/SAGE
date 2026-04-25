# Prompting

## Video (best)
- **Andrej Karpathy** — "Intro to Large Language Models"
- youtube_id: zjkBMFhNj_g
- Why: Karpathy's talk naturally covers how prompting works in the context of LLM inference, including zero-shot and few-shot patterns, temperature, and how the model responds to context. It's the most pedagogically grounded explanation of *why* prompting works, not just *how* to do it — rooted in the mechanics of next-token prediction. Already curated for this platform.
- Level: beginner/intermediate

> **Coverage note:** This video is a strong general LLM intro but does not deeply cover structured outputs, top-p sampling, or advanced prompting techniques. A more prompting-specific video would strengthen this topic.

---

## Blog / Written explainer (best)
- **Lilian Weng** — "Prompt Engineering"
- url: https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/
- Why: Weng's post is the gold standard written reference for prompting. It systematically covers zero-shot, few-shot, chain-of-thought, self-consistency, and structured output strategies with clear examples and citations. Her writing bridges intuition and rigor, making it suitable for learners who want depth without reading papers directly.
- Level: intermediate

[NOT VERIFIED] — URL structure is consistent with her blog conventions; confirm post slug is exact.

---

## Deep dive
- **DAIR.AI / Elvis Saravia** — "Prompt Engineering Guide"
- url: https://www.promptingguide.ai/
- Why: The most comprehensive freely available reference covering the full prompting landscape: zero-shot, few-shot, chain-of-thought, ReAct, structured outputs, temperature/top-p parameters, and more. Actively maintained, well-organized, and widely used in both academic and industry settings. Serves as a living technical reference rather than a static article.
- Level: intermediate/advanced

---

## Original paper
- **Brown et al. (OpenAI), 2020** — "Language Models are Few-Shot Learners" (GPT-3 paper)
- url: https://arxiv.org/abs/2005.14165
- Why: This is the seminal paper that introduced and formalized the concepts of zero-shot, one-shot, and few-shot prompting as distinct in-context learning paradigms. It is the foundational citation for virtually all prompting research. The results sections are readable without deep ML background, making it accessible to motivated learners.
- Level: intermediate/advanced

---

## Code walkthrough
- **OpenAI Cookbook** — "Techniques to improve reliability" (few-shot, structured outputs, temperature)
- url: https://cookbook.openai.com/articles/techniques_to_improve_reliability
- Why: Hands-on, runnable examples demonstrating few-shot prompting, structured output formatting (JSON mode), and the practical effect of temperature and top-p on outputs. Uses the OpenAI API directly, which is the most common practical context learners will encounter. Bridges conceptual understanding to working code.
- Level: beginner/intermediate

[NOT VERIFIED] — OpenAI Cookbook URLs have shifted; confirm this slug resolves correctly.

---

## Coverage notes
- **Strong:** Zero-shot and few-shot prompting (well covered by GPT-3 paper + Weng blog + Karpathy video); in-context learning conceptual foundations; temperature intuition
- **Weak:** Top-p (nucleus) sampling mechanics — most resources mention it but few explain it deeply at a pedagogical level; structured outputs / JSON mode is underrepresented in video format
- **Gap:** No single excellent YouTube video exists that is *specifically* about prompting techniques end-to-end (zero-shot → few-shot → structured outputs → sampling parameters). Karpathy's video is the best available but is not a dedicated prompting tutorial. A video from a source like Serrano.Academy or a Stanford lecture specifically on prompt engineering would significantly strengthen this topic's video coverage.

---

## Cross-validation
This topic appears in 2 courses: **intro-to-agentic-ai**, **intro-to-llms**
- For `intro-to-llms`: the Karpathy video and GPT-3 paper are the natural anchors; Weng's blog provides the written complement.
- For `intro-to-agentic-ai`: the promptingguide.ai deep dive and OpenAI Cookbook are more actionable for learners building agents who need structured outputs and reliable prompting patterns.

---


> **[Structural note]** "Scaled Dot-Product Attention and Masking" appears to have sub-concepts:
> temperature scaling, numerical stability
> *Discovered during enrichment for course "Attention Mechanisms (pipeline test)" | 2026-04-08*

## Last Verified
2025-04-06