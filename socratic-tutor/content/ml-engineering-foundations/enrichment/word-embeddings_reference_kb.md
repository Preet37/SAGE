## Core Definitions

**Word embeddings**: Dense, low-dimensional numeric vectors assigned to words (or tokens) so that words used in similar ways end up with similar vectors; this makes text usable as input features for neural networks and other ML models. Weng contrasts this with one-hot encoding: one-hot is extremely high-dimensional and does not encode similarity, while embeddings are dense and can place similar words near each other in vector space. (Weng, “Learning Word Embedding”)

**Distributional hypothesis**: A working assumption behind many embedding methods: words that occur in similar contexts tend to have similar meanings, so “context” statistics can be used to learn semantic representations. Weng explicitly motivates embedding learning from contextual information (“similar words may appear in similar context often”). (Weng)

**Word2Vec**: A family of efficient neural methods for learning word vectors from large corpora by training a model on a prediction task involving local context. The original implementation describes two architectures—CBOW and Skip-gram—and two main training approximations—hierarchical softmax and negative sampling. (Mikolov et al. 2013; word2vec C archive)

**Skip-gram (Word2Vec architecture)**: A Word2Vec architecture trained to predict surrounding context words given a center (target) word, using a sliding window over text. Mikolov et al. define the objective as maximizing the average log probability of context words within a window around each target token. (Mikolov et al. 2013 NeurIPS paper)

**CBOW (Word2Vec architecture)**: A Word2Vec architecture trained to predict the center (target) word from its surrounding context words; the word2vec reference notes CBOW is typically faster, while Skip-gram tends to work better for infrequent words. (word2vec C archive; Weng)

**Negative sampling (NEG / SGNS)**: A training objective/approximation for Skip-gram that replaces the expensive full softmax with a binary classification objective: distinguish observed (word, context) pairs from noise (negative) pairs sampled from a distribution (commonly unigram\*\*3/4). Mikolov et al. give the NEG objective; Goldberg & Levy present the SGNS objective explicitly and interpret it as binary classification. (Mikolov et al. 2013 NeurIPS; Goldberg & Levy 2014)

**Hierarchical softmax (HS)**: A softmax approximation that factorizes word probability along a binary tree path (often a Huffman tree), reducing computation from summing over the whole vocabulary to visiting ~log(V) nodes. (Mikolov et al. 2013 NeurIPS; word2vec C archive)

**GloVe**: A count-based embedding method that learns vectors from aggregated global word–word co-occurrence statistics. The Stanford GloVe page summarizes the goal as matching dot products to log co-occurrence probabilities; the original paper formalizes this as a weighted least-squares objective over nonzero co-occurrence entries. (Stanford GloVe site; Pennington et al. 2014)

**Static (context-independent) embeddings**: Traditional word *type* embeddings (e.g., GloVe/word2vec) assign one vector per word type, regardless of the sentence it appears in. (Peters et al. 2018, ELMo)

**Contextual embeddings**: Token representations computed as a function of the entire input sentence, so the same word type can have different vectors in different contexts. ELMo is a concrete example: it produces token vectors from a bidirectional language model and mixes internal layers. (Peters et al. 2018, ELMo)

---

## Key Formulas & Empirical Results

### Word2Vec Skip-gram objective (local context prediction)
Mikolov et al. (2013) define Skip-gram as maximizing:
\[
\frac{1}{T}\sum_{t=1}^{T}\sum_{-c\le j\le c, j\ne 0}\log p(w_{t+j}\mid w_t)
\]
- **T**: number of tokens in corpus  
- **c**: context window size  
- Supports the claim: Word2Vec learns embeddings by predicting nearby words from a center word. (Mikolov et al. 2013 NeurIPS)

### Softmax parameterization (expensive baseline)
\[
p(w_O\mid w_I)=\frac{\exp({v'_{w_O}}^\top v_{w_I})}{\sum_{w=1}^{W}\exp({v'_w}^\top v_{w_I})}
\]
- **\(v_w\)**: “input” vector for word w  
- **\(v'_w\)**: “output” vector for word w  
- **W**: vocabulary size  
- Supports: why approximations (HS/NEG) are used—denominator sums over all words. (Mikolov et al. 2013 NeurIPS; Goldberg & Levy 2014)

### Negative sampling (Mikolov et al. 2013) / SGNS objective (Goldberg & Levy 2014)
Mikolov et al. replace \(\log p(w_O\mid w_I)\) with:
\[
\log\sigma({v'_{w_O}}^\top v_{w_I})+\sum_{i=1}^{k}\mathbb{E}_{w_i\sim P_n(w)}[\log\sigma(-{v'_{w_i}}^\top v_{w_I})]
\]
Goldberg & Levy give the SGNS form:
\[
\sum_{(w,c)\in D}\log\sigma(v_c\cdot v_w)+\sum_{(w,c)\in D'}\log\sigma(-v_c\cdot v_w)
\]
- **k**: number of negatives per positive  
- **\(P_n(w)\)**: noise distribution; Mikolov recommends unigram\*\*3/4; Goldberg & Levy describe sampling contexts from unigram\*\*3/4.  
- Supports: NEG/SGNS trains by pushing observed pairs’ dot products up and sampled negatives’ dot products down. (Mikolov et al. 2013 NeurIPS; Goldberg & Levy 2014)

**Typical k guidance (Mikolov et al.)**: k ≈ **5–20** for small data; **2–5** for large data. (Mikolov et al. 2013 NeurIPS)

### Subsampling frequent words (Word2Vec)
Discard frequent token \(w_i\) with:
\[
P(w_i)=1-\sqrt{\frac{t}{f(w_i)}}
\]
- **t**: threshold, about **1e−5** in Mikolov et al.  
- **f(w_i)**: frequency of word \(w_i\)  
- Supports: improves speed (2×–10×) and can improve rare-word vectors. (Mikolov et al. 2013 NeurIPS)

**word2vec implementation guidance**: subsampling values **1e−3 to 1e−5** are useful on large corpora. (word2vec C archive)

### Hierarchical softmax probability (tree factorization)
Mikolov et al. define:
\[
p(w\mid w_I)=\prod_{j=1}^{L(w)-1}\sigma\Big(\big[\![n(w,j+1)=ch(n(w,j))]\!\big]\cdot {v'_{n(w,j)}}^\top v_{w_I}\Big)
\]
- Uses a **Huffman tree** so frequent words have shorter codes.  
- Supports: HS reduces computation to ~log(V) node visits. (Mikolov et al. 2013 NeurIPS)

### GloVe objective (Pennington et al. 2014)
Co-occurrence counts \(X_{ij}\) and objective:
\[
w_i^\top \tilde w_j + b_i + \tilde b_j = \log(X_{ij})
\]
\[
J=\sum_{i,j=1}^V f(X_{ij})\left(w_i^\top \tilde w_j+b_i+\tilde b_j-\log X_{ij}\right)^2
\]
Weighting function:
\[
f(x)=\begin{cases}(x/x_{\max})^\alpha & x<x_{\max}\\ 1 & \text{otherwise}\end{cases}
\]
Defaults reported: \(x_{\max}=100\), \(\alpha=3/4\). (Pennington et al. 2014; Stanford GloVe site)

**Training defaults reported (Pennington et al.)**
- Symmetric window: **10 left + 10 right**, distance weighting **1/d**
- Optimizer: **AdaGrad**, initial LR **0.05**
- Iterations: **50** if dim < 300; **100** otherwise
- Final vectors often **\(W+\tilde W\)** (Pennington et al. 2014)

### Empirical benchmarks (GloVe paper)
**Analogy accuracy (Table 2)**:
- GloVe **300d, 42B tokens**: Sem **81.9**, Syn **69.3**, Total **75.0** (best overall in their table)
- GloVe **300d, 6B**: Total **71.7** vs **SG† 69.1**, **CBOW† 65.7** (Pennington et al. 2014)

**Word similarity (Table 3, Spearman, 300d)**:
- GloVe **42B**: WS353 **75.9**, MC **83.6**, RG **82.9**, RW **47.8**
- GloVe **6B**: WS353 **65.8** (Pennington et al. 2014)

### Empirical speed/accuracy tradeoffs (Word2Vec paper)
On 1B words (vocab 692K, min count 5, 300d), Mikolov et al. report (Table 1):
- With subsampling \(10^{-5}\): **NEG-5 total 60% (14 min)**; **NEG-15 total 61% (36 min)**; **HS-Huffman total 55% (21 min)**  
Supports: NEG can be faster and strong; subsampling improves speed and accuracy. (Mikolov et al. 2013 NeurIPS)

### Contextual vs static embeddings (ELMo definition + formula)
Peters et al. define ELMo token representation (Eq. 1):
\[
\mathrm{ELMo}^{task}_k=\gamma^{task}\sum_{j=0}^L s^{task}_j\, h^{LM}_{k,j}
\]
- **k**: token position; **j**: layer index (0..L)  
- **\(s^{task}_j\)**: softmax-normalized layer weights; **\(\gamma^{task}\)**: learned scalar  
Supports: contextual embeddings are computed from a sentence-conditioned biLM and can mix layers per task. (Peters et al. 2018)

**ELMo downstream gains (Table 1 examples)**:
- SQuAD F1: **81.1 → 85.8** (+4.7)
- NER F1: **90.15 → 92.22** (+2.06) (Peters et al. 2018)

### Gensim Word2Vec defaults (API-level)
From `gensim.models.Word2Vec` docs:
- `vector_size=100`, `window=5`, `min_count=5`, `sample=0.001`, `epochs=5`
- `sg=0` (CBOW), `hs=0`, `negative=5`, `ns_exponent=0.75`
- `alpha=0.025`, `min_alpha=0.0001`
- `shrink_windows=True` (effective window sampled uniformly from `[1, window]`) (Gensim Word2Vec docs)

---

## How It Works

### A. Word2Vec training loop (Skip-gram + Negative Sampling, mechanics)
1. **Build vocabulary** from corpus; drop words below `min_count`. (word2vec C archive; Gensim docs)
2. **Generate training pairs** with a sliding window:
   - For each position t (center word \(w_t\)), collect context words \(w_{t+j}\) for \(j \in [-c,c]\setminus\{0\}\). (Mikolov et al. 2013)
3. **(Optional) Subsample frequent words** using Mikolov’s discard probability \(1-\sqrt{t/f(w)}\). (Mikolov et al. 2013)
4. **For each positive pair (w, c)**:
   - Compute score \(s^+ = v_w \cdot v'_c\)
   - Add loss term \(\log \sigma(s^+)\). (Mikolov et al. 2013; Goldberg & Levy 2014)
5. **Sample k negative contexts** \(c_1..c_k\) from noise distribution (commonly unigram\*\*3/4):
   - For each negative \(c_i\), compute \(s^-_i = v_w \cdot v'_{c_i}\)
   - Add loss term \(\log \sigma(-s^-_i)\). (Mikolov et al. 2013; Goldberg & Levy 2014)
6. **Update parameters** (the embedding matrices for input vectors \(v\) and output vectors \(v'\)) by gradient ascent/descent.
7. After training, **use learned vectors** (often the input vectors, or some combination depending on implementation) for similarity/analogy queries. (word2vec C archive; Gensim docs)

### B. Word2Vec alternatives: Hierarchical Softmax (HS)
1. Build a **binary tree** over vocabulary (often Huffman-coded so frequent words have shorter paths). (Mikolov et al. 2013)
2. Probability of a word is the **product of sigmoid decisions** along its path (Eq. 3). (Mikolov et al. 2013)
3. Training updates only the nodes on the path, giving ~log(V) complexity per example.

### C. GloVe training pipeline (official workflow + objective)
1. **Single corpus pass** to build sparse global co-occurrence statistics (non-zero entries only). (Stanford GloVe site)
2. Train vectors by minimizing weighted least squares so that:
   - \(w_i^\top \tilde w_j + b_i + \tilde b_j \approx \log X_{ij}\) (Pennington et al. 2014)
3. Use weighting function \(f(X_{ij})\) with defaults \(x_{\max}=100\), \(\alpha=3/4\). (Pennington et al. 2014)
4. After training, use **\(W+\tilde W\)** as final word vectors (as reported in the paper). (Pennington et al. 2014)

### D. Contextual embeddings via ELMo (concrete “static vs contextual” mechanism)
1. **Pretrain a bidirectional language model (biLM)**:
   - Forward LM predicts \(t_k\) from \(t_{1:k-1}\)
   - Backward LM predicts \(t_k\) from \(t_{k+1:N}\)
   - Joint objective sums forward + backward log-likelihoods. (Peters et al. 2018)
2. For each token position k, collect internal layer representations \(h^{LM}_{k,j}\) (including token layer \(j=0\)). (Peters et al. 2018)
3. For a downstream task, compute a **learned weighted mixture** of layers:
   - \(\mathrm{ELMo}^{task}_k=\gamma \sum_j s_j h_{k,j}\). (Peters et al. 2018)
4. Use \([x_k; \mathrm{ELMo}_k]\) as features in a supervised model; Peters et al. often **freeze** the biLM and train only task parameters + mixing weights. (Peters et al. 2018)

---

## Teaching Approaches

### Intuitive (no math)
- Start with the problem: one-hot vectors treat every word as equally unrelated; “great” and “awesome” are far apart even though they’re similar. (StatQuest transcript; Weng)
- Embeddings are “smart numbers”: similar words get similar vectors because the model learns from how words appear near each other in text (distributional idea). (Weng; StatQuest transcript)
- Word2Vec learns these vectors by playing a prediction game: guess nearby words (Skip-gram) or guess the center word (CBOW). (word2vec C archive; Weng)

### Technical (with math)
- Skip-gram maximizes \(\sum \log p(context \mid center)\) (Mikolov et al. 2013).
- Full softmax is expensive; NEG replaces it with \(\log\sigma(v\cdot v')\) for positives and \(\log\sigma(-v\cdot v')\) for sampled negatives (Mikolov et al. 2013; Goldberg & Levy 2014).
- GloVe instead fits dot products to \(\log X_{ij}\) with weighted least squares (Pennington et al. 2014).

### Analogy-based
- “Words as coordinates”: each word is a point in a semantic space; closeness corresponds to similarity (StatQuest transcript; Weng).
- “Two ways to learn a map”:
  - Word2Vec: learn by repeatedly predicting neighbors (local prediction game).
  - GloVe: learn by fitting a global co-occurrence table (global statistics). (Weng; Stanford GloVe site)

---

## Common Misconceptions

1. **“Word2Vec/GloVe understand meaning like a dictionary.”**  
   - **Why wrong:** The training signals are co-occurrence/prediction objectives (Skip-gram/CBOW; log co-occurrence fitting), not explicit definitions or grounded semantics. (Mikolov et al. 2013; Pennington et al. 2014; Weng)  
   - **Correct model:** They capture *distributional* regularities: words used in similar contexts get similar vectors (distributional hypothesis framing in Weng).

2. **“Each word has one true embedding, even in different sentences.”**  
   - **Why wrong:** Static embeddings assign one vector per word type; contextual methods compute token vectors as a function of the whole sentence. (Peters et al. 2018)  
   - **Correct model:** Static = type-level; contextual = token-level. ELMo explicitly produces different vectors for the same word in different contexts via a biLM and layer mixing. (Peters et al. 2018)

3. **“Negative sampling is just picking random wrong words; the distribution doesn’t matter.”**  
   - **Why wrong:** Mikolov et al. report unigram\*\*3/4 works better than unigram or uniform; Goldberg & Levy specify the 3/4 exponent in how negatives are sampled. (Mikolov et al. 2013; Goldberg & Levy 2014)  
   - **Correct model:** NEG performance depends on the noise distribution; word2vec commonly uses unigram\*\*3/4 and a tunable number of negatives k.

4. **“CBOW and Skip-gram are basically the same; choose either.”**  
   - **Why wrong:** The word2vec reference explicitly notes CBOW is faster, while Skip-gram is slower but better for infrequent words; they also reverse prediction direction (context→target vs target→context). (word2vec C archive)  
   - **Correct model:** Choose based on speed vs rare-word quality and your data regime.

5. **“GloVe is just SVD/matrix factorization; it doesn’t have a real objective.”**  
   - **Why wrong:** Pennington et al. give an explicit weighted least-squares objective over co-occurrence entries with a specific weighting function and defaults. (Pennington et al. 2014)  
   - **Correct model:** GloVe is a log-bilinear regression on \(\log X_{ij}\) with weighting \(f(X_{ij})\), trained with AdaGrad and specific windowing choices.

---

## Worked Examples

### 1) Train and query Word2Vec in Gensim (minimal, tutor-runnable)
```python
from gensim.models import Word2Vec

sentences = [
    ["the", "man", "walks"],
    ["the", "woman", "walks"],
    ["the", "king", "rules"],
    ["the", "queen", "rules"],
]

# Key params from Gensim docs: vector_size, window, min_count, workers
model = Word2Vec(
    sentences=sentences,
    vector_size=50,
    window=5,
    min_count=1,
    workers=1,
    sg=1,          # 1 = skip-gram, 0 = CBOW (Gensim docs)
    negative=5,    # default negative sampling count (Gensim docs)
)

# Vector lookup
vec_king = model.wv["king"]
print(vec_king.shape)

# Nearest neighbors by cosine similarity
print(model.wv.most_similar("king", topn=3))
```

**Tutor notes (what to point out mid-conversation)**
- `model.wv` holds the trained vectors; the full model includes extra training state. (Gensim docs)
- If a student tries to stream data: remind them sentences must be **restartable** for multiple epochs. (Gensim docs)

### 2) Two-step streamed training pattern (common failure mode)
```python
from gensim.models import Word2Vec

sentences = [
    ["this", "is", "a", "sentence"],
    ["this", "is", "another", "sentence"],
]

model = Word2Vec(min_count=1)
model.build_vocab(sentences)
model.train(
    sentences,
    total_examples=model.corpus_count,  # required for LR decay/progress (Gensim docs)
    epochs=model.epochs                 # pass explicit epochs (Gensim docs)
)
```

### 3) Phrase preprocessing hook (when student asks about “Air Canada”)
Mikolov et al. propose a bigram phrase score:
\[
score(w_i,w_j)=\frac{count(w_iw_j)-\delta}{count(w_i)\,count(w_j)}
\]
Keep bigrams above a threshold; run multiple passes to build longer phrases, then treat phrases as single tokens during training. (Mikolov et al. 2013 NeurIPS)

---

## Comparisons & Trade-offs

| Method | Representation type | Training signal | Strengths (from sources) | Limitations (from sources) | When to choose |
|---|---|---|---|---|---|
| Word2Vec (Skip-gram/CBOW) | Static (type-level) | Local context prediction; softmax approximations (NEG/HS) | Efficient; NEG/HS + subsampling speedups; Skip-gram better for infrequent words (word2vec ref); concrete speed/accuracy tradeoffs reported (Mikolov et al.) | Indifferent to word order; struggles with idiomatic phrases unless phrase modeling is added (Mikolov arXiv abs 1310.4546) | Need fast, strong static vectors; limited compute; classic similarity/analogy features |
| GloVe | Static (type-level) | Fit dot products to log co-occurrence counts with weighted LS | Uses global co-occurrence; strong analogy/similarity benchmarks reported (Pennington et al.) | Still one vector per word type (context-independent) | Want count-based global-statistics embeddings; easy use of pretrained sets |
| ELMo | Contextual (token-level) | biLM pretraining + task-specific layer mixing | Explicit contextual-vs-static improvement; large gains on multiple tasks (Peters et al.) | More complex; requires sentence context and LM computation | Polysemy matters; downstream tasks benefit from context-dependent token vectors |

**Selection note:** If the student’s pain point is “same word, different meaning,” surface the static-vs-contextual definition from Peters et al. and the ELMo mixing equation; if the pain point is “how do we train embeddings efficiently,” surface NEG/HS/subsampling from Mikolov et al. and/or Gensim defaults.

---

## Prerequisite Connections

- **One-hot encoding & vocabulary size**: Needed to appreciate why embeddings are dense and why one-hot is impractical at large vocabularies. (Weng)
- **Softmax and cross-entropy intuition**: Helps explain why full softmax is expensive and why NEG/HS are approximations. (Mikolov et al. 2013; StatQuest transcript references softmax/cross-entropy as assumed)
- **Dot product / cosine similarity**: Used for similarity queries and appears directly in objectives (e.g., \(v\cdot v'\)). (Mikolov et al. 2013; Stanford GloVe site)
- **Language modeling concept**: Needed to understand contextual embeddings like ELMo (forward/backward LM objectives). (Peters et al. 2018)

---

## Socratic Question Bank

1. **If two words never appear in the same sentence but appear in very similar contexts, what would you expect about their embeddings? Why?**  
   - Good answer: they can still be close because training uses context patterns (distributional idea; Weng).

2. **In Skip-gram, what are the training examples generated from a sentence with window size c?**  
   - Good answer: (center, context) pairs for each token and each neighbor within ±c excluding itself (Mikolov et al. 2013).

3. **Why is the full softmax in Word2Vec expensive, and what do NEG or HS change computationally?**  
   - Good answer: denominator sums over all vocab; NEG uses k negatives; HS uses log(V) tree path (Mikolov et al. 2013; Goldberg & Levy 2014).

4. **What does subsampling frequent words do to training speed and (according to Mikolov et al.) to rare-word vectors?**  
   - Good answer: discards frequent tokens with probability based on t/f; yields 2×–10× speedup and improves rare-word vectors (Mikolov et al. 2013).

5. **How does GloVe’s objective connect dot products to corpus statistics?**  
   - Good answer: fits \(w_i^\top \tilde w_j + b_i + \tilde b_j\) to \(\log X_{ij}\) with weighting \(f(X_{ij})\) (Pennington et al. 2014).

6. **What is the key difference between a static embedding and a contextual embedding, in one sentence?**  
   - Good answer: static gives one vector per word type; contextual gives a vector per token depending on the whole sentence (Peters et al. 2018).

7. **If you load vectors in word2vec C format into Gensim, can you continue training? Why/why not?**  
   - Good answer: no; `KeyedVectors` lacks hidden weights/frequencies/tree needed to resume (Gensim docs).

8. **Why does ELMo mix layers instead of always using the last layer?**  
   - Good answer: ELMo defines a learned weighted sum over layers per task (Eq. 1), and ablations show all layers can outperform last-only (Peters et al. 2018).

---

## Likely Student Questions

**Q: What’s the exact negative sampling loss used in Word2Vec?**  
→ **A:** Mikolov et al. replace \(\log p(w_O\mid w_I)\) with \(\log\sigma({v'_{w_O}}^\top v_{w_I})+\sum_{i=1}^{k}\mathbb{E}_{w_i\sim P_n(w)}[\log\sigma(-{v'_{w_i}}^\top v_{w_I})]\), where k is the number of negatives and \(P_n\) is typically unigram\*\*3/4. (https://proceedings.neurips.cc/paper_files/paper/2013/file/9aa42b31882ec039965f3c4923ce901b-Paper.pdf)

**Q: How are negative examples sampled (what distribution)?**  
→ **A:** Both Mikolov et al. and Goldberg & Levy describe sampling negatives from unigram\*\*3/4 (word2vec uses unigram distribution raised to the 3/4 power, normalized). (Mikolov 2013 NeurIPS; https://arxiv.org/pdf/1402.3722.pdf)

**Q: What does subsampling frequent words look like mathematically, and what t should I use?**  
→ **A:** Mikolov et al. discard token \(w_i\) with probability \(1-\sqrt{t/f(w_i)}\) and report \(t\approx 10^{-5}\); the word2vec reference suggests useful values in the range **1e−3 to 1e−5** on large corpora. (Mikolov 2013 NeurIPS; https://code.google.com/archive/p/word2vec/)

**Q: What objective does GloVe optimize?**  
→ **A:** Pennington et al. minimize \(J=\sum_{i,j} f(X_{ij})\left(w_i^\top \tilde w_j+b_i+\tilde b_j-\log X_{ij}\right)^2\) with \(f(x)=(x/x_{\max})^\alpha\) for \(x<x_{\max}\) else 1; defaults \(x_{\max}=100\), \(\alpha=3/4\). (https://aclanthology.org/D14-1162.pdf)

**Q: What are the typical GloVe training hyperparameters reported in the paper?**  
→ **A:** They report a symmetric context window of **10 left + 10 right** with distance weighting **1/d**, AdaGrad with initial LR **0.05**, and **50** iterations if dim < 300 else **100**; final vectors often use **\(W+\tilde W\)**. (https://aclanthology.org/D14-1162.pdf)

**Q: How do contextual embeddings differ from Word2Vec/GloVe in a precise way?**  
→ **A:** Peters et al. state traditional embeddings (GloVe/word2vec) give one context-independent vector per word type, while ELMo assigns each token a vector as a function of the entire sentence, computed from a bidirectional LM and a learned layer mixture (Eq. 1). (https://aclanthology.org/N18-1202.pdf)

**Q: What are Gensim Word2Vec defaults for negative sampling and window size?**  
→ **A:** Gensim defaults include `window=5`, `negative=5`, `ns_exponent=0.75`, `epochs=5`, `vector_size=100`, and `sg=0` (CBOW). (https://radimrehurek.com/gensim/models/word2vec.html)

**Q: Can I keep only vectors to save RAM after training in Gensim?**  
→ **A:** Yes—Gensim stores vectors in `model.wv` (`KeyedVectors`), and you can save/load `KeyedVectors` (including memory-mapped loading via `mmap='r'`) to reduce RAM; but continuing training requires saving/loading the full `Word2Vec` model. (https://radimrehurek.com/gensim/models/word2vec.html)

---

## Available Resources

### Videos
- [Word Embedding and Word2Vec, Clearly Explained!!! (StatQuest)](https://www.youtube.com/watch?v=viZrOnJclY0) — **Surface when:** student is stuck on “why embeddings” or needs an intuition-first explanation of similarity in vector space and the motivation for Word2Vec.
- [makemore series (Karpathy) — embedding tables built from scratch](https://www.youtube.com/watch?v=PaCmpygFfXo) — **Surface when:** student wants to see embeddings as a learned lookup table inside a neural net and how training updates those vectors.

### Articles & Tutorials
- [The Illustrated Word2Vec (Jay Alammar)](https://jalammar.github.io/illustrated-word2vec/) — **Surface when:** student asks for a visual walkthrough of Skip-gram/CBOW, sliding windows, and negative sampling.
- [Learning Word Embedding (Lilian Weng)](https://lilianweng.github.io/posts/2017-10-15-word-embedding/) — **Surface when:** student wants a compact technical reference comparing count-based vs context-based methods.
- [Distributed Representations of Words and Phrases and their Compositionality (Mikolov et al.)](https://arxiv.org/abs/1310.4546) — **Surface when:** student asks about limitations (word order, idioms) and phrase extensions.

---

## Visual Aids

![A word represented as a dense numeric vector (embedding). — Jay Alammar](/api/wiki-images/word-embeddings/images/jalammar-illustrated-bert_011.png)  
**Show when:** student needs the basic “word → dense vector” mental model before any training details.

![Skip-gram model: one-hot input → N-dim embedding → softmax output. (Weng, 2017)](/api/wiki-images/word-embeddings/images/lilianweng-posts-2017-10-15-word-embedding_001.png)  
**Show when:** student asks “where is the embedding stored in the network?” or “what are the weight matrices?”

![CBOW model: multiple context vectors averaged → predict target word. (Weng, 2017)](/api/wiki-images/word-embeddings/images/lilianweng-posts-2017-10-15-word-embedding_002.png)  
**Show when:** student confuses CBOW vs Skip-gram directionality.

![GloVe gives 'stick' one fixed vector regardless of meaning. — Jay Alammar](/api/wiki-images/word-embeddings/images/jalammar-illustrated-bert_013.png)  
**Show when:** student asks why static embeddings fail for polysemy.

![ELMo assigns different embeddings to 'stick' based on context. — Jay Alammar](/api/wiki-images/word-embeddings/images/jalammar-illustrated-bert_012.png)  
**Show when:** student asks what “contextual embedding” concretely means.

---

## Key Sources

- [Word2Vec Skip-gram—NEG, Hierarchical Softmax, Subsampling, Phrases (Mikolov et al., 2013 NeurIPS)](https://proceedings.neurips.cc/paper_files/paper/2013/file/9aa42b31882ec039965f3c4923ce901b-Paper.pdf) — Primary formulas for Skip-gram, NEG, HS, subsampling; includes speed/accuracy numbers.
- [GloVe: Global Vectors for Word Representation (Pennington et al., 2014)](https://aclanthology.org/D14-1162.pdf) — Definitive GloVe objective, weighting function defaults, and benchmark tables.
- [GloVe project page (Stanford)](https://nlp.stanford.edu/projects/glove/) — Practical training workflow and objective intuition (dot product ≈ log co-occurrence probability).
- [Deep contextualized word representations (ELMo) (Peters et al., 2018)](https://aclanthology.org/N18-1202.pdf) — Precise static-vs-contextual definition and the ELMo layer-mixing equation + downstream gains.
- [Gensim Word2Vec documentation](https://radimrehurek.com/gensim/models/word2vec.html) — Tutor-ready API defaults and common training/save/load pitfalls.