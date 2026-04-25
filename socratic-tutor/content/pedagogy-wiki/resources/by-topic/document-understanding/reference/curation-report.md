# Curation Report: Document Understanding
**Topic:** `document-understanding` | **Date:** 2026-04-09 18:33
**Library:** 4 existing → 18 sources (14 added, 9 downloaded)
**Candidates evaluated:** 43
**Reviewer verdict:** needs_additions

## Added (14)
- **[paper]** [OCR-free Document Understanding Transformer](https://arxiv.org/abs/2111.15664)
  This is the primary authoritative source for OCR-free document understanding, detailing how outputs are serialized and generated step-by-step for structured extraction and VQA.
- **[paper]** [LayoutLMv3: Pre-training for Document AI with Unified Text and Image Masking](https://arxiv.org/pdf/2204.08387.pdf)
  Provides citable equations/objectives and design rationale for modern layout-aware pretraining, useful for explaining how multimodal alignment is learned.
- **[reference_doc]** [Python Inference for PP-OCR Model Zoo¶](https://paddlepaddle.github.io/PaddleOCR/en/ppocr/infer_deploy/python_infer.html)
  Official PaddleOCR deployment documentation that the tutor can quote for practical pipeline defaults and configuration knobs that affect accuracy/latency.
- **[paper]** [ColPali: Efficient Document Retrieval with Vision Language Models](https://arxiv.org/abs/2407.01449)
  Directly targets visual document retrieval comparisons and provides a benchmark plus a concrete late-interaction embedding/scoring recipe for page-level retrieval.
- **[paper]** [LayoutLMv3: Pre-training for Document AI with Unified Text and Image Masking](https://arxiv.org/pdf/2204.08387v3.pdf)
  The HF docs are implementation-facing; the paper PDF is the authoritative, citable source for exact objective formulations and training design rationale.
- **[paper]** [arXiv:2304.14936 (KIE benchmark generalization / train-test similarity analysis)](https://arxiv.org/pdf/2304.14936.pdf)
  Even if it’s not a pure leaderboard table, it directly addresses the unfilled need around benchmark validity and provides concrete empirical findings the tutor can cite when discussing evaluation pitfalls.
- **[paper]** [Robustness Evaluation of OCR-based Visual Document Understanding Models](https://arxiv.org/pdf/2506.16407.pdf)
  This is exactly the kind of numbers-heavy empirical source that complements standard benchmark tables by adding robustness and OCR-failure-mode metrics relevant to OCR-based vs OCR-free tradeoffs.
- **[paper]** [EMNLP 2024 Industry Track paper (pages 1056–1067) on KIE/VDU evaluation and generalization](https://aclanthology.org/2024.emnlp-industry.79.pdf)
  Industry-track papers frequently include concrete metrics and operational considerations (latency/cost/error sources) that academic model papers omit; this likely helps fill the compute/robustness side of the unfilled need.
- **[paper]** [Layout Attention with Gaussian Biases for Structured Document Understanding](https://aclanthology.org/2023.findings-emnlp.521.pdf)
  The current library is heavy on LayoutLM-family baselines; this adds a distinct, citable mechanism for layout-aware attention with clear equations and design rationale useful for teaching alternatives.
- **[paper]** [LayoutLMv3: Pre-training for Document AI with Unified Text and Image Masking](https://arxiv.org/pdf/2204.08387v3.pdf) *(promoted by reviewer)*
  The HF docs are implementation-facing; the paper PDF is the authoritative, citable source for exact objective formulations and training design rationale.
- **[paper]** [arXiv:2304.14936 (KIE benchmark generalization / train-test similarity analysis)](https://arxiv.org/pdf/2304.14936.pdf) *(promoted by reviewer)*
  Even if it’s not a pure leaderboard table, it directly addresses the unfilled need around benchmark validity and provides concrete empirical findings the tutor can cite when discussing evaluation pitfalls.
- **[paper]** [Robustness Evaluation of OCR-based Visual Document Understanding Models](https://arxiv.org/pdf/2506.16407.pdf) *(promoted by reviewer)*
  This is exactly the kind of numbers-heavy empirical source that complements standard benchmark tables by adding robustness and OCR-failure-mode metrics relevant to OCR-based vs OCR-free tradeoffs.
- **[paper]** [EMNLP 2024 Industry Track paper (pages 1056–1067) on KIE/VDU evaluation and generalization](https://aclanthology.org/2024.emnlp-industry.79.pdf) *(promoted by reviewer)*
  Industry-track papers frequently include concrete metrics and operational considerations (latency/cost/error sources) that academic model papers omit; this likely helps fill the compute/robustness side of the unfilled need.
- **[paper]** [Layout Attention with Gaussian Biases for Structured Document Understanding](https://aclanthology.org/2023.findings-emnlp.521.pdf) *(promoted by reviewer)*
  The current library is heavy on LayoutLM-family baselines; this adds a distinct, citable mechanism for layout-aware attention with clear equations and design rationale useful for teaching alternatives.

## Near-Misses (3) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **OCR-free Document Understanding Transformer - ar5iv - arXiv** — [OCR-free Document Understanding Transformer - ar5iv - arXiv](https://ar5iv.labs.arxiv.org/html/2111.15664)
  _Skipped because:_ Useful HTML rendering, but the canonical arXiv entry is preferable for citation stability and versioning.
- **Python Inference for PP-OCR Model Zoo** — [Python Inference for PP-OCR Model Zoo](http://www.paddleocr.ai/main/en/version2.x/legacy/python_infer.html)
  _Skipped because:_ Appears to be a legacy/mirrored page; the PaddlePaddle GitHub Pages doc is the more official and maintained reference.
- **ColBERTv2: Effective and Efficient Retrieval via ...** — [ColBERTv2: Effective and Efficient Retrieval via ...](https://aclanthology.org/2022.naacl-main.272.pdf)
  _Skipped because:_ Strong late-interaction retrieval reference, but it is not document/page-image specific and does not provide the visual-document benchmark comparisons requested.

## Reasoning
**Curator:** Selections prioritize canonical, citable sources that directly provide (1) Donut’s end-to-end OCR-free generation/serialization pipeline, (2) explicit layout-aware pretraining objective equations, (3) official OCR deployment defaults, and (4) a modern visual document retrieval benchmark with late-interaction comparisons.
**Reviewer:** The core picks are strong, but the library should add at least one robustness/generalization-focused empirical paper and one additional formula-level layout mechanism paper to better cover evaluation tradeoffs and layout modeling beyond LayoutLM.
