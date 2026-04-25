# Card: GloVe (Stanford) — official training pipeline + rationale
**Source:** https://nlp.stanford.edu/projects/glove/  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Reference implementation workflow: build global co-occurrence stats, then train GloVe vectors; plus what the objective is trying to match.

## Key Content
- **Model type / data:** Unsupervised word embeddings trained on **aggregated global word–word co-occurrence statistics** from a corpus (a sparse co-occurrence matrix of **non-zero entries**).
- **Core objective (Eq. 1, described):** Learn word vectors so that  
  **wᵢ · ŵⱼ ≈ log P(i, j)** (log of word–word co-occurrence probability).  
  - *wᵢ*: “word” vector for target word *i*  
  - *ŵⱼ*: “context” vector for context word *j*  
  - *P(i, j)*: probability of co-occurrence of *i* and *j* in the corpus  
  - Training uses a **weighted least-squares** objective over observed (non-zero) co-occurrences.
- **Design rationale:** Uses **ratios of co-occurrence probabilities** to encode meaning; since **log(a/b)=log a − log b**, **log-ratios map to vector differences**, explaining linear analogy structure (e.g., **man − woman ≈ king − queen ≈ brother − sister**).
- **Pipeline / workflow (official code):**
  1. **Download/compile:** `git clone` (or zip), then `make` in repo.
  2. **Run end-to-end demo:** `./demo.sh` (automates preprocessing + training).
  3. **Conceptual steps:** single corpus pass to **collect co-occurrence stats** (expensive one-time); then **multiple training iterations** are faster due to sparsity.
  4. **Further usage:** see included `README` / `Training_README`.
- **Concrete pretrained sets (empirical numbers):**
  - **2024 Dolma:** **220B tokens**, **1.2M vocab**, **uncased**, **300d**, **1.6GB**.
  - **2024 Wiki+Gigaword5:** **11.9B tokens**, **1.2M vocab**, **uncased**, **50/100/200/300d** (≈**290MB/560MB/1.1GB/1.6GB**).
  - **glove.6B:** **6B tokens**, **400K vocab**, **uncased**, **50/100/200/300d**, **822MB**.
  - **Common Crawl:** **42B tokens**, **1.9M vocab**, **uncased**, **300d**, **1.75GB**; and **840B tokens**, **2.2M vocab**, **cased**, **300d**, **2.03GB**.
  - **Twitter:** **27B tokens**, **1.2M vocab**, **uncased**, **25/50/100/200d**, **1.42GB**.

## When to surface
Use when a student asks how GloVe is trained in practice (official scripts/steps), what objective it optimizes (log co-occurrence / ratios), or needs concrete pretrained dataset sizes/dimensions.