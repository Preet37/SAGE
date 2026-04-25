# Card: RT-1 empirical results + evaluation/protocol snapshot
**Source:** https://robotics-transformer1.github.io  
**Role:** benchmark | **Need:** EMPIRICAL_DATA  
**Anchor:** Centralized access to reported success-rate numbers, dataset scale, and evaluation setup highlights

## Key Content
- **Model I/O + control loop (procedure/defaults):**
  - Input: **short sequence of images** + **natural-language task description**.
  - Output each step: **discretized action tokens** for robot control.
  - **Action space:** 7D arm (x, y, z, roll, pitch, yaw, gripper open/close) + 3D base (x, y, yaw) + **1 discrete mode** (arm vs base vs terminate).
  - **Closed-loop control at 3 Hz** until **terminate** action or max steps reached.
- **Architecture (design choices):**
  - Images + text processed by **ImageNet-pretrained EfficientNet**, **FiLM-conditioned** on a pretrained instruction embedding (to make visual features task-relevant).
  - **Token Learner** compresses visual features into a compact token set; then a **Transformer** attends over tokens to predict action tokens (scalable “data-absorbent” design).
- **Dataset scale (empirical context):**
  - **>130k episodes**, **>700 tasks**, collected over **17 months** using a fleet of **13 robots**.
  - Skills include: picking/placing; opening/closing drawers; in/out of drawers; placing elongated items upright; knocking over; pulling napkins; opening jars.
- **Reported success rates (key empirical results):**
  - **Seen tasks:** RT-1 **97%** success over 700+ instructions (**+25% vs BC-Z**, **+32% vs Gato**).
  - **Unseen instructions:** RT-1 **76%** success (**+24% vs next best baseline**).
  - **Robustness:** distractors **83%** (**+36% vs next best**); new backgrounds/environments **59%** (**+18% vs next best**).
  - **SayCan integration:** RT-1 achieves **67% execution success in Kitchen1**; baselines (SayCan+Gato, SayCan+BC-Z) drop sharply in harder unseen kitchen while RT-1 shows no visible drop.
- **Cross-domain data mixing (transfer):**
  - Mixing real+sim improves performance on **sim-only objects** with only **~2% drop** on other objects.
  - Adding **Kuka IIWA** bin-picking data improves accuracy **22% → 39%** (**+17%**, ~2×).

## When to surface
Use for questions about **RT-1 dataset scale**, **action/control details (3 Hz, terminate mode)**, and **specific success-rate comparisons** (seen vs unseen tasks, distractors/backgrounds, kitchen generalization, sim/other-robot transfer).