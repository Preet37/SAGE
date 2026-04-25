# Card: DAgger API (imitation.algorithms.dagger)
**Source:** https://imitation.readthedocs.io/en/latest/_api/imitation.algorithms.dagger.html  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Constructor/API surface for `DAggerTrainer` (+ schedules, collectors, defaults)

## Key Content
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

## When to surface
Use when students ask how DAgger is implemented in the `imitation` library: round structure, beta-mixing behavior, how interactive collection works, default BC training epochs, checkpoint/demo directory layout, or how to resume training.