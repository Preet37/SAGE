# Card: Diffusion Policy (Action Diffusion for Visuomotor BC)
**Source:** https://diffusion-policy.cs.columbia.edu/diffusion_policy_ijrr.pdf  
**Role:** paper | **Need:** EMPIRICAL_DATA  
**Anchor:** Full diffusion-policy objective + sampling procedure; benchmark tables across multiple manipulation suites

## Key Content
- **DDPM sampling / policy inference (Eq. 1, Eq. 4):** start from Gaussian noise \(x_K\) (or action-seq \(A_t^K\)). Iterate  
  \(x_{k-1}=\alpha\big(x_k-\gamma\,\varepsilon_\theta(x_k,k)+\mathcal N(0,\sigma^2 I)\big)\) (Eq. 1).  
  Conditional visuomotor form: \(A_{t}^{k-1}=\alpha\big(A_t^k-\gamma\,\varepsilon_\theta(O_t,A_t^k,k)+\mathcal N(0,\sigma^2 I)\big)\) (Eq. 4).  
  Interpretable as noisy gradient step \(x' = x-\gamma\nabla E(x)\) (Eq. 2).
- **Training objective (Eq. 3, Eq. 5):** sample data \(x_0\) (or \(A_t^0\)), pick random diffusion step \(k\), add noise \(\varepsilon_k\). Minimize  
  \(L=\mathrm{MSE}(\varepsilon_k,\varepsilon_\theta(x_0+\varepsilon_k,k))\) (Eq. 3); conditional:  
  \(L=\mathrm{MSE}(\varepsilon_k,\varepsilon_\theta(O_t,A_t^0+\varepsilon_k,k))\) (Eq. 5).
- **Closed-loop receding horizon (Sec. 2.3):** observe last \(T_o\) steps \(O_t\); predict \(T_p\) future actions; execute only \(T_a\) then replan; warm-start next plan with unexecuted actions.
- **Design defaults:** Square Cosine noise schedule (Sec. 3.3). DDIM for speed: **100 training iterations, 10 inference iterations → ~0.1s latency on RTX 3080** (Sec. 3.4). Action horizon **8 steps** often best (Sec. 5.3, Fig. 5).
- **Vision encoder (Sec. 3.2):** ResNet-18 (no pretrain), spatial softmax (replace GAP), GroupNorm (replace BatchNorm) for EMA stability.
- **Empirical headline:** across **15 tasks / 4 benchmarks**, Diffusion Policy improves average success by **46.9%** vs prior SOTA (Abstract/Sec. 5.3).
- **Key benchmark numbers:**  
  - RoboMimic visual (Table 2): **Transport (PH)** LSTM-GMM 0.88/0.62 vs DiffusionPolicy-C **1.00/0.93**; **ToolHang (PH)** 0.68/0.49 vs **0.95/0.73**.  
  - Multi-stage state (Table 4): **BlockPush p2** BET 0.71 vs DiffusionPolicy-T **0.94**; **Kitchen p4** BET 0.44 vs DiffusionPolicy-C **0.99** (T: 0.96).  
  - Real Push-T (Table 6): Diffusion Policy (end2end) **Succ 0.95**, IoU **0.80**; IBC **0.00**, LSTM-GMM best **0.20**.

## When to surface
Use when students ask how diffusion models become real-time robot policies (objective + sampling), why action-sequence + receding horizon helps, or to cite concrete benchmark gains vs BC-RNN/LSTM-GMM, IBC, BET on manipulation tasks.