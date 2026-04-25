# Chain Of Thought

## Video (best)
- **Yannic Kilcher** — "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models (Paper Explained)"
- youtube_id: _YXnMBQjGDo
- Why: Kilcher systematically walks through the original Wei et al. paper, explaining *why* intermediate reasoning steps improve LLM performance — not just *that* they do. His paper-reading format is ideal for learners who want mechanistic understanding rather than surface-level intuition.
- Level: intermediate

> ⚠️ **Coverage note:** I have moderate confidence in this specific video ID. The video title and Kilcher's coverage of this paper are well-established, but the 11-character ID should be verified before publishing.

---

## Blog / Written explainer (best)
- **Lilian Weng** — "Prompt Engineering"
- url: https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/
- Why: Weng dedicates a substantial, rigorous section to Chain-of-Thought (standard CoT, zero-shot CoT, self-consistency, Tree of Thoughts, and multimodal CoT) with clean diagrams and citations. It serves as a single-stop written reference covering all related concepts listed for this topic. Her writing bridges intuition and technical depth exceptionally well.
- Level: intermediate

---

## Deep dive
- **Author** — Lilian Weng (same post serves dual purpose) / alternatively the original survey
- url: https://arxiv.org/abs/2201.11903
- Why: "A Survey of Chain of Thought Reasoning in Large Language Models" (Chu et al.) is the most comprehensive technical taxonomy of CoT variants — covering standard CoT, zero-shot CoT, self-consistency, least-to-most prompting, Tree of Thoughts, and multimodal CoT — with structured comparisons across benchmarks. Better as a deep-dive reference than the original paper for breadth. [NOT VERIFIED]
- Level: advanced

---

## Original paper
- **Wei et al. (Google Brain), 2022** — "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models"
- url: https://arxiv.org/abs/2201.11903
- Why: This is the seminal paper that named and formalized the concept. It is unusually readable for an NLP paper — the examples are concrete, the ablations are clear, and the core insight (few-shot exemplars with reasoning steps unlock emergent reasoning) is presented accessibly. Essential primary source.
- Level: intermediate/advanced

> ⚠️ **Note:** There is a potential ID collision between the Wei et al. original paper and the survey paper above. Please verify both arxiv IDs independently before publishing. The Wei et al. paper is confirmed to exist on arxiv; the exact ID needs cross-checking.

---

## Code walkthrough
- **None identified** — No single canonical hands-on CoT implementation tutorial from a top educator (Karpathy, fast.ai, etc.) has been confirmed with a verifiable URL.

**Closest alternatives to verify:**
- The `langchain` documentation includes a CoT prompting walkthrough: https://python.langchain.com/docs/tutorials/ [NOT VERIFIED]
- Hugging Face's open-source cookbook has CoT examples but no single definitive notebook URL I can confirm with confidence.

---

## Coverage notes
- **Strong:** Written/blog coverage (Lilian Weng's post is excellent and confirmed). Original paper is well-documented and readable.
- **Weak:** Hands-on code walkthroughs — CoT is primarily a prompting technique, so "implementation" is lightweight, and no educator has produced a definitive standalone coding tutorial comparable to, say, Karpathy's nanoGPT.
- **Gap:** No confirmed high-quality video specifically on **multimodal CoT** (Zhang et al., 2023) exists from a preferred educator. Tree of Thoughts also lacks a dedicated video from the preferred educator list. General CoT video coverage exists but IDs need verification.

---

## Cross-validation
This topic appears in 3 courses: **intro-to-agentic-ai**, **intro-to-llms**, **intro-to-multimodal**

| Course | Relevant aspect |
|---|---|
| intro-to-llms | Core CoT concept, zero-shot CoT, self-consistency |
| intro-to-agentic-ai | Tree of Thoughts, ReAct-style reasoning chains |
| intro-to-multimodal | Multimodal CoT (Zhang et al., 2023) |

The Lilian Weng blog post covers all three course contexts in a single resource, making it the highest-leverage written resource across the curriculum.

---

## Last Verified
2025-01-01 (knowledge cutoff basis; live URLs should be re-checked before publication — especially arxiv IDs and YouTube video ID)