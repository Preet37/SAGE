---
title: "Physics Simulation"
subject: "Physical AI & Robotics"
date: 2025-01-15
tags:
  - "subject/physical-ai-and-robotics"
  - "level/intermediate"
  - "level/advanced"
  - "educator/yannic-kilcher"
  - "educator/lilian-weng"
  - "resource/video"
  - "resource/blog"
  - "resource/deep-dive"
  - "resource/paper"
  - "resource/code"
educators:
  - "Yannic Kilcher"
  - "Lilian Weng"
levels:
  - "intermediate"
  - "advanced"
resources:
  - "video"
  - "blog"
  - "deep-dive"
  - "paper"
  - "code"
---

# Physics Simulation

## Video (best)
- **Two Minute Papers** — "OpenAI Trains a Hand to Solve a Rubik's Cube"
- **Link:** [https://openai.com/research/solving-rubiks-cube](https://openai.com/research/solving-rubiks-cube)
- Why: No single YouTube video cleanly covers the full scope of physics simulation for robotics/AI (domain randomization, MuJoCo, Isaac Sim, parallel simulation together). Two Minute Papers covers adjacent results but not the pedagogical fundamentals.
- Level: intermediate

> **Note:** No excellent dedicated explainer video exists on YouTube that covers physics simulation for Physical AI as a unified topic. The closest candidates are NVIDIA GTC talks (not on YouTube in standard form) and scattered robotics lectures.

**Partial alternative:**
- **Yannic Kilcher** — covers RT-X and foundation model papers but not simulation infrastructure
- **Stanford CS329L / CS336** lectures touch on sim-to-real but are not cleanly indexed as standalone YouTube videos

## Blog / Written explainer (best)
- **Lilian Weng** — "Domain Randomization for Sim-to-Real Transfer"
- **Link:** [https://lilianweng.github.io/posts/2019-05-05-domain-randomization/](https://lilianweng.github.io/posts/2019-05-05-domain-randomization/)
- Why: Weng's post is the most cited, pedagogically structured written explainer on domain randomization — the core technique linking physics simulation to real-world robot learning. It covers the motivation, taxonomy (uniform vs. structured randomization), and key results with clear diagrams. Directly relevant to MuJoCo/Isaac Sim workflows.
- Level: intermediate

## Deep dive
- **MuJoCo Documentation & Technical Reference** — DeepMind/Google
- **Link:** [https://mujoco.readthedocs.io/en/stable/overview.html](https://mujoco.readthedocs.io/en/stable/overview.html)
- Why: The official MuJoCo docs are the most comprehensive technical reference for physics simulation in AI/ML robotics contexts. They cover rigid body dynamics, contact modeling, actuator models, and integration with Python/RL frameworks. MuJoCo is the de facto standard simulator for the concepts in this topic cluster (Octo, RT-X, and most foundation model robot training use it).
- Level: advanced

## Original paper
- **Todorov et al. (2012)** — "MuJoCo: A physics engine for model-based control"
- **Link:** [https://homes.cs.washington.edu/~todorov/papers/TodorovIROS12.pdf](https://homes.cs.washington.edu/~todorov/papers/TodorovIROS12.pdf)
- Why: MuJoCo is the foundational simulator underpinning the majority of modern robot learning research. This paper introduces the core design philosophy — fast, differentiable, contact-rich simulation — that makes it suitable for RL and imitation learning at scale. Readable and concise (~6 pages).
- Level: advanced

**Honorable mention for domain randomization:**
- Tobin et al. (2017) "Domain Randomization for Transferring Deep Neural Networks from Simulation to the Real World"
- **Link:** [https://arxiv.org/abs/1703.06907](https://arxiv.org/abs/1703.06907)
- Why: The seminal paper establishing domain randomization as a practical sim-to-real technique.

## Code walkthrough
- **NVIDIA Isaac Lab Tutorials** — Official hands-on implementation notebooks
- **Link:** [https://isaac-sim.github.io/IsaacLab/main/source/tutorials/index.html](https://isaac-sim.github.io/IsaacLab/main/source/tutorials/index.html)
- Why: Isaac Lab (built on Isaac Sim) provides the most complete code walkthrough for modern GPU-accelerated parallel simulation, directly covering concepts like domain randomization, rigid body dynamics, and integration with robot learning pipelines. The tutorials progress from environment setup through RL training with domain randomization — matching the topic's concept list most completely.
- Level: intermediate/advanced

**Alternative for MuJoCo specifically:**
- DeepMind MuJoCo Colab tutorials: https://github.com/google-deepmind/mujoco/tree/main/python/tutorial [NOT VERIFIED]

---

## Coverage notes
- **Strong:** Domain randomization (Lilian Weng blog is excellent), MuJoCo fundamentals (official docs + paper), Isaac Sim code (official tutorials)
- **Weak:** NVIDIA GR00T and Octo-specific simulation pipelines — these are very new (2024) and pedagogical resources lag behind
- **Gap:** No high-quality YouTube video exists that unifies physics simulation + domain randomization + parallel GPU simulation + foundation model robotics as a single explainer. This is a genuine content gap in the public AI education ecosystem as of early 2025.
- **Gap:** Photorealistic rendering for sim-to-real (NeRF/Gaussian Splatting in simulation loops) has almost no dedicated pedagogical coverage yet.
- **Gap:** RT-X dataset and its relationship to simulation is covered in the paper but not in accessible tutorial form.

---

## Additional Resources for Tutor Depth

> **8 sources** — papers, official docs, working code, benchmarks, and deep explainers that give the AI tutor precision on this topic.

### 📄 Isaac Gym end-to-end GPU RL pipeline + speedups
**Paper** · [source](https://datasets-benchmarks-proceedings.neurips.cc/paper/2021/file/28dd2c7955ce926456240b2ff0100bde-Paper-round2.pdf)

*End-to-end GPU pipeline (PhysX buffers exposed as PyTorch tensors) + reported 100–1000× (2–3 orders) speedups vs CPU-sim RL stacks.*

<details>
<summary>Key content</summary>

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

</details>

### 📄 Nine Physics Engines for RL — comparison & performance takeaways
**Paper** · [source](https://arxiv.org/html/2407.08590v1)

*Structured comparison of 9 engines for RL (features/usability, MARL readiness, performance notes, popularity/citations, and evaluation criteria).*

<details>
<summary>Key content</summary>

- **Engines reviewed (9):** Brax, Chrono, Gazebo, MuJoCo, ODE, PhysX (via IsaacGym/IsaacSim), PyBullet, Webots, Unity (Sec. I).
- **Methodology (Sec. II):**
  - Popularity = citation counts (overall + ML-related) as of **2023-09-06**.
  - Feature analysis from docs + publications + prior reviews.
  - **Comparison criteria (14):** open source, documentation, community resources, model library/creation, environment library/creation, sensors, gym wrapper, rigid body dynamics, multi-joint dynamics, file formats (URDF/MJCF), visualization, performance.
- **Popularity table (Sec. III-A; citations):**
  - **MuJoCo:** 3827 total / **3541 ML** (since 2012)
  - **Gazebo:** 2698 / **1948 ML** (since 2004)
  - **PyBullet:** 1308 / **1000+ ML** (since 2016)
  - **Webots:** 988 / 548 ML (since 2004)
  - **Unity:** 576 / 528 ML (since 2018)
  - **ODE:** 1573 / 143 ML (since 2004)
  - **PhysX:** 310 / 288 ML (since 2021)
  - **Chrono:** 170 / 104 ML (since 2016)
  - **Brax:** 166 / 151 ML (since 2021)
- **Performance findings (Sec. IV):**
  - Prior comparison (Erez et al. 2015) found **MuJoCo best** on speed/stability/accuracy vs Bullet, ODE, PhysX, especially for **many-joint/connected-body** scenarios.
  - Cross-engine generalization study: agents trained in **MuJoCo transferred** to other engines; **PyBullet-trained agents did not transfer**.
  - RTF comparison (MuJoCo/PyBullet/Gazebo/Webots): **MuJoCo high RTF** (some accuracy cost); **PyBullet lower RTF** but better usability; **Webots high stability/RTF** but lacks native parallelization; **Gazebo** unwieldy, better for sim-to-real.
- **Design rationale / selection guidance (Sec. VI):**
  - **MuJoCo**: dominant for RL due to performance/flexibility; environment creation can be strenuous; dm_control usability issues.
  - **Unity**: easiest environment design + ML-Agents assets, but **poor scalability/parallel throughput**; fidelity can degrade as complexity rises.
  - **GPU sim (IsaacGym/Brax):** can boost throughput, but may compete with GPU needed for learning; Brax reported to scale poorly for complex MARL.

</details>

### 📄 Octo — Transformer-first Diffusion Generalist Robot Policy
**Paper** · [source](https://octo-models.github.io/paper.pdf)

*Concrete Octo architecture + training pipeline on Open X-Embodiment (inputs/outputs, tokenization, diffusion decoding, finetuning recipe, scale: ~800k episodes)*

<details>
<summary>Key content</summary>

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

</details>

### 📄 Open X-Embodiment (OXE) + RT‑X (RT‑1‑X / RT‑2‑X) design
**Paper** · [source](https://arxiv.org/abs/2310.08864)

*Standardized Open X‑Embodiment data format + RT‑X model design (obs/action reps, conditioning, multi-dataset mixture training)*

<details>
<summary>Key content</summary>

- **Dataset (Sec. III-A):** Open X‑Embodiment Dataset aggregates **60 existing robot datasets** into **1M+ real robot trajectories** spanning multiple embodiments (single arms, bimanual, quadrupeds). Converted to **RLDS** format (serialized **TFRecord**), supports heterogeneous modalities (multiple RGB cams, depth, point clouds) and **efficient parallelized loading** across major DL frameworks.
- **Observation/action consolidation (Sec. IV-A):**
  - Input: **history of recent images + natural-language instruction**.
  - Output: **7‑D end-effector action**: \((x,y,z,\text{roll},\text{pitch},\text{yaw},\text{gripper})\) (or rates). One canonical camera view per dataset; images resized to common resolution.
  - Actions **normalized per-dataset before discretization**; at inference, outputs are **de-normalized per embodiment**.
  - **Not aligned:** camera poses/properties vary; **coordinate frames not aligned**; actions may be absolute/relative positions/velocities → same 7‑vector can cause different motions across robots.
- **Action tokenization (Sec. IV-B):** actions discretized into **256 bins** along **8 dimensions** = **7 action dims + 1 terminate-episode dim**.
- **RT‑1 architecture (Sec. IV-B):** **35M params**; ImageNet‑pretrained **EfficientNet** for images; language → **USE embedding**; vision+language fused via **FiLM** producing **81 vision-language tokens**; decoder-only Transformer outputs tokenized actions.
- **RT‑2 architecture (Sec. IV-B):** VLA model; casts action tokens as **text tokens** (example: `"1 128 91 241 5 101 127"`). Variant used: **RT‑2‑PaLI‑X** (ViT + UL2), pretrained mainly on **WebLI**.
- **Training/inference (Sec. IV-C):**
  - Loss: **categorical cross-entropy** over discrete outputs (RT‑1 buckets; RT‑2 language tokens).
  - **Robotics mixture datasets:** RT‑1, QT‑Opt, Bridge, Task Agnostic Robot Play, Jaco Play, Cable Routing, RoboTurk, NYU VINN, Austin VIOLA, Berkeley Autolab UR5, TOTO, Language Table.
  - **RT‑1‑X:** trained on robotics mixture only. **RT‑2‑X:** **co-fine-tuning** with ~**1:1** split between original VLM data and robotics mixture.
  - Inference rate: **3–10 Hz**; RT‑1 local, RT‑2 via **cloud**.
- **Key empirical results (Sec. V):**
  - Small-scale domains: **RT‑1‑X beats “Original Method” on 4/5 datasets** (Kitchen Manipulation, Cable Routing, NYU Door Opening, Autolab UR5, Robot Play).
  - Large-scale domains: **RT‑1‑X does not beat** RT‑1 trained only on embodiment-specific data (underfitting); **RT‑2‑X outperforms** both Original Method and RT‑1 (needs higher capacity).
  - Emergent skills (Google Robot; skills from Bridge/WidowX): **RT‑2‑X 75.8% vs RT‑2 62%** success (Table II). Removing Bridge data **significantly reduces** emergent-skill performance.
  - Ablations (Table II): adding **short image history** improves generalization (row (4) vs (5)); **web pretraining critical** (row (4) vs (6)); higher capacity improves transfer (55B > 5B).

</details>

### 📄 Robust visual sim-to-real via domain randomization + proxy tuning
**Paper** · [source](https://arxiv.org/pdf/2307.15320.pdf)

*Quantitative sim-to-real manipulation results + DR ablations; proxy task for selecting DR parameters.*

<details>
<summary>Key content</summary>

- **Policy + loss (Eq. 1, Sec. III-A):** Learn closed-loop visuomotor policy \(\pi_\theta(a_t|o_t)\). Action \(a_t=(v_t,\omega_t,g_t)\) with \(v_t\in\mathbb{R}^3\) linear vel, \(\omega_t\in\mathbb{R}^3\) angular vel, \(g_t\in\{0,1\}\) gripper open/close. Train by behavior cloning:  
  \[
  L=\lambda L_{\text{MSE}}((\hat v_t,\hat\omega_t),(v_t,\omega_t))+(1-\lambda)L_{\text{BCE}}(\hat g_t,g_t)
  \]
  with \(\lambda=0.8\).
- **Architecture (Fig. 2):** Two RGB cameras (90° baseline). Input: last 3 frames per view + last 3 proprioceptive values \(P_t=[pos_t,\sin\phi_t,\cos\phi_t]\). ResNet-18 per view → 512-d each; concat + MLP (2 layers, 512 hidden, ReLU).
- **DR components + tuned defaults (Sec. III-B, V-D):**
  - Textures: randomize robot/table/wall/floor (not objects). AmbientCG (1203 textures) >> procedural.
  - Lighting: sample light position on sphere: distance [1,3] m; azimuth [0, \(\pi/2\)]; polar [\(\pi/10\), \(4\pi/10\)]. Randomize diffuse/specular/ambient around 0.3 with offset in \([-0.6,0.6]\).
  - Object color: HSV offsets best at \(\phi_o=(0.05,0.1,0.1)\) (too large confuses colors).
  - Camera: position \(\pm10\) cm; angle \(\pm0.05\) rad; FOV \(\pm1^\circ\).
- **Proxy task (Sec. III-C):** Cube localization (3 colored cubes) predicts 3D cube positions relative to gripper; used to greedily pick DR params offline; correlates with real policy success.
- **Key empirical results:**
  - **Sim policy design (Table I, avg success in sim):** baseline (1 view, 1 frame) 44.97%; +2nd view 65.43%; +3 frames 93.94%; +proprio 98.34%.
  - **Proxy DR ablation (Table II, mean position error cm on real images):** 20k synth no DR 7.55 (default)/8.22 (variations); +ACG textures 2.52/3.53; +obj color 1.62/2.92; +camera 1.33/2.70; +2D aug 0.95/1.97; 100k synth +full DR 0.48/1.39. Real-only (750 imgs) 0.72/3.08 (worse under variations than synth+DR).
  - **Real robot success (Table III, 20 trials/task):** 2D aug only = 0/20 all tasks; +ACG textures avg 11.3/20; +light+obj color avg 14.0/20; +camera (full DR) avg 18.6/20 ≈ 93%.
  - **Robustness vs limited real data (Table IV, stacking):** DR avg 17.3/20 vs real-only 13.2/20; textured tablecloth DR 20/20 vs real-only 1/20.

</details>

### 📊 SimBenchmark — contact-rich physics engine comparison
**Benchmark** · [source](https://leggedrobotics.github.io/SimBenchmark/)

*Benchmark suite comparing multiple physics engines on contact-rich robotics tasks using speed–accuracy curves + task-specific metrics (trajectory error, energy/momentum, penetration drift) and summarized rankings.*

<details>
<summary>Key content</summary>

- **Motivation / rationale:** Contact dynamics accuracy + runtime are critical for legged robotics (feet–terrain contact drives whole-body motion). Contact dynamics is **NP-hard** due to non-convexity/discontinuity; engines use relaxed approximations with different accuracy/speed tradeoffs.
- **Multibody dynamics complexity:** naive articulated dynamics for **n links** has **O(n³)** complexity; modern engines use **linear-complexity** algorithms for efficiency.
- **Engines evaluated:** RaiSim (unreleased, proprietary), Bullet (2006, zlib), ODE (2001, GPL/BSD), MuJoCo (2015, proprietary), DART (2012, BSD).
- **Model/solver/integration (table facts):**
  - Contacts: RaiSim hard; Bullet hard/soft; ODE hard/soft; MuJoCo soft; DART hard.
  - Solvers: RaiSim bisection; Bullet MLCP; ODE LCP; MuJoCo Newton/PGS/CG; DART LCP.
  - Integrators: mostly semi-implicit Euler; MuJoCo also RK4.
  - Coordinates: ODE maximal; others minimal.
- **Evaluation methodology (procedure):**
  - Compare **speed–accuracy curves** (ideal = top-right).
  - For simple single-body few-contact cases: use **analytical trajectory** reference from **Newton rigid-body dynamics + Coulomb friction cone**.
  - For complex systems: evaluate generic quantities (**total kinetic energy**, **linear momentum**) + **penetration error** (position-level drift; should be 0 for rigid hard contacts).
- **Tests:** Rolling (friction), Bouncing (elastic collision), 666 balls (hard contact), Elastic 666 (energy), ANYmal PD (speed), ANYmal momentum, ANYmal energy.
- **Summary rankings (+ more is better):**
  - Rolling: Bullet +++; RaiSim ++; MuJoCo +; ODE −; DART −.
  - ANYmal PD: RaiSim +++++; MuJoCo ++++; Bullet +++; ODE +; DART ++.
  - ANYmal Momentum: ODE +++++; MuJoCo ++++ (RK4) / ++ (Euler); RaiSim +++; Bullet ++; DART +.
  - ANYmal Energy: MuJoCo +++++ (RK4) / +++ (Euler); RaiSim ++++; Bullet +++; ODE ++; DART +.
- **Noted limitations:** ODE/DART LCP can fail to simulate slip; DART poor with many objects; Bullet severe drift without post-solver correction; MuJoCo soft contact can’t control elasticity + consistent slip (needs post-process).

</details>

### 📖 Isaac Sim Python API Index (Physics/Simulation/DR)
**Reference Doc** · [source](https://docs.omniverse.nvidia.com/py/isaacsim/genindex.html)

*Authoritative Python API surface + config/workflow snippets for Isaac Sim / Isaac Lab (simulation stepping, scene setup, articulations, sensors, domain randomization).*

<details>
<summary>Key content</summary>

- **Core simulation/world callbacks (lookup exact signatures in index):**  
  `SimulationContext.add_physics_callback()`, `add_render_callback()`, `add_stage_callback()`, `add_timeline_callback()`; corresponding clears: `clear_physics_callbacks()`, `clear_render_callbacks()`, `clear_stage_callbacks()`, `clear_timeline_callbacks()`. Also `World.add_task()`, `World.add_world_view()`, `World.clear()`.
- **Scene construction primitives:**  
  `Scene.add_default_ground_plane()`, `Scene.add_ground_plane()`, `WorldInterface.add_cuboid()/add_sphere()/add_cone()/add_cylinder()`, `SceneRegistry.add_rigid_object()/add_robot()/add_sensor()` and `*_view()` variants.
- **Articulation control API surface:**  
  `Articulation.apply_action()`, `ArticulationController.apply_action()`, `ArticulationView.apply_action()`; DOF metadata: `dof_names`, `dof_properties`; body metadata: `body_names`.
- **PhysicsContext toggles:** `PhysicsContext.enable_gpu_dynamics()`, `enable_fabric()`.
- **Domain randomization timing conversion (Eq. 1):**  
  `time_s = num_steps * (decimation * dt)`  
  where `dt` = sim timestep (s), `decimation` = controlFrequencyInv renamed, `num_steps` = steps between randomizations.
- **Empirical/default config numbers (from config table/snippet):**  
  Example sim `dt = 1/120 ≈ 0.0083 s`; `decimation = 2` (→ 60 Hz control). Gravity `[0,0,-9.81]`. Solver iterations: position `4`, velocity `0`. Contact: `contact_offset=0.02`, `rest_offset=0.001`, `bounce_threshold_velocity=0.2`. `max_depenetration_velocity=100.0`. GPU buffers: `gpu_max_rigid_contact_count=524288`, `gpu_max_rigid_patch_count=81920`, `gpu_heap_capacity=67108864`, `gpu_temp_buffer_capacity=16777216`, `gpu_max_num_partitions=8`.
- **Workflow rationale (Isaac Lab vs OmniIsaacGymEnvs):** resets can occur based on *current-step* state (restriction removed); canonical loop: apply actions → step sim → collect states → compute dones/rewards → reset → compute observations (no required `post_physics_step`).

</details>

### 📖 Isaac Sim simulation fundamentals (USD ↔ PhysX pipeline)
**Reference Doc** · [source](https://docs.omniverse.nvidia.com/isaacsim/latest/simulation_fundamentals.html?highlight=Deformable%2520Body)

*System-level description of Isaac Sim’s simulation stack: USD scene representation, PhysX GPU simulation, sensor simulation, and integration points (ROS 2, Omnigraph, Replicator, Isaac Lab).*

<details>
<summary>Key content</summary>

- **Core purpose (What Isaac Sim is):** A reference application on **NVIDIA Omniverse Kit** for developing, simulating, and testing **AI-driven robots** in **physically-based virtual environments**.
- **Scene representation (USD):**
  - Isaac Sim uses **Universal Scene Description (USD)** as the **unifying data interchange format** at the heart of the platform.
  - USD is described as **extensible**, **open source**, and used broadly beyond VFX (architecture, robotics, manufacturing).
- **Physics + rendering backend:**
  - Simulation uses a **high-fidelity GPU-based PhysX engine**.
  - Supports **multi-sensor RTX rendering** “at industrial scale.”
  - Sensor simulation examples explicitly listed: **cameras**, **RTX Lidars**, **contact sensors**.
- **Workflow/toolchain integration points:**
  - **Import** workflows: **Onshape**, **URDF**, **MuJoCo XML (MJCF)**.
  - **Synthetic data**: **Replicator**.
  - **Graph orchestration**: **Omnigraph**.
  - **Physics tuning**: PhysX simulation parameter tuning to match reality.
  - **Training/control**: **Isaac Lab** for RL training of control agents.
  - **Deployment/bridging**: **ROS 2 bridge APIs** + integration with **NVIDIA Isaac ROS** packages.
- **Architecture rationale:**
  - Built on **Omniverse Kit** plugin system (lightweight plugins; C interfaces for API compatibility; Python interpreter for scripting).
  - Designed to **collaborate with existing tools**, not replace them; supports standalone apps or partial integration.

</details>

---

## Related Topics

- [[topics/physical-ai-foundations|Physical AI Foundations]]
- [[topics/robot-manipulation|Robot Manipulation]]
- [[topics/reinforcement-learning|Reinforcement Learning]]
