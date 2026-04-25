---
title: "Reinforcement Learning"
subject: "Physical AI & Robotics"
date: 2026-04-06
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

# Reinforcement Learning

## Video (best)
- **Pieter Abbeel (UC Berkeley)** — "Deep Reinforcement Learning" (CS285 Lecture 1 / intro lecture)
- **Watch:** [YouTube](https://www.youtube.com/watch?v=2GwTxsAcmJQ)
- Why: Abbeel is one of the foremost RL educators; the CS285 series systematically builds from MDPs through policy gradients to modern deep RL methods including PPO and SAC, covering the full conceptual arc needed for physical AI and multimodal applications. The lecture style balances intuition with mathematical rigor.
- Level: intermediate

> **Note:** The CS285 (Deep RL) playlist from UC Berkeley is the gold-standard lecture series. The specific video ID above should be verified against the current YouTube upload. The playlist URL `https://www.youtube.com/playlist?list=PL_iWQOsE6TfURIIhCrlt-wj9ByIVpbfGc` is well-established.

---

## Blog / Written explainer (best)
- **Lilian Weng** — "A (Long) Peek into Reinforcement Learning"
- **Link:** [https://lilianweng.github.io/posts/2018-02-19-rl-overview/](https://lilianweng.github.io/posts/2018-02-19-rl-overview/)
- Why: Lilian Weng's post is the definitive written survey for practitioners entering RL. It covers MDPs, value functions, policy gradients, actor-critic methods, and model-based RL in a single coherent narrative with clean notation. Her follow-up posts on PPO and SAC extend this foundation directly into the related concepts listed.
- Level: intermediate

---

## Deep dive
- **Lilian Weng** — "Policy Gradient Algorithms" (comprehensive technical reference covering REINFORCE, A3C, PPO, SAC, and reward shaping)
- **Link:** [https://lilianweng.github.io/posts/2018-04-08-policy-gradient/](https://lilianweng.github.io/posts/2018-04-08-policy-gradient/)
- Why: This post is the most thorough single-document treatment of the policy gradient family — the algorithmic backbone of modern RL for locomotion and physical AI. It derives each algorithm from first principles, shows the connections between them, and includes reward shaping discussion. Pairs directly with the related concepts (PPO, SAC, policy gradient) listed for this topic.
- Level: advanced

---

## Original paper
- **Schulman et al. (2017)** — "Proximal Policy Optimization Algorithms"
- **Link:** [https://arxiv.org/abs/1707.06347](https://arxiv.org/abs/1707.06347)
- Why: PPO is the dominant practical RL algorithm used in physical AI, robotics locomotion, and RLHF for multimodal models. This paper is unusually readable for a seminal work — short, clearly motivated, and directly applicable. It represents the convergence point of the policy gradient thread and is the algorithm students will encounter most in real deployments.
- Level: advanced

---

## Code walkthrough
- **CleanRL** — "PPO Implementation Walkthrough" (single-file, heavily annotated PPO implementation)
- **Link:** [https://docs.cleanrl.dev/rl-algorithms/ppo/](https://docs.cleanrl.dev/rl-algorithms/ppo/)
- Why: CleanRL's philosophy of single-file, fully annotated implementations is pedagogically superior to framework-heavy alternatives. Every design decision is explained inline. The PPO walkthrough covers discrete and continuous action spaces (relevant to locomotion), includes W&B logging, and has a companion paper. This is the resource most likely to bridge theory → working code for learners in physical AI contexts.
- Level: intermediate

---

## Coverage notes
- **Strong:** Policy gradient theory (PPO, SAC), written explainers (Lilian Weng's blog is exceptional), practical implementation (CleanRL)
- **Weak:** World models and perception-prediction-planning as a unified RL framework — most resources treat these separately; no single resource covers the full end-to-end learning pipeline from raw perception through planning to control
- **Gap:** No single excellent YouTube video exists that specifically connects RL to multimodal/physical AI contexts (locomotion + world models + end-to-end learning together). The CS285 series is the closest but requires watching multiple lectures. A dedicated explainer on reward shaping for robotics locomotion specifically is also absent from top-tier educators.

---

## Cross-validation
This topic appears in 2 courses: **intro-to-multimodal**, **intro-to-physical-ai**

- For `intro-to-physical-ai`: the locomotion, SAC, PPO, and end-to-end learning concepts are central — CleanRL + CS285 + PPO paper form a strong trio
- For `intro-to-multimodal`: the world models and perception-prediction-planning angle is less well served by existing resources; instructors may need to supplement with the Dreamer/DreamerV3 paper (`https://arxiv.org/abs/2301.04104`) for the world models thread

---

---

## Additional Resources for Tutor Depth

> **10 sources** — papers, official docs, working code, benchmarks, and deep explainers that give the AI tutor precision on this topic.

### 📄 Deep RL Reproducibility & Variance (Henderson et al., 2017/2019)
**Paper** · [source](https://arxiv.org/abs/1709.06560)

*Quantified variance/reproducibility findings (seed + hyperparameter sensitivity) and recommended reporting practices for RL benchmarks*

<details>
<summary>Key content</summary>

- **Core problem (Abstract):** Reported deep RL results are hard to interpret because of (i) **non-determinism in benchmark environments** and (ii) **intrinsic variance** of deep RL methods; without **significance metrics** and **standardized reporting**, “improvements” over SOTA may be meaningless.
- **Algorithms examined (Summary/Body):** Continuous-control, policy-gradient family methods: **TRPO, DDPG, PPO, ACKTR** (MuJoCo-style benchmarks).
- **Empirical variability factors (Summary):**
  - **Random seeds:** Same algorithm + same hyperparameters can yield **drastically different outcomes** across seeds → single-run comparisons are unreliable.
  - **Hyperparameters / architecture:** Small changes (e.g., **activation function: ReLU vs tanh vs Leaky ReLU**) can cause **substantial performance differences**, inconsistently across tasks/algorithms.
  - **Reward scaling (DDPG):** Reward scaling can have **profound effects**; arbitrary rescaling can mislead comparisons.
  - **Environment dependence:** No method dominates across tasks (example given: **DDPG strong on HalfCheetah, weak on Hopper**).
  - **Codebase discrepancies:** Different implementations of the “same” algorithm (e.g., **DDPG, TRPO**) can produce **significantly different performance**.
- **Recommended evaluation/reporting practices (Summary):**
  - Run **multiple trials with different random seeds**; report **mean performance** (not a single best run).
  - Report **all hyperparameters + implementation details** (network, activations, reward scaling, etc.).
  - Use **statistical significance metrics**: bootstrap confidence intervals; tests mentioned include **2-sample t-test** and **Kolmogorov–Smirnov**.

</details>

### 📄 Learning by Cheating (LBC) for Vision Driving
**Paper** · [source](https://arxiv.org/abs/1912.12294)

*Two-stage autonomous driving pipeline: privileged “cheating” teacher in sim → vision-policy distillation; observation/action design + training rationale*

<details>
<summary>Key content</summary>

- **Two-stage procedure (Fig. 1):**
  1) Train **privileged agent** with access to ground-truth state/map to **imitate expert** trajectories (behavior cloning).  
  2) Train **sensorimotor (vision) agent** to **imitate privileged agent**, using (i) offline cloning + (ii) **on-policy** oracle supervision (DAgger-style), plus **white-box multi-branch** supervision over all commands.
- **Inputs/observations:**
  - Sensorimotor policy input: monocular RGB image **I**, speed **v**, high-level command **c** ∈ {follow-lane, turn-left, turn-right, go-straight}.  
  - Privileged policy additionally sees **map** \(M \in \{0,1\}^{W\times H\times 7}\): road, lane boundaries, vehicles, pedestrians, traffic lights (green/yellow/red), anchored at ego.
- **Action representation:** both policies predict **K future waypoints** in ego frame; low-level control via PID.
  - Ground-truth waypoint construction:  
    \[
    w_t=\{R_t^{-1}(x_{t+1}-x_t),\dots,R_t^{-1}(x_{t+K}-x_t)\}
    \]
    where \(x_t\)=position, \(R_t\)=orientation.
- **Privileged BC objective (Section 2.1):**
  \[
  \min_\theta \ \mathbb{E}_{(M,v,c,w)\sim\tau}\big[\|w-f^*_\theta(M,v)_c\|_1\big]
  \]
- **Augmentation rationale:** simulate trajectory noise **offline** by **random rotation + shift** of \(M\) and applying same transform to waypoints (Fig. 3b) → recovery from perturbed poses.
- **Sensorimotor imitation loss (Section 2.2):**
  \[
  \min_\theta \ \mathbb{E}_{(M,I,v)\sim D}\big[\|T_P(f(I,v)) - f^*_\theta(M,v)\|_1\big]
  \]
  \(T_P\): closed-form transform from predicted image-space waypoints to privileged/map frame.
- **Controller details:** brake if predicted \(v^*<\varepsilon\), with **\(\varepsilon=2.0\) km/h**; lateral control fits a circular arc to waypoints and steers to point \(p\): \(s^*=\tan^{-1}(p_y/p_x)\).
- **Vision input/output sizes + aug:** image **384×160 RGB** → heatmaps **96×40**; augment by rotation **[-5°, 5°]** and horizontal shift **[-5, 5] px** (~**1 m**).
- **Key empirical results:** achieves **100% success** on all tasks in original CARLA benchmark; on NoCrash (test town) reaches **100%** in “Empty” and **≥85%** in other traffic conditions; reduces infractions by **≥10×** vs prior SOTA (e.g., CILRS).

</details>

### 📄 PPO (Clipped Objective + KL Penalty) Core Equations
**Paper** · [source](https://arxiv.org/abs/1707.06347v2)

*Canonical PPO math: clipped surrogate objective, KL-penalty variant, combined actor-critic loss, and update workflow (multiple epochs/minibatches)*

<details>
<summary>Key content</summary>

- **Policy gradient estimator (Eq. 1) & objective (Eq. 2):**  
  \[
  \hat g=\hat{\mathbb E}_t\left[\nabla_\theta \log \pi_\theta(a_t|s_t)\,\hat A_t\right],\quad
  L^{PG}(\theta)=\hat{\mathbb E}_t\left[\log \pi_\theta(a_t|s_t)\,\hat A_t\right]
  \]
  where \(\hat{\mathbb E}_t\) is empirical average over a batch; \(\hat A_t\) advantage estimate.
- **TRPO surrogate + KL constraint (Eq. 3–4):**  
  maximize \(\hat{\mathbb E}_t\left[\frac{\pi_\theta(a_t|s_t)}{\pi_{\theta_{old}}(a_t|s_t)}\hat A_t\right]\)  
  s.t. \(\hat{\mathbb E}_t[KL(\pi_{\theta_{old}}(\cdot|s_t),\pi_\theta(\cdot|s_t))]\le \delta\).
- **Probability ratio definition (Section 3):**  
  \[
  r_t(\theta)=\frac{\pi_\theta(a_t|s_t)}{\pi_{\theta_{old}}(a_t|s_t)},\quad r_t(\theta_{old})=1
  \]
- **CPI surrogate (Eq. 6):** \(L^{CPI}(\theta)=\hat{\mathbb E}_t[r_t(\theta)\hat A_t]\).
- **PPO clipped surrogate (Eq. 7, main PPO objective):**  
  \[
  L^{CLIP}(\theta)=\hat{\mathbb E}_t\left[\min\left(r_t(\theta)\hat A_t,\; \text{clip}(r_t(\theta),1-\epsilon,1+\epsilon)\hat A_t\right)\right]
  \]
  Default cited: \(\epsilon=0.2\). Rationale: removes incentive to push \(r_t\) outside \([1-\epsilon,1+\epsilon]\); min makes a pessimistic (lower-bound) surrogate.
- **KL-penalty objective (Eq. 8):**  
  \[
  L^{KLPEN}(\theta)=\hat{\mathbb E}_t\left[r_t(\theta)\hat A_t-\beta\, KL(\pi_{\theta_{old}}(\cdot|s_t),\pi_\theta(\cdot|s_t))\right]
  \]
  **Adaptive \(\beta\) (Section 4):** compute \(d=\hat{\mathbb E}_t[KL(\cdot)]\). If \(d<d_{targ}/1.5\Rightarrow \beta\leftarrow \beta/2\); if \(d>d_{targ}\times1.5\Rightarrow \beta\leftarrow 2\beta\).
- **Combined actor-critic + entropy (Eq. 9):**  
  \[
  L^{CLIP+VF+S}(\theta)=\hat{\mathbb E}_t\left[L^{CLIP}_t(\theta)-c_1 L^{VF}_t(\theta)+c_2 S[\pi_\theta](s_t)\right]
  \]
  with \(L^{VF}_t=(V_\theta(s_t)-V^{targ}_t)^2\); \(S\) entropy bonus.
- **Advantage estimators (Eq. 10–12):** truncated return-style (Eq. 10) and truncated GAE (Eq. 11)  
  \[
  \hat A_t=\delta_t+(\gamma\lambda)\delta_{t+1}+\cdots+(\gamma\lambda)^{T-t+1}\delta_{T-1},\quad
  \delta_t=r_t+\gamma V(s_{t+1})-V(s_t)
  \]
- **Training workflow (Section 5 / Algorithm 1):** collect \(T\) steps from each of \(N\) parallel actors \(\Rightarrow NT\) samples; optimize surrogate with minibatch SGD/Adam for \(K\) epochs (enables multiple epochs per batch).
- **Empirical numbers (Table 1 excerpt):** adaptive KL penalty: \(d_{targ}=0.01\Rightarrow 0.74\) avg normalized score; \(d_{targ}=0.03\Rightarrow 0.71\). Fixed KL: \(\beta=0.3\Rightarrow 0.62\); \(\beta=1\Rightarrow 0.71\); \(\beta=3\Rightarrow 0.72\); \(\beta=10\Rightarrow 0.69\). (Clipped objective reported as best-performing variant in experiments.)

</details>

### 📄 PPO clipped objective + KL penalty + pseudocode
**Paper** · [source](https://arxiv.org/abs/1707.06347)

*Clipped surrogate objective (min of unclipped/clipped ratios), KL-penalty variant, full pseudocode, TRPO connection, typical use with GAE*

<details>
<summary>Key content</summary>

- **Vanilla policy gradient estimator** (Eq. 1–2):  
  \[
  \hat g=\hat{\mathbb E}_t[\nabla_\theta \log \pi_\theta(a_t|s_t)\,\hat A_t],\quad
  L^{PG}(\theta)=\hat{\mathbb E}_t[\log \pi_\theta(a_t|s_t)\,\hat A_t]
  \]
  where \(\hat{\mathbb E}_t\) is empirical average over a batch; \(\hat A_t\) advantage estimate.
- **TRPO constrained surrogate** (Eq. 3–4):  
  maximize \(\hat{\mathbb E}_t\!\left[\frac{\pi_\theta(a_t|s_t)}{\pi_{\theta_{old}}(a_t|s_t)}\hat A_t\right]\)  
  s.t. \(\hat{\mathbb E}_t[KL(\pi_{\theta_{old}}(\cdot|s_t),\pi_\theta(\cdot|s_t))]\le \delta\).
- **TRPO penalty form** (Eq. 5):  
  \[
  \max_\theta \hat{\mathbb E}_t\!\left[\frac{\pi_\theta}{\pi_{\theta_{old}}}\hat A_t-\beta\, KL(\pi_{\theta_{old}},\pi_\theta)\right]
  \]
- **Probability ratio** (Section 3): \(r_t(\theta)=\frac{\pi_\theta(a_t|s_t)}{\pi_{\theta_{old}}(a_t|s_t)}\), with \(r_t(\theta_{old})=1\).
- **Clipped surrogate objective** (Section 3):  
  \[
  L^{CLIP}(\theta)=\hat{\mathbb E}_t\Big[\min\big(r_t(\theta)\hat A_t,\; \text{clip}(r_t(\theta),1-\epsilon,1+\epsilon)\hat A_t\big)\Big]
  \]
  Rationale: removes incentive to push \(r_t\) outside \([1-\epsilon,1+\epsilon]\); min makes a **pessimistic/lower-bound** surrogate.
- **Adaptive KL penalty** (Section 4): optimize \(L^{KLPEN}\) (above) and adapt \(\beta\) to hit target KL \(d_{targ}\); heuristic multipliers **2** and **1.5** used for adjusting \(\beta\).
- **Full PPO loss with value + entropy** (Eq. 9):  
  \[
  L^{CLIP+VF+S}(\theta)=\hat{\mathbb E}_t\left[L^{CLIP}_t(\theta)-c_1 L^{VF}_t(\theta)+c_2 S[\pi_\theta](s_t)\right]
  \]
  with \(L^{VF}_t=(V_\theta(s_t)-V^{targ}_t)^2\).
- **GAE-style advantage recursion** (Eq. 11–12): \(\delta_t=r_t+\gamma V(s_{t+1})-V(s_t)\); advantages computed from \(\delta_t\) with discount \(\gamma\) and parameter \(\lambda\).
- **Procedure (Section 5 pseudocode):** collect \(T\) steps from each of \(N\) parallel actors using \(\pi_{\theta_{old}}\); compute returns/advantages; then do **multiple epochs** of minibatch SGD/Adam on \(L^{CLIP}\) (or \(L^{KLPEN}\)), plus value/entropy terms if used.
- **Defaults / reported settings:** common clip \(\epsilon=0.2\) (continuous-control experiments). Policy MLP: **2 hidden layers, 64 units, tanh**, Gaussian mean output with learned std (Section 6.1).
- **Empirical note:** in continuous control, “no clipping or penalty” can be catastrophically bad (Table 1 mentions HalfCheetah causing very negative score); fixed KL penalty example row: **β=10 → avg normalized score 0.69** (Table 1).

</details>

### 📄 Sim-to-real RL for ANYmal agile locomotion
**Paper** · [source](https://arxiv.org/abs/1901.08652)

*Real-robot deployment details: sim-to-real training (dynamics randomization + learned actuator), control stack integration, real-world metrics*

<details>
<summary>Key content</summary>

- **RL objective (Eq. 1):** maximize discounted return  
  \[
  \max_\pi \; \mathbb{E}_{\tau\sim p(\tau|\pi)}\Big[\sum_{t=0}^{\infty}\gamma^t r_t\Big]
  \]
  where \(\pi(a_t|o_{t-k:t})\) is a stochastic policy over actions given recent observation history; \(\gamma\) discount; \(\tau\) trajectory.
- **Control I/O (Method: Observation & action):**
  - Observations: joint angles, joint velocities, body twist; uses **history window** of recent states.
  - Actions: **joint position targets** (sent to actuators).
- **Sim-to-real pipeline (Fig. 1, Method):**
  1) Fast rigid-body sim with **hard contact** solver respecting Coulomb friction cone; ~**900,000 sim steps/s** on desktop.  
  2) **Learned actuator model** via supervised learning: network predicts joint torque from history of **position errors** (measured − commanded) and velocities; uses current + **two past states**.  
  3) Train policy in sim with RL (**TRPO** with default params); ~**0.25B transitions in ~4 hours**; runs on **1 CPU + 1 GPU**, each session **<11 hours**.
  4) **Curriculum**: multiplicative curriculum factor increases with iteration to ramp cost weights/disturbances.
  5) Episode length **6 s**; terminate on **joint limit violation** or **base hits ground**; init state sampled 50/50 from previous trajectory vs random distribution.
- **Actuator-data collection:** sine-wave foot trajectories (IK to joint targets); amplitude **5–10 cm**, frequency **1–25 Hz**; manual disturbances; must excite broad frequency spectrum to avoid oscillations.
- **Real-robot results (ANYmal):**
  - Random command tracking (30 s, new cmd every **2 s**): avg linear vel error **0.143 m/s**, yaw-rate error **0.174 rad/s**.
  - Step speed commands (0.25/0.5/0.75/1.0 m/s): avg velocity error **2.2%** real; **1.1%** higher than sim.
  - Efficiency: **23–36% less torque** vs prior gaits; straighter knees by **10–15°**.
  - High-speed: command 1.6 m/s → **1.5 m/s** real (1.58 sim); hits hardware limits **40 Nm** torque, **12 rad/s** joint speed; **25%** faster than previous ANYmal record.
  - Fall recovery: **9/9** random configurations successful on hardware; improved to **100%** after relaxing joint-velocity constraints; successful on **first hardware attempt**.
- **Recovery training init:** drop from **1.0 m**, random orientation/joints, simulate **1.2 s**, use resulting state; randomize collision body sizes/positions (filter unrealistic internal collisions); model has **41 collision bodies**.

</details>

### 📄 Soft Actor-Critic (SAC) core equations & losses
**Paper** · [source](https://proceedings.mlr.press/v80/haarnoja18b/haarnoja18b.pdf)

*Soft Bellman backup + exact SAC losses (critic/value/policy), reparameterization gradient, temperature α role*

<details>
<summary>Key content</summary>

- **Max-entropy RL objective (Eq. 1):**  
  \(J(\pi)=\sum_{t=0}^{T}\mathbb{E}_{(s_t,a_t)\sim\rho_\pi}\big[r(s_t,a_t)+\alpha\,\mathcal{H}(\pi(\cdot|s_t))\big]\).  
  α trades off reward vs entropy; standard RL recovered as \(\alpha\to 0\) (Sec. 3.2).
- **Soft policy evaluation backup (Eq. 2–3):**  
  \( \mathcal{T}^\pi Q(s_t,a_t)= r(s_t,a_t)+\gamma\,\mathbb{E}_{s_{t+1}\sim p}[V(s_{t+1})]\).  
  \( V(s_t)=\mathbb{E}_{a_t\sim\pi}[Q(s_t,a_t)-\log\pi(a_t|s_t)]\).
- **Soft policy improvement as KL projection (Eq. 4):**  
  \(\pi_{\text{new}}=\arg\min_{\pi'\in\Pi} D_{KL}\!\left(\pi'(\cdot|s_t)\,\|\,\frac{\exp(Q^{\pi_{\text{old}}}(s_t,\cdot))}{Z_{\pi_{\text{old}}}(s_t)}\right)\).
- **Practical SAC losses (Sec. 4.2):** with replay buffer \(D\), networks \(V_\psi, Q_\theta, \pi_\phi\).  
  **Value loss (Eq. 5):**  
  \(J_V(\psi)=\mathbb{E}_{s_t\sim D}\Big[\tfrac12\big(V_\psi(s_t)-\mathbb{E}_{a_t\sim\pi_\phi}[Q_\theta(s_t,a_t)-\log\pi_\phi(a_t|s_t)]\big)^2\Big]\).  
  **Q loss (Eq. 7–8):**  
  \(J_Q(\theta)=\mathbb{E}_{(s_t,a_t)\sim D}\big[\tfrac12(Q_\theta(s_t,a_t)-\hat Q(s_t,a_t))^2\big]\),  
  \(\hat Q=r(s_t,a_t)+\gamma\,\mathbb{E}_{s_{t+1}\sim p}[V_{\bar\psi}(s_{t+1})]\) using target value net \(V_{\bar\psi}\).
  **Policy objective (Eq. 10, 12):** minimize  
  \(J_\pi(\phi)=\mathbb{E}_{s_t\sim D}\!\left[D_{KL}\!\left(\pi_\phi(\cdot|s_t)\,\|\,\frac{\exp(Q_\theta(s_t,\cdot))}{Z_\theta(s_t)}\right)\right]\)  
  ⇒ via reparameterization \(a_t=f_\phi(\epsilon_t;s_t)\) (Eq. 11):  
  \(J_\pi(\phi)=\mathbb{E}_{s_t\sim D,\epsilon_t\sim\mathcal N}\big[\log\pi_\phi(f_\phi(\epsilon_t;s_t)|s_t)-Q_\theta(s_t,f_\phi(\epsilon_t;s_t))\big]\) (Eq. 12).  
  Gradient estimator given in Eq. 13.
- **Algorithm 1 workflow:** collect env transitions into replay \(D\); do gradient steps on \(J_V, J_Q\) (two Qs \(\theta_1,\theta_2\) to reduce positive bias), and \(J_\pi\); update target value params by EMA: \(\bar\psi \leftarrow \tau\psi+(1-\tau)\bar\psi\).
- **Defaults/empirical notes:** uses **two Q-functions** (Sec. 4.2). Target smoothing coefficient used across tasks: **\(\tau=0.005\)** (Sec. 5.2). Reward scaling acts like inverse temperature; sensitive (Sec. 5.2). Deterministic evaluation uses mean action (Sec. 5.2).

</details>

### 📄 Soft Actor-Critic (SAC) — max-entropy objective + α auto-tuning
**Paper** · [source](https://arxiv.org/abs/1812.05905)

*Automatic entropy-temperature tuning objective (α optimization to match target entropy) + consolidated SAC algorithm variants*

<details>
<summary>Key content</summary>

- **Maximum-entropy RL objective (Eq. 1):**  
  \[
  J(\pi)=\sum_{t=0}^{T-1}\mathbb{E}_{(s_t,a_t)\sim \rho_\pi}\big[r(s_t,a_t)+\alpha\,\mathcal{H}(\pi(\cdot|s_t))\big]
  \]  
  where \(\mathcal{H}(\pi(\cdot|s))=\mathbb{E}_{a\sim\pi}[-\log \pi(a|s)]\); \(\alpha\) trades off reward vs entropy (as \(\alpha\to 0\), recovers standard RL).
- **Soft Bellman equations (Eq. 2–3):**  
  \[
  Q^\pi(s_t,a_t)=r(s_t,a_t)+\gamma\,\mathbb{E}_{s_{t+1}\sim p}\big[V^\pi(s_{t+1})\big]
  \]
  \[
  V^\pi(s_t)=\mathbb{E}_{a_t\sim\pi}\big[Q^\pi(s_t,a_t)-\log \pi(a_t|s_t)\big]
  \]
- **Soft policy improvement as KL projection (Eq. 6):**  
  \[
  \pi_{\text{new}}=\arg\min_{\pi'\in\Pi}D_{KL}\Big(\pi'(\cdot|s_t)\,\Big\|\,\exp(Q^{\pi_{\text{old}}}(s_t,\cdot)-\log Z(s_t))\Big)
  \]
  (improves soft Q everywhere; Lemma 2).
- **Practical SAC training loop (Algorithm 2, Sec. 4.2):** alternate (i) collect transitions with current stochastic policy into replay buffer \(D\); (ii) sample minibatches from \(D\) for **off-policy** SGD updates of value/Q/policy networks.
- **Stability design choices:** (i) **stochastic actor + entropy maximization** improves exploration/robustness; (ii) **two Q-functions** and use \(\min(Q_{\theta_1},Q_{\theta_2})\) to reduce positive bias (Sec. 4.2; Hasselt/TD3 rationale); (iii) separate \(V_\psi(s)\) network often stabilizes training.
- **Empirical comparisons (Sec. 5):** SAC reported to outperform DDPG and PPO on harder continuous-control benchmarks; notably stable across random seeds (curves shown in Fig. 1).

</details>

### 📊 Benchmark details & normalized-score procedure (PIC/POIC paper)
**Benchmark** · [source](http://proceedings.mlr.press/v139/furuta21a/furuta21a-supp.pdf)

*Supplementary benchmark tables/plots + experimental settings for reproducible Gym/MuJoCo/DMControl comparisons (SAC/MPO/AWR + leaderboard baselines), plus reward-shaping and noise-tuning setups.*

<details>
<summary>Key content</summary>

- **Environment specs (Table 2):**  
  Ant-v2 state 111, action 8, horizon 1000; HalfCheetah-v2 state 17, action 6, horizon 1000; Hopper-v2 state 11, action 3, horizon 1000; Walker2d-v2 state 17, action 6, horizon 1000; Humanoid-v2 state 376, action 17, horizon 1000. (Also classic control + DMControl tasks listed.)
- **Reward equations (Appendix A):**  
  Pendulum: \(r_t=-(\phi_t^2+0.1\dot\phi_t^2+0.001\|a_t\|_2^2)\).  
  HalfCheetah: \(r_t=\dot x_t-0.1\|a_t\|_2^2\).  
  Hopper/Walker2d: \(r_t=\dot x_t-0.01\|a_t\|_2^2+1\).  
  Ant: \(r_t=\dot x_t-0.5\|a_t\|_2^2-0.0005\|s^{contact}_t\|_2^2+1\).  
  Humanoid: \(r_t=1.25\dot x_t-0.1\|a_t\|_2^2-\min(5\!\times\!10^{-7}\|s^{contact}_t\|_2^2,10)+5\).
- **Algorithm-based normalized score (Appendix C):**  
  \[
  \text{NormScore}=\frac{r^{algo}_{avg}-r^{rand}_{min}}{\max(r^{rand}_{max},r^{algo}_{max})-r^{rand}_{min}}
  \]
  where \(r^{algo}_{avg}\)=avg return over an algorithm set; \(r^{algo}_{max}\)=best algorithm return; \(r^{rand}_{min},r^{rand}_{max}\)=min/max from random policy sampling.
- **MuJoCo training budgets (Appendix C.1.2):** SAC/MPO/AWR averaged over **10 seeds**; train **1M steps (Hopper)**, **3M (Ant/HalfCheetah/Walker2d)**, **10M (Humanoid)**.
- **MuJoCo baseline numbers:**  
  Table 5 (10-seed): SAC Ant **5526.4**, HalfCheetah **15266.5**, Hopper **2948.9**, Walker2d **5771.8**, Humanoid **8264.0**; MPO Ant **6584.2**; AWR Hopper **3084.7**.  
  Table 4 (aggregated): average/max scores—Ant **2450.8/6584.2**, HalfCheetah **6047.2/15266.5**, Hopper **2206.7/3564.1**, Walker2d **3190.8/5813.0**, Humanoid **3880.8/8264.0**.
- **DMControl (500k steps, 10 seeds):** Table 9 SAC cheetah run **536.0**, reacher easy **961.2**, ball in cup catch **971.9**; Table 8 aggregated avg/max: cheetah run **474.4/795.0**, reacher easy **691.5/961.2**, ball in cup catch **751.7/978.2**.
- **Reward shaping families (Appendix G):**  
  L1: \(r=-\alpha\|s-s_g\|_1\); L2: \(r=-\alpha\|s-s_g\|_2\); Fraction: \(r=\frac{\beta}{\gamma+\|s-s_g\|_2}\); Sparse: \(r=-\mathbf{1}[\|s-s_g\|_2\ge \epsilon]\). PPO trained **500k steps**, **5 seeds**, scores normalized for reward-scale comparability.

</details>

### 📊 Tianshou MuJoCo Benchmark (SAC example + suite contents)
**Benchmark** · [source](https://github.com/ChenDRAG/mujoco-benchmark)

*Concrete MuJoCo returns (mean±std) under a single Tianshou benchmark + links to scripts/data/pretrained agents.*

<details>
<summary>Key content</summary>

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

</details>

### 📋 # Source: https://spinningup.openai.com/en/latest/spinningup/bench.html
**Source** ·

---

## Related Topics

- [[topics/rlhf-alignment|RLHF & Alignment]]
- [[topics/imitation-learning|Imitation Learning]]
- [[topics/robot-manipulation|Robot Manipulation]]
- [[topics/physical-ai-foundations|Physical AI Foundations]]
- [[topics/reasoning-models|Reasoning Models]]
