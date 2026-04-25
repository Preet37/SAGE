# Curation Report: Luong (Multiplicative) Attention and Variants
**Topic:** `self-attention` | **Date:** 2026-04-09 15:52
**Library:** 29 existing → 39 sources (10 added, 7 downloaded)
**Candidates evaluated:** 35
**Reviewer verdict:** needs_additions

## Added (10)
- **[paper]** [Effective Approaches to Attention-based Neural Machine Translation](https://aclanthology.org/D15-1166/)
  This is the canonical, citable source for the multiplicative attention variants and their precise mathematical definitions, including local-m/local-p mechanics.
- **[benchmark]** [Effective Approaches to Attention-based Neural Machine Translation (PDF)](https://aclanthology.org/anthology-files/pdf/D/D15/D15-1166.pdf)
  Provides primary empirical evidence (BLEU and ablations) directly tied to Luong attention design choices, suitable for quoting and for guiding student comparisons.
- **[reference_doc]** [tfa.seq2seq.LuongAttention - Addons](https://www.tensorflow.org/addons/api_docs/python/tfa/seq2seq/LuongAttention)
  Official documentation gives authoritative, implementation-level details (defaults, shapes, masking) that students often ask for when reproducing Luong attention in TensorFlow.
- **[code]** [The model](https://www.tensorflow.org/text/tutorials/nmt_with_attention)
  A reproducible, step-by-step tutorial implementation helps the tutor demonstrate how Luong attention is wired in practice and how tensors move through the model.
- **[paper]** [Effective Approaches to Attention-based Neural Machine Translation (Luong, Pham, Manning, 2015) — full PDF](https://arxiv.org/pdf/1508.04025.pdf)
  The library already has the abstract and an ACL/Stanford PDF link, but explicitly including the arXiv PDF ensures the tutor can reliably cite the canonical equations and procedural details without link-rot or paywall issues.
- **[reference_doc]** [tf.contrib.seq2seq.LuongMonotonicAttention — TensorFlow v1.15 API Docs](https://www.tensorflow.org/versions/r1.15/api_docs/python/tf/contrib/seq2seq/LuongMonotonicAttention)
  Even if the lesson centers on core Luong attention, students frequently encounter TF1 codebases; this “thin” doc is high-signal for exact signatures/defaults and complements TFA docs.
- **[explainer]** [TensorFlow Addons Tutorial: Seq2Seq NMT (Luong-style attention usage)](https://www.tensorflow.org/addons/tutorials/networks_seq2seq_nmt)
  The curator wants a working example; this is an official, runnable reference that demonstrates the full integration path (not just the scoring function) and answers common “how do I plug it in?” questions.
- **[paper]** [Effective Approaches to Attention-based Neural Machine Translation (Luong, Pham, Manning, 2015) — full PDF](https://arxiv.org/pdf/1508.04025.pdf) *(promoted by reviewer)*
  The library already has the abstract and an ACL/Stanford PDF link, but explicitly including the arXiv PDF ensures the tutor can reliably cite the canonical equations and procedural details without link-rot or paywall issues.
- **[reference_doc]** [tf.contrib.seq2seq.LuongMonotonicAttention — TensorFlow v1.15 API Docs](https://www.tensorflow.org/versions/r1.15/api_docs/python/tf/contrib/seq2seq/LuongMonotonicAttention) *(promoted by reviewer)*
  Even if the lesson centers on core Luong attention, students frequently encounter TF1 codebases; this “thin” doc is high-signal for exact signatures/defaults and complements TFA docs.
- **[explainer]** [TensorFlow Addons Tutorial: Seq2Seq NMT (Luong-style attention usage)](https://www.tensorflow.org/addons/tutorials/networks_seq2seq_nmt) *(promoted by reviewer)*
  The curator wants a working example; this is an official, runnable reference that demonstrates the full integration path (not just the scoring function) and answers common “how do I plug it in?” questions.

## Near-Misses (3) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **tfa.seq2seq.LuongMonotonicAttention | TensorFlow Addons** — [tfa.seq2seq.LuongMonotonicAttention | TensorFlow Addons](https://www.tensorflow.org/addons/api_docs/python/tfa/seq2seq/LuongMonotonicAttention)
  _Skipped because:_ Useful for monotonic variants, but the core LuongAttention doc already covers the main multiplicative attention API surface needed for this lesson.
- **tfa.seq2seq.AttentionWrapper | TensorFlow Addons** — [tfa.seq2seq.AttentionWrapper | TensorFlow Addons](https://www.tensorflow.org/addons/api_docs/python/tfa/seq2seq/AttentionWrapper)
  _Skipped because:_ Important for integration details, but it is broader than Luong-style scoring and would dilute the small, high-signal library given the 6-source cap.
- **Math behind √dₖ Scaling Factor in Attention - Outcome School** — [Math behind √dₖ Scaling Factor in Attention - Outcome School](https://outcomeschool.com/blog/scaling-dot-product-attention)
  _Skipped because:_ Explains scaling intuition but is not an authoritative benchmark/cost comparison source with explicit FLOPs/memory formulas across additive vs multiplicative scoring.

## Reasoning
**Curator:** Selections prioritize primary/official sources: the ACL paper/PDF for exact equations and citable ablations, TensorFlow Addons for authoritative API defaults, and an end-to-end TensorFlow tutorial for a reproducible Luong-attention implementation. The remaining gap is a truly authoritative, formula-level cost/stability comparison across scoring functions.
**Reviewer:** Core Luong (2015) coverage is strong, but adding the arXiv PDF explicitly plus official TF1/TFA integration docs would materially improve formula reliability and implementation-level teachability.

---

# Curation Report: Scaled Dot-Product Attention: Math and Implementation
**Topic:** `self-attention` | **Date:** 2026-04-11 17:58
**Library:** 37 existing → 47 sources (10 added, 5 downloaded)
**Candidates evaluated:** 43
**Reviewer verdict:** needs_additions

## Added (10)
- **[reference_doc]** [torch.nn.functional.scaled_dot_product_attention](https://docs.pytorch.org/docs/stable/generated/torch.nn.functional.scaled_dot_product_attention.html)
  This is the official, citable PyTorch SDPA primitive the tutor can quote for defaults, argument meanings, and the reference-equivalent pseudocode used to define correctness.
- **[code]** [scaled_dot_product_attention_tu... - PyTorch documentation](https://docs.pytorch.org/tutorials/_sources/intermediate/scaled_dot_product_attention_tutorial.rst.txt)
  Provides an authoritative, runnable implementation narrative that can be adapted into a from-scratch reference implementation and used to teach the exact tensor shapes and masking conventions.
- **[benchmark]** [[PDF] FlashAttention: Fast and Memory-Efficient Exact Attention with IO ...](https://arxiv.org/pdf/2205.14135.pdf)
  Adds citable empirical tradeoffs (throughput/memory vs sequence length) and a clear explanation of why attention is memory-bound and how exact attention can be computed with fewer HBM reads/writes.
- **[benchmark]** [FlashAttention-3: Fast and Accurate Attention with Asynchrony and ...](https://arxiv.org/html/2407.08608v1)
  Extends the empirical picture to modern GPUs and precision regimes, giving the tutor up-to-date performance numbers and design rationale for newer attention kernels.
- **[reference_doc]** [torch.nn.attention.sdpa_kernel — PyTorch documentation](https://docs.pytorch.org/docs/stable/generated/torch.nn.attention.sdpa_kernel.html)
  The library already cites the SDPA API signature, but not the official mechanism that controls which implementation is used—critical for teaching reproducibility, performance debugging, and why results/precision can differ across machines.
- **[reference_doc]** [torch.nn.attention.SDPBackend — PyTorch documentation](https://docs.pytorch.org/docs/stable/generated/torch.nn.attention.SDPBackend.html)
  Even if “thin,” this is exactly the kind of citable reference a tutor needs when explaining backend choices and mapping conceptual attention math to concrete kernel implementations.
- **[paper]** [Why Low-Precision Transformer Training Fails: An Analysis ...](https://arxiv.org/html/2510.04212v1)
  This directly targets the unfilled numerical-stability need in the attention context (not generic log-sum-exp), and provides an authoritative, attention-focused treatment that complements FlashAttention’s stability discussion.
- **[reference_doc]** [torch.nn.attention.sdpa_kernel — PyTorch documentation](https://docs.pytorch.org/docs/stable/generated/torch.nn.attention.sdpa_kernel.html) *(promoted by reviewer)*
  The library already cites the SDPA API signature, but not the official mechanism that controls which implementation is used—critical for teaching reproducibility, performance debugging, and why results/precision can differ across machines.
- **[reference_doc]** [torch.nn.attention.SDPBackend — PyTorch documentation](https://docs.pytorch.org/docs/stable/generated/torch.nn.attention.SDPBackend.html) *(promoted by reviewer)*
  Even if “thin,” this is exactly the kind of citable reference a tutor needs when explaining backend choices and mapping conceptual attention math to concrete kernel implementations.
- **[paper]** [Why Low-Precision Transformer Training Fails: An Analysis ...](https://arxiv.org/html/2510.04212v1) *(promoted by reviewer)*
  This directly targets the unfilled numerical-stability need in the attention context (not generic log-sum-exp), and provides an authoritative, attention-focused treatment that complements FlashAttention’s stability discussion.

## Near-Misses (4) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **torch.nn.functional.scaled_dot_product_attention — PyTorch 2** — [torch.nn.functional.scaled_dot_product_attention — PyTorch 2.9 ...](https://docs.pytorch.org/docs/2.9/generated/torch.nn.functional.scaled_dot_product_attention.html)
  _Skipped because:_ Redundant with the stable docs pick; would only be useful if the tutor specifically needs version-pinned 2.9 wording.
- **Function at::scaled_dot_product_attention** — [Function at::scaled_dot_product_attention](https://docs.pytorch.org/cppdocs/api/function_namespaceat_1a2975cf6a82b6b322f4dc62df301b3737.html)
  _Skipped because:_ Good for C++ users, but the Python reference doc plus tutorial better cover the tutor’s likely teaching and student usage scenarios.
- **FlashAttention-2: Faster Attention with Better Parallelism a** — [FlashAttention-2: Faster Attention with Better Parallelism and Work ...](https://crfm.stanford.edu/2023/07/17/flash2.html)
  _Skipped because:_ Useful practitioner summary, but the library benefits more from primary benchmark papers (FlashAttention and FlashAttention-3) for citable tables and methodological detail.
- **ACCURATE COMPUTATION OF THE LOG-SUM-EXP AND** — [ACCURATE COMPUTATION OF THE LOG-SUM-EXP AND](http://arxiv.org/pdf/1909.03469.pdf)
  _Skipped because:_ Strong on log-sum-exp numerics in general, but not tied directly to attention masking conventions (-inf), causal masks, or fp16/bf16 attention-specific failure modes.

## Reasoning
**Curator:** Selections prioritize official PyTorch SDPA documentation/tutorial for precise API defaults and a canonical implementation pattern, and primary FlashAttention papers for concrete, citable performance/memory tradeoffs. The remaining gaps (sqrt(d_k) derivation and attention-specific softmax stability walkthrough) are not adequately met by the provided candidates.
**Reviewer:** The curation is strong on core attention papers and FlashAttention benchmarks, but it should add PyTorch’s official SDPA backend-selection docs and at least one attention-specific low-precision/numerical-stability analysis paper to fully cover implementation semantics and stability pitfalls.

---

# Curation Report: Scaled Dot-Product Attention: Math and Implementation
**Topic:** `self-attention` | **Date:** 2026-04-11 19:28
**Library:** 39 existing → 50 sources (11 added, 5 downloaded)
**Candidates evaluated:** 43
**Reviewer verdict:** needs_additions

## Added (11)
- **[reference_doc]** [torch.nn.functional.scaled_dot_product_attention](https://docs.pytorch.org/docs/stable/generated/torch.nn.functional.scaled_dot_product_attention.html)
  This is the authoritative PyTorch SDPA API reference the tutor can quote for parameter defaults, mask handling, and how PyTorch routes to optimized implementations.
- **[reference_doc]** [Methods](https://www.tensorflow.org/api_docs/python/tf/keras/layers/MultiHeadAttention)
  Provides the official TensorFlow/Keras MultiHeadAttention surface and defaults needed for cross-framework API precision when students ask how masking/dropout are specified in TF.
- **[reference_doc]** [flax.linen.MultiHeadDotProductAttention](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.MultiHeadDotProductAttention.html)
  Gives an official JAX/Flax reference point so the tutor can compare how masking and dropout are expressed differently from PyTorch/TF, even when exact mask broadcasting rules differ.
- **[reference_doc]** [MultiheadAttention — PyTorch 2.11 documentation](https://docs.pytorch.org/docs/stable/generated/torch.ao.nn.quantizable.modules.activation.MultiheadAttention.html)
  Helps the tutor explain how the higher-level PyTorch MHA module relates to SDPA and what shape conventions (e.g., batch_first) imply for mask dimensions.
- **[benchmark]** [FLASHATTENTION: Fast and](https://proceedings.neurips.cc/paper_files/paper/2022/file/67d57c32e20fd0a7a302cb81d36e40d5-Paper-Conference.pdf)
  Adds citable empirical performance numbers and an authoritative algorithmic explanation for why fused/tiling attention improves throughput and memory, which students often ask about.
- **[code]** [(Beta) Implementing High-Performance Transformers with Scaled Dot Product Attention (PyTorch tutorial)](https://docs.pytorch.org/tutorials/intermediate/scaled_dot_product_attention_tutorial.html)
  It was rejected as “tutorial,” but it directly fills the missing runnable-reference gap and is maintainer-authored, making it a reliable canonical implementation guide beyond the thin API page.
- **[benchmark]** [FlashAttention: Fast Transformer Training with Long Sequences (HazyResearch blog)](https://hazyresearch.stanford.edu/blog/2023-01-12-flashattention-long-sequences)
  Even if the FlashAttention paper is already included, this post often contains clearer, directly quotable benchmark figures and practitioner-facing measurement context that helps answer “how much faster/when does it matter?”
- **[reference_doc]** [tf.keras.layers.MultiHeadAttention (TensorFlow v2.13.1 API docs)](https://www.tensorflow.org/versions/r2.13.1/api_docs/python/tf/keras/layers/MultiHeadAttention)
  The library notes “Methods” generically; pinning an explicit versioned TF API page prevents ambiguity and supports precise cross-framework comparisons when students’ environments differ.
- **[code]** [(Beta) Implementing High-Performance Transformers with Scaled Dot Product Attention (PyTorch tutorial)](https://docs.pytorch.org/tutorials/intermediate/scaled_dot_product_attention_tutorial.html) *(promoted by reviewer)*
  It was rejected as “tutorial,” but it directly fills the missing runnable-reference gap and is maintainer-authored, making it a reliable canonical implementation guide beyond the thin API page.
- **[benchmark]** [FlashAttention: Fast Transformer Training with Long Sequences (HazyResearch blog)](https://hazyresearch.stanford.edu/blog/2023-01-12-flashattention-long-sequences) *(promoted by reviewer)*
  Even if the FlashAttention paper is already included, this post often contains clearer, directly quotable benchmark figures and practitioner-facing measurement context that helps answer “how much faster/when does it matter?”
- **[reference_doc]** [tf.keras.layers.MultiHeadAttention (TensorFlow v2.13.1 API docs)](https://www.tensorflow.org/versions/r2.13.1/api_docs/python/tf/keras/layers/MultiHeadAttention) *(promoted by reviewer)*
  The library notes “Methods” generically; pinning an explicit versioned TF API page prevents ambiguity and supports precise cross-framework comparisons when students’ environments differ.

## Near-Misses (3) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **scaled_dot_product_attention_tu... - PyTorch documentation** — [scaled_dot_product_attention_tu... - PyTorch documentation](https://docs.pytorch.org/tutorials/_sources/intermediate/scaled_dot_product_attention_tutorial.rst.txt)
  _Skipped because:_ Likely useful as a worked tutorial, but the API reference page already anchors the precise defaults/semantics more directly for quoting.
- **[PDF] FlashAttention: Fast and Memory-Efficient Exact Attent** — [[PDF] FlashAttention: Fast and Memory-Efficient Exact Attention with IO ...](https://arxiv.org/pdf/2205.14135.pdf)
  _Skipped because:_ Redundant with the NeurIPS proceedings PDF of the same work; kept only one canonical version to stay within the size limit.
- **flax/distil_whisper/layers.py · supawichwac/training at 7e6c** — [flax/distil_whisper/layers.py · supawichwac/training at 7e6cffe14cf1488329c739736b89f97e6612efe5](https://huggingface.co/supawichwac/training/blob/7e6cffe14cf1488329c739736b89f97e6612efe5/flax/distil_whisper/layers.py)
  _Skipped because:_ Runnable code, but not a maintainer-canonical reference and may not clearly isolate mask-to-logits-before-softmax patterns in a minimal, didactic way.

## Reasoning
**Curator:** Selections prioritize official framework docs for quotable API defaults and semantics, plus a canonical benchmark paper for empirical performance. Several needs remain unfilled because the candidate set lacks a truly authoritative cross-framework mask-shape comparison and maintainer-grade runnable masking/stability examples.
**Reviewer:** The core papers and PyTorch API reference are solid, but adding the official PyTorch SDPA tutorial (runnable masking/backends), a benchmark-rich FlashAttention systems post, and a version-pinned TF MultiHeadAttention doc would materially improve implementation fidelity and empirical grounding.
