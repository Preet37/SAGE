# Card: SWE-bench Verified (human-validated SWE-bench subset)
**Source:** https://openai.com/index/introducing-swe-bench-verified/  
**Role:** benchmark | **Need:** EMPIRICAL_DATA  
**Anchor:** Defines SWE-bench Verified (500 human-filtered SWE-bench instances) and reports verified performance comparisons + rationale for filtering.

## Key Content
- **What SWE-bench evaluates (workflow):**
  - Input to agent: **GitHub issue text (“problem statement”) + repository codebase**; **tests are hidden**.
  - Output: a **patch** (multi-file edits allowed) intended to fix the issue.
  - Scoring requires **both**:
    - `FAIL_TO_PASS` tests: **fail before** PR solution, **pass after**; passing implies the issue is solved.
    - `PASS_TO_PASS` tests: pass before/after; passing implies no regressions.
- **Why Verified was created (design rationale):** Original SWE-bench can **systematically underestimate** capability due to:
  1) overly specific / unrelated unit tests rejecting valid solutions,  
  2) underspecified issue descriptions,  
  3) unreliable environment setup causing failures independent of solution.
- **SWE-bench Verified definition & construction (procedure):**
  - Human annotation campaign: **93 Python-experienced developers**.
  - Annotated **1,699 random SWE-bench test samples**; **each sample labeled 3×**.
  - Two main criteria labeled on **severity scale {0,1,2,3}**: underspecification; unfair `FAIL_TO_PASS` tests.
  - **Ensembling rule:** take **max severity** across 3 annotators.
  - **Filter rule:** discard any sample where either criterion has **ensemble ≥ 2**, or “other major issues” flagged.
  - Final dataset: **500 non-problematic samples**; includes difficulty slicing from released annotations: **easy = 196 (<15 min)**, **hard = 45 (>1 hr)**.
- **Key empirical results:**
  - **68.3%** of SWE-bench samples filtered out (underspecification, unfair tests, or other issues).
  - Flag rates: **38.3%** underspecified problem statements; **61.1%** unfair unit tests.
  - Difficulty estimate (original SWE-bench, from 1,699-sample estimate): **77.8%** of samples **< 1 hour**.
  - Performance: **GPT‑4o = 33.2%** solve rate on **SWE-bench Verified** (model `gpt-4o-2024-05-13`); vs **16%** on original SWE-bench (best scaffold reported).  
  - Scaffold sensitivity example (SWE-bench Lite): **GPT‑4 ranges 2.7% → 28.3%** depending on scaffold (early RAG vs CodeR).
- **Evaluation reliability improvement:** new **Docker/containerized harness** for easier, more reliable evaluation.

## When to surface
Use when students ask how agentic coding systems are **empirically evaluated**, why SWE-bench scores can be misleading, or what **Verified** changes (filtering rules, dataset size, and headline solve rates).