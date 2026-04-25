# Curation Report: Scaled Dot-Product Attention in Depth
**Topic:** `neural-networks` | **Date:** 2026-04-07 15:48
**Library:** 6 existing → 11 sources (5 added, 3 downloaded, 1 failed)
**Candidates evaluated:** 35
**Reviewer verdict:** needs_additions

## Added (5)
- **[paper]** [Properties of Dot Product of Random Vectors](https://funnywii.com/upload/proof.pdf)
  Provides a rigorous mathematical proof that Var(q·k) = d_k when components are i.i.d. with zero mean and unit variance — the foundational lemma for the 1/√d_k scaling factor — which no existing library source covers.
   — covers: Variance of dot products: proof that Var(q·k) = d_k when components are i.i.d. with zero mean and unit variance, Full derivation of 1/√d_k scaling factor from variance analysis of dot products with d_k-dimensional vectors
- **[tutorial]** [A Gentle Introduction to Attention Masking in Transformer Models](https://machinelearningmastery.com/a-gentle-introduction-to-attention-masking-in-transformer-models/)
  Covers both padding masks (setting scores to -infinity before softmax) and causal/look-ahead masking with concrete PyTorch code, filling multiple masking gaps absent from the current library.
   — covers: Padding mask: how to mask out padding tokens in attention by setting scores to -infinity before softmax, Causal mask / autoregressive masking: upper-triangular mask to prevent attending to future positions, Look-ahead mask: implementation details and use in decoder self-attention
- **[tutorial]** [Math behind √dₖ Scaling Factor in Attention - Outcome School](https://outcomeschool.com/blog/scaling-dot-product-attention)
  Provides a focused, well-structured walkthrough of the full matrix form Attention(Q,K,V) = softmax(QK^T/√d_k)V with dimensional analysis and the variance motivation, covering gaps not addressed by any existing library source.
   — covers: Matrix form of scaled dot-product attention: Attention(Q,K,V) = softmax(QK^T/√d_k)V with full dimensional analysis, Full derivation of 1/√d_k scaling factor from variance analysis of dot products with d_k-dimensional vectors, Softmax saturation: detailed explanation of gradient vanishing when inputs have large magnitude
- **[paper]** [Attention Is All You Need](https://arxiv.org/html/1706.03762v7)
  This is the seminal Vaswani et al. 2017 paper that introduced scaled dot-product attention; it is the primary authoritative reference for the entire lesson topic and its absence from the library is a significant oversight regardless of what tutorials cover.
   — covers: Matrix form of scaled dot-product attention: Attention(Q,K,V) = softmax(QK^T/√d_k)V with full dimensional analysis, Causal mask / autoregressive masking: upper-triangular mask to prevent attending to future positions, Look-ahead mask: implementation details and use in decoder self-attention
- **[paper]** [Attention Is All You Need](https://arxiv.org/html/1706.03762v7) *(promoted by reviewer)*
  This is the seminal Vaswani et al. 2017 paper that introduced scaled dot-product attention; it is the primary authoritative reference for the entire lesson topic and its absence from the library is a significant oversight regardless of what tutorials cover.
   — fills: Matrix form of scaled dot-product attention: Attention(Q,K,V) = softmax(QK^T/√d_k)V with full dimensional analysis, Causal mask / autoregressive masking: upper-triangular mask to prevent attending to future positions, Look-ahead mask: implementation details and use in decoder self-attention

## Near-Misses (5) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **Scaled Dot-Product Attention Explained - ApX Machine Learnin** — [Scaled Dot-Product Attention Explained - ApX Machine Learning](https://apxml.com/courses/foundations-transformers-architecture/chapter-2-attention-mechanism-core-concepts/scaled-dot-product-attention)
  _Skipped because:_ Content appears largely duplicated across multiple apxml.com course pages and overlaps heavily with the outcomeschool.com source already selected.
- **Scaled Dot-Product Attention and Masking in Transformers** — [Scaled Dot-Product Attention and Masking in Transformers](https://codesignal.com/learn/courses/sequence-models-the-dawn-of-attention-1/lessons/scaled-dot-product-attention-and-masking-in-transformers-1)
  _Skipped because:_ Covers similar ground to the selected masking and scaling sources but is behind a course paywall/login, making it unsuitable for a stable open library.
- **Alternatives to the Scaled Dot Product for Attention** — [Alternatives to the Scaled Dot Product for Attention](https://arxiv.org/pdf/2311.09406.pdf)
  _Skipped because:_ Focuses on alternatives to scaled dot-product attention rather than substantively teaching the mechanism itself, so it does not fill the identified gaps.
- **Learn Masking in Attention: Causal and Padding Masks** — [Learn Masking in Attention: Causal and Padding Masks](https://codefinity.com/courses/v2/e7ee0772-6b82-4a1c-96ba-69b85ddee608/f35bf119-fe3c-4db6-8a48-51dbc163416f/8c99758d-e015-49c3-9f59-44cb55ae9aae)
  _Skipped because:_ Redundant with the selected machinelearningmastery.com masking tutorial and hosted on a platform with less stable URLs.
- **Why do we normalize by the root of the dimension in attentio** — [Why do we normalize by the root of the dimension in attention?](https://will-ye.com/attention-root/)
  _Skipped because:_ Covers the scaling derivation but appears to be a personal blog with uncertain long-term stability; the proof PDF and outcomeschool sources are more authoritative.

## Uncovered Gaps (1) — No Good Candidates Found
_Consider manually sourcing these, or run enrichment again with different search terms._

- Numerical stability in attention: techniques such as subtracting the maximum logit before applying softmax

## Reasoning
**Curator:** The three selected sources collectively fill the most critical mathematical and practical gaps: a rigorous proof PDF for the variance lemma, a focused math tutorial for the matrix form and scaling derivation, and a reputable practical tutorial covering all three masking variants. Redundant apxml/codesignal candidates were excluded to keep the library lean, and the numerical stability gap remains uncovered as no candidate addresses it substantively.
**Reviewer:** The curator made reasonable choices for tutorials and derivations but critically omitted the Vaswani et al. 'Attention Is All You Need' paper — the seminal source for the entire lesson — while no candidate adequately fills the still-open numerical stability gap.

---

# Curation Report: Bahdanau (Additive) Attention: Equations and Intuition
**Topic:** `neural-networks` | **Date:** 2026-04-08 00:34
**Library:** 9 existing → 14 sources (5 added, 2 downloaded, 2 failed)
**Candidates evaluated:** 28
**Reviewer verdict:** needs_additions

## Added (5)
- **[paper]** [Neural Machine Translation by Jointly Learning to Align and Translate](https://arxiv.org/pdf/1409.0473v3.pdf)
  This is the original Bahdanau et al. paper introducing the alignment model and additive (MLP) scoring, with the canonical equations for energies, soft alignments (attention weights), and context vectors in NMT.
   — covers: Bahdanau (additive) attention equations: e_{t,i} = v^T tanh(W_s s_{t-1} + W_h h_i) and alpha_{t,i} = softmax(e_{t,i}), Definition and intuition of the alignment model in NMT (how it learns soft alignments between target step t and source position i), Role of decoder state as the query in additive attention (using s_{t-1} or s_t) and how it interacts with encoder hidden states h_i, Energy/score function terminology and how it differs from dot-product attention, Context vector computation c_t = sum_i alpha_{t,i} h_i and how it conditions the decoder output, Why an MLP (additive) scoring function can be effective vs dot-product (capacity, learned similarity, handling differing dimensions)
- **[tutorial]** [11.4. The Bahdanau Attention Mechanism - Dive into Deep Learning](https://d2l.ai/chapter_attention-mechanisms-and-transformers/bahdanau-attention.html)
  A clear, stable textbook-style walkthrough of Bahdanau attention with step-by-step equations and implementation-oriented intuition (decoder state as query, energies → softmax weights → context vector).
   — covers: Bahdanau (additive) attention equations: e_{t,i} = v^T tanh(W_s s_{t-1} + W_h h_i) and alpha_{t,i} = softmax(e_{t,i}), Definition and intuition of the alignment model in NMT (how it learns soft alignments between target step t and source position i), Role of decoder state as the query in additive attention (using s_{t-1} or s_t) and how it interacts with encoder hidden states h_i, Context vector computation c_t = sum_i alpha_{t,i} h_i and how it conditions the decoder output
- **[reference_doc]** [11.3. Attention Scoring Functions - Dive into Deep Learning](https://d2l.ai/chapter_attention-mechanisms-and-transformers/attention-scoring-functions.html)
  Provides a focused comparison of additive vs dot-product scoring (energy functions), including terminology and the modeling-capacity rationale for MLP-based scoring and handling mismatched dimensions.
   — covers: Energy/score function terminology and how it differs from dot-product attention, Why an MLP (additive) scoring function can be effective vs dot-product (capacity, learned similarity, handling differing dimensions)
- **[reference_doc]** [Speech and Language Processing (3rd ed. draft) — Encoder-Decoder Models, Attention, and Contextual Embeddings (Jurafsky & Martin)](https://web.stanford.edu/~jurafsky/slp3/old_oct19/10.pdf)
  This is a highly authoritative Stanford textbook draft with a very clear, pedagogical derivation of encoder–decoder attention (including Bahdanau-style alignment intuition) that complements the original paper and D2L with more narrative explanation and standard terminology.
- **[reference_doc]** [Speech and Language Processing (3rd ed. draft) — Encoder-Decoder Models, Attention, and Contextual Embeddings (Jurafsky & Martin)](https://web.stanford.edu/~jurafsky/slp3/old_oct19/10.pdf) *(promoted by reviewer)*
  This is a highly authoritative Stanford textbook draft with a very clear, pedagogical derivation of encoder–decoder attention (including Bahdanau-style alignment intuition) that complements the original paper and D2L with more narrative explanation and standard terminology.

## Near-Misses (5) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **Chapter 8 Attention and Self-Attention for NLP** — [Chapter 8 Attention and Self-Attention for NLP](https://slds-lmu.github.io/seminar_nlp_ss20/attention-and-self-attention-for-nlp.html)
  _Skipped because:_ Covers the right equations, but is less authoritative/stable than D2L for a core library slot and overlaps heavily with the D2L chapters.
- **The Bahdanau Attention Mechanism - MachineLearningMastery.co** — [The Bahdanau Attention Mechanism - MachineLearningMastery.com](https://machinelearningmastery.com/the-bahdanau-attention-mechanism/)
  _Skipped because:_ Readable but largely redundant once the original paper and D2L are included, and tends to be lighter on precise alignment-model framing.
- **Transformer** — [Transformer](https://lilianweng.github.io/posts/2018-06-24-attention/)
  _Skipped because:_ High quality, but its emphasis is broader attention/transformers rather than the specific Bahdanau alignment-model equations and decoder-query details targeted by the gaps.
- **why Bahdanau is Additive?** — [why Bahdanau is Additive?](https://gist.github.com/ritwikraha/2466b901cb22bbe65288e4bb499e0ebc)
  _Skipped because:_ Too thin and informal (gist) for a curated teaching wiki, despite matching the equation gap.
- **[PDF] Class Notes: Attention Mechanisms in Neural Networks** — [[PDF] Class Notes: Attention Mechanisms in Neural Networks](https://www.khoury.northeastern.edu/home/vip/teach/MLcourse/7_adv_NN/notes/chatGPT_responses/attention_mechanisms_tikz.pdf)
  _Skipped because:_ Looks potentially useful but appears to be a generated/compiled notes artifact with unclear provenance and long-term stability compared to D2L and the original paper.

## Reasoning
**Curator:** The library is missing the seminal Bahdanau alignment paper and a high-quality, equation-forward tutorial; adding the original paper plus the two D2L chapters fills essentially all listed gaps with authoritative, stable sources while avoiding redundant or thin writeups.
**Reviewer:** The core picks (Bahdanau + D2L) are strong, but adding the Jurafsky & Martin SLP chapter would materially improve authority and clarity without being redundant.
