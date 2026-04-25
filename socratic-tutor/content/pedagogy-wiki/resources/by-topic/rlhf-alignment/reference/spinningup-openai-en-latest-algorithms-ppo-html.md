# Source: https://spinningup.openai.com/en/latest/algorithms/ppo.html
# Author: Spinning Up (OpenAI)
# Author Slug: spinning-up
# Title: Proximal Policy Optimization (PPO) — Spinning Up documentation
# Fetched via: trafilatura
# Date: 2026-04-09

[Proximal Policy Optimization](#id3)[¶](#proximal-policy-optimization)
Table of Contents
[Background](#id4)[¶](#background)
(Previously: [Background for TRPO](../algorithms/trpo.html#background))
PPO is motivated by the same question as TRPO: how can we take the biggest possible improvement step on a policy using the data we currently have, without stepping so far that we accidentally cause performance collapse? Where TRPO tries to solve this problem with a complex second-order method, PPO is a family of first-order methods that use a few other tricks to keep new policies close to old. PPO methods are significantly simpler to implement, and empirically seem to perform at least as well as TRPO.
There are two primary variants of PPO: PPO-Penalty and PPO-Clip.
PPO-Penalty approximately solves a KL-constrained update like TRPO, but penalizes the KL-divergence in the objective function instead of making it a hard constraint, and automatically adjusts the penalty coefficient over the course of training so that it’s scaled appropriately.
PPO-Clip doesn’t have a KL-divergence term in the objective and doesn’t have a constraint at all. Instead relies on specialized clipping in the objective function to remove incentives for the new policy to get far from the old policy.
Here, we’ll focus only on PPO-Clip (the primary variant used at OpenAI).
[Quick Facts](#id5)[¶](#quick-facts)
- PPO is an on-policy algorithm.
- PPO can be used for environments with either discrete or continuous action spaces.
- The Spinning Up implementation of PPO supports parallelization with MPI.
[Key Equations](#id6)[¶](#key-equations)
PPO-clip updates policies via
typically taking multiple steps of (usually minibatch) SGD to maximize the objective. Here is given by
in which is a (small) hyperparameter which roughly says how far away the new policy is allowed to go from the old.
This is a pretty complex expression, and it’s hard to tell at first glance what it’s doing, or how it helps keep the new policy close to the old policy. As it turns out, there’s a considerably simplified version [[1]](#id2) of this objective which is a bit easier to grapple with (and is also the version we implement in our code):
where
To figure out what intuition to take away from this, let’s look at a single state-action pair , and think of cases.
Advantage is positive: Suppose the advantage for that state-action pair is positive, in which case its contribution to the objective reduces to
Because the advantage is positive, the objective will increase if the action becomes more likely—that is, if increases. But the min in this term puts a limit to how much the objective can increase. Once , the min kicks in and this term hits a ceiling of . Thus: the new policy does not benefit by going far away from the old policy.
Advantage is negative: Suppose the advantage for that state-action pair is negative, in which case its contribution to the objective reduces to
Because the advantage is negative, the objective will increase if the action becomes less likely—that is, if decreases. But the max in this term puts a limit to how much the objective can increase. Once , the max kicks in and this term hits a ceiling of . Thus, again: the new policy does not benefit by going far away from the old policy.
What we have seen so far is that clipping serves as a regularizer by removing incentives for the policy to change dramatically, and the hyperparameter corresponds to how far away the new policy can go from the old while still profiting the objective.
You Should Know
While this kind of clipping goes a long way towards ensuring reasonable policy updates, it is still possible to end up with a new policy which is too far from the old policy, and there are a bunch of tricks used by different PPO implementations to stave this off. In our implementation here, we use a particularly simple method: early stopping. If the mean KL-divergence of the new policy from the old grows beyond a threshold, we stop taking gradient steps.
When you feel comfortable with the basic math and implementation details, it’s worth checking out other implementations to see how they handle this issue!
|
[this note](https://drive.google.com/file/d/1PDzn9RPvaXjJFZkGeapMHbHGiWWW20Ey/view?usp=sharing)for a derivation of the simplified form of the PPO-Clip objective.[Exploration vs. Exploitation](#id7)[¶](#exploration-vs-exploitation)
PPO trains a stochastic policy in an on-policy way. This means that it explores by sampling actions according to the latest version of its stochastic policy. The amount of randomness in action selection depends on both initial conditions and the training procedure. Over the course of training, the policy typically becomes progressively less random, as the update rule encourages it to exploit rewards that it has already found. This may cause the policy to get trapped in local optima.
[Documentation](#id9)[¶](#documentation)
You Should Know
In what follows, we give documentation for the PyTorch and Tensorflow implementations of PPO in Spinning Up. They have nearly identical function calls and docstrings, except for details relating to model construction. However, we include both full docstrings for completeness.
[Documentation: PyTorch Version](#id10)[¶](#documentation-pytorch-version)
-
spinup.
ppo_pytorch
(env_fn, actor_critic=<MagicMock spec='str' id='140554322637768'>, ac_kwargs={}, seed=0, steps_per_epoch=4000, epochs=50, gamma=0.99, clip_ratio=0.2, pi_lr=0.0003, vf_lr=0.001, train_pi_iters=80, train_v_iters=80, lam=0.97, max_ep_len=1000, target_kl=0.01, logger_kwargs={}, save_freq=10)[¶](#spinup.ppo_pytorch) Proximal Policy Optimization (by clipping),
with early stopping based on approximate KL
Parameters: - env_fn – A function which creates a copy of the environment. The environment must satisfy the OpenAI Gym API.
- actor_critic –
The constructor method for a PyTorch Module with a
step
method, anact
method, api
module, and av
module. Thestep
method should accept a batch of observations and return:Symbol Shape Description a
(batch, act_dim) Numpy array of actions for eachobservation.v
(batch,) Numpy array of value estimatesfor the provided observations.logp_a
(batch,) Numpy array of log probs for theactions ina
.The
act
method behaves the same asstep
but only returnsa
.The
pi
module’s forward call should accept a batch of observations and optionally a batch of actions, and return:Symbol Shape Description pi
N/A Torch Distribution object, containinga batch of distributions describingthe policy for the provided observations.logp_a
(batch,) Optional (only returned if batch ofactions is given). Tensor containingthe log probability, according tothe policy, of the provided actions.If actions not given, will containNone
.The
v
module’s forward call should accept a batch of observations and return:Symbol Shape Description v
(batch,) Tensor containing the value estimatesfor the provided observations. (Critical:make sure to flatten this!) - ac_kwargs (dict) – Any kwargs appropriate for the ActorCritic object you provided to PPO.
- seed (int) – Seed for random number generators.
- steps_per_epoch (int) – Number of steps of interaction (state-action pairs) for the agent and the environment in each epoch.
- epochs (int) – Number of epochs of interaction (equivalent to number of policy updates) to perform.
- gamma (float) – Discount factor. (Always between 0 and 1.)
- clip_ratio (float) – Hyperparameter for clipping in the policy objective. Roughly: how far can the new policy go from the old policy while still profiting (improving the objective function)? The new policy can still go farther than the clip_ratio says, but it doesn’t help on the objective anymore. (Usually small, 0.1 to 0.3.) Typically denoted by .
- pi_lr (float) – Learning rate for policy optimizer.
- vf_lr (float) – Learning rate for value function optimizer.
- train_pi_iters (int) – Maximum number of gradient descent steps to take on policy loss per epoch. (Early stopping may cause optimizer to take fewer than this.)
- train_v_iters (int) – Number of gradient descent steps to take on value function per epoch.
- lam (float) – Lambda for GAE-Lambda. (Always between 0 and 1, close to 1.)
- max_ep_len (int) – Maximum length of trajectory / episode / rollout.
- target_kl (float) – Roughly what KL divergence we think is appropriate between new and old policies after an update. This will get used for early stopping. (Usually small, 0.01 or 0.05.)
- logger_kwargs (dict) – Keyword args for EpochLogger.
- save_freq (int) – How often (in terms of gap between epochs) to save the current policy and value function.
[Saved Model Contents: PyTorch Version](#id11)[¶](#saved-model-contents-pytorch-version)
The PyTorch saved model can be loaded with ac = torch.load('path/to/model.pt')
, yielding an actor-critic object (ac
) that has the properties described in the docstring for ppo_pytorch
.
You can get actions from this model with
actions = ac.act(torch.as_tensor(obs, dtype=torch.float32))
[Documentation: Tensorflow Version](#id12)[¶](#documentation-tensorflow-version)
-
spinup.
ppo_tf1
(env_fn, actor_critic=<function mlp_actor_critic>, ac_kwargs={}, seed=0, steps_per_epoch=4000, epochs=50, gamma=0.99, clip_ratio=0.2, pi_lr=0.0003, vf_lr=0.001, train_pi_iters=80, train_v_iters=80, lam=0.97, max_ep_len=1000, target_kl=0.01, logger_kwargs={}, save_freq=10)[¶](#spinup.ppo_tf1) Proximal Policy Optimization (by clipping),
with early stopping based on approximate KL
Parameters: - env_fn – A function which creates a copy of the environment. The environment must satisfy the OpenAI Gym API.
- actor_critic –
A function which takes in placeholder symbols for state,
x_ph
, and action,a_ph
, and returns the main outputs from the agent’s Tensorflow computation graph:Symbol Shape Description pi
(batch, act_dim) Samples actions from policy givenstates.logp
(batch,) Gives log probability, according tothe policy, of taking actionsa_ph
in statesx_ph
.logp_pi
(batch,) Gives log probability, according tothe policy, of the action sampled bypi
.v
(batch,) Gives the value estimate for statesinx_ph
. (Critical: make sureto flatten this!) - ac_kwargs (dict) – Any kwargs appropriate for the actor_critic function you provided to PPO.
- seed (int) – Seed for random number generators.
- steps_per_epoch (int) – Number of steps of interaction (state-action pairs) for the agent and the environment in each epoch.
- epochs (int) – Number of epochs of interaction (equivalent to number of policy updates) to perform.
- gamma (float) – Discount factor. (Always between 0 and 1.)
- clip_ratio (float) – Hyperparameter for clipping in the policy objective. Roughly: how far can the new policy go from the old policy while still profiting (improving the objective function)? The new policy can still go farther than the clip_ratio says, but it doesn’t help on the objective anymore. (Usually small, 0.1 to 0.3.) Typically denoted by .
- pi_lr (float) – Learning rate for policy optimizer.
- vf_lr (float) – Learning rate for value function optimizer.
- train_pi_iters (int) – Maximum number of gradient descent steps to take on policy loss per epoch. (Early stopping may cause optimizer to take fewer than this.)
- train_v_iters (int) – Number of gradient descent steps to take on value function per epoch.
- lam (float) – Lambda for GAE-Lambda. (Always between 0 and 1, close to 1.)
- max_ep_len (int) – Maximum length of trajectory / episode / rollout.
- target_kl (float) – Roughly what KL divergence we think is appropriate between new and old policies after an update. This will get used for early stopping. (Usually small, 0.01 or 0.05.)
- logger_kwargs (dict) – Keyword args for EpochLogger.
- save_freq (int) – How often (in terms of gap between epochs) to save the current policy and value function.
[Saved Model Contents: Tensorflow Version](#id13)[¶](#saved-model-contents-tensorflow-version)
The computation graph saved by the logger includes:
| Key | Value |
|---|---|
x |
Tensorflow placeholder for state input. |
pi |
Samples an action from the agent, conditioned on states in x . |
v |
Gives value estimate for states in x . |
This saved model can be accessed either by
- running the trained policy with the
[test_policy.py](../user/saving_and_loading.html#loading-and-running-trained-policies)tool, - or loading the whole saved graph into a program with
[restore_tf_graph](../utils/logger.html#spinup.utils.logx.restore_tf_graph).
[References](#id14)[¶](#references)
[Relevant Papers](#id15)[¶](#relevant-papers)
[Proximal Policy Optimization Algorithms](https://arxiv.org/abs/1707.06347), Schulman et al. 2017[High Dimensional Continuous Control Using Generalized Advantage Estimation](https://arxiv.org/abs/1506.02438), Schulman et al. 2016[Emergence of Locomotion Behaviours in Rich Environments](https://arxiv.org/abs/1707.02286), Heess et al. 2017
[Why These Papers?](#id16)[¶](#why-these-papers)
Schulman 2017 is included because it is the original paper describing PPO. Schulman 2016 is included because our implementation of PPO makes use of Generalized Advantage Estimation for computing the policy gradient. Heess 2017 is included because it presents a large-scale empirical analysis of behaviors learned by PPO agents in complex environments (although it uses PPO-penalty instead of PPO-clip).
[Other Public Implementations](#id17)[¶](#other-public-implementations)
[Baselines](https://github.com/openai/baselines/tree/master/baselines/ppo2)[ModularRL](https://github.com/joschu/modular_rl/blob/master/modular_rl/ppo.py)(Caution: this implements PPO-penalty instead of PPO-clip.)[rllab](https://github.com/rll/rllab/blob/master/rllab/algos/ppo.py)(Caution: this implements PPO-penalty instead of PPO-clip.)[rllib (Ray)](https://github.com/ray-project/ray/tree/master/python/ray/rllib/agents/ppo)