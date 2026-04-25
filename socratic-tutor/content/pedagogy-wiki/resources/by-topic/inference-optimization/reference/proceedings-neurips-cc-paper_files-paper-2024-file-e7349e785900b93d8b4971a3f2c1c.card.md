# Card: Speculative Decoding—Expected Rejections & Optimality (TV-distance)
**Source:** https://proceedings.neurips.cc/paper_files/paper/2024/file/e7349e785900b93d8b4971a3f2c1cefe-Paper-Conference.pdf  
**Role:** paper | **Need:** CONCEPT_EXPLAINER  
**Anchor:** Formal correctness + optimality for speculative decoding; exact expected rejections formula in terms of draft/target distributions (TV distance).

## Key Content
- **Speculative Decoding acceptance/rejection (Alg. 1):** draft token \(\tilde x_t \sim p_t(\cdot\mid x_{1:n-1},\tilde x_{n:t-1})\). Accept with  
  \[
  b_t(\tilde x_t)=\min\left\{1,\frac{q_t(\tilde x_t)}{p_t(\tilde x_t)}\right\}
  \]
  If rejected, sample \(x_n \sim r(q_t-p_t)_+(\cdot)\), i.e. normalized \(\max(0,q-p)\).
- **Runtime proxy:** under Assumption 1 (draft cost negligible; one parallel “oracle call” for target logits costs \(O(1)\)), **#oracle calls = #rejections**, so **acceleration** \(\approx T/\#\text{rejections}\).
- **Exact expected rejections (Thm. 1, Sec. 3):** with \(R_n\in\{0,1\}\) rejection indicator and \(N_{\text{rej}}=\sum_{n=1}^T R_n\),
  \[
  \mathbb E[N_{\text{rej}}]=\sum_{n=1}^T \mathbb E_{x_{1:n-1}\sim q}\Big[\mathrm{TV}\big(p_n(\cdot\mid x_{1:n-1}),\,q_n(\cdot\mid x_{1:n-1})\big)\Big].
  \]
  Implications: if TV=0 always ⇒ accel \(=T\); if TV=1 always ⇒ accel \(=1\).
- **Correctness/unbiasedness (Thm. 1):** output joint distribution matches target: \(P_{\text{SD}}(x_{1:T})=q(x_{1:T})\).
- **Optimality among unbiased rejection-based decoders (Thm. 2):**
  \[
  \inf_{A\in\mathcal F}\mathbb E_A[N_{\text{rej}}]\ \ge\ \sum_{n=1}^T \mathbb E_{x_{1:n-1}\sim q}[\mathrm{TV}(p_n,q_n)],
  \]
  matching SD’s value ⇒ cannot reduce rejections by changing \(b_t,P_t\) without bias/extra info.
- **Empirical check (Fig. 2a):** nonstationary Markov-chain sim, \(T=50\): theoretical \(\mathbb E[N_{\text{rej}}]=16.41\); observed converges to 16.41; accel \(50/16.41=3.05\).

## When to surface
Use when students ask how speculative decoding speedup depends on draft/target mismatch, why TV distance appears, or whether any unbiased variant can beat SD’s rejection rate.