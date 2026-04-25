# Card: word2vec (original C impl) — training choices & usage
**Source:** https://code.google.com/archive/p/word2vec/  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Authoritative description of CBOW vs Skip-gram, training pipeline, and recommended hyperparameter ranges; demo tools (distance/analogy/accuracy/phrases/classes).

## Key Content
- **Core procedure (training pipeline):**
  - Input: **text corpus** → build **vocabulary** → train **word vectors** → output vector file usable as ML/NLP features.
  - Two architectures: **CBOW** and **Skip-gram**; selected by CLI switch **`-cbow`** (CBOW faster; Skip-gram slower but better for infrequent words).
  - Two training objectives/approximations: **hierarchical softmax** (better for infrequent words) vs **negative sampling** (better for frequent words; better with low-dimensional vectors).
  - **Parallelism:** speed up with multi-CPU training via **`-threads N`**.
- **Key “equations” / vector operations (empirical property):**
  - Analogy-style linearity:  
    - **v(Paris) − v(France) + v(Italy) ≈ v(Rome)**  
    - **v(king) − v(man) + v(woman) ≈ v(queen)**
  - Sentence/phrase composition: averaging/addition of multiple word/phrase vectors can represent short text (weakly holds).
- **Hyperparameter guidance (numbers):**
  - **Subsampling of frequent words:** useful values **1e−3 to 1e−5** (improves accuracy + speed on large corpora).
  - **Context window:** Skip-gram usually **~10**; CBOW usually **~5**.
  - Strong regularities require **large datasets** and **sufficient vector dimensionality**.
- **Tools / workflows:**
  - **`distance`**: nearest neighbors by cosine similarity (example: “france” neighbors include spain 0.6785, belgium 0.6659…).
  - **`word2phrase`**: preprocess to form phrases (e.g., “san_francisco”).
  - **Evaluation demos:** `demo-word-accuracy.sh`, `demo-phrase-accuracy.sh`; best reported **>70% accuracy** with **~100% coverage** (data-dependent).
  - **Clustering:** K-means over vectors to produce word classes (`demo-classes.sh`).

## When to surface
Use when students ask how word2vec trains (CBOW vs Skip-gram), what hyperparameters to pick (window, subsampling, threads), or how to evaluate/inspect embeddings (distance, analogies, accuracy, phrases, clustering).