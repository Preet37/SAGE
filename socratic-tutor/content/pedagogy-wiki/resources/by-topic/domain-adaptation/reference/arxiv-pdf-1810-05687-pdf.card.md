# Card: SimOpt / Bayesian Domain Randomization Loop
**Source:** https://arxiv.org/pdf/1810.05687.pdf  
**Role:** paper | **Need:** CONCEPT_EXPLAINER  
**Anchor:** Closed-loop procedure to update simulator parameter distributions from a few real rollouts (KL-constrained Bayesian-style update) interleaved with RL policy training.

## Key Content
- **Domain randomization objective (Eq. 1, Sec. III-A):** sample sim params \(\xi \sim p_\phi(\xi)\) to induce dynamics \(P_{\xi\sim p_\phi}\). Train policy \(\pi_\theta(a|s)\) to maximize  
  \[
  \max_\theta \ \mathbb{E}_{\xi\sim p_\phi}\big[\mathbb{E}_{\pi_\theta}[R(\tau)]\big]
  \]
  where \(\tau=(s_0,a_0,\dots,s_T,a_T)\), \(R(\tau)=\sum_{t=0}^T \gamma^t R(s_t,a_t)\).
- **Sim-to-real matching objective (Eq. 2, Sec. III-B):** minimize expected discrepancy between **real** and **sim** observation trajectories:  
  \[
  \min_\phi \ \mathbb{E}_{\xi\sim p_\phi}\big[\mathbb{E}_{\pi_{\theta,p_\phi}}[D(\tau^{ob}_\xi,\tau^{ob}_{real})]\big]
  \]
  Policy inputs and discrepancy observations need not match; only partial real observations required.
- **Iterative KL-trust-region update (Eq. 3 + Alg. 1 “SimOpt”):**  
  \[
  \min_{\phi_{i+1}} \mathbb{E}_{\xi_{i+1}\sim p_{\phi_{i+1}}}\big[\mathbb{E}_{\pi_{\theta,p_{\phi_i}}}[D(\tau^{ob}_{\xi_{i+1}},\tau^{ob}_{real})]\big]
  \ \text{s.t.}\ D_{KL}(p_{\phi_{i+1}}\|p_{\phi_i})\le \epsilon
  \]
  **Algorithm 1 steps:** init \(p_{\phi_0}\); loop: train RL in sim with \(p_{\phi_i}\); collect real rollout; sample \(\xi\sim p_{\phi_i}\) and sim rollouts; compute cost \(c(\xi)=D(\cdot)\); update \(p_{\phi_{i+1}}\) with KL step \(\epsilon\).
- **Discrepancy function (Eq. 4):** weighted \(\ell_1+\ell_2\) over time with per-dimension weights \(W\):  
  \(D = w_{\ell_1}\sum_{i=0}^T |W(o_{i,\xi}-o_{i,real})| + w_{\ell_2}\sum_{i=0}^T \|W(o_{i,\xi}-o_{i,real})\|_2^2\). Gaussian temporal smoothing used (std 5 timesteps, trunc 4).
- **Implementation defaults:** \(p_\phi(\xi)=\mathcal{N}(\mu,\Sigma)\) (full covariance). Update via **REPS** (relative entropy policy search) gradient-free, treating simulator as black box.
- **Empirical results (key numbers):**
  - **Swing-peg-in-hole (real ABB Yumi):** per SimOpt iter: 100 RL iters (~7 min), **3 real rollouts**, **3 REPS updates**, **9600 sim samples/update**, 453 timesteps/sample. After **2 SimOpt iterations**, **90% success over 20 trials**.
  - **Drawer opening (real Franka Panda):** per iter: 200 RL iters (~22 min), **3 real rollouts**, **20 REPS updates**, **9600 samples/update**. After **1 SimOpt update**, **20/20 successful** openings.
  - **Why not “very wide” randomization:** wide distributions can include infeasible instances (e.g., peg too large / rope too short) and hinder learning; in sim drawer task, policy only opened drawer at cabinet-position std **2 cm**; larger (up to **10 cm**) led to conservative/failing policies. SimOpt handled target offsets **15 cm (3 iterations)** and **22 cm (5 iterations)** by progressively shifting the distribution.

## When to surface
Use when students ask how to “close the sim-to-real loop,” how to update domain randomization using real data, why KL-constrained updates help, or why overly wide randomization can hurt learning/transfer.