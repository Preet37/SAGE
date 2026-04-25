# Curation Report: Luong (Multiplicative) Attention and Variants
**Topic:** `scaling-laws` | **Date:** 2026-04-08 01:18
**Library:** 9 existing → 17 sources (8 added, 3 downloaded, 2 failed)
**Candidates evaluated:** 19
**Reviewer verdict:** needs_additions

## Added (8)
- **[paper]** [[PDF] arXiv:1508.04025v5 [cs.CL] 20 Sep 2015](https://arxiv.org/pdf/1508.04025.pdf)
  This is the original Luong et al. paper that formally defines global vs local attention (including predictive position p_t and windowing) and the multiplicative scoring variants, providing the authoritative reference missing from the current library.
   — covers: Luong (multiplicative) attention scoring functions: dot (q^T k), general (q^T W k), concat (v^T tanh(W[q;k]))—definitions, when used, dimensionality constraints, and worked examples, Luong global vs local attention: formal definitions, alignment computation, local window selection (predictive position p_t), and practical implications for long sequences, Complexity analysis: per decoding step cost for global attention vs local/windowed attention; impact on training/inference latency and memory
- **[paper]** [Attention Is All You Need](https://arxiv.org/html/1706.03762v7)
  Adds a canonical, citable treatment of dot-product attention and the key scaling/efficiency motivation (scaled dot-product vs additive), which helps ground the Luong-vs-Bahdanau comparison and speed/memory tradeoffs in an authoritative source.
   — covers: Comparison of multiplicative (Luong) vs additive (Bahdanau) attention: parameterization, expressiveness, and typical speed/memory tradeoffs (matrix multiplies vs MLP), including scaling with hidden size
- **[paper]** [Neural Machine Translation by Jointly Learning to Align and Translate (Bahdanau et al., 2014)](https://arxiv.org/abs/1409.0473)
  Even though the lesson centers on Luong (multiplicative) attention, Bahdanau et al. is the seminal additive-attention reference that defines the baseline comparison (additive vs multiplicative) and is routinely cited alongside Luong and Transformers.
   — covers: Luong (multiplicative) attention scoring functions: dot (q^T k), general (q^T W k), concat (v^T tanh(W[q;k]))—definitions, when used, dimensionality constraints, and worked examples
- **[tutorial]** [Dive into Deep Learning (d2l.ai) — Attention Mechanisms](https://d2l.ai/chapter_attention-mechanisms/index.html)
  High-authority, stable, and pedagogically strong; it gives clear derivations and implementations of attention scoring functions (including dot-product and additive) with shape/dimensionality discussion that directly supports teaching Luong-style scoring.
   — covers: Luong (multiplicative) attention scoring functions: dot (q^T k), general (q^T W k), concat (v^T tanh(W[q;k]))—definitions, when used, dimensionality constraints, and worked examples
- **[video]** [Stanford CS224N — Lecture notes/videos on Attention and Transformers](https://nlp.stanford.edu/courses/cs224n/)
  A highly authoritative course source that typically includes the clearest shape/complexity explanations and the historical progression (Bahdanau → Luong → scaled dot-product), making it a strong teaching complement to the primary papers.
   — covers: Luong (multiplicative) attention scoring functions: dot (q^T k), general (q^T W k), concat (v^T tanh(W[q;k]))—definitions, when used, dimensionality constraints, and worked examples
- **[paper]** [Neural Machine Translation by Jointly Learning to Align and Translate (Bahdanau et al., 2014)](https://arxiv.org/abs/1409.0473) *(promoted by reviewer)*
  Even though the lesson centers on Luong (multiplicative) attention, Bahdanau et al. is the seminal additive-attention reference that defines the baseline comparison (additive vs multiplicative) and is routinely cited alongside Luong and Transformers.
   — fills: Luong (multiplicative) attention scoring functions: dot (q^T k), general (q^T W k), concat (v^T tanh(W[q;k]))—definitions, when used, dimensionality constraints, and worked examples
- **[tutorial]** [Dive into Deep Learning (d2l.ai) — Attention Mechanisms](https://d2l.ai/chapter_attention-mechanisms/index.html) *(promoted by reviewer)*
  High-authority, stable, and pedagogically strong; it gives clear derivations and implementations of attention scoring functions (including dot-product and additive) with shape/dimensionality discussion that directly supports teaching Luong-style scoring.
   — fills: Luong (multiplicative) attention scoring functions: dot (q^T k), general (q^T W k), concat (v^T tanh(W[q;k]))—definitions, when used, dimensionality constraints, and worked examples
- **[video]** [Stanford CS224N — Lecture notes/videos on Attention and Transformers](https://nlp.stanford.edu/courses/cs224n/) *(promoted by reviewer)*
  A highly authoritative course source that typically includes the clearest shape/complexity explanations and the historical progression (Bahdanau → Luong → scaled dot-product), making it a strong teaching complement to the primary papers.
   — fills: Luong (multiplicative) attention scoring functions: dot (q^T k), general (q^T W k), concat (v^T tanh(W[q;k]))—definitions, when used, dimensionality constraints, and worked examples

## Near-Misses (13) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **Luong Attention: Dot Product, General & Local Attention Mech** — [Luong Attention: Dot Product, General & Local Attention Mechanisms](https://mbrenndoerfer.com/writing/luong-attention-mechanisms-dot-product-general-local)
  _Skipped because:_ Likely useful as a tutorial, but it appears to overlap heavily with the SOTAAZ/Language AI Handbook content and is less authoritative than adding the original Luong paper.
- **Which One Should You Actually Use? (Spoiler: Luong) | SOTAAZ** — [Which One Should You Actually Use? (Spoiler: Luong) | SOTAAZ Blog](https://www.sotaaz.com/blog/attention-mechanism-implementation-en)
  _Skipped because:_ Covers the right topics but is a blog-style secondary source; the library benefits more from the seminal Luong paper plus a canonical attention paper than from an opinionated implementation article.
- **Bahdanau vs Luong Attention: Which One Should You Actually U** — [Bahdanau vs Luong Attention: Which One Should You Actually Use ...](https://www.sotaaz.com/post/attention-mechanism-implementation-en)
  _Skipped because:_ Redundant with other SOTAAZ entries and not as stable/authoritative as primary literature for a curated teaching wiki.
- **Bahdanau vs Luong Attention: Which One Should You ...** — [Bahdanau vs Luong Attention: Which One Should You ...](https://blog.sotaaz.com/post/attention-mechanism-implementation-en)
  _Skipped because:_ Same content family as the other SOTAAZ links; adds little beyond what primary papers can cover more reliably.
- **Define the luong attention mechanism** — [Define the luong attention mechanism](https://gist.github.com/edumunozsala/faa33c7abe2358b7944708f6cb31ec0f)
  _Skipped because:_ A gist is not a stable, high-quality reference for a teaching wiki and is likely too thin compared to papers/tutorial chapters.
- **[PDF] Class Notes: Attention Mechanisms in Neural Networks** — [[PDF] Class Notes: Attention Mechanisms in Neural Networks](https://www.khoury.northeastern.edu/home/vip/teach/MLcourse/7_adv_NN/notes/chatGPT_responses/attention_mechanisms_tikz.pdf)
  _Skipped because:_ Course notes can be helpful, but the 'chatGPT_responses' path suggests uncertain provenance and long-term stability for citation-quality curation.
- **Class Notes: Attention Mechanisms in Neural Networks** — [Class Notes: Attention Mechanisms in Neural Networks](https://www.khoury.northeastern.edu/home/vip/teach/MLcourse/7_adv_NN/notes/chatGPT_responses/attention_mechanisms_latest.pdf)
  _Skipped because:_ Same provenance/stability concerns as the other notes PDF; not clearly more valuable than adding primary sources.
- **Chapter 8 Attention and Self-Attention for NLP** — [Chapter 8 Attention and Self-Attention for NLP](https://slds-lmu.github.io/seminar_nlp_ss20/attention-and-self-attention-for-nlp.html)
  _Skipped because:_ Potentially solid, but without clear evidence it deeply covers Luong local attention (p_t/windowing) and complexity per decoding step, it’s less compelling than the seminal Luong paper.
- **The Luong Attention Mechanism | MKAI** — [The Luong Attention Mechanism | MKAI](https://mkai.org/ai-global-news/the-luong-attention-mechanism/)
  _Skipped because:_ Looks like a secondary summary and may be shallow/derivative; not needed once the original Luong paper is included.
- **Attention in Neural Networks - 12. Various attention mechani** — [Attention in Neural Networks - 12. Various attention mechanisms (1)](https://buomsoo-kim.github.io/attention/2020/03/18/Attention-mechanism-12.md/)
  _Skipped because:_ Blog notes can be useful, but this is less authoritative and potentially redundant with stronger primary references.
- **Ecotransformer: Attention without Multiplication - arXiv** — [Ecotransformer: Attention without Multiplication - arXiv](https://arxiv.org/html/2507.20096v1)
  _Skipped because:_ Not directly focused on Luong attention variants/global-vs-local definitions; it’s more about alternative attention formulations than filling the specific gaps.
- **[PDF] arXiv:2312.08618v1 [cs.CL] 14 Dec 2023** — [[PDF] arXiv:2312.08618v1 [cs.CL] 14 Dec 2023](https://arxiv.org/pdf/2312.08618.pdf)
  _Skipped because:_ Covers Transformer full-attention vs efficient variants rather than Luong global/local attention in seq2seq decoding; useful but off-target for the stated lesson.
- **arXiv:1508.04025v5  [cs.CL]  20 Sep 2015** — [arXiv:1508.04025v5  [cs.CL]  20 Sep 2015](https://arxiv.org/pdf/1508.04025v5.pdf)
  _Skipped because:_ Duplicate of the same Luong paper already added (prefer a single canonical URL).

## Uncovered Gaps (1) — No Good Candidates Found
_Consider manually sourcing these, or run enrichment again with different search terms._

- Luong (multiplicative) attention scoring functions: dot (q^T k), general (q^T W k), concat (v^T tanh(W[q;k]))—definitions, when used, dimensionality constraints, and worked examples

## Reasoning
**Curator:** The library is missing primary, authoritative coverage of Luong attention; adding the original Luong et al. paper fills the core definitions (global/local, scoring) and supports complexity discussion. Adding the Transformer paper provides a canonical reference for dot-product attention efficiency and scaling to support the multiplicative-vs-additive tradeoff discussion, while most blog/tutorial candidates are redundant or less reliable.
**Reviewer:** The curator correctly prioritized Luong (2015) and the Transformer paper, but the library still lacks the canonical additive-attention paper and at least one high-authority teaching reference (e.g., d2l.ai/CS224N) to close the remaining scoring-function/shape-explanation gap.
