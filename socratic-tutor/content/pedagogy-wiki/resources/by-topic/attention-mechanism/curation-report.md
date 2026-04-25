# Curation Report: Attention as Differentiable Retrieval: Queries, Keys, Values
**Topic:** `attention-mechanism` | **Date:** 2026-04-08 01:17
**Library:** 10 existing → 14 sources (4 added, 3 downloaded)
**Candidates evaluated:** 18
**Reviewer verdict:** needs_additions

## Added (4)
- **[tutorial]** [11.1. Queries, Keys, and Values - Dive into Deep Learning](https://d2l.ai/chapter_attention-mechanisms-and-transformers/queries-keys-values.html)
  Adds an explicit, database-style framing of attention as querying a set of (key, value) pairs, with clear definitions of what keys do relative to queries and how values are retrieved via softmax weights—more direct than the current library’s mostly transformer-focused intuition pieces.
   — covers: Explicit definition and role of keys in attention (what keys represent and how they are used with queries), Attention as differentiable retrieval/lookup: interpreting keys as addresses, values as stored content, and softmax weights as differentiable read weights, Explicit formulation of attention output as a weighted sum over values (alpha = softmax(sim(q,k)); output = Σ alpha_i v_i) with a worked example
- **[tutorial]** [Scaled Dot Product Attention](https://jaykmody.com/blog/attention-intuition/)
  Provides a compact, math-forward walkthrough of scaled dot-product attention that makes the weighted-sum-over-values computation concrete, complementing the more narrative/visual explanations already in the library.
   — covers: Explicit formulation of attention output as a weighted sum over values (alpha = softmax(sim(q,k)); output = Σ alpha_i v_i) with a worked example, Attention as differentiable retrieval/lookup: interpreting keys as addresses, values as stored content, and softmax weights as differentiable read weights
- **[paper]** [Key-Value Memory Networks for Directly Reading Documents](https://ar5iv.labs.arxiv.org/html/1606.03126)
  This is the canonical ML paper that explicitly formalizes key-value memory access as attention-style differentiable retrieval, directly connecting Q/K/V intuition to memory networks rather than just Transformers.
   — covers: Connection to memory networks / key-value memory networks and how attention implements differentiable memory access
- **[paper]** [Key-Value Memory Networks for Directly Reading Documents](https://ar5iv.labs.arxiv.org/html/1606.03126) *(promoted by reviewer)*
  This is the canonical ML paper that explicitly formalizes key-value memory access as attention-style differentiable retrieval, directly connecting Q/K/V intuition to memory networks rather than just Transformers.
   — fills: Connection to memory networks / key-value memory networks and how attention implements differentiable memory access

## Near-Misses (6) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **Keys, Queries, and Values: The celestial mechanics of attent** — [Keys, Queries, and Values: The celestial mechanics of attention](https://www.youtube.com/watch?v=RFdb2rKAqFw)
  _Skipped because:_ Potentially good intuition, but video-only and harder to cite/skim than the stronger, stable D2L chapter already added for the same conceptual ground.
- **What is Query, Key, and Value (QKV) in the Transformer Archi** — [What is Query, Key, and Value (QKV) in the Transformer Architecture ...](https://epichka.com/blog/2023/qkv-transformer/)
  _Skipped because:_ Appears redundant with existing QKV explainers and overlaps heavily with the added D2L chapter without clear additional depth or authority.
- **Chapter 8 Attention and Self-Attention for NLP** — [Chapter 8 Attention and Self-Attention for NLP](https://slds-lmu.github.io/seminar_nlp_ss20/attention-and-self-attention-for-nlp.html)
  _Skipped because:_ Likely solid lecture notes, but overlaps with D2L/Jalammar/Weng coverage and is less canonical/stable than D2L for the same material.
- **[2501.02950] Key-value memory in the brain - ar5iv - arXiv** — [[2501.02950] Key-value memory in the brain - ar5iv - arXiv](https://ar5iv.labs.arxiv.org/html/2501.02950)
  _Skipped because:_ High-quality but focused on neuroscience/computational memory rather than explaining memory networks/key-value memory in the ML sense (e.g., KVMemNN), so it doesn’t directly fill the library’s memory-network connection gap.
- **[PDF] Key-value memory in the brain - Gershman Lab** — [[PDF] Key-value memory in the brain - Gershman Lab](https://gershmanlab.com/pubs/GershmanFieteIrie25.pdf)
  _Skipped because:_ Authoritative review, but its emphasis is biological key-value memory; it does not concretely connect to memory networks / key-value memory networks implementations in deep learning as requested.
- **Differentiable Window for Dynamic Local Attention** — [Differentiable Window for Dynamic Local Attention](http://arxiv.org/pdf/2006.13561.pdf)
  _Skipped because:_ Research on a specific attention variant; too specialized for the conceptual gaps (keys/values as retrieval and key-value memory networks) and not the best use of limited shelf space.

## Uncovered Gaps (1) — No Good Candidates Found
_Consider manually sourcing these, or run enrichment again with different search terms._

- Connection to memory networks / key-value memory networks and how attention implements differentiable memory access

## Reasoning
**Curator:** The additions prioritize authoritative, stable explanations that directly formalize Q/K/V roles and attention as differentiable retrieval with explicit equations and examples; candidates that were redundant, less stable, or off-target (neuroscience/specialized variants) were excluded.
**Reviewer:** The library is strong on Transformer/QKV intuition and standard attention math, but it still needs at least one seminal key-value memory networks paper to close the stated memory-network connection gap.

---

# Curation Report: From Encoder–Decoder Bottlenecks to Attention
**Topic:** `attention-mechanism` | **Date:** 2026-04-08 01:19
**Library:** 13 existing → 15 sources (2 added, 0 downloaded, 2 failed)
**Candidates evaluated:** 14
**Reviewer verdict:** good

## Added (2)
- **[reference_doc]** [CS224n: Natural Language Processing with Deep Learning — Lecture Notes: Part VI Neural Machine Translation, Seq2seq and Attention](https://web.stanford.edu/class/cs224n/readings/cs224n-2019-notes06-NMT_seq2seq_attention.pdf)
  Gives a clear, step-by-step definition of the classic seq2seq context vector (encoder final state) and how the decoder conditions on it, then motivates and derives attention as a per-time-step context computed from alignment weights over encoder states.
   — covers: Explicit definition and role of the seq2seq 'context vector' (how it is computed in classic encoder-decoder RNNs and how the decoder conditions on it at each step), Detailed explanation of the fixed-length context 'information bottleneck' in classic seq2seq (why it limits performance, especially on long sequences; typical failure modes/intuition and/or evidence), Mechanics of alignment in attention-based NMT (alignment scores/weights, soft alignment vs hard alignment, how per-target-step context is computed as a weighted sum of encoder hidden states, worked example/visualization)
- **[paper]** [Effective Approaches to Attention-based Neural Machine Translation](https://nlp.stanford.edu/pubs/emnlp15_attn.pdf)
  Seminal, highly-cited NMT attention paper that precisely formalizes alignment scores/weights and the per-decoder-step context vector, with concrete architectural variants (global/local attention) that deepen the library’s treatment of alignment mechanics beyond high-level tutorials.
   — covers: Mechanics of alignment in attention-based NMT (alignment scores/weights, soft alignment vs hard alignment, how per-target-step context is computed as a weighted sum of encoder hidden states, worked example/visualization)

## Near-Misses (11) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **Seq2seq - Wikipedia** — [Seq2seq - Wikipedia](https://en.wikipedia.org/wiki/Seq2seq)
  _Skipped because:_ Covers the terms but is not consistently deep or stable enough pedagogically compared to CS224n/D2L, and risks redundancy.
- **Encoder-Decoder Framework: Seq2Seq Architecture for ...** — [Encoder-Decoder Framework: Seq2Seq Architecture for ...](https://mbrenndoerfer.com/writing/encoder-decoder-framework-seq2seq-architecture-machine-translation)
  _Skipped because:_ Likely a decent blog-level overview, but overlaps with existing D2L/PyTorch/Jalammar resources and is less authoritative than CS224n notes.
- **[PDF] Sequence-to-Sequence Modeling with Encoder-Decoder Arc** — [[PDF] Sequence-to-Sequence Modeling with Encoder-Decoder Architectures](https://swabhs.com/f24-csci544-appliednlp/assets/slides/24f-csci544-appliednlp-lec10-seq2seq.pdf)
  _Skipped because:_ Course slides can be useful but are typically terse and less self-contained than CS224n notes for the specific gaps.
- **5.3 Why Lstm Also Has...** — [5.3 Why Lstm Also Has...](https://blog.sotaaz.com/post/context-vector-limitation-en)
  _Skipped because:_ Targets the bottleneck gap, but appears to be an unvetted blog with unclear provenance; the library already has stronger, more reputable sources to build from.
- **[PDF] Neural Machine Translation Model (Seq2seq Models With ** — [[PDF] Neural Machine Translation Model (Seq2seq Models With Attention)](https://bimsa.net/doc/notes/27196.pdf)
  _Skipped because:_ Unclear authorship/authority and stability; overlaps with CS224n/D2L without offering a clearly superior treatment.
- **Challenges in Sequence-to-Sequence Tasks** — [Challenges in Sequence-to-Sequence Tasks](https://apxml.com/courses/introduction-to-transformer-models/chapter-1-sequence-modeling-attention-fundamentals/sequence-to-sequence-challenges)
  _Skipped because:_ Redundant with an existing apxml entry already in the library (same topic/site) and thus unlikely to add distinct value.
- **Sequence-to-Sequence Task Challenges** — [Sequence-to-Sequence Task Challenges](https://www.apxml.com/courses/introduction-to-transformer-models/chapter-1-sequence-modeling-attention-fundamentals/sequence-to-sequence-challenges)
  _Skipped because:_ Duplicate of the apxml challenges page and redundant with existing apxml coverage in the library.
- **Effective Approaches to Attention-based Neural Machine Trans** — [Effective Approaches to Attention-based Neural Machine Translation (arXiv mirror)](https://arxiv.org/pdf/1507.01053.pdf)
  _Skipped because:_ Same paper as the Stanford-hosted PDF; kept only one canonical, stable copy to avoid duplication.
- **Generating Alignments Using Target Foresight in Attention-Ba** — [Generating Alignments Using Target Foresight in Attention-Based Neural Machine Translation](https://ufal.mff.cuni.cz/pbml/108/art-peter-nix-ney.pdf)
  _Skipped because:_ Interesting specialized alignment work, but too niche for filling the core conceptual gaps compared to adding the foundational Luong et al. paper.
- **[PDF] Investigating alignment interpretability for low-resou** — [[PDF] Investigating alignment interpretability for low-resource NMT](https://eprints.whiterose.ac.uk/id/eprint/166668/1/MTJ_2020.pdf)
  _Skipped because:_ Focuses on interpretability/low-resource nuances rather than teaching the baseline alignment mechanics needed for this lesson.
- **Generating Alignments Using Target Foresight in Attention- .** — [Generating Alignments Using Target Foresight in Attention- ...](https://d-nb.info/1196210853/34)
  _Skipped because:_ Appears to be an alternate host/record for the same niche alignment work; not necessary for the core lesson.

## Reasoning
**Curator:** The CS224n NMT+attention notes are the single best candidate to directly and authoritatively address all three gaps in a cohesive narrative, while Luong et al. (2015) adds a seminal, formal treatment of alignment/context computation that complements the existing tutorial-heavy library without being redundant.
**Reviewer:** The curator’s additions (CS224n notes + Luong et al.) already cover the key bottleneck-to-attention narrative with authoritative and seminal sources, and none of the listed near-misses/remaining candidates clearly add unique, higher-value coverage beyond what’s already in the library.

---

# Curation Report: Bahdanau (Additive) Attention: Formulation and Intuition
**Topic:** `attention-mechanism` | **Date:** 2026-04-08 01:22
**Library:** 13 existing → 21 sources (8 added, 5 downloaded)
**Candidates evaluated:** 21
**Reviewer verdict:** needs_additions

## Added (8)
- **[tutorial]** [11.4. The Bahdanau Attention Mechanism - Dive into Deep Learning](https://d2l.ai/chapter_attention-mechanisms-and-transformers/bahdanau-attention.html)
  Directly and systematically derives Bahdanau/additive attention with the classic MLP+tanh energy function, softmax alignment weights, and context-vector computation in an encoder-decoder RNN setting—exactly the missing formulation details.
   — covers: Bahdanau (additive) attention formulation with equations: energy/score function using an MLP (tanh) over decoder state and encoder hidden states, Definition and computation of alignment scores e_{t,i} and attention weights alpha_{t,i} for RNN seq2seq, Context vector computation c_t as a weighted sum of encoder hidden states and how it feeds into the decoder, Role of the RNN decoder hidden state (s_{t-1} or s_t) as the query in additive attention
- **[tutorial]** [Seq2seq and Attention](https://lena-voita.github.io/nlp_course/seq2seq_and_attention.html)
  Provides a clear seq2seq-to-attention narrative with explicit alignment/weight equations and strong intuition for soft alignment and the fixed-length bottleneck, complementing the more implementation/textbook-style sources already in the library.
   — covers: Definition and computation of alignment scores e_{t,i} and attention weights alpha_{t,i} for RNN seq2seq, Context vector computation c_t as a weighted sum of encoder hidden states and how it feeds into the decoder, Intuition for soft alignment vs hard alignment and how attention mitigates the fixed-length bottleneck / improves long-range dependencies
- **[paper]** [Effective Approaches to Attention-based Neural Machine Translation (Luong et al., 2015)](https://arxiv.org/abs/1508.04025)
  A second canonical early attention paper that cleanly contrasts global vs local attention and gives alternative scoring functions (dot/general/concat) that help students situate Bahdanau’s additive form among the standard variants.
- **[paper]** [Neural Machine Translation by Jointly Learning to Align and Translate (Bahdanau et al., 2014/2015)](https://arxiv.org/abs/1412.7449)
  The library currently lists arxiv:1409.0473 (seq2seq without attention); the actual Bahdanau attention paper is 1412.7449 and is the primary source for the additive energy function, alignment interpretation, and the fixed-length bottleneck motivation.
- **[tutorial]** [Engineering AI Agents — RNN NMT + Attention (lecture notes)](https://pantelis.github.io/aiml-common/lectures/nlp/nmt/rnn-nmt-attention/index.html)
  If you want a second, stable set of equation-level notes beyond D2L, these are clear and structured, and they explicitly walk through the query/decoder-state role and the context-vector pipeline in an RNN NMT setting.
- **[paper]** [Effective Approaches to Attention-based Neural Machine Translation (Luong et al., 2015)](https://arxiv.org/abs/1508.04025) *(promoted by reviewer)*
  A second canonical early attention paper that cleanly contrasts global vs local attention and gives alternative scoring functions (dot/general/concat) that help students situate Bahdanau’s additive form among the standard variants.
- **[paper]** [Neural Machine Translation by Jointly Learning to Align and Translate (Bahdanau et al., 2014/2015)](https://arxiv.org/abs/1412.7449) *(promoted by reviewer)*
  The library currently lists arxiv:1409.0473 (seq2seq without attention); the actual Bahdanau attention paper is 1412.7449 and is the primary source for the additive energy function, alignment interpretation, and the fixed-length bottleneck motivation.
- **[tutorial]** [Engineering AI Agents — RNN NMT + Attention (lecture notes)](https://pantelis.github.io/aiml-common/lectures/nlp/nmt/rnn-nmt-attention/index.html) *(promoted by reviewer)*
  If you want a second, stable set of equation-level notes beyond D2L, these are clear and structured, and they explicitly walk through the query/decoder-state role and the context-vector pipeline in an RNN NMT setting.

## Near-Misses (13) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **[PDF] Encoder‐Decoder Models and Attention** — [[PDF] Encoder‐Decoder Models and Attention](https://www1.se.cuhk.edu.hk/~seem5680/lecture/Encoder-Decoder-Attention-2022spring.pdf)
  _Skipped because:_ Likely solid lecture slides, but overlaps heavily with the added D2L chapter and is less canonical/stable for long-term wiki curation.
- **Attention in RNN-based NMT - Introduction** — [Attention in RNN-based NMT - Introduction](https://pantelis.github.io/aiml-common/lectures/nlp/nmt/rnn-nmt-attention/)
  _Skipped because:_ Appears to mirror the CUHK slide content and doesn’t clearly add unique depth beyond the D2L and Voita resources.
- **Bahdanau Attention: Dynamic Context for Neural Machine Trans** — [Bahdanau Attention: Dynamic Context for Neural Machine Translation](https://mbrenndoerfer.com/writing/bahdanau-attention-neural-machine-translation)
  _Skipped because:_ Good explanatory blog, but largely redundant once the authoritative D2L Bahdanau chapter is included.
- **[PDF] Deep Learning - Gilles Louppe** — [[PDF] Deep Learning - Gilles Louppe](https://glouppe.github.io/info8010-deep-learning/pdf/lec7.pdf)
  _Skipped because:_ High-quality slides, but as a broad lecture deck it’s less focused on the specific Bahdanau e_{t,i}/alpha_{t,i}/c_t pipeline than the chosen additions.
- **Chapter 8 Attention and Self-Attention for NLP** — [Chapter 8 Attention and Self-Attention for NLP](https://slds-lmu.github.io/seminar_nlp_ss20/attention-and-self-attention-for-nlp.html)
  _Skipped because:_ Potentially useful, but likely overlaps with existing general attention coverage (Weng/D2L) without being the best single source for Bahdanau-specific formulation.
- **Attention Mechanism in ML** — [Attention Mechanism in ML](https://www.geeksforgeeks.org/artificial-intelligence/ml-attention-mechanism/)
  _Skipped because:_ Not authoritative enough for a high-quality curated shelf and typically too shallow/derivative for the specific equation-level gaps.
- **why Bahdanau is Additive?** — [why Bahdanau is Additive?](https://gist.github.com/ritwikraha/2466b901cb22bbe65288e4bb499e0ebc)
  _Skipped because:_ A gist is not a stable, citable teaching reference and is redundant with stronger sources.
- **The Seq2seq Model Provides...** — [The Seq2seq Model Provides...](https://arxiv.org/html/2506.17424v1)
  _Skipped because:_ Not a seminal/standard reference for Bahdanau attention and appears duplicative of existing tutorial material.
- **Attention Mechanism [1]: Seq2Seq Models - Chunpai Wang** — [Attention Mechanism [1]: Seq2Seq Models - Chunpai Wang](https://chunpai.github.io/2020/06/15/Attention-Mechanism-1.html)
  _Skipped because:_ Blog-level coverage that is likely redundant with the added Voita course page and existing Jalammar/Weng resources.
- **Advanced Sequence Models: From Bidirectional RNNs to Attenti** — [Advanced Sequence Models: From Bidirectional RNNs to Attention](https://datajourney24.substack.com/p/advanced-sequence-models-from-bidirectional)
  _Skipped because:_ Substack posts are less stable and typically less rigorous than textbook/course notes for equation-level formulation.
- **[PDF] Neural Machine Translation Model (Seq2seq Models With ** — [[PDF] Neural Machine Translation Model (Seq2seq Models With Attention)](https://bimsa.net/doc/notes/27196.pdf)
  _Skipped because:_ Unclear provenance and long-term stability; likely overlaps with standard seq2seq+attention lecture notes.
- **Proceedings of the The 8th International Joint Conference on** — [Proceedings of the The 8th International Joint Conference on Natural Language Processing, pages 431–440,](https://ahcweb01.naist.jp/papers/conference/2017/201711_IJCNLP_Tjandra_1/201711_IJCNLP_Tjandra_1.paper.pdf)
  _Skipped because:_ A research paper but not clearly targeted at explaining Bahdanau attention formulation/intuition for teaching; snippet suggests generic motivation slides.
- **A** — [A](https://proceedings.neurips.cc/paper/2021/file/ba3c736667394d5082f86f28aef38107-Supplemental.pdf)
  _Skipped because:_ Supplemental material with unclear context/title; not a reliable primary teaching reference for Bahdanau attention.

## Reasoning
**Curator:** D2L’s dedicated Bahdanau chapter is the most authoritative, equation-complete fill for the missing formulation details, while Voita’s course page adds especially strong intuition and alignment-focused explanation without being redundant with the existing Transformer-heavy attention resources.
**Reviewer:** The curator’s additions are strong, but the shelf is missing the actual Bahdanau attention paper (1412.7449) and would benefit from adding Luong et al. (2015) as the other seminal early attention reference; most other candidates are correctly deprioritized.

---

# Curation Report: Attention Complexity and Efficient Alternatives
**Topic:** `attention-mechanism` | **Date:** 2026-04-08 01:24
**Library:** 18 existing → 25 sources (7 added, 3 downloaded, 2 failed)
**Candidates evaluated:** 30
**Reviewer verdict:** needs_additions

## Added (7)
- **[paper]** [[PDF] On The Computational Complexity of Self-Attention](https://proceedings.mlr.press/v201/duman-keles23a/duman-keles23a.pdf)
  Gives a focused, formal treatment of self-attention’s computational (time) complexity, clarifying where the O(n^2) term arises and how it changes under common variants—more rigorous than the current mostly-intuitive/tutorial coverage.
   — covers: Derivation and explanation of standard self-attention O(n^2) time and memory complexity (attention matrix computation and softmax)
- **[paper]** [Efficient Attention Mechanisms for Large Language Models: A Survey](https://arxiv.org/html/2507.19595v1)
  A broad, structured survey that maps the sparse-attention design space (fixed patterns, block-sparse, routing/clustering, global tokens) and discusses efficiency/quality tradeoffs, providing the missing “big picture” reference for efficient alternatives.
   — covers: Sparse attention strategies: local/windowed attention, block-sparse patterns, global tokens, routing-based sparsity, and complexity/quality tradeoffs
- **[paper]** [[PDF] Efficient Content-Based Sparse Attention with Routing Transformers](https://david.grangier.info/papers/2020/aurkoroy-routing-transformer-2020.pdf)
  A seminal, concrete routing-based sparsity method (Routing Transformer) that complements the survey with an implementable mechanism and empirical evidence for content-based sparse attention beyond fixed windows/blocks.
   — covers: Sparse attention strategies: local/windowed attention, block-sparse patterns, global tokens, routing-based sparsity, and complexity/quality tradeoffs
- **[paper]** [Linformer: Self-Attention with Linear Complexity](https://arxiv.org/abs/2006.04768)
  This is one of the canonical low-rank/projection-based efficient attention papers and directly addresses the “low-rank approximation” gap with a concrete method, complexity analysis, and empirical results; it’s too central to omit if teaching efficient alternatives.
   — covers: Low-rank attention approximations
- **[paper]** [Rethinking Attention with Performers](https://arxiv.org/abs/2009.14794)
  Performer (FAVOR+) is the seminal kernelization/random-features route to linear-time softmax attention approximation, and it squarely fills the kernelization + numerical stability + approximation framing that the current library lacks.
   — covers: Kernelization for attention efficiency, Linear attention mechanisms
- **[paper]** [Linformer: Self-Attention with Linear Complexity](https://arxiv.org/abs/2006.04768) *(promoted by reviewer)*
  This is one of the canonical low-rank/projection-based efficient attention papers and directly addresses the “low-rank approximation” gap with a concrete method, complexity analysis, and empirical results; it’s too central to omit if teaching efficient alternatives.
   — fills: Low-rank attention approximations
- **[paper]** [Rethinking Attention with Performers](https://arxiv.org/abs/2009.14794) *(promoted by reviewer)*
  Performer (FAVOR+) is the seminal kernelization/random-features route to linear-time softmax attention approximation, and it squarely fills the kernelization + numerical stability + approximation framing that the current library lacks.
   — fills: Kernelization for attention efficiency, Linear attention mechanisms

## Near-Misses (12) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **[PDF] on the computational complexity of self-attention - ar** — [[PDF] on the computational complexity of self-attention - arXiv](https://arxiv.org/pdf/2209.04881.pdf)
  _Skipped because:_ Largely overlaps with the PMLR version of the same work; keeping one canonical venue copy avoids redundancy.
- **Attention2D: Communication Efficient Distributed Self ...** — [Attention2D: Communication Efficient Distributed Self ...](https://arxiv.org/html/2503.15758v1)
  _Skipped because:_ Primarily about distributed/communication-efficient attention rather than teaching the core O(n^2) derivation and practical memory footprint details targeted by the gaps.
- **Efficient self-attention mechanism** — [Efficient self-attention mechanism](https://dev.to/lewis_won/efficient-self-attention-mechanism-1p64)
  _Skipped because:_ Blog-level and likely derivative; not authoritative enough compared to the added survey and seminal papers.
- **Self-Attention - Page 5 of 5 | OneNoughtOne** — [Self-Attention - Page 5 of 5 | OneNoughtOne](https://www.onenoughtone.com/learn/self-attention/5)
  _Skipped because:_ Thin/fragmentary and not clearly more rigorous or comprehensive than existing tutorials already in the library.
- **Inference-Time Hyper-Scaling with KV Cache Compression - arX** — [Inference-Time Hyper-Scaling with KV Cache Compression - arXiv.org](https://arxiv.org/html/2506.05345v1)
  _Skipped because:_ Potentially relevant, but it’s a very recent, specialized method paper; the library would benefit more from a stable, broadly educational KV-cache/memory-footprint reference first.
- **[PDF] Adaptive KV Cache Management for Efficient Transformer** — [[PDF] Adaptive KV Cache Management for Efficient Transformer-based ...](https://odr.chalmers.se/server/api/core/bitstreams/46f57dac-8274-4fb1-8e51-ea179b75d95e/content)
  _Skipped because:_ Looks like a thesis/report with less clear long-term stability/canonical status than major-venue papers; also method-specific rather than a general memory-footprint explainer.
- **[PDF] PackKV: Reducing KV Cache Memory Footprint through LLM** — [[PDF] PackKV: Reducing KV Cache Memory Footprint through LLM-Aware ...](https://www.arxiv.org/pdf/2512.24449v2.pdf)
  _Skipped because:_ Method paper on KV compression; without a more general KV-cache/memory primer among candidates, adding this risks skewing the lesson toward one technique.
- **[PDF] Attention in Low-Rank Space for KV Cache Compression** — [[PDF] Attention in Low-Rank Space for KV Cache Compression](https://aclanthology.org/2024.findings-emnlp.899.pdf)
  _Skipped because:_ Relevant but narrow (KV compression via low-rank space) and doesn’t directly fill the broader “practical memory footprint details” gap as a teaching reference.
- **[PDF] Towards 10 Million Context Length LLM Inference with K** — [[PDF] Towards 10 Million Context Length LLM Inference with KV Cache ...](https://papers.nips.cc/paper_files/paper/2024/file/028fcbcf85435d39a40c4d61b42c99a4-Paper-Conference.pdf)
  _Skipped because:_ Highly specialized systems/method paper; not the clearest foundational resource for explaining KV cache scaling and memory accounting.
- **Content-Based Learnable Sparse Attention via Expert-Choice R** — [Content-Based Learnable Sparse Attention via Expert-Choice Routing](https://arxiv.org/html/2505.00315v1)
  _Skipped because:_ Promising but very recent and overlaps conceptually with the more established Routing Transformer paper plus the added survey.
- **Content-Based Learnable Sparse Attention Via Expert-Choice R** — [Content-Based Learnable Sparse Attention Via Expert-Choice Routing](https://www.scribd.com/document/968919690/2505-00315v1)
  _Skipped because:_ Unofficial repost (Scribd) is not a stable/authoritative source compared to the arXiv version.
- **Efficient Content-Based Sparse Attention with Routing ...** — [Efficient Content-Based Sparse Attention with Routing ...](https://aclanthology.org/2021.tacl-1.4.pdf)
  _Skipped because:_ Redundant with the Routing Transformers PDF already selected; keeping one canonical copy is sufficient.

## Uncovered Gaps (4) — No Good Candidates Found
_Consider manually sourcing these, or run enrichment again with different search terms._

- Practical memory footprint details: training activations vs inference, attention matrix storage, KV cache, and scaling with context length
- Low-rank attention approximations: Linformer, Nyströmformer, SVD/factorization intuition, projection dimensions, and approximation error considerations
- Linear attention mechanisms: rewriting attention to avoid n×n matrix, associativity tricks, normalization variants, and when linear attention works/fails
- Kernelization for attention efficiency: softmax as a kernel, random feature maps (e.g., Performer/FAVOR+), kernel feature approximations, and numerical stability

## Reasoning
**Curator:** The strongest improvements are (1) a rigorous complexity-focused paper to shore up the O(n^2) derivation gap and (2) authoritative coverage of sparse attention via a survey plus a seminal routing-based method. The remaining candidates skew toward narrow, recent KV-cache compression methods and do not provide the foundational, teaching-oriented memory/linear/kernel/low-rank coverage still missing.
**Reviewer:** The additions are solid for quadratic complexity and sparse/routing attention, but the lesson still needs at least one canonical low-rank paper (Linformer) and one canonical kernelized linear-attention paper (Performer) to cover the remaining core gaps.

---

# Curation Report: Luong (Multiplicative) Attention and Score Functions
**Topic:** `attention-mechanism` | **Date:** 2026-04-08 11:01
**Library:** 21 existing → 28 sources (7 added, 2 downloaded, 1 failed)
**Candidates evaluated:** 22
**Reviewer verdict:** needs_additions

## Added (7)
- **[reference_doc]** [Natural Language Processing (CS224N 2021 Lecture Slides)](https://web.stanford.edu/class/archive/cs/cs224n/cs224n.1214/slides/cs224n-2021-lecture08-final-project.pdf)
  CS224N slides typically give a clean, authoritative side-by-side of Bahdanau (additive) vs Luong (multiplicative) attention, including the dot/general/concat score functions and how scores become softmax weights—filling in derivation/definition clarity beyond what’s currently in the library.
   — covers: Luong (2015) multiplicative attention: definition and full derivation of score functions (dot, general, concat) and how they plug into softmax weighting, Explicit comparison to Bahdanau/additive attention: behavioral differences, parameterization, and when multiplicative is preferred
- **[paper]** [Attention Is All You Need (Vaswani et al., 2017)](https://arxiv.org/abs/1706.03762)
  Even though it’s already in the library, it should be explicitly treated as the authoritative reference for scaled dot-product attention (including the 1/sqrt(d_k) scaling motivation) and as the bridge from Luong dot-product to Transformer attention.
   — covers: Scaled dot-product attention: why scaling by 1/sqrt(d_k) is used, relation to Luong dot-product attention, and numerical stability/gradient behavior
- **[tutorial]** [Numerical Example (mlwithramin.com) — Attention](https://www.mlwithramin.com/blog/attention)
  This is one of the few candidates that appears to provide a concrete, step-by-step numeric walkthrough of computing attention scores and the resulting distribution, which directly targets the missing worked-example gap.
   — covers: Worked numeric examples computing attention scores and weights for each scoring variant
- **[tutorial]** [Self-Attention from Scratch (Sebastian Raschka)](https://sebastianraschka.com/blog/2023/self-attention-from-scratch.html)
  Raschka is a consistently high-signal educator; this piece is unusually clear about the mechanics and dimensions of Q/K/V and often includes concrete computations that can be adapted into worked examples for dot-product-style scoring.
   — covers: Worked numeric examples computing attention scores and weights for each scoring variant
- **[paper]** [Attention Is All You Need (Vaswani et al., 2017)](https://arxiv.org/abs/1706.03762) *(promoted by reviewer)*
  Even though it’s already in the library, it should be explicitly treated as the authoritative reference for scaled dot-product attention (including the 1/sqrt(d_k) scaling motivation) and as the bridge from Luong dot-product to Transformer attention.
   — fills: Scaled dot-product attention: why scaling by 1/sqrt(d_k) is used, relation to Luong dot-product attention, and numerical stability/gradient behavior
- **[tutorial]** [Numerical Example (mlwithramin.com) — Attention](https://www.mlwithramin.com/blog/attention) *(promoted by reviewer)*
  This is one of the few candidates that appears to provide a concrete, step-by-step numeric walkthrough of computing attention scores and the resulting distribution, which directly targets the missing worked-example gap.
   — fills: Worked numeric examples computing attention scores and weights for each scoring variant
- **[tutorial]** [Self-Attention from Scratch (Sebastian Raschka)](https://sebastianraschka.com/blog/2023/self-attention-from-scratch.html) *(promoted by reviewer)*
  Raschka is a consistently high-signal educator; this piece is unusually clear about the mechanics and dimensions of Q/K/V and often includes concrete computations that can be adapted into worked examples for dot-product-style scoring.
   — fills: Worked numeric examples computing attention scores and weights for each scoring variant

## Near-Misses (14) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **Luong Attention: Dot Product, General & Local Attention Mech** — [Luong Attention: Dot Product, General & Local Attention Mechanisms](https://mbrenndoerfer.com/writing/luong-attention-mechanisms-dot-product-general-local)
  _Skipped because:_ Potentially useful, but it’s a personal blog and likely overlaps with existing high-quality attention explainers already in the library without clearly adding the missing cost/scale/numeric-worked-example depth.
- **The Luong Attention Mechanism - MachineLearningMastery.com** — [The Luong Attention Mechanism - MachineLearningMastery.com](https://machinelearningmastery.com/the-luong-attention-mechanism/)
  _Skipped because:_ Often clear but tends to be higher-level and can be redundant with D2L/Voita/Weng; not reliably strong on derivations, cost breakdowns, or rigorous comparisons.
- **Scaled Dot-Product Attention Explained - ApX Machine Learnin** — [Scaled Dot-Product Attention Explained - ApX Machine Learning](https://apxml.com/courses/foundations-transformers-architecture/chapter-2-attention-mechanism-core-concepts/scaled-dot-product-attention)
  _Skipped because:_ Covers scaling intuition, but you already have a scaled dot-product attention explainer plus multiple transformer references; this is unlikely to add enough unique depth on numerical stability/gradient behavior to justify inclusion.
- **Class Notes: Attention Mechanisms in Neural Networks** — [Class Notes: Attention Mechanisms in Neural Networks](https://www.khoury.northeastern.edu/home/vip/teach/MLcourse/7_adv_NN/notes/chatGPT_responses/attention_mechanisms_latest.pdf)
  _Skipped because:_ The URL/path suggests it may be an unstable or derivative compilation (“chatGPT_responses”), making it less suitable for a high-quality, durable curated shelf.
- **Aman's AI Journal • Natural Language Processing • Attention** — [Aman's AI Journal • Natural Language Processing • Attention](https://aman.ai/primers/ai/attention/)
  _Skipped because:_ Likely a broad attention overview that overlaps with existing survey/tutorial sources (Weng, Voita, Jalammar, D2L) without clearly targeting the specific Luong score-function derivations and worked numeric examples.
- **自然语言处理中的注意力机制Summary of Attention Module in NLP_state of art** — [自然语言处理中的注意力机制Summary of Attention Module in NLP_state of art method till 2019 (Updating)...](https://blog.csdn.net/diankuaiyong2124/article/details/101216024)
  _Skipped because:_ CSDN repost/summary content is often redundant and less stable/authoritative than the existing textbook-style sources already included.
- **why Bahdanau is Additive?** — [why Bahdanau is Additive?](https://gist.github.com/ritwikraha/2466b901cb22bbe65288e4bb499e0ebc)
  _Skipped because:_ Too thin (gist-style note) for a curated library; doesn’t provide the comprehensive comparison/derivation depth needed.
- **Bahdanau Attention Mechanism (Also Known As Additive ...** — [Bahdanau Attention Mechanism (Also Known As Additive ...](https://www.scribd.com/document/854839826/16)
  _Skipped because:_ Scribd is paywalled/unstable for long-term curation and is likely redundant with D2L’s Bahdanau chapter already in the library.
- **What is an attention mechanism?** — [What is an attention mechanism?](https://www.ibm.com/think/topics/attention-mechanism)
  _Skipped because:_ High-level industry overview; unlikely to add the missing Luong score-function derivations, cost comparisons, or worked numeric examples.
- **Lecture 14: Neural Networks and Matrix Multiply.** — [Lecture 14: Neural Networks and Matrix Multiply.](https://www.cs.cornell.edu/courses/cs4787/2022fa/lectures/lecture14.pdf)
  _Skipped because:_ Good general background on matrix-multiply cost, but it doesn’t specifically analyze attention score-function variants (dot/general/concat/additive) in the way your gap requires.
- **[PDF] Copyright © by SIAM. Unauthorized reproduction of this** — [[PDF] Copyright © by SIAM. Unauthorized reproduction of this article is ...](https://www.cs.utsa.edu/~atc/pub/J42.pdf)
  _Skipped because:_ Not clearly about attention mechanisms; appears unrelated/too generic to fill the specific attention cost-comparison gap.
- **Copyright © by SIAM. Unauthorized reproduction of this artic** — [Copyright © by SIAM. Unauthorized reproduction of this article is prohibited.](http://www.cs.utsa.edu/faculty/atc/pub/J42.pdf)
  _Skipped because:_ Duplicate of the UTSA SIAM PDF and not clearly relevant to attention scoring-function cost comparisons.
- **Computational cost of matrix multiplication** — [Computational cost of matrix multiplication](https://www.emergentmind.com/open-problems/computational-cost-of-matrix-multiplication)
  _Skipped because:_ Too far from the concrete attention-mechanism comparison you need (dot vs general vs concat vs additive); would add generic complexity discussion without mapping to attention variants.
- **Attention Mechanism in Neural Networks - 13. Various ...** — [Attention Mechanism in Neural Networks - 13. Various ...](https://buomsoo-kim.github.io/attention/2020/03/19/Attention-mechanism-13.md/)
  _Skipped because:_ May discuss variants, but it’s a blog chapter and likely overlaps with existing tutorials; unclear that it provides the rigorous parameter-count/runtime comparison and worked numeric examples you’re missing.

## Uncovered Gaps (3) — No Good Candidates Found
_Consider manually sourcing these, or run enrichment again with different search terms._

- Computational cost comparison: dot vs general vs concat vs additive (matrix multiplies, parameter counts, runtime implications)
- Scaled dot-product attention: why scaling by 1/sqrt(d_k) is used, relation to Luong dot-product attention, and numerical stability/gradient behavior
- Worked numeric examples computing attention scores and weights for each scoring variant

## Reasoning
**Curator:** Most candidates are either broad/duplicative tutorials or generic matrix-multiply material; the CS224N slides are the only clearly authoritative, stable addition likely to improve coverage of Luong score functions and the Bahdanau-vs-Luong comparison. The remaining gaps (cost breakdowns and fully worked numeric examples across variants) are not well addressed by the candidate set.
**Reviewer:** The core seminal/authoritative bases are covered (Luong, Bahdanau, D2L, CS224N, Vaswani), but adding at least one strong worked-numeric-example source would materially close the remaining teaching gaps.

---

# Curation Report: Sequence-to-Sequence Basics and the Bottleneck Problem
**Topic:** `attention-mechanism` | **Date:** 2026-04-11 17:37
**Library:** 27 existing → 33 sources (6 added, 4 downloaded)
**Candidates evaluated:** 25
**Reviewer verdict:** needs_additions

## Added (6)
- **[reference_doc]** [[PDF] Encoder‐Decoder Models and Attention](https://www1.se.cuhk.edu.hk/~seem5680/lecture/Encoder-Decoder-Attention-2022spring.pdf)
  A coherent lecture-style walkthrough of classic encoder–decoder RNN seq2seq, explicitly covering training vs inference, autoregressive decoding, and the role of the context vector—material that’s currently scattered across your library.
   — covers: Encoder-decoder mechanics: encoder hidden states, decoder autoregressive generation, start/end tokens, inference vs training, Context vector definition and computation in classic RNN/LSTM seq2seq (final hidden state or pooled state) and how decoder conditions on it, Long-range dependencies: definition, why they are hard for RNNs/fixed vectors, and how attention alleviates them
- **[reference_doc]** [[PDF] Encoder-decoder RNN architecture - Cornell: Computer Science](https://www.cs.cornell.edu/courses/cs4740/2025sp/lectures/Lec12.pdf)
  A reputable, stable course lecture that tends to be very explicit about the seq2seq training objective and decoding procedure (teacher forcing vs test-time autoregressive generation), helping fill the practical mechanics gaps.
   — covers: Clear tutorial-style definition of sequence-to-sequence learning with examples (e.g., translation) and typical loss/objective, Encoder-decoder mechanics: encoder hidden states, decoder autoregressive generation, start/end tokens, inference vs training, Teacher forcing: definition, how it is applied in decoder training, exposure bias, and difference from inference-time decoding
- **[reference_doc]** [Lecture 16: Learning Long-Term Dependencies (Roger Grosse, University of Toronto CSC321)](https://www.cs.toronto.edu/~rgrosse/courses/csc321_2018/readings/L16%20Learning%20Long%20Term%20Dependencies.pdf)
  High-authority course notes that clearly explain why vanilla RNN encoder summaries struggle with long sequences (vanishing/exploding gradients, credit assignment), giving concrete intuition for the pre-attention fixed-vector bottleneck story.
   — covers: Information bottleneck in fixed-length context representations: why performance degrades with longer inputs; illustrative examples/intuition
- **[paper]** [Feed-Forward Networks with Attention Can Solve Some Long-Term Memory Problems (2015)](https://www.arxiv.org/pdf/1512.08756v1.pdf)
  A useful early paper connecting attention mechanisms to solving long-term dependency/path-length issues; it complements the NMT attention papers by focusing on the long-range dependency motivation rather than translation specifics.
   — covers: Information bottleneck in fixed-length context representations: why performance degrades with longer inputs; illustrative examples/intuition
- **[reference_doc]** [Lecture 16: Learning Long-Term Dependencies (Roger Grosse, University of Toronto CSC321)](https://www.cs.toronto.edu/~rgrosse/courses/csc321_2018/readings/L16%20Learning%20Long%20Term%20Dependencies.pdf) *(promoted by reviewer)*
  High-authority course notes that clearly explain why vanilla RNN encoder summaries struggle with long sequences (vanishing/exploding gradients, credit assignment), giving concrete intuition for the pre-attention fixed-vector bottleneck story.
   — fills: Information bottleneck in fixed-length context representations: why performance degrades with longer inputs; illustrative examples/intuition
- **[paper]** [Feed-Forward Networks with Attention Can Solve Some Long-Term Memory Problems (2015)](https://www.arxiv.org/pdf/1512.08756v1.pdf) *(promoted by reviewer)*
  A useful early paper connecting attention mechanisms to solving long-term dependency/path-length issues; it complements the NMT attention papers by focusing on the long-range dependency motivation rather than translation specifics.
   — fills: Information bottleneck in fixed-length context representations: why performance degrades with longer inputs; illustrative examples/intuition

## Near-Misses (13) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **What is Sequence-to-Sequence Learning?** — [What is Sequence-to-Sequence Learning?](https://www.geeksforgeeks.org/deep-learning/what-is-sequence-to-sequence-learning/)
  _Skipped because:_ Covers definitions at a high level but is typically too shallow/variable in rigor and stability compared with your existing D2L/CS224n/SLP coverage.
- **seq2seq Model** — [seq2seq Model](https://www.geeksforgeeks.org/machine-learning/seq2seq-model-in-machine-learning/)
  _Skipped because:_ Likely redundant with higher-quality sources already in the library (D2L, CS224n notes, PyTorch tutorial) and may not add enough depth on objectives/inference details.
- **[PDF] Sequence to Sequence Learning** — [[PDF] Sequence to Sequence Learning](http://www.cips-cl.org/static/CCL2017/slides/T1_part2.pdf)
  _Skipped because:_ Unclear provenance/maintenance and appears to duplicate basic seq2seq explanations already covered by SLP/CS224n/D2L.
- **[PDF] An Information Bottleneck Approach for Controlling Con** — [[PDF] An Information Bottleneck Approach for Controlling Conciseness in ...](https://aclanthology.org/2020.emnlp-main.153.pdf)
  _Skipped because:_ Uses information bottleneck in a different setting (rationale extraction) and doesn’t directly teach the classic fixed-length context-vector bottleneck in seq2seq.
- **[PDF] Lost in the Middle: How Language Models Use Long Conte** — [[PDF] Lost in the Middle: How Language Models Use Long Contexts](https://cs.stanford.edu/~nfliu/papers/lost-in-the-middle.arxiv2023.pdf)
  _Skipped because:_ High-quality, but it targets transformer long-context utilization rather than the seq2seq fixed-vector bottleneck and teacher-forcing mechanics you’re trying to shore up.
- **[PDF] How Information Bottleneck Helps Representation Learni** — [[PDF] How Information Bottleneck Helps Representation Learning](https://yichaocai.com/posts/information-bottleneck.pdf)
  _Skipped because:_ Potentially useful background, but it’s not an authoritative/standard reference and may not connect concretely to the seq2seq fixed-length context bottleneck.
- **arXiv:2501.00999v2 [cs.CL] 6 Jan 2025** — [arXiv:2501.00999v2 [cs.CL] 6 Jan 2025](https://www.arxiv.org/pdf/2501.00999.pdf)
  _Skipped because:_ Insufficiently identified from the candidate list and not clearly targeted at the specific seq2seq bottleneck/teacher-forcing gaps.
- **Sequence to Sequence Learning with Neural Networks** — [Sequence to Sequence Learning with Neural Networks](https://arxiv.org/pdf/1409.3215.pdf)
  _Skipped because:_ Already in your current library (same paper), so adding the PDF link would be redundant.
- **[PDF] Sequence to Sequence Learning with Neural Networks - N** — [[PDF] Sequence to Sequence Learning with Neural Networks - NIPS](https://static.googleusercontent.com/media/research.google.com/en/pubs/archive/43155.pdf)
  _Skipped because:_ Already in your current library (same paper), so this would be redundant.
- **[PDF] Encoder-Decoder Models, At- tention, and Contextual Em** — [[PDF] Encoder-Decoder Models, At- tention, and Contextual Em- beddings](https://web.stanford.edu/~jurafsky/slp3/old_oct19/10.pdf)
  _Skipped because:_ You already have an SLP Chapter 10 link in the library; this is essentially a redundant older snapshot.
- **[PDF] Neural Machine Translation Model (Seq2seq Models With ** — [[PDF] Neural Machine Translation Model (Seq2seq Models With Attention)](https://bimsa.net/doc/notes/27196.pdf)
  _Skipped because:_ Provenance/authority is unclear compared with established course notes and textbooks already present.
- **Part VI Neural Machine Translation, Seq2seq and Attenti** — [Part VI Neural Machine Translation, Seq2seq and Attenti](https://web.stanford.edu/class/cs224n/readings/cs224n-2019-notes06-NMT_seq2seq_attention.pdf)
  _Skipped because:_ Already in your current library.
- **CS224n: Natural Language Processing with Deep Learning   Lec** — [CS224n: Natural Language Processing with Deep Learning   Lecture Notes: Part VI  Neural Machine Translation, Seq2seq and Attention](http://web.stanford.edu/class/cs224n/readings/cs224n-2019-notes06-NMT_seq2seq_attention.pdf)
  _Skipped because:_ Already in your current library (duplicate URL variant).

## Uncovered Gaps (1) — No Good Candidates Found
_Consider manually sourcing these, or run enrichment again with different search terms._

- Information bottleneck in fixed-length context representations: why performance degrades with longer inputs; illustrative examples/intuition

## Reasoning
**Curator:** Most candidates are either redundant with your already-strong D2L/CS224n/SLP coverage or are lower-quality tutorials; the two course-lecture PDFs add the most value by clearly consolidating seq2seq mechanics (training objective, decoding, and teacher forcing) in a teachable format. None of the candidates directly and pedagogically targets the classic fixed-length context-vector bottleneck with strong intuition/examples.
**Reviewer:** The curator’s additions are solid for seq2seq mechanics, but adding one authoritative long-term-dependency lecture note (and optionally an early attention-for-memory paper) would better close the remaining bottleneck intuition gap.

---

# Curation Report: Sequence-to-Sequence Basics and the Bottleneck Problem
**Topic:** `attention-mechanism` | **Date:** 2026-04-11 18:02
**Library:** 31 existing → 38 sources (7 added, 4 downloaded)
**Candidates evaluated:** 21
**Reviewer verdict:** needs_additions

## Added (7)
- **[reference_doc]** [[PDF] Encoder-Decoder Models, Attention, and Contextual Embeddings](https://web.stanford.edu/~jurafsky/slp3/old_oct19/10.pdf)
  Adds an authoritative, tutorial-style walkthrough of classic RNN encoder–decoder seq2seq mechanics (including start/end tokens, autoregressive decoding, and training vs inference) that your current library only covers partially across scattered notes.
   — covers: A tutorial-level definition of sequence-to-sequence learning (inputs/outputs, sequence transduction tasks, likelihood objective), Encoder-decoder mechanics: encoder hidden states, decoder autoregressive generation, start/end tokens, inference vs training, Context vector: definition, how classic seq2seq uses a single fixed-size vector (e.g., final encoder state), and how it conditions the decoder
- **[paper]** [Scheduled Sampling for Sequence Prediction with Recurrent Neural Networks](https://arxiv.org/abs/1506.03099)
  This is the canonical paper for exposure bias and the standard mitigation to teacher forcing (scheduled sampling); it directly fills the only explicitly stated gap and is more authoritative than handbook/blog writeups.
   — covers: Teacher forcing: definition, how it is applied in decoder training, exposure bias, and contrast with free-running decoding
- **[paper]** [Professor Forcing: A New Algorithm for Training Recurrent Networks](https://www.arxiv.org/abs/1606.03498)
  A well-cited follow-on that frames the teacher-forcing vs free-running mismatch explicitly and proposes an adversarial alignment objective; useful as a second, higher-level reference once scheduled sampling is introduced.
   — covers: Teacher forcing: definition, how it is applied in decoder training, exposure bias, and contrast with free-running decoding
- **[tutorial]** [Teacher Forcing (Language AI Handbook chapter; arXiv:1809.03132v1)](https://arxiv.org/pdf/1809.03132.pdf)
  Among the remaining candidates, this is the most directly on-target for a clear, tutorial definition of teacher forcing and exposure bias; it can serve as the approachable teaching companion to the seminal papers above.
   — covers: Teacher forcing: definition, how it is applied in decoder training, exposure bias, and contrast with free-running decoding
- **[paper]** [Scheduled Sampling for Sequence Prediction with Recurrent Neural Networks](https://arxiv.org/abs/1506.03099) *(promoted by reviewer)*
  This is the canonical paper for exposure bias and the standard mitigation to teacher forcing (scheduled sampling); it directly fills the only explicitly stated gap and is more authoritative than handbook/blog writeups.
   — fills: Teacher forcing: definition, how it is applied in decoder training, exposure bias, and contrast with free-running decoding
- **[paper]** [Professor Forcing: A New Algorithm for Training Recurrent Networks](https://www.arxiv.org/abs/1606.03498) *(promoted by reviewer)*
  A well-cited follow-on that frames the teacher-forcing vs free-running mismatch explicitly and proposes an adversarial alignment objective; useful as a second, higher-level reference once scheduled sampling is introduced.
   — fills: Teacher forcing: definition, how it is applied in decoder training, exposure bias, and contrast with free-running decoding
- **[tutorial]** [Teacher Forcing (Language AI Handbook chapter; arXiv:1809.03132v1)](https://arxiv.org/pdf/1809.03132.pdf) *(promoted by reviewer)*
  Among the remaining candidates, this is the most directly on-target for a clear, tutorial definition of teacher forcing and exposure bias; it can serve as the approachable teaching companion to the seminal papers above.
   — fills: Teacher forcing: definition, how it is applied in decoder training, exposure bias, and contrast with free-running decoding

## Near-Misses (14) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **Seq2seq - Wikipedia** — [Seq2seq - Wikipedia](https://en.wikipedia.org/wiki/Seq2seq)
  _Skipped because:_ Useful as a quick overview but typically too shallow/unstable in depth and rigor for filling the specific mechanics and bottleneck gaps in a high-quality teaching shelf.
- **seq2seq Model** — [seq2seq Model](https://www.geeksforgeeks.org/machine-learning/seq2seq-model-in-machine-learning/)
  _Skipped because:_ Covers basics but is comparatively low-authority and tends to be surface-level relative to the textbook/lecture material already in the library.
- **5.3 Why Lstm Also Has...** — [5.3 Why Lstm Also Has...](https://blog.sotaaz.com/post/context-vector-limitation-en)
  _Skipped because:_ Directly targets the bottleneck intuition, but it’s a blog of uncertain longevity/authority and overlaps with stronger primary/teaching sources you already have on attention and bottlenecks.
- **Step-by-Step with Transformers: From Seq2Seq Bottlenecks to ** — [Step-by-Step with Transformers: From Seq2Seq Bottlenecks to ...](https://arbisoft.com/blogs/step-by-step-with-transformers-from-seq2-seq-bottlenecks-to-cutting-edge-attention-mechanisms-in-nlp)
  _Skipped because:_ Likely a decent narrative blog, but not as citable/stable as textbook chapters and largely redundant with existing attention/Transformer explainers in the library.
- **Challenges in Sequence-to-Sequence Tasks** — [Challenges in Sequence-to-Sequence Tasks](https://apxml.com/courses/introduction-to-transformer-models/chapter-1-sequence-modeling-attention-fundamentals/sequence-to-sequence-challenges)
  _Skipped because:_ Seems relevant, but you already have multiple APXML pages plus stronger canonical sources; this would be incremental rather than a clear gap-filler.
- **[PDF] Sequence to Sequence Learning with Neural Networks - N** — [[PDF] Sequence to Sequence Learning with Neural Networks - NIPS](https://static.googleusercontent.com/media/research.google.com/en/pubs/archive/43155.pdf)
  _Skipped because:_ Seminal and high-quality, but it’s redundant because the same paper is already in your library (arxiv:1409.3215).
- **[PDF] Sequence to Sequence Learning with Neural Networks** — [[PDF] Sequence to Sequence Learning with Neural Networks](https://proceedings.neurips.cc/paper_files/paper/2014/file/5a18e133cbf9f257297f410bb7eca942-Paper.pdf)
  _Skipped because:_ Redundant with the existing arXiv entry for the same Sutskever et al. paper.
- **Sequence to Sequence Learning with Neural Networks** — [Sequence to Sequence Learning with Neural Networks](https://arxiv.org/pdf/1409.3215.pdf)
  _Skipped because:_ Already present in the library (arxiv:1409.3215), so adding the PDF link would be duplicative.
- **Sequence to Sequence Learning with Neural Networks** — [Sequence to Sequence Learning with Neural Networks](https://cs224d.stanford.edu/papers/seq2seq.pdf)
  _Skipped because:_ Another hosted copy of Sutskever et al.; redundant with the existing arXiv listing.
- **Part VI Neural Machine Translation, Seq2seq and Attenti** — [Part VI Neural Machine Translation, Seq2seq and Attenti](https://web.stanford.edu/class/cs224n/readings/cs224n-2019-notes06-NMT_seq2seq_attention.pdf)
  _Skipped because:_ Already in your library (same CS224n notes URL), so it doesn’t add anything new.
- **CS224n: Natural Language Processing with Deep Learning   Lec** — [CS224n: Natural Language Processing with Deep Learning   Lecture Notes: Part VI  Neural Machine Translation, Seq2seq and Attention](https://web.stanford.edu/class/archive/cs/cs224n/cs224n.1194/readings/cs224n-2019-notes06-NMT_seq2seq_attention.pdf)
  _Skipped because:_ Effectively the same CS224n notes already included; adding another archive path is redundant.
- **Learning Transductions and Alignments with RNN Seq2seq ...** — [Learning Transductions and Alignments with RNN Seq2seq ...](https://proceedings.mlr.press/v217/wang23a/wang23a.pdf)
  _Skipped because:_ Research-focused and not the best use of shelf space for the stated beginner gaps (definition/mechanics/teacher forcing/bottleneck intuition).
- **Improving Sequence to Sequence Neural Machine ...** — [Improving Sequence to Sequence Neural Machine ...](https://aclanthology.org/I17-1003.pdf)
  _Skipped because:_ Potentially valuable but too specialized for the core “seq2seq basics + bottleneck” lesson, and the library already has the key foundational NMT/attention papers.
- **Hands-On Deep Learning Algorithms with Python** — [Hands-On Deep Learning Algorithms with Python](https://www.oreilly.com/library/view/hands-on-deep-learning/9781789344158/84352544-52f0-4bbe-ad68-773528eb8587.xhtml)
  _Skipped because:_ Paywalled and likely redundant with the existing free, high-quality tutorials/notes (D2L, CS224n, SLP).

## Uncovered Gaps (1) — No Good Candidates Found
_Consider manually sourcing these, or run enrichment again with different search terms._

- Teacher forcing: definition, how it is applied in decoder training, exposure bias, and contrast with free-running decoding

## Reasoning
**Curator:** Most candidates are duplicates of sources already in the library or are lower-authority blog/overview material. The Jurafsky & Martin SLP chapter is the single strongest addition because it consolidates the missing seq2seq definition and encoder–decoder mechanics in a stable, authoritative, tutorial-friendly reference.
**Reviewer:** The library is strong on seq2seq/attention and the bottleneck story, but it should add at least one canonical exposure-bias/teacher-forcing source (scheduled sampling) plus an accessible tutorial to close the remaining gap.

---

# Curation Report: Sequence-to-Sequence Basics and the Bottleneck Problem
**Topic:** `attention-mechanism` | **Date:** 2026-04-11 19:40
**Library:** 35 existing → 38 sources (3 added, 2 downloaded)
**Candidates evaluated:** 20
**Reviewer verdict:** good

## Added (3)
- **[paper]** [Sequence Transduction with Recurrent Neural Networks](https://arxiv.org/abs/1211.3711)
  Adds an explicit, foundational treatment of sequence transduction as a learning problem (beyond NMT), with concrete examples and mechanics that complement the existing NMT-focused seq2seq/attention readings.
   — covers: Clear definition and worked explanation of sequence-to-sequence modeling (sequence transduction) with examples, Encoder-decoder mechanics: encoder states, decoder autoregressive generation, training objective, inference (greedy/beam) basics
- **[reference_doc]** [CS224n (Stanford) Notes: Neural Machine Translation, Seq2seq and Attention](https://web.stanford.edu/class/cs224n/readings/cs224n-2019-notes06-NMT_seq2seq_attention.pdf)
  This is a high-authority Stanford reference that explicitly walks through the classic encoder-decoder with a fixed-length context vector (often the final encoder state) and motivates attention as the remedy—directly targeting the bottleneck explanation the lesson still lacks.
   — covers: Explicit definition and computation of the context vector in classic RNN/LSTM seq2seq (e.g., final hidden state) and why fixed-size is limiting, Long-range dependencies in sequence models and why fixed-length context vectors/RNNs struggle as input length grows
- **[reference_doc]** [CS224n (Stanford) Notes: Neural Machine Translation, Seq2seq and Attention](https://web.stanford.edu/class/cs224n/readings/cs224n-2019-notes06-NMT_seq2seq_attention.pdf) *(promoted by reviewer)*
  This is a high-authority Stanford reference that explicitly walks through the classic encoder-decoder with a fixed-length context vector (often the final encoder state) and motivates attention as the remedy—directly targeting the bottleneck explanation the lesson still lacks.
   — fills: Explicit definition and computation of the context vector in classic RNN/LSTM seq2seq (e.g., final hidden state) and why fixed-size is limiting, Long-range dependencies in sequence models and why fixed-length context vectors/RNNs struggle as input length grows

## Near-Misses (13) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **Sequence Transduction with Recurrent Neural Networks** — [Sequence Transduction with Recurrent Neural Networks](https://www.cs.toronto.edu/~graves/icml_2012.pdf)
  _Skipped because:_ Redundant with the arXiv version of the same paper; keep the canonical arXiv URL for stability and citation clarity.
- **[PDF] Sequence Transduction with Recurrent Neural Networks** — [[PDF] Sequence Transduction with Recurrent Neural Networks](http://www.cs.toronto.edu/~graves/icml_2012.pdf)
  _Skipped because:_ Same content as the arXiv entry; prefer the canonical arXiv URL.
- **Sequence Transduction - EITC** — [Sequence Transduction - EITC](http://www.eitc.org/research-opportunities/new-media-and-new-digital-economy/ai-machine-learning-deep-learning-and-neural-networks/ml-research-and-applications/foundations-of-ml/sequence-transduction)
  _Skipped because:_ Appears to mirror/host Graves content without being the authoritative source; less stable and potentially duplicative.
- **Encoder-Decoder** — [Encoder-Decoder](https://elearning.di.unipi.it/pluginfile.php/89869/mod_resource/content/1/AID-L19.pdf)
  _Skipped because:_ Likely overlaps heavily with Jurafsky & Martin chapter/CS224n notes already in the library; unclear it adds unique coverage beyond existing authoritative docs.
- **Text Generation and Encoder-Decoder Models** — [Text Generation and Encoder-Decoder Models](https://opencourse.inf.ed.ac.uk/sites/default/files/https/opencourse.inf.ed.ac.uk/fnlp/2024/25slides4.pdf)
  _Skipped because:_ Slides appear to reuse Jurafsky & Martin material and are likely redundant with the existing SLP chapter and CS224n notes.
- **seq2seq Model** — [seq2seq Model](https://www.geeksforgeeks.org/machine-learning/seq2seq-model-in-machine-learning/)
  _Skipped because:_ Too shallow and non-authoritative relative to existing high-quality lecture notes and textbook chapters.
- **[PDF] Neural Machine Translation Model (Seq2seq Models With ** — [[PDF] Neural Machine Translation Model (Seq2seq Models With Attention)](https://bimsa.net/doc/notes/27196.pdf)
  _Skipped because:_ Unclear provenance/authority and likely redundant with CS224n + SLP + D2L coverage already present.
- **Seq2seq - Wikipedia** — [Seq2seq - Wikipedia](https://en.wikipedia.org/wiki/Seq2seq)
  _Skipped because:_ Good for quick orientation but not substantive enough for the specific worked mechanics/context-vector bottleneck gaps given the existing library depth.
- **References And Notes** — [References And Notes](https://arxiv.org/html/2506.00588)
  _Skipped because:_ Not a clear, canonical resource for long-range dependency limitations; looks like ancillary notes rather than a focused, authoritative explanation.
- **Under peer review** — [Under peer review](http://arxiv.org/pdf/2410.07145.pdf)
  _Skipped because:_ Not yet vetted/accepted and not clearly the best canonical reference for long-term dependency limitations compared to established readings already in the library.
- **Revisiting the problem of learning long-term dependencies ..** — [Revisiting the problem of learning long-term dependencies ... - PubMed](https://pubmed.ncbi.nlm.nih.gov/39637825/)
  _Skipped because:_ Index/abstract page rather than a stable, accessible full resource; also the library already includes a strong long-term dependencies lecture note.
- **Revisiting Sequence Models: RNNs, LSTMs, and Their Limits** — [Revisiting Sequence Models: RNNs, LSTMs, and Their Limits](https://codesignal.com/learn/courses/sequence-models-the-dawn-of-attention-1/lessons/revisiting-sequence-models-rnns-lstms-and-their-limits-1)
  _Skipped because:_ Paywalled/platform-tied and likely redundant with the existing University of Toronto long-term dependencies lecture.
- **RNN Performance: Sequence Length & Batch Size | PDF** — [RNN Performance: Sequence Length & Batch Size | PDF](https://www.scribd.com/document/967706616/NNDL-1)
  _Skipped because:_ Low-quality/unstable hosting and unclear authorship; not suitable for a high-quality curated shelf.

## Uncovered Gaps (3) — No Good Candidates Found
_Consider manually sourcing these, or run enrichment again with different search terms._

- Explicit definition and computation of the context vector in classic RNN/LSTM seq2seq (e.g., final hidden state) and why fixed-size is limiting
- Long-range dependencies in sequence models and why fixed-length context vectors/RNNs struggle as input length grows
- Exposure bias: formal definition, why teacher forcing causes it, and common mitigations (scheduled sampling, professor forcing, etc.)

## Reasoning
**Curator:** Most candidates are redundant with existing authoritative seq2seq/attention materials (CS224n, SLP, D2L) or are low-authority. Graves (2012) is a canonical, high-signal paper that broadens the library’s seq2seq foundations with a clear sequence transduction framing and concrete mechanics.
**Reviewer:** Overall the curation is strong and already includes the key seminal seq2seq/attention papers; the only clear miss among the provided candidates is the Stanford CS224n notes, which directly and authoritatively fill the remaining context-vector bottleneck gap.
