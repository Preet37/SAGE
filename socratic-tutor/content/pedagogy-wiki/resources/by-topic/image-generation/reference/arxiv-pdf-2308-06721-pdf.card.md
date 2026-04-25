# Card: IP-Adapter (Decoupled Cross-Attention for Image Prompts in Diffusion)
**Source:** http://arxiv.org/pdf/2308.06721.pdf  
**Role:** paper | **Need:** FORMULA_SOURCE  
**Anchor:** Exact IP-Adapter formulation: CLIP image embedding projection + cross-attention injection into U-Net; training objective and insertion details.

## Key Content
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

## When to surface
Use when students ask how IP-Adapter injects image prompts into Stable Diffusion mathematically/architecturally, how it’s trained (frozen U-Net + new K/V projections), or how \(\lambda\) and CFG control image-vs-text conditioning strength.