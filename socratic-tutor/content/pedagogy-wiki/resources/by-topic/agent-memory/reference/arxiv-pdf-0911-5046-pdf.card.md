# Card: BM25 / BM25F scoring (Lucene implementation notes)
**Source:** https://arxiv.org/pdf/0911.5046.pdf  
**Role:** paper | **Need:** FORMULA_SOURCE  
**Anchor:** Concrete BM25 scoring + parameter meanings (k1, b, tf, length norm) and BM25F fielded variant (Eq. 1–2)

## Key Content
- **BM25 term contribution (as implemented):** for query *q* and document *d*, sum over terms *t ∈ q* that occur in *d*:  
  \[
  R(q,d)=\sum_{t\in q} idf(t)\cdot \frac{tf_{t,d}}{k_1\left((1-b)+b\frac{l_d}{avl_d}\right)+tf_{t,d}}
  \]
  where \(tf_{t,d}\) (“occurs\(_{d,t}\)”) = term frequency of *t* in *d*; \(l_d\)=doc length; \(avl_d\)=average doc length in collection; \(k_1\) free parameter (usually **2**); \(b\in[0,1]\) (usually **0.75**).  
  - \(b=0\): no length normalization; \(b=1\): full length normalization.
- **IDF (classical):**  
  \[
  idf(t)=\log\frac{N-df(t)+0.5}{df(t)+0.5}
  \]
  where \(N\)=#documents; \(df(t)\)=#documents containing term *t*.  
  - Note: a common variant multiplies BM25 weight by \((k_1+1)\) (mentioned as Wikipedia variant).
- **BM25F (fielded) accumulated term weight:**  
  \[
  weight(t,d)=\sum_{c\in d}\frac{tf_{t,d,c}\cdot boost_c}{(1-b_c)+b_c\frac{l_c}{avl_c}}
  \]
  with field length \(l_c\), avg field length \(avl_c\), field parameter \(b_c\), and field boost \(boost_c\).
- **BM25F final score (Eq. 1):**  
  \[
  R(q,d)=\sum_{t\in q} idf(t)\cdot \frac{weight(t,d)}{k_1+weight(t,d)}
  \]
  with \(idf(t)\) as above (Eq. 2).
- **Implementation workflow (Lucene):** average lengths not in API → compute at index time via custom Similarity counting tokens per field; after indexing, divide total field length by numDocs and load into parameters at search time.
- **Defaults:** BM25Parameters: \(k_1=2\), \(b=0.75\). BM25FParameters: same \(k_1\); per-field \(b_c\) defaults 0.75; per-field boosts default 1; arrays must align with fields order.
- **Design/engineering note:** Lucene docFreq is field-level; for BM25F they heuristically compute IDF using the field with the **longest average length** unless indexing an “all terms” field.

## When to surface
Use when students ask for the exact BM25/BM25F scoring equations, what \(k_1\)/\(b\) do, how length normalization works, or how to implement sparse retrieval scoring (including fielded documents) for agent memory / hybrid retrieval.