# Card: GAIL = occupancy-measure matching via GAN objective
**Source:** https://arxiv.org/pdf/1606.03476.pdf  
**Role:** paper | **Need:** FORMULA_SOURCE  
**Anchor:** Minimax objective over occupancy measures, discriminator-derived reward, connection to regularized IRL / Jensen–Shannon divergence

## Key Content
- **Max causal entropy IRL (Eq. 1):**  
  \[
  \max_{c\in\mathcal C}\Big(\min_{\pi\in\Pi}-H(\pi)+\mathbb E_\pi[c(s,a)]\Big)-\mathbb E_{\pi_E}[c(s,a)]
  \]
  with **causal entropy** \(H(\pi)=\mathbb E_\pi[-\log \pi(a|s)]\). RL step (Eq. 2):  
  \[
  RL(c)=\arg\min_{\pi}-H(\pi)+\mathbb E_\pi[c(s,a)].
  \]
- **Occupancy measure:** \(\rho_\pi(s,a)=\pi(a|s)\sum_{t\ge0}\gamma^t P(s_t=s|\pi)\). Then \(\mathbb E_\pi[c]=\sum_{s,a}\rho_\pi(s,a)c(s,a)\). Valid \(\rho\) satisfy flow constraints (Section 3) and map 1–1 to policies: \(\pi_\rho(a|s)=\rho(s,a)/\sum_{a'}\rho(s,a')\) (Prop. 3.1).
- **Key characterization (Prop. 3.2, Eq. 4):** with convex cost regularizer \(\psi\),
  \[
  RL\circ IRL_\psi(\pi_E)=\arg\min_{\pi}\; -H(\pi)+\psi^*(\rho_\pi-\rho_{\pi_E}).
  \]
  If \(\psi\) constant ⇒ exact matching \(\rho_{\tilde\pi}=\rho_{\pi_E}\) (Cor. 3.2.1).
- **GAIL regularizer (Eq. 13) ⇒ GAN loss (Eq. 14):**  
  \[
  \psi^*_{GA}(\rho_\pi-\rho_E)=\max_{D:(S\times A)\to(0,1)}\mathbb E_\pi[\log D]+\mathbb E_{\pi_E}[\log(1-D)].
  \]
  This equals (up to constant) **Jensen–Shannon divergence**; objective (Eq. 15):  
  \[
  \min_\pi D_{JS}(\rho_\pi,\rho_E)-\lambda H(\pi).
  \]
- **Saddle-point training (Eq. 16) + Algorithm 1:** alternate  
  1) sample \(\tau_i\sim\pi_{\theta_i}\);  
  2) update discriminator \(w\) by gradient (Eq. 17): \(\hat{\mathbb E}_{\tau_i}[\nabla_w\log D_w]+\hat{\mathbb E}_{\tau_E}[\nabla_w\log(1-D_w)]\);  
  3) TRPO policy step on cost \(c(s,a)=\log D_{w}(s,a)\) with gradient (Eq. 18) and entropy term \(-\lambda\nabla_\theta H\).
- **Empirical results (Table 3):** Humanoid-v1: with 80 expert traj, **GAIL 10200.73±1324.47** vs BC 1397.06±1057.84; FEM 5093.12±583.11; GTAL 5096.43±24.96. Ant-v1 (4 traj): **GAIL 3186.80±903.57** vs FEM −2052.51±49.41, GTAL −5743.81±723.48.
- **Defaults/params:** GAE used with \(\gamma=0.995,\lambda=0.97\) (Appendix B). Training interaction (Table 2): MuJoCo tasks typically 500 iters × 50k state-action pairs/iter; Humanoid 1500×50k.

## When to surface
Use when students ask how GAIL’s discriminator objective becomes occupancy-measure matching / JS divergence, why it avoids behavior cloning’s covariate shift, or how the practical alternating updates (discriminator + TRPO) are derived from regularized IRL.