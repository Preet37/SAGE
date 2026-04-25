## Core Definitions

**Multi-modal RAG (retrieval-augmented generation for visual documents).** Multi-modal RAG is a RAG setup where the retriever and/or generator can operate on *document images* (pages with layout, tables, charts, figures) rather than only plain text chunks; the goal is to retrieve relevant pages/regions and generate answers grounded in those visual documents. Lewis et al. define RAG as combining a parametric seq2seq model with a non-parametric memory accessed by a neural retriever, improving factuality and allowing provenance via retrieved context (https://arxiv.org/abs/2005.11401). In document settings, the “memory” is often page images (or OCR+layout representations) rather than Wikipedia passages.

**OCR-free document understanding.** OCR-free document understanding is an end-to-end approach that maps a raw document image directly to text/structured outputs without running an external OCR engine, avoiding OCR compute cost, language/domain inflexibility, and OCR error propagation. Donut is the canonical example: a Transformer visual encoder plus an autoregressive text decoder that generates a serialized target (JSON-like) directly from the image (https://arxiv.org/abs/2111.15664).

**Donut (OCR-free Document Understanding Transformer).** Donut is an end-to-end Transformer-only pipeline that uses a visual encoder (Swin Transformer) to encode the document image into embeddings and a text decoder (BART, initialized from multilingual BART) to autoregressively generate a token sequence that is invertible to structured JSON via special field delimiters (https://arxiv.org/abs/2111.15664).

**Visual document retrieval.** Visual document retrieval is retrieval where the indexed items are document images (often at page level) and the query is text; the system retrieves relevant pages based on cross-modal similarity without requiring OCR text as the primary representation. ColPali is a visual page retriever that embeds each page into multiple vectors (patch-level) and scores with late interaction (MaxSim-style) (https://arxiv.org/abs/2407.01449).

**ColPali.** ColPali is a multi-vector visual page retrieval model evaluated on the ViDoRe benchmark; it stores one vector per image patch (projected to 128-d) and uses late-interaction scoring between query token vectors and page patch vectors, avoiding OCR/layout/chunking and improving retrieval on visually complex pages (https://arxiv.org/abs/2407.01449).

**Late interaction (MaxSim) retrieval.** Late interaction retrieval encodes queries and documents independently into *sets* (bags) of contextualized embeddings and computes relevance with a lightweight interaction, typically summing over query tokens the maximum similarity to any document token/patch embedding. ColBERT defines this as \( \sum_i \max_j e_{q_i}\cdot e_{d_j} \) (https://arxiv.org/abs/2004.12832); ColPali applies the same idea to query tokens vs page patch vectors (https://arxiv.org/abs/2407.01449).

**DocVQA (Document Visual Question Answering).** DocVQA is the task of answering natural-language questions about document images; models typically use text, layout (bounding boxes), and image features, and many benchmarks are extractive (answers appear on the page). The ICDAR 2021 DocVQA competition defines multiple tasks (Single Document VQA, Document Collection VQA, Infographics VQA) and uses ANLS/ANLSL for scoring (https://arxiv.org/pdf/2111.05547.pdf). Hugging Face’s task page summarizes DocQA as taking (document, question) → answer (https://huggingface.co/tasks/document-question-answering).

**Structured data extraction (from documents).** Structured extraction is producing a machine-readable schema (fields/values, often JSON) from a document (e.g., invoice number, total, vendor). Donut frames classification, information extraction, and DocVQA as JSON prediction by generating a serialized target sequence with field delimiters that is invertible to JSON (https://arxiv.org/abs/2111.15664).

**Cross-modal retrieval.** Cross-modal retrieval retrieves items in one modality (document images/pages) using a query in another modality (text). In ColPali, text queries are embedded into multi-vectors and matched to page patch vectors via late interaction (https://arxiv.org/abs/2407.01449).

---

## Key Formulas & Empirical Results

### Late-interaction scoring (ColBERT / ColPali)
- **Formula (ColBERT MaxSim; also used by ColPali):**
  \[
  S_{q,d} := \sum_{i}\max_{j}\mathbf{e}_{q_i}\cdot \mathbf{e}_{d_j}^{\top}
  \]
  where \( \mathbf{e}_{q_i} \) are query token embeddings and \( \mathbf{e}_{d_j} \) are document token embeddings (https://arxiv.org/abs/2004.12832).
- **ColPali page scoring (same structure):**
  \[
  s(Q,D)=\sum_{i=1}^{|Q|}\max_{j\in[1,|D|]} q_i^\top d_j
  \]
  where \(Q\) is the set of query vectors and \(D\) is the set of page vectors (patch embeddings) (https://arxiv.org/abs/2407.01449).
- **Claim supported:** late interaction preserves fine-grained matching while enabling offline doc/page encoding and fast online scoring (https://arxiv.org/abs/2004.12832; https://arxiv.org/abs/2407.01449).

### DPR bi-encoder scoring + training objective (baseline RAG retriever math)
- **Similarity (dot product):**
  \[
  \text{sim}(q,p)=E_Q(q)^\top E_P(p)
  \]
  (https://aclanthology.org/2020.emnlp-main.550.pdf).
- **InfoNCE-style NLL loss:**
  \[
  \mathcal{L}=-\log \frac{e^{\text{sim}(q_i,p_i^+)}}{e^{\text{sim}(q_i,p_i^+)}+\sum_{j=1}^n e^{\text{sim}(q_i,p_{i,j}^-)}}
  \]
  (https://aclanthology.org/2020.emnlp-main.550.pdf).
- **In-batch negatives:** with batch size \(B\), similarity matrix \(S=QP^\top\) gives each question \(B-1\) negatives “for free” (https://aclanthology.org/2020.emnlp-main.550.pdf).

### Donut: structured output as generation + key defaults
- **Architecture:** image encoder (Swin) produces patch tokens \(\{\mathbf{z}_i\}_{i=1}^{n}\), decoder generates token sequence \((\mathbf{y}_i)_{i=1}^{m}\) (https://arxiv.org/abs/2111.15664).
- **Serialization:** output token sequence is 1–1 invertible to JSON using delimiters \([START_*],[END_*]\); malformed fields (e.g., missing end token) are treated as lost (https://arxiv.org/abs/2111.15664).
- **Defaults reported:** input resolution **2560×1920**, decoder max length **1536**, Adam LR initial **1e-5 to 1e-4** (https://arxiv.org/abs/2111.15664).
- **IE metric (TED-based accuracy):**
  \[
  \max\left(0, 1-\frac{\mathrm{TED}(\mathrm{pr},\mathrm{gt})}{\mathrm{TED}(\varnothing,\mathrm{gt})}\right)
  \]
  (https://arxiv.org/abs/2111.15664).

### ColPali / ViDoRe: retrieval quality + efficiency numbers
- **ViDoRe benchmark:** 10 tasks; includes DocVQA, InfoVQA, TAT-DQA, arXiVQA, TabFQuAD, plus practical corpora (Energy/Gov/Healthcare/AI/Shift) (https://arxiv.org/abs/2407.01449).
- **Key retrieval result (avg nDCG@5):** ColPali (+late interaction) **81.3** vs captioning+BGE-M3 **67.0**, OCR+BGE-M3 **66.1**, SigLIP **51.4** (https://arxiv.org/abs/2407.01449).
- **Index representation:** stores **one vector per image patch**, projected to **128-d**; memory **~154 KB/page** (https://arxiv.org/abs/2407.01449).
- **Token pooling:** pool factor 3 reduces vectors by **~66%** while keeping **~97%** performance (https://arxiv.org/abs/2407.01449).
- **Training details (as reported):** 118,695 query–page pairs; 1 epoch; bf16; LoRA; LR **1e-4**; batch **32**; query augmentation appends **5 `<unused0>` tokens** (https://arxiv.org/abs/2407.01449).

### DocVQA (ICDAR 2021): tasks + metrics + headline scores
- **Tasks:** Single Document VQA; Document Collection VQA (must output answers + evidence doc IDs); Infographics VQA (layout/visual/numerical reasoning) (https://arxiv.org/pdf/2111.05547.pdf).
- **Metrics:** ANLS for Single Doc + Infographics; ANLSL for Collection VQA (Hungarian matching for unordered sets); MAP for evidence retrieval (not used for ranking) (https://arxiv.org/pdf/2111.05547.pdf).
- **Leaderboard examples:** Single Doc VQA winner TILT **0.8705 ANLS**; Infographics VQA winner TILT **0.6120 ANLS**; human ~0.98 (https://arxiv.org/pdf/2111.05547.pdf).

### Grounded evaluation for DocVQA (SMuDGE)
- **Grounding distance (NMD):**
  \(d=\frac{|x_p-x_g|}{W}+\frac{|y_p-y_g|}{H}\) and grounding score \(G=\exp(-d)\) (https://arxiv.org/html/2503.19120v1).
- **Composite:** \( \text{SMuDGE}_\alpha = \alpha S + (1-\alpha)G\); recommended \(\alpha \approx 0.7\) from calibration analysis (https://arxiv.org/html/2503.19120v1).
- **Claim supported:** ANLS/NLS can reward hallucinations (e.g., digit overlap), so adding grounding changes rankings and relates to calibration/robustness (https://arxiv.org/html/2503.19120v1).

---

## How It Works

### A. Multi-modal RAG for document images (page-level retrieval → answer)
1. **Ingest documents**
   1) Convert PDFs to page images (page = retrieval unit in ViDoRe/ColPali framing) (https://arxiv.org/abs/2407.01449).  
   2) Store page IDs and metadata (doc ID, page number).
2. **Index pages (OCR-free visual retrieval path)**
   1) Encode each page image into a *set of patch vectors* (multi-vector representation).  
   2) Store vectors in an index; ColPali projects patch vectors to **128-d** and stores ~**154 KB/page** (https://arxiv.org/abs/2407.01449).
3. **Query-time retrieval**
   1) Encode the user query text into a *set of query vectors* (token-level).  
   2) Score each candidate page with late interaction:
      \[
      s(Q,D)=\sum_i \max_j q_i^\top d_j
      \]
      (https://arxiv.org/abs/2407.01449).  
   3) Return top‑K pages.
4. **Answering (generation / VQA)**
   - Feed the retrieved page image(s) + question to a document QA model (e.g., Donut fine-tuned for DocVQA, or other DocVQA-capable models per HF pipeline) (https://huggingface.co/tasks/document-question-answering; https://arxiv.org/abs/2111.15664).
5. **(Optional) Evidence + grounded evaluation**
   - If evaluating groundedness, compute SMuDGE by combining type-aware similarity with spatial grounding distance between predicted and GT spans (https://arxiv.org/html/2503.19120v1).

### B. OCR-free document understanding with Donut (image → JSON/text)
1. **Encode image**
   - Input image \( \mathbf{x}\in\mathbb{R}^{H\times W\times C} \) → encoder outputs patch embeddings \(\{\mathbf{z}_i\}_{i=1}^{n}\) (Swin Transformer) (https://arxiv.org/abs/2111.15664).
2. **Decode autoregressively**
   - Decoder (BART) generates tokens one-by-one conditioned on image embeddings + previous tokens (https://arxiv.org/abs/2111.15664).
3. **Training**
   - Use **teacher forcing**: feed ground-truth previous tokens during training (https://arxiv.org/abs/2111.15664).
   - Pretrain with pseudo-OCR objective: generate all texts in reading order (top-left → bottom-right) (https://arxiv.org/abs/2111.15664).
4. **Task prompting at inference**
   - Provide task-specific prompt tokens; generate output sequence (GPT-3-style prompting) (https://arxiv.org/abs/2111.15664).
5. **Parse to structure**
   - Use delimiters \([START_*],[END_*]\) to invert generated sequence into JSON; missing end tokens imply field loss (https://arxiv.org/abs/2111.15664).

### C. OCR-based document understanding (contrast path: LayoutLM-style)
1. Run OCR to get **words + bounding boxes** (HF LayoutLM docs emphasize external OCR is required) (https://huggingface.co/docs/transformers/model_doc/layoutlm).
2. Normalize boxes to 0–1000 coordinate scale (HF LayoutLM docs provide normalization function) (https://huggingface.co/docs/transformers/model_doc/layoutlm).
3. Feed tokens + boxes (and optionally image features in v2+) into a layout-aware Transformer (https://huggingface.co/docs/transformers/model_doc/layoutlmv2).

---

## Teaching Approaches

### Intuitive (no math)
- **“RAG, but the library is a stack of scanned pages.”** Instead of retrieving text paragraphs, you retrieve *pages as images* that likely contain the answer (tables, charts, forms). Then a document QA model reads those pages to answer.
- **OCR-free angle:** Donut skips the “transcribe then parse” pipeline; it learns to directly “read and write JSON” from pixels, which avoids OCR mistakes cascading into extraction.

### Technical (with math)
- **Retriever:** late interaction computes relevance by aligning each query token vector to its best-matching page patch vector and summing those best matches:
  \[
  s(Q,D)=\sum_i \max_j q_i^\top d_j
  \]
  (https://arxiv.org/abs/2407.01449; https://arxiv.org/abs/2004.12832).
- **Generator:** Donut models \(p(\text{JSON tokens}\mid \text{image})\) with an encoder–decoder Transformer and teacher forcing during training (https://arxiv.org/abs/2111.15664).

### Analogy-based
- **Late interaction = “highlight matching evidence.”** For each word in the question, you look for the *single most relevant* visual patch on the page (max), then add up how well the page covers all query words (sum). This mirrors how a human scans a page for multiple cues (title, column header, number formatting).
- **Donut = “dictation to a form.”** The model looks at the document and directly fills a structured form (JSON fields) rather than first typing out everything (OCR) and then re-reading it.

---

## Common Misconceptions

1. **“Multi-modal RAG just means the LLM can see images; retrieval is still text-only.”**  
   - **Why wrong:** ColPali is explicitly *visual page retrieval*—it indexes page images as multi-vector patch embeddings and retrieves without OCR/layout/chunking (https://arxiv.org/abs/2407.01449).  
   - **Correct model:** In multi-modal RAG, the *retriever itself* can be cross-modal (text query → image/page vectors), not only the generator.

2. **“OCR-free means the model doesn’t output text.”**  
   - **Why wrong:** Donut is OCR-free *in the pipeline*, but it still outputs text tokens—often a serialized JSON-like sequence—via an autoregressive decoder (https://arxiv.org/abs/2111.15664).  
   - **Correct model:** OCR-free = no external OCR engine; the model still generates text/structure.

3. **“Late interaction is basically the same as a single-vector embedding search.”**  
   - **Why wrong:** Late interaction uses *multiple vectors per query and per document/page* and scores with MaxSim aggregation \( \sum_i \max_j \cdot \) (https://arxiv.org/abs/2004.12832). Single-vector retrieval uses one vector per item and one similarity computation.  
   - **Correct model:** Late interaction preserves token/patch-level matching signals at retrieval time, at the cost of more storage/compute than single-vector.

4. **“DocVQA evaluation (ANLS) guarantees the model is grounded.”**  
   - **Why wrong:** SMuDGE argues ANLS/NLS can reward hallucinations due to surface similarity (e.g., digit overlap) and introduces a grounding component based on spatial proximity (https://arxiv.org/html/2503.19120v1).  
   - **Correct model:** ANLS measures string similarity; groundedness requires evidence alignment (e.g., span localization).

5. **“Document Collection VQA is just like Single Document VQA but with more pages.”**  
   - **Why wrong:** In DocVQA 2021, Collection VQA requires outputting **answers + positive evidence doc IDs**, and uses ANLSL plus MAP for evidence retrieval (https://arxiv.org/pdf/2111.05547.pdf).  
   - **Correct model:** It’s a joint retrieval+answering task with explicit evidence requirements.

---

## Worked Examples

### Example 1: Donut-style structured extraction as JSON generation (conceptual target format)
**Goal:** show how to represent extraction as a sequence that is invertible to JSON using delimiters (Donut) (https://arxiv.org/abs/2111.15664).

**Suppose schema:** `{ "invoice_id": ..., "total": ... }`

**Target sequence (illustrative of Donut’s delimiter idea):**
```
[START_invoice_id] INV-10023 [END_invoice_id]
[START_total] 20,000$ [END_total]
```

**Invert to JSON:**
```json
{"invoice_id":"INV-10023","total":"20,000$"}
```

**Tutor moves mid-conversation**
- Ask student: “What happens if `[END_total]` is missing?”  
  Donut notes malformed fields can be treated as *lost* (https://arxiv.org/abs/2111.15664).

### Example 2: Late-interaction scoring with tiny vectors (hand-computable)
**Goal:** make MaxSim concrete (ColBERT/ColPali) (https://arxiv.org/abs/2004.12832; https://arxiv.org/abs/2407.01449).

Let query have 2 token vectors \(q_1,q_2\). Page has 3 patch vectors \(d_1,d_2,d_3\). Similarities (dot products) are:

|        | d1  | d2  | d3  |
|--------|-----|-----|-----|
| q1     | 0.2 | 0.9 | 0.1 |
| q2     | 0.4 | 0.3 | 0.8 |

MaxSim per query token:
- For \(q_1\): \(\max(0.2,0.9,0.1)=0.9\)
- For \(q_2\): \(\max(0.4,0.3,0.8)=0.8\)

Score:
\[
s(Q,D)=0.9+0.8=1.7
\]

**Interpretation:** the page is good because it has *some patch* that matches each query token strongly; it doesn’t require the same patch to match everything.

### Example 3: Hugging Face DocQA pipeline call (runnable skeleton)
From HF task page (https://huggingface.co/tasks/document-question-answering):

```python
from transformers import pipeline
from PIL import Image

pipe = pipeline("document-question-answering",
                model="naver-clova-ix/donut-base-finetuned-docvqa")

image = Image.open("your-document.png")
question = "What is the purchase amount?"

pipe(image=image, question=question)
# [{'answer': '20,000$'}]
```

**Tutor note:** This demonstrates the *DocVQA-style* interface: (image, question) → answer string. It does not itself implement retrieval; in multi-modal RAG you’d run retrieval first, then call this on retrieved pages.

---

## Comparisons & Trade-offs

| Choice | What it indexes | Retrieval scoring | Strengths (per sources) | Costs / Risks (per sources) | When to choose |
|---|---|---|---|---|---|
| OCR-based DU + text retrieval (LayoutLM-style pipeline) | OCR tokens + boxes (and sometimes image features) | Often text embedding / BM25 / hybrid (not detailed in sources) | Mature tooling; explicit text tokens + layout boxes (HF LayoutLM docs) (https://huggingface.co/docs/transformers/model_doc/layoutlm) | Requires OCR; pipeline complexity; OCR errors propagate (Donut motivation) (https://arxiv.org/abs/2111.15664) | When OCR is reliable and you need explicit text spans/boxes for downstream systems |
| OCR-free understanding (Donut) | Raw page images | Generation (image→tokens) | Avoids OCR compute + error propagation; outputs structured JSON via serialization (https://arxiv.org/abs/2111.15664) | Needs model trained for task/schema; output can be malformed (field loss) (https://arxiv.org/abs/2111.15664) | When you want end-to-end extraction/QA and can fine-tune or use strong pretrained checkpoints |
| Visual page retrieval (ColPali) | Page images as patch vectors | Late interaction \( \sum_i \max_j q_i^\top d_j \) (https://arxiv.org/abs/2407.01449) | Strong retrieval on visually complex tasks; avoids OCR/layout/chunking; high nDCG@5 (81.3 avg) (https://arxiv.org/abs/2407.01449) | Higher storage (multi-vector; ~154 KB/page) (https://arxiv.org/abs/2407.01449) | When retrieval must work on tables/figures/layout-heavy pages and OCR is brittle or expensive |
| Single-vector dense retrieval (DPR-style) | Text passages | Dot product \(E_Q(q)^\top E_P(p)\) (https://aclanthology.org/2020.emnlp-main.550.pdf) | Simple, fast ANN; standard RAG retriever math (https://aclanthology.org/2020.emnlp-main.550.pdf) | Loses token-level matching; depends on good chunking/OCR in doc setting | When you have clean text chunks and need maximum throughput |

**Selection heuristic (grounded in sources):**
- If OCR errors/latency are a major bottleneck, Donut’s motivation is explicitly to remove OCR cost and error propagation (https://arxiv.org/abs/2111.15664).
- If retrieval quality on visually complex pages is the bottleneck, ColPali reports large gains over OCR/captioning baselines on ViDoRe (https://arxiv.org/abs/2407.01449).

---

## Prerequisite Connections

- **Basic RAG concept (parametric + non-parametric memory).** Needed to understand why retrieval exists at all and how it conditions generation (https://arxiv.org/abs/2005.11401).
- **Dense retrieval training (bi-encoders, in-batch negatives).** Helps when students ask “how is the retriever trained?” (https://aclanthology.org/2020.emnlp-main.550.pdf).
- **Transformer encoder–decoder generation + teacher forcing.** Needed to understand Donut’s training/inference mechanics (https://arxiv.org/abs/2111.15664).
- **DocVQA task framing + metrics (ANLS/ANLSL).** Needed to interpret benchmark claims and evaluation pitfalls (https://arxiv.org/pdf/2111.05547.pdf; https://arxiv.org/html/2503.19120v1).

---

## Socratic Question Bank

1. **If you remove OCR from the pipeline, what *new* problem must the model solve that OCR used to solve explicitly?**  
   *Good answer:* It must learn to map pixels to text/structure directly (reading + parsing), as Donut does with image encoder + autoregressive decoder (https://arxiv.org/abs/2111.15664).

2. **In late interaction \( \sum_i \max_j q_i^\top d_j \), what does the “max over \(j\)” buy you compared to averaging similarities?**  
   *Good answer:* Each query token can latch onto its best matching patch/token, preserving sparse evidence matching (https://arxiv.org/abs/2004.12832).

3. **Why might ANLS give partial credit to a wrong numeric answer, and what does SMuDGE add to address that?**  
   *Good answer:* Surface similarity can be high for similar strings/digits; SMuDGE adds grounding via spatial distance and type-aware numeric matching (https://arxiv.org/html/2503.19120v1).

4. **What is the retrieval unit in ColPali/ViDoRe, and why does that matter for indexing and evaluation?**  
   *Good answer:* A *page* is the document; affects memory (~154 KB/page) and retrieval metrics (nDCG@5, etc.) (https://arxiv.org/abs/2407.01449).

5. **If a Donut output is missing an end delimiter for a field, what’s the practical consequence?**  
   *Good answer:* That field is treated as lost; parsing may rely on regex but malformed structure reduces extraction reliability (https://arxiv.org/abs/2111.15664).

6. **How is Document Collection VQA different from Single Document VQA in what the system must output?**  
   *Good answer:* Must output answers plus evidence doc IDs; evaluated with ANLSL and MAP for evidence (https://arxiv.org/pdf/2111.05547.pdf).

7. **What trade-off does ColPali make to get higher retrieval quality than single-vector baselines?**  
   *Good answer:* Stores many vectors per page (patch-level), increasing memory (~154 KB/page) but improving nDCG@5 (https://arxiv.org/abs/2407.01449).

8. **Where can retrieval be inserted in a DocVQA pipeline, and what changes if you add it?**  
   *Good answer:* Before QA: retrieve top-K pages, then run DocQA on those pages; changes from single-image QA to collection QA / multi-page answering (DocVQA task distinction) (https://arxiv.org/pdf/2111.05547.pdf).

---

## Likely Student Questions

**Q: What’s the exact late-interaction scoring equation used by ColPali?** → **A:** \( s(Q,D)=\sum_{i=1}^{|Q|}\max_{j} q_i^\top d_j \), where \(Q\) is the set of query vectors and \(D\) is the set of page vectors (patch embeddings) (https://arxiv.org/abs/2407.01449).

**Q: How does Donut avoid OCR, mechanically?** → **A:** It uses a Transformer visual encoder (Swin) to encode the image into embeddings and an autoregressive text decoder (BART) to generate the target token sequence directly from the image; no external OCR step is used (https://arxiv.org/abs/2111.15664).

**Q: How does Donut represent structured extraction targets?** → **A:** As a token sequence that is 1–1 invertible to JSON using special delimiters \([START_*],[END_*]\); missing end tokens imply the field is lost (https://arxiv.org/abs/2111.15664).

**Q: What are Donut’s reported default-ish input/output sizes?** → **A:** Experiments report input resolution **2560×1920** and decoder max length **1536** (https://arxiv.org/abs/2111.15664).

**Q: What’s the main empirical retrieval gain of ColPali over OCR/captioning baselines?** → **A:** On ViDoRe, average nDCG@5 is **81.3** for ColPali (+late interaction) vs **67.0** for captioning+BGE-M3 and **66.1** for OCR+BGE-M3 (https://arxiv.org/abs/2407.01449).

**Q: How big is a ColPali page representation?** → **A:** It stores one vector per image patch projected to **128-d**, with reported memory **~154 KB/page** (https://arxiv.org/abs/2407.01449).

**Q: What metrics does DocVQA 2021 use?** → **A:** ANLS for Single Document VQA and Infographics VQA; ANLSL for Document Collection VQA (Hungarian matching for unordered sets); MAP for evidence retrieval (not used for ranking) (https://arxiv.org/pdf/2111.05547.pdf).

**Q: Why isn’t ANLS enough to measure grounded DocVQA performance?** → **A:** SMuDGE argues ANLS/NLS can reward hallucinations via surface similarity; it adds a grounding score based on spatial distance between predicted and GT spans and combines it with type-aware similarity \( \text{SMuDGE}_\alpha=\alpha S+(1-\alpha)G \) (https://arxiv.org/html/2503.19120v1).

---

## Available Resources

### Videos
- [Intro to Large Language Models](https://www.youtube.com/watch?v=zjkBMFhNj_g) — **Surface when:** a student asks “why do we need retrieval at all?” or needs intuition for RAG as “external memory.”

### Articles & Tutorials
- [Hugging Face — Document Question Answering task page](https://huggingface.co/tasks/document-question-answering) — **Surface when:** student asks “what does the DocVQA interface look like in code?” or “which models can I call with (image, question)?”
- [Hugging Face Docs — LayoutLM](https://huggingface.co/docs/transformers/model_doc/layoutlm) — **Surface when:** student asks “how do OCR tokens + bounding boxes get fed into a model?” or needs bbox normalization details.
- [Hugging Face Docs — LayoutLMv2](https://huggingface.co/docs/transformers/model_doc/layoutlmv2) — **Surface when:** student asks “what changed from LayoutLM to v2?” or wants the multimodal (text+layout+image) framing.
- [Lewis et al. — Retrieval-Augmented Generation](https://arxiv.org/abs/2005.11401) — **Surface when:** student asks for the canonical definition of RAG or the two RAG formulations (same passages vs per-token retrieval).
- [Pinecone — Retrieval Augmented Generation](https://www.pinecone.io/learn/retrieval-augmented-generation/) — **Surface when:** student asks for a practical, non-paper explanation of hallucination motivation and why RAG improves trust via citations.

---

## Visual Aids

![Self-Ask: LLM decomposes questions and queries external search. (Press et al. 2022)](/api/wiki-images/rag-retrieval/images/lilianweng-posts-2023-03-15-prompt-engineering_001.png)  
**Show when:** student confuses “retrieval augmentation” with “just prompting”; use to illustrate explicit query-to-tool/retrieval steps as part of reasoning.

---

## Key Sources

- [Donut: OCR-free Document Understanding Transformer](https://arxiv.org/abs/2111.15664) — definitive OCR-free end-to-end doc understanding + JSON serialization details and defaults.
- [ColPali + ViDoRe](https://arxiv.org/abs/2407.01449) — core reference for OCR-free *visual page retrieval* with late interaction and benchmark/efficiency numbers.
- [ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction](https://arxiv.org/abs/2004.12832) — canonical late-interaction (MaxSim) definition and rationale.
- [ICDAR 2021 DocVQA competition report](https://arxiv.org/pdf/2111.05547.pdf) — authoritative task definitions and official metrics (ANLS/ANLSL/MAP).
- [SMuDGE grounded evaluation for Document VQA](https://arxiv.org/html/2503.19120v1) — groundedness-sensitive evaluation and why surface metrics can mis-rank hallucinations.