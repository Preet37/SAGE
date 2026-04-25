# Card: DPR dual-encoder retrieval (dot product + in-batch negatives)
**Source:** https://aclanthology.org/2020.emnlp-main.550.pdf  
**Role:** paper | **Need:** FORMULA_SOURCE  
**Anchor:** Dual-encoder similarity scoring (dot product), in-batch negatives objective, retrieval pipeline (question encoder + passage encoder + ANN/FAISS index)

## Key Content
- **Retrieval setup (Section 3.1):** Encode passages with \(E_P(\cdot)\in\mathbb{R}^d\) and questions with \(E_Q(\cdot)\in\mathbb{R}^d\); precompute all passage vectors and build ANN index (FAISS). At runtime embed question \(v_q=E_Q(q)\) and retrieve top-\(k\) passages by similarity.
- **Similarity (Eq. 1):**  
  \[
  \mathrm{sim}(q,p)=E_Q(q)^\top E_P(p)
  \]
  (dot product / maximum inner product search). Chosen because decomposable ⇒ passage embeddings can be precomputed; ablations show comparable to L2, better than cosine.
- **Training objective (Eq. 2):** For each question \(q_i\), positive passage \(p_i^+\), negatives \(\{p_{i,j}^-\}_{j=1}^n\):  
  \[
  \mathcal{L}=-\log \frac{e^{\mathrm{sim}(q_i,p_i^+)}}{e^{\mathrm{sim}(q_i,p_i^+)}+\sum_{j=1}^n e^{\mathrm{sim}(q_i,p_{i,j}^-)}}
  \]
- **In-batch negatives (Section 3.2):** Batch size \(B\). Let \(Q,P\in\mathbb{R}^{B\times d}\); \(S=QP^\top\in\mathbb{R}^{B\times B}\). Pair \((q_i,p_i)\) is positive (diagonal), all \((q_i,p_j), j\neq i\) are negatives ⇒ \(B-1\) negatives per question; effectively trains on \(B^2\) pairs/batch. Best: in-batch “gold” negatives + **one** extra BM25 hard negative per question.
- **Encoders/defaults:** Two independent BERT-base (uncased); use \([CLS]\) vector; \(d=768\). Passage units: fixed 100-word blocks; Wikipedia Dec 20, 2018 ⇒ **21,015,324** passages.
- **Key retrieval results (Table 2, Top-20):** DPR vs BM25: NQ **78.4 vs 59.1**, TriviaQA **79.4 vs 66.9**, WQ **73.2 vs 55.0**, TREC **79.8 vs 70.9** (SQuAD is exception: DPR 63.2 vs BM25 68.8). BM25+DPR can improve (e.g., TREC 85.2 Top-20).
- **Efficiency (Section 5.4):** FAISS index retrieval ~**995 questions/sec** (top-100). Index build: embed 21M passages ~**8.8h on 8 GPUs**; build FAISS index ~**8.5h**; Lucene inverted index ~**30 min**.

## When to surface
Use when students ask how long-term memory retrieval can be implemented as vector search: dual-encoder embeddings, dot-product scoring, in-batch negative training, and ANN indexing assumptions/throughput tradeoffs.