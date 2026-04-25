# Source: https://imitation.readthedocs.io/en/latest/_api/imitation.algorithms.dagger.html
# Title: imitation.algorithms.dagger
# Fetched via: trafilatura
# Date: 2026-04-09

imitation.algorithms.dagger[#](#module-imitation.algorithms.dagger)
DAgger ([https://arxiv.org/pdf/1011.0686.pdf](https://arxiv.org/pdf/1011.0686.pdf)).
Interactively trains policy by collecting some demonstrations, doing BC, collecting more demonstrations, doing BC again, etc. Initially the demonstrations just come from the expert’s policy; over time, they shift to be drawn more and more from the imitator’s policy.
Functions
|
Reconstruct trainer from the latest snapshot in some working directory. |
Classes
Computes beta (% of time demonstration action used) from training round. |
|
|
DAgger training class with low-level API suitable for interactive human feedback. |
|
Exponentially decaying schedule for beta. |
|
DAgger VecEnvWrapper for querying and saving expert actions. |
|
Linearly-decreasing schedule for beta. |
|
Simpler subclass of DAggerTrainer for training with synthetic feedback. |
Exceptions
Signals demos need to be collected for current round before continuing. |
-
class imitation.algorithms.dagger.BetaSchedule
[[source]](../_modules/imitation/algorithms/dagger.html#BetaSchedule)[#](#imitation.algorithms.dagger.BetaSchedule) Bases:
ABC
Computes beta (% of time demonstration action used) from training round.
-
class imitation.algorithms.dagger.DAggerTrainer(*, venv, scratch_dir, rng, beta_schedule=None, bc_trainer, custom_logger=None)
[[source]](../_modules/imitation/algorithms/dagger.html#DAggerTrainer)[#](#imitation.algorithms.dagger.DAggerTrainer) Bases:
BaseImitationAlgorithm
DAgger training class with low-level API suitable for interactive human feedback.
In essence, this is just BC with some helpers for incrementally resuming training and interpolating between demonstrator/learnt policies. Interaction proceeds in “rounds” in which the demonstrator first provides a fresh set of demonstrations, and then an underlying BC is invoked to fine-tune the policy on the entire set of demonstrations collected in all rounds so far. Demonstrations and policy/trainer checkpoints are stored in a directory with the following structure:
scratch-dir-name/ checkpoint-001.pt checkpoint-002.pt … checkpoint-XYZ.pt checkpoint-latest.pt demos/ round-000/ demos_round_000_000.npz demos_round_000_001.npz … round-001/ demos_round_001_000.npz … … round-XYZ/ …
-
DEFAULT_N_EPOCHS: int = 4
[#](#imitation.algorithms.dagger.DAggerTrainer.DEFAULT_N_EPOCHS) The default number of BC training epochs in extend_and_update.
-
__init__(*, venv, scratch_dir, rng, beta_schedule=None, bc_trainer, custom_logger=None)
[[source]](../_modules/imitation/algorithms/dagger.html#DAggerTrainer.__init__)[#](#imitation.algorithms.dagger.DAggerTrainer.__init__) Builds DAggerTrainer.
- Parameters
venv (
VecEnv
) – Vectorized training environment.scratch_dir (
Union
[str
,bytes
,PathLike
]) – Directory to use to store intermediate training information (e.g. for resuming training).rng (
Generator
) – random state for random number generation.beta_schedule (
Optional
[Callable
[[int
],float
]]) – Provides a value of beta (the probability of taking expert action in any given state) at each round of training. If None, then linear_beta_schedule will be used instead.bc_trainer (
) – A BC instance used to train the underlying policy.BC
custom_logger (
Optional
[]) – Where to log to; if None (default), creates a new logger.HierarchicalLogger
-
property batch_size: int
[#](#imitation.algorithms.dagger.DAggerTrainer.batch_size) - Return type
int
-
create_trajectory_collector()
[[source]](../_modules/imitation/algorithms/dagger.html#DAggerTrainer.create_trajectory_collector)[#](#imitation.algorithms.dagger.DAggerTrainer.create_trajectory_collector) Create trajectory collector to extend current round’s demonstration set.
- Return type
- Returns
A collector configured with the appropriate beta, imitator policy, etc. for the current round. Refer to the documentation for InteractiveTrajectoryCollector to see how to use this.
-
extend_and_update(bc_train_kwargs=None)
[[source]](../_modules/imitation/algorithms/dagger.html#DAggerTrainer.extend_and_update)[#](#imitation.algorithms.dagger.DAggerTrainer.extend_and_update) Extend internal batch of data and train BC.
Specifically, this method will load new transitions (if necessary), train the model for a while, and advance the round counter. If there are no fresh demonstrations in the demonstration directory for the current round, then this will raise a NeedsDemosException instead of training or advancing the round counter. In that case, the user should call .create_trajectory_collector() and use the returned InteractiveTrajectoryCollector to produce a new set of demonstrations for the current interaction round.
- Parameters
bc_train_kwargs (
Optional
[Mapping
[str
,Any
]]) – Keyword arguments for calling BC.train(). If the log_rollouts_venv key is not provided, then it is set to self.venv by default. If neither of the n_epochs and n_batches keys are provided, then n_epochs is set to self.DEFAULT_N_EPOCHS.- Return type
int
- Returns
New round number after advancing the round counter.
-
property logger:
[HierarchicalLogger](imitation.util.logger.html#imitation.util.logger.HierarchicalLogger)[#](#imitation.algorithms.dagger.DAggerTrainer.logger) Returns logger for this object.
- Return type
-
property policy: BasePolicy
[#](#imitation.algorithms.dagger.DAggerTrainer.policy) - Return type
BasePolicy
-
save_trainer()
[[source]](../_modules/imitation/algorithms/dagger.html#DAggerTrainer.save_trainer)[#](#imitation.algorithms.dagger.DAggerTrainer.save_trainer) Create a snapshot of trainer in the scratch/working directory.
The created snapshot can be reloaded with reconstruct_trainer(). In addition to saving one copy of the policy in the trainer snapshot, this method saves a second copy of the policy in its own file. Having a second copy of the policy is convenient because it can be loaded on its own and passed to evaluation routines for other algorithms.
- Returns
a path to one of the created DAggerTrainer checkpoints. policy_path: a path to one of the created DAggerTrainer policies.
- Return type
checkpoint_path
-
DEFAULT_N_EPOCHS: int = 4
-
class imitation.algorithms.dagger.ExponentialBetaSchedule(decay_probability)
[[source]](../_modules/imitation/algorithms/dagger.html#ExponentialBetaSchedule)[#](#imitation.algorithms.dagger.ExponentialBetaSchedule) Bases:
BetaSchedule
Exponentially decaying schedule for beta.
-
class imitation.algorithms.dagger.InteractiveTrajectoryCollector(venv, get_robot_acts, beta, save_dir, rng)
[[source]](../_modules/imitation/algorithms/dagger.html#InteractiveTrajectoryCollector)[#](#imitation.algorithms.dagger.InteractiveTrajectoryCollector) Bases:
VecEnvWrapper
DAgger VecEnvWrapper for querying and saving expert actions.
Every call to .step(actions) accepts and saves expert actions to self.save_dir, but only forwards expert actions to the wrapped VecEnv with probability self.beta. With probability 1 - self.beta, a “robot” action (i.e an action from the imitation policy) is forwarded instead.
Demonstrations are saved as TrajectoryWithRew to self.save_dir at the end of every episode.
-
__init__(venv, get_robot_acts, beta, save_dir, rng)
[[source]](../_modules/imitation/algorithms/dagger.html#InteractiveTrajectoryCollector.__init__)[#](#imitation.algorithms.dagger.InteractiveTrajectoryCollector.__init__) Builds InteractiveTrajectoryCollector.
- Parameters
venv (
VecEnv
) – vectorized environment to sample trajectories from.get_robot_acts (
Callable
[[ndarray
],ndarray
]) – get robot actions that can be substituted for human actions. Takes a vector of observations as input & returns a vector of actions.beta (
float
) – fraction of the time to use action given to .step() instead of robot action. The choice of robot or human action is independently randomized for each individual Env at every timestep.save_dir (
Union
[str
,bytes
,PathLike
]) – directory to save collected trajectories in.rng (
Generator
) – random state for random number generation.
-
reset()
[[source]](../_modules/imitation/algorithms/dagger.html#InteractiveTrajectoryCollector.reset)[#](#imitation.algorithms.dagger.InteractiveTrajectoryCollector.reset) Resets the environment.
- Returns
first observation of a new trajectory.
- Return type
obs
-
seed(seed=None)
[[source]](../_modules/imitation/algorithms/dagger.html#InteractiveTrajectoryCollector.seed)[#](#imitation.algorithms.dagger.InteractiveTrajectoryCollector.seed) Set the seed for the DAgger random number generator and wrapped VecEnv.
The DAgger RNG is used along with self.beta to determine whether the expert or robot action is forwarded to the wrapped VecEnv.
- Parameters
seed (
Optional
[int
]) – The random seed. May be None for completely random seeding.- Return type
List
[Optional
[int
]]- Returns
A list containing the seeds for each individual env. Note that all list elements may be None, if the env does not return anything when seeded.
-
step_async(actions)
[[source]](../_modules/imitation/algorithms/dagger.html#InteractiveTrajectoryCollector.step_async)[#](#imitation.algorithms.dagger.InteractiveTrajectoryCollector.step_async) Steps with a 1 - beta chance of using self.get_robot_acts instead.
DAgger needs to be able to inject imitation policy actions randomly at some subset of time steps. This method has a self.beta chance of keeping the actions passed in as an argument, and a 1 - self.beta chance of forwarding actions generated by self.get_robot_acts instead. “robot” (i.e. imitation policy) action if necessary.
At the end of every episode, a TrajectoryWithRew is saved to self.save_dir, where every saved action is the expert action, regardless of whether the robot action was used during that timestep.
- Parameters
actions (
ndarray
) – the _intended_ demonstrator/expert actions for the current state. This will be executed with probability self.beta. Otherwise, a “robot” (typically a BC policy) action will be sampled and executed instead via self.get_robot_act.- Return type
None
-
step_wait()
[[source]](../_modules/imitation/algorithms/dagger.html#InteractiveTrajectoryCollector.step_wait)[#](#imitation.algorithms.dagger.InteractiveTrajectoryCollector.step_wait) Returns observation, reward, etc after previous step_async() call.
Stores the transition, and saves trajectory as demo once complete.
- Return type
Tuple
[Union
[ndarray
,Dict
[str
,ndarray
],Tuple
[ndarray
,...
]],ndarray
,ndarray
,List
[Dict
]]- Returns
Observation, reward, dones (is terminal?) and info dict.
-
traj_accum: Optional[
[TrajectoryAccumulator](imitation.data.rollout.html#imitation.data.rollout.TrajectoryAccumulator)][#](#imitation.algorithms.dagger.InteractiveTrajectoryCollector.traj_accum)
-
__init__(venv, get_robot_acts, beta, save_dir, rng)
-
class imitation.algorithms.dagger.LinearBetaSchedule(rampdown_rounds)
[[source]](../_modules/imitation/algorithms/dagger.html#LinearBetaSchedule)[#](#imitation.algorithms.dagger.LinearBetaSchedule) Bases:
BetaSchedule
Linearly-decreasing schedule for beta.
-
exception imitation.algorithms.dagger.NeedsDemosException
[[source]](../_modules/imitation/algorithms/dagger.html#NeedsDemosException)[#](#imitation.algorithms.dagger.NeedsDemosException) Bases:
Exception
Signals demos need to be collected for current round before continuing.
-
class imitation.algorithms.dagger.SimpleDAggerTrainer(*, venv, scratch_dir, expert_policy, rng, expert_trajs=None, **dagger_trainer_kwargs)
[[source]](../_modules/imitation/algorithms/dagger.html#SimpleDAggerTrainer)[#](#imitation.algorithms.dagger.SimpleDAggerTrainer) Bases:
DAggerTrainer
Simpler subclass of DAggerTrainer for training with synthetic feedback.
-
__init__(*, venv, scratch_dir, expert_policy, rng, expert_trajs=None, **dagger_trainer_kwargs)
[[source]](../_modules/imitation/algorithms/dagger.html#SimpleDAggerTrainer.__init__)[#](#imitation.algorithms.dagger.SimpleDAggerTrainer.__init__) Builds SimpleDAggerTrainer.
- Parameters
venv (
VecEnv
) – Vectorized training environment. Note that when the robot action is randomly injected (in accordance with beta_schedule argument), every individual environment will get a robot action simultaneously for that timestep.scratch_dir (
Union
[str
,bytes
,PathLike
]) – Directory to use to store intermediate training information (e.g. for resuming training).expert_policy (
BasePolicy
) – The expert policy used to generate synthetic demonstrations.rng (
Generator
) – Random state to use for the random number generator.expert_trajs (
Optional
[Sequence
[]]) – Optional starting dataset that is inserted into the round 0 dataset.Trajectory
dagger_trainer_kwargs – Other keyword arguments passed to the superclass initializer DAggerTrainer.__init__.
- Raises
ValueError – The observation or action space does not match between venv and expert_policy.
-
allow_variable_horizon: bool
[#](#imitation.algorithms.dagger.SimpleDAggerTrainer.allow_variable_horizon) If True, allow variable horizon trajectories; otherwise error if detected.
-
train(total_timesteps, *, rollout_round_min_episodes=3, rollout_round_min_timesteps=500, bc_train_kwargs=None)
[[source]](../_modules/imitation/algorithms/dagger.html#SimpleDAggerTrainer.train)[#](#imitation.algorithms.dagger.SimpleDAggerTrainer.train) Train the DAgger agent.
The agent is trained in “rounds” where each round consists of a dataset aggregation step followed by BC update step.
During a dataset aggregation step, self.expert_policy is used to perform rollouts in the environment but there is a 1 - beta chance (beta is determined from the round number and self.beta_schedule) that the DAgger agent’s action is used instead. Regardless of whether the DAgger agent’s action is used during the rollout, the expert action and corresponding observation are always appended to the dataset. The number of environment steps in the dataset aggregation stage is determined by the rollout_round_min* arguments.
During a BC update step, BC.train() is called to update the DAgger agent on all data collected so far.
- Parameters
total_timesteps (
int
) – The number of timesteps to train inside the environment. In practice this is a lower bound, because the number of timesteps is rounded up to finish the minimum number of episodes or timesteps in the last DAgger training round, and the environment timesteps are executed in multiples of self.venv.num_envs.rollout_round_min_episodes (
int
) – The number of episodes the must be completed completed before a dataset aggregation step ends.rollout_round_min_timesteps (
int
) – The number of environment timesteps that must be completed before a dataset aggregation step ends. Also, that any round will always train for at least self.batch_size timesteps, because otherwise BC could fail to receive any batches.bc_train_kwargs (
Optional
[dict
]) – Keyword arguments for calling BC.train(). If the log_rollouts_venv key is not provided, then it is set to self.venv by default. If neither of the n_epochs and n_batches keys are provided, then n_epochs is set to self.DEFAULT_N_EPOCHS.
- Return type
None
-
__init__(*, venv, scratch_dir, expert_policy, rng, expert_trajs=None, **dagger_trainer_kwargs)
-
imitation.algorithms.dagger.reconstruct_trainer(scratch_dir, venv, custom_logger=None, device='auto')
[[source]](../_modules/imitation/algorithms/dagger.html#reconstruct_trainer)[#](#imitation.algorithms.dagger.reconstruct_trainer) Reconstruct trainer from the latest snapshot in some working directory.
Requires vectorized environment and (optionally) a logger, as these objects cannot be serialized.
- Parameters
scratch_dir (
Union
[str
,bytes
,PathLike
]) – path to the working directory created by a previous run of this algorithm. The directory should contain checkpoint-latest.pt and policy-latest.pt files.venv (
VecEnv
) – Vectorized training environment.custom_logger (
Optional
[]) – Where to log to; if None (default), creates a new logger.HierarchicalLogger
device (
Union
[device
,str
]) – device on which to load the trainer.
- Return type
- Returns
A deserialized DAggerTrainer.