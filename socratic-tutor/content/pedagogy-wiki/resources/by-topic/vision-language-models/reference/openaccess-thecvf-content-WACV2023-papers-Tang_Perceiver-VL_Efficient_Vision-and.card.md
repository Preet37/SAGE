# Card: Perceiver-VL efficiency via iterative latent attention
**Source:** https://openaccess.thecvf.com/content/WACV2023/papers/Tang_Perceiver-VL_Efficient_Vision-and-Language_Modeling_With_Iterative_Latent_Attention_WACV_2023_paper.pdf  
**Role:** paper | **Need:** COMPARISON_DATA  
**Anchor:** Perceiver-style iterative latent cross-attention as a visual token bottleneck; concrete FLOPs/latency vs accuracy tradeoffs + LayerDrop/mixed-stream retrieval.

## Key Content
- **Core idea (Sec. 3.2):** Map input array length **M** (concat visual+text embeddings) to latent array length **N** via **iterative cross-attention**, then self-attend only over latents.
- **Complexity formulas (Sec. 3.2):**
  - Perceiver-VL encoder with **k** blocks, each: 1 cross-attn + **l** latent self-attns  
    **O(kMN + klN²)**  
  - Standard transformer encoder with same # self-attns over inputs: **O(klM²)**  
  - Example input length: video 8 frames, 224², patch 16 ⇒ **M=(224/16)²·8=1568**, typical **N=128**.
- **Embeddings (Sec. 3.1):** input embedding = modality + temporal (video only) + positional + patch/token embedding; treat image as 1-frame video.
- **LayerDrop on cross-attn (Sec. 3.3, Table 3):** drop cross-attn layers during training with prob **pLD** (not first cross-attn). Enables inference-time depth reduction.
  - With LD during finetuning: inference time **72.0→58.0 ms** (−19.4%) with **R@1 27.1→26.3** on MSRVTT retrieval.
- **Mixed-stream retrieval (Sec. 3.5, Fig. 6):** accuracy/latency tradeoff on MSRVTT val:  
  - single-stream **R@1 27.2** (slowest), multi-stream **26.0** (fastest), **mixed-stream 26.8** (near single-stream, faster).
- **Key efficiency/accuracy comparisons (Tables 1–2):**
  - MSRVTT retrieval: **Perceiver-VL N=128 mixed**: **R@1 32.6**, **43.2 GFLOPs**, **72.0 ms** vs Frozen-in-Time: **R@1 31.0**, **89.0 GFLOPs**, **260 ms**.
  - VQAv2: **Perceiver-VL N=128**: **70.91 acc**, **30.5 GFLOPs**, **18 ms** vs ViLT-B/32: **71.26**, **55.9 GFLOPs**, **32 ms**.
- **Defaults (Sec. 4.1):** hidden 768, 12 heads; **k=3**, **l=3** (3 cross-attn, 12 self-attn); decoder: 1 cross-attn; image/frame size **384**, patch **32**; **pLD=0.5**.
- **Pretraining (Sec. 4.3):** CC (3M) + WebVid (2.5M); Adam lr **1e-5**, wd **0.001**, **200k steps**, batch **4096** (grad accum), 4×RTX2080Ti ~14 days.

## When to surface
Use when students ask why Perceiver/Q-Former-style bottlenecks reduce compute vs token-heavy fusion, or want concrete FLOPs/latency vs accuracy numbers and how LayerDrop/mixed-stream enable controllable inference cost.