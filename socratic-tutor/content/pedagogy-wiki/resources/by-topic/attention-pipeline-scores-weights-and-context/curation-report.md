# Curation Report: Scaled Dot-Product Attention: Math and Implementation
**Topic:** `attention-pipeline-scores-weights-and-context` | **Date:** 2026-04-11 19:19
**Library:** 0 existing → 7 sources (7 added, 5 downloaded)
**Candidates evaluated:** 23
**Reviewer verdict:** needs_additions

## Added (7)
- **[tutorial]** [Tutorial 6: Transformers and Multi-Head Attention¶](https://uvadlc-notebooks.readthedocs.io/en/latest/tutorial_notebooks/tutorial6/Transformers_and_MHAttention.html)
  High-quality, pedagogical notebook that derives scaled dot-product attention and multi-head attention with explicit tensor shapes, making QK^T logits and (batch, heads, query_len, key_len) dimensions concrete in code.
   — covers: Define attention logits explicitly as QK^T (pre-softmax) and explain their tensor shapes (batch, heads, query_len, key_len)
- **[tutorial]** [Streaming Softmax: A Trick Powering FlashAttention - Seth Weidman](https://www.sethweidman.com/blog/streaming_softmax.html)
  Clear explanation of numerically stable softmax (max-subtraction, log-sum-exp style reasoning) and why stability matters in attention implementations, connecting directly to practical kernel behavior.
   — covers: Numerically stable softmax in attention (subtract max, handling -inf for masks, dtype considerations)
- **[tutorial]** [A Gentle Introduction to Attention Masking in Transformer Models](https://machinelearningmastery.com/a-gentle-introduction-to-attention-masking-in-transformer-models/)
  Practical walkthrough of padding vs causal masking and how masks are applied to attention scores before softmax, with implementation-oriented discussion that helps bridge theory to PyTorch usage.
   — covers: Padding masks: creation from padding tokens/attention_mask, and applying to logits before softmax, Causal masks: triangular masks for autoregressive decoding and combining with padding masks, Broadcasting rules for masks across batch and heads; practical PyTorch/NumPy implementations of masked softmax and attention
- **[paper]** [StableMask: Refining Causal Masking in Decoder Transformers](https://ar5iv.labs.arxiv.org/html/2402.04779)
  Even if specialized, it is a directly relevant, research-grade treatment of causal masking details and edge cases (where many implementations go wrong), making it a strong complement to tutorials for a math+implementation lesson.
   — covers: Causal masks: triangular masks for autoregressive decoding and combining with padding masks
- **[tutorial]** [Dive into Deep Learning — The Transformer](https://d2l.ai/chapter_attention-mechanisms-and-transformers/transformer.html)
  The near-miss rejection is a bit strict: d2l’s Transformer chapter is a high-authority, stable reference that clearly defines scaled dot-product attention and includes masking in code, making it valuable as a canonical baseline alongside more implementation-kernel-focused posts.
   — covers: Padding masks: creation from padding tokens/attention_mask, and applying to logits before softmax, Causal masks: triangular masks for autoregressive decoding and combining with padding masks, Broadcasting rules for masks across batch and heads; practical PyTorch/NumPy implementations of masked softmax and attention
- **[paper]** [StableMask: Refining Causal Masking in Decoder Transformers](https://ar5iv.labs.arxiv.org/html/2402.04779) *(promoted by reviewer)*
  Even if specialized, it is a directly relevant, research-grade treatment of causal masking details and edge cases (where many implementations go wrong), making it a strong complement to tutorials for a math+implementation lesson.
   — fills: Causal masks: triangular masks for autoregressive decoding and combining with padding masks
- **[tutorial]** [Dive into Deep Learning — The Transformer](https://d2l.ai/chapter_attention-mechanisms-and-transformers/transformer.html) *(promoted by reviewer)*
  The near-miss rejection is a bit strict: d2l’s Transformer chapter is a high-authority, stable reference that clearly defines scaled dot-product attention and includes masking in code, making it valuable as a canonical baseline alongside more implementation-kernel-focused posts.
   — fills: Padding masks: creation from padding tokens/attention_mask, and applying to logits before softmax, Causal masks: triangular masks for autoregressive decoding and combining with padding masks, Broadcasting rules for masks across batch and heads; practical PyTorch/NumPy implementations of masked softmax and attention

## Near-Misses (3) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **11.3. Attention Scoring Functions - Dive into Deep Learning** — [11.3. Attention Scoring Functions - Dive into Deep Learning](https://d2l.ai/chapter_attention-mechanisms-and-transformers/attention-scoring-functions.html)
  _Skipped because:_ Authoritative, but this section is broader on scoring functions and doesn’t focus enough on the concrete masking/broadcasting and stable-softmax implementation details needed for the listed gaps.
- **Tracing Attention Computation Through Feature Interactions** — [Tracing Attention Computation Through Feature Interactions](https://transformer-circuits.pub/2025/attention-qk/index.html)
  _Skipped because:_ Excellent interpretability-oriented deep dive, but it’s less targeted to the core math+implementation mechanics (masking, stable softmax, broadcasting) that the lesson gaps emphasize.
- **FLASH-D: FlashAttention with Hidden Softmax Division - arXiv** — [FLASH-D: FlashAttention with Hidden Softmax Division - arXiv](https://arxiv.org/html/2505.14201v1)
  _Skipped because:_ Potentially valuable for kernel-level softmax stability, but it’s specialized and less suitable as a primary teaching resource for implementing standard scaled dot-product attention and masking.

## Uncovered Gaps (3) — No Good Candidates Found
_Consider manually sourcing these, or run enrichment again with different search terms._

- Padding masks: creation from padding tokens/attention_mask, and applying to logits before softmax
- Causal masks: triangular masks for autoregressive decoding and combining with padding masks
- Broadcasting rules for masks across batch and heads; practical PyTorch/NumPy implementations of masked softmax and attention

## Reasoning
**Curator:** Selections prioritize one strong shapes-and-QK^T derivation (UVADLC), one numerically-stable softmax deep dive (Weidman), and one practical masking tutorial to cover padding/causal/broadcasting. Some masking sub-gaps remain only partially addressed by the candidates and would benefit from a more authoritative PyTorch/HF reference or a high-quality implementation note.
**Reviewer:** The current picks are solid for logits/softmax stability and practical masking, but adding an authoritative baseline (d2l) and one focused causal-masking paper would strengthen coverage and credibility.
