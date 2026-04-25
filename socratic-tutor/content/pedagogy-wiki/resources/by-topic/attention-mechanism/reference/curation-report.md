# Curation Report: Attention Mechanism
**Topic:** `attention-mechanism` | **Date:** 2026-04-09 16:15
**Library:** 23 existing → 35 sources (12 added, 8 downloaded)
**Candidates evaluated:** 52
**Reviewer verdict:** needs_additions

## Added (12)
- **[paper]** [[PDF] FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning](https://tridao.me/publications/flash2/flash2.pdf)
  Gives the tutor citable, step-by-step kernel-level mechanics (tiling + stable softmax) that go beyond high-level summaries and directly answer “how does FlashAttention compute exact attention without O(n^2) memory?”
- **[benchmark]** [FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning](https://arxiv.org/abs/2307.08691)
  Provides authoritative performance numbers and comparisons suitable for quoting when students ask for concrete speed/memory improvements and how they vary with sequence length and attention mode.
- **[paper]** [Fast Transformer Decoding: One Write-Head is All You Need](https://arxiv.org/abs/1911.02150)
  Seminal, citable source for why sharing K/V works and what it buys in decoding, enabling the tutor to explain the compute/memory tradeoff and the inference-speed motivation.
- **[paper]** [GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints](https://aclanthology.org/2023.emnlp-main.298/)
  Adds the missing step-by-step explanation of GQA (how grouping is implemented and trained) and provides evidence about quality impact, which is crucial for teaching when/why to use GQA.
- **[reference_doc]** [torch.nn.functional.scaled_dot_product_attention](https://docs.pytorch.org/docs/stable/generated/torch.nn.functional.scaled_dot_product_attention.html)
  Lets the tutor quote exact API defaults and explain how PyTorch’s SDPA maps to attention math (including causal masking and optional scaling/GQA flag).
- **[paper]** [Efficient Memory Management for Large Language Model Serving with PagedAttention](https://arxiv.org/abs/2309.06180)
  Directly addresses production KV-cache deployment concerns (memory budgeting/fragmentation, batching constraints) with an OS-inspired design and measurable serving benefits.
- **[reference_doc]** [torch.nn.functional.scaled_dot_product_attention — PyTorch (stable docs)](https://docs.pytorch.org/docs/stable/generated/torch.nn.functional.scaled_dot_product_attention)
  The curator already added an SDPA reference doc, but this stable canonical page is the most citable/authoritative and should be included explicitly (forum threads/tutorial sources are secondary).
- **[explainer]** [Scaled Dot Product Attention tutorial (PyTorch tutorial source)](https://docs.pytorch.org/tutorials/_sources/intermediate/scaled_dot_product_attention_tutorial.rst.txt)
  Thin API docs give signatures, but this tutorial adds the missing “how to use it correctly” procedural context that prevents common student mistakes while still being official PyTorch material.
- **[paper]** [FlashAttention-3: Fast and Accurate Attention with Asynchrony and ...](https://arxiv.org/html/2407.08608v1)
  Even if FA-2 is the baseline for teaching the core online-softmax/tiling algorithm, FA-3 is a high-value empirical and architecture update that helps answer “what changed on H100 and why,” addressing the unfilled multi-GPU benchmark need.
- **[reference_doc]** [torch.nn.functional.scaled_dot_product_attention — PyTorch (stable docs)](https://docs.pytorch.org/docs/stable/generated/torch.nn.functional.scaled_dot_product_attention) *(promoted by reviewer)*
  The curator already added an SDPA reference doc, but this stable canonical page is the most citable/authoritative and should be included explicitly (forum threads/tutorial sources are secondary).
- **[explainer]** [Scaled Dot Product Attention tutorial (PyTorch tutorial source)](https://docs.pytorch.org/tutorials/_sources/intermediate/scaled_dot_product_attention_tutorial.rst.txt) *(promoted by reviewer)*
  Thin API docs give signatures, but this tutorial adds the missing “how to use it correctly” procedural context that prevents common student mistakes while still being official PyTorch material.
- **[paper]** [FlashAttention-3: Fast and Accurate Attention with Asynchrony and ...](https://arxiv.org/html/2407.08608v1) *(promoted by reviewer)*
  Even if FA-2 is the baseline for teaching the core online-softmax/tiling algorithm, FA-3 is a high-value empirical and architecture update that helps answer “what changed on H100 and why,” addressing the unfilled multi-GPU benchmark need.

## Near-Misses (4) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **[PDF] FlashAttention-3: Fast and Accurate Attention with Asy** — [[PDF] FlashAttention-3: Fast and Accurate Attention with Asynchrony and ...](https://tridao.me/publications/flash3/flash3.pdf)
  _Skipped because:_ Strong for newest kernels, but FlashAttention-2 is the more established baseline for teaching core tiling + online-softmax mechanics and widely cited benchmark comparisons.
- **FlashAttention-2: Faster Attention with Better Parallelism a** — [FlashAttention-2: Faster Attention with Better Parallelism and Work ...](https://crfm.stanford.edu/2023/07/17/flash2.html)
  _Skipped because:_ Useful narrative, but the paper/PDF is more authoritative and contains the formal algorithms and benchmark details needed for precise citation.
- **Multi-Head, Multi-Query, and Group-Query Attention — TensorR** — [Multi-Head, Multi-Query, and Group-Query Attention — TensorRT-LLM](https://nvidia.github.io/TensorRT-LLM/advanced/gpt-attention.html)
  _Skipped because:_ Excellent practical documentation, but it didn’t win a slot because the chosen set already covers GQA/MQA conceptually (papers) and deployment (vLLM); this would be the next add for stack-specific implementation details.
- **Introducing New KV Cache Reuse Optimizations in NVIDIA ...** — [Introducing New KV Cache Reuse Optimizations in NVIDIA ...](https://developer.nvidia.com/blog/introducing-new-kv-cache-reuse-optimizations-in-nvidia-tensorrt-llm/)
  _Skipped because:_ Good production-oriented discussion, but the vLLM/PagedAttention paper is a more canonical, citable systems reference with clearer algorithmic framing.

## Reasoning
**Curator:** Selections prioritize primary, citable sources that directly supply missing algorithmic specifics (FlashAttention-2), concrete performance data (FlashAttention-2 benchmarks), foundational and modern explanations for MQA/GQA (seminal decoding paper + EMNLP GQA), one official API reference (PyTorch SDPA), and one production-serving case study (PagedAttention/vLLM).
**Reviewer:** The curator’s core picks are strong (FA-2 + MQA/GQA + PagedAttention), but adding the canonical PyTorch SDPA docs/tutorial and FlashAttention-3 would materially improve API-citation reliability and multi-GPU benchmark coverage.

---

# Curation Report: Sequence-to-Sequence Basics and the Bottleneck Problem
**Topic:** `attention-mechanism` | **Date:** 2026-04-11 17:38
**Library:** 31 existing → 44 sources (13 added, 8 downloaded)
**Candidates evaluated:** 45
**Reviewer verdict:** needs_additions

## Added (13)
- **[paper]** [Learning Phrase Representations using RNN Encoder-Decoder for Statistical Machine Translation](https://arxiv.org/abs/1406.1078)
  This is the original RNN encoder–decoder formulation with explicit probabilistic objective and conditioning structure that underlies teacher forcing in practice.
- **[benchmark]** [Neural Machine Translation by Jointly Learning to Align and Translate](https://arxiv.org/pdf/1409.0473.pdf)
  This paper both names the fixed-vector bottleneck and provides quantitative evidence (length-based analysis) that attention mitigates it.
- **[explainer]** [Neural Machine Translation (Cho & van Merrienboer tutorial/demo notes)](https://cs224d.stanford.edu/papers/nmt.pdf)
  Provides an authoritative, pedagogical walkthrough of classic encoder–decoder NMT that a tutor can mirror when explaining training/inference flow and the origin of the bottleneck.
- **[reference_doc]** [GRU — PyTorch 2.11 documentation](https://docs.pytorch.org/docs/stable/generated/torch.nn.GRU.html)
  Gives citable framework-level specifics that affect seq2seq implementations (state shapes, dropout behavior, bidirectionality), which are often the source of student confusion.
- **[paper]** [Google's Neural Machine Translation System: Bridging the Gap between Human and Machine Translation](https://arxiv.org/pdf/1609.08144.pdf)
  Adds a structured, engineering-focused view of how the community mitigated the bottleneck and scaled RNN seq2seq, including practical tradeoffs beyond just BLEU.
- **[paper]** [Learning Phrase Representations using RNN Encoder–Decoder for Statistical Machine Translation (Cho et al., 2014)](https://aclanthology.org/D14-1179/)
  The arXiv link in the library is ambiguous (“arxiv-abs-1409-0473”) and the ACL Anthology version is the stable, citable canonical record; it directly supports the missing ‘teacher forcing’/MLE formulation with explicit notation.
- **[reference_doc]** [torch.nn.GRU — PyTorch documentation](http://docs.pytorch.org/docs/stable/generated/torch.nn.GRU.html)
  The curator’s chosen GRU doc URL points to a quantized/dynamic variant; the canonical torch.nn.GRU page is the authoritative reference students will actually use and cite for shape/default confusion.
- **[reference_doc]** [torch.nn.Transformer — PyTorch documentation](https://docs.pytorch.org/docs/stable/generated/torch.nn.Transformer.html)
  Even if the lesson centers on seq2seq basics, students commonly implement the ‘attention fixes the bottleneck’ story via Transformer modules; thin official docs are exactly what’s needed for exact defaults and tensor/mask semantics.
- **[reference_doc]** [NLP From Scratch: Translation with a Sequence to Sequence Network and Attention (PyTorch tutorial)](https://docs.pytorch.org/tutorials/intermediate/seq2seq_translation_tutorial.html)
  This is already in the library but it directly fills the unfilled ‘teacher_forcing_ratio behavior’ need; it should be explicitly tagged/used as the canonical procedural reference for teacher forcing in PyTorch.
- **[paper]** [Learning Phrase Representations using RNN Encoder–Decoder for Statistical Machine Translation (Cho et al., 2014)](https://aclanthology.org/D14-1179/) *(promoted by reviewer)*
  The arXiv link in the library is ambiguous (“arxiv-abs-1409-0473”) and the ACL Anthology version is the stable, citable canonical record; it directly supports the missing ‘teacher forcing’/MLE formulation with explicit notation.
- **[reference_doc]** [torch.nn.GRU — PyTorch documentation](http://docs.pytorch.org/docs/stable/generated/torch.nn.GRU.html) *(promoted by reviewer)*
  The curator’s chosen GRU doc URL points to a quantized/dynamic variant; the canonical torch.nn.GRU page is the authoritative reference students will actually use and cite for shape/default confusion.
- **[reference_doc]** [torch.nn.Transformer — PyTorch documentation](https://docs.pytorch.org/docs/stable/generated/torch.nn.Transformer.html) *(promoted by reviewer)*
  Even if the lesson centers on seq2seq basics, students commonly implement the ‘attention fixes the bottleneck’ story via Transformer modules; thin official docs are exactly what’s needed for exact defaults and tensor/mask semantics.
- **[reference_doc]** [NLP From Scratch: Translation with a Sequence to Sequence Network and Attention (PyTorch tutorial)](https://docs.pytorch.org/tutorials/intermediate/seq2seq_translation_tutorial.html) *(promoted by reviewer)*
  This is already in the library but it directly fills the unfilled ‘teacher_forcing_ratio behavior’ need; it should be explicitly tagged/used as the canonical procedural reference for teacher forcing in PyTorch.

## Near-Misses (4) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **Learning Phrase Representations using RNN Encoder-Decoder fo** — [Learning Phrase Representations using RNN Encoder-Decoder for Statistical Machine Translation](https://aclanthology.org/D14-1179.pdf)
  _Skipped because:_ Redundant with the arXiv version; kept only one canonical copy.
- **Effective Approaches to Attention-based Neural Machine Trans** — [Effective Approaches to Attention-based Neural Machine Translation](https://aclanthology.org/D15-1166/)
  _Skipped because:_ Already present in the existing library (Luong et al., 2015), so it doesn’t add new coverage here.
- **arXiv:1409.1259v2 [cs.CL] 7 Oct 2014** — [arXiv:1409.1259v2 [cs.CL] 7 Oct 2014](https://arxiv.org/pdf/1409.1259.pdf)
  _Skipped because:_ Overlaps heavily with the cs224d NMT notes; selected the more directly reusable tutorial-style version.
- **Last hidden state in bidirectional stacked GRU - nlp - PyTor** — [Last hidden state in bidirectional stacked GRU - nlp - PyTorch Forums](https://discuss.pytorch.org/t/last-hidden-state-in-bidirectional-stacked-gru/57971)
  _Skipped because:_ Useful implementation clarification but not an authoritative API reference compared to official docs.

## Reasoning
**Curator:** Selections prioritize primary sources and official docs that directly supply (1) citable equations/objectives, (2) length-based bottleneck evidence, (3) an authoritative pipeline explanation, (4) framework defaults/shapes, and (5) system-level tradeoff discussion for pre-Transformer bottleneck mitigations.
**Reviewer:** The core paper coverage is strong, but the library should add the canonical ACL Anthology record for Cho et al. (for explicit MLE/teacher-forcing notation) and the canonical PyTorch GRU/Transformer docs (plus explicitly leverage the existing PyTorch seq2seq tutorial) to satisfy the missing API- and procedure-level needs.

---

# Curation Report: Sequence-to-Sequence Basics and the Bottleneck Problem
**Topic:** `attention-mechanism` | **Date:** 2026-04-11 18:03
**Library:** 35 existing → 51 sources (16 added, 9 downloaded)
**Candidates evaluated:** 45
**Reviewer verdict:** needs_additions

## Added (16)
- **[paper]** [Sequence to Sequence Learning with Neural Networks (Sutskever, Vinyals, Le, 2014)](https://arxiv.org/pdf/1409.3215v3.pdf)
  This is the canonical fixed-vector encoder–decoder formulation with the exact probabilistic factorization and training objective needed for precise quoting and derivations.
- **[benchmark]** [Neural Machine Translation by Jointly Learning to Align and Translate (Bahdanau, Cho, Bengio, 2014/2015)](https://arxiv.org/pdf/1409.0473.pdf)
  Provides the most direct quantitative evidence for the fixed-length context bottleneck and demonstrates how attention mitigates it, with citable length-based comparisons.
- **[paper]** [Scheduled Sampling for Sequence Prediction with Recurrent Neural Networks (Bengio et al., NeurIPS 2015)](https://proceedings.neurips.cc/paper/2015/file/e995f98d56967d946471af29d7bf99f1-Paper.pdf)
  Gives an authoritative, procedural account of how training differs from inference in seq2seq and a concrete mitigation strategy the tutor can explain and reference.
- **[reference_doc]** [LSTM — PyTorch documentation (stable)](https://docs.pytorch.org/docs/stable/generated/torch.nn.LSTM.html)
  Official, citable API details let the tutor answer precise questions about LSTM defaults and what dropout/bidirectionality actually do in common seq2seq implementations.
- **[benchmark]** [Effective Approaches to Attention-based Neural Machine Translation (Luong, Pham, Manning, 2015)](https://arxiv.org/pdf/1508.04025.pdf)
  Adds a clear pre-Transformer comparison of attention variants with concrete criteria and results, useful for teaching alternatives to the single-vector bottleneck.
- **[paper]** [Google's Neural Machine Translation System: Bridging the Gap between Human and Machine Translation (Wu et al., 2016)](https://arxiv.org/abs/1609.08144)
  Provides an authoritative system-level comparison point showing how depth/residuals/bidirectionality/attention and decoding choices were combined to improve long-sequence behavior.
- **[paper]** [Learning Phrase Representations using RNN Encoder-Decoder for Statistical Machine Translation](https://arxiv.org/abs/1406.1078)
  This is a seminal pre-attention encoder–decoder paper whose value is in the full text (equations + training procedure), not the abstract; it strengthens the “fixed-vector bottleneck” narrative with primary-source math.
- **[reference_doc]** [torch.nn.utils.rnn.pack_padded_sequence — PyTorch (stable)](https://pytorch.org/docs/stable/generated/torch.nn.utils.rnn.pack_padded_sequence.html)
  The unfilled need explicitly calls out masking/packed sequences; this is the canonical, citable PyTorch reference that replaces tutorial-level guidance with precise defaults and constraints.
- **[reference_doc]** [torch.nn.utils.rnn.pad_packed_sequence — PyTorch (stable)](https://pytorch.org/docs/stable/generated/torch.nn.utils.rnn.pad_packed_sequence.html)
  Pack/unpack is a paired API; having only one leaves gaps when teaching how to implement seq2seq encoders with padding and then feed outputs into attention.
- **[reference_doc]** [torch.nn.utils.rnn.pad_sequence — PyTorch (stable)](https://pytorch.org/docs/stable/generated/torch.nn.utils.rnn.pad_sequence.html)
  Thin but essential: it provides exact parameter names/defaults for a ubiquitous seq2seq preprocessing step that otherwise gets explained inconsistently across tutorials.
- **[reference_doc]** [tf.keras.layers.LSTM — TensorFlow API docs (current)](https://www.tensorflow.org/api_docs/python/tf/keras/layers/LSTM)
  The library currently anchors LSTM behavior only in PyTorch; adding the official Keras LSTM reference covers a major framework and directly addresses the “official docs for defaults/behaviors” requirement.
- **[paper]** [Learning Phrase Representations using RNN Encoder-Decoder for Statistical Machine Translation](https://arxiv.org/abs/1406.1078) *(promoted by reviewer)*
  This is a seminal pre-attention encoder–decoder paper whose value is in the full text (equations + training procedure), not the abstract; it strengthens the “fixed-vector bottleneck” narrative with primary-source math.
- **[reference_doc]** [torch.nn.utils.rnn.pack_padded_sequence — PyTorch (stable)](https://pytorch.org/docs/stable/generated/torch.nn.utils.rnn.pack_padded_sequence.html) *(promoted by reviewer)*
  The unfilled need explicitly calls out masking/packed sequences; this is the canonical, citable PyTorch reference that replaces tutorial-level guidance with precise defaults and constraints.
- **[reference_doc]** [torch.nn.utils.rnn.pad_packed_sequence — PyTorch (stable)](https://pytorch.org/docs/stable/generated/torch.nn.utils.rnn.pad_packed_sequence.html) *(promoted by reviewer)*
  Pack/unpack is a paired API; having only one leaves gaps when teaching how to implement seq2seq encoders with padding and then feed outputs into attention.
- **[reference_doc]** [torch.nn.utils.rnn.pad_sequence — PyTorch (stable)](https://pytorch.org/docs/stable/generated/torch.nn.utils.rnn.pad_sequence.html) *(promoted by reviewer)*
  Thin but essential: it provides exact parameter names/defaults for a ubiquitous seq2seq preprocessing step that otherwise gets explained inconsistently across tutorials.
- **[reference_doc]** [tf.keras.layers.LSTM — TensorFlow API docs (current)](https://www.tensorflow.org/api_docs/python/tf/keras/layers/LSTM) *(promoted by reviewer)*
  The library currently anchors LSTM behavior only in PyTorch; adding the official Keras LSTM reference covers a major framework and directly addresses the “official docs for defaults/behaviors” requirement.

## Near-Misses (3) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **LSTM — PyTorch 2.11 documentation (modules.rnn path)** — [LSTM — PyTorch 2.11 documentation (modules.rnn path)](https://docs.pytorch.org/docs/stable/generated/torch.nn.modules.rnn.LSTM.html)
  _Skipped because:_ Substantially duplicates the stable torch.nn.LSTM reference; keeping one canonical doc avoids redundancy.
- **Dropout in LSTM (PyTorch Forums thread)** — [Dropout in LSTM (PyTorch Forums thread)](https://discuss.pytorch.org/t/dropout-in-lstm/7784)
  _Skipped because:_ Useful clarifications, but it is not official documentation and is less citable than the API reference.
- **Effective Approaches to Attention-based Neural Machine Trans** — [Effective Approaches to Attention-based Neural Machine Translation (ACL Anthology landing page)](https://aclanthology.org/D15-1166/)
  _Skipped because:_ Landing page is less directly useful than the PDF for extracting equations, tables, and exact experimental details.

## Reasoning
**Curator:** Selections prioritize primary sources that (1) define the fixed-vector seq2seq objective and equations, (2) empirically demonstrate the long-sequence bottleneck with length-stratified results, (3) document training/inference mismatch and mitigation, and (4) provide official API defaults plus pre-Transformer architectural comparisons with concrete tradeoffs.
**Reviewer:** The core paper/benchmark choices are strong, but the library should add at least one seminal pre-attention encoder–decoder math source (Cho et al. 2014) and official framework docs for variable-length masking/packing (and optionally Keras LSTM) to fully cover the remaining API-reference gaps.

---

# Curation Report: Sequence-to-Sequence Basics and the Bottleneck Problem
**Topic:** `attention-mechanism` | **Date:** 2026-04-11 19:41
**Library:** 37 existing → 46 sources (9 added, 7 downloaded)
**Candidates evaluated:** 35
**Reviewer verdict:** needs_additions

## Added (9)
- **[paper]** [Scheduled Sampling for Sequence Prediction with Recurrent Neural Networks](https://arxiv.org/abs/1506.03099)
  This is the primary source that precisely defines how teacher forcing is relaxed by mixing ground-truth and model predictions during decoding, including explicit schedules and training procedure details.
- **[paper]** [SEQUENCE LEVEL TRAINING WITH RECURRENT NEURAL NETWORKS](https://michaelauli.github.io/papers/iclr2016_mixer.pdf)
  Gives a formal, commonly cited treatment of exposure bias and a concrete sequence-level alternative with derivations and a step-by-step training recipe.
- **[paper]** [Neural Machine Translation by Jointly Learning to Align and Translate](https://www.arxiv.org/pdf/1409.0473v2.pdf)
  This seminal attention paper explicitly motivates and evidences the fixed-size context bottleneck with controlled comparisons against a non-attention encoder–decoder, including results broken down by sentence length.
- **[paper]** [Effective Approaches to Attention-based Neural Machine Translation](https://aclanthology.org/D15-1166/)
  Provides the most authoritative structured comparison among classic seq2seq attention scoring functions and variants, with clear formulas and empirical results used widely for teaching tradeoffs.
- **[reference_doc]** [TransformersWrapper — torchrl main documentation](https://docs.pytorch.org/rl/main/reference/generated/torchrl.modules.llm.TransformersWrapper.html)
  Adds an official, citable API surface for decoding controls that affect exposure-bias-relevant behavior at inference (greedy vs sampling vs beam search) with precise parameter meanings.
- **[paper]** [Autoregressive Knowledge Distillation through Imitation Learning](https://aclanthology.org/2020.emnlp-main.494.pdf)
  This directly targets the still-unfilled “DAgger-style” exposure-bias need with a concrete, citable algorithmic procedure and math, rather than another general exposure-bias discussion.
- **[reference_doc]** [Hugging Face Transformers — Text generation API (Generation)](https://huggingface.co/docs/transformers/main_classes/text_generation)
  Thin but authoritative API documentation is exactly what’s needed for precise decoding/beam-search semantics; it also aligns with the curator’s stated goal of citing standardized decoding knobs.
- **[paper]** [Autoregressive Knowledge Distillation through Imitation Learning](https://aclanthology.org/2020.emnlp-main.494.pdf) *(promoted by reviewer)*
  This directly targets the still-unfilled “DAgger-style” exposure-bias need with a concrete, citable algorithmic procedure and math, rather than another general exposure-bias discussion.
- **[reference_doc]** [Hugging Face Transformers — Text generation API (Generation)](https://huggingface.co/docs/transformers/main_classes/text_generation) *(promoted by reviewer)*
  Thin but authoritative API documentation is exactly what’s needed for precise decoding/beam-search semantics; it also aligns with the curator’s stated goal of citing standardized decoding knobs.

## Near-Misses (6) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **TransformersWrapper — torchrl 0.0 documentation - PyTorch** — [TransformersWrapper — torchrl 0.0 documentation - PyTorch](https://docs.pytorch.org/rl/stable/reference/generated/torchrl.modules.llm.TransformersWrapper.html)
  _Skipped because:_ Redundant with the main (newer) TorchRL documentation; kept only one authoritative version.
- **arXiv:1508.04025v5  [cs.CL]  20 Sep 2015** — [arXiv:1508.04025v5  [cs.CL]  20 Sep 2015](http://arxiv.org/pdf/1508.04025v5.pdf)
  _Skipped because:_ Same Luong et al. paper as the ACL Anthology entry; preferred the canonical Anthology landing page.
- **Effective Approaches to Attention-based Neural Machine ...** — [Effective Approaches to Attention-based Neural Machine ...](https://nlp.stanford.edu/pubs/emnlp15_attn.pdf)
  _Skipped because:_ Alternate PDF host for the same paper; the ACL Anthology record is more stable and citable.
- **Effective Approaches To Attention Based Neural Machine Trans** — [Effective Approaches To Attention Based Neural Machine Translation - Paper Explained](https://www.youtube.com/watch?v=Fbn2DWlHRt4)
  _Skipped because:_ Not an authoritative primary source and unlikely to contain the precise formulas/benchmark tables needed for citation.
- **4. Bahdanau Attention** — [4. Bahdanau Attention](https://www.baeldung.com/cs/attention-luong-vs-bahdanau)
  _Skipped because:_ Secondary explainer; less precise and citable than the original papers for formulas and empirical comparisons.
- **Effective Approaches to Attention-based Neural Machine ...** — [Effective Approaches to Attention-based Neural Machine ...](https://aclanthology.org/anthology-files/pdf/D/D15/D15-1166.pdf)
  _Skipped because:_ Direct PDF for the same Luong et al. paper; kept the Anthology landing page as the single reference.

## Reasoning
**Curator:** Selections prioritize primary/official sources that contain explicit algorithms, equations, and empirical comparisons directly tied to seq2seq bottlenecks and exposure bias, plus at least one official API reference for decoding controls. Redundant hosts and non-authoritative explainers were excluded to keep the library small and citable.
**Reviewer:** The core seq2seq/attention/bottleneck coverage is strong, but the library still benefits from adding one DAgger-style exposure-bias formula source and one authoritative generation/beam-search API reference.
