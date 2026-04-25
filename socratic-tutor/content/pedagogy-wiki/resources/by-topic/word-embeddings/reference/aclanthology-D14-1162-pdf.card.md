# Card: GloVe benchmarks + core objective
**Source:** https://aclanthology.org/D14-1162.pdf  
**Role:** benchmark | **Need:** EMPIRICAL_DATA  
**Anchor:** Analogy accuracy + word similarity (WS-353 etc.) tables and the hyperparameters used.

## Key Content
- **Core co-occurrence setup (Section 3):**  
  - Co-occurrence counts: \(X_{ij}\) = # times context word \(j\) occurs in context of target \(i\).  
  - \(X_i=\sum_k X_{ik}\); \(P_{ij}=P(j|i)=X_{ij}/X_i\).
- **Log-bilinear relation (Eq. 7):**  
  \[
  w_i^\top \tilde w_j + b_i + \tilde b_j = \log(X_{ij})
  \]
  with separate **word vectors** \(w\) and **context vectors** \(\tilde w\), plus biases.
- **Weighted least squares objective (Eq. 8):**  
  \[
  J=\sum_{i,j=1}^V f(X_{ij})\left(w_i^\top \tilde w_j+b_i+\tilde b_j-\log X_{ij}\right)^2
  \]
- **Weighting function (Eq. 9) + defaults:**  
  \[
  f(x)=\begin{cases}(x/x_{\max})^\alpha & x<x_{\max}\\ 1 & \text{otherwise}\end{cases}
  \]
  Defaults used: \(x_{\max}=100\), \(\alpha=3/4\).
- **Training pipeline + defaults (Section 4.2):**  
  - Tokenize+lowercase; vocab = top **400k** words (Common Crawl uses ~2M).  
  - Build \(X\) with **symmetric window 10 left + 10 right**; distance weighting \(1/d\).  
  - Optimize with **AdaGrad**, initial LR **0.05**, sample **nonzero** \(X_{ij}\).  
  - Iterations: **50** if dim < 300; **100** otherwise. Use final vectors **\(W+\tilde W\)**.
- **Analogy benchmark (Table 2, accuracy %):**  
  - **GloVe 300d, 42B tokens:** Sem 81.9 / Syn 69.3 / **Total 75.0** (best overall).  
  - **GloVe 300d, 6B:** Total **71.7** vs **SG† 69.1**, **CBOW† 65.7**.  
  - **GloVe 300d, 1.6B:** Total **70.3**.
- **Word similarity (Table 3, Spearman; 300d):**  
  - **GloVe 6B:** WS353 **65.8** (vs SG† 62.8; CBOW† 57.2).  
  - **GloVe 42B:** WS353 **75.9**, MC **83.6**, RG **82.9**, RW **47.8**.

## When to surface
Use for questions asking “What objective does GloVe optimize?”, “What hyperparameters did they use (window, dim, \(x_{\max}\), \(\alpha\), iterations)?”, or “What are the reported analogy/WS-353 benchmark numbers vs word2vec/SVD?”