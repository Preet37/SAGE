# Card: Milvus IVF_FLAT (and IVF knobs) quick reference
**Source:** https://milvus.io/docs/ivf.md  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Exact IVF parameters (`nlist`, `nprobe`), build/search tradeoffs, supported metrics

## Key Content
- **IVF concept (procedure):** Partition vectors into `nlist` clusters (centroids). **Search**: (1) compute distance from query to **all centroids**, (2) pick `nprobe` nearest clusters, (3) scan vectors in those clusters to produce `topK`. IVF_FLAT stores **raw vectors** in lists (no compression).
- **Build params (IVF_FLAT):**  
  - `index_type: "IVF_FLAT"`  
  - `metric_type`: `"L2"` or `"IP"`  
  - `nlist`: number of clusters, **int 1–65536**.
- **Search params (IVF_FLAT):**  
  - `nprobe`: clusters probed, **int 1–nlist (CPU)**; **1–min(2048, nlist) (GPU)**.  
  - Tradeoff: higher `nprobe` ⇒ higher recall, slower search (more candidates scanned).
- **Binary IVF variant:** `BIN_IVF_FLAT` supports `metric_type` ∈ {`jaccard`, `hamming`, `tanimoto`}; same `nlist` (1–65536) and `nprobe` bounds as above.
- **Index anatomy (design rationale):** data structure (e.g., IVF) + optional **quantization** (SQ8/PQ) + optional **refiner**. Query retrieves `topK × expansion_rate` candidates then refines distances on that subset.
- **Empirical guidance (selection):**
  - Graph indexes usually higher **QPS** than IVF; **IVF fits large `topK`** (e.g., **> 2,000**).
  - If **filter ratio** < **85%** ⇒ graph-based better; **85–95%** ⇒ IVF; **>98%** ⇒ **FLAT**.
  - Scenario table: **Large k (≥1% of dataset)** ⇒ IVF; **High filter ratio (>95%)** ⇒ FLAT.
- **Memory example (1M vectors, dim=128, nlist=2000):** totals: **IVF-PQ (no refine) 11.0 MB**; **IVF-PQ + 10% raw refine 62.2 MB**; **IVF-SQ8 131.0 MB**; **IVF-FLAT 515.0 MB**.

## When to surface
Use when students ask how to tune IVF in Milvus (exact `nlist`/`nprobe` ranges, CPU vs GPU limits), choose IVF vs HNSW/FLAT based on `topK` or filter ratio, or estimate memory/accuracy tradeoffs for IVF_FLAT vs IVF_PQ/SQ8.