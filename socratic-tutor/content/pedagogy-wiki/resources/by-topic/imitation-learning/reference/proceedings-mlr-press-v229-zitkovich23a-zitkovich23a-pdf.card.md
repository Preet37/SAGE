# Card: RT-2 VLA empirical eval + co-finetuning recipe
**Source:** https://proceedings.mlr.press/v229/zitkovich23a/zitkovich23a.pdf  
**Role:** benchmark | **Need:** EMPIRICAL_DATA  
**Anchor:** ~6k-trial evaluation; generalization + emergent instruction/object reasoning; RT-2 variants vs baselines with success rates

## Key Content
- **Core idea (Sec. 3):** Train a pretrained vision-language model to output **robot actions as text tokens** (Vision-Language-Action / VLA).
- **Action encoding (Sec. 3.2):**
  - Action space: 6-DoF end-effector displacement + gripper extension + **terminate**.
  - Continuous dims discretized into **256 uniform bins**; action represented as **8 integer tokens**.
  - Output string format:  
    **“terminate Δposx Δposy Δposz Δrotx Δroty Δrotz gripper”**  
    Example: “1 128 91 241 5 101 127 …” (integers are token IDs/bins).
- **Tokenization choices (Sec. 3.2):**
  - **PaLI-X:** integers up to 1000 have unique tokens → map bins directly to integer tokens.
  - **PaLM-E:** overwrite **256 least-frequent tokens** to serve as action vocabulary (“symbol tuning”).
- **Training procedure (Sec. 3.2):**
  - Prompt as VQA-style: **“Q: what action should the robot take to [instruction]? A:”**
  - **Co-fine-tuning** on (robot trajectories + original web VLM data) with **upweighted robot sampling** improves generalization vs robot-only finetune (reduces forgetting).
  - **Output constraint:** during robot-action decoding, restrict vocabulary to valid action tokens.
- **Inference (Sec. 3.3):** Cloud TPU serving for real-time control. **55B** model runs **1–3 Hz**; **5B** runs **~5 Hz**.
- **Empirical results (Sec. 4):**
  - **~6,000 real-robot evaluation trajectories** across seen tasks + generalization (unseen objects/backgrounds/environments).
  - RT-2 generalization: **~2×** improvement over next best baselines (RT-1, MOO) on average; **~6×** over other baselines (e.g., VC-1/R3M variants).
  - Emergent skills A/B tests: best RT-2 achieves **>3×** average success vs **RT-1** across **symbol understanding, reasoning, human recognition**.
  - Language-Table sim (Table 1): **RT-2-PaLI-3B 90±10** vs **BC-Zero 72±3**, **RT-1 74±13**, **LAVA 77±4**.

## When to surface
Use for questions about imitation-learning-style behavior cloning with distribution shift, why co-training with web VLM data helps generalization, and concrete success-rate comparisons between RT-2 variants and baselines.