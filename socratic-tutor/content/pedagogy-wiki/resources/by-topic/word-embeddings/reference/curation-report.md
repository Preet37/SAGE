# Curation Report: Word Embeddings
**Topic:** `word-embeddings` | **Date:** 2026-04-09 16:40
**Library:** 5 existing → 20 sources (15 added, 10 downloaded)
**Candidates evaluated:** 40
**Reviewer verdict:** needs_additions

## Added (15)
- **[paper]** [Glove: Global Vectors for Word Representation](https://aclanthology.org/D14-1162.pdf)
  Provides the canonical, citable GloVe loss and training setup, with the explicit connection to co-occurrence statistics that a tutor can derive and quote.
- **[benchmark]** [Glove: Global Vectors for Word Representation](https://aclanthology.org/D14-1162.pdf)
  Supplies canonical early embedding evaluation numbers and experimental settings that can be cited when students ask “how good is it” and “what settings mattered.”
- **[reference_doc]** [models.word2vec – Word2vec embeddings — gensim](https://radimrehurek.com/gensim/models/word2vec.html)
  Gives the tutor exact, quotable API defaults and parameter semantics for a widely used library, enabling precise guidance and mapping to paper terminology.
- **[paper]** [Deep Contextualized Word Representations](https://aclanthology.org/N18-1202.pdf)
  Provides an authoritative, citable basis for explaining why contextual embeddings handle polysemy and how they are evaluated extrinsically, with concrete metrics.
- **[paper]** [Talent Search and Recommendation Systems at LinkedIn: Practical Challenges and Lessons Learned](https://engineering.linkedin.com/content/dam/me/engineering/li-en/research/SIGIR-2018.pdf)
  Adds a real-world, system-level view of how embeddings are used in large-scale search/recommendation, supporting teaching about deployment constraints and design decisions.
- **[paper]** [Distributed Representations of Words and Phrases and their Compositionality](https://proceedings.neurips.cc/paper_files/paper/2013/file/9aa42b31882ec039965f3c4923ce901b-Paper.pdf)
  This is the canonical word2vec paper that actually defines negative sampling and HS in a citable way; it directly fills the missing “exact loss/training procedure” need.
- **[paper]** [Deriving Mikolov et al.'s Negative-Sampling Word-Embedding Method](https://arxiv.org/pdf/1402.3722.pdf)
  Even if the library has Mikolov papers, this is the cleanest, most teachable derivation for the PMI/shifted-PMI connection that students commonly ask about.
- **[reference_doc]** [word2vec (original C implementation) — code + README/usage flags](https://code.google.com/archive/p/word2vec/)
  The “thin” README/usage is exactly the authoritative source for parameter names/defaults that learners encounter in practice and that map directly to the original papers.
- **[reference_doc]** [GloVe project page (Stanford NLP) — code + training instructions](https://nlp.stanford.edu/projects/glove/)
  Not redundant with the paper: it’s the canonical place for implementation-level knobs and the end-to-end procedure students need to reproduce results.
- **[paper]** [A Systematic Comparison of Contextualized Word Embeddings for Lexical Semantic Change](https://aclanthology.org/2024.naacl-long.240.pdf)
  While task-specific, it’s a recent, careful “apples-to-apples” comparison paper with tables and protocol discussion—useful for teaching how contextual embedding evaluations can be misleading without controls.
- **[paper]** [Distributed Representations of Words and Phrases and their Compositionality](https://proceedings.neurips.cc/paper_files/paper/2013/file/9aa42b31882ec039965f3c4923ce901b-Paper.pdf) *(promoted by reviewer)*
  This is the canonical word2vec paper that actually defines negative sampling and HS in a citable way; it directly fills the missing “exact loss/training procedure” need.
- **[paper]** [Deriving Mikolov et al.'s Negative-Sampling Word-Embedding Method](https://arxiv.org/pdf/1402.3722.pdf) *(promoted by reviewer)*
  Even if the library has Mikolov papers, this is the cleanest, most teachable derivation for the PMI/shifted-PMI connection that students commonly ask about.
- **[reference_doc]** [word2vec (original C implementation) — code + README/usage flags](https://code.google.com/archive/p/word2vec/) *(promoted by reviewer)*
  The “thin” README/usage is exactly the authoritative source for parameter names/defaults that learners encounter in practice and that map directly to the original papers.
- **[reference_doc]** [GloVe project page (Stanford NLP) — code + training instructions](https://nlp.stanford.edu/projects/glove/) *(promoted by reviewer)*
  Not redundant with the paper: it’s the canonical place for implementation-level knobs and the end-to-end procedure students need to reproduce results.
- **[paper]** [A Systematic Comparison of Contextualized Word Embeddings for Lexical Semantic Change](https://aclanthology.org/2024.naacl-long.240.pdf) *(promoted by reviewer)*
  While task-specific, it’s a recent, careful “apples-to-apples” comparison paper with tables and protocol discussion—useful for teaching how contextual embedding evaluations can be misleading without controls.

## Near-Misses (4) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **[PDF] GloVe: Global Vectors for Word Representation - Stanfo** — [[PDF] GloVe: Global Vectors for Word Representation - Stanford NLP Group](https://nlp.stanford.edu/pubs/glove.pdf)
  _Skipped because:_ Redundant with the ACL Anthology version of the same paper; kept only one canonical copy.
- **models.word2vec – Word2vec embeddings - gensim** — [models.word2vec – Word2vec embeddings - gensim](https://radimrehurek.com/gensim_3.8.3/models/word2vec.html)
  _Skipped because:_ Version-pinned docs can be useful, but the main gensim docs are sufficient and reduce duplication.
- **A Survey on Contextual Embeddings** — [A Survey on Contextual Embeddings](https://ar5iv.labs.arxiv.org/html/2003.07278)
  _Skipped because:_ Potentially useful for broad comparison, but the ar5iv HTML mirror is less canonical than primary venues and the candidate list lacks a clearly benchmark-heavy comparison section.
- **KDD 2017 Deep Learning Tutorial** — [KDD 2017 Deep Learning Tutorial](https://engineering.linkedin.com/data/publications/kdd-2017/deep-learning-tutorial)
  _Skipped because:_ More tutorial-like and less specific/quantitative about embedding training/serving details than the SIGIR-2018 LinkedIn paper.

## Reasoning
**Curator:** Selections prioritize canonical papers for equations/benchmarks (GloVe, ELMo), an authoritative API reference (gensim Word2Vec docs), and a credible production-oriented system paper (LinkedIn SIGIR-2018). Remaining gaps are primarily word2vec-specific objectives/ablations and official CLI/code defaults, which require additional targeted sources beyond the provided candidates.
**Reviewer:** The library is strong on high-level explainers and GloVe/ELMo, but it’s missing the canonical word2vec objective/derivation sources and the official word2vec/GloVe implementation docs that provide exact losses, defaults, and reproducible training procedures.

---

# Curation Report: Retrieval-Augmented Generation (RAG) Inside Agents
**Topic:** `word-embeddings` | **Date:** 2026-04-10 19:29
**Library:** 11 existing → 24 sources (13 added, 8 downloaded)
**Candidates evaluated:** 45
**Reviewer verdict:** needs_additions

## Added (13)
- **[paper]** [[PDF] Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://proceedings.neurips.cc/paper/2020/file/6b493230205f780e1bc26945df7481e5-Paper.pdf)
  This is the canonical RAG paper with the exact probabilistic formulation and training objective details the tutor can quote when students ask how RAG marginalizes over retrieved passages.
- **[paper]** [[PDF] Dense Passage Retrieval for Open-Domain Question Answering](https://aclanthology.org/2020.emnlp-main.550.pdf)
  Provides the standard dense retrieval scoring function and contrastive training setup used in modern RAG stacks, including concrete equations and the negative sampling procedure.
- **[benchmark]** [[PDF] KILT: a Benchmark for Knowledge Intensive Language Tasks](https://aclanthology.org/2021.naacl-main.200.pdf)
  Gives citable benchmark numbers and an evaluation framework explicitly tying generation quality to evidence retrieval/attribution, which is central for teaching grounded RAG inside agents.
- **[reference_doc]** [HNSW | Milvus Documentation](https://milvus.io/docs/hnsw.md)
  Official, production-oriented documentation that the tutor can cite for exact ANN index knobs and how they affect recall/latency in vector search.
- **[paper]** [Metamorphic Testing for Hallucination Detection in RAG Systems](https://arxiv.org/html/2509.09360v1)
  Closest candidate to a production-facing RAG evaluation/monitoring story, offering a concrete, repeatable testing workflow that can be taught as an operational practice.
- **[paper]** [Dense Passage Retrieval for Open-Domain Question Answering](https://aclanthology.org/2020.emnlp-main.550.pdf)
  The arXiv version is fine, but the ACL Anthology PDF is the authoritative, stable, citable version that students can quote for the exact loss and training procedure without link-rot.
- **[paper]** [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://proceedings.neurips.cc/paper/2020/hash/6b493230205f780e1bc26945df7481e5-Abstract.html)
  Even if you already include the PDF, the official NeurIPS proceedings entry is a high-value bibliographic anchor for teaching and citation (version-of-record), and was skipped due to being 'just an abstract'.
- **[benchmark]** [KILT: a Benchmark for Knowledge Intensive Language Tasks](https://discovery.ucl.ac.uk/id/eprint/10129948/1/Rockta%CC%88schel_2021.naacl-main.200.pdf)
  This is the stable, camera-ready NAACL PDF; it’s more reliable for quoting exact tables/metrics than mirrored HTML/PDF variants and was likely overlooked as duplicative.
- **[reference_doc]** [IVF_FLAT | Milvus Documentation](https://milvus.io/docs/ivf.md)
  Thin API docs are precisely what a reference library needs; IVF is widely deployed and teaches a different recall/latency control surface than HNSW, so excluding it leaves a practical gap.
- **[paper]** [Dense Passage Retrieval for Open-Domain Question Answering](https://aclanthology.org/2020.emnlp-main.550.pdf) *(promoted by reviewer)*
  The arXiv version is fine, but the ACL Anthology PDF is the authoritative, stable, citable version that students can quote for the exact loss and training procedure without link-rot.
- **[paper]** [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://proceedings.neurips.cc/paper/2020/hash/6b493230205f780e1bc26945df7481e5-Abstract.html) *(promoted by reviewer)*
  Even if you already include the PDF, the official NeurIPS proceedings entry is a high-value bibliographic anchor for teaching and citation (version-of-record), and was skipped due to being 'just an abstract'.
- **[benchmark]** [KILT: a Benchmark for Knowledge Intensive Language Tasks](https://discovery.ucl.ac.uk/id/eprint/10129948/1/Rockta%CC%88schel_2021.naacl-main.200.pdf) *(promoted by reviewer)*
  This is the stable, camera-ready NAACL PDF; it’s more reliable for quoting exact tables/metrics than mirrored HTML/PDF variants and was likely overlooked as duplicative.
- **[reference_doc]** [IVF_FLAT | Milvus Documentation](https://milvus.io/docs/ivf.md) *(promoted by reviewer)*
  Thin API docs are precisely what a reference library needs; IVF is widely deployed and teaches a different recall/latency control surface than HNSW, so excluding it leaves a practical gap.

## Near-Misses (3) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **IVF_FLAT | Milvus Documentation** — [IVF_FLAT | Milvus Documentation](https://milvus.io/docs/ivf-flat.md)
  _Skipped because:_ Useful for IVF nlist/nprobe-style parameters, but HNSW was selected as the single most broadly used ANN configuration reference among the provided Milvus candidates.
- **Designing Production-Ready RAG Pipelines: Tackling Latency .** — [Designing Production-Ready RAG Pipelines: Tackling Latency ...](https://hackernoon.com/designing-production-ready-rag-pipelines-tackling-latency-hallucinations-and-cost-at-scale)
  _Skipped because:_ Not as authoritative/citable as the arXiv version of the same content, so the peer-reviewable/preprint source was preferred.
- **From Explainable Evaluation to Actionable Guidance of RAG Pi** — [From Explainable Evaluation to Actionable Guidance of RAG Pipelines](https://arxiv.org/html/2505.13538v2)
  _Skipped because:_ Potentially strong for ablations and actionable diagnostics, but the provided preview appears mismatched/duplicative, making KILT the safer, clearly identified benchmark pick from the candidates.

## Reasoning
**Curator:** Selections prioritize (1) canonical equations for RAG and dense retrieval training, (2) a widely cited benchmark tying generation to evidence provenance, and (3) official vector-search parameter documentation; remaining candidates did not provide a clearly authoritative, code-level agentic RAG loop example.
**Reviewer:** The curator’s core picks are strong, but adding the version-of-record PDFs/proceedings for DPR/RAG/KILT and including IVF_FLAT docs would materially improve citation stability and practical ANN parameter coverage.
