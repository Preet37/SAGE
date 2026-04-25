# Image Generation

## Video (best)
- **Two Minute Papers** — "DALL·E 2 Explained!"
- youtube_id: qTgPSKKjfVg
- Why: Clear, accessible overview of modern text-to-image diffusion-style generation and what “prompted image synthesis” is doing at a high level.
- Level: Beginner → Intermediate

## Blog / Written explainer (best)
- **Lil’Log (Lilian Weng)** — "What are Diffusion Models?"
- Why: One of the clearest written explanations of diffusion models (the backbone of many text-to-image systems), with intuition + math + references.
- Level: Intermediate

## Deep dive
- **Hugging Face (Documentation / Course-style guides)** — "Diffusion models" (Stable Diffusion & related concepts)
- Why: Practical, implementation-oriented deep dive into diffusion pipelines (text-to-image, img2img, inpainting/outpainting) and common components.
- Level: Intermediate → Advanced  
- url: https://huggingface.co/docs/diffusers/index

## Original paper
- **Ho, Jain, Abbeel (2020)** — "Denoising Diffusion Probabilistic Models"
- Why: Foundational diffusion model paper that underpins many modern image generation systems.
- Level: Advanced  
- url: https://arxiv.org/abs/2006.11239

## Code walkthrough
- **Hugging Face Diffusers** — Example scripts / pipelines (text-to-image, img2img, inpainting)
- Why: Widely used reference implementation; easy to map concepts (scheduler, UNet, VAE, conditioning) to working code.
- Level: Intermediate  
- url: https://github.com/huggingface/diffusers

## Coverage notes
- Strong: diffusion fundamentals; text-to-image basics; practical pipelines (text-to-image, img2img, inpainting) via Diffusers; foundational DDPM paper.
- Weak: model-specific coverage for **DALL·E 3**, **Midjourney**, **Imagen**, **FLUX** (often proprietary and not fully documented publicly); **IP-Adapter** specifics; **aesthetic scoring** as a control signal.
- Gap: a single, authoritative educator resource that compares major proprietary systems (DALL·E 3 vs Midjourney vs Imagen vs FLUX) with reproducible technical detail; a best-in-class walkthrough focused specifically on **IP-Adapter** and modern conditioning/control stacks.

## Last Verified
2026-04-09