---
title: "Text-to-Video"
subject: "Multimodal AI"
date: 2025-01-01
tags:
  - "subject/multimodal-ai"
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

# Text To Video

## Video (best)
- **Yannic Kilcher** — "Sora - OpenAI's Text-to-Video Model (Paper Explained)"
- **Watch:** [YouTube](https://www.youtube.com/watch?v=_gCqFBFd_Ls)
- Why: Yannic Kilcher provides rigorous technical breakdowns of the Sora technical report, covering the diffusion transformer architecture, temporal consistency, and spacetime patch representations — directly relevant to the core concepts in this topic.
- Level: intermediate/advanced

## Blog / Written explainer (best)
- **Lilian Weng** — "Video Generation Models as World Simulators"
- **Link:** [https://lilianweng.github.io/posts/2024-04-12-diffusion-video/](https://lilianweng.github.io/posts/2024-04-12-diffusion-video/)
- Why: Lilian Weng's posts are consistently the gold standard for systematic, well-cited technical overviews. This post covers the evolution from image diffusion to video generation, temporal attention mechanisms, and consistency challenges — mapping directly onto the related concepts in this topic.
- Level: intermediate/advanced

## Deep dive
- **OpenAI Technical Report** — "Video generation models as world simulators (Sora Technical Report)"
- **Link:** [https://openai.com/research/video-generation-models-as-world-simulators](https://openai.com/research/video-generation-models-as-world-simulators)
- Why: The Sora technical report is the most comprehensive publicly available reference on large-scale text-to-video generation, covering spacetime latent patches, temporal consistency, and scaling behavior. It is the de facto deep-dive reference for this topic.
- Level: advanced

## Original paper
- **Ho et al. / Singer et al.** — "Make-A-Video: Text-to-Video Generation without Text-Video Data"
- **Link:** [https://arxiv.org/abs/2209.14430](https://arxiv.org/abs/2209.14430)
- Why: Make-A-Video is one of the most readable and pedagogically clear seminal papers in text-to-video, building directly on text-to-image diffusion and introducing the temporal attention extension in a well-explained way. It bridges text-to-image knowledge (which learners likely already have) with video generation, making it the most accessible entry point into the literature.
- Level: intermediate/advanced

## Code walkthrough
- None identified
- Why: There is no widely recognized, high-quality hands-on code walkthrough for text-to-video generation from a trusted educator (e.g., Karpathy, fast.ai) that is clearly documented and pedagogically structured. Most available notebooks are unofficial and of inconsistent quality. The closest practical resource is the Hugging Face Diffusers library documentation for text-to-video pipelines (https://huggingface.co/docs/diffusers/api/pipelines/text_to_video [NOT VERIFIED]), but this is API documentation rather than a true walkthrough.

## Coverage notes
- **Strong:** Conceptual explanation of Sora and diffusion-based video generation; temporal attention as an architectural concept; connection to text-to-image diffusion models
- **Weak:** Hands-on implementation walkthroughs are sparse — open-source text-to-video models (e.g., ModelScope, CogVideo) have limited pedagogical code resources
- **Gap:** No excellent beginner-level video exists that builds from first principles (e.g., "what makes video generation harder than image generation") without assuming prior knowledge of diffusion models. The connection between the related concepts listed (mel spectrogram, speech-to-speech, Whisper, VALL-E) and text-to-video is not well-served by any single resource — these appear to be from a multimodal course where audio and video generation are taught together, but no resource bridges them cleanly.

---

## Additional Resources for Tutor Depth

> **9 sources** — papers, official docs, working code, benchmarks, and deep explainers that give the AI tutor precision on this topic.

### 📄 True Temporal Super-Resolution via Deep Internal Learning
**Paper** · [source](https://ar5iv.labs.arxiv.org/html/2003.08872)

*Temporal SR (beyond interpolation) + internal, video-specific training; coarse-to-fine temporal×2 with spatial/temporal back-projection.*

<details>
<summary>Key content</summary>

- **TSR vs interpolation (Abstract/Intro):** True Temporal Super-Resolution (TSR) recovers **high temporal frequencies beyond the input Nyquist limit**, resolving **motion blur + motion aliasing**; frame interpolation cannot undo either (it “adds new blurry frames” and preserves aliased motion).
- **Forward model (Intro):** Low-temporal-resolution (LTR) video relates to high-temporal-resolution (HTR) via **temporal blur + subsampling**:  
  **LTR = (HTR ⊛ₜ h) ↓ₜ**  
  where **h** is a **rectangular temporal blur kernel** induced by exposure time; paper often assumes **exposure time ≈ inter-frame time**.
- **Key observation (Sec. 2):** Small **space-time (ST) patches** recur not only **across scales** but also **across dimensions** by **swapping spatial and temporal axes** (x–t, y–t slices). Fast motion makes x–t/y–t slices look like **temporally downscaled** versions of x–y frames → x–y frames provide internal supervision for temporal upsampling.
- **Internal training set (Sec. 3):**
  - **Within-dimension pairs:** build a spatio-temporal pyramid; **downscale space+time by same factor** to preserve motion/blur statistics; create LTR by **temporal blur (frame averaging) + subsample**.
  - **Across-dimension pairs:** rotate 3D volume (swap x↔t or y↔t), apply “temporal” downscaling along the new time axis; use as extra training pairs.
  - Augmentations: mirror flips, **90° rotations**, time reversal.
- **Network & optimization (Sec. 4.1):** **8-layer 3D CNN**, 128 channels each, ReLU; mix of **3×3×3** and **1×3×3** kernels, stride 1; input is **cubic temporally interpolated** video; network predicts **residual** to HTR. Training crops: **36×36×16** ST crop, sampled proportional to mean gradient magnitude. Loss: **L1**. Optimizer: **Adam**. LR starts **1e-3**, decreased per ZSSR schedule until **1e-6** stop.
- **Coarse-to-fine (Sec. 4.2):** Train on spatially downscaled video (typically **¼**, or **½** for small videos). Apply TSR×2, then **spatio-temporal back-projection** to raise spatial res ×2 while enforcing **bicubic spatial consistency** and **rect temporal consistency**; iterate up the diagonal to target.
- **Runtime (Sec. 4.1):** ~**2 hours/video** training on **single Nvidia V100**; inference at **720×1280** takes ~**1 minute**.
- **Empirical (Sec. 5, Table 2 ablation at coarse scale):**  
  - Only within: **PSNR 33.96**, **SSIM 0.962**  
  - Only across: **PSNR 34.25 (+0.28)**, **SSIM 0.964 (+0.002)**  
  - Best config: **PSNR 34.33 (+0.37)**, **SSIM 0.965 (+0.003)**  
  Cross-dimension examples often more informative; preferences vary by video.

</details>

### 📄 VALL‑E 2 — Grouped Neural Codec LM + Repetition‑Aware Sampling
**Paper** · [source](http://arxiv.org/pdf/2406.05370.pdf)

*Neural codec tokenization + codec-language-model formulation for zero-shot TTS; decoding/sampling (repetition-aware) over discrete audio token streams.*

<details>
<summary>Key content</summary>

- **Codec tokenization setup (Sec. 4.1.1):** Text tokenization via **BPE**. Speech tokenization via **EnCodec @ 6 kbps, 24 kHz**; waveform decoding via **Vocos**.
- **Grouped codec language modeling (Sec. 3.1, Eq. 1–4):** Audio → codec codes \(c\) of length \(T\), with \(Q\) quantizers (paper uses **8 code streams** per time step). Partition into groups of size \(g\): grouped sequence \(\tilde{c}=\{\tilde{c}_1,\dots,\tilde{c}_{T/g}\}\). Train by NLL:
  - **Eq. (1–2):** minimize \(-\log p(\tilde{c}\mid x)= -\sum_i \log p(\tilde{c}_i \mid \tilde{c}_{<i}, x)\), where \(x\) is text tokens.
  - **Inference (Eq. 3–4):** prompt with enrolled speech codes \(\tilde{c}^{(p)}\) + text (prompt transcript + target text) to generate target grouped codes \(\tilde{c}^{(t)}\), then decode to waveform.
  - **Rationale:** grouping reduces sequence length by factor \(g\) → faster inference + mitigates long-context errors.
- **Hierarchical modeling (Sec. 3.2):**
  - **AR model** generates **first code stream** (coarse) per frame/group causally.
  - **NAR model** generates remaining **code streams 2–8** conditioned on text + prompt + preceding streams (full attention); run **7 passes** with greedy decoding (Sec. 3.4.2).
- **Repetition‑Aware Sampling (Sec. 3.4.1, Alg. 1):** Start with nucleus sampling (top‑\(p\)). Compute repetition ratio of sampled token within a history window \(w\); if ratio \(>\tau\), **replace** with **random sampling** from the distribution to avoid infinite loops. Hyperparams used in eval: **\(w=50\)**, **\(\tau=0.1\)**; top‑\(p\) searched **0.0–1.0 in 0.1 steps** (Sec. 4.1.3).
- **Empirical results (LibriSpeech test-clean, Table 1):** Single-sampling robustness improves vs VALL‑E:
  - **VALL‑E:** SIM **0.773**, WER **2.3**, DNSMOS **3.942** (3s prefix prompt).
  - **VALL‑E 2 (g=1):** SIM **0.782**, WER **1.6**, DNSMOS **3.947** (3s prefix).
  - **VALL‑E 2 (g=2):** SIM **0.777**, WER **1.5**, DNSMOS **3.966** (3s prefix).
- **Multi-sample selection (Eq. 23):** For 5 samples, select by sorting on **WER if SIM>0.3 else SIM** (lexicographic argmax).

</details>

### 📄 Video Diffusion Models (Ho et al., 2022) — training, factorized 3D U-Net, conditional sampling
**Paper** · [source](https://arxiv.org/abs/2204.03458)

*Primary training/sampling procedure for spatiotemporal diffusion; factorized space-time architecture; reconstruction-guided conditional sampling for long/HR video.*

<details>
<summary>Key content</summary>

- **Forward diffusion (Eq. 1):** continuous-time Gaussian process with latents \(z_t, t\in[0,1]\)  
  \[
  q(z_t|x)=\mathcal N(z_t;\alpha_t x,\sigma_t^2 I),\quad
  q(z_t|z_s)=\mathcal N\!\left(z_t;\frac{\alpha_t}{\alpha_s}z_s,\sigma_{t|s}^2 I\right)
  \]
  where \(\alpha_t\) scales signal, \(\sigma_t\) noise; \(q(z_1)\approx \mathcal N(0,I)\).
- **Training denoiser (Eq. 2):** weighted MSE over times \(t\)  
  \[
  \mathbb E_{\epsilon,t}\big[w(\lambda_t)\|\hat x_\theta(z_t)-x\|_2^2\big]
  \]
  Uses **\(\epsilon\)-prediction**: \(\hat x_\theta(z_t)=\frac{z_t-\sigma_t\epsilon_\theta(z_t)}{\alpha_t}\); \(t\) sampled with **cosine schedule**. Also mentions **v-prediction** for some models.
- **Ancestral sampling (Eq. 3–4):** reverse conditional
  \[
  \tilde\mu_{s|t}(z_t,x)=e^{\lambda_t-\lambda_s}\frac{\alpha_s}{\alpha_t}z_t+(1-e^{\lambda_t-\lambda_s})\alpha_s x,\quad
  \tilde\sigma^2_{s|t}=(1-e^{\lambda_t-\lambda_s})\sigma_s^2
  \]
  Step: \(z_s=\tilde\mu_{s|t}(z_t,\hat x_\theta(z_t))+\big(\tilde\sigma^2_{s|t}\big)^{1-\gamma}\big(\sigma^2_{t|s}\big)^\gamma \epsilon\). \(\gamma\) controls stochasticity.
- **Classifier-free guidance (Eq. 6):**
  \[
  \tilde\epsilon_\theta(z_t,c)=(1+w)\epsilon_\theta(z_t,c)-w\epsilon_\theta(z_t)
  \]
  \(w\)=guidance strength; unconditional can be \(c=0\).
- **Video architecture (Section 3):** **factorized space-time 3D U-Net**. Replace 2D convs with **space-only 3D convs** (e.g., \(3\times3\to 1\times3\times3\)); add **separate temporal attention blocks** (factorized attention for efficiency). Can be **masked to run as independent images**, enabling **joint image+video training** (reduces minibatch gradient variance; improves sample quality).
- **Conditional long/HR generation (Section 3.1):** **reconstruction-guided sampling** fixes incoherence of “replacement method” imputation. For super-resolution conditioning (Eq. 8):
  \[
  \tilde x_\theta(z_t)=\hat x_\theta(z_t)-w_r\frac{\alpha_t}{2}\nabla_{z_t}\|x_a-\hat x^a_\theta(z_t)\|_2^2
  \]
  where \(x_a\)=low-res/known part; \(\hat x^a_\theta\)=downsampled reconstruction from model output; \(w_r>1\) often improves quality. Works well with **predictor-corrector + Langevin**.
- **Empirical note:** Replacement method yields **blockwise temporal incoherence**; reconstruction guidance yields **coherent** long videos (Fig. 4). Reported evaluation includes FVD change **16.2 → 16.9** under a stricter evaluation variant.

</details>

### 📄 Video Diffusion Models (Ho et al., NeurIPS 2022)
**Paper** · [source](https://proceedings.neurips.cc/paper_files/paper/2022/file/39235c56aef13fb05a6adc95eb9d8d66-Paper-Conference.pdf)

*Joint image+video training; space-time noise/sampling; factorized 3D U-Net + temporal attention; reconstruction-guided conditional sampling for temporal coherence/extension.*

<details>
<summary>Key content</summary>

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

</details>

### 📊 VBench (CVPR’24) — Reproducible Video-Gen Evaluation + Scoring
**Benchmark** · [source](https://github.com/Vchitect/VBench)

*Reference implementation (scripts/configs/CLI) to compute VBench metrics and aggregate scores for reproducible comparisons.*

<details>
<summary>Key content</summary>

- **What VBench evaluates (16 dimensions; released 12/2023):**  
  `['subject_consistency','background_consistency','temporal_flickering','motion_smoothness','dynamic_degree','aesthetic_quality','imaging_quality','object_class','multiple_objects','human_action','color','spatial_relationship','scene','temporal_style','appearance_style','overall_consistency']`
- **Design rationale:** enforce **standard prompt lists** for fair model comparison via `vbench/VBench_full_info.json`; warns when required videos missing. Supports **custom videos** when `--mode=custom_input` (no filename requirements).
- **Custom-input supported dimensions (subset):**  
  `subject_consistency, background_consistency, motion_smoothness, dynamic_degree, aesthetic_quality, imaging_quality`
- **Core workflow (CLI):**
  - Install: `pip install vbench` (+ PyTorch; Detectron2 needed for some dimensions; Detectron2 works with CUDA 12.1 or 11.x).  
  - Evaluate: `vbench evaluate --videos_path $VIDEO_PATH --dimension $DIMENSION`  
  - Custom videos: `vbench evaluate --dimension $DIMENSION --videos_path ... --mode=custom_input`  
  - Multi-GPU: `vbench evaluate --ngpus=${GPUS} ...` or `torchrun --nproc_per_node=${GPUS} --standalone evaluate.py ...`
- **Temporal flicker preprocessing:** run `static_filter.py --videos_path $VIDEOS_PATH` before `temporal_flickering` (options: `--filter_scope all` or JSON prompt list).
- **Aggregate scoring formulas (Leaderboard scripts):**
  - **Normalization (Eq. 1):** `norm = (dim_score - min_val) / (max_val - min_val)`  
  - **Quality Score:** weighted avg of `{subject, background, temporal_flickering, motion_smoothness, aesthetic_quality, imaging_quality, dynamic_degree}`  
  - **Semantic Score:** weighted avg of `{object_class, multiple_objects, human_action, color, spatial_relationship, scene, appearance_style, temporal_style, overall_consistency}`  
  - **Total Score (Eq. 2):** `Total = w1*Quality + w2*Semantic`  
  - `min/max` and weights in `scripts/constant.py`; compute via `scripts/cal_final_score.py --zip_file ... --model_name ...`

</details>

### 📊 VBench++ (VBench) — Multi-dimensional, human-aligned evaluation for video generation
**Benchmark** · [source](https://arxiv.org/html/2411.13503)

*Standardized benchmark protocol + leaderboard-style per-dimension scoring for T2V/I2V models, with metric definitions and human-preference alignment.*

<details>
<summary>Key content</summary>

- **Design rationale (Section 3.1):** Single-number metrics (e.g., FVD/IS/FID/CLIPSIM) can hide strengths/weaknesses and misalign with human judgment; VBench decomposes “video generation quality” into **16 disentangled dimensions** for fine-grained diagnosis.
- **Top-level hierarchy:**  
  - **Video Quality** (“video alone looks good”) → **Temporal Quality** + **Frame-wise Quality**  
  - **Video-Condition Consistency** (“matches user condition”) → **Semantics** + **Style** (+ overall consistency)
- **Temporal Quality dimensions + methods (Section 3.1.1):**
  - **Subject Consistency:** DINO feature similarity across frames.  
  - **Background Consistency:** CLIP feature similarity across frames.  
  - **Temporal Flickering:** mean absolute difference across (static) frames.  
  - **Motion Smoothness:** motion priors from a video frame interpolation model.  
  - **Dynamic Degree:** RAFT optical flow magnitude as motion/dynamics estimate.
- **Frame-wise Quality (Section 3.1.1):**
  - **Aesthetic Quality:** LAION aesthetic predictor.  
  - **Imaging Quality:** MUSIQ predictor (trained on SPAQ).
- **T2V condition-consistency (Section 3.1.2):**
  - **Object Class / Multiple Objects / Color:** GRiT detection + color captioning.  
  - **Human Action:** UMT action recognition (actions drawn from **Kinetics-400**; **100** representative actions).  
  - **Spatial Relationship:** rule-based evaluation over **4** relationship types.  
  - **Scene:** Tag2Text scene captioning match.  
  - **Style:** Appearance style via CLIP similarity; Temporal style + Overall video-text via **ViCLIP** similarity.
- **Prompt suite defaults (Section 3.2.1):** ~**100 prompts per dimension**; plus **8 categories** × **100 prompts each** = **800** (Animal, Architecture, Food, Human, Lifestyle, Plant, Scenery, Vehicles).
- **Human preference protocol (Section 3.4.1):** For each prompt: **4 models** generate videos → **5 groups** sampled; within each group, **6 pairwise comparisons** (all pairs), randomized order; annotators judge **only the target dimension**.
- **I2V additions (Section 3.1.3 & 3.3):** Image Suite with **adaptive aspect ratio**; evaluate at each model’s **default resolution/aspect** (examples: **SVD 1024×576**, **ConsistI2V 256×256**). I2V consistency uses DINOv1 (subject), DreamSim (background), and camera motion classification over **7** types (pan/tilt/zoom/static) using Co-Tracker edge-point tracking + heuristics.
- **Trustworthiness (Section 3.1.4 & 3.2.2):**
  - **Culture Fairness:** **9** culture classes × **14** scenarios = **126 prompts**, scored via ViCLIP.  
  - **Human Bias prompts:** **90 prompts** (6 aspects × 15). Bias quantified as distance to uniform distribution (gender: L1; skin tone: L2 after merging 6 Fitzpatrick tones → 3 classes).  
  - **Safety:** NudeNet + SD Safety Checker + Q16; **frame unsafe if any flags**; **video unsafe if >50% frames unsafe**; safety prompt suite: **90 prompts** across **7** harm classes.

</details>

### 📖 OpenAI API Model Catalog (selection + limits)
**Reference Doc** · [source](https://platform.openai.com/docs/models)

*Model availability/capability matrix + documented limits (context/output), tool compatibility, and pricing pointers.*

<details>
<summary>Key content</summary>

- **Default model choice guidance (Choosing a model):**
  - Start with **`gpt-5.4`** for **complex reasoning and coding**.
  - For **lower latency/cost**, choose **`gpt-5.4-mini`** or **`gpt-5.4-nano`**.
- **Common capability baseline (latest OpenAI models):**
  - Support **text + image input**, **text output**, **multilingual**, and **vision**.
  - Available via the **Responses API** and **Client SDKs**.
- **Frontier model rows (key empirical numbers):**
  - **`gpt-5.4`**
    - Pricing: **$2.50 / input MTok**, **$15 / output MTok**
    - **Context window:** **1M tokens**
    - **Max output:** **128K tokens**
    - Tools: **Functions, Web search, File search, Computer use**
    - Knowledge cutoff: **Aug 31, 2025**
    - Latency: **Fast**
  - **`gpt-5.4-mini`**
    - Pricing: **$0.75 / input MTok**, **$4.50 / output MTok**
    - **Context window:** **400K tokens**
    - **Max output:** **128K tokens**
    - Tools: **Functions, Web search, File search, Computer use**
    - Knowledge cutoff: **Aug 31, 2025**
    - Latency: **Faster**
  - **`gpt-5.4-nano`**
    - Pricing: **$0.20 / input MTok**, **$1.25 / output MTok**
    - **Context window:** **400K tokens**
    - **Max output:** **128K tokens**
    - Tools: **Functions, Web search, File search, MCP**
    - Knowledge cutoff: **Aug 31, 2025**
    - Latency: **Faster**
- **Specialized model categories listed:** **Image**, **Realtime (speech-to-speech)**, **Speech generation (TTS)**, **Transcription (STT)**.

</details>

### 📖 Sora Videos API (create/poll/download, refs, edits, extensions)
**Reference Doc** · [source](https://platform.openai.com/docs/guides/video-generation)

*Concrete request/response schema + constraints for production text-to-video usage*

<details>
<summary>Key content</summary>

- **Deprecation:** Sora 2 video generation models + Videos API shut down **Sep 24, 2026** (affects **/videos**, models **sora-2**, **sora-2-pro**, **sora-2-2025-10-06**, **sora-2-2025-12-08**, **sora-2-pro-2025-10-06**).
- **Models & capabilities:**  
  - **sora-2** = faster iteration; **sora-2-pro** = higher fidelity, production quality; use pro for **1080p exports (1920×1080 or 1080×1920)**.  
  - Both support **16s and 20s** generations.
- **Core async workflow (Videos API):**
  1) **POST `/v1/videos`** → returns job object `{id, status, model, progress, seconds, size}` (status: **queued/in_progress/completed/failed**).  
  2) Poll **GET `/v1/videos/{video_id}`** (suggested **10–20s** interval; exponential backoff). Or use **webhooks**.  
  3) When **completed**, download MP4 via **GET `/v1/videos/{video_id}/content`**. Download URLs valid **≤ 1 hour**.
- **Webhooks:** event types **`video.completed`** and **`video.failed`**; payload includes `data.id` = video job id.
- **Supporting assets:** `/content?variant=thumbnail` (webp) or `variant=spritesheet` (jpg); default `variant=video`.
- **Image reference (first frame conditioning):** `input_reference` with **jpeg/png/webp**; must **match target `size`**. JSON form accepts `{file_id}` or `{image_url}`; multipart supports file upload.
- **Characters (consistency):** upload MP4 to **POST `/v1/videos/characters`**, then include `characters: [{id: "char_..."}]` and **mention character name verbatim in prompt**. Best: **2–4s**, **16:9 or 9:16**, **720p–1080p**; **max 2 characters**. **No characters in extensions.**
- **Extensions:** **POST `/v1/videos/extensions`** with source `{video:{id}}` + prompt; each adds **≤20s**; extend **≤6 times** → **max total 120s**; **no characters/image refs**.
- **Edits:** **POST `/v1/videos/edits`** with `{video:{id}}` (model inferred) + prompt; if uploading video, set `model` explicitly. Remix endpoint deprecated.
- **Batch:** supports **POST `/v1/videos` only**, **JSON only** (no multipart); upload assets first; batch outputs downloadable **≤24h**.
- **Library mgmt:** **GET `/v1/videos`** supports `limit`, `after`, `order`; **DELETE `/v1/videos/{video_id}`**.
- **Guardrails:** only **<18-suitable** content; **copyrighted characters/music rejected**; **no real people/public figures**; human-likeness character uploads blocked by default; **input images with human faces rejected**.

</details>

### 📖 Whisper Audio Transcription — Create Endpoint
**Reference Doc** · [source](https://platform.openai.com/docs/api-reference/whisper/create)

*Whisper transcription endpoint parameters and defaults (model, response_format, temperature, language, timestamp granularities) + request/response schema.*

<details>
<summary>Key content</summary>

- **Endpoint (Audio → Text):** Create a transcription by uploading an audio file and selecting a Whisper model.
- **Core request fields (multipart form):**
  - `file` (required): audio file upload.
  - `model` (required): Whisper model identifier to use for transcription.
- **Optional request parameters (common controls):**
  - `language`: ISO language code to bias/force transcription language (improves accuracy/latency when known).
  - `prompt`: text prompt to guide style/terminology (useful for names, jargon).
  - `response_format`: output format selector (e.g., plain text vs structured JSON variants).
  - `temperature`: sampling temperature for decoding; lower = more deterministic, higher = more varied.
  - `timestamp_granularities`: controls whether timestamps are returned and at what granularity (e.g., segment- and/or word-level timestamps) when using structured formats.
- **Response schema (varies by `response_format`):**
  - Text formats return the transcript as text.
  - JSON formats return structured objects (e.g., transcript text plus timing/segment metadata when timestamps enabled).
- **Procedure/workflow:**
  1. Send multipart request with `file` + `model`.
  2. Optionally set `language`, `prompt`, `temperature`, `response_format`.
  3. If you need timings, choose a structured `response_format` and set `timestamp_granularities`.
  4. Parse response according to chosen format (text vs JSON with segments/words).

</details>

---

## Related Topics

- [[topics/diffusion-models|Diffusion Models]]
- [[topics/multimodal-fundamentals|Multimodal Fundamentals]]
- [[topics/vision-language-models|Vision Language Models]]
- [[topics/video-understanding|Video Understanding]]
- [[topics/image-generation|Image Generation & Editing]]
