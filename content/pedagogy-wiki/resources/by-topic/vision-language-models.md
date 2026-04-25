# Vision Language Models

## Video (best)
- **Yannic Kilcher** — "Flamingo: a Visual Language Model for Few-Shot Learning (Paper Explained)"
- youtube_id: EhlnhGBZZAo
- Why: Yannic Kilcher's paper walkthroughs are uniquely strong for VLMs because he dissects the architectural decisions (cross-attention fusion, perceiver resampler) with clear diagrams and critical commentary. Flamingo is the most pedagogically central paper for understanding modern VLM design patterns, making this the best entry point for the fusion architecture concepts that underpin BLIP-2, LLaVA, and GPT-4V.
- Level: intermediate/advanced

> ⚠️ **Coverage note on video:** No single video comprehensively covers the full VLM landscape (Flamingo → BLIP-2 → LLaVA → GPT-4V progression). The Kilcher video is the best single anchor, but instructors should supplement.

---

## Blog / Written explainer (best)
- **Lilian Weng** — "Large Multimodal Models"
- url: https://lilianweng.github.io/posts/2022-06-09-vlm/
- Why: Lilian Weng's posts are the gold standard for systematic, well-cited ML surveys. This post traces VLMs from contrastive pretraining (CLIP) through generative fusion architectures, covering visual tokens, patch embeddings, and Q-Former with consistent notation. Her writing bridges intuition and technical rigor better than any other single written resource for this topic.
- Level: intermediate

---

## Deep dive
- **Chip Huyen** — "Multimodal and Large Language Models" (CS329A course notes / blog)
- url: https://huyenchip.com/2023/10/10/multimodal.html
- Why: Chip Huyen's multimodal deep dive is the most comprehensive *practical* technical reference covering the full pipeline: how visual tokens are constructed, how patch embeddings are projected into language model space, the tradeoffs between different fusion architectures (early vs. late fusion, cross-attention vs. prefix), and dynamic resolution strategies. It connects architecture to deployment concerns in a way that pure academic surveys do not.
- Level: advanced

---

## Original paper
- **Alayrac et al. (DeepMind)** — "Flamingo: a Visual Language Model for Few-Shot Learning"
- url: https://arxiv.org/abs/2204.14198
- Why: Flamingo is the clearest seminal paper for the generative VLM paradigm. It introduces the Perceiver Resampler, cross-attention fusion layers interleaved with a frozen LLM, and visual token compression — concepts that directly influenced BLIP-2's Q-Former, LLaVA's projection head, and Gemini's architecture. The paper is unusually well-written with strong ablations, making it the most readable entry point into the design space.
- Level: advanced

---

## Code walkthrough
- **Hugging Face** — "BLIP-2 with Transformers — practical walkthrough"
- url: https://huggingface.co/docs/transformers/model_doc/blip-2
- Why: The HuggingFace BLIP-2 documentation and associated notebooks provide the most hands-on, runnable implementation of the core VLM concepts: Q-Former architecture, visual token extraction via patch embeddings, and conditional text generation. BLIP-2 is architecturally richer than LLaVA for teaching purposes (it makes the vision-language bridge explicit via Q-Former) while remaining accessible. The HF ecosystem means learners can run inference and fine-tuning without custom infrastructure.
- Level: intermediate

---

## Coverage notes
- **Strong:** Flamingo architecture, Q-Former / BLIP-2, fusion architecture concepts, patch embeddings, visual tokens — all well covered across the resources above.
- **Weak:** Dynamic resolution (as used in LLaVA-HD, InternVL, Gemini) has no dedicated high-quality explainer; it appears only as a subsection in survey posts.
- **Weak:** GPT-4V and Gemini are closed models — no authoritative architectural walkthrough exists; only the technical reports (which are incomplete).
- **Gap:** No excellent standalone video exists that surveys the *full* VLM landscape from CLIP → Flamingo → BLIP-2 → LLaVA → GPT-4V in a single coherent narrative. This is a genuine pedagogical gap in the ecosystem as of early 2024.
- **Gap:** No distill.pub-style interactive explainer exists for visual token compression (Perceiver / Q-Former) — a concept that benefits greatly from visualization.

---

## Last Verified
2025-01-01 (resource existence confirmed to knowledge cutoff; URLs marked should be checked before publishing to platform)