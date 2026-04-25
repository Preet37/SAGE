# Card: Word2Vec Skip-gram—NEG, Hierarchical Softmax, Subsampling, Phrases
**Source:** https://proceedings.neurips.cc/paper_files/paper/2013/file/9aa42b31882ec039965f3c4923ce901b-Paper.pdf  
**Role:** paper | **Need:** FORMULA_SOURCE  
**Anchor:** Original negative sampling objective, hierarchical softmax setup, subsampling frequent words, plus phrase extension + key training details.

## Key Content
- **Skip-gram objective (Eq. 1):** maximize  
  \[
  \frac{1}{T}\sum_{t=1}^{T}\sum_{-c\le j\le c, j\ne 0}\log p(w_{t+j}\mid w_t)
  \]
  where \(c\)=context window size, \(T\)=#tokens.
- **Softmax (Eq. 2):**  
  \[
  p(w_O\mid w_I)=\frac{\exp({v'_{w_O}}^\top v_{w_I})}{\sum_{w=1}^{W}\exp({v'_w}^\top v_{w_I})}
  \]
  \(v_w\)=“input” vector, \(v'_w\)=“output” vector, \(W\)=vocab size.
- **Hierarchical softmax (Sec. 2.1, Eq. 3):** binary tree; probability is product along path nodes \(n(w,j)\):  
  \[
  p(w\mid w_I)=\prod_{j=1}^{L(w)-1}\sigma\Big(\big[\![n(w,j+1)=ch(n(w,j))]\!\big]\cdot {v'_{n(w,j)}}^\top v_{w_I}\Big)
  \]
  Uses **Huffman tree** so frequent words have short codes ⇒ faster training (~\(\log W\) nodes).
- **Negative sampling objective (Sec. 2.2, Eq. 4):** replace each \(\log p(w_O\mid w_I)\) with  
  \[
  \log\sigma({v'_{w_O}}^\top v_{w_I})+\sum_{i=1}^{k}\mathbb{E}_{w_i\sim P_n(w)}[\log\sigma(-{v'_{w_i}}^\top v_{w_I})]
  \]
  Typical \(k\): **5–20** (small data), **2–5** (large data). Noise \(P_n(w)\): unigram\(^{3/4}\) (i.e., \(U(w)^{3/4}/Z\)) beats unigram/uniform.
- **Subsampling frequent words (Sec. 2.3, Eq. 5):** discard token \(w_i\) with  
  \[
  P(w_i)=1-\sqrt{\frac{t}{f(w_i)}}
  \]
  \(f(w_i)\)=frequency; \(t\approx 10^{-5}\). Gives **2×–10× speedup** and improves rare-word vectors.
- **Empirical (Sec. 3, Table 1; 1B words, vocab 692K, min count 5, 300d):**  
  - No subsampling: **NEG-5 total 59% (38 min)**; **NEG-15 total 61% (97 min)**; **HS-Huffman total 47% (41 min)**.  
  - With \(10^{-5}\) subsampling: **NEG-5 total 60% (14 min)**; **NEG-15 total 61% (36 min)**; **HS-Huffman total 55% (21 min)**.
- **Phrase learning (Sec. 4, Eq. 6):** form bigram phrases via  
  \[
  score(w_i,w_j)=\frac{count(w_iw_j)-\delta}{count(w_i)\,count(w_j)}
  \]
  Keep bigrams above threshold; run **2–4 passes** with decreasing threshold to build longer phrases; then treat phrases as single tokens in training.
- **Phrase results (Table 3; 1B words, 300d, window 5):** accuracy no subsampling vs \(10^{-5}\): **NEG-15: 27%→42%**; **HS-Huffman: 19%→47%**. Best phrase model reported: **HS**, **1000d**, **full-sentence context**, **33B words** ⇒ **72%** phrase analogy accuracy.

## When to surface
Use for questions about the exact **NEG loss**, **hierarchical softmax probability**, **subsampling formula**, recommended **k/t defaults**, and concrete **accuracy/speed tradeoffs** (NEG vs HS; with/without subsampling), including the **phrase-tokenization scoring** method.