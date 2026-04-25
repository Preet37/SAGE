# Card: Gensim Word2Vec API essentials (params + train/save/load)
**Source:** https://radimrehurek.com/gensim/models/word2vec.html  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Authoritative parameter meanings/defaults for `gensim.models.Word2Vec`, plus training + persistence workflows.

## Key Content
- **Core object & storage**
  - Full trainable model: `gensim.models.Word2Vec`; trained vectors live in `model.wv` (`KeyedVectors`).
  - Rationale: keep only `KeyedVectors` when done training to **reduce RAM** and enable **memory-mapped** fast loading/shared RAM: `KeyedVectors.load(..., mmap='r')`.
- **Initialization / training workflow**
  - One-shot: `model = Word2Vec(sentences=..., vector_size=100, window=5, min_count=1, workers=4)` then `model.save("word2vec.model")`.
  - Streamed training: `sentences` can be an iterable (disk/network), but **must be restartable** (not a one-pass generator) because multiple epochs require multiple passes.
  - Two-step explicit: `model = Word2Vec(min_count=1)` → `model.build_vocab(sentences)` → `model.train(sentences, total_examples=model.corpus_count, epochs=model.epochs)`.
  - `train()` requirement: must pass **either** `total_examples` (sentence count) **or** `total_words` for learning-rate decay/progress; must pass explicit `epochs` (often `epochs=model.epochs`).
- **Key querying**
  - Vector: `model.wv['computer']`; neighbors: `model.wv.most_similar('computer', topn=10)`.
- **Save/load variants**
  - Continue training only from full `Word2Vec.save()` / `Word2Vec.load()`.
  - Load original C word2vec format as `KeyedVectors.load_word2vec_format(..., binary=...)`; **cannot continue training** (missing hidden weights/frequencies/tree).
- **Important defaults (constructor)**
  - `vector_size=100`, `window=5`, `min_count=5`, `sample=0.001`, `workers=3`, `epochs=5`
  - `alpha=0.025`, `min_alpha=0.0001`
  - `sg=0` (CBOW), `hs=0`, `negative=5`, `ns_exponent=0.75`, `cbow_mean=1`
  - `seed=1`, `batch_words=10000`, `sorted_vocab=1`, `shrink_windows=True` (effective window sampled uniformly from `[1, window]`)

## When to surface
Use when students ask what Word2Vec hyperparameters mean/default to in Gensim, how to correctly stream/train with `build_vocab()` + `train()`, or how saving/loading differs between full models vs `KeyedVectors`/C-format vectors.