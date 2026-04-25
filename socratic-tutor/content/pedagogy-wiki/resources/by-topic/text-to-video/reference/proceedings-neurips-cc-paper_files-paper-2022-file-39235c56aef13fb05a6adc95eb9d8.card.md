# Card: Video Diffusion Models (Ho et al., NeurIPS 2022)
**Source:** https://proceedings.neurips.cc/paper_files/paper/2022/file/39235c56aef13fb05a6adc95eb9d8d66-Paper-Conference.pdf  
**Role:** paper | **Need:** CONCEPT_EXPLAINER  
**Anchor:** Joint image+video training; space-time noise/sampling; factorized 3D U-Net + temporal attention; reconstruction-guided conditional sampling for temporal coherence/extension.

## Key Content
- **Forward diffusion (Eq. 1):** for data \(x\), latent \(z_t\):  
  \(q(z_t|x)=\mathcal N(z_t;\alpha_t x,\sigma_t^2 I)\), and for \(0\le s<t\le 1\):  
  \(q(z_t|z_s)=\mathcal N(z_t;(\alpha_t/\alpha_s)z_s,\sigma_{t|s}^2 I)\), with log-SNR \(\lambda_t=\log(\alpha_t^2/\sigma_t^2)\) decreasing so \(q(z_1)\approx \mathcal N(0,I)\).
- **Training objective (Eq. 2):** weighted denoising MSE  
  \(\mathbb E_{\epsilon,t}[w(\lambda_t)\|\hat x_\theta(z_t)-x\|_2^2]\). Uses **\(\epsilon\)-prediction**: \(\hat x_\theta(z_t)=(z_t-\sigma_t\epsilon_\theta(z_t))/\alpha_t\); \(t\) sampled with **cosine schedule**.
- **Sampling:**  
  Reverse conditional (Eq. 3) with mean \(\tilde\mu_{s|t}(z_t,x)\); **ancestral step** (Eq. 4):  
  \(z_s=\tilde\mu_{s|t}(z_t,\hat x_\theta(z_t))+\sqrt{(\tilde\sigma_{s|t}^2)^{1-\gamma}(\sigma_{t|s}^2)^\gamma}\,\epsilon\).  
  **Predictor-corrector** adds Langevin correction (Eq. 5): \(z_s\leftarrow z_s-\tfrac12\delta\sigma_s\epsilon_\theta(z_s)+\sqrt{\delta\sigma_s}\epsilon'\), with **\(\delta=0.1\)**.
- **Classifier-free guidance (Eq. 6):** \(\tilde\epsilon_\theta(z_t,c)=(1+w)\epsilon_\theta(z_t,c)-w\epsilon_\theta(z_t)\).
- **Video architecture (Section 3, Fig. 1):** factorized **3D U-Net**: replace 2D conv with **space-only 3D conv** (e.g., \(3\times3\to1\times3\times3\)); keep **spatial attention** over H×W (frames as batch); insert **temporal attention** over frames (H×W as batch) with **relative position embeddings**. Temporal attention can be **masked** to treat frames as independent images → enables joint image+video training.
- **Joint image+video training (Section 4.3.1):** append **0/4/8 independent image frames** to each video; mask temporal attention to prevent mixing; improves metrics (16×64×64 text-to-video): **FVD** 202.28→68.11→57.84 as image frames 0→4→8; **FID-avg** 37.52→18.62→15.57.
- **Reconstruction-guided conditional sampling (Section 3.1, Eq. 7):** fixes incoherence of “replacement” imputation by adding gradient guidance using model reconstruction of conditioning part \(x_a\):  
  \(\tilde x_{b,\theta}(z_t)=\hat x_{b,\theta}(z_t)-w_r\frac{\alpha_t}{2}\nabla_{z_{b,t}}\|x_a-\hat x_{a,\theta}(z_t)\|_2^2\).  
  Spatial SR variant (Eq. 8): \(\tilde x_\theta(z_t)=\hat x_\theta(z_t)-w_r\frac{\alpha_t}{2}\nabla_{z_t}\|x_a-\hat x_{a,\theta}(z_t)\|_2^2\) where \(\hat x_{a,\theta}\) is **downsampled** (e.g., bilinear) model output.
- **Empirical coherence gain (Table 6):** autoregressive extension to **64 frames** from 16-frame model: with guidance weight 2.0, **FVD 136.22** (recon guidance) vs **451.45** (replacement); similar at 5.0: **133.92** vs **456.24**.
- **Video prediction SOTA (Tables 2–3):** BAIR: **FVD 66.92** (Langevin, 256 steps) vs prior best 86.9; Kinetics-600: **FVD 16.2** (Langevin, 128 steps).

## When to surface
Use when students ask how video diffusion enforces temporal coherence (architecture + temporal attention), how to extend/upsample videos via conditional sampling, or want the exact guidance/sampling equations and concrete metric improvements over replacement/imputation.