---
title: "Domain Adaptation"
subject: "Retrieval & Knowledge"
date: 2025-01-01
tags:
  - "subject/retrieval-and-knowledge"
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

# Domain Adaptation

## Video (best)
- **Yannic Kilcher** — "Domain Adaptation / Transfer Learning overview"
- **Link:** [https://arxiv.org/abs/2010.03978](https://arxiv.org/abs/2010.03978)
- Why: No single Yannic Kilcher or 3Blue1Brown video squarely covers sim-to-real / domain adaptation as a unified topic. Stanford CS231N guest lectures touch on domain adaptation but are fragmented across years.
- Level: intermediate

> **Note:** The closest verified option is a Stanford CS231N lecture segment, but no single canonical YouTube explainer from the preferred educators cleanly covers sim-to-real + domain adaptation together.

---

## Blog / Written explainer (best)
- **Lilian Weng** — "Domain Randomization for Sim-to-Real Transfer"
- **Link:** [https://lilianweng.github.io/posts/2019-05-05-domain-randomization/](https://lilianweng.github.io/posts/2019-05-05-domain-randomization/)
- Why: Lilian Weng's blog is consistently the gold standard for structured ML topic overviews. This post covers domain randomization, sim-to-real gap, system identification, and progressive transfer with clear diagrams and paper citations — directly mapping to all related concepts listed for this topic.
- Level: intermediate/advanced

---

## Deep dive
- **Author** — Lilian Weng — "Meta-Learning: Learning to Learn Fast" + domain adaptation survey literature
- **Link:** [https://lilianweng.github.io/posts/2018-11-30-meta-learning/](https://lilianweng.github.io/posts/2018-11-30-meta-learning/)
> **Better candidate:** The survey paper "A Survey on Transfer Learning" (Pan & Yang, 2010) and OpenAI's technical blog on domain randomization serve as the most comprehensive references, but a single deep-dive blog post specifically unifying sim-to-real + cross-embodiment transfer does not clearly exist from the preferred authors.

- url: https://openai.com/index/learning-dexterity/ [VERIFY — OpenAI Dactyl blog post covering sim-to-real in depth]
- Why: OpenAI's Dexterous In-Hand Manipulation (Dactyl) write-up is one of the most thorough public technical references for sim-to-real transfer, domain randomization, and system identification applied at scale. It bridges theory and practice concretely.
- Level: advanced

---

## Original paper
- **Tobin et al. (2017)** — "Domain Randomization for Transferring Deep Neural Networks from Simulation to the Real World"
- **Link:** [https://arxiv.org/abs/1703.06907](https://arxiv.org/abs/1703.06907)
- Why: This is the seminal, highly readable paper that introduced domain randomization as a principled approach to closing the sim-to-real gap. It is widely cited, clearly written, and directly foundational to all related concepts (reality gap, sim-to-real transfer, generalization). Accessible to readers without deep robotics background.
- Level: intermediate

---

## Code walkthrough
- None identified
- Why: No single well-maintained, pedagogically structured code walkthrough from a trusted source (fast.ai, Hugging Face, PyTorch tutorials) specifically covers sim-to-real domain adaptation end-to-end. Isaac Gym / Isaac Lab examples exist but lack narrative explanation.

> **Closest option:** NVIDIA Isaac Lab tutorials cover sim-to-real workflows in code, but are documentation-style rather than pedagogical walkthroughs. [NOT VERIFIED]

---

## Coverage notes
- **Strong:** Written/blog coverage (Lilian Weng), seminal paper (Tobin et al. 2017), OpenAI technical posts on domain randomization
- **Weak:** Video explainers — no preferred educator has produced a focused, high-quality video on sim-to-real or domain adaptation as a unified concept
- **Gap:** Cross-embodiment transfer specifically is very underserved across all resource types; progressive transfer and system identification as sub-topics lack standalone pedagogical resources. Code walkthroughs with narrative explanation are essentially absent for this topic.

---

## Cross-validation
This topic appears in 2 courses: **intro-to-multimodal**, **intro-to-physical-ai**
- For `intro-to-physical-ai`: sim-to-real gap, domain randomization, and system identification are core — Tobin et al. + Weng blog are strong anchors
- For `intro-to-multimodal`: domain adaptation in the sense of cross-modal/cross-domain generalization is less well served by these robotics-focused resources; a separate resource targeting distribution shift in vision-language models would be needed

---

---

## Additional Resources for Tutor Depth

> **9 sources** — papers, official docs, working code, benchmarks, and deep explainers that give the AI tutor precision on this topic.

### 📄 Domain Adaptation Generalization Bound (A-distance + labeling disagreement)
**Paper** · [source](https://proceedings.neurips.cc/paper/2006/file/b1b0432ceafb0ce714426e9114852ac7-Paper.pdf)

*Upper bound on target risk including (i) source empirical risk, (ii) domain discrepancy via \(d_{\mathcal H}\) (A-distance), and (iii) conditional/labeling-function disagreement term \(\lambda\).*

<details>
<summary>Key content</summary>

- **Setup (Sec. 2):** Representation \(R:X\to Z\). Induced feature distributions: \(\Pr_{\tilde D}[B]=\Pr_D[R^{-1}(B)]\). Induced labeling: \(\tilde f(z)=\mathbb E_D[f(x)\mid R(x)=z]\).  
  Predictor \(h:Z\to\{0,1\}\). Errors:  
  \[
  \epsilon_S(h)=\mathbb E_{z\sim \tilde D_S}\big[|\tilde f(z)-h(z)|\big],\quad
  \epsilon_T(h)=\mathbb E_{z\sim \tilde D_T}\big[|\tilde f(z)-h(z)|\big].
  \]
- **A-distance / \(\mathcal H\)-divergence (Sec. 3.1–3.2):** For subset family \(\mathcal A\),  
  \[
  d_{\mathcal A}(D,D')=2\sup_{A\in\mathcal A}|\Pr_D[A]-\Pr_{D'}[A]|.
  \]
  For hypothesis class \(\mathcal H\), use \(\mathcal A=\{Z_h:h\in\mathcal H\}\) and denote \(d_{\mathcal H}(\tilde D_S,\tilde D_T)\).
- **Labeling disagreement / conditional shift term (Sec. 3.1):** \(\tilde f\) is **\(\lambda\)-close** to \(\mathcal H\) if  
  \[
  \inf_{h\in\mathcal H}\big(\epsilon_S(h)+\epsilon_T(h)\big)\le \lambda.
  \]
- **Main bound (Thm. 1, Sec. 3.2):** For VC-dim \(d\), labeled source sample size \(m\), w.p. \(\ge 1-\delta\), \(\forall h\in\mathcal H\):  
  \[
  \epsilon_T(h)\le \hat\epsilon_S(h)+\sqrt{\frac{4}{m}\Big(d\log\frac{2em}{d}+\log\frac{4}{\delta}\Big)}+d_{\mathcal H}(\tilde D_S,\tilde D_T)+\lambda.
  \]
- **Computable version with unlabeled samples (Thm. 2):** With unlabeled \(\tilde U_S,\tilde U_T\) of size \(m'\):  
  \[
  \epsilon_T(h)\le \hat\epsilon_S(h)+4\sqrt{\frac{d\log\frac{2em}{d}+\log\frac{4}{\delta}}{m}}+\lambda+d_{\mathcal H}(\tilde U_S,\tilde U_T)+4\sqrt{\frac{d\log(2m')+\log\frac{4}{\delta}}{m'}}.
  \]
- **Estimating \(d_{\mathcal H}\) from domain-classification (Sec. 4):** Given \(\tilde U_S,\tilde U_T\) (each size \(m'\)), define domain-discrimination error  
  \[
  \mathrm{err}(h)=\frac{1}{2m'}\sum_{i=1}^{2m'}\big|h(z_i)-\mathbf 1[z_i\in \tilde U_S]\big|.
  \]
  Then  
  \[
  d_{\mathcal A}(\tilde U_S,\tilde U_T)=2\Big(1-2\min_{h'\in\mathcal H}\mathrm{err}(h')\Big).
  \]
  For linear separators, exact optimization NP-hard; authors approximate via convex surrogate (modified Huber loss) + SGD.
- **Empirical numbers (Sec. 5.3, Fig. 2b; PoS WSJ→MEDLINE, projection dim \(d=200\)):**  
  - Identity: Huber loss 0.003, A-distance 1.796, target error 0.253  
  - Random Proj: Huber loss 0.254, A-distance 0.223, target error 0.561  
  - SCL: Huber loss 0.07, A-distance 0.211, target error 0.216  
  Data: 100 labeled WSJ sentences (~2500 words); 1M unlabeled words (500k/domain) to estimate A-distance.

</details>

### 📄 Humanoid-Gym zero-shot sim-to-real recipe (Isaac Gym → MuJoCo → real)
**Paper** · [source](https://arxiv.org/html/2404.05695v2)

*Practical sim-to-real pipeline for humanoid locomotion with domain randomization + sim2sim validation; reported zero-shot transfer on two real humanoids.*

<details>
<summary>Key content</summary>

- **Problem framing (Sec. III-A):** Real deployment is **POMDP** (partial observations), while training can use **privileged info** via **Asymmetric Actor-Critic** + **PPO** with **GAE**.  
  - **Policy objective (Eq. 1):** PPO clipped surrogate loss (standard PPO form) using advantage estimates.  
  - **Value/advantage (Eq. 2):** GAE-based advantage requiring updated value function.
- **Observations/actions (Sec. III-B, Table I):**
  - **Action:** target joint positions for a **PD controller**.
  - **Policy inputs (single frame):** clock (2), commands (3), joint pos (12), joint vel (12), angular vel (3), Euler angles (3), last actions (12), periodic stance mask (2), feet contact detection (2).  
  - **Privileged (state-only) examples:** friction (1), body mass (1), base linear vel (3), push force (2), push torques (3), tracking difference (12).
  - **Gait design:** sinusoidal reference motion + **periodic stance/contact mask** synchronized to DS/SS phases.
- **Control rates:** policy at **50 Hz**; internal PD at **500 Hz**.
- **Training setup (Appendix Table II):** **8192 environments**, episode length **2400 steps**, discount **0.994**, GAE λ **0.95**, entropy coef **0.001**, learning rate **1e-5**, frame stack obs **15**, privileged stack **3**, single obs dim **47**, privileged dim **73**.
- **Domain randomization (Sec. IV-A, Appendix Table III):** joint pos noise ±0.05 rad (Gaussian), joint vel ±0.5 rad/s (Gaussian), ang vel ±0.1 rad/s (Gaussian), Euler ±0.03 rad (Gaussian), **system delay 0–10 ms (Uniform)**, **friction 0.1–2.0 (Uniform)**, motor strength **95–105% (Gaussian scaling)**, payload **±5 kg (Gaussian additive)**.
- **Reward components (Sec. III-C, Appendix Table IV scales):** lin vel track **1.2**, ang vel track **1.0**, orientation **1.0**, base height **0.5**, contact pattern **1.0**, joint pos tracking **1.5**, default joint **0.2**, energy **-1e-4**, action smoothness **-0.01**, large contact **-0.01**; “velocity mismatch” term present (scale **0.5**) but commands set to zero to encourage stable walking.
- **Workflow/results (Sec. IV):** Train in **Isaac Gym (GPU, fast)** → validate robustness in **MuJoCo (more accurate)** (“sim2sim”) → **zero-shot sim-to-real** on **XBot-S (1.2 m)** and **XBot-L (1.65 m)**; policies traverse **flat** and **uneven** terrains. MuJoCo calibrated to match real joint swing trajectories/phase portraits more closely than Isaac Gym.

</details>

### 📄 Invariant representations can fail in Domain Adaptation
**Paper** · [source](http://proceedings.mlr.press/v97/zhao19a/zhao19a.pdf)

*Formal bounds/counterexamples for invariant representation learning; sufficient/necessary conditions via conditional shift + label-marginal mismatch.*

<details>
<summary>Key content</summary>

- **DA setup/notation (Sec. 2):** Source domain ⟨D_S, f_S⟩, target ⟨D_T, f_T⟩ with deterministic labels Y=f(X). Hypothesis h: X→{0,1}. Risk: ε_S(h,f):=E_{x~D_S}[|h(x)-f(x)|]; ε_S(h):=ε_S(h,f_S) (similarly ε_T).
- **H-divergence (Def. 2.1):** A_H:={h^{-1}(1) | h∈H}.  
  d_H(D,D′):= sup_{A∈A_H} |Pr_D(A) − Pr_{D′}(A)|.
- **Classic DA bound (Thm 2.1, Eq. (1)):** For VC-dim d, w.p. ≥1−δ, ∀h∈H:  
  ε_T(h) ≤ \hat ε_S(h) + ½ d_{HΔH}(\hat D_S,\hat D_T) + λ* + O(√((d log n + log(1/δ))/n)),  
  where h*:=argmin_{h∈H} ε_S(h)+ε_T(h), λ*:=ε_S(h*)+ε_T(h*).
- **Counterexample (Sec. 4.1, Fig. 1):** X=Z=R.  
  D_S=U(−1,0), f_S(x)=0 if x≤−½ else 1.  
  D_T=U(1,2), f_T(x)=0 if x≥3/2 else 1.  
  There exists h*(x)=1 iff x∈(−½,3/2) with **0 error on both**.  
  But with g(x)=I_{x≤0}(x+1)+I_{x>0}(x−1): induced D_ZS=D_ZT=U(0,1) (perfectly invariant), yet **∀h: ε_S(h∘g)+ε_T(h∘g)=1** (smaller source error ⇒ larger target error). Here λ*_g=1.
- **Sufficient-condition bound without λ\* (Thm 4.1):** For H⊆[0,1]^X, ∀h∈H:  
  ε_T(h) ≤ ε_S(h) + d_{\tilde H}(D_S,D_T) + min{E_{D_S}|f_S−f_T|, E_{D_T}|f_S−f_T|},  
  where \tilde H := { sgn(|h(x)−h′(x)|−t) : h,h′∈H, t∈[0,1] }.  
  Note: E_{D_S}|f_S−f_T|=ε_S(f_T), E_{D_T}|f_S−f_T|=ε_T(f_S) (cross-domain errors).
- **Info-theoretic lower bound (Sec. 4.3):** With Markov chain X→^g Z→^h Ŷ and JS distance d_JS:  
  Lemma 4.8: d_JS(D_{Y_S},D_{Y_T}) ≤ d_JS(D_{Z_S},D_{Z_T}) + √ε_S(h∘g)+√ε_T(h∘g).  
  Thm 4.3: if d_JS(D_{Y_S},D_{Y_T}) ≥ d_JS(D_{Z_S},D_{Z_T}), then  
  ε_S(h∘g)+ε_T(h∘g) ≥ ½ ( d_JS(D_{Y_S},D_{Y_T}) − d_JS(D_{Z_S},D_{Z_T}) )^2.  
  ⇒ If label marginals differ, forcing invariance (small d_JS(D_ZS,D_ZT)) can **force large joint error**.
- **Empirical pipeline (Sec. 5):** DANN on MNIST/USPS/SVHN (10 classes). Preprocess to grayscale 16×16. Classifier: 2 conv layers (5×5 kernels; 10 then 20 channels) → FC 1280→100 → softmax(10). Discriminator: conv features → FC 500→100 → 1-unit domain output. Observation: target accuracy rises quickly (<10 iters) then decreases with continued training (over-training hurts when label distributions differ).

</details>

### 📄 SimOpt / Bayesian Domain Randomization Loop
**Paper** · [source](https://arxiv.org/pdf/1810.05687.pdf)

*Closed-loop procedure to update simulator parameter distributions from a few real rollouts (KL-constrained Bayesian-style update) interleaved with RL policy training.*

<details>
<summary>Key content</summary>

- **Domain randomization objective (Eq. 1, Sec. III-A):** sample sim params \(\xi \sim p_\phi(\xi)\) to induce dynamics \(P_{\xi\sim p_\phi}\). Train policy \(\pi_\theta(a|s)\) to maximize  
  \[
  \max_\theta \ \mathbb{E}_{\xi\sim p_\phi}\big[\mathbb{E}_{\pi_\theta}[R(\tau)]\big]
  \]
  where \(\tau=(s_0,a_0,\dots,s_T,a_T)\), \(R(\tau)=\sum_{t=0}^T \gamma^t R(s_t,a_t)\).
- **Sim-to-real matching objective (Eq. 2, Sec. III-B):** minimize expected discrepancy between **real** and **sim** observation trajectories:  
  \[
  \min_\phi \ \mathbb{E}_{\xi\sim p_\phi}\big[\mathbb{E}_{\pi_{\theta,p_\phi}}[D(\tau^{ob}_\xi,\tau^{ob}_{real})]\big]
  \]
  Policy inputs and discrepancy observations need not match; only partial real observations required.
- **Iterative KL-trust-region update (Eq. 3 + Alg. 1 “SimOpt”):**  
  \[
  \min_{\phi_{i+1}} \mathbb{E}_{\xi_{i+1}\sim p_{\phi_{i+1}}}\big[\mathbb{E}_{\pi_{\theta,p_{\phi_i}}}[D(\tau^{ob}_{\xi_{i+1}},\tau^{ob}_{real})]\big]
  \ \text{s.t.}\ D_{KL}(p_{\phi_{i+1}}\|p_{\phi_i})\le \epsilon
  \]
  **Algorithm 1 steps:** init \(p_{\phi_0}\); loop: train RL in sim with \(p_{\phi_i}\); collect real rollout; sample \(\xi\sim p_{\phi_i}\) and sim rollouts; compute cost \(c(\xi)=D(\cdot)\); update \(p_{\phi_{i+1}}\) with KL step \(\epsilon\).
- **Discrepancy function (Eq. 4):** weighted \(\ell_1+\ell_2\) over time with per-dimension weights \(W\):  
  \(D = w_{\ell_1}\sum_{i=0}^T |W(o_{i,\xi}-o_{i,real})| + w_{\ell_2}\sum_{i=0}^T \|W(o_{i,\xi}-o_{i,real})\|_2^2\). Gaussian temporal smoothing used (std 5 timesteps, trunc 4).
- **Implementation defaults:** \(p_\phi(\xi)=\mathcal{N}(\mu,\Sigma)\) (full covariance). Update via **REPS** (relative entropy policy search) gradient-free, treating simulator as black box.
- **Empirical results (key numbers):**
  - **Swing-peg-in-hole (real ABB Yumi):** per SimOpt iter: 100 RL iters (~7 min), **3 real rollouts**, **3 REPS updates**, **9600 sim samples/update**, 453 timesteps/sample. After **2 SimOpt iterations**, **90% success over 20 trials**.
  - **Drawer opening (real Franka Panda):** per iter: 200 RL iters (~22 min), **3 real rollouts**, **20 REPS updates**, **9600 samples/update**. After **1 SimOpt update**, **20/20 successful** openings.
  - **Why not “very wide” randomization:** wide distributions can include infeasible instances (e.g., peg too large / rope too short) and hinder learning; in sim drawer task, policy only opened drawer at cabinet-position std **2 cm**; larger (up to **10 cm**) led to conservative/failing policies. SimOpt handled target offsets **15 cm (3 iterations)** and **22 cm (5 iterations)** by progressively shifting the distribution.

</details>

### 📄 i-S2R (Iterative Sim-to-Real) for Human-Robot Table Tennis
**Paper** · [source](https://proceedings.mlr.press/v205/abeyruwan23a/abeyruwan23a.pdf)

*Iterative sim↔real RL pipeline that updates a *human behavior model* from real interaction data to reduce sim-to-real gap in tight HRI; includes transfer/generalization results.*

<details>
<summary>Key content</summary>

- **Objective / MDP (Section 3):** MDP \((S,A,R,p)\), policy \(\pi_\theta:S\to A\), maximize expected return  
  \[
  \mathbb{E}\left[\sum_{t=1}^{N} r(s_t,\pi_\theta(s_t))\right]
  \]
  Episodes simplified: start with a hit (no serve); episode = single ball throw + return; reward encourages cooperative returns → longer rallies.
- **Iterative-Sim-to-Real procedure (Section 4, Fig. 2):**
  1) Collect initial human-only data \(D_0\) (player hits across table, no robot).  
  2) Fit initial human ball distribution model \(M_0\).  
  3) Train policy in sim on balls sampled from \(M_k\) → \(\theta_k^S\).  
  4) Deploy + **real fine-tune with human-in-loop** → \(\theta_k^R\); collect interaction hits → update dataset \(D_{k+1}\).  
  5) Update human model \(M_{k+1}\) from \(D_{k+1}\); continue sim training from \(\theta_k^R\). Repeat until model deltas shrink (they found ~3 iterations sufficient).
- **Human behavior model (Section 4):** uniform distribution defined by **16 numbers**: min/max of initial ball position (6), velocity (6), and landing \(x,y\) on robot side (4). Fit per-trajectory initial pos/vel by Nelder–Mead minimizing Euclidean trajectory error; remove outliers via DBSCAN; take per-dimension min/max.
- **RL optimizer (Section 3):** Blackbox Gradient Sensing (BGS), an ES method optimizing smoothed objective (Eq. 1):  
  \[
  F_\sigma(\theta)=\mathbb{E}_{\delta\sim\mathcal{N}(0,I)}[F(\theta+\sigma\delta)]
  \]
  Uses orthogonal perturbation ensembles + “elite-choice” sample selection; other RL (PPO, SAC, QT-OPT) didn’t transfer as well.
- **System / policy defaults (Section 5):** 8-DOF robot (6-DOF arm + 2D linear actuator). Obs = 3D ball pos + 8 joint angles = 11D; stack past **7** obs → input size \(8\times 11\). Action = 8 joint velocities at **75 Hz**. Policy net: 3-layer 1D dilated gated CNN. Sim: PyBullet; add uniform ball obs noise = **2× ball diameter** per timestep; must simulate sensor/action latency (Gaussian from real measurements) or transfer “completely failed.”
- **Key empirical results (Abstract, Section 6–7):**
  - Final performance: **22 hits average**, **150 best** rally.  
  - For **80% of players**, i-S2R rallies **70%–175% longer** than S2R+FT baseline (beginner ≈70%, intermediate ≈175%).  
  - Aggregated: i-S2R ≈ **9%** higher rally length than S2R+FT.  
  - Cross-eval generalization: i-S2R retains ~**70%** of self-performance vs S2R+FT ~**30%** (Fig. 7).  
  - S2R-Oracle+FT (trained on penultimate learned human model) matches i-S2R with only **35%** of real fine-tuning budget → gains largely from improved human model.

</details>

### 📊 SKADA-Bench (UDA) — realistic validation + standardized results
**Benchmark** · [source](https://arxiv.org/html/2407.11676v2)

*Standardized UDA comparison tables + explicit realistic validation protocol (nested CV, unsupervised scorers), enabling fair number quoting.*

<details>
<summary>Key content</summary>

- **UDA definition (Sec. 1):** adapt a model trained on **labeled source** to **unlabeled target** under distribution shift.
- **Shift types (Sec. 2.1):**
  - *Covariate shift:* \(P_s(y\mid x)=P_t(y\mid x)\), but \(P_s(x)\neq P_t(x)\).
  - *Target shift:* \(P_s(y)\neq P_t(y)\) with conditionals preserved.
  - *Conditional shift:* \(P_s(y\mid x)\neq P_t(y\mid x)\).
  - *Subspace shift:* exists subspace \(Z=g(X)\) where distributions align and a classifier on \(Z\) transfers.
- **Realistic model selection protocol (Sec. 3.1):**
  - **Nested cross-validation**: outer loop creates train/test splits; inner loop selects DA hyperparameters using **unlabeled target validation** via unsupervised scorers.
  - **Splits:** 5 random stratified repeats, **80/20 train/test** (outer + inner), except **Deep DA**: only **1 outer split** (compute).
  - **Timeout:** **4 hours** per method for nested loop.
  - **Base estimator selection (before DA tuning):** grid-search on **source** among Logistic Regression, RBF-SVM, XGBoost; some methods require SVM (JDOT, DASVM).
  - **Deep backbones:** 2-layer CNN (MNIST/USPS), ImageNet-pretrained ResNet50 (Office31/OfficeHome), ShallowFBCSPNet (BCI).
- **Unsupervised scorers (Sec. 2.2):** IW, DEV, Prediction Entropy (PE), SND, Circular Validation (CircV), MixVal. CircV not used for Deep DA (too expensive).
- **Key empirical table (Table 2, realistic best scorer):**
  - **Train Src baseline accuracies:** Cov 0.88, Tar 0.85, Cond 0.66, Sub 0.19; Office31 0.65; OfficeHome 0.56; MNIST/USPS 0.54; 20News 0.59; Amazon 0.70; Mushrooms 0.72; Phishing 0.91; BCI 0.55.
  - **Top average ranks (real datasets):** **LinOT rank 4.06** (Office31 0.66; OfficeHome 0.57; MNIST/USPS 0.64; 20News 0.82; Amazon 0.70; Mushrooms 0.76; Phishing 0.91; BCI 0.61; scorer CircV). **CORAL rank 5.08** (scorer CircV).
  - **Conditional shift (simulated):** mapping methods strong: **EntOT 0.82**, **ClassRegOT 0.81** vs Train Src 0.66 (near Train Tgt 0.82).
- **Scorer selection frequency (Sec. 4.1):** **CircV best for 10/20 methods**, **IW best for 4/20**.
- **Scorer–accuracy correlation (Sec. 4.2, Pearson r):** MixVal **0.51**, IW **0.44**, CircV **0.40**; SND/DEV/PE “do not provide a good proxy” (low correlation). High variance: IW/CircV score ≈1 can correspond to accuracy **0.5–1.0**.
- **Compute cost (Sec. 4):** shallow experiments **1,215 CPU-hours**; deep experiments **244 GPU-hours**.
- **Design rationale:** supervised target validation is unrealistic; nested CV + unsupervised scorers estimate real-world performance and reveal performance drops vs supervised tuning; simple linear transforms (LinOT, CORAL, JPCA, SA) are “safe defaults” when shift type unknown.

</details>

### 📊 VisDA-2017 (Sim-to-Real) UDA Benchmark
**Benchmark** · [source](https://ar5iv.labs.arxiv.org/html/1710.06924)

*Official VisDA-2017 challenge description + dataset/task definitions + baseline & top challenge scores (classification/segmentation) + evaluation metrics*

<details>
<summary>Key content</summary>

- **Problem setup (UDA, sim→real):** Train on **labeled source** (synthetic) and adapt using **unlabeled target**; **no target annotations** used for training. Two **different target domains**: one for **validation (hyperparams)** and a different one for **test** to prevent tuning on test labels (Section 3).
- **VisDA-C (classification) domains & scale (12 classes):**
  - **Source/train:** CAD-synthetic renderings, **152,397 images**, **1,907 3D models**.
  - **Target/val:** **MS COCO** crops, **55,388 images** (person capped at **4,000**).
  - **Target/test:** **YouTube-BB** frame crops, **72,372 images**.
  - Total across splits: **>280K images**.
- **Metric (classification):** **mean accuracy averaged over categories** (reported at **40k iterations** in baselines).
- **Baseline training defaults (AlexNet):** ImageNet init (except last FC=12); **SGD**, **momentum 0.9** (weight decay/base LR given but not legible in excerpt).  
  **ResNeXt-152:** last FC=12 with Xavier init; output layer LR = **10×** other layers; LR schedule: \(lr(p)=lr_0(1+\alpha p)^{-\beta}\), \(p\in[0,1]\), \(\alpha=10,\beta=0.75\).
- **Baseline results (VisDA-C):**
  - **Oracle (in-domain) AlexNet:** synthetic **99.92%**, real-val **87.62%**.
  - **Source-only AlexNet → real-val:** **28.12%**; **Deep CORAL 45.53%**; **DAN 51.62%**.
  - **Test domain:** Oracle AlexNet **92.08%**, Oracle ResNeXt-152 **93.40%**; Source-only AlexNet **30.81%**; **DAN 49.78%**, **Deep CORAL 45.29%**.
  - **Challenge top score (test):** GFColourLabUEA improved **ResNet-152 source-only 45.3% → 92.8%** using **Mean Teacher + label propagation** (student CE on source + student/teacher consistency MSE on both domains; teacher = EMA of student weights).
- **VisDA-S (segmentation) domains (19 classes) & metric:** GTA5 (source, **24,966** labeled frames) → CityScapes (val labeled) → Nexar/BDD (test, **1,500** images); metric **mIoU**.
  - **Dilation F.E. source:** **21.4 mIoU** on CityScapes val; **oracle 64.0**. On Nexar test: **source 25.9 mIoU**. Hoffman et al. adaptation reported **~25.5 mIoU** on val (also cited as **27.1** for their method in table caption).

</details>

### 🔍 ASID—Active Exploration for System Identification (Sim→Real→Sim→Real)
**Explainer** · [source](https://arxiv.org/html/2404.12308v2)

*Step-by-step pipeline: Fisher-information exploration → system ID → downstream policy optimization in identified simulator (test-time simulation construction)*

<details>
<summary>Key content</summary>

- **Problem setup (Section 3):** Real dynamics unknown but in parametric family \(P_\theta\); there exists true \(\theta^\*\) s.t. real MDP \(M = M_{\theta^\*}\). Simulator can sample trajectories \(\tau \sim P_\theta^\pi\) “for free” for any \(\theta,\pi\).
- **Learning protocol (Section 3):**  
  1) Choose exploration policy \(\pi_{\text{exp}}\), run **one real episode** → trajectory \(\tau\).  
  2) Use \(\tau\) + simulator to produce task policy \(\pi\).  
  3) Deploy \(\pi\) in real.
- **Fisher information + estimation bound (Eq. 1):** For unbiased estimator \(\hat\theta\), MSE is lower-bounded by Fisher information \(I(\theta)\):  
  \[
  \mathbb{E}\|\hat\theta-\theta\|^2 \ \ge\ \mathrm{tr}\!\left(I(\theta)^{-1}\right)
  \]
  (via Cramér–Rao). Fisher information depends on trajectory distribution induced by \(\pi_{\text{exp}}\): \(I(\theta;\pi_{\text{exp}})\).
- **Exploration objective = A-optimal design (Eq. 2):**  
  \[
  \pi_{\text{exp}}^\* \in \arg\min_{\pi_{\text{exp}}}\ \mathrm{tr}\!\left(I(\theta;\pi_{\text{exp}})^{-1}\right)
  \]
  **Rationale:** large \(I\) ⇒ trajectories highly sensitive to \(\theta\) (log-likelihood gradient large) ⇒ more informative data.
- **Practical implementation (Section 4.1):**
  - Assume next-state model \(s_{t+1}=f_\theta(s_t,a_t)+\varepsilon\) with Gaussian noise (Eq. 3) ⇒ \(I\) reduces to sensitivity of dynamics wrt \(\theta\) (uses \(\nabla_\theta f_\theta\)).  
  - Unknown \(\theta^\*\): optimize **expected** objective under parameter distribution \(p(\theta)\) (domain randomization) (Eq. 4).  
  - If simulator non-differentiable: approximate \(\nabla_\theta f_\theta\) via **finite differences**.  
  - Train \(\pi_{\text{exp}}\) with standard RL (e.g., **PPO**).
- **System identification (Section 4.2):** Fit a **distribution** over parameters \(p(\theta)\) to match real trajectory \(\tau\) by minimizing mismatch between \(\tau\) and simulated rollouts using the **same action sequence**. Implemented with **REPS** (simulation) and **CEM** (real experiments).
- **Downstream policy (Section 4.3):** Train task policy entirely in the **identified simulator**; transfer **zero-shot** to real.
- **Key empirical results (real-world, Section 5.5):**
  - **Rod balancing:** Domain Randomization (DR) **0/3, 0/3, 0/3** (left/middle/right inertia); **ASID 2/3, 1/3, 3/3** (total **6/9**).  
  - **Shuffleboard:** DR **2/5** (yellow/close), **1/5** (blue/far); **ASID 4/5**, **3/5** (total **7/10**).  
  - Typical data need: **single real episode** often suffices.

</details>

### 📋 DomainBed DG Experiment Surface (CLI, registries, sweeps)
**Code** · [source](https://github.com/facebookresearch/DomainBed)

*Configuration/implementation surface for domain generalization experiments (datasets, algorithms, hparams registry, training + sweep scripts, model selection).*

<details>
<summary>Key content</summary>

- **Purpose:** PyTorch suite for benchmarking **domain generalization** (per *In Search of Lost Domain Generalization*, arXiv:2007.01434). Official results for **commit `7df6f06`** provided in `domainbed/results/2020_10_06_7df6f06/results.tex`.
- **Algorithm registry (`domainbed/algorithms.py`):** includes ERM, IRM, GroupDRO, Mixup, MTL, MLDG, MMD, CORAL, DANN, CDANN, SagNet, ARM, VREx, RSC, SD, AND-Mask, IGA, Fish, SelfReg, SAND-mask, Fishr, TRM, IB-ERM, IB-IRM, CAD/CondCAD, Transfer, CausIRL (CORAL or MMD), EQRM, RDM, ADRMX, ERM++, URM.
- **Dataset registry (`domainbed/datasets.py`):** RotatedMNIST, ColoredMNIST, VLCS, PACS, Office-Home, TerraIncognita (subset), DomainNet, SVIRO (subset), WILDS FMoW, WILDS Camelyon17, Spawrious. Custom image datasets supported via folder structure: `dataset/domain/class/image.xyz`.
- **Backbones + hparams:** implementations use **ResNet50 / ResNet18**; hyperparameter grids defined in `domainbed/hparams_registry.py`.
- **Model selection methods (`domainbed/model_selection.py`):**
  - `IIDAccuracySelectionMethod`: validation subset from **training domains**.
  - `LeaveOneOutSelectionMethod`: validation subset from a **held-out domain** (not train/test).
  - `OracleSelectionMethod`: validation subset from the **test domain**.
- **Core CLI workflows:**
  - Download: `python3 -m domainbed.scripts.download --data_dir=./domainbed/data`
  - Train: `python3 -m domainbed.scripts.train --data_dir=... --algorithm IGA --dataset ColoredMNIST --test_env 2`
  - Sweep launch: `python -m domainbed.scripts.sweep launch --data_dir=... --output_dir=... --command_launcher MyLauncher`
  - Sweep scale defaults: “**tens of thousands**” models = (all algos × all datasets × **3 trials** × **20 hparam** samples). Can restrict via `--algorithms`, `--datasets`, `--n_hparams`, `--n_trials`.
  - Results: `python -m domainbed.scripts.collect_results --input_dir=...`
  - Cleanup/retry: `python -m domainbed.scripts.sweep delete_incomplete` then relaunch with identical args.
- **Tests:** `python -m unittest discover`; with datasets: `DATA_DIR=/path python -m unittest discover`.

</details>

---

## Related Topics

- [[topics/lora-peft|LoRA & PEFT]]
- [[topics/pre-training|Pre-Training]]
