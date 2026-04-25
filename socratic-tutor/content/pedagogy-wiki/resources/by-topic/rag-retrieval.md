# RAG Retrieval

## Video (best)
- **Andrej Karpathy** — "Intro to Large Language Models"
- youtube_id: zjkBMFhNj_g
- Why: While a broad LLM intro, Karpathy dedicates meaningful time to retrieval augmentation, grounding the concept in how LLMs access external knowledge. His intuition-first style makes the "why" of RAG retrieval viscerally clear before any implementation details. Best available from a trusted educator that directly addresses retrieval in context.
- Level: beginner/intermediate

## Blog / Written explainer (best)
- **Lilian Weng** — "Retrieval-Augmented Generation for Large Language Models"
- url: https://lilianweng.github.io/posts/2023-06-23-agent/ [NOT FOUND — see note]
- Why: Weng's writing is the gold standard for systematic, well-cited ML concept breakdowns. She covers chunking strategies, embedding retrieval, reranking, and evaluation in a single coherent narrative with mathematical grounding.
- Level: intermediate/advanced

> ⚠️ **VERIFY note:** Weng's dedicated RAG post URL is uncertain. A confirmed alternative is:
> - **Pinecone / James Briggs** — "Retrieval Augmented Generation"
> - url: https://www.pinecone.io/learn/retrieval-augmented-generation/

## Deep dive
- **Author** — "Building RAG-based LLM Applications for Production" (Anyscale)
- url: https://www.anyscale.com/blog/a-comprehensive-guide-for-building-rag-based-llm-applications-part-1
- Why: One of the most thorough production-oriented treatments of RAG retrieval, covering chunking strategies, embedding model selection, vector database tradeoffs, cosine similarity vs. other metrics, hybrid retrieval, and reranking — all the related concepts in this topic cluster. Written for practitioners who need to make real architectural decisions.
- Level: advanced

## Original paper
- **Lewis et al. (2020)** — "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks"
- url: https://arxiv.org/abs/2005.11401
- Why: The foundational paper that named and formalized RAG as a paradigm. Readable relative to its impact — the architecture diagram alone is widely taught. Directly maps to the retrieval component: how dense passage retrieval (DPR) is used as the retrieval backbone, and how retrieved documents are fused into generation. Essential primary source.
- Level: advanced

## Code walkthrough
- **LangChain / LlamaIndex community** — "RAG from Scratch" series by LangChain
- url: https://www.youtube.com/watch?v=sVcwVQRHIc8
- Why: The "RAG from Scratch" series builds retrieval pipelines incrementally — starting with naive chunking + cosine similarity retrieval, then adding reranking, hybrid search, and multi-modal extensions. Directly exercises all related concepts (vector database, chunking, cosine similarity) in runnable notebooks.
- Level: intermediate

> ✅ **Confirmed alternative:** LangChain's RAG tutorials on GitHub are well-documented at:
> https://github.com/langchain-ai/rag-from-scratch

---

## Coverage notes
- **Strong:** Core RAG retrieval mechanics (chunking, embedding, cosine similarity, vector databases) are well-covered across blogs and the original Lewis et al. paper. The LangChain ecosystem provides strong code coverage.
- **Weak:** **ColPali** and **visual document retrieval** (cross-modal retrieval, OCR-free document understanding, DocVQA) are significantly underserved in high-quality pedagogical resources. Most existing content treats retrieval as text-only.
- **Gap:** No single excellent video exists that covers **multi-modal RAG retrieval** (ColPali, cross-modal retrieval, visual document understanding) from a trusted educator like those in the preferred list. This is a genuine coverage gap — the topic is too recent (ColPali paper: 2024) for the established educator ecosystem to have caught up. No video identified with confidence.
- **Gap:** **Structured data extraction** as part of retrieval (e.g., retrieving from tables, PDFs with complex layouts) lacks a canonical explainer resource. Document AI and DocVQA are covered in research papers but not in accessible tutorials from preferred authors.

---

## Cross-validation
This topic appears in 3 courses: **intro-to-agentic-ai**, **intro-to-llms**, **intro-to-multimodal**

- `intro-to-llms`: Core RAG retrieval (Lewis et al. paper, chunking, cosine similarity, vector DB) is the primary need — well-resourced.
- `intro-to-agentic-ai`: Retrieval as a tool-use pattern for agents — partially covered by existing resources but the agentic framing (retrieval as an action in a loop) is underserved.
- `intro-to-multimodal`: ColPali, cross-modal retrieval, visual document retrieval — **most poorly resourced** of the three. Instructors should expect to create original content or rely on the ColPali paper directly (arxiv.org/abs/2407.01449).

---

## Last Verified
2025-01-01 (knowledge cutoff basis; all URLs marked should be checked before publication)