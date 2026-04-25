# Card: Faiss `IndexIVFPQR` (IVF + PQ + PQ refinement) API tunables
**Source:** https://faiss.ai/cpp_api/struct/structfaiss_1_1IndexIVFPQR.html  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Concrete IVF-PQ-R constructor fields and tunables (e.g., `nlist`, `M`, `nbits`, `by_residual`, `nprobe`, refinement PQ, reranking via `store_pairs`)

## Key Content
- **What it is:** `faiss::IndexIVFPQR` extends `IndexIVFPQ` with an **additional PQ refinement level** (“3rd level quantizer”).
- **Constructor (core hyperparameters):**  
  `IndexIVFPQR(Index* quantizer, size_t d, size_t nlist, size_t M, size_t nbits_per_idx, size_t M_refine, size_t nbits_per_idx_refine)`  
  - `d`: vector dimension  
  - `nlist`: number of inverted lists (coarse clusters)  
  - `M`, `nbits_per_idx`: PQ codebook structure for main PQ  
  - `M_refine`, `nbits_per_idx_refine`: PQ structure for refinement PQ
- **Key search-time parameters (public members):**
  - `size_t nprobe = 1`: number of IVF lists probed per query.
  - `size_t max_codes = 0`: cap on number of codes visited per query (0 = no cap).
  - `float k_factor`: multiplier between requested `k` and the `k` requested from the underlying IVFPQ stage.
- **Encoding / residual design:**
  - `bool by_residual = true`: codes encode vectors **relative to coarse centroids** (residual coding).
  - `size_t code_size`: bytes per vector code.
- **Refinement structures:**
  - `ProductQuantizer pq`: main PQ producing codes.
  - `ProductQuantizer refine_pq`: refinement PQ; `std::vector<uint8_t> refine_codes` stores corresponding codes.
- **Speed/accuracy knobs:**
  - `int use_precomputed_table`: precompute query tables (memory tradeoff; used only for `by_residual` + L2).
  - `size_t scan_table_threshold`: choose table computation vs on-the-fly.
  - Polysemous filtering/training: `do_polysemous_training`, `polysemous_ht`, `polysemous_training*`.
- **Reranking / reconstruction workflow:**
  - `search_preassigned(..., bool store_pairs, ...)`: if `store_pairs=true`, results store **(invlist id, offset)** in upper/lower 32 bits (instead of ids), enabling `reconstruct_from_offset(list_no, offset, ...)` and `search_and_reconstruct(...)` without maintaining `direct_map`.

## When to surface
Use when students ask how to configure Faiss IVF+PQ with refinement (IVFPQR): which constructor args map to `nlist/M/nbits`, what defaults like `nprobe=1` are, and how `store_pairs` enables reranking/reconstruction without a direct map.