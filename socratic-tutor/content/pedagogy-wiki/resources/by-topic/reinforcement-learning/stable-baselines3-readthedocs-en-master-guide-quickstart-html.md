# Source: https://stable-baselines3.readthedocs.io/en/master/guide/quickstart.html
# Downloaded: 2026-04-06
# Words: 156
# Author: Stable Baselines3
# Author Slug: stable-baselines3
Getting Started[](#getting-started)
Note
Stable-Baselines3 (SB3) uses [vectorized environments (VecEnv)](vec_envs.html) internally.
Please read the associated section to learn more about its features and differences compared to a single Gym environment.
Most of the library tries to follow a sklearn-like syntax for the Reinforcement Learning algorithms.
Here is a quick example of how to train and run A2C on a CartPole environment:
import gymnasium as gym
from stable_baselines3 import A2C
env = gym.make("CartPole-v1", render_mode="rgb_array")
model = A2C("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=10_000)
vec_env = model.get_env()
obs = vec_env.reset()
for i in range(1000):
action, _state = model.predict(obs, deterministic=True)
obs, reward, done, info = vec_env.step(action)
vec_env.render("human")
# VecEnv resets automatically
# if done:
# obs = vec_env.reset()
Note
You can find explanations about the logger output and names in the [Logger](../common/logger.html#logger) section.
Or just train a model with a one line if
[the environment is registered in Gymnasium](https://gymnasium.farama.org/tutorials/gymnasium_basics/environment_creation/#registering-envs) and if
the policy is registered:
from stable_baselines3 import A2C
model = A2C("MlpPolicy", "CartPole-v1").learn(10_000)