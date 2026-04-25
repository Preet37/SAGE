# Card: Isaac Gym end-to-end GPU RL pipeline + speedups
**Source:** https://datasets-benchmarks-proceedings.neurips.cc/paper/2021/file/28dd2c7955ce926456240b2ff0100bde-Paper-round2.pdf  
**Role:** paper | **Need:** DEPLOYMENT_CASE  
**Anchor:** End-to-end GPU pipeline (PhysX buffers exposed as PyTorch tensors) + reported 100–1000× (2–3 orders) speedups vs CPU-sim RL stacks.

## Key Content
- **Design pattern (Fig. 2, Abstract, Sec. 1–2):** Physics simulation + policy training both on GPU; **Tensor API** wraps **physics buffers as PyTorch tensors** so observations/rewards/actions move **GPU→GPU** (no CPU copies). Addresses prior GPU-sim bottleneck where state was copied back to CPU for obs/reward then back to GPU.
- **Parallelism workflow (Sec. 2, 5):**
  1) Duplicate environment **N times** (thousands) with optional per-copy variation (domain randomization).  
  2) Step PhysX on GPU; read state tensors; compute obs/reward/non-physics logic in Python using tensors; run PPO; write action tensors back to simulator.
  3) For scaling studies, keep total experience roughly constant by **decreasing PPO horizon length proportionally** as N increases.
- **Physics backend (Sec. 3):** NVIDIA **PhysX** reduced-coordinate articulations; **Temporal Gauss Seidel (TGS)** solver.
- **Empirical speed/throughput (A100, single GPU unless noted):**
  - Claim: **100×–1000× overall RL training speedup** (Fig. 2); **2–3 orders of magnitude** vs conventional CPU-sim + GPU NN (Abstract).
  - **Ant:** performant locomotion at reward ~3000 in **20 s**; fully converge **<2 min**; peak ~**700K env steps/s**; best at **8192 envs, horizon 16** (Sec. 5.1, 6.1).
  - **Humanoid:** reward threshold 5000 in **<4 min**; best at **4096 envs, horizon 32**; ~**200K env steps/s** (Sec. 5.2, 6.1).
  - **Shadow Hand (standard):** 10 consecutive successes in **~5 min**; 20 consecutive successes **<35 min** (Sec. 5.3, 6.4.1).
  - **OpenAI Shadow Hand reproduction:** >20 consecutive successes **<1 hr** (FF); **40** successes **within 3 hr** (LSTM seq len **4**). Compared to OpenAI setup: **30 hr** (FF) and **~20 hr** (LSTM) using **384×16-core CPUs (6144 cores) + 8×V100** with MuJoCo (Sec. 6.4.1).
  - **AMP humanoid animation:** ~**39M samples** in **~6 min** with **4096 envs** vs **~30 hr** on **16 CPU cores** in PyBullet ⇒ **~300× (2.48 orders)** faster (Sec. 6.2).
  - **Franka cube stacking:** converge **<25 min** using **16384 envs** with **Operational Space Control (OSC)** actions (Sec. 6.3).
  - **ANYmal:** flat terrain train **<2 min** with **4096 envs**; rough-terrain sim-to-real train+transfer **<20 min** with pushes, noise, friction randomization, actuator network, curriculum (Sec. 6.1).
- **Default sim/control dts (Table 1):**  
  Ant sim dt **1/120 s**, control dt **1/60 s**, action dim **8**; Humanoid **1/120**, **1/60**, **21**; ANYmal **1/200**, **1/50**, **12**; Shadow Hand standard **1/120**, **1/60**, **20**; Shadow Hand OpenAI **1/120**, **1/20**, **20**; TriFinger **1/200**, **1/50**, **9**; Allegro **1/120**, **1/20**, **16**; Franka **1/60**, **1/60**, **7**.
- **Limitations (Sec. 7):** Biggest gains require **thousands** of parallel envs; some nondeterminism from GPU scheduling when randomizing **scale/mass at runtime**—they randomize these at startup, not at reset; tensor API cannot add new actors to a running sim.

## When to surface
Use when students ask how to eliminate CPU↔GPU bottlenecks in RL simulation/training, how massive parallel simulation changes training time, or want concrete speedup/throughput numbers comparing GPU end-to-end pipelines vs CPU-based simulators (e.g., MuJoCo/PyBullet stacks).