# Card: SGNS objective + negative sampling derivation (Goldberg & Levy 2014)
**Source:** https://arxiv.org/pdf/1402.3722.pdf  
**Role:** paper | **Need:** FORMULA_SOURCE  
**Anchor:** Explicit derivation of Skip-gram with Negative Sampling (SGNS) objective; assumptions about word/context vectors; negative-sampling distribution details.

## Key Content
- **Skip-gram MLE objective (Eq. 1–2):** maximize corpus likelihood of contexts given words  
  \[
  \arg\max_\theta \prod_{w\in Text}\prod_{c\in C(w)} p(c\mid w;\theta)
  \equiv \arg\max_\theta \prod_{(w,c)\in D} p(c\mid w;\theta)
  \]
  where \(D\) is extracted word–context pairs; \(C(w)\) contexts of \(w\).
- **Softmax parameterization (Eq. 3):**  
  \[
  p(c\mid w;\theta)=\frac{e^{v_c\cdot v_w}}{\sum_{c'\in C} e^{v_{c'}\cdot v_w}}
  \]
  with embeddings \(v_w, v_c\in\mathbb{R}^d\); \(C\)=all contexts.
- **Log objective (Eq. 4):**  
  \[
  \sum_{(w,c)\in D}\left(v_c\cdot v_w-\log\sum_{c'} e^{v_{c'}\cdot v_w}\right)
  \]
  Computational bottleneck: sum over all contexts \(c'\).
- **Negative sampling as binary classification (Section 2):** define  
  \[
  p(D{=}1\mid w,c;\theta)=\sigma(v_c\cdot v_w)=\frac{1}{1+e^{-v_c\cdot v_w}}
  \]
  Add negative pairs \(D'\) to avoid trivial solution (all dot-products large; \(K\approx 40\) yields near-1 probability).
- **SGNS objective (Section 2):**  
  \[
  \arg\max_\theta \sum_{(w,c)\in D}\log\sigma(v_c\cdot v_w)+\sum_{(w,c)\in D'}\log\sigma(-v_c\cdot v_w)
  \]
- **How \(D'\) is constructed (k-negative sampling):** for each positive \((w,c)\in D\), sample \(k\) negatives \((w,c_j)\) with \(c_j\) drawn from unigram\(^ {3/4}\). Equivalent sampling:  
  \[
  (w,c)\sim \frac{p_{\text{words}}(w)\,p_{\text{contexts}}(c)^{3/4}}{Z}
  \]
  In word2vec, contexts are words so \(p_{\text{context}}(x)=p_{\text{words}}(x)=\frac{\text{count}(x)}{|Text|}\).
- **Design rationale:** use **separate vocabularies/vectors** for words vs contexts (footnote): if shared, model would need low \(p(dog\mid dog)\) though \(v\cdot v\) can’t be low.

## When to surface
Use when students ask: “What exactly is the SGNS/negative-sampling loss?”, “How are negatives sampled (3/4 power, k negatives)?”, or “Why separate word and context embeddings / why softmax is expensive?”