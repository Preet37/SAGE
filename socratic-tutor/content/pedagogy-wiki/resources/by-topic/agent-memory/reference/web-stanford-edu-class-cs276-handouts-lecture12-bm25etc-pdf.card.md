# Card: BM25 / BM25F (Okapi) core equations + rationale
**Source:** https://web.stanford.edu/class/cs276/handouts/lecture12-bm25etc.pdf  
**Role:** explainer | **Need:** FORMULA_SOURCE  
**Anchor:** Derivation-style presentation of BM25/BM25F with notation, saturation + length normalization, plus a concrete tf-idf vs BM25 comparison.

## Key Content
- **BIM (Binary Independence Model) log-odds RSV (Eq. 1):**  
  \[
  RSV_{BIM}=\sum_{i\in q} c_i,\quad 
  c_i=\log\frac{p_i(1-r_i)}{(1-p_i)r_i}
  \]
  where \(p_i=P(x_i=1\mid R=1)\), \(r_i=P(x_i=1\mid R=0)\), \(x_i\) indicates term presence. With constant \(p_i=0.5\) simplifies to **IDF weighting** \(\log(N/df_i)\).
- **BM25 term saturation (Eq. 2):** bounded tf contribution via  
  \[
  \frac{tf}{k_1+tf}
  \]
  (monotone in \(tf\), asymptotically saturating).
- **Document length normalization (Eq. 3):**  
  \[
  B=(1-b)+b\frac{dl}{avdl},\quad 0\le b\le 1
  \]
  \(dl\)=doc length, \(avdl\)=avg doc length.
- **Okapi BM25 scoring (Eq. 4):**  
  \[
  RSV_{BM25}=\sum_{i\in q}\log\frac{N}{df_i}\cdot
  \frac{(k_1+1)tf_i}{k_1\left((1-b)+b\frac{dl}{avdl}\right)+tf_i}
  \]
  Defaults: \(k_1\approx 1.2\text{–}2\), \(b\approx 0.75\). Interpretations: \(k_1=0\) binary; large \(k_1\) ≈ raw tf. \(b=0\) none; \(b=1\) full length norm.
- **BM25F (zones) (Eq. 5):** weighted tf/length across zones \(z\):  
  \[
  \tilde{tf}_i=\sum_{z=1}^Z v_z\frac{tf_{zi}}{B_z},\quad
  B_z=(1-b_z)+b_z\frac{len_z}{avlen_z}
  \]
  Then  
  \[
  RSV_{BM25F}=\sum_{i\in q}\log\frac{N}{df_i}\cdot\frac{(k_1+1)\tilde{tf}_i}{k_1+\tilde{tf}_i}
  \]
  Rationale: eliteness is shared across zones; zone-specific normalization (\(b_z\)) helps empirically.
- **Empirical comparison (machine learning query, \(k_1=2\)):**  
  doc1: learning 1024, machine 1 → **tf-idf 87**, **BM25 31**;  
  doc2: learning 16, machine 8 → **tf-idf 75**, **BM25 42.7** (BM25 favors balanced evidence; tf-idf over-rewards huge tf).

## When to surface
Use when students ask for BM25/BM25F formulas, parameter meanings/defaults, why BM25 saturates tf and normalizes length, or to contrast BM25 vs tf-idf with a numeric example.