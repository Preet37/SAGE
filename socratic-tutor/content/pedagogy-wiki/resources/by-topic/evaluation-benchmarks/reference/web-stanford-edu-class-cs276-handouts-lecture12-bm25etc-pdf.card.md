# Card: Okapi BM25 (Probabilistic Relevance Framework)
**Source:** https://web.stanford.edu/class/cs276/handouts/lecture12-bm25etc.pdf  
**Role:** reference_doc | **Need:** FORMULA_SOURCE  
**Anchor:** BM25 scoring formula + parameter meanings (k1, b), IDF term, length normalization

## Key Content
- **BM25 ranking score (Eq. BM25):**  
  \[
  RSV_{BM25}(d,q)=\sum_{i\in q} \log\frac{N}{df_i}\cdot \frac{(k_1+1)\,tf_i}{k_1\left((1-b)+b\frac{dl}{avdl}\right)+tf_i}
  \]
  - \(N\): number of documents in collection  
  - \(df_i\): document frequency of term \(i\)  
  - \(tf_i\): term frequency of term \(i\) in document \(d\)  
  - \(dl\): document length (often \(dl=\sum_{i\in V} tf_i\))  
  - \(avdl\): average document length in collection  
  - \(k_1\): term-frequency saturation control  
  - \(b\in[0,1]\): length normalization strength
- **Length normalization component (Eq. B):**  
  \[
  B=(1-b)+b\frac{dl}{avdl}
  \]
  and normalized term frequency \(t'_f=tf/B\).
- **Parameter interpretations + defaults:**  
  - \(k_1=0\) → binary model; large \(k_1\) → approaches raw \(tf\).  
  - \(b=0\) → no length norm; \(b=1\) → full relative-frequency scaling.  
  - Typical settings: \(k_1\approx 1.2\text{–}2\), \(b\approx 0.75\).
- **Design rationale:** BM25 approximates a probabilistic “2-Poisson/eliteness” view with a **saturating tf curve** (bounded contribution vs unbounded tf-idf), plus **partial** length normalization to balance verbosity vs scope.
- **Empirical comparison (machine learning query example, \(k_1=2\)):**  
  - doc1: learning=1024, machine=1 → BM25: \(7\cdot3 + 10\cdot1 = 31\)  
  - doc2: learning=16, machine=8 → BM25: \(7\cdot2.67 + 10\cdot2.4 = 42.7\)  
  (tf-idf ranks doc1 higher: 87 vs 75)

## When to surface
Use when students ask how BM25 is computed, what \(k_1\) and \(b\) do, why BM25 beats tf-idf on extreme term counts, or how length normalization and tf saturation are implemented in retrieval/reranking pipelines.