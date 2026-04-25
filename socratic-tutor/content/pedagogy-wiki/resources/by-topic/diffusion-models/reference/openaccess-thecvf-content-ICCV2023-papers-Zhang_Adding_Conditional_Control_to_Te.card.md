# Card: ControlNet (Zero-Conv Conditional Control for Stable Diffusion)
**Source:** https://openaccess.thecvf.com/content/ICCV2023/papers/Zhang_Adding_Conditional_Control_to_Text-to-Image_Diffusion_Models_ICCV_2023_paper.pdf  
**Role:** paper | **Need:** FORMULA_SOURCE  
**Anchor:** ControlNet mechanism: trainable UNet copy + zero-conv adapters, injection points, training objective preserving base model

## Key Content
- **ControlNet block definition (Section 3.1):** For a pretrained block \(F(\cdot;\Theta)\), baseline output  
  **Eq. (1)** \(y = F(x;\Theta)\), where \(x\in\mathbb{R}^{h\times w\times c}\).  
  ControlNet freezes \(\Theta\), clones a trainable copy with \(\Theta_c\), and connects via **zero convolutions** \(Z(\cdot;\cdot)\) (1×1 conv with weight+bias initialized to 0):  
  **Eq. (2)** \(y_c = F(x;\Theta) + Z\!\left(F(x + Z(c;\Theta_{z1});\Theta_c);\Theta_{z2}\right)\).  
  At initialization, \(Z(\cdot)=0\) so **Eq. (3)** \(y_c=y\) ⇒ no harmful perturbation at training start; trainable copy still receives \(x\) (backbone reuse).
- **Where injected in Stable Diffusion UNet (Section 3.2, Fig. 3):** Trainable copy of **12 encoder blocks + 1 middle block** (total 13). Outputs are **added to 12 skip connections + middle block** of the locked UNet. SD has **25 blocks** total; encoder/decoder each **12 blocks** + middle.
- **Condition encoder (Eq. 4):** Convert 512×512 condition image \(c_i\) to 64×64 feature \(c_f\) via tiny CNN \(E\):  
  \(c_f = E(c_i)\), with **4 conv layers**, kernel **4×4**, stride **2×2**, ReLU, channels **16, 32, 64, 128**.
- **Training objective (Section 3.3):** Standard diffusion noise-prediction loss:  
  **Eq. (5)** \(L=\mathbb{E}_{z_0,t,c_t,c_f,\epsilon\sim\mathcal{N}(0,1)}\left[\|\epsilon-\epsilon_\theta(z_t,t,c_t,c_f)\|_2^2\right]\).  
  **Prompt dropout:** replace **50%** of text prompts \(c_t\) with empty string to improve semantic recognition from condition alone. Observed “**sudden convergence**” typically **<10k** steps.
- **Efficiency claim (Section 3.2):** On **A100 40GB**, optimizing SD+ControlNet uses **~23% more GPU memory** and **~34% more time/iter** vs SD finetune.
- **CFG + ControlNet (Section 3.4):** CFG formula: \(\epsilon_{prd}=\epsilon_{uc}+\beta_{cfg}(\epsilon_c-\epsilon_{uc})\). Proposed **CFG Resolution Weighting:** multiply each ControlNet→SD connection by \(w_i=64/h_i\) where block resolution \(h_i\in\{8,16,\dots,64\}\).
- **Multiple ControlNets (Section 3.4):** Compose by **directly adding** outputs of multiple ControlNets to SD; “no extra weighting” required.
- **Empirical numbers:** User study AUR (Table 1): **ControlNet 4.22±0.43 quality**, **4.28±0.45 fidelity** vs **ControlNet-lite 3.93±0.59**, **4.09±0.46**. Segmentation-conditioned generation (Table 3): **ControlNet FID 15.27** vs **ControlNet-lite 17.92**, **PIPT 19.74**, **Stable Diffusion 6.09** (unconditioned baseline).

## When to surface
Use when students ask how ControlNet preserves a pretrained diffusion model while adding spatial conditioning, where/what is injected into the UNet, or for the exact equations (zero-conv block, diffusion loss, CFG weighting) and key quantitative comparisons.