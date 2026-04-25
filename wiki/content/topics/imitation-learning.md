---
title: "Imitation Learning"
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

# Imitation Learning

## Video (best)
- **Sergey Levine (UC Berkeley CS285)** — "Imitation Learning" (CS285 Lecture 2)
- **Watch:** [YouTube](https://www.youtube.com/watch?v=zDvcNTVkDxk)
- Why: Levine's CS285 Deep RL course is the gold standard academic treatment. The imitation learning lecture covers behavior cloning, DAgger, distribution shift, and the compounding error problem with rigorous mathematical grounding — exactly the conceptual scaffolding learners need before tackling IRL and GAIL.
- Level: intermediate/advanced

## Blog / Written explainer (best)
- **Lilian Weng** — "Imitation Learning Overview"
- **Link:** [https://lilianweng.github.io/posts/2018-04-08-policy-gradient/](https://lilianweng.github.io/posts/2018-04-08-policy-gradient/)
- Why: Lilian Weng's blog posts are renowned for combining intuitive explanation with mathematical precision. Her coverage of behavior cloning, DAgger, GAIL, and IRL in a single structured post makes it ideal for learners who want a map of the entire landscape before diving into papers.
- Level: intermediate

> ⚠️ **[VERIFY]** — Weng's exact IL post URL is uncertain. Her confirmed IL post may be at `https://lilianweng.github.io/posts/2018-04-08-policy-gradient/` or a dedicated imitation learning post. Check her blog index directly.

## Deep dive
- **Sergey Levine** — CS285 Course Notes / Slides on Imitation Learning
- **Link:** [https://rail.eecs.berkeley.edu/deeprlcourse/](https://rail.eecs.berkeley.edu/deeprlcourse/)
- Why: The CS285 lecture slides and notes provide the most comprehensive technical treatment available freely online — covering the formal problem setup, behavioral cloning failure modes (covariate shift), DAgger's theoretical guarantees, inverse RL formulations, and GAIL. Used in graduate-level RL courses worldwide.
- Level: advanced

## Original paper
- **Stéphane Ross, Geoffrey Gordon, Drew Bagnell** — "A Reduction of Imitation Learning and Structured Prediction to No-Regret Online Learning" (DAgger paper)
- **Link:** [https://arxiv.org/abs/1011.0686](https://arxiv.org/abs/1011.0686)
- Why: DAgger is the canonical algorithmic contribution that formally characterizes the distribution shift problem in behavior cloning and proposes a principled fix. It remains the most cited and pedagogically important paper in imitation learning — every serious treatment of the topic references it. Highly readable for an academic paper.
- Level: advanced

## Code walkthrough
- **None identified with high confidence**
- Why: No single widely-recognized hands-on IL code walkthrough (YouTube or blog) with verified existence stands out clearly. The closest candidates are:
  - The `imitation` library by CHAI/Adam Gleave: https://github.com/HumanCompatibleAI/imitation
  - Spinning Up by OpenAI covers related RL but not IL specifically.

> Recommend pairing the `imitation` library's documented examples with the CS285 lectures as a substitute until a dedicated walkthrough is identified.

---

## Coverage notes
- **Strong:** Behavior cloning fundamentals, DAgger algorithm, distribution shift problem, IRL vs. GAIL distinction — all well-covered in Levine's CS285 and Weng-style blog posts.
- **Weak:** Robotics-specific IL (RT-1, RT-2, SayCan, VLA models, affordance grounding) — these are cutting-edge topics with limited pedagogical video content; most resources are primary papers only.
- **Weak:** Teleoperation data collection pipelines and open-vocabulary manipulation — almost no beginner-friendly explainers exist; learners must go directly to papers (e.g., RT-2 arxiv).
- **Gap:** No high-quality 3Blue1Brown / Andrej Karpathy style visual explainer exists specifically for imitation learning. The best videos are graduate lecture recordings, which assume significant RL background.
- **Gap:** GAIL specifically lacks a standalone accessible explainer video — it is typically covered briefly within broader IL or GAN lectures.
- **Gap:** Code walkthrough — no single canonical hands-on tutorial analogous to Karpathy's nanoGPT exists for IL.

---

---

## Additional Resources for Tutor Depth

> **9 sources** — papers, official docs, working code, benchmarks, and deep explainers that give the AI tutor precision on this topic.

### 📄 DAgger = No-Regret Reduction for Imitation Learning
**Paper** · [source](https://proceedings.mlr.press/v15/ross11a.html)

*DAgger no-regret reduction and performance guarantee (dataset aggregation procedure + bound relating learned policy loss to online learning regret and expert loss).*

<details>
<summary>Key content</summary>

- **Problem setting (sequential prediction / imitation learning):** future observations depend on previous predictions/actions ⇒ i.i.d. supervised learning assumptions fail; leads to compounding errors under **distribution shift** (train on expert states, test on learner-induced states). (Abstract)
- **Core algorithm (DAgger; iterative dataset aggregation):**
  - Iterate training while collecting data from the **current learned policy’s induced state distribution**.
  - Query the **expert** for the correct action/label on visited states.
  - **Aggregate** all collected (state, expert-action) pairs across iterations into a growing dataset.
  - Train a **single stationary deterministic policy** on the aggregated dataset each iteration. (Abstract)
- **Reduction to online learning / no-regret view:**
  - Treat each iteration as an online learning round with loss defined on the states visited by the current policy.
  - If the underlying learner is **no-regret**, then the procedure “must find a policy with good performance under the distribution of observations it induces” in sequential settings. (Abstract)
- **Design rationale vs prior approaches:**
  - Avoids training **non-stationary** or **stochastic** policies.
  - Avoids requiring a **large number of iterations** compared to some earlier methods; aims for stronger guarantees in non-i.i.d. sequential prediction. (Abstract)
- **Empirical claim (no numbers in excerpt):** reported to outperform previous approaches on **two challenging imitation learning problems** and a **benchmark sequence labeling** task. (Abstract)

</details>

### 📄 DAgger no-regret reduction (Ross et al., AISTATS’11)
**Paper** · [source](https://www.ri.cmu.edu/pub_files/2011/4/Ross-AISTATS11-NoRegret.pdf)

*Full theorem statements/proofs; Algorithm 3.1 DAgger; bounds linking policy performance to online-learning regret + expert loss*

<details>
<summary>Key content</summary>

- **State distributions & cost (Sec. 2):**  
  - \(d_t^\pi\): state distribution at time \(t\) when executing \(\pi\) from steps \(1..t-1\).  
  - \(d^\pi=\frac1T\sum_{t=1}^T d_t^\pi\).  
  - Immediate cost \(C(s,a)\in[0,1]\); \(C^\pi(s)=\mathbb E_{a\sim\pi(s)}[C(s,a)]\).  
  - Total cost \(J(\pi)=\sum_{t=1}^T \mathbb E_{s\sim d_t^\pi}[C^\pi(s)]=T\,\mathbb E_{s\sim d^\pi}[C^\pi(s)]\).
- **Imitation objective (Eq. 1):** \(\hat\pi=\arg\min_{\pi\in\Pi}\mathbb E_{s\sim d^\pi}[\ell(s,\pi)]\) (non-i.i.d. due to distribution shift).
- **Behavior cloning failure (Thm 2.1):** if \(\mathbb E_{s\sim d^{\pi^*}}[\ell(s,\pi)]=\epsilon\) (0-1 or upper bound), then  
  \(J(\pi)\le J(\pi^*)+T^2\epsilon\) (quadratic compounding).
- **Forward-training-style guarantee (Thm 2.2):** if \(\mathbb E_{s\sim d^\pi}[\ell(s,\pi)]=\epsilon\) and expert disadvantage bound  
  \(Q^{\pi^*}_{T-t+1}(s,a)-Q^{\pi^*}_{T-t+1}(s,\pi^*)\le u\), then \(J(\pi)\le J(\pi^*)+uT\epsilon\).
- **DAgger procedure (Alg. 3.1):** iterate \(i=1..N\): execute mixed policy \(\pi_i=\beta_i\pi^*+(1-\beta_i)\hat\pi_i\); collect visited states labeled by expert \(D_i=\{(s,\pi^*(s))\}\); aggregate \(D\leftarrow D\cup D_i\); train \(\hat\pi_{i+1}\) on \(D\). Return best \(\hat\pi_i\) on validation. Default often \(\beta_i=\mathbb I(i=1)\).
- **No-regret link (Eq. 3, Sec. 4):** online regret  
  \(\frac1N\sum_{i=1}^N \ell_i(\pi_i)-\min_{\pi\in\Pi}\frac1N\sum_{i=1}^N \ell_i(\pi)\le \gamma_N\), \(\gamma_N\to0\); use \(\ell_i(\pi)=\mathbb E_{s\sim d^{\pi_i}}[\ell(s,\pi)]\).
- **Distribution mismatch lemma (Lemma 4.1):** \(\|d^{\pi_i}-d^{\hat\pi_i}\|_1\le 2T\beta_i\).
- **Core guarantee (Thm 4.1):** \(\exists \hat\pi\in\{\hat\pi_1.. \hat\pi_N\}\):  
  \(\mathbb E_{s\sim d^{\hat\pi}}[\ell(s,\hat\pi)]\le \epsilon_N+\gamma_N+\frac{2\ell_{\max}}{N}\Big[n_\beta+T\sum_{i=n_\beta+1}^N\beta_i\Big]\),  
  where \(\epsilon_N=\min_{\pi\in\Pi}\frac1N\sum_i \mathbb E_{s\sim d^{\pi_i}}[\ell(s,\pi)]\), \(n_\beta=\max\{n:\beta_n>1/T\}\).
- **DAgger performance bounds (Thm 3.1–3.2):** if \(N=\tilde O(T)\), \(\exists \hat\pi\) with \(\mathbb E_{s\sim d^{\hat\pi}}[\ell]\le \epsilon_N+O(1/T)\); if \(\ell\) upper-bounds 0-1 vs expert, then \(J(\hat\pi)\le J(\pi^*)+uT\epsilon_N+O(1)\) (needs \(N=\tilde O(uT)\)).
- **Finite-sample (Thm 4.2):** add generalization term \(+\ell_{\max}\sqrt{\frac{2\log(1/\delta)}{mN}}\) when using \(m\) trajectories/iter.
- **Empirics (Sec. 5):**
  - Super Tux Kart: linear ridge regression, \(\lambda=10^{-3}\), 20 iters, ~1000 pts/iter; DAgger with \(\beta_i=\mathbb I(i=1)\) reaches **0 falls/lap after 15 iters**, while SMILe (\(\alpha=0.1\)) still ~**2 falls/lap** after 20; supervised stagnates.
  - Super Mario: 4 linear SVMs, \(\lambda=10^{-4}\), 20 iters, 5000 pts/iter; DAgger best reported **3030** avg distance (with \(\beta_i=0.5^{i-1}\)), vs **2980** (\(\beta_i=\mathbb I(i=1)\)); supervised low/stagnant.

</details>

### 📄 GAIL = occupancy-measure matching via GAN objective
**Paper** · [source](https://arxiv.org/pdf/1606.03476.pdf)

*Minimax objective over occupancy measures, discriminator-derived reward, connection to regularized IRL / Jensen–Shannon divergence*

<details>
<summary>Key content</summary>

- **Max causal entropy IRL (Eq. 1):**  
  \[
  \max_{c\in\mathcal C}\Big(\min_{\pi\in\Pi}-H(\pi)+\mathbb E_\pi[c(s,a)]\Big)-\mathbb E_{\pi_E}[c(s,a)]
  \]
  with **causal entropy** \(H(\pi)=\mathbb E_\pi[-\log \pi(a|s)]\). RL step (Eq. 2):  
  \[
  RL(c)=\arg\min_{\pi}-H(\pi)+\mathbb E_\pi[c(s,a)].
  \]
- **Occupancy measure:** \(\rho_\pi(s,a)=\pi(a|s)\sum_{t\ge0}\gamma^t P(s_t=s|\pi)\). Then \(\mathbb E_\pi[c]=\sum_{s,a}\rho_\pi(s,a)c(s,a)\). Valid \(\rho\) satisfy flow constraints (Section 3) and map 1–1 to policies: \(\pi_\rho(a|s)=\rho(s,a)/\sum_{a'}\rho(s,a')\) (Prop. 3.1).
- **Key characterization (Prop. 3.2, Eq. 4):** with convex cost regularizer \(\psi\),
  \[
  RL\circ IRL_\psi(\pi_E)=\arg\min_{\pi}\; -H(\pi)+\psi^*(\rho_\pi-\rho_{\pi_E}).
  \]
  If \(\psi\) constant ⇒ exact matching \(\rho_{\tilde\pi}=\rho_{\pi_E}\) (Cor. 3.2.1).
- **GAIL regularizer (Eq. 13) ⇒ GAN loss (Eq. 14):**  
  \[
  \psi^*_{GA}(\rho_\pi-\rho_E)=\max_{D:(S\times A)\to(0,1)}\mathbb E_\pi[\log D]+\mathbb E_{\pi_E}[\log(1-D)].
  \]
  This equals (up to constant) **Jensen–Shannon divergence**; objective (Eq. 15):  
  \[
  \min_\pi D_{JS}(\rho_\pi,\rho_E)-\lambda H(\pi).
  \]
- **Saddle-point training (Eq. 16) + Algorithm 1:** alternate  
  1) sample \(\tau_i\sim\pi_{\theta_i}\);  
  2) update discriminator \(w\) by gradient (Eq. 17): \(\hat{\mathbb E}_{\tau_i}[\nabla_w\log D_w]+\hat{\mathbb E}_{\tau_E}[\nabla_w\log(1-D_w)]\);  
  3) TRPO policy step on cost \(c(s,a)=\log D_{w}(s,a)\) with gradient (Eq. 18) and entropy term \(-\lambda\nabla_\theta H\).
- **Empirical results (Table 3):** Humanoid-v1: with 80 expert traj, **GAIL 10200.73±1324.47** vs BC 1397.06±1057.84; FEM 5093.12±583.11; GTAL 5096.43±24.96. Ant-v1 (4 traj): **GAIL 3186.80±903.57** vs FEM −2052.51±49.41, GTAL −5743.81±723.48.
- **Defaults/params:** GAE used with \(\gamma=0.995,\lambda=0.97\) (Appendix B). Training interaction (Table 2): MuJoCo tasks typically 500 iters × 50k state-action pairs/iter; Humanoid 1500×50k.

</details>

### 📄 GAIL objective = occupancy-measure matching via JS divergence
**Paper** · [source](https://proceedings.neurips.cc/paper_files/paper/2016/file/cc7e2b878868cbae992d1fb743995d8f-Paper.pdf)

*GAIL minimax objective over occupancy measures; equivalence to regularized max-causal-entropy IRL via convex conjugates; discriminator-derived reward/cost.*

<details>
<summary>Key content</summary>

- **Max causal entropy IRL (Eq. 1–2):**  
  IRL: \(\max_{c\in\mathcal C}\left(\min_{\pi\in\Pi}-H(\pi)+\mathbb E_\pi[c(s,a)]\right)-\mathbb E_{\pi_E}[c(s,a)]\).  
  RL step: \(\mathrm{RL}(c)=\arg\min_{\pi\in\Pi}-H(\pi)+\mathbb E_\pi[c(s,a)]\).  
  \(H(\pi)=\mathbb E_\pi[-\log \pi(a|s)]\) (discounted causal entropy).
- **Occupancy measure:** \(\rho_\pi(s,a)=\pi(a|s)\sum_{t=0}^\infty \gamma^t P(s_t=s\mid \pi)\). Then \(\mathbb E_\pi[c]=\sum_{s,a}\rho_\pi(s,a)c(s,a)\).
- **Regularized IRL → direct policy objective (Prop. 3.1, Eq. 4):** with convex regularizer \(\psi\) on costs,  
  \(\mathrm{RL}\circ \mathrm{IRL}_\psi(\pi_E)=\arg\min_{\pi\in\Pi}-H(\pi)+\psi^*(\rho_\pi-\rho_{\pi_E})\) where \(\psi^*\) is convex conjugate.
- **GAIL regularizer (Eq. 13–16):**  
  \(\psi_{GA}(c)=\mathbb E_{\pi_E}[g(c(s,a))]\) if \(c<0\) else \(+\infty\); \(g(x)=-x-\log(1-e^x)\) for \(x<0\).  
  Conjugate yields (Eq. 14) \(\psi^*_{GA}(\rho_\pi-\rho_E)=\sup_{D\in(0,1)^{S\times A}}\mathbb E_\pi[\log D]+\mathbb E_{\pi_E}[\log(1-D)]\).  
  Leads to (Eq. 15) \(\min_\pi D_{JS}(\rho_\pi,\rho_E)-\lambda H(\pi)\) (JS divergence between occupancy measures).
- **Training procedure (Alg. 1):** alternate  
  (i) discriminator ascent (Eq. 17): \(\hat{\mathbb E}_{\tau_i}[\nabla_w\log D_w]+\hat{\mathbb E}_{\tau_E}[\nabla_w\log(1-D_w)]\) using Adam;  
  (ii) policy update via TRPO to **decrease** (Eq. 16) using cost \(c(s,a)=\log D(s,a)\) and entropy term \(-\lambda\nabla_\theta H(\pi_\theta)\) (Eq. 18 uses \(Q\) from rollouts).
- **Empirical setup/results (Sec. 6):** 9 control tasks (classic + MuJoCo incl. Humanoid). Expert generated by TRPO on true environment cost. Trajectories ~50 state-action pairs each. Networks: 2 hidden layers, 100 tanh units (policy + discriminator). On Reacher, entropy regularization improved: \(\lambda=10^{-3}\) beat \(\lambda=0\) in 4-trajectory setting (Wilcoxon rank-sum, \(p=.05\)); otherwise \(\lambda=0\).

</details>

### 📊 RT-1 empirical results + evaluation/protocol snapshot
**Benchmark** · [source](https://robotics-transformer1.github.io)

*Centralized access to reported success-rate numbers, dataset scale, and evaluation setup highlights*

<details>
<summary>Key content</summary>

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

</details>

### 📊 RT-1 empirical scaling + real-robot success rates
**Benchmark** · [source](https://arxiv.org/html/2212.06817v2)

*Real-robot evaluation tables (success rates across seen/unseen/robustness/long-horizon) + dataset scaling/ablations on size vs diversity.*

<details>
<summary>Key content</summary>

- **Problem setup (Sec. 3):** Learn language-conditioned vision policy \(\pi(a_t \mid o_{t-5:t}, \ell)\) over episodes; binary success reward at episode end.  
  **Imitation learning:** behavior cloning minimizes NLL of demonstrated actions:  
  \[
  \min_\theta \; \mathbb{E}_{(o,\ell,a)\sim D}\left[-\log \pi_\theta(a\mid o,\ell)\right]
  \]
- **Dataset scale (Sec. 5.2):** 130k successful demonstration episodes, collected over **17 months** with **13 robots**, covering **700+ instructions / 744 instructions** grouped into **9 skills**.
- **RT-1 architecture defaults (Sec. 5.1):**
  - Input: **history of 6 images** + language instruction.
  - Vision-language tokenizer: EfficientNet-B3 + FiLM conditioned on **Universal Sentence Encoder**; outputs **81 vision-language tokens**; **16M params**.
  - TokenLearner compresses to **8 tokens per image** → **48 tokens** total to Transformer.
  - Transformer: decoder-only, **8 layers**, **19M params**. Total RT-1 ~**35M params**.
  - Actions: **11 dims** (7 arm + 3 base + 1 mode {arm/base/terminate}); each discretized into **256 bins**; categorical cross-entropy with causal masking.
  - Real-time constraint: ≥**3 Hz** control; inference budget **<100 ms**; speedups via TokenLearner + token reuse across overlapping windows.
- **Key real-robot results (Sec. 6.2, Table 2):** RT-1 success: **Seen 97%**, **Unseen 76%**, **Distractors 83%**, **Backgrounds 59%**. Claimed gains vs next best: **+25% seen**, **+24% unseen**, **+36% distractors**, **+18% backgrounds**.
- **Heterogeneous data (Sec. 6.3):**
  - **Real+Sim (Table 4):** Real objects/seen skill **92→90 (-2)**; Sim-only objects/seen skill **23→87 (+64)**; Sim objects/unseen skill **7→33 (+26)** (all evaluated in real world).
  - **Multi-robot (Table 5):** Train on **Kuka QT-Opt 209k episodes** + EDR data: Classroom eval **90 (-2)**; Bin-picking eval **39 (+17)** vs EDR-only **22**; Kuka-only transfers **0%**.
- **Scaling ablation (Sec. 6.5, Table 7):** Reducing data (same task diversity) hurts generalization sharply (e.g., **51% data → unseen 52%, distractors 39%**). Narrowing diversity (**75% tasks, 97% data**) drops **All to 54%** and **distractors to 42%**; takeaway: **diversity > quantity**.

</details>

### 📊 RT-2 VLA empirical eval + co-finetuning recipe
**Benchmark** · [source](https://proceedings.mlr.press/v229/zitkovich23a/zitkovich23a.pdf)

*~6k-trial evaluation; generalization + emergent instruction/object reasoning; RT-2 variants vs baselines with success rates*

<details>
<summary>Key content</summary>

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

</details>

### 📖 DAgger API (imitation.algorithms.dagger)
**Reference Doc** · [source](https://imitation.readthedocs.io/en/latest/_api/imitation.algorithms.dagger.html)

*Constructor/API surface for `DAggerTrainer` (+ schedules, collectors, defaults)*

<details>
<summary>Key content</summary>

- **Core DAgger idea (workflow in “rounds”):** collect demonstrations → run Behavior Cloning (BC) on *all demos so far* → repeat. Demo distribution shifts from expert-only to increasingly on-policy (imitator) states.
- **Key probability (“beta”):**  
  **Eq. 1:** \( \beta_r \in [0,1] \) = probability of executing the **expert** action at training round \(r\). With probability \(1-\beta_r\), execute the **robot/imitator** action. (Beta provided by a `BetaSchedule` callable.)
- **`DAggerTrainer` constructor:**  
  `DAggerTrainer(*, venv, scratch_dir, rng, beta_schedule=None, bc_trainer, custom_logger=None)`  
  - `beta_schedule=None` ⇒ uses `linear_beta_schedule` by default.  
  - Stores checkpoints + demos under `scratch_dir/` with structure:  
    `checkpoint-001.pt ... checkpoint-latest.pt`, `policy-latest.pt`, and `demos/round-000/... .npz`, etc.
- **Default hyperparameter:** `DAggerTrainer.DEFAULT_N_EPOCHS = 4` used by `extend_and_update()` when neither `n_epochs` nor `n_batches` provided.
- **`extend_and_update(bc_train_kwargs=None)` procedure:** loads new transitions if present, calls `BC.train(**bc_train_kwargs)`, then increments round.  
  - If no fresh demos for current round ⇒ raises `NeedsDemosException`.  
  - If `log_rollouts_venv` missing in `bc_train_kwargs`, it is set to `self.venv`.
- **Interactive data collection:** `create_trajectory_collector()` returns `InteractiveTrajectoryCollector(venv, get_robot_acts, beta, save_dir, rng)`  
  - `step_async(actions)`: per-env, per-timestep random choice: keep passed-in expert `actions` w.p. `beta`, else substitute `get_robot_acts(obs)`.  
  - **Saved demos always record expert actions**, regardless of what was executed; saved as `TrajectoryWithRew` at episode end.
- **Synthetic-feedback trainer:** `SimpleDAggerTrainer(*, venv, scratch_dir, expert_policy, rng, expert_trajs=None, **kwargs)`  
  - `train(total_timesteps, rollout_round_min_episodes=3, rollout_round_min_timesteps=500, bc_train_kwargs=None)`; each round: rollout with expert labeling + BC update. Ensures each round has at least `batch_size` timesteps.
- **Resuming:** `reconstruct_trainer(scratch_dir, venv, custom_logger=None, device='auto')` loads latest snapshot (`checkpoint-latest.pt`, `policy-latest.pt`).

</details>

### 🔍 SayCan scoring = LLM “Say” × affordance “Can”
**Explainer** · [source](http://arxiv.org/pdf/2204.01691.pdf)

*SayCan scoring rule combining LLM prior over skill sequences with value-function grounding*

<details>
<summary>Key content</summary>

- **Setup (Section 3):** Given high-level instruction **i**, current state **s**, and a discrete skill set **Π**. Each skill **π ∈ Π** has:
  - language label **ℓπ** (e.g., “pick up the sponge”)
  - affordance / success probability **p(cπ | s, ℓπ)** where **cπ** is Bernoulli “skill completes successfully”.
- **LLM task-grounding:** score each candidate skill label as next step via **p(ℓπ | i)** (in practice conditioned on prior chosen steps appended to prompt).
- **SayCan factorization (Section 3):** probability a skill makes progress on instruction:
  - **p(ci | i, s, ℓπ) ∝ p(cπ | s, ℓπ) · p(ℓπ | i)**  
  Interpreted as **world-grounding × task-grounding**.
- **Selection rule (Section 3 / Alg. 1):**
  - For each step **n**, compute  
    **pLLMπ = p(ℓπ | i, ℓπₙ₋₁, …, ℓπ₀)**  
    **paffordanceπ = p(cπ | sₙ, ℓπ)**  
    **pcombinedπ = paffordanceπ · pLLMπ**  
    Choose **πₙ = argmaxπ pcombinedπ**, execute, update state, repeat until token **“done”**.
- **Affordances via RL value functions (Section 2,4):** with sparse terminal reward **1** on success else **0**, TD-learned value corresponds to affordance probability.
- **Empirical results (Table 2, mock kitchen, 101 tasks):**
  - **PaLM-SayCan:** Plan **84%**, Execute **74%**
  - **No VF (no affordance grounding):** Plan **67%**
  - **Generative + projection:** Plan **74%**
  - **BC NL:** Execute **0%** total; **BC USE:** Execute **9%** total (60% only on single primitives).
- **Real kitchen generalization (Table 2):** Plan **81%**, Execute **60%**.
- **LLM ablation (Table 3):** **PaLM-SayCan 84/74** vs **FLAN-SayCan 70/61** (plan/execute).

</details>

---

## Related Topics

- [[topics/robot-manipulation|Robot Manipulation]]
- [[topics/reinforcement-learning|Reinforcement Learning]]
