# Card: Maximal Marginal Relevance (MMR) selection criterion
**Source:** https://www.cs.cmu.edu/~jgc/publication/MMR_DiversityBased_Reranking_SIGIR_1998.pdf  
**Role:** paper | **Need:** FORMULA_SOURCE  
**Anchor:** Original MMR equation balancing query relevance vs novelty/diversity via λ

## Key Content
- **MMR selection criterion (Eq. 1 / Section 2):** incrementally select the next item \(D_i\) from retrieved set \(R\) given already-selected set \(S\):  
  \[
  \mathrm{MMR} \triangleq \arg\max_{D_i \in R \setminus S}\Big[\lambda\, \mathrm{Sim}_1(D_i,Q)\;-\;(1-\lambda)\max_{D_j \in S}\mathrm{Sim}_2(D_i,D_j)\Big]
  \]
  **Variables:**  
  - \(C\): document collection/stream; \(Q\): query/user profile  
  - \(R = IR(C,Q,\theta)\): retrieved/ranked list from an IR system with threshold \(\theta\) (match degree or top-N cutoff)  
  - \(S\subset R\): already selected docs/passages; \(R\setminus S\): unselected candidates  
  - \(\mathrm{Sim}_1\): similarity for relevance (doc/passages ↔ query)  
  - \(\mathrm{Sim}_2\): similarity for redundancy (candidate ↔ selected); may equal \(\mathrm{Sim}_1\) or differ  
  - \(\lambda\in[0,1]\): tradeoff; \(\lambda=1\) ⇒ pure relevance ranking; \(\lambda=0\) ⇒ maximal diversity among \(R\)
- **Procedure (reranking / summarization):** segment document into passages (sentences), compute cosine similarity, apply MMR to rerank passages for a query; output top passages in original document order (Section 4).
- **Suggested λ strategy (Section 2):** start broad with \(\lambda\approx 0.3\), then refocus with reformulated query and \(\lambda\approx 0.7\).
- **Empirical results:**  
  - User study (Section 3): 80% (4/5) chose MMR method for a search task.  
  - SUMMAC’98 (Section 4): MMR summarizer achieved **F-score 0.73** for query-relevant summaries; **70% accuracy** on “informative summaries.”  
  - Sentence precision (Table 1): compression 10%: \(\lambda=1\) **0.78/0.83**, \(\lambda=.7\) **0.76/0.83**, \(\lambda=.3\) **0.74/0.79**; Lead sentences **0.74/0.83**. Compression 25%: \(\lambda=1\) **0.74/0.76**, \(\lambda=.7\) **0.73/0.74**, \(\lambda=.3\) **0.74/0.76**; Lead sentences **0.60/0.65**.

## When to surface
Use when students ask how to **reduce redundancy in retrieval/RAG context selection** or need the **canonical MMR formula** and how \(\lambda\) controls relevance vs diversity in reranking/summarization.