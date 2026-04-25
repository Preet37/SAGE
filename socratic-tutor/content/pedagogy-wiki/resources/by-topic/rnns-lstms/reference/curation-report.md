# Curation Report: Bahdanau (Additive) Attention: Formulation and Intuition
**Topic:** `rnns-lstms` | **Date:** 2026-04-09 15:50
**Library:** 24 existing → 36 sources (12 added, 8 downloaded)
**Candidates evaluated:** 43
**Reviewer verdict:** needs_additions

## Added (12)
- **[paper]** [[PDF] Neural Machine Translation by Jointly Learning to Align and Translate](https://iclr.cc/archive/www/lib/exe/fetch.php%3Fmedia=iclr2015:bahdanau-iclr2015.pdf)
  This is the original, citable source for Bahdanau (additive) attention equations, dimensional conventions, and the training objective used in early attention-based NMT.
- **[benchmark]** [Effective Approaches to Attention-based Neural Machine Translation](https://aclanthology.org/anthology-files/pdf/D/D15/D15-1166.pdf)
  Provides reproducible comparative results and ablations that help students see how additive-style (concat/MLP) vs multiplicative scoring affects BLEU and efficiency.
- **[code]** [Translation with a Sequence to Sequence Network and Attention](https://docs.pytorch.org/tutorials/intermediate/seq2seq_translation_tutorial.html)
  Gives a runnable reference implementation that a tutor can map directly to the Bahdanau equations and use to answer shape/masking/teacher-forcing questions concretely.
- **[explainer]** [Implementing additive and multiplicative attention in PyTorch](https://tomekkorbak.com/2020/06/26/implementing-attention-in-pytorch/)
  Offers a structured, code-grounded comparison that helps explain when additive vs dot-product attention is preferable and what changes in compute/parameters.
- **[reference_doc]** [Neural machine translation with attention (TensorFlow Text tutorial)](https://www.tensorflow.org/text/tutorials/nmt_with_attention)
  Even though it’s a tutorial, it’s official TF documentation and is one of the few stable references that clarifies defaults/semantics and end-to-end attention integration in Keras—directly addressing the still-unfilled API-reference need.
- **[reference_doc]** [Neural machine translation with attention (TensorFlow tutorial, Korean)](https://www.tensorflow.org/tutorials/text/nmt_with_attention?hl=ko)
  If the library aims to support broader audiences, this is a high-signal duplicate of the official doc in another language; otherwise it can be omitted.
- **[paper]** [Attention Is All You Need (NeurIPS 2017 PDF)](https://proceedings.neurips.cc/paper_files/paper/2017/file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf)
  The library already has an arXiv HTML version, but the official proceedings PDF is a better stable citation and preserves canonical pagination/figure references used in teaching and academic discussion.
- **[benchmark]** [Effective Approaches to Attention-based Neural Machine Translation (EMNLP 2015 PDF)](https://nlp.stanford.edu/pubs/emnlp15_attn.pdf)
  You already include arXiv/ACL links, but the official PDF is the most reliable for teaching from tables/figures (stable formatting, page numbers) and is the version most people cite.
- **[reference_doc]** [Neural machine translation with attention (TensorFlow Text tutorial)](https://www.tensorflow.org/text/tutorials/nmt_with_attention) *(promoted by reviewer)*
  Even though it’s a tutorial, it’s official TF documentation and is one of the few stable references that clarifies defaults/semantics and end-to-end attention integration in Keras—directly addressing the still-unfilled API-reference need.
- **[reference_doc]** [Neural machine translation with attention (TensorFlow tutorial, Korean)](https://www.tensorflow.org/tutorials/text/nmt_with_attention?hl=ko) *(promoted by reviewer)*
  If the library aims to support broader audiences, this is a high-signal duplicate of the official doc in another language; otherwise it can be omitted.
- **[paper]** [Attention Is All You Need (NeurIPS 2017 PDF)](https://proceedings.neurips.cc/paper_files/paper/2017/file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf) *(promoted by reviewer)*
  The library already has an arXiv HTML version, but the official proceedings PDF is a better stable citation and preserves canonical pagination/figure references used in teaching and academic discussion.
- **[benchmark]** [Effective Approaches to Attention-based Neural Machine Translation (EMNLP 2015 PDF)](https://nlp.stanford.edu/pubs/emnlp15_attn.pdf) *(promoted by reviewer)*
  You already include arXiv/ACL links, but the official PDF is the most reliable for teaching from tables/figures (stable formatting, page numbers) and is the version most people cite.

## Near-Misses (2) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **arXiv:2202.08371v1  [cs.LG]  15 Feb 2022** — [arXiv:2202.08371v1  [cs.LG]  15 Feb 2022](https://arxiv.org/pdf/2202.08371.pdf)
  _Skipped because:_ Useful high-level discussion, but less directly tied to classic NMT additive-vs-multiplicative tradeoffs and lacks the canonical benchmark focus needed here.
- **Implementing Bahdanau's Attention - nlp - PyTorch Forums** — [Implementing Bahdanau's Attention - nlp - PyTorch Forums](https://discuss.pytorch.org/t/implementing-bahdanaus-attention/83557)
  _Skipped because:_ Contains non-authoritative, user-generated code without stable API guarantees or documented defaults; better as troubleshooting than as a reference.

## Reasoning
**Curator:** Selections prioritize primary sources for exact equations and objective (Bahdanau), a canonical benchmark paper with comparative tables (Luong), and a runnable implementation plus a concrete additive-vs-multiplicative comparison to support both precision and intuition.
**Reviewer:** Core seminal coverage is strong (Bahdanau + Luong + solid explainers), but the library still benefits from adding at least one official framework documentation/tutorial source to satisfy the explicit API-reference need, plus camera-ready PDFs for stable citation of key tables/equations.
