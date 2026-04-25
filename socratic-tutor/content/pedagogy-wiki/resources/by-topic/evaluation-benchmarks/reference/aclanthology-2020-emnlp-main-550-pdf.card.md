# Card: DPR dual-encoder objective + in-batch negatives
**Source:** https://aclanthology.org/2020.emnlp-main.550.pdf  
**Role:** paper | **Need:** FORMULA_SOURCE  
**Anchor:** Dual-encoder DPR training objective (in-batch negatives / contrastive log-likelihood), dot-product scoring, end-to-end retriever→reader procedure + key hyperparams/results

## Key Content
- **Retrieval scoring (Eq. 1, Sec. 3.1):**  
  \[
  \text{sim}(q,p)=E_Q(q)^\top E_P(p)
  \]
  where \(E_Q, E_P\) are question/passage encoders; vectors are \(d\)-dim (BERT-base [CLS], \(d=768\)). Retrieve top-\(k\) passages by maximum inner product search (FAISS).
- **Training loss (Eq. 2, Sec. 3.2):** for instance \(\langle q_i,p_i^+,p_{i,1}^-,...,p_{i,n}^-\rangle\),
  \[
  L=-\log \frac{e^{\text{sim}(q_i,p_i^+)}}{e^{\text{sim}(q_i,p_i^+)}+\sum_{j=1}^n e^{\text{sim}(q_i,p_{i,j}^-)}}
  \]
- **In-batch negatives (Sec. 3.2):** batch size \(B\). Build \(Q,P\in\mathbb{R}^{B\times d}\); \(S=QP^\top\in\mathbb{R}^{B\times B}\). Positive pairs are diagonal \(i=j\); negatives are other batch passages (\(B-1\) per question), yielding \(B^2\) pairs/batch.
- **Negatives used (Sec. 3.2, 5.2):** best model uses **gold in-batch negatives + 1 BM25 hard negative per question** (BM25 passage that doesn’t contain answer). Adding 1 BM25 negative helps; adding 2 doesn’t.
- **Key retrieval results (Table 2):** Top-20 accuracy (answer in retrieved passages):  
  - NQ: **DPR 78.4 vs BM25 59.1**  
  - TriviaQA: **79.4 vs 66.9**  
  - WQ: **73.2 vs 55.0**  
  - TREC: **79.8 vs 70.9**
- **Training hyperparams (Sec. 5):** batch size **128**; epochs **40** (large datasets) / **100** (small); LR **1e-5** Adam + linear warmup; dropout **0.1**.
- **Indexing/runtime (Sec. 5.4):** Wikipedia split into **21,015,324** passages of **100 words** (+ title + [SEP]). FAISS retrieval ~**995 Q/s** (top-100). Dense embedding compute ~**8.8h on 8 GPUs**; FAISS index build **8.5h**; Lucene index build **~30 min**.

## When to surface
Use when students ask how DPR-style dense retrieval is trained (contrastive softmax / in-batch negatives), how scoring works (dot product/MIPS), or what concrete hyperparameters and retrieval gains vs BM25 look like in practice.