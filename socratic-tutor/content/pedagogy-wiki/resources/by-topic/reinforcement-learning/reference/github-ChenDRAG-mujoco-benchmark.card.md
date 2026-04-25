# Card: Tianshou MuJoCo Benchmark (SAC example + suite contents)
**Source:** https://github.com/ChenDRAG/mujoco-benchmark  
**Role:** benchmark | **Need:** EMPIRICAL_DATA  
**Anchor:** Concrete MuJoCo returns (mean±std) under a single Tianshou benchmark + links to scripts/data/pretrained agents.

## Key Content
- **What this repo is:** A pointer to **Tianshou’s maintained MuJoCo benchmark** (latest under `thu-ml/tianshou`, path: `examples/mujoco`). Provides **default hyperparameters + reproduction scripts**, **graphs + raw data**, **training logs**, **pretrained agents**, and **tuning hints** for supported algorithms/environments.
- **Benchmarked coverage:** “9 out of 13” environments from the **MuJoCo Gym task suite**.
- **Supported algorithms (listed):**
  - **REINFORCE** (Williams 1999) + referenced Tianshou commit id `e27b5a26...`
  - **Natural Policy Gradient (NPG)** (Kakade 2001) + commit id `844d7703...`
  - **A2C** (OpenAI baselines blog) + commit id `1730a900...`
  - Repo topics/description also mention **DDPG, TD3, SAC, PPO, PG, A2C**.
- **Empirical results (Example benchmark: SAC; average return ± std):**  
  - Ant: **5850.2 ± 475.7** (SpinningUp ~3980; SAC paper ~3720)  
  - HalfCheetah: **12138.8 ± 1049.3** (SpinningUp ~11520; paper ~10400)  
  - Hopper: **3542.2 ± 51.5** (SpinningUp ~3150; paper ~3370)  
  - Walker2d: **5007.0 ± 251.5** (SpinningUp ~4250; paper ~3740)  
  - Swimmer: **44.4 ± 0.5** (SpinningUp ~41.7)  
  - Humanoid: **5488.5 ± 81.2** (paper ~5200)  
  - Reacher: **-2.6 ± 0.2**  
  - InvertedPendulum: **1000.0 ± 0.0**  
  - InvertedDoublePendulum: **9359.5 ± 0.4**
- **Design rationale:** Standardized, single-codebase benchmarking with **comparisons to SpinningUp and original papers**, plus reproducibility artifacts (scripts/data/logs/agents).

## When to surface
Use when students ask for **actual MuJoCo learning performance numbers** (e.g., “What return does SAC get on Ant?”) or how to **reproduce standardized benchmarks** (scripts, defaults, logs, pretrained agents) across algorithms/environments.