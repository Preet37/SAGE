# Curation Report: Positional Information: Sinusoidal and Learned Embeddings
**Topic:** `transformer-architecture` | **Date:** 2026-04-08 01:26
**Library:** 4 existing → 10 sources (6 added, 0 downloaded, 4 failed)
**Candidates evaluated:** 28
**Reviewer verdict:** needs_additions

## Added (6)
- **[paper]** [[PDF] Journal of Machine Learning Why Self-Attention is Natural for ...](https://web.stanford.edu/~lexing/selfattention.pdf)
  Adds a formal symmetry/equivariance perspective that makes the permutation-invariance of self-attention (without positional information) precise—something the current library mostly treats intuitively.
   — covers: Why self-attention is permutation-invariant without positional information; formal intuition/examples
- **[tutorial]** [Position Encoding Comparison: Sinusoidal, Learned, RoPE & ALiBi ...](https://mbrenndoerfer.com/writing/position-encoding-comparison-transformers)
  Provides a practical, side-by-side comparison of absolute (sinusoidal/learned) and modern relative schemes (RoPE/ALiBi), emphasizing tradeoffs like length extrapolation and long-context behavior that the current library doesn’t consolidate in one place.
   — covers: Learned positional embeddings: parameterization, training behavior, length limits, generalization tradeoffs vs sinusoidal, Relative positional approaches (high-level): relative position embeddings, relative attention bias (e.g., Shaw et al.), RoPE/ALiBi; when they matter (long context, extrapolation, locality), Inductive bias introduced by different positional schemes (absolute vs relative; fixed vs learned) and practical implications
- **[paper]** [RoFormer: Enhanced Transformer with Rotary Position Embedding](https://arxiv.org/pdf/2104.09864.pdf)
  RoPE is now a canonical relative-position method in modern LLMs; this is the primary paper and gives the cleanest authoritative account of the mechanism and why it helps extrapolation/relative reasoning.
   — covers: Relative positional approaches (high-level): relative position embeddings, relative attention bias (e.g., Shaw et al.), RoPE/ALiBi; when they matter (long context, extrapolation, locality)
- **[paper]** [Explore Better Relative Position Embeddings from Encoding Perspective](https://aclanthology.org/2021.emnlp-main.237.pdf)
  A strong, peer-reviewed ACL/EMNLP reference that systematizes relative position embedding design and comparisons; it’s more authoritative than a generic comparison blog for the “relative schemes” gap.
   — covers: Relative positional approaches (high-level): relative position embeddings, relative attention bias (e.g., Shaw et al.), RoPE/ALiBi; when they matter (long context, extrapolation, locality)
- **[paper]** [RoFormer: Enhanced Transformer with Rotary Position Embedding](https://arxiv.org/pdf/2104.09864.pdf) *(promoted by reviewer)*
  RoPE is now a canonical relative-position method in modern LLMs; this is the primary paper and gives the cleanest authoritative account of the mechanism and why it helps extrapolation/relative reasoning.
   — fills: Relative positional approaches (high-level): relative position embeddings, relative attention bias (e.g., Shaw et al.), RoPE/ALiBi; when they matter (long context, extrapolation, locality)
- **[paper]** [Explore Better Relative Position Embeddings from Encoding Perspective](https://aclanthology.org/2021.emnlp-main.237.pdf) *(promoted by reviewer)*
  A strong, peer-reviewed ACL/EMNLP reference that systematizes relative position embedding design and comparisons; it’s more authoritative than a generic comparison blog for the “relative schemes” gap.
   — fills: Relative positional approaches (high-level): relative position embeddings, relative attention bias (e.g., Shaw et al.), RoPE/ALiBi; when they matter (long context, extrapolation, locality)

## Near-Misses (13) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **[PDF] Theoretical Analysis of Positional Encodings in Transf** — [[PDF] Theoretical Analysis of Positional Encodings in Transformer Models](https://arxiv.org/pdf/2506.06398.pdf)
  _Skipped because:_ Potentially valuable, but it’s very new and not yet clearly established as a reliable/standard reference compared to more canonical positional-encoding sources.
- **Theoretical Analysis of Positional Encodings in ...** — [Theoretical Analysis of Positional Encodings in ...](https://arxiv.org/html/2506.06398v1)
  _Skipped because:_ Same work as the PDF; kept out for now due to recency and uncertain long-term canonical status.
- **Inside Sinusoidal Position Embeddings: A Sense of Order** — [Inside Sinusoidal Position Embeddings: A Sense of Order](https://learnopencv.com/sinusoidal-position-embeddings/)
  _Skipped because:_ Likely a decent explanation, but it overlaps with existing Transformer explainers and doesn’t clearly add authoritative depth beyond what a stronger positional-encoding reference would.
- **What is Positional Encoding? | IBMwww.ibm.com › think › topi** — [What is Positional Encoding? | IBMwww.ibm.com › think › topics › positional-encoding](https://www.ibm.com/think/topics/positional-encoding)
  _Skipped because:_ High-level overview that’s too introductory/thin for the specific mechanics and tradeoffs the library is missing.
- **Positional Encoding in Transformers - GeeksforGeeks** — [Positional Encoding in Transformers - GeeksforGeeks](https://www.geeksforgeeks.org/nlp/positional-encoding-in-transformers/)
  _Skipped because:_ Generally lower signal-to-noise and less authoritative; unlikely to add beyond existing sources.
- **Function Periods** — [Function Periods](https://erdem.pl/2021/05/understanding-positional-encoding-in-transformers/)
  _Skipped because:_ Could be helpful, but it’s a personal blog and not clearly more comprehensive/authoritative than the best candidates added.
- **Sinusoidal Positional Encoding Formula** — [Sinusoidal Positional Encoding Formula](https://apxml.com/courses/foundations-transformers-architecture/chapter-4-positional-encoding-embedding-layer/sinusoidal-encoding-formulation)
  _Skipped because:_ Too narrow (mostly formula-focused) and not clearly a widely trusted/stable canonical reference.
- **A** — [A](https://proceedings.neurips.cc/paper_files/paper/2021/file/be3e9d3f7d70537357c67bb3f4086846-Supplemental.pdf)
  _Skipped because:_ Supplemental material with unclear metadata/title; not a stable, self-contained primary reference for the stated gap.
- **[PDF] Deep learning 13.2. Attention Mechanisms - François Fl** — [[PDF] Deep learning 13.2. Attention Mechanisms - François Fleuret](https://fleuret.org/dlc/materials/dlc-handout-13-2-attention-mechanisms.pdf)
  _Skipped because:_ Good general attention notes, but not specifically focused enough on positional encodings/relative schemes to justify inclusion for this lesson.
- **Position Encoding Vs...** — [Position Encoding Vs...](https://mbrenndoerfer.com/writing/position-problem-self-attention-word-order)
  _Skipped because:_ Likely overlaps with the added comparison post and appears less definitive than the symmetry-based paper for the permutation-invariance gap.
- **Positional Encoding in Transformer-Based Time Series ...** — [Positional Encoding in Transformer-Based Time Series ...](https://arxiv.org/html/2502.12370v1)
  _Skipped because:_ Domain-specific (time series) and likely not the best general-purpose reference for positional encoding mechanics and tradeoffs in NLP/LLMs.
- **Learning interpretable positional encodings in transformers ** — [Learning interpretable positional encodings in transformers ... - arXiv](https://arxiv.org/html/2406.08272v4)
  _Skipped because:_ Interesting but specialized; not clearly the best foundational addition versus more canonical relative-position papers (not present among candidates).
- **Position-Aware Sequential Attention for Accurate Next Item .** — [Position-Aware Sequential Attention for Accurate Next Item ... - arXiv](https://arxiv.org/html/2602.21052v1)
  _Skipped because:_ Recommender-system specific and not a core reference for positional encoding in standard Transformer architectures.

## Uncovered Gaps (3) — No Good Candidates Found
_Consider manually sourcing these, or run enrichment again with different search terms._

- Definition and mechanics of positional encoding in Transformers (how added/concatenated; where applied in encoder/decoder)
- Sinusoidal positional embeddings: formula, frequency spectrum, dot-product properties, extrapolation to longer sequences
- Relative positional approaches (high-level): relative position embeddings, relative attention bias (e.g., Shaw et al.), RoPE/ALiBi; when they matter (long context, extrapolation, locality)

## Reasoning
**Curator:** Added one rigorous paper to cover the formal permutation-invariance intuition and one strong comparative tutorial to cover practical tradeoffs across absolute/learned/relative schemes. Other candidates were either too thin, too domain-specific, or not yet clearly canonical/stable enough to merit inclusion.
**Reviewer:** The curator’s additions help, but the library still lacks at least one primary, canonical relative-position paper (RoPE) and a solid peer-reviewed relative-position reference to anchor the modern tradeoff discussion.

---

# Curation Report: Scaled Dot-Product Self-Attention: Math and Shapes
**Topic:** `transformer-architecture` | **Date:** 2026-04-08 11:03
**Library:** 4 existing → 6 sources (2 added, 2 downloaded)
**Candidates evaluated:** 15
**Reviewer verdict:** good

## Added (2)
- **[tutorial]** [Tutorial 6: Transformers and Multi-Head Attention¶](https://uvadlc-notebooks.readthedocs.io/en/latest/tutorial_notebooks/tutorial6/Transformers_and_MHAttention.html)
  Provides a concrete, implementation-oriented walkthrough of multi-head attention with explicit tensor shapes, including the batch/head reshapes and transposes that are usually glossed over in higher-level explanations.
   — covers: Explicit tensor shape walkthrough for scaled dot-product self-attention (Q, K, V, logits, attention weights, output) including batching and multi-head reshaping/transposes, Attention matrix definition and interpretation with shapes (e.g., T×T per head) and how it multiplies V
- **[tutorial]** [Numerical Stability in Flash Attention - - jarbus](https://jarbus.net/blog/numerical-stability-in-flash-attention/)
  Goes deep on the numerically-stable softmax used in attention (max-subtraction/log-sum-exp style), and discusses practical stability issues that arise with masking and low-precision (fp16/bfloat16) implementations.
   — covers: Softmax numerical stability in attention implementations (logit max-subtraction, masking strategy, handling -inf, fp16/bfloat16 stability)

## Near-Misses (13) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **[PDF] A Mathematical View of Attention Models in Deep Learni** — [[PDF] A Mathematical View of Attention Models in Deep Learning](https://people.tamu.edu/~sji/classes/attn.pdf)
  _Skipped because:_ Likely solid mathematically, but it is broader than scaled dot-product self-attention and is less directly focused on the specific Q/K/V shape bookkeeping and implementation details this lesson targets.
- **Transformers from Scratch** — [Transformers from Scratch](https://brandonrohrer.com/transformers.html)
  _Skipped because:_ Clear and approachable, but overlaps heavily with existing intuitive transformer explainers and is less rigorous about full batched multi-head tensor shapes.
- **Explained: Multi-head Attention (Part 1) - Erik Storrs** — [Explained: Multi-head Attention (Part 1) - Erik Storrs](https://storrs.io/attention/)
  _Skipped because:_ Good conceptual explanation, but not clearly superior to the existing Illustrated Transformer/Weng coverage for the specific math-and-shapes gaps.
- **Dot-product and Multi-head attention implementation in Tenso** — [Dot-product and Multi-head attention implementation in Tensorflow 2](https://gist.github.com/ekreutz/160070126d5e2261a939c4ddf6afb642)
  _Skipped because:_ Useful code, but a gist is a less stable/curatable reference than a maintained tutorial or library implementation, and it’s not clearly adding beyond nanoGPT for this library.
- **Practice: Implementing Scaled Dot-Product Attention** — [Practice: Implementing Scaled Dot-Product Attention](https://apxml.com/courses/foundations-transformers-architecture/chapter-2-attention-mechanism-core-concepts/practice-implementing-attention)
  _Skipped because:_ Potentially helpful, but appears to be courseware with uncertain long-term accessibility and unclear depth/rigor relative to the best free references.
- **Attention (machine learning) - Wikipedia** — [Attention (machine learning) - Wikipedia](https://en.wikipedia.org/wiki/Attention_(machine_learning))
  _Skipped because:_ Too high-level and not focused on the detailed tensor-shape walkthrough or numerical stability implementation details.
- **Efficient attention explained: the math behind linear-time t** — [Efficient attention explained: the math behind linear-time transformers](https://blog.lambdaclass.com/efficient-attention-explained-the-math-behind-linear-time-transformers/)
  _Skipped because:_ Focuses on efficient/linear attention variants rather than nailing the core scaled dot-product attention shapes and stable softmax/masking mechanics.
- **Paper page - Revisiting Softmax Masking for Stability in Con** — [Paper page - Revisiting Softmax Masking for Stability in Continual Learning](https://huggingface.co/papers/2309.14808)
  _Skipped because:_ Not primarily about attention implementations; the stability discussion is in a different context and the HF page is a secondary wrapper rather than the canonical paper source.
- **FLASH-D: FlashAttention with Hidden Softmax Division - arXiv** — [FLASH-D: FlashAttention with Hidden Softmax Division - arXiv](https://arxiv.org/html/2505.14201v1)
  _Skipped because:_ Research-focused and likely valuable, but it’s about a specific FlashAttention variant; for this lesson’s gap, a targeted numerical-stability explainer is more directly useful.
- **Statistical Advantage of Softmax Attention** — [Statistical Advantage of Softmax Attention](https://arxiv.org/html/2509.21936v1)
  _Skipped because:_ More theoretical/statistical than implementation-oriented; doesn’t directly address the practical masking/-inf/fp16 stability concerns.
- **Tensor Product Attention Is All You Need** — [Tensor Product Attention Is All You Need](https://arxiv.org/html/2501.06425v3)
  _Skipped because:_ About an alternative attention mechanism; not the best fit for a lesson specifically on scaled dot-product self-attention math/shapes.
- **Attention Is All You Need** — [Attention Is All You Need](https://arxiv.org/html/1706.03762v7)
  _Skipped because:_ Already included in the current library (redundant).
- **Long Context Attention - Harold Benoit** — [Long Context Attention - Harold Benoit](https://haroldbenoit.com/notes/ml/llms/architecture/transformers/long-context-attention)
  _Skipped because:_ Likely useful notes, but the focus is long-context methods rather than the core attention tensor-shape walkthrough and stable softmax implementation details.

## Reasoning
**Curator:** The UVADLC notebook is the strongest single addition for explicit Q/K/V-to-output tensor shape bookkeeping (including multi-head reshaping), while the FlashAttention numerical stability post directly addresses the missing practical details around stable softmax, masking, and low-precision behavior.
**Reviewer:** The current library plus the two added tutorials already cover the core scaled dot-product attention math, tensor shapes (batched + multi-head), and practical numerical-stability/masking concerns; none of the near-misses clearly add unique, authoritative value for this specific lesson.
