## Core Definitions

**Imitation learning (IL).** Learning a policy from **expert demonstrations** rather than from an explicit reward function; in the sequential setting, the learner’s future observations depend on its past actions, so standard i.i.d. supervised learning assumptions can fail due to **distribution shift** between expert-visited states and learner-visited states (Ross et al., 2011 AISTATS; proceedings.mlr.press/v15/ross11a.html; arxiv.org/abs/1011.0686).

**Demonstration / expert trajectory.** A dataset of state(-observation) and action pairs (often grouped into trajectories/episodes) produced by an expert policy \(\pi^*\); used as training data for behavior cloning or as expert samples for adversarial/IRL-style methods (Ross et al., 2011; GAIL paper arxiv.org/pdf/1606.03476.pdf).

**Teleoperation.** A practical way to collect demonstrations where a human directly controls the robot to generate expert actions; in IL pipelines this is typically the source of \((s,a)\) labels used for behavior cloning/DAgger-style aggregation (implied by “expert demonstrations” collection in IL workflows; see DAgger interactive collection API in imitation.readthedocs).

**Behavior cloning (BC).** A direct supervised-learning approach that fits a policy \(\pi_\theta(a\mid o,\ell)\) to maximize likelihood (or minimize negative log-likelihood) of expert actions under the demonstration dataset; e.g., RT-1 explicitly trains by minimizing \(\mathbb{E}_{(o,\ell,a)\sim D}[-\log \pi_\theta(a\mid o,\ell)]\) (RT-1: arxiv.org/html/2212.06817v2).

**Distribution shift / covariate shift (in IL).** The mismatch between the state distribution in the training data (typically \(d^{\pi^*}\), states visited by the expert) and the state distribution induced at test time by the learned policy (typically \(d^\pi\)); this causes compounding errors in sequential prediction (Ross et al., 2011 AISTATS; proceedings.mlr.press/v15/ross11a.html).

**DAgger (Dataset Aggregation).** An iterative imitation learning algorithm that repeatedly (i) rolls out the current learned policy (often mixed with the expert), (ii) queries the expert for the correct action on the visited states, (iii) aggregates all collected labeled data, and (iv) retrains a stationary policy on the aggregated dataset; it is analyzed as a reduction to **no-regret online learning** (Ross et al., 2011 AISTATS; proceedings.mlr.press/v15/ross11a.html).

**Inverse reinforcement learning (IRL).** A family of methods that infer a cost/reward function that explains expert behavior, then derive a policy by solving an RL problem under that inferred cost; GAIL is derived from regularized maximum causal entropy IRL but avoids explicitly outputting a reward by directly matching occupancy measures (GAIL: arxiv.org/pdf/1606.03476.pdf; NeurIPS’16 paper PDF).

**Occupancy measure.** The discounted visitation distribution over state-action pairs under a policy: \(\rho_\pi(s,a)=\pi(a|s)\sum_{t\ge0}\gamma^t P(s_t=s\mid \pi)\); matching \(\rho_\pi\) to expert \(\rho_{\pi_E}\) is a core objective in GAIL (arxiv.org/pdf/1606.03476.pdf).

**GAIL (Generative Adversarial Imitation Learning).** An imitation learning method that trains a policy to match the expert’s occupancy measure by solving a GAN-like minimax game between a discriminator \(D(s,a)\) and the policy; the resulting objective corresponds (up to constants/regularization) to minimizing Jensen–Shannon divergence between \(\rho_\pi\) and \(\rho_{\pi_E}\) with an entropy regularizer (arxiv.org/pdf/1606.03476.pdf; NeurIPS’16 paper PDF).

---

## Key Formulas & Empirical Results

### Behavior cloning objective (RT-1)
\[
\min_\theta \; \mathbb{E}_{(o,\ell,a)\sim D}\left[-\log \pi_\theta(a\mid o,\ell)\right]
\]
- **Variables:** \(o\)=observation (RT-1 uses a history of images), \(\ell\)=language instruction, \(a\)=demonstrated action, \(D\)=demo dataset.
- **Supports claim:** BC is supervised learning on demonstrations (RT-1: https://arxiv.org/html/2212.06817v2).

### Sequential IL state distributions and total cost (Ross et al., 2011)
- \(d_t^\pi\): state distribution at time \(t\) when executing \(\pi\) from steps \(1..t-1\).  
- \(d^\pi=\frac1T\sum_{t=1}^T d_t^\pi\).  
- Immediate cost \(C(s,a)\in[0,1]\); \(C^\pi(s)=\mathbb E_{a\sim\pi(s)}[C(s,a)]\).  
- Total cost:
\[
J(\pi)=\sum_{t=1}^T \mathbb E_{s\sim d_t^\pi}[C^\pi(s)]=T\,\mathbb E_{s\sim d^\pi}[C^\pi(s)].
\]
(Ross et al., AISTATS’11: https://www.ri.cmu.edu/pub_files/2011/4/Ross-AISTATS11-NoRegret.pdf)

### Imitation objective highlights non-i.i.d. issue (Ross et al., 2011)
\[
\hat\pi=\arg\min_{\pi\in\Pi}\mathbb E_{s\sim d^\pi}[\ell(s,\pi)]
\]
- **Key point:** the expectation is under \(d^\pi\), the learner-induced distribution, not the expert’s distribution (Ross et al., 2011).

### Behavior cloning compounding error bound (Ross et al., 2011 Thm 2.1)
If \(\mathbb E_{s\sim d^{\pi^*}}[\ell(s,\pi)]=\epsilon\), then
\[
J(\pi)\le J(\pi^*)+T^2\epsilon.
\]
- **Supports claim:** small per-step imitation error under expert states can yield **quadratic** degradation over horizon \(T\) due to distribution shift (Ross et al., 2011).

### DAgger algorithm (Ross et al., 2011 Alg. 3.1) + mixing coefficient
At iteration \(i\), execute mixed policy:
\[
\pi_i=\beta_i\pi^*+(1-\beta_i)\hat\pi_i
\]
collect visited states labeled by expert, aggregate datasets, retrain.
- **\(\beta_i\)** is the probability of taking the expert action during data collection (Ross et al., 2011; also mirrored in `imitation` library docs).

### No-regret online learning connection (Ross et al., 2011 Eq. 3)
Online regret:
\[
\frac1N\sum_{i=1}^N \ell_i(\pi_i)-\min_{\pi\in\Pi}\frac1N\sum_{i=1}^N \ell_i(\pi)\le \gamma_N,\quad \gamma_N\to0
\]
with \(\ell_i(\pi)=\mathbb E_{s\sim d^{\pi_i}}[\ell(s,\pi)]\).
- **Supports claim:** if the learner is no-regret, DAgger finds a policy that performs well on its own induced distribution (Ross et al., 2011).

### DAgger distribution mismatch lemma (Ross et al., 2011 Lemma 4.1)
\[
\|d^{\pi_i}-d^{\hat\pi_i}\|_1\le 2T\beta_i.
\]
- **Supports claim:** as \(\beta_i\) decreases, the executed distribution approaches the learned policy’s distribution (Ross et al., 2011).

### DAgger core guarantee (Ross et al., 2011 Thm 4.1; abbreviated)
There exists \(\hat\pi\in\{\hat\pi_1.. \hat\pi_N\}\) such that
\[
\mathbb E_{s\sim d^{\hat\pi}}[\ell(s,\hat\pi)]\le \epsilon_N+\gamma_N+\frac{2\ell_{\max}}{N}\Big[n_\beta+T\sum_{i=n_\beta+1}^N\beta_i\Big]
\]
with \(\epsilon_N=\min_{\pi\in\Pi}\frac1N\sum_i \mathbb E_{s\sim d^{\pi_i}}[\ell(s,\pi)]\).
(Ross et al., 2011)

### GAIL: occupancy-measure matching and GAN objective
- Max causal entropy IRL form (GAIL Eq. 1):
\[
\max_{c\in\mathcal C}\Big(\min_{\pi\in\Pi}-H(\pi)+\mathbb E_\pi[c(s,a)]\Big)-\mathbb E_{\pi_E}[c(s,a)]
\]
with causal entropy \(H(\pi)=\mathbb E_\pi[-\log \pi(a|s)]\). (https://arxiv.org/pdf/1606.03476.pdf)

- GAIL regularizer yields GAN loss (Eq. 14):
\[
\max_{D:(S\times A)\to(0,1)}\mathbb E_\pi[\log D]+\mathbb E_{\pi_E}[\log(1-D)].
\]
- Equivalent policy objective (Eq. 15):
\[
\min_\pi D_{JS}(\rho_\pi,\rho_E)-\lambda H(\pi).
\]
(https://arxiv.org/pdf/1606.03476.pdf; also NeurIPS’16 PDF)

### Implementation defaults / API facts (imitation library)
- `DAggerTrainer.DEFAULT_N_EPOCHS = 4` used by `extend_and_update()` if neither `n_epochs` nor `n_batches` provided.
- `beta_schedule=None` defaults to `linear_beta_schedule`.
- Interactive collector executes expert action w.p. \(\beta\), robot action w.p. \(1-\beta\); **saved demos always record expert actions** regardless of what was executed.
(https://imitation.readthedocs.io/en/latest/_api/imitation.algorithms.dagger.html)

### Empirical success rates (RT-1, RT-2) and GAIL vs BC
- **RT-1 real-robot success (Table 2):** Seen **97%**, Unseen **76%**, Distractors **83%**, Backgrounds **59%** (https://arxiv.org/html/2212.06817v2; also summarized at https://robotics-transformer1.github.io).
- **RT-2 (Language-Table sim Table 1):** RT-2-PaLI-3B **90±10** vs BC-Zero **72±3** (https://proceedings.mlr.press/v229/zitkovich23a/zitkovich23a.pdf).
- **GAIL vs BC (MuJoCo Table 3):** Humanoid-v1 with 80 expert traj: **GAIL 10200.73±1324.47** vs **BC 1397.06±1057.84** (https://arxiv.org/pdf/1606.03476.pdf).

---

## How It Works

### Behavior Cloning (BC): mechanics
1. **Collect demonstrations** \(D=\{(o_t,\ell,a_t)\}\) (often via teleoperation).
2. **Choose policy parameterization** \(\pi_\theta(a\mid o,\ell)\) (classification over discretized actions in RT-1/RT-2; RT-1 discretizes each action dimension into 256 bins).
3. **Train supervised objective**: minimize negative log-likelihood of expert actions (RT-1 formula above).
4. **Deploy policy closed-loop**: at each timestep, feed current observation/history and instruction, sample/argmax action token(s), execute.

### Why BC fails in sequential settings (distribution shift loop)
1. Train on expert distribution \(d^{\pi^*}\).
2. At test time, small action errors move the agent into states the expert rarely visits.
3. The policy has no training labels for those off-distribution states → error rate increases.
4. Errors compound over horizon \(T\), yielding the \(T^2\epsilon\) style bound (Ross et al., 2011 Thm 2.1).

### DAgger (Ross et al., 2011 Alg. 3.1): mechanics
**Goal:** collect labels on the learner’s induced states.

Algorithm sketch (stationary policy training with dataset aggregation):
1. Initialize dataset \(D \leftarrow \emptyset\). Initialize policy \(\hat\pi_1\) (often from initial expert demos / BC).
2. For rounds \(i=1..N\):
   1. **Roll out** a mixed policy \(\pi_i=\beta_i\pi^*+(1-\beta_i)\hat\pi_i\).
   2. **Record visited states** \(s\) (or observations \(o\)).
   3. **Query expert** for each visited state: label \(a^*=\pi^*(s)\).
   4. Aggregate: \(D \leftarrow D \cup \{(s,a^*)\}\).
   5. **Train** next policy \(\hat\pi_{i+1}\) on aggregated \(D\) (supervised learning).
3. **Return** best \(\hat\pi_i\) (Ross et al. mention selecting best on validation).

Practical note from `imitation` library:
- In interactive collection, the environment may execute expert actions with probability \(\beta\), but the stored dataset logs **expert actions** for supervision (imitation.readthedocs DAgger API).

### GAIL: mechanics (GAN-style imitation)
1. **Inputs:** expert trajectories \(\tau_E\) (state-action samples) and an initial policy \(\pi_\theta\).
2. **Discriminator update:** train \(D_w(s,a)\in(0,1)\) to classify policy samples vs expert samples by maximizing:
   \[
   \mathbb E_{\pi_\theta}[\log D_w(s,a)] + \mathbb E_{\pi_E}[\log(1-D_w(s,a))]
   \]
   (GAIL Eq. 14).
3. **Policy update:** treat a discriminator-derived cost \(c(s,a)=\log D_w(s,a)\) (as stated in the algorithm description) and update \(\pi_\theta\) with an RL algorithm (the paper uses TRPO) while also applying entropy regularization \(-\lambda H(\pi)\) (GAIL Eq. 16–18).
4. Alternate steps 2–3 until occupancy measures match (conceptually minimizing \(D_{JS}(\rho_\pi,\rho_E)\) with entropy term; GAIL Eq. 15).

---

## Teaching Approaches

### Intuitive (no math): “Learn from corrections where you actually go”
- **BC** is like copying a driving instructor by watching only perfect highway driving; once you drift slightly, you end up on roads you never practiced.
- **DAgger** fixes this by letting the student drive; whenever the student reaches a new situation, the instructor tells them what they *should* do there, and those situations get added to the practice set.
- **GAIL** doesn’t copy actions directly; it tries to make the learner’s overall “footprint” of behavior indistinguishable from the expert’s, using an adversarial judge.

### Technical (with math): distributions \(d^{\pi^*}\) vs \(d^\pi\)
- BC minimizes imitation loss on \(s\sim d^{\pi^*}\), but performance depends on \(s\sim d^\pi\).
- Ross et al. formalize sequential cost \(J(\pi)\) and show compounding error: if per-step error under expert states is \(\epsilon\), then \(J(\pi)\le J(\pi^*)+T^2\epsilon\).
- DAgger defines per-round losses \(\ell_i(\pi)=\mathbb E_{s\sim d^{\pi_i}}[\ell(s,\pi)]\) and uses no-regret learning to guarantee existence of a policy with low loss under its own induced distribution (Thm 4.1).

### Analogy-based: “Exam questions vs homework questions”
- BC trains on “homework questions” written by the expert (expert states).
- Deployment is an “exam” where your own earlier answers determine which questions you see next (learner-induced states).
- DAgger is like taking practice exams where a teacher annotates *your* wrong turns, so the training distribution becomes the exam distribution.

---

## Common Misconceptions (required)

1. **“If my behavior cloning accuracy is high on the demo dataset, the robot will work fine.”**  
   - **Why wrong:** BC accuracy is measured on states from \(d^{\pi^*}\), but at test time the robot visits states from \(d^\pi\); small errors change future states, causing compounding errors. Ross et al. show a \(T^2\epsilon\) degradation bound (Thm 2.1).  
   - **Correct model:** In sequential decision-making, you must care about performance under the **policy-induced distribution** \(d^\pi\), not just the expert’s distribution.

2. **“DAgger just adds more data; it’s basically the same as collecting more expert demos offline.”**  
   - **Why wrong:** DAgger’s key is *which* data: it labels states visited by the learner (or a learner/expert mixture), directly targeting distribution shift (Alg. 3.1).  
   - **Correct model:** DAgger is **interactive** dataset construction to approximate training on \(d^\pi\).

3. **“In DAgger, the actions executed during rollouts are the labels saved for training.”**  
   - **Why wrong:** In the `imitation` library’s interactive collector, executed actions may be expert or robot depending on \(\beta\), but **saved demos always record expert actions** (imitation.readthedocs DAgger API).  
   - **Correct model:** Execution is for reaching relevant states; supervision is always the expert’s action on those states.

4. **“GAIL is just behavior cloning with a discriminator.”**  
   - **Why wrong:** GAIL’s objective is occupancy-measure matching via a GAN loss (Eq. 14) and is equivalent to minimizing \(D_{JS}(\rho_\pi,\rho_E)\) with entropy regularization (Eq. 15), not supervised action matching.  
   - **Correct model:** GAIL learns a policy through an RL loop using discriminator-derived costs, aiming to match **state-action visitation frequencies**, not necessarily per-state action labels.

5. **“Inverse RL always recovers the true reward the expert had.”**  
   - **Why wrong:** The GAIL derivation shows IRL is posed as an optimization over costs with regularization (max causal entropy IRL form), and the end result can be framed as matching occupancy measures rather than uniquely identifying a reward (GAIL Eq. 1–4, Prop. 3.2 style statements).  
   - **Correct model:** Many rewards can explain the same behavior; regularization/entropy selects among them, and some methods (GAIL) bypass explicit reward recovery.

---

## Worked Examples

### Example A: Minimal DAgger loop (pseudocode you can adapt)
This mirrors Ross et al. Alg. 3.1 and the `imitation` library’s “rounds” concept.

```python
# Pseudocode: DAgger with dataset aggregation
D = []  # aggregated dataset of (obs, expert_action)
pi_hat = initialize_policy_via_BC(initial_expert_demos)  # optional

for i in range(1, N_rounds + 1):
    beta = beta_schedule(i)  # e.g., 1.0 for i=1 then 0.0 afterwards (Ross et al. mention this common choice)
    trajectories = []

    obs = env.reset()
    done = False
    while not done:
        a_robot = pi_hat.act(obs)
        a_expert = expert.act(obs)

        # execute mixed policy
        if random.uniform(0, 1) < beta:
            a_exec = a_expert
        else:
            a_exec = a_robot

        next_obs, rew, done, info = env.step(a_exec)

        # IMPORTANT: label with expert action (as in DAgger)
        D.append((obs, a_expert))

        obs = next_obs

    # supervised update on aggregated dataset
    pi_hat = supervised_train(pi_hat, D)

# return best checkpoint by validation (Ross et al. recommend selecting best)
return pi_hat
```

**Tutor prompts while using this example**
- Ask the student to identify where distribution shift is addressed (the line `D.append((obs, a_expert))` on learner-visited `obs`).
- Ask what happens if `beta` stays at 1 forever (you revert to expert-only states → BC-like).

### Example B: GAIL objective components (what to compute each iteration)
Use this to ground “what is the discriminator loss?” and “what reward does the policy see?”

1. Sample policy rollouts \((s,a)\sim \pi_\theta\).
2. Sample expert pairs \((s,a)\sim \pi_E\).
3. Update discriminator \(D_w\) to maximize:
   \[
   \mathbb E_{\pi_\theta}[\log D_w(s,a)] + \mathbb E_{\pi_E}[\log(1-D_w(s,a))]
   \]
   (GAIL Eq. 14).
4. Define cost for RL update as \(c(s,a)=\log D_w(s,a)\) (as described in the training procedure in the paper).
5. Update \(\pi_\theta\) with an RL method (paper uses TRPO) plus entropy regularization \(-\lambda H(\pi)\) (GAIL Eq. 16–18).

---

## Comparisons & Trade-offs

| Method | What supervision you need | Core objective (from sources) | Main failure mode | When it’s a good choice |
|---|---|---|---|---|
| Behavior Cloning (BC) | Offline expert \((o,\ell,a)\) pairs | Minimize \(\mathbb{E}[-\log \pi_\theta(a\mid o,\ell)]\) (RT-1) | Distribution shift / compounding errors (Ross Thm 2.1) | When you can collect lots of diverse demos and distribution shift is limited (RT-1/RT-2 style scaling shows strong results with large diverse data) |
| DAgger | Expert labeling during learner rollouts | Minimize loss under learner-induced distributions via no-regret reduction (Ross Eq. 3, Thm 4.1) | Requires interactive expert queries; safety/UX constraints | When you can query an expert online and need robustness to off-demo states |
| IRL / GAIL-style | Expert trajectories (state-action samples), plus environment interaction for RL | Occupancy measure matching via GAN loss; minimize \(D_{JS}(\rho_\pi,\rho_E)-\lambda H(\pi)\) (GAIL Eq. 15) | Can be interaction-heavy; adversarial training instability | When action labels are available but BC is brittle, and you can do RL-in-the-loop to match expert visitation patterns |

**Rule of thumb grounded in sources:** Ross et al. motivate DAgger specifically to address BC’s distribution shift; GAIL motivates occupancy-measure matching as an alternative to direct supervised cloning and reports large gains over BC on MuJoCo benchmarks (Humanoid-v1 Table 3).

---

## Prerequisite Connections

- **Policies and trajectories (RL basics).** Needed to parse \(\pi(a\mid s)\), rollouts, and horizon \(T\) in Ross et al. and GAIL.
- **Supervised learning losses (classification/regression).** Needed to understand BC as NLL minimization (RT-1 objective).
- **State distribution under a policy.** Needed to understand \(d^{\pi^*}\) vs \(d^\pi\) and why i.i.d. assumptions fail (Ross et al.).
- **GAN minimax training (basic idea).** Needed to understand GAIL’s discriminator/policy alternating updates (GAIL Eq. 14–18).

---

## Socratic Question Bank

1. **If BC has error rate \(\epsilon\) on expert states, why might the robot’s performance degrade faster than \(T\epsilon\) over a horizon \(T\)?**  
   *Good answer:* mentions distribution shift and compounding; references Ross Thm 2.1’s \(T^2\epsilon\) style behavior.

2. **What distribution are you training on in BC, and what distribution do you care about at test time?**  
   *Good answer:* training on \(d^{\pi^*}\), care about \(d^\pi\).

3. **In DAgger, why do we still label with the expert action even when the robot executed its own action?**  
   *Good answer:* execution is to reach learner states; labels must be expert to provide corrective supervision; aligns with `imitation` API note that saved demos record expert actions.

4. **What does \(\beta_i\) control in DAgger, and what happens as \(\beta_i\to 0\)?**  
   *Good answer:* probability of executing expert; as it decreases, rollouts become on-policy for learner; connects to Lemma 4.1 bound scaling with \(T\beta_i\).

5. **How is GAIL’s discriminator objective different from supervised action prediction?**  
   *Good answer:* discriminator classifies expert vs policy state-action pairs; objective is GAN loss (Eq. 14), not NLL of expert actions.

6. **What does it mean to “match occupancy measures,” and why might that help with covariate shift?**  
   *Good answer:* match \(\rho_\pi(s,a)\) to \(\rho_E(s,a)\); focuses on visitation frequencies under the learned policy, aligning train/test distributions.

7. **Given a fixed set of expert trajectories, which methods require additional environment interaction during training?**  
   *Good answer:* DAgger (rollouts + expert queries) and GAIL (policy rollouts for RL + discriminator training) require interaction; BC can be offline.

8. **RT-1/RT-2 discretize actions into bins/tokens—why might that be convenient for BC?**  
   *Good answer:* turns action prediction into categorical cross-entropy / token prediction; cites RT-1/RT-2 action discretization into 256 bins.

---

## Likely Student Questions

**Q: What exactly is the BC loss used in RT-1?**  
→ **A:** RT-1 states imitation learning via behavior cloning minimizes negative log-likelihood of demonstrated actions: \(\min_\theta \mathbb{E}_{(o,\ell,a)\sim D}[-\log \pi_\theta(a\mid o,\ell)]\) (https://arxiv.org/html/2212.06817v2).

**Q: What is the formal statement of “compounding errors” in behavior cloning?**  
→ **A:** Ross et al. (AISTATS’11) show that if the expected imitation loss under expert states is \(\epsilon\), then the total cost can satisfy \(J(\pi)\le J(\pi^*)+T^2\epsilon\) (Thm 2.1 in https://www.ri.cmu.edu/pub_files/2011/4/Ross-AISTATS11-NoRegret.pdf).

**Q: What are the steps of DAgger in the original paper?**  
→ **A:** Execute a mixture \(\pi_i=\beta_i\pi^*+(1-\beta_i)\hat\pi_i\), collect visited states labeled by the expert, aggregate datasets across iterations, retrain a stationary policy on the aggregated dataset, and return the best iterate (Alg. 3.1 in Ross et al. 2011 PDF).

**Q: In the `imitation` library, what does \(\beta\) do during interactive collection?**  
→ **A:** In `InteractiveTrajectoryCollector`, at each step it executes the expert action with probability \(\beta\) and otherwise substitutes the robot action; however, the saved demonstrations always record the expert actions (https://imitation.readthedocs.io/en/latest/_api/imitation.algorithms.dagger.html).

**Q: What default training setting does `DAggerTrainer` use for BC updates?**  
→ **A:** `DAggerTrainer.DEFAULT_N_EPOCHS = 4` is used by `extend_and_update()` when neither `n_epochs` nor `n_batches` is provided (imitation DAgger API docs).

**Q: What is GAIL’s actual minimax objective?**  
→ **A:** GAIL uses a GAN-style objective over state-action pairs: \(\max_D \mathbb E_{\pi}[\log D(s,a)] + \mathbb E_{\pi_E}[\log(1-D(s,a))]\) (Eq. 14), and the induced policy objective corresponds to \(\min_\pi D_{JS}(\rho_\pi,\rho_E)-\lambda H(\pi)\) (Eq. 15) (https://arxiv.org/pdf/1606.03476.pdf).

**Q: Do we have concrete evidence that large-scale BC can generalize?**  
→ **A:** RT-1 reports real-robot success rates of **97% seen** and **76% unseen** instructions, plus robustness numbers (**83% distractors**, **59% backgrounds**) (https://arxiv.org/html/2212.06817v2; also summarized at https://robotics-transformer1.github.io). RT-2 reports Language-Table sim success **90±10** vs **BC-Zero 72±3** (https://proceedings.mlr.press/v229/zitkovich23a/zitkovich23a.pdf).

---

## Available Resources

### Videos
- [Imitation Learning (CS285 Lecture 2)](https://youtube.com/watch?v=zDvcNTVkDxk) — **Surface when:** a student wants the canonical walkthrough of BC → distribution shift → DAgger, with the “sequential prediction” framing used in graduate RL.

### Articles & Tutorials
- [CS285 course materials (UC Berkeley RAIL)](https://rail.eecs.berkeley.edu/deeprlcourse/) — **Surface when:** the student asks for formal lecture slides/notes on BC distribution shift or wants more derivations around DAgger/IRL/GAIL.
- [Ross, Gordon, Bagnell — DAgger / no-regret reduction (arXiv)](https://arxiv.org/abs/1011.0686) — **Surface when:** the student asks for the original DAgger statement/intuition and the no-regret framing.
- [Lilian Weng — policy gradient article (contains RL notation background)](https://lilianweng.github.io/posts/2018-04-08-policy-gradient/) — **Surface when:** the student is missing RL notation (policies, \(Q\), advantage, entropy) needed to parse GAIL’s RL update discussion.

---

## Visual Aids

![General form of policy gradient theorem with equivalent formulations. (Schulman et al., 2016)](/api/wiki-images/imitation-learning/images/lilianweng-posts-2018-04-08-policy-gradient_001.png)  
**Show when:** the student gets stuck on how GAIL can “update the policy” from a learned cost; use this to refresh what a policy gradient is optimizing (connect to GAIL’s TRPO/policy-update step described in the paper).

---

## Key Sources

- [A Reduction of Imitation Learning and Structured Prediction to No-Regret Online Learning (Ross et al., 2011)](https://www.ri.cmu.edu/pub_files/2011/4/Ross-AISTATS11-NoRegret.pdf) — Formal definitions of \(d_t^\pi\), \(J(\pi)\), BC compounding error bound, DAgger algorithm, and no-regret guarantees.
- [DAgger abstract page (PMLR v15)](https://proceedings.mlr.press/v15/ross11a.html) — Concise statement of the distribution shift problem and DAgger’s dataset aggregation idea.
- [Generative Adversarial Imitation Learning (Ho & Ermon, 2016)](https://arxiv.org/pdf/1606.03476.pdf) — Exact GAIL minimax objective, occupancy measure definition, and equivalence to JS divergence + entropy regularization; includes benchmark comparisons vs BC.
- [`imitation` library DAgger API docs](https://imitation.readthedocs.io/en/latest/_api/imitation.algorithms.dagger.html) — Practical details tutors get asked: beta schedules, what gets executed vs what gets saved, default epochs, and trainer workflow.
- [RT-1 paper (arXiv HTML)](https://arxiv.org/html/2212.06817v2) — Concrete BC objective in a modern large-scale robot policy and real-robot success rates (seen/unseen/robustness).