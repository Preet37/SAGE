# Card: KILT unified benchmark + provenance-aware evaluation
**Source:** https://aclanthology.org/2021.naacl-main.200.pdf  
**Role:** benchmark | **Need:** EMPIRICAL_DATA  
**Anchor:** KILT task suite + unified evaluation protocol (downstream + retrieval + provenance-gated “KILT scores”)

## Key Content
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

## When to surface
Use when students ask how to **evaluate RAG/agent retrieval quality**, how to **score answers only when grounded**, or what **retrieval metrics (R-Prec/Recall@k) and provenance workflows** look like in a standard benchmark.