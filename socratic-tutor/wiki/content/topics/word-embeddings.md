---
title: "Word Embeddings"
subject: "Foundational AI"
date: 2025-04-06
tags:
  - "subject/foundational-ai"
  - "level/beginner"
  - "level/intermediate"
  - "level/advanced"
  - "educator/jay-alammar"
  - "educator/lilian-weng"
  - "educator/andrej-karpathy"
  - "resource/video"
  - "resource/blog"
  - "resource/deep-dive"
  - "resource/paper"
  - "resource/code"
educators:
  - "Jay Alammar"
  - "Lilian Weng"
  - "Andrej Karpathy"
levels:
  - "beginner"
  - "intermediate"
  - "advanced"
resources:
  - "video"
  - "blog"
  - "deep-dive"
  - "paper"
  - "code"
---

# Word Embeddings

## Video (best)
- **StatQuest (Josh Starmer)** — "Word Embedding and Word2Vec, Clearly Explained!!!"
- **Watch:** [YouTube](https://www.youtube.com/watch?v=viZrOnJclY0)
- Why: Starmer's signature visual-first, jargon-minimizing style makes the distributional hypothesis and the skip-gram/CBOW mechanics genuinely intuitive. He builds from "why do we need embeddings at all?" before showing the geometry, which is exactly the right pedagogical order for beginners entering LLM or multimodal courses.
- Level: beginner/intermediate

## Blog / Written explainer (best)
- **Jay Alammar** — "The Illustrated Word2Vec"
- **Link:** [https://jalammar.github.io/illustrated-word2vec/](https://jalammar.github.io/illustrated-word2vec/)
- Why: Alammar's step-by-step animated diagrams walk through the training process, the sliding window, negative sampling, and the resulting vector space properties better than any other written resource. It bridges intuition and mechanism without requiring the reader to open a paper first. Directly relevant to all three courses listed.
- Level: beginner/intermediate

## Deep dive
- **Lilian Weng** — "Learning Word Embedding"
- **Link:** [https://lilianweng.github.io/posts/2017-10-15-word-embedding/](https://lilianweng.github.io/posts/2017-10-15-word-embedding/)
- Why: Weng's post is the most thorough single-page technical reference covering Word2Vec (skip-gram + CBOW), GloVe, FastText, and evaluation methods with clean mathematical notation. It serves as a reliable reference for ML engineering contexts where implementation details and loss functions matter.
- Level: intermediate/advanced

## Original paper
- **Mikolov et al. (2013)** — "Distributed Representations of Words and Phrases and their Compositionality"
- **Link:** [https://arxiv.org/abs/1310.4546](https://arxiv.org/abs/1310.4546)
- Why: This is the canonical Word2Vec paper introducing negative sampling and phrase embeddings. It is more readable than the original 2013 ICLR submission and is the paper most courses actually assign. GloVe (Pennington et al., 2014) is the natural companion paper but Word2Vec is the clearer pedagogical starting point.
- Level: intermediate

## Code walkthrough
- **Andrej Karpathy** — "makemore" series, specifically the bigram/MLP episodes where embedding tables are built from scratch
- **Watch:** [YouTube](https://www.youtube.com/watch?v=PaCmpygFfXo)
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

---

## Additional Resources for Tutor Depth

> **17 sources** — papers, official docs, working code, benchmarks, and deep explainers that give the AI tutor precision on this topic.

### 📄 Contextual Embeddings for Lexical Semantic Change (LSC) — Controlled Comparison
**Paper** · [source](https://aclanthology.org/2024.naacl-long.240.pdf)

*Controlled, multi-language comparison of contextual embedding choices + concrete evaluation protocols and reported numbers.*

<details>
<summary>Key content</summary>

- **LSC framework (i–iii)** (Intro/§2): (i) semantic proximity judgments for usage pairs; (ii) induce senses by clustering a Diachronic Word Usage Graph (DWUG); (iii) quantify change from time-specific sense distributions.
- **Embeddings setup** (§3): For each target word, collect contextual embeddings for all usages in two periods:  
  Φ₁ = {a₁…aₙ} (time t₁), Φ₂ = {b₁…bₘ} (time t₂). Default: **no extra fine-tuning**, use **last layer (12th)** embeddings; average subword embeddings when token splits.
- **GCD (Graded Change Detection) metrics**: evaluate by **Spearman correlation** between predicted change scores and gold rankings (§2, §4).
- **Form-based change scores** (§4.1):  
  - **PRT** (Eq.1): PRT(Φ₁,Φ₂)= 1 − cosine(μ₁, μ₂), where μ₁, μ₂ are mean (prototype) embeddings in each period.  
  - **APD** (Eq.2): APD(Φ₁,Φ₂)= (1/(|Φ₁||Φ₂|)) Σ_{a∈Φ₁,b∈Φ₂} d(a,b), with d = cosine distance.
- **Sense-based** (§4.2): **AP+JSD** (cluster Φ₁∪Φ₂ with Affinity Propagation; compute JSD between cluster distributions p₁,p₂; Eq.3). **WiDiD**: cluster Φ₁ and Φ₂ separately with APP; compute **APDP = APD(Ψ₁,Ψ₂)** over sense prototypes (Eq.4; uses **Canberra distance** per footnote).
- **Key empirical results (Table 1/2)**:  
  - Best overall GCD: **XL-LEXEME + APD weighted avg Spearman = .751** (8 languages). Leaderboard: **APD > PRT > WiDiD > AP+JSD**.  
  - Computational annotators (Table 2): WiC avg Spearman **BERT .358, mBERT .301, XLM-R .272, XL-LEXEME .568**; EN WiC: **XL-LEXEME .626 vs GPT-4 .606**, human agreement (Krippendorff α) **.633**.  
  - GCD as annotators avg Spearman: **BERT .422, mBERT .357, XLM-R .324, XL-LEXEME .754**; EN GCD: **XL-LEXEME .801, GPT-4 .818**.
- **Layer choice finding** (§4.3): earlier/middle layers often better; best results typically **layers 8–10**; **no consistent gain** from aggregating last 4 layers.

</details>

### 📄 Deep contextualized word representations (ELMo)
**Paper** · [source](https://aclanthology.org/N18-1202.pdf)

*Concrete contextual-vs-static embedding definition via biLM token embeddings + six-task benchmark gains*

<details>
<summary>Key content</summary>

- **Contextual vs. static:** Traditional word *type* embeddings (e.g., GloVe/word2vec) give **one context-independent vector per word**. ELMo assigns **each token** a vector **as a function of the entire sentence** (Sec. 1, 3).
- **biLM objective (Sec. 3.1):** For tokens \((t_1,\dots,t_N)\)  
  Forward LM: \(p(t_{1:N})=\prod_{k=1}^N p(t_k\mid t_{1:k-1})\)  
  Backward LM: \(p(t_{1:N})=\prod_{k=1}^N p(t_k\mid t_{k+1:N})\)  
  Joint training maximizes \(\sum_{k=1}^N [\log p(t_k\mid t_{1:k-1})+\log p(t_k\mid t_{k+1:N})]\), tying token-repr params \(\Theta_x\) and softmax \(\Theta_s\) across directions.
- **ELMo layer mixing (Eq. 1, Sec. 3.2):** For token \(k\), representations  
  \(R_k=\{h^{LM}_{k,j}\mid j=0..L\}\), where \(h^{LM}_{k,0}=x^{LM}_k\) (token layer) and \(h^{LM}_{k,j}=[\overrightarrow{h}^{LM}_{k,j};\overleftarrow{h}^{LM}_{k,j}]\).  
  Task vector: \(\mathrm{ELMo}^{task}_k=\gamma^{task}\sum_{j=0}^L s^{task}_j\, h^{LM}_{k,j}\), with \(s^{task}\) softmax-normalized; \(\gamma\) is a learned scalar.
- **Pipeline (Sec. 3.3):** Pretrain biLM → **freeze** biLM weights → concatenate \([x_k;\mathrm{ELMo}_k]\) into supervised model input; sometimes also concatenate at RNN output \([h_k;\mathrm{ELMo}_k]\). Use dropout on ELMo; optional L2 regularization on layer weights toward uniform average.
- **biLM architecture/defaults (Sec. 3.4):** \(L=2\) biLSTM layers; **4096** units with **512-d** projections; residual connection between layers. Character CNN: **2048** char n-gram filters → 2 highway layers → project to **512**. Trained **10 epochs** on **1B Word Benchmark (~30M sentences)**; avg forward/backward perplexity **39.7**.
- **Six-task gains (Table 1):**  
  - **SQuAD F1:** 81.1 → **85.8** (+4.7; **24.9%** rel. error reduction)  
  - **SNLI acc:** 88.0 → **88.7** (+0.7; 5.8%)  
  - **SRL F1:** 81.4 → **84.6** (+3.2; 17.2%)  
  - **Coref avg F1:** 67.2 → **70.4** (+3.2; 9.8%)  
  - **NER F1:** 90.15 → **92.22** (+2.06; 21%)  
  - **SST-5 acc:** 51.4 → **54.7** (+3.3; 6.8%)
- **Ablations (Tables 2,7):** Using **all layers** > last-only (e.g., SQuAD dev: baseline 80.8; last-only 84.7; all layers up to **85.2** with \(\lambda=0.001\)). Gains mainly from **contextual** layers, not just char/subword token layer (SQuAD dev: GloVe 80.8 vs char-only 81.4 vs full ELMo 85.6 with GloVe).

</details>

### 📄 Dense Passage Retrieval (DPR) objective + in-batch negatives
**Paper** · [source](https://aclanthology.org/2020.emnlp-main.550.pdf)

*Exact DPR bi-encoder scoring + softmax objective with in-batch negatives; batching/hard-negative details + key retrieval/QA numbers*

<details>
<summary>Key content</summary>

- **Bi-encoder scoring (Eq. 1, Sec. 3.1):**  
  - Question encoder \(E_Q(\cdot)\), passage encoder \(E_P(\cdot)\) (two independent BERT-base uncased); use \([CLS]\) vector, \(d=768\).  
  - Similarity: \(\mathrm{sim}(q,p)=E_Q(q)^\top E_P(p)\) (dot product / MIPS-friendly).
- **Training objective (Eq. 2, Sec. 3.2):** for instance \(\langle q_i, p_i^+, p_{i,1}^-,\dots,p_{i,n}^-\rangle\)  
  \[
  \mathcal{L}=-\log \frac{e^{\mathrm{sim}(q_i,p_i^+)}}{e^{\mathrm{sim}(q_i,p_i^+)}+\sum_{j=1}^n e^{\mathrm{sim}(q_i,p_{i,j}^-)}}
  \]
- **In-batch negatives (Sec. 3.2):** batch size \(B\). Let \(Q,P\in\mathbb{R}^{B\times d}\); similarity matrix \(S=QP^\top\in\mathbb{R}^{B\times B}\). For question \(i\), passage \(j=i\) is positive; all \(j\neq i\) are negatives ⇒ \(B-1\) negatives per question; effectively trains on \(B^2\) pairs/batch.
- **Negative types (Sec. 3.2/5.2):** Random; **BM25 hard negatives** (high BM25 but no answer string); **Gold** (positives from other questions). **Best:** in-batch gold negatives + **1 BM25 hard negative per question** (adding 2 didn’t help).
- **Corpus/chunking (Sec. 4.1):** Wikipedia Dec 20, 2018; DrQA cleaning; split into **disjoint 100-word passages**; prepend title + \([SEP]\); **21,015,324 passages**.
- **Key retrieval results (Table 2):** Top-20 accuracy (% answer-containing)  
  - **NQ:** DPR 78.4 vs BM25 59.1  
  - **TriviaQA:** 79.4 vs 66.9  
  - **WQ:** 73.2 vs 55.0  
  - **TREC:** 79.8 vs 70.9
- **Key end-to-end QA EM (Table 4, Single):**  
  - **NQ:** DPR 41.5 vs BM25 32.6; ORQA 33.3  
  - **TriviaQA:** DPR 56.8 vs BM25 52.4
- **Efficiency (Sec. 5.4):** FAISS (CPU HNSW) retrieves top-100 at **995 Q/s**; BM25/Lucene **23.7 Q/s per CPU thread**. FAISS index build on 21M vectors: **8.5h**; embedding compute: **8.8h on 8 GPUs**. HNSW params: neighbors/node=512, construction ef=200, search ef=128.

</details>

### 📄 GPT-3 Few-/One-/Zero-shot In-Context Learning (NeurIPS 2020 record)
**Paper** · [source](https://proceedings.neurips.cc/paper/2020/hash/6b493230205f780e1bc26945df7481e5-Abstract.html)

*NeurIPS 2020 canonical publication record (as captured here) for GPT-3-style in-context learning settings, evaluation defaults, and scaling setup.*

<details>
<summary>Key content</summary>

- **Model scale & setting (Section 2):**
  - GPT-3 is a **175B-parameter** autoregressive Transformer (same architecture family as GPT-2), evaluated primarily in **few-shot** settings **without gradient updates / fine-tuning**.
- **In-context learning modes (Section 2 “Approach”):**
  - **Fine-Tuning (FT):** update weights using thousands of labeled examples per task.
  - **Few-Shot (FS):** provide **K demonstrations** in the prompt; **no weight updates**.
  - **One-Shot (1S):** FS with **K = 1**.
  - **Zero-Shot (0S):** provide **natural-language task description** (no examples).
  - **Typical K range:** **10–100**, constrained by context window **nctx = 2048 tokens**.
- **Evaluation procedure defaults (Section 2.4):**
  - For each evaluation example, **randomly draw K training examples** as prompt conditioning; delimiter is **1–2 newlines** depending on task.
  - For free-form generation tasks: **beam search** with **beam width = 4** and **length penalty α = 0.6**.
  - Example: on **SuperGLUE**, few-shot uses **32 examples** for all tasks.
- **Training data pipeline (Section 2.2):**
  1) Filter CommonCrawl by similarity to high-quality corpora  
  2) **Fuzzy deduplicate at document level** (within/across datasets)  
  3) Mix in curated corpora (e.g., WebText-like, Books, Wikipedia).

</details>

### 📄 LinkedIn Talent Search/RecSys Production Architecture (SIGIR’18)
**Paper** · [source](https://engineering.linkedin.com/content/dam/me/engineering/li-en/research/SIGIR-2018.pdf)

*End-to-end production retrieval/ranking architecture + operational constraints/trade-offs (multi-pass ranking, logging, offline training, near-real-time index updates)*

<details>
<summary>Key content</summary>

- **Problem setting (scale + query complexity):** Rank “most relevant candidates in real-time among **hundreds of millions** of structured member profiles.” Queries can combine **structured facets** (canonical title(s), canonical skill(s), company name, region) + **unstructured free-text keywords**.
- **Two-sided objective / metrics rationale:** Talent search requires **mutual interest**: not only candidate relevance to recruiter query, but also candidate interest in the opportunity. Example optimization/AB metrics mentioned: likelihood of **receiving an InMail** and **responding positively**; “ideal” metrics like job offer/accept may be **unavailable or delayed**.
- **Online serving architecture (Figure 1):**
  - Input: recruiter request (explicit query or implicit via **job opening / ideal candidate(s)**) + recruiter/session context.
  - Transform into complex query; issue to LinkedIn **Galene** search engine.
  - **Retrieve candidate set** from search index.
  - **Multi-pass ranking** with ML scoring models “of varying complexity.”
  - Return top-ranked candidates to frontend; **log recruiter interactions**.
  - Search index updated in **near real-time** as member data changes.
- **Offline modeling pipeline (Figure 2):**
  - Periodically train ranking models using **recruiter usage logs**.
  - Training labels from recruiter interactions + candidate responses to messages.
  - **Log computed features at serving time** along with shown results (instead of recomputing later) because member data changes over time.
  - Pipeline designed for **feature engineering ease**, supporting different model types, and **experimentation agility**.
- **No equations/hyperparameters/numeric benchmarks** provided in this 2-page paper.

</details>

### 📄 MetaRAG (Metamorphic Testing) for RAG Hallucination Detection
**Paper** · [source](https://arxiv.org/html/2509.09360v1)

*Deployment-oriented, black-box pipeline to detect *extrinsic* hallucinations in RAG via factoid mutations + context verification + scoring; includes operational safeguards.*

<details>
<summary>Key content</summary>

- **Problem framing (Intro):** RAG reduces *intrinsic* hallucinations but still suffers *extrinsic* hallucinations when outputs conflict with/ignore retrieved context.
- **MetaRAG constraints:** real-time, **unsupervised**, **reference-free**, **black-box** (no gold answers, no model internals).
- **4-stage pipeline (Section 3):**
  1) **Factoid decomposition:** split answer \(A\) into atomic, independently verifiable factoids \(\{f_i\}\). Extractor prompt enforces: one proposition/line, no paraphrase/inference beyond \(A\), includes coreference resolution.  
  2) **Mutation generation:** for each factoid \(f_i\), generate \(k\) **synonym** variants \(s_{ij}\) (meaning-preserving) and \(k\) **antonym/negation** variants \(a_{ij}\) (meaning-opposed). Expectation: if \(f_i\) is supported by retrieved context \(C\), then \(s_{ij}\) should be **entailed** by \(C\) and \(a_{ij}\) **contradicted** by \(C\).  
  3) **Verification:** LLM verifier conditioned on \(C\) outputs \(\in\{\text{Yes (entailed)},\text{No (contradicted)},\text{Not sure}\}\). **Penalty table:**  
     - Synonym: Yes 0.0, Not sure 0.5, No 1.0  
     - Antonym: Yes 1.0, Not sure 0.5, No 0.0  
  4) **Scoring:** **Factoid score (Eq. 1)**  
     \[
     h(f_i)=\frac{1}{2k}\sum_{j=1}^{k}\big(p(s_{ij})+p(a_{ij})\big)
     \]
     **Response score (Eq. 2):**  
     \[
     H(A)=\max_i h(f_i)
     \]
     Flag if \(H(A)>\tau\) (example threshold \(\tau=0.5\)).
- **Empirical setup (Section 4):** 23 proprietary enterprise docs; chunked “few hundred tokens”; retrieval: cosine similarity over **text-embedding-3-large**, top-\(k\) chunks appended. Eval set: **67** responses (36 non-hallucinated, 31 hallucinated). Binary classification by thresholding \(H(A)\) at \(\tau\).
- **Key results (Table 2 / Section 5):** Best F1 config **ID 5** (mini/41/multi/2/0): **F1 0.9391, Precision 1.0000, Recall 0.8853, Acc 0.9401**. Other strong: **ID 18** (mini/mini/41/5/0.7): F1 0.9372, Prec 0.9087, Rec 0.9676, Acc 0.9401; **ID 19** (mini/mini/41/5/0): F1=Prec=Rec **0.9352**, Acc 0.9400.
- **Stability (Section 5.3, 5 seeds):** ID 16 CV(F1) **1.31%**; ID 18 **0.95%**; ID 19 **3.26%**; ID 5 **3.80%**.
- **Deployment safeguards (Section 3.6):** topic tagging (no protected-attribute inference) → **topic-aware thresholds** (stricter for sensitive domains), **span highlighting + forced citations**, **abstain/regenerate/escalate**, and **auditing logs** (scores + spans + topic labels).

</details>

### 📄 RAG marginalization + DPR MIPS retrieval
**Paper** · [source](https://proceedings.neurips.cc/paper/2020/file/6b493230205f780e1bc26945df7481e5-Paper.pdf)

*RAG-Sequence / RAG-Token marginalization over retrieved docs; DPR retriever scoring as MIPS over dense embeddings*

<details>
<summary>Key content</summary>

- **Setup (Sec. 2):** Input sequence \(x\), retrieved passages \(z\), output sequence \(y=(y_1,\dots,y_N)\). Retriever \(p_\eta(z\mid x)\); generator \(p_\theta(y_i\mid x,z,y_{1:i-1})\) (BART).
- **RAG-Sequence (Sec. 2.1, Eq. “RAG-Sequence”):** same document for whole output; top-\(K\) approximation  
  \[
  p_{\text{RAG-Seq}}(y\mid x)\approx \sum_{z\in \text{top-}K(p(\cdot\mid x))} p_\eta(z\mid x)\,p_\theta(y\mid x,z)
  =\sum_{z} p_\eta(z\mid x)\prod_{i=1}^N p_\theta(y_i\mid x,z,y_{1:i-1})
  \]
- **RAG-Token (Sec. 2.1, Eq. “RAG-Token”):** latent doc per token  
  \[
  p_{\text{RAG-Tok}}(y\mid x)\approx \prod_{i=1}^N \sum_{z\in \text{top-}K} p_\eta(z\mid x)\,p_\theta(y_i\mid x,z,y_{1:i-1})
  \]
- **Retriever = DPR bi-encoder (Sec. 2.2):**  
  \(d(z)=\text{BERT}_d(z)\), \(q(x)=\text{BERT}_q(x)\),  
  \[
  p_\eta(z\mid x)\propto \exp(d(z)^\top q(x))
  \]
  Top-\(K\) retrieval is **Maximum Inner Product Search (MIPS)**; approximated with FAISS (HNSW).
- **Generator (Sec. 2.3):** BART-large (~400M params); **concatenate** \(x\) and \(z\) as encoder input.
- **Training (Sec. 2.4):** minimize \(-\log p(y_j\mid x_j)\) end-to-end; **keep document encoder/index fixed**, fine-tune query encoder + generator.
- **Defaults (Sec. 3):** Wikipedia Dec 2018; split articles into **disjoint 100-word chunks** → **21M** passages; train with \(k\in\{5,10\}\).
- **Key results (Table 1):** Open-domain QA EM: NQ **44.5** (RAG-Seq) vs DPR 41.5; WQ **45.5** (RAG-Tok) vs DPR 41.1; CT **52.2** (RAG-Seq) vs DPR 50.6.  
  (Table 2) FEVER label acc: **72.5/89.5** (RAG-Tok, 3-way/2-way).

</details>

### 📄 SGNS objective + negative sampling derivation (Goldberg & Levy 2014)
**Paper** · [source](https://arxiv.org/pdf/1402.3722.pdf)

*Explicit derivation of Skip-gram with Negative Sampling (SGNS) objective; assumptions about word/context vectors; negative-sampling distribution details.*

<details>
<summary>Key content</summary>

- **Skip-gram MLE objective (Eq. 1–2):** maximize corpus likelihood of contexts given words  
  \[
  \arg\max_\theta \prod_{w\in Text}\prod_{c\in C(w)} p(c\mid w;\theta)
  \equiv \arg\max_\theta \prod_{(w,c)\in D} p(c\mid w;\theta)
  \]
  where \(D\) is extracted word–context pairs; \(C(w)\) contexts of \(w\).
- **Softmax parameterization (Eq. 3):**  
  \[
  p(c\mid w;\theta)=\frac{e^{v_c\cdot v_w}}{\sum_{c'\in C} e^{v_{c'}\cdot v_w}}
  \]
  with embeddings \(v_w, v_c\in\mathbb{R}^d\); \(C\)=all contexts.
- **Log objective (Eq. 4):**  
  \[
  \sum_{(w,c)\in D}\left(v_c\cdot v_w-\log\sum_{c'} e^{v_{c'}\cdot v_w}\right)
  \]
  Computational bottleneck: sum over all contexts \(c'\).
- **Negative sampling as binary classification (Section 2):** define  
  \[
  p(D{=}1\mid w,c;\theta)=\sigma(v_c\cdot v_w)=\frac{1}{1+e^{-v_c\cdot v_w}}
  \]
  Add negative pairs \(D'\) to avoid trivial solution (all dot-products large; \(K\approx 40\) yields near-1 probability).
- **SGNS objective (Section 2):**  
  \[
  \arg\max_\theta \sum_{(w,c)\in D}\log\sigma(v_c\cdot v_w)+\sum_{(w,c)\in D'}\log\sigma(-v_c\cdot v_w)
  \]
- **How \(D'\) is constructed (k-negative sampling):** for each positive \((w,c)\in D\), sample \(k\) negatives \((w,c_j)\) with \(c_j\) drawn from unigram\(^ {3/4}\). Equivalent sampling:  
  \[
  (w,c)\sim \frac{p_{\text{words}}(w)\,p_{\text{contexts}}(c)^{3/4}}{Z}
  \]
  In word2vec, contexts are words so \(p_{\text{context}}(x)=p_{\text{words}}(x)=\frac{\text{count}(x)}{|Text|}\).
- **Design rationale:** use **separate vocabularies/vectors** for words vs contexts (footnote): if shared, model would need low \(p(dog\mid dog)\) though \(v\cdot v\) can’t be low.

</details>

### 📄 Word2Vec Skip-gram—NEG, Hierarchical Softmax, Subsampling, Phrases
**Paper** · [source](https://proceedings.neurips.cc/paper_files/paper/2013/file/9aa42b31882ec039965f3c4923ce901b-Paper.pdf)

*Original negative sampling objective, hierarchical softmax setup, subsampling frequent words, plus phrase extension + key training details.*

<details>
<summary>Key content</summary>

- **Skip-gram objective (Eq. 1):** maximize  
  \[
  \frac{1}{T}\sum_{t=1}^{T}\sum_{-c\le j\le c, j\ne 0}\log p(w_{t+j}\mid w_t)
  \]
  where \(c\)=context window size, \(T\)=#tokens.
- **Softmax (Eq. 2):**  
  \[
  p(w_O\mid w_I)=\frac{\exp({v'_{w_O}}^\top v_{w_I})}{\sum_{w=1}^{W}\exp({v'_w}^\top v_{w_I})}
  \]
  \(v_w\)=“input” vector, \(v'_w\)=“output” vector, \(W\)=vocab size.
- **Hierarchical softmax (Sec. 2.1, Eq. 3):** binary tree; probability is product along path nodes \(n(w,j)\):  
  \[
  p(w\mid w_I)=\prod_{j=1}^{L(w)-1}\sigma\Big(\big[\![n(w,j+1)=ch(n(w,j))]\!\big]\cdot {v'_{n(w,j)}}^\top v_{w_I}\Big)
  \]
  Uses **Huffman tree** so frequent words have short codes ⇒ faster training (~\(\log W\) nodes).
- **Negative sampling objective (Sec. 2.2, Eq. 4):** replace each \(\log p(w_O\mid w_I)\) with  
  \[
  \log\sigma({v'_{w_O}}^\top v_{w_I})+\sum_{i=1}^{k}\mathbb{E}_{w_i\sim P_n(w)}[\log\sigma(-{v'_{w_i}}^\top v_{w_I})]
  \]
  Typical \(k\): **5–20** (small data), **2–5** (large data). Noise \(P_n(w)\): unigram\(^{3/4}\) (i.e., \(U(w)^{3/4}/Z\)) beats unigram/uniform.
- **Subsampling frequent words (Sec. 2.3, Eq. 5):** discard token \(w_i\) with  
  \[
  P(w_i)=1-\sqrt{\frac{t}{f(w_i)}}
  \]
  \(f(w_i)\)=frequency; \(t\approx 10^{-5}\). Gives **2×–10× speedup** and improves rare-word vectors.
- **Empirical (Sec. 3, Table 1; 1B words, vocab 692K, min count 5, 300d):**  
  - No subsampling: **NEG-5 total 59% (38 min)**; **NEG-15 total 61% (97 min)**; **HS-Huffman total 47% (41 min)**.  
  - With \(10^{-5}\) subsampling: **NEG-5 total 60% (14 min)**; **NEG-15 total 61% (36 min)**; **HS-Huffman total 55% (21 min)**.
- **Phrase learning (Sec. 4, Eq. 6):** form bigram phrases via  
  \[
  score(w_i,w_j)=\frac{count(w_iw_j)-\delta}{count(w_i)\,count(w_j)}
  \]
  Keep bigrams above threshold; run **2–4 passes** with decreasing threshold to build longer phrases; then treat phrases as single tokens in training.
- **Phrase results (Table 3; 1B words, 300d, window 5):** accuracy no subsampling vs \(10^{-5}\): **NEG-15: 27%→42%**; **HS-Huffman: 19%→47%**. Best phrase model reported: **HS**, **1000d**, **full-sentence context**, **33B words** ⇒ **72%** phrase analogy accuracy.

</details>

### 📊 GloVe benchmarks + core objective
**Benchmark** · [source](https://aclanthology.org/D14-1162.pdf)

*Analogy accuracy + word similarity (WS-353 etc.) tables and the hyperparameters used.*

<details>
<summary>Key content</summary>

- **Core co-occurrence setup (Section 3):**  
  - Co-occurrence counts: \(X_{ij}\) = # times context word \(j\) occurs in context of target \(i\).  
  - \(X_i=\sum_k X_{ik}\); \(P_{ij}=P(j|i)=X_{ij}/X_i\).
- **Log-bilinear relation (Eq. 7):**  
  \[
  w_i^\top \tilde w_j + b_i + \tilde b_j = \log(X_{ij})
  \]
  with separate **word vectors** \(w\) and **context vectors** \(\tilde w\), plus biases.
- **Weighted least squares objective (Eq. 8):**  
  \[
  J=\sum_{i,j=1}^V f(X_{ij})\left(w_i^\top \tilde w_j+b_i+\tilde b_j-\log X_{ij}\right)^2
  \]
- **Weighting function (Eq. 9) + defaults:**  
  \[
  f(x)=\begin{cases}(x/x_{\max})^\alpha & x<x_{\max}\\ 1 & \text{otherwise}\end{cases}
  \]
  Defaults used: \(x_{\max}=100\), \(\alpha=3/4\).
- **Training pipeline + defaults (Section 4.2):**  
  - Tokenize+lowercase; vocab = top **400k** words (Common Crawl uses ~2M).  
  - Build \(X\) with **symmetric window 10 left + 10 right**; distance weighting \(1/d\).  
  - Optimize with **AdaGrad**, initial LR **0.05**, sample **nonzero** \(X_{ij}\).  
  - Iterations: **50** if dim < 300; **100** otherwise. Use final vectors **\(W+\tilde W\)**.
- **Analogy benchmark (Table 2, accuracy %):**  
  - **GloVe 300d, 42B tokens:** Sem 81.9 / Syn 69.3 / **Total 75.0** (best overall).  
  - **GloVe 300d, 6B:** Total **71.7** vs **SG† 69.1**, **CBOW† 65.7**.  
  - **GloVe 300d, 1.6B:** Total **70.3**.
- **Word similarity (Table 3, Spearman; 300d):**  
  - **GloVe 6B:** WS353 **65.8** (vs SG† 62.8; CBOW† 57.2).  
  - **GloVe 42B:** WS353 **75.9**, MC **83.6**, RG **82.9**, RW **47.8**.

</details>

### 📊 KILT unified benchmark + provenance-aware evaluation
**Benchmark** · [source](https://aclanthology.org/2021.naacl-main.200.pdf)

*KILT task suite + unified evaluation protocol (downstream + retrieval + provenance-gated “KILT scores”)*

<details>
<summary>Key content</summary>

- **Design rationale (Intro/§2):** Unify **11 datasets / 5 tasks** (fact checking, entity linking, slot filling, open-domain QA, dialogue) under **one Wikipedia snapshot (2019/08/01; 5.9M articles)** to reuse indexing/infra and enable task-agnostic memory architectures; every instance is **in-KB** (answerable from the snapshot).
- **Common instance format (§3):** JSONL with `id`, `input` (string), `output` (list). Each output has **non-empty provenance** = list of Wikipedia **text spans/pages** sufficient to justify the output.
- **Dataset→snapshot mapping procedure (§2):**
  1) Match pages via Wikipedia redirects.  
  2) Locate provenance span by scanning page and selecting span with **max BLEU** vs original provenance (tie→shortest span).  
  3) Replace provenance with matched span; compute BLEU.  
  4) Filter dev/test if any provenance span BLEU < **0.5** (drops ~**18%** dev/test on avg; train kept).
- **Retrieval metrics (Section 5):**
  - **R-Precision:** \( \text{RPrec} = r/R \). \(R\)=#pages in a provenance set; \(r\)=#relevant pages in top-\(R\). Report **max over provenance sets** per example; mean over dataset. (Often \(R=1\Rightarrow\) Precision@1.)
  - **Recall@k:** \( \text{Recall@k} = w/n \). \(n\)=#distinct provenance sets; \(w\)=#complete provenance sets contained in top-\(k\) pages (multi-page sets positioned by lowest-ranked page).
- **Provenance-gated “KILT scores” (Section 5):** Award downstream points **only if RPrec = 1** (complete provenance set ranked at top). Metrics: **KILT-AC/EM/RL/F1**.
- **Key empirical results (Tables 3–5):**
  - **Downstream:** RAG beats BART-only on NQ **EM 44.39 vs 21.75**; TQA **71.27 vs 32.39**; FEVER **86.31 vs 78.93**.
  - **Retrieval (R-Prec):** Multi-task DPR improves DPR on FEVER **74.48 vs 55.33**, NQ **59.42 vs 28.96**, TQA **61.49 vs 44.49**.
  - **KILT scores:** RAG NQ **KILT-EM 32.69**; TQA **38.13**; HotpotQA **3.21** (shows provenance remains hard).

</details>

### 📊 KILT unified evaluation w/ provenance (RAG benchmark)
**Benchmark** · [source](https://discovery.ucl.ac.uk/id/eprint/10129948/1/Rockta%CC%88schel_2021.naacl-main.200.pdf)

*Benchmark tables + unified evaluation protocol tying task scores to retrieval provenance (evidence attribution) with concrete retrieval metrics*

<details>
<summary>Key content</summary>

- **Unification / design rationale (Sec. 1–2):** 11 datasets, 5 tasks (fact checking, entity linking, slot filling, open-domain QA, dialogue) all grounded in **one Wikipedia snapshot (2019/08/01; 5.9M articles)** to reuse indexing/infrastructure and enable task-agnostic memory architectures.
- **Common instance format (Sec. 3):** JSONL with `id`, `input` (string), `output` (list). Each output string has **provenance** = non-empty list of Wikipedia **spans/pages** sufficient to justify the output.
- **Dataset→snapshot mapping procedure (Sec. 2):**
  1) Match pages via Wikipedia redirects.  
  2) Locate provenance span by scanning matched page and selecting span with **max BLEU** vs original provenance (tie→shortest span).  
  3) Replace provenance; compute BLEU.  
  4) Filter dev/test if any provenance span BLEU < **0.5** (avg **18%** removed; train kept).
- **Retrieval metrics (Sec. 5):**
  - **R-precision = r/R**, where **R** = #pages in a provenance set, **r** = #relevant pages in top-R retrieved; report **max over provenance sets** per input. (For most datasets R=1 ⇒ Precision@1.)
  - **Recall@k = w/n**, where **n** = #distinct provenance sets, **w** = #complete provenance sets found in top-k.
- **KILT scores (Sec. 5):** KILT-AC / KILT-EM / KILT-RL / KILT-F1 award downstream points **only if R-precision = 1** (i.e., a complete provenance set is ranked at the top).
- **Key empirical results (Tables 3–5):**
  - **Downstream:** RAG beats BART+DPR on several QA/SF: e.g., **TriviaQA EM 71.27 vs 58.55**; **zsRE EM 44.74 vs 30.43**; **NQ EM 44.39 vs 41.27**.
  - **Retrieval (R-Prec):** Multi-task DPR improves over DPR broadly (e.g., **FEVER 74.48 vs 55.33**; **NQ 59.42 vs 54.29**; **Hotpot 42.92 vs 25.04**).
  - **Grounded (KILT) scores are much lower than downstream:** e.g., **RAG NQ KILT-EM 32.69** (vs EM 44.39); **RAG Hotpot KILT-EM 3.21** (vs EM 26.97).

</details>

### 📖 Gensim Word2Vec API essentials (params + train/save/load)
**Reference Doc** · [source](https://radimrehurek.com/gensim/models/word2vec.html)

*Authoritative parameter meanings/defaults for `gensim.models.Word2Vec`, plus training + persistence workflows.*

<details>
<summary>Key content</summary>

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

</details>

### 📖 GloVe (Stanford) — official training pipeline + rationale
**Reference Doc** · [source](https://nlp.stanford.edu/projects/glove/)

*Reference implementation workflow: build global co-occurrence stats, then train GloVe vectors; plus what the objective is trying to match.*

<details>
<summary>Key content</summary>

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

</details>

### 📖 Milvus HNSW index params (M, efConstruction, ef) + metrics
**Reference Doc** · [source](https://milvus.io/docs/hnsw.md)

*Milvus HNSW index/search parameter specs and supported distance metrics for float vectors*

<details>
<summary>Key content</summary>

- **What HNSW is (design rationale):** Graph-based ANN index for **high-dimensional floating vectors**; delivers **excellent accuracy + low latency** but has **high memory overhead** due to hierarchical graph structure.
- **Algorithm workflow (overview):**
  - Multi-layer graph: **bottom layer = all points**, upper layers = **subsampled** points.
  - **Search procedure:** start at **fixed entry point** (top layer) → **greedy** move to closest neighbor until local minimum → **descend** a layer via established connection → repeat → **bottom-layer refinement** returns nearest neighbors.
- **Supported similarity metrics (index build):** `COSINE`, `L2`, `IP`.
- **Index build API (PyMilvus):**
  - Use `MilvusClient.prepare_index_params()` then `index_params.add_index(field_name, index_type="HNSW", index_name, metric_type, params={...})`.
  - Build params:
    - **M** = max connections/edges per node (includes outgoing + incoming).
    - **efConstruction** = candidate neighbors considered during construction.
- **Search API:**
  - `search_params = {"params": {"ef": <int>}}`
  - `MilvusClient.search(collection_name, anns_field, data=[query_vector], limit=K, search_params=search_params)`
  - **ef** = number of neighbors/nodes evaluated during search (bottom layer).
- **Parameter specs (with defaults/ranges + tuning):**
  - **M:** int **[2, 2048]**, default **30** (up to 30 outgoing + 30 incoming). Recommended **[5, 100]**. Higher M → higher recall/accuracy, more memory, slower build/search.
  - **efConstruction:** int **[1, int_max]**, default **360**. Recommended **[50, 500]**. Higher → better graph/accuracy, slower build, more memory during construction.
  - **ef (search):** int **[1, int_max]**, default **limit (TopK)**. Recommended **[K, 10K]**. Higher → higher recall, slower search.

</details>

### 📖 Milvus IVF_FLAT (and IVF knobs) quick reference
**Reference Doc** · [source](https://milvus.io/docs/ivf.md)

*Exact IVF parameters (`nlist`, `nprobe`), build/search tradeoffs, supported metrics*

<details>
<summary>Key content</summary>

- **IVF concept (procedure):** Partition vectors into `nlist` clusters (centroids). **Search**: (1) compute distance from query to **all centroids**, (2) pick `nprobe` nearest clusters, (3) scan vectors in those clusters to produce `topK`. IVF_FLAT stores **raw vectors** in lists (no compression).
- **Build params (IVF_FLAT):**  
  - `index_type: "IVF_FLAT"`  
  - `metric_type`: `"L2"` or `"IP"`  
  - `nlist`: number of clusters, **int 1–65536**.
- **Search params (IVF_FLAT):**  
  - `nprobe`: clusters probed, **int 1–nlist (CPU)**; **1–min(2048, nlist) (GPU)**.  
  - Tradeoff: higher `nprobe` ⇒ higher recall, slower search (more candidates scanned).
- **Binary IVF variant:** `BIN_IVF_FLAT` supports `metric_type` ∈ {`jaccard`, `hamming`, `tanimoto`}; same `nlist` (1–65536) and `nprobe` bounds as above.
- **Index anatomy (design rationale):** data structure (e.g., IVF) + optional **quantization** (SQ8/PQ) + optional **refiner**. Query retrieves `topK × expansion_rate` candidates then refines distances on that subset.
- **Empirical guidance (selection):**
  - Graph indexes usually higher **QPS** than IVF; **IVF fits large `topK`** (e.g., **> 2,000**).
  - If **filter ratio** < **85%** ⇒ graph-based better; **85–95%** ⇒ IVF; **>98%** ⇒ **FLAT**.
  - Scenario table: **Large k (≥1% of dataset)** ⇒ IVF; **High filter ratio (>95%)** ⇒ FLAT.
- **Memory example (1M vectors, dim=128, nlist=2000):** totals: **IVF-PQ (no refine) 11.0 MB**; **IVF-PQ + 10% raw refine 62.2 MB**; **IVF-SQ8 131.0 MB**; **IVF-FLAT 515.0 MB**.

</details>

### 📖 word2vec (original C impl) — training choices & usage
**Reference Doc** · [source](https://code.google.com/archive/p/word2vec/)

*Authoritative description of CBOW vs Skip-gram, training pipeline, and recommended hyperparameter ranges; demo tools (distance/analogy/accuracy/phrases/classes).*

<details>
<summary>Key content</summary>

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

</details>

---

## Related Topics

- [[topics/neural-networks|Neural Networks]]
- [[topics/tokenization|Tokenization]]
- [[topics/pre-training|Pre-Training]]
- [[topics/contrastive-learning|Contrastive Learning]]
