# Card: VisDA-2017 (Sim-to-Real) UDA Benchmark
**Source:** https://ar5iv.labs.arxiv.org/html/1710.06924  
**Role:** benchmark | **Need:** EMPIRICAL_DATA  
**Anchor:** Official VisDA-2017 challenge description + dataset/task definitions + baseline & top challenge scores (classification/segmentation) + evaluation metrics

## Key Content
- **Problem setup (UDA, sim→real):** Train on **labeled source** (synthetic) and adapt using **unlabeled target**; **no target annotations** used for training. Two **different target domains**: one for **validation (hyperparams)** and a different one for **test** to prevent tuning on test labels (Section 3).
- **VisDA-C (classification) domains & scale (12 classes):**
  - **Source/train:** CAD-synthetic renderings, **152,397 images**, **1,907 3D models**.
  - **Target/val:** **MS COCO** crops, **55,388 images** (person capped at **4,000**).
  - **Target/test:** **YouTube-BB** frame crops, **72,372 images**.
  - Total across splits: **>280K images**.
- **Metric (classification):** **mean accuracy averaged over categories** (reported at **40k iterations** in baselines).
- **Baseline training defaults (AlexNet):** ImageNet init (except last FC=12); **SGD**, **momentum 0.9** (weight decay/base LR given but not legible in excerpt).  
  **ResNeXt-152:** last FC=12 with Xavier init; output layer LR = **10×** other layers; LR schedule: \(lr(p)=lr_0(1+\alpha p)^{-\beta}\), \(p\in[0,1]\), \(\alpha=10,\beta=0.75\).
- **Baseline results (VisDA-C):**
  - **Oracle (in-domain) AlexNet:** synthetic **99.92%**, real-val **87.62%**.
  - **Source-only AlexNet → real-val:** **28.12%**; **Deep CORAL 45.53%**; **DAN 51.62%**.
  - **Test domain:** Oracle AlexNet **92.08%**, Oracle ResNeXt-152 **93.40%**; Source-only AlexNet **30.81%**; **DAN 49.78%**, **Deep CORAL 45.29%**.
  - **Challenge top score (test):** GFColourLabUEA improved **ResNet-152 source-only 45.3% → 92.8%** using **Mean Teacher + label propagation** (student CE on source + student/teacher consistency MSE on both domains; teacher = EMA of student weights).
- **VisDA-S (segmentation) domains (19 classes) & metric:** GTA5 (source, **24,966** labeled frames) → CityScapes (val labeled) → Nexar/BDD (test, **1,500** images); metric **mIoU**.
  - **Dilation F.E. source:** **21.4 mIoU** on CityScapes val; **oracle 64.0**. On Nexar test: **source 25.9 mIoU**. Hoffman et al. adaptation reported **~25.5 mIoU** on val (also cited as **27.1** for their method in table caption).

## When to surface
Use for questions about **VisDA-2017 protocol**, **sim-to-real UDA evaluation**, **dataset/domain definitions**, and **benchmark numbers** (source-only vs adapted vs oracle; classification mean-per-class accuracy; segmentation mIoU).