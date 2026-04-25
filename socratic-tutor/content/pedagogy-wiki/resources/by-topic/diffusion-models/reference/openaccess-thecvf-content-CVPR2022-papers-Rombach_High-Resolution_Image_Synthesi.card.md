# Card: Latent Diffusion Models (LDM) training pipeline + conditioning
**Source:** https://openaccess.thecvf.com/content/CVPR2022/papers/Rombach_High-Resolution_Image_Synthesis_With_Latent_Diffusion_Models_CVPR_2022_paper.pdf  
**Role:** paper | **Need:** CONCEPT_EXPLAINER  
**Anchor:** LDM training pipeline details: autoencoder latent space, diffusion objective in latent, UNet + cross-attention conditioning, compute/quality tradeoffs & ablations.

## Key Content
- **Two-stage pipeline (Sec. 3):**
  1) Train perceptual **autoencoder** with encoder \(E\), decoder \(D\): \(z=E(x)\), \(\tilde x=D(z)\), where \(x\in\mathbb{R}^{H\times W\times 3}\), \(z\in\mathbb{R}^{h\times w\times c}\), downsampling factor \(f=H/h=W/w\) with \(f=2^m\). Loss uses **perceptual loss** + **patch-based adversarial** objective (Sec. 3.1). Regularize latents via **KL-reg** (VAE-like) or **VQ-reg** (vector quantization in decoder).
  2) Train diffusion model in latent space (Sec. 3.2) using time-conditional **UNet** \(\epsilon_\theta\).
- **Diffusion objectives:**
  - Pixel DM (Eq. 1): \(\mathcal{L}_{DM}=\mathbb{E}_{x,\epsilon\sim\mathcal{N}(0,1),t}\left[\|\epsilon-\epsilon_\theta(x_t,t)\|_2^2\right]\).
  - **Latent DM** (Eq. 2): \(\mathcal{L}_{LDM}=\mathbb{E}_{E(x),\epsilon,t}\left[\|\epsilon-\epsilon_\theta(z_t,t)\|_2^2\right]\).
  - **Conditional** (Eq. 3): \(\mathcal{L}_{LDM}=\mathbb{E}_{E(x),y,\epsilon,t}\left[\|\epsilon-\epsilon_\theta(z_t,t,\tau_\theta(y))\|_2^2\right]\).
- **Cross-attention conditioning (Sec. 3.3):** \(\tau_\theta(y)\in\mathbb{R}^{M\times d_\tau}\) (e.g., transformer for text). At UNet layer \(i\), with flattened features \(\phi_i(z_t)\in\mathbb{R}^{N\times d_\epsilon^i}\):  
  \(Q=W_Q^{(i)}\phi_i(z_t)\), \(K=W_K^{(i)}\tau_\theta(y)\), \(V=W_V^{(i)}\tau_\theta(y)\);  
  \(\text{Attn}(Q,K,V)=\text{softmax}(QK^\top/\sqrt d)\,V\).
- **Design rationale:** operate in latent space to avoid expensive repeated UNet evals over full RGB pixels; mild compression removes imperceptible detail while preserving semantics (Fig. 2). UNet conv inductive bias allows **less aggressive compression** than AR latent models.
- **Key empirical tradeoffs (Sec. 4.1):** Best balance at **\(f\in\{4,8\}\)**; too small \(f\) trains slowly; too large \(f\) loses fidelity. On ImageNet after 2M steps, **FID gap ~38** between pixel LDM-1 and LDM-8 (Fig. 5).
- **Text-to-image (Table 2, MS-COCO):** LDM-KL-8 FID **23.35**; with **classifier-free guidance** (scale **1.5**) FID **12.61** (250 DDIM steps).
- **Class-conditional ImageNet (Table 3, 250 DDIM):** LDM-4 FID **10.56**; LDM-4 + classifier-free guidance (scale **1.5**) FID **3.60**, IS **247.67**; params **400M**.
- **Efficiency (Table 6, inpainting):** train throughput @256: pixel LDM-1 **0.11** samples/s vs LDM-4(VQ) **0.33**; sampling @512: **0.07** vs **0.34**; hours/epoch **20.66** vs **7.04**.

## When to surface
Use when students ask how Stable Diffusion/LDMs are trained (autoencoder + latent diffusion), why latent space reduces compute, or how cross-attention enables text/layout conditioning and classifier-free guidance boosts FID.