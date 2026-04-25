# Document Understanding

## Video (best)
- **None identified**
- Why: Document understanding spans OCR, layout modeling, and structured extraction; no single, clearly best, widely recognized video resource is confidently identifiable.
- Level: —

## Blog / Written explainer (best)
- **Hugging Face Docs** — "LayoutLM"
- url: https://huggingface.co/docs/transformers/model_doc/layoutlm
- Why: Clear, practical overview of a canonical layout-aware document understanding model family; includes usage patterns and key ideas.
- Level: Intermediate

## Deep dive
- **Hugging Face Docs** — "LayoutLMv2"
- url: https://huggingface.co/docs/transformers/model_doc/layoutlmv2
- Why: Deeper treatment of multimodal/layout-aware modeling (text + layout + image features) commonly used for forms, receipts, and scanned documents.
- Level: Intermediate–Advanced

## Original paper
- **Xu et al.** — "LayoutLM: Pre-training of Text and Layout for Document Image Understanding"
- url: https://arxiv.org/abs/1912.13318
- Why: Foundational paper for layout-aware document understanding; establishes the text+2D layout pretraining paradigm.
- Level: Advanced

## Code walkthrough
- **Hugging Face Transformers** — "Document Question Answering" (pipeline task page)
- url: https://huggingface.co/tasks/document-question-answering
- Why: Practical entry point showing how document understanding models are applied end-to-end (inputs, outputs, typical models).
- Level: Beginner–Intermediate

## Coverage notes
- Strong: Layout-aware models (LayoutLM family) and practical usage via Hugging Face; general document QA workflows.
- Weak: OCR-free understanding and modern OCR-free pipelines (e.g., Donut-style approaches) are not covered here as a single “best” resource.
- Gap: Visual document retrieval (e.g., ColPali/page-level embeddings) and specific libraries like docTR; table extraction and form understanding need dedicated, high-confidence “best” explainers and code walkthroughs.

## Last Verified
2026-04-09