# Card: Benchmark details & normalized-score procedure (PIC/POIC paper)
**Source:** http://proceedings.mlr.press/v139/furuta21a/furuta21a-supp.pdf  
**Role:** benchmark | **Need:** EMPIRICAL_DATA  
**Anchor:** Supplementary benchmark tables/plots + experimental settings for reproducible Gym/MuJoCo/DMControl comparisons (SAC/MPO/AWR + leaderboard baselines), plus reward-shaping and noise-tuning setups.

## Key Content
- **Environment specs (Table 2):**  
  Ant-v2 state 111, action 8, horizon 1000; HalfCheetah-v2 state 17, action 6, horizon 1000; Hopper-v2 state 11, action 3, horizon 1000; Walker2d-v2 state 17, action 6, horizon 1000; Humanoid-v2 state 376, action 17, horizon 1000. (Also classic control + DMControl tasks listed.)
- **Reward equations (Appendix A):**  
  Pendulum: \(r_t=-(\phi_t^2+0.1\dot\phi_t^2+0.001\|a_t\|_2^2)\).  
  HalfCheetah: \(r_t=\dot x_t-0.1\|a_t\|_2^2\).  
  Hopper/Walker2d: \(r_t=\dot x_t-0.01\|a_t\|_2^2+1\).  
  Ant: \(r_t=\dot x_t-0.5\|a_t\|_2^2-0.0005\|s^{contact}_t\|_2^2+1\).  
  Humanoid: \(r_t=1.25\dot x_t-0.1\|a_t\|_2^2-\min(5\!\times\!10^{-7}\|s^{contact}_t\|_2^2,10)+5\).
- **Algorithm-based normalized score (Appendix C):**  
  \[
  \text{NormScore}=\frac{r^{algo}_{avg}-r^{rand}_{min}}{\max(r^{rand}_{max},r^{algo}_{max})-r^{rand}_{min}}
  \]
  where \(r^{algo}_{avg}\)=avg return over an algorithm set; \(r^{algo}_{max}\)=best algorithm return; \(r^{rand}_{min},r^{rand}_{max}\)=min/max from random policy sampling.
- **MuJoCo training budgets (Appendix C.1.2):** SAC/MPO/AWR averaged over **10 seeds**; train **1M steps (Hopper)**, **3M (Ant/HalfCheetah/Walker2d)**, **10M (Humanoid)**.
- **MuJoCo baseline numbers:**  
  Table 5 (10-seed): SAC Ant **5526.4**, HalfCheetah **15266.5**, Hopper **2948.9**, Walker2d **5771.8**, Humanoid **8264.0**; MPO Ant **6584.2**; AWR Hopper **3084.7**.  
  Table 4 (aggregated): average/max scores—Ant **2450.8/6584.2**, HalfCheetah **6047.2/15266.5**, Hopper **2206.7/3564.1**, Walker2d **3190.8/5813.0**, Humanoid **3880.8/8264.0**.
- **DMControl (500k steps, 10 seeds):** Table 9 SAC cheetah run **536.0**, reacher easy **961.2**, ball in cup catch **971.9**; Table 8 aggregated avg/max: cheetah run **474.4/795.0**, reacher easy **691.5/961.2**, ball in cup catch **751.7/978.2**.
- **Reward shaping families (Appendix G):**  
  L1: \(r=-\alpha\|s-s_g\|_1\); L2: \(r=-\alpha\|s-s_g\|_2\); Fraction: \(r=\frac{\beta}{\gamma+\|s-s_g\|_2}\); Sparse: \(r=-\mathbf{1}[\|s-s_g\|_2\ge \epsilon]\). PPO trained **500k steps**, **5 seeds**, scores normalized for reward-scale comparability.

## When to surface
Use for questions about *exact benchmark settings*, *reward definitions*, *training step budgets/seeds*, or *how “normalized score” is computed* for cross-environment task difficulty comparisons in Gym/MuJoCo/DMControl.