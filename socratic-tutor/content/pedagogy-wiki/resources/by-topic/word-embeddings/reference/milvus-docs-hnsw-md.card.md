# Card: Milvus HNSW index params (M, efConstruction, ef) + metrics
**Source:** https://milvus.io/docs/hnsw.md  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Milvus HNSW index/search parameter specs and supported distance metrics for float vectors

## Key Content
- **What HNSW is (design rationale):** Graph-based ANN index for **high-dimensional floating vectors**; delivers **excellent accuracy + low latency** but has **high memory overhead** due to hierarchical graph structure.
- **Algorithm workflow (overview):**
  - Multi-layer graph: **bottom layer = all points**, upper layers = **subsampled** points.
  - **Search procedure:** start at **fixed entry point** (top layer) → **greedy** move to closest neighbor until local minimum → **descend** a layer via established connection → repeat → **bottom-layer refinement** returns nearest neighbors.
- **Supported similarity metrics (index build):** `COSINE`, `L2`, `IP`.
- **Index build API (PyMilvus):**
  - Use `MilvusClient.prepare_index_params()` then `index_params.add_index(field_name, index_type="HNSW", index_name, metric_type, params={...})`.
  - Build params:
    - **M** = max connections/edges per node (includes outgoing + incoming).
    - **efConstruction** = candidate neighbors considered during construction.
- **Search API:**
  - `search_params = {"params": {"ef": <int>}}`
  - `MilvusClient.search(collection_name, anns_field, data=[query_vector], limit=K, search_params=search_params)`
  - **ef** = number of neighbors/nodes evaluated during search (bottom layer).
- **Parameter specs (with defaults/ranges + tuning):**
  - **M:** int **[2, 2048]**, default **30** (up to 30 outgoing + 30 incoming). Recommended **[5, 100]**. Higher M → higher recall/accuracy, more memory, slower build/search.
  - **efConstruction:** int **[1, int_max]**, default **360**. Recommended **[50, 500]**. Higher → better graph/accuracy, slower build, more memory during construction.
  - **ef (search):** int **[1, int_max]**, default **limit (TopK)**. Recommended **[K, 10K]**. Higher → higher recall, slower search.

## When to surface
Use when students ask how to configure Milvus **HNSW** for RAG retrieval (which params to tune, defaults/ranges, and which distance metrics are supported) or how to call the **build/search APIs** with `M`, `efConstruction`, and `ef`.