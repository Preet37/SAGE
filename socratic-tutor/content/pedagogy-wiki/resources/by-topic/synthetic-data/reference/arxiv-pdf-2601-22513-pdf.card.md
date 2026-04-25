# Card: Why Self-Rewarding Works (Iterative SRLM Guarantees)
**Source:** https://arxiv.org/pdf/2601.22513.pdf  
**Role:** paper | **Need:** FORMULA_SOURCE  
**Anchor:** Formal assumptions + convergence/guarantee statements for iterative self-rewarding/DPO; when self-judging improves and when single-step can fail.

## Key Content
- **Setup (Section 3):** Policy is a conditional distribution \(\pi(y\mid x)\) over responses \(y\in\mathcal V^L\) given prompt \(x\sim\mathcal D\). Iterations \(t=0,1,\dots,T\): \(\pi_0\to \pi_1\to\cdots\to \pi_T\).
- **Self-reward (Eq. 1):** \(r_{\pi_t}(x,y)=\log \pi_t(y\mid x)\). Data per round: sample \(x\), generate two responses \(y^+,y^-\), define preference by reward difference \(\Delta r = r_{\pi_t}(x,y^+)-r_{\pi_t}(x,y^-)\).
- **KL-regularized improvement objective (Eq. 2):** choose \(\pi_{t+1}\) maximizing expected reward while staying close to reference \(\pi_t\) via KL regularization.
- **DPO-style loss (Eq. 3):** minimize logistic regression on pairwise preferences with reference \(\pi_t\):  
  \[
  \mathcal L_t(\pi)=\mathbb E\Big[\log\big(1+\exp(-\beta(\log\pi(y^+\!\mid x)-\log\pi(y^-\!\mid x)-(\log\pi_t(y^+\!\mid x)-\log\pi_t(y^-\!\mid x))))\big)\Big]
  \]
  Update operator (Eq. 4): \(\pi_{t+1}=\mathcal T(\pi_t)=\arg\min_{\pi\in\Pi}\mathcal L_t(\pi)\).
- **Policy condition number (Eq. 5, Section 4):**  
  \[
  \kappa(\pi)=\mathbb E_{x\sim\mathcal D}\Big[\frac{1}{\max_y \pi(y\mid x)}\Big]
  \]
  Large \(\kappa\) = diffuse/low-confidence policy → unstable self-rewarding.
- **Single-step limitation (Theorem 4.1):** For any one-step self-rewarding algorithm with sample budget \(n\), there exists a hard instance where failure probability is lower-bounded as a function of \(\kappa(\pi_0)\) (Eq. 6; \(\tilde\Omega(\cdot)\) hides logs). Near-uniform or low top-1 autoregressive policies make \(\kappa(\pi_0)\) scale like response-space size or \(\alpha^{-L}\), yielding constant failure when \(n\) is comparable.
- **Inference consequence (Proposition 4.3):** If the unique optimal sequence has probability \(\le 1/2\), greedy decoding can be guaranteed to miss it.
- **Iterative guarantees (Section 5):**
  - **Assumption 5.1 (Realizability):** optimal KL-regularized policy \(\pi^\star\in\Pi\).
  - **Stability constants (Def. 5.2):** minimum confidence \(\mu=\min_{t,x}\max_y \pi_t(y\mid x)\); margin \(\gamma=\min_{t,x}\big(\log\pi_t(y^\star\mid x)-\max_{y\ne y^\star}\log\pi_t(y\mid x)\big)\).
  - **Finite-sample bound (Theorem 5.3 + Remark 5.4):** failure probability after \(T\) rounds scales like a **statistical term** \(\tilde O(1/\sqrt n)\) times \((\text{stable floor depending on }\mu)+(\text{transient term depending on }\kappa(\pi_0)\text{ decaying exponentially in }T)\). For large \(T\), simplifies (up to logs/constants) to \(\tilde O(1/\sqrt n)\); initialization influence vanishes exponentially.
  - **Mechanism (Remark 5.5):** early iterations induce a **contraction mapping on \(\kappa(\pi_t)\)**: \(\kappa(\pi_t)\to \kappa_\infty\) with geometric decay of the initialization component.
  - **Iterations needed (Cor. 5.7):** \(T\) only needs to grow **logarithmically in \(\kappa(\pi_0)\)** to make initialization effects negligible; larger per-round \(n\) reduces required \(T\).

## When to surface
Use when students ask: “Why does iterative self-rewarding/DPO improve without humans?”, “When can self-judging fail?”, or “What are the formal convergence/sample-size/iteration guarantees and key assumptions (realizability, confidence, margin, condition number)?”