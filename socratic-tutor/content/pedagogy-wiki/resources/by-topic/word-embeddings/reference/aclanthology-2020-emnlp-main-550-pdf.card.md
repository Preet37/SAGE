# Card: Dense Passage Retrieval (DPR) objective + in-batch negatives
**Source:** https://aclanthology.org/2020.emnlp-main.550.pdf  
**Role:** paper | **Need:** FORMULA_SOURCE  
**Anchor:** Exact DPR bi-encoder scoring + softmax objective with in-batch negatives; batching/hard-negative details + key retrieval/QA numbers

## Key Content
- **Bi-encoder scoring (Eq. 1, Sec. 3.1):**  
  - Question encoder \(E_Q(\cdot)\), passage encoder \(E_P(\cdot)\) (two independent BERT-base uncased); use \([CLS]\) vector, \(d=768\).  
  - Similarity: \(\mathrm{sim}(q,p)=E_Q(q)^\top E_P(p)\) (dot product / MIPS-friendly).
- **Training objective (Eq. 2, Sec. 3.2):** for instance \(\langle q_i, p_i^+, p_{i,1}^-,\dots,p_{i,n}^-\rangle\)  
  \[
  \mathcal{L}=-\log \frac{e^{\mathrm{sim}(q_i,p_i^+)}}{e^{\mathrm{sim}(q_i,p_i^+)}+\sum_{j=1}^n e^{\mathrm{sim}(q_i,p_{i,j}^-)}}
  \]
- **In-batch negatives (Sec. 3.2):** batch size \(B\). Let \(Q,P\in\mathbb{R}^{B\times d}\); similarity matrix \(S=QP^\top\in\mathbb{R}^{B\times B}\). For question \(i\), passage \(j=i\) is positive; all \(j\neq i\) are negatives ⇒ \(B-1\) negatives per question; effectively trains on \(B^2\) pairs/batch.
- **Negative types (Sec. 3.2/5.2):** Random; **BM25 hard negatives** (high BM25 but no answer string); **Gold** (positives from other questions). **Best:** in-batch gold negatives + **1 BM25 hard negative per question** (adding 2 didn’t help).
- **Corpus/chunking (Sec. 4.1):** Wikipedia Dec 20, 2018; DrQA cleaning; split into **disjoint 100-word passages**; prepend title + \([SEP]\); **21,015,324 passages**.
- **Key retrieval results (Table 2):** Top-20 accuracy (% answer-containing)  
  - **NQ:** DPR 78.4 vs BM25 59.1  
  - **TriviaQA:** 79.4 vs 66.9  
  - **WQ:** 73.2 vs 55.0  
  - **TREC:** 79.8 vs 70.9
- **Key end-to-end QA EM (Table 4, Single):**  
  - **NQ:** DPR 41.5 vs BM25 32.6; ORQA 33.3  
  - **TriviaQA:** DPR 56.8 vs BM25 52.4
- **Efficiency (Sec. 5.4):** FAISS (CPU HNSW) retrieves top-100 at **995 Q/s**; BM25/Lucene **23.7 Q/s per CPU thread**. FAISS index build on 21M vectors: **8.5h**; embedding compute: **8.8h on 8 GPUs**. HNSW params: neighbors/node=512, construction ef=200, search ef=128.

## When to surface
Use when students ask for the **exact DPR loss/scoring**, how **in-batch negatives** work, or what **hard negatives/batch sizes** and **retrieval/QA gains** DPR achieved over BM25.