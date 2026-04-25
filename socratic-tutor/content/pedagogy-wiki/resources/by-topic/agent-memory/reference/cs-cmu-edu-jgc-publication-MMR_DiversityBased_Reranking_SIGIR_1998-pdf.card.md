# Card: Maximal Marginal Relevance (MMR) objective
**Source:** https://www.cs.cmu.edu/~jgc/publication/MMR_DiversityBased_Reranking_SIGIR_1998.pdf  
**Role:** paper | **Need:** FORMULA_SOURCE  
**Anchor:** Primary-source MMR objective with explicit tradeoff parameter λ balancing query relevance vs novelty/diversity (anti-redundancy)

## Key Content
- **MMR objective (Eq. 1 / Section 2):** select next item incrementally to balance relevance to query and novelty vs already-selected items:  
  \[
  \mathrm{MMR} \triangleq \arg\max_{D_i \in R \setminus S}\Big[\lambda\,\mathrm{Sim}_1(D_i,Q)\;-\;(1-\lambda)\max_{D_j\in S}\mathrm{Sim}_2(D_i,D_j)\Big]
  \]
  **Definitions:**  
  - \(C\): document collection/stream; \(Q\): query (or user profile)  
  - \(R = IR(C,Q,\theta)\): retrieved/ranked set from an IR system with threshold \(\theta\)  
  - \(S\): subset already selected; \(R\setminus S\): unselected candidates  
  - \(\mathrm{Sim}_1\): similarity for query relevance; \(\mathrm{Sim}_2\): similarity for redundancy (can equal \(\mathrm{Sim}_1\) or differ)  
  - \(\lambda \in [0,1]\): tradeoff parameter
- **Parameter behavior (Section 2):**
  - \(\lambda=1\) ⇒ standard relevance ranking.
  - \(\lambda=0\) ⇒ maximal diversity ranking within \(R\).
  - Suggested interactive strategy: start **\(\lambda \approx 0.3\)** (broad sampling), then refine query and use **\(\lambda \approx 0.7\)** (focus).
- **Summarization procedure (Section 4):** segment document into passages (sentences); rerank passages with **MMR + cosine similarity**; output top passages in original document order.
- **Empirical results:**
  - User pilot (Section 3): **80%** chose MMR method for a search task.
  - SUMMAC’98 (Section 4): query-relevant summaries **F-score = 0.73**; informative summaries **70% accuracy**.
  - Table 1 (sentence precision; compression 10% / 25%):  
    - 10%: \(\lambda=1\) **.78/.83**, \(\lambda=.7\) **.76/.83**, \(\lambda=.3\) **.74/.79**, Lead **.74/.83**  
    - 25%: \(\lambda=1\) **.74/.76**, \(\lambda=.7\) **.73/.74**, \(\lambda=.3\) **.74/.76**, Lead **.60/.65**

## When to surface
Use when students ask how to rank retrieved memories/passages to reduce redundancy while staying relevant (e.g., “diverse retrieval,” “anti-repetition,” “novelty-aware reranking,” “MMR formula and λ tuning”).