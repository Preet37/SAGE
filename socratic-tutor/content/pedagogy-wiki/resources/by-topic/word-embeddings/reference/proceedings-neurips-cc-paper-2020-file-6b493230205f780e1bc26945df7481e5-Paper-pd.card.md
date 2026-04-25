# Card: RAG marginalization + DPR MIPS retrieval
**Source:** https://proceedings.neurips.cc/paper/2020/file/6b493230205f780e1bc26945df7481e5-Paper.pdf  
**Role:** paper | **Need:** FORMULA_SOURCE  
**Anchor:** RAG-Sequence / RAG-Token marginalization over retrieved docs; DPR retriever scoring as MIPS over dense embeddings

## Key Content
- **Setup (Sec. 2):** Input sequence \(x\), retrieved passages \(z\), output sequence \(y=(y_1,\dots,y_N)\). Retriever \(p_\eta(z\mid x)\); generator \(p_\theta(y_i\mid x,z,y_{1:i-1})\) (BART).
- **RAG-Sequence (Sec. 2.1, Eq. “RAG-Sequence”):** same document for whole output; top-\(K\) approximation  
  \[
  p_{\text{RAG-Seq}}(y\mid x)\approx \sum_{z\in \text{top-}K(p(\cdot\mid x))} p_\eta(z\mid x)\,p_\theta(y\mid x,z)
  =\sum_{z} p_\eta(z\mid x)\prod_{i=1}^N p_\theta(y_i\mid x,z,y_{1:i-1})
  \]
- **RAG-Token (Sec. 2.1, Eq. “RAG-Token”):** latent doc per token  
  \[
  p_{\text{RAG-Tok}}(y\mid x)\approx \prod_{i=1}^N \sum_{z\in \text{top-}K} p_\eta(z\mid x)\,p_\theta(y_i\mid x,z,y_{1:i-1})
  \]
- **Retriever = DPR bi-encoder (Sec. 2.2):**  
  \(d(z)=\text{BERT}_d(z)\), \(q(x)=\text{BERT}_q(x)\),  
  \[
  p_\eta(z\mid x)\propto \exp(d(z)^\top q(x))
  \]
  Top-\(K\) retrieval is **Maximum Inner Product Search (MIPS)**; approximated with FAISS (HNSW).
- **Generator (Sec. 2.3):** BART-large (~400M params); **concatenate** \(x\) and \(z\) as encoder input.
- **Training (Sec. 2.4):** minimize \(-\log p(y_j\mid x_j)\) end-to-end; **keep document encoder/index fixed**, fine-tune query encoder + generator.
- **Defaults (Sec. 3):** Wikipedia Dec 2018; split articles into **disjoint 100-word chunks** → **21M** passages; train with \(k\in\{5,10\}\).
- **Key results (Table 1):** Open-domain QA EM: NQ **44.5** (RAG-Seq) vs DPR 41.5; WQ **45.5** (RAG-Tok) vs DPR 41.1; CT **52.2** (RAG-Seq) vs DPR 50.6.  
  (Table 2) FEVER label acc: **72.5/89.5** (RAG-Tok, 3-way/2-way).

## When to surface
Use when students ask how RAG combines multiple retrieved documents probabilistically (sequence- vs token-level marginalization) or how dense retrieval scoring/top‑K MIPS retrieval is defined and trained end-to-end.