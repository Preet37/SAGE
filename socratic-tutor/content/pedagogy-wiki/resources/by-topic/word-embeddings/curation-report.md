# Curation Report: Retrieval-Augmented Generation (RAG) Inside Agents
**Topic:** `word-embeddings` | **Date:** 2026-04-10 19:03
**Library:** 5 existing → 14 sources (9 added, 6 downloaded)
**Candidates evaluated:** 40
**Reviewer verdict:** needs_additions

## Added (9)
- **[reference_doc]** [Information Retrieval and Retrieval-Augmented Generation](https://web.stanford.edu/~jurafsky/slp3/11.pdf)
  An authoritative textbook chapter that connects modern neural/embedding-based IR to RAG, covering the end-to-end retrieval pipeline and core retrieval concepts with more rigor than vendor/blog explainers.
   — covers: Clear definition of Retrieval-Augmented Generation (RAG) and end-to-end pipeline steps (indexing, retrieval, augmentation, generation), Embedding-based retrieval: how embeddings are computed for queries/documents and used for similarity matching, Vector search fundamentals: similarity metrics (cosine/dot/L2), ANN indexes (HNSW/IVF/FAISS), top-k retrieval, filtering
- **[paper]** [Retrieval-Augmented Generation for Large Language Models](https://arxiv.org/html/2312.10997v5)
  A comprehensive, research-oriented survey of RAG for LLMs that systematizes components (indexing/retrieval/augmentation/generation) and discusses grounding, evaluation, and design choices—material missing from the current embedding-focused library.
   — covers: Clear definition of Retrieval-Augmented Generation (RAG) and end-to-end pipeline steps (indexing, retrieval, augmentation, generation), Grounded generation: definition, how grounding reduces hallucinations, and ways to audit/attribute outputs to sources, Context injection patterns: prompt templates, citations, tool-result formatting, and managing context window/token budgets
- **[paper]** [The Faiss Library - arXiv](https://arxiv.org/html/2401.08281v2)
  Deep, implementation-grounded reference on vector search tradeoffs (distance metrics, IVF/HNSW families, benchmarking, and filtered search), directly addressing the vector-search fundamentals gap with a stable, citable source.
   — covers: Vector search fundamentals: similarity metrics (cosine/dot/L2), ANN indexes (HNSW/IVF/FAISS), top-k retrieval, filtering
- **[paper]** [Agentic Retrieval-Augmented Generation: A Survey on Agentic RAG](https://arxiv.org/abs/2501.09136)
  Directly targets the lesson’s core theme (RAG inside agents) rather than generic RAG, covering iterative retrieval, planning/controller patterns, and system-level design choices that the current shelf doesn’t yet anchor with a citable survey.
   — covers: RAG as a callable tool in agent loops: repeated retrieval, planner-controller patterns, and tracing/auditability of retrieval steps
- **[paper]** [A Systematic Investigation of Document Chunking Strategies for Dense Retrieval](https://arxiv.org/html/2603.06976)
  Chunking is an explicitly uncovered gap and this appears to be a rare large-scale, cross-domain empirical study of segmentation methods—more durable and teachable than ad-hoc blog heuristics.
   — covers: Document chunking strategies: chunk size, overlap, structure-aware splitting, metadata, and impact on retrieval quality
- **[paper]** [Memory Storage & Retrieval](https://arxiv.org/abs/2508.06433v2)
  Addresses long-term memory in agents with concrete storage/retrieval/update strategies (procedural memory, distillation of trajectories), which is a distinct need from standard document RAG and is currently missing from the library.
   — covers: Long-term memory retrieval in agents: memory stores, retrieval/ranking (recency/importance/relevance), summarization vs raw recall, and update policies
- **[paper]** [Agentic Retrieval-Augmented Generation: A Survey on Agentic RAG](https://arxiv.org/abs/2501.09136) *(promoted by reviewer)*
  Directly targets the lesson’s core theme (RAG inside agents) rather than generic RAG, covering iterative retrieval, planning/controller patterns, and system-level design choices that the current shelf doesn’t yet anchor with a citable survey.
   — fills: RAG as a callable tool in agent loops: repeated retrieval, planner-controller patterns, and tracing/auditability of retrieval steps
- **[paper]** [A Systematic Investigation of Document Chunking Strategies for Dense Retrieval](https://arxiv.org/html/2603.06976) *(promoted by reviewer)*
  Chunking is an explicitly uncovered gap and this appears to be a rare large-scale, cross-domain empirical study of segmentation methods—more durable and teachable than ad-hoc blog heuristics.
   — fills: Document chunking strategies: chunk size, overlap, structure-aware splitting, metadata, and impact on retrieval quality
- **[paper]** [Memory Storage & Retrieval](https://arxiv.org/abs/2508.06433v2) *(promoted by reviewer)*
  Addresses long-term memory in agents with concrete storage/retrieval/update strategies (procedural memory, distillation of trajectories), which is a distinct need from standard document RAG and is currently missing from the library.
   — fills: Long-term memory retrieval in agents: memory stores, retrieval/ranking (recency/importance/relevance), summarization vs raw recall, and update policies

## Near-Misses (12) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **What is RAG? - Retrieval-Augmented Generation AI ...** — [What is RAG? - Retrieval-Augmented Generation AI ...](https://aws.amazon.com/what-is/retrieval-augmented-generation/)
  _Skipped because:_ Clear but vendor-oriented and relatively shallow compared to the Stanford chapter and the RAG survey.
- **What is Retrieval Augmented Generation (RAG)?** — [What is Retrieval Augmented Generation (RAG)?](https://www.databricks.com/blog/what-is-retrieval-augmented-generation)
  _Skipped because:_ Good overview, but overlaps heavily with stronger, more citable sources (SLP + survey) for the same gaps.
- **[PDF] A Simple Guide to Retrieval Augmented Generation** — [[PDF] A Simple Guide to Retrieval Augmented Generation](https://elibrary-dev.nusamandiri.ac.id/assets/fileebook/250125.pdf)
  _Skipped because:_ Likely introductory and potentially unstable/less authoritative; doesn’t beat the textbook chapter or survey.
- **RAG: A Simple Introduction to Retrieval Augmented Generation** — [RAG: A Simple Introduction to Retrieval Augmented Generation](https://studylib.net/doc/28051935/intro-to-rag-1722494456)
  _Skipped because:_ Appears to be a repost/secondary hosting with unclear provenance and limited depth.
- **Document Retrieval using Embedding Search** — [Document Retrieval using Embedding Search](https://www.cs.columbia.edu/~sedwards/classes/2024/4995-fall/proposals/document_retrieval.pdf)
  _Skipped because:_ A student project proposal rather than a polished, durable teaching reference.
- **[PDF] An Efficient Model For Embedding-Based Large-Scale Ret** — [[PDF] An Efficient Model For Embedding-Based Large-Scale Retrieval](https://aclanthology.org/2021.naacl-main.292.pdf)
  _Skipped because:_ High-quality research, but it’s specialized on retrieval modeling efficiency and doesn’t directly teach RAG-in-agents or practical pipeline decisions as well as the selected sources.
- **How to Choose Between IVF and HNSW for ANN Vector Search** — [How to Choose Between IVF and HNSW for ANN Vector Search](https://milvus.io/blog/understanding-ivf-vector-index-how-It-works-and-when-to-choose-it-over-hnsw.md)
  _Skipped because:_ Useful practitioner blog, but redundant once the Faiss reference is included and less authoritative.
- **Hierarchical Navigable Small...** — [Hierarchical Navigable Small...](https://www.pinecone.io/learn/series/faiss/vector-indexes/)
  _Skipped because:_ Good practical tutorial, but overlaps with the Faiss paper and is narrower than the chosen references.
- **Filtered Approximate Nearest Neighbor Search in Vector ...** — [Filtered Approximate Nearest Neighbor Search in Vector ...](https://arxiv.org/html/2602.11443)
  _Skipped because:_ Potentially valuable but very narrow (filtered ANN) and not necessary for a core teaching shelf compared to the broader Faiss reference.
- **[PDF] Vector Retrieval** — [[PDF] Vector Retrieval](https://mdi.hkust-gz.edu.cn/static/website/files/projects/vector_retrieval.pdf)
  _Skipped because:_ Unclear provenance/authority and likely course-project notes; the Faiss paper and SLP chapter cover the fundamentals more reliably.
- **Word Embeddings for Similarity Scoring in Practical ...** — [Word Embeddings for Similarity Scoring in Practical ...](https://www.zbw.eu/fileadmin/pdf/forschung/2017-colloquium-galke-word-embeddings.pdf)
  _Skipped because:_ Older and more about word embeddings generally; doesn’t directly address modern vector DB/ANN or RAG pipeline needs.
- **Word embeddings for practical information retrieval** — [Word embeddings for practical information retrieval](https://www.mpi.nl/publications/item3367544/word-embeddings-practical-information-retrieval)
  _Skipped because:_ Likely relevant historically, but the library already has strong embedding primers and needs RAG/agent-specific material more.

## Uncovered Gaps (3) — No Good Candidates Found
_Consider manually sourcing these, or run enrichment again with different search terms._

- Document chunking strategies: chunk size, overlap, structure-aware splitting, metadata, and impact on retrieval quality
- Long-term memory retrieval in agents: memory stores, retrieval/ranking (recency/importance/relevance), summarization vs raw recall, and update policies
- RAG as a callable tool in agent loops: repeated retrieval, planner-controller patterns, and tracing/auditability of retrieval steps

## Reasoning
**Curator:** The additions prioritize authoritative, durable sources that collectively cover RAG definitions/pipelines, grounding and augmentation considerations, and the core mechanics of embedding retrieval and ANN vector search. Introductory vendor/blog explainers and student/project PDFs were excluded as redundant or insufficiently authoritative for a high-quality teaching shelf.
**Reviewer:** The curator’s additions solidly cover core RAG and vector search, but the shelf still needs one strong agentic-RAG reference plus dedicated, citable coverage for chunking and agent long-term memory.
