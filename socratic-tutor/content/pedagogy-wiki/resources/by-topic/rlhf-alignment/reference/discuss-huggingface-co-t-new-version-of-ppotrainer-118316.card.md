# Source: https://discuss.huggingface.co/t/new-version-of-ppotrainer/118316
# Title: New Version of PPOTrainer - Hugging Face Forums
# Fetched via: trafilatura
# Date: 2026-04-09

mrin
November 13, 2024, 9:23am
1
Hi, I’m trying to create a PPO loop for the Gemma2b model, I have already trained my reward model.
In the new class of PPOTrainer - policy, ref_policy and reward_model have type ‘module’ unlike the previous version of PPOTrainer.
Now when I’m passing the huggingFace model as policy,ref_policy and my trained reward model, I’m getting the following error -
what to pass in policy, ref_policy and reward model ?
2 Likes
This is the only example I could find…
---
title: "Putting RL back in RLHF"
thumbnail: /blog/assets/putting_rl_back_in_rlhf_with_rloo/thumbnail.png
authors:
- user: vwxyzjn
- user: ArashAhmadian
org: CohereForAI
guest: true
---
# Putting RL back in RLHF
We are excited to introduce the RLOO (REINFORCE Leave One-Out) Trainer in TRL. As an alternative to PPO, RLOO is a new online RLHF training algorithm designed to be more accessible and easier to implement. In particular, **RLOO requires less GPU memory and takes less wall time to converge.** As shown in the figures below:
1. 🤑RLOO uses **approximately 50-70% less** vRAM than PPO, depending on the model size
2. 🚀RLOO runs **2x faster** than PPO with 1B models and up to **3x faster** than PPO with 6.9B models.
3. 🔥RLOO performs **competitively to PPO** in terms of the response win rate (judged by GPT4) and consistently outperforms popular offline methods like DPO.
With RLOO, we bring Reinforcement Learning back into RLHF, enabling the community to explore online RL methods more easily. This is exciting because more and more studies have shown that online RL is more effective than offline methods such as DPO ([https://arxiv.org/abs/2402.04792](https://arxiv.org/abs/2402.04792), [https://arxiv.org/abs/2405.08448](https://arxiv.org/abs/2405.08448)).
This file has been truncated. show original
mrin
November 14, 2024, 4:24am
3
but…I can’t understand how to pass huggingface Pretrained wrapper model as module in policy,ref_policy and reward…could you please help me ?
1 Like
I have no idea, too. But maybe this?
from transformers import (
AutoModelForCausalLM,
AutoModelForSequenceClassification,
AutoTokenizer,
)
from trl.trainer.rloo_trainer import RLOOConfig, RLOOTrainer
from trl.trainer.utils import SIMPLE_QUERY_CHAT_TEMPLATE
base_model_name = "EleutherAI/pythia-1b-deduped"
tokenizer = AutoTokenizer.from_pretrained(base_model_name, padding_side="left")
tokenizer.add_special_tokens({"pad_token": "[PAD]"})
if tokenizer.chat_template is None:
tokenizer.chat_template = SIMPLE_QUERY_CHAT_TEMPLATE
reward_model = AutoModelForSequenceClassification.from_pretrained(base_model_name, num_labels=1)
ref_policy = AutoModelForCausalLM.from_pretrained(base_model_name)
policy = AutoModelForCausalLM.from_pretrained(base_model_name)
train_dataset = ... # make sure to have columns "input_ids"
eval_dataset = ...
trainer = RLOOTrainer(
config=RLOOConfig(
per_device_train_batch_size=1,
gradient_accumulation_steps=64,
total_episodes=30000,
),
tokenizer=tokenizer,
policy=policy,
ref_policy=ref_policy,
reward_model=reward_model,
train_dataset=train_dataset,
eval_dataset=eval_dataset,
)
trainer.train()
mrin
November 14, 2024, 8:07am
5
is it like DPOTrainer…I mean here we no need to write PPO training loop like we do in DPO ?
1 Like
You might be able to write it, but unlike DPOTrainer, PPOTrainer has a default value for the reward model path, so it seems to work without specifying any special options.
However, there is so little documentation that it’s really hard to understand…
reward_model_path (str
, optional , defaults to "EleutherAI/pythia-160m"
) — Path to the reward model.
Hi! I’m also trying to write my own training loop for the PPOTrainer. The new version doesn’t even seem to have a ‘generate’ function to get the policy rollouts. If anyone has been able to find a workaround, that would be really helpful.
1 Like