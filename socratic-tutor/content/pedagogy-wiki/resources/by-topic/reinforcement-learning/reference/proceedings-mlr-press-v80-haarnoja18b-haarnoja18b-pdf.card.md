# Card: Soft Actor-Critic (SAC) core equations & losses
**Source:** https://proceedings.mlr.press/v80/haarnoja18b/haarnoja18b.pdf  
**Role:** paper | **Need:** FORMULA_SOURCE  
**Anchor:** Soft Bellman backup + exact SAC losses (critic/value/policy), reparameterization gradient, temperature α role

## Key Content
- **Max-entropy RL objective (Eq. 1):**  
  \(J(\pi)=\sum_{t=0}^{T}\mathbb{E}_{(s_t,a_t)\sim\rho_\pi}\big[r(s_t,a_t)+\alpha\,\mathcal{H}(\pi(\cdot|s_t))\big]\).  
  α trades off reward vs entropy; standard RL recovered as \(\alpha\to 0\) (Sec. 3.2).
- **Soft policy evaluation backup (Eq. 2–3):**  
  \( \mathcal{T}^\pi Q(s_t,a_t)= r(s_t,a_t)+\gamma\,\mathbb{E}_{s_{t+1}\sim p}[V(s_{t+1})]\).  
  \( V(s_t)=\mathbb{E}_{a_t\sim\pi}[Q(s_t,a_t)-\log\pi(a_t|s_t)]\).
- **Soft policy improvement as KL projection (Eq. 4):**  
  \(\pi_{\text{new}}=\arg\min_{\pi'\in\Pi} D_{KL}\!\left(\pi'(\cdot|s_t)\,\|\,\frac{\exp(Q^{\pi_{\text{old}}}(s_t,\cdot))}{Z_{\pi_{\text{old}}}(s_t)}\right)\).
- **Practical SAC losses (Sec. 4.2):** with replay buffer \(D\), networks \(V_\psi, Q_\theta, \pi_\phi\).  
  **Value loss (Eq. 5):**  
  \(J_V(\psi)=\mathbb{E}_{s_t\sim D}\Big[\tfrac12\big(V_\psi(s_t)-\mathbb{E}_{a_t\sim\pi_\phi}[Q_\theta(s_t,a_t)-\log\pi_\phi(a_t|s_t)]\big)^2\Big]\).  
  **Q loss (Eq. 7–8):**  
  \(J_Q(\theta)=\mathbb{E}_{(s_t,a_t)\sim D}\big[\tfrac12(Q_\theta(s_t,a_t)-\hat Q(s_t,a_t))^2\big]\),  
  \(\hat Q=r(s_t,a_t)+\gamma\,\mathbb{E}_{s_{t+1}\sim p}[V_{\bar\psi}(s_{t+1})]\) using target value net \(V_{\bar\psi}\).
  **Policy objective (Eq. 10, 12):** minimize  
  \(J_\pi(\phi)=\mathbb{E}_{s_t\sim D}\!\left[D_{KL}\!\left(\pi_\phi(\cdot|s_t)\,\|\,\frac{\exp(Q_\theta(s_t,\cdot))}{Z_\theta(s_t)}\right)\right]\)  
  ⇒ via reparameterization \(a_t=f_\phi(\epsilon_t;s_t)\) (Eq. 11):  
  \(J_\pi(\phi)=\mathbb{E}_{s_t\sim D,\epsilon_t\sim\mathcal N}\big[\log\pi_\phi(f_\phi(\epsilon_t;s_t)|s_t)-Q_\theta(s_t,f_\phi(\epsilon_t;s_t))\big]\) (Eq. 12).  
  Gradient estimator given in Eq. 13.
- **Algorithm 1 workflow:** collect env transitions into replay \(D\); do gradient steps on \(J_V, J_Q\) (two Qs \(\theta_1,\theta_2\) to reduce positive bias), and \(J_\pi\); update target value params by EMA: \(\bar\psi \leftarrow \tau\psi+(1-\tau)\bar\psi\).
- **Defaults/empirical notes:** uses **two Q-functions** (Sec. 4.2). Target smoothing coefficient used across tasks: **\(\tau=0.005\)** (Sec. 5.2). Reward scaling acts like inverse temperature; sensitive (Sec. 5.2). Deterministic evaluation uses mean action (Sec. 5.2).

## When to surface
Use when students ask for SAC’s exact loss functions/targets, the “soft” Bellman backup/value definition, how entropy/temperature α enters, or how the reparameterized actor update is derived/implemented.