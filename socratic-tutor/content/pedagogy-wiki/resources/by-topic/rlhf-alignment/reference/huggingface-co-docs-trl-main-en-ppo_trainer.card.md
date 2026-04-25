# Card: TRL PPOTrainer (API + key metrics)
**Source:** https://huggingface.co/docs/trl/main/en/ppo_trainer  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Authoritative parameter names/semantics for `trl.experimental.ppo.PPOTrainer` + `PPOConfig` (KL control, clipping, batching, reward shaping, logging)

## Key Content
- **Core reward decomposition (Eq. 1):**  
  - `objective/non_score_reward = beta * kl.sum(1)` where `beta = kl_coef` and `kl` is **per-token KL** between policy and reference.  
  - `objective/rlhf_reward = score - non_score_reward` where `score = objective/scores` (reward model output).
- **Key logged PPO diagnostics (definitions):**
  - `objective/kl`: mean KL(current policy || reference policy).  
  - `policy/approxkl_avg`: approx KL between consecutive PPO policies (not same as `objective/kl`).  
  - `val/ratio`: mean prob ratio (new/old); should hover ~1.0; clipped by `--cliprange 0.2`.  
  - `policy/clipfrac_avg`, `val/clipfrac_avg`: fraction of updates clipped (policy/value).  
  - `objective/entropy`, `policy/entropy_avg`: action randomness.
- **Training workflow (scripted):** run `examples/scripts/ppo/ppo.py` with SFT model path + reward model path; recommends **“EOS trick”**: `missing_eos_penalty` subtracts a positive scalar from `score` if completion lacks EOS to encourage coherent/shorter completions.
- **Empirical benchmark (TL;DR, 1B model):** GPT-4o mini judge win-rate: **SFT 33.00%** vs **PPO 64.70%** preferred.
- **PPOTrainer constructor (API):** `PPOTrainer(args: PPOConfig, processing_class, model, ref_model=None, reward_model, train_dataset, value_model, ...)`. If `ref_model=None`, **copies policy model** for KL reference.
- **Key PPOConfig defaults (selected):** `learning_rate=3e-6`, `num_ppo_epochs=4`, `num_mini_batches=1`, `local_rollout_forward_batch_size=64`, `response_length=53`, `temperature=0.7`, `kl_coef=0.05`, `kl_estimator='k1'` (or `'k3'` lower variance), `cliprange=0.2`, `cliprange_value=0.2`, `vf_coef=0.1`, `gamma=1.0`, `lam=0.95`, `num_sample_generations=10`, `gradient_checkpointing=True`.

## When to surface
Use when students ask how TRL’s PPO implements KL penalties/clipping, what metrics mean during RLHF PPO runs, or which exact `PPOConfig`/`PPOTrainer` parameters control batching, rollouts, EOS penalties, and KL estimation.