# Curation Report: Scaled Dot-Product Attention: Math and Implementation
**Topic:** `attention-pipeline-scores-weights-and-context` | **Date:** 2026-04-11 19:20
**Library:** 5 existing → 15 sources (10 added, 6 downloaded)
**Candidates evaluated:** 44
**Reviewer verdict:** needs_additions

## Added (10)
- **[paper]** [Attention Is All You Need - arXiv](https://arxiv.org/html/1706.03762v7)
  This is the primary source that introduced the exact scaled dot-product attention equation and explicitly motivates the 1/sqrt(d_k) factor, making it citable and authoritative for derivations and definitions.
- **[reference_doc]** [torch.nn.functional.scaled_dot_product_attention](https://docs.pytorch.org/docs/stable/generated/torch.nn.functional.scaled_dot_product_attention.html)
  Official PyTorch documentation is the most reliable place to quote exact parameter semantics, defaults, and mask handling rules that students routinely get wrong in implementations.
- **[code]** [(Beta) Implementing High-Performance Transformers with Scaled Dot-Product Attention](https://docs.pytorch.org/tutorials/intermediate/scaled_dot_product_attention_tutorial.html)
  This tutorial provides an authoritative, runnable baseline that demonstrates where masking is applied (pre-softmax) and how shapes/broadcasting work in practice, bridging math to implementation.
- **[benchmark]** [FlashAttention-3: Fast and Accurate Attention with Asynchrony and Low-precision](https://arxiv.org/abs/2407.08608)
  Provides quantitative, modern evidence about stability/accuracy tradeoffs and performance characteristics of attention implementations under low-precision regimes relevant to NaNs/overflow concerns.
- **[reference_doc]** [torch.nn.functional.scaled_dot_product_attention — PyTorch (stable)](https://docs.pytorch.org/docs/stable/generated/torch.nn.functional.scaled_dot_product_attention)
  Even if it feels “thin,” this is the canonical contract students will implement against; it’s the most citable source for mask handling and default scaling behavior and prevents common implementation mistakes.
- **[reference_doc]** [tf.keras.layers.MultiHeadAttention — TensorFlow API Docs](https://www.tensorflow.org/api_docs/python/tf/keras/layers/MultiHeadAttention)
  The library currently anchors implementation semantics almost entirely on PyTorch; adding the official TensorFlow/Keras doc gives a second authoritative reference and helps catch framework-specific masking conventions.
- **[paper]** [FlashMask: Efficient and Rich Mask Extension of FlashAttention](https://arxiv.org/html/2410.01359v1)
  This directly targets the “masking variants” gap: it’s not just performance narrative, but an algorithmic/system design for mask handling in high-performance attention, which is central to teaching correct pre-softmax masking in fused implementations.
- **[reference_doc]** [torch.nn.functional.scaled_dot_product_attention — PyTorch (stable)](https://docs.pytorch.org/docs/stable/generated/torch.nn.functional.scaled_dot_product_attention) *(promoted by reviewer)*
  Even if it feels “thin,” this is the canonical contract students will implement against; it’s the most citable source for mask handling and default scaling behavior and prevents common implementation mistakes.
- **[reference_doc]** [tf.keras.layers.MultiHeadAttention — TensorFlow API Docs](https://www.tensorflow.org/api_docs/python/tf/keras/layers/MultiHeadAttention) *(promoted by reviewer)*
  The library currently anchors implementation semantics almost entirely on PyTorch; adding the official TensorFlow/Keras doc gives a second authoritative reference and helps catch framework-specific masking conventions.
- **[paper]** [FlashMask: Efficient and Rich Mask Extension of FlashAttention](https://arxiv.org/html/2410.01359v1) *(promoted by reviewer)*
  This directly targets the “masking variants” gap: it’s not just performance narrative, but an algorithmic/system design for mask handling in high-performance attention, which is central to teaching correct pre-softmax masking in fused implementations.

## Near-Misses (2) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **torch.nn.functional.scaled_dot_product_attention — PyTorch 2** — [torch.nn.functional.scaled_dot_product_attention — PyTorch 2.9 ...](https://docs.pytorch.org/docs/2.9/generated/torch.nn.functional.scaled_dot_product_attention.html)
  _Skipped because:_ Redundant with the stable PyTorch API reference; keeping one canonical doc link avoids duplication.
- **Out of the box acceleration and memory savings of decoder mo** — [Out of the box acceleration and memory savings of decoder models ...](https://pytorch.org/blog/out-of-the-box-acceleration/)
  _Skipped because:_ Useful performance narrative, but less precise than the API doc and less methodologically detailed than the FlashAttention papers for citable benchmarks.

## Reasoning
**Curator:** Selections prioritize primary/official sources for exact equations and API semantics, plus authoritative implementation and benchmark references that connect masking/scaling to real low-precision behavior. Lower-authority explainers and redundant links were excluded to keep the library small and citable.
**Reviewer:** The core picks are strong for defining scaled dot-product attention and modern fused implementations, but the library should add at least one canonical API doc link (PyTorch stable) plus a masking-in-fused-attention paper (FlashMask) to better cover mask semantics and masking-variant tradeoffs.
