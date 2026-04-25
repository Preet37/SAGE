# Card: Deployed Dense Retrieval for Semantic Podcast Episode Search
**Source:** https://engineering.atspotify.com/2022/03/introducing-natural-language-search-for-podcast-episodes  
**Role:** explainer | **Need:** DEPLOYMENT_CASE  
**Anchor:** End-to-end deployed dense retrieval architecture (shared embeddings + ANN serving) + operational considerations for online vector search

## Key Content
- **Dense retrieval setup (Eq. 1: cosine similarity):** Train encoders to map **query text** and **episode text metadata** into a **shared embedding space**; retrieve by nearest neighbors.  
  - Episode input text = concatenation of fields: episode title/description + parent show title/description + other metadata.  
  - Similarity: **cos(q, d) = (q·d) / (||q||·||d||)** where *q* = query vector, *d* = episode vector.
- **Model choice rationale:** Vanilla BERT not ideal because (1) off-the-shelf **sentence** embeddings are weak (SBERT finding), (2) English-only pretraining. Chosen base: **Universal Sentence Encoder CMLM multilingual** (100+ languages) with **Conditional Masked Language Modeling** objective designed for sentence embeddings.
- **Training procedure (siamese + in-batch negatives):**
  - Siamese network with **shared weights** for query/episode encoders.
  - Batch size **B**: for each positive (q, d) in batch, treat other docs as negatives → **B positives** and **B² − B negatives** per batch.
  - Compute **B×B cosine similarity matrix** once per batch; diagonal = positives.
  - Losses mentioned: MSE vs identity matrix; later improved with **in-batch hard negative mining** + **margin loss**.
- **Data pipeline:** positives from (1) successful search logs (Elasticsearch-derived), (2) query reformulations after initial failure, (3) synthetic queries generated via **BART** fine-tuned on **MS MARCO**, (4) curated semantic queries (eval only). Ensure eval episodes not in train.
- **Production deployment workflow:**
  - **Offline:** precompute episode vectors; index in **Vespa** with **ANN** (tens of millions of episodes) + first-phase rerank using features like popularity.
  - **Online:** compute query vector via **Vertex AI GPU inference**; retrieve **top 30** semantic episodes from Vespa; use **vector cache** to avoid recomputation.
  - GPU cost result: **T4 GPU ~6× cheaper than CPU** for inference (load tests).
- **System design:** Dense retrieval complements (doesn’t replace) sparse/term retrieval (Elasticsearch). Final-stage reranker blends sources; add **cosine similarity feature** to help rank semantic candidates.

## When to surface
Use when students ask how to deploy long-term memory / vector retrieval in production: offline embedding indexing, ANN serving, online query embedding, caching, and blending dense + sparse retrieval with reranking.