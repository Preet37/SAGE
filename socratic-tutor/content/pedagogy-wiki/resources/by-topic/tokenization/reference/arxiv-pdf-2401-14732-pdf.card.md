# Card: Residual Vector Quantization (RQ) & QINCo objectives
**Source:** https://arxiv.org/pdf/2401.14732.pdf  
**Role:** paper | **Need:** FORMULA_SOURCE  
**Anchor:** Clear RQ/RVQ recursion + training objectives (Eqs. 2–3) and “implicit neural codebooks” conditioning on partial reconstruction.

## Key Content
- **Conventional Residual Quantization (RQ) recursion (Sec. 3):**  
  Quantize vectors \(x\in\mathbb{R}^d\) over \(M\) steps with codebooks \(C_m\in\mathbb{R}^{d\times K}\) (columns are centroids \(c_{m,k}\)).  
  Initialize reconstruction \(\hat x_0=0\). Residual at step \(m\): \(r_m = x-\hat x_{m-1}\).  
  Encode by nearest centroid: \(k_m=\arg\min_k \|r_m - c_{m,k}\|^2\), choose \(q_m=c_{m,k_m}\).  
  Decode/add: \(\hat x_m=\hat x_{m-1}+q_m\). Final \(\hat x=\hat x_M\). Indices \((k_1,\dots,k_M)\) stored (bits \(\approx M\log_2 K\)).
- **QINCo: implicit neural codebooks (Sec. 3.1):** fixed per-step codebook is suboptimal because residual distribution depends on previous choices. QINCo generates a *specialized* codebook per step conditioned on partial reconstruction:  
  \(C_m(\hat x_{m-1}) = f_{\theta_m}(\hat x_{m-1},\, C_m^{\text{base}})\) (residual-style MLP blocks; base codebooks initialized from pretrained RQ; base codebooks also trainable).
- **Training objective (Sec. 3.2):** per-step “elementary” loss (Eq. 2) is MSE between residual and selected centroid; total loss sums across steps (Eq. 3):  
  \(L=\sum_{m=1}^M \|r_m - q_m\|^2\). Gradients from later steps backprop to earlier steps because \(r_m,\ q_m\) depend on \(\theta\).
- **Sequential decoding in QINCo (Sec. 3.2):** must reconstruct step-by-step since codebook generation needs \(\hat x_{m-1}\).
- **Empirical compression/search (Tab. 1):** BigANN1M R@1: **QINCo 45.2** vs RQ 27.9 (8 bytes); **QINCo 71.9** vs RQ 49.0 (16 bytes). Deep1M R@1: **36.3** vs 21.4 (8B); **59.8** vs 43.0 (16B). MSE also substantially lower (e.g., BigANN1M 8B: **1.12** vs 2.49).
- **Defaults noted:** common setting \(K=256\) (8 bits/step); “8 bytes” \(\Rightarrow M=8\), “16 bytes” \(\Rightarrow M=16\). QINCo trained with Adam, effective batch size 1024, LR decay ×10 on val plateau (10 epochs), early stop after 50 epochs no improvement (App. A.3).

## When to surface
Use when students ask for the **RVQ/RQ mathematical objective**, residual recursion, or how **neural RVQ variants** (e.g., EnCodec-style RVQ) relate to a formal MSE residual-quantization loss and stepwise reconstruction.