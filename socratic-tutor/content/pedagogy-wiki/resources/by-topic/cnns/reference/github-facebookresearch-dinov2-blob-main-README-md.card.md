# Card: DINOv2 model loading + eval entry points (PyTorch Hub)
**Source:** https://github.com/facebookresearch/dinov2/blob/main/README.md  
**Role:** code | **Need:** API_REFERENCE  
**Anchor:** Official model-loading/usage patterns, model variants, and evaluation commands.

## Key Content
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

## When to surface
Use when students ask “How do I load a DINOv2 backbone/classifier in PyTorch?”, “Which model variants exist (registers, lc, dino.txt)?”, or “What’s the official command to run ImageNet linear/k-NN eval or reproduce training checkpoints?”