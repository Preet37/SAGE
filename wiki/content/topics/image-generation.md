---
title: "Image Generation & Editing"
subject: "Generative Models"
date: 2026-04-09
tags:
  - "subject/generative-models"
  - "level/intermediate"
  - "level/advanced"
  - "resource/video"
  - "resource/blog"
  - "resource/deep-dive"
  - "resource/paper"
  - "resource/code"
educators:
  []
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

# Image Generation

## Video (best)
- **Two Minute Papers** — "DALL·E 2 Explained!"
- **Watch:** [YouTube](https://www.youtube.com/watch?v=qTgPSKKjfVg)
- Why: Clear, accessible overview of modern text-to-image diffusion-style generation and what “prompted image synthesis” is doing at a high level.
- Level: Beginner → Intermediate

## Blog / Written explainer (best)
- **Lil’Log (Lilian Weng)** — "What are Diffusion Models?"
- Why: One of the clearest written explanations of diffusion models (the backbone of many text-to-image systems), with intuition + math + references.
- Level: Intermediate

## Deep dive
- **Hugging Face (Documentation / Course-style guides)** — "Diffusion models" (Stable Diffusion & related concepts)
- Why: Practical, implementation-oriented deep dive into diffusion pipelines (text-to-image, img2img, inpainting/outpainting) and common components.
- Level: Intermediate → Advanced  
- **Link:** [https://huggingface.co/docs/diffusers/index](https://huggingface.co/docs/diffusers/index)
## Original paper
- **Ho, Jain, Abbeel (2020)** — "Denoising Diffusion Probabilistic Models"
- Why: Foundational diffusion model paper that underpins many modern image generation systems.
- Level: Advanced  
- **Link:** [https://arxiv.org/abs/2006.11239](https://arxiv.org/abs/2006.11239)
## Code walkthrough
- **Hugging Face Diffusers** — Example scripts / pipelines (text-to-image, img2img, inpainting)
- Why: Widely used reference implementation; easy to map concepts (scheduler, UNet, VAE, conditioning) to working code.
- Level: Intermediate  
- **Link:** [https://github.com/huggingface/diffusers](https://github.com/huggingface/diffusers)
## Coverage notes
- Strong: diffusion fundamentals; text-to-image basics; practical pipelines (text-to-image, img2img, inpainting) via Diffusers; foundational DDPM paper.
- Weak: model-specific coverage for **DALL·E 3**, **Midjourney**, **Imagen**, **FLUX** (often proprietary and not fully documented publicly); **IP-Adapter** specifics; **aesthetic scoring** as a control signal.
- Gap: a single, authoritative educator resource that compares major proprietary systems (DALL·E 3 vs Midjourney vs Imagen vs FLUX) with reproducible technical detail; a best-in-class walkthrough focused specifically on **IP-Adapter** and modern conditioning/control stacks.

---

## Additional Resources for Tutor Depth

> **9 sources** — papers, official docs, working code, benchmarks, and deep explainers that give the AI tutor precision on this topic.

### 📄 IP-Adapter (Decoupled Cross-Attention for Image Prompts in Diffusion)
**Paper** · [source](http://arxiv.org/pdf/2308.06721.pdf)

*Exact IP-Adapter formulation: CLIP image embedding projection + cross-attention injection into U-Net; training objective and insertion details.*

<details>
<summary>Key content</summary>

- **Diffusion training objective (noise prediction)** (Eq. 1):  
  \(L_{\text{simple}}=\mathbb{E}_{x_0,\epsilon\sim\mathcal{N}(0,I),c,t}\|\epsilon-\epsilon_\theta(x_t,c,t)\|_2^2\),  
  where \(x_t=\alpha_t x_0+\sigma_t\epsilon\), \(t\in[0,T]\), \(c\)=condition.
- **Classifier-free guidance** (Eq. 2):  
  \(\hat\epsilon_\theta(x_t,c,t)=w\,\epsilon_\theta(x_t,c,t)+(1-w)\,\epsilon_\theta(x_t,t)\).
- **Baseline SD cross-attention** (Eq. 3):  
  \(Z'=\text{Attn}(Q,K,V)=\text{Softmax}(QK^\top/\sqrt d)\,V\),  
  \(Q=ZW_q,\;K=c_tW_k,\;V=c_tW_v\). \(Z\)=U-Net query features; \(c_t\)=text features.
- **IP-Adapter image encoder/projection** (Sec. 3.2.1): frozen CLIP image encoder global embedding → trainable projection (Linear + LayerNorm) → sequence \(c_i\) of length \(N=4\), same dim as text tokens.
- **Decoupled cross-attention injection** (Eqs. 4–5): add per U-Net cross-attn layer a *new* image cross-attn:  
  \(Z''=\text{Softmax}(Q(K')^\top/\sqrt d)\,V'\), \(K'=c_iW'_k,\;V'=c_iW'_v\).  
  Final: \(Z_{\text{new}}=\text{Attn}(Q,K,V)+\text{Attn}(Q,K',V')\).  
  **Trainable only:** \(W'_k,W'_v\) (initialize from \(W_k,W_v\)); U-Net frozen; same \(Q\) as text.
- **Training objective with both conditions** (Eq. 6):  
  \(L_{\text{simple}}=\mathbb{E}_{x_0,\epsilon,c_t,c_i,t}\|\epsilon-\epsilon_\theta(x_t,c_t,c_i,t)\|_2^2\).
- **Dropping image condition for CFG** (Eq. 7): zero out CLIP image embedding when dropped.
- **Inference control of image strength** (Eq. 8):  
  \(Z_{\text{new}}=\text{Attn}(Q,K,V)+\lambda\,\text{Attn}(Q,K',V')\); \(\lambda=0\) recovers original text-only model.
- **Defaults / hyperparams (Sec. 4.1.2):** SD v1.5 base; OpenCLIP ViT-H/14 image encoder; 16 cross-attn layers → add 16 image cross-attn layers; total trainable params ≈ **22M**. Train: 8×V100, **1M steps**, batch **8/GPU**, AdamW lr **1e-4**, wd **0.01**; images resized shortest side to 512 then center-crop 512². Drop probs: 0.05 text, 0.05 image, 0.05 both. Inference: DDIM 50 steps, guidance scale **7.5**; image-only uses empty text + \(\lambda=1.0\).
- **Key quantitative result (Table 1, COCO val):** IP-Adapter (**22M**) achieves **CLIP-T 0.588**, **CLIP-I 0.828**; better than Uni-ControlNet Global (47M: 0.506/0.736) and T2I-Adapter Style (39M: 0.485/0.648); comparable to SD unCLIP (870M: 0.584/0.810).

</details>

### 📄 ImageReward & ReFL (human preference reward for text-to-image)
**Paper** · [source](https://arxiv.org/abs/2304.05977)

*ImageReward training pipeline + preference objective; reported human-alignment metrics; using reward as reranker and for diffusion fine-tuning (ReFL)*

<details>
<summary>Key content</summary>

- **Human preference data pipeline (Sec. 2.1, App. A):**
  - Prompts from **DiffusionDB**; diversity via **graph-based selection** using **Sentence-BERT** embeddings; select **10,000** candidate prompts → **177,304** candidate image pairs (4–9 images/prompt).
  - 3-stage expert annotation: **Prompt Annotation** (category + problematic prompt flags), **Text-Image Rating** (7-point Likert for **alignment**, **fidelity**, **overall** + harmlessness/problem checkboxes), then **Image Ranking** (best→worst; limited ties).
  - After ~2 months: **8,878** valid prompts, **136,892** comparison pairs (also stated as **137k expert comparisons** total).
- **Reward model objective (Eq. 1, Sec. 2.2):** pairwise ranking loss  
  \[
  \mathcal{L} = -\log \sigma\big(r_\theta(p, y_w) - r_\theta(p, y_l)\big)
  \]
  where \(p\)=prompt, \(y_w\)=preferred image, \(y_l\)=less-preferred image, \(r_\theta(\cdot)\)=scalar reward, \(\sigma\)=sigmoid.
- **Model design choices (Sec. 2.2/4.1):** **BLIP** backbone (cross-attention fusion + MLP scalar head) chosen over CLIP; mitigate overfitting by **freezing ~70% transformer layers**.
  - Best setting reported: freeze **70%** layers, **lr=1e-5**, **batch=64**; trained on **4×A100 40GB** (per-GPU batch 16).
- **Preference prediction results (Sec. 4.1, Table 3):**
  - **Preference accuracy:** ImageReward **65.14%** vs CLIP score **54.82%**, Aesthetic **57.35%**, BLIP score **57.76%**.
  - **Recall@1/@2/@4:** ImageReward **39.62 / 63.07 / 90.84** (CLIP: **27.22 / 48.52 / 78.17**).
- **Metric alignment across models (Sec. 2.3, Table 1):** Spearman correlation to human eval: **ImageReward 1.00**, **CLIP 0.60**, **zero-shot FID 0.09**.
- **ReFL diffusion tuning (Sec. 3, Eq. 2–3):** direct fine-tune diffusion by backprop through reward at a **random late denoising step** (stability vs last-step-only). Final loss combines **reward loss + reweighted term + pretraining regularization**.
  - ReFL insight: reward becomes distinguishable after ~**>30/40** denoising steps; use late-step feedback.
  - ReFL training (Sec. 4.2): SD v1.4 baseline; **lr=1e-5**, total **batch=128**; **8×A100 40GB**; inference uses **PNDM** scheduler, **CFG=7.5**.

</details>

### 📄 Imagen—T5 text encoder scaling + cascaded diffusion + dynamic thresholding
**Paper** · [source](https://papers.neurips.cc/paper_files/paper/2022/file/ec795aeadae0b7d230fa35cbaf04c041-Paper-Conference.pdf)

*Imagen design choice/rationale: frozen large text-only LM (T5) as encoder; scaling text encoder improves alignment/fidelity more than scaling diffusion U-Net; end-to-end cascade (64→256→1024) diffusion pipeline.*

<details>
<summary>Key content</summary>

- **Core finding (Abstract, Sec. 2.1, 4.4):** Large **frozen** text-only LMs (e.g., **T5-XXL, 4.6B params**) are “surprisingly effective” text encoders; **scaling text encoder size improves fidelity + image-text alignment more than scaling U-Net** (Fig. 4a vs 4b). Human raters prefer **T5-XXL over CLIP** on challenging prompts (DrawBench), even if COCO metrics are similar.
- **Pipeline (Intro, Sec. 2.4):** Frozen T5 encoder → **base 64×64 text-conditional diffusion** → **two text-conditional super-resolution diffusion models**: **64→256** then **256→1024**. Uses **classifier-free guidance** and **noise conditioning augmentation** in SR stages (aug_level ∈ **[0,1]**; Gaussian noise); during inference **sweep aug_level** for best quality.
- **Diffusion training objective (Eq. 1, Sec. 2.2):**  
  \[
  \mathbb{E}_{x,c,\epsilon,t}\big[w_t\|\hat x_\theta(\alpha_t x+\sigma_t\epsilon, c)-x\|_2^2\big]
  \]
  where \(t\sim U([0,1])\), \(\epsilon\sim\mathcal N(0,I)\), \(z_t=\alpha_t x+\sigma_t\epsilon\), \(c\)=conditioning (text).
- **Classifier-free guidance (Eq. 2):** drop conditioning during training with **10% probability**; sampling uses  
  \[
  \tilde\epsilon_\theta(z_t,c)=w\,\epsilon_\theta(z_t,c)+(1-w)\epsilon_\theta(z_t)
  \]
  \(w\)=guidance weight (>1 strengthens conditioning).
- **Dynamic thresholding (Sec. 2.3):** high guidance causes \(\hat x_t\) to exceed **[-1,1]**; dynamic thresholding sets \(s\)=percentile(|\(\hat x_t\)|); if \(s>1\), clip to **[-s,s]** then divide by \(s\). Improves photorealism/alignment at large \(w\) (Fig. 4c).
- **Key results (Tables 1–2):** **COCO zero-shot FID-30K = 7.27** (Imagen) vs **GLIDE 12.24**, **DALL·E 2 10.39**, **Make-A-Scene 7.55**. Human eval (COCO): alignment **91.4±0.44** vs original **91.9±0.42**; photorealism preference **39.5±0.75%** (no-people subset: **43.9±1.01%**).
- **Training defaults (Sec. 4.1):** base model **2B params**; SR models **600M** and **400M**; batch **2048**; **2.5M steps**; base guidance **1.35**, SR guidance **8.0**; 256 TPU-v4 (base), 128 TPU-v4 (SR). Data: ~**460M** internal + **LAION-400M**.

</details>

### 📄 Pick-a-Pic & PickScore (preference-based scoring for T2I)
**Paper** · [source](https://proceedings.neurips.cc/paper_files/paper/2023/file/73aacd8b3b05b4b503d58310b523553c-Paper-Conference.pdf)

*Pick-a-Pic dataset construction; PickScore model/objective; evidence PickScore correlates with human preferences better than baselines; guidance for evaluation/reranking.*

<details>
<summary>Key content</summary>

- **Dataset (Section 2):** Each example = *(prompt x, two generated images y1,y2, label: prefer y1 / prefer y2 / tie)*. Built via web app loop: user sees 2 images → picks preferred/tie → rejected image replaced → repeat until prompt changes (Fig. 2).  
  - Paper experiments use NSFW-filtered snapshot: **583,747 train**, **500 val**, **500 test**; **37,523 prompts**, **4,375 users** (train). Overall logged: **968,965 rankings**, **66,798 prompts**, **6,394 users**.
  - Images generated from **SD 2.1**, **Dreamlike Photoreal 2.0**, **SDXL variants**, varying **classifier-free guidance (CFG)**.
  - Split procedure: sample **1000 prompts** (unique users) → split into val/test prompts; **1 example per prompt** in val/test; train excludes those prompts.
- **PickScore model (Eq. 1, Section 3):** CLIP-style scorer  
  - \(s(x,y)=E_{txt}(x)\cdot E_{img}(y)\cdot T\) where \(T\) is learned scalar temperature.
- **Preference objective (Eqs. 2–3):** preference distribution \(p=[1,0]\) (y1 wins), \([0,1]\) (y2 wins), \([0.5,0.5]\) (tie).  
  - \(\hat p_i=\frac{\exp s(x,y_i)}{\sum_{j=1}^2 \exp s(x,y_j)}\)  
  - \(L_{pref}=\sum_{i=1}^2 p_i(\log p_i-\log \hat p_i)\) (KL). Batch loss weighted inversely by prompt frequency (reduce overfitting to frequent prompts). In-batch negatives tried; worse (**65.2** vs PickScore **70.5** accuracy).
- **Training defaults (Section 3):** finetune **CLIP-H** for **4000 steps**, **lr 3e-6**, **batch 128**, **warmup 500**, linear decay; best checkpoint by val accuracy every 100 steps; ~<1 hour on **8×A100**.
- **Preference prediction results (Table 1b):** Accuracy on test (tie-aware metric): **PickScore 70.5%**, **Human expert 68.0%**, **HPS 66.7%**, **ImageReward 61.1%**, **CLIP-H 60.8%**, **Aesthetics 56.8%**, **Random 56.8%**. Tie threshold \(t\): predict tie if \(|\hat p_1-\hat p_2|<t\) (selected on val).
- **Model evaluation (Section 5):**
  - On **MS-COCO** captions: Spearman correlation with human win-rates: **PickScore 0.917** vs **FID -0.900** (FID prompt-agnostic; CFG confound—higher CFG preferred by humans but worsens FID).
  - Using real user prefs (Pick-a-Pic test; **14k** prefs; **45 models**) Elo correlation with users: **PickScore 0.790±0.054**, **HPS 0.670±0.071**, **ImageReward 0.492±0.086**, **CLIP-H 0.313±0.075**.
- **Reranking (Section 6, Table 2):** Generate **100 images/prompt** (Dreamlike Photoreal 2.0, **CFG 7.5**, **5 seeds × 20 prompt templates**). Humans prefer PickScore-selected image vs: **Random seed+null template 71.4%**, **Random template 82.0%**, **Aesthetics 85.1%**, **CLIP-H 71.3%**.

</details>

### 📊 GenEval — object-focused T2I alignment benchmark & scoring
**Benchmark** · [source](https://proceedings.neurips.cc/paper_files/paper/2023/file/a3bf71c7c63f0c3bcb7ff67c67b1e7b1-Paper-Datasets_and_Benchmarks.pdf)

*GenEval protocol + binary correctness scoring for object/attribute/relation alignment; human-agreement validation; model comparison table.*

<details>
<summary>Key content</summary>

- **Tasks & prompt templates (Table 1; 553 prompts total; 4 images/prompt):**
  - Single object (80): “a photo of a/an [OBJECT]”
  - Two object (99): “a photo of a/an [OBJECT A] and a/an [OBJECT B]”
  - Counting (80): “a photo of [NUMBER] [OBJECT]s”, NUMBER ∈ {2,3,4}
  - Colors (94): “a photo of a/an [COLOR] [OBJECT]”
  - Position (100): “a photo of a/an [OBJECT A] [REL POS] a/an [OBJECT B]”, REL POS ∈ {above, below, left of, right of}
  - Attribute binding (100): “a photo of a/an [COLOR A] [OBJECT A] and a/an [COLOR B] [OBJECT B]”
  - Objects: 80 MS-COCO classes (some renamed); Colors: 11 basic terms but **exclude gray**; exclude “person” for color tasks.
- **Evaluation pipeline (Section 3.2):**
  - **Instance segmentation:** Mask2Former (MMDetection), default conf **0.3**; for **counting use 0.9** (reduces spurious low-conf boxes).
  - **Position rule (Appendix C.3):** centroids (xA,yA),(xB,yB) with min-offset threshold **c=0.1**:  
    - B right of A if **xB > xA + c(wA+wB)**; left if **xB < xA − c(wA+wB)**  
    - B below A if **yB > yA + c(hA+hB)**; above if **yB < yA − c(hA+hB)**  
    where w*, h* are bbox width/height.
  - **Color classification:** CLIP ViT-L/14 zero-shot over candidate colors using prompts “a photo of a [COLOR] [OBJECT]”; **crop to bbox + mask background to gray** improves agreement (Table 4).
- **Scoring (Section 3.2):** per-image **binary correctness** (“all prompt elements satisfied”); average per task; overall score = mean across 6 tasks; also outputs error breakdown (missing objects, wrong count/position/color).
- **Human agreement (Section 4):** 6,000 annotations / 1,200 images; GenEval **83%** vs inter-annotator **88%**; on unanimous subset GenEval **91%** (CLIPScore **87%**). GenEval beats threshold-tuned CLIPScore especially on counting (+22 pts agreement).
- **Benchmark results (Table 2, overall GenEval):** minDALL-E **0.23**, SDv1.5 **0.43**, SDv2.1 **0.50**, SD-XL **0.55**, IF-XL **0.61**. Hard tasks remain low: **position best 0.15 (SD-XL)** / **0.13 (IF-XL)**; **attribute binding best 0.35 (IF-XL)**.

</details>

### 📊 HEIM — Holistic Evaluation of Text-to-Image Models
**Benchmark** · [source](https://proceedings.neurips.cc/paper_files/paper/2023/file/dd83eada2c3c74db3c7fe1c087513756-Paper-Datasets_and_Benchmarks.pdf)

*Standardized benchmark suite (12 aspects, 62 scenarios, 25 metrics) + comparative results across 26 T2I models with human + automated eval.*

<details>
<summary>Key content</summary>

- **Framework components (Sec. 2, Fig. 4):** Each eval run = **Aspect** × **Scenario** × **Model+Adaptation** × **Metric**. Adaptation mainly **zero-shot prompting**; also prompt engineering (e.g., **Promptist**).
- **12 aspects (Table 1):** alignment, quality/photorealism, aesthetics, originality, reasoning, knowledge, bias, toxicity, fairness, robustness, multilinguality, efficiency.
- **Scenarios (Table 2):** 62 total incl. MS-COCO base + art-style variants; MS-COCO gender substitution & dialect (fairness); MS-COCO typos (robustness); MS-COCO translated to **Chinese/Hindi/Spanish** (multilinguality); I2P toxicity prompts; originality/aesthetics scenarios (Landing Pages, Logos, Magazine Covers, dailydall.e); reasoning (PaintSkills, Winoground, DrawBench counting/positional, etc.).
- **Metrics (Table 3):**
  - Human: **Overall alignment (1–5)**, **Photorealism (1–5)**, **Overall aesthetics (1–5)**, **Overall originality (1–5)**, **Subject clarity (yes/no/else)**.
  - Automated: CLIPScore; **FID**, Inception Score; LAION Aesthetics; **Fractal coefficient**; object detection accuracy (reasoning); watermark detector; LAION NSFW, NudeNet; blackout/rejection rates; gender/skin-tone bias; fairness/robustness/multilinguality = **performance change** under perturbations; efficiency = **raw** and **denoised inference time**.
- **Human eval procedure (Sec. 5):** crowdsourcing; **≥5 workers/image**; **≥100 image samples/aspect**.
- **Key empirical results (Sec. 7):**
  - **Photorealism ceiling:** real MS-COCO images rated **4.48/5**; **no model > 3/5**.
  - **Reasoning:** best model (DALL-E 2) **47.2%** object-detection accuracy on **PaintSkills**.
  - **Metric correlations:** human vs automated: alignment **0.42** (CLIPScore), quality **0.59** (FID), aesthetics **0.39** (LAION aesthetics).
  - **Toxicity:** some models generate inappropriate images for non-toxic prompts **>10%**; minDALL-E/DALL-E mini/GigaGAN **<1%**.
  - **Multilinguality:** DALL-E 2 alignment drops: Chinese **−0.536**, Spanish **−0.162**, Hindi **−2.640**.
  - **Efficiency:** vanilla Stable Diffusion denoised runtime **~2s**; autoregressive models **~2s slower** at similar parameter count.

</details>

### 📊 Human multi-task benchmark + human ratings for text-to-image
**Benchmark** · [source](https://arxiv.org/html/2211.12112)

*Human-study protocol + quantitative tables comparing Stable Diffusion vs DALL‑E 2 across tasks/difficulty*

<details>
<summary>Key content</summary>

- **Benchmark design (Table 2 / Methods):**
  - Proposes a **multi-task text-to-image benchmark** with **~32 tasks** (paper also references **50 tasks & applications**), each targeting a distinct capability (e.g., **counting**, **spatial positioning**, **quoted text spelling**, **negation**, **bias**, **editing without manual annotation**, **changing image dimensions**).
  - Each task has **3 difficulty levels** (**easy/medium/hard**) and **10 prompt instances per level** (i.e., **30 prompts per task**).
  - Example difficulty heuristic (Counting): **easy = 1–3 objects**, **medium = 4–10**, **hard = >10**.
- **Human evaluation protocol (Methods / Results):**
  - **20 AI graduate students** rated images on a **1–5 scale** (1 worst, 5 best).
  - Compared **Stable Diffusion (SD)** vs **DALL‑E 2**, using **identical default model parameters**.
  - Total ratings: **3,600** = 20 raters × 2 models × 3 tasks × 3 difficulty levels × 10 prompts.
  - Some generations may fail due to **content filters** (marked with an asterisk in figures).
- **Key empirical results (Table 1; normalized % of best possible score):**
  - **Counting:** SD **54.4%** vs DALL‑E 2 **65.7%** (easy: **74.8 vs 91.8**; medium: **52.2 vs 51.4**; hard: **36.1 vs 54.0**).
  - **Faces:** SD **70.2%** vs DALL‑E 2 **81.7%** (easy: **72.5 vs 93.5**; medium: **74.0 vs 74.3**; hard: **64.2 vs 77.2**).
  - **Shapes:** SD **57.6%** vs DALL‑E 2 **56.8%** (easy: **70.8 vs 67.1**; medium: **56.8 vs 46.0**; hard: **45.1 vs 57.3**).
  - Overall: DALL‑E 2 better on **6/9** sub-tasks; performance generally **degrades with difficulty**.

</details>

### 📖 DALL·E 3 — model-specific constraints, pricing, rate limits
**Reference Doc** · [source](https://platform.openai.com/docs/models/dall-e-3)

*Model-specific behavior/constraints for DALL·E 3 (supported endpoints, sizes, pricing, rate limits)*

<details>
<summary>Key content</summary>

- **What DALL·E 3 does:** Generates a **new image from a text prompt**; “currently supports… create a new image with a specific size.”
- **Modalities / capabilities**
  - **Input:** Text only  
  - **Output:** Image only  
  - **Not supported:** Audio, Video
- **Endpoints listed for image workflows**
  - **Image generation:** `v1/images/generations`
  - **Image edit:** `v1/images/edits`
- **Supported output sizes (and used for pricing tiers)**
  - `1024x1024`
  - `1024x1536`
  - `1536x1024`
- **Pricing (per image)**
  - **Standard quality**
    - `1024x1024`: **$0.04**
    - `1024x1536`: **$0.08**
    - `1536x1024`: **$0.08**
  - **HD quality**
    - `1024x1024`: **$0.08**
    - `1024x1536`: **$0.12**
    - `1536x1024`: **$0.12**
  - **Quick comparison (Standard, 1024x1024):** DALL·E 3 **$0.04** vs DALL·E 2 **$0.02**
- **Rate limits (images per minute, RPM)**
  - Free: **Not supported**
  - Tier 1: **500 img/min**
  - Tier 2: **2500 img/min**
  - Tier 3: **5000 img/min**
  - Tier 4: **7500 img/min**
  - Tier 5: **10000 img/min**
- **Model naming / snapshots:** Alias/snapshot shown as `dall-e-3` (marked “Deprecated” in the listing).

</details>

### 📖 Images API (Generate/Edit/Variations) — DALL·E 3 parameter constraints
**Reference Doc** · [source](https://platform.openai.com/docs/api-reference/images?lang=node.js)

*Images endpoints + request/response schema; DALL·E 3 constraints/defaults (sizes, quality, etc.)*

<details>
<summary>Key content</summary>

- **Endpoints (Images resource)**
  - **Generate an image:** `POST /v1/images/generations`
  - **Edit an image:** `POST /v1/images/edits`
  - **Create variation:** `POST /v1/images/variations`
  - Streaming event specs exist for generation/edit (see “Image generation streaming events”, “Image edit streaming events” in API reference nav).

- **Core request fields (Generate)**
  - `model`: image model identifier (e.g., DALL·E 3).
  - `prompt`: text prompt describing desired image.
  - `n`: number of images to generate (commonly `1` for DALL·E 3).
  - `size`: **allowed (DALL·E 3):** `1024x1024`, `1024x1792`, `1792x1024`.
  - `quality`: **default:** `"standard"`; **option:** `"hd"`.
  - `response_format`: typically `"url"` or `"b64_json"` (controls whether you receive hosted URLs or base64 payloads).
  - `user`: optional end-user identifier for tracking/abuse monitoring.

- **Edit workflow (inpainting/outpainting)**
  - Provide an `image` plus optional `mask` (mask indicates editable region), along with `prompt` and other generation params (e.g., `size`, `response_format`).

- **Response schema (common)**
  - Returns an object with a `data` array; each element contains either a `url` (if `response_format="url"`) or `b64_json` (if `response_format="b64_json"`).

</details>

---

## Related Topics

- [[topics/diffusion-models|Diffusion Models]]
- [[topics/text-to-video|Text-to-Video]]
- [[topics/contrastive-learning|Contrastive Learning]]
- [[topics/vision-language-models|Vision Language Models]]
