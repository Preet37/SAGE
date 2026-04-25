# Curation Report: Convolutional Neural Networks
**Topic:** `cnns` | **Date:** 2026-04-09 16:15
**Library:** 6 existing → 21 sources (15 added, 10 downloaded)
**Candidates evaluated:** 39
**Reviewer verdict:** needs_additions

## Added (15)
- **[reference_doc]** [Conv2d — PyTorch 2.11 documentation](https://docs.pytorch.org/docs/stable/generated/torch.nn.Conv2d.html)
  Gives authoritative, citable API defaults and the exact operator definition used in a major deep learning library, which is essential when students ask what “convolution” means in practice.
- **[explainer]** [[PDF] A guide to convolution arithmetic for deep learning - arXiv](https://arxiv.org/pdf/1603.07285.pdf)
  Provides the most teachable, step-by-step derivations for shape arithmetic that students routinely get wrong, enabling precise explanations and quick checks.
- **[paper]** [Published in Transactions on Machine Learning Research (01/2024)](http://arxiv.org/pdf/2304.07193.pdf)
  This is the primary authoritative source for DINOv2’s empirical results and methodology, giving the tutor concrete numbers and the exact evaluation setup to cite.
- **[code]** [dinov2/README.md at main · facebookresearch/dinov2](https://github.com/facebookresearch/dinov2/blob/main/README.md)
  Complements the paper with practical, reproducible code paths and “how to use the pretrained models” details students often need when implementing.
- **[paper]** [[PDF] Training data-efficient image transformers & distillation through ...](https://arxiv.org/pdf/2012.12877.pdf)
  Gives a concrete, step-by-step transformer-for-images pipeline (including special tokens) that can be contrasted with CNN feature maps/pooling when teaching architectural differences.
- **[reference_doc]** [MaxPool2d — PyTorch documentation (stable)](https://docs.pytorch.org/docs/stable/generated/torch.nn.MaxPool2d.html)
  Pooling defaults and shape rules are a frequent source of student errors; even “thin” API docs are exactly what you want for citable specs and to complement the Conv2d reference.
- **[reference_doc]** [vit_b_16 — Torchvision documentation (stable)](https://docs.pytorch.org/vision/stable/models/generated/torchvision.models.vit_b_16.html)
  This fills the missing “official ViT patch embedding implementation parameters” need with a stable, citable source; forum threads are not a substitute for canonical docs.
- **[paper]** [Very Deep Convolutional Networks for Large-Scale Image Recognition (VGG)](https://arxiv.org/abs/1409.1556)
  Your library lacks the classic CNN benchmark tables/training setups; VGG is one of the cleanest sources for depth/kernel-size ablations and widely cited numbers.
- **[paper]** [Going Deeper with Convolutions (GoogLeNet / Inception v1)](https://arxiv.org/abs/1409.4842)
  Directly addresses the unfilled need for early CNN recipes and ablations (architecture choices for compute/accuracy), which are central to teaching why CNNs evolved the way they did.
- **[paper]** [Deep Residual Learning for Image Recognition (ResNet)](https://arxiv.org/abs/1512.03385)
  This is already in the current library by ID, but if the curator treated it as “just an abstract,” the full paper is essential: it contains the canonical numbers and the core architectural argument that modern CNN teaching relies on.
- **[reference_doc]** [MaxPool2d — PyTorch documentation (stable)](https://docs.pytorch.org/docs/stable/generated/torch.nn.MaxPool2d.html) *(promoted by reviewer)*
  Pooling defaults and shape rules are a frequent source of student errors; even “thin” API docs are exactly what you want for citable specs and to complement the Conv2d reference.
- **[reference_doc]** [vit_b_16 — Torchvision documentation (stable)](https://docs.pytorch.org/vision/stable/models/generated/torchvision.models.vit_b_16.html) *(promoted by reviewer)*
  This fills the missing “official ViT patch embedding implementation parameters” need with a stable, citable source; forum threads are not a substitute for canonical docs.
- **[paper]** [Very Deep Convolutional Networks for Large-Scale Image Recognition (VGG)](https://arxiv.org/abs/1409.1556) *(promoted by reviewer)*
  Your library lacks the classic CNN benchmark tables/training setups; VGG is one of the cleanest sources for depth/kernel-size ablations and widely cited numbers.
- **[paper]** [Going Deeper with Convolutions (GoogLeNet / Inception v1)](https://arxiv.org/abs/1409.4842) *(promoted by reviewer)*
  Directly addresses the unfilled need for early CNN recipes and ablations (architecture choices for compute/accuracy), which are central to teaching why CNNs evolved the way they did.
- **[paper]** [Deep Residual Learning for Image Recognition (ResNet)](https://arxiv.org/abs/1512.03385) *(promoted by reviewer)*
  This is already in the current library by ID, but if the curator treated it as “just an abstract,” the full paper is essential: it contains the canonical numbers and the core architectural argument that modern CNN teaching relies on.

## Near-Misses (3) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **Conv2d — PyTorch main documentation** — [Conv2d — PyTorch main documentation](https://docs.pytorch.org/docs/main/generated/torch.nn.modules.conv.Conv2d.html)
  _Skipped because:_ Similar content to the stable docs but less ideal for citation because “main” can change across commits/versions.
- **DINOv2: Learning Robust Visual Features without Supervision ** — [DINOv2: Learning Robust Visual Features without Supervision - arXiv](https://arxiv.org/html/2304.07193v2)
  _Skipped because:_ The HTML version is convenient, but the PDF is more stable for quoting tables/figures and page-referenced citations.
- **Training data-efficient image transformers & distillation ..** — [Training data-efficient image transformers & distillation ...](https://proceedings.mlr.press/v139/touvron21a/touvron21a.pdf)
  _Skipped because:_ Essentially the same work as the arXiv PDF; kept only one canonical PDF to avoid duplication.

## Reasoning
**Curator:** Selections prioritize authoritative, citable sources that directly provide (1) exact operator/API definitions and defaults (PyTorch docs, official DINOv2 repo) and (2) concrete empirical results and training/evaluation procedures (DINOv2 paper, DeiT). Remaining gaps require sources not present in the candidate list (early CNN benchmark papers and ViT original/torchvision pooling+patch-embed docs).
**Reviewer:** The curation is strong on CNN intuition and convolution arithmetic, but it still needs a few canonical benchmark papers (VGG/Inception/ResNet) and thin-but-essential official docs for pooling and torchvision ViT specs.
