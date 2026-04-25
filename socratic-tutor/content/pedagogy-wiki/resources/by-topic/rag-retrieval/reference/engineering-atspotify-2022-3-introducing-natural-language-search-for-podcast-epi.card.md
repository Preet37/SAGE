# Card: Spotify Natural Language Search (Dense Retrieval) for Podcast Episodes
**Source:** https://engineering.atspotify.com/2022/3/introducing-natural-language-search-for-podcast-episodes  
**Role:** explainer | **Need:** DEPLOYMENT_CASE  
**Anchor:** Production architecture narrative for moving from term-based search to semantic retrieval + ranking + operational constraints

## Key Content
- **Problem with term matching:** Elasticsearch term-based retrieval can return nothing for natural-language queries (e.g., “electric cars climate impact”) when no episode metadata contains all query terms; fuzzy matching/aliases don’t cover all paraphrases.
- **Dense retrieval setup (shared embedding space):** Train encoders to map **query text** and **episode text** (concatenated metadata: episode title/description + parent show title/description, etc.) into vectors.
- **Eq. 1 (Cosine similarity):**  
  \[
  s(q,e)=\cos(\mathbf{v}_q,\mathbf{v}_e)=\frac{\mathbf{v}_q\cdot \mathbf{v}_e}{\|\mathbf{v}_q\|\;\|\mathbf{v}_e\|}
  \]  
  where \(\mathbf{v}_q\)=query embedding, \(\mathbf{v}_e\)=episode embedding.
- **Model choice rationale:** Vanilla BERT yields weak off-the-shelf sentence embeddings (per SBERT findings) and is English-only; Spotify chose **Universal Sentence Encoder CMLM multilingual** (100+ languages) because **CMLM objective** targets sentence embeddings directly.
- **Training data pipeline:**  
  1) Positive (query, episode) pairs from successful search logs (from prior Elasticsearch results).  
  2) Query reformulations: (failed_query_before_success, episode).  
  3) Synthetic queries: fine-tune **BART on MS MARCO**, generate (synthetic_query, episode) pairs (inspired by “Embedding-based Zero-shot Retrieval through Query Generation”).  
  4) Small manually curated semantic query set (evaluation only).  
  Split ensures eval episodes not in train.
- **Negatives & loss:** Use **in-batch negatives** with batch size \(B\): positives \(=B\); negatives \(=B^2-B\). Compute in-batch cosine similarity matrix; use losses incl. **MSE vs identity**, plus **hard negative mining** and **margin loss**.
- **Offline/online production architecture:**  
  - Offline: precompute episode vectors; index in **Vespa** with **ANN** for tens of millions of episodes; first-phase ranking can add features (e.g., popularity).  
  - Online: compute query vector via **Vertex AI GPU inference**; **T4 GPU ~6× cheaper than CPU** in load tests; retrieve **top 30** semantic episodes; use **vector cache** for repeated queries.
- **Multi-source retrieval:** Dense retrieval is an *additional* source (can underperform exact term matching and is costlier). Final-stage reranker blends candidates from dense + other sources (incl. Elasticsearch) and adds **cosine similarity** as a feature.  
- **Outcome:** A/B test showed **significant increase in podcast engagement**; rolled out to most users.

## When to surface
Use when students ask how to deploy semantic search in production (offline indexing + ANN + online encoding), how to blend dense and sparse retrieval, or how to train dense retrievers with in-batch negatives and operational cost/latency constraints.