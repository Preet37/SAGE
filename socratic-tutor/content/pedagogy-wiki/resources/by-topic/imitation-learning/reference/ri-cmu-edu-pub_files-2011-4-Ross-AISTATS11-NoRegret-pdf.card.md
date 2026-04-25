# Card: DAgger no-regret reduction (Ross et al., AISTATS’11)
**Source:** https://www.ri.cmu.edu/pub_files/2011/4/Ross-AISTATS11-NoRegret.pdf  
**Role:** paper | **Need:** FORMULA_SOURCE  
**Anchor:** Full theorem statements/proofs; Algorithm 3.1 DAgger; bounds linking policy performance to online-learning regret + expert loss

## Key Content
- **State distributions & cost (Sec. 2):**  
  - \(d_t^\pi\): state distribution at time \(t\) when executing \(\pi\) from steps \(1..t-1\).  
  - \(d^\pi=\frac1T\sum_{t=1}^T d_t^\pi\).  
  - Immediate cost \(C(s,a)\in[0,1]\); \(C^\pi(s)=\mathbb E_{a\sim\pi(s)}[C(s,a)]\).  
  - Total cost \(J(\pi)=\sum_{t=1}^T \mathbb E_{s\sim d_t^\pi}[C^\pi(s)]=T\,\mathbb E_{s\sim d^\pi}[C^\pi(s)]\).
- **Imitation objective (Eq. 1):** \(\hat\pi=\arg\min_{\pi\in\Pi}\mathbb E_{s\sim d^\pi}[\ell(s,\pi)]\) (non-i.i.d. due to distribution shift).
- **Behavior cloning failure (Thm 2.1):** if \(\mathbb E_{s\sim d^{\pi^*}}[\ell(s,\pi)]=\epsilon\) (0-1 or upper bound), then  
  \(J(\pi)\le J(\pi^*)+T^2\epsilon\) (quadratic compounding).
- **Forward-training-style guarantee (Thm 2.2):** if \(\mathbb E_{s\sim d^\pi}[\ell(s,\pi)]=\epsilon\) and expert disadvantage bound  
  \(Q^{\pi^*}_{T-t+1}(s,a)-Q^{\pi^*}_{T-t+1}(s,\pi^*)\le u\), then \(J(\pi)\le J(\pi^*)+uT\epsilon\).
- **DAgger procedure (Alg. 3.1):** iterate \(i=1..N\): execute mixed policy \(\pi_i=\beta_i\pi^*+(1-\beta_i)\hat\pi_i\); collect visited states labeled by expert \(D_i=\{(s,\pi^*(s))\}\); aggregate \(D\leftarrow D\cup D_i\); train \(\hat\pi_{i+1}\) on \(D\). Return best \(\hat\pi_i\) on validation. Default often \(\beta_i=\mathbb I(i=1)\).
- **No-regret link (Eq. 3, Sec. 4):** online regret  
  \(\frac1N\sum_{i=1}^N \ell_i(\pi_i)-\min_{\pi\in\Pi}\frac1N\sum_{i=1}^N \ell_i(\pi)\le \gamma_N\), \(\gamma_N\to0\); use \(\ell_i(\pi)=\mathbb E_{s\sim d^{\pi_i}}[\ell(s,\pi)]\).
- **Distribution mismatch lemma (Lemma 4.1):** \(\|d^{\pi_i}-d^{\hat\pi_i}\|_1\le 2T\beta_i\).
- **Core guarantee (Thm 4.1):** \(\exists \hat\pi\in\{\hat\pi_1.. \hat\pi_N\}\):  
  \(\mathbb E_{s\sim d^{\hat\pi}}[\ell(s,\hat\pi)]\le \epsilon_N+\gamma_N+\frac{2\ell_{\max}}{N}\Big[n_\beta+T\sum_{i=n_\beta+1}^N\beta_i\Big]\),  
  where \(\epsilon_N=\min_{\pi\in\Pi}\frac1N\sum_i \mathbb E_{s\sim d^{\pi_i}}[\ell(s,\pi)]\), \(n_\beta=\max\{n:\beta_n>1/T\}\).
- **DAgger performance bounds (Thm 3.1–3.2):** if \(N=\tilde O(T)\), \(\exists \hat\pi\) with \(\mathbb E_{s\sim d^{\hat\pi}}[\ell]\le \epsilon_N+O(1/T)\); if \(\ell\) upper-bounds 0-1 vs expert, then \(J(\hat\pi)\le J(\pi^*)+uT\epsilon_N+O(1)\) (needs \(N=\tilde O(uT)\)).
- **Finite-sample (Thm 4.2):** add generalization term \(+\ell_{\max}\sqrt{\frac{2\log(1/\delta)}{mN}}\) when using \(m\) trajectories/iter.
- **Empirics (Sec. 5):**
  - Super Tux Kart: linear ridge regression, \(\lambda=10^{-3}\), 20 iters, ~1000 pts/iter; DAgger with \(\beta_i=\mathbb I(i=1)\) reaches **0 falls/lap after 15 iters**, while SMILe (\(\alpha=0.1\)) still ~**2 falls/lap** after 20; supervised stagnates.
  - Super Mario: 4 linear SVMs, \(\lambda=10^{-4}\), 20 iters, 5000 pts/iter; DAgger best reported **3030** avg distance (with \(\beta_i=0.5^{i-1}\)), vs **2980** (\(\beta_i=\mathbb I(i=1)\)); supervised low/stagnant.

## When to surface
Use for questions about **distribution shift/compounding errors in behavior cloning**, the **DAgger algorithm steps**, and **formal guarantees** connecting imitation learning performance to **no-regret online learning** (regret \(\gamma_N\), \(\epsilon_N\), and \(uT\epsilon\) bounds).