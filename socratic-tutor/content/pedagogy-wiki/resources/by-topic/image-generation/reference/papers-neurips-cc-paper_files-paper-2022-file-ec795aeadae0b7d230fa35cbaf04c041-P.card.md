# Card: Imagen—T5 text encoder scaling + cascaded diffusion + dynamic thresholding
**Source:** https://papers.neurips.cc/paper_files/paper/2022/file/ec795aeadae0b7d230fa35cbaf04c041-Paper-Conference.pdf  
**Role:** paper | **Need:** CONCEPT_EXPLAINER  
**Anchor:** Imagen design choice/rationale: frozen large text-only LM (T5) as encoder; scaling text encoder improves alignment/fidelity more than scaling diffusion U-Net; end-to-end cascade (64→256→1024) diffusion pipeline.

## Key Content
- **Core finding (Abstract, Sec. 2.1, 4.4):** Large **frozen** text-only LMs (e.g., **T5-XXL, 4.6B params**) are “surprisingly effective” text encoders; **scaling text encoder size improves fidelity + image-text alignment more than scaling U-Net** (Fig. 4a vs 4b). Human raters prefer **T5-XXL over CLIP** on challenging prompts (DrawBench), even if COCO metrics are similar.
- **Pipeline (Intro, Sec. 2.4):** Frozen T5 encoder → **base 64×64 text-conditional diffusion** → **two text-conditional super-resolution diffusion models**: **64→256** then **256→1024**. Uses **classifier-free guidance** and **noise conditioning augmentation** in SR stages (aug_level ∈ **[0,1]**; Gaussian noise); during inference **sweep aug_level** for best quality.
- **Diffusion training objective (Eq. 1, Sec. 2.2):**  
  \[
  \mathbb{E}_{x,c,\epsilon,t}\big[w_t\|\hat x_\theta(\alpha_t x+\sigma_t\epsilon, c)-x\|_2^2\big]
  \]
  where \(t\sim U([0,1])\), \(\epsilon\sim\mathcal N(0,I)\), \(z_t=\alpha_t x+\sigma_t\epsilon\), \(c\)=conditioning (text).
- **Classifier-free guidance (Eq. 2):** drop conditioning during training with **10% probability**; sampling uses  
  \[
  \tilde\epsilon_\theta(z_t,c)=w\,\epsilon_\theta(z_t,c)+(1-w)\epsilon_\theta(z_t)
  \]
  \(w\)=guidance weight (>1 strengthens conditioning).
- **Dynamic thresholding (Sec. 2.3):** high guidance causes \(\hat x_t\) to exceed **[-1,1]**; dynamic thresholding sets \(s\)=percentile(|\(\hat x_t\)|); if \(s>1\), clip to **[-s,s]** then divide by \(s\). Improves photorealism/alignment at large \(w\) (Fig. 4c).
- **Key results (Tables 1–2):** **COCO zero-shot FID-30K = 7.27** (Imagen) vs **GLIDE 12.24**, **DALL·E 2 10.39**, **Make-A-Scene 7.55**. Human eval (COCO): alignment **91.4±0.44** vs original **91.9±0.42**; photorealism preference **39.5±0.75%** (no-people subset: **43.9±1.01%**).
- **Training defaults (Sec. 4.1):** base model **2B params**; SR models **600M** and **400M**; batch **2048**; **2.5M steps**; base guidance **1.35**, SR guidance **8.0**; 256 TPU-v4 (base), 128 TPU-v4 (SR). Data: ~**460M** internal + **LAION-400M**.

## When to surface
Use for questions about why Imagen uses a **large frozen T5** text encoder (vs CLIP), how **text-encoder scaling** affects alignment/fidelity, and how **cascaded diffusion + classifier-free guidance + dynamic thresholding** enables high-res photorealistic generation.