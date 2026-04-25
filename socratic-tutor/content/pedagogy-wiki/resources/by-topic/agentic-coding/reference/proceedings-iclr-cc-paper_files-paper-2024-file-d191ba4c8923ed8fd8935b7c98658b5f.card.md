# Card: RepoBench — repository-level code completion benchmark
**Source:** https://proceedings.iclr.cc/paper_files/paper/2024/file/d191ba4c8923ed8fd8935b7c98658b5f-Paper-Conference.pdf  
**Role:** benchmark | **Need:** EMPIRICAL_DATA  
**Anchor:** RepoBench task suite (RepoBench-R retrieval, RepoBench-C completion, RepoBench-P pipeline) + multi-file evaluation protocol

## Key Content
- **Motivation (Sec. 1):** Prior benchmarks are mostly single-file; RepoBench targets **repository-level** (multi-file) auto-completion with explicit cross-file context.
- **Data (Sec. 3.1–3.2):**
  - Train source: `github-code` (cutoff **Mar 16, 2022**); select repos with **32–128** Python/Java files.
  - Test source: newly crawled non-fork GitHub repos created **Feb 9, 2023–Aug 3, 2023** (to reduce leakage).
  - Parsed with **tree-sitter** focusing on **import statements** → identify cross-file modules, “cross-file lines,” and defining snippets.
  - Sizes: training repos **10,345 Python / 14,956 Java**; test repos **1,075 Python / 594 Java**.
- **Task settings (Sec. 3.3):**  
  - **XF-F:** mask *first* cross-file line (hardest). **XF-R:** mask random non-first cross-file line. **IF:** mask in-file line (no cross-file module).
- **Prompt construction (Fig. 1, App. A):** cross-file snippets (commented, with path) + in-file context (path + imports + preceding lines). Default in RepoBench-C: **max 30 preceding lines**.
- **RepoBench-R retrieval (Sec. 3.3, 4.1):**
  - Retrieval objective: top‑k by similarity  
    \[
    \arg\max_{i\in\{1..n\}}^{k} f(C[-m:], S_i)
    \]
    where \(C\)=in-file code, \(S_i\)=candidate snippet, \(n\)=#candidates, \(m\)=kept preceding lines (**baseline m=3**), \(f\)=similarity.
  - Candidates: Easy **5–9**, Hard **≥10**. Metric: **acc@k** (Easy: @1,@3; Hard: @1,@3,@5).
  - Key results (Table 2, Hard/Python acc@1): **InstructOR 19.10**, **UniXcoder 18.48**, **Jaccard 10.47**, Random **6.43**. (Easy/Python acc@1: InstructOR **28.22**, UniXcoder **27.09**.)
- **RepoBench-C completion (Sec. 3.3, 4.2):**
  - Autoregressive next-line probability (Eq. 1):  
    \[
    P(Y)=\prod_{i=1}^{n} P(y_i \mid y_{<i}, C_x, C_{in})
    \]
    \(C_x\)=cross-file context, \(C_{in}\)=in-file context.
  - Subsets: **2k** prompts ≤ **1,925 tokens** (for 2,048 limit); **8k** prompts ≤ **7,685 tokens**.
  - Metrics: **Exact Match (EM)**, **Edit Similarity**, **CodeBLEU**.
  - Key results (Table 3, 2k/Python EM): **CodeLlama‑34B 37.40** (best); Codex **31.31**. (2k/Java EM: Codex **42.47** best; CodeLlama‑34B **39.41**.)
- **RepoBench-P pipeline (Sec. 4.3):**
  - Pipeline probability (Eq. 2):  
    \[
    P(Y)=\prod_{i=1}^{n} P(y_i \mid y_{<i}, S_1..S_k, C_{in})
    \]
  - Constraints: minimum prompt tokens **12k (Python)** / **24k (Java)**; retrieval requires **≥10 candidates**.
  - Codex baseline config: reserve **1,600 tokens** for in-file; crop **60** preceding lines; fill to **6,400 tokens** with cross-file snippets.
  - Key result (Table 4, Python EM): in-file-only baseline **33.15** vs **Jaccard 36.46** vs **UniXcoder-L2H 37.11**; even **Random 34.94** improves → cross-file context helps; snippet **ordering matters** (higher-similarity nearer completion helps).

## When to surface
Use when students ask how coding agents/IDEs should manage **multi-file context**, how to evaluate retrieval+completion pipelines, or what **empirical evidence** shows about cross-file context length, retrieval quality, and snippet ordering.