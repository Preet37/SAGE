# Card: Flexible VLP via detachable parallel fusion (FOD)
**Source:** https://aclanthology.org/2023.findings-acl.316.pdf  
**Role:** benchmark | **Need:** EMPIRICAL_DATA  
**Anchor:** Ablation comparisons of fusion strategies (concatenation/cascading/parallel) + benchmark results on retrieval & VL understanding

## Key Content
- **Architecture (Section 3, Eq. 4–5):** Dual-encoder (ViT image encoder + BERT-like text encoder) with **detachable cross-modal fusion** placed on text side.  
  - **Fusion-free text layer (Eq. 4):**  
    \(T_l^s=\text{MSA}(T_{l-1},T_{l-1},T_{l-1});\ \hat T_l=\text{LN}(T_l^s+T_{l-1});\ T_l=\text{LN}(\text{MLP}(\hat T_l)+\hat T_l)\). Output \(T=T_L\).
  - **Fusion-based (parallel) text layer (Eq. 5):**  
    \(M_l^s=\text{MSA}(M_{l-1},M_{l-1},M_{l-1});\ M_l^c=\text{MCA}(M_{l-1},V,V);\ \tilde M_l=\tfrac12(M_l^s+M_l^c)\) then LN+MLP as above. Output \(M=M_L\). **Parallel** makes fusion easy to remove at inference.
- **Training objectives (Section 4):**
  - **ITC contrastive (Eq. 6–8):** similarities \(s_{i2t}, s_{t2i}\) via projected, L2-normalized CLS embeddings; softmax with temperature \(\sigma\); loss \(L_{itc}=\tfrac12[H(y_{i2t},p_{i2t})+H(y_{t2i},p_{t2i})]\). Uses MoCo-style queues of size \(K\).
  - **ITM (Eq. 9):** binary match classifier on \(M_{cls}\); hard negatives sampled by similarity.
  - **Cross-modal knowledge transfer CKT (Eq. 11):** force unimodal CLS to approximate multimodal CLS:  
    \(L_{I2M}=\text{MSE}(f_v(V_{cls}), f_t(M_{cls}))\), \(L_{T2M}=\text{MSE}(f_t(T_{cls}), f_t(M_{cls}))\).
- **Fusion ablation (Table 4, 50K pretrain steps):** Parallel best.  
  - MSCOCO TR@1/IR@1: Concatenation 72.5/54.2; Cascading 73.0/54.5; **Parallel 73.5/55.4**.  
  - Flickr30k TR@1/IR@1: 92.6/80.5; 91.7/81.2; **93.1/81.6**.
- **CKT ablation (Table 5):** I2M helps text-retrieval; T2M helps image-retrieval; both best overall. With both: MSCOCO avg retrieval 87.2 (vs 86.3 baseline), VQAv2 test-dev 77.57, NLVR2 test-P 83.37.
- **Placing fusions on both sides hurts (Fig. 4):** FOD-both drops vs FOD on VQA/NLVR and Flickr30k TR/IR (authors attribute to harder self-supervision on vision side vs MLM on text).
- **Key downstream results:**  
  - **VQAv2 test-std 78.91; NLVR2 test-P 85.29** (Table 3; pretrain 3M).  
  - Retrieval fine-tuned (Table 1, Dual): MSCOCO TR R@1 **77.3**, IR R@1 **58.9**; Flickr30k TR R@1 **94.6**, IR R@1 **83.5**.
- **Defaults (Section 5.1.2):** Pretrain on 3.4M images (“3M”); ViT-Base init BEiT; text init uncased BERT-base; image res 256², patch 16²; AdamW wd 1e-2; lr 1e-4 warmup 1k; 300K steps on 32×A100, batch 2048.

## When to surface
Use when students ask how **early/late/parallel fusion** affects VL performance/efficiency, or want **ablation numbers** comparing fusion strategies and the role of **knowledge transfer** in retaining dual-encoder retrieval quality.