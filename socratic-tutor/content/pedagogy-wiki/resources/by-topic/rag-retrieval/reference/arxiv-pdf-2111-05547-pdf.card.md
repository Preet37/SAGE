# Card: DocVQA ICDAR 2021 — Tasks, Metrics, Leaderboards
**Source:** https://arxiv.org/pdf/2111.05547.pdf  
**Role:** benchmark | **Need:** EMPIRICAL_DATA  
**Anchor:** DocVQA 2021 task definitions + official results (ANLS/ANLSL/MAP)

## Key Content
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

## When to surface
Use when students ask about **DocVQA task setup**, **evaluation metrics for document VQA/retrieval**, or need **concrete benchmark scores** to justify RAG/retrieval + multimodal modeling choices.