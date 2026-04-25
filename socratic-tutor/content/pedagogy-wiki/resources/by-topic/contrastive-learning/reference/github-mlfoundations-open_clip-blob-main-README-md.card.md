# Card: OpenCLIP quick API + training knobs (README)
**Source:** https://github.com/mlfoundations/open_clip/blob/main/README.md  
**Role:** code | **Need:** API_REFERENCE  
**Anchor:** Factory entry points for loading CLIP/OpenCLIP models + standard zero-shot workflow; training CLI defaults/flags; notes on activations & distributed loss scaling.

## Key Content
- **Load model + preprocess (factory):**
  - `model, _, preprocess = open_clip.create_model_and_transforms(model_name, pretrained=...)`
  - `tokenizer = open_clip.get_tokenizer(model_name)`
  - Set `model.eval()` (README notes model defaults to train mode; affects models w/ BatchNorm or stochastic depth).
- **Zero-shot inference procedure (cosine + temperature):**
  - Encode: `image_features = model.encode_image(image)`; `text_features = model.encode_text(text)`
  - L2 normalize: `x /= ||x||` along last dim.
  - Similarity logits: `logits = 100.0 * image_features @ text_features.T`
  - Probabilities: `softmax(logits, dim=-1)`
  - Variables: `image_features ∈ R^{B×D}`, `text_features ∈ R^{T×D}`.
- **Pretrained discovery:** `open_clip.list_pretrained()`. `pretrained` can be a key or local path (e.g., `/path/to/my/b32.pt`), including HF-downloaded `open_clip_pytorch_model.bin`.
- **Activation rationale / default:** Many checkpoints use **QuickGELU**; OpenCLIP model defs now default to `nn.GELU`. Use `-quickgelu` model variants to match QuickGELU weights; otherwise accuracy drop (fine-tuning may recover).
- **Distributed training memory rationale:** naive all-gather logit matrix is **O(n²)** space; use `--gather-with-grad` + `--local-loss` for effectively linear scaling with **numerically identical** results.
- **Training CLI example (key hyperparams):** `--batch-size=128 --lr=1e-3 --wd=0.1 --epochs=30 --warmup 10000 --workers=8 --model RN50`.
- **Empirical zero-shot ImageNet-1k examples (from table):**
  - ConvNext-Large LAION-2B 320px: **76.9%**
  - ViT-L-14 DataComp-1B 224px: **79.2%**
  - ViT-bigG-14 LAION-2B 224px: **80.1%**

## When to surface
Use when students ask how to load OpenCLIP models, run zero-shot classification, choose the correct `-quickgelu` variant, or scale CLIP training across many GPUs without quadratic logit-memory blowup.