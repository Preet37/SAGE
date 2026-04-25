---
title: "CNNs"
subject: "Foundational AI"
date: 2025-04-06
tags:
  - "subject/foundational-ai"
  - "level/beginner"
  - "level/intermediate"
  - "level/advanced"
  - "educator/christopher-olah"
  - "educator/sebastian-raschka"
  - "resource/video"
  - "resource/blog"
  - "resource/deep-dive"
  - "resource/paper"
  - "resource/code"
educators:
  - "Christopher Olah"
  - "Sebastian Raschka"
levels:
  - "beginner"
  - "intermediate"
  - "advanced"
resources:
  - "video"
  - "blog"
  - "deep-dive"
  - "paper"
  - "code"
---

# Cnns

## Video (best)
- **Andrej Karpathy / Stanford CS231n** — "Lecture 5: Convolutional Neural Networks"
- **Watch:** [YouTube](https://www.youtube.com/watch?v=YRhxdVk_sIs)
- Why: CS231n Lecture 5 is the canonical academic treatment of CNNs — covers convolution mechanics, stride, padding, pooling, and feature maps with precise mathematical intuition. Karpathy's delivery bridges theory and practice better than any other single lecture on this topic.
- Level: intermediate

## Blog / Written explainer (best)
- **Christopher Olah** — "Conv Nets: A Modular Perspective"
- **Link:** [https://colah.github.io/posts/2014-07-Conv-Nets-Modular/](https://colah.github.io/posts/2014-07-Conv-Nets-Modular/)
- Why: Olah builds CNN intuition from first principles using a modular decomposition — convolution as a patch operation, pooling as downsampling, and how these compose into feature hierarchies. His visual style makes abstract spatial operations concrete. Pairs well with his companion post on understanding convolutions.
- Level: beginner/intermediate

## Deep dive
- **CS231n Course Notes** — "Convolutional Neural Networks for Visual Recognition"
- **Link:** [https://cs231n.github.io/convolutional-networks/](https://cs231n.github.io/convolutional-networks/)
- Why: The most comprehensive freely available written reference for CNNs. Covers the full stack: convolution arithmetic, parameter sharing, pooling variants, common architectures (LeNet, AlexNet, VGG, ResNet), and practical implementation considerations. Regularly cited in research and industry onboarding.
- Level: intermediate/advanced

## Original paper
- **Krizhevsky, Sutskever, Hinton (2012)** — "ImageNet Classification with Deep Convolutional Neural Networks" (AlexNet)
- **Link:** [https://papers.nips.cc/paper/2012/hash/c399862d3b9d6b76c8436e924a68c45b-Abstract.html](https://papers.nips.cc/paper/2012/hash/c399862d3b9d6b76c8436e924a68c45b-Abstract.html)
- Why: AlexNet is the inflection point for modern CNNs — it demonstrated that deep convolutional architectures trained on ImageNet with GPUs and ReLU activations could dramatically outperform prior methods. Highly readable for a systems paper; directly motivates every concept in the topic (convolution, pooling, feature maps, ImageNet benchmark). The arxiv mirror is: https://arxiv.org/abs/1404.5997 [NOT VERIFIED]
- Level: intermediate

## Code walkthrough
- **Sebastian Raschka** — "Convolutional Neural Networks from Scratch in PyTorch"
- **Link:** [https://github.com/rasbt/machine-learning-book](https://github.com/rasbt/machine-learning-book)
- Why: Raschka's implementations are pedagogically structured — he builds from a manual convolution operation up to a full training loop, with clear annotation of each step. His code prioritizes readability over performance, making it ideal for learners.
- Level: intermediate

> **Alternative (higher confidence):** The official PyTorch tutorial "Training a Classifier" at https://pytorch.org/tutorials/beginner/blitz/cifar10_tutorial.html is a well-maintained, verified code walkthrough that covers CNN construction, feature maps, and training on a real dataset (CIFAR-10, closely related to ImageNet-scale thinking).

---

## Coverage notes
- **Strong:** Core convolution mechanics, pooling, feature maps, ImageNet benchmarking, AlexNet-era architecture design — all extremely well covered across video, blog, and reference materials.
- **Weak:** The transition from CNNs to Vision Transformers (ViT) and DINOv2 specifically is underserved in single resources — most CNN resources predate or treat ViT as a separate topic.
- **Gap:** No single excellent resource cleanly bridges CNNs → DINOv2 (self-supervised ViT) in one narrative. For the `intro-to-multimodal` course context, instructors will need to supplement with the DINOv2 paper (https://arxiv.org/abs/2304.07193) and Yannic Kilcher's ViT walkthrough separately. The related concept `vision transformer` likely needs its own resource card.

---

## Cross-validation
This topic appears in 2 courses: **intro-to-multimodal**, **ml-engineering-foundations**

- For `intro-to-multimodal`: Emphasis should be on CNNs as feature extractors and the conceptual bridge to ViT/DINOv2. The Olah blog and CS231n notes cover the extractor framing well.
- For `ml-engineering-foundations`: Emphasis should be on implementation, parameter counts, memory/compute tradeoffs, and practical training. The PyTorch CIFAR-10 walkthrough and CS231n notes are most relevant here.

---

---

## Additional Resources for Tutor Depth

> **10 sources** — papers, official docs, working code, benchmarks, and deep explainers that give the AI tutor precision on this topic.

### 📄 DINOv2 (LVD-142M curation + eval results)
**Paper** · [source](http://arxiv.org/pdf/2304.07193.pdf)

*DINOv2 details: LVD-142M dataset curation/processing, evaluation protocols, ImageNet + downstream results, linear vs k-NN vs finetune, ablations, ViT sizes/patch sizes/distillation.*

<details>
<summary>Key content</summary>

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

</details>

### 📄 DeiT/ViT tokenization + distillation token (DeiT)
**Paper** · [source](https://arxiv.org/pdf/2012.12877.pdf)

*Practical ViT token pipeline (patch→tokens + class token + positional embeddings) and DeiT’s distillation token + key training/accuracy impacts.*

<details>
<summary>Key content</summary>

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

</details>

### 📄 Inception v1 / GoogLeNet (ILSVRC14) — efficiency via multi-branch + 1×1 bottlenecks
**Paper** · [source](https://arxiv.org/abs/1409.4842)

*ImageNet results + Inception module rationale (1×1 reductions, multi-scale branches, auxiliary classifiers) and compute/parameter efficiency*

<details>
<summary>Key content</summary>

- **Compute/parameter efficiency targets (Intro):**
  - Designed around ~**1.5 billion multiply-adds** at inference (computational budget).
  - **GoogLeNet uses ~12× fewer parameters** than Krizhevsky et al. (AlexNet, ILSVRC12 winner) while being **more accurate**.
- **Inception module design (Section 4, Fig. 2):**
  - Parallel branches: **1×1 conv**, **3×3 conv**, **5×5 conv**, and **3×3 max-pool**, then **concatenate** along channels.
  - **1×1 convolutions used as dimension reduction** (“#3×3 reduce”, “#5×5 reduce”) before expensive 3×3/5×5 convs to prevent compute blow-up; also used as **pool projection** after pooling.
  - Rationale: approximate an “optimal sparse” structure with dense ops; **multi-scale processing** (different receptive fields) aggregated per module.
- **Depth / architecture facts (Section 4):**
  - GoogLeNet is **22 layers deep** (counting layers with parameters); Inception modules stacked with occasional stride-2 pooling.
  - Uses **ReLU** throughout (including reduction/projection layers).
- **Auxiliary classifiers (Section 5):**
  - Added at outputs of **Inception (4a)** and **(4d)** to help gradient propagation + regularization.
  - **Aux loss weight = 0.3** added to main loss during training; **discarded at inference**.
  - Aux head: avg pool **5×5, stride 3** → **1×1 conv 128** → FC **1024** → dropout **70% dropped** → softmax (1000 classes).
- **Training/testing procedure (Sections 6–7):**
  - **Async SGD**, **momentum 0.9**; learning rate **decreased by 4% every 8 epochs**; **Polyak averaging** for final model.
  - ILSVRC metric: **top-5 error** (correct if GT in top 5).
- **Key empirical results (Section 7):**
  - Final ILSVRC14 submission: **top-5 error = 6.67%** (validation and test), **7-model ensemble** with **144 crops**.
  - Detection: ensemble of **6 GoogLeNets** improves region classification accuracy **40% → 43.9%**; proposal reduction to ~**60%** of R-CNN proposals while coverage **92% → 93%**; ~**+1% mAP** single-model effect from proposal changes.

</details>

### 📄 ResNet—Residual blocks, degradation problem, ImageNet depth results
**Paper** · [source](https://arxiv.org/abs/1512.03385)

*ImageNet benchmark across depths (18/34/50/101/152), residual-block rationale + optimization evidence (degradation)*

<details>
<summary>Key content</summary>

- **Degradation problem (Intro, Fig.1/Fig.4):** Increasing depth in *plain* nets can **increase training error** (not just overfitting). Example: on ImageNet, **34-layer plain** has **higher training error throughout training** than **18-layer plain** (Fig.4 left), despite BN and healthy gradient norms.
- **Residual learning reformulation (Sec.3.1):**  
  - Desired mapping: **H(x)**. Residual mapping: **F(x) := H(x) − x**.  
  - Output with shortcut: **y = F(x, {Wi}) + x** (**Eq.1**).  
  - If dimensions differ: **y = F(x, {Wi}) + Ws x** (**Eq.2**), where **Ws** is a linear projection (typically **1×1 conv**) used mainly for dimension matching.
  - **Rationale:** If identity mapping is optimal, easier to push **F(x) → 0** than to make stacked nonlinear layers approximate identity.
- **Empirical optimization benefit (Sec.4, Fig.4):** With residual blocks, situation reverses: **ResNet-34 > ResNet-18** and shows **lower training error** + better validation generalization (Fig.4 right).
- **Bottleneck design for deeper nets (Sec.3.3):** Residual block uses **1×1, 3×3, 1×1** conv stack (Fig.5) for efficiency; identity shortcuts preferred; projection shortcuts can increase cost.
- **Complexity & depth (Sec.4):**  
  - **ResNet-50:** ~**3.8B FLOPs**.  
  - **ResNet-152:** ~**11.3B FLOPs**, still < **VGG-16/19** (**15.3/19.6B FLOPs**).
- **Headline ImageNet results (Abstract/Table 5):** **152-layer** evaluated; **ensemble top-5 test error = 3.57%** (ILSVRC 2015 winner). Single-model **152-layer top-5 val error = 4.49%**.
- **Training defaults (Sec.3.4):** **SGD**, batch size **256**, LR **0.1** then ÷10 on plateau; **BN after each conv before activation**; weight decay **0.0001**, momentum **0.9**; **no dropout**; global average pooling + 1000-way FC.

</details>

### 📄 VGG (Very Deep ConvNets) — depth + 3×3 stacks on ImageNet
**Paper** · [source](https://arxiv.org/abs/1409.1556)

*Canonical ImageNet error tables across depth variants (11/13/16/19) + rationale for stacking 3×3 convs vs larger kernels*

<details>
<summary>Key content</summary>

- **Architecture defaults (Sec. 2.1):**
  - Input: **224×224 RGB**; preprocess: **subtract mean RGB** (train-set mean).
  - Convs: **3×3 filters**, **stride 1**, **padding 1** (preserve spatial size). Optional **1×1 conv** in one config.
  - Pooling: **5 max-pool** layers, **2×2 window**, **stride 2**.
  - Classifier: **3 FC layers**: 4096, 4096, 1000 + softmax. **ReLU** on hidden layers.
  - **LRN**: tested (A-LRN) but **no improvement** → omitted in deeper nets (B–E).
- **Depth variants (Sec. 2.2):** configs differ mainly by depth: **A=11** (8 conv + 3 FC) … **E=19** (16 conv + 3 FC). Channels start **64**, double after each max-pool up to **512**.
- **Design rationale (Sec. 2.3): effective receptive field + parameter count**
  - Two 3×3 convs ⇒ **5×5** effective RF; three 3×3 ⇒ **7×7** effective RF.
  - Parameter comparison (C channels in/out):  
    - 3-layer 3×3 stack: **3·(3²)·C² = 27C²** weights  
    - single 7×7: **7²·C² = 49C²** weights (**81% more**)  
  - Benefit: **more non-linearities** (3 ReLUs vs 1) + fewer params (regularizing decomposition).
- **Training hyperparameters (Sec. 3.1):**
  - Mini-batch SGD: **batch 256**, **momentum 0.9**, **weight decay 5e−4**, **dropout 0.5** (first two FC).
  - LR: start **1e−2**, drop ×10 when val stalls; **3 drops total**; stop **370k iters (~74 epochs)**.
  - Init: weights ~ **N(0, 1e−2)**, biases 0; deeper nets partially initialized from net A.
  - Scale: train at **S=256**, optionally fine-tune at **S=384** (LR **1e−3**); also **scale jittering** with S sampled from **[Smin, Smax]**.
- **Testing workflow (Sec. 3.2):**
  - Resize so min side **Q ≥ 224**; convert FC→conv (**FC1→7×7 conv; FC2/FC3→1×1 conv**); apply **densely** over whole image; **spatially average (sum-pool)** score map; average with **horizontal flip**.
- **Key empirical findings (Sec. 4):**
  - Error decreases with depth **11→16 layers**; **19 layers saturates** (no further gain).
  - **Config D (all 3×3)** beats **Config C (includes 1×1)** despite same depth → spatial context matters.
  - Replacing pairs of 3×3 with single 5×5 (same RF) yields **top-1 error ~7% higher** (shallower worse).
  - Best single-network reported with scale jittering: **25.9% top-1 / 8.0% top-5** error.
  - Ensemble: **2 nets** achieve **6.8% top-5 test error** (multi-crop & dense eval).

</details>

### 📖 Torchvision `vit_b_16` (Vision Transformer Base, patch=16) API + Weights/Transforms
**Reference Doc** · [source](https://docs.pytorch.org/vision/stable/models/generated/torchvision.models.vit_b_16.html)

*Official builder signature, available pretrained weight enums, and exact inference preprocessing transforms (resize/crop/normalize), plus key metrics (acc, params, GFLOPs, min input size).*

<details>
<summary>Key content</summary>

- **Model builder (signature):**  
  `torchvision.models.vit_b_16(*, weights=None, progress=True, **kwargs) -> VisionTransformer`  
  - `weights`: optional pretrained weights enum (or string like `'DEFAULT'`).  
  - `progress`: download progress bar (default `True`).  
  - `**kwargs`: forwarded to `torchvision.models.vision_transformer.VisionTransformer` base class.
- **Weights enum:** `torchvision.models.ViT_B_16_Weights`  
  - `ViT_B_16_Weights.DEFAULT == ViT_B_16_Weights.IMAGENET1K_V1`
- **Empirical results / model stats (ImageNet-1K):**
  - `IMAGENET1K_V1`: acc@1 **81.072**, acc@5 **95.318**, **86,567,656** params, **17.56** GFLOPs, min_size **224×224**, file **330.3 MB**.
  - `IMAGENET1K_SWAG_E2E_V1` (end-to-end fine-tune): acc@1 **85.304**, acc@5 **97.65**, **86,859,496** params, **55.48** GFLOPs, min_size **384×384**, file **331.4 MB**.
  - `IMAGENET1K_SWAG_LINEAR_V1` (frozen trunk + linear head): acc@1 **81.886**, acc@5 **96.18**, **86,567,656** params, **17.56** GFLOPs, min_size **224×224**, file **330.3 MB**.
- **Inference preprocessing (via `weights.transforms`):** accepts `PIL.Image` or `torch.Tensor` images: single `(C,H,W)` or batched `(B,C,H,W)`.  
  - Common final steps: rescale to **[0.0, 1.0]**, then normalize with **mean=[0.485, 0.456, 0.406]**, **std=[0.229, 0.224, 0.225]**.
  - `IMAGENET1K_V1.transforms`: resize **[256]** (BILINEAR) → center crop **[224]**.
  - `SWAG_E2E_V1.transforms`: resize **[384]** (BICUBIC) → center crop **[384]**.
  - `SWAG_LINEAR_V1.transforms`: resize **[224]** (BICUBIC) → center crop **[224]**.

</details>

### 📋 # Source: https://docs.pytorch.org/docs/stable/generated/torch.nn.Conv2d.html
**Source** · 

### 📋 # Source: https://docs.pytorch.org/docs/stable/generated/torch.nn.MaxPool2d.html
**Source** · 

### 🔍 Convolution / Pooling / Transposed Conv Output-Size Arithmetic
**Explainer** · [source](https://arxiv.org/pdf/1603.07285.pdf)

*Output-size formulas for conv/pooling/transposed conv (incl. padding/stride/dilation), with canonical “same/full” cases.*

<details>
<summary>Key content</summary>

- **Per-axis independence (Sec. 2):** compute output size separately for each axis \(j\) using input \(i_j\), kernel/window \(k_j\), stride \(s_j\), padding \(p_j\). (Paper often shows square 2D case: \(i,k,s,p\).)
- **Direct convolution output size**
  - **No padding, stride 1 (Rel. 1):** \(o = (i-k)+1\).
  - **Padding \(p\), stride 1 (Rel. 2):** \(o = (i-k)+2p+1\) (effective input \(i+2p\)).
  - **“Same” / half padding, stride 1, odd \(k=2n+1\) (Rel. 3):** \(p=\lfloor k/2\rfloor=n \Rightarrow o=i\).
  - **“Full” padding, stride 1 (Rel. 4):** \(p=k-1 \Rightarrow o=i+(k-1)\).
  - **No padding, stride \(s\) (Rel. 5):** \(o=\left\lfloor\frac{i-k}{s}\right\rfloor+1\).
  - **General padding + stride (Rel. 6):** \(o=\left\lfloor\frac{i+2p-k}{s}\right\rfloor+1\).
- **Pooling output size (Sec. 3, Rel. 7):** same as strided conv without padding: \(o=\left\lfloor\frac{i-k}{s}\right\rfloor+1\).
- **Transposed convolution output size**
  - **Stride 1 (Rel. 9):** for conv with kernel \(k\), padding \(p\): transposed has \(p' = k-p-1\), output \(o' = i' + (k-1) - 2p\). Special cases:  
    - **No padding (Rel. 8):** \(p=0 \Rightarrow p'=k-1,\ o'=i'+(k-1)\).  
    - **Same padding (Rel. 10):** \(p=\lfloor k/2\rfloor \Rightarrow o'=i'\).  
    - **Full padding (Rel. 11):** \(p=k-1 \Rightarrow p'=0,\ o'=i'-(k-1)\).
  - **Stride \(s>1\) (Rel. 14):** \(o' = s(i'-1) + a + k - 2p\), where \(a=(i+2p-k)\bmod s\) (disambiguates cases); conceptual “stretching” inserts \(s-1\) zeros between input units.
- **Dilated conv (Sec. 5.1):** effective kernel \(\hat{k}=k+(k-1)(d-1)\); output (Rel. 15):  
  \(o=\left\lfloor\frac{i+2p-k-(k-1)(d-1)}{s}\right\rfloor+1\).

</details>

### 📋 DINOv2 model loading + eval entry points (PyTorch Hub)
**Code** · [source](https://github.com/facebookresearch/dinov2/blob/main/README.md)

*Official model-loading/usage patterns, model variants, and evaluation commands.*

<details>
<summary>Key content</summary>

- **What DINOv2 provides (design rationale):** pretrained self-supervised ViT backbones that yield **robust visual features usable “as-is”** with simple classifiers (e.g., linear layers) across tasks/domains **without fine-tuning**. Pretrained on **142M images** with **no labels/annotations**.
- **Backbone variants + params (empirical):** ViT-S/14 distilled **21M params** (table lists additional ViT-B/14, ViT-L/14, ViT-g/14; also “with registers” variants).
- **ImageNet performance example (empirical):** ViT-S/14 distilled (no registers): **79.0% k-NN**, **81.1% linear** (ImageNet-1k).
- **Load pretrained backbones (procedure):**
  ```python
  import torch
  dinov2_vits14 = torch.hub.load('facebookresearch/dinov2','dinov2_vits14')
  dinov2_vitb14 = torch.hub.load('facebookresearch/dinov2','dinov2_vitb14')
  dinov2_vitl14 = torch.hub.load('facebookresearch/dinov2','dinov2_vitl14')
  dinov2_vitg14 = torch.hub.load('facebookresearch/dinov2','dinov2_vitg14')
  # with registers
  dinov2_vits14_reg = torch.hub.load('facebookresearch/dinov2','dinov2_vits14_reg')
  ```
- **Load full classifier (“lc”) models (procedure):**
  ```python
  dinov2_vitb14_lc = torch.hub.load('facebookresearch/dinov2','dinov2_vitb14_lc')
  dinov2_vitb14_reg_lc = torch.hub.load('facebookresearch/dinov2','dinov2_vitb14_reg_lc')
  ```
- **Evaluate pretrained weights on ImageNet-1k (procedure):**
  ```bash
  python dinov2/run/eval/linear.py \
    --config-file dinov2/configs/eval/vitg14_pretrain.yaml \
    --pretrained-weights https://dl.fbaipublicfiles.com/dinov2/dinov2_vitg14/dinov2_vitg14_pretrain.pth \
    --train-dataset ImageNet:split=TRAIN:root=<ROOT>:extra=<EXTRA> \
    --val-dataset   ImageNet:split=VAL:root=<ROOT>:extra=<EXTRA>
  ```
- **Training defaults/examples (procedure + parameters):**
  - Requires **PyTorch 2.0** + **xFormers 0.0.18** (Linux-tested).
  - Example runs: **4 nodes / 32 GPUs A100-80GB**, config `vitl16_short.yaml`, ~**1 day**, reaches **81.6% k-NN / 82.9% linear**; teacher weights saved every **12500 iterations**.
  - Larger: **12 nodes / 96 GPUs**, config `vitl14.yaml`, ~**3.3 days**, **82.0% k-NN / 84.5% linear**.
- **Extra model entry points (procedure):**
  - **dino.txt** hub id: `dinov2_vitl14_reg4_dinotxt_tet1280d20h24l`.
  - **XRay-DINO / Cell-DINO / Channel-Adaptive DINO** loaded via `torch.hub.load(REPO_DIR, ..., source='local', weights=... or pretrained_path/pretrained_url=...)`.

</details>

---

## Related Topics

- [[topics/neural-networks|Neural Networks]]
- [[topics/multimodal-fundamentals|Multimodal Fundamentals]]
- [[topics/vision-language-models|Vision Language Models]]
