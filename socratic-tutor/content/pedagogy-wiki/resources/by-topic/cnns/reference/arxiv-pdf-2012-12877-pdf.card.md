# Card: DeiT/ViT tokenization + distillation token (DeiT)
**Source:** https://arxiv.org/pdf/2012.12877.pdf  
**Role:** paper | **Need:** CONCEPT_EXPLAINER  
**Anchor:** Practical ViT token pipeline (patch→tokens + class token + positional embeddings) and DeiT’s distillation token + key training/accuracy impacts.

## Key Content
- **Self-attention (Eq. 1):**  
  \[
  \text{Attention}(Q,K,V)=\text{Softmax}(QK^\top/\sqrt{d})V
  \]
  with queries \(Q\in\mathbb{R}^{N\times d}\), keys/values \(K,V\in\mathbb{R}^{k\times d}\) (self-attn uses \(k=N\)). \(Q=XW^Q, K=XW^K, V=XW^V\) for token matrix \(X\in\mathbb{R}^{N\times D}\).
- **ViT tokenization (Section 3):** image split into \(N\) patches of size \(16\times16\) (for 224px: \(N=14\times14\)). Each patch (dim \(3\cdot16\cdot16=768\)) is linearly projected to embedding dim \(D\). **Positional embeddings** (fixed or trainable) are **added before** transformer blocks.
- **Class token (Section 3):** trainable vector appended → sequence length \(N+1\). Only class token is used for classification head; forces attention to route patch info into class token.
- **Resolution change:** keep patch size fixed ⇒ \(N\) changes; **interpolate positional embeddings** when fine-tuning at higher resolution (ViT approach). DeiT uses **bicubic** interpolation to better preserve embedding norms (bilinear reduced norms harmed accuracy without fine-tuning).
- **Distillation losses:**  
  **Soft KD (Eq. 2):**  
  \(L=(1-\lambda)L_{CE}(\psi(Z_s),y)+\lambda\tau^2 KL(\psi(Z_s/\tau),\psi(Z_t/\tau))\). Defaults: \(\tau=3.0,\lambda=0.1\).  
  **Hard KD (Eq. 3):** \(y_t=\arg\max_c Z_t(c)\),  
  \(L=\tfrac12 CE(\psi(Z_s),y)+\tfrac12 CE(\psi(Z_s),y_t)\).
- **Distillation token (Section 4):** add a **new token** alongside class+patch tokens; its head predicts teacher label (hard). At test time: use class head, distill head, or **late-fuse** by summing softmax outputs.
- **Empirical (Table 3, ImageNet):** DeiT-B 224: **81.8%**; usual soft distill: **81.8%**; hard distill: **83.0%**; DeiT-B⚗ class: **83.0%**, distill: **83.1%**, class+distill fusion: **83.4%**. At 384: DeiT-B **83.1%** vs DeiT-B⚗ fusion **84.5%**.
- **Teacher choice (Table 2):** convnet teachers (RegNetY-16GF teacher acc **82.9%**) yield better student; DeiT-B⚗ at 384 reaches **84.2%** with RegNetY-16GF teacher.

## When to surface
Use when students ask how ViT turns images into tokens (patch embeddings, class token, positional embeddings, resolution changes) or how DeiT’s **distillation token** and **hard distillation** improve training/accuracy on ImageNet.