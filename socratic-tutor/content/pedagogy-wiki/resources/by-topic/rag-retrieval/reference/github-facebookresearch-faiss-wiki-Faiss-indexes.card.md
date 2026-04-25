# Card: Faiss index types ↔ classes, parameters, and IVF/HNSW rules of thumb
**Source:** https://github.com/facebookresearch/faiss/wiki/Faiss-indexes  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Index class ↔ algorithm mapping + key parameters (M, nlist/nprobe, cosine via IndexFlatIP)

## Key Content
- **Exact (exhaustive) search**
  - `IndexFlatL2` (“Flat”): exact L2; params: `d`; memory **4*d bytes/vector**.
  - `IndexFlatIP` (“Flat”): exact inner product; params: `d`; memory **4*d**; **cosine similarity via pre-normalizing vectors** (then IP ≡ cosine).
- **HNSW graph (approximate)**
  - `IndexHNSWFlat` (“HNSW,Flat”): params `d, M`; memory **4*d + x*M*2*4** bytes/vector (graph overhead term shown in table).
  - Key HNSW params: **`M`** (#neighbors; ↑M ⇒ ↑accuracy, ↑memory), **`efConstruction`** (add-time exploration depth), **`efSearch`** (query-time exploration depth).
  - Restriction: HNSW **does not support removal** (would break graph).
- **IVF (cell-probe / inverted lists; approximate)**
  - `IndexIVFFlat` (“IVFx,Flat”): params `quantizer, d, nlist(s), metric`; memory **4*d + 8** bytes/vector (**+8 bytes for stored vector id**). Uses another index (“coarse quantizer”) to assign vectors to lists; typically a Flat quantizer.
  - Query-time parameter: **`nprobe`** = number of inverted lists visited.
  - **Eq. 1 (scan fraction):** approx scanned fraction ≈ **nprobe / nlist** (underestimates due to uneven list lengths).
  - **Rule of thumb (centroids):** for `n` points, choose **nlist = C * sqrt(n)** with **C ≈ 10** (balances assignment cost vs list scanning).
- **PQ / SQ encodings (compression)**
  - `IndexScalarQuantizer` (“SQ8”): memory **d bytes/vector** (also 6/4-bit variants).
  - `IndexPQ` (“PQx” / “PQ”M”x”nbits”): memory **ceil(M*nbits/8)**; constraints: **d multiple of M**; `nbits` **8/12/16**.
  - `IndexIVFPQ` (“IVFx,PQy×nbits”): memory **ceil(M*nbits/8)+8**; typical usage: `IndexFlatL2(d)` as coarse quantizer; set `index.nprobe` at query time.

## When to surface
Use when students ask which Faiss index to choose (Flat vs IVF vs HNSW vs PQ/SQ), how to set **M / nlist / nprobe / efSearch**, memory-per-vector tradeoffs, or how to do **cosine similarity** in Faiss.