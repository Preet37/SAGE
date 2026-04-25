# Curation Report: Knowledge Graphs and Structured Knowledge
**Topic:** `knowledge-graphs` | **Date:** 2026-04-09 18:41
**Library:** 1 existing → 15 sources (14 added, 9 downloaded)
**Candidates evaluated:** 50
**Reviewer verdict:** needs_additions

## Added (14)
- **[explainer]** [Construction of Knowledge Graphs: State and Challenges - arXiv](https://arxiv.org/html/2302.11509)
  Gives the tutor a structured, step-by-step view of how KGs are built in practice beyond RDF basics, including where entity linking, schema alignment, canonicalization, and quality control fit and why they are hard.
- **[paper]** [Complex Embeddings for Simple Link Prediction](https://arxiv.org/pdf/1606.06357.pdf)
  Provides citable, explicit equations for a core KG embedding model (ComplEx) and its learning setup, which the tutor can use to derive link prediction behavior (symmetry/antisymmetry) and losses.
- **[paper]** [2019 Formatting Instructions for Authors Using LaTeX](http://arxiv.org/pdf/1811.04441v2.pdf)
  Despite the odd title, this is the RotatE arXiv PDF and is a strong single source for both benchmark tables and a widely-taught embedding model’s empirical performance.
- **[reference_doc]** [Creating Single Property Indexes](https://www.graphacademy.neo4j.com/courses/cypher-indexes-constraints/3-indexes/02-create-index/)
  Adds production-grade, query-language-specific guidance the tutor can quote when teaching how KGs are operationalized in graph databases (index creation and expected behavior).
- **[paper]** [Translating Embeddings for Modeling Multi-relational Data (TransE)](https://papers.nips.cc/paper_files/paper/2013/hash/1cecc7a77928ca8133fa24680a88d2f9-Abstract.html)
  The library explicitly lacks a primary, citable TransE formulation and objective; this seminal paper is the canonical source for the equations and the negative-sampling training procedure tutors routinely teach.
- **[paper]** [Embedding Entities and Relations for Learning and Inference in Knowledge Bases (DistMult)](https://arxiv.org/abs/1412.6575)
  DistMult is a core baseline in KG embeddings, but the current library has no primary source with the explicit formula and learning setup; this paper provides the exact equations used in most derivations and comparisons.
- **[reference_doc]** [Neo4j Cypher Manual — Indexes for search performance](https://neo4j.com/docs/cypher-manual/current/indexes-for-search-performance/)
  The current index page is useful but narrow; the Cypher Manual section is the authoritative, comprehensive reference a tutor can quote for index types and semantics across versions.
- **[reference_doc]** [Neo4j Cypher Manual — Constraints](https://neo4j.com/docs/cypher-manual/current/constraints/)
  Constraints are central to KG integrity (deduplication, identifiers, schema enforcement) and are missing from the library; this is the official place for exact syntax and semantics.
- **[benchmark]** [DAEA: Enhancing Entity Alignment in Real-World Knowledge Graphs](https://aclanthology.org/2025.coling-main.393v1.pdf)
  Entity alignment benchmark numbers are an explicitly unfilled need; this paper appears to include concrete tables and modern comparisons that a tutor can cite when teaching alignment evaluation.
- **[paper]** [Translating Embeddings for Modeling Multi-relational Data (TransE)](https://papers.nips.cc/paper_files/paper/2013/hash/1cecc7a77928ca8133fa24680a88d2f9-Abstract.html) *(promoted by reviewer)*
  The library explicitly lacks a primary, citable TransE formulation and objective; this seminal paper is the canonical source for the equations and the negative-sampling training procedure tutors routinely teach.
- **[paper]** [Embedding Entities and Relations for Learning and Inference in Knowledge Bases (DistMult)](https://arxiv.org/abs/1412.6575) *(promoted by reviewer)*
  DistMult is a core baseline in KG embeddings, but the current library has no primary source with the explicit formula and learning setup; this paper provides the exact equations used in most derivations and comparisons.
- **[reference_doc]** [Neo4j Cypher Manual — Indexes for search performance](https://neo4j.com/docs/cypher-manual/current/indexes-for-search-performance/) *(promoted by reviewer)*
  The current index page is useful but narrow; the Cypher Manual section is the authoritative, comprehensive reference a tutor can quote for index types and semantics across versions.
- **[reference_doc]** [Neo4j Cypher Manual — Constraints](https://neo4j.com/docs/cypher-manual/current/constraints/) *(promoted by reviewer)*
  Constraints are central to KG integrity (deduplication, identifiers, schema enforcement) and are missing from the library; this is the official place for exact syntax and semantics.
- **[benchmark]** [DAEA: Enhancing Entity Alignment in Real-World Knowledge Graphs](https://aclanthology.org/2025.coling-main.393v1.pdf) *(promoted by reviewer)*
  Entity alignment benchmark numbers are an explicitly unfilled need; this paper appears to include concrete tables and modern comparisons that a tutor can cite when teaching alignment evaluation.

## Near-Misses (4) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **[PDF] Complex Embeddings for Simple Link Prediction** — [[PDF] Complex Embeddings for Simple Link Prediction](https://proceedings.mlr.press/v48/trouillon16.pdf)
  _Skipped because:_ Redundant with the arXiv PDF version selected; kept only one canonical copy to conserve library slots.
- **Creating and Using Full-text Indexes** — [Creating and Using Full-text Indexes](https://www.graphacademy.neo4j.com/courses/cypher-indexes-constraints/4-full-text/02-create-full-text-index/)
  _Skipped because:_ Useful for full-text specifics (db.index.fulltext.queryNodes/Relationships), but the single-property index page was prioritized as the more foundational API reference given the slot limit.
- **Uncertainty Management in the Construction of Knowledge Grap** — [Uncertainty Management in the Construction of Knowledge Graphs](https://arxiv.org/html/2405.16929v2)
  _Skipped because:_ Excellent for provenance/uncertainty handling, but the broader construction pipeline survey was chosen as the primary end-to-end explainer under the slot cap.
- **KnowledgeGraphEmbedding/README.md at master · DeepGraphLearn** — [KnowledgeGraphEmbedding/README.md at master · DeepGraphLearning/KnowledgeGraphEmbedding](https://github.com/DeepGraphLearning/KnowledgeGraphEmbedding/blob/master/README.md)
  _Skipped because:_ Strong practical implementation pointer, but it is not as citable/authoritative for benchmark numbers and formulas as the original papers selected.

## Reasoning
**Curator:** Selections prioritize (1) an end-to-end KG construction survey for practical pipeline teaching, (2) primary-source embedding equations (ComplEx) plus a widely-used benchmarked model (RotatE), and (3) a production graph DB/Cypher indexing reference; remaining gaps require additional primary papers and an authoritative GraphRAG implementation.
**Reviewer:** The current set is strong for RDF basics and a couple of embedding models, but it misses canonical primary sources for TransE/DistMult, official Neo4j constraint/index documentation, and a concrete entity-alignment benchmark table source.
