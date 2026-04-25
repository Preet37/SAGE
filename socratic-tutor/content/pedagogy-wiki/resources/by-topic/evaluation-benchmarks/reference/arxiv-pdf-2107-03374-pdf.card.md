# Card: Unbiased pass@k for code functional correctness (HumanEval/Codex)
**Source:** https://arxiv.org/pdf/2107.03374.pdf  
**Role:** paper | **Need:** FORMULA_SOURCE  
**Anchor:** Primary-source definition + unbiased estimator + sampling protocol for pass@k (HumanEval-style)

## Key Content
- **Why pass@k (functional correctness) vs BLEU/match metrics (Sec. 2.1):** Many programs are functionally equivalent but text-different; unit-test passing matches how developers judge code. BLEU can overlap heavily between correct/incorrect solutions (Fig. 8), so BLEU improvements may not imply correctness.
- **pass@k definition + unbiased estimator (Eq. 1, Sec. 2.1):** For each task, generate **n ≥ k** samples, run unit tests, count **c** correct samples (c ≤ n). Unbiased estimator:
  \[
  \text{pass@}k := \mathbb{E}_{\text{problems}}\left[1 - \frac{\binom{n-c}{k}}{\binom{n}{k}}\right]
  \]
  where \(n\)=#samples, \(c\)=#passing samples, \(k\)=budget. Authors use **n=200**, **k≤100** to reduce variance vs naive “any of k” computation.
- **Numerically stable computation (Fig. 3):**
  - If \(n-c<k\): return 1.0  
  - Else: \(1 - \prod_{i=n-c+1}^{n}\left(1-\frac{k}{i}\right)\)
  - (Given as a stable numpy implementation.)
- **Bias warning:** Estimating pass@k as \(1-(1-\hat p)^k\) with \(\hat p=\) empirical pass@1 is **biased** (Appendix A).
- **HumanEval dataset (Sec. 2.2):** **164** hand-written Python function tasks; avg **7.7** unit tests/problem.
- **Key empirical pass rates (Table 1, HumanEval):** Codex-12B **pass@1 28.81%**, **pass@100 72.31%**; GPT-J 6B **11.62% / 27.74%**; GPT-Neo 2.7B **6.41% / 21.37%**; TabNine **2.58% / 7.59%**.
- **Sampling defaults:** nucleus sampling **top-p=0.95**; stop sequences include `\nclass`, `\ndef`, `\n#`, `\nif`, `\nprint`. Temperature tuned by k (e.g., optimal for 679M: **T*=0.2** for pass@1, **T*=0.8** for pass@100).

## When to surface
Use when students ask how to compute/estimate **pass@k**, why **n≥k** sampling is used, or how HumanEval-style code benchmarks report “best-of-k” success rates and avoid biased/high-variance estimates.