# Card: MS-HAB baseline results + ablations for low-level home rearrangement
**Source:** https://proceedings.iclr.cc/paper_files/paper/2025/file/27aa3a0e6d63db269977bb2df5607cb8-Paper-Conference.pdf  
**Role:** benchmark | **Need:** EMPIRICAL_DATA  
**Anchor:** Benchmark tables: subtask success rates (RL/IL), per-object vs all-object ablations, trajectory labeling/filtering effects; simulator speed benchmark.

## Key Content
- **Simulation benchmark (Fig. 1, Sec. 4.2):** Interact benchmark @ 100Hz sim / 20Hz control, 2×128×128 RGB-D cams, RTX 4090 (24GB).  
  - Habitat peak: **1397.65 ± 11.02 SPS** at **22.60 GB** VRAM.  
  - MS-HAB peak: **4299.18 ± 26.36 SPS** at **15.35 GB** VRAM (**3.08× faster**, **32% less VRAM**) using **4096 envs**.
- **Subtask definitions & success formulas (App. A.2):**  
  - Distance: \(d_{ab}=\|a_{pos}-b_{pos}\|_2\) (m).  
  - Joint deviation: \(j_k=\max_i |q_{k,i}-r_{k,i}|\).  
  - Cumulative collision force \(C[0:t]\) (N).  
  - **Pick success:** \(1_{grasped}(x)\land d_{r,ee}\le0.05\land j_{arm}\le0.6\land 1_{static}\land C[0:t]\le5000\). Fail if \(C>5000\).  
  - **Place success:** \(\neg1_{grasped}(x)\land d_{g,x}\le0.15\land d_{r,ee}\le0.05\land j_{arm}\le0.2\land j_{tor}\le0.01\land 1_{static}\land C\le7500\).  
  - **Open/Close success:** articulation thresholds + \(d_{r,ee}\le0.05, j_{arm}\le0.2, j_{tor}\le0.01, 1_{static}, C\le10000\). Open fraction: **0.75 (fridge)**, **0.9 (drawer)**.
- **RL/IL baselines (Table 1, Sec. 6.1): success-once % (Train/Val)**  
  - TidyHouse Pick: **RL-per 81.75/77.48**, RL-all 71.63/68.15, IL 61.11/59.03.  
  - PrepareGroceries Pick: **RL-per 66.57/72.32**, RL-all 51.88/62.10.  
  - PrepareGroceries Place: **RL-per 60.22/65.67**, RL-all 53.37/58.63.  
  - Close Fridge: **Train 86.81**, **Val 0.00** (scene geometry blocks handle reach).
- **Per-object vs all-object rationale (Sec. 5.1, 6.2.1):** per-object Pick/Place overfits geometry → higher success esp. **many objects** or **tight tolerances** (fridge shelf).
- **Trajectory labeling ablation (Table 2/3, Sec. 6.2.2):** events: Contact, Grasped, Dropped, ExcessiveCollisions; filter “straightforward success” (no drop, low collisions).  
  - Pick Cracker Box (TidyHouse Train): RL-all **S-once 29.46%** vs RL-per **71.63%**; RL-all has higher collision/grasp failures.  
  - IL behavior control via filtering (PrepareGroceries Place): “place-only” dataset yields **Place:Drop 3.17:1** (train), “drop-only” yields **1:2.22**.

## When to surface
Use for questions about **benchmarking low-level contact-rich manipulation**, **baseline success rates**, **why per-object policies help**, **collision-force safety thresholds**, or **how trajectory labeling/filtering changes IL behavior**.