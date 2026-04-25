# Curation Report: Scaled Dot-Product Attention and Masking
**Topic:** `prompting` | **Date:** 2026-04-08 01:16
**Library:** 4 existing → 10 sources (6 added, 2 downloaded, 2 failed)
**Candidates evaluated:** 20
**Reviewer verdict:** needs_additions

## Added (6)
- **[paper]** [[PDF] Silent Tokens, Loud Effects: Padding in LLMs - arXiv](https://www.arxiv.org/pdf/2510.01238.pdf)
  Adds a research-grade treatment of padding effects and masking pitfalls in LLM training/inference, going beyond basic “ignore pads” explanations and helping justify correct padding-mask handling in variable-length batches.
   — covers: Padding masks: masking pad tokens in keys/values (and sometimes queries), interaction with variable-length batches, and effect on attention weights
- **[tutorial]** [A Gentle Introduction to Attention Masking in Transformer Models](https://machinelearningmastery.com/a-gentle-introduction-to-attention-masking-in-transformer-models/)
  Provides a clear, implementation-oriented explanation of attention masks (padding vs causal) and the practical “add large negative before softmax” pattern, which directly addresses missing conceptual/engineering details in the current library.
   — covers: Causal (look-ahead) masking in self-attention: mask matrix form, applying -inf to future positions before softmax, effect on attention weights in autoregressive decoding, Padding masks: masking pad tokens in keys/values (and sometimes queries), interaction with variable-length batches, and effect on attention weights
- **[paper]** [Accurately computing the log-sum-exp and softmax functions](https://academic.oup.com/imajna/article/41/4/2311/5893596)
  This is a peer-reviewed numerical analysis treatment of stable log-sum-exp/softmax computation—much higher authority and longer shelf-life than blog posts, and directly applicable to stable attention/softmax implementations (including masking with large negatives).
   — covers: Numerical stability in attention/softmax: log-sum-exp trick, subtracting max logit, stable masking implementation, and handling -inf in practice
- **[tutorial]** [Numerically Stable Softmax and Cross Entropy](https://jaykmody.com/blog/stable-softmax/)
  A uniquely clear, implementation-oriented walkthrough of the max-trick/log-sum-exp and stable cross-entropy that maps cleanly onto attention softmax; it’s a strong teaching complement to a more formal numerical-analysis reference.
   — covers: Numerical stability in attention/softmax: log-sum-exp trick, subtracting max logit, stable masking implementation, and handling -inf in practice
- **[paper]** [Accurately computing the log-sum-exp and softmax functions](https://academic.oup.com/imajna/article/41/4/2311/5893596) *(promoted by reviewer)*
  This is a peer-reviewed numerical analysis treatment of stable log-sum-exp/softmax computation—much higher authority and longer shelf-life than blog posts, and directly applicable to stable attention/softmax implementations (including masking with large negatives).
   — fills: Numerical stability in attention/softmax: log-sum-exp trick, subtracting max logit, stable masking implementation, and handling -inf in practice
- **[tutorial]** [Numerically Stable Softmax and Cross Entropy](https://jaykmody.com/blog/stable-softmax/) *(promoted by reviewer)*
  A uniquely clear, implementation-oriented walkthrough of the max-trick/log-sum-exp and stable cross-entropy that maps cleanly onto attention softmax; it’s a strong teaching complement to a more formal numerical-analysis reference.
   — fills: Numerical stability in attention/softmax: log-sum-exp trick, subtracting max logit, stable masking implementation, and handling -inf in practice

## Near-Misses (12) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **Exploring the Impact of Temperature Scaling in Softmax ...** — [Exploring the Impact of Temperature Scaling in Softmax ...](https://arxiv.org/html/2502.20604v1)
  _Skipped because:_ Potentially relevant, but as a very recent preprint with unclear staying power and unknown quality/impact, it’s not yet a reliable “best resource” pick for a teaching wiki.
- **Unpacking Softmax: How Temperature Drives Representation ...** — [Unpacking Softmax: How Temperature Drives Representation ...](https://arxiv.org/html/2506.01562v1)
  _Skipped because:_ Appears overlapping with Candidate 1 and similarly too new/uncertain to prefer over more established explanations of temperature and softmax behavior.
- **Introducing a learnable temperature value into the softmax s** — [Introducing a learnable temperature value into the softmax self ...](https://nickcdryan.com/2024/08/02/introducing-a-learnable-temperature-value-into-the-self-attention-scores/)
  _Skipped because:_ Likely useful but is a personal blog post and may be narrower (learnable temperature in attention) than needed for a canonical, stable reference on temperature scaling fundamentals.
- **Learnable-Temperature Softmax: Adaptive Scaling - Emergent M** — [Learnable-Temperature Softmax: Adaptive Scaling - Emergent Mind](https://www.emergentmind.com/topics/learnable-temperature-softmax)
  _Skipped because:_ Aggregator-style content is often uneven and less citable than primary sources or well-known textbooks/tutorials.
- **Investigating Softmax Tempering** — [Investigating Softmax Tempering](https://aclanthology.org/anthology-files/pdf/mtsummit/2021.mtsummit-research.10.pdf)
  _Skipped because:_ Could be valuable, but it’s oriented toward MT/tempering and may not directly teach temperature scaling in attention with the clarity and breadth needed for this lesson.
- **The Causal Mask** — [The Causal Mask](https://www.abhik.ai/concepts/attention/masked-attention)
  _Skipped because:_ Covers the right topic but is likely too lightweight compared with more thorough tutorials; the library benefits more from a broader masking reference that also covers padding.
- **Decoder Architecture: Causal Masking & Autoregressive ...** — [Decoder Architecture: Causal Masking & Autoregressive ...](https://mbrenndoerfer.com/writing/decoder-architecture-causal-masking-autoregressive-transformers)
  _Skipped because:_ Good focus on causal masking, but overlaps with other causal-mask explainers and doesn’t clearly add padding-mask or numerical-stability depth.
- **Understanding causal attention or masked self attention | Tr** — [Understanding causal attention or masked self attention | Transformers for vision series](https://www.youtube.com/watch?v=CJSYo2Mw8R0)
  _Skipped because:_ Video format can be helpful, but this appears narrower (vision-series framing) and less referenceable than a strong written tutorial for a teaching wiki.
- **Masked Self-Attention in Decoders** — [Masked Self-Attention in Decoders](https://apxml.com/courses/foundations-transformers-architecture/chapter-5-encoder-decoder-stacks/masked-self-attention)
  _Skipped because:_ Likely solid, but course content can be less stable/accessible long-term than widely cited tutorials or papers.
- **Scaled Dot-Product Attention and Masking in Transformers** — [Scaled Dot-Product Attention and Masking in Transformers](https://codesignal.com/learn/courses/sequence-models-the-dawn-of-attention-1/lessons/scaled-dot-product-attention-and-masking-in-transformers-1)
  _Skipped because:_ May be gated or less stable as a long-term reference; also unclear whether it goes deep on numerical stability and masking edge cases beyond introductory coverage.
- **Padding and Attention Masks in LLMs: Preparing Batches for T** — [Padding and Attention Masks in LLMs: Preparing Batches for Training](https://www.youtube.com/watch?v=fwI_tVHcg4Q)
  _Skipped because:_ Potentially useful, but videos are harder to skim/cite and quality varies; the added arXiv paper plus a written tutorial already cover padding masks more reliably.
- **Understanding Transformers and Attention Mechanisms - arXiv** — [Understanding Transformers and Attention Mechanisms - arXiv](https://arxiv.org/html/2604.00965v1)
  _Skipped because:_ Too new and likely broad/introductory; doesn’t clearly target the specific masking/temperature/numerical-stability gaps better than more focused sources.

## Uncovered Gaps (2) — No Good Candidates Found
_Consider manually sourcing these, or run enrichment again with different search terms._

- Explicit definition of temperature scaling in softmax (softmax(logits/T)) and how changing T affects attention sharpness/entropy and gradients
- Numerical stability in attention/softmax: log-sum-exp trick, subtracting max logit, stable masking implementation, and handling -inf in practice

## Reasoning
**Curator:** The best improvements here are (1) a strong, practical masking tutorial covering causal and padding masks and (2) a research paper specifically about padding effects in LLMs. The temperature-scaling and numerical-stability gaps are not convincingly addressed by any clearly authoritative, stable candidate source.
**Reviewer:** The masking additions are solid, but the library still lacks a durable, high-authority reference (and a clear practical explainer) for numerically stable softmax/log-sum-exp, which is central to masked scaled dot-product attention.
