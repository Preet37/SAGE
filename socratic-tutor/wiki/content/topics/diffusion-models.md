---
title: "Diffusion Models"
subject: "Generative Models"
date: 2025-01-01
tags:
  - "subject/generative-models"
  - "level/intermediate"
  - "level/advanced"
  - "educator/yannic-kilcher"
  - "educator/lilian-weng"
  - "resource/video"
  - "resource/blog"
  - "resource/deep-dive"
  - "resource/paper"
  - "resource/code"
educators:
  - "Yannic Kilcher"
  - "Lilian Weng"
levels:
  - "intermediate"
  - "advanced"
resources:
  - "video"
  - "blog"
  - "deep-dive"
  - "paper"
  - "code"
---

# Diffusion Models

## Video (best)
- **Yannic Kilcher** — "DDPM - Denoising Diffusion Probabilistic Models | Paper Explained"
- **Watch:** [YouTube](https://www.youtube.com/watch?v=fbLgFrlTnGU)
- Why: Kilcher walks through the DDPM paper rigorously, explaining the math behind the forward/reverse diffusion process, the noise schedule, and the training objective. He balances formalism with intuition, making it ideal for learners who want to understand *why* the math works, not just *what* the algorithm does.
- Level: intermediate/advanced

## Blog / Written explainer (best)
- **Lilian Weng** — "What are Diffusion Models?"
- **Link:** [https://lilianweng.github.io/posts/2021-07-11-diffusion-models/](https://lilianweng.github.io/posts/2021-07-11-diffusion-models/)
- Why: Weng's post is the gold standard written explainer for diffusion models. It covers DDPM, score matching, SMLD, and the connections between them in a single coherent narrative. The mathematical derivations are complete but well-motivated, and the post has been updated over time to include newer developments. It serves as both an introduction and a lasting reference.
- Level: intermediate

## Deep dive
- **Lilian Weng** — "What are Diffusion Models?" (extended/updated version) + **Hugging Face Annotated Diffusion Models**
- **Link:** [https://huggingface.co/blog/annotated-diffusion](https://huggingface.co/blog/annotated-diffusion)
- Why: The Hugging Face annotated diffusion post by Niels Rogge and Kashif Rasul walks line-by-line through a full DDPM implementation in PyTorch, with inline explanations of every design choice. It bridges the gap between the mathematical formulation and working code better than almost any other resource, making it the best deep-dive for learners who need to go from theory to implementation.
- Level: advanced

## Original paper
- **Ho et al. (2020)** — "Denoising Diffusion Probabilistic Models"
- **Link:** [https://arxiv.org/abs/2006.11239](https://arxiv.org/abs/2006.11239)
- Why: DDPM is the clearest and most pedagogically accessible entry point into the diffusion model literature. Unlike earlier score-based papers, it frames the problem in terms of a simple noise-prediction objective that is easy to implement and reason about. It is the paper that made diffusion models practically accessible and is the standard starting point for the field.
- Level: advanced

## Code walkthrough
- **Hugging Face / Niels Rogge & Kashif Rasul** — "The Annotated Diffusion Model" (notebook)
- **Link:** [https://colab.research.google.com/github/huggingface/notebooks/blob/main/examples/annotated_diffusion.ipynb](https://colab.research.google.com/github/huggingface/notebooks/blob/main/examples/annotated_diffusion.ipynb)
- Why: This Colab notebook implements DDPM from scratch on a small dataset (Fashion-MNIST / flowers), with every block of code directly annotated to the corresponding equation in the Ho et al. paper. It is the most direct "paper → code" walkthrough available and is maintained by Hugging Face, ensuring code quality and compatibility.
- Level: intermediate/advanced

---

## Coverage notes
- **Strong:** Core DDPM theory, score matching connections, mathematical derivations (Weng blog), paper-to-code translation (HF annotated diffusion)
- **Weak:** Classifier-free guidance and ControlNet have no single dedicated resource of comparable quality — they are typically covered as addenda in broader diffusion posts or in their own papers rather than in polished tutorials
- **Gap:** No excellent standalone beginner-friendly *video* exists that covers the full arc from DDPM → latent diffusion → Stable Diffusion in one place without either oversimplifying or assuming heavy prior knowledge. Most videos either stay at a high level or dive straight into paper-level math with little scaffolding. A 3Blue1Brown-style visual treatment of the diffusion process does not yet exist as of this writing.
- **Gap:** ControlNet specifically lacks a strong written pedagogical explainer at the level of Weng's diffusion post.

---

## Additional Resources for Tutor Depth

> **6 sources** — papers, official docs, working code, benchmarks, and deep explainers that give the AI tutor precision on this topic.

### 📄 Classifier-Free Guidance (CFG) in Diffusion
**Paper** · [source](https://arxiv.org/abs/2207.12598)

*Step-by-step CFG procedure: conditional dropout training + exact guidance combination formula and guidance-scale behavior.*

<details>
<summary>Key content</summary>

- **Bayes/score decomposition (Intro):**  
  \[
  \nabla_x \log p(x\mid c)=\nabla_x \log p(c\mid x)+\nabla_x \log p(x)
  \]
  where \(\nabla_x \log p(c)=0\). (Motivates guidance as adding a “condition” term to an unconditional score.)

- **Training procedure (Algorithm 1, Section 3.2):** joint conditional+unconditional in one model via **conditioning dropout**.  
  1) Sample \((x,c)\sim p(x,c)\)  
  2) With probability \(p_{\text{uncond}}\), set \(c\leftarrow \emptyset\) (drop condition)  
  3) Sample noise level \(\lambda\sim p(\lambda)\), noise \(\epsilon\sim\mathcal N(0,I)\)  
  4) Corrupt: \(z_\lambda=\alpha_\lambda x+\sigma_\lambda \epsilon\)  
  5) Update \(\theta\) on denoising loss (Eq. 5): \(\mathbb E\|\epsilon_\theta(z_\lambda,c)-\epsilon\|_2^2\)

- **Sampling / guidance formula (Algorithm 2, Eq. 6):** two forward passes (conditional + unconditional) and linear combination  
  \[
  \tilde\epsilon_\theta(z_\lambda,c)=(1+w)\epsilon_\theta(z_\lambda,c)-w\,\epsilon_\theta(z_\lambda)
  \]
  \(w\ge 0\) increases condition adherence/fidelity but reduces diversity (truncation-like tradeoff).

- **Empirical knobs/results (Section 4.1):**
  - Best **FID** at small guidance: \(w=0.1\) or \(w=0.3\) (dataset-dependent).  
  - Best **IS** at strong guidance: \(w\ge 4\).  
  - ImageNet-128: at \(w=0.3\), their FID beats classifier-guided ADM-G (Dhariwal & Nichol, 2021).  
  - Conditioning dropout: \(p_{\text{uncond}}\in\{0.1,0.2\}\) works about equally well.

- **Defaults mentioned (Experiments):** log-SNR endpoints \(\lambda_{\min}=-20,\lambda_{\max}=20\); sampler noise interpolation \(v=0.3\) (64×64) / \(v=0.2\) (128×128).

</details>

### 📄 ControlNet (Zero-Conv Conditional Control for Stable Diffusion)
**Paper** · [source](https://openaccess.thecvf.com/content/ICCV2023/papers/Zhang_Adding_Conditional_Control_to_Text-to-Image_Diffusion_Models_ICCV_2023_paper.pdf)

*ControlNet mechanism: trainable UNet copy + zero-conv adapters, injection points, training objective preserving base model*

<details>
<summary>Key content</summary>

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

</details>

### 📄 DDPM core derivations (Ho et al., 2020)
**Paper** · [source](https://arxiv.org/abs/2006.11239)

*Original DDPM forward/reverse processes, ELBO terms, and simplified ε-prediction loss + sampling update.*

<details>
<summary>Key content</summary>

- **Reverse (generative) Markov chain (Eq. 1):**  
  \(p_\theta(x_{0:T}) := p(x_T)\prod_{t=1}^T p_\theta(x_{t-1}\mid x_t)\), with \(p(x_T)=\mathcal N(0,I)\) and  
  \(p_\theta(x_{t-1}\mid x_t)=\mathcal N(x_{t-1};\mu_\theta(x_t,t),\Sigma_\theta(x_t,t))\).
- **Forward (diffusion) process:** fixed Gaussian noising with schedule \(\beta_t\); define \(\alpha_t=1-\beta_t\), \(\bar\alpha_t=\prod_{s=1}^t \alpha_s\). Reparameterization used in training:  
  \(x_t=\sqrt{\bar\alpha_t}\,x_0+\sqrt{1-\bar\alpha_t}\,\epsilon,\ \epsilon\sim\mathcal N(0,I)\).
- **Variational bound / ELBO decomposition (Eq. 3, 5):**  
  \( \mathbb E[-\log p_\theta(x_0)] \le \mathbb E_q\Big[-\log p(x_T)-\sum_{t\ge1}\log \frac{p_\theta(x_{t-1}\mid x_t)}{q(x_t\mid x_{t-1})}\Big]=:L\).  
  Rewritten: \(L= L_T+\sum_{t>1} L_{t-1}+L_0\) where  
  \(L_T=D_{KL}(q(x_T\mid x_0)\|p(x_T))\),  
  \(L_{t-1}=D_{KL}(q(x_{t-1}\mid x_t,x_0)\|p_\theta(x_{t-1}\mid x_t))\),  
  \(L_0=-\log p_\theta(x_0\mid x_1)\).
- **Closed-form forward posterior (Eq. 6–7):**  
  \(q(x_{t-1}\mid x_t,x_0)=\mathcal N(x_{t-1};\tilde\mu_t(x_t,x_0),\tilde\beta_t I)\),  
  \(\tilde\mu_t=\frac{\sqrt{\bar\alpha_{t-1}}\beta_t}{1-\bar\alpha_t}x_0+\frac{\sqrt{\alpha_t}(1-\bar\alpha_{t-1})}{1-\bar\alpha_t}x_t\),  
  \(\tilde\beta_t=\frac{1-\bar\alpha_{t-1}}{1-\bar\alpha_t}\beta_t\).
- **ε-parameterization & sampling update (Alg. 2 / Eq. 10 style):** predict noise \(\epsilon_\theta(x_t,t)\) and sample  
  \(x_{t-1}=\frac{1}{\sqrt{\alpha_t}}\Big(x_t-\frac{\beta_t}{\sqrt{1-\bar\alpha_t}}\epsilon_\theta(x_t,t)\Big)+\sigma_t z,\ z\sim\mathcal N(0,I)\).
- **Simplified training objective (Eq. 14):** sample \(t\sim \text{Unif}\{1,\dots,T\}\), \(\epsilon\sim\mathcal N(0,I)\), set \(x_t=\sqrt{\bar\alpha_t}x_0+\sqrt{1-\bar\alpha_t}\epsilon\), minimize  
  \(\mathbb E\|\epsilon-\epsilon_\theta(x_t,t)\|^2\) (unweighted MSE).
- **Defaults / hyperparameters (Section 4):** \(T=1000\); linear \(\beta_t\) from \(\beta_1=10^{-4}\) to \(\beta_T=0.02\); data scaled to \([-1,1]\).
- **Empirical results:** unconditional CIFAR-10 Inception Score **9.46**, FID **3.17** (train-set FID); test-set FID **5.24**. On 256×256 LSUN, sample quality similar to ProgressiveGAN.

</details>

### 📄 Latent Diffusion Models (LDM) training pipeline + conditioning
**Paper** · [source](https://openaccess.thecvf.com/content/CVPR2022/papers/Rombach_High-Resolution_Image_Synthesis_With_Latent_Diffusion_Models_CVPR_2022_paper.pdf)

*LDM training pipeline details: autoencoder latent space, diffusion objective in latent, UNet + cross-attention conditioning, compute/quality tradeoffs & ablations.*

<details>
<summary>Key content</summary>

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

</details>

### 📖 Diffusers Stable Diffusion Pipelines — loading, inference, schedulers
**Reference Doc** · [source](https://huggingface.co/docs/diffusers/api/pipelines/stable_diffusion/stable_diffusion)

*Exact pipeline composition + canonical `from_pretrained` / `__call__` inference workflow; scheduler swapping; seed/generator usage; SDXL base+refiner latent handoff (`output_type="latent"`, `denoising_start/end`).*

<details>
<summary>Key content</summary>

- **Pipeline components (Stable Diffusion family):** Autoencoder (VAE), conditional UNet, CLIP text encoder, **scheduler**, CLIPImageProcessor, **safety checker**. Pipelines are **inference-only** (no training functionality).
- **Loading workflow (`from_pretrained`):**
  - Accepts HF Hub repo id (e.g., `"stable-diffusion-v1-5/stable-diffusion-v1-5"`) or local path (`"./stable-diffusion"`).
  - Uses `model_index.json` mapping: `<name>: ["<library>", "<class name>"]` to know which components to load.
  - `save_pretrained(path)` saves each component under `path/<component_name>/` and writes `model_index.json` at root.
- **Inference entrypoint:** pipeline `__call__` encapsulates preprocessing → diffusion loop → postprocessing; API varies by pipeline (text2img vs img2img vs inpaint).
- **Reproducibility / seed:** pass a Torch generator, e.g. `generator=torch.manual_seed(seed)` (example seed: `42`).
- **Scheduler swapping (procedure):**
  - `pipeline.scheduler = EulerDiscreteScheduler.from_config(pipeline.scheduler.config)` (example swap from `PNDMScheduler` to `EulerDiscreteScheduler`).
- **Empirical/model detail:** SD 2.1 commonly generates **768×768**; SD 1.5 **512×512** (as stated in examples narrative).
- **SDXL base→refiner two-stage (procedure + params):**
  - Base call: `denoising_end=high_noise_frac` and `output_type="latent"`.
  - Refiner call: `denoising_start=high_noise_frac`, `image=latent_image`.
  - Example values: `n_steps=40`, `high_noise_frac=0.8`.
- **SDXL defaults/flags:** `force_zeros_for_empty_prompt: bool = True` (default). `add_watermarker` defaults to True if `invisible_watermark` installed.

</details>

### 📖 Stable Diffusion ControlNet Pipelines (Diffusers)
**Reference Doc** · [source](https://huggingface.co/docs/diffusers/api/pipelines/controlnet)

*ControlNet pipeline parameters/behaviors (scales, guess mode, guidance windows, multi-ControlNet, image inputs) and integration with StableDiffusion pipelines.*

<details>
<summary>Key content</summary>

- **What ControlNet adds (design rationale):** Adds *spatial conditioning* to a pretrained text-to-image diffusion model while “locking” the base model; uses **zero convolutions** (zero-initialized conv layers) so added paths start at 0 and “no harmful noise” affects finetuning (per ControlNet paper abstract quoted).
- **Core pipelines/classes:**
  - `StableDiffusionControlNetPipeline(vae, text_encoder, tokenizer, unet, controlnet, scheduler, safety_checker, feature_extractor, image_encoder=None, requires_safety_checker=True)`
  - `StableDiffusionControlNetImg2ImgPipeline(... same components ...)`
- **Multi-ControlNet behavior:** `controlnet` can be a single `ControlNetModel` or a list/tuple; **outputs from each ControlNet are added together** to form combined conditioning.
- **Key call parameters (text2img ControlNet):**  
  `__call__(prompt, image, height=None, width=None, num_inference_steps=50, guidance_scale=7.5, eta=0.0, ... controlnet_conditioning_scale=1.0, guess_mode=False, control_guidance_start=0.0, control_guidance_end=1.0, clip_skip=None, ...)`
- **Key call parameters (img2img ControlNet):** adds `image` (init image) + `control_image` (ControlNet condition), `strength=0.8`; default `controlnet_conditioning_scale=0.8`.
- **ControlNet scaling formula (API behavior):**  
  **Residual_added = Residual_unet + (controlnet_conditioning_scale × ControlNet_output)**  
  (`controlnet_conditioning_scale` can be `float` or `list[float]` matching multiple ControlNets).
- **Guess mode:** ControlNet encoder “recognizes content” even with prompts removed; recommended `guidance_scale` **3.0–5.0**.
- **Control guidance window:** `control_guidance_start/end` are **fractions of total steps** when ControlNet starts/stops applying; can be per-ControlNet lists.
- **Image input expectations:** `image`/`control_image` accept `PIL`, `np.ndarray`, `torch.Tensor`; if `height/width` provided, control image is resized; for multiple ControlNets, pass a **list** (or list-of-lists for batching per prompt).

</details>

---

## Related Topics

- [[topics/text-to-video|Text-to-Video]]
- [[topics/contrastive-learning|Contrastive Learning]]
- [[topics/multimodal-fundamentals|Multimodal Fundamentals]]
- [[topics/image-generation|Image Generation & Editing]]
