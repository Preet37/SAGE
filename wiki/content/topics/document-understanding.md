---
title: "Document Understanding"
subject: "Multimodal AI"
date: 2026-04-09
tags:
  - "subject/multimodal-ai"
  - "level/beginner"
  - "level/intermediate"
  - "level/advanced"
  - "resource/video"
  - "resource/blog"
  - "resource/deep-dive"
  - "resource/paper"
  - "resource/code"
educators:
  []
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

# Document Understanding

## Video (best)
- **None identified**
- Why: Document understanding spans OCR, layout modeling, and structured extraction; no single, clearly best, widely recognized video resource is confidently identifiable.
- Level: —

## Blog / Written explainer (best)
- **Hugging Face Docs** — "LayoutLM"
- **Link:** [https://huggingface.co/docs/transformers/model_doc/layoutlm](https://huggingface.co/docs/transformers/model_doc/layoutlm)
- Why: Clear, practical overview of a canonical layout-aware document understanding model family; includes usage patterns and key ideas.
- Level: Intermediate

## Deep dive
- **Hugging Face Docs** — "LayoutLMv2"
- **Link:** [https://huggingface.co/docs/transformers/model_doc/layoutlmv2](https://huggingface.co/docs/transformers/model_doc/layoutlmv2)
- Why: Deeper treatment of multimodal/layout-aware modeling (text + layout + image features) commonly used for forms, receipts, and scanned documents.
- Level: Intermediate–Advanced

## Original paper
- **Xu et al.** — "LayoutLM: Pre-training of Text and Layout for Document Image Understanding"
- **Link:** [https://arxiv.org/abs/1912.13318](https://arxiv.org/abs/1912.13318)
- Why: Foundational paper for layout-aware document understanding; establishes the text+2D layout pretraining paradigm.
- Level: Advanced

## Code walkthrough
- **Hugging Face Transformers** — "Document Question Answering" (pipeline task page)
- **Link:** [https://huggingface.co/tasks/document-question-answering](https://huggingface.co/tasks/document-question-answering)
- Why: Practical entry point showing how document understanding models are applied end-to-end (inputs, outputs, typical models).
- Level: Beginner–Intermediate

## Coverage notes
- Strong: Layout-aware models (LayoutLM family) and practical usage via Hugging Face; general document QA workflows.
- Weak: OCR-free understanding and modern OCR-free pipelines (e.g., Donut-style approaches) are not covered here as a single “best” resource.
- Gap: Visual document retrieval (e.g., ColPali/page-level embeddings) and specific libraries like docTR; table extraction and form understanding need dedicated, high-confidence “best” explainers and code walkthroughs.

---

## Additional Resources for Tutor Depth

> **9 sources** — papers, official docs, working code, benchmarks, and deep explainers that give the AI tutor precision on this topic.

### 📄 ColPali + ViDoRe (visual page retrieval w/ late interaction)
**Paper** · [source](https://arxiv.org/abs/2407.01449)

*ViDoRe benchmark + ColPali multi-vector page embeddings w/ late-interaction scoring; retrieval metrics + efficiency (indexing/latency/memory) tradeoffs*

<details>
<summary>Key content</summary>

- **Problem setting (Sec. 2):** page-level retrieval (each *page* is the “document”). Industrial requirements: **R1** retrieval quality (nDCG, Recall@K, MRR), **R2** online query latency, **R3** offline indexing throughput.
- **ViDoRe benchmark (Sec. 3):** 10 tasks across modalities/domains/languages. Examples: DocVQA (500q/500 docs), InfoVQA (500/500), TAT-DQA (1600/1600), arXiVQA (500/500), TabFQuAD French tables (210/210); practical corpora: Energy/Gov/Healthcare/AI/Shift (each 100 queries, 1000 pages).
- **Late interaction scoring (Eq. 1):** with query multi-vectors \(Q=\{q_i\}_{i=1}^{|Q|}\) and page multi-vectors \(D=\{d_j\}_{j=1}^{|D|}\),  
  \[
  s(Q,D)=\sum_{i=1}^{|Q|}\max_{j\in[1,|D|]} q_i^\top d_j
  \]
- **Training (Sec. 4.2):** 118,695 query–page pairs (English), incl. academic train sets + synthetic PDF pages with VLM-generated pseudo-questions. **1 epoch**, **bf16**, **LoRA** on LM layers + projection; **paged_adamw_8bit**, **LR 1e-4** linear decay, **2.5% warmup**, **batch 32**, **8 GPUs**. Query augmentation: append **5 `<unused0>` tokens**.
- **Key result (Table 2, nDCG@5 avg):** **ColPali (+Late Inter.) 81.3** vs Unstructured+Captioning+BGE-M3 **67.0**, Unstructured+OCR+BGE-M3 **66.1**, SigLIP vanilla **51.4**, Jina-CLIP **17.7**. ColPali strong on visually complex tasks (e.g., InfoVQA **81.8**, TabFQuAD **83.9**).
- **Efficiency (Sec. 5.2):** ColPali skips OCR/layout/chunking → faster indexing despite larger model. Stores **one vector per image patch** (+ prompt tokens “Describe the image”), projected to **128-d**; memory **~154 KB/page**. Token pooling: **pool factor 3** reduces vectors by **~66%** while keeping **~97%** of performance.

</details>

### 📄 Donut (OCR-free Document Understanding Transformer)
**Paper** · [source](https://arxiv.org/abs/2111.15664)

*Donut end-to-end pipeline: image encoder + autoregressive text decoder; task-specific target serialization (JSON-like) and training/inference via teacher forcing and sequence generation*

<details>
<summary>Key content</summary>

- **Problem with OCR-based VDU (Abstract/Intro):** (1) high OCR compute cost, (2) inflexible across languages/domains, (3) OCR error propagation to downstream parsing/QA.
- **End-to-end architecture (Sec. 2.2):** Transformer-only **visual encoder + textual decoder** mapping raw image → structured output (no OCR).
  - **Encoder (Sec. 2.2.1):** image \( \mathbf{x}\in\mathbb{R}^{H\times W\times C} \rightarrow \{\mathbf{z}_i\}_{i=1}^{n}, \mathbf{z}_i\in\mathbb{R}^{d}\). \(n\)=#patches/feature-map tokens, \(d\)=embedding dim. Uses **Swin Transformer** (patch split, shifted-window attention, patch merging).
  - **Decoder (Sec. 2.2.2):** generates token sequence \((\mathbf{y}_i)_{i=1}^{m}\), \(\mathbf{y}_i\in\mathbb{R}^{v}\) one-hot; \(v\)=vocab size, \(m\)=max length. Uses **BART**; initialized from a **multilingual BART** checkpoint.
- **Training/inference (Sec. 2.2.3):**
  - **Teacher forcing** during training (ground-truth previous tokens as input).
  - **Prompted generation** at test time (GPT-3-style); task-specific special prompt tokens.
- **Output serialization (Sec. 2.2.4):** token sequence is **1–1 invertible to JSON** using field delimiters \([START_\*],[END_\*]\). If malformed (e.g., missing end token), treat field as **lost**; can parse via regex.
- **Pre-training objective (Sec. 2.3.1):** pseudo-OCR: generate **all texts in reading order** (top-left→bottom-right) with **next-token cross-entropy** conditioned on image + prior tokens. Uses **SynthDoG** synthetic generator for multilingual/domain flexibility.
- **Fine-tuning (Sec. 2.4):** cast downstream tasks (classification/IE/DocVQA) as **JSON prediction**; e.g., class “memo”: \([START\_class][memo][END\_class]\) ↔ \(\{"class":"memo"\}\).
- **Metrics for IE (Sec. 3.1.2):** field-level **F1** and **TED-based accuracy**  
  \[
  \max\left(0, 1-\frac{\mathrm{TED}(\mathrm{pr},\mathrm{gt})}{\mathrm{TED}(\varnothing,\mathrm{gt})}\right)
  \]
  where gt=ground truth tree, pr=predicted tree, \(\varnothing\)=empty tree.
- **Defaults/hyperparams (Experiments):** input resolution **2560×1920**, decoder max length **1536**, Adam LR initial **1e-5 to 1e-4**.
- **Empirical comparisons (Sec. 3.3 + Fig. 1):**
  - Document classification: Donut **SOTA vs LayoutLM/LayoutLMv2**, reported **~2× faster** than LayoutLMv2 while using fewer params (OCR pipelines add extra OCR params; example OCR model **>80M params**).
  - Fig. 1 example: avg runtime **~0.6 s** (Donut E2E) vs **~1.9 s** (OCR + downstream BERT-like); parsing quality **~6.0 nTED** (Donut) vs **~14.2 nTED** (OCR+BERT extractor) (lower is better).
  - Resolution tradeoff example (Sec. 3.3.2): CORD at **1280×960**: **0.7 s/image**, **91.1 accuracy** (TED-based).

</details>

### 📄 Gaussian-biased layout attention (LAGaBi)
**Paper** · [source](https://aclanthology.org/2023.findings-emnlp.521.pdf)

*Explicit math for injecting 2D geometry into attention via polar coords + Gaussian bias; ablations/impact*

<details>
<summary>Key content</summary>

- **Polar relative geometry (Section 3.1):** For query token *i* and key token *j*, using normalized top-left box coords \((x_i,y_i)\), \((x_j,y_j)\):  
  - Distance \(\rho_{ij}=\sqrt{(x_j-x_i)^2+(y_j-y_i)^2\) (Eq. 1), \(\rho_{ij}\in[0,1]\)  
  - Angle \(\theta_{ij}=\tan^{-1}\left(\frac{y_j-y_i}{x_j-x_i}\right)\) (Eq. 2), \(\theta_{ij}\in[-\pi/2,\pi/2]\)  
  - Spatial relation \(u_{ij}=(\rho_{ij},\theta_{ij})\).
- **Gaussian layout bias + attention injection (Section 3.2):** Modify single-head attention distribution:  
  \[
  a_{ij}=\frac{\exp\left(\frac{q_i k_j^\top}{\sqrt{d_k}}+\alpha\,(g(u_{ij})-1)\right)}{\sum_{j=1}^N \exp\left(\frac{q_i k_j^\top}{\sqrt{d_k}}+\alpha\,(g(u_{ij})-1)\right)}
  \]  
  (Eq. 3) where \(q_i,k_j\) are query/key vectors, \(d_k\) head dim, \(\alpha\) trade-off.  
  Bias from 2D Gaussian kernel:  
  \[
  g(u)=\exp\left(-\tfrac12 (u-\mu)^\top \Sigma^{-1}(u-\mu)\right)
  \]
  (Eq. 4), with learnable \(\mu\in\mathbb{R}^{2\times1}\), \(\Sigma\in\mathbb{R}^{2\times2}\) **diagonal** (2 params). Kernels differ per head, **shared across layers**. Extra params \(=2\times2\times N_{\text{heads}}\) (e.g., 12 heads → **48 params**). Layout affects **queries/keys, not values**.
- **Defaults/training:** Coordinates normalized to integers \([0,1000]\); special tokens get empty box \([0,0,0,0]\). Fine-tune 2000 steps, batch 16; Adam; LR \(5e{-5}\) (FUNSD) / \(7e{-5}\) (CORD/XFUND). \(\alpha\) tuned best at **4** (CORD val: 94.77 at \(\alpha=4\); Table 4).
- **Key results (F1):**  
  - RoBERTa baseline: FUNSD **66.48**, CORD **93.54** (Table 1).  
  - RoBERTa+LAGaBi (no doc pretrain): FUNSD **84.84** (+18.36), CORD **95.97** (+2.43).  
  - RoBERTa+LAGaBi (1M doc pretrain): FUNSD **89.15**, CORD **96.56**.  
  - Ablations (Table 3, FUNSD / CORD val): baseline 66.48/92.29; +embedding 69.59/92.67; +linear bias 76.32/93.00; +fixed Gaussian 83.81/93.00; +Euclidean dist 73.05/93.72; +angle only 84.48/94.70; +2D-xy dist 79.85/94.21; **full LAGaBi 84.84/94.77**. Angle > distance; learnable Gaussian > fixed/linear.

</details>

### 📄 KIE benchmarks have train/test template leakage (SROIE, FUNSD)
**Paper** · [source](https://arxiv.org/pdf/2304.14936.pdf)

*Empirical evidence that standard KIE benchmarks overestimate generalization due to train/test template similarity; proposes resampled “0% overlap” splits and reports performance drops.*

<details>
<summary>Key content</summary>

- **Problem/Rationale (Sec. 3.1):** Official IID splits can include near-duplicate document templates across train/test, enabling memorization rather than **generalization to unseen templates** (real-world domain shift).
- **Task formalization (Eq. 1, Sec. 2.3):** Token classification for KIE with IOB tags.  
  - Tokens: \(T=\{t_i\}_{0<i\le n}\) from document \(D\); image \(I\).  
  - Entity types \(m\) ⇒ classes \(2m+1\) (B-entity, I-entity, O).  
  - Classifier: \(F(t_i\mid T,I)=c,\; c\in\{1,\dots,2m+1\}\). Entity correct only if all span tokens correctly tagged.
- **Template similarity quantification (Sec. 3.2):**
  - **SROIE:** group receipts by **business/template**; found **75% template replication in the official test set** (abstract). Group sizes range **1–76** receipts.
  - **FUNSD:** define form similarity via question overlap:  
    \[
    \text{Overlap}(doc_A,doc_B)=\frac{\text{Count}(Questions_A\cap Questions_B)}{\max(\lvert Questions_A\rvert,\lvert Questions_B\rvert)}
    \]
    Use threshold **0.7**; in official test set, **8/50 = 16%** forms share a template with training.
  - **Resampling rule:** ensure each template group appears in **only one split** (“0% overlap”).
- **Training defaults (Sec. 4.1):** batch size **2**; Adam; LR **2e-5**; halve LR every **10 epochs** w/o val-F1 improvement; stop when LR < **1e-7**; pick best val-F1. For each experiment: fixed test set; create **4** train/val splits (80/20) from remaining data; report average.
- **Empirical impact (Tables 1–2, Sec. 4.3):**
  - **SROIE:** average F1 drops **94.34 → 85.60**; best F1 **96.55 → 89.38**. Text-only models drop **~10.5 F1** vs multimodal **~7.5 F1**.
  - **FUNSD:** text-only models drop **~3.5 F1** vs multimodal **~0.5 F1** on adjusted splits.

</details>

### 📄 LOFI pipeline (Language/OCR/Form Independent) for SER in LRL documents
**Paper** · [source](https://aclanthology.org/2024.emnlp-industry.79.pdf)

*Industry-oriented experimental results + practical evaluation for KIE/SER generalization (Korean/Japanese), robustness, and deployment constraints*

<details>
<summary>Key content</summary>

- **Problem framing (Intro/§3):** Industrial SER on visually rich documents faces 3 dependencies: **Language** (LRL data/model scarcity), **OCR** (word/line/char-level box granularity varies by language/OCR), **Form** (reading order unreliable under rotation/distortion).
- **LOFI pipeline steps (§3):**
  1) **OCR & text alignment:** OCR → (text, boxes); sort boxes **Top-Left→Bottom-Right** (Algorithm 1; row grouping by height tolerance ϵ, then left-to-right).  
  2) **Token-level box split:** convert any OCR box granularity to **token-level boxes** (Algorithm 2): tokenize text; classify characters (number/symbol/upper/lower etc.); apply **predefined size ratios** per char type to proportionally split/adjust original OCR box into token boxes.  
  3) **Model inference:** (token, token-box) → **LiLT** encoder; **SPADE decoder** outputs **ITC** (initial token entity type) + **STC** (token-to-token connectivity) to recover entities despite wrong reading order.  
  4) Combine outputs → final SER.
- **Design rationale:**  
  - **LiLT** chosen because layout encoder is relatively **language-independent**; swap **text encoder PLM** per language (Korean/Japanese) without extra pretraining (§2.1/§3).  
  - **SPADE** used to reduce reliance on correct 1D reading order under distortions (§2.3/§3).
- **Key empirical results (entity-level F1, §5):**
  - **Korean medical bills:** LayoutXLM 95.58%; **LOFI-ko 95.64%** with **116M params** vs LayoutXLM **369M** (~68.6% fewer).  
  - **Japanese receipts:** LayoutXLM 94.35%; **LOFI-mul† (InfoXLM+lilt-only-base) 94.60%** (284M, no image embedding); LOFI-ja 93.78%.
  - **Open datasets (§5.2):** FUNSD—BROS 83.05% (best), LOFI-en 78.99%; CORD—LayoutLMv3 96.80% (best), LOFI-en 96.39%.
- **Ablations (§6):**
  - **Training data need:** “Satisfactory” SER typically needs **~300–400 docs**; **<200 docs → ≥5% F1 drop** vs full set.  
  - **Pretrained layout encoder helps:** Pretrained vs initialized layout encoder F1: **0.9564 vs 0.9259** (Ko), **0.9290 vs 0.9035** (Ja).
- **Defaults/hyperparams (Appendix Table 5):** max length **512**; epochs **50** (Ko bills), **100** (Ja receipts/FUNSD/CORD); LR **1e-5** (Ko), **5e-5** (Ja/FUNSD/CORD); batch **24** (Ko), **32** (Ja), **4** (FUNSD), **16** (CORD). Base arch: hidden **768**, heads **12**, FFN **3072**, layers **12**.

</details>

### 📄 LayoutLMv3 unified MLM/MIM + Word-Patch Alignment
**Paper** · [source](https://arxiv.org/pdf/2204.08387.pdf)

*Exact pretraining objective formulations (MLM/MIM/WPA) + architecture choices enabling multimodal alignment*

<details>
<summary>Key content</summary>

- **Architecture (Sec. 2.1):** Single multimodal Transformer over concatenated sequences: text embeddings \(Y=y_{1:L}\) and image patch embeddings \(X=x_{1:M}\).  
  - **Text embedding:** word embeddings (init from RoBERTa) + 1D position + **2D layout** embeddings from OCR bounding boxes; uses **segment-level** 2D positions (words in a segment share a box).  
  - **Image embedding:** resize to \(3\times224\times224\), split into \(P\times P\) patches with \(P=16\), so \(M=HW/P^2=196\); linear projection to hidden dim + learnable **1D** position (no 2D pos improvement reported).
- **Total pretraining loss (Sec. 2.2):**  
  \[
  \mathcal{L}=\mathcal{L}_{MLM}+\mathcal{L}_{MIM}+\mathcal{L}_{WPA}.
  \]
- **MLM (Eq. 1):** mask **30%** text tokens via **span masking** (Poisson \(\lambda=3\)).  
  \[
  \mathcal{L}_{MLM}(\theta)=-\sum_{\ell=1}^{L'}\log p_\theta(y_\ell\mid X_{M'},Y_{L'})
  \]
  where \(L'\)=# masked text positions; \(X_{M'},Y_{L'}\)=corrupted sequences.
- **MIM (Eq. 2):** mask ~**40%** image tokens with **blockwise masking**; targets are **discrete VAE tokens** (visual vocab size **8192**, tokenizer init from DiT).  
  \[
  \mathcal{L}_{MIM}(\theta)=-\sum_{m=1}^{M'}\log p_\theta(x_m\mid X_{M'},Y_{L'})
  \]
- **WPA (Eq. 3):** binary classify for each **unmasked** text token whether its aligned image patch is masked (“unaligned”) or not (“aligned”); exclude masked text tokens; 2-layer MLP + BCE:  
  \[
  \mathcal{L}_{WPA}(\theta)=-\sum_{\ell=1}^{L-L'}\log p_\theta(z_\ell\mid X_{M'},Y_{L'})
  \]
  \(z_\ell\in\{0,1\}\).
- **Key results (Table 1):** LayoutLMv3 **BASE** (133M, patch/linear) FUNSD **90.29 F1**, CORD **96.56 F1**, RVL-CDIP **95.44 Acc**, DocVQA **78.76 ANLS**; **LARGE** FUNSD **92.08**, CORD **97.46**, RVL-CDIP **95.93**, DocVQA **83.37**.  
- **Ablation (Table 3/Fig. 4):** linear patches + **MLM only** causes **PubLayNet loss divergence**; adding **MIM** enables convergence (mAP **94.38**), adding **WPA** improves further (mAP **94.43**).

</details>

### 📄 LayoutLMv3 unified MLM/MIM + Word-Patch Alignment
**Paper** · [source](https://arxiv.org/pdf/2204.08387v3.pdf)

*Objective definitions (MLM/MIM/WPA), architecture + training details, key benchmark numbers*

<details>
<summary>Key content</summary>

- **Architecture (Sec. 2.1):** Single multimodal Transformer over concatenated sequences: text embeddings \(Y=y_{1:L}\) + image patch embeddings \(X=x_{1:M}\).  
  - **Text:** OCR provides tokens + 2D boxes; embeddings = word (init from RoBERTa) + 1D position + **2D layout** (x, y, w, h embedded separately; coords normalized by image size). Uses **segment-level** layout positions (words in a segment share same 2D box).  
  - **Image:** resize to \(3\times224\times224\); split into \(P\times P\) patches with \(P=16\) → \(M=196\); linear projection to hidden dim + learnable **1D** pos emb (no 2D pos gains reported).
- **Pretraining loss (Sec. 2.2):** \(L=L_{\text{MLM}}+L_{\text{MIM}}+L_{\text{WPA}}\).  
  - **MLM (Eq. 1):** mask **30%** text tokens via span masking (Poisson \(\lambda=3\));  
    \[
    L_{\text{MLM}}(\theta)=-\sum_{l=1}^{L'}\log p_\theta(y_l\mid X_{M'},Y_{L'})
    \]
    \(L'\)=#masked text positions; \(X_{M'},Y_{L'}\)=corrupted sequences.  
  - **MIM (Eq. 2):** mask ~**40%** image tokens blockwise; discrete targets from image tokenizer (dVAE-style; vocab **8192**);  
    \[
    L_{\text{MIM}}(\theta)=-\sum_{m=1}^{M'}\log p_\theta(x_m\mid X_{M'},Y_{L'})
    \]
  - **WPA (Eq. 3):** for each **unmasked** text token, predict if its corresponding image patch is masked (aligned=both unmasked); exclude masked text tokens; 2-layer MLP + BCE:  
    \[
    L_{\text{WPA}}(\theta)=-\sum_{\ell=1}^{L-L'}\log p_\theta(z_\ell\mid X_{M'},Y_{L'})
    \]
    \(z_\ell\in\{0,1\}\).
- **Pretraining setup (Sec. 3.2):** IIT-CDIP **11M** docs; Adam, batch **2048**, **500k** steps; wd \(1e{-2}\), \((\beta_1,\beta_2)=(0.9,0.98)\). LR: BASE \(1e{-4}\) warmup **4.8%**; LARGE \(5e{-5}\) warmup **10%**.
- **Model sizes (Sec. 3.1):** BASE 12L/12H, \(D=768\), FFN 3072; LARGE 24L/16H, \(D=1024\), FFN 4096; max text length \(L=512\).
- **Key results (Table 1):** LayoutLMv3 **BASE** (133M, patch/linear) FUNSD **90.29** F1; CORD **96.56** F1; RVL-CDIP **95.44%**; DocVQA **78.76** ANLS. LayoutLMv3 **LARGE** FUNSD **92.08**; CORD **97.46**; RVL-CDIP **95.93%**; DocVQA **83.37**.  
  - vs LayoutLMv2 BASE: FUNSD 82.76 → **90.29**; DocVQA 78.08 → **78.76** with simpler image embedding.
- **Ablation (Table 3/Fig. 4):** Linear patches + **MLM only** causes PubLayNet loss divergence; adding **MIM** enables convergence (PubLayNet mAP **94.38**), adding **WPA** improves further (mAP **94.43**).

</details>

### 📄 Robustness attacks for OCR-based VDU (BBox/Text/Pixel)
**Paper** · [source](https://arxiv.org/pdf/2506.16407.pdf)

*Quantitative robustness/perturbation evaluation showing OCR/layout error propagation and degradation under realistic, budgeted noise*

<details>
<summary>Key content</summary>

- **Unified threat model & budgets (Sec. 3.1):**
  - **Layout budget:** constrain perturbed box \(b'\) vs. original \(b\) by **IoU\((b,b') \ge \tau\)** (default **\(\tau=0.6\)**; ablations at 0.75, 0.9).
  - **Text budget:** **edit\_rate** = character replacement rate (no insert/delete; positions aligned). Default **0.1**.
  - **Pixel budget:** apply document-specific transforms from **RoDLA (12 augmentations)** (blur/noise/occlusion/shadow/contrast, etc.) after shifting pixels with the box.
- **BBox predictor enabling gradients (Sec. 3.2, Eq. 1):**
  - Train per-model predictor mapping token embeddings \(\rightarrow (x,y,w,h)\) using **SmoothL1 + GIoU loss** (Eq. 1).
  - Architecture: **2-layer MLP → 4-layer Transformer encoder → 2-layer MLP**.
- **PGD layout attack with mIoU-budget loss (Sec. 3.3):**
  - Iterative PGD updates on embeddings/boxes; **project back** to feasible set satisfying IoU budget; keep best of **10 candidates**.
- **Six attack scenarios (Sec. 3.5):**  
  S1 BBox; S2 BBox+Pixel; S3 S2+Augment; S4 Text; S5 BBox+Text; **S6 BBox+Pixel+Text**. Evaluate **word vs. line** granularity.
- **Defaults/training (Sec. 4.1):** finetune **100 epochs**, **AdamW**, **lr** (given), **batch 32**, **weight decay** (given), **NVIDIA L40S 48GB**.
- **Empirical results (IoU=0.6, 5 seeds):**
  - Max reported vulnerability: **up to 29.18% F1 drop** (LayoutLMv3, **S6 PGD**, Table 3).
  - **PGD > Random** in compound attacks (Table 3): e.g., LayoutLMv3 **S5** Random **16.55** vs PGD **22.78**; **S6** Random **28.91** vs PGD **29.18**.
  - **Line-level > word-level** (FUNSD, Table 4): biggest gap **S6** = **+21.37 pp (Random)**, **+13.44 pp (PGD)**.
  - **Tighter IoU reduces Random more than PGD** (Table 7, FUNSD S1 line): Random drop **7.94→2.94→0.54** (IoU 0.6/0.75/0.9) vs PGD **13.32→6.60→6.50**.
  - **Unicode diacritic text attacks stronger** than random edits (Table 8): FUNSD **16.75 vs 7.31**; CORD **22.35 vs 7.13**.
  - **Transferability (Table 5):** PGD crafted on LayoutLMv3 transfers; e.g., LayoutLMv2 FUNSD **S6 PGD 55.54% drop**; GeoLayoutLM FUNSD **S6 PGD 53.56%**; ERNIE-Layout drops **<7%** even under PGD.

</details>

### 📖 PaddleOCR 3.0 Python/CLI Inference (PP-OCRv5 pipeline + deployment knobs)
**Reference Doc** · [source](https://paddlepaddle.github.io/PaddleOCR/en/ppocr/infer_deploy/python_infer.html)

*End-to-end PaddleOCR inference pipeline (detector + recognizer + optional orientation/unwarp/textline orientation), with concrete CLI/Python API usage and default-ish deployment settings (CPU/GPU, HPI).*

<details>
<summary>Key content</summary>

- **General OCR pipeline modules (mandatory/optional):** mandatory **text detection + text recognition**; optional **document image orientation classification**, **text image correction (unwarping/rectification)**, **text line orientation classification** (pipeline described near “General OCR pipeline…”).
- **Python API (PP-OCRv5):**
  - `from paddleocr import PaddleOCR`
  - `ocr = PaddleOCR(use_doc_orientation_classify=False, use_doc_unwarping=False, use_textline_orientation=False)`
  - `result = ocr.predict(input="test.png")`; per-result: `res.print()`, `res.save_to_img("output")`, `res.save_to_json("output")`.
- **Python API (PP-StructureV3):** `from paddleocr import PPStructureV3`; `pipeline = PPStructureV3(use_doc_orientation_classify=False, use_doc_unwarping=False)`; `output = pipeline.predict(input="test.png")`; save: JSON + Markdown.
- **CLI examples:** `paddleocr ocr -i test.png --use_doc_orientation_classify False ...`; PP-ChatOCRv4 doc: `paddleocr pp_chatocrv4_doc -i test.png -k number --qianfan_api_key ... --use_doc_orientation_classify False`.
- **High-Performance Inference (HPI) rationale:** enable `enable_hpi` to auto-select backend (Paddle Inference / OpenVINO / ONNX Runtime / TensorRT) + built-in multithreading/FP16; example speedups on **NVIDIA T4**: **PP-OCRv5_mobile_rec latency −73.1%**, **PP-OCRv5_mobile_det −40.4%**.
- **Benchmark rows (selected):**
  - Doc orientation model **PP-LCNet_x1_0_doc_ori**: **Top-1 99.06%**, size **7 MB**, GPU **2.62→0.59 ms** (Normal/HPI), CPU **3.24→1.19 ms**.
  - Detector **PP-OCRv5_server_det**: Hmean **83.8**, size **84.3 MB**, GPU **89.55→70.19 ms**, CPU **383.15 ms**.
  - Detector **PP-OCRv5_mobile_det**: Hmean **79.0**, size **4.7 MB**, GPU **10.67→6.36 ms**, CPU **57.77→28.15 ms**.
  - Recognizer **PP-OCRv5_server_rec**: avg acc **86.38%**, size **81 MB**, GPU **8.46→2.36 ms**, CPU **31.21 ms**.
  - Recognizer **PP-OCRv5_mobile_rec**: avg acc **81.29%**, size **16 MB**, GPU **5.43→1.46 ms**, CPU **21.20→5.32 ms**.
- **Mobile (Paddle-Lite) key parameters:** compile with `--with_cv=ON --with_extra=ON`; `paddle_lite_opt` outputs `.nb` (set `--optimize_out_type naive_buffer` for mobile). Example config values: `max_side_len 960`, `det_db_thresh 0.3`, `det_db_box_thresh 0.5`, `det_db_unclip_ratio 1.6`, `use_direction_classify 0`, `rec_image_height 48` (PP-OCRv3; PP-OCRv2 uses 32).

</details>

---

## Related Topics

- [[topics/rag-retrieval|RAG & Retrieval]]
- [[topics/vision-language-models|Vision Language Models]]
- [[topics/multimodal-fundamentals|Multimodal Fundamentals]]
- [[topics/contrastive-learning|Contrastive Learning]]
