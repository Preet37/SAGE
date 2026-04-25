# Card: DAEA—Domain Adaptation for Real-World Entity Alignment
**Source:** https://aclanthology.org/2025.coling-main.393v1.pdf  
**Role:** benchmark | **Need:** EMPIRICAL_DATA  
**Anchor:** Entity-alignment evaluation tables (Hits@1/10, MRR) on real-world KGs + source-KG selection distances + ablations

## Key Content
- **Task defs (Section 3):** KG \(G=(E,R,A,V,T_r,T_a)\) with relation triples \(T_r\subseteq E\times R\times E\) and attribute triples \(T_a\subseteq E\times A\times V\). EA: given aligned seed pairs \(S=\{(e_i^1,e_j^2)\mid e_i^1\equiv e_j^2\}\), predict remaining equivalents.
- **Pipeline (Section 4):** (1) **Multi-source KG selection** (Fig.2): choose source DBP15K sub-dataset closest to target via **semantic + structural distance**. (2) **Domain adaptation training** (Fig.3): BERT-INT-style fine-tuning with total loss \(Loss=L_s+L_t+L_{DA}\) (Eq.11).
- **Source selection distance:** \(D_{G_sG_t}=\{D_{G_{s1}G_t},...,D_{G_{su}G_t}\}\) (Eq.1), with \(D_{G_{si}G_t}=d^{SE}_{G_{si}G_t}+d^{ST}_{G_{si}G_t}\) (Eq.2). Semantic distance uses **GloVe** entity-name embeddings + **JS distance** (Eq.5–7). Structural distance uses **2-layer GAT** (Eq.8–9) trained with contrastive loss \(L_c=\frac{1}{|N_i|}\sum_{e_j\in N_i}\max(0,M-\text{Eu}(e_i,e_j))\) (Eq.10).
- **Pairwise margin loss (Eq.12):** for \((e_i^1,e_j^2)\in S\), negative \(e_{j^-}^2\sim E_2\): \(\max\{0,\|e_i^1-e_j^2\|_1-\|e_i^1-e_{j^-}^2\|_1+M\}\).
- **Domain adaptive loss (Eq.13–16):** align source/target **positive** and **negative** distributions using **MMD** with Gaussian kernel (Eq.15); \(L_{DA}=DA_P+DA_N\).
- **Key empirical results (Table 2, real-world):**
  - **DOREMUS:** DAEA **H@1 77.84**, H@10 88.62, MRR 0.815 vs BERT-INT H@1 47.9 (MRR 0.515) and Attr-Int H@1 48.74 (MRR 0.587). Reported improvement: **+29.94 H@1** over prior best.
  - **AGROLD:** DAEA **H@1 27.14**, H@10 34.85, MRR 0.300 vs BERT-INT H@1 21.50 (MRR 0.229). Reported improvement: **+5.64 H@1**.
- **Source-KG choice matters (Table 3):** FR-EN has smallest distance and best results. Example: DOREMUS \(D=67.51\Rightarrow\) H@1 77.84; ZH-EN \(D=90.72\Rightarrow\) H@1 71.25; JA-EN \(D=105.71\Rightarrow\) H@1 70.65.
- **Ablation (Table 4):** removing DA drops DOREMUS H@1 **77.84→71.86**; AGROLD **27.14→26.24**. Using only positives: DOREMUS H@1 76.05; only negatives: AGROLD H@1 27.97 (best for AGROLD).
- **Defaults (Section 5.1.3):** train/test split **3:7**. Batch size: source **24**, AGROLD **19**. DOREMUS training set repeated **6×**, batch size **1**.

## When to surface
Use for questions about **why EA methods degrade on real-world KGs**, how to **select a transfer source KG**, and for **authoritative Hits@k/MRR comparisons and ablation evidence** on DOREMUS/AGROLD vs DBP15K-derived transfer.