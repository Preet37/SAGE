# Card: Octo — Transformer-first Diffusion Generalist Robot Policy
**Source:** https://octo-models.github.io/paper.pdf  
**Role:** paper | **Need:** CONCEPT_EXPLAINER  
**Anchor:** Concrete Octo architecture + training pipeline on Open X-Embodiment (inputs/outputs, tokenization, diffusion decoding, finetuning recipe, scale: ~800k episodes)

## Key Content
- **Scale & checkpoints:** Pretrained on **800k robot trajectories** (Open X-Embodiment subset of **25 datasets**). Released models: **Octo-Small 27M params**, **Octo-Base ~86–93M params** (Table 4; text also states 93M).
- **Inputs → tokens (Section 2.1):**
  - Language: tokenize + **T5-base (111M)** → **16 language embedding tokens**.
  - Images (observations + goals): shallow CNN → **16×16 patches** → tokens (**256 tokens** for 256×256 3rd-person; **64 tokens** for 128×128 wrist).
  - Sequence assembled with learnable positional embeddings; supports **multi-camera**, **history**, **language or goal image**.
- **Transformer backbone (Section 2.1):** **block-wise masked attention**: observation tokens attend causally to same/earlier timesteps + task tokens; missing modalities fully masked. Learned **readout tokens** attend to prior tokens but are not attended to (enables modular add/remove I/O).
- **Diffusion action decoding (Eq. 1, Section 3):** sample \(x_K\sim\mathcal N(0,I)\); denoise with \(\epsilon_\theta(x_k,e,k)\) conditioned on transformer readout embedding \(e\) and step \(k\):  
  **Eq. 1:** \(x_{k-1}=\alpha\big(x_k-\gamma\,\epsilon_\theta(x_k,e,k)+\mathcal N(0,\sigma^2 I)\big)\).  
  Uses **DDPM objective** (Ho et al. 2020) + **cosine noise schedule** (Nichol & Dhariwal 2021); **20 diffusion steps** train/infer; only **one transformer forward pass** per action (denoising in small head).
- **Training recipe (Section 3 / App. D):** AdamW, **LR 3e-4**, **warmup 2000**, **inverse-sqrt LR decay**, **weight decay 0.1**, **grad clip 1.0**, **batch 2048**. ViT-B-sized model trained **300k steps** on **TPU v4-128** in **14 hours**.
- **Finetuning (Section 3/5):** ~**100 trajectories**, **50k steps**, cosine LR decay + linear warmup; **update full model** (better than head-only). **~5 hours** on **single NVIDIA A5000 24GB**.
- **Data/conditioning tricks:** remove datasets w/o images or w/o **delta end-effector control**; **zero-pad missing cameras**; align gripper so **+1=open, 0=closed**. Use **hindsight goal relabeling** (random future obs). Randomly **drop language or goal** per example; if no language, use goal images.
- **Empirical results:**
  - **Zero-shot:** Octo averages **33% higher success** than **RT-1-X (35M)** across tested robots; goal-image conditioning on WidowX gave **+25%** success vs language.
  - **Finetuning success (Table 1):** ResNet+Transformer scratch **avg 20%**; VC-1 **avg 9%**; **Octo avg 64%** (CMU Baking 50%, Stanford Coffee 75%, Berkeley Peg Insert 70% (new force-torque obs), Berkeley Pick-up 60% (new joint-position action space)).
- **Design rationale (Section 2.2 / App. E):**
  - “**Transformer-first**” (shallow CNN, big transformer) > deep ResNet encoders at scale.
  - **Early fusion** for goal images: channel-stack goal with observation before patching (compute vs token length tradeoff).
  - ImageNet-pretrained ResNets gave **no improvement**; diffusion head beats MSE/discrete heads (MSE “hedging” slow actions).

## When to surface
Use for questions about **how Octo/RT-X-style generalist robot policies are built/trained**, especially **tokenization, modular transformer masking/readouts, diffusion action decoding**, and **practical finetuning hyperparameters + performance numbers**.