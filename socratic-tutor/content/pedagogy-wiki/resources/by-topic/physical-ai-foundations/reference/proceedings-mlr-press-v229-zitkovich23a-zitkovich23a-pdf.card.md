# Card: RT-2 (Vision-Language-Action) — tokenized actions + co-fine-tuning boosts generalization
**Source:** https://proceedings.mlr.press/v229/zitkovich23a/zitkovich23a.pdf  
**Role:** paper | **Need:** EMPIRICAL_DATA  
**Anchor:** RT-2 evaluation results (success rates across seen/unseen + emergent skills) and ablations (model size, co-fine-tuning vs robot-only vs scratch)

## Key Content
- **Core idea (Sec. 3.2):** Train a pretrained VLM to output **robot actions as text tokens** (Vision-Language-Action / VLA).  
  - Action space: 6-DoF end-effector **Δposition (x,y,z)** + **Δrotation (x,y,z)** + **gripper extension** + **terminate**.
  - **Discretization:** all continuous dims discretized into **256 uniform bins** → action represented as **8 integer tokens**.
  - Output string format: `"terminate Δposx Δposy Δposz Δrotx Δroty Δrotz gripper"` (example token sequence shown in paper).
- **Token mapping:**  
  - **PaLI-X:** integers up to 1000 have unique tokens → map bins directly to integer tokens.  
  - **PaLM-E:** overwrite **256 least-frequent tokens** to serve as action vocabulary (“symbol tuning”).
- **Training procedure (Sec. 3.2):** **Co-fine-tune** on (a) robot trajectories + (b) original web VLM mixture (VQA/captioning/interleaved image-text). Increase robot sampling weight to balance batches.
- **Decoding constraint:** when prompted for robot action, **restrict output vocabulary** to valid action tokens only.
- **Real-time control (Sec. 3.3):** serve models via **cloud TPU**; RT-2-PaLI-X **55B runs ~1–3 Hz**, **5B runs ~5 Hz**.
- **Empirical results:**  
  - ~**6,000** real-robot evaluation trials total.  
  - Generalization: RT-2 models achieve **~2×** average improvement over next best baselines (RT-1, MOO) on unseen objects/backgrounds/environments; **~6×** over other baselines (Sec. 4.1, Fig. 4).  
  - Emergent skills: best RT-2 achieves **>3×** average success vs next best baseline (RT-1) across symbol understanding/reasoning/human recognition (Sec. 4.2, Fig. 6a).  
  - Ablations (Sec. 4.3, Fig. 6b): **training from scratch performs poorly**; **co-fine-tuning > robot-only fine-tuning**; **55B > 5B** for generalization.
- **Language-Table sim benchmark (Table 1):** RT-2-PaLI-3B **90 ± 10** vs BC-Zero **72 ± 3**, RT-1 **74 ± 13**, LAVA **77 ± 4**.

## When to surface
Use when students ask how VLM knowledge transfers to robot control, what “tokenized actions” means, or for concrete success-rate comparisons/ablations showing why **co-fine-tuning** and **larger models** improve robotic generalization and emergent semantic reasoning.