# Card: SigLIP/SigLiT — Pairwise Sigmoid Loss vs Softmax (InfoNCE) + Batch-Size Effects
**Source:** https://arxiv.org/pdf/2303.15343v3.pdf  
**Role:** benchmark | **Need:** EMPIRICAL_DATA  
**Anchor:** Tables/ablations with ImageNet zero-shot accuracy vs batch size; shows sigmoid loss benefits (esp. small BS) and saturation ~32k; includes 84.5% claim (large LiT + SigLIP/SigLiT).

## Key Content
- **Softmax (InfoNCE) loss (Sec. 3.1):** for batch \(B\), normalized embeddings \(x_i=\frac{f(I_i)}{\|f(I_i)\|_2}\), \(y_i=\frac{g(T_i)}{\|g(T_i)\|_2}\), temperature \(t=\exp(t')\):  
  \[
  \mathcal{L}_{softmax}=-\frac{1}{2|B|}\sum_{i=1}^{|B|}\Big(\log\frac{e^{t x_i\cdot y_i}}{\sum_j e^{t x_i\cdot y_j}}+\log\frac{e^{t x_i\cdot y_i}}{\sum_j e^{t x_j\cdot y_i}}\Big)
  \]
- **Pairwise sigmoid loss (Sec. 3.2, Alg. 1):** logits \(s_{ij}=t\,x_i\!\cdot\! y_j + b\); labels \(z_{ij}=+1\) if matched else \(-1\):  
  \[
  \mathcal{L}_{sigmoid}=-\frac{1}{|B|}\sum_i\sum_j \log \sigma(z_{ij}\, s_{ij})
  \]
  **Defaults:** initialize \(t'=\log 10\) (so \(t=10\)), **bias** \(b=-10\) to prevent early over-correction from huge neg:pos imbalance.
- **Efficient “chunked” distributed implementation (Sec. 3.3, Fig. 1):** avoid all-gathers; compute loss on local \(b\times b\) blocks while permuting text (or image) embeddings across devices; reduces memory from \(|B|^2\) to \(b^2\).
- **Key ImageNet zero-shot results (Table 1):**
  - **SigLiT** (frozen public ViT-g/14 vision; LiT dataset): **BS 20k**, **4 TPUv4**, **2 days** → **84.5%**
  - SigLiT (frozen public B/8; BS 32k; 4 TPUv4; 1 day) → **79.7%**
  - SigLIP (from scratch, WebLI): B/16, BS 32k, 32 TPUv4, 5 days → **73.4%**
- **Batch-size ablations (Fig. 2; Tables 4–5):**
  - Sigmoid **outperforms softmax strongly when BS < 16k**; gap closes at large BS.
  - Performance **saturates around 32k**; very large BS (e.g., 307k) can hurt.
  - **SigLIP 9B examples (Table 4):** sigmoid peak **73.4% @32k** vs softmax peak **73.2% @98k**; at **307k**: sigmoid **71.6%**, softmax **72.6%**.
- **Stabilizing large-batch training (Sec. 4.6):** reduce Adam/AdaFactor \(\beta_2\) from **0.999 → 0.95** to mitigate gradient spikes.
- **Bias ablation (Table 3, BS 8k, 900M examples):** with bias \(b=-10\): ImageNet **63.0%** vs **62.0%** without bias.

## When to surface
Use when students ask how SigLIP/SigLiT differs from CLIP/InfoNCE, why sigmoid loss helps at smaller batch sizes, how batch size affects zero-shot ImageNet accuracy, or how to implement contrastive loss efficiently across devices.