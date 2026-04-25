# Card: BM25 (Okapi) scoring + parameter meanings
**Source:** https://web.stanford.edu/class/cs276/handouts/lecture12-bm25etc.pdf  
**Role:** explainer | **Need:** [FORMULA_SOURCE] BM25 exact formulation and parameter meanings  
**Anchor:** BM25 scoring equation (k1, b, IDF variants), term saturation + length normalization intuition

## Key Content
- **BM25 score (Eq. 1):**  
  \[
  RSV_{BM25}(d,q)=\sum_{i\in q} \log\frac{N}{df_i}\cdot \frac{(k_1+1)\,tf_i}{k_1\left((1-b)+b\frac{dl}{avdl}\right)+tf_i}
  \]
  - \(N\): #documents; \(df_i\): document frequency of term \(i\)  
  - \(tf_i\): term frequency of \(i\) in document \(d\)  
  - \(dl\): document length; \(avdl\): average document length in collection  
  - \(k_1\): term-frequency scaling (saturation) parameter  
  - \(b\in[0,1]\): length normalization strength
- **Length normalization component (Eq. 2):**  
  \[
  B=(1-b)+b\frac{dl}{avdl},\quad \tilde{tf}_i=\frac{tf_i}{B}
  \]
  (BM25 can be written using \(\tilde{tf}_i\) equivalently.)
- **Term-frequency saturation curve (motivation):** \(\frac{tf}{k_1+tf}\) is monotone in \(tf\) but approaches a maximum (bounded term contribution); low \(k_1\) saturates quickly, high \(k_1\) keeps rewarding increases.
- **Parameter defaults (rule-of-thumb):** \(k_1\approx 1.2\text{–}2\), \(b\approx 0.75\). Extremes: \(k_1=0\) → binary; large \(k_1\) → closer to raw \(tf\). \(b=0\) no length norm; \(b=1\) full relative-frequency scaling.
- **Empirical comparison example (machine learning query, \(k_1=2\)):**  
  doc1 (learning 1024, machine 1): tf-idf 87 vs BM25 31; doc2 (learning 16, machine 8): tf-idf 75 vs BM25 42.7 (BM25 prefers doc2 due to saturation).

## When to surface
Use when students ask for the exact BM25 formula, what \(k_1\)/\(b\) do, why BM25 saturates TF, or how length normalization changes rankings vs tf-idf.