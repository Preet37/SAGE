---
title: "Robot Manipulation"
subject: "Physical AI & Robotics"
date: 2025-01-15
tags:
  - "subject/physical-ai-and-robotics"
  - "level/intermediate"
  - "level/advanced"
  - "resource/video"
  - "resource/blog"
  - "resource/deep-dive"
  - "resource/paper"
  - "resource/code"
educators:
  []
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

# Robot Manipulation

## Video (best)
- **Pieter Abbeel (Berkeley)** — "Deep Learning for Robot Manipulation" (CS287 Advanced Robotics lecture)
- **Watch:** [YouTube](https://www.youtube.com/watch?v=KhgCnMFhNd8)
- Why: Abbeel is one of the foremost researchers in robot learning and manipulation. His lectures systematically cover grasp planning, dexterous manipulation, and learning from demonstration — directly mapping to the related concepts in this topic. Berkeley's CS287 series is widely regarded as the gold standard for robot learning pedagogy.
- Level: intermediate/advanced

> ⚠️ **Coverage note on video:** No single canonical YouTube explainer from the preferred educators (3Blue1Brown, Karpathy, etc.) covers robot manipulation specifically. The best verified lecture series are from Abbeel (Berkeley) or Russ Tedrake (MIT 6.832). The specific video ID above should be verified — searching "Pieter Abbeel robot manipulation lecture" on YouTube is recommended.

---

## Blog / Written explainer (best)
- **Lilian Weng (OpenAI)** — "Generalized Visual Language Models" / "Learning Dexterous In-Hand Manipulation"
- url: https://lilianweng.github.io/posts/2022-06-09-vlm/ [NOT VERIFIED]
- Why: Lilian Weng's blog posts are exceptionally well-structured, mathematically grounded, and pedagogically clear. Her post on dexterous in-hand manipulation covers the OpenAI Dactyl work, reward shaping, sim-to-real transfer, and degrees of freedom — directly addressing the core concepts of this topic. Her writing bridges theory and implementation better than most academic papers.
- Level: intermediate

---

## Deep dive
- **Russ Tedrake — "Robotic Manipulation: Perception, Planning, and Control" (MIT Open Course Notes)**
- **Link:** [https://manipulation.csail.mit.edu/](https://manipulation.csail.mit.edu/)
- Why: This is the most comprehensive freely available technical reference for robot manipulation. Tedrake's online textbook covers the full stack: grasp planning, contact-rich manipulation, in-hand manipulation, degrees of freedom, real-time control, and perception. It is actively maintained, includes Drake code examples, and is used in MIT's graduate robotics curriculum. No other single resource matches its breadth and depth for this topic.
- Level: advanced

---

## Original paper
- **OpenAI et al. — "Dexterous In-Hand Manipulation" (Dactyl)**
- **Link:** [https://arxiv.org/abs/1808.00177](https://arxiv.org/abs/1808.00177)
- Why: This paper is the seminal demonstration of learned dexterous in-hand manipulation at scale, combining sim-to-real transfer, domain randomization, and deep RL. It directly addresses in-hand manipulation, degrees of freedom, and real-time control. It is highly readable relative to its technical depth and has become a standard reference in the field.
- Level: advanced

---

## Code walkthrough
- **Russ Tedrake / MIT — Drake + Manipulation Notebooks (Google Colab)**
- **Link:** [https://manipulation.csail.mit.edu/intro.html](https://manipulation.csail.mit.edu/intro.html)
- Why: The MIT manipulation course provides executable Jupyter/Colab notebooks that walk through grasp planning, contact simulation, and perception pipelines using the Drake robotics toolkit. These are the most pedagogically complete hands-on implementations available for this topic, directly tied to the deep-dive textbook above. Learners can run real manipulation scenarios without local hardware setup.
- Level: intermediate/advanced

---

## Coverage notes
- **Strong:** Grasp planning, contact-rich manipulation, in-hand manipulation, degrees of freedom, real-time control — all well covered by Tedrake's textbook and the Dactyl paper.
- **Strong:** Dexterous manipulation — Weng's blog and the Dactyl paper provide excellent coverage.
- **Weak:** BEV representation and occupancy networks in the context of robot manipulation (these concepts are more native to autonomous driving; their application to manipulation perception is an emerging area with limited dedicated tutorials).
- **Weak:** Levels of autonomy — covered conceptually in robotics literature but lacks a single best standalone explainer.
- **Gap:** No excellent beginner-friendly YouTube video exists specifically for robot manipulation from the preferred educator list. Most high-quality video content is at the graduate lecture level (Abbeel, Tedrake). A 3Blue1Brown-style visual explainer for manipulation fundamentals does not currently exist.
- **Gap:** The connection between NVIDIA Drive / autonomous driving concepts (BEV, occupancy networks) and robot manipulation is an emerging research area — no dedicated tutorial resource bridges these cleanly as of early 2025.

---

---

## Additional Resources for Tutor Depth

> **8 sources** — papers, official docs, working code, benchmarks, and deep explainers that give the AI tutor precision on this topic.

### 📄 Amazon Picking Challenge (APC) Winning System — System-Building Lessons
**Paper** · [source](https://www.roboticsproceedings.org/rss12/p36.pdf)

*System-level lessons from APC deployments: integration choices, feedback-heavy manipulation, failure modes, reliability numbers.*

<details>
<summary>Key content</summary>

- **Task & scoring (Sec. II):** Pick **12/25** known-bin objects from **12 bins** in **20 min**. Correct pick: **10/15/20 pts** depending on **0–3** extra objects in bin; difficult-object bonus **up to +3**; wrong object **−12**.
- **Environment constraints (Sec. II):** Bin opening **21×28 cm**, depth **43 cm**; reflective metal floors degrade RGB-D; harsh lighting (front “white”, back “black”).
- **Hardware (Sec. III-A):**
  - **7-DOF Barrett WAM** on **holonomic XR4000 base** → **10 holonomic DOF** total; mobility simplifies reaching; avoids high-DOF motion planning by using feedback controllers.
  - **Suction end-effector:** vacuum cleaner **250 W**, lifts **up to 1.5 kg**; thin nozzle fits between objects; grasp success insensitive to exact contact → relaxes perception/pose accuracy. Fails on **meshed pencil cup**.
  - Sensors: arm RGB-D (Asus XTion), wrist **6-axis F/T**, tube pressure sensor, base laser (SICK LMS-200).
- **Motion generation (Sec. III-B):** Two primitives:
  - **Top-down:** descend until F/T contact, then suction.
  - **Side:** force-guarded push orthogonal to wall to align object, then suction.
  - Execution via **hybrid automaton**: example primitive **26 states / 50 transitions**, **34** for error handling (retract/reattempt on collisions; pressure detects grasp failure).
- **Perception pipeline (Sec. III-C, Fig. 7):** Shelf tracking via **ICP** → crop bin → per-pixel features (6): hue/white-gray-black, edge, distance-to-shelf, height-above-ground, image-plane height (if no depth), depth-present flag → histogram likelihoods from manually segmented training → per-pixel class probabilities (only objects known in bin + bin) → smooth/argmax labeling → select segment with max target prob → point cloud → outlier filter → **bounding box fit** (size constrained to known object dims) for approach direction.
- **Empirical results (Sec. IV):**
  - Competition: **148/190 (77.8%)**, **10/12** targets; avg pick **87 s**; 2nd place **88**, 3rd **35**.
  - Post-hoc: **200 min**, **95** picks, **85** targets; mean **117.6 pts (σ=29.2)** = **62.5%** of available; only **1/10** trials would place 2nd.
  - Failures over **120 attempts** (Table I): **13** recognition; **9** bulky stuck at removal; **9** small objects missed (open-loop FK error **up to 1 cm**); **2** displaced objects; **2** pencil cup (unpickable).
- **Design rationale (Sec. V):** Favor **tight integration**, **embodiment** (simple suction), **feedback over planning** (most teams used motion planning; **80%** used it, **44%** MoveIt), and **task-specific assumptions** (known shelf + known bin contents) to achieve robustness; planning needed for in-bin reorientation of bulky items.

</details>

### 📄 Diffusion Policy (Action Diffusion for Visuomotor BC)
**Paper** · [source](https://diffusion-policy.cs.columbia.edu/diffusion_policy_ijrr.pdf)

*Training procedure (action diffusion, conditioning, horizons) + benchmark results (RoboMimic/Push-T/BlockPush/Kitchen + real-world)*

<details>
<summary>Key content</summary>

- **DDPM sampling / policy inference (Eq. 1):**  
  \(x_{k-1}=\alpha\big(x_k-\gamma\,\varepsilon_\theta(x_k,k)+\mathcal N(0,\sigma^2 I)\big)\).  
  Interpretable as noisy gradient step (Eq. 2): \(x' = x-\gamma\nabla E(x)\), where \(\varepsilon_\theta\) predicts a gradient/score field.
- **DDPM training (Eq. 3):** sample data \(x_0\), pick random diffusion step \(k\), sample noise \(\varepsilon_k\); minimize  
  \(L=\mathrm{MSE}(\varepsilon_k,\varepsilon_\theta(x_0+\varepsilon_k,k))\).
- **Visuomotor conditional action diffusion (Eq. 4–5):** model \(p(A_t\mid O_t)\) (not joint).  
  \(A^{k-1}_t=\alpha(A^k_t-\gamma\,\varepsilon_\theta(O_t,A^k_t,k)+\mathcal N(0,\sigma^2I))\).  
  Loss: \(L=\mathrm{MSE}(\varepsilon_k,\varepsilon_\theta(O_t,A^0_t+\varepsilon_k,k))\).
- **Closed-loop horizons (Sec. 2.3):** observation horizon \(T_o\); predict \(T_p\) actions; execute \(T_a\) before replanning (receding horizon). Warm-start next plan with unexecuted actions.
- **Architectures (Sec. 3.1):** CNN backbone with FiLM conditioning each conv layer; Transformer (“time-series diffusion transformer”) uses cross-attention to observation embeddings + causal self-attention over action tokens. Recommendation: start CNN; use Transformer for high-rate action changes.
- **Vision encoder (Sec. 3.2):** ResNet-18 (no pretrain), spatial softmax pooling; GroupNorm (EMA + BatchNorm conflict).
- **Noise schedule (Sec. 3.3):** Square Cosine schedule (iDDPM) worked best.
- **Real-time inference (Sec. 3.4):** DDIM: 100 training diffusion steps, 10 inference steps → ~0.1s latency on Nvidia 3080.
- **Key sim results (Tables 1–2, success rates shown as max / avg last-10 checkpoints):**  
  RoboMimic **state** examples: Transport (PH) LSTM-GMM 0.76/0.47 vs DiffPolicy-C 0.94/0.82 vs DiffPolicy-T 1.00/0.84; ToolHang (PH) 0.67/0.31 vs 0.50/0.30 vs 1.00/0.87.  
  RoboMimic **visual** example: Transport (MH) LSTM-GMM 0.44/0.24 vs DiffPolicy-C 0.89/0.69 vs DiffPolicy-T 0.73/0.50.
- **Multi-stage state tasks (Table 4):** BlockPush p2: BET 0.71 vs DiffPolicy-T 0.94; Kitchen p4: BET 0.44 vs DiffPolicy-T 0.96.
- **Real-world Push-T (Table 6):** Human IoU 0.84, Succ 1.00; DiffPolicy (E2E) IoU 0.80, Succ 0.95; LSTM-GMM (E2E) Succ 0.20; IBC (E2E) Succ 0.00. Control at 10 Hz, interpolated to 125 Hz.
- **Real-world other tasks:** Mug Flip: DiffPolicy 0.9 success (20 trials) vs LSTM-GMM 0.0. Sauce Pour: IoU 0.74, Succ 0.79 (human 0.79/1.00). Sauce Spread: coverage 0.77, Succ 1.00 (human 0.79/1.00).

</details>

### 📄 MIT APC 2015 End-to-End Picking System (Perception→Primitives→Planning→Heuristic)
**Paper** · [source](https://arxiv.org/pdf/1604.03639.pdf)

*Deployed competition system architecture + concrete integration choices for shelf picking*

<details>
<summary>Key content</summary>

- **Task setup (APC 2015):** 20 min autonomous run; 12 target bins in a **1.0 m (H) × 0.87 m (W) × 0.43 m (D)** region; bin openings vary (**19–22 cm** height, **25–30 cm** width) with lips that impede sliding/pulling. Items placed near front; not stacked/behind; not tightly packed.
- **Hardware choices & parameters (Sections IV-A/B):**
  - Arm: **ABB 1600ID**, tool max speed used **1 m/s**; hollow wrist for cable/air routing (maneuverability, fewer snags).
  - Gripper: **WSG-50** parallel jaw, **110 mm** opening, **70 N** max force; **force + position control** used for preloading spatula against shelf.
  - Custom fingers: thin aluminum plates; one finger has **compliant spring-steel spatula** (environment-assisted insertion); other integrates **suction cup** + in-line Venturi; **vacuum pressure sensor** for seal feedback.
  - Cameras: **2× Kinect2** (ToF, **0.8–4 m**, **512×424**) + arm-mounted **Intel RealSense** (structured light, **0.2–1.2 m**, **640×480**). Kinect2 IR can blind RealSense → cameras toggled during Percept primitive.
- **Software architecture (Section V, Fig. 7):** ROS-based; **central heuristic (state machine)** selects among **motion primitives** using camera + gripper encoder + suction pressure feedback; primitives executed via **Drake IK planner** (MATLAB; TCP+JSON interface).
- **Perception pipeline (Section V-A):**
  1) Transform pointcloud to shelf frame; filter outside shelf convex hull + NaNs.  
  2) Apply bin physical constraints (within walls; intersect thickened/up-shifted bin floor).  
  3) Run Capsen model-fitting on **depth-only** pointcloud + mask + constraints + known item IDs → multiple hypotheses with **log-likelihood scores** (IDs + 6D poses).  
  4) Reject hypotheses with COM outside bin; pick highest score.  
  5) Robustness: run **5×** on closest Kinect depth + **5×** on RealSense depth.
- **Motion primitives (Section V-B):** Percept (preselected 2 viewpoints/bin; IK with tolerance), Grasp (front approach; search pitch/yaw to avoid shelf lips; use spatula pretension if near wall), Scoop (preload spatula on floor via force control; push to back to capture), Suction (down/side; stop on contact via force control; verify expected contact height; up to **5 attempts** with XY jitter; confirm via pressure sensor), Topple (fast push above COM; re-perceive), Push-Rotate (reorient to expose graspable dimension; re-perceive).
- **Empirical outcome (Section VI):** Picked **7/12** items; **~7 min** before torque overload stop; scored **88 points**, **2nd** of 30+ teams. Initial failure: gripper reboot due to heavy TCP/IP traffic → **5 min** penalty.

</details>

### 📄 Unified complementarity contact model (Unicomp)
**Paper** · [source](https://arxiv.org/html/2602.04522v1)

*Complementarity/LCP-style contact formulation (normal-force complementarity + friction constraints) integrated with rigid-body dynamics; discrete-time setup for contact-rich manipulation*

<details>
<summary>Key content</summary>

- **MCP/LCP definitions (Sec. 2.1):** MCP seeks \(x\in[l,u]\) s.t. for each component \(i\):  
  \(x_i=l_i \Rightarrow F_i(x)\ge 0;\;\; l_i<x_i<u_i \Rightarrow F_i(x)=0;\;\; x_i=u_i \Rightarrow F_i(x)\le 0\) (Eq. 1–2).  
  LCP special case: \(F(x)=Mx+q\), find \(x\ge 0\) with \(Mx+q\ge 0\), \(x^\top(Mx+q)=0\) (Eq. 3–4).
- **Continuous rigid-body dynamics + unilateral normal complementarity (Sec. 2.2):** Newton–Euler (Eq. 5) with contact at ECP: normal force magnitude \(\lambda_n\), tangential forces \(\lambda_t\), torsional friction moment \(\lambda_o\). Normal constraint:  
  \(0\le \lambda_n \perp \phi(q)\ge 0\) where \(\phi\) is signed normal gap at ECP (Eq. 6).
- **Friction via maximum power dissipation + ellipsoidal limit surface (Eq. 7):** choose friction wrench \(w_f=[\lambda_t;\lambda_o]\) to minimize dissipation \(v^\top w_f\) subject to ellipsoid constraint  
  \(\left(\frac{\lambda_{t1}}{\mu \lambda_n}\right)^2+\left(\frac{\lambda_{t2}}{\mu \lambda_n}\right)^2+\left(\frac{\lambda_o}{\mu \lambda_n e_o}\right)^2 \le 1\) (parameters \(\mu\), \(e_t,e_o>0\)); equivalent NCP via Fritz–John conditions (Eq. 8–11; discrete-time analog Eq. 27–30).
- **Discrete-time time-stepping (Sec. 4):** free update (Eq. 13) and with contact impulse \(p\):  
  \(V^{k+1}=V^k+M^{-1}(p+p_\text{ext})\) (Eq. 22); pose update via SE(3) integration (Eq. 23). Contact impulse parameterization at ECP (Eq. 24) using tangential impulses \(p_t\), torsional impulse \(p_o\), normal direction \(n\), tangents \(t_1,t_2\), moment arm \(r\).
- **Discrete non-penetration complementarity (Eq. 25):** \(0\le p_n \perp (\phi^k + h\,v_n^{k+1} + \epsilon)\ge 0\) (step \(h\), regulation \(\epsilon\)).
- **ECP selection inside convex hull (Eq. 17–21):** half-space constraints \(A x_\text{ECP}\le b\) enforced via KKT complementarity with duals \(\gamma\) (Eq. 18–19) plus tie-break potential (Eq. 20–21).
- **Two-body contact (Sec. 4.1):** equal-and-opposite impulses (Eq. 32), velocity updates (Eq. 33), relative slip/twist at ECP (Eq. 34–35), two-body gap (Eq. 36).
- **Whole-body collision avoidance as LCP (Sec. 4.2):** robot links approximated by spheres; signed gap (Eq. 37) with safety margin \(s\); one-step separation (Eq. 39–40). Correct nominal joint increment \(\Delta q_\text{nom}\) via \(\Delta q=\Delta q_\text{nom}+N\lambda\) (Eq. 43) where \(\lambda\ge 0\) solves LCP (Eq. 46–47).
- **Empirical/config defaults:** planar pushing experiments run at fixed step \(h=0.001\) s (1000 Hz) on a single CPU core (Sec. 5.2). Stick/slide/break annotated from solver outputs: break if \(p_n\approx 0\); else slide if limit-surface saturation \(\approx 1\); stick otherwise (Sec. 5.1, Eq. 48–49).

</details>

### 📊 MS-HAB baseline results + ablations for low-level home rearrangement
**Benchmark** · [source](https://proceedings.iclr.cc/paper_files/paper/2025/file/27aa3a0e6d63db269977bb2df5607cb8-Paper-Conference.pdf)

*Benchmark tables: subtask success rates (RL/IL), per-object vs all-object ablations, trajectory labeling/filtering effects; simulator speed benchmark.*

<details>
<summary>Key content</summary>

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

</details>

### 📖 libfranka `franka::Robot` control loops (1 kHz callbacks)
**Reference Doc** · [source](https://frankaemika.github.io/libfranka/classfranka_1_1Robot.html)

*Robot API surface for real-time control loops: `Robot::control` callback structure, motion generators, torque commands, and command/feedback interfaces.*

<details>
<summary>Key content</summary>

- **Connection & setup**
  - `Robot(franka_address, realtime_config=RealtimeConfig::kEnforce, log_size=50)` establishes network connection.
  - `realtime_config=kEnforce`: throws if realtime priority cannot be set; `Ignore` disables this behavior.
  - `log_size`: number of last states kept for logging; provided when `ControlException` is thrown.
  - `serverVersion() -> uint16_t` returns robot server software version.
  - `loadModel()` loads model library from robot.

- **State reading**
  - `read(read_callback: bool(const RobotState&))`: loop reading robot state; **cannot run while a control/motion loop is running**.
  - `readOnce() -> RobotState`: blocks until next state update.

- **Real-time control loop (core procedure)**
  - `control(...)` runs at **1 kHz**; callback must compute quickly to be accepted.
  - Callback signature: `(const RobotState& robot_state, franka::Duration time_step) -> CommandType`.
  - **Time update pattern:** `time += time_step.toSec();` at start of callback.
  - **Stopping a motion:** return `franka::MotionFinished(command)` (e.g., `MotionFinished(Torques)`).
  - **Important detail:** `time_step` is **0 on the first invocation**.
  - **Mutual exclusion:** only **one** `control`/motion-generator loop active at a time; otherwise `ControlException` / `InvalidOperationException`.

- **Control overloads & defaults**
  - Torque-only: `control(Torques cb, limit_rate=true, cutoff_frequency=kDefaultCutoffFrequency)`.
  - Torque + motion generator: joint positions/velocities or Cartesian pose/velocities.
  - Motion-generator-only: `control(JointPositions|JointVelocities|CartesianPose|CartesianVelocities cb, controller_mode=ControllerMode::kJointImpedance, limit_rate=true, cutoff_frequency=...)`.
  - `limit_rate=true` by default; note: “could distort your motion!”
  - `cutoff_frequency`: 1st-order low-pass on commanded signal; set to `franka::kMaxCutoffFrequency` to disable.

- **Non-real-time commands (don’t call inside loops)**
  - `setCollisionBehavior(...)`: thresholds; between lower/upper => “contact” in `RobotState`; above upper => “collision” and robot stops.
  - `setJointImpedance(K_theta[7])`, `setCartesianImpedance(K_x[6])`, `setGuidingMode(bool[6], elbow)`, `setK(EE_T_K[16])`, `setEE(NE_T_EE[16])`, `setLoad(mass, F_x_Cload[3], inertia[9])`, `setFilters(...)` (**1–1000 Hz**, 1000 Hz = no filtering), `automaticErrorRecovery()`, `stop()` (preempts other thread’s loop with `ControlException`).

</details>

### 📖 libfranka `setDefaultBehavior()` + collision behavior pattern
**Reference Doc** · [source](https://frankaemika.github.io/libfranka/examples__common_8h.html)

*Official example pattern: call `setDefaultBehavior(robot)` early; then optionally override `Robot::setCollisionBehavior(...)` thresholds before realtime control.*

<details>
<summary>Key content</summary>

- **Canonical startup workflow (official examples):**
  1. Construct `franka::Robot robot(<hostname/ip>)`.
  2. Call `setDefaultBehavior(robot);` (helper used across examples to apply a safe baseline configuration before motion/control).
  3. Move to a known joint configuration (example uses `q_goal = {0, -π/4, 0, -3π/4, 0, π/2, π/4}` with `MotionGenerator(0.5, q_goal)`).
  4. Optionally **override collision thresholds** via `robot.setCollisionBehavior(...)`.
  5. Start realtime control (e.g., `robot.startTorqueControl()` or `robot.control(...)`) and loop at ~1 kHz.

- **Collision behavior thresholds (example numbers):** `robot.setCollisionBehavior(...)` is called with **8 arrays** (torque/force, lower/upper, accel/decel vs constant-velocity phases). Example values:
  - Joint torque thresholds (7-DoF), repeated across phases/bounds:  
    `{20.0, 20.0, 18.0, 18.0, 16.0, 14.0, 12.0}`
  - Cartesian force thresholds (6 axes), repeated across phases/bounds:  
    `{20.0, 20.0, 20.0, 25.0, 25.0, 25.0}`

- **Realtime loop detail:** callback/`readOnce()` period is **0 on first cycle**; examples send a safe initial command (e.g., zero torques) when `time == 0`.

</details>

### 🔍 Manipulator dynamics via spatial vectors (RNEA/CRBA/ABA)
**Explainer** · [source](https://gaoyichao.com/Xiaotu/papers/2008%20-%20Rigid%20body%20dynamics%20algorithms.pdf)

*Derivations + pseudocode for RNEA (inverse dynamics), CRBA & ABA (forward dynamics), using 6D spatial vectors to build \(H(q)\)/\(M(q)\) and bias terms \(C(q,\dot q)\), incl. gravity/external forces.*

<details>
<summary>Key content</summary>

- **Canonical equation of motion (Eq. 1.1):**  
  \[
  \tau = H(q)\,\ddot q + C(q,\dot q)
  \]
  \(q,\dot q,\ddot q\): generalized position/velocity/acceleration; \(\tau\): generalized forces; \(H\): joint-space inertia; \(C\): Coriolis/centrifugal + gravity + other non-\(\tau\) forces.
- **Forward/inverse dynamics function interfaces (Eqs. 1.2–1.3):**  
  \[
  \ddot q = FD(\text{model},q,\dot q,\tau),\qquad
  \tau = ID(\text{model},q,\dot q,\ddot q)
  \]
  with \(FD = H^{-1}(\tau - C)\), \(ID = H\ddot q + C\).
- **Spatial rigid-body equation (Eq. 1.5):**  
  \[
  f = I a + v \times^{*} (I v)
  \]
  \(v,a\): spatial (6D) velocity/acceleration; \(f\): spatial force; \(I\): spatial inertia; \(\times^{*}\): spatial cross-product operator.
- **Design rationale:** spatial (6D) notation unifies linear+angular quantities, reduces algebra, enables efficient recursion; spatial inertias add under rigid attachment: \(I_{\text{new}}=I_1+I_2\).
- **Algorithmic workflow (Chs. 5–7):**
  - **RNEA (inverse dynamics):** 2-pass recursion—forward pass propagates kinematics; backward pass accumulates subtree forces → joint torques \(\tau\).
  - **CRBA:** computes \(H(q)\) efficiently via composite rigid-body inertias.
  - **ABA:** forward dynamics recursion to compute \(\ddot q\) without explicitly forming \(H\).

</details>

---

## Related Topics

- [[topics/physical-ai-foundations|Physical AI Foundations]]
- [[topics/imitation-learning|Imitation Learning]]
- [[topics/reinforcement-learning|Reinforcement Learning]]
