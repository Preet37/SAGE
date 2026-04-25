---
title: "Physical AI Foundations"
subject: "Physical AI & Robotics"
date: 2025-01-01
tags:
  - "subject/physical-ai-and-robotics"
  - "level/intermediate"
  - "level/advanced"
  - "educator/lilian-weng"
  - "resource/video"
  - "resource/blog"
  - "resource/deep-dive"
  - "resource/paper"
  - "resource/code"
educators:
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

# Physical AI Foundations

## Video (best)
- **MIT OpenCourseWare / Russ Tedrake** — "Underactuated Robotics Lecture Series (Perception & Control)"
- **Link:** [https://ocw.mit.edu/courses/6-832-underactuated-robotics-spring-2009/](https://ocw.mit.edu/courses/6-832-underactuated-robotics-spring-2009/)
- Why: Russ Tedrake's MIT 6.832 lectures are the closest rigorous academic treatment of the perception-action loop, embodied intelligence, and autonomous systems foundations. However, no single YouTube video cleanly covers "Physical AI Foundations" as a unified topic with the sensor fusion + embodied intelligence framing used in modern Physical AI discourse.
- Level: advanced

> ⚠️ **Coverage Gap Note:** No single YouTube explainer from the preferred educators (3Blue1Brown, Karpathy, Yannic, StatQuest) covers Physical AI Foundations as a unified concept. The term "Physical AI" as used by NVIDIA/industry (convergence of perception, action, and embodied intelligence) is too recent (2023–2024) for polished explainers to exist.

**Best available alternative:**
- **NVIDIA GTC Keynote clips** — Jensen Huang's GTC 2024 "Physical AI" segment on YouTube provides the conceptual framing, but is a product keynote, not a pedagogical resource. [Video ID: _waPvOwL9Z8 (GTC March 2025 Keynote)]

---

## Blog / Written explainer (best)
- **Lilian Weng** — "Autonomous Agents" (covers embodied intelligence, perception-action loops, and agent grounding)
- **Link:** [https://lilianweng.github.io/posts/2023-06-23-agent/](https://lilianweng.github.io/posts/2023-06-23-agent/)
- Why: Weng's characteristic depth and clarity covers the cognitive architecture underlying Physical AI — perception, memory, action, and tool use — with rigorous citations. While not exclusively about robotics hardware, it is the best written explainer from a trusted educator that addresses the embodied intelligence and perception-action loop concepts central to this topic. Her treatment bridges the gap between LLM-based reasoning and physical grounding.
- Level: intermediate/advanced

---

## Deep dive
- **Author/Source** — Russ Tedrake, "Robotic Manipulation: Perception, Planning, and Control" (MIT Open Textbook)
- **Link:** [https://manipulation.csail.mit.edu/](https://manipulation.csail.mit.edu/)
- Why: This is the most comprehensive freely available technical reference covering the full stack of Physical AI: depth cameras, sensor fusion, perception-action loops, grasping, and manipulation planning. Written by one of the field's leading researchers, it includes code, lecture notes, and problem sets. Covers sim-to-real, tactile sensing concepts, and safety considerations. Far more rigorous than any blog post for learners who need implementation depth.
- Level: advanced

---

## Original paper
- **None identified** — Physical AI as a unified concept does not have a single seminal "founding paper" in the way that, e.g., the Transformer or AlexNet do. The topic is a convergence of multiple subfields.

**Closest candidates (use with caveat):**
- For embodied intelligence: Pfeifer & Bongard's work, or the RT-2 paper (arxiv.org/abs/2307.15818) for vision-language-action models
- For sensor fusion foundations: No single canonical paper
- For tactile sensing (GelSight): Yuan et al., 2017 — "GelSight: High-Resolution Robot Tactile Sensors for Estimating Geometry and Force" https://pmc.ncbi.nlm.nih.gov/articles/PMC5751610/

> Recommendation: Do not force a single paper here. Assign RT-2 + one tactile sensing paper as a paired reading instead.

---

## Code walkthrough
- **Source** — MIT Manipulation Course Notebooks (Drake-based)
- **Link:** [https://manipulation.csail.mit.edu/clutter.html](https://manipulation.csail.mit.edu/clutter.html)
- Why: Tedrake's course provides runnable Jupyter/Colab notebooks using the Drake simulator that walk through perception pipelines (depth cameras, point clouds), grasp planning, and sensor integration — directly mapping to the core concepts of Physical AI Foundations. These are the most pedagogically complete hands-on implementations available for this topic from a credible academic source.
- Level: advanced

**Alternative for beginners:**
- NVIDIA Isaac Sim tutorials cover sensor fusion and robot perception in a more accessible way, but require proprietary software setup. [NOT VERIFIED]

---

## Coverage notes
- **Strong:** Perception-action loop, embodied intelligence (conceptual), manipulation and depth cameras (Tedrake's materials), autonomous systems architecture
- **Weak:** Tactile sensing (GelSight) — no strong standalone tutorial exists outside research lab pages; LiDAR-specific educational content tends to live in autonomous driving courses, not general Physical AI courses
- **Weak:** Safety certification for physical AI systems — this is a genuine educational gap; most content is either too theoretical (formal verification literature) or too domain-specific (automotive ISO 26262)
- **Gap:** No high-quality beginner-to-intermediate YouTube series exists for Physical AI Foundations as a unified topic. This is a significant gap for the platform — original content creation would add real value here.
- **Gap:** Sensor fusion for humanoid robots specifically (as opposed to autonomous vehicles) has almost no dedicated educational resources outside of proprietary robot SDK documentation.

---

---

## Additional Resources for Tutor Depth

> **10 sources** — papers, official docs, working code, benchmarks, and deep explainers that give the AI tutor precision on this topic.

### 📄 Diffusion Policy (Action Diffusion for Visuomotor BC)
**Paper** · [source](https://diffusion-policy.cs.columbia.edu/diffusion_policy_ijrr.pdf)

*Full diffusion-policy objective + sampling procedure; benchmark tables across multiple manipulation suites*

<details>
<summary>Key content</summary>

- **DDPM sampling / policy inference (Eq. 1, Eq. 4):** start from Gaussian noise \(x_K\) (or action-seq \(A_t^K\)). Iterate  
  \(x_{k-1}=\alpha\big(x_k-\gamma\,\varepsilon_\theta(x_k,k)+\mathcal N(0,\sigma^2 I)\big)\) (Eq. 1).  
  Conditional visuomotor form: \(A_{t}^{k-1}=\alpha\big(A_t^k-\gamma\,\varepsilon_\theta(O_t,A_t^k,k)+\mathcal N(0,\sigma^2 I)\big)\) (Eq. 4).  
  Interpretable as noisy gradient step \(x' = x-\gamma\nabla E(x)\) (Eq. 2).
- **Training objective (Eq. 3, Eq. 5):** sample data \(x_0\) (or \(A_t^0\)), pick random diffusion step \(k\), add noise \(\varepsilon_k\). Minimize  
  \(L=\mathrm{MSE}(\varepsilon_k,\varepsilon_\theta(x_0+\varepsilon_k,k))\) (Eq. 3); conditional:  
  \(L=\mathrm{MSE}(\varepsilon_k,\varepsilon_\theta(O_t,A_t^0+\varepsilon_k,k))\) (Eq. 5).
- **Closed-loop receding horizon (Sec. 2.3):** observe last \(T_o\) steps \(O_t\); predict \(T_p\) future actions; execute only \(T_a\) then replan; warm-start next plan with unexecuted actions.
- **Design defaults:** Square Cosine noise schedule (Sec. 3.3). DDIM for speed: **100 training iterations, 10 inference iterations → ~0.1s latency on RTX 3080** (Sec. 3.4). Action horizon **8 steps** often best (Sec. 5.3, Fig. 5).
- **Vision encoder (Sec. 3.2):** ResNet-18 (no pretrain), spatial softmax (replace GAP), GroupNorm (replace BatchNorm) for EMA stability.
- **Empirical headline:** across **15 tasks / 4 benchmarks**, Diffusion Policy improves average success by **46.9%** vs prior SOTA (Abstract/Sec. 5.3).
- **Key benchmark numbers:**  
  - RoboMimic visual (Table 2): **Transport (PH)** LSTM-GMM 0.88/0.62 vs DiffusionPolicy-C **1.00/0.93**; **ToolHang (PH)** 0.68/0.49 vs **0.95/0.73**.  
  - Multi-stage state (Table 4): **BlockPush p2** BET 0.71 vs DiffusionPolicy-T **0.94**; **Kitchen p4** BET 0.44 vs DiffusionPolicy-C **0.99** (T: 0.96).  
  - Real Push-T (Table 6): Diffusion Policy (end2end) **Succ 0.95**, IoU **0.80**; IBC **0.00**, LSTM-GMM best **0.20**.

</details>

### 📄 Diffusion Policy (Action Diffusion for Visuomotor Control)
**Paper** · [source](https://arxiv.org/abs/2303.04137)

*Benchmark success rates across manipulation suites + diffusion-policy objective & action-sequence sampling (DDPM/DDIM)*

<details>
<summary>Key content</summary>

- **Policy as conditional DDPM over action sequences** (Sec. 2): generate an action trajectory by iterative denoising, conditioned on observation \(o\).  
  - **Sampling update (Eq. 1 / Eq. 4):** \(a_{t-1} = f_\theta(a_t, t, o) + \sigma_t z\), with \(z\sim\mathcal N(0,I)\). (Unconditional form in Eq. 1; conditional on \(o\) in Eq. 4.)  
  - **Gradient-descent view (Eq. 2):** update interpretable as a noisy gradient step where the network predicts a score/gradient field; \(\sigma_t\) controls noise, step size acts like a learning rate.
- **Training objective (Eq. 3 / Eq. 5):** sample data action sequence \(a_0\), choose diffusion step \(t\), add Gaussian noise to get \(a_t\); train \(\epsilon_\theta(\cdot)\) to predict the injected noise (MSE on noise prediction), conditioned on \(o\).
- **Closed-loop receding-horizon execution** (Sec. 2.3): at time \(k\), input last \(T_o\) observations, predict \(T_a\) future actions, execute first \(T_e\) actions, then replan; can **warm-start** next plan from previous predicted sequence.
- **Real-time acceleration** (Sec. 3.4): use **DDIM**; example: **100 training diffusion steps, 10 inference steps → ~0.1 s latency** on **NVIDIA 3080**.
- **Design choices/rationale**
  - Condition on observations (not joint obs-action diffusion) to avoid inferring future states → faster inference, feasible end-to-end vision training (Sec. 2.3).
  - **CNN vs Transformer** (Sec. 3.1): CNN works “out of the box”; Transformer helps when actions change rapidly (reduces CNN over-smoothing) but is more hyperparameter-sensitive.
  - **Noise schedule:** Square Cosine (iDDPM) worked best empirically (Sec. 3.3).
- **Key empirical results (success rates)**
  - Across **15 tasks / 4 benchmarks**, Diffusion Policy improves average success by **46.9%** (Abstract/Sec. 5).
  - **BlockPush / Kitchen table:** DiffusionPolicy-T: **BlockPush p1=0.99, p2=0.94**; **Kitchen p1=1.00, p2=0.99, p3=0.99, p4=0.96** (beats BET p4=0.44).
  - **Real-world Push-T:** Diffusion Policy (E2E vision) **Succ%=0.95, IoU=0.80** vs **IBC best Succ%=0.00** and **LSTM-GMM best Succ%=0.20** (Tab. 6).
  - **Real-world Pour/Spread:** Diffusion Policy **Pour IoU=0.74, Succ=0.79; Spread Coverage=0.77, Succ=1.00** vs LSTM-GMM **Succ=0.00** both (Sec. 6.3 table).

</details>

### 📄 Diffusion Policy (DDPM for visuomotor action sequences)
**Paper** · [source](https://roboticsproceedings.org/rss19/p026.pdf)

*Proceedings version with definitive method description, experimental protocol, and results tables*

<details>
<summary>Key content</summary>

- **DDPM denoising update (Eq. 1):**  
  \(x_{k-1}=\alpha\big(x_k-\gamma\,\epsilon_\theta(x_k,k)+\mathcal{N}(0,\sigma^2 I)\big)\).  
  Interpretable as noisy gradient step (Eq. 2): \(x' = x-\gamma\nabla E(x)\), where \(\epsilon_\theta\) predicts the gradient field.
- **Training objective (Eq. 3):** sample data \(x_0\), pick random step \(k\), add noise \(\epsilon_k\); minimize  
  \(L=\mathrm{MSE}(\epsilon_k,\epsilon_\theta(x_0+\epsilon_k,k))\).
- **Policy conditioning + closed-loop horizons (Sec. II-C, Fig. 3):** learn conditional \(p(A_t|O_t)\) with action sequences.  
  Conditioned denoising (Eq. 4): \(A^{k-1}_t=\alpha(A^k_t-\gamma\,\epsilon_\theta(O_t,A^k_t,k)+\mathcal{N}(0,\sigma^2I))\).  
  Loss (Eq. 5): \(L=\mathrm{MSE}(\epsilon_k,\epsilon_\theta(O_t,A^0_t+\epsilon_k,k))\).  
  Horizons: observation \(T_o\), prediction \(T_p\), execute \(T_a\) steps before replanning (receding horizon).
- **Architectures (Sec. III-A):** CNN backbone with FiLM conditioning; **Time-series Diffusion Transformer** (cross-attention to obs; causal attention over actions) reduces CNN over-smoothing for high-rate control.
- **Visual encoder (Sec. III-B):** ResNet-18 (no pretrain), spatial softmax pooling, GroupNorm (stable with EMA).
- **Defaults/acceleration:** Square Cosine noise schedule (iDDPM) works best (Sec. III-C). DDIM speeds inference: **100 training steps, 10 inference steps → ~0.1s latency on RTX 3080** (Sec. III-D).
- **Key empirical results:**  
  - Across **12 tasks / 4 benchmarks**, Diffusion Policy average **+46.9%** success-rate improvement vs prior SOTA (Abstract/Sec. V).  
  - **Real Push-T:** Diffusion Policy (end-to-end transformer) **95% success**, **IoU 0.80** vs Human **1.00 / 0.84**; IBC best **0%**, LSTM-GMM best **20%** (Table V).  
  - **Mug flip:** Diffusion Policy **90%** vs LSTM-GMM **0%** (Fig. 10).  
  - **Sauce tasks:** Pour IoU **0.74**, succ **0.79**; Spread coverage **0.77**, succ **1.00** (Fig. 11).
- **Design rationale:** conditioning on \(O_t\) (not joint \(A,O\)) extracts vision once → real-time control; action-sequence diffusion handles multimodality + temporal consistency; score modeling avoids EBM normalization/negative sampling → training stability (Sec. IV-D).

</details>

### 📄 RT-2 (Vision-Language-Action) — tokenized actions + co-fine-tuning boosts generalization
**Paper** · [source](https://proceedings.mlr.press/v229/zitkovich23a/zitkovich23a.pdf)

*RT-2 evaluation results (success rates across seen/unseen + emergent skills) and ablations (model size, co-fine-tuning vs robot-only vs scratch)*

<details>
<summary>Key content</summary>

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

</details>

### 📄 Robustness of LiDAR vs RADAR vs Depth Camera on ill-reflective surfaces
**Paper** · [source](https://arxiv.org/html/2309.10504)

*Measured robustness comparisons across sensing modalities (LiDAR vs depth camera vs radar) with failure modes and performance under adverse (ill-reflective) conditions*

<details>
<summary>Key content</summary>

- **Sensor principles (Section II):**
  - LiDAR: active ToF in near-infrared; detects returned reflected light along emitted beam path.
  - FMCW RADAR: range from beat frequency; **range resolution** \(\Delta R = \frac{c}{2B}\). Velocity from phase differences across chirps; AoA via beamforming + CFAR to form point clouds.
  - Depth camera (Intel D455): IR stereo; depth from disparity: **Eq. 1** \(Z = \frac{f\,b}{d}\) where \(Z\)=depth, \(f\)=focal length, \(b\)=baseline, \(d\)=disparity.
- **Evaluation metrics (Section IV):**
  - **Eq. 2 (MAE):** \(\text{MAE}=\frac{1}{N}\sum_{i=1}^{N}\left|r^{gt}_i-r^{meas}_i\right|\).
  - **Eq. 3 (Std):** \(\sigma=\sqrt{\frac{1}{N}\sum_{i=1}^{N}(x_i-\mu)^2}\).
- **Material reflectivity (Section V-A, Table I):**
  - White matt max power reflectivity **9.5%** vs black matt **4.7% (s-pol)** and **0.3% (p-pol)**; black p-pol reflectivity **13× lower** than black s-pol.
- **Static ranging results (Section V-B):**
  - Baseline (white): LiDAR max **10 m**; MAE **<5 cm up to 8.5 m**. RADAR max **7 m**, MAE ~**10–15 cm**. Depth camera max **6 m**, MAE **61 cm at 6 m** (monotonically worsens with distance).
  - Ill-reflective (black): LiDAR max **3 m** (**33%** of baseline). RADAR max **7.5 m**, MAE **<10 cm** for **≥2.5 m** but more false positives at short range. Depth camera keeps **6 m** max range; similar trend, lower MAE beyond **3 m** vs baseline.
- **Dynamic downstream impact (Section III-C, V-C):**
  - Track half reflective/half ill-reflective; **10 laps** each config; fusion prioritizes LiDAR, uses depth/RADAR when LiDAR unavailable.
  - Mean lap times: **LiDAR+Depth 7.686 s** (best); **LiDAR-only 7.729 s** (+0.043 s, **0.573%** worse); **LiDAR+RADAR 8.011 s** (**12.026%** worse vs LiDAR+Depth). Std dev ≤ **0.054 s**.

</details>

### 📊 Waymo public-road safety metrics & benchmarks
**Benchmark** · [source](https://storage.googleapis.com/sdc-prod/v1/safety-report/Waymo-Public-Road-Safety-Performance-Data.pdf)

*Operational safety metrics + comparative crash/incident rates for public-road autonomous operation*

<details>
<summary>Key content</summary>

- **Exposure (Abstract):** >6.1M miles automated driving in Phoenix ODD; includes **65,000 miles driverless** (2019–first 9 months 2020).
- **Event accounting (Section 3):** **47 total contact events** = **18 actual** + **29 simulated** (from counterfactual “what-if” post-disengagement simulation). **1 event during driverless operation.**
- **Severity framework (Section 2.3 / Table 1 description):** Events categorized using **ISO 26262 severity classes S0–S3** (S0 no injury expected → S3 possible critical injuries). Waymo estimates injury likelihood using **AIS-linked** probabilities; severity estimation uses **impact object, impact velocity, impact geometry**, and **ΔV / principle direction of force**.
- **Airbag-deployment-level events (Table 1 notes):** **8 most severe events** defined as involving **actual or expected airbag deployment**; **all 8** involved road rule violations/other errors by human road users. **No actual or predicted S2 or S3 events.**
- **Counterfactual simulation workflow (Section 2.3):**
  1) Re-simulate AV post-disengagement using recorded **pre-disengage state** (position/attitude/velocity/acceleration) + **recorded sensor observations** to generate AV’s counterfactual trajectory.  
  2) If needed, simulate other agents using deterministic **human collision-avoidance behavior models** (calibrated on naturalistic collision/near-collision data; response triggered by deviations from expectations).  
  3) Infer contact; assign severity via national crash databases; add scenario to regression library.
- **Collision-mode result (Discussion):** **0 actual or simulated** events in **“road departure, fixed object, rollover”** typology (noted as **27% of US roadway fatalities**).
- **Benchmarking rationale (Comparison benchmarks):** Comparisons to human crash stats are hard due to **ODD specificity**, **different crash definitions** (Waymo includes minor contacts), and **model assumptions**; use **rates per mile** and confidence bounds (6.1M miles supports S0/S1 signal, not rare S2/S3).

</details>

### 📖 Bayes Filter → Kalman/EKF foundations
**Reference Doc** · [source](https://docs.ufpr.br/~danielsantos/ProbabilisticRobotics.pdf)

*Bayes filter framing; Markov assumptions; KF/EKF live in Ch.3 (Gaussian filters)*

<details>
<summary>Key content</summary>

- **Belief (posterior) definition (Eq. 2.35):**  
  \[
  bel(x_t)=p(x_t\mid z_{1:t},u_{1:t})
  \]
  where \(x_t\)=state at time \(t\), \(z_t\)=measurement, \(u_t\)=control.
- **Prediction belief (Eq. 2.36):**  
  \[
  \overline{bel}(x_t)=p(x_t\mid z_{1:t-1},u_{1:t})
  \]
- **Markov/conditional independence assumptions:**  
  **State transition (Eq. 2.33):**  
  \[
  p(x_t\mid x_{0:t-1},z_{1:t-1},u_{1:t})=p(x_t\mid x_{t-1},u_t)
  \]
  **Measurement model (Eq. 2.34):**  
  \[
  p(z_t\mid x_{0:t},z_{1:t-1},u_{1:t})=p(z_t\mid x_t)
  \]
  These define a **DBN/HMM** with transition \(p(x_t\mid x_{t-1},u_t)\) and sensor model \(p(z_t\mid x_t)\) plus initial \(p(x_0)\).
- **Bayes rule (Eq. 2.15):**  
  \[
  p(x\mid y)=\eta\,p(y\mid x)p(x)
  \]
  (\(\eta\)=normalizer independent of \(x\)).
- **Total probability (Eq. 2.11–2.12):**  
  \[
  p(x)=\sum_y p(x\mid y)p(y)\quad\text{or}\quad p(x)=\int p(x\mid y)p(y)\,dy
  \]
- **Gaussian PDF (Eq. 2.4):**  
  \[
  \mathcal N(x;\mu,\Sigma)=\det(2\pi\Sigma)^{-1/2}\exp\{-\tfrac12(x-\mu)^T\Sigma^{-1}(x-\mu)\}
  \]
  (basis for KF/EKF in **Chapter 3**).

</details>

### 📖 ROS 2 QoS Policies + Standard Profiles (Iron)
**Reference Doc** · [source](https://docs.ros.org/en/iron/Concepts/Intermediate/About-Quality-of-Service-Settings.html)

*ROS 2 QoS policy definitions + predefined QoS profiles (defaults for pub/sub, services, sensor data, parameters) and compatibility rules.*

<details>
<summary>Key content</summary>

- **QoS = profile of policies** applied per publisher/subscription/service client/server; **incompatible QoS can prevent any message delivery**.
- **Core QoS policies (definitions):**
  - **History:** *Keep last* (store up to **N** samples) vs *Keep all* (store all, limited by middleware resources).
  - **Depth:** queue size **N**, **only honored if History=Keep last**.
  - **Reliability:** *Best effort* (may drop) vs *Reliable* (guaranteed delivery; may retry).
  - **Durability:** *Transient local* (publisher persists samples for late joiners) vs *Volatile* (no persistence).
  - **Deadline:** expected max time between publishes.
  - **Lifespan:** max time from publish to receive before message is **stale**; expired messages **silently dropped**.
  - **Liveliness:** *Automatic* vs *Manual by topic* (publisher must assert alive via API).
  - **Lease duration:** max time allowed without liveliness assertion before considered lost.
- **Default pub/sub profile (ROS 1–like):** History=Keep last, **Depth=10**, Reliability=Reliable, Durability=Volatile, Liveliness=System default; Deadline/Lifespan/Lease duration = Default (unspecified).
- **Services profile rationale:** **Reliable + Volatile** (avoid restarted servers receiving **outdated requests**; client protected from multiple responses, server not protected from side-effects).
- **Sensor data profile rationale:** prioritize timeliness over completeness → **Best effort** + **smaller queue** (than default).
- **Parameters profile:** like services but **much larger depth** to avoid losing requests when client can’t reach server.
- **Compatibility model (Request vs Offered):** subscriber requests “minimum acceptable”; publisher offers “maximum provided”; connect only if **every policy** requested is **not more stringent** than offered.
  - **Reliability compatibility (Pub→Sub):** BE→BE Yes; BE→Reliable **No**; Reliable→BE Yes; Reliable→Reliable Yes.
  - **Durability compatibility:** Volatile→Transient local **No**; Transient local→Transient local Yes (**new+old**); Transient local→Volatile Yes (**new only**). **Latched behavior requires both sides Transient local.**
  - **Deadline/Lease duration:** Default→x **No**; x→Default Yes; x→y compatible iff **y ≥ x**.
  - **Liveliness:** Automatic→Manual **No**; Manual→Automatic Yes.
- **QoS events:** offered/requested deadline missed, liveliness lost/changed, offered/requested incompatible QoS; plus **matched events** on connect/disconnect.

</details>

### 📋 # Source: https://github.com/TheGreatGalaxy/sensor-fusion
**Source** · 

### 🔍 Waymo Safety Case (AUR) structure + evidence credibility
**Explainer** · [source](https://assets.ctfassets.net/e6t5diu0txbw/66jOjPtNIjzawaK0ZjpU3q/7f081b392cf29a3355c97d0d758fe6cf/Waymo_Safety_Case_Approach.pdf)

*Safety-case structure: hazard/risk framing, safety argumentation, evidence types (simulation + on-road) for deployment*

<details>
<summary>Key content</summary>

- **Safety case definition (UL 4600:2022):** “Structured argument, supported by a body of evidence… that a system is safe for a given application in a given environment.”
- **Top-level goal:** **Absence of Unreasonable Risk (AUR)**; treated as a **risk assessment** problem requiring explicit **Acceptance Criteria (AC)** + **Validation Targets** (ISO 21448:2022; ISO/AWI TS 5083).
- **Key formula (risk):**  
  **Risk = P(harm) × Severity(harm)** (ISO 26262:2018 framing).  
  Variables: **P(harm)** probability of harm; **Severity(harm)** magnitude of harm.
- **Hazard decomposition (Section 2.2):** pin residual risk to 3 hazard categories:  
  1) **Architectural** (e.g., sensor placement blindspots)  
  2) **Behavioral** (e.g., unsafe proximity / driving behavior)  
  3) **In-service operational** (e.g., cargo securement, malicious access)
- **Causal chain framing (Section 2.2.1):** scenario triggering conditions → hazardous causal element/behavior → hazard manifestation → harm; risk influenced by **exposure** + **controllability** (ISO concepts).
- **Behavioral AC framework = 5D coverage space (Section 2.3):**  
  1) **Severity potential** (injury severity; AIS scale **1–6**)  
  2) **Conflict role** (ADS as **initiator** vs **responder**)  
  3) **Behavioral capability**: **regulatory compliance**, **conflict avoidance**, **collision avoidance**  
  4) **ADS functionality status**: **nominal** vs **degraded**  
  5) **Level of aggregation**: **event-level** + **aggregate-rate** ACs (use both; aggregates alone can miss rare scenario risks)
- **Safety determination lifecycle (Section 3.1):** (1) safety-by-design development → (2) readiness review using **on-road data (10+ years)** + **simulation** + expert judgment; failures to meet targets delay approval → (3) post-deploy monitoring for continuous confidence growth.
- **Credibility structuring (Section 4 overview):** **Case Credibility Assessment (CCA)** = credibility of **argument** (top-down) + credibility of **evidence** (bottom-up) + implementation credibility check.

</details>

---

## Related Topics

- [[topics/physics-simulation|Physics Simulation]]
- [[topics/robot-manipulation|Robot Manipulation]]
- [[topics/reinforcement-learning|Reinforcement Learning]]
