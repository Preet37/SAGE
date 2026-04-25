# Card: DINOv2 (LVD-142M curation + eval results)
**Source:** http://arxiv.org/pdf/2304.07193.pdf  
**Role:** paper | **Need:** EMPIRICAL_DATA  
**Anchor:** DINOv2 details: LVD-142M dataset curation/processing, evaluation protocols, ImageNet + downstream results, linear vs k-NN vs finetune, ablations, ViT sizes/patch sizes/distillation.

## Key Content
- **LVD-142M data pipeline (Sec. 3):**
  - Start from **1.2B unique web images** after URL filtering + postprocess: **PCA-hash dedup**, **NSFW filtering**, **blur identifiable faces**.
  - Remove near-duplicates via **copy detection** (Pizzi et al. 2022) and remove near-duplicates of **any benchmark val/test** images.
  - **Self-supervised retrieval curation:** embed images with **self-supervised ViT-H/16 pretrained on ImageNet-22k**; use **cosine similarity**; **k-means** cluster uncurated pool; retrieve typically **k=4 nearest neighbors** per curated query (more neighbors increased “collisions”).
  - Uses **Faiss** GPU IVF+PQ; processing distributed on **20 nodes × 8×V100-32GB**, **<2 days**.
- **Training objective (Sec. 4):** combined **DINO (image-level)** + **iBOT (patch-level masked tokens)** with **SwAV centering**.
  - DINO loss: cross-entropy between student/teacher prototype distributions from **[CLS] token** (teacher is **EMA** of student).
  - iBOT loss: cross-entropy on **masked patch tokens** (student sees masks; teacher sees visible patches).
  - **Sinkhorn-Knopp centering:** **3 iterations** for teacher; student uses softmax.
  - **KoLeo regularizer:** \(L=\frac{1}{n}\sum_i \log d_i\), \(d_i=\min_{j\neq i}\|x_i-x_j\|\) on **L2-normalized** features (encourages spread).
  - **Resolution schedule:** short high-res phase: train at **224**, then **+10k iters at 518**.
- **Ablation (Table 1, ViT-L on INet-22k):** iBOT **kNN 72.9 / linear 82.3** → DINOv2 **kNN 82.0 / linear 84.5**; key steps include **128k prototypes**, **patch size 14**, **teacher momentum 0.994**, **batch size 3k**, **untying DINO/iBOT heads**.
- **Data source impact (Table 2, ViT-g/14):** Uncurated **INet-1k 83.3, Im-A 59.4** vs **LVD-142M INet-1k 85.8, Im-A 73.9**, Oxford-M **64.6**.
- **Loss ablations (Table 3):** KoLeo improves Oxford-M **55.6→63.9**; removing MIM drops ADE20k **47.1→44.2**.
- **Distillation (Sec. 5, Table in 6.5):** ViT-L/14 **scratch INet-1k 84.5** vs **distill 86.3** (teacher ViT-g/14 scratch **86.5**).
- **ImageNet linear eval (Table 4, frozen):** DINOv2 **ViT-B/14 84.5**, **ViT-L/14 86.3**, **ViT-g/14 86.5** (val top-1).
- **Finetuning sanity check (Table 5):** ViT-g/14 linear **86.5@224 → finetuned 88.5**; **86.7@448 → 88.9**.
- **Robustness (Table 6, linear head):** DINOv2 ViT-g/14: **Im-A 75.9, Im-R 78.8, Sketch 62.5**.
- **Dense tasks (Table 10):** ADE20k mIoU (linear): OpenCLIP-G **39.3** vs DINOv2 ViT-g/14 **49.0**; +ms: **46.0 vs 53.0**.

## When to surface
Use for questions about **how DINOv2 curates LVD-142M**, **what losses/regularizers it uses (DINO+iBOT+SK+KoLeo)**, and **concrete benchmark numbers comparing k-NN vs linear probe vs finetuning/distillation across ViT sizes/patch sizes**.