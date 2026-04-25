## Key Facts & Specifications

### DDPM forward (noising) process definitions
- Diffusion models are latent-variable models with latents \(x_1,\dots,x_T\) of the **same dimensionality** as data \(x_0\). (Ho et al., 2020, NeurIPS PDF: https://proceedings.neurips.cc/paper/2020/file/4c5bcfec8584af0d967f1ab10179ca4b-Paper.pdf)
- Forward process is a Markov chain that **adds Gaussian noise** with a variance schedule \(\beta_1,\dots,\beta_T\):  
  \[
  q(x_{1:T}\mid x_0)=\prod_{t=1}^T q(x_t\mid x_{t-1}),\quad
  q(x_t\mid x_{t-1})=\mathcal{N}(x_t;\sqrt{1-\beta_t}\,x_{t-1},\beta_t I)
  \]
  (Ho et al., 2020, Eq. (2) in NeurIPS PDF)
- Define \(\alpha_t := 1-\beta_t\) and \(\bar{\alpha}_t := \prod_{s=1}^t \alpha_s\). Then the marginal at arbitrary timestep \(t\) has closed form:  
  \[
  q(x_t\mid x_0)=\mathcal{N}(x_t;\sqrt{\bar{\alpha}_t}x_0,(1-\bar{\alpha}_t)I)
  \]
  (Ho et al., 2020, Eq. (4) NeurIPS PDF; Nichol & Dhariwal, 2021, Eq. (8) https://proceedings.mlr.press/v139/nichol21a/nichol21a.pdf)

### DDPM reverse (denoising) process parameterization
- Reverse process is modeled as Gaussian conditionals:
  \[
  p_\theta(x_{t-1}\mid x_t)=\mathcal{N}(x_{t-1};\mu_\theta(x_t,t),\Sigma_\theta(x_t,t))
  \]
  (Ho et al., 2020 NeurIPS PDF; also summarized in johnsee.net blog quoting the paper: https://johnsee.net/blog/2020/DDPM/)
- The true posterior conditioned on \(x_0\) is Gaussian:
  \[
  q(x_{t-1}\mid x_t,x_0)=\mathcal{N}(x_{t-1};\tilde{\mu}_t(x_t,x_0),\tilde{\beta}_t I)
  \]
  (Ho et al., 2020 NeurIPS PDF Eq. (6); also restated in ApX “Mathematical Formulation…”: https://apxml.com/courses/intro-diffusion-models/chapter-3-reverse-diffusion-process/math-formulation-denoising-step)
- Two fixed variance choices reported as having **similar results**:
  - \(\sigma_t^2=\beta_t\)
  - \(\sigma_t^2=\tilde{\beta}_t=\frac{1-\bar{\alpha}_{t-1}}{1-\bar{\alpha}_t}\beta_t\)  
  (Ho et al., 2020 NeurIPS PDF; johnsee.net summary quoting the same: https://johnsee.net/blog/2020/DDPM/; ApX page also states these options)

### DDPM sampling / reconstruction identity
- Progressive estimate of \(x_0\) from \(x_t\) and predicted noise:
  \[
  \hat{x}_0=\frac{x_t-\sqrt{1-\bar{\alpha}_t}\,\epsilon_\theta(x_t,t)}{\sqrt{\bar{\alpha}_t}}
  \]
  (Ho et al., 2020 NeurIPS PDF Eq. (15))

### Common DDPM hyperparameters (as reported in secondary sources)
- A commonly cited “linear variance schedule” in DDPM uses:
  - \(T=1000\)
  - \(\beta\) range \([0.0001, 0.02]\)  
  (learnopencv DDPM guide: https://learnopencv.com/denoising-diffusion-probabilistic-models/; also shown in johnsee.net table quoting DDPM: https://johnsee.net/blog/2020/DDPM/)  
  **Note:** These values appear in secondary sources; the search results excerpt does not show the exact DDPM paper section listing them.

### Improved DDPM cosine schedule (Nichol & Dhariwal, 2021)
- Cosine schedule defined via \(\bar{\alpha}_t=f(t)/f(0)\) with:
  \[
  f(t)=\cos^2\left(\frac{t/T+s}{1+s}\cdot\frac{\pi}{2}\right)
  \]
  and \(\beta_t = 1-\frac{\bar{\alpha}_t}{\bar{\alpha}_{t-1}}\).  
  (Nichol & Dhariwal, 2021, Eq. (16) https://proceedings.mlr.press/v139/nichol21a/nichol21a.pdf)
- In practice they **clip** \(\beta_t \le 0.999\) “to prevent singularities” near \(t=T\). (Nichol & Dhariwal, 2021)

### Classifier-Free Guidance (CFG)
- CFG avoids training a separate classifier by **jointly training** conditional and unconditional behavior by randomly dropping conditioning with probability \(p_{\text{uncond}}\). (Ho & Salimans, 2022 https://arxiv.org/abs/2207.12598; Algorithm 1 in PDF)
- CFG trades off **sample fidelity vs diversity** similarly to classifier guidance; increasing guidance strength decreases variety and increases fidelity. (Ho & Salimans, 2022 PDF https://arxiv.org/pdf/2207.12598.pdf)

### Stable Diffusion / latent scaling factor
- Stable Diffusion config uses `scale_factor: 0.18215` (referenced in diffusers issue pointing to CompVis config). (Hugging Face diffusers issue #437: https://github.com/huggingface/diffusers/issues/437)
- Rombach (CompVis) explanation (in that issue thread): scale factor was introduced in the latent diffusion paper to make latent space have **approximately unit variance**, enabling similar noise schedules across different autoencoders; computed as a simple global rescaling (user paraphrase confirmed by author: “Yes, your understanding is correct.”). (diffusers issue #437)

### CLIP prompt length / embeddings (Stable Diffusion in diffusers context)
- CLIP text encoder has a **77 token limit** in this context; chunking prompts into segments padded to 77 yields embeddings shaped like \((1,77,768)\) per chunk; concatenation yields e.g. \((1,154,768)\). (diffusers issue #2136: https://github.com/huggingface/diffusers/issues/2136)

### Diffusers Stable Diffusion pipeline constraints & defaults
- `guidance_scale` default shown as **7.5**; guidance enabled when `guidance_scale > 1`. (diffusers `pipeline_stable_diffusion.py`: https://github.com/huggingface/diffusers/blob/main/src/diffusers/pipelines/stable_diffusion/pipeline_stable_diffusion.py)
- Default `num_inference_steps` is **50** in the pipeline signature; docs note more steps usually improve quality but slow inference. (same file)
- `height` and `width` must be **divisible by 8**. (same file)
- DDIM parameter `eta` is documented as between **[0, 1]** and only used by `DDIMScheduler`. (same file)

### ControlNet core design facts
- ControlNet “copies the weights” of network blocks into a **locked copy** and a **trainable copy**; the locked copy preserves the original model. (ControlNet README: https://github.com/lllyasviel/ControlNet/blob/main/README.md)
- “Zero convolution” is a **1×1 convolution** with weight and bias initialized to **zeros**; before training it outputs zeros so ControlNet causes no distortion initially. (ControlNet README)

### DiT (Diffusion Transformer) scaling results & specs
- DiT replaces U-Net backbone with a transformer operating on **latent patches**. (Peebles & Xie, 2023 https://arxiv.org/abs/2212.09748)
- DiTs with higher compute (measured in **Gflops**) “consistently have lower FID.” (Peebles & Xie, 2023 arXiv/ICCV paper PDF)
- Reported benchmark: DiT-XL/2 achieves **FID 2.27** on class-conditional ImageNet **256×256**. (Peebles & Xie, 2023 arXiv abstract)
- DiT model size/compute ranges reported on project page:
  - Parameters: **33M to 675M**
  - Compute: **0.4 to 119 Gflops**
  - Patch sizes explored: **2, 4, 8**
  - Halving patch size **quadruples** token count and at least quadruples Gflops. (DiT project page: https://www.wpeebles.com/DiT; also in ICCV paper text)

### Stable Diffusion 3 (MMDiT) stated architecture points (blog summary)
- Uses three text embedders: **two CLIP models and T5**; uses an improved autoencoding model for image tokens. (Stability AI SD3 research post: https://stability.ai/news-updates/stable-diffusion-3-research-paper)
- MMDiT uses **separate sets of weights** for image and language representations; sequences are joined for attention so information flows between modalities. (same Stability AI post)
- Scaling study mentioned: models from **15 blocks / 450M parameters** to **38 blocks / 8B parameters**. (same Stability AI post)

### Troubleshooting: black images / NaNs (AUTOMATIC1111 issue)
- Suggested workaround for black images: add `--no-half-vae`. (AUTOMATIC1111 issue #6723: https://github.com/AUTOMATIC1111/stable-diffusion-webui/issues/6723)
- Comment claims a “widespread leaked Nai VAE” can produce **NaNs with FP16 at high resolutions**; proposes using **bfloat16** for VAE on Ampere+ GPUs; notes PyTorch interpolate bfloat16 support was merged in nightly `torch-2.0.0.dev20230228`. (same issue thread)

---

## Technical Details & Procedures

### DDPM: closed-form noising (“jump to timestep”)
- Given \(x_0\), sample \(x_t\) directly:
  \[
  x_t=\sqrt{\bar{\alpha}_t}x_0+\sqrt{1-\bar{\alpha}_t}\,\epsilon,\quad \epsilon\sim\mathcal{N}(0,I)
  \]
  (Ho et al., 2020 NeurIPS PDF Eq. (4); Nichol & Dhariwal, 2021 Eq. (8))

### DDPM: reverse-step mean using \(\epsilon_\theta\)
- One commonly used parameterization (as summarized in ApX and johnsee.net) for the reverse mean:
  \[
  \mu_\theta(x_t,t)=\frac{1}{\sqrt{\alpha_t}}\left(x_t-\frac{\beta_t}{\sqrt{1-\bar{\alpha}_t}}\epsilon_\theta(x_t,t)\right)
  \]
  (ApX “Mathematical Formulation…”; johnsee.net DDPM derivation page)

### DDPM: sampling update (stochastic)
- Sample step:
  \[
  x_{t-1}=\mu_\theta(x_t,t)+\sigma_t z,\quad z\sim\mathcal{N}(0,I)
  \]
  with \(\sigma_t^2\) chosen as \(\beta_t\) or \(\tilde{\beta}_t\). (ApX page; Ho et al., 2020 NeurIPS PDF discussion of fixed \(\Sigma_\theta\))

### DDPM training objective (noise-prediction MSE in practice)
- Example training loop (code excerpt) samples random timestep \(t\), constructs \(x_t\), predicts noise, and uses MSE:
  ```python
  noise = torch.randn_like(x_start)
  x_noisy = q_sample(x_start, t, noise=noise)
  predicted_noise = model(x_noisy, t)
  loss = F.mse_loss(noise, predicted_noise)
  ```
  (arXiv HTML “Understanding Diffusion Models via Code Execution”: https://arxiv.org/html/2512.07201v1)

### Improved DDPM cosine schedule procedure
- Define \(\bar{\alpha}_t\) via cosine formula (Eq. 16), then compute:
  \[
  \beta_t = 1-\frac{\bar{\alpha}_t}{\bar{\alpha}_{t-1}}
  \]
- Clip: \(\beta_t \le 0.999\). (Nichol & Dhariwal, 2021)

### CFG: training procedure (conditioning dropout)
- Algorithm 1 includes: sample \((x,c)\), then set \(c\leftarrow \emptyset\) with probability \(p_{\text{uncond}}\). (Ho & Salimans, 2022 PDF)

### CFG: inference mixing (diffusers implementation pattern)
- In diffusers pipelines, the guidance combination is implemented as:
  ```python
  noise_pred_uncond, noise_pred_text = noise_pred.chunk(2)
  noise_pred = noise_pred_uncond + guidance_scale * (noise_pred_text - noise_pred_uncond)
  ```
  (Hugging Face forum thread quoting diffusers code: https://discuss.huggingface.co/t/why-does-classifer-free-guidance-cfg-add-guidances-to-a-negative-prompts-conditional-distribution-instead-of-an-unconditional-distribution/37491)

### Long prompts in diffusers by chunking embeddings
- Procedure (from diffusers issue #2136) to exceed 77 tokens:
  - Tokenize prompt without truncation.
  - Split token IDs into chunks of `max_length = pipe.tokenizer.model_max_length` (77).
  - Encode each chunk with text encoder to get tensors shaped \((1,77,768)\).
  - Concatenate along sequence dimension to get \((1, 77*k, 768)\).
- Working code snippet provided in the issue (uses `StableDiffusionPipeline`, `prompt_embeds`, `negative_prompt_embeds`). (diffusers issue #2136)

### Diffusers Stable Diffusion pipeline: key parameter checks
- `height` and `width` must be divisible by 8 or a `ValueError` is raised. (pipeline_stable_diffusion.py)
- `guidance_scale > 1` enables CFG (`do_classifier_free_guidance`). (pipeline_stable_diffusion.py)
- `eta` is only passed if the scheduler step accepts it; documented range [0,1]. (pipeline_stable_diffusion.py)
- Custom schedules:
  - `retrieve_timesteps` enforces **only one** of `timesteps` or `sigmas` can be passed; otherwise raises `ValueError`. (pipeline_stable_diffusion.py)

### ControlNet: environment setup (official README)
- Create and activate conda env:
  ```bash
  conda env create -f environment.yaml
  conda activate control
  ```
  (ControlNet README)

### ControlNet model I/O example (OpenVINO notebook)
- Example ControlNet inputs (shapes explicitly shown):
  - `sample`: `torch.randn((2, 4, 64, 64))`
  - `timestep`: `torch.tensor(1)`
  - `encoder_hidden_states`: `torch.randn((2,77,768))`
  - `controlnet_cond`: `torch.randn((2,3,512,512))`
- Output described as “down and middle block” residual samples used as additional context for UNet. (OpenVINO notebook: https://docs.openvino.ai/2023.3/notebooks/235-controlnet-stable-diffusion-with-output.html)

---

## Comparisons & Trade-offs

### DDPM vs DDIM sampling (as described in ApX course page)
- Speed:
  - DDPM sampling typically uses **T steps** (often \(T=1000\)), requiring T sequential network evaluations.
  - DDIM can use a subsequence \(S<T\) (examples given: **50, 100, 200**), reducing evaluations; “DDIM with 100 steps can be 10 times faster than DDPM with 1000 steps.” (ApX trade-offs page: https://apxml.com/courses/intro-diffusion-models/chapter-5-sampling-generation-process/tradeoffs-ddpm-ddim)
- Stochasticity:
  - DDPM: “always stochastic” (per that page’s summary table).
  - DDIM: controlled by \(\eta\); \(\eta=0\) deterministic; \(\eta=1\) behaves similarly to DDPM in stochasticity. (ApX trade-offs page)
- Quality:
  - DDPM with many steps produces high fidelity; DDIM can be comparable but may degrade if too few steps (page mentions “below 20–50” can degrade, model-dependent). (ApX trade-offs page)

### CFG vs classifier guidance (Ho & Salimans, 2022)
- Classifier guidance requires training a separate classifier; CFG does not. (Ho & Salimans, 2022)
- Both provide a trade-off between fidelity and diversity by varying guidance strength. (Ho & Salimans, 2022)

### ControlNet vs depth-to-image model (community guide)
- ControlNet can be used with **any v1 or v2** Stable Diffusion models; depth-to-image model referenced as a v2 model. (stable-diffusion-art ControlNet guide: https://stable-diffusion-art.com/controlnet/)
- ControlNet is described as more versatile (supports depth, edge, pose, etc.). (same guide)
- Note: these are community guide claims, not the ControlNet paper/README.

### DiT scaling: parameters vs compute
- DiT results emphasize compute (Gflops) rather than parameter count:
  - Example claim: DiT-XL/8 has slightly more parameters than XL/2 but “much fewer Gflops” and performs poorly; compute is “key.” (DiT project page: https://www.wpeebles.com/DiT)
- Concrete compute comparisons at 256×256 (project page):
  - LDM-4: **103 Gflops**
  - ADM-U: **742 Gflops**
  - DiT-XL/2: **119 Gflops**  
  and at 512×512:
  - ADM-U: **2813 Gflops**
  - XL/2: **525 Gflops**  
  (DiT project page)

### Precision trade-off for VAE (AUTOMATIC1111 issue)
- `--no-half-vae` increases VRAM usage and can reduce performance, but may avoid NaNs/black images for some VAEs. (AUTOMATIC1111 issue #6723)
- Proposed alternative: bfloat16 VAE on Ampere+ to avoid NaNs while being closer in speed to fp16 than float32; depends on PyTorch bfloat16 interpolate support. (same issue thread)

---

## Architecture & Design Rationale

### Why DDPM uses small \(\beta_t\) and Gaussian reverse conditionals
- Ho et al. state expressiveness of reverse process is ensured in part by choosing Gaussian conditionals in \(p_\theta(x_{t-1}\mid x_t)\) because forward and reverse have the same functional form when \(\beta_t\) are small. (Ho et al., 2020 NeurIPS PDF)

### Why latent scaling factor exists in Stable Diffusion
- Rombach explanation: `scale_factor` was introduced to handle different latent spaces from different autoencoders with similar noise schedules; it ensures the diffusion model operates on latents with approximately **unit variance**. (diffusers issue #437)

### ControlNet: locked/trainable copies + zero conv
- Rationale in README:
  - Locked copy preserves the “production-ready diffusion model.”
  - Trainable copy learns the new condition.
  - Zero conv initialized to zeros ensures no distortion before training; “no layer is trained from scratch,” i.e., it is fine-tuning. (ControlNet README)

### DiT conditioning via adaLN / identity initialization
- DiT block design rationale:
  - Uses adaptive layer norm (adaLN) to inject conditioning (timestep/class embedding).
  - adaLN-Zero variant initializes each block as the **identity function** by regressing modulation parameters and initializing outputs to zero, analogous to zero-initializing final conv in residual blocks. (DiT project page; ICCV paper text excerpts)

### SD3 MMDiT: separate modality weights + joint attention
- Stability AI describes rationale:
  - Text and image embeddings are “conceptually quite different,” so use separate weights.
  - Join sequences for attention so modalities can “take the other one into account,” improving comprehension/typography. (Stability AI SD3 research post)

---

## Common Questions & Answers

### Q1: What is the exact forward noising distribution in DDPM?
- DDPM uses:
  \[
  q(x_t\mid x_{t-1})=\mathcal{N}(x_t;\sqrt{1-\beta_t}x_{t-1},\beta_t I)
  \]
  and the closed-form marginal:
  \[
  q(x_t\mid x_0)=\mathcal{N}(x_t;\sqrt{\bar{\alpha}_t}x_0,(1-\bar{\alpha}_t)I)
  \]
  (Ho et al., 2020 NeurIPS PDF Eq. (2) and Eq. (4))

### Q2: How do you compute \(\bar{\alpha}_t\) and what does it mean?
- \(\alpha_t=1-\beta_t\), \(\bar{\alpha}_t=\prod_{s=1}^t \alpha_s\). It appears in the closed-form \(q(x_t\mid x_0)\) and determines the signal/noise mixture. (Ho et al., 2020 NeurIPS PDF)

### Q3: What variance do we use in the reverse process?
- Ho et al. report setting \(\Sigma_\theta(x_t,t)=\sigma_t^2 I\) to untrained time-dependent constants; both \(\sigma_t^2=\beta_t\) and \(\sigma_t^2=\tilde{\beta}_t=\frac{1-\bar{\alpha}_{t-1}}{1-\bar{\alpha}_t}\beta_t\) had similar results. (Ho et al., 2020 NeurIPS PDF; also restated in johnsee.net and ApX page)

### Q4: What is the “simplified” DDPM training loss people implement?
- A common implementation trains \(\epsilon_\theta(x_t,t)\) to predict the noise used to form \(x_t\), minimizing MSE between predicted and true noise. (arXiv HTML tutorial with code: https://arxiv.org/html/2512.07201v1)

### Q5: How does classifier-free guidance work at training time?
- During joint training, conditioning \(c\) is randomly dropped (set to \(\emptyset\)) with probability \(p_{\text{uncond}}\), so the same model learns conditional and unconditional behavior. (Ho & Salimans, 2022 PDF, Algorithm 1)

### Q6: What is the exact CFG combination formula used in diffusers?
- diffusers uses:
  \[
  \text{noise} = \text{noise}_{\text{uncond}} + s(\text{noise}_{\text{text}}-\text{noise}_{\text{uncond}})
  \]
  implemented by chunking the batch into unconditional and conditional halves. (HF forum thread quoting diffusers code: https://discuss.huggingface.co/t/why-does-classifer-free-guidance-cfg-add-guidances-to-a-negative-prompts-conditional-distribution-instead-of-an-unconditional-distribution/37491)

### Q7: Why does Stable Diffusion scale latents by 0.18215?
- The `scale_factor` is used to rescale VAE latents so the diffusion model operates on a latent space with approximately **unit variance**, enabling similar noise schedules across different autoencoders. (diffusers issue #437, comment by @rromb: https://github.com/huggingface/diffusers/issues/437)

### Q8: What is the CLIP token limit and how do people exceed it in diffusers?
- In this context CLIP has a **77 token** limit; one workaround is chunking into 75-token segments (plus start/end to 77), encoding each chunk to \((1,77,768)\), then concatenating to e.g. \((1,154,768)\) before passing to the U-Net. (diffusers issue #2136)

### Q9: What constraints does the diffusers Stable Diffusion pipeline enforce on image size?
- `height` and `width` must be divisible by **8**. (diffusers `pipeline_stable_diffusion.py`)

### Q10: What is “zero convolution” in ControlNet and why doesn’t it block learning?
- ControlNet defines “zero convolution” as a **1×1 convolution** with weights and bias initialized to **zero**, so it outputs zeros before training and initially does not distort the base model. The README explicitly addresses the FAQ that “if the weight is zero, the gradient will also be zero” and states “This is not true.” (ControlNet README)

### Q11: What concrete performance number is reported for DiT?
- DiT-XL/2 reports **FID 2.27** on class-conditional ImageNet **256×256**. (Peebles & Xie, 2023 arXiv abstract: https://arxiv.org/abs/2212.09748)

### Q12: Why might Stable Diffusion WebUI sometimes output black images?
- In one reported case, users suggest `--no-half-vae` and attribute black images to NaNs produced by a particular VAE when run in FP16 at high resolutions. (AUTOMATIC1111 issue #6723)