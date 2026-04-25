# Card: TRL PPOTrainer (API + key PPO knobs)
**Source:** https://huggingface.co/docs/trl/en/ppo_trainer  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Authoritative parameter names/semantics for `trl.experimental.ppo.PPOTrainer` + `PPOConfig` defaults; logged metrics meanings; rollout/generation controls.

## Key Content
- **Core objective components (logged):**
  - **Non-score reward (Eq. 1):** `objective/non_score_reward = beta * kl.sum(1)`  
    - `beta` = KL penalty coefficient (`PPOConfig.kl_coef`)  
    - `kl` = per-token KL divergence between policy and reference.
  - **RLHF reward (Eq. 2):** `objective/rlhf_reward = score - non_score_reward`  
    - `score` = reward model output (`objective/scores`).
- **Debugging heuristics (procedural):**
  - `objective/rlhf_reward` should increase if PPO training is working.
  - `val/ratio` should hover near **1.0**; it is clipped by `--cliprange 0.2`. Ratios like **2.0**, **1000.0**, or **0.1** indicate overly drastic updates.
- **EOS trick (design rationale):** `missing_eos_penalty` subtracts a **positive** scalar penalty from the score when no EOS is generated; encourages coherent/shorter completions (shorter than `max_new_tokens`).
- **Empirical result (TL;DR benchmark):** Judge eval (GPT-4o mini) win rate: **SFT 33.00%** vs **PPO 64.70%** preferred.
- **Key classes / signatures:**
  - `PPOTrainer(args: PPOConfig, processing_class, model, ref_model=None, reward_model, train_dataset, value_model, ...)`
  - If `ref_model=None`, a **copy of the policy model** is created for KL computation.
- **`PPOConfig` PPO-specific defaults (selected):**
  - `learning_rate=3e-6`, `gradient_checkpointing=True`, `logging_steps=10`
  - PPO: `num_ppo_epochs=4`, `num_mini_batches=1`, `kl_coef=0.05`, `kl_estimator='k1'|'k3' (default 'k1')`, `cliprange=0.2`, `vf_coef=0.1`, `cliprange_value=0.2`, `gamma=1.0`, `lam=0.95`, `whiten_rewards=False`
  - Generation/rollout: `response_length=53`, `temperature=0.7`, `num_sample_generations=10`, `local_rollout_forward_batch_size=64`, `stop_token` mutually exclusive with `stop_token_id`
  - ZeRO-3: `ds3_gather_for_generation=True` (faster gen; disable to fit larger-than-single-GPU models).

## When to surface
Use when students ask how TRL’s PPOTrainer is configured (exact hyperparameter names/defaults), how KL penalty and RLHF reward are computed/logged, or how generation/EOS penalties and clipping diagnostics work.