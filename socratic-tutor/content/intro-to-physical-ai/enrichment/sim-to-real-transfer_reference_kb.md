## Core Definitions

**Sim-to-real transfer**: Training a model (often a control policy) in a simulator (“source domain”) and deploying it in the physical world (“target domain”), while managing the **reality gap**—the performance drop caused by mismatches between simulated and real dynamics/observations. Weng frames three main families for closing this gap: **system identification**, **domain randomization**, and **domain adaptation** (https://lilianweng.github.io/posts/2019-05-05-domain-randomization/).

**Reality gap**: The gap between simulator and real world induced by incorrect physical parameters (e.g., friction, damping, mass) and, more severely, incorrect physical modeling (e.g., contact/collision modeling). Weng emphasizes that even small mismatches can cause failure, and that parameters can drift over time due to temperature, wear, humidity, etc. (https://lilianweng.github.io/posts/2019-05-05-domain-randomization/).

**Domain randomization (DR)**: Train on a *distribution* of simulated environments by randomizing simulator parameters \(\xi\) (textures, lighting, friction, delays, masses, etc.) so that the real world is “just another variation.” Tobin et al. describe the core idea as: with enough variability in simulation, real images can appear as another simulated variation (https://arxiv.org/abs/1703.06907). Weng formalizes DR as sampling \(\xi \in \Xi \subset \mathbb{R}^N\) during training to induce varied environments (https://lilianweng.github.io/posts/2019-05-05-domain-randomization/).

**Domain adaptation (DA)**: Transfer techniques that use (typically unlabeled) target-domain data to reduce distribution shift between source and target—often by learning a mapping/representation where domains align, or by regularizing the task model to be domain-invariant. Weng notes many DA methods use adversarial losses / GAN-style training (https://lilianweng.github.io/posts/2019-05-05-domain-randomization/). Ganin et al. define domain-adversarial training as learning features that are discriminative for the task yet indiscriminate for domain, implemented via a gradient reversal layer (https://arxiv.org/abs/1505.07818).

**System identification (SysID)**: Building/calibrating a mathematical model of the physical system; in RL sim-to-real, this means identifying simulator parameters so simulated trajectories match real trajectories. Weng highlights SysID as effective but expensive, and complicated by time-varying parameters (https://lilianweng.github.io/posts/2019-05-05-domain-randomization/). ASID frames real dynamics as belonging to a parametric family \(P_\theta\) with true \(\theta^\*\), and uses targeted real exploration to identify \(\theta^\*\) (https://arxiv.org/html/2404.12308v2).

**Progressive transfer (progressive sim↔real)**: A staged approach that alternates between simulation training and real-world data collection/fine-tuning, progressively reducing mismatch. Examples include SimOpt’s iterative update of the simulator parameter distribution using a few real rollouts (https://arxiv.org/pdf/1810.05687.pdf) and i-S2R’s iterative updates of a *human behavior model* using real interaction data (https://proceedings.mlr.press/v205/abeyruwan23a/abeyruwan23a.pdf).

**Safety validation (for sim-to-real deployment)**: Rigorous validation steps before and during real deployment to reduce risk from model errors and unmodeled dynamics. In the provided sources, this appears operationally as (i) robustness checks via **sim2sim** validation (Isaac Gym → MuJoCo) before real deployment (https://arxiv.org/html/2404.05695v2), and (ii) explicit modeling of real-world latencies/noise without which transfer “completely failed” in i-S2R (https://proceedings.mlr.press/v205/abeyruwan23a/abeyruwan23a.pdf). (Use this definition as a tutoring handle: “safety validation = staged robustness testing + conservative rollout practices,” grounded in these concrete protocols.)

---

## Key Formulas & Empirical Results

### Domain adaptation generalization bound (discrepancy + labeling disagreement)
From Ben-David et al. (NeurIPS 2006), for hypothesis class \(\mathcal H\) and VC-dim \(d\), with labeled source sample size \(m\), with probability \(\ge 1-\delta\), for all \(h\in\mathcal H\):
\[
\epsilon_T(h)\le \hat\epsilon_S(h)+\sqrt{\frac{4}{m}\Big(d\log\frac{2em}{d}+\log\frac{4}{\delta}\Big)}+d_{\mathcal H}(\tilde D_S,\tilde D_T)+\lambda.
\]
- \(\hat\epsilon_S(h)\): empirical source error.
- \(d_{\mathcal H}(\tilde D_S,\tilde D_T)\): \(\mathcal H\)-divergence (domain discrepancy) between induced feature distributions.
- \(\lambda = \inf_{h\in\mathcal H}(\epsilon_S(h)+\epsilon_T(h))\): labeling-function disagreement term (conditional shift).
**Tutoring use:** counters “just align domains and you’re done”—\(\lambda\) can dominate.  
Source: https://proceedings.neurips.cc/paper/2006/file/b1b0432ceafb0ce714426e9114852ac7-Paper.pdf

### Invariant representations can fail (counterexample + lower bound intuition)
Zhao et al. show a counterexample where a representation \(g\) makes feature distributions perfectly invariant (\(D_{Z_S}=D_{Z_T}\)) yet forces joint error \(\epsilon_S(h\circ g)+\epsilon_T(h\circ g)=1\) for all \(h\). They also give an information-theoretic lower bound: if label marginals differ, forcing invariance can force large error.  
**Tutoring use:** pre-empt “domain-invariant features guarantee transfer.”  
Source: http://proceedings.mlr.press/v97/zhao19a/zhao19a.pdf

### SimOpt (Bayesian domain randomization loop) objectives + KL trust region
Chebotar et al. define DR training objective:
\[
\max_\theta \ \mathbb{E}_{\xi\sim p_\phi}\big[\mathbb{E}_{\pi_\theta}[R(\tau)]\big]
\]
and simulator distribution update:
\[
\min_{\phi_{i+1}} \ \mathbb{E}_{\xi_{i+1}\sim p_{\phi_{i+1}}}\big[\mathbb{E}_{\pi_{\theta,p_{\phi_i}}}[D(\tau^{ob}_\xi,\tau^{ob}_{real})]\big]
\quad \text{s.t.}\quad D_{KL}(p_{\phi_{i+1}}\|p_{\phi_i})\le \epsilon.
\]
- \(\xi\): simulator parameters; \(p_\phi(\xi)\) often Gaussian \(\mathcal N(\mu,\Sigma)\).
- \(D(\cdot)\): trajectory discrepancy (weighted \(\ell_1+\ell_2\) with smoothing).
**Claim supported:** “close the loop” with a few real rollouts while avoiding destabilizing distribution jumps via KL constraint.  
Source: https://arxiv.org/pdf/1810.05687.pdf

**SimOpt empirical numbers (real robots):**
- Swing-peg-in-hole (ABB Yumi): after **2** SimOpt iterations → **90% success over 20 trials**; per iteration includes **3 real rollouts** (plus sim training and REPS updates).  
- Drawer opening (Franka Panda): after **1** SimOpt update → **20/20 successful** openings.  
Source: https://arxiv.org/pdf/1810.05687.pdf

### ASID (active exploration for system identification): Fisher information objective
ASID uses Cramér–Rao style bound:
\[
\mathbb{E}\|\hat\theta-\theta\|^2 \ge \mathrm{tr}(I(\theta)^{-1})
\]
and chooses exploration policy via A-optimal design:
\[
\pi_{\text{exp}}^\* \in \arg\min_{\pi_{\text{exp}}}\ \mathrm{tr}\!\left(I(\theta;\pi_{\text{exp}})^{-1}\right).
\]
**Claim supported:** targeted exploration yields more informative real trajectories for identifying dynamics parameters.  
Source: https://arxiv.org/html/2404.12308v2

**ASID empirical outcomes (real-world):**
- Rod balancing: DR total **0/9** successes vs ASID **6/9**.
- Shuffleboard: DR **3/10** vs ASID **7/10**.  
Source: https://arxiv.org/html/2404.12308v2

### Concrete DR parameter ranges (humanoid locomotion recipe)
Humanoid-Gym reports DR ranges such as:
- system delay **0–10 ms (Uniform)**
- friction **0.1–2.0 (Uniform)**
- motor strength **95–105% (Gaussian scaling)**
- payload **±5 kg (Gaussian additive)**  
Also: policy **50 Hz**, PD inner loop **500 Hz**; training uses **8192 envs**.  
Source: https://arxiv.org/html/2404.05695v2

### i-S2R (iterative sim-to-real) key implementation facts + failure mode
- Adds ball observation noise: uniform noise per timestep of **2× ball diameter**.
- Must simulate sensor/action latency (Gaussian from real measurements) or transfer “**completely failed**.”
- Control frequency: **75 Hz**; stacks past **7** observations.  
**Empirical:** final **22 hits average**, **150 best** rally; i-S2R retains ~**70%** cross-player performance vs baseline ~**30%**.  
Source: https://proceedings.mlr.press/v205/abeyruwan23a/abeyruwan23a.pdf

### Visual DR ablations (manipulation) + success rates
In a visuomotor BC setup, full 3D DR (textures+lighting+object color+camera) yields **18.6/20** average real success (~93%) across tasks; “2D aug only” yields **0/20**.  
Source: https://arxiv.org/pdf/2307.15320.pdf

### UDA benchmark numbers (VisDA-2017)
VisDA-C (synthetic → real):
- Source-only AlexNet → real-val: **28.12%**
- Deep CORAL: **45.53%**
- DAN: **51.62%**
- Oracle AlexNet on real-val: **87.62%**  
Source: https://ar5iv.labs.arxiv.org/html/1710.06924

### Isaac Sim / Isaac Lab timing conversion for DR schedules
Isaac Sim API notes:
\[
\text{time\_s} = \text{num\_steps} \cdot (\text{decimation} \cdot dt)
\]
Source: https://docs.omniverse.nvidia.com/py/isaacsim/genindex.html

---

## How It Works

### A. Domain Randomization (DR) workflow (policy learning)
1. **Choose randomization parameters** \(\xi\) (physics: friction, masses, delays; visuals: textures, lighting, camera pose; sensor noise).
2. **Define a distribution** \(p_\phi(\xi)\) (often uniform ranges or Gaussian).
3. **Training loop:** for each episode, sample \(\xi \sim p_\phi\), instantiate sim with \(\xi\), roll out policy, update policy to maximize expected return under \(p_\phi\) (SimOpt Eq. 1 gives the canonical expectation form).
4. **Deploy** policy in real (zero-shot) or with limited fine-tuning.

**Tutor move:** ask what is being randomized (dynamics vs observation vs latency) and whether the real world is plausibly inside the support of \(p_\phi\).

### B. Real-data-guided DR (SimOpt-style progressive transfer)
1. Initialize simulator parameter distribution \(p_{\phi_0}(\xi)\).
2. Train policy in sim under \(p_{\phi_i}\).
3. Collect a small number of **real rollouts** under the current policy.
4. For many sampled \(\xi\), run sim rollouts and compute discrepancy \(D(\tau^{ob}_\xi,\tau^{ob}_{real})\).
5. Update \(p_{\phi_{i+1}}\) to reduce expected discrepancy **subject to** KL constraint \(D_{KL}(p_{\phi_{i+1}}\|p_{\phi_i})\le \epsilon\).
6. Repeat until transfer is satisfactory.  
Source: https://arxiv.org/pdf/1810.05687.pdf

### C. Active system identification (ASID-style)
1. Assume real dynamics are in a parametric family \(P_\theta\) with unknown \(\theta^\*\).
2. Train an **exploration policy** \(\pi_{\text{exp}}\) to maximize information about \(\theta\) (minimize \(\mathrm{tr}(I^{-1})\)).
3. Run **one real episode** with \(\pi_{\text{exp}}\) to collect trajectory \(\tau\).
4. Fit parameter distribution \(p(\theta)\) (or point estimate) by matching real \(\tau\) with simulated rollouts under the same action sequence.
5. Train task policy in the identified simulator; deploy zero-shot.  
Source: https://arxiv.org/html/2404.12308v2

### D. Iterative sim↔real in human-in-the-loop settings (i-S2R)
1. Collect initial real human-only data \(D_0\) (no robot).
2. Fit initial human ball distribution model \(M_0\) (min/max bounds over initial pos/vel and landing).
3. Train policy in sim on balls sampled from \(M_k\) → \(\theta_k^S\).
4. Deploy and **real fine-tune with human-in-loop** → \(\theta_k^R\); collect interaction data.
5. Update dataset \(D_{k+1}\), refit \(M_{k+1}\), continue sim training from \(\theta_k^R\).
6. Stop when model deltas shrink (they found ~3 iterations sufficient).  
Source: https://proceedings.mlr.press/v205/abeyruwan23a/abeyruwan23a.pdf

### E. “Sim2Sim” validation as a safety/robustness gate (Humanoid-Gym)
1. Train in a fast simulator (Isaac Gym).
2. Validate robustness in a different simulator with different modeling assumptions (MuJoCo).
3. Only then deploy to real (reported zero-shot on two humanoids).  
Source: https://arxiv.org/html/2404.05695v2

---

## Teaching Approaches

### Intuitive (no math)
- **DR:** “Make the simulator a *training gym* with lots of variations so the policy learns what matters and ignores what doesn’t.”
- **SysID:** “Instead of making the policy robust to many worlds, try to make the simulated world match *this* real robot.”
- **DA:** “Use real (often unlabeled) data to adjust the model so its internal features look similar across sim and real.”

### Technical (with math)
- **DR objective:** optimize expected return under randomized simulator parameters (SimOpt Eq. 1).
- **SimOpt loop:** alternate \(\theta\)-updates (policy) with \(\phi\)-updates (sim distribution) using discrepancy minimization under KL trust region (SimOpt Eq. 3).
- **DA bound:** target error is bounded by source error + domain discrepancy + labeling disagreement \(\lambda\) (Ben-David Thm. 1), so aligning distributions alone is insufficient if \(\lambda\) is large.

### Analogy-based
- **DR as “vaccination”:** expose the policy to many “strains” (variations) so it’s immune to real-world perturbations.
- **SysID as “prescription glasses”:** tune parameters until the simulator “sees” the world like the robot does.
- **Sim2Sim as “wind tunnel testing”:** test in a second facility (different simulator) to catch overfitting to one simulator’s quirks.

---

## Common Misconceptions (required)

1. **“If I randomize *a lot*, transfer is guaranteed.”**  
   - **Why wrong:** SimOpt reports that overly wide randomization can include infeasible instances and can produce conservative/failing policies (e.g., drawer task sensitivity to cabinet-position std; wide offsets hinder learning).  
   - **Correct model:** DR must be *plausible and learnable*; sometimes you need **progressive** updates (SimOpt) rather than “maximally wide” from the start.  
   Source: https://arxiv.org/pdf/1810.05687.pdf

2. **“Domain-invariant features + low source error implies low target error.”**  
   - **Why wrong:** Ben-David’s bound includes \(\lambda\) (labeling disagreement), and Zhao et al. give explicit counterexamples where perfect invariance forces high joint error.  
   - **Correct model:** You need both (i) small discrepancy and (ii) small conditional/label shift (small \(\lambda\)); invariance can be harmful when label marginals differ.  
   Sources: https://proceedings.neurips.cc/paper/2006/file/b1b0432ceafb0ce714426e9114852ac7-Paper.pdf and http://proceedings.mlr.press/v97/zhao19a/zhao19a.pdf

3. **“Only physics parameters matter; observation delay/noise is secondary.”**  
   - **Why wrong:** i-S2R reports transfer “completely failed” without simulating sensor/action latency from real measurements; they also inject substantial ball observation noise (2× ball diameter).  
   - **Correct model:** The “dynamics” the policy experiences includes sensing, latency, and control interfaces; mismodeling these can dominate the reality gap.  
   Source: https://proceedings.mlr.press/v205/abeyruwan23a/abeyruwan23a.pdf

4. **“One simulator is enough; if it works in sim, it’s safe to try on hardware.”**  
   - **Why wrong:** Humanoid-Gym explicitly uses **sim2sim** (Isaac Gym → MuJoCo) before real deployment, implying single-simulator success is not a robust indicator.  
   - **Correct model:** Use staged validation: cross-simulator checks can reveal simulator-specific overfitting before risking hardware.  
   Source: https://arxiv.org/html/2404.05695v2

5. **“Domain adaptation always helps if I have unlabeled real data.”**  
   - **Why wrong:** Zhao et al. show DA/invariance can degrade target performance under label-marginal mismatch; SKADA-Bench also emphasizes realistic model selection is hard without labels and unsupervised scorers can correlate weakly/variably with accuracy.  
   - **Correct model:** DA needs careful assumptions (shift type) and careful validation protocols; unlabeled target data is not a free win.  
   Sources: http://proceedings.mlr.press/v97/zhao19a/zhao19a.pdf and https://arxiv.org/html/2407.11676v2

---

## Worked Examples

### 1) Minimal SimOpt-style loop (pseudocode you can adapt)
Grounded in SimOpt Algorithm 1 + objectives (Chebotar et al.). This is *structure*, not a full implementation.

```python
# SimOpt-style progressive sim-to-real (structure)
# Source: https://arxiv.org/pdf/1810.05687.pdf

phi = init_sim_param_distribution()   # e.g., Gaussian N(mu, Sigma)
theta = init_policy()

for i in range(num_simopt_iters):
    # (A) Train policy in randomized sim
    for _ in range(num_rl_iters):
        xi = sample(phi)              # simulator parameters
        tau = rollout_sim(policy=theta, sim_params=xi)
        theta = rl_update(theta, tau) # maximize E_{xi~p_phi}[R(tau)]

    # (B) Collect a few real rollouts
    tau_real = rollout_real(policy=theta, num_rollouts=K_real)

    # (C) Evaluate discrepancy for many sampled sim params
    costs = []
    xis = [sample(phi) for _ in range(N_samples)]
    for xi in xis:
        tau_sim_obs = rollout_sim_observations(policy=theta, sim_params=xi)
        c = discrepancy(tau_sim_obs, tau_real)  # weighted L1+L2 + smoothing in paper
        costs.append(c)

    # (D) Update phi to reduce expected discrepancy with KL trust region
    phi = reps_update_with_kl_trust_region(phi, xis, costs, epsilon=kl_budget)
```

**Tutor prompts while stepping through:**
- “What are your \(\xi\) parameters—friction? delay? camera pose?”
- “What observation trajectory do you compare in \(D(\cdot)\) (paper allows partial observations)?”
- “Why the KL constraint?” → to avoid destabilizing jumps in \(p_\phi\) (SimOpt Eq. 3).

### 2) Concrete DR parameter checklist (humanoid locomotion)
Use Humanoid-Gym’s reported DR ranges as a ready-made starting point:
- Delay: uniform **0–10 ms**
- Friction: uniform **0.1–2.0**
- Motor strength: Gaussian scaling **95–105%**
- Payload: Gaussian additive **±5 kg**
- Policy rate **50 Hz**, PD inner loop **500 Hz**  
Source: https://arxiv.org/html/2404.05695v2

**Tutor use:** when a student asks “what do I randomize and by how much?”—quote these as an existence proof and then ask what their robot’s analogous parameters are.

---

## Comparisons & Trade-offs

| Approach | Uses real data during adaptation? | Main lever | Strengths (per sources) | Failure modes / cautions (per sources) | When to choose |
|---|---:|---|---|---|---|
| Domain Randomization (DR) | Optional (can be none) | Robustness via variability | Can enable zero-shot transfer (Tobin; Humanoid-Gym recipe) | Too-wide DR can hinder learning / include infeasible sims (SimOpt) | When real data is scarce; when you can randomize key uncertainties |
| Real-data-guided DR (SimOpt) | Yes (few rollouts/iter) | Update \(p_\phi(\xi)\) to match real trajectories | High real success with few rollouts (e.g., 20/20 drawer after 1 update) | Needs discrepancy design; iterative overhead | When you can afford small real rollouts and want principled simulator distribution tuning |
| System ID (ASID) | Yes (targeted episode) | Identify dynamics parameters \(\theta\) | Can beat DR with very little real data (single episode often) | Requires parametric family; exploration design | When dynamics are parameterizable and you can run informative exploration safely |
| Domain Adaptation (DANN-style) | Yes (unlabeled target) | Learn domain-invariant features | Strong in classic UDA settings (Ganin) | Invariance can fail under label shift; \(\lambda\) term matters (Zhao; Ben-David) | When you have unlabeled target data and shift assumptions are plausible |

---

## Prerequisite Connections

- **MDPs/POMDPs and policy learning:** Humanoid-Gym explicitly frames real deployment as POMDP and uses asymmetric actor-critic (https://arxiv.org/html/2404.05695v2).
- **Distribution shift basics (covariate/conditional/label shift):** Needed to interpret DA bounds and why invariance can fail (Ben-David 2006; Zhao 2019).
- **Physics simulation interfaces (control rate, latency, PD control):** Needed to understand why modeling delay/noise can dominate transfer (i-S2R; Humanoid-Gym).
- **Basic optimization / trust regions:** Needed to understand SimOpt’s KL-constrained updates and why they stabilize iterative distribution changes (SimOpt).

---

## Socratic Question Bank

1. **“What specific mismatch do you think is causing the reality gap in your setup—dynamics, sensing, latency, or visuals?”**  
   *Good answer:* names concrete parameters (e.g., friction, delay 0–10 ms, camera pose) and ties them to observed failures.

2. **“If you widen your randomization ranges, what’s the downside?”**  
   *Good answer:* mentions infeasible sims / conservative policies (SimOpt’s warning about overly wide randomization).

3. **“Suppose you perfectly align feature distributions between sim and real. What term in the DA bound can still make target error large?”**  
   *Good answer:* \(\lambda\) (labeling disagreement / conditional shift) from Ben-David.

4. **“How would you test whether your policy is overfitting to one simulator’s quirks before touching hardware?”**  
   *Good answer:* proposes sim2sim validation (Isaac Gym → MuJoCo) as in Humanoid-Gym.

5. **“What would an ‘informative’ real trajectory look like for system identification?”**  
   *Good answer:* trajectory that makes dynamics sensitive to parameters; references Fisher information idea (ASID).

6. **“Why might modeling latency be more important than matching friction in some tasks?”**  
   *Good answer:* points to i-S2R’s ‘transfer completely failed’ without latency modeling.

7. **“If you have unlabeled real images, would you prefer DR or DA—and what assumption decides?”**  
   *Good answer:* discusses whether label/conditional shift is present; cites Zhao counterexample risk for invariance.

8. **“What would you randomize first: visuals or dynamics? Why?”**  
   *Good answer:* depends on observation modality; for vision-heavy tasks, cites DR ablations showing textures/lighting/camera matter (https://arxiv.org/pdf/2307.15320.pdf).

---

## Likely Student Questions

**Q: “What’s the formal reason domain adaptation can fail even if features are invariant?”**  
→ **A:** Ben-David’s target-risk bound includes a labeling disagreement term \(\lambda=\inf_{h\in\mathcal H}(\epsilon_S(h)+\epsilon_T(h))\), so even if domain discrepancy \(d_{\mathcal H}\) is small, target error can be large when \(\lambda\) is large (conditional shift). Zhao et al. give a counterexample where \(D_{Z_S}=D_{Z_T}\) but \(\epsilon_S(h\circ g)+\epsilon_T(h\circ g)=1\) for all \(h\). Sources: https://proceedings.neurips.cc/paper/2006/file/b1b0432ceafb0ce714426e9114852ac7-Paper.pdf and http://proceedings.mlr.press/v97/zhao19a/zhao19a.pdf

**Q: “What’s SimOpt, mechanically?”**  
→ **A:** SimOpt alternates (i) training a policy in sim under randomized parameters \(\xi\sim p_\phi(\xi)\) and (ii) updating \(p_\phi\) to minimize discrepancy between simulated and real observation trajectories, with a KL trust-region constraint \(D_{KL}(p_{\phi_{i+1}}\|p_{\phi_i})\le\epsilon\). Source: https://arxiv.org/pdf/1810.05687.pdf

**Q: “Do you have real numbers showing SimOpt works with few real trials?”**  
→ **A:** In SimOpt’s drawer opening on a real Franka Panda, after **1** SimOpt update they report **20/20** successful openings; swing-peg-in-hole reaches **90% success over 20 trials** after **2** iterations. Source: https://arxiv.org/pdf/1810.05687.pdf

**Q: “What should I randomize for locomotion sim-to-real?”**  
→ **A:** Humanoid-Gym reports DR including system delay **0–10 ms (Uniform)**, friction **0.1–2.0 (Uniform)**, motor strength **95–105% (Gaussian scaling)**, payload **±5 kg (Gaussian additive)**; policy runs at **50 Hz** with PD at **500 Hz**. Source: https://arxiv.org/html/2404.05695v2

**Q: “Is latency actually that important?”**  
→ **A:** In i-S2R table tennis, they report that without simulating sensor/action latency (Gaussian from real measurements), transfer “**completely failed**.” Source: https://proceedings.mlr.press/v205/abeyruwan23a/abeyruwan23a.pdf

**Q: “How do I pick DR parameters for vision-based manipulation?”**  
→ **A:** In the visuomotor BC study, full 3D DR (textures+lighting+object color+camera) yields **18.6/20** average real success (~93%), while “2D aug only” yields **0/20**. Source: https://arxiv.org/pdf/2307.15320.pdf

**Q: “What’s a standard sim-to-real UDA benchmark and baseline gap?”**  
→ **A:** VisDA-2017 classification (synthetic→real) reports source-only AlexNet **28.12%** on real validation, while oracle AlexNet on real validation is **87.62%**; adaptation baselines include Deep CORAL **45.53%** and DAN **51.62%**. Source: https://ar5iv.labs.arxiv.org/html/1710.06924

**Q: “In Isaac Sim / Isaac Lab, how do I convert ‘randomize every N steps’ into seconds?”**  
→ **A:** Isaac Sim’s API index gives: \(\text{time\_s} = \text{num\_steps} \cdot (\text{decimation} \cdot dt)\), where \(dt\) is sim timestep and decimation maps sim steps to control steps. Source: https://docs.omniverse.nvidia.com/py/isaacsim/genindex.html

---

## Available Resources

### Videos
- [Yannic Kilcher — “Domain Adaptation / Transfer Learning overview”](https://arxiv.org/abs/2010.03978) — **Surface when:** student asks for a single coherent overview of DA concepts/assumptions and how methods relate.

### Articles & Tutorials
- [Lilian Weng — “Domain Randomization for Sim-to-Real Transfer”](https://lilianweng.github.io/posts/2019-05-05-domain-randomization/) — **Surface when:** student needs the landscape (SysID vs DR vs DA) and practical DR considerations.
- [OpenAI — “Learning Dexterity” (Dactyl)](https://openai.com/index/learning-dexterity/) — **Surface when:** student asks for a high-profile, detailed sim-to-real case study using domain randomization at scale.
- [Tobin et al. (2017) — “Domain Randomization…”](https://arxiv.org/abs/1703.06907) — **Surface when:** student asks for the canonical origin story / core claim of DR for vision transfer.

---

## Visual Aids

![Three approaches to sim2real transfer: system ID, domain randomization, and domain adaptation.](/api/wiki-images/physics-simulation/images/lilianweng-posts-2019-05-05-domain-randomization_001.png)  
**Show when:** student is confused about how DR vs DA vs SysID differ; use as a map before diving into any one method.

![SimOpt iteratively aligns simulator and real-world trajectory distributions. (Chebotar et al., 2019)](/api/wiki-images/physics-simulation/images/lilianweng-posts-2019-05-05-domain-randomization_004.png)  
**Show when:** student asks “what does it mean to close the loop with real data?” or “how is SimOpt different from plain DR?”

![RCAN translates randomized or real images to canonical simulator views. (James et al., 2019)](/api/wiki-images/physics-simulation/images/lilianweng-posts-2019-05-05-domain-randomization_005.png)  
**Show when:** student asks about image-based domain adaptation vs “randomize sim until real fits.”

---

## Key Sources

- [Domain Randomization for Sim-to-Real Transfer (Weng)](https://lilianweng.github.io/posts/2019-05-05-domain-randomization/) — best single written map of DR/DA/SysID and the reality gap framing.
- [SimOpt / Bayesian Domain Randomization Loop (Chebotar et al.)](https://arxiv.org/pdf/1810.05687.pdf) — canonical progressive sim↔real loop with KL-constrained simulator distribution updates + real-robot success numbers.
- [ASID—Active Exploration for System Identification](https://arxiv.org/html/2404.12308v2) — concrete “Sim→Real→Sim→Real” pipeline with Fisher-information objective and real-world comparisons vs DR.
- [i-S2R for Human-Robot Table Tennis (Abeyruwan et al.)](https://proceedings.mlr.press/v205/abeyruwan23a/abeyruwan23a.pdf) — strong evidence that latency/noise modeling and iterative real-data updates matter in tight HRI sim-to-real.
- [Domain Adaptation Bound (Ben-David et al., 2006)](https://proceedings.neurips.cc/paper/2006/file/b1b0432ceafb0ce714426e9114852ac7-Paper.pdf) — the go-to formal decomposition: source error + discrepancy + labeling disagreement \(\lambda\).