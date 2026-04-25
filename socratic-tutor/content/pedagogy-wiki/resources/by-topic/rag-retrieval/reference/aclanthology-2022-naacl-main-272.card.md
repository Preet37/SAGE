# Card: ColBERTv2 (late interaction + compression + denoised supervision)
**Source:** https://aclanthology.org/2022.naacl-main.272/  
**Role:** paper | **Need:** CONCEPT_EXPLAINER  
**Anchor:** Concrete improvements over ColBERT: (i) residual compression to cut index size, (ii) denoised supervision to improve training signal; effectiveness/efficiency tradeoffs with ablations.

## Key Content
- **Late interaction vs single-vector retrieval (core idea):**  
  Late-interaction retrievers encode **queries and documents as multiple vectors (token-level)** and compute relevance via **scalable token-level computations**, rather than collapsing each text into a single embedding vector. This typically improves retrieval quality but increases storage footprint by ~**an order of magnitude** (abstract).
- **ColBERTv2 contributions (abstract):**
  - **Aggressive residual compression mechanism** to reduce the **space footprint** of token-level (multi-vector) document representations while retaining effectiveness.
  - **Denoised supervision strategy** to improve training quality (cleaner/more reliable supervision signal than prior recipes).
- **Empirical headline result (abstract):**
  - Achieves **state-of-the-art quality** “within and outside the training domain”.
  - Reduces late-interaction index/storage footprint by **6–10×** compared to prior late-interaction models (i.e., ColBERT-style) while improving quality.
- **Design rationale (abstract):**
  - Late interaction is effective but storage-heavy; **compression** targets the main bottleneck (index size).  
  - **Denoised supervision** targets robustness/generalization beyond the training domain.

## When to surface
Use when students ask: “What is late interaction (ColBERT) and why is it better than single-vector retrieval?”, “How does ColBERTv2 make ColBERT practical (index size) without losing accuracy?”, or “What are the key training/indexing refinements and their measured gains (e.g., 6–10× smaller)?”