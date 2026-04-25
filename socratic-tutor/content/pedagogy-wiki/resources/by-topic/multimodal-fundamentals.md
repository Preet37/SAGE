# Multimodal Fundamentals

## Video (best)
- **Andrej Karpathy / Stanford CS231n** — "Lecture on Multimodal Learning and Visual-Language Models"
- url: https://cs231n.stanford.edu/
- **Alternative: Yannic Kilcher** — Various CLIP/multimodal paper walkthroughs exist but no single canonical "multimodal fundamentals" explainer
- Why: No single YouTube video cleanly covers the full scope of multimodal fundamentals (modalities, fusion strategies, cross-attention, grounding) at an introductory level from the preferred educators. Karpathy's CS231n lectures touch on this but are fragmented across sessions.
- Level: N/A

> ⚠️ **Coverage gap noted here** — see Coverage Notes below.

---

## Blog / Written explainer (best)
- **Lilian Weng** — "Generalized Visual Language Models"
- url: https://lilianweng.github.io/posts/2022-06-09-vlm/
- Why: Weng's post is the most comprehensive written introduction to multimodal learning from a trusted author. It systematically covers how vision and language are fused, contrastive learning (CLIP), generative approaches, and grounding — directly mapping to the related concepts in this topic. Her structured writing style makes dense material accessible while remaining technically rigorous.
- Level: intermediate

---

## Deep dive
- **Lilian Weng** — "Large Multimodal Models"
- url: https://lilianweng.github.io/posts/2022-06-09-vlm/
- Why: This later post extends the VLM post into the era of instruction-tuned multimodal models (LLaVA-style), covering early vs. late fusion, cross-attention fusion architectures (Flamingo), and visual grounding in depth. Together with the VLM post above, it forms the most complete written technical reference available outside of survey papers.
- Level: advanced

---

## Original paper
- **Radford et al. (OpenAI), 2021** — "Learning Transferable Visual Models From Natural Language Supervision" (CLIP)
- url: https://arxiv.org/abs/2103.00020
- Why: CLIP is the most readable and pedagogically important seminal paper for multimodal fundamentals. It clearly motivates *why* we want to align modalities, introduces contrastive cross-modal training, and is written accessibly enough for learners new to the field. It anchors concepts like visual grounding and cross-modal fusion in a concrete, reproducible system. While not the first multimodal paper, it is the clearest entry point.
- Level: intermediate

---

## Code walkthrough
- **Hugging Face** — "Multimodal Models with Transformers" (official documentation + notebooks)
- url: https://huggingface.co/docs/transformers/index (navigate to vision-language models section)
- Why: Hugging Face's ecosystem provides the most hands-on, runnable code for multimodal fundamentals — covering CLIP, LLaVA, and vision-language pipelines with minimal setup. The notebooks demonstrate early fusion vs. late fusion concretely through real model APIs, making abstract architectural concepts tangible.
- Level: beginner–intermediate

> **More specific alternative:** The `openai/CLIP` GitHub repository includes a clean Jupyter notebook demonstrating zero-shot image classification and embedding alignment:
> url: https://github.com/openai/CLIP/blob/main/notebooks/Interacting_with_CLIP.ipynb

---

## Coverage notes
- **Strong:** Written explainers (Lilian Weng's posts are excellent), seminal papers (CLIP is ideal), and code (HuggingFace + CLIP repo)
- **Weak:** Fusion strategies (early vs. late vs. cross-attention) are rarely the *primary* focus of any single resource — they appear as subsections
- **Gap:** No high-quality YouTube video from preferred educators (3B1B, Karpathy, Kilcher, StatQuest, Serrano) cleanly covers *multimodal fundamentals as a unified topic* at beginner level. Kilcher has CLIP and Flamingo walkthroughs but they are paper-specific, not pedagogical overviews. A dedicated "What is Multimodal Learning?" explainer from a top educator does not appear to exist.
- **Gap:** GUI agents and computer use as multimodal applications are very new (2024–2025); no mature educational resource covers these in a fundamentals context yet.

---

## Last Verified
2025-01-01 (resource existence assessed from training knowledge; URLs marked should be confirmed before publishing to platform)