## Core Definitions

**Retrieval-Augmented Generation (RAG)**: A model/pipeline that “combine[s] pre-trained parametric and non-parametric memory for language generation,” where the parametric memory is a pretrained seq2seq model and the non-parametric memory is “a dense vector index of Wikipedia, accessed with a pre-trained neural retriever” (Lewis et al., 2020, *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*, https://arxiv.org/abs/2005.11401). In practice, RAG retrieves relevant passages and conditions generation on them to produce more factual, specific outputs and enable provenance and easier knowledge updates (Lewis et al., 2020).

**Vector database (vector index / ANN index)**: A storage + indexing system for embedding vectors that supports nearest-neighbor search (exact or approximate) to retrieve items whose vectors are most similar to a query vector. In production dense retrieval, Spotify precomputes episode vectors offline and indexes them in Vespa with ANN for tens of millions of episodes; online it embeds the query and retrieves top candidates by vector similarity (Spotify Engineering, 2022, https://engineering.atspotify.com/2022/3/introducing-natural-language-search-for-podcast-episodes). Faiss documents common index types and how cosine similarity is implemented via inner product on normalized vectors (Faiss wiki, https://github.com/facebookresearch/faiss/wiki/Faiss-indexes).

**Embeddings**: Numeric vector representations of text (queries, documents, passages) such that semantic similarity can be computed as a vector similarity (e.g., cosine). Dense retrieval maps query text and document text into a shared embedding space and ranks by cosine similarity (Spotify Engineering, 2022). (Contrast note for tutor: static embeddings like word2vec/GloVe give one vector per word type; contextual embeddings give token vectors dependent on sentence context—ELMo defines this distinction explicitly (ELMo paper, https://aclanthology.org/N18-1202.pdf).)

**Chunking**: Splitting source documents into smaller units (“chunks”/passages) that are embedded and indexed for retrieval. (This is a standard RAG ingestion step described in practitioner guides; within the provided sources, chunking is referenced as part of RAG pipeline construction and scaling in the Anyscale RAG production guide (https://www.anyscale.com/blog/a-comprehensive-guide-for-building-rag-based-llm-applications-part-1).)

**Cosine similarity**: A similarity measure between vectors defined as  
\[
\cos(\mathbf{v}_q,\mathbf{v}_e)=\frac{\mathbf{v}_q\cdot \mathbf{v}_e}{\|\mathbf{v}_q\|\;\|\mathbf{v}_e\|}
\]
used by Spotify for dense retrieval scoring between query embedding \(\mathbf{v}_q\) and episode embedding \(\mathbf{v}_e\) (Spotify Engineering, 2022). Faiss notes cosine similarity can be implemented as inner product search by pre-normalizing vectors and using `IndexFlatIP` (Faiss wiki).

**Hallucination (LLM context)**: Confidently inaccurate or fabricated output that can arise because foundation models are “stuck in the past” (knowledge cutoff) and are optimized to produce plausible text; Pinecone describes this as “confidently inaccurate and irrelevant output” and motivates RAG as a mitigation by grounding responses in retrieved context (Pinecone RAG explainer, https://www.pinecone.io/learn/retrieval-augmented-generation/). GPT-4 System Card lists hallucinations as a key evaluated risk area and reports improvements in avoiding hallucinations between model variants (https://cdn.openai.com/papers/gpt-4-system-card.pdf).

---

## Key Formulas & Empirical Results

### Cosine similarity (dense retrieval scoring)
From Spotify’s production dense retrieval:
\[
s(q,e)=\cos(\mathbf{v}_q,\mathbf{v}_e)=\frac{\mathbf{v}_q\cdot \mathbf{v}_e}{\|\mathbf{v}_q\|\;\|\mathbf{v}_e\|}
\]
- \(\mathbf{v}_q\): query embedding; \(\mathbf{v}_e\): episode embedding (Spotify Engineering, 2022).
- Supports: ranking candidates by semantic similarity even when term overlap is low.

### Faiss: cosine via inner product on normalized vectors
- `IndexFlatIP` performs exact inner product search; “cosine similarity via pre-normalizing vectors (then IP ≡ cosine)” (Faiss wiki).
- Supports: implementation detail students often ask: “How do I do cosine in Faiss?”

### IVF scan fraction and tuning rule of thumb (Faiss)
- Approx scanned fraction \(\approx \text{nprobe}/\text{nlist}\) (Faiss wiki, Eq. 1).
- Rule of thumb: choose `nlist = C * sqrt(n)` with \(C \approx 10\) for \(n\) points (Faiss wiki).
- Supports: practical ANN tuning trade-offs (latency vs recall).

### Late interaction (ColBERT) scoring (useful for “retrieval” variants)
ColBERT scores query–doc with MaxSim over token embeddings:
\[
S_{q,d} := \sum_{i \in [|E_q|]} \max_{j \in [|E_d|]} \mathbf{e}_{q_i}\cdot \mathbf{e}_{d_j}^{\top}
\]
- \(E_q\): set of contextualized query token embeddings; \(E_d\): doc token embeddings (ColBERT paper card, https://arxiv.org/abs/2004.12832).
- Dot product implements cosine similarity due to normalization (ColBERT card).
- Supports: explaining multi-vector retrieval and why it can outperform single-vector bi-encoders while still enabling offline indexing.

### RAG paper: key claim (qualitative, but central)
Lewis et al. (2020) report RAG “set[s] the state-of-the-art on three open domain QA tasks” and “generate[s] more specific, diverse and factual language” than a parametric-only seq2seq baseline (https://arxiv.org/abs/2005.11401).  
- Supports: why retrieval improves factuality and specificity.

### GPT-4 System Card: hallucination avoidance deltas
GPT-4-launch scored **+19 percentage points** vs latest GPT-3.5 at avoiding **open-domain** hallucinations; **+29 pp** at avoiding **closed-domain** hallucinations (GPT-4 System Card, Sec. 2.2, https://cdn.openai.com/papers/gpt-4-system-card.pdf).  
- Supports: grounding and mitigation are evaluated quantitatively in deployment.

---

## How It Works

### A. “Classic” RAG pipeline (practical, tutor-ready sequence)
1. **Ingest documents** (internal docs, web pages, PDFs, etc.).  
2. **Chunk** documents into passages suitable for retrieval (Anyscale RAG guide frames chunking as a core workload to scale: load → chunk → embed → index → serve; https://www.anyscale.com/blog/a-comprehensive-guide-for-building-rag-based-llm-applications-part-1).  
3. **Embed each chunk** into a vector using an embedding model; store vectors + metadata (doc id, source, offsets).  
4. **Index vectors** in a vector DB / ANN index (Faiss/Vespa-style).  
   - Offline indexing is standard in production: Spotify precomputes episode vectors offline and indexes in Vespa ANN (Spotify Engineering, 2022).  
5. **At query time**:
   1) Embed the **query** into \(\mathbf{v}_q\).  
   2) Retrieve **top-k** chunks by similarity (often cosine).  
   3) **Construct the LLM prompt**: user question + retrieved chunks as grounding context.  
   4) **Generate** answer conditioned on retrieved context (Lewis et al., 2020 describe conditioning generation on retrieved passages; https://arxiv.org/abs/2005.11401).  
6. **(Optional) Rerank / blend**:
   - Spotify uses dense retrieval as an additional source and blends candidates with other sources (e.g., Elasticsearch), using cosine similarity as a feature in later ranking (Spotify Engineering, 2022).  
7. **(Optional) Cite sources** by attaching chunk metadata to the answer (motivated by RAG’s provenance goal in Lewis et al., 2020).

### B. Dense retrieval in production (Spotify as concrete reference)
- **Offline**: concatenate episode metadata → embed → index in Vespa ANN for tens of millions of episodes.  
- **Online**: compute query embedding via GPU inference (Vertex AI); retrieve top ~30 semantic episodes; cache vectors for repeated queries; blend with other retrieval sources (Spotify Engineering, 2022).

### C. Alternative retrieval scoring: late interaction (ColBERT-style)
When a student asks “why not just one embedding per doc?”:
1. Encode query and doc independently into **sets** of token embeddings (bags of contextualized token vectors).  
2. Score with MaxSim aggregation (formula above).  
3. Enables **offline doc encoding** + fast online query encoding, while preserving token-level matching signals (ColBERT card, https://arxiv.org/abs/2004.12832).

---

## Teaching Approaches

### Intuitive (no math)
- **RAG = open-book exam**: the LLM is the student; the vector DB is the library index. Instead of answering from memory (parameters), it looks up relevant pages and answers with them in view. This reduces confident guessing when the model’s “memory” is outdated (knowledge cutoff) or missing private info (Pinecone RAG explainer).

### Technical (with math)
- Represent query and chunks as vectors; retrieve by cosine similarity \( \cos(\mathbf{v}_q,\mathbf{v}_d)\) (Spotify).  
- Use ANN indexes (Faiss IVF/HNSW) to avoid scanning all vectors; tune `nlist/nprobe` or `M/efSearch` to trade recall vs latency (Faiss wiki).  
- Generation is conditioned on retrieved passages; Lewis et al. (2020) frame this as combining parametric + non-parametric memory.

### Analogy-based
- **Parametric vs non-parametric memory** (Lewis et al., 2020):  
  - Parametric memory = what’s “baked into” weights (hard to update).  
  - Non-parametric memory = an external, editable knowledge store (vector index) you can update without retraining the LLM.

---

## Common Misconceptions

1. **“If I add RAG, the model can’t hallucinate anymore.”**  
   - Why wrong: RAG *reduces* hallucination risk by grounding, but the generator can still ignore/misuse context or retrieve irrelevant chunks. Pinecone motivates RAG as a mitigation for hallucination, not a guarantee (https://www.pinecone.io/learn/retrieval-augmented-generation/).  
   - Correct model: RAG adds an evidence channel; quality depends on retrieval (recall/precision), prompt conditioning, and downstream ranking.

2. **“A vector database is just a normal database with vectors; it always returns the exact nearest neighbors.”**  
   - Why wrong: Many deployments use **approximate** nearest neighbor (ANN) for speed (Spotify uses Vespa ANN; Faiss documents IVF/HNSW). ANN trades accuracy for latency.  
   - Correct model: Choose exact (`IndexFlat*`) vs approximate (IVF/HNSW/PQ) based on scale/latency; tune parameters like `nprobe` (Faiss wiki).

3. **“Cosine similarity and dot product are totally different; I must implement cosine explicitly.”**  
   - Why wrong: If vectors are normalized, inner product equals cosine similarity; Faiss explicitly notes cosine via `IndexFlatIP` with pre-normalization (Faiss wiki).  
   - Correct model: Normalize embeddings once; use inner product search.

4. **“Chunking is just splitting every N tokens; it doesn’t affect retrieval quality much.”**  
   - Why wrong: The Anyscale guide treats chunking as a core design lever in RAG pipelines (load/chunk/embed/index/serve) and a major axis of evaluation/optimization (https://www.anyscale.com/blog/a-comprehensive-guide-for-building-rag-based-llm-applications-part-1).  
   - Correct model: Chunk size/overlap changes what can be retrieved and what context fits in the prompt; it’s a first-order quality knob.

5. **“Dense retrieval replaces keyword search; you should delete Elasticsearch.”**  
   - Why wrong: Spotify explicitly treats dense retrieval as an additional source that can underperform exact term matching and is costlier; they blend dense + Elasticsearch candidates and rerank (Spotify Engineering, 2022).  
   - Correct model: Hybrid retrieval is common: sparse for exact matches, dense for semantic matches, rerank to combine.

---

## Worked Examples

### Example 1: Minimal RAG retrieval loop (Faiss cosine via inner product)
Goal: show the *mechanics* students ask for: embed → normalize → index → query → top-k.

```python
import numpy as np
import faiss

# Suppose you already have embeddings from an embedding model:
# doc_vecs: (N, d), query_vec: (d,)
doc_vecs = np.random.randn(1000, 384).astype("float32")
query_vec = np.random.randn(384).astype("float32")

# 1) Normalize so inner product == cosine similarity (Faiss wiki)
faiss.normalize_L2(doc_vecs)
faiss.normalize_L2(query_vec.reshape(1, -1))

# 2) Build an exact inner-product index (cosine via IP)
d = doc_vecs.shape[1]
index = faiss.IndexFlatIP(d)  # exact search

# 3) Add vectors
index.add(doc_vecs)

# 4) Search top-k
k = 5
scores, ids = index.search(query_vec.reshape(1, -1), k)

print(ids[0], scores[0])
```

Tutor notes (tie to sources):
- Use `IndexFlatIP` + normalization for cosine (Faiss wiki).
- For scale, swap to IVF/HNSW and tune `nlist/nprobe` or `M/efSearch` (Faiss wiki).

### Example 2: ANN tuning intuition with IVF (Faiss)
If a student asks “what does `nprobe` do?”:
- IVF partitions vectors into `nlist` clusters; query probes `nprobe` lists.  
- Approx scanned fraction \(\approx nprobe/nlist\) (Faiss wiki).  
- So increasing `nprobe` increases recall but increases latency.

---

## Comparisons & Trade-offs

| Choice | What it is | Pros | Cons | When to choose | Source |
|---|---|---|---|---|---|
| Sparse (term) retrieval | Keyword/term matching (e.g., Elasticsearch) | Exact matches, cheap | Misses paraphrases/semantic matches | When queries match metadata/text well | Spotify notes term search can return nothing for NL queries | https://engineering.atspotify.com/2022/3/introducing-natural-language-search-for-podcast-episodes |
| Dense retrieval (bi-encoder) | One vector per query/doc; cosine similarity | Semantic matching; multilingual possible | Can miss exact constraints; costlier | Natural-language queries, semantic search | Spotify dense retrieval | same |
| Late interaction (ColBERT) | Multi-vector per doc; MaxSim scoring | Better token-level matching than single-vector | More storage/compute than bi-encoder | When bi-encoder recall is insufficient | ColBERT | https://arxiv.org/abs/2004.12832 |
| Exact NN (Flat) | Scan all vectors | Exact results, simple | Too slow at large N | Small corpora / evaluation baseline | Faiss | https://github.com/facebookresearch/faiss/wiki/Faiss-indexes |
| ANN IVF | Inverted lists + probing | Fast at scale; tunable | Approximate; needs training | Large corpora; latency constraints | Faiss | same |
| ANN HNSW | Graph-based ANN | High recall/latency tradeoff | No removal support (per Faiss) | Static-ish corpora needing fast queries | Faiss | same |

---

## Prerequisite Connections

- **Vector similarity & normalization**: Needed to understand cosine similarity and why Faiss can use inner product for cosine (Faiss wiki; Spotify cosine formula).  
- **Embeddings concept**: Needed to understand how text becomes vectors for retrieval (Spotify dense retrieval description).  
- **Indexing vs querying (offline vs online)**: Needed to reason about latency/cost; Spotify’s offline precompute + online query embedding is the canonical pattern (Spotify Engineering, 2022).  
- **LLM prompting / context windows**: Needed to understand “inject retrieved chunks into the prompt” and why chunking matters (Anyscale RAG guide).

---

## Socratic Question Bank

1. **If your retriever returns irrelevant chunks, what failure mode do you expect from the generator—and how would you detect whether the problem is retrieval vs generation?**  
   - Good answer: distinguish retrieval precision/recall vs model ignoring context; propose inspecting retrieved passages and measuring retrieval quality separately.

2. **Why does Spotify keep term-based retrieval in the system even after adding dense retrieval?**  
   - Good answer: dense can underperform exact matching and is costlier; blending improves coverage (Spotify).

3. **If you normalize all vectors, what similarity metric does `IndexFlatIP` implement? Why?**  
   - Good answer: cosine similarity because normalized dot product equals cosine (Faiss wiki).

4. **In IVF, what happens to latency and recall when you increase `nprobe`?**  
   - Good answer: both increase; scanned fraction \(\approx nprobe/nlist\) (Faiss).

5. **What is the conceptual difference between parametric memory and non-parametric memory in RAG?**  
   - Good answer: weights vs external index; external is editable and can provide provenance (Lewis et al., 2020).

6. **When might a single-vector bi-encoder be insufficient, and what retrieval model family addresses that?**  
   - Good answer: token-level matching needed; late interaction like ColBERT (MaxSim) (ColBERT).

7. **How would chunk size affect retrieval and generation quality?**  
   - Good answer: too small loses context; too large dilutes relevance and wastes context window; chunking is a key pipeline knob (Anyscale).

8. **What operational constraints show up in production dense retrieval systems?**  
   - Good answer: offline indexing throughput, online embedding latency/cost, caching, blending sources (Spotify).

---

## Likely Student Questions

**Q: What’s the exact cosine similarity formula used in dense retrieval?**  
→ **A:** Spotify defines \(s(q,e)=\cos(\mathbf{v}_q,\mathbf{v}_e)=\frac{\mathbf{v}_q\cdot \mathbf{v}_e}{\|\mathbf{v}_q\|\|\mathbf{v}_e\|}\), where \(\mathbf{v}_q\) is the query embedding and \(\mathbf{v}_e\) is the episode embedding (Spotify Engineering, 2022, https://engineering.atspotify.com/2022/3/introducing-natural-language-search-for-podcast-episodes).

**Q: How do I do cosine similarity search in Faiss?**  
→ **A:** Pre-normalize vectors and use inner product search; Faiss notes “cosine similarity via pre-normalizing vectors (then IP ≡ cosine)” and you can use `IndexFlatIP` for exact search (Faiss wiki, https://github.com/facebookresearch/faiss/wiki/Faiss-indexes).

**Q: What does `nprobe` do in an IVF index?**  
→ **A:** `nprobe` is the number of inverted lists visited at query time; Faiss gives an approximate scanned fraction \(\approx nprobe/nlist\) (Faiss wiki).

**Q: Why doesn’t dense retrieval fully replace keyword search?**  
→ **A:** Spotify reports dense retrieval is an additional source: it can underperform exact term matching and is costlier; they blend dense candidates with Elasticsearch and rerank, using cosine similarity as a feature (Spotify Engineering, 2022).

**Q: What is RAG, formally, in the original paper’s framing?**  
→ **A:** Lewis et al. define RAG as combining parametric memory (a pretrained seq2seq model) with non-parametric memory (a dense vector index of Wikipedia accessed by a neural retriever) for language generation (https://arxiv.org/abs/2005.11401).

**Q: How does ColBERT scoring work, and why is it relevant to retrieval for RAG?**  
→ **A:** ColBERT encodes query and doc into sets of token embeddings and scores \(S_{q,d}=\sum_i \max_j \mathbf{e}_{q_i}\cdot \mathbf{e}_{d_j}^\top\) (MaxSim late interaction). It preserves token-level matching while enabling offline doc encoding and fast retrieval via vector indexes (ColBERT card, https://arxiv.org/abs/2004.12832).

**Q: Do deployed models still have hallucination issues even with mitigations? How is it measured?**  
→ **A:** The GPT-4 System Card lists hallucinations as a key risk area and reports GPT-4-launch improved at avoiding hallucinations vs GPT-3.5 by **+19 pp** (open-domain) and **+29 pp** (closed-domain) (https://cdn.openai.com/papers/gpt-4-system-card.pdf). Pinecone motivates RAG as a mitigation for hallucinations caused by knowledge cutoffs and missing private data (https://www.pinecone.io/learn/retrieval-augmented-generation/).

---

## Available Resources

### Videos
- [Intro to Large Language Models (Karpathy)](https://youtube.com/watch?v=zjkBMFhNj_g) — Surface when: student asks *why* retrieval helps LLMs or wants intuition for “LLM as two files + external knowledge access” framing.

### Articles & Tutorials
- [Pinecone — Retrieval-Augmented Generation](https://www.pinecone.io/learn/retrieval-augmented-generation/) — Surface when: student asks what hallucination is, why knowledge cutoffs matter, or what RAG fixes at a product level.
- [Anyscale — Comprehensive guide for building RAG-based LLM applications (Part 1)](https://www.anyscale.com/blog/a-comprehensive-guide-for-building-rag-based-llm-applications-part-1) — Surface when: student asks about end-to-end production pipeline steps (chunk/embed/index/serve) and evaluation/cost trade-offs.
- [Lewis et al. (2020) — Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401) — Surface when: student asks for the original formal definition of RAG and what variants exist (conditioning on same passages vs varying per token, per abstract).
- [Spotify Engineering — Natural Language Search for Podcast Episodes](https://engineering.atspotify.com/2022/3/introducing-natural-language-search-for-podcast-episodes) — Surface when: student asks “how does this look in production?” (offline indexing, ANN, GPU query embedding, blending with Elasticsearch).

---

## Visual Aids

![Self-Ask: LLM decomposes questions and queries external search. (Press et al. 2022)](/api/wiki-images/rag-retrieval/images/lilianweng-posts-2023-03-15-prompt-engineering_001.png)  
Show when: student confuses “RAG retrieval” with “just add more prompt text”; use to illustrate explicit external querying as part of a reasoning/retrieval loop.

---

## Key Sources

- [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks (Lewis et al., 2020)](https://arxiv.org/abs/2005.11401) — Foundational RAG framing: parametric + non-parametric memory for generation; motivates provenance and updatable knowledge.
- [Spotify Engineering: Natural Language Search for Podcast Episodes](https://engineering.atspotify.com/2022/3/introducing-natural-language-search-for-podcast-episodes) — Concrete production dense retrieval architecture, cosine scoring, blending dense+sparse, and operational constraints.
- [Faiss Indexes Wiki](https://github.com/facebookresearch/faiss/wiki/Faiss-indexes) — Authoritative implementation reference for index choices and cosine-via-inner-product details.
- [Pinecone RAG explainer](https://www.pinecone.io/learn/retrieval-augmented-generation/) — Clear articulation of hallucination drivers (knowledge cutoff, missing private data) and why RAG improves trust via grounding.
- [ColBERT (Khattab & Zaharia, 2020)](https://arxiv.org/abs/2004.12832) — Retrieval scoring alternative (late interaction MaxSim) useful for advanced “why embeddings sometimes fail” discussions.