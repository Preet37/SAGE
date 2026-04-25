# Self Attention

## Video (best)
- **3Blue1Brown** — "Attention in transformers, visually explained | 3Blue1Brown"
- youtube_id: eMlx5fFNoYc
- Why: Exceptional visual intuition for queries, keys, and values as geometric operations in embedding space. Builds understanding of scaled dot-product attention from first principles without assuming prior knowledge. The animation of attention weights as "which tokens attend to which" is the clearest visual treatment available for beginners.
- Level: beginner/intermediate

## Blog / Written explainer (best)
- **Jay Alammar** — "The Illustrated Transformer"
- url: https://jalammar.github.io/illustrated-transformer/
- Why: The definitive written explainer for self-attention. Step-by-step diagrams show exactly how Q, K, V matrices are computed, how dot products become attention weights via softmax, and how multi-head attention works. Widely used in university courses precisely because it makes the matrix math visually concrete. Covers causal masking in the decoder context.
- Level: beginner/intermediate

## Deep dive
- **Lilian Weng** — "Attention? Attention!"
- url: https://lilianweng.github.io/posts/2018-06-24-attention/
- Why: Comprehensive technical survey tracing attention from its seq2seq origins through self-attention and Transformers. Covers the full mathematical formulation of scaled dot-product attention, multi-head variants, and positional encoding interactions. Ideal for readers who want to understand *why* each design choice was made, not just how to implement it.
- Level: intermediate/advanced

## Original paper
- **Vaswani et al.** — "Attention Is All You Need"
- url: https://arxiv.org/abs/1706.03762
- Why: The seminal paper introducing the Transformer architecture and scaled dot-product self-attention. Section 3.2 ("Attention") is unusually readable for a research paper and directly defines the canonical Q/K/V formulation still used today. The scaling factor (1/√d_k) motivation is explained clearly in the paper itself.
- Level: intermediate/advanced

## Code walkthrough
- **Andrej Karpathy** — "Let's build GPT: from scratch, in code, spelled out"
- youtube_id: kCc8FmEb1nY
- Why: Karpathy implements self-attention (including causal masking) from scratch in ~100 lines of PyTorch, narrating every line. The progression from raw dot-products → scaled attention → masked attention → multi-head is the best available code-first treatment. Viewers see exactly why the triangular mask is applied and how attention weights are computed in practice. Paired with the nanoGPT repo for hands-on experimentation.
- Level: intermediate

## Coverage notes
- **Strong:** Visual/conceptual explanation of Q/K/V (3B1B video + Jay Alammar blog are both excellent and complementary). Mathematical formulation (Weng deep dive + original paper). From-scratch implementation (Karpathy).
- **Weak:** Efficient attention variants (Flash Attention, sparse attention) are not well covered by any of the above. Causal masking gets coverage in Karpathy but is underemphasized in the beginner resources.
- **Gap:** No single resource cleanly bridges the gap between the visual intuition (3B1B) and production-level implementation details (e.g., KV caching, memory layout). Advanced practitioners looking for hardware-aware attention implementations should consult the Flash Attention paper (arxiv.org/abs/2205.14135) separately.


> **[Structural note]** "Queries, Keys, and Values: The QKV Framework" appears to have sub-concepts:
> scaled dot-product attention
> *Discovered during enrichment for course "Attention Mechanisms (pipeline test)" | 2026-04-07*


> **[Structural note]** "Visualizing and Interpreting Attention Weights" appears to have sub-concepts:
> attention heatmaps, alignment visualization, soft alignment, hard alignment, interpretability limits, weight extraction
> *Discovered during enrichment for course "Attention Mechanisms (pipeline test)" | 2026-04-07*


> **[Structural note]** "Bahdanau (Additive) Attention: Deep Dive" appears to have sub-concepts:
> additive scoring function, alignment model, softmax normalization, attention weights
> *Discovered during enrichment for course "Attention Mechanisms (pipeline test)" | 2026-04-07*


> **[Structural note]** "Luong (Multiplicative) Attention and Scoring Variants" appears to have sub-concepts:
> dot-product scoring, computational complexity
> *Discovered during enrichment for course "Attention Mechanisms (pipeline test)" | 2026-04-07*


> **[Structural note]** "Queries, Keys, and Values: A Unified Framework" appears to have sub-concepts:
> qkv abstraction, soft retrieval, cross-attention vs self-attention
> *Discovered during enrichment for course "Attention Mechanisms (pipeline test)" | 2026-04-07*


> **[Structural note]** "Visualizing and Interpreting Attention Weights" appears to have sub-concepts:
> attention heatmaps, alignment visualization
> *Discovered during enrichment for course "Attention Mechanisms (pipeline test)" | 2026-04-07*


> **[Structural note]** "Multi-Head Attention: Representation Subspaces and Implementation" appears to have sub-concepts:
> multi-head attention, parallel attention
> *Discovered during enrichment for course "Attention Mechanisms (pipeline test)" | 2026-04-08*


> **[Structural note]** "Scaled Dot-Product Attention: Math, Masking, and Stability" appears to have sub-concepts:
> scaled dot-product attention, softmax stability
> *Discovered during enrichment for course "Attention Mechanisms (pipeline test)" | 2026-04-08*


> **[Structural note]** "Luong (Multiplicative) Attention and Variants" appears to have sub-concepts:
> dot-product attention, multiplicative attention, global attention, local attention, computational complexity
> *Discovered during enrichment for course "Attention Mechanisms (pipeline test)" | 2026-04-08*


> **[Structural note]** "Luong (Multiplicative) Attention and Variants" appears to have sub-concepts:
> dot-product attention, global attention, local attention, computational efficiency
> *Discovered during enrichment for course "Attention Mechanisms (pipeline test)" | 2026-04-09*


> **[Structural note]** "Scaled Dot-Product Attention: Math and Implementation" appears to have sub-concepts:
> softmax, attention matrix, numerical stability
> *Discovered during enrichment for course "This course builds a focused, end-to-end understanding of attention in neural ne" | 2026-04-11*


> **[Structural note]** "Scaled Dot-Product Attention: Math and Implementation" appears to have sub-concepts:
> attention logits, padding mask, causal mask
> *Discovered during enrichment for course "This course builds a focused, end-to-end understanding of attention in neural ne" | 2026-04-11*

## Last Verified
2025-01-01 (youtube_id eMlx5fFNoYc and kCc8FmEb1nY confirmed; jalammar.github.io and lilianweng.github.io URLs confirmed stable; arxiv 1706.03762 confirmed)