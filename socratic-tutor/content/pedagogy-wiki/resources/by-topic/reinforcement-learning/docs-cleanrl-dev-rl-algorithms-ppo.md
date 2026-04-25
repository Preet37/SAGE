# Source: https://docs.cleanrl.dev/rl-algorithms/ppo/
# Downloaded: 2026-04-06
# Words: 7498
# Author: CleanRL
# Author Slug: cleanrl
Proximal Policy Gradient (PPO)
Overview
PPO is one of the most popular DRL algorithms. It runs reasonably fast by leveraging vector (parallel) environments and naturally works well with different action spaces, therefore supporting a variety of games. It also has good sample efficiency compared to algorithms such as DQN.
Original paper:
Reference resources:
[Implementation Matters in Deep Policy Gradients: A Case Study on PPO and TRPO](https://arxiv.org/abs/2005.12729)[What Matters In On-Policy Reinforcement Learning? A Large-Scale Empirical Study](https://arxiv.org/abs/2006.05990)- ⭐
[The 37 Implementation Details of Proximal Policy Optimization](https://iclr-blog-track.github.io/2022/03/25/ppo-implementation-details/)
All our PPO implementations below are augmented with the same code-level optimizations presented in openai/baselines
's [PPO](https://github.com/openai/baselines/tree/master/baselines/ppo2). To achieve this, see how we matched the implementation details in our blog post [The 37 Implementation Details of Proximal Policy Optimization](https://iclr-blog-track.github.io/2022/03/25/ppo-implementation-details/).
Implemented Variants
| Variants Implemented | Description |
|---|---|
|
ppo.py |
[docs](/rl-algorithms/ppo/#ppopy)
CartPole-v1
.[,](https://github.com/vwxyzjn/cleanrl/blob/master/cleanrl/ppo_atari.py)ppo_atari.py
[docs](/rl-algorithms/ppo/#ppo_ataripy)[,](https://github.com/vwxyzjn/cleanrl/blob/master/cleanrl/ppo_continuous_action.py)ppo_continuous_action.py
[docs](/rl-algorithms/ppo/#ppo_continuous_actionpy)[,](https://github.com/vwxyzjn/cleanrl/blob/master/cleanrl/ppo_atari_lstm.py)ppo_atari_lstm.py
[docs](/rl-algorithms/ppo/#ppo_atari_lstmpy)[,](https://github.com/vwxyzjn/cleanrl/blob/master/cleanrl/ppo_atari_envpool.py)ppo_atari_envpool.py
[docs](/rl-algorithms/ppo/#ppo_atari_envpoolpy)[,](https://github.com/vwxyzjn/cleanrl/blob/master/cleanrl/ppo_atari_envpool_xla_jax.py)ppo_atari_envpool_xla_jax.py
[docs](/rl-algorithms/ppo/#ppo_atari_envpool_xla_jaxpy)[,](https://github.com/vwxyzjn/cleanrl/blob/master/cleanrl/ppo_atari_envpool_xla_jax_scan.py)ppo_atari_envpool_xla_jax_scan.py
[docs](/rl-algorithms/ppo/#ppo_atari_envpool_xla_jax_scanpy)jax.scan
as opposed to python loops for faster compilation time.[,](https://github.com/vwxyzjn/cleanrl/blob/master/cleanrl/ppo_procgen.py)ppo_procgen.py
[docs](/rl-algorithms/ppo/#ppo_procgenpy)[,](https://github.com/vwxyzjn/cleanrl/blob/master/cleanrl/ppo_atari_multigpu.py)ppo_atari_multigpu.py
[docs](/rl-algorithms/ppo/#ppo_atari_multigpupy)[,](https://github.com/vwxyzjn/cleanrl/blob/master/cleanrl/ppo_pettingzoo_ma_atari.py)ppo_pettingzoo_ma_atari.py
[docs](/rl-algorithms/ppo/#ppo_pettingzoo_ma_ataripy)Below are our single-file implementations of PPO:
ppo.py
The [ppo.py](https://github.com/vwxyzjn/cleanrl/blob/master/cleanrl/ppo.py) has the following features:
- Works with the
Box
observation space of low-level features - Works with the
Discrete
action space - Works with envs like
CartPole-v1
Usage
uv pip install .
uv run python cleanrl/ppo.py --help
uv run python cleanrl/ppo.py --env-id CartPole-v1
python cleanrl/ppo.py --help
python cleanrl/ppo.py --env-id CartPole-v1
Explanation of the logged metrics
Running python cleanrl/ppo.py
will automatically record various metrics such as actor or value losses in Tensorboard. Below is the documentation for these metrics:
charts/episodic_return
: episodic return of the gamecharts/episodic_length
: episodic length of the gamecharts/SPS
: number of steps per secondcharts/learning_rate
: the current learning ratelosses/value_loss
: the mean value loss across all data pointslosses/policy_loss
: the mean policy loss across all data pointslosses/entropy
: the mean entropy value across all data pointslosses/old_approx_kl
: the approximate Kullback–Leibler divergence, measured by(-logratio).mean()
, which corresponds to the k1 estimator in John Schulman’s blog post on[approximating KL](http://joschu.net/blog/kl-approx.html)losses/approx_kl
: better alternative toolad_approx_kl
measured by(logratio.exp() - 1) - logratio
, which corresponds to the k3 estimator in[approximating KL](http://joschu.net/blog/kl-approx.html)losses/clipfrac
: the fraction of the training data that triggered the clipped objectivelosses/explained_variance
: the explained variance for the value function
Implementation details
[ppo.py](https://github.com/vwxyzjn/cleanrl/blob/master/cleanrl/ppo.py) is based on the "13 core implementation details" in [The 37 Implementation Details of Proximal Policy Optimization](https://iclr-blog-track.github.io/2022/03/25/ppo-implementation-details/), which are as follows:
- Vectorized architecture (
[common/cmd_util.py#L22](https://github.com/openai/baselines/blob/ea25b9e8b234e6ee1bca43083f8f3cf974143998/baselines/common/cmd_util.py#L22)) - Orthogonal Initialization of Weights and Constant Initialization of biases (
[a2c/utils.py#L58)](https://github.com/openai/baselines/blob/ea25b9e8b234e6ee1bca43083f8f3cf974143998/baselines/a2c/utils.py#L58)) - The Adam Optimizer's Epsilon Parameter (
[ppo2/model.py#L100](https://github.com/openai/baselines/blob/ea25b9e8b234e6ee1bca43083f8f3cf974143998/baselines/ppo2/model.py#L100)) - Adam Learning Rate Annealing (
[ppo2/ppo2.py#L133-L135](https://github.com/openai/baselines/blob/ea25b9e8b234e6ee1bca43083f8f3cf974143998/baselines/ppo2/ppo2.py#L133-L135)) - Generalized Advantage Estimation (
[ppo2/runner.py#L56-L65](https://github.com/openai/baselines/blob/ea25b9e8b234e6ee1bca43083f8f3cf974143998/baselines/ppo2/runner.py#L56-L65)) - Mini-batch Updates (
[ppo2/ppo2.py#L157-L166](https://github.com/openai/baselines/blob/ea25b9e8b234e6ee1bca43083f8f3cf974143998/baselines/ppo2/ppo2.py#L157-L166)) - Normalization of Advantages (
[ppo2/model.py#L139](https://github.com/openai/baselines/blob/ea25b9e8b234e6ee1bca43083f8f3cf974143998/baselines/ppo2/model.py#L139)) - Clipped surrogate objective (
[ppo2/model.py#L81-L86](https://github.com/openai/baselines/blob/ea25b9e8b234e6ee1bca43083f8f3cf974143998/baselines/ppo2/model.py#L81-L86)) - Value Function Loss Clipping (
[ppo2/model.py#L68-L75](https://github.com/openai/baselines/blob/ea25b9e8b234e6ee1bca43083f8f3cf974143998/baselines/ppo2/model.py#L68-L75)) - Overall Loss and Entropy Bonus (
[ppo2/model.py#L91](https://github.com/openai/baselines/blob/ea25b9e8b234e6ee1bca43083f8f3cf974143998/baselines/ppo2/model.py#L91)) - Global Gradient Clipping (
[ppo2/model.py#L102-L108](https://github.com/openai/baselines/blob/ea25b9e8b234e6ee1bca43083f8f3cf974143998/baselines/ppo2/model.py#L102-L108)) - Debug variables (
[ppo2/model.py#L115-L116](https://github.com/openai/baselines/blob/ea25b9e8b234e6ee1bca43083f8f3cf974143998/baselines/ppo2/model.py#L115-L116)) - Separate MLP networks for policy and value functions (
[common/policies.py#L156-L160](https://github.com/openai/baselines/blob/ea25b9e8b234e6ee1bca43083f8f3cf974143998/baselines/common/policies.py#L156-L160),[baselines/common/models.py#L75-L103](https://github.com/openai/baselines/blob/ea25b9e8b234e6ee1bca43083f8f3cf974143998/baselines/common/models.py#L75-L103))
Experiment results
To run benchmark experiments, see [benchmark/ppo.sh](https://github.com/vwxyzjn/cleanrl/blob/master/benchmark/ppo.sh). Specifically, execute the following command:
| benchmark/ppo.sh | |
|---|---|
1 2 3 4 5 6 |
|
Below are the average episodic returns for ppo.py
. To ensure the quality of the implementation, we compared the results against openai/baselies
' PPO.
| Environment | ppo.py |
openai/baselies ' PPO (Huang et al., 2022)
|
|---|---|---|
| CartPole-v1 | 490.04 ± 6.12 | 497.54 ± 4.02 |
| Acrobot-v1 | -86.36 ± 1.32 | -81.82 ± 5.58 |
| MountainCar-v0 | -200.00 ± 0.00 | -200.00 ± 0.00 |
Learning curves:
| benchmark/ppo_plot.sh | |
|---|---|
1 2 3 4 5 6 7 8 9 |
|
Tracked experiments and game play videos:
Video tutorial
If you'd like to learn ppo.py
in-depth, consider checking out the following video tutorial:
ppo_atari.py
The [ppo_atari.py](https://github.com/vwxyzjn/cleanrl/blob/master/cleanrl/ppo_atari.py) has the following features:
- For Atari games. It uses convolutional layers and common atari-based pre-processing techniques.
- Works with the Atari's pixel
Box
observation space of shape(210, 160, 3)
- Works with the
Discrete
action space
Usage
uv pip install ".[atari]"
uv run python cleanrl/ppo_atari.py --help
uv run python cleanrl/ppo_atari.py --env-id BreakoutNoFrameskip-v4
pip install -r requirements/requirements-atari.txt
python cleanrl/ppo_atari.py --help
python cleanrl/ppo_atari.py --env-id BreakoutNoFrameskip-v4
Explanation of the logged metrics
See [related docs](/rl-algorithms/ppo/#explanation-of-the-logged-metrics) for ppo.py
.
Implementation details
[ppo_atari.py](https://github.com/vwxyzjn/cleanrl/blob/master/cleanrl/ppo_atari.py) is based on the "9 Atari implementation details" in [The 37 Implementation Details of Proximal Policy Optimization](https://iclr-blog-track.github.io/2022/03/25/ppo-implementation-details/), which are as follows:
- The Use of
NoopResetEnv
([common/atari_wrappers.py#L12](https://github.com/openai/baselines/blob/ea25b9e8b234e6ee1bca43083f8f3cf974143998/baselines/common/atari_wrappers.py#L12)) - The Use of
MaxAndSkipEnv
([common/atari_wrappers.py#L97](https://github.com/openai/baselines/blob/ea25b9e8b234e6ee1bca43083f8f3cf974143998/baselines/common/atari_wrappers.py#L97)) - The Use of
EpisodicLifeEnv
([common/atari_wrappers.py#L61](https://github.com/openai/baselines/blob/ea25b9e8b234e6ee1bca43083f8f3cf974143998/baselines/common/atari_wrappers.py#L61)) - The Use of
FireResetEnv
([common/atari_wrappers.py#L41](https://github.com/openai/baselines/blob/ea25b9e8b234e6ee1bca43083f8f3cf974143998/baselines/common/atari_wrappers.py#L41)) - The Use of
WarpFrame
(Image transformation)[common/atari_wrappers.py#L134](https://github.com/openai/baselines/blob/ea25b9e8b234e6ee1bca43083f8f3cf974143998/baselines/common/atari_wrappers.py#L134) - The Use of
ClipRewardEnv
([common/atari_wrappers.py#L125](https://github.com/openai/baselines/blob/ea25b9e8b234e6ee1bca43083f8f3cf974143998/baselines/common/atari_wrappers.py#L125)) - The Use of
FrameStack
([common/atari_wrappers.py#L188](https://github.com/openai/baselines/blob/ea25b9e8b234e6ee1bca43083f8f3cf974143998/baselines/common/atari_wrappers.py#L188)) - Shared Nature-CNN network for the policy and value functions (
[common/policies.py#L157](https://github.com/openai/baselines/blob/ea25b9e8b234e6ee1bca43083f8f3cf974143998/baselines/common/policies.py#L157),[common/models.py#L15-L26](https://github.com/openai/baselines/blob/ea25b9e8b234e6ee1bca43083f8f3cf974143998/baselines/common/models.py#L15-L26)) - Scaling the Images to Range [0, 1] (
[common/models.py#L19](https://github.com/openai/baselines/blob/9b68103b737ac46bc201dfb3121cfa5df2127e53/baselines/common/models.py#L19))
Experiment results
To run benchmark experiments, see [benchmark/ppo.sh](https://github.com/vwxyzjn/cleanrl/blob/master/benchmark/ppo.sh). Specifically, execute the following command:
| benchmark/ppo.sh | |
|---|---|
1 2 3 4 5 6 |
|
Below are the average episodic returns for ppo_atari.py
. To ensure the quality of the implementation, we compared the results against openai/baselies
' PPO.
| Environment | ppo_atari.py |
openai/baselies ' PPO (Huang et al., 2022)
|
|---|---|---|
| BreakoutNoFrameskip-v4 | 414.66 ± 28.09 | 406.57 ± 31.554 |
| PongNoFrameskip-v4 | 20.36 ± 0.20 | 20.512 ± 0.50 |
| BeamRiderNoFrameskip-v4 | 1915.93 ± 484.58 | 2642.97 ± 670.37 |
Learning curves:
| benchmark/ppo_plot.sh | |
|---|---|
1 2 3 4 5 6 7 8 9 |
|
Tracked experiments and game play videos:
Video tutorial
If you'd like to learn ppo_atari.py
in-depth, consider checking out the following video tutorial:
ppo_continuous_action.py
The [ppo_continuous_action.py](https://github.com/vwxyzjn/cleanrl/blob/master/cleanrl/ppo_continuous_action.py) has the following features:
- For continuous action space. Also implemented Mujoco-specific code-level optimizations
- Works with the
Box
observation space of low-level features - Works with the
Box
(continuous) action space - adding experimental support for
[Gymnasium](https://gymnasium.farama.org/) - 🧪 support
dm_control
environments via[Shimmy](https://github.com/Farama-Foundation/Shimmy)
Warning
We are now recommending users to use [ rpo_continuous_action.py](https://github.com/vwxyzjn/cleanrl/blob/master/cleanrl/rpo_continuous_action.py) instead of
[because](https://github.com/vwxyzjn/cleanrl/blob/master/cleanrl/ppo_continuous_action.py)
ppo_continuous_action.py
rpo_continuous_action.py
empirically performs better than ppo_continuous_action.py
in 93% of the environments we tested. Please see [experiment results](/rl-algorithms/rpo/#experiment-results)for detailed analysis.
Usage
# mujoco v4 environments
uv pip install ".[mujoco]"
python cleanrl/ppo_continuous_action.py --help
python cleanrl/ppo_continuous_action.py --env-id Hopper-v4
# dm_control environments
uv pip install ".[mujoco, dm_control]"
python cleanrl/ppo_continuous_action.py --env-id dm_control/cartpole-balance-v0
pip install -r requirements/requirements-mujoco.txt
python cleanrl/ppo_continuous_action.py --help
python cleanrl/ppo_continuous_action.py --env-id Hopper-v4
pip install -r requirements/requirements-dm_control.txt
python cleanrl/ppo_continuous_action.py --env-id dm_control/cartpole-balance-v0
dm_control installation issue
If you run into error like AttributeError: 'GLFWContext' object has no attribute '_context'
in Linux, it's because the rendering dependencies are not installed properly. To fix it, try running
sudo apt-get update && sudo apt-get -y install libgl1-mesa-glx libosmesa6 libglfw3
See [https://github.com/deepmind/dm_control#rendering](https://github.com/deepmind/dm_control#rendering) for more detail.
Explanation of the logged metrics
See [related docs](/rl-algorithms/ppo/#explanation-of-the-logged-metrics) for ppo.py
.
Implementation details
[ppo_continuous_action.py](https://github.com/vwxyzjn/cleanrl/blob/master/cleanrl/ppo_continuous_action.py) is based on the "9 details for continuous action domains (e.g. Mujoco)" in [The 37 Implementation Details of Proximal Policy Optimization](https://iclr-blog-track.github.io/2022/03/25/ppo-implementation-details/), which are as follows:
- Continuous actions via normal distributions (
[common/distributions.py#L103-L104](https://github.com/openai/baselines/blob/9b68103b737ac46bc201dfb3121cfa5df2127e53/baselines/common/distributions.py#L103-L104)) - State-independent log standard deviation (
[common/distributions.py#L104](https://github.com/openai/baselines/blob/9b68103b737ac46bc201dfb3121cfa5df2127e53/baselines/common/distributions.py#L104)) - Independent action components (
[common/distributions.py#L238-L246](https://github.com/openai/baselines/blob/9b68103b737ac46bc201dfb3121cfa5df2127e53/baselines/common/distributions.py#L238-L246)) - Separate MLP networks for policy and value functions (
[common/policies.py#L160](https://github.com/openai/baselines/blob/ea25b9e8b234e6ee1bca43083f8f3cf974143998/baselines/common/policies.py#L160),[baselines/common/models.py#L75-L103](https://github.com/openai/baselines/blob/ea25b9e8b234e6ee1bca43083f8f3cf974143998/baselines/common/models.py#L75-L103) - Handling of action clipping to valid range and storage (
[common/cmd_util.py#L99-L100](https://github.com/openai/baselines/blob/ea25b9e8b234e6ee1bca43083f8f3cf974143998/baselines/common/cmd_util.py#L99-L100)) - Normalization of Observation (
[common/vec_env/vec_normalize.py#L4](https://github.com/openai/baselines/blob/ea25b9e8b234e6ee1bca43083f8f3cf974143998/baselines/common/vec_env/vec_normalize.py#L4)) - Observation Clipping (
[common/vec_env/vec_normalize.py#L39](https://github.com/openai/baselines/blob/ea25b9e8b234e6ee1bca43083f8f3cf974143998/baselines/common/vec_env/vec_normalize.py#L39)) - Reward Scaling (
[common/vec_env/vec_normalize.py#L28](https://github.com/openai/baselines/blob/ea25b9e8b234e6ee1bca43083f8f3cf974143998/baselines/common/vec_env/vec_normalize.py#L28)) - Reward Clipping (
[common/vec_env/vec_normalize.py#L32](https://github.com/openai/baselines/blob/ea25b9e8b234e6ee1bca43083f8f3cf974143998/baselines/common/vec_env/vec_normalize.py#L32))
Experiment results
To run benchmark experiments, see [benchmark/ppo.sh](https://github.com/vwxyzjn/cleanrl/blob/master/benchmark/ppo.sh). Specifically, execute the following command:
MuJoCo v4
| benchmark/ppo.sh | |
|---|---|
1 2 3 4 5 6 |
|
| openrlbenchmark/cleanrl/ppo_continuous_action ({'tag': ['pr-424']}) | |
|---|---|
| HalfCheetah-v4 | 1442.64 ± 46.03 |
| Walker2d-v4 | 2287.95 ± 571.78 |
| Hopper-v4 | 2382.86 ± 271.74 |
| InvertedPendulum-v4 | 963.09 ± 22.20 |
| Humanoid-v4 | 716.11 ± 49.08 |
| Pusher-v4 | -40.38 ± 7.15 |
| dm_control/acrobot-swingup-v0 | 25.60 ± 6.30 |
| dm_control/acrobot-swingup_sparse-v0 | 1.35 ± 0.27 |
| dm_control/ball_in_cup-catch-v0 | 619.26 ± 278.67 |
Learning curves:
| benchmark/ppo_plot.sh | |
|---|---|
1 2 3 4 5 6 7 8 9 |
|
Tracked experiments and game play videos:
| benchmark/ppo.sh | |
|---|---|
1 2 3 4 5 6 |
|
Below are the average episodic returns for ppo_continuous_action.py
in dm_control
environments.
| ppo_continuous_action ({'tag': ['v1.0.0-13-gcbd83f6']}) | |
|---|---|
| dm_control/acrobot-swingup-v0 | 27.84 ± 9.25 |
| dm_control/acrobot-swingup_sparse-v0 | 1.60 ± 1.17 |
| dm_control/ball_in_cup-catch-v0 | 900.78 ± 5.26 |
| dm_control/cartpole-balance-v0 | 855.47 ± 22.06 |
| dm_control/cartpole-balance_sparse-v0 | 999.93 ± 0.10 |
| dm_control/cartpole-swingup-v0 | 640.86 ± 11.44 |
| dm_control/cartpole-swingup_sparse-v0 | 51.34 ± 58.35 |
| dm_control/cartpole-two_poles-v0 | 203.86 ± 11.84 |
| dm_control/cartpole-three_poles-v0 | 164.59 ± 3.23 |
| dm_control/cheetah-run-v0 | 432.56 ± 82.54 |
| dm_control/dog-stand-v0 | 307.79 ± 46.26 |
| dm_control/dog-walk-v0 | 120.05 ± 8.80 |
| dm_control/dog-trot-v0 | 76.56 ± 6.44 |
| dm_control/dog-run-v0 | 60.25 ± 1.33 |
| dm_control/dog-fetch-v0 | 34.26 ± 2.24 |
| dm_control/finger-spin-v0 | 590.49 ± 171.09 |
| dm_control/finger-turn_easy-v0 | 180.42 ± 44.91 |
| dm_control/finger-turn_hard-v0 | 61.40 ± 9.59 |
| dm_control/fish-upright-v0 | 516.21 ± 59.52 |
| dm_control/fish-swim-v0 | 87.91 ± 6.83 |
| dm_control/hopper-stand-v0 | 2.72 ± 1.72 |
| dm_control/hopper-hop-v0 | 0.52 ± 0.48 |
| dm_control/humanoid-stand-v0 | 6.59 ± 0.18 |
| dm_control/humanoid-walk-v0 | 1.73 ± 0.03 |
| dm_control/humanoid-run-v0 | 1.11 ± 0.04 |
| dm_control/humanoid-run_pure_state-v0 | 0.98 ± 0.03 |
| dm_control/humanoid_CMU-stand-v0 | 4.79 ± 0.18 |
| dm_control/humanoid_CMU-run-v0 | 0.88 ± 0.05 |
| dm_control/manipulator-bring_ball-v0 | 0.50 ± 0.29 |
| dm_control/manipulator-bring_peg-v0 | 1.80 ± 1.58 |
| dm_control/manipulator-insert_ball-v0 | 35.50 ± 13.04 |
| dm_control/manipulator-insert_peg-v0 | 60.40 ± 21.76 |
| dm_control/pendulum-swingup-v0 | 242.81 ± 245.95 |
| dm_control/point_mass-easy-v0 | 273.95 ± 362.28 |
| dm_control/point_mass-hard-v0 | 143.25 ± 38.12 |
| dm_control/quadruped-walk-v0 | 239.03 ± 66.17 |
| dm_control/quadruped-run-v0 | 180.44 ± 32.91 |
| dm_control/quadruped-escape-v0 | 28.92 ± 11.21 |
| dm_control/quadruped-fetch-v0 | 193.97 ± 22.20 |
| dm_control/reacher-easy-v0 | 626.28 ± 15.51 |
| dm_control/reacher-hard-v0 | 443.80 ± 9.64 |
| dm_control/stacker-stack_2-v0 | 75.68 ± 4.83 |
| dm_control/stacker-stack_4-v0 | 68.02 ± 4.02 |
| dm_control/swimmer-swimmer6-v0 | 158.19 ± 10.22 |
| dm_control/swimmer-swimmer15-v0 | 131.94 ± 0.88 |
| dm_control/walker-stand-v0 | 564.46 ± 235.22 |
| dm_control/walker-walk-v0 | 392.51 ± 56.25 |
| dm_control/walker-run-v0 | 125.92 ± 10.01 |
Note that the dm_control/lqr-lqr_2_1-v0 dm_control/lqr-lqr_6_2-v0 environments are never terminated or truncated. See https://wandb.ai/openrlbenchmark/cleanrl/runs/3tm00923 and https://wandb.ai/openrlbenchmark/cleanrl/runs/1z9us07j as an example.
Learning curves:
Tracked experiments and game play videos:
Info
In the gymnasium environments, we use the v4 mujoco environments, which roughly results in the same performance as the v2 mujoco environments.
Video tutorial
If you'd like to learn ppo_continuous_action.py
in-depth, consider checking out the following video tutorial:
ppo_atari_lstm.py
The [ppo_atari_lstm.py](https://github.com/vwxyzjn/cleanrl/blob/master/cleanrl/ppo_atari_lstm.py) has the following features:
- For Atari games using LSTM without stacked frames. It uses convolutional layers and common atari-based pre-processing techniques.
- Works with the Atari's pixel
Box
observation space of shape(210, 160, 3)
- Works with the
Discrete
action space
Usage
uv pip install ".[atari]"
uv run python cleanrl/ppo_atari_lstm.py --help
uv run python cleanrl/ppo_atari_lstm.py --env-id BreakoutNoFrameskip-v4
pip install -r requirements/requirements-atari.txt
python cleanrl/ppo_atari_lstm.py --help
python cleanrl/ppo_atari_lstm.py --env-id BreakoutNoFrameskip-v4
Explanation of the logged metrics
See [related docs](/rl-algorithms/ppo/#explanation-of-the-logged-metrics) for ppo.py
.
Implementation details
[ppo_atari_lstm.py](https://github.com/vwxyzjn/cleanrl/blob/master/cleanrl/ppo_atari_lstm.py) is based on the "5 LSTM implementation details" in [The 37 Implementation Details of Proximal Policy Optimization](https://iclr-blog-track.github.io/2022/03/25/ppo-implementation-details/), which are as follows:
- Layer initialization for LSTM layers (
[a2c/utils.py#L84-L86](https://github.com/openai/baselines/blob/ea25b9e8b234e6ee1bca43083f8f3cf974143998/baselines/a2c/utils.py#L84-L86)) - Initialize the LSTM states to be zeros (
[common/models.py#L179](https://github.com/openai/baselines/blob/ea25b9e8b234e6ee1bca43083f8f3cf974143998/baselines/common/models.py#L179)) - Reset LSTM states at the end of the episode (
[common/models.py#L141](https://github.com/openai/baselines/blob/ea25b9e8b234e6ee1bca43083f8f3cf974143998/baselines/common/models.py#L141)) - Prepare sequential rollouts in mini-batches (
[a2c/utils.py#L81](https://github.com/openai/baselines/blob/ea25b9e8b234e6ee1bca43083f8f3cf974143998/baselines/a2c/utils.py#L81)) - Reconstruct LSTM states during training (
[a2c/utils.py#L81](https://github.com/openai/baselines/blob/ea25b9e8b234e6ee1bca43083f8f3cf974143998/baselines/a2c/utils.py#L81))
To help test out the memory, we remove the 4 stacked frames from the observation (i.e., using env = gym.wrappers.FrameStack(env, 1)
instead of env = gym.wrappers.FrameStack(env, 4)
like in ppo_atari.py
)
Experiment results
To run benchmark experiments, see [benchmark/ppo.sh](https://github.com/vwxyzjn/cleanrl/blob/master/benchmark/ppo.sh). Specifically, execute the following command:
| benchmark/ppo.sh | |
|---|---|
1 2 3 4 5 6 |
|
Below are the average episodic returns for ppo_atari_lstm.py
. To ensure the quality of the implementation, we compared the results against openai/baselies
' PPO.
| Environment | ppo_atari_lstm.py |
openai/baselies ' PPO (Huang et al., 2022)
|
|---|---|---|
| BreakoutNoFrameskip-v4 | 128.92 ± 31.10 | 138.98 ± 50.76 |
| PongNoFrameskip-v4 | 19.78 ± 1.58 | 19.79 ± 0.67 |
| BeamRiderNoFrameskip-v4 | 1536.20 ± 612.21 | 1591.68 ± 372.95 |
Learning curves:
| benchmark/ppo_plot.sh | |
|---|---|
1 2 3 4 5 6 7 8 9 |
|
Tracked experiments and game play videos:
ppo_atari_envpool.py
The [ppo_atari_envpool.py](https://github.com/vwxyzjn/cleanrl/blob/master/cleanrl/ppo_atari_envpool.py) has the following features:
- Uses the blazing fast
[Envpool](https://github.com/sail-sg/envpool)vectorized environment. - For Atari games. It uses convolutional layers and common atari-based pre-processing techniques.
- Works with the Atari's pixel
Box
observation space of shape(210, 160, 3)
- Works with the
Discrete
action space
Warning
Note that ppo_atari_envpool.py
does not work in Windows and MacOs . See envpool's built wheels here: [https://pypi.org/project/envpool/#files](https://pypi.org/project/envpool/#files)
Bug
EnvPool's vectorized environment does not behave the same as gym's vectorized environment, which causes a compatibility bug in our PPO implementation. When an action \(a\) results in an episode termination or truncation, the environment generates \(s_{last}\) as the terminated or truncated state; we then use \(s_{new}\) to denote the initial state of the new episodes. Here is how the bahviors differ:
- Under the vectorized environment of
envpool<=0.6.4
, theobs
inobs, reward, done, info = env.step(action)
is the truncated state \(s_{last}\) - Under the vectorized environment of
gym==0.23.1
, theobs
inobs, reward, done, info = env.step(action)
is the initial state \(s_{new}\).
This causes the \(s_{last}\) to be off by one.
See [ sail-sg/envpool#194](https://github.com/sail-sg/envpool/issues/194) for more detail. However, it does not seem to impact performance, so we take a note here and await for the upstream fix.
Usage
uv pip install ".[envpool]"
uv run python cleanrl/ppo_atari_envpool.py --help
uv run python cleanrl/ppo_atari_envpool.py --env-id Breakout-v5
pip install -r requirements/requirements-envpool.txt
python cleanrl/ppo_atari_envpool.py --help
python cleanrl/ppo_atari_envpool.py --env-id Breakout-v5
Explanation of the logged metrics
See [related docs](/rl-algorithms/ppo/#explanation-of-the-logged-metrics) for ppo.py
.
Implementation details
[ppo_atari_envpool.py](https://github.com/vwxyzjn/cleanrl/blob/master/cleanrl/ppo_atari_envpool.py) uses a customized RecordEpisodeStatistics
to work with envpool but has the same other implementation details as ppo_atari.py
(see [related docs](/rl-algorithms/ppo/#implementation-details_1)).
Experiment results
To run benchmark experiments, see [benchmark/ppo.sh](https://github.com/vwxyzjn/cleanrl/blob/master/benchmark/ppo.sh). Specifically, execute the following command:
| benchmark/ppo.sh | |
|---|---|
1 2 3 4 5 6 |
|
| openrlbenchmark/cleanrl/ppo_atari_envpool ({'tag': ['pr-424']}) | openrlbenchmark/cleanrl/ppo_atari ({'tag': ['pr-424']}) | |
|---|---|---|
| Pong-v5 | 20.45 ± 0.09 | 20.36 ± 0.20 |
| BeamRider-v5 | 2501.85 ± 210.52 | 1915.93 ± 484.58 |
| Breakout-v5 | 211.24 ± 151.84 | 414.66 ± 28.09 |
Learning curves:
| benchmark/ppo_plot.sh | |
|---|---|
1 2 3 4 5 6 7 8 9 10 11 12 |
|
Tracked experiments and game play videos:
ppo_atari_envpool_xla_jax.py
The [ppo_atari_envpool_xla_jax.py](https://github.com/vwxyzjn/cleanrl/blob/master/cleanrl/ppo_atari_envpool_xla_jax.py) has the following features:
- Uses the blazing fast
[Envpool](https://github.com/sail-sg/envpool)vectorized environment.- Uses EnvPool's experimental
[XLA interface](https://envpool.readthedocs.io/en/latest/content/xla_interface.html).
- Uses EnvPool's experimental
- Uses
[Jax](https://github.com/google/jax),[Flax](https://github.com/google/flax), and[Optax](https://github.com/deepmind/optax)instead oftorch
. - For Atari games. It uses convolutional layers and common atari-based pre-processing techniques.
- Works with the Atari's pixel
Box
observation space of shape(210, 160, 3)
- Works with the
Discrete
action space
Warning
Note that ppo_atari_envpool_xla_jax.py
does not work in Windows and MacOs . See envpool's built wheels here: [https://pypi.org/project/envpool/#files](https://pypi.org/project/envpool/#files)
Bug
EnvPool's vectorized environment does not behave the same as gym's vectorized environment, which causes a compatibility bug in our PPO implementation. When an action \(a\) results in an episode termination or truncation, the environment generates \(s_{last}\) as the terminated or truncated state; we then use \(s_{new}\) to denote the initial state of the new episodes. Here is how the bahviors differ:
- Under the vectorized environment of
envpool<=0.6.4
, theobs
inobs, reward, done, info = env.step(action)
is the truncated state \(s_{last}\) - Under the vectorized environment of
gym==0.23.1
, theobs
inobs, reward, done, info = env.step(action)
is the initial state \(s_{new}\).
This causes the \(s_{last}\) to be off by one.
See [ sail-sg/envpool#194](https://github.com/sail-sg/envpool/issues/194) for more detail. However, it does not seem to impact performance, so we take a note here and await for the upstream fix.
Usage
uv pip install ".[envpool, jax]"
uv pip install --upgrade "jax[cuda11_cudnn82]==0.4.8" -f https://storage.googleapis.com/jax-releases/jax_cuda_releases.html
uv run python cleanrl/ppo_atari_envpool_xla_jax.py --help
uv run python cleanrl/ppo_atari_envpool_xla_jax.py --env-id Breakout-v5
pip install -r requirements/requirements-envpool.txt
pip install -r requirements/requirements-jax.txt
pip install --upgrade "jax[cuda]==0.3.17" -f https://storage.googleapis.com/jax-releases/jax_cuda_releases.html
python cleanrl/ppo_atari_envpool_xla_jax.py --help
python cleanrl/ppo_atari_envpool_xla_jax.py --env-id Breakout-v5
Explanation of the logged metrics
See [related docs](/rl-algorithms/ppo/#explanation-of-the-logged-metrics) for ppo.py
. In [ppo_atari_envpool_xla_jax.py](https://github.com/vwxyzjn/cleanrl/blob/master/cleanrl/ppo_atari_envpool_xla_jax.py) we omit logging losses/old_approx_kl
and losses/clipfrac
for brevity.
Additionally, we record the following metric:
charts/avg_episodic_return
: the average value of the latest episodic returns ofargs.num_envs=8
envscharts/avg_episodic_length
: the average value of the latest episodic lengths ofargs.num_envs=8
envs
Info
Note that we use charts/avg_episodic_return
and charts/avg_episodic_length
in place of charts/episodic_return
and charts/episodic_length
because under the EnvPool's XLA interface, we can only record fixed-shape metrics where as there could be a variable number of raw episodic returns / lengths. To resolve this challenge, we create variables (e.g., returned_episode_returns
, returned_episode_lengths
) to keep track of the latest episodic returns / lengths of each environment and average them for reporting purposes.
Implementation details
[ppo_atari_envpool_xla_jax.py](https://github.com/vwxyzjn/cleanrl/blob/master/cleanrl/ppo_atari_envpool_xla_jax.py) uses the same other implementation details as ppo_atari.py
(see [related docs](/rl-algorithms/ppo/#implementation-details_1)), with two differences
[ppo_atari_envpool_xla_jax.py](https://github.com/vwxyzjn/cleanrl/blob/master/cleanrl/ppo_atari_envpool_xla_jax.py)does not use the value function clipping by default, because there is no sufficient evidence that value function clipping actually improves performance.[ppo_atari_envpool_xla_jax.py](https://github.com/vwxyzjn/cleanrl/blob/master/cleanrl/ppo_atari_envpool_xla_jax.py)uses a customizedEpisodeStatistics
to record episode statistics instead of theRecordEpisodeStatistics
used in other variants.RecordEpisodeStatistics
is a stateful python wrapper which is incompatible with EnvPool's stateless XLA interface. To address this issue, we used aEpisodeStatistics
dataclass and simply implement the logic ofRecordEpisodeStatistics
. However,EpisodeStatistics
comes with a major limitation: its storage has a fixed shape and can only record the latest episodic return of the sub-environments. Furthermore, the default episodic return values inEpisodeStatistics
are set to zeros, which does not necessarily correspond to the episodic return obtained by a random policy. For example, we would reportcharts/avg_episodic_return=0
forPong-v5
, even if they should have beencharts/avg_episodic_return=-21
. That said, this issue goes away as soon as the sub-environments finished their first episodes, therefore not impacting the reported results.
Info
We benchmarked the PPO implementation w/ and w/o value function clipping, finding no significant difference in performance, which is consistent with the findings in Andrychowicz et al.[2](#fn:2). See the related report [part 1](https://wandb.ai/costa-huang/cleanRL/reports/CleanRL-PPO-JAX-EnvPool-s-XLA-w-and-w-o-value-loss-clipping-vs-openai-baselins-PPO-part-1---VmlldzoyNzQ3MzQ1) and [part 2](https://wandb.ai/costa-huang/cleanRL/reports/CleanRL-PPO-JAX-EnvPool-s-XLA-w-and-w-o-value-loss-clipping-vs-openai-baselins-PPO-part-2---VmlldzoyNzQ3MzUw).
Experiment results
To run benchmark experiments, see [benchmark/ppo.sh](https://github.com/vwxyzjn/cleanrl/blob/master/benchmark/ppo.sh). Specifically, execute the following command:
| benchmark/ppo.sh | |
|---|---|
1 2 3 4 5 6 |
|
| openrlbenchmark/envpool-atari/ppo_atari_envpool_xla_jax ({}) | openrlbenchmark/baselines/baselines-ppo2-cnn ({}) | |
|---|---|---|
| Alien-v5 | 1736.39 ± 68.65 | 1705.80 ± 439.74 |
| Amidar-v5 | 653.53 ± 44.06 | 585.99 ± 52.92 |
| Assault-v5 | 6791.74 ± 420.03 | 4878.67 ± 815.64 |
| Asterix-v5 | 4820.33 ± 1091.83 | 3738.50 ± 745.13 |
| Asteroids-v5 | 1633.67 ± 247.21 | 1556.90 ± 151.20 |
| Atlantis-v5 | 3778458.33 ± 117680.68 | 2036749.00 ± 95929.75 |
| BankHeist-v5 | 1195.44 ± 18.54 | 1213.47 ± 14.46 |
| BattleZone-v5 | 24283.75 ± 1841.94 | 19980.00 ± 1355.21 |
| BeamRider-v5 | 2478.44 ± 336.55 | 2835.71 ± 387.92 |
| Berzerk-v5 | 992.88 ± 196.90 | 1049.77 ± 144.58 |
| Bowling-v5 | 51.62 ± 13.53 | 59.66 ± 0.62 |
| Boxing-v5 | 92.68 ± 1.41 | 93.32 ± 0.36 |
| Breakout-v5 | 430.09 ± 8.12 | 405.73 ± 11.47 |
| Centipede-v5 | 3309.34 ± 325.05 | 3688.54 ± 412.24 |
| ChopperCommand-v5 | 5642.83 ± 802.34 | 816.33 ± 114.14 |
| CrazyClimber-v5 | 118763.04 ± 4915.34 | 119344.67 ± 4902.83 |
| Defender-v5 | 48558.98 ± 4466.76 | 50161.67 ± 4477.49 |
| DemonAttack-v5 | 29283.83 ± 7007.31 | 13788.43 ± 1313.44 |
| DoubleDunk-v5 | -6.81 ± 0.24 | -12.96 ± 0.31 |
| Enduro-v5 | 1297.23 ± 143.71 | 986.69 ± 25.28 |
| FishingDerby-v5 | 21.21 ± 6.73 | 26.23 ± 2.76 |
| Freeway-v5 | 33.10 ± 0.31 | 32.97 ± 0.37 |
| Frostbite-v5 | 1137.34 ± 1192.05 | 933.60 ± 885.92 |
| Gopher-v5 | 6505.29 ± 7655.20 | 3672.53 ± 1749.20 |
| Gravitar-v5 | 1099.33 ± 603.06 | 881.67 ± 33.73 |
| Hero-v5 | 26429.65 ± 924.74 | 24746.88 ± 3530.10 |
| IceHockey-v5 | -4.33 ± 0.43 | -4.12 ± 0.20 |
| Jamesbond-v5 | 496.08 ± 24.60 | 536.50 ± 82.33 |
| Kangaroo-v5 | 6582.12 ± 5395.44 | 5325.33 ± 3464.80 |
| Krull-v5 | 9718.09 ± 649.15 | 8737.10 ± 294.58 |
| KungFuMaster-v5 | 26000.25 ± 1965.22 | 30451.67 ± 5515.45 |
| MontezumaRevenge-v5 | 0.08 ± 0.12 | 1.00 ± 1.41 |
| MsPacman-v5 | 2345.67 ± 185.94 | 2152.83 ± 152.80 |
| NameThisGame-v5 | 5750.00 ± 181.32 | 6815.63 ± 1098.95 |
| Phoenix-v5 | 14474.11 ± 1794.83 | 9517.73 ± 1176.62 |
| Pitfall-v5 | 0.00 ± 0.00 | -0.76 ± 0.55 |
| Pong-v5 | 20.39 ± 0.24 | 20.45 ± 0.81 |
| PrivateEye-v5 | 100.00 ± 0.00 | 31.83 ± 43.74 |
| Qbert-v5 | 17246.27 ± 605.40 | 15228.25 ± 920.95 |
| Riverraid-v5 | 8275.25 ± 256.63 | 9023.57 ± 1386.85 |
| RoadRunner-v5 | 33040.38 ± 16488.95 | 40125.33 ± 7249.13 |
| Robotank-v5 | 14.43 ± 4.98 | 16.45 ± 3.37 |
| Seaquest-v5 | 1240.30 ± 419.36 | 1518.33 ± 400.35 |
| Skiing-v5 | -18483.46 ± 8684.71 | -22978.48 ± 9894.25 |
| Solaris-v5 | 2198.36 ± 147.23 | 2365.33 ± 157.75 |
| SpaceInvaders-v5 | 1188.82 ± 80.52 | 1019.75 ± 49.08 |
| StarGunner-v5 | 43519.12 ± 4709.23 | 44457.67 ± 3031.86 |
| Surround-v5 | -2.58 ± 2.31 | -4.97 ± 0.99 |
| Tennis-v5 | -17.64 ± 4.60 | -16.44 ± 1.46 |
| TimePilot-v5 | 6476.46 ± 993.30 | 6346.67 ± 663.31 |
| Tutankham-v5 | 249.05 ± 16.56 | 190.73 ± 12.00 |
| UpNDown-v5 | 487495.41 ± 39751.49 | 156143.70 ± 70620.88 |
| Venture-v5 | 0.00 ± 0.00 | 109.33 ± 61.57 |
| VideoPinball-v5 | 43133.94 ± 6362.12 | 53121.26 ± 2580.70 |
| WizardOfWor-v5 | 6353.58 ± 116.59 | 5346.33 ± 277.11 |
| YarsRevenge-v5 | 55757.68 ± 7467.49 | 9394.97 ± 2743.74 |
| Zaxxon-v5 | 3689.67 ± 2477.25 | 5532.67 ± 2607.65 |
Learning curves:
| benchmark/ppo_plot.sh | |
|---|---|
1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 |
|
Info
Note the original openai/baselines uses atari-py==0.2.6
which hangs on gym.make("DefenderNoFrameskip-v4")
and does not support SurroundNoFrameskip-v4 (see issue [ openai/atari-py#73](https://github.com/openai/atari-py/issues/73)). To get results on these environments, we use gym==0.23.1 ale-py==0.7.4 "AutoROM[accept-rom-license]==0.4.2
and [manually register SurroundNoFrameskip-v4 in our fork](https://github.com/vwxyzjn/baselines/blob/e2cb1c938a62fa8d7fe98187246cde08dfd57bd1/baselines/common/register_all_atari_envs.py#L2).
Median Human Normalized Score (HNS) compared to SEEDRL's R2D2 (data available [here](https://github.com/google-research/seed_rl/blob/66e8890261f09d0355e8bf5f1c5e41968ca9f02b/docs/seed_r2d2_atari_graphs.csv)).
Info
Note the SEEDRL's R2D2's median HNS data does not include learning curves for Defender
and Surround
(see [google-research/seed_rl#78](https://github.com/google-research/seed_rl/issues/78)). Also note the SEEDRL's R2D2 uses slightly different Atari preprocessing than our ppo_atari_envpool_xla_jax.py
, so we may be comparing apples and oranges; however, the results are still informative at the scale of 57 Atari games — we would be at least comparing similar apples.
Tracked experiments and game play videos:
ppo_atari_envpool_xla_jax_scan.py
The [ppo_atari_envpool_xla_jax_scan.py](https://github.com/vwxyzjn/cleanrl/blob/master/cleanrl/ppo_atari_envpool_xla_jax_scan.py) has the following features:
- Replaces python loops in
compute_gae
,update_ppo
, androllout
functions of[ppo_atari_envpool_xla_jax.py](/rl-algorithms/ppo/#ppo_atari_envpool_xla_jaxpy)with nativejax.scan
- Warnings and caveats from
[ppo_atari_envpool_xla_jax.py](/rl-algorithms/ppo/#ppo_atari_envpool_xla_jaxpy)also apply here
Usage
uv pip install ".[envpool, jax]"
uv pip install --upgrade "jax[cuda11_cudnn82]==0.4.8" -f https://storage.googleapis.com/jax-releases/jax_cuda_releases.html
uv run python cleanrl/ppo_atari_envpool_xla_jax_scan.py --help
uv run python cleanrl/ppo_atari_envpool_xla_jax_scan.py --env-id Breakout-v5
pip install -r requirements/requirements-envpool.txt
pip install -r requirements/requirements-jax.txt
pip install --upgrade "jax[cuda]==0.3.17" -f https://storage.googleapis.com/jax-releases/jax_cuda_releases.html
python cleanrl/ppo_atari_envpool_xla_jax_scan.py --help
python cleanrl/ppo_atari_envpool_xla_jax_scan.py --env-id Breakout-v5
Explanation of the logged metrics
See [related docs](/rl-algorithms/ppo/#explanation-of-the-logged-metrics) for ppo.py
. The metrics are the same as those in [ppo_atari_envpool_xla_jax.py](https://github.com/vwxyzjn/cleanrl/blob/master/cleanrl/ppo_atari_envpool_xla_jax.py).
Implementation details
[ppo_atari_envpool_xla_jax_scan.py](https://github.com/vwxyzjn/cleanrl/blob/master/cleanrl/ppo_atari_envpool_xla_jax_scan.py) is a clone of [ppo_atari_envpool_xla_jax.py](https://github.com/vwxyzjn/cleanrl/blob/master/cleanrl/ppo_atari_envpool_xla_jax.py) that replaces the python loops with native jax.scan
.
Experiment results
To run benchmark experiments, see [benchmark/ppo.sh](https://github.com/vwxyzjn/cleanrl/blob/master/benchmark/ppo.sh). Specifically, execute the following command:
| benchmark/ppo.sh | |
|---|---|
1 2 3 4 5 6 |
|
| openrlbenchmark/cleanrl/ppo_atari_envpool_xla_jax ({'tag': ['pr-424']}) | openrlbenchmark/cleanrl/ppo_atari_envpool_xla_jax_scan ({'tag': ['pr-424']}) | |
|---|---|---|
| Pong-v5 | 20.82 ± 0.21 | 20.52 ± 0.32 |
| BeamRider-v5 | 2678.73 ± 426.42 | 2860.61 ± 801.30 |
| Breakout-v5 | 420.92 ± 16.75 | 423.90 ± 5.49 |
Learning curves:
| benchmark/ppo_plot.sh | |
|---|---|
1 2 3 4 5 6 7 8 9 10 |
|
Learning curves:
Info
The training time of this variant and that of [ppo_atari_envpool_xla_jax.py](https://github.com/vwxyzjn/cleanrl/blob/master/cleanrl/ppo_atari_envpool_xla_jax.py) are very similar but the compilation time is reduced significantly (see [vwxyzjn/cleanrl#328](https://github.com/vwxyzjn/cleanrl/pull/328#issuecomment-1340474894)). Note that the hardware also affects the speed in the learning curve below. Runs from [ costa-huang](https://github.com/vwxyzjn/) (red) are slower from those of
[(blue and orange) because of hardware differences.](https://github.com/51616/)
51616
Tracked experiments:
ppo_procgen.py
The [ppo_procgen.py](https://github.com/vwxyzjn/cleanrl/blob/master/cleanrl/ppo_procgen.py) has the following features:
- For the procgen environments
- Uses IMPALA-style neural network
- Works with the
Discrete
action space
Usage
uv pip install ".[procgen]"
uv run python cleanrl/ppo_procgen.py --help
uv run python cleanrl/ppo_procgen.py --env-id starpilot
pip install -r requirements/requirements-procgen.txt
python cleanrl/ppo_procgen.py --help
python cleanrl/ppo_procgen.py --env-id starpilot
Explanation of the logged metrics
See [related docs](/rl-algorithms/ppo/#explanation-of-the-logged-metrics) for ppo.py
.
Implementation details
[ppo_procgen.py](https://github.com/vwxyzjn/cleanrl/blob/master/cleanrl/ppo_procgen.py) is based on the details in "Appendix" in [The 37 Implementation Details of Proximal Policy Optimization](https://iclr-blog-track.github.io/2022/03/25/ppo-implementation-details/), which are as follows:
- IMPALA-style Neural Network (
[common/models.py#L28](https://github.com/openai/baselines/blob/ea25b9e8b234e6ee1bca43083f8f3cf974143998/baselines/common/models.py#L28)) - Use the same
gamma
parameter in theNormalizeReward
wrapper. Note that the original implementation from[openai/train-procgen](https://github.com/openai/train-procgen)uses the defaultgamma=0.99
in[the](https://github.com/openai/train-procgen/blob/1a2ae2194a61f76a733a39339530401c024c3ad8/train_procgen/train.py#L43)butVecNormalize
wrappergamma=0.999
as PPO's parameter. The mismatch between thegamma
s is technically incorrect. See[#209](https://github.com/vwxyzjn/cleanrl/pull/209)
Experiment results
To run benchmark experiments, see [benchmark/ppo.sh](https://github.com/vwxyzjn/cleanrl/blob/master/benchmark/ppo.sh). Specifically, execute the following command:
| benchmark/ppo.sh | |
|---|---|
1 2 3 4 5 6 7 8 9 10 |
|
We try to match the default setting in [openai/train-procgen](https://github.com/openai/train-procgen) except that we use the easy
distribution mode and total_timesteps=25e6
to save compute. Notice [openai/train-procgen](https://github.com/openai/train-procgen) has the following settings:
- Learning rate annealing is turned off by default
- Reward scaling and reward clipping is used
Below are the average episodic returns for ppo_procgen.py
. To ensure the quality of the implementation, we compared the results against openai/baselies
' PPO.
| Environment | ppo_procgen.py |
openai/baselies ' PPO (Huang et al., 2022)
|
|---|---|---|
| StarPilot (easy) | 30.99 ± 1.96 | 33.97 ± 7.86 |
| BossFight (easy) | 8.85 ± 0.33 | 9.35 ± 2.04 |
| BigFish (easy) | 16.46 ± 2.71 | 20.06 ± 5.34 |
Learning curves:
| benchmark/ppo_plot.sh | |
|---|---|
1 2 3 4 5 6 7 8 9 |
|
Info
Note that we have run the procgen experiments using the easy
distribution for reducing the computational cost.
Tracked experiments and game play videos:
ppo_atari_multigpu.py
The [ppo_atari_multigpu.py](https://github.com/vwxyzjn/cleanrl/blob/master/cleanrl/ppo_atari_multigpu.py) leverages data parallelism to speed up training time at no cost of sample efficiency.
ppo_atari_multigpu.py
has the following features:
- Allows the users to use do training leveraging data parallelism
- For playing Atari games. It uses convolutional layers and common atari-based pre-processing techniques.
- Works with the Atari's pixel
Box
observation space of shape(210, 160, 3)
- Works with the
Discrete
action space
Warning
Note that ppo_atari_multigpu.py
does not work in Windows and MacOs . It will error out with NOTE: Redirects are currently not supported in Windows or MacOs.
See [pytorch/pytorch#20380](https://github.com/pytorch/pytorch/issues/20380)
Usage
uv pip install ".[atari]"
uv run python cleanrl/ppo_atari_multigpu.py --help
# `--nproc_per_node=2` specifies how many subprocesses we spawn for training with data parallelism
# note it is possible to run this with a *single GPU*: each process will simply share the same GPU
uv run torchrun --standalone --nnodes=1 --nproc_per_node=2 cleanrl/ppo_atari_multigpu.py --env-id BreakoutNoFrameskip-v4
# by default we use the `gloo` backend, but you can use the `nccl` backend for better multi-GPU performance
uv run torchrun --standalone --nnodes=1 --nproc_per_node=2 cleanrl/ppo_atari_multigpu.py --env-id BreakoutNoFrameskip-v4 --backend nccl
# it is possible to spawn more processes than the amount of GPUs you have via `--device-ids`
# e.g., the command below spawns two processes using GPU 0 and two processes using GPU 1
uv run torchrun --standalone --nnodes=1 --nproc_per_node=2 cleanrl/ppo_atari_multigpu.py --env-id BreakoutNoFrameskip-v4 --device-ids 0 0 1 1
pip install -r requirements/requirements-atari.txt
python cleanrl/ppo_atari_multigpu.py --help
# `--nproc_per_node=2` specifies how many subprocesses we spawn for training with data parallelism
# note it is possible to run this with a *single GPU*: each process will simply share the same GPU
torchrun --standalone --nnodes=1 --nproc_per_node=2 cleanrl/ppo_atari_multigpu.py --env-id BreakoutNoFrameskip-v4
# by default we use the `gloo` backend, but you can use the `nccl` backend for better multi-GPU performance
torchrun --standalone --nnodes=1 --nproc_per_node=2 cleanrl/ppo_atari_multigpu.py --env-id BreakoutNoFrameskip-v4 --backend nccl
# it is possible to spawn more processes than the amount of GPUs you have via `--device-ids`
# e.g., the command below spawns two processes using GPU 0 and two processes using GPU 1
torchrun --standalone --nnodes=1 --nproc_per_node=2 cleanrl/ppo_atari_multigpu.py --env-id BreakoutNoFrameskip-v4 --device-ids 0 0 1 1
Explanation of the logged metrics
See [related docs](/rl-algorithms/ppo/#explanation-of-the-logged-metrics) for ppo.py
.
Implementation details
[ppo_atari_multigpu.py](https://github.com/vwxyzjn/cleanrl/blob/master/cleanrl/ppo_atari_multigpu.py) is based on ppo_atari.py
(see its [related docs](/rl-algorithms/ppo/#implementation-details_1)).
We use [Pytorch's distributed API](https://pytorch.org/tutorials/intermediate/dist_tuto.html) to implement the data parallelism paradigm. The basic idea is that the user can spawn \(N\) processes each running a copy of ppo_atari.py
, holding a copy of the model, stepping the environments, and averaging their gradients together for the backward pass. Here are a few note-worthy implementation details.
- Local versus global parameters: All of the parameters in
ppo_atari.py
are global (such as batch size), but inppo_atari_multigpu.py
we have local parameters as well. Say we runtorchrun --standalone --nnodes=1 --nproc_per_node=2 cleanrl/ppo_atari_multigpu.py --env-id BreakoutNoFrameskip-v4 --local-num-envs=4
; here are how all multi-gpu related parameters are adjusted:- number of environments:
num_envs = local_num_envs * world_size = 4 * 2 = 8
- batch size:
local_batch_size = local_num_envs * num_steps = 4 * 128 = 512
,batch_size = num_envs * num_steps) = 8 * 128 = 1024
- minibatch size:
local_minibatch_size = int(args.local_batch_size // args.num_minibatches) = 512 // 4 = 128
,minibatch_size = int(args.batch_size // args.num_minibatches) = 1024 // 4 = 256
- number of updates:
num_iterations = args.total_timesteps // args.batch_size = 10000000 // 1024 = 9765
- number of environments:
-
Adjust seed per process: we need be very careful with seeding: we could have used the exact same seed for each subprocess. To ensure this does not happen, we do the following
# CRUCIAL: note that we needed to pass a different seed for each data parallelism worker args.seed += local_rank random.seed(args.seed) np.random.seed(args.seed) torch.manual_seed(args.seed - local_rank) torch.backends.cudnn.deterministic = args.torch_deterministic # ... envs = gym.vector.SyncVectorEnv( [make_env(args.env_id, args.seed + i, i, args.capture_video, run_name) for i in range(args.num_envs)] ) assert isinstance(envs.single_action_space, gym.spaces.Discrete), "only discrete action space is supported" agent = Agent(envs).to(device) torch.manual_seed(args.seed) optimizer = optim.Adam(agent.parameters(), lr=args.learning_rate, eps=1e-5)
Notice that we adjust the seed with
args.seed += local_rank
(line 2), wherelocal_rank
is the index of the subprocesses. This ensures we seed packages and envs with uncorrealted seeds. However, we do need to use the sametorch
seed for all process to initialize same weights for theagent
(line 5), after which we can use a different seed fortorch
(line 16). 1. Efficient gradient averaging: PyTorch recommends to average the gradient across the whole world via the following (see[docs](https://pytorch.org/tutorials/intermediate/dist_tuto.html#distributed-training))for param in agent.parameters(): dist.all_reduce(param.grad.data, op=dist.ReduceOp.SUM) param.grad.data /= world_size
However,
[@cswinter](https://github.com/cswinter)introduces a more efficient gradient averaging scheme with proper batching (see[entity-neural-network/incubator#220](https://github.com/entity-neural-network/incubator/pull/220)), which looks like:all_grads_list = [] for param in agent.parameters(): if param.grad is not None: all_grads_list.append(param.grad.view(-1)) all_grads = torch.cat(all_grads_list) dist.all_reduce(all_grads, op=dist.ReduceOp.SUM) offset = 0 for param in agent.parameters(): if param.grad is not None: param.grad.data.copy_( all_grads[offset : offset + param.numel()].view_as(param.grad.data) / world_size ) offset += param.numel()
In our previous empirical testing (see
[vwxyzjn/cleanrl#162](https://github.com/vwxyzjn/cleanrl/pull/162#issuecomment-1107909696)), we have found[@cswinter](https://github.com/cswinter)'s implementation to be faster, hence we adopt it in our implementation.
Experiment results
To run benchmark experiments, see [benchmark/ppo.sh](https://github.com/vwxyzjn/cleanrl/blob/master/benchmark/ppo.sh). Specifically, execute the following command:
| benchmark/ppo.sh | |
|---|---|
1 2 3 4 5 6 |
|
Below are the average episodic returns for ppo_atari_multigpu.py
. To ensure no loss of sample efficiency, we compared the results against ppo_atari.py
.
| openrlbenchmark/cleanrl/ppo_atari_multigpu ({'tag': ['pr-424']}) | openrlbenchmark/cleanrl/ppo_atari ({'tag': ['pr-424']}) | |
|---|---|---|
| PongNoFrameskip-v4 | 20.34 ± 0.43 | 20.36 ± 0.20 |
| BeamRiderNoFrameskip-v4 | 2414.65 ± 643.74 | 1915.93 ± 484.58 |
| BreakoutNoFrameskip-v4 | 414.94 ± 20.60 | 414.66 ± 28.09 |
Learning curves:
| benchmark/ppo_plot.sh | |
|---|---|
1 2 3 4 5 6 7 8 9 10 |
|
Under the same hardware, we see that ppo_atari_multigpu.py
is about 30% faster than ppo_atari.py
with no loss of sample efficiency.
Info
The experiments above is to show correctness -- we show that by aligning the same hyperparameters of ppo_atari.py
and ppo_atari_multigpu.py
, we can achieve the same sample efficiency. However, we can train even faster by simply running a much larger batch size. For example, we can run torchrun --standalone --nnodes=1 --nproc_per_node=8 cleanrl/ppo_atari_multigpu.py --env-id BreakoutNoFrameskip-v4 --local-num-envs=8
, which will run 8 x 8 = 64 environments in parallel and achieve a batch size of 64 x 128 = 8192. This will likely result in a sample efficiency but should increase the wall time efficiency.
Info
Although ppo_atari_multigpu.py
is 30% faster than ppo_atari.py
, ppo_atari_multigpu.py
is still slower than ppo_atari_envpool.py
, as shown below. This comparison really highlights the different kinds of optimization possible.
The purpose of ppo_atari_multigpu.py
is not (yet) to achieve the fastest PPO + Atari example. Rather, its purpose is to rigorously validate data parallelism does provide performance benefits. We could do something like ppo_atari_multigpu_envpool.py
to possibly obtain the fastest PPO + Atari possible, but that is for another day. Note we may need numba
to pin the threads envpool
is using in each subprocess to avoid threads fighting each other and lowering the throughput.
Tracked experiments and game play videos:
ppo_pettingzoo_ma_atari.py
[ppo_pettingzoo_ma_atari.py](https://github.com/vwxyzjn/cleanrl/blob/master/cleanrl/ppo_pettingzoo_ma_atari.py) trains an agent to learn playing Atari games via selfplay. The selfplay environment is implemented as a vectorized environment from [PettingZoo.ml](https://www.pettingzoo.ml/atari). The basic idea is to create vectorized environment \(E\) with num_envs = N
, where \(N\) is the number of players in the game. Say \(N = 2\), then the 0-th sub environment of \(E\) will return the observation for player 0 and 1-th sub environment will return the observation of player 1. Then the two environments takes a batch of 2 actions and execute them for player 0 and player 1, respectively. See "Vectorized architecture" in [The 37 Implementation Details of Proximal Policy Optimization](https://iclr-blog-track.github.io/2022/03/25/ppo-implementation-details/) for more detail.
ppo_pettingzoo_ma_atari.py
has the following features:
- For playing the pettingzoo's multi-agent Atari game.
- Works with the pixel-based observation space
- Works with the
Box
action space
Warning
Note that ppo_pettingzoo_ma_atari.py
does not work in Windows . See [https://pypi.org/project/multi-agent-ale-py/#files](https://pypi.org/project/multi-agent-ale-py/#files)
Usage
uv pip install ".[pettingzoo, atari]"
uv run AutoROM --accept-license
uv run cleanrl/ppo_pettingzoo_ma_atari.py --help
uv run cleanrl/ppo_pettingzoo_ma_atari.py --env-id pong_v3
uv run cleanrl/ppo_pettingzoo_ma_atari.py --env-id surround_v2
pip install -r requirements/requirements-pettingzoo.txt
pip install -r requirements/requirements-atari.txt
AutoROM --accept-license
python cleanrl/ppo_pettingzoo_ma_atari.py --help
python cleanrl/ppo_pettingzoo_ma_atari.py --env-id pong_v3
python cleanrl/ppo_pettingzoo_ma_atari.py --env-id surround_v2
See [https://www.pettingzoo.ml/atari](https://www.pettingzoo.ml/atari) for a full-list of supported environments such as basketball_pong_v3
. Notice pettingzoo sometimes introduces breaking changes, so make sure to install the pinned dependencies via poetry
.
Explanation of the logged metrics
Additionally, it logs the following metrics
charts/episodic_return-player0
: episodic return of the game for player 0charts/episodic_return-player1
: episodic return of the game for player 1charts/episodic_length-player0
: episodic length of the game for player 0charts/episodic_length-player1
: episodic length of the game for player 1
See other logged metrics in the [related docs](/rl-algorithms/ppo/#explanation-of-the-logged-metrics) for ppo.py
.
Implementation details
[ppo_pettingzoo_ma_atari.py](https://github.com/vwxyzjn/cleanrl/blob/master/cleanrl/ppo_pettingzoo_ma_atari.py) is based on ppo_atari.py
(see its [related docs](/rl-algorithms/ppo/#implementation-details_1)).
ppo_pettingzoo_ma_atari.py
additionally has the following implementation details:
-
supersuit
wrappers: uses preprocessing wrappers fromsupersuit
instead of fromstable_baselines3
, which looks like the following. In particular note that thesupersuit
does not offer a wrapper similar toNoopResetEnv
, and that it uses theagent_indicator_v0
to add two channels indicating the which player the agent controls.1. A more detailed note on the-env = gym.make(env_id) -env = NoopResetEnv(env, noop_max=30) -env = MaxAndSkipEnv(env, skip=4) -env = EpisodicLifeEnv(env) -if "FIRE" in env.unwrapped.get_action_meanings(): - env = FireResetEnv(env) -env = ClipRewardEnv(env) -env = gym.wrappers.ResizeObservation(env, (84, 84)) -env = gym.wrappers.GrayScaleObservation(env) -env = gym.wrappers.FrameStack(env, 4) +env = importlib.import_module(f"pettingzoo.atari.{args.env_id}").parallel_env() +env = ss.max_observation_v0(env, 2) +env = ss.frame_skip_v0(env, 4) +env = ss.clip_reward_v0(env, lower_bound=-1, upper_bound=1) +env = ss.color_reduction_v0(env, mode="B") +env = ss.resize_v1(env, x_size=84, y_size=84) +env = ss.frame_stack_v1(env, 4) +env = ss.agent_indicator_v0(env, type_only=False) +env = ss.pettingzoo_env_to_vec_env_v1(env) +envs = ss.concat_vec_envs_v1(env, args.num_envs // 2, num_cpus=0, base_class="gym")
agent_indicator_v0
wrapper: let's dig deeper into howagent_indicator_v0
works. We doprint(envs.reset(), envs.reset().shape)
[ 0., 0., 0., 236., 1, 0.]], [[ 0., 0., 0., 236., 0., 1.], [ 0., 0., 0., 236., 0., 1.], [ 0., 0., 0., 236., 0., 1.], ..., [ 0., 0., 0., 236., 0., 1.], [ 0., 0., 0., 236., 0., 1.], [ 0., 0., 0., 236., 0., 1.]]]]) torch.Size([16, 84, 84, 6])
So the
agent_indicator_v0
adds the last two columns, where[ 0., 0., 0., 236., 1, 0.]]
means this observation is for player 0, and[ 0., 0., 0., 236., 0., 1.]
is for player 1. Notice the observation still has the range of \([0, 255]\) but the agent indicator channel has the range of \([0,1]\), so we need to be careful when dividing the observation by 255. In particular, we would only divide the first four channels by 255 and leave the agent indicator channels untouched as follows:def get_action_and_value(self, x, action=None): x = x.clone() x[:, :, :, [0, 1, 2, 3]] /= 255.0 hidden = self.network(x.permute((0, 3, 1, 2)))
Experiment results
To run benchmark experiments, see [benchmark/ppo.sh](https://github.com/vwxyzjn/cleanrl/blob/master/benchmark/ppo.sh). Specifically, execute the following command:
Info
Note that evaluation is usually tricker in in selfplay environments. The usual episodic return is not a good indicator of the agent's performance in zero-sum games because the episodic return converges to zero. To evaluate the agent's ability, an intuitive approach is to take a look at the videos of the agents playing the game (included below), visually inspect the agent's behavior. The best scheme, however, is rating systems like [Trueskill](https://www.microsoft.com/en-us/research/project/trueskill-ranking-system/) or [ELO scores](https://en.wikipedia.org/wiki/Elo_rating_system). However, they are more difficult to implement and are outside the scode of ppo_pettingzoo_ma_atari.py
.
For simplicity, we measure the episodic length instead, which in a sense measures how many "back and forth" the agent can create. In other words, the longer the agent can play the game, the better the agent can play. Empirically, we have found episodic length to be a good indicator of the agent's skill, especially in pong_v3
and surround_v2
. However, it is not the case for tennis_v3
and we'd need to visually inspect the agents' game play videos.
Below are the average episodic length for ppo_pettingzoo_ma_atari.py
. To ensure no loss of sample efficiency, we compared the results against ppo_atari.py
.
| Environment | ppo_pettingzoo_ma_atari.py |
|---|---|
| pong_v3 | 4153.60 ± 190.80 |
| surround_v2 | 3055.33 ± 223.68 |
| tennis_v3 | 14538.02 ± 7005.54 |
Learning curves:
Tracked experiments and game play videos:
ppo_continuous_action_isaacgym.py
Warning
ppo_continuous_action_isaacgym.py
is temporarily deprecated. Please checkout the code in [https://github.com/vwxyzjn/cleanrl/releases/tag/v1.0.0](https://github.com/vwxyzjn/cleanrl/releases/tag/v1.0.0)
The [ppo_continuous_action_isaacgym.py](https://github.com/vwxyzjn/cleanrl/blob/master/cleanrl/ppo_continuous_action_isaacgym/ppo_continuous_action_isaacgym.py) has the following features:
- Works with IsaacGymEnvs.
- Works with the
Box
observation space of low-level features - Works with the
Box
(continuous) action space
[IsaacGymEnvs](https://github.com/NVIDIA-Omniverse/IsaacGymEnvs) is a hardware-accelerated (or GPU-accelerated) robotics simulation environment based on torch
, which allows us to run thousands of simulation environments at the same time, empowering RL agents to learn many MuJoCo-style robotics tasks in minutes instead of hours. When creating an environment with IsaacGymEnvs via isaacgymenvs.make("Ant")
, it creates a vectorized environment which produces GPU tensors as observations and take GPU tensors as actions to execute.
Info
Note that Isaac Gym is the underlying core physics engine, and IssacGymEnvs is a collection of environments built on Isaac Gym.
Info
ppo_continuous_action_isaacgym.py
works with most environments in IsaacGymEnvs but it does not work with the following environments yet:
- AnymalTerrain
- FrankaCabinet
- ShadowHandOpenAI_FF
- ShadowHandOpenAI_LSTM
- Trifinger
- Ingenuity Quadcopter
🔥 we need contributors to work on supporting and tuning our PPO implementation in these envs. If you are interested, please read our [contribution guide](https://github.com/vwxyzjn/cleanrl/blob/master/CONTRIBUTING.md) and reach out!
Usage
The installation of isaacgym
requires a bit of work since it's not a standard Python package.
Please go to [https://developer.nvidia.com/isaac-gym](https://developer.nvidia.com/isaac-gym) to download and install the latest version of Issac Gym which should look like IsaacGym_Preview_4_Package.tar.gz
. Put this IsaacGym_Preview_4_Package.tar.gz
into the ~/Downloads/
folder. Make sure your python version is either 3.7, or 3.8 (3.9 not supported yet).
# extract and move the content in `python` folder in the IsaacGym_Preview_4_Package.tar.gz
# into the `cleanrl/ppo_continuous_action_isaacgym/isaacgym/` folder
cp ~/Downloads/IsaacGym_Preview_4_Package.tar.gz IsaacGym_Preview_4_Package.tar.gz
stat IsaacGym_Preview_4_Package.tar.gz
mkdir temp_isaacgym
tar -xf IsaacGym_Preview_4_Package.tar.gz -C temp_isaacgym
mv temp_isaacgym/isaacgym/python/* cleanrl/ppo_continuous_action_isaacgym/isaacgym
rm -rf temp_isaacgym
# if your global python version is not either 3.7 nor 3.8, you need to tell poetry specifically to use a 3.7 or 3.8 python
# e.g., `poetry env use /home/costa/.pyenv/versions/3.7.8/bin/python`
poetry install --with isaacgym
# if you are using NVIDIA's 30xx GPU, you need to specifically install cuda 11.3 wheels
# `uv pip install torch --upgrade --extra-index-url https://download.pytorch.org/whl/cu113`
uv run python cleanrl/ppo_continuous_action_isaacgym/ppo_continuous_action_isaacgym.py --help
uv run python cleanrl/ppo_continuous_action_isaacgym/ppo_continuous_action_isaacgym.py --env-id Ant
Warning
If you encounter the following installation error
Python.h: No such file or directory
#include <Python.h>
or
libpython3.8.so.1.0: cannot open shared object file: No such file or directory
It usually means your python distribution does not include the shared library files. If you are ubuntu, you can install the following packages:
sudo apt-get install libpython3.8-dev # or sudo apt-get install libpython3.7-dev
If you are using [pyenv](https://github.com/pyenv/pyenv), you may try the following:
env PYTHON_CONFIGURE_OPTS="--enable-shared" pyenv install 3.7.8
Explanation of the logged metrics
See [related docs](/rl-algorithms/ppo/#explanation-of-the-logged-metrics) for ppo.py
.
Additionally, charts/consecutive_successes
means the number of consecutive episodes that the agent has successfully manipulating the rubix cube to the desired state.
Implementation details
[ppo_continuous_action_isaacgym.py](https://github.com/vwxyzjn/cleanrl/blob/master/cleanrl/ppo_continuous_action_isaacgym/ppo_continuous_action_isaacgym.py) is based on ppo_continuous_action.py
(see related [docs](/rl-algorithms/ppo/#ppo_continuous_actionpy)), with a few modifications:
- Different set of hyperparameters:
ppo_continuous_action_isaacgym.py
uses hyperparameters primarily derived from[rl-games](https://github.com/Denys88/rl_games)' configuration (see[example](https://github.com/NVIDIA-Omniverse/IsaacGymEnvs/blob/main/isaacgymenvs/cfg/train/AntPPO.yaml)). The basic spirit is to run moretotal_timesteps
, with largernum_envs
and smallernum_steps
.
| arguments | ppo_continuous_action.py |
ppo_continuous_action_isaacgym.py |
ppo_continuous_action_isaacgym.py (for ShadowHand and AllegroHand ) |
|---|---|---|---|
| --total-timesteps | 1000000 | 30000000 | 600000000 |
| --learning-rate | 3e-4 | 0.0026 | 0.0026 |
| --num-envs | 1 | 4096 | 8192 |
| --num-steps | 2048 | 16 | 8 |
| --anneal-lr | True | False | False |
| --num-minibatches | 32 | 2 | 4 |
| --update-epochs | 10 | 4 | 5 |
| --clip-vloss | True | False | False |
| --vf-coef | 0.5 | 2 | 2 |
| --max-grad-norm | 0.5 | 1 | 1 |
| --reward-scaler | N/A | 1 | 0.01 |
- Slightly larger NN:
ppo_continuous_action.py
uses the following NN:whileself.critic = nn.Sequential( layer_init(nn.Linear(np.array(envs.single_observation_space.shape).prod(), 64)), nn.Tanh(), layer_init(nn.Linear(64, 64)), nn.Tanh(), layer_init(nn.Linear(64, 1), std=1.0), ) self.actor_mean = nn.Sequential( layer_init(nn.Linear(np.array(envs.single_observation_space.shape).prod(), 64)), nn.Tanh(), layer_init(nn.Linear(64, 64)), nn.Tanh(), layer_init(nn.Linear(64, np.prod(envs.single_action_space.shape)), std=0.01), )
ppo_continuous_action_isaacgym.py
uses the following NN:self.critic = nn.Sequential( layer_init(nn.Linear(np.array(envs.single_observation_space.shape).prod(), 256)), nn.Tanh(), layer_init(nn.Linear(256, 256)), nn.Tanh(), layer_init(nn.Linear(256, 1), std=1.0), ) self.actor_mean = nn.Sequential( layer_init(nn.Linear(np.array(envs.single_observation_space.shape).prod(), 256)), nn.Tanh(), layer_init(nn.Linear(256, 256)), nn.Tanh(), layer_init(nn.Linear(256, np.prod(envs.single_action_space.shape)), std=0.01), )
- No normalization and clipping:
ppo_continuous_action_isaacgym.py
does not do observation and reward normalization and clipping for simplicity. It does however optionally offer an option to scale the rewards via--reward-scaler x
, which multiplies all the rewards obtained byx
as an example. - Remove all CPU-related code:
ppo_continuous_action_isaacgym.py
needs to remove all CPU-related code (e.g.action.cpu().numpy()
). This is because almost everything in IsaacGymEnvs happens in GPU. To do this, the major modifications include the following: - Create a custom
RecordEpisodeStatisticsTorch
wrapper that records statstics using GPU tensors instead ofnumpy
arrays. - Avoid transferring the tensors to CPU. The related code in
ppo_continuous_action.py
looks likeand the related code innext_obs, reward, done, info = envs.step(action.cpu().numpy()) rewards[step] = torch.tensor(reward).to(device).view(-1) next_obs, next_done = torch.Tensor(next_obs).to(device), torch.Tensor(done).to(device)
ppo_continuous_action_isaacgym.py
looks likenext_obs, rewards[step], next_done, info = envs.step(action)
Experiment results
To run benchmark experiments, see [benchmark/ppo.sh](https://github.com/vwxyzjn/cleanrl/blob/master/benchmark/ppo.sh). Specifically, execute the following command:
Below are the average episodic returns for ppo_continuous_action_isaacgym.py
. To ensure the quality of the implementation, we compared the results against [Denys88/rl_games](https://github.com/Denys88/rl_games)' PPO and present the training time (units being s (seconds), m (minutes)
). The hardware used is a NVIDIA RTX A6000 in a 24 core machine.
| Environment (training time) | ppo_continuous_action_isaacgym.py |
|
|---|
Learning curves:
Info
Note ppo_continuous_action_isaacgym.py
's performance seems poor compared to [Denys88/rl_games](https://github.com/Denys88/rl_games)' PPO. This is likely due to a few reasons.
[Denys88/rl_games](https://github.com/Denys88/rl_games)' PPO uses different sets of tuned hyperparameters and neural network architecture configuration for different tasks, whereasppo_continuous_action_isaacgym.py
only uses one neural network architecture and 2 set of hyperparameters (ignoring--total-timesteps
).ppo_continuous_action_isaacgym.py
does not use observation normalization (because in my preliminary testing for some reasons it did not help).
While it should be possible to obtain higher scores with more tuning, the purpose of ppo_continuous_action_isaacgym.py
is to hit a balance between simplicity and performance. I think ppo_continuous_action_isaacgym.py
has relatively good performance with a concise codebase, which should be easy to modify and extend for practitioners.
Tracked experiments and game play videos:
Old Learning curves w/ Isaac Gym Preview 3 (no longer available in Nvidia's website for download):
Info
Note the AllegroHand
and ShadowHand
experiments used the following command ppo_continuous_action_isaacgym.py --track --capture_video --num-envs 16384 --num-steps 8 --update-epochs 5 --reward-scaler 0.01 --total-timesteps 600000000 --record-video-step-frequency 3660
. Costa: I was able to run this during my internship at NVIDIA, but in my home setup, the computer has less GPU memory which makes it hard to replicate the results w/ --num-envs 16384
.
-
Huang, Shengyi; Dossa, Rousslan Fernand Julien; Raffin, Antonin; Kanervisto, Anssi; Wang, Weixun (2022). The 37 Implementation Details of Proximal Policy Optimization. ICLR 2022 Blog Track https://iclr-blog-track.github.io/2022/03/25/ppo-implementation-details/
[↩](#fnref:1)[↩](#fnref2:1)[↩](#fnref3:1)[↩](#fnref4:1) -
Andrychowicz, Marcin, Anton Raichuk, Piotr Stańczyk, Manu Orsini, Sertan Girgin, Raphael Marinier, Léonard Hussenot et al. "What matters in on-policy reinforcement learning? a large-scale empirical study." International Conference on Learning Representations 2021, https://openreview.net/forum?id=nIAxjsniDzg
[↩](#fnref:2)