## Key Facts & Specifications

### PPO (Proximal Policy Optimization)
- **Core stabilization mechanism (PPO-Clip):** PPO limits policy updates by **clipping a probability ratio** into a range **\([1-\epsilon, 1+\epsilon]\)** to “remove the incentive for the current policy to go too far from the old one.” (Hugging Face PPO blog, URL: https://huggingface.co/blog/deep-rl-ppo)
- **Original paper clip range example:** The PPO paper constrains the ratio to **0.8–1.2**, corresponding to **\(\epsilon = 0.2\)**. (Hugging Face PPO blog citing paper; also consistent with PPO paper: https://arxiv.org/pdf/1707.06347.pdf)
- **Spinning Up PPO default hyperparameters (PyTorch / TF1 API):**
  - `steps_per_epoch=4000`, `epochs=50`
  - `gamma=0.99`
  - `clip_ratio=0.2`
  - `pi_lr=0.0003`, `vf_lr=0.001`
  - `train_pi_iters=80`, `train_v_iters=80`
  - `lam=0.97`
  - `max_ep_len=1000`
  - `target_kl=0.01` (used for early stopping)  
  (OpenAI Spinning Up PPO docs: https://spinningup.openai.com/en/latest/algorithms/ppo.html)
- **Typical clip ratio range:** `clip_ratio` is “usually small, **0.1 to 0.3**.” (OpenAI Spinning Up PPO docs: https://spinningup.openai.com/en/latest/algorithms/ppo.html)
- **Early stopping criterion:** In Spinning Up PPO, gradient steps are **stopped early** if mean KL divergence exceeds a threshold (`target_kl`). (OpenAI Spinning Up PPO docs: https://spinningup.openai.com/en/latest/algorithms/ppo.html)

### Stable-Baselines3 PPO (SB3)
- **Default PPO constructor parameters (SB3):**
  - `learning_rate=0.0003`, `n_steps=2048`, `batch_size=64`, `n_epochs=10`
  - `gamma=0.99`, `gae_lambda=0.95`
  - `clip_range=0.2`, `clip_range_vf=None`
  - `ent_coef=0.0`, `vf_coef=0.5`
  - `max_grad_norm=0.5`
  - `use_sde=False`, `sde_sample_freq=-1`
  - `target_kl=None` (no KL limit by default)  
  (SB3 PPO docs: https://stable-baselines3.readthedocs.io/en/master/modules/ppo.html)
- **Rollout buffer size constraint:** `n_steps * n_envs` must be **greater than 1** “because of the advantage normalization.” (SB3 PPO docs and source: https://stable-baselines3.readthedocs.io/en/master/modules/ppo.html ; GitHub source excerpt: https://github.com/DLR-RM/stable-baselines3/blob/d8148deeaad3dbd1fb2b601e6f21d71f210366b1/stable_baselines3/ppo/ppo.py)
- **Value function clipping note:** `clip_range_vf` is “specific to the OpenAI implementation”; if `None`, no VF clipping; “IMPORTANT: this clipping depends on the reward scaling.” (SB3 PPO docs: https://stable-baselines3.readthedocs.io/en/master/modules/ppo.html)

### SAC (Soft Actor-Critic)
- **SAC objective includes entropy bonus:** SAC augments the RL objective with an entropy term:  
  \(J(\pi) = \sum_{t=0}^{T} \gamma^t \mathbb{E}[r(s_t,a_t) + \alpha H(\pi(\cdot|s_t))]\).  
  (Meta-SAC paper describing SAC: https://www.automl.org/wp-content/uploads/2020/07/AutoML_2020_paper_47.pdf)
- **Entropy temperature sensitivity (SAC-v1):** SAC-v1 is described as “particularly sensitive” to entropy temperature \(\alpha\); large \(\alpha\) can push policy toward near-uniform and degrade exploitation; small \(\alpha\) can become nearly deterministic and get stuck due to lack of exploration. (Meta-SAC, 2020: https://www.automl.org/wp-content/uploads/2020/07/AutoML_2020_paper_47.pdf)
- **SAC-v2 target entropy heuristic (as reported):** The paper reports a heuristic for minimal expected entropy / target entropy: **\(H = -\mathrm{dim}(a)\)** (negative action dimension), while noting it’s unclear if optimal for every task. (Meta-SAC, 2020: https://www.automl.org/wp-content/uploads/2020/07/AutoML_2020_paper_47.pdf)
- **Spinning Up SAC “Quick Facts”:**
  - SAC is **off-policy**
  - Spinning Up SAC implementation supports **continuous action spaces only**
  - Spinning Up SAC implementation **does not support parallelization**  
  (OpenAI Spinning Up SAC docs: https://spinningup.openai.com/en/latest/algorithms/sac.html)
- **Spinning Up SAC default hyperparameters (PyTorch / TF1 API):**
  - `steps_per_epoch=4000`, `epochs=100`
  - `replay_size=1000000`
  - `gamma=0.99`, `polyak=0.995`
  - `lr=0.001`, `alpha=0.2`
  - `batch_size=100`
  - `start_steps=10000`, `update_after=1000`, `update_every=50`
  - `num_test_episodes=10`, `max_ep_len=1000`  
  (OpenAI Spinning Up SAC docs: https://spinningup.openai.com/en/latest/algorithms/sac.html)
- **Exploration warm-start in Spinning Up SAC:** For `start_steps`, actions are sampled **uniform-random** over valid actions before switching to policy sampling. (OpenAI Spinning Up SAC docs: https://spinningup.openai.com/en/latest/algorithms/sac.html)

### Stable-Baselines3 SAC (SB3)
- **Default SAC constructor parameters (SB3):**
  - `learning_rate=0.0003`, `buffer_size=1000000`, `learning_starts=100`
  - `batch_size=256`, `tau=0.005`, `gamma=0.99`
  - `train_freq=1`, `gradient_steps=1`
  - `ent_coef='auto'`, `target_entropy='auto'`
  - `target_update_interval=1`  
  (SB3 SAC docs: https://stable-baselines3.readthedocs.io/en/master/modules/sac.html)
- **Auto target entropy in SB3:** If `target_entropy="auto"`, SB3 sets  
  `target_entropy = -np.prod(env.action_space.shape)` (negative product of action dimensions). (SB3 SAC source: https://stable-baselines3.readthedocs.io/en/v1.0/_modules/stable_baselines3/sac/sac.html)
- **Auto entropy coefficient optimization detail:** When `ent_coef='auto'`, SB3 optimizes the **log** entropy coefficient (`log_ent_coef`) rather than `ent_coef` directly; SB3 notes this is “consistent with the original implementation” and “more stable.” (SB3 SAC docs: https://stable-baselines3.readthedocs.io/en/master/modules/sac.html)
- **Entropy coefficient loss (SB3 source):**  
  `ent_coef_loss = -(log_ent_coef * (log_prob + target_entropy).detach()).mean()` when learning entropy coefficient. (SB3 SAC source: https://stable-baselines3.readthedocs.io/en/v1.0/_modules/stable_baselines3/sac/sac.html)

### Potential-Based Reward Shaping (PBRS)
- **Policy invariance condition:** Ng, Harada, and Russell (1999) show that adding shaping rewards expressible as a **difference of a potential function** preserves the optimal policy; other transformations may yield suboptimal policies unless extra assumptions hold. (Ng et al., 1999 landing page: https://www.andrewng.org/publications/policy-invariance-under-reward-transformations-theory-and-application-to-reward-shaping/ ; UT Austin bib page: https://www.cs.utexas.edu/~shivaram/readings/b2hd-NgHR1999.html)
- **Canonical PBRS shaping term (as summarized):**  
  \(F(s,a,s') = \gamma \Phi(s') - \Phi(s)\), and \(R'(s,a,s') = R(s,a,s') + F(s,a,s')\). (Emergent Mind PBRS summary: https://www.emergentmind.com/topics/potential-based-reward-shaping)

### Reward hacking / specification gaming
- **Definition:** Reward hacking/specification gaming occurs when an RL agent optimizes the formal objective without achieving the intended outcome. (Wikipedia: https://en.wikipedia.org/wiki/Reward_hacking)
- **Robotics-related example (reported):** A 2017 DeepMind paper is quoted as encountering reward-function design failures (e.g., “agent flips the brick because it gets a grasping reward calculated with the wrong reference point”). (Wikipedia: https://en.wikipedia.org/wiki/Reward_hacking)

### Domain Randomization (sim-to-real)
- **Randomizable visual parameters (examples list):** object position/shape/color, material texture, lighting, image noise, camera pose/FOV. (Lilian Weng DR post: https://lilianweng.github.io/posts/2019-05-05-domain-randomization/)
- **Randomizable dynamics parameters (examples list):** masses/dimensions, joint damping/kp/friction, PID gains, joint limits, action delay, observation noise. (Lilian Weng DR post: https://lilianweng.github.io/posts/2019-05-05-domain-randomization/)
- **Theoretical framing:** One paper models the simulator as a set of MDPs with tunable parameters (e.g., friction) and provides “sharp bounds” on the sim-to-real gap; it also highlights the importance of **memory/history-dependent policies** in domain randomization. (arXiv: https://arxiv.org/abs/2110.03239)

### Quadruped gait specification via Reward Machines (RMLL)
- **Foot contact boolean propositions:** \(P_{FL}, P_{FR}, P_{BL}, P_{BR}\) indicate whether each foot is in contact. (RMLL paper: https://arxiv.org/html/2107.10969v3)
- **Foot-in-air threshold used in training:** a foot is considered “in the air” if height is **> 0.03 m**. (RMLL paper: https://arxiv.org/html/2107.10969v3)
- **Command sampling ranges (simulation training):**
  - For gaits Trot/Bound/Pace/Three-One/Half-Bound: linear & angular velocity commands sampled from **[-1, 1] m/s**, gait frequency command from **[6, 12] time steps**.
  - For Walk: velocity commands **[-0.5, 0.5] m/s**, gait frequency **[5, 10] time steps**.  
  (RMLL paper: https://arxiv.org/html/2107.10969v3)
- **Reward term scales (Table excerpt):**
  - Joint torques \(\|\tau\|^2\): **-0.0002**
  - Joint accelerations: **-2.5e-7**
  - Feet air time: **1.0**
  - Action rate: **-0.01**  
  (RMLL paper: https://arxiv.org/html/2107.10969v3)
- **Energy/stability table includes specific values** (example): Trot energy per meter on Flat: **2165.04**; on Downhill: **2137.38**; etc. (RMLL Table 2: https://arxiv.org/html/2107.10969v3)

### Empirical comparison on MuJoCo tasks (DDPG/TD3/SAC/PPO)
- A comparative study reports experiments on **HalfCheetah-v4, Swimmer-v4, Ant-v4, Hopper-v3** and concludes **TD3 and SAC** “were found to be able to learn the controlling policy more effectively,” while noting hyperparameter sensitivity and that PPO’s performance is “still debatable.” (Liu, “An Evaluation of DDPG, TD3, SAC, and PPO”: https://www.atlantis-press.com/article/125998066.pdf)
- The same paper reports environment details for Ant: **observation dimension 27**, **action dimension 8**. (Liu paper Table 1: https://www.atlantis-press.com/article/125998066.pdf)
- Reported qualitative findings include:
  - In Ant-v4, PPO “can achieve the highest reward finally but seems more unstable.”
  - SAC and TD3 achieve rewards “over 2000,” with SAC taking more time (attributed to entropy bonus exploration).
  - DDPG performs worst (attributed to overestimation of target Q).  
  (Liu paper discussion: https://www.atlantis-press.com/article/125998066.pdf)

---

## Technical Details & Procedures

### PPO objective mechanics (clipping)
- **Probability ratio definition:** ratio is “probability of taking action \(a_t\) at state \(s_t\) in the current policy divided by the previous one.” (Hugging Face PPO blog: https://huggingface.co/blog/deep-rl-ppo)
- **Clipping range:** clip ratio to \([1-\epsilon, 1+\epsilon]\); paper example \(\epsilon=0.2\Rightarrow[0.8,1.2]\). (Hugging Face PPO blog: https://huggingface.co/blog/deep-rl-ppo)
- **Min of clipped/unclipped objective:** PPO takes the **minimum** of clipped and unclipped objective, producing a “pessimistic bound” on the unclipped objective. (Hugging Face PPO blog: https://huggingface.co/blog/deep-rl-ppo)

### OpenAI Spinning Up: PPO implementation details (buffer + GAE)
- **GAE-Lambda deltas computation (code):**  
  `deltas = rews[:-1] + gamma * vals[1:] - vals[:-1]`  
  `adv = discount_cumsum(deltas, gamma * lam)`  
  `ret = discount_cumsum(rews, gamma)[:-1]`  
  (Spinning Up PPO PyTorch source: https://spinningup.openai.com/en/latest/_modules/spinup/algos/pytorch/ppo/ppo.html)
- **Trajectory cutoff bootstrapping rule:** `last_val` should be **0** if terminal; otherwise **V(s_T)** to bootstrap beyond episode horizon/epoch cutoff. (Spinning Up PPO PyTorch source: https://spinningup.openai.com/en/latest/_modules/spinup/algos/pytorch/ppo/ppo.html)
- **Advantage normalization:** buffer `get()` normalizes advantages to mean 0, std 1. (Spinning Up PPO PyTorch source: https://spinningup.openai.com/en/latest/_modules/spinup/algos/pytorch/ppo/ppo.html)

### OpenAI Spinning Up: exact PPO call signature (PyTorch)
- `spinup.ppo_pytorch(env_fn, actor_critic=..., seed=0, steps_per_epoch=4000, epochs=50, gamma=0.99, clip_ratio=0.2, pi_lr=0.0003, vf_lr=0.001, train_pi_iters=80, train_v_iters=80, lam=0.97, max_ep_len=1000, target_kl=0.01, save_freq=10, ...)`  
  (OpenAI Spinning Up PPO docs: https://spinningup.openai.com/en/latest/algorithms/ppo.html)

### Stable-Baselines3: PPO minimal training snippet (parallel envs)
```python
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.vec_env import SubprocVecEnv
if __name__=="__main__":
    env = make_vec_env("CartPole-v1", n_envs=8, vec_env_cls=SubprocVecEnv)
    model = PPO("MlpPolicy", env, device="cpu")
    model.learn(total_timesteps=25_000)
```
(SB3 PPO docs: https://stable-baselines3.readthedocs.io/en/master/modules/ppo.html)

### OpenAI Spinning Up: exact SAC call signature (PyTorch)
- `spinup.sac_pytorch(env_fn, seed=0, steps_per_epoch=4000, epochs=100, replay_size=1000000, gamma=0.99, polyak=0.995, lr=0.001, alpha=0.2, batch_size=100, start_steps=10000, update_after=1000, update_every=50, num_test_episodes=10, max_ep_len=1000, save_freq=1, ...)`  
  (OpenAI Spinning Up SAC docs: https://spinningup.openai.com/en/latest/algorithms/sac.html)

### Stable-Baselines3: SAC auto-entropy configuration
- Set `ent_coef='auto'` to learn entropy coefficient; `target_entropy='auto'` sets target entropy to `-np.prod(action_space.shape)`. (SB3 SAC docs + source: https://stable-baselines3.readthedocs.io/en/master/modules/sac.html ; https://stable-baselines3.readthedocs.io/en/v1.0/_modules/stable_baselines3/sac/sac.html)
- SB3 supports `ent_coef='auto_0.1'` to initialize learned entropy coefficient at **0.1** (must be > 0). (SB3 SAC docs: https://stable-baselines3.readthedocs.io/en/master/modules/sac.html)

### Reward Machines locomotion: procedure-relevant details
- **RM state as history abstraction:** policy gets current RM state (abstract history of foot contacts) rather than needing long observation history; used to avoid non-Markovian reward when specifying gait sequences. (RMLL paper: https://arxiv.org/html/2107.10969v3)
- **Gait frequency command:** adding gait frequency command alone makes reward non-Markovian because agent must remember steps since last RM state change; RM state + counter \(\phi\) addresses this. (RMLL paper: https://arxiv.org/html/2107.10969v3)

---

## Comparisons & Trade-offs

### PPO vs TRPO (update constraint mechanism)
- **TRPO:** uses **KL divergence constraints outside the objective**; described as “complicated to implement and takes more computation time.” (Hugging Face PPO blog: https://huggingface.co/blog/deep-rl-ppo)
- **PPO:** clips probability ratio **inside** the objective (PPO-Clip). (Hugging Face PPO blog; OpenAI Spinning Up PPO docs: https://huggingface.co/blog/deep-rl-ppo ; https://spinningup.openai.com/en/latest/algorithms/ppo.html)

### PPO-Penalty vs PPO-Clip (Spinning Up)
- **PPO-Penalty:** penalizes KL divergence in the objective and **automatically adjusts** penalty coefficient. (OpenAI Spinning Up PPO docs: https://spinningup.openai.com/en/latest/algorithms/ppo.html)
- **PPO-Clip:** no KL term; relies on clipping to remove incentives for large updates. (OpenAI Spinning Up PPO docs: https://spinningup.openai.com/en/latest/algorithms/ppo.html)

### On-policy vs off-policy (conceptual trade-off)
- **On-policy:** learns from the policy currently being executed, including exploration steps. (GeeksforGeeks, 2025: https://www.geeksforgeeks.org/machine-learning/on-policy-vs-off-policy-methods-reinforcement-learning/)
- **Off-policy:** can learn from data generated by a different policy; includes discussion of importance sampling to correct distribution mismatch. (GeeksforGeeks, 2025: https://www.geeksforgeeks.org/machine-learning/on-policy-vs-off-policy-methods-reinforcement-learning/)

### SAC vs TD3 (Spinning Up perspective)
- SAC incorporates **clipped double-Q trick** and benefits from stochasticity similarly to TD3’s target policy smoothing, but:
  - SAC uses **current policy** for next-state actions in targets (not a target policy).
  - SAC has **no explicit target policy smoothing**; stochastic policy noise provides similar effect.  
  (OpenAI Spinning Up SAC docs: https://spinningup.openai.com/en/latest/algorithms/sac.html)

### Empirical comparison (MuJoCo study; qualitative)
- In the Liu MuJoCo comparison, **TD3 or SAC** is concluded “most likely to perform best” across tried environments; PPO performance “still unsure,” DDPG often worst. (Liu paper: https://www.atlantis-press.com/article/125998066.pdf)
- The same paper suggests PPO instability may relate to **batch size** and variable episode lengths (up to **1000** steps or sometimes **<10**), while off-policy methods can sample from replay buffer with larger batch sizes. (Liu paper: https://www.atlantis-press.com/article/125998066.pdf)

**Discrepancy note:** The Liu paper states PPO achieves the highest final reward on Ant-v4 but is unstable, while also concluding TD3/SAC are most likely best overall; this is not a strict contradiction but indicates task-dependent outcomes and sensitivity to hyperparameters. (https://www.atlantis-press.com/article/125998066.pdf)

---

## Architecture & Design Rationale

### Why PPO clipping improves stability
- PPO’s design goal is to “avoid having too large policy updates,” because empirically smaller updates are “more likely to converge,” and too big a step can cause a “bad policy” with long/no recovery. (Hugging Face PPO blog: https://huggingface.co/blog/deep-rl-ppo)
- Clipping removes incentive for ratio to move outside \([1-\epsilon,1+\epsilon]\), restricting how far the new policy can vary from the old. (Hugging Face PPO blog: https://huggingface.co/blog/deep-rl-ppo)

### Why Spinning Up PPO uses early stopping on KL
- Spinning Up notes clipping “goes a long way” but it’s still possible for the new policy to be too far from old; early stopping halts gradient steps when mean KL exceeds `target_kl`. (OpenAI Spinning Up PPO docs: https://spinningup.openai.com/en/latest/algorithms/ppo.html)

### Why SAC uses entropy regularization
- Entropy regularization is a “central feature” of SAC; increasing entropy increases exploration and can prevent premature convergence to a bad local optimum. (OpenAI Spinning Up SAC docs: https://spinningup.openai.com/en/latest/algorithms/sac.html)
- The entropy temperature \(\alpha\) explicitly controls the exploration/exploitation trade-off; the “right coefficient” may vary by environment and may require tuning. (OpenAI Spinning Up SAC docs: https://spinningup.openai.com/en/latest/algorithms/sac.html)

### Why auto-entropy introduces “target entropy” (and its caveat)
- Meta-SAC describes SAC-v2’s constrained optimization approach as introducing a new hyperparameter “target entropy,” with a heuristic \(H=-\mathrm{dim}(a)\), but notes it’s unknown if optimal for every task. (Meta-SAC, 2020: https://www.automl.org/wp-content/uploads/2020/07/AutoML_2020_paper_47.pdf)
- SB3 implements `target_entropy='auto'` as negative action dimension product, aligning with the heuristic form. (SB3 SAC source: https://stable-baselines3.readthedocs.io/en/v1.0/_modules/stable_baselines3/sac/sac.html)

### Why potential-based shaping preserves optimal policy
- Ng et al. (1999) show that adding a shaping reward equal to a difference of a potential function (over transitions) preserves the optimal policy; other shaping can introduce “bugs” and may change optimality. (Ng et al., 1999 pages: https://www.andrewng.org/publications/policy-invariance-under-reward-transformations-theory-and-application-to-reward-shaping/ ; https://www.cs.utexas.edu/~shivaram/readings/b2hd-NgHR1999.html)

### Why domain randomization may need memory
- A theoretical framework for domain randomization highlights the importance of **memory/history-dependent policies** for sim-to-real success. (arXiv: https://arxiv.org/abs/2110.03239)
- Practical DR reports (OpenAI dexterity as summarized by Weng) observed an LSTM policy transferring better than a feedforward policy in a dexterous manipulation setting. (Lilian Weng DR post: https://lilianweng.github.io/posts/2019-05-05-domain-randomization/)

---

## Common Questions & Answers

### Q1: What exact range does PPO clip the policy ratio to?
- PPO clips the probability ratio to **\([1-\epsilon, 1+\epsilon]\)**; the PPO paper example uses **\(\epsilon=0.2\)**, i.e., **[0.8, 1.2]**. (Hugging Face PPO blog: https://huggingface.co/blog/deep-rl-ppo ; PPO paper: https://arxiv.org/pdf/1707.06347.pdf)

### Q2: What are the default PPO hyperparameters in OpenAI Spinning Up?
- Spinning Up `ppo_pytorch` defaults include: `steps_per_epoch=4000`, `epochs=50`, `gamma=0.99`, `clip_ratio=0.2`, `pi_lr=0.0003`, `vf_lr=0.001`, `lam=0.97`, `train_pi_iters=80`, `train_v_iters=80`, `max_ep_len=1000`, `target_kl=0.01`. (OpenAI Spinning Up PPO docs: https://spinningup.openai.com/en/latest/algorithms/ppo.html)

### Q3: Why does Spinning Up PPO stop early based on KL divergence?
- Spinning Up states clipping may not fully prevent large updates; it uses **early stopping** when mean KL exceeds `target_kl`. (OpenAI Spinning Up PPO docs: https://spinningup.openai.com/en/latest/algorithms/ppo.html)

### Q4: What are SB3 PPO defaults (n_steps, batch_size, clip_range, etc.)?
- SB3 PPO defaults include `n_steps=2048`, `batch_size=64`, `n_epochs=10`, `gamma=0.99`, `gae_lambda=0.95`, `clip_range=0.2`, `vf_coef=0.5`, `ent_coef=0.0`, `max_grad_norm=0.5`. (SB3 PPO docs: https://stable-baselines3.readthedocs.io/en/master/modules/ppo.html)

### Q5: What does SAC’s entropy temperature \(\alpha\) do?
- \(\alpha\) balances expected task reward and expected policy entropy; higher \(\alpha\) encourages more randomness (exploration), lower \(\alpha\) encourages exploitation. SAC-v1 is reported to be sensitive to \(\alpha\). (Meta-SAC, 2020: https://www.automl.org/wp-content/uploads/2020/07/AutoML_2020_paper_47.pdf ; Spinning Up SAC docs: https://spinningup.openai.com/en/latest/algorithms/sac.html)

### Q6: What is SB3’s “auto” target entropy for SAC?
- If `target_entropy="auto"`, SB3 sets it to **\(-\prod \text{action_space.shape}\)** (negative action dimension product). (SB3 SAC source: https://stable-baselines3.readthedocs.io/en/v1.0/_modules/stable_baselines3/sac/sac.html)

### Q7: What is potential-based reward shaping, exactly?
- PBRS adds a shaping term derived from a potential function: \(F(s,a,s')=\gamma\Phi(s')-\Phi(s)\), and uses \(R'=R+F\). Ng et al. (1999) show this preserves the optimal policy (policy invariance). (Emergent Mind PBRS summary: https://www.emergentmind.com/topics/potential-based-reward-shaping ; Ng et al., 1999 pages: https://www.andrewng.org/publications/policy-invariance-under-reward-transformations-theory-and-application-to-reward-shaping/)

### Q8: What parameters are commonly randomized in domain randomization for sim-to-real?
- Visual: object pose/shape/color, textures, lighting, image noise, camera pose/FOV.  
- Dynamics: masses/dimensions, joint damping/kp/friction, PID gains, joint limits, action delay, observation noise.  
  (Lilian Weng DR post: https://lilianweng.github.io/posts/2019-05-05-domain-randomization/)

### Q9: Does SAC parallelize well in Spinning Up?
- Spinning Up explicitly states its SAC implementation **does not support parallelization**. (OpenAI Spinning Up SAC docs: https://spinningup.openai.com/en/latest/algorithms/sac.html)

### Q10: What’s a concrete example of reward hacking in robotics?
- Wikipedia reports a Mindstorms robot path-following setup where the robot learned to **zig-zag backwards** to maximize reward; the reward had to be patched with an action-based reward for moving forward. (Wikipedia: https://en.wikipedia.org/wiki/Reward_hacking)

---