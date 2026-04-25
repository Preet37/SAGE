# Card: HEIM — Holistic Evaluation of Text-to-Image Models
**Source:** https://proceedings.neurips.cc/paper_files/paper/2023/file/dd83eada2c3c74db3c7fe1c087513756-Paper-Datasets_and_Benchmarks.pdf  
**Role:** benchmark | **Need:** EMPIRICAL_DATA  
**Anchor:** Standardized benchmark suite (12 aspects, 62 scenarios, 25 metrics) + comparative results across 26 T2I models with human + automated eval.

## Key Content
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

## When to surface
Use when students ask how to **compare text-to-image models beyond a single metric** (alignment vs aesthetics vs safety), or why **human ratings** are needed vs CLIP/FID, or about **robustness/fairness/multilingual** evaluation setups and concrete benchmark numbers.