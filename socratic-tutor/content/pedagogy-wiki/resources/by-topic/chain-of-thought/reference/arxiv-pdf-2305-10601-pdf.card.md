# Card: Tree of Thoughts (ToT) — deliberate search over “thoughts”
**Source:** https://arxiv.org/pdf/2305.10601.pdf  
**Role:** paper | **Need:** EMPIRICAL_DATA, FORMULA_SOURCE  
**Anchor:** Empirical ToT gains (Game of 24, Creative Writing, Crosswords) + ToT search components (generate/evaluate/search; value/vote).

## Key Content
- **Core formulation (Sec. 3):** Problem solving as **search over a tree**.  
  - **State** \(s\): input + sequence of thoughts so far (partial solution).  
  - **Thought**: coherent text unit (size chosen per task: equation line / plan paragraph / crossword word).
- **Thought generation (Sec. 3):** from state \(s\), generate candidates \(T=\{t_i\}\) via LM prompting (i.i.d. sampling or sequential proposals conditioned on \(s\)).
- **State evaluation heuristics (Sec. 3):**
  - **Value:** \(V(s)\) from a value prompt → scalar (e.g., 1–10) or labels (e.g., **sure/maybe/impossible**) mapped to numeric scores; can sample multiple times and aggregate.
  - **Vote:** given frontier \(S\), sample votes to pick most promising state: \( \text{Vote}(S)\rightarrow s^\*\).
- **Search algorithms (Sec. 3):**
  - **BFS (Alg. 1):** keep top \(b\) states per depth step (beam-like). Used when depth is small and early pruning helps (Game of 24, Creative Writing).
  - **DFS (Alg. 2):** expand best-looking state; **prune** if \(V(s)<v_{\text{th}}\); **backtrack** on prune or completion. Used for Crosswords; step budget **100**.
- **Empirical results — Game of 24 (Sec. 4.1, 100 hard games):**  
  IO 7.3%; CoT 4.0%; CoT-SC (k=100) 9.0%; **ToT BFS b=1: 45%**; **ToT BFS b=5: 74%**; IO+Refine (k=10) 27%; IO best-of-100 33%; CoT best-of-100 49%.  
  Setup: 3 ToT steps (3 intermediate equations); evaluator labels sure/maybe/impossible; temperature **0.7**.
- **Creative Writing (Sec. 4.2, 100 inputs):** GPT-4 coherency score (1–10, avg of 5 evals): **ToT 7.56** vs IO 6.19 vs CoT 6.93; humans prefer ToT over CoT **41/100** (CoT over ToT 21/100). ToT: depth 2 (plan→passage), **5 votes** each step, breadth limit \(b=1\).
- **Crosswords (Sec. 4.3):** ToT DFS improves letter/word/game metrics; solves **4/20** games; oracle “+best state” solves **7/20**; ablations show **-prune worse**, **-backtrack word success 25%**.

## When to surface
Use when students ask why CoT fails on search/planning tasks, how ToT differs (value/vote + BFS/DFS + backtracking), or want concrete performance comparisons (e.g., Game of 24: 4% CoT vs 74% ToT).