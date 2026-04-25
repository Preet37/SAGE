# Card: KILT unified evaluation w/ provenance (RAG benchmark)
**Source:** https://discovery.ucl.ac.uk/id/eprint/10129948/1/Rockta%CC%88schel_2021.naacl-main.200.pdf  
**Role:** benchmark | **Need:** EMPIRICAL_DATA  
**Anchor:** Benchmark tables + unified evaluation protocol tying task scores to retrieval provenance (evidence attribution) with concrete retrieval metrics

## Key Content
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

## When to surface
Use when students ask how to **evaluate RAG/agent retrieval with evidence attribution**, compare **retrieval vs task accuracy**, or need **standard retrieval metrics (R-precision/Recall@k) and “only-if-evidence” scoring** for grounded generation.