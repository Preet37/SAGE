# Card: Diffusion Policy (DDPM for visuomotor action sequences)
**Source:** https://roboticsproceedings.org/rss19/p026.pdf  
**Role:** paper | **Need:** EMPIRICAL_DATA  
**Anchor:** Proceedings version with definitive method description, experimental protocol, and results tables

## Key Content
- **DDPM denoising update (Eq. 1):**  
  \(x_{k-1}=\alpha\big(x_k-\gamma\,\epsilon_\theta(x_k,k)+\mathcal{N}(0,\sigma^2 I)\big)\).  
  Interpretable as noisy gradient step (Eq. 2): \(x' = x-\gamma\nabla E(x)\), where \(\epsilon_\theta\) predicts the gradient field.
- **Training objective (Eq. 3):** sample data \(x_0\), pick random step \(k\), add noise \(\epsilon_k\); minimize  
  \(L=\mathrm{MSE}(\epsilon_k,\epsilon_\theta(x_0+\epsilon_k,k))\).
- **Policy conditioning + closed-loop horizons (Sec. II-C, Fig. 3):** learn conditional \(p(A_t|O_t)\) with action sequences.  
  Conditioned denoising (Eq. 4): \(A^{k-1}_t=\alpha(A^k_t-\gamma\,\epsilon_\theta(O_t,A^k_t,k)+\mathcal{N}(0,\sigma^2I))\).  
  Loss (Eq. 5): \(L=\mathrm{MSE}(\epsilon_k,\epsilon_\theta(O_t,A^0_t+\epsilon_k,k))\).  
  Horizons: observation \(T_o\), prediction \(T_p\), execute \(T_a\) steps before replanning (receding horizon).
- **Architectures (Sec. III-A):** CNN backbone with FiLM conditioning; **Time-series Diffusion Transformer** (cross-attention to obs; causal attention over actions) reduces CNN over-smoothing for high-rate control.
- **Visual encoder (Sec. III-B):** ResNet-18 (no pretrain), spatial softmax pooling, GroupNorm (stable with EMA).
- **Defaults/acceleration:** Square Cosine noise schedule (iDDPM) works best (Sec. III-C). DDIM speeds inference: **100 training steps, 10 inference steps → ~0.1s latency on RTX 3080** (Sec. III-D).
- **Key empirical results:**  
  - Across **12 tasks / 4 benchmarks**, Diffusion Policy average **+46.9%** success-rate improvement vs prior SOTA (Abstract/Sec. V).  
  - **Real Push-T:** Diffusion Policy (end-to-end transformer) **95% success**, **IoU 0.80** vs Human **1.00 / 0.84**; IBC best **0%**, LSTM-GMM best **20%** (Table V).  
  - **Mug flip:** Diffusion Policy **90%** vs LSTM-GMM **0%** (Fig. 10).  
  - **Sauce tasks:** Pour IoU **0.74**, succ **0.79**; Spread coverage **0.77**, succ **1.00** (Fig. 11).
- **Design rationale:** conditioning on \(O_t\) (not joint \(A,O\)) extracts vision once → real-time control; action-sequence diffusion handles multimodality + temporal consistency; score modeling avoids EBM normalization/negative sampling → training stability (Sec. IV-D).

## When to surface
Use for questions about diffusion-model policies for robots: exact DDPM equations for action generation, receding-horizon execution, real-time inference tricks (DDIM), and concrete benchmark/real-robot performance numbers vs BC baselines.