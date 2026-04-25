# Curation Report: Bahdanau (Additive) Attention: Formulation and Intuition
**Topic:** `rnns-lstms` | **Date:** 2026-04-09 15:49
**Library:** 21 existing → 26 sources (5 added, 3 downloaded)
**Candidates evaluated:** 29
**Reviewer verdict:** needs_additions

## Added (5)
- **[tutorial]** [11.4. The Bahdanau Attention Mechanism - Dive into Deep Learning](https://d2l.ai/chapter_attention-mechanisms-and-transformers/bahdanau-attention.html)
  Adds a dedicated, textbook-quality treatment of Bahdanau/additive attention with the full scoring function, softmax alignment weights, context-vector computation, and how these integrate into an RNN seq2seq decoder step-by-step (often with code). This directly targets the missing formulation/timing details beyond the more general attention resources already in the library.
   — covers: Bahdanau (additive) attention score function: e_{t,i} = v^T tanh(W_s s_{t-1} + W_h h_i) (or equivalent) and how it differs from dot-product attention, Alignment model definition and training: computing e_{t,i}, applying softmax to get α_{t,i}, and learning parameters jointly with seq2seq, Decoder hidden state as the attention query at each decoding step; timing (use of s_{t-1} vs s_t) and integration with output generation, Encoder hidden states/annotations as keys/values (memory) for attention in RNN seq2seq, Context vector computation: c_t = Σ_i α_{t,i} h_i and how it conditions the decoder/output layer, Soft alignment intuition and interpretability: attention weights as alignment probabilities; qualitative alignment visualization and training dynamics vs fixed-length bottleneck
- **[reference_doc]** [Speech and Language Processing (3rd ed. draft), Chapter 10: Encoder-Decoder Models, Attention, and Contextual Embeddings (Jurafsky & Martin)](https://web.stanford.edu/~jurafsky/slp3/old_oct19/10.pdf)
  This is a high-authority, textbook-style treatment from Stanford authors that cleanly derives the seq2seq+attention equations and provides strong intuition/terminology alignment (query/key/value, context vector) that complements D2L with a more canonical NLP-textbook framing.
- **[reference_doc]** [CS224n Notes: Neural Machine Translation, Seq2seq and Attention (Stanford)](https://web.stanford.edu/class/cs224n/readings/cs224n-2019-notes06-NMT_seq2seq_attention.pdf)
  A durable, widely-cited institutional note set that explains Bahdanau-style attention in the original RNN NMT setting (alignment scores, softmax weights, context vector, decoder integration) with unusually clear diagrams and consistent notation—excellent for teaching and cross-checking timing/details.
- **[reference_doc]** [Speech and Language Processing (3rd ed. draft), Chapter 10: Encoder-Decoder Models, Attention, and Contextual Embeddings (Jurafsky & Martin)](https://web.stanford.edu/~jurafsky/slp3/old_oct19/10.pdf) *(promoted by reviewer)*
  This is a high-authority, textbook-style treatment from Stanford authors that cleanly derives the seq2seq+attention equations and provides strong intuition/terminology alignment (query/key/value, context vector) that complements D2L with a more canonical NLP-textbook framing.
- **[reference_doc]** [CS224n Notes: Neural Machine Translation, Seq2seq and Attention (Stanford)](https://web.stanford.edu/class/cs224n/readings/cs224n-2019-notes06-NMT_seq2seq_attention.pdf) *(promoted by reviewer)*
  A durable, widely-cited institutional note set that explains Bahdanau-style attention in the original RNN NMT setting (alignment scores, softmax weights, context vector, decoder integration) with unusually clear diagrams and consistent notation—excellent for teaching and cross-checking timing/details.

## Near-Misses (14) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **The Bahdanau Attention Mechanism - MachineLearningMastery.co** — [The Bahdanau Attention Mechanism - MachineLearningMastery.com](https://machinelearningmastery.com/the-bahdanau-attention-mechanism/)
  _Skipped because:_ Covers the core equations, but is less authoritative/stable than D2L and tends to be more redundant with existing general-attention blog resources already in the library.
- **[PDF] Encoder‐Decoder Models and Attention** — [[PDF] Encoder‐Decoder Models and Attention](https://www1.se.cuhk.edu.hk/~seem5680/lecture/Encoder-Decoder-Attention-2022spring.pdf)
  _Skipped because:_ Likely useful lecture slides, but course PDFs can be less stable and the library already has multiple strong explanations of encoder-decoder attention; D2L is the more durable, comprehensive gap-filler.
- **Building Attention Mechanisms from Scratch - ApX Machine Lea** — [Building Attention Mechanisms from Scratch - ApX Machine Learning](https://apxml.com/courses/advanced-tensorflow/chapter-7-implementing-advanced-architectures/building-attention-mechanisms)
  _Skipped because:_ Redundant with existing ApX materials already in the library and unlikely to add substantially beyond the dedicated D2L Bahdanau chapter.
- **why Bahdanau is Additive?** — [why Bahdanau is Additive?](https://gist.github.com/ritwikraha/2466b901cb22bbe65288e4bb499e0ebc)
  _Skipped because:_ Too thin/unstable (gist) for a curated teaching wiki despite being on-topic.
- **Attention in Neural Networks - 8. Alignment Models (1) - Buo** — [Attention in Neural Networks - 8. Alignment Models (1) - Buomsoo Kim](https://buomsoo-kim.github.io/attention/2020/03/05/Attention-mechanism-8.md/)
  _Skipped because:_ Potentially relevant, but appears inconsistent with the provided preview and is less clearly authoritative than D2L for filling the specific Bahdanau formulation/training gaps.
- **Attention Networks and Diffusion Models** — [Attention Networks and Diffusion Models](https://gds.techfak.uni-bielefeld.de/_media/teaching/2023summer/attention/lecture2-180423.pdf)
  _Skipped because:_ Looks like broader lecture material; unclear it focuses deeply on Bahdanau seq2seq alignment/context details versus more modern attention topics.
- **Attention Mechanism in ML - GeeksforGeeks** — [Attention Mechanism in ML - GeeksforGeeks](https://www.geeksforgeeks.org/artificial-intelligence/ml-attention-mechanism/)
  _Skipped because:_ Generally introductory and not reliably deep on the exact Bahdanau alignment formulation/timing; also lower signal-to-noise than existing sources.
- **Attention Mechanism [1]: Seq2Seq Models - Chunpai Wang** — [Attention Mechanism [1]: Seq2Seq Models - Chunpai Wang](https://chunpai.github.io/2020/06/15/Attention-Mechanism-1.html)
  _Skipped because:_ Hard to validate quality from the snippet (which appears mismatched); likely redundant with existing blog-style explanations.
- **Sequence-To-Sequence Model...** — [Sequence-To-Sequence Model...](https://www.davidsbatista.net/blog/2020/01/25/Attention-seq2seq/)
  _Skipped because:_ May be a decent walkthrough, but the library already includes strong seq2seq+attention explainers (e.g., Jalammar, Weng, D2L); not clearly additive versus those.
- **arXiv:2307.01715v3 [cs.CL] 7 Mar 2024** — [arXiv:2307.01715v3 [cs.CL] 7 Mar 2024](https://arxiv.org/pdf/2307.01715.pdf)
  _Skipped because:_ About CTC alignment optimization rather than Bahdanau additive attention in RNN seq2seq; off-target for the lesson.
- **ALIGN WITH PURPOSE: OPTIMIZE DESIRED PROPER** — [ALIGN WITH PURPOSE: OPTIMIZE DESIRED PROPER](https://proceedings.iclr.cc/paper_files/paper/2024/file/5aadf1e309cc03cab3ec35afb7c9d0c8-Paper-Conference.pdf)
  _Skipped because:_ Same issue as the arXiv version: alignment in CTC, not the Bahdanau attention alignment model used in encoder-decoder NMT.
- **Published as a conference paper at ICLR 2024** — [Published as a conference paper at ICLR 2024](https://arxiv.org/pdf/2307.01715v3.pdf)
  _Skipped because:_ Duplicate of the same CTC-focused work; not relevant to Bahdanau attention formulation/intuitions.
- **A** — [A](https://proceedings.neurips.cc/paper/2021/file/ba3c736667394d5082f86f28aef38107-Supplemental.pdf)
  _Skipped because:_ Insufficiently identified and not clearly about Bahdanau attention; supplemental PDFs without clear context are poor curated-library entries.
- **Sequence-to-Sequence Models with Attention Mechanistically .** — [Sequence-to-Sequence Models with Attention Mechanistically ...](https://arxiv.org/pdf/2506.17424.pdf)
  _Skipped because:_ Interesting but tangential (cognitive/memory mapping) and not a focused resource for teaching the Bahdanau attention formulation and decoder integration.

## Reasoning
**Curator:** Only the dedicated D2L Bahdanau chapter clearly and authoritatively fills the specific additive-attention formulation, alignment/softmax/context computation, and decoder-timing integration gaps without being redundant. The remaining candidates are either lower-quality/unstable, redundant with existing blog resources, or off-topic (CTC alignment).
**Reviewer:** The D2L Bahdanau chapter is a strong core choice, but adding one or two Stanford-authoritative references (SLP3 + CS224n notes) would materially improve authority, durability, and pedagogical clarity without redundancy.
