# Card: DPR (Dense Passage Retrieval) objective + bi-encoder training
**Source:** https://aclanthology.org/2020.emnlp-main.550.pdf  
**Role:** paper | **Need:** [FORMULA_SOURCE]  
**Anchor:** Dual-encoder DPR with inner-product scoring; InfoNCE-style NLL with in-batch negatives + hard negatives; key hyperparams + retrieval gains vs BM25.

## Key Content
- **Retrieval scoring (Eq. 1, Sec. 3.1):**  
  \[
  \text{sim}(q,p)=E_Q(q)^\top E_P(p)
  \]  
  where \(E_Q(\cdot)\) encodes questions, \(E_P(\cdot)\) encodes passages into \(d\)-dim vectors (BERT-base [CLS], \(d=768\)). Retrieve top-\(k\) passages by maximum inner product search (MIPS); passages pre-encoded + indexed with **FAISS**.
- **Training objective (Eq. 2, Sec. 3.2):** for instance \(\langle q_i,p_i^+,p_{i,1}^-,...,p_{i,n}^-\rangle\)  
  \[
  \mathcal{L}=-\log \frac{e^{\text{sim}(q_i,p_i^+)}}{e^{\text{sim}(q_i,p_i^+)}+\sum_{j=1}^n e^{\text{sim}(q_i,p_{i,j}^-)}}
  \]  
  (softmax NLL / InfoNCE over positives vs negatives).
- **In-batch negatives (Sec. 3.2):** batch size \(B\). Let \(Q,P\in\mathbb{R}^{B\times d}\); similarity matrix \(S=QP^\top\in\mathbb{R}^{B\times B}\). Positive pairs are diagonal \((i=j)\); each question gets \(B-1\) negatives “for free” (effective \(B^2\) pairs/batch).
- **Negative choices (Sec. 3.2, Table 3):** Random, BM25-hard, Gold (positives from other questions). Best: **in-batch gold negatives + 1 BM25 hard negative per question** (adding 2 didn’t help).
- **Defaults / hyperparams (Sec. 5):** in-batch training, **batch=128**, **+1 BM25 negative**, Adam, lr **1e-5**, dropout **0.1**, linear warmup schedule; up to **40 epochs** (large datasets) / **100** (small).
- **Empirical retrieval gains (Table 2):** Top-20 accuracy: **NQ DPR 78.4 vs BM25 59.1**; Top-5 on NQ: **DPR 65.2 vs BM25 42.9** (reported in intro).  
  Sample efficiency (Fig. 1): **DPR with 1k training examples already beats BM25** on NQ dev.
- **Efficiency (Sec. 5.4):** FAISS DPR retrieval ~**995 Q/s** (top-100) vs Lucene BM25 **23.7 Q/s per CPU thread**. Indexing: encode 21M passages ~**8.8h on 8 GPUs**; build FAISS index ~**8.5h**; Lucene index ~**30 min**.

## When to surface
Use when students ask how DPR/RAG retrievers are trained (InfoNCE/in-batch negatives), why dot-product bi-encoders enable fast retrieval, or want concrete DPR-vs-BM25 accuracy/throughput numbers and hyperparameters.