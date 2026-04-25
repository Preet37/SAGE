# Card: OVQA — Open-vocabulary VideoQA benchmark (long-tail + unseen answers)
**Source:** https://arxiv.org/pdf/2308.09363.pdf  
**Role:** benchmark | **Need:** EMPIRICAL_DATA  
**Anchor:** Benchmark definition + category-wise tables measuring generalization to rare/unseen answers (distribution shift) in open-ended VideoQA.

## Key Content
- **Problem (Sec.1–2):** “Open-ended” VideoQA is often implemented as **closed-vocabulary classification** over top-k frequent answers (e.g., top-1000), causing near-zero performance on **out-of-vocabulary (unseen)** answers. Example stat: in MSRVTT-QA, **top-1000 answers = 17.8% of unique answers but 90.2% of samples** (Fig.1).
- **OVQA answer categories (Sec.2.1, Table 1):** based on training frequency: **Base (≥101), Common (11–100), Rare (1–10), Unseen (0)**. Unique-answer counts:  
  - MSVD-QA: Base 41 / Common 333 / Rare 1,478 / Unseen 391 (Total 2,243)  
  - MSRVTT-QA: 205 / 937 / 2,858 / 1,632 (Total 5,632)  
  - TGIF-QA: 38 / 210 / 1,292 / 206 (Total 1,746)  
  - ActivityNet-QA: 26 / 275 / 1,353 / 1,378 (Total 3,032)
- **Task definition (Sec.2.2):** replace MLP-over-classes with **similarity between [MASK] feature** \(m\in\mathbb{R}^D\) and **answer embeddings**; report **Total acc** plus per-category (B/C/R/U) and **mAcc** = mean accuracy over unique answers.
- **GNN soft verbalizer (Sec.3, Eq.1/5–8):** message passing  
  \(h_i^{(l)}=\sigma\!\left(W^{(l)}\cdot \text{AGG}(\{h_j^{(l-1)}:j\in N_i\})\right)\) (Eq.1); GAT attention \(\alpha_{ij}^{(l)}\) (Eq.5), aggregate \(\sum_{j\in N_i}\alpha_{ij}^{(l)}h_j^{(l-1)}\) (Eq.6). Convex combine: \(\hat H=\varepsilon V+(1-\varepsilon)H\) (Eq.7). Train with CE: \(L=\text{CE}(a_{GT},\text{Softmax}(\hat H m))\) (Eq.8). Defaults: **K=2 hops**, **L=2 layers**, search \(\varepsilon\in\{0.5,0.6,0.7,0.8,0.9\}\); answer encoder frozen; use **GloVe** neighbors.
- **Key empirical results (Table 2):** CVQA models often have **U=0.0** and tiny mAcc. Example MSRVTT-QA: **VIOLET (CVQA)** T=40.9, **U=0.0**, **mAcc=1.4**. **FrozenBiLM → FrozenBiLM+ (OVQA)** improves unseen and mAcc:  
  - MSRVTT-QA: U **0.0→6.6**, mAcc **6.7→12.4**, T **46.6→47.0**  
  - TGIF-QA: U **0.0→21.3**, mAcc **23.5→30.2**, T **68.6→69.0**
- **GNN gain (Table 3):** FrozenBiLM+ w/ GNN improves unseen: MSVD **13.7→16.1**, ActivityNet **4.2→5.8**, TGIF **18.7→21.3**, MSRVTT **5.8→6.6**.

## When to surface
Use when students ask how to evaluate VideoQA **generalization under long-tail/unseen answers**, or need **category-wise evidence** that “good overall accuracy” can hide failure on rare/OOV answers.