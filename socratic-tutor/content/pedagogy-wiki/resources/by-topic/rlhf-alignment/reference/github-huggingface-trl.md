# Source: https://github.com/huggingface/trl
# Author: Hugging Face
# Author Slug: hugging-face
# Title: Hugging Face TRL (source code as API reference for PPOTrainer/DPOTrainer defaults)
# Fetched via: trafilatura
# Date: 2026-04-09

TRL v1: We released TRL v1 — a major milestone that marks a real shift in what TRL is. Read the [blog post](https://huggingface.co/blog/trl-v1) to learn more.
TRL is a cutting-edge library designed for post-training foundation models using advanced techniques like Supervised Fine-Tuning (SFT), Group Relative Policy Optimization (GRPO), and Direct Preference Optimization (DPO). Built on top of the [🤗 Transformers](https://github.com/huggingface/transformers) ecosystem, TRL supports a variety of model architectures and modalities, and can be scaled-up across various hardware setups.
-
Trainers: Various fine-tuning methods are easily accessible via trainers like
,SFTTrainer
,GRPOTrainer
,DPOTrainer
and more.RewardTrainer
-
Efficient and scalable:
- Leverages
[🤗 Accelerate](https://github.com/huggingface/accelerate)to scale from single GPU to multi-node clusters using methods like[DDP](https://pytorch.org/tutorials/intermediate/ddp_tutorial.html)and[DeepSpeed](https://github.com/deepspeedai/DeepSpeed). - Full integration with
[🤗 PEFT](https://github.com/huggingface/peft)enables training on large models with modest hardware via quantization and LoRA/QLoRA. - Integrates
[🦥 Unsloth](https://github.com/unslothai/unsloth)for accelerating training using optimized kernels.
- Leverages
-
Command Line Interface (CLI): A simple interface lets you fine-tune with models without needing to write code.
Install the library using pip
:
pip install trl
If you want to use the latest features before an official release, you can install TRL from source:
pip install git+https://github.com/huggingface/trl.git
If you want to use the examples you can clone the repository with the following command:
git clone https://github.com/huggingface/trl.git
For more flexibility and control over training, TRL provides dedicated trainer classes to post-train language models or PEFT adapters on a custom dataset. Each trainer in TRL is a light wrapper around the 🤗 Transformers trainer and natively supports distributed training methods like DDP, DeepSpeed ZeRO, and FSDP.
Here is a basic example of how to use the [ SFTTrainer](https://huggingface.co/docs/trl/sft_trainer):
from trl import SFTTrainer
from datasets import load_dataset
dataset = load_dataset("trl-lib/Capybara", split="train")
trainer = SFTTrainer(
model="Qwen/Qwen2.5-0.5B",
train_dataset=dataset,
)
trainer.train()
[ GRPOTrainer](https://huggingface.co/docs/trl/grpo_trainer) implements the
[Group Relative Policy Optimization (GRPO) algorithm](https://huggingface.co/papers/2402.03300)that is more memory-efficient than PPO and was used to train
[Deepseek AI's R1](https://huggingface.co/deepseek-ai/DeepSeek-R1).
from datasets import load_dataset
from trl import GRPOTrainer
from trl.rewards import accuracy_reward
dataset = load_dataset("trl-lib/DeepMath-103K", split="train")
trainer = GRPOTrainer(
model="Qwen/Qwen2.5-0.5B-Instruct",
reward_funcs=accuracy_reward,
train_dataset=dataset,
)
trainer.train()
Note
For reasoning models, use the reasoning_accuracy_reward()
function for better results.
[ DPOTrainer](https://huggingface.co/docs/trl/dpo_trainer) implements the popular
[Direct Preference Optimization (DPO) algorithm](https://huggingface.co/papers/2305.18290)that was used to post-train
[Llama 3](https://huggingface.co/papers/2407.21783)and many other models. Here is a basic example of how to use the
DPOTrainer
:from datasets import load_dataset
from trl import DPOTrainer
dataset = load_dataset("trl-lib/ultrafeedback_binarized", split="train")
trainer = DPOTrainer(
model="Qwen3/Qwen-0.6B",
train_dataset=dataset,
)
trainer.train()
Here is a basic example of how to use the [ RewardTrainer](https://huggingface.co/docs/trl/reward_trainer):
from trl import RewardTrainer
from datasets import load_dataset
dataset = load_dataset("trl-lib/ultrafeedback_binarized", split="train")
trainer = RewardTrainer(
model="Qwen/Qwen2.5-0.5B-Instruct",
train_dataset=dataset,
)
trainer.train()
You can use the TRL Command Line Interface (CLI) to quickly get started with post-training methods like Supervised Fine-Tuning (SFT) or Direct Preference Optimization (DPO):
SFT:
trl sft --model_name_or_path Qwen/Qwen2.5-0.5B \
--dataset_name trl-lib/Capybara \
--output_dir Qwen2.5-0.5B-SFT
DPO:
trl dpo --model_name_or_path Qwen/Qwen2.5-0.5B-Instruct \
--dataset_name argilla/Capybara-Preferences \
--output_dir Qwen2.5-0.5B-DPO
Read more about CLI in the [relevant documentation section](https://huggingface.co/docs/trl/clis) or use --help
for more details.
If you want to contribute to trl
or customize it to your needs make sure to read the [contribution guide](https://github.com/huggingface/trl/blob/main/CONTRIBUTING.md) and make sure you make a dev install:
git clone https://github.com/huggingface/trl.git
cd trl/
pip install -e .[dev]
A minimal incubation area is available under trl.experimental
for unstable / fast-evolving features. Anything there may change or be removed in any release without notice.
Example:
from trl.experimental.new_trainer import NewTrainer
Read more in the [Experimental docs](https://huggingface.co/docs/trl/experimental_overview).
@software{vonwerra2020trl,
title = {{TRL: Transformers Reinforcement Learning}},
author = {von Werra, Leandro and Belkada, Younes and Tunstall, Lewis and Beeching, Edward and Thrush, Tristan and Lambert, Nathan and Huang, Shengyi and Rasul, Kashif and Gallouédec, Quentin},
license = {Apache-2.0},
url = {https://github.com/huggingface/trl},
year = {2020}
}
This repository's source code is available under the [Apache-2.0 License](/huggingface/trl/blob/main/LICENSE).