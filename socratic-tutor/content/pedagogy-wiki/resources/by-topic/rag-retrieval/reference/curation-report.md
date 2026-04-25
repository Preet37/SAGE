# Curation Report: RAG and Retrieval
**Topic:** `rag-retrieval` | **Date:** 2026-04-09 16:31
**Library:** 6 existing → 22 sources (16 added, 11 downloaded)
**Candidates evaluated:** 45
**Reviewer verdict:** needs_additions

## Added (16)
- **[reference_doc]** [Faiss indexes · facebookresearch/faiss Wiki](https://github.com/facebookresearch/faiss/wiki/Faiss-indexes)
  Gives authoritative, citable parameter surfaces and index-type selection details for common ANN backends used in RAG, including metric implications (IP vs L2) and the practical cosine-normalization convention.
- **[reference_doc]** [Struct faiss::IndexIVFPQR - Faiss documentation](https://faiss.ai/cpp_api/struct/structfaiss_1_1IndexIVFPQR.html)
  Provides the most precise, implementation-level specification for IVF-PQ(-R) parameters and their meanings, enabling the tutor to answer exact questions about IVF/PQ defaults and knobs.
- **[paper]** [ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT](https://arxiv.org/abs/2004.12832)
  Seminal, equation-level description of token-level matching and why late interaction improves effectiveness while keeping retrieval efficient—directly transferable to explaining late-interaction RAG retrievers.
- **[paper]** [ColPali: Efficient Document Retrieval with Vision Language Models](https://arxiv.org/abs/2407.01449)
  Targets visual-document retrieval specifically, giving a step-by-step design and training/inference rationale for multimodal late interaction that a tutor can map onto image+text RAG architectures.
- **[paper]** [OCR-free Document Understanding Transformer](https://arxiv.org/abs/2111.15664)
  Adds citable empirical results and an OCR-free pipeline description that helps the tutor discuss tradeoffs and performance baselines for document-centric RAG/QA settings.
- **[explainer]** [Introducing Natural Language Search for Podcast Episodes | Spotify Engineering](https://engineering.atspotify.com/2022/3/introducing-natural-language-search-for-podcast-episodes)
  Provides a real-world, end-to-end deployment story (system design decisions, rollout considerations, and practical retrieval issues) that the tutor can use to teach production retrieval tradeoffs.
- **[paper]** [Dense Passage Retrieval for Open-Domain Question Answering](https://aclanthology.org/2020.emnlp-main.550.pdf)
  This is the canonical dense-retrieval training recipe that most RAG retrievers build on; it directly fills the missing equations and training pipeline details.
- **[explainer]** [The Probabilistic Relevance Framework: BM25 and Beyond (CS276 handout)](https://web.stanford.edu/class/cs276/handouts/lecture12-bm25etc.pdf)
  RAG lessons routinely need BM25 as the baseline and for hybrid retrieval; this provides the exact formula and parameter semantics in a teachable reference.
- **[paper]** [ColBERTv2: Effective and Efficient Retrieval via Lightweight Late Interaction](https://aclanthology.org/2022.naacl-main.272/)
  Even if ColBERT is foundational, ColBERTv2 is the practical, widely-cited “how to make late interaction work well” reference and adds procedure-level details useful for tutoring.
- **[benchmark]** [ICDAR 2021 Competition on Document Visual Question Answering (DocVQA)](https://arxiv.org/pdf/2111.05547.pdf)
  This directly supplies the missing “specific numbers” for DocVQA and gives authoritative task framing that’s useful when teaching document-centric RAG evaluation.
- **[paper]** [Where is this coming from? Making groundedness count in the evaluation of Document VQA models](https://arxiv.org/html/2503.19120v1)
  RAG tutoring needs evidence-grounded evaluation beyond accuracy; this provides a concrete, citable evaluation methodology with numbers.
- **[paper]** [Dense Passage Retrieval for Open-Domain Question Answering](https://aclanthology.org/2020.emnlp-main.550.pdf) *(promoted by reviewer)*
  This is the canonical dense-retrieval training recipe that most RAG retrievers build on; it directly fills the missing equations and training pipeline details.
- **[explainer]** [The Probabilistic Relevance Framework: BM25 and Beyond (CS276 handout)](https://web.stanford.edu/class/cs276/handouts/lecture12-bm25etc.pdf) *(promoted by reviewer)*
  RAG lessons routinely need BM25 as the baseline and for hybrid retrieval; this provides the exact formula and parameter semantics in a teachable reference.
- **[paper]** [ColBERTv2: Effective and Efficient Retrieval via Lightweight Late Interaction](https://aclanthology.org/2022.naacl-main.272/) *(promoted by reviewer)*
  Even if ColBERT is foundational, ColBERTv2 is the practical, widely-cited “how to make late interaction work well” reference and adds procedure-level details useful for tutoring.
- **[benchmark]** [ICDAR 2021 Competition on Document Visual Question Answering (DocVQA)](https://arxiv.org/pdf/2111.05547.pdf) *(promoted by reviewer)*
  This directly supplies the missing “specific numbers” for DocVQA and gives authoritative task framing that’s useful when teaching document-centric RAG evaluation.
- **[paper]** [Where is this coming from? Making groundedness count in the evaluation of Document VQA models](https://arxiv.org/html/2503.19120v1) *(promoted by reviewer)*
  RAG tutoring needs evidence-grounded evaluation beyond accuracy; this provides a concrete, citable evaluation methodology with numbers.

## Near-Misses (3) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **Guidelines to choose an index · facebookresearch/faiss Wiki ** — [Guidelines to choose an index · facebookresearch/faiss Wiki - GitHub](https://github.com/facebookresearch/faiss/wiki/Guidelines-to-choose-an-index)
  _Skipped because:_ Useful for decision heuristics, but the Faiss-indexes page plus the IVFPQR API doc better satisfy the need for precise parameter specs and citable API-level details.
- **ColBERTv2: Effective and Efficient Retrieval via ...** — [ColBERTv2: Effective and Efficient Retrieval via ...](https://aclanthology.org/2022.naacl-main.272.pdf)
  _Skipped because:_ Strong follow-up with training improvements, but ColBERT (original) is the more foundational reference for teaching the core late-interaction formulation.
- **Introducing Voyager: Spotify’s New Nearest-Neighbor Search .** — [Introducing Voyager: Spotify’s New Nearest-Neighbor Search ...](https://engineering.atspotify.com/2023/10/introducing-voyager-spotifys-new-nearest-neighbor-search-library)
  _Skipped because:_ Relevant to ANN deployment, but the provided preview appears mismatched and the natural-language search case study more directly supports retrieval-in-product teaching.

## Reasoning
**Curator:** Selections prioritize authoritative specs (Faiss docs) and seminal, equation-bearing retrieval papers (ColBERT/ColPali) plus at least one concrete document-AI benchmark source (Donut) and one real production retrieval case study (Spotify). Several needs remain unfilled because the candidate set lacks canonical BM25/DPR/InfoNCE formula sources and document-VQA benchmark/leaderboard-style retrieval metric tables.
**Reviewer:** The curation is strong on ANN/Faiss and late-interaction concepts, but it still lacks canonical dense-retrieval training equations (DPR/InfoNCE), BM25 formulas for hybrid baselines, and benchmark/evaluation tables for document VQA groundedness.
