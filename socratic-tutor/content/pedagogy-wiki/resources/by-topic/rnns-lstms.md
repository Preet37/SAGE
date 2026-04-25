# Rnns Lstms

## Video (best)
- **Andrej Karpathy** — "The spelled-out intro to language modeling: building makemore" (covers RNNs deeply in context)
- youtube_id: PaCmpygFfXo
- Why: Karpathy builds RNN-based character-level language models from scratch, explaining hidden states, backpropagation through time, and vanishing gradients with hands-on code. The ground-up construction makes abstract concepts concrete. For LSTM specifically, his CS231n lecture is the canonical reference.
- Level: intermediate

> [NOT VERIFIED] — Confirm this video ID maps to the makemore/RNN episode in the series. The broader "Neural Networks: Zero to Hero" playlist is well-established.

## Blog / Written explainer (best)
- **Christopher Olah** — "Understanding LSTM Networks"
- url: https://colah.github.io/posts/2015-08-Understanding-LSTMs/
- Why: The single most-cited pedagogical resource on LSTMs. Olah's diagrams of cell state, forget/input/output gates, and the comparison to vanilla RNNs are exceptionally clear. Covers vanishing gradients motivation and gating mechanisms in a visually intuitive way that textbooks rarely match.
- Level: beginner/intermediate

## Deep dive
- **Lilian Weng** — "Attention? Attention!"
- url: https://lilianweng.github.io/posts/2018-06-24-attention/
- Why: Covers the full arc from seq2seq bottleneck → Bahdanau attention → alignment scores → encoder-decoder attention in one comprehensive post. Includes mathematical derivations, architecture diagrams, and historical context. Bridges the LSTM/RNN foundation to the attention mechanism that superseded it, making it ideal for the full topic scope listed here.
- Level: intermediate/advanced

## Original paper
- **Hochreiter & Schmidhuber (1997)** — "Long Short-Term Memory"
- url: https://www.bioinf.jku.at/publications/older/2604.pdf
- Why: The foundational LSTM paper. While dense, it remains the definitive reference for the gating mechanism design rationale and the explicit treatment of the vanishing gradient problem. For Bahdanau attention specifically, the companion paper is below.

**Companion — Bahdanau et al. (2014)** — "Neural Machine Translation by Jointly Learning to Align and Translate"
- url: https://arxiv.org/abs/1409.0473
- Why: Introduces alignment scores and the attention mechanism over encoder hidden states — directly maps to the seq2seq bottleneck and encoder-decoder attention concepts in this topic. Highly readable for a research paper.

## Code walkthrough
- **Jay Alammar** — "Visualizing A Neural Machine Translation Model (Mechanics of Seq2seq Models With Attention)"
- url: https://jalammar.github.io/visualizing-neural-machine-translation-mechanics-of-seq2seq-models-with-attention/
- Why: Step-by-step animated walkthrough of a seq2seq model with Bahdanau-style attention, showing exactly how encoder hidden states are queried, how alignment scores are computed, and how the context vector is formed. Pairs naturally with Olah's LSTM post as a two-part reading sequence. Includes enough implementation detail to guide coding.
- Level: intermediate

> **Note:** For a pure code implementation, the PyTorch official tutorial "NLP From Scratch: Translation with a Sequence to Sequence Network and Attention" at https://pytorch.org/tutorials/intermediate/seq2seq_translation_tutorial.html is the best hands-on complement.

## Coverage notes
- **Strong:** LSTM gating mechanisms and cell state (Olah blog is definitive), Bahdanau attention and alignment scores (Weng + Alammar are excellent), seq2seq bottleneck motivation, original papers
- **Weak:** Dedicated video covering *all* related concepts (RNN → LSTM → seq2seq → attention) in a single resource without jumping between multiple videos
- **Gap:** No single YouTube video cleanly covers the full arc from vanishing gradients → LSTM → seq2seq bottleneck → Bahdanau attention in one sitting. Karpathy's series requires watching multiple episodes. StatQuest has individual LSTM videos but does not connect through to attention. A purpose-built video for this exact topic cluster would be valuable for the ml-engineering-foundations course.


> **[Structural note]** "Luong Attention and Scoring Function Variants" appears to have sub-concepts:
> multiplicative attention, global attention, local attention
> *Discovered during enrichment for course "Attention Mechanisms (pipeline test)" | 2026-04-07*


> **[Structural note]** "Luong Attention and Score Function Variants" appears to have sub-concepts:
> multiplicative attention, dot-product scoring, general attention, concat scoring, global vs local attention
> *Discovered during enrichment for course "Attention Mechanisms (pipeline test)" | 2026-04-07*


> **[Structural note]** "Luong Attention and Score Function Variants" appears to have sub-concepts:
> multiplicative attention, dot-product scoring, general scoring function, concat scoring function, global vs local attention, score normalization
> *Discovered during enrichment for course "Attention Mechanisms (pipeline test)" | 2026-04-07*


> **[Structural note]** "The Bottleneck Problem in Seq2Seq Models" appears to have sub-concepts:
> encoder-decoder architecture, fixed-length context vector, information bottleneck, recurrent neural networks, sequence-to-sequence learning
> *Discovered during enrichment for course "Attention Mechanisms (pipeline test)" | 2026-04-07*


> **[Structural note]** "Bahdanau (Additive) Attention: Formulation and Intuition" appears to have sub-concepts:
> additive attention, alignment model, decoder state, encoder hidden states, soft alignment
> *Discovered during enrichment for course "Attention Mechanisms (pipeline test)" | 2026-04-09*

## Last Verified
2026-04-06