# Word Embeddings

## Video (best)
- **StatQuest (Josh Starmer)** — "Word Embedding and Word2Vec, Clearly Explained!!!"
- youtube_id: viZrOnJclY0
- Why: Starmer's signature visual-first, jargon-minimizing style makes the distributional hypothesis and the skip-gram/CBOW mechanics genuinely intuitive. He builds from "why do we need embeddings at all?" before showing the geometry, which is exactly the right pedagogical order for beginners entering LLM or multimodal courses.
- Level: beginner/intermediate

## Blog / Written explainer (best)
- **Jay Alammar** — "The Illustrated Word2Vec"
- url: https://jalammar.github.io/illustrated-word2vec/
- Why: Alammar's step-by-step animated diagrams walk through the training process, the sliding window, negative sampling, and the resulting vector space properties better than any other written resource. It bridges intuition and mechanism without requiring the reader to open a paper first. Directly relevant to all three courses listed.
- Level: beginner/intermediate

## Deep dive
- **Lilian Weng** — "Learning Word Embedding"
- url: https://lilianweng.github.io/posts/2017-10-15-word-embedding/
- Why: Weng's post is the most thorough single-page technical reference covering Word2Vec (skip-gram + CBOW), GloVe, FastText, and evaluation methods with clean mathematical notation. It serves as a reliable reference for ML engineering contexts where implementation details and loss functions matter.
- Level: intermediate/advanced

## Original paper
- **Mikolov et al. (2013)** — "Distributed Representations of Words and Phrases and their Compositionality"
- url: https://arxiv.org/abs/1310.4546
- Why: This is the canonical Word2Vec paper introducing negative sampling and phrase embeddings. It is more readable than the original 2013 ICLR submission and is the paper most courses actually assign. GloVe (Pennington et al., 2014) is the natural companion paper but Word2Vec is the clearer pedagogical starting point.
- Level: intermediate

## Code walkthrough
- **Andrej Karpathy** — "makemore" series, specifically the bigram/MLP episodes where embedding tables are built from scratch
- youtube_id: PaCmpygFfXo
- Why: Karpathy builds a character-level embedding table by hand in PyTorch, showing exactly how `nn.Embedding` works under the hood, why lookup tables are equivalent to one-hot × weight matrix, and how gradients flow. This is the best "from-scratch" implementation for learners in ml-engineering-foundations who need to understand embeddings mechanistically rather than just call an API.
- Level: intermediate/advanced

---

## Coverage notes
- **Strong:** Intuitive visual explanations (Alammar), mathematical depth (Weng), seminal theory (Mikolov et al.), from-scratch implementation (Karpathy)
- **Weak:** Contextual embeddings (ELMo, BERT-style) are only lightly covered by these resources — they focus on static embeddings. The transition from Word2Vec/GloVe to contextual embeddings needs a separate resource (e.g., Alammar's "The Illustrated BERT").
- **Weak:** Shared embedding spaces for multimodal settings (relevant to intro-to-multimodal) are not well covered by any single canonical resource at the beginner level.
- **Gap:** No single excellent video exists that covers **GloVe specifically** with the same clarity as the StatQuest Word2Vec video. The GloVe paper itself is the best available treatment.
- **Gap:** The **distributional hypothesis** as a standalone concept (Harris 1954 → Firth 1957 lineage) has no great modern video explainer; it is typically covered as a one-slide aside in broader NLP lectures.

---

## Cross-validation
This topic appears in 3 courses: **intro-to-llms**, **intro-to-multimodal**, **ml-engineering-foundations**

| Resource | intro-to-llms | intro-to-multimodal | ml-engineering-foundations |
|---|---|---|---|
| StatQuest video | ✅ foundation | ✅ foundation | ✅ foundation |
| Alammar blog | ✅ primary | ✅ primary | ✅ primary |
| Weng deep dive | ✅ reference | ⚠️ partial | ✅ reference |
| Mikolov paper | ✅ seminal | ⚠️ context only | ✅ seminal |
| Karpathy code | ✅ implementation | ❌ not multimodal | ✅ core |

The multimodal course will need supplementary material on **shared/joint embedding spaces** (e.g., CLIP) that none of these resources fully address.

---


> **[Structural note]** "Retrieval-Augmented Generation (RAG) Inside Agents" appears to have sub-concepts:
> retrieval-augmented generation, vector search, context injection, grounded generation, long-term memory retrieval
> *Discovered during enrichment for course "A hands-on intermediate course for software developers and AI/ML engineers cover" | 2026-04-10*

## Last Verified
2025-04-06