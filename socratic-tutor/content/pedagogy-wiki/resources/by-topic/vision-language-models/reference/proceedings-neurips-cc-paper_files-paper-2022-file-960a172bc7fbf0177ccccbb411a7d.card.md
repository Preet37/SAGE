# Card: Flamingo supplement — few-shot benchmarks & ablations
**Source:** https://proceedings.neurips.cc/paper_files/paper/2022/file/960a172bc7fbf0177ccccbb411a7d800-Supplemental-Conference.pdf  
**Role:** benchmark | **Need:** EMPIRICAL_DATA  
**Anchor:** Supplemental benchmark tables + ablations for Flamingo (few-shot across tasks/scales; design choices like Perceiver Resampler, gated cross-attn, data mixture)

## Key Content
- **Autoregressive objective (Eq. 1):**  
  \(p(y|x)=\prod_{\ell=1}^{L} p(y_\ell \mid y_{<\ell}, x_{\le \ell})\)  
  where \(y_\ell\)=\(\ell\)-th text token; \(x_{\le \ell}\)=images/videos occurring before token \(\ell\) in the interleaved sequence.
- **Training loss (Eq. 2):** weighted multi-dataset NLL  
  \(\sum_{m=1}^{M}\lambda_m \, \mathbb{E}_{(x,y)\sim \mathcal{D}_m}\left[-\sum_{\ell=1}^{L}\log p(y_\ell|y_{<\ell},x_{\le \ell})\right]\).  
  Uses **gradient accumulation across datasets** (better than round-robin; Table 3 row (ii)).
- **Architecture defaults (Sec. 2):**
  - Frozen **NFNet-F6** vision encoder; frames at **1 FPS** for video.
  - **Perceiver Resampler** outputs **64 visual tokens** per image/video (Sec. 2.1).
  - Frozen pretrained LM (Chinchilla 1.4B/7B/70B → **Flamingo-3B/9B/80B**); insert **GATED XATTN-DENSE** blocks with **tanh gating** scalars \(\alpha\) init **0** (Fig. 4) for stability.
  - **Per-image causal masking**: each text token cross-attends only to the **most recent** image’s tokens (Sec. 2.3); enables >5 images at inference though trained with ≤5.
- **Data mixture (Sec. 2.4):** M3W interleaved webpages (**~43M** pages; sample **L=256** tokens, keep **N=5** images), plus ALIGN **1.8B** image-text, LTIP **312M** image-text, VTP **27M** video-text.
- **Key few-shot results (Table 1, 32 shots, Flamingo-80B):** OKVQA **57.8**, VQAv2 **67.6**, COCO **113.8** (CIDEr), VATEX **65.1** (CIDEr), VizWiz **49.8**, TextVQA **55.6**, HatefulMemes **37.9**, VisDial **86.8**, YouCook2 **45.3**, MSRVTTQA **75.4**.
- **Ablations (Table 3, Flamingo-3B, 4-shot DEV):**
  - Remove **M3W**: Overall **70.7 → 53.4** (largest drop).
  - No tanh gating: **70.7 → 66.5**.
  - Cross-attn frequency: every layer best; **every 4th** gives **70.7 → 68.8** with faster step time (**1.74s → 1.02s**).
  - Resampler: **Perceiver** best vs MLP/Transformer (Overall **70.7** vs **66.6/66.7**).
  - Vision encoder: NFNet-F6 beats CLIP ViT-L/14 (Overall **70.7 vs 64.9**).
  - Unfreezing LM hurts (catastrophic forgetting): fine-tune pretrained LM **70.7 → 62.7**; train from scratch **→ 57.8**.

## When to surface
Use for questions about **Flamingo’s few-shot benchmark numbers**, **what ablations mattered (data mixture, gating, resampler, freezing)**, or **how interleaved image-text training + per-image masking enables in-context multimodal prompting**.