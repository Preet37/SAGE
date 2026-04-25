# Card: LayoutLMv3 unified MLM/MIM + Word-Patch Alignment
**Source:** https://arxiv.org/pdf/2204.08387v3.pdf  
**Role:** paper | **Need:** FORMULA_SOURCE  
**Anchor:** Objective definitions (MLM/MIM/WPA), architecture + training details, key benchmark numbers

## Key Content
- **Architecture (Sec. 2.1):** Single multimodal Transformer over concatenated sequences: text embeddings \(Y=y_{1:L}\) + image patch embeddings \(X=x_{1:M}\).  
  - **Text:** OCR provides tokens + 2D boxes; embeddings = word (init from RoBERTa) + 1D position + **2D layout** (x, y, w, h embedded separately; coords normalized by image size). Uses **segment-level** layout positions (words in a segment share same 2D box).  
  - **Image:** resize to \(3\times224\times224\); split into \(P\times P\) patches with \(P=16\) → \(M=196\); linear projection to hidden dim + learnable **1D** pos emb (no 2D pos gains reported).
- **Pretraining loss (Sec. 2.2):** \(L=L_{\text{MLM}}+L_{\text{MIM}}+L_{\text{WPA}}\).  
  - **MLM (Eq. 1):** mask **30%** text tokens via span masking (Poisson \(\lambda=3\));  
    \[
    L_{\text{MLM}}(\theta)=-\sum_{l=1}^{L'}\log p_\theta(y_l\mid X_{M'},Y_{L'})
    \]
    \(L'\)=#masked text positions; \(X_{M'},Y_{L'}\)=corrupted sequences.  
  - **MIM (Eq. 2):** mask ~**40%** image tokens blockwise; discrete targets from image tokenizer (dVAE-style; vocab **8192**);  
    \[
    L_{\text{MIM}}(\theta)=-\sum_{m=1}^{M'}\log p_\theta(x_m\mid X_{M'},Y_{L'})
    \]
  - **WPA (Eq. 3):** for each **unmasked** text token, predict if its corresponding image patch is masked (aligned=both unmasked); exclude masked text tokens; 2-layer MLP + BCE:  
    \[
    L_{\text{WPA}}(\theta)=-\sum_{\ell=1}^{L-L'}\log p_\theta(z_\ell\mid X_{M'},Y_{L'})
    \]
    \(z_\ell\in\{0,1\}\).
- **Pretraining setup (Sec. 3.2):** IIT-CDIP **11M** docs; Adam, batch **2048**, **500k** steps; wd \(1e{-2}\), \((\beta_1,\beta_2)=(0.9,0.98)\). LR: BASE \(1e{-4}\) warmup **4.8%**; LARGE \(5e{-5}\) warmup **10%**.
- **Model sizes (Sec. 3.1):** BASE 12L/12H, \(D=768\), FFN 3072; LARGE 24L/16H, \(D=1024\), FFN 4096; max text length \(L=512\).
- **Key results (Table 1):** LayoutLMv3 **BASE** (133M, patch/linear) FUNSD **90.29** F1; CORD **96.56** F1; RVL-CDIP **95.44%**; DocVQA **78.76** ANLS. LayoutLMv3 **LARGE** FUNSD **92.08**; CORD **97.46**; RVL-CDIP **95.93%**; DocVQA **83.37**.  
  - vs LayoutLMv2 BASE: FUNSD 82.76 → **90.29**; DocVQA 78.08 → **78.76** with simpler image embedding.
- **Ablation (Table 3/Fig. 4):** Linear patches + **MLM only** causes PubLayNet loss divergence; adding **MIM** enables convergence (PubLayNet mAP **94.38**), adding **WPA** improves further (mAP **94.43**).

## When to surface
Use when students ask for the exact **objective equations** for unified MLM/MIM and **alignment (WPA)**, or need concrete **hyperparameters/benchmark numbers** for LayoutLMv3’s training and performance.