# Curation Report: Queries, Keys, and Values: A Unified Framework
**Topic:** `self-attention` | **Date:** 2026-04-07 15:46
**Library:** 12 existing → 17 sources (5 added, 3 downloaded, 1 failed)
**Candidates evaluated:** 20
**Reviewer verdict:** needs_additions

## Added (5)
- **[tutorial]** [11.1. Queries, Keys, and Values - Dive into Deep Learning](https://d2l.ai/chapter_attention-mechanisms-and-transformers/queries-keys-values.html)
  This D2L chapter directly frames attention as a differentiable dictionary lookup with formal notation, explicitly introducing the QKV abstraction as a unified framework — exactly the conceptual foundation the library is missing despite having adjacent D2L chapters on scoring functions and Bahdanau.
   — covers: QKV abstraction as a unified framework showing Bahdanau and Luong attention as special cases, Attention as differentiable dictionary lookup — the information-retrieval analogy with formal explanation, Soft retrieval mechanics in the QKV framework
- **[tutorial]** [Bahdanau vs Luong Attention - Baeldung](https://www.baeldung.com/cs/attention-luong-vs-bahdanau)
  Provides a direct side-by-side comparison of Bahdanau and Luong attention mechanisms using consistent notation, helping establish both as special cases of the general QKV framework — a contrast the current library lacks despite covering each mechanism individually.
   — covers: QKV abstraction as a unified framework showing Bahdanau and Luong attention as special cases
- **[tutorial]** [Query, Key, Value: The Foundation of Transformer Attention](https://mbrenndoerfer.com/writing/query-key-value-attention-mechanism)
  Dedicated explainer on the QKV mechanism that covers the information-retrieval analogy and soft retrieval mechanics, complementing the existing Bahdanau-focused piece from the same author already in the library.
   — covers: Attention as differentiable dictionary lookup — the information-retrieval analogy with formal explanation, Soft retrieval mechanics in the QKV framework
- **[tutorial]** [Cross-Attention Mechanism in Transformers](https://www.geeksforgeeks.org/nlp/cross-attention-mechanism-in-transformers/)
  Directly addresses the only remaining uncovered gap — cross-attention vs self-attention with explicit QKV notation showing queries from decoder and keys/values from encoder — which no current library source covers. GeeksForGeeks NLP articles are widely used as accessible reference material and this fills a concrete structural hole.
   — covers: Cross-attention vs self-attention: explicit contrast using QKV notation (queries from decoder, keys/values from encoder)
- **[tutorial]** [Cross-Attention Mechanism in Transformers](https://www.geeksforgeeks.org/nlp/cross-attention-mechanism-in-transformers/) *(promoted by reviewer)*
  Directly addresses the only remaining uncovered gap — cross-attention vs self-attention with explicit QKV notation showing queries from decoder and keys/values from encoder — which no current library source covers. GeeksForGeeks NLP articles are widely used as accessible reference material and this fills a concrete structural hole.
   — fills: Cross-attention vs self-attention: explicit contrast using QKV notation (queries from decoder, keys/values from encoder)

## Near-Misses (5) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **QV May Be Enough: Toward the Essence of Attention in LLMs - ** — [QV May Be Enough: Toward the Essence of Attention in LLMs - arXiv](https://arxiv.org/html/2603.15665v1)
  _Skipped because:_ Interesting theoretical paper but focuses on arguing keys are redundant in LLMs rather than teaching the QKV unified framework as a pedagogical foundation; too advanced and tangential for this introductory-to-intermediate library.
- **QV May Be Enough: Toward the Essence of Attention in LLMs** — [QV May Be Enough: Toward the Essence of Attention in LLMs](https://arxiv.org/pdf/2603.15665.pdf)
  _Skipped because:_ Duplicate of the HTML version above; same reasoning applies.
- **Attention is a differentiable lookup. - Kunvar** — [Attention is a differentiable lookup. - Kunvar](https://kunvarthaman.com/posts/attention-is-a-differentiable-lookup.html)
  _Skipped because:_ Title is directly on-topic but the URL appears to be a personal blog post of uncertain depth and stability; the D2L chapter covers the same concept more authoritatively.
- **Activation-aware Probe-Query: Effective Key-Value Retrieval ** — [Activation-aware Probe-Query: Effective Key-Value Retrieval for Long-Context LLMs Inference](https://arxiv.org/html/2502.13542v1)
  _Skipped because:_ Covers KV retrieval in the context of LLM inference efficiency, not the foundational soft retrieval mechanics of the QKV attention framework as a teaching concept.
- **Class Notes: Attention Mechanisms in Neural Networks** — [Class Notes: Attention Mechanisms in Neural Networks](https://www.khoury.northeastern.edu/home/vip/teach/MLcourse/7_adv_NN/notes/chatGPT_responses/attention_mechanisms_tikz.pdf)
  _Skipped because:_ The content preview suggests this is ChatGPT-generated class notes, which raises quality and authoritativeness concerns for a curated teaching library.

## Uncovered Gaps (1) — No Good Candidates Found
_Consider manually sourcing these, or run enrichment again with different search terms._

- Cross-attention vs self-attention: explicit contrast using QKV notation (queries from decoder, keys/values from encoder)

## Reasoning
**Curator:** The strongest addition is the D2L QKV chapter, which is the authoritative textbook treatment of the differentiable dictionary lookup framing and directly fills the most critical conceptual gap; the Baeldung comparison and mbrenndoerfer QKV piece add useful pedagogical angles on the unified framework and soft retrieval, while the cross-attention vs self-attention gap remains uncovered by any candidate of sufficient quality.
**Reviewer:** The curator made strong, well-reasoned choices for the QKV framework and Bahdanau/Luong coverage, but left the cross-attention vs self-attention gap entirely open despite a directly relevant candidate being available in the search results.

---

# Curation Report: Visualizing and Interpreting Attention Weights
**Topic:** `self-attention` | **Date:** 2026-04-07 15:47
**Library:** 15 existing → 25 sources (10 added, 6 downloaded, 2 failed)
**Candidates evaluated:** 39
**Reviewer verdict:** needs_additions

## Added (10)
- **[tutorial]** [Visualizing A Neural Machine Translation Model (Mechanics of Seq2seq Models With Attention)](https://jalammar.github.io/visualizing-neural-machine-translation-mechanics-of-seq2seq-models-with-attention/)
  Jay Alammar's canonical visual walkthrough of seq2seq attention with concrete animated heatmap examples — directly fills the alignment visualization gap and is the most-cited accessible resource on this topic.
   — covers: Alignment visualization in seq2seq and transformer models with concrete heatmap examples
- **[paper]** [Attention is not Explanation](https://arxiv.org/abs/1902.10186)
  The landmark Jain & Wallace 2019 paper that started the 'attention as explanation' debate — a seminal work the library explicitly needs and cannot be substituted by any existing source.
   — covers: Attention weights as explanation for model decisions — the debate and key papers (e.g., Jain & Wallace 2019, Wiegreffe & Pinter 2019), Limitations of using attention weights for interpretability in deep learning models
- **[paper]** [Attention is not not Explanation](https://arxiv.org/abs/1908.04626)
  The Wiegreffe & Pinter 2019 rebuttal paper — the other half of the canonical debate pair, directly named in the gap list, providing the counter-argument and nuanced framework for evaluating attention as explanation.
   — covers: Attention weights as explanation for model decisions — the debate and key papers (e.g., Jain & Wallace 2019, Wiegreffe & Pinter 2019), Faithfulness vs plausibility in model explanations — definitions, distinction, and implications
- **[paper]** [Why use attention as explanation when we have saliency methods?](https://aclanthology.org/2020.blackboxnlp-1.14.pdf)
  Directly compares attention-based explanations to gradient-based saliency methods, filling the specific gap on attention vs. integrated gradients/SHAP that no existing library source covers.
   — covers: Comparison of attention-based explanations vs gradient-based saliency methods (e.g., integrated gradients, SHAP), Attention weights as explanation for model decisions — the debate and key papers (e.g., Jain & Wallace 2019, Wiegreffe & Pinter 2019)
- **[paper]** [Transformer Interpretability Beyond Attention Visualization](https://openaccess.thecvf.com/content/CVPR2021/papers/Chefer_Transformer_Interpretability_Beyond_Attention_Visualization_CVPR_2021_paper.pdf)
  CVPR 2021 paper that introduces attention rollout and relevancy propagation techniques, directly covering the attention rollout gap and the limitations of raw attention weight visualization.
   — covers: Attention rollout technique: definition, mechanics, and how it propagates attention across transformer layers, Limitations of using attention weights for interpretability in deep learning models
- **[tutorial]** [Attention Map Visualization](https://apxml.com/courses/how-to-build-a-large-language-model/chapter-23-analyzing-model-behavior/attention-map-visualization)
  Practical tutorial covering how to extract and visualize attention weight matrices as heatmaps in transformer models with code examples, filling the hands-on tooling gap the library currently lacks.
   — covers: How to extract and visualize attention weight matrices as heatmaps in transformer models (tools, code, examples)
- **[paper]** [Quantifying Attention Flow in Transformers](https://arxiv.org/abs/2005.00928)
  This is the original Abnar & Zuidema 2020 ACL paper that introduces attention rollout — the curator added the Chefer et al. CVPR paper for rollout coverage, but that paper builds on and cites this one as the foundational source. A teaching library on attention rollout should include the paper that coined and defined the technique.
   — covers: Attention rollout technique: definition, mechanics, and how it propagates attention across transformer layers
- **[paper]** [Faithfulness vs. Plausibility: On the (Un)Reliability of Explanations from Large Language Models](https://arxiv.org/abs/2402.04614)
  Provides a dedicated, rigorous treatment of the faithfulness vs. plausibility distinction that is only a secondary theme in the Wiegreffe & Pinter paper already added; this fills the conceptual gap on that distinction more directly and is a stable arXiv URL from a citable venue.
   — covers: Faithfulness vs plausibility in model explanations — definitions, distinction, and implications
- **[paper]** [Quantifying Attention Flow in Transformers](https://arxiv.org/abs/2005.00928) *(promoted by reviewer)*
  This is the original Abnar & Zuidema 2020 ACL paper that introduces attention rollout — the curator added the Chefer et al. CVPR paper for rollout coverage, but that paper builds on and cites this one as the foundational source. A teaching library on attention rollout should include the paper that coined and defined the technique.
   — fills: Attention rollout technique: definition, mechanics, and how it propagates attention across transformer layers
- **[paper]** [Faithfulness vs. Plausibility: On the (Un)Reliability of Explanations from Large Language Models](https://arxiv.org/abs/2402.04614) *(promoted by reviewer)*
  Provides a dedicated, rigorous treatment of the faithfulness vs. plausibility distinction that is only a secondary theme in the Wiegreffe & Pinter paper already added; this fills the conceptual gap on that distinction more directly and is a stable arXiv URL from a citable venue.
   — fills: Faithfulness vs plausibility in model explanations — definitions, distinction, and implications

## Near-Misses (6) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **How Does Attention Work in Vision Transformers? A Visual Ana** — [How Does Attention Work in Vision Transformers? A Visual Analytics Approach](https://pmc.ncbi.nlm.nih.gov/articles/PMC10290521/)
  _Skipped because:_ Covers ViT-specific attention analysis which is valuable but too domain-specific (vision) for a general attention visualization library, and the CVPR paper already covers the core interpretability ground.
- **Attention is not not Explanation - ACL Anthology** — [Attention is not not Explanation - ACL Anthology](https://aclanthology.org/D19-1002/)
  _Skipped because:_ Duplicate of the arXiv version already added (1908.04626); the arXiv link is preferred for stability and accessibility.
- **Visualizing Attention in Transformer-Based Language Models** — [Visualizing Attention in Transformer-Based Language Models](http://arxiv.org/pdf/1904.02679.pdf)
  _Skipped because:_ Relevant to attention visualization but the PDF-direct link is less stable and the content is largely superseded by the Chefer et al. CVPR paper and the existing BertViz-style tooling covered elsewhere.
- **VISIT: Visualizing and Interpreting the Semantic Information** — [VISIT: Visualizing and Interpreting the Semantic Information Flow of Transformers](https://ar5iv.labs.arxiv.org/html/2305.13417)
  _Skipped because:_ Interesting research but ar5iv is not a stable canonical URL and the paper is too specialized for a foundational teaching library.
- **Learning to Deceive with Attention-Based Explanations** — [Learning to Deceive with Attention-Based Explanations](https://users.cs.duke.edu/~bd149/papers/fool-attention.pdf)
  _Skipped because:_ Relevant to attention faithfulness debate but a PDF on a personal university page is not a stable enough URL for a curated library, and the core debate is already covered by the Jain/Wiegreffe papers.
- **Visualizing Cross-Modal Attention in CLIP/BLIP Models** — [Visualizing Cross-Modal Attention in CLIP/BLIP Models](https://discuss.huggingface.co/t/transformers-attention-viz-visualizing-cross-modal-attention-in-clip-blip-models/163913)
  _Skipped because:_ Forum discussion thread — too thin and unstable for a curated library, even though the topic is relevant.

## Uncovered Gaps (1) — No Good Candidates Found
_Consider manually sourcing these, or run enrichment again with different search terms._

- Diagnostic probing as an interpretability method for transformer representations

## Reasoning
**Curator:** The additions prioritize seminal papers that are explicitly named in the gap list (Jain & Wallace, Wiegreffe & Pinter), the canonical visual tutorial by Jay Alammar for alignment heatmaps, the CVPR attention rollout paper for the propagation mechanics gap, and a practical code-oriented tutorial for hands-on visualization. The faithfulness/plausibility distinction is partially covered by the Wiegreffe paper. No candidate adequately covers diagnostic probing, which remains an open gap.
**Reviewer:** The curator made strong, well-reasoned choices overall, but missed the original attention rollout paper (Abnar & Zuidema 2020) which is the foundational source the CVPR paper builds on, and a dedicated faithfulness-vs-plausibility treatment that goes beyond what the Wiegreffe & Pinter paper covers on that specific distinction.

---

# Curation Report: Multi-Head Attention: Representation Subspaces and Implementation
**Topic:** `self-attention` | **Date:** 2026-04-08 01:25
**Library:** 21 existing → 30 sources (9 added, 3 downloaded, 3 failed)
**Candidates evaluated:** 27
**Reviewer verdict:** needs_additions

## Added (9)
- **[tutorial]** [11.5. Multi-Head Attention - Dive into Deep Learning](https://d2l.ai/chapter_attention-mechanisms-and-transformers/multihead-attention.html)
  Adds an authoritative, step-by-step formal definition of multi-head attention with clear notation and explicit reshape/transpose shape bookkeeping, which your current library lacks for MHA specifically.
   — covers: Formal definition of multi-head attention (per-head scaled dot-product attention) and intuition for representation subspaces, Head dimension relationships (d_model, num_heads, d_head) and scaling factor sqrt(d_head), Tensor shapes for batched multi-head attention and common reshape/transpose patterns (e.g., [B,S,D] -> [B,H,S,d_head]), Concatenation of head outputs and final linear layer; alternative implementations (stacking vs concat, einsum/matmul patterns)
- **[paper]** [[PDF] Attention is All you Need - NIPS](https://proceedings.neurips.cc/paper_files/paper/2017/file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf)
  The seminal source that precisely defines multi-head attention (including per-head projections and the final output projection) and motivates the representation-subspace intuition; it’s a foundational reference missing from the library.
   — covers: Formal definition of multi-head attention (per-head scaled dot-product attention) and intuition for representation subspaces, Learned linear projections for Q, K, V and output projection (W_Q, W_K, W_V, W_O) and how they are applied, Head dimension relationships (d_model, num_heads, d_head) and scaling factor sqrt(d_head), Concatenation of head outputs and final linear layer; alternative implementations (stacking vs concat, einsum/matmul patterns)
- **[tutorial]** [Tutorial 6: Transformers and Multi-Head Attention¶](https://uvadlc-notebooks.readthedocs.io/en/latest/tutorial_notebooks/tutorial6/Transformers_and_MHAttention.html)
  Provides implementation-oriented coverage with concrete tensor shapes and efficient PyTorch-style patterns (including combined projections and reshaping), directly addressing the practical MHA implementation gaps.
   — covers: Tensor shapes for batched multi-head attention and common reshape/transpose patterns (e.g., [B,S,D] -> [B,H,S,d_head]), How parallel attention across heads is implemented efficiently in modern frameworks (PyTorch/TF), including fused QKV projections, Concatenation of head outputs and final linear layer; alternative implementations (stacking vs concat, einsum/matmul patterns)
- **[reference_doc]** [torch.nn.MultiheadAttention — PyTorch Documentation](https://docs.pytorch.org/docs/stable/generated/torch.nn.MultiheadAttention.html)
  This is the authoritative reference for how a major framework actually implements MHA (including fused in-projection weights/biases and expected tensor layouts), directly addressing the remaining implementation-efficiency gap better than most tutorials.
   — covers: How parallel attention across heads is implemented efficiently in modern frameworks (PyTorch/TF), including fused QKV projections
- **[tutorial]** [Understanding Multi-Head Attention for ML Framework Developers (PyTorch Dev Discuss)](https://dev-discuss.pytorch.org/t/understanding-multi-head-attention-for-ml-framework-developers/1792)
  Goes deeper than typical learner-facing posts into the exact packing/unpacking, fused QKV projection, and performance-oriented shape conventions used in real implementations—highly aligned with the lesson’s implementation focus.
   — covers: How parallel attention across heads is implemented efficiently in modern frameworks (PyTorch/TF), including fused QKV projections
- **[tutorial]** [CS224N Note 10: Self-Attention & Transformers (Stanford)](https://web.stanford.edu/class/cs224n/readings/cs224n-self-attention-transformers-2023_draft.pdf)
  A high-authority Stanford teaching note that typically provides unusually clear shape/notation bookkeeping for MHA and its projections; it complements D2L by offering an independent, institution-grade explanation students often find easier to follow.
- **[reference_doc]** [torch.nn.MultiheadAttention — PyTorch Documentation](https://docs.pytorch.org/docs/stable/generated/torch.nn.MultiheadAttention.html) *(promoted by reviewer)*
  This is the authoritative reference for how a major framework actually implements MHA (including fused in-projection weights/biases and expected tensor layouts), directly addressing the remaining implementation-efficiency gap better than most tutorials.
   — fills: How parallel attention across heads is implemented efficiently in modern frameworks (PyTorch/TF), including fused QKV projections
- **[tutorial]** [Understanding Multi-Head Attention for ML Framework Developers (PyTorch Dev Discuss)](https://dev-discuss.pytorch.org/t/understanding-multi-head-attention-for-ml-framework-developers/1792) *(promoted by reviewer)*
  Goes deeper than typical learner-facing posts into the exact packing/unpacking, fused QKV projection, and performance-oriented shape conventions used in real implementations—highly aligned with the lesson’s implementation focus.
   — fills: How parallel attention across heads is implemented efficiently in modern frameworks (PyTorch/TF), including fused QKV projections
- **[tutorial]** [CS224N Note 10: Self-Attention & Transformers (Stanford)](https://web.stanford.edu/class/cs224n/readings/cs224n-self-attention-transformers-2023_draft.pdf) *(promoted by reviewer)*
  A high-authority Stanford teaching note that typically provides unusually clear shape/notation bookkeeping for MHA and its projections; it complements D2L by offering an independent, institution-grade explanation students often find easier to follow.

## Near-Misses (11) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **Linear Projections for Q, K, V per Head - ApX Machine Learni** — [Linear Projections for Q, K, V per Head - ApX Machine Learning](https://apxml.com/courses/foundations-transformers-architecture/chapter-3-multi-head-self-attention/linear-projections-qkv-heads)
  _Skipped because:_ Likely good, but your library already includes multiple ApX attention resources and this would be somewhat redundant versus adding D2L + the original paper + an implementation-focused notebook.
- **Concatenation and Final Linear Projection - ApX Machine Lear** — [Concatenation and Final Linear Projection - ApX Machine Learning](https://apxml.com/courses/foundations-transformers-architecture/chapter-3-multi-head-self-attention/concatenation-final-projection)
  _Skipped because:_ Covers a gap, but overlaps heavily with what D2L and the Vaswani paper cover more authoritatively, so it’s not the best incremental addition.
- **Multi-Head Attention Mechanism - GeeksforGeeks** — [Multi-Head Attention Mechanism - GeeksforGeeks](https://www.geeksforgeeks.org/nlp/multi-head-attention-mechanism/)
  _Skipped because:_ Generally thinner and less rigorous than D2L/UVADLC for the same concepts, so it’s not worth a slot in a high-quality curated shelf.
- **Attention | Andy Arditi** — [Attention | Andy Arditi](https://www.andyrdt.com/notes/attention)
  _Skipped because:_ Good intuition and notation, but it doesn’t beat D2L/UVADLC on end-to-end MHA tensor-shape and implementation details, so it’s not sufficiently additive.
- **The Q, K, V Matrices - Arpit Bhayani** — [The Q, K, V Matrices - Arpit Bhayani](https://arpitbhayani.me/blogs/qkv-matrices/)
  _Skipped because:_ Focuses more on QKV basics than multi-head implementation specifics, and your library already has multiple strong QKV explainers.
- **Transformer Architecture Hyperparameters: Depth, Width, Head** — [Transformer Architecture Hyperparameters: Depth, Width, Heads ...](https://mbrenndoerfer.com/writing/transformer-architecture-hyperparameters-design-guide)
  _Skipped because:_ Useful for design tradeoffs, but it’s adjacent to (not centered on) the missing MHA formalism and tensor-shape/implementation mechanics.
- **Multi-Head Attention: Parallel Attention for Richer Represen** — [Multi-Head Attention: Parallel Attention for Richer Representations](https://mbrenndoerfer.com/writing/multi-head-attention-transformers)
  _Skipped because:_ Potentially solid, but likely overlaps with D2L’s MHA chapter; the UVADLC notebook better fills the implementation-efficiency gap.
- **MoH: Multi-Head Attention as Mixture-of- ...** — [MoH: Multi-Head Attention as Mixture-of- ...](https://arxiv.org/html/2410.11842v2)
  _Skipped because:_ Researchy and not targeted at teaching the core MHA definition/shapes/implementation; better as an advanced extension after the fundamentals are covered.
- **W_K,W_V is probably all you need: On the necessity of the Qu** — [W_K,W_V is probably all you need: On the necessity of the Query ...](https://arxiv.org/html/2510.23912v4)
  _Skipped because:_ Interesting specialized research about projection necessity, but it doesn’t primarily address the foundational teaching gaps for MHA implementation.
- **[PDF] QKV Projections Require a Fraction of Their Memory - a** — [[PDF] QKV Projections Require a Fraction of Their Memory - arXiv.org](https://arxiv.org/pdf/2506.02939.pdf)
  _Skipped because:_ Optimization-focused and advanced; not the best use of limited slots for covering the missing baseline MHA mechanics.
- **Scaling Laws for Neural Language Models** — [Scaling Laws for Neural Language Models](https://cdn.jsdelivr.net/gh/yanfeng98/paper-is-all-you-need/papers/00001-scaling-laws.pdf)
  _Skipped because:_ Not directly about multi-head attention representation subspaces or implementation details; it doesn’t target the stated gaps.

## Uncovered Gaps (1) — No Good Candidates Found
_Consider manually sourcing these, or run enrichment again with different search terms._

- How parallel attention across heads is implemented efficiently in modern frameworks (PyTorch/TF), including fused QKV projections

## Reasoning
**Curator:** Added one authoritative textbook chapter (D2L), the seminal original paper (Vaswani et al.), and one implementation-heavy notebook (UVADLC) to cover formal definition, projections, dimensions, and tensor-shape mechanics without redundancy. The remaining efficiency/fused-kernel details are only partially addressed by candidates and would benefit from a framework reference doc or kernel-level writeup not present here.
**Reviewer:** The curator’s core picks (Vaswani + D2L + an implementation notebook) are strong, but adding PyTorch’s official MHA docs and the PyTorch dev-focused explainer would materially close the remaining fused-QKV/efficient-implementation gap, with CS224N as an additional high-authority teaching reference.

---

# Curation Report: Scaled Dot-Product Attention: Math, Masking, and Stability
**Topic:** `self-attention` | **Date:** 2026-04-08 11:02
**Library:** 24 existing → 28 sources (4 added, 1 downloaded, 2 failed)
**Candidates evaluated:** 18
**Reviewer verdict:** needs_additions

## Added (4)
- **[tutorial]** [Attention Masking: Controlling Information Flow in Transformers](https://mbrenndoerfer.com/writing/attention-masking-transformers)
  Adds a focused, implementation-oriented explanation of causal (look-ahead) masking as an additive pre-softmax score/logit mask (e.g., -inf), which is a core gap not covered cleanly by the current library’s broader attention intros.
   — covers: Causal (look-ahead) masking in scaled dot-product attention: definition, why it prevents attending to future tokens, and how it is applied to the score matrix (additive -inf mask before softmax)., Definition and usage of logits in attention: pre-softmax attention scores (QK^T/sqrt(d_k) + mask), terminology, and examples.
- **[reference_doc]** [[PDF] From Online Softmax to FlashAttention](https://courses.cs.washington.edu/courses/cse599m/23sp/notes/flashattn.pdf)
  Provides an authoritative, math-forward treatment of numerically stable softmax (online/max-subtraction/log-sum-exp style) in the exact context of attention, including practical stability considerations that typical transformer tutorials omit.
   — covers: Softmax numerical stability in attention: subtracting max logit, avoiding overflow/underflow, stable handling of masked positions (-inf), and practical implementation notes.
- **[paper]** [Attention Is All You Need](https://arxiv.org/html/1706.03762v7)
  Even though an arXiv entry is already in the library, the canonical Transformer paper is the primary citable source that explicitly motivates and defines masking (both look-ahead and padding) in scaled dot-product attention; it should be included as the definitive reference rather than relying on secondary tutorials.
   — covers: Padding masks: masking pad tokens in attention, typical shapes/broadcasting across heads and query positions, and interaction with variable-length batches.
- **[paper]** [Attention Is All You Need](https://arxiv.org/html/1706.03762v7) *(promoted by reviewer)*
  Even though an arXiv entry is already in the library, the canonical Transformer paper is the primary citable source that explicitly motivates and defines masking (both look-ahead and padding) in scaled dot-product attention; it should be included as the definitive reference rather than relying on secondary tutorials.
   — fills: Padding masks: masking pad tokens in attention, typical shapes/broadcasting across heads and query positions, and interaction with variable-length batches.

## Near-Misses (12) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **Scaled Dot-Product Attention and Masking in Transformers** — [Scaled Dot-Product Attention and Masking in Transformers](https://codesignal.com/learn/courses/sequence-models-the-dawn-of-attention-1/lessons/scaled-dot-product-attention-and-masking-in-transformers-1)
  _Skipped because:_ Likely covers causal/padding masks, but it’s on a course platform with uncertain long-term accessibility and tends to be less citable/stable than standalone references.
- **Masked Self-Attention in Decoders** — [Masked Self-Attention in Decoders](https://apxml.com/courses/foundations-transformers-architecture/chapter-5-encoder-decoder-stacks/masked-self-attention)
  _Skipped because:_ Redundant with existing ApX coverage already in the library and unlikely to add substantially beyond what you have from ApX plus standard transformer explainers.
- **Practice: Implement Scaled Dot-Product Attention** — [Practice: Implement Scaled Dot-Product Attention](https://apxml.com/courses/introduction-to-transformer-models/chapter-2-self-attention-multi-head-attention/practice-scaled-dot-product-attention)
  _Skipped because:_ Practice-oriented and probably helpful, but overlaps heavily with existing scaled dot-product attention resources and doesn’t clearly add the missing padding-mask shape/broadcasting details.
- **A Gentle Introduction to Attention Masking in Transformer Mo** — [A Gentle Introduction to Attention Masking in Transformer Models](https://machinelearningmastery.com/a-gentle-introduction-to-attention-masking-in-transformer-models/)
  _Skipped because:_ Often mixes solid intuition with promotional framing and tends to be lighter on precise mask shapes/broadcasting and pre-softmax additive masking details than more technical references.
- **Silent Tokens, Loud Effects: Padding in LLMs** — [Silent Tokens, Loud Effects: Padding in LLMs](https://arxiv.org/html/2510.01238v1)
  _Skipped because:_ Potentially relevant to padding effects, but it’s not clearly targeted at the practical “how to implement padding masks (shapes/broadcasting)” gap for scaled dot-product attention.
- **Enhancing Training Efficiency Using Packing with Flash Atten** — [Enhancing Training Efficiency Using Packing with Flash Attention](https://arxiv.org/html/2407.09105v6)
  _Skipped because:_ More about efficiency/packing than the foundational padding-mask mechanics and broadcasting patterns you’re trying to fill.
- **Padding and Attention Masks in LLMs: Preparing Batches for T** — [Padding and Attention Masks in LLMs: Preparing Batches for Training](https://www.youtube.com/watch?v=fwI_tVHcg4Q)
  _Skipped because:_ Could be useful, but video quality/precision is hard to verify from metadata alone and it’s less stable/citable than a strong written reference for mask shapes and broadcasting.
- **Implementing Softmax From Scratch: Avoiding the Numerical ..** — [Implementing Softmax From Scratch: Avoiding the Numerical ...](https://www.marktechpost.com/2026/01/06/implementing-softmax-from-scratch-avoiding-the-numerical-stability-trap/)
  _Skipped because:_ Covers generic softmax stability but is not attention-specific and is from a news/blog aggregator style site, making it less authoritative than the UW FlashAttention notes.
- **Implementing Softmax From Scratch: Avoiding the ...** — [Implementing Softmax From Scratch: Avoiding the ...](https://www.marktechpost.com/2026/01/06/implementing-softmax-from-scratch-avoiding-the-numerical-stability-trap/?amp)
  _Skipped because:_ Same content concerns as the non-AMP version and adds no additional value.
- **Numerical Stability in Flash Attention - - jarbus** — [Numerical Stability in Flash Attention - - jarbus](https://jarbus.net/blog/numerical-stability-in-flash-attention/)
  _Skipped because:_ Likely good, but the UW course notes are a more authoritative and durable reference for the same stability topic.
- **Artifact 2.2b: FlashAttention — Online Softmax - Hugging Fac** — [Artifact 2.2b: FlashAttention — Online Softmax - Hugging Face](https://huggingface.co/blog/atharv6f/flash-attention-online-softmax)
  _Skipped because:_ Potentially strong, but overlaps with the UW notes; keeping the library lean favors the more canonical PDF reference.
- **LLM breakdown 5/6: Attention - by Mike X Cohen, PhD** — [LLM breakdown 5/6: Attention - by Mike X Cohen, PhD](https://mikexcohen.substack.com/p/llm-breakdown-56-attention)
  _Skipped because:_ Explains Q/K/V and the pre-softmax scores, but it’s a Substack post (paywall/availability can change) and overlaps with existing QKV/attention explainers already in the library.

## Uncovered Gaps (1) — No Good Candidates Found
_Consider manually sourcing these, or run enrichment again with different search terms._

- Padding masks: masking pad tokens in attention, typical shapes/broadcasting across heads and query positions, and interaction with variable-length batches.

## Reasoning
**Curator:** The best improvements are (1) a focused, stable tutorial on additive causal masking at the logit/score-matrix level and (2) an authoritative reference on numerically stable softmax in attention; none of the candidates clearly and reliably nails the practical padding-mask shape/broadcasting details without quality or redundancy concerns.
**Reviewer:** The additions on causal masking and softmax stability are strong, but the library still needs an explicit canonical reference for padding masking (and the existing Transformer paper entry should be made unambiguously the official citation).

---

# Curation Report: Luong (Multiplicative) Attention and Variants
**Topic:** `self-attention` | **Date:** 2026-04-08 11:13
**Library:** 25 existing → 33 sources (8 added, 3 downloaded, 1 failed)
**Candidates evaluated:** 14
**Reviewer verdict:** needs_additions

## Added (8)
- **[paper]** [[PDF] Effective Approaches to Attention-based Neural Machine Translation](https://nlp.stanford.edu/pubs/emnlp15_attn.pdf)
  This is the primary Luong et al. source and gives the definitive, implementable description of global vs. local attention, including local-m/local-p, predicted alignment position, windowing, and the optional Gaussian weighting—details not covered cleanly in the current library.
   — covers: Global attention mechanics in Luong et al. (context vector over all encoder states; alignment weights via softmax over scores), Local attention mechanics in Luong et al.: monotonic/local-p and local-m variants, predicted alignment position, window size, and optional Gaussian weighting
- **[tutorial]** [Luong Attention: Dot Product, General & Local Attention Mechanisms](https://mbrenndoerfer.com/writing/luong-attention-mechanisms-dot-product-general-local)
  A clear, formula-forward walkthrough that explicitly distinguishes Luong dot vs. general (q^T W k) scoring and ties them to the global attention computation (softmax alignment over encoder states), which is currently a stated gap.
   — covers: Explicit definition and formula of Luong (multiplicative) attention scoring functions: dot, general (q^T W k), and (optionally) concat, Clear distinction between 'dot-product attention' and 'general attention' within Luong attention, Global attention mechanics in Luong et al. (context vector over all encoder states; alignment weights via softmax over scores)
- **[paper]** [Neural Machine Translation by Jointly Learning to Align and Translate (Bahdanau et al., 2014)](https://arxiv.org/abs/1409.0473)
  Even though the lesson is Luong-focused, this is the seminal additive-attention paper and the cleanest primary source for the additive vs. multiplicative comparison the gaps call out; it also provides the canonical formulation to contrast parameterization and per-step computation.
   — covers: Computational tradeoffs: additive (Bahdanau) vs multiplicative (Luong) attention—parameterization, matrix multiplications, and relative efficiency
- **[tutorial]** [Stanford CS224N (NLP with Deep Learning) — Attention / Seq2Seq lecture notes](https://web.stanford.edu/class/cs224n/)
  A high-authority, stable institutional reference that typically includes side-by-side additive vs. multiplicative attention scoring, shapes, and computational considerations; it’s a strong “teaching wiki” anchor beyond blogs.
   — covers: Computational tradeoffs: additive (Bahdanau) vs multiplicative (Luong) attention—parameterization, matrix multiplications, and relative efficiency
- **[tutorial]** [Dive into Deep Learning — 11.3 Attention Scoring Functions](https://d2l.ai/chapter_attention-mechanisms-and-transformers/attention-scoring-functions.html)
  This is already in the library but should be explicitly elevated in the Luong-variants lesson because it gives a textbook-style, implementation-oriented comparison of additive vs. dot-product/general scoring that directly supports the stated tradeoff gap.
   — covers: Computational tradeoffs: additive (Bahdanau) vs multiplicative (Luong) attention—parameterization, matrix multiplications, and relative efficiency
- **[paper]** [Neural Machine Translation by Jointly Learning to Align and Translate (Bahdanau et al., 2014)](https://arxiv.org/abs/1409.0473) *(promoted by reviewer)*
  Even though the lesson is Luong-focused, this is the seminal additive-attention paper and the cleanest primary source for the additive vs. multiplicative comparison the gaps call out; it also provides the canonical formulation to contrast parameterization and per-step computation.
   — fills: Computational tradeoffs: additive (Bahdanau) vs multiplicative (Luong) attention—parameterization, matrix multiplications, and relative efficiency
- **[tutorial]** [Stanford CS224N (NLP with Deep Learning) — Attention / Seq2Seq lecture notes](https://web.stanford.edu/class/cs224n/) *(promoted by reviewer)*
  A high-authority, stable institutional reference that typically includes side-by-side additive vs. multiplicative attention scoring, shapes, and computational considerations; it’s a strong “teaching wiki” anchor beyond blogs.
   — fills: Computational tradeoffs: additive (Bahdanau) vs multiplicative (Luong) attention—parameterization, matrix multiplications, and relative efficiency
- **[tutorial]** [Dive into Deep Learning — 11.3 Attention Scoring Functions](https://d2l.ai/chapter_attention-mechanisms-and-transformers/attention-scoring-functions.html) *(promoted by reviewer)*
  This is already in the library but should be explicitly elevated in the Luong-variants lesson because it gives a textbook-style, implementation-oriented comparison of additive vs. dot-product/general scoring that directly supports the stated tradeoff gap.
   — fills: Computational tradeoffs: additive (Bahdanau) vs multiplicative (Luong) attention—parameterization, matrix multiplications, and relative efficiency

## Near-Misses (12) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **4. Bahdanau Attention** — [4. Bahdanau Attention](https://www.baeldung.com/cs/attention-luong-vs-bahdanau)
  _Skipped because:_ Potentially useful for tradeoffs, but it appears to substantially overlap with other generic explainers and is less authoritative than adding the original Luong paper plus a focused Luong-specific tutorial.
- **Chapter 8 Attention and Self-Attention for NLP** — [Chapter 8 Attention and Self-Attention for NLP](https://slds-lmu.github.io/seminar_nlp_ss20/attention-and-self-attention-for-nlp.html)
  _Skipped because:_ Likely covers scoring-function basics, but it’s broader course notes and would be redundant once the Luong paper and a dedicated Luong scoring tutorial are included.
- **The Luong Attention Mechanism - MachineLearningMastery.com** — [The Luong Attention Mechanism - MachineLearningMastery.com](https://machinelearningmastery.com/the-luong-attention-mechanism/)
  _Skipped because:_ Often clear but tends to be higher-level and less precise/primary-source-aligned than the added Luong-specific tutorial and the original paper.
- **Luong Attention: A Comprehensive Guide for 2025 - Shadecoder** — [Luong Attention: A Comprehensive Guide for 2025 - Shadecoder](https://www.shadecoder.com/topics/luong-attention-a-comprehensive-guide-for-2025)
  _Skipped because:_ Unclear authoritativeness and long-term stability; overlaps with better, more reputable Luong-focused material.
- **Bahdanau vs Luong Attention: Which One Should You ...** — [Bahdanau vs Luong Attention: Which One Should You ...](https://blog.sotaaz.com/post/attention-mechanism-implementation-en)
  _Skipped because:_ Covers the tradeoff angle, but the source is blog-level and not clearly more rigorous than existing materials; better to rely on primary papers/textbook-style references for efficiency/complexity claims.
- **Which One Should You Actually Use? (Spoiler: Luong) | SOTAAZ** — [Which One Should You Actually Use? (Spoiler: Luong) | SOTAAZ Blog](https://www.sotaaz.com/blog/attention-mechanism-implementation-en)
  _Skipped because:_ Same content class as the other SOTAAZ URL and not sufficiently authoritative for a curated “best resources” shelf.
- **What is an attention mechanism?** — [What is an attention mechanism?](https://www.ibm.com/think/topics/attention-mechanism)
  _Skipped because:_ Too general for the specific Luong global/local mechanics and scoring-function distinctions you’re trying to fill.
- **Aman's AI Journal • Natural Language Processing • Attention** — [Aman's AI Journal • Natural Language Processing • Attention](https://aman.ai/primers/ai/attention/)
  _Skipped because:_ Broad attention overview; likely helpful but not specifically targeted enough to Luong local/global variants and exact scoring definitions to justify inclusion here.
- **arXiv:1508.04025v5  [cs.CL]  20 Sep 2015** — [arXiv:1508.04025v5  [cs.CL]  20 Sep 2015](https://arxiv.org/pdf/1508.04025v5.pdf)
  _Skipped because:_ Redundant with the Stanford-hosted PDF of the same paper, which is the cleaner canonical link to keep.
- **[PDF] arXiv:1508.04025v5 [cs.CL] 20 Sep 2015** — [[PDF] arXiv:1508.04025v5 [cs.CL] 20 Sep 2015](https://arxiv.org/pdf/1508.04025.pdf)
  _Skipped because:_ Redundant with the Stanford-hosted PDF of the same paper.
- **emnlp15.dvi** — [emnlp15.dvi](https://www-nlp.stanford.edu/pubs/emnlp15_attn.pdf)
  _Skipped because:_ Duplicate mirror of the same PDF; keep a single canonical Stanford link.
- **Effective Approaches to Attention-based Neural Machine ...** — [Effective Approaches to Attention-based Neural Machine ...](https://aclanthology.org/anthology-files/pdf/D/D15/D15-1166.pdf)
  _Skipped because:_ Also the same paper; the Stanford PDF is sufficient as the canonical addition.

## Uncovered Gaps (1) — No Good Candidates Found
_Consider manually sourcing these, or run enrichment again with different search terms._

- Computational tradeoffs: additive (Bahdanau) vs multiplicative (Luong) attention—parameterization, matrix multiplications, and relative efficiency (especially for large hidden sizes), including complexity per decoding step

## Reasoning
**Curator:** The best way to fill the Luong-specific gaps is to add the original Luong et al. paper for authoritative global/local mechanics, plus one high-quality tutorial that explicitly lays out and contrasts the Luong scoring functions. The remaining candidates are either duplicates, too general, or insufficiently authoritative to improve the shelf.
**Reviewer:** The curator’s Luong-specific additions are strong, but the shelf still lacks a primary-source anchor for additive attention and at least one high-authority course/text reference that explicitly discusses additive vs. multiplicative computational tradeoffs.

---

# Curation Report: Luong (Multiplicative) Attention and Variants
**Topic:** `self-attention` | **Date:** 2026-04-09 15:49
**Library:** 28 existing → 31 sources (3 added, 2 downloaded)
**Candidates evaluated:** 17
**Reviewer verdict:** good

## Added (3)
- **[paper]** [[PDF] Effective Approaches to Attention-based Neural Machine Translation](https://nlp.stanford.edu/pubs/emnlp15_attn.pdf)
  Authoritative primary source for Luong attention: precisely defines dot/general/concat scoring and the global vs. local attention mechanisms (including predicted alignment position and windowing) with full equations and algorithmic details.
   — covers: Luong 'general' / bilinear attention: score=q^T W k, parameterization, relation to dot-product, Luong attention variants: 'dot', 'general', and (if included) 'concat' scoring; how they compare to Bahdanau additive attention, Global vs local attention in Luong et al. (2015): how local attention selects a subset (window) and/or predicts alignment position; equations and algorithm steps
- **[paper]** [Effective Approaches to Attention-based Neural Machine Translation (Luong et al., 2015) — arXiv abstract page](https://arxiv.org/abs/1508.04025)
  Even if a Stanford-hosted PDF is preferred, keeping the canonical arXiv landing page is valuable for stable citation metadata, versioning, and long-term discoverability; it’s the primary seminal source for Luong attention variants.
- **[paper]** [Effective Approaches to Attention-based Neural Machine Translation (Luong et al., 2015) — arXiv abstract page](https://arxiv.org/abs/1508.04025) *(promoted by reviewer)*
  Even if a Stanford-hosted PDF is preferred, keeping the canonical arXiv landing page is valuable for stable citation metadata, versioning, and long-term discoverability; it’s the primary seminal source for Luong attention variants.

## Near-Misses (14) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **[PDF] arXiv:1508.04025v5 [cs.CL] 20 Sep 2015** — [[PDF] arXiv:1508.04025v5 [cs.CL] 20 Sep 2015](https://arxiv.org/pdf/1508.04025.pdf)
  _Skipped because:_ Redundant with the already-in-library arXiv abstract page for the same paper; prefer the stable Stanford-hosted PDF.
- **arXiv:1508.04025v5  [cs.CL]  20 Sep 2015** — [arXiv:1508.04025v5  [cs.CL]  20 Sep 2015](http://arxiv.org/pdf/1508.04025v5.pdf)
  _Skipped because:_ Same content as the chosen PDF but less canonical than the Stanford-hosted version.
- **Scaled Dot-Product Attention and Masking in Transformers** — [Scaled Dot-Product Attention and Masking in Transformers](https://codesignal.com/learn/courses/sequence-models-the-dawn-of-attention-1/lessons/scaled-dot-product-attention-and-masking-in-transformers-1)
  _Skipped because:_ Likely overlaps heavily with existing dot-product/scaled-dot-product explanations already in the library (D2L + multiple tutorials), without clear unique depth on Luong-specific variants.
- **4. Bahdanau Attention** — [4. Bahdanau Attention](https://www.baeldung.com/cs/attention-luong-vs-bahdanau)
  _Skipped because:_ Secondary overview that tends to be higher-level and potentially imprecise (e.g., conflating Luong with scaled dot-product); not needed given stronger existing sources and the primary paper.
- **The Luong Attention Mechanism - MachineLearningMastery.com** — [The Luong Attention Mechanism - MachineLearningMastery.com](https://machinelearningmastery.com/the-luong-attention-mechanism/)
  _Skipped because:_ Blog-level treatment that is often verbose and less rigorous than the primary paper and existing high-quality tutorials already included.
- **[PDF] I want to know what attention is I want you to show me** — [[PDF] I want to know what attention is I want you to show me - Simon Šuster](https://simonsuster.github.io/talks/attention_ML_RG.pdf)
  _Skipped because:_ Slide deck format is less stable as a reference and typically less complete on Luong local/global algorithmic details than the original paper.
- **[PDF] Class Notes: Attention Mechanisms in Neural Networks** — [[PDF] Class Notes: Attention Mechanisms in Neural Networks](https://www.khoury.northeastern.edu/home/vip/teach/MLcourse/7_adv_NN/notes/chatGPT_responses/attention_mechanisms_tikz.pdf)
  _Skipped because:_ Course notes of unclear provenance/maintenance and not as authoritative or citable as the original Luong et al. paper.
- **Bahdanau vs Luong Attention: Which One Should You ...** — [Bahdanau vs Luong Attention: Which One Should You ...](https://blog.sotaaz.com/post/attention-mechanism-implementation-en)
  _Skipped because:_ Unclear authoritativeness and likely redundant with existing comparisons and the primary paper.
- **Attention Mechanism Bahdanau attention vs Luong ... - CSDN博客** — [Attention Mechanism Bahdanau attention vs Luong ... - CSDN博客](https://blog.csdn.net/IT_flying625/article/details/103498539)
  _Skipped because:_ Blog repost/aggregation with variable quality and stability; not suitable for a high-quality curated shelf.
- **Chapter 8 Attention and Self-Attention for NLP** — [Chapter 8 Attention and Self-Attention for NLP](https://slds-lmu.github.io/seminar_nlp_ss20/attention-and-self-attention-for-nlp.html)
  _Skipped because:_ Potentially useful, but likely overlaps with existing D2L/CS224N coverage and is not clearly focused on Luong local attention mechanics beyond a summary.
- **(2015. 8) Luong Attention | HumanBrain** — [(2015. 8) Luong Attention | HumanBrain](https://humanbrain.gitbook.io/notes/notes/natural-language-processing/luong_attention)
  _Skipped because:_ Looks like brief notes/summaries; not a sufficiently deep or authoritative treatment compared to the original paper.
- **Efficient Attention: Attention with Linear Complexities** — [Efficient Attention: Attention with Linear Complexities](https://arxiv.org/pdf/1812.01243.pdf)
  _Skipped because:_ High-quality but focuses on efficient attention for vision/transformer-style dot-product attention rather than the specific additive-vs-multiplicative and global-vs-local trade-offs in Luong seq2seq attention.
- **A Comparative Study of Resource Utilization for Variants ...** — [A Comparative Study of Resource Utilization for Variants ...](https://arxiv.org/html/2507.07247)
  _Skipped because:_ Unclear maturity/authority and likely broader than Luong attention; not obviously the best source to fill the specific cost/trade-off gap.
- **Aman's AI Journal • Natural Language Processing • Attention** — [Aman's AI Journal • Natural Language Processing • Attention](https://aman.ai/primers/ai/attention/)
  _Skipped because:_ Good general primer, but the library already has multiple strong general attention explanations; not clearly adding unique Luong-specific depth.

## Uncovered Gaps (2) — No Good Candidates Found
_Consider manually sourcing these, or run enrichment again with different search terms._

- Explicit definition and mechanics of dot-product (multiplicative) attention: score=q·k (optionally scaled), softmax weights, context vector computation, worked example
- Computational cost and practical trade-offs: additive vs multiplicative attention complexity, parameter counts, speed on GPU/CPU; global vs local runtime/memory implications

## Reasoning
**Curator:** The only candidate that clearly and authoritatively fills multiple Luong-specific gaps without redundancy is the original Luong et al. (2015) PDF, which provides the definitive equations and global/local variants. Other candidates are either redundant with existing dot-product resources or are lower-authority summaries that don’t add enough beyond the primary paper and current library.
**Reviewer:** The curation is already strong for Luong attention definitions/variants via the primary paper and multiple high-quality tutorials; the only worthwhile addition from the provided near-misses/candidates is retaining the canonical arXiv landing page for the Luong et al. paper, while the remaining candidates skew toward efficient self-attention rather than Luong-specific gaps.

---

# Curation Report: Scaled Dot-Product Attention: Math and Implementation
**Topic:** `self-attention` | **Date:** 2026-04-11 17:51
**Library:** 29 existing → 37 sources (8 added, 6 downloaded)
**Candidates evaluated:** 20
**Reviewer verdict:** needs_additions

## Added (8)
- **[video]** [[PDF] Lecture 8: Attention and Transformers - CS231n](https://cs231n.stanford.edu/slides/2025/lecture_8.pdf)
  High-quality Stanford course slides that explicitly walk through scaled dot-product attention in matrix form with shapes (QK^T, scaling, row-wise softmax, AV) and typically include the batched/multi-head reshaping view used in efficient implementations.
   — covers: Full matrix-operations walkthrough of scaled dot-product attention with tensor shapes: QK^T, scaling, row-wise softmax to form attention matrix A, and AV to produce outputs, Vectorized/batched implementation details (multi-head reshaping, efficient matmul patterns, avoiding Python loops)
- **[video]** [Henry Chai & Matt Gormley](http://www.cs.cmu.edu/~mgormley/courses/10423-f24/slides/lecture3-learning.pdf)
  CMU lecture slides that clearly present scaled dot-product attention step-by-step and in matrix form, including the key detail of which dimension softmax is applied over (row-wise normalization), helping close the shapes/operations gap.
   — covers: Full matrix-operations walkthrough of scaled dot-product attention with tensor shapes: QK^T, scaling, row-wise softmax to form attention matrix A, and AV to produce outputs
- **[paper]** [IMA Journal of Numerical Analysis (2021) 41, 2311–2330](https://academic.oup.com/imajna/article-pdf/41/4/2311/40758053/draa038.pdf)
  Authoritative numerical analysis treatment of stable softmax/log-sum-exp (shifted formulations, overflow/underflow, low-precision considerations), providing a rigorous foundation for attention softmax stability beyond typical ML blog-level explanations.
   — covers: Numerical stability in softmax for attention (subtract max/log-sum-exp, masking with -inf, fp16/bf16 considerations)
- **[tutorial]** [Numerical Stability in Flash Attention - - jarbus](https://jarbus.net/blog/numerical-stability-in-flash-attention/)
  Practical, attention-specific discussion of numerically stable softmax as implemented in FlashAttention-style kernels, including how stability is maintained under fp16/bf16 and masking—directly applicable to real implementations.
   — covers: Numerical stability in softmax for attention (subtract max/log-sum-exp, masking with -inf, fp16/bf16 considerations), Vectorized/batched implementation details (multi-head reshaping, efficient matmul patterns, avoiding Python loops)
- **[tutorial]** [Notes on implementing Attention](https://eli.thegreenplace.net/2025/notes-on-implementing-attention/)
  This is unusually implementation-forward and explicit about tensor shapes, masking, and numerically stable softmax in real code—exactly the “math-to-vectorized-implementation” bridge learners struggle with.
   — covers: Softmax definition and formula, including an explicit example on attention logits and how it normalizes rows
- **[tutorial]** [Multi-Head Attention From Scratch (Part 1 of Understanding Transformers Architecture)](https://sanjayasubedi.com.np/deeplearning/multihead-attention-from-scratch/)
  Despite being a blog, it directly targets the missing “from-scratch” vectorized MHA reshape/matmul pipeline and typically includes concrete row-wise softmax usage on attention logits; it complements (not replaces) the Stanford/CMU slides with runnable detail.
   — covers: Softmax definition and formula, including an explicit example on attention logits and how it normalizes rows
- **[tutorial]** [Notes on implementing Attention](https://eli.thegreenplace.net/2025/notes-on-implementing-attention/) *(promoted by reviewer)*
  This is unusually implementation-forward and explicit about tensor shapes, masking, and numerically stable softmax in real code—exactly the “math-to-vectorized-implementation” bridge learners struggle with.
   — fills: Softmax definition and formula, including an explicit example on attention logits and how it normalizes rows
- **[tutorial]** [Multi-Head Attention From Scratch (Part 1 of Understanding Transformers Architecture)](https://sanjayasubedi.com.np/deeplearning/multihead-attention-from-scratch/) *(promoted by reviewer)*
  Despite being a blog, it directly targets the missing “from-scratch” vectorized MHA reshape/matmul pipeline and typically includes concrete row-wise softmax usage on attention logits; it complements (not replaces) the Stanford/CMU slides with runnable detail.
   — fills: Softmax definition and formula, including an explicit example on attention logits and how it normalizes rows

## Near-Misses (11) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **Softmax function - Wikipedia** — [Softmax function - Wikipedia](https://en.wikipedia.org/wiki/Softmax_function)
  _Skipped because:_ Good general reference, but it’s not attention-specific (row-wise normalization on attention logits, masking, fp16/bf16) and is less aligned with the implementation-focused gaps than the selected sources.
- **Stable softmax for sparse matrices** — [Stable softmax for sparse matrices](https://peterbloem.nl/blog/stable-softmax)
  _Skipped because:_ Useful stability notes, but it’s oriented toward sparse-matrix contexts and is less directly tied to attention masking and modern fp16/bf16 transformer implementations than the FlashAttention-focused writeup.
- **nGPT: Normalized Transformer with Representation Learning ..** — [nGPT: Normalized Transformer with Representation Learning ... - arXiv](https://arxiv.org/html/2410.01131v1)
  _Skipped because:_ Mentions softmax and attention, but the paper’s core contribution is normalized representations rather than teaching softmax with explicit attention-logit examples or implementation/stability details.
- **The Softmax Function for Attention Weights** — [The Softmax Function for Attention Weights](https://apxml.com/courses/foundations-transformers-architecture/chapter-2-attention-mechanism-core-concepts/softmax-attention-weights)
  _Skipped because:_ Likely helpful, but it appears to overlap heavily with existing ApX coverage already in the library and doesn’t clearly add unique depth on stability or vectorized implementation.
- **Softmax Attention Mechanism** — [Softmax Attention Mechanism](https://www.emergentmind.com/topics/softmax-attention-mechanism)
  _Skipped because:_ Aggregator-style content is typically less stable/authoritative and often redundant with stronger primary sources (course notes, textbooks, or papers).
- **Scaled Dot-Product Attention: Ungraded Lab - AIBook - Rahul ** — [Scaled Dot-Product Attention: Ungraded Lab - AIBook - Rahul Saraf](https://aibook.zealmaker.com/nlp/dlai4/c4_w1_ungraded_lab_2_qkv_attention)
  _Skipped because:_ Potentially useful as a lab, but it’s a third-party repost of course material and is less authoritative/stable than the original university course slides added.
- **Scaled Dot-Product Attention | Abhik Sarkar** — [Scaled Dot-Product Attention | Abhik Sarkar](https://www.abhik.ai/concepts/attention/scaled-dot-product)
  _Skipped because:_ Covers the basic walkthrough, but it’s redundant with higher-authority course materials (CS231n/CMU) for the same matrix-form/shapes gap.
- **Scalable-Softmax Is Superior for Attention** — [Scalable-Softmax Is Superior for Attention](https://arxiv.org/html/2501.19399v1)
  _Skipped because:_ Research-focused and potentially valuable, but it’s about proposing an alternative softmax variant rather than clearly teaching the standard stable softmax/masking mechanics needed for this lesson.
- **Softplus Attention with Re-weighting Boosts Length Extrapola** — [Softplus Attention with Re-weighting Boosts Length Extrapolation in ...](https://arxiv.org/html/2501.13428v3)
  _Skipped because:_ Focuses on an alternative attention nonlinearity for extrapolation, not on the core softmax definition/example or standard implementation/stability details.
- **The Softmax Function Exponentiation Normalization and the ..** — [The Softmax Function Exponentiation Normalization and the ...](https://emberverse.ai/stage1/the_softmax_function_exponentiation_normalization_and_the_competition_for_attent.html)
  _Skipped because:_ Unclear authorship/authority and likely introductory; doesn’t convincingly add beyond stronger references and course materials.
- **Supplementary Material for Kernel Identification** — [Supplementary Material for Kernel Identification](https://proceedings.neurips.cc/paper_files/paper/2021/file/56c3b2c6ea3a83aaeeff35eeb45d700d-Supplemental.pdf)
  _Skipped because:_ Not a primary teaching resource for attention; any attention recap inside is incidental and not the focus.

## Uncovered Gaps (1) — No Good Candidates Found
_Consider manually sourcing these, or run enrichment again with different search terms._

- Softmax definition and formula, including an explicit example on attention logits and how it normalizes rows

## Reasoning
**Curator:** Priority was given to authoritative course materials for the matrix/shapes and vectorization gaps, and to rigorous + implementation-relevant sources for numerical stability. None of the candidates clearly provide a high-quality, attention-specific softmax worked example that explicitly demonstrates row-wise normalization on attention logits.
**Reviewer:** The curator’s additions are strong for matrix-form attention and stability, but adding one or two implementation-centric sources that explicitly spell out row-wise softmax on attention logits would better close the remaining gap.

---

# Curation Report: Scaled Dot-Product Attention: Math and Implementation
**Topic:** `self-attention` | **Date:** 2026-04-11 17:57
**Library:** 35 existing → 37 sources (2 added, 2 downloaded)
**Candidates evaluated:** 16
**Reviewer verdict:** good

## Added (2)
- **[reference_doc]** [Softmax function - Wikipedia](https://en.wikipedia.org/wiki/Softmax_function)
  Adds a stable, canonical reference for the softmax definition, normalization properties, and the Jacobian/gradient—useful for precisely stating row-wise softmax behavior in attention and discussing gradient behavior.
   — covers: Softmax definition and mechanics (formula, normalization, row-wise application in attention, gradient behavior)
- **[paper]** [1 Introduction - arXiv](https://arxiv.org/html/2510.21770v1)
  Provides unusually direct, implementation-facing treatment of row-wise softmax (including its Jacobian) under floating-point models and diagnostics, which helps address numerical stability concerns in attention beyond what typical tutorials cover.
   — covers: Softmax definition and mechanics (formula, normalization, row-wise application in attention, gradient behavior), Numerical stability in softmax/attention implementations (subtract max logits, handling masking with -inf, fp16/bf16 stability)

## Near-Misses (13) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **The Softmax Function for Attention Weights** — [The Softmax Function for Attention Weights](https://apxml.com/courses/foundations-transformers-architecture/chapter-2-attention-mechanism-core-concepts/softmax-attention-weights)
  _Skipped because:_ Likely overlaps heavily with existing ApX attention material already in the library and is less authoritative than a standard reference for softmax mechanics/gradients.
- **Scaled Dot-Product Attention and Masking in Transformers** — [Scaled Dot-Product Attention and Masking in Transformers](https://codesignal.com/learn/courses/sequence-models-the-dawn-of-attention-1/lessons/scaled-dot-product-attention-and-masking-in-transformers-1)
  _Skipped because:_ Covers shapes/masking but appears to be a platform lesson with uncertain long-term stability/access and is redundant with existing D2L/CS lecture notes and implementation notes.
- **Scaled Dot-Product Attention Mechanism** — [Scaled Dot-Product Attention Mechanism](https://apxml.com/courses/introduction-to-transformer-models/chapter-2-self-attention-multi-head-attention/scaled-dot-product-attention)
  _Skipped because:_ Redundant with existing ApX scaled dot-product attention coverage already present in the library.
- **[PDF] Self-Adjust Softmax - ACL Anthology** — [[PDF] Self-Adjust Softmax - ACL Anthology](https://aclanthology.org/2025.emnlp-main.397.pdf)
  _Skipped because:_ Research on a modified softmax rather than a clear, foundational treatment of standard softmax mechanics/implementation for attention.
- **Statistical Advantage of Softmax Attention: Insights from Si** — [Statistical Advantage of Softmax Attention: Insights from Single ...](https://arxiv.org/pdf/2509.21936v1.pdf)
  _Skipped because:_ Focuses on theoretical/statistical properties rather than practical softmax/attention mechanics, stability, and vectorized implementation details targeted by the gaps.
- **Softplus Attention with Re-weighting Boosts Length ...** — [Softplus Attention with Re-weighting Boosts Length ...](https://arxiv.org/html/2501.13428v2)
  _Skipped because:_ Primarily proposes an alternative to softmax attention; does not directly strengthen the core implementation/stability understanding of standard scaled dot-product attention.
- **Low-Precision Transformer Training with Flash Attention** — [Low-Precision Transformer Training with Flash Attention](https://www.emergentmind.com/papers/2510.04212)
  _Skipped because:_ Secondary aggregator page rather than the primary paper URL; also likely overlaps with existing FlashAttention/numerical-stability resources without guaranteeing additional core coverage.
- **Reimplementing FlashAttention for performance and giggles** — [Reimplementing FlashAttention for performance and giggles](https://aminediro.com/posts/flash_attn/)
  _Skipped because:_ Potentially useful, but blog-level and may be redundant with the existing numerical-stability-in-FlashAttention resource already in the library.
- **Transformer Attention: A Guide to the Q, K, and V Matrices -** — [Transformer Attention: A Guide to the Q, K, and V Matrices - billparker.ai](https://www.billparker.ai/2024/10/transformer-attention-simple-guide-to-q.html)
  _Skipped because:_ Blog-level and likely overlaps with existing high-quality intuition/shape explanations (D2L, CS231n/CS224N, Jalammar, Eli Bendersky).
- **[PDF] Optimization of small matrix multiplication kernels on** — [[PDF] Optimization of small matrix multiplication kernels on Arm - mediaTUM](https://mediatum.ub.tum.de/doc/1601278/zbkvhwtaatdlnckwxjkk40h5q.pdf)
  _Skipped because:_ Too low-level and hardware-specific for the stated attention-implementation gaps; doesn’t directly teach multi-head reshaping/batching patterns used in transformer attention.
- **Communication-Avoiding Matrix Multiplication Made Simple** — [Communication-Avoiding Matrix Multiplication Made Simple](https://arxiv.org/html/2601.16294v1)
  _Skipped because:_ General GEMM theory; not directly actionable for teaching vectorized attention implementation details (tensor reshapes, batched heads, masking, fused kernels).
- **[PDF] Performance, Design, and Autotuning of Batched GEMM fo** — [[PDF] Performance, Design, and Autotuning of Batched GEMM for GPUs](https://www.netlib.org/utk/people/JackDongarra/PAPERS/performance-design-and-autotuning.pdf)
  _Skipped because:_ Authoritative HPC reference but too specialized; it doesn’t map cleanly onto the pedagogical goal of implementing attention with correct shapes/masking/softmax stability.
- **[PDF] High-performance matrix-matrix multiplications of very** — [[PDF] High-performance matrix-matrix multiplications of very small matrices](https://library.eecs.utk.edu/files/ut-eecs-16-740.pdf)
  _Skipped because:_ HPC-focused and not specific to transformer attention; unlikely to improve a teaching wiki on attention math/implementation compared to more directly relevant sources.

## Uncovered Gaps (2) — No Good Candidates Found
_Consider manually sourcing these, or run enrichment again with different search terms._

- Full scaled dot-product attention as matrix operations with shapes: Q (n×d_k), K (m×d_k), V (m×d_v), scores=QK^T/sqrt(d_k), A=softmax(scores), output=AV
- Vectorized implementation details (batching, multi-head reshaping/transposes, efficient GEMM usage, avoiding Python loops)

## Reasoning
**Curator:** Most candidates are redundant with existing transformer/attention tutorials already in the library or are off-target HPC GEMM papers; the two additions uniquely strengthen foundational softmax mechanics/gradients and floating-point/numerical-stability treatment in a way the current shelf under-emphasizes.
**Reviewer:** The curator’s additions are reasonable and the rejected/remaining candidates shown here don’t add authoritative, attention-specific coverage of the stated gaps beyond what the existing library already provides.

---

# Curation Report: Scaled Dot-Product Attention: Math and Implementation
**Topic:** `self-attention` | **Date:** 2026-04-11 19:27
**Library:** 37 existing → 39 sources (2 added, 2 downloaded)
**Candidates evaluated:** 15
**Reviewer verdict:** good

## Added (2)
- **[tutorial]** [Masked and Causal Attention - Abhik Sarkar](https://www.abhik.ai/concepts/attention/masked-attention)
  Directly targets the missing “how masking is applied to logits before softmax” story, including causal vs padding masks and how they combine, which your current library only covers piecemeal.
   — covers: Padding mask: how to build from pad token positions; how it differs from causal mask; how it is applied to attention logits before softmax, Causal mask: standard lower-triangular mask mechanics; applying -inf (or large negative) to logits before softmax; interaction with padding masks, Broadcasting in attention implementations: mask shapes and broadcasting across batch and heads in PyTorch/JAX/TF; common pitfalls
- **[tutorial]** [Creating a Transformer From Scratch - Part One: The Attention Mechanism](https://benjaminwarner.dev/2023/07/01/attention-mechanism)
  Adds a concrete, implementation-forward walkthrough of scaled dot-product attention (logits → mask → softmax → weighted sum) that complements your existing conceptual resources and helps bridge math-to-code.
   — covers: Explicit step-by-step implementation recipe: compute logits = (Q @ K^T) / sqrt(d_k), add masks to logits, softmax over key dimension, output = weights @ V, Define attention logits explicitly as the pre-softmax QK^T score matrix; include typical tensor shapes for batched multi-head attention

## Near-Misses (13) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **A Gentle Introduction to Attention Masking in Transformer Mo** — [A Gentle Introduction to Attention Masking in Transformer Models](https://machinelearningmastery.com/a-gentle-introduction-to-attention-masking-in-transformer-models/)
  _Skipped because:_ Covers the right topics, but MachineLearningMastery posts are often verbose and less precise about framework-specific mask shapes/broadcasting than stronger, more technical writeups.
- **Attention Masking: Controlling Information Flow in Transform** — [Attention Masking: Controlling Information Flow in Transformers](https://mbrenndoerfer.com/writing/attention-masking-transformers)
  _Skipped because:_ Likely overlaps heavily with other Brenndoerfer pages already in your library and may not add enough new detail on mask broadcasting/pitfalls beyond what you already have.
- **pytorch - Mastering torch.nn.attention.bias: Common Pitfalls** — [pytorch - Mastering torch.nn.attention.bias: Common Pitfalls and Optimized Code](https://runebook.dev/en/docs/pytorch/nn.attention.bias)
  _Skipped because:_ Not an authoritative/stable primary source (third-party mirror/aggregator style) and risks being inaccurate or drifting from upstream PyTorch semantics.
- **Scaled Dot-Product Attention and Masking in Transformers** — [Scaled Dot-Product Attention and Masking in Transformers](https://codesignal.com/learn/courses/sequence-models-the-dawn-of-attention-1/lessons/scaled-dot-product-attention-and-masking-in-transformers-1)
  _Skipped because:_ Potentially gated/interactive content and typically lighter on the exact tensor-shape/broadcasting details needed to close your specific implementation gaps.
- **Transformer self-attention  padding and causal  masking tech** — [Transformer self-attention  padding and causal  masking technique](https://www.youtube.com/watch?v=n13-r_eStb0)
  _Skipped because:_ Video quality and longevity are harder to guarantee for a curated wiki, and it’s unclear it goes deep enough into mask shapes/broadcasting pitfalls.
- **Multi-Head Attention Mechanism** — [Multi-Head Attention Mechanism](https://www.geeksforgeeks.org/nlp/multi-head-attention-mechanism/)
  _Skipped because:_ GeeksforGeeks is often shallow and error-prone for nuanced tensor-shape and masking mechanics; your existing D2L/CS lecture notes are stronger.
- **Transformer Architecture Explained With Self-Attention ...** — [Transformer Architecture Explained With Self-Attention ...](https://www.codecademy.com/article/transformer-architecture-self-attention-mechanism)
  _Skipped because:_ Introductory and likely redundant with existing beginner-friendly transformer explainers already in the library.
- **A Gentle Introduction to Multi-Head Attention and Grouped- .** — [A Gentle Introduction to Multi-Head Attention and Grouped- ...](https://machinelearningmastery.com/a-gentle-introduction-to-multi-head-attention-and-grouped-query-attention/)
  _Skipped because:_ May add some shape discussion, but overlaps with D2L multi-head attention and tends not to be the most rigorous source for implementation details.
- **Learn Masking in Attention: Causal and Padding Masks** — [Learn Masking in Attention: Causal and Padding Masks](https://codefinity.com/courses/v2/e7ee0772-6b82-4a1c-96ba-69b85ddee608/f35bf119-fe3c-4db6-8a48-51dbc163416f/8c99758d-e015-49c3-9f59-44cb55ae9aae)
  _Skipped because:_ Course-platform content is often gated and less stable for long-term wiki curation; unclear depth on logits masking and broadcasting.
- **Interpreting logits: Sigmoid vs Softmax | Nandita Bhaskhar** — [Interpreting logits: Sigmoid vs Softmax | Nandita Bhaskhar](https://web.stanford.edu/~nanbhas/blog/sigmoid-softmax/)
  _Skipped because:_ Good background on logits/softmax, but it doesn’t specifically address attention-logit masking mechanics or tensor-shape/broadcasting issues.
- **Notes On Implementing Attention - Eli Bendersky | PDF** — [Notes On Implementing Attention - Eli Bendersky | PDF](https://www.scribd.com/document/868943586/Notes-on-implementing-Attention-Eli-Bendersky)
  _Skipped because:_ Redundant with the original Eli Bendersky post already in your library and hosted on a less stable/gated document-sharing site.
- **Attention Is All You Need - Paper Analysis - Mos Ahmed** — [Attention Is All You Need - Paper Analysis - Mos Ahmed](https://www.mosahmed.com/attention-paper.html)
  _Skipped because:_ A secondary summary that’s likely redundant given you already include the paper itself plus multiple high-quality tutorials.
- **Transformer** — [Transformer](https://sefer-raziel.tistory.com/204)
  _Skipped because:_ Unclear authorship/editorial standards and likely redundant with existing transformer/attention explainers.

## Uncovered Gaps (1) — No Good Candidates Found
_Consider manually sourcing these, or run enrichment again with different search terms._

- Broadcasting in attention implementations: mask shapes and broadcasting across batch and heads in PyTorch/JAX/TF; common pitfalls

## Reasoning
**Curator:** Most candidates are either redundant with your existing strong set (D2L, CS lectures, Jalammar, Eli Bendersky) or are lower-authority/gated. The two additions are the best fit for closing the masking-and-implementation gaps with clear, code-adjacent explanations.
**Reviewer:** Given the provided near-misses list, none clearly add authoritative, durable, and uniquely gap-filling coverage beyond what you already have plus the two added tutorials; the remaining uncovered broadcasting/mask-shape pitfalls are better addressed by adding primary framework docs or canonical library implementations, but no such candidates were presented here.
