# Card: Diffusion Policy (Action Diffusion for Visuomotor BC)
**Source:** https://diffusion-policy.cs.columbia.edu/diffusion_policy_ijrr.pdf  
**Role:** paper | **Need:** EMPIRICAL_DATA  
**Anchor:** Training procedure (action diffusion, conditioning, horizons) + benchmark results (RoboMimic/Push-T/BlockPush/Kitchen + real-world)

## Key Content
- **DDPM sampling / policy inference (Eq. 1):**  
  \(x_{k-1}=\alpha\big(x_k-\gamma\,\varepsilon_\theta(x_k,k)+\mathcal N(0,\sigma^2 I)\big)\).  
  Interpretable as noisy gradient step (Eq. 2): \(x' = x-\gamma\nabla E(x)\), where \(\varepsilon_\theta\) predicts a gradient/score field.
- **DDPM training (Eq. 3):** sample data \(x_0\), pick random diffusion step \(k\), sample noise \(\varepsilon_k\); minimize  
  \(L=\mathrm{MSE}(\varepsilon_k,\varepsilon_\theta(x_0+\varepsilon_k,k))\).
- **Visuomotor conditional action diffusion (Eq. 4–5):** model \(p(A_t\mid O_t)\) (not joint).  
  \(A^{k-1}_t=\alpha(A^k_t-\gamma\,\varepsilon_\theta(O_t,A^k_t,k)+\mathcal N(0,\sigma^2I))\).  
  Loss: \(L=\mathrm{MSE}(\varepsilon_k,\varepsilon_\theta(O_t,A^0_t+\varepsilon_k,k))\).
- **Closed-loop horizons (Sec. 2.3):** observation horizon \(T_o\); predict \(T_p\) actions; execute \(T_a\) before replanning (receding horizon). Warm-start next plan with unexecuted actions.
- **Architectures (Sec. 3.1):** CNN backbone with FiLM conditioning each conv layer; Transformer (“time-series diffusion transformer”) uses cross-attention to observation embeddings + causal self-attention over action tokens. Recommendation: start CNN; use Transformer for high-rate action changes.
- **Vision encoder (Sec. 3.2):** ResNet-18 (no pretrain), spatial softmax pooling; GroupNorm (EMA + BatchNorm conflict).
- **Noise schedule (Sec. 3.3):** Square Cosine schedule (iDDPM) worked best.
- **Real-time inference (Sec. 3.4):** DDIM: 100 training diffusion steps, 10 inference steps → ~0.1s latency on Nvidia 3080.
- **Key sim results (Tables 1–2, success rates shown as max / avg last-10 checkpoints):**  
  RoboMimic **state** examples: Transport (PH) LSTM-GMM 0.76/0.47 vs DiffPolicy-C 0.94/0.82 vs DiffPolicy-T 1.00/0.84; ToolHang (PH) 0.67/0.31 vs 0.50/0.30 vs 1.00/0.87.  
  RoboMimic **visual** example: Transport (MH) LSTM-GMM 0.44/0.24 vs DiffPolicy-C 0.89/0.69 vs DiffPolicy-T 0.73/0.50.
- **Multi-stage state tasks (Table 4):** BlockPush p2: BET 0.71 vs DiffPolicy-T 0.94; Kitchen p4: BET 0.44 vs DiffPolicy-T 0.96.
- **Real-world Push-T (Table 6):** Human IoU 0.84, Succ 1.00; DiffPolicy (E2E) IoU 0.80, Succ 0.95; LSTM-GMM (E2E) Succ 0.20; IBC (E2E) Succ 0.00. Control at 10 Hz, interpolated to 125 Hz.
- **Real-world other tasks:** Mug Flip: DiffPolicy 0.9 success (20 trials) vs LSTM-GMM 0.0. Sauce Pour: IoU 0.74, Succ 0.79 (human 0.79/1.00). Sauce Spread: coverage 0.77, Succ 1.00 (human 0.79/1.00).

## When to surface
Use when students ask how diffusion models are trained/used as robot policies (conditioning, horizons, DDIM speedups), or when they need quantitative comparisons vs BC-RNN/LSTM-GMM, BET, IBC on RoboMimic/Push-T/Kitchen or real-world manipulation.