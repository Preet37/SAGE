# Contrastive Learning

## Video (best)
- **Yannic Kilcher** — "CLIP: Connecting Text and Images (Paper Explained)"
- youtube_id: OZF1t_Hieq8
- Why: Kilcher walks through the original CLIP paper with exceptional clarity, explaining the dual-encoder architecture, InfoNCE loss, and zero-shot classification in a single cohesive narrative. His paper-explanation style is ideal for learners who want to understand *why* design choices were made, not just *what* they are.
- Level: intermediate

## Blog / Written explainer (best)
- **Lilian Weng** — "Contrastive Representation Learning"
- url: https://lilianweng.github.io/posts/2021-05-31-contrastive/
- Why: Weng's post is the canonical written reference for contrastive learning — it covers the theoretical motivation, loss functions (InfoNCE, NT-Xent, triplet loss), and major methods (SimCLR, MoCo, CLIP) with clean math and diagrams. It bridges self-supervised vision methods and multimodal contrastive learning in one place, making it ideal for the full conceptual arc of this topic.
- Level: intermediate/advanced

## Deep dive
- **Author** — OpenAI CLIP model card + Hugging Face CLIP docs combined with Sebastian Raschka's "Understanding Contrastive Learning"
- url: https://sebastianraschka.com/blog/2022/understanding-contrastive-learning.html [NOT VERIFIED]
- Why: Raschka's treatment is unusually rigorous about the mathematical underpinnings of InfoNCE loss and why contrastive objectives work as representation learners. He connects theory to implementation more carefully than most blog posts, making it the best resource for learners who want to go from intuition to derivation to code.
- Level: advanced

## Original paper
- **Radford et al. (OpenAI)** — "Learning Transferable Visual Models From Natural Language Supervision" (CLIP)
- url: https://arxiv.org/abs/2103.00020
- Why: This is the seminal paper that crystallized contrastive learning for multimodal settings and introduced the dual-encoder + InfoNCE framework at scale. It is unusually readable for an OpenAI paper — the motivation, method, and zero-shot evaluation protocol are explained with enough detail to be self-contained. SigLIP and OpenCLIP are direct descendants, so understanding this paper unlocks the whole family.
- Level: intermediate/advanced

## Code walkthrough
- **Hugging Face / @merveenoyan** — CLIP fine-tuning notebook on Hugging Face
- url: https://huggingface.co/blog/fine_tune_clip_fashion [NOT VERIFIED]
- Why: This notebook demonstrates the full contrastive training loop end-to-end — projection layers, InfoNCE loss computation, dual-encoder forward pass, and evaluation — using real data and the `transformers` library. It is more pedagogically complete than most standalone scripts because it explains each component inline, and it maps directly to the OpenCLIP/SigLIP ecosystem learners will encounter in practice.
- Level: intermediate

## Coverage notes
- **Strong:** The CLIP paper itself is exceptionally clear; Lilian Weng's blog post is one of the best technical explainers in the entire ML blogosphere for this topic; Hugging Face ecosystem has strong practical coverage.
- **Weak:** SigLIP-specific content (sigmoid loss vs. softmax InfoNCE) has very limited dedicated tutorial coverage. Projection layer design choices are rarely explained in depth outside of paper appendices.
- **Gap:** No excellent standalone beginner-friendly video exists that covers *contrastive learning as a general framework* (not just CLIP specifically) with visual intuition — something in the 3Blue1Brown or StatQuest style. Kilcher's video is the best available but assumes paper-reading familiarity. OpenCLIP and SigLIP also lack dedicated video explainers as of early 2025.

## Last Verified
2025-01-01 (resource existence confidence: Lilian Weng post — high; CLIP arxiv — high; Kilcher video ID — moderate [NOT VERIFIED]; Raschka post URL — moderate [NOT VERIFIED]; HF fine-tuning blog — moderate [NOT VERIFIED])