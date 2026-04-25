# Multi Head Attention

## Video (best)
- **3Blue1Brown** — "Attention in transformers, visually explained | Chapter 6, Deep Learning"
- youtube_id: eMlx5fFNoYc
- Why: Exceptional visual intuition for how attention heads carve up representation space, with geometric analogies that make the multi-head mechanism genuinely comprehensible rather than just mechanically described. Part of the "Neural Networks" series which builds context cleanly.
- Level: beginner/intermediate

## Blog / Written explainer (best)
- **Jay Alammar** — "The Illustrated Transformer"
- url: https://jalammar.github.io/illustrated-transformer/
- Why: The definitive visual walkthrough of multi-head attention. Alammar's step-by-step diagrams showing Q/K/V projections, the splitting into heads, parallel attention computation, and concatenation/projection are unmatched in clarity. Widely considered the canonical introductory reference for this exact mechanism.
- Level: beginner/intermediate

## Deep dive
- **Lilian Weng** — "Attention? Attention!"
- url: https://lilianweng.github.io/posts/2018-06-24-attention/
- Why: Comprehensive technical treatment covering the full attention family tree — from Bahdanau through self-attention to multi-head — with precise mathematical notation, architectural variants, and historical context. Weng's posts are research-grade while remaining pedagogically structured.
- Level: intermediate/advanced

## Original paper
- **Vaswani et al.** — "Attention Is All You Need"
- url: https://arxiv.org/abs/1706.03762
- Why: The seminal paper introducing multi-head attention as a named, formalized mechanism. Section 3.2 is unusually readable for a foundational ML paper, with clear equations and explicit motivation for why multiple heads are used (attending to information from different representation subspaces).
- Level: intermediate/advanced

## Code walkthrough
- **Andrej Karpathy** — "Let's build GPT: from scratch, in code, spelled out"
- youtube_id: kCc8FmEb1nY
- Why: Karpathy builds multi-head attention from absolute scratch in PyTorch, narrating every design decision. The progression from single-head to multi-head is explicit and the code is minimal enough to see the structure clearly. Paired with the nanoGPT repo for reference implementation.
- Level: intermediate

## Coverage notes
- **Strong:** Introductory visual explanations (Alammar, 3B1B) are exceptional. The original paper is highly readable. From-scratch code implementation (Karpathy) is best-in-class.
- **Weak:** Cross-attention and gated cross-attention (relevant to `intro-to-multimodal`) are underserved by the resources above, which focus on self-attention in decoder/encoder-only contexts.
- **Gap:** No single excellent resource specifically targets **gated cross-attention** (as used in Flamingo-style multimodal architectures). For `intro-to-multimodal`, instructors should supplement with the Flamingo paper directly (https://arxiv.org/abs/2204.14198) and Weng's multimodal post. No dedicated YouTube explainer for gated cross-attention exists at the quality tier specified.

## Cross-validation
This topic appears in 2 courses: **intro-to-llms**, **intro-to-multimodal**
- For `intro-to-llms`: All resources above apply directly. Karpathy's code walkthrough is especially well-aligned.
- For `intro-to-multimodal`: The self-attention resources provide necessary foundation, but cross-attention and gated cross-attention require supplementary material not covered by the primary resources listed here. Flag this gap for curriculum designers.


> **[Structural note]** "Visualizing and Interpreting Attention Weights" appears to have sub-concepts:
> attention heatmaps, alignment visualization, soft vs hard attention
> *Discovered during enrichment for course "Attention Mechanisms (pipeline test)" | 2026-04-07*

## Last Verified
2026-04-06