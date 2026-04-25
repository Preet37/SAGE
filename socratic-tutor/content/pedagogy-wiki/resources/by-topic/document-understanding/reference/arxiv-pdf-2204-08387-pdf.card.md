# Card: LayoutLMv3 unified MLM/MIM + Word-Patch Alignment
**Source:** https://arxiv.org/pdf/2204.08387.pdf  
**Role:** paper | **Need:** FORMULA_SOURCE  
**Anchor:** Exact pretraining objective formulations (MLM/MIM/WPA) + architecture choices enabling multimodal alignment

## Key Content
- **Architecture (Sec. 2.1):** Single multimodal Transformer over concatenated sequences: text embeddings \(Y=y_{1:L}\) and image patch embeddings \(X=x_{1:M}\).  
  - **Text embedding:** word embeddings (init from RoBERTa) + 1D position + **2D layout** embeddings from OCR bounding boxes; uses **segment-level** 2D positions (words in a segment share a box).  
  - **Image embedding:** resize to \(3\times224\times224\), split into \(P\times P\) patches with \(P=16\), so \(M=HW/P^2=196\); linear projection to hidden dim + learnable **1D** position (no 2D pos improvement reported).
- **Total pretraining loss (Sec. 2.2):**  
  \[
  \mathcal{L}=\mathcal{L}_{MLM}+\mathcal{L}_{MIM}+\mathcal{L}_{WPA}.
  \]
- **MLM (Eq. 1):** mask **30%** text tokens via **span masking** (Poisson \(\lambda=3\)).  
  \[
  \mathcal{L}_{MLM}(\theta)=-\sum_{\ell=1}^{L'}\log p_\theta(y_\ell\mid X_{M'},Y_{L'})
  \]
  where \(L'\)=# masked text positions; \(X_{M'},Y_{L'}\)=corrupted sequences.
- **MIM (Eq. 2):** mask ~**40%** image tokens with **blockwise masking**; targets are **discrete VAE tokens** (visual vocab size **8192**, tokenizer init from DiT).  
  \[
  \mathcal{L}_{MIM}(\theta)=-\sum_{m=1}^{M'}\log p_\theta(x_m\mid X_{M'},Y_{L'})
  \]
- **WPA (Eq. 3):** binary classify for each **unmasked** text token whether its aligned image patch is masked (“unaligned”) or not (“aligned”); exclude masked text tokens; 2-layer MLP + BCE:  
  \[
  \mathcal{L}_{WPA}(\theta)=-\sum_{\ell=1}^{L-L'}\log p_\theta(z_\ell\mid X_{M'},Y_{L'})
  \]
  \(z_\ell\in\{0,1\}\).
- **Key results (Table 1):** LayoutLMv3 **BASE** (133M, patch/linear) FUNSD **90.29 F1**, CORD **96.56 F1**, RVL-CDIP **95.44 Acc**, DocVQA **78.76 ANLS**; **LARGE** FUNSD **92.08**, CORD **97.46**, RVL-CDIP **95.93**, DocVQA **83.37**.  
- **Ablation (Table 3/Fig. 4):** linear patches + **MLM only** causes **PubLayNet loss divergence**; adding **MIM** enables convergence (mAP **94.38**), adding **WPA** improves further (mAP **94.43**).

## When to surface
Use when students ask for the *exact* LayoutLMv3 pretraining equations/objectives, masking ratios/strategies, or why unified discrete MIM + WPA is needed for stable multimodal/vision transfer.