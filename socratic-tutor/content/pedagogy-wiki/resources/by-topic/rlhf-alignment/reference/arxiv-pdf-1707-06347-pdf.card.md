# Card: PPO clipped objective & KL-penalty (trust-region-like stability)
**Source:** https://arxiv.org/pdf/1707.06347.pdf  
**Role:** paper | **Need:** FORMULA_SOURCE  
**Anchor:** Primary-source definition of PPO clipped surrogate objective + KL-penalty variant; motivation vs TRPO; empirical stability comparisons

## Key Content
- **Vanilla policy gradient objective (Eq. 2):**  
  \(L^{PG}(\theta)=\hat{\mathbb E}_t[\log \pi_\theta(a_t|s_t)\,\hat A_t]\). Multiple epochs on \(L^{PG}\) often cause destructively large updates (Sec. 2.1).
- **TRPO surrogate + KL constraint (Eq. 3–4):**  
  Maximize \(\hat{\mathbb E}_t\!\left[\frac{\pi_\theta(a_t|s_t)}{\pi_{\theta_{old}}(a_t|s_t)}\hat A_t\right]\)  
  s.t. \(\hat{\mathbb E}_t[KL(\pi_{\theta_{old}}(\cdot|s_t),\pi_\theta(\cdot|s_t))]\le \delta\).
- **KL-penalty form (Eq. 5, 8):**  
  \(L^{KLPEN}(\theta)=\hat{\mathbb E}_t\!\left[\frac{\pi_\theta(a_t|s_t)}{\pi_{\theta_{old}}(a_t|s_t)}\hat A_t-\beta\, KL(\pi_{\theta_{old}}(\cdot|s_t),\pi_\theta(\cdot|s_t))\right]\).  
  **Adaptive \(\beta\)** (Sec. 4): compute \(d=\hat{\mathbb E}_t[KL(\cdot)]\); if \(d<d_{targ}/1.5\), \(\beta\leftarrow\beta/2\); if \(d>d_{targ}\times1.5\), \(\beta\leftarrow 2\beta\).
- **Probability ratio (Sec. 3):** \(r_t(\theta)=\frac{\pi_\theta(a_t|s_t)}{\pi_{\theta_{old}}(a_t|s_t)}\), so \(r_t(\theta_{old})=1\).
- **Clipped surrogate objective (Eq. 7):**  
  \(L^{CLIP}(\theta)=\hat{\mathbb E}_t\left[\min\left(r_t(\theta)\hat A_t,\; \text{clip}(r_t(\theta),1-\epsilon,1+\epsilon)\hat A_t\right)\right]\).  
  Rationale: clipping removes incentive to push \(r_t\) outside \([1-\epsilon,1+\epsilon]\); min makes a pessimistic (lower-bound) surrogate; behaves like TRPO-style trust region while using first-order SGD/Adam.
- **Combined objective (Eq. 9):**  
  \(\hat{\mathbb E}_t[L^{CLIP}_t(\theta)-c_1 L^{VF}_t(\theta)+c_2 S[\pi_\theta](s_t)]\), with \(L^{VF}_t=(V_\theta(s_t)-V^{targ}_t)^2\).
- **PPO training loop (Alg. 1):** collect \(N\) actors × \(T\) steps with \(\pi_{\theta_{old}}\); compute advantages \(\hat A_t\); optimize surrogate for \(K\) epochs with minibatches \(M\le NT\); set \(\theta_{old}\leftarrow\theta\).
- **Empirical stability (Table 1, 7 MuJoCo tasks, 1M steps):** avg normalized score  
  - No clipping/penalty: **-0.39**  
  - Clipping \(\epsilon=0.2\): **0.82** (best among shown)  
  - Clipping \(\epsilon=0.1\): 0.76; \(\epsilon=0.3\): 0.70  
  - Adaptive KL \(d_{targ}=0.01\): 0.74 (worse than clip 0.2)
- **Default hyperparams (Table 3, MuJoCo):** \(T=2048\), Adam lr \(3\times10^{-4}\), epochs 10, minibatch 64, \(\gamma=0.99\), GAE \(\lambda=0.95\).  
  **Atari (Table 5):** \(T=128\), epochs 3, \(\gamma=0.99\), \(\lambda=0.95\), actors 8, \(\epsilon=0.1\times\alpha\), entropy \(c_2=0.01\), VF \(c_1=1\), lr \(2.5\times10^{-4}\times\alpha\) with \(\alpha\) annealed 1→0.

## When to surface
Use when students ask for the exact PPO objective(s), how PPO approximates trust-region constraints, or what empirical evidence shows clipping improves stability vs KL penalties / no constraint.