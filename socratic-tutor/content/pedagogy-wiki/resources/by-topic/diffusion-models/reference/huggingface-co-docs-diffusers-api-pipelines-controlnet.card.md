# Card: Stable Diffusion ControlNet Pipelines (Diffusers)
**Source:** https://huggingface.co/docs/diffusers/api/pipelines/controlnet  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** ControlNet pipeline parameters/behaviors (scales, guess mode, guidance windows, multi-ControlNet, image inputs) and integration with StableDiffusion pipelines.

## Key Content
- **What ControlNet adds (design rationale):** Adds *spatial conditioning* to a pretrained text-to-image diffusion model while “locking” the base model; uses **zero convolutions** (zero-initialized conv layers) so added paths start at 0 and “no harmful noise” affects finetuning (per ControlNet paper abstract quoted).
- **Core pipelines/classes:**
  - `StableDiffusionControlNetPipeline(vae, text_encoder, tokenizer, unet, controlnet, scheduler, safety_checker, feature_extractor, image_encoder=None, requires_safety_checker=True)`
  - `StableDiffusionControlNetImg2ImgPipeline(... same components ...)`
- **Multi-ControlNet behavior:** `controlnet` can be a single `ControlNetModel` or a list/tuple; **outputs from each ControlNet are added together** to form combined conditioning.
- **Key call parameters (text2img ControlNet):**  
  `__call__(prompt, image, height=None, width=None, num_inference_steps=50, guidance_scale=7.5, eta=0.0, ... controlnet_conditioning_scale=1.0, guess_mode=False, control_guidance_start=0.0, control_guidance_end=1.0, clip_skip=None, ...)`
- **Key call parameters (img2img ControlNet):** adds `image` (init image) + `control_image` (ControlNet condition), `strength=0.8`; default `controlnet_conditioning_scale=0.8`.
- **ControlNet scaling formula (API behavior):**  
  **Residual_added = Residual_unet + (controlnet_conditioning_scale × ControlNet_output)**  
  (`controlnet_conditioning_scale` can be `float` or `list[float]` matching multiple ControlNets).
- **Guess mode:** ControlNet encoder “recognizes content” even with prompts removed; recommended `guidance_scale` **3.0–5.0**.
- **Control guidance window:** `control_guidance_start/end` are **fractions of total steps** when ControlNet starts/stops applying; can be per-ControlNet lists.
- **Image input expectations:** `image`/`control_image` accept `PIL`, `np.ndarray`, `torch.Tensor`; if `height/width` provided, control image is resized; for multiple ControlNets, pass a **list** (or list-of-lists for batching per prompt).

## When to surface
Use when students ask how to wire ControlNet into Stable Diffusion in Diffusers, how multi-ControlNet inputs/scales combine, or what `guess_mode`, `control_guidance_start/end`, and image batching/resizing actually do.