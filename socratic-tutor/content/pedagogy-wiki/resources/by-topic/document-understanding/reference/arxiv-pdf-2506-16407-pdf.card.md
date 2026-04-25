# Card: Robustness attacks for OCR-based VDU (BBox/Text/Pixel)
**Source:** https://arxiv.org/pdf/2506.16407.pdf  
**Role:** paper | **Need:** EMPIRICAL_DATA  
**Anchor:** Quantitative robustness/perturbation evaluation showing OCR/layout error propagation and degradation under realistic, budgeted noise

## Key Content
- **Unified threat model & budgets (Sec. 3.1):**
  - **Layout budget:** constrain perturbed box \(b'\) vs. original \(b\) by **IoU\((b,b') \ge \tau\)** (default **\(\tau=0.6\)**; ablations at 0.75, 0.9).
  - **Text budget:** **edit\_rate** = character replacement rate (no insert/delete; positions aligned). Default **0.1**.
  - **Pixel budget:** apply document-specific transforms from **RoDLA (12 augmentations)** (blur/noise/occlusion/shadow/contrast, etc.) after shifting pixels with the box.
- **BBox predictor enabling gradients (Sec. 3.2, Eq. 1):**
  - Train per-model predictor mapping token embeddings \(\rightarrow (x,y,w,h)\) using **SmoothL1 + GIoU loss** (Eq. 1).
  - Architecture: **2-layer MLP → 4-layer Transformer encoder → 2-layer MLP**.
- **PGD layout attack with mIoU-budget loss (Sec. 3.3):**
  - Iterative PGD updates on embeddings/boxes; **project back** to feasible set satisfying IoU budget; keep best of **10 candidates**.
- **Six attack scenarios (Sec. 3.5):**  
  S1 BBox; S2 BBox+Pixel; S3 S2+Augment; S4 Text; S5 BBox+Text; **S6 BBox+Pixel+Text**. Evaluate **word vs. line** granularity.
- **Defaults/training (Sec. 4.1):** finetune **100 epochs**, **AdamW**, **lr** (given), **batch 32**, **weight decay** (given), **NVIDIA L40S 48GB**.
- **Empirical results (IoU=0.6, 5 seeds):**
  - Max reported vulnerability: **up to 29.18% F1 drop** (LayoutLMv3, **S6 PGD**, Table 3).
  - **PGD > Random** in compound attacks (Table 3): e.g., LayoutLMv3 **S5** Random **16.55** vs PGD **22.78**; **S6** Random **28.91** vs PGD **29.18**.
  - **Line-level > word-level** (FUNSD, Table 4): biggest gap **S6** = **+21.37 pp (Random)**, **+13.44 pp (PGD)**.
  - **Tighter IoU reduces Random more than PGD** (Table 7, FUNSD S1 line): Random drop **7.94→2.94→0.54** (IoU 0.6/0.75/0.9) vs PGD **13.32→6.60→6.50**.
  - **Unicode diacritic text attacks stronger** than random edits (Table 8): FUNSD **16.75 vs 7.31**; CORD **22.35 vs 7.13**.
  - **Transferability (Table 5):** PGD crafted on LayoutLMv3 transfers; e.g., LayoutLMv2 FUNSD **S6 PGD 55.54% drop**; GeoLayoutLM FUNSD **S6 PGD 53.56%**; ERNIE-Layout drops **<7%** even under PGD.

## When to surface
Use when students ask how OCR/layout noise or adversarial perturbations affect document AI models, or how to design/measure robustness with **IoU-bounded bbox shifts**, text edits, and pixel corruptions with **quantitative F1-drop evidence**.