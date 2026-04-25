# Card: LXMERT cross-attention + multimodal pretraining objectives
**Source:** https://aclanthology.org/D19-1514.pdf  
**Role:** paper | **Need:** FORMULA_SOURCE  
**Anchor:** Cross-modality encoder cross-attention equations + explicit pretraining objectives

## Key Content
- **Inputs/embeddings (Sec. 2.1, Eq. 1):**
  - Words: \(\hat w_i=\text{WordEmbed}(w_i)\), \(\hat u_i=\text{IdxEmbed}(i)\), \(h_i=\text{LayerNorm}(\hat w_i+\hat u_i)\).
  - Objects: each object \(o_j\) has RoI feature \(f_j\in\mathbb{R}^{2048}\) and box coords \(p_j\).  
    \(\hat f_j=\text{LayerNorm}(W_F f_j+b_F)\), \(\hat p_j=\text{LayerNorm}(W_P p_j+b_P)\),  
    \(v_j=(\hat f_j+\hat p_j)/2\). (Eq. 1; position needed for masked object prediction.)
- **Attention definition (Sec. 2.2):** for query \(x\), contexts \(\{y_j\}\):  
  \(a_j=\text{score}(x,y_j)\), \(\alpha_j=\exp(a_j)/\sum_k\exp(a_k)\), output \(=\sum_j \alpha_j y_j\). Uses **multi-head attention** (Transformer).
- **Cross-modality encoder (Sec. 2.2):** per layer \(k\), bidirectional cross-attn then self-attn:
  - \(\hat h_i^k=\text{CrossAtt}_{L\to R}(h_i^{k-1},\{v_1^{k-1}\dots v_m^{k-1}\})\)  
    \(\hat v_j^k=\text{CrossAtt}_{R\to L}(v_j^{k-1},\{h_1^{k-1}\dots h_n^{k-1}\})\)
  - \(\tilde h_i^k=\text{SelfAtt}_{L\to L}(\hat h_i^k,\{\hat h_1^k\dots \hat h_n^k\})\),  
    \(\tilde v_j^k=\text{SelfAtt}_{R\to R}(\hat v_j^k,\{\hat v_1^k\dots \hat v_m^k\})\)  
  - Residual + LayerNorm after each sub-layer; [CLS] token’s final language vector is cross-modal output (Sec. 2.3).
- **Pretraining tasks (Sec. 3.1; mask prob 0.15):**
  1) Masked cross-modality LM (predict masked words using text + vision).  
  2) Masked object prediction: (a) RoI-feature regression (L2 on \(f_j\)); (b) detected-label classification (cross-entropy on Faster R-CNN labels).  
  3) Cross-modality matching: replace sentence w.p. 0.5; classify match vs mismatch.  
  4) Image QA: predict answer (9500-way answer table) when image-question matched.
- **Data/compute defaults (Sec. 3.2–3.3):** 9.18M image-sentence pairs, 180K images; ~100M words, 6.5M objects. Keep **36 objects/image** (avoid padding). Layers: \(N_L=9\), \(N_X=5\), \(N_R=5\); hidden size 768. Pretrain 20 epochs (~670K steps), batch 256, Adam, peak LR \(1e{-4}\), linear decay; QA loss only last 10 epochs; equal-weight sum of losses. Fine-tune 4 epochs, batch 32, LR \(1e{-5}\) or \(5e{-5}\).
- **Key results (Table 2):** LXMERT test: VQA Acc 72.5 (Binary 88.2 / Number 54.2 / Other 63.1); GQA Acc 60.3 (Binary 77.8 / Open 45.0); NLVR2 Acc 76.2, Consistency 42.1 (prior SotA 53.5 / 12.0).
- **Ablations (Tables 4–5):** adding QA pretrain improves NLVR2 72.4→74.9; vision tasks matter: no-vision-tasks gives NLVR2 50.9 vs feat+label 74.9.

## When to surface
Use when students ask how **cross-attention fuses vision+language** in LXMERT-style models, or what **multimodal pretraining objectives and hyperparameters** are used (MLM, masked objects, matching, QA) and their measured impact.