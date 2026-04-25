# Card: Diffusers Stable Diffusion Pipelines — loading, inference, schedulers
**Source:** https://huggingface.co/docs/diffusers/api/pipelines/stable_diffusion/stable_diffusion  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Exact pipeline composition + canonical `from_pretrained` / `__call__` inference workflow; scheduler swapping; seed/generator usage; SDXL base+refiner latent handoff (`output_type="latent"`, `denoising_start/end`).

## Key Content
- **Pipeline components (Stable Diffusion family):** Autoencoder (VAE), conditional UNet, CLIP text encoder, **scheduler**, CLIPImageProcessor, **safety checker**. Pipelines are **inference-only** (no training functionality).
- **Loading workflow (`from_pretrained`):**
  - Accepts HF Hub repo id (e.g., `"stable-diffusion-v1-5/stable-diffusion-v1-5"`) or local path (`"./stable-diffusion"`).
  - Uses `model_index.json` mapping: `<name>: ["<library>", "<class name>"]` to know which components to load.
  - `save_pretrained(path)` saves each component under `path/<component_name>/` and writes `model_index.json` at root.
- **Inference entrypoint:** pipeline `__call__` encapsulates preprocessing → diffusion loop → postprocessing; API varies by pipeline (text2img vs img2img vs inpaint).
- **Reproducibility / seed:** pass a Torch generator, e.g. `generator=torch.manual_seed(seed)` (example seed: `42`).
- **Scheduler swapping (procedure):**
  - `pipeline.scheduler = EulerDiscreteScheduler.from_config(pipeline.scheduler.config)` (example swap from `PNDMScheduler` to `EulerDiscreteScheduler`).
- **Empirical/model detail:** SD 2.1 commonly generates **768×768**; SD 1.5 **512×512** (as stated in examples narrative).
- **SDXL base→refiner two-stage (procedure + params):**
  - Base call: `denoising_end=high_noise_frac` and `output_type="latent"`.
  - Refiner call: `denoising_start=high_noise_frac`, `image=latent_image`.
  - Example values: `n_steps=40`, `high_noise_frac=0.8`.
- **SDXL defaults/flags:** `force_zeros_for_empty_prompt: bool = True` (default). `add_watermarker` defaults to True if `invisible_watermark` installed.

## When to surface
Use when students ask how to correctly load/save Stable Diffusion pipelines, set seeds/generators for reproducibility, swap schedulers, or run SDXL base+refiner with latent handoff and `denoising_start/end` / `output_type`.