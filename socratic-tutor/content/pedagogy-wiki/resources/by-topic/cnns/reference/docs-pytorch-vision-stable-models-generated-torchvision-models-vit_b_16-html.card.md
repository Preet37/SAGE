# Card: Torchvision `vit_b_16` (Vision Transformer Base, patch=16) API + Weights/Transforms
**Source:** https://docs.pytorch.org/vision/stable/models/generated/torchvision.models.vit_b_16.html  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Official builder signature, available pretrained weight enums, and exact inference preprocessing transforms (resize/crop/normalize), plus key metrics (acc, params, GFLOPs, min input size).

## Key Content
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

## When to surface
Use when students ask how to instantiate `vit_b_16` in Torchvision, which pretrained weights exist (and their accuracy/compute), or what exact input size and preprocessing/normalization pipeline to use for inference.