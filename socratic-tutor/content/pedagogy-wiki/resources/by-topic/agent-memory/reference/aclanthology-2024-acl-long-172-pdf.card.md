# Card: LongBench — Task taxonomy & long-context baselines
**Source:** https://aclanthology.org/2024.acl-long.172.pdf  
**Role:** benchmark | **Need:** EMPIRICAL_DATA  
**Anchor:** 6-category / 21-task taxonomy + quantitative long-context performance baselines (LongBench, LongBench-E) + effects of truncation & context compression

## Key Content
- **Problem formalization (Sec. 3.1):** Given **(I, C)** → output **A**, where **I** (input) and **A** (answer) are short; **C** is long (thousands of tokens). (Task-specific instantiations in Table 7.)
- **Benchmark composition:** **21 datasets across 6 categories** (Single-Doc QA, Multi-Doc QA, Summarization, Few-shot Learning, Synthetic, Code). **4,750** test instances. Avg length: **6,711 words (EN)** / **13,386 chars (ZH)**.
- **Datasets & metrics (Table 1):** QA uses **F1** (most) / **ROUGE-L** (DuReader); Summarization uses **ROUGE-L**; Few-shot uses **Accuracy (CLS)** / **F1** / **ROUGE-L**; Synthetic uses **Accuracy (EM)**; Code uses **Edit Sim**.
- **Truncation rule when input length L > model max M (Sec. 4.1):** truncate **from the middle**:  
  **S₁:L → [S₁:⌊M/2⌋ ; S_{L-⌊M/2⌋-1:L}]** (keep beginning + end).
- **Model baselines (Tables 2–3, Overall-All):** GPT-3.5-Turbo-16k **44.7**; ChatGLM2-6B-32k **41.4**; Vicuna-16k **30.5**; LongChat-32k **31.6**; Llama2-4k **26.8**.
- **LongBench-E length robustness (Fig. 3):** relative drop from **0–4k → 8k+**: ChatGLM2-6B-32k **−4%**, LongChat-32k **−7%**, GPT-3.5-16k **−17%**.
- **Context compression (Sec. 4.2):** Retrieval pipeline: chunk size **M=200 or 500** words/chars; take **top-N=7 (M=200)** or **top-N=3 (M=500)**; retrievers: **ada-002**, **Contriever**, **BM25**. Best retrieval improves **Llama2-4k by +21%**, but GPT-3.5-16k **−2%**, ChatGLM2-32k **−5%** (Table 4). Summarization-based compression generally hurts (Table 5; only helps VCSUM).
- **Memorization check (Sec. 4.3, Table 6):** evaluate **w/o context** vs with context; ∆score indicates reliance on context (e.g., GPT-3.5 NarrativeQA **4.7→23.6 (+18.9)**; MultiFieldQA-zh **10.9→61.2 (+50.3)**).

## When to surface
Use when students ask how to **evaluate long-context/memory methods**, compare **sliding-window vs retrieval/summarization**, or need **numeric baselines** and **length-robustness evidence** for long-context handling.