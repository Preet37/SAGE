# Card: Procedural Memory Retrieval Benchmark (ALFWorld)
**Source:** https://arxiv.org/pdf/2511.21730.pdf  
**Role:** benchmark | **Need:** COMPARISON_DATA  
**Anchor:** Benchmark tasks + quantitative results isolating *procedural* (skill/trajectory) retrieval under cross-context (vocabulary shift) generalization.

## Key Content
- **Problem definitions (Sec. 3.1):**
  - *Procedural trajectory:* sequence of state–action pairs \((s_t, a_t)\).
  - *Procedural similarity* aims at functional equivalence independent of object vocabulary: combines **structural patterns** (action sequence) + **semantic intent** (Eq. 1; described conceptually).
  - *Cross-context retrieval:* given corpus \(C\), query \(q\) with unseen object vocab, retrieval function \(R(q,C)\to\) ranked subset; objective maximize expected “procedural utility” over relevant set (Eq. 2).
  - *Generalization gap:* performance drop from seen→unseen contexts for method \(m\) (Eq. 3–4; defined as degradation).
- **Corpora (Sec. 3.2):**
  - **Expert ALFWorld corpus:** 78 trajectories (63 successful + 15 interrupted), avg length **14.2** actions, **42** unique object types, 6 task types.
  - **AgentInstruct corpus:** **336** trajectories (filtered from 954; **35.2%** retained), avg length **12.7** actions, **38** object types.
- **Retrieval methods (Sec. 3.3):** embeddings use **all-MiniLM-L6-v2** (384-d), cosine similarity (Eq. 5), stored in **ChromaDB**. Variants: action-only, enriched (adds task metadata/context), **LLM procedural summaries** (GPT-5), combined. Keyword baseline uses Jaccard (Eq. 6). **BM25 omitted** in final benchmark due to leakage from keyword-based coverage filtering.
- **Evaluation workflow (Sec. 3.4):**
  - **LLM-as-judge:** GPT-5, reasoning effort “low”, relevance score **1–10**; binary relevance threshold **6** (avoids zero-relevant queries).
  - **Coverage-balanced benchmark:** select validation tasks with **8–20** relevant trajectories (estimated via lightweight keyword overlap), then stratify into **EASY/MEDIUM/HARD** by procedural complexity; final **40 queries**.
  - Metrics: **MAP** (Eq. 7), P@k (Eq. 8), Recall@k (Eq. 9), F1@k (Eq. 10), NDCG@k (Eq. 11).
- **Key empirical results:**
  - **Generalization cliff (Table 1; 78 traj, 36 queries):**  
    - Combined embeddings MAP **0.844→0.592** (−**29.9%**)  
    - Enriched **0.794→0.565** (−**28.9%**)  
    - Action-only **0.756→0.488** (−**35.5%**)  
    - **Summary embeddings** **0.754→0.671** (−**11.0%**), rank **6→1** (best on unseen).
  - **Coverage-balanced (336 traj, 40 queries; Table Sec. 4.2):**  
    - State-aware MAP **0.7945** (EASY **0.842**, MED **0.746**, HARD **0.791**)  
    - Action-only MAP **0.7231** (EASY **0.668**, MED **0.802**, HARD **0.699**)
  - **Corpus scale ablation (Sec. 4.3.1):** 336 vs 78 (state-aware) MAP **0.7945 vs 0.644**; subsample retains **81.0%** of full.
- **Design rationale (Sec. 5):** mean-pooled sentence-transformers behave like **bag-of-words**, discarding temporal order; LLM summaries help by **explicitly abstracting** object-specific details before embedding.

## When to surface
Use when students ask how to **evaluate long-term/procedural memory retrieval** (not execution), how retrieval **fails under distribution shift**, or want **numbers comparing embedding vs abstraction-based memory representations**.