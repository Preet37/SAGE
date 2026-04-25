# Card: ViLBERT two-stream co-attention + pretraining tasks
**Source:** https://proceedings.neurips.cc/paper_files/paper/2019/file/c74d97b01eae257e44aa9d5bade97baf-Paper.pdf  
**Role:** paper | **Need:** FORMULA_SOURCE  
**Anchor:** Two-stream co-attentional Transformer layer (cross-modal key/value exchange) + masked multimodal modeling & image-text alignment pretraining

## Key Content
- **Two-stream architecture (Sec. 2.2, Fig. 1):** separate visual stream over region features \(v_1,\dots,v_T\) and linguistic stream over tokens \(w_0,\dots,w_T\); interact via **Co-TRM** layers.
- **Co-attentional Transformer (Sec. 2.2, Fig. 2b):** like standard multi-head attention but **swap key/value across modalities**:  
  - Visual update uses \(Q_v\) from \(H_V\) and \(K_w,V_w\) from \(H_W\) → “vision attends to language”.  
  - Linguistic update uses \(Q_w\) from \(H_W\) and \(K_v,V_v\) from \(H_V\) → “language attends to vision”.  
  Residual + FFN as in Transformer encoder blocks.
- **Image representation (Sec. 2.2):** Faster R-CNN regions (10–36 boxes, confidence-thresholded). Add **5-d spatial encoding** \((x_1,y_1,x_2,y_2,\text{area frac})\) projected and summed with region feature. Special **IMG** token = mean-pooled region features + full-image spatial encoding.
- **Pretraining tasks (Sec. 2.2, Fig. 3):**
  - **Masked multimodal modeling:** mask ~15% of words + regions. Text masking as BERT; region features zeroed 90% / unchanged 10%. Predict **region semantic class distribution**; loss = **KL divergence** to detector’s class distribution. Word loss = cross-entropy over vocab.
  - **Multimodal alignment:** input \(\{\text{IMG}, v_{1:T}, \text{CLS}, w_{1:T}, \text{SEP}\}\). Use holistic reps \(h_{\text{IMG}}, h_{\text{CLS}}\); combine by **element-wise product** \(h_{\text{IMG}}\odot h_{\text{CLS}}\) → linear layer → aligned/not (binary CE). Negatives by random image or caption replacement.
- **Defaults/hyperparams (Sec. 3.1):** Conceptual Captions ~3.1M pairs used; batch 512 on 8 TitanX; 10 epochs; Adam LR \(1\mathrm{e}{-4}\) with warmup + linear decay; task losses equally weighted. Linguistic init: **BERT-BASE** (12 layers, 12 heads, hidden 768). Visual stream: hidden 1024, 8 heads.
- **Key transfer results (Table 1):** ViLBERT (pretrained) vs ViLBERT† (no pretrain):  
  - **VQA test-dev:** 70.55 vs 68.93  
  - **VCR Q→AR:** 54.04 vs 49.48  
  - **RefCOCO+ testA/testB:** 78.52/62.61 vs 75.97/58.44  
  - **Image retrieval R@1:** 58.20 vs 45.50  
  - **Zero-shot retrieval R@1:** 31.86 (no fine-tune)
- **Depth ablation (Table 2):** retrieval improves with depth; e.g., ZS R@1: 26.14 (2-layer) → 31.86 (6-layer) → 32.80 (8-layer).

## When to surface
Use when students ask how **cross-attention fusion** can be implemented as **two-stream co-attention**, or what concrete **multimodal pretraining objectives** (masking + alignment) and **numbers/hyperparameters** ViLBERT used.