# Card: PPO clipping ≠ trust region; rollback + KL-trigger variants
**Source:** http://proceedings.mlr.press/v115/wang20b/wang20b-supp.pdf  
**Role:** paper | **Need:** EMPIRICAL_DATA  
**Anchor:** When/why PPO clipping fails to be a trust-region method; theory + empirical evidence; KL-trigger + rollback improves stability/sample efficiency.

## Key Content
- **Policy-gradient surrogate (Eq. 1):**  
  \(L_{\pi_{\text{old}}}(\pi)=\mathbb{E}_{s,a}[r_\pi(s,a)A_{\pi_{\text{old}}}(s,a)]+\eta(\pi_{\text{old}})\), where \(r_\pi=\pi(a|s)/\pi_{\text{old}}(a|s)\).
- **TRPO trust-region bound (Thm 1, Eq. 2–3):**  
  \(\eta(\pi)\ge M_{\pi_{\text{old}}}(\pi)=L_{\pi_{\text{old}}}(\pi)-C\max_s D^{s}_{KL}(\pi_{\text{old}},\pi)\), with \(C=\max_{s,a}|A_{\pi_{\text{old}}}(s,a)|\frac{4\gamma}{(1-\gamma)^2}\). TRPO constrains \(\max_s D^{s}_{KL}\le \delta\).
- **PPO clipped objective (Eq. 4–7):**  
  \(L^{CLIP}_t(\theta)=\min(r_tA_t,\;F_{CLIP}(r_t,\epsilon)A_t)\), \(F_{CLIP}=\text{clip}(r_t,1-\epsilon,1+\epsilon)\). Clipping condition: \(r_t\ge 1+\epsilon \land A_t>0\) or \(r_t\le 1-\epsilon \land A_t<0\) ⇒ zero gradient for that sample.
- **Why ratios can still blow up (Thm 2):** even if clipped, overall gradient can push \(r_t\) further out when \(\langle\nabla L^{CLIP}(\theta_0),\nabla r_t(\theta_0)\rangle A_t>0\). Empirically this condition occurs **25%–45%** of samples (1M-sample stats).
- **Clipping does NOT enforce KL trust region (Thm 3):** even with \(1-\epsilon\le r_t\le 1+\epsilon\), \(\sup_{\theta\in\Theta} D^{s_t}_{KL}(\theta_{old},\theta)=\infty\) (discrete \(|A|\ge 3\) and Gaussian continuous).
- **Rollback PPO (Eq. 11):** replace clip with  
  \(F_{RB}(r_t,\epsilon,\alpha)= -\alpha r_t+(1+\alpha)(1\pm\epsilon)\) when out of range; else \(r_t\). Reverses slope (negative incentive). Default **\(\alpha=0.3\)** (Humanoid **0.1**). Improves ratio control (Thm 4).
- **KL-trigger PPO (TR-PPO, Eq. 13–15):** clip when \(D^{s_t}_{KL}(\theta_{old},\theta)\ge \delta\): set \(F_{TR}=r_t(\theta_{old})=1\). Must keep **min(·,·)**; “TR-PPO-simple” (no min) performs extremely badly. Defaults: **\(\delta=0.025\)** (Humanoid/HalfCheetah **0.03**).
- **Combine (TR-PPO-RB, Eq. 16):** if \(D_{KL}\ge\delta\), use \(-\alpha r_t\) (negative incentive). Defaults: **\(\delta=0.03,\alpha=0.05\)** (Humanoid/HalfCheetah \(\alpha=0.1\)).
- **Empirics:** PPO ratios often exceed clip; max ratio **>3** on all tested tasks (with \(\epsilon=0.2\)); some tasks can reach **~40** (noted). PPO KL max grows over training. New methods reduce out-of-range ratios/KL and improve learning.
- **Sample-efficiency (Table 1a, timesteps×10³ to threshold):**  
  Hopper(3000): PPO **273**, PPO-RB **179**, TR-PPO **153**, TR-PPO-RB **130**.  
  Walker2d(3000): PPO **528**, PPO-RB **305**, TR-PPO **345**, TR-PPO-RB **320**.  
  HalfCheetah(2100): PPO **374**, PPO-RB **227**, TR-PPO **266**, TR-PPO-RB **39**.  
  Humanoid(5000, 20M steps): PPO **8410**, TR-PPO **7580**, TR-PPO-RB **6422**.
- **Performance (Table 1b, avg top-10 returns):** Walker2d: PPO **4036**, PPO-RB **4992**, TR-PPO-RB **5011**. HalfCheetah: PPO **1623**, TR-PPO **4672**, TR-PPO-RB **4048**.
- **Training pipeline (“epoch”):** (1) sample \((s_t,a_t)\sim \rho_{\pi_{\theta_{old}}},\pi_{\theta_{old}}\); (2) optimize surrogate to get new \(\theta\); measure ratios/KL per epoch.

## When to surface
Use when students ask whether PPO clipping is a trust region / guarantees bounded KL, why PPO can be unstable, or what modifications (KL-trigger, rollback) empirically improve stability and sample efficiency.