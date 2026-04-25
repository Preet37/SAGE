---
title: "RAG & Retrieval"
subject: "Retrieval & Knowledge"
date: 2025-01-01
tags:
  - "subject/retrieval-and-knowledge"
  - "level/beginner"
  - "level/intermediate"
  - "level/advanced"
  - "educator/andrej-karpathy"
  - "educator/lilian-weng"
  - "resource/video"
  - "resource/blog"
  - "resource/deep-dive"
  - "resource/paper"
  - "resource/code"
educators:
  - "Andrej Karpathy"
  - "Lilian Weng"
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

# RAG Retrieval

## Video (best)
- **Andrej Karpathy** — "Intro to Large Language Models"
- **Watch:** [YouTube](https://www.youtube.com/watch?v=zjkBMFhNj_g)
- Why: While a broad LLM intro, Karpathy dedicates meaningful time to retrieval augmentation, grounding the concept in how LLMs access external knowledge. His intuition-first style makes the "why" of RAG retrieval viscerally clear before any implementation details. Best available from a trusted educator that directly addresses retrieval in context.
- Level: beginner/intermediate

## Blog / Written explainer (best)
- **Lilian Weng** — "Retrieval-Augmented Generation for Large Language Models"
- url: https://lilianweng.github.io/posts/2023-06-23-agent/ [NOT FOUND — see note]
- Why: Weng's writing is the gold standard for systematic, well-cited ML concept breakdowns. She covers chunking strategies, embedding retrieval, reranking, and evaluation in a single coherent narrative with mathematical grounding.
- Level: intermediate/advanced

> ⚠️ **VERIFY note:** Weng's dedicated RAG post URL is uncertain. A confirmed alternative is:
> - **Pinecone / James Briggs** — "Retrieval Augmented Generation"
> - url: https://www.pinecone.io/learn/retrieval-augmented-generation/

## Deep dive
- **Author** — "Building RAG-based LLM Applications for Production" (Anyscale)
- **Link:** [https://www.anyscale.com/blog/a-comprehensive-guide-for-building-rag-based-llm-applications-part-1](https://www.anyscale.com/blog/a-comprehensive-guide-for-building-rag-based-llm-applications-part-1)
- Why: One of the most thorough production-oriented treatments of RAG retrieval, covering chunking strategies, embedding model selection, vector database tradeoffs, cosine similarity vs. other metrics, hybrid retrieval, and reranking — all the related concepts in this topic cluster. Written for practitioners who need to make real architectural decisions.
- Level: advanced

## Original paper
- **Lewis et al. (2020)** — "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks"
- **Link:** [https://arxiv.org/abs/2005.11401](https://arxiv.org/abs/2005.11401)
- Why: The foundational paper that named and formalized RAG as a paradigm. Readable relative to its impact — the architecture diagram alone is widely taught. Directly maps to the retrieval component: how dense passage retrieval (DPR) is used as the retrieval backbone, and how retrieved documents are fused into generation. Essential primary source.
- Level: advanced

## Code walkthrough
- **LangChain / LlamaIndex community** — "RAG from Scratch" series by LangChain
- **Link:** [https://www.youtube.com/watch?v=sVcwVQRHIc8](https://www.youtube.com/watch?v=sVcwVQRHIc8)
- Why: The "RAG from Scratch" series builds retrieval pipelines incrementally — starting with naive chunking + cosine similarity retrieval, then adding reranking, hybrid search, and multi-modal extensions. Directly exercises all related concepts (vector database, chunking, cosine similarity) in runnable notebooks.
- Level: intermediate

> ✅ **Confirmed alternative:** LangChain's RAG tutorials on GitHub are well-documented at:
> https://github.com/langchain-ai/rag-from-scratch

---

## Coverage notes
- **Strong:** Core RAG retrieval mechanics (chunking, embedding, cosine similarity, vector databases) are well-covered across blogs and the original Lewis et al. paper. The LangChain ecosystem provides strong code coverage.
- **Weak:** **ColPali** and **visual document retrieval** (cross-modal retrieval, OCR-free document understanding, DocVQA) are significantly underserved in high-quality pedagogical resources. Most existing content treats retrieval as text-only.
- **Gap:** No single excellent video exists that covers **multi-modal RAG retrieval** (ColPali, cross-modal retrieval, visual document understanding) from a trusted educator like those in the preferred list. This is a genuine coverage gap — the topic is too recent (ColPali paper: 2024) for the established educator ecosystem to have caught up. No video identified with confidence.
- **Gap:** **Structured data extraction** as part of retrieval (e.g., retrieving from tables, PDFs with complex layouts) lacks a canonical explainer resource. Document AI and DocVQA are covered in research papers but not in accessible tutorials from preferred authors.

---

## Cross-validation
This topic appears in 3 courses: **intro-to-agentic-ai**, **intro-to-llms**, **intro-to-multimodal**

- `intro-to-llms`: Core RAG retrieval (Lewis et al. paper, chunking, cosine similarity, vector DB) is the primary need — well-resourced.
- `intro-to-agentic-ai`: Retrieval as a tool-use pattern for agents — partially covered by existing resources but the agentic framing (retrieval as an action in a loop) is underserved.
- `intro-to-multimodal`: ColPali, cross-modal retrieval, visual document retrieval — **most poorly resourced** of the three. Instructors should expect to create original content or rely on the ColPali paper directly (arxiv.org/abs/2407.01449).

---

---

## Additional Resources for Tutor Depth

> **11 sources** — papers, official docs, working code, benchmarks, and deep explainers that give the AI tutor precision on this topic.

### 📄 ColBERT late interaction (MaxSim) + 2-stage retrieval
**Paper** · [source](https://arxiv.org/abs/2004.12832)

*Late-interaction scoring (MaxSim over token embeddings) and two-stage pipeline (offline doc encoding + online query encoding + MaxSim aggregation)*

<details>
<summary>Key content</summary>

- **Core idea (late interaction, §3.1):** encode query and document *independently* with BERT into **bags of contextualized token embeddings**, then score with a cheap interaction.
- **Representations:**  
  - Query encoder \(f_Q\) outputs \(E_q=\{ \mathbf{e}_{q_i}\}_{i=1}^{|E_q|}\)  
  - Doc encoder \(f_D\) outputs \(E_d=\{ \mathbf{e}_{d_j}\}_{j=1}^{|E_d|}\)  
  Each embedding is contextualized by other tokens *within* its sequence.
- **Scoring (Late Interaction / MaxSim, Eq. 3, §3.3):**  
  \[
  S_{q,d} := \sum_{i \in [|E_q|]} \max_{j \in [|E_d|]} \mathbf{e}_{q_i}\cdot \mathbf{e}_{d_j}^{\top}
  \]
  Dot-product implements **cosine similarity** due to embedding normalization; paper also evaluates **squared L2** as similarity.
- **Design rationale:** preserves fine-grained token matching (like interaction models) while enabling **offline document encoding** (like representation models) → large speedups and supports **pruning-friendly top‑k retrieval** via vector indexes.
- **Encoders & key choices (§3.2):**
  - Add special markers **[Q]** and **[D]** to distinguish query vs doc inputs.
  - **Query augmentation:** pad/truncate query to length \(N_q\) using **[MASK]** tokens; intended as soft differentiable query expansion / reweighting; reported as **essential** for effectiveness (§4.4).
  - Linear projection (no activation) to **m-dimensional** embeddings (typically \(m \ll\) BERT hidden size).
  - Document encoder filters out **punctuation embeddings** to reduce per-doc vectors.
- **Training (§3.3):** end-to-end differentiable; fine-tune BERT + train linear layer and [Q]/[D] embeddings with **Adam**; optimize **pairwise softmax cross-entropy** on triples \(\langle q,d^+,d^-\rangle\).
- **Retrieval workflows:**
  - **Re-ranking (§3.5):** precompute doc embeddings; at query time encode query once, then compute MaxSim scores over candidate docs.
  - **End-to-end retrieval (§3.6):** issue \(N_q\) vector-similarity searches (one per query embedding) to a **FAISS** index; retrieve top-\(k'\) per embedding, aggregate candidates, then apply full MaxSim scoring.
- **Empirical headline numbers (abstract/intro):**
  - Competitive with BERT rankers while **~2 orders-of-magnitude faster**; **up to 4 orders-of-magnitude fewer FLOPs/query**.
  - As re-ranker: **>170× speedup** and **~14,000× fewer FLOPs** vs existing BERT-based models.
  - Indexing practicality: **MS MARCO 9M passages indexed in ~3 hours** on **1 server with 4 GPUs**; footprint “few tens of GiBs” (with compression options discussed in §4.5/§3.6).

</details>

### 📄 ColBERTv2 (late interaction + compression + denoised supervision)
**Paper** · [source](https://aclanthology.org/2022.naacl-main.272/)

*Concrete improvements over ColBERT: (i) residual compression to cut index size, (ii) denoised supervision to improve training signal; effectiveness/efficiency tradeoffs with ablations.*

<details>
<summary>Key content</summary>

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

</details>

### 📄 ColPali — OCR-free visual document retrieval via late interaction
**Paper** · [source](https://arxiv.org/abs/2407.01449)

*Cross-modal late-interaction retrieval for visually rich documents (page-image multi-vector embeddings + token/patch matching) as a simpler alternative to brittle OCR-heavy RAG ingestion.*

<details>
<summary>Key content</summary>

- **Problem framing (Sec. 2):** Page-level retrieval under industrial constraints: (R1) retrieval quality, (R2) fast online querying latency, (R3) high-throughput offline indexing.
- **Why vision-space retrieval (Intro/Sec. 3):** Standard PDF ingestion is multi-step and brittle: parsing/OCR → layout detection → chunking → optional captioning. Authors find ingestion optimization often matters more than swapping text embedding models for visually rich docs.
- **Late interaction scoring (Eq. 1):** Given query multi-vectors \(E_q=\{q_i\}_{i=1}^{|q|}\) and page multi-vectors \(E_d=\{d_j\}_{j=1}^{|d|}\) in shared space, score  
  \[
  s(q,d)=\sum_{i=1}^{|q|}\max_{j\in[1,|d|]} q_i^\top d_j
  \]
  (sum over query vectors of max dot-product over document vectors).
- **Training loss (Eq. 2):** In-batch contrastive objective over query–page pairs; implemented as softmax cross-entropy reformulated with numerically stable **softplus**; uses in-batch negatives (hard-negative variant discussed).
- **Model/procedure (Sec. 4):** ColPali = PaliGemma-3B adapted to output **ColBERT-style multi-vector embeddings** for both text tokens and image patch tokens; add a **projection layer** to reduced dimension (ColBERT-like) for lightweight storage.
- **Training defaults (Sec. 4.2):** 118,695 query–page pairs; 1 epoch; bf16; **LoRA** on LM transformer layers + projection; paged_adamw_8bit; 8 GPUs; batch size 32; LR \(1\mathrm{e}{-4}\) with linear decay + 2.5% warmup. **Query augmentation:** append 5 `<unused0>` tokens.
- **Key benchmark (Sec. 3):** ViDoRe spans domains/modalities/languages; main metric **nDCG@5** (also Recall@K, MRR).
- **Key empirical result (Table 2):** **ColPali (+Late Inter.) avg nDCG@5 = 81.3**, vs best OCR/captioning pipelines ~**66–67**, and vanilla SigLIP bi-encoder **51.4**. Notable task gains: DocVQA **54.4**, InfoVQA **81.8**, TabFQuAD **83.9**, AI **96.2**, Energy **91.0**, Gov **92.7**, Healthcare **94.4**.
- **Efficiency notes (Sec. 5.2):** Query encoding slower than text encoders (ColPali LM-based), but late-interaction overhead small for small corpora; optimized engines scale to millions. Storage: multi-vector per patch + 6 prompt tokens (“Describe the image”); projected embeddings yield ~**tens of KB/page**; token pooling factor 3 reduces vectors ~**3×** while retaining ~**98%** performance (Shift text-dense outlier).

</details>

### 📄 DPR (Dense Passage Retrieval) objective + bi-encoder training
**Paper** · [source](https://aclanthology.org/2020.emnlp-main.550.pdf)

*Dual-encoder DPR with inner-product scoring; InfoNCE-style NLL with in-batch negatives + hard negatives; key hyperparams + retrieval gains vs BM25.*

<details>
<summary>Key content</summary>

- **Retrieval scoring (Eq. 1, Sec. 3.1):**  
  \[
  \text{sim}(q,p)=E_Q(q)^\top E_P(p)
  \]  
  where \(E_Q(\cdot)\) encodes questions, \(E_P(\cdot)\) encodes passages into \(d\)-dim vectors (BERT-base [CLS], \(d=768\)). Retrieve top-\(k\) passages by maximum inner product search (MIPS); passages pre-encoded + indexed with **FAISS**.
- **Training objective (Eq. 2, Sec. 3.2):** for instance \(\langle q_i,p_i^+,p_{i,1}^-,...,p_{i,n}^-\rangle\)  
  \[
  \mathcal{L}=-\log \frac{e^{\text{sim}(q_i,p_i^+)}}{e^{\text{sim}(q_i,p_i^+)}+\sum_{j=1}^n e^{\text{sim}(q_i,p_{i,j}^-)}}
  \]  
  (softmax NLL / InfoNCE over positives vs negatives).
- **In-batch negatives (Sec. 3.2):** batch size \(B\). Let \(Q,P\in\mathbb{R}^{B\times d}\); similarity matrix \(S=QP^\top\in\mathbb{R}^{B\times B}\). Positive pairs are diagonal \((i=j)\); each question gets \(B-1\) negatives “for free” (effective \(B^2\) pairs/batch).
- **Negative choices (Sec. 3.2, Table 3):** Random, BM25-hard, Gold (positives from other questions). Best: **in-batch gold negatives + 1 BM25 hard negative per question** (adding 2 didn’t help).
- **Defaults / hyperparams (Sec. 5):** in-batch training, **batch=128**, **+1 BM25 negative**, Adam, lr **1e-5**, dropout **0.1**, linear warmup schedule; up to **40 epochs** (large datasets) / **100** (small).
- **Empirical retrieval gains (Table 2):** Top-20 accuracy: **NQ DPR 78.4 vs BM25 59.1**; Top-5 on NQ: **DPR 65.2 vs BM25 42.9** (reported in intro).  
  Sample efficiency (Fig. 1): **DPR with 1k training examples already beats BM25** on NQ dev.
- **Efficiency (Sec. 5.4):** FAISS DPR retrieval ~**995 Q/s** (top-100) vs Lucene BM25 **23.7 Q/s per CPU thread**. Indexing: encode 21M passages ~**8.8h on 8 GPUs**; build FAISS index ~**8.5h**; Lucene index ~**30 min**.

</details>

### 📄 SMuDGE grounded evaluation for Document VQA
**Paper** · [source](https://arxiv.org/html/2503.19120v1)

*Groundedness-sensitive evaluation protocol + reported reranking/calibration/robustness findings for DocVQA-style benchmarks*

<details>
<summary>Key content</summary>

- **Problem with ANLS/NLS:** surface similarity can reward hallucinations (e.g., predicting “26” vs GT “12” can score **0.5** due to shared digit) and penalize semantically correct variants (Section 1–2).
- **SMuDGE components (Section 3):**
  - **Multimodal grounding score**: locate predicted answer span and GT span in OCR word+box dictionary; compute distance between their boxes.
    - If predicted span not found above similarity threshold, set predicted box by mirroring GT box into “negative space” so distance becomes 1 (**Eq. 1**).
    - **Normalized Manhattan Distance (NMD)** between centroids (**Eq. 2**):  
      \(d=\frac{|x_p-x_g|}{W}+\frac{|y_p-y_g|}{H}\) where \(W,H\)=page width/height; \(x_*,y_*\)=centroid coords.
    - Grounding score: \(G=\exp(-d)\) (exponential decay rewards proximity/alignment).
  - **Type-aware surface similarity \(S\)** (Section 3.2):
    - Textual: NLS.
    - Numeric: **binary exact match**, allowing scaling by 100/1k/1M/1B.
    - Hybrid: split numeric/non-numeric substrings; combine via **weighted harmonic mean**; numeric weighted **10:1** over text (Appendix B.4).
- **Composite score (Eq. 3):** \( \text{SMuDGE}_\alpha = \alpha S + (1-\alpha)G\). \(\alpha=0\Rightarrow\) grounding-only; \(\alpha=1\Rightarrow\) type-aware similarity-only.
- **Defaults/parameters:**
  - Similarity threshold for “found on page”: **NLS = 0.3** (Appendix B.5; tuned via human match/mismatch on 100 pairs).
  - Recommended \(\alpha\) from calibration analysis: **~0.7** (Section 5.3; tuned on DUDE; DUDE excluded from analyses using this optimal \(\alpha\)).
- **Empirical findings:**
  - **DocVQA top-10 reranking:** with \(\alpha=0.7\), **all non-human/non-Qwen2-VL models move ≥1 position** (Section 5.1).
  - **Calibration link (DUDE):** small \(\alpha\) (more grounding) shows **negative correlation** with ECE; correlation crosses ~0 around **\(\alpha\approx0.7\)** (Section 5.3).
  - **Robustness:** volatility–ranking regression coefficient **0.58 (SMuDGE)** vs **0.33 (ANLS)** (Section 5.4). Top-5 robustness list differs: SMuDGE includes **Molmo-72B** and **Snowflake Arctic-TILT** (Table 3).
  - **Human eval:** 3 annotators; mean Cohen’s \(\kappa\) reported as high; majority agreement favors SMuDGE over NLS across DocVQA/MP-DocVQA/InfographicVQA (Section 5.5).

</details>

### 📊 DocVQA ICDAR 2021 — Tasks, Metrics, Leaderboards
**Benchmark** · [source](https://arxiv.org/pdf/2111.05547.pdf)

*DocVQA 2021 task definitions + official results (ANLS/ANLSL/MAP)*

<details>
<summary>Key content</summary>

- **Tasks (Sec. 1):**
  - **Single Document VQA:** answer questions on a *single-page business document*; answers usually appear in-image (extractive).
  - **Document Collection VQA:** questions over a *collection (~14K images) of same-template docs*; must output **answers + positive evidence doc IDs**.
  - **Infographics VQA:** questions on *infographics* emphasizing layout/visual/numerical reasoning beyond running text.
- **InfographicsVQA dataset (Sec. 3.2):** **5,485 images**, **30,035 QA pairs**, split **80/10/10** train/val/test; OCR provided via **Amazon Textract**. Answer types annotated: **image-span, multi-span (unordered list), question-span, non-span**; evidence types: **Text, Table/list, Figure, Map, Visual/layout**; operation tags: **counting/arithmetic/sorting**.
- **Metrics (Sec. 3.1, 4.1):**
  - **ANLS** (Average Normalized Levenshtein Similarity) for Single Doc + Infographics; for **multi-span unordered lists** in Infographics, accept **all permutations**.
  - **ANLSL** for Document Collection VQA: ANLS adapted to **unordered answer sets** using **Hungarian matching**.
  - **MAP** for evidence retrieval in Document Collection VQA (not used for ranking).
- **Key leaderboard results (Tables 1–3):**
  - **Infographics VQA (ANLS):** Human **0.9800**; **TILT 0.6120** (winner); IG-BERT **0.3854**; NAVER CLOVA **0.3219**; LayoutLM baseline **0.2720**; M4C baseline **0.1470**.
  - **Document Collection VQA:** **Infrrd-RADAR ANLSL 0.7743, MAP 74.66%**; Database baseline **0.7068, 71.06%**; TS-BERT baseline **0.4513, 72.84%**.
  - **Single Document VQA (ANLS):** Human **0.9811**; **TILT 0.8705**; LayoutLM 2.0 **0.8672**; Alibaba DAMO NLP **0.8506**; BERT Large baseline **0.6650**; M4C baseline **0.3910**.
- **Design rationale (Sec. 3):** 2020-era OCR→text-QA pipelines did well on text-heavy docs but failed more on **layout/graphics/handwriting**; InfographicsVQA created to stress **visual/layout reasoning** and **non-extractive** cases.

</details>

### 📖 Faiss `IndexIVFPQR` (IVF + PQ + PQ refinement) API tunables
**Reference Doc** · [source](https://faiss.ai/cpp_api/struct/structfaiss_1_1IndexIVFPQR.html)

*Concrete IVF-PQ-R constructor fields and tunables (e.g., `nlist`, `M`, `nbits`, `by_residual`, `nprobe`, refinement PQ, reranking via `store_pairs`)*

<details>
<summary>Key content</summary>

- **What it is:** `faiss::IndexIVFPQR` extends `IndexIVFPQ` with an **additional PQ refinement level** (“3rd level quantizer”).
- **Constructor (core hyperparameters):**  
  `IndexIVFPQR(Index* quantizer, size_t d, size_t nlist, size_t M, size_t nbits_per_idx, size_t M_refine, size_t nbits_per_idx_refine)`  
  - `d`: vector dimension  
  - `nlist`: number of inverted lists (coarse clusters)  
  - `M`, `nbits_per_idx`: PQ codebook structure for main PQ  
  - `M_refine`, `nbits_per_idx_refine`: PQ structure for refinement PQ
- **Key search-time parameters (public members):**
  - `size_t nprobe = 1`: number of IVF lists probed per query.
  - `size_t max_codes = 0`: cap on number of codes visited per query (0 = no cap).
  - `float k_factor`: multiplier between requested `k` and the `k` requested from the underlying IVFPQ stage.
- **Encoding / residual design:**
  - `bool by_residual = true`: codes encode vectors **relative to coarse centroids** (residual coding).
  - `size_t code_size`: bytes per vector code.
- **Refinement structures:**
  - `ProductQuantizer pq`: main PQ producing codes.
  - `ProductQuantizer refine_pq`: refinement PQ; `std::vector<uint8_t> refine_codes` stores corresponding codes.
- **Speed/accuracy knobs:**
  - `int use_precomputed_table`: precompute query tables (memory tradeoff; used only for `by_residual` + L2).
  - `size_t scan_table_threshold`: choose table computation vs on-the-fly.
  - Polysemous filtering/training: `do_polysemous_training`, `polysemous_ht`, `polysemous_training*`.
- **Reranking / reconstruction workflow:**
  - `search_preassigned(..., bool store_pairs, ...)`: if `store_pairs=true`, results store **(invlist id, offset)** in upper/lower 32 bits (instead of ids), enabling `reconstruct_from_offset(list_no, offset, ...)` and `search_and_reconstruct(...)` without maintaining `direct_map`.

</details>

### 📖 Faiss index types ↔ classes, parameters, and IVF/HNSW rules of thumb
**Reference Doc** · [source](https://github.com/facebookresearch/faiss/wiki/Faiss-indexes)

*Index class ↔ algorithm mapping + key parameters (M, nlist/nprobe, cosine via IndexFlatIP)*

<details>
<summary>Key content</summary>

- **Exact (exhaustive) search**
  - `IndexFlatL2` (“Flat”): exact L2; params: `d`; memory **4*d bytes/vector**.
  - `IndexFlatIP` (“Flat”): exact inner product; params: `d`; memory **4*d**; **cosine similarity via pre-normalizing vectors** (then IP ≡ cosine).
- **HNSW graph (approximate)**
  - `IndexHNSWFlat` (“HNSW,Flat”): params `d, M`; memory **4*d + x*M*2*4** bytes/vector (graph overhead term shown in table).
  - Key HNSW params: **`M`** (#neighbors; ↑M ⇒ ↑accuracy, ↑memory), **`efConstruction`** (add-time exploration depth), **`efSearch`** (query-time exploration depth).
  - Restriction: HNSW **does not support removal** (would break graph).
- **IVF (cell-probe / inverted lists; approximate)**
  - `IndexIVFFlat` (“IVFx,Flat”): params `quantizer, d, nlist(s), metric`; memory **4*d + 8** bytes/vector (**+8 bytes for stored vector id**). Uses another index (“coarse quantizer”) to assign vectors to lists; typically a Flat quantizer.
  - Query-time parameter: **`nprobe`** = number of inverted lists visited.
  - **Eq. 1 (scan fraction):** approx scanned fraction ≈ **nprobe / nlist** (underestimates due to uneven list lengths).
  - **Rule of thumb (centroids):** for `n` points, choose **nlist = C * sqrt(n)** with **C ≈ 10** (balances assignment cost vs list scanning).
- **PQ / SQ encodings (compression)**
  - `IndexScalarQuantizer` (“SQ8”): memory **d bytes/vector** (also 6/4-bit variants).
  - `IndexPQ` (“PQx” / “PQ”M”x”nbits”): memory **ceil(M*nbits/8)**; constraints: **d multiple of M**; `nbits` **8/12/16**.
  - `IndexIVFPQ` (“IVFx,PQy×nbits”): memory **ceil(M*nbits/8)+8**; typical usage: `IndexFlatL2(d)` as coarse quantizer; set `index.nprobe` at query time.

</details>

### 🔍 BM25 (Okapi) scoring + parameter meanings
**Explainer** · [source](https://web.stanford.edu/class/cs276/handouts/lecture12-bm25etc.pdf)

*BM25 scoring equation (k1, b, IDF variants), term saturation + length normalization intuition*

<details>
<summary>Key content</summary>

- **BM25 score (Eq. 1):**  
  \[
  RSV_{BM25}(d,q)=\sum_{i\in q} \log\frac{N}{df_i}\cdot \frac{(k_1+1)\,tf_i}{k_1\left((1-b)+b\frac{dl}{avdl}\right)+tf_i}
  \]
  - \(N\): #documents; \(df_i\): document frequency of term \(i\)  
  - \(tf_i\): term frequency of \(i\) in document \(d\)  
  - \(dl\): document length; \(avdl\): average document length in collection  
  - \(k_1\): term-frequency scaling (saturation) parameter  
  - \(b\in[0,1]\): length normalization strength
- **Length normalization component (Eq. 2):**  
  \[
  B=(1-b)+b\frac{dl}{avdl},\quad \tilde{tf}_i=\frac{tf_i}{B}
  \]
  (BM25 can be written using \(\tilde{tf}_i\) equivalently.)
- **Term-frequency saturation curve (motivation):** \(\frac{tf}{k_1+tf}\) is monotone in \(tf\) but approaches a maximum (bounded term contribution); low \(k_1\) saturates quickly, high \(k_1\) keeps rewarding increases.
- **Parameter defaults (rule-of-thumb):** \(k_1\approx 1.2\text{–}2\), \(b\approx 0.75\). Extremes: \(k_1=0\) → binary; large \(k_1\) → closer to raw \(tf\). \(b=0\) no length norm; \(b=1\) full relative-frequency scaling.
- **Empirical comparison example (machine learning query, \(k_1=2\)):**  
  doc1 (learning 1024, machine 1): tf-idf 87 vs BM25 31; doc2 (learning 16, machine 8): tf-idf 75 vs BM25 42.7 (BM25 prefers doc2 due to saturation).

</details>

### 📋 Donut — OCR-free Document Understanding Transformer
**Research Paper** · [source](https://arxiv.org/abs/2111.15664)

*End-to-end Transformer mapping document images → structured JSON (no OCR), with training pipeline + key metrics*

<details>
<summary>Key content</summary>

- **Problem with OCR-based VDU (Abstract/Intro):** (1) high compute cost; (2) inflexible across languages/domains; (3) OCR error propagation.
- **Model (Section 2.2):** Transformer-only **encoder–decoder**.
  - **Input image:** \(\mathbf{x}\in\mathbb{R}^{H\times W\times C}\).
  - **Encoder output embeddings:** \(\{\mathbf{z}_i\in\mathbb{R}^d\}_{i=1}^{n}\), where \(n\)=#patches/feature-map size, \(d\)=latent dim. Encoder instantiated with **Swin Transformer** (chosen after backbone comparison; Sec. 3.4.2).
  - **Decoder:** **BART**; generates token sequence \((\mathbf{y}_i)_{i=1}^{m}\), \(\mathbf{y}_i\in\mathbb{R}^{v}\) one-hot, \(v\)=vocab size, \(m\)=max length. Uses **teacher forcing** in training; **prompt-based generation** at test time with task-specific special tokens (Sec. 2.2.3).
- **Output format (Sec. 2.2.4):** tokens are **1–1 invertible to JSON** using field delimiters \([START_\*]\), \([END_\*]\). If malformed (missing end token), field treated as **lost**; parsing via regex.
- **Pre-training task (Sec. 2.3.1):** “pseudo-OCR”: read **all text in reading order** (top-left→bottom-right). Objective: **cross-entropy next-token prediction** conditioned on image + previous tokens.
- **Synthetic data (Intro/Contrib):** **SynthDoG** generator enables multilingual/domain-flexible pretraining.
- **IE evaluation metrics (Sec. 3.1.2):**
  - **Field-level F1:** exact match per field (any character miss ⇒ fail).
  - **TED-based accuracy:** \(\max(0, 1-\mathrm{TED}(\mathrm{pr},\mathrm{gt})/\mathrm{TED}(\phi,\mathrm{gt}))\), where pr=pred tree, gt=ground-truth tree, \(\phi\)=empty tree.
- **Defaults/hyperparams (Training details):** input resolution **2560×1920**; decoder max length **1536**; Adam LR init searched **1e-5 to 1e-4**.
- **Empirical speed/quality (Fig. 1):** avg runtime **Donut ~0.6s** vs OCR+downstream **~1.9s**; parsing quality **~6.0 nTED** (Donut) vs **~14.2 nTED** (OCR+BERT extractor). Larger resolution improves accuracy but slows inference (Sec. 3.4.3).

</details>

### 🔍 Spotify Natural Language Search (Dense Retrieval) for Podcast Episodes
**Explainer** · [source](https://engineering.atspotify.com/2022/3/introducing-natural-language-search-for-podcast-episodes)

*Production architecture narrative for moving from term-based search to semantic retrieval + ranking + operational constraints*

<details>
<summary>Key content</summary>

- **Problem with term matching:** Elasticsearch term-based retrieval can return nothing for natural-language queries (e.g., “electric cars climate impact”) when no episode metadata contains all query terms; fuzzy matching/aliases don’t cover all paraphrases.
- **Dense retrieval setup (shared embedding space):** Train encoders to map **query text** and **episode text** (concatenated metadata: episode title/description + parent show title/description, etc.) into vectors.
- **Eq. 1 (Cosine similarity):**  
  \[
  s(q,e)=\cos(\mathbf{v}_q,\mathbf{v}_e)=\frac{\mathbf{v}_q\cdot \mathbf{v}_e}{\|\mathbf{v}_q\|\;\|\mathbf{v}_e\|}
  \]  
  where \(\mathbf{v}_q\)=query embedding, \(\mathbf{v}_e\)=episode embedding.
- **Model choice rationale:** Vanilla BERT yields weak off-the-shelf sentence embeddings (per SBERT findings) and is English-only; Spotify chose **Universal Sentence Encoder CMLM multilingual** (100+ languages) because **CMLM objective** targets sentence embeddings directly.
- **Training data pipeline:**  
  1) Positive (query, episode) pairs from successful search logs (from prior Elasticsearch results).  
  2) Query reformulations: (failed_query_before_success, episode).  
  3) Synthetic queries: fine-tune **BART on MS MARCO**, generate (synthetic_query, episode) pairs (inspired by “Embedding-based Zero-shot Retrieval through Query Generation”).  
  4) Small manually curated semantic query set (evaluation only).  
  Split ensures eval episodes not in train.
- **Negatives & loss:** Use **in-batch negatives** with batch size \(B\): positives \(=B\); negatives \(=B^2-B\). Compute in-batch cosine similarity matrix; use losses incl. **MSE vs identity**, plus **hard negative mining** and **margin loss**.
- **Offline/online production architecture:**  
  - Offline: precompute episode vectors; index in **Vespa** with **ANN** for tens of millions of episodes; first-phase ranking can add features (e.g., popularity).  
  - Online: compute query vector via **Vertex AI GPU inference**; **T4 GPU ~6× cheaper than CPU** in load tests; retrieve **top 30** semantic episodes; use **vector cache** for repeated queries.
- **Multi-source retrieval:** Dense retrieval is an *additional* source (can underperform exact term matching and is costlier). Final-stage reranker blends candidates from dense + other sources (incl. Elasticsearch) and adds **cosine similarity** as a feature.  
- **Outcome:** A/B test showed **significant increase in podcast engagement**; rolled out to most users.

</details>

---

## Related Topics

- [[topics/agent-memory|Agent Memory]]
- [[topics/agent-fundamentals|Agent Fundamentals]]
- [[topics/evaluation-benchmarks|Evaluation Benchmarks]]
- [[topics/knowledge-graphs|Knowledge Graphs & Structured Knowledge]]
- [[topics/document-understanding|Document Understanding]]
- [[topics/long-context|Long Context Models]]
