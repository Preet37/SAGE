# Card: PPO policy training w/ KL control (lm-human-preferences)
**Source:** https://github.com/openai/lm-human-preferences/blob/cbfd210bb8b08f6bc5c26878c10984b90f516c66/lm_human_preferences/train_policy.py  
**Role:** code | **Need:** API_REFERENCE  
**Anchor:** Reference implementation of policy optimization from human preferences: PPO loop + reward shaping with KL penalty (fixed/adaptive), batching across MPI ranks, and default hyperparameters.

## Key Content
- **Training objective (reward shaping) (Eq. 1):**  
  - Per-token KL term: `kl = logprobs - ref_logprobs` (same shape as tokens).  
  - Non-score reward: `r_kl = - kl_coef * kl`.  
  - Final per-token reward: `rewards = r_kl; rewards[:, -1] += scores` (scalar preference score added only to last token).  
  - Returns `(rewards, non_score_reward, kl_coef)` from `compute_rewards(...)`.
- **KL controllers:**
  - **FixedKLController:** `kl_coef` constant (`update` is no-op).
  - **AdaptiveKLController update (Eq. 2):**  
    - `proportional_error = clip(current/target - 1, -0.2, 0.2)`  
    - `mult = 1 + proportional_error * n_steps / horizon`  
    - `kl_coef *= mult`  
    - Defaults: `target=None` (must be set if used), `horizon=10000` episodes.
- **Default PPO hyperparameters (PpoHParams):**  
  `total_episodes=2_000_000`, `batch_size=64`, `nminibatches=1`, `noptepochs=4`, `lr=5e-6`, `vf_coef=0.1`, `cliprange=0.2`, `cliprange_value=0.2`, `gamma=1`, `lam=0.95`, `whiten_rewards=True`.
- **Batching across MPI ranks:**  
  - `per_rank_rollout_batch_size = batch_size / comm_size`  
  - `per_rank_minibatch_size = per_rank_rollout_batch_size / nminibatches`  
  - Whitening constraint: minibatch size ≥ 8 (also enforced per-rank).
- **Training loop procedure:** initialize vars → `sync_models()` (broadcast/sync score model + ref_policy + policy params) → repeat until `global_step < ceil(total_episodes/batch_size)`: `ppo_trainer.step()` → `global_step += 1` → periodic checkpoint save (`save_interval`).

## When to surface
Use when students ask how RLHF PPO rewards are computed (score + KL penalty), how adaptive KL is updated, or what concrete default PPO/KL hyperparameters and batching rules this reference implementation uses.