# Source: https://discuss.huggingface.co/t/negative-kl-values-during-ppo-training-trl-library/84143
# Title: Negative KL values during PPO training (TRL library) - Hugging Face Forums
# Fetched via: jina
# Date: 2026-04-09

Title: Negative Kl values during PPO training (TRL library) - 🤗Transformers - Hugging Face Forums



# Negative Kl values during PPO training (TRL library) - 🤗Transformers - Hugging Face Forums



Log In
*    ​ 

*   [Topics](https://discuss.huggingface.co/latest "All topics")
*    More 

 Categories 

*   [Beginners](https://discuss.huggingface.co/c/beginners/5 "Use this category for any basic question you have on any of the Hugging Face  library. Don’t moderate yourself, everyone has to begin somewhere and everyone on this forum is here to help!")
*   [Intermediate](https://discuss.huggingface.co/c/intermediate/6 "Use this category for any advanced question you have on any of the Hugging Face  library or to share/coordinate with other users your projects using them.")
*   [Course](https://discuss.huggingface.co/c/course/20 "Use this category to ask any question related to the course or organize study groups.")
*   [Research](https://discuss.huggingface.co/c/research/7 "Use this category for any research question or to coordinate on a project with other users.")
*   [Models](https://discuss.huggingface.co/c/models/13 "Use this category for any question specific to a given model: questions not really related to the library per se and more research-like such as tips to fine-tune/train, where to use/not to use etc.")
*   [All categories](https://discuss.huggingface.co/categories)

 ​ 

 ​ 

You can login using your [huggingface.co](https://huggingface.co/) credentials.

This forum is powered by [Discourse](https://www.discourse.org/) and relies on a [trust-level system](https://blog.discourse.org/2018/06/understanding-discourse-trust-levels/). As a new user, you’re temporarily limited in the number of topics and posts you can create. To lift those restrictions, just spend time reading other posts (to be precise, enter 5 topics, read through 30 posts and spend a total of 10 minutes reading).

Start with reading [this post](https://discuss.huggingface.co/t/how-to-ask-questions-on-the-forum/54). Then maybe someone already had that error that is bugging you check with a quick [search](https://discuss.huggingface.co/search). Or you can read the latest [awesome paper](http://discuss.huggingface.co/c/research/awesome-paper/) the team discussed.

# [Negative Kl values during PPO training (TRL library)](https://discuss.huggingface.co/t/negative-kl-values-during-ppo-training-trl-library/84143)

[🤗Transformers](https://discuss.huggingface.co/c/transformers/9)

You have selected **0** posts.

[select all](https://discuss.huggingface.co/t/negative-kl-values-during-ppo-training-trl-library/84143)

[cancel selecting](https://discuss.huggingface.co/t/negative-kl-values-during-ppo-training-trl-library/84143)

## post by naviiiid on Apr 28, 2024

[![Image 3](https://avatars.discourse-cdn.com/v4/letter/n/4bbf92/48.png)](https://discuss.huggingface.co/u/naviiiid)

[naviiiid](https://discuss.huggingface.co/u/naviiiid)

1

[Apr 2024](https://discuss.huggingface.co/t/negative-kl-values-during-ppo-training-trl-library/84143 "Post date")

Hey everyone!

 I am trying to train my model using PPO trainer from TRL library. However I receive negative kl values. any Idea where might have gone wrong?

 The configs:

 generation_kwargs = {

 “do_sample”:True,

 “top_k”:9,

 “max_length”:1024,

 “top_p”:0.9,

 }

dataset = train_dataset

ppo_config = {“mini_batch_size”: 1,

 “batch_size”: 1,

 “learning_rate”: 1.41e-5,

 }

 ppo_trainer = PPOTrainer(config, model, tokenizer = tokenizer, dataset = dataset)

 ​ 

 ​ 

394 views 

Reply

### Related topics

Topic list, column headers with buttons are sortable.| Topic | Replies | Views | Activity |
| --- | --- | --- | --- |
| [Unstable PPO training: Highly negative KL divergence and highly positive average ratio of batch on LLMs](https://discuss.huggingface.co/t/unstable-ppo-training-highly-negative-kl-divergence-and-highly-positive-average-ratio-of-batch-on-llms/114220) [🤗Transformers](https://discuss.huggingface.co/c/transformers/9) | [0](https://discuss.huggingface.co/t/unstable-ppo-training-highly-negative-kl-divergence-and-highly-positive-average-ratio-of-batch-on-llms/114220/1) | 418 | [Oct 2024](https://discuss.huggingface.co/t/unstable-ppo-training-highly-negative-kl-divergence-and-highly-positive-average-ratio-of-batch-on-llms/114220/1) |
| [How do I fix this error when training in TRL with QLora and PPO?](https://discuss.huggingface.co/t/how-do-i-fix-this-error-when-training-in-trl-with-qlora-and-ppo/81614) [Intermediate](https://discuss.huggingface.co/c/intermediate/6) | [0](https://discuss.huggingface.co/t/how-do-i-fix-this-error-when-training-in-trl-with-qlora-and-ppo/81614/1) | 483 | [Apr 2024](https://discuss.huggingface.co/t/how-do-i-fix-this-error-when-training-in-trl-with-qlora-and-ppo/81614/1) |
| [PPOTrainer: Output generated during training different than that during inference](https://discuss.huggingface.co/t/ppotrainer-output-generated-during-training-different-than-that-during-inference/70703) [🤗Transformers](https://discuss.huggingface.co/c/transformers/9) | [1](https://discuss.huggingface.co/t/ppotrainer-output-generated-during-training-different-than-that-during-inference/70703/1) | 485 | [Jan 2024](https://discuss.huggingface.co/t/ppotrainer-output-generated-during-training-different-than-that-during-inference/70703/2) |
| [Negative KL-divergence RLHF implementation](https://discuss.huggingface.co/t/negative-kl-divergence-rlhf-implementation/53275) [Intermediate](https://discuss.huggingface.co/c/intermediate/6) | [1](https://discuss.huggingface.co/t/negative-kl-divergence-rlhf-implementation/53275/1) | 1.6k | [May 2024](https://discuss.huggingface.co/t/negative-kl-divergence-rlhf-implementation/53275/2) |
| [Finetune Llama with PPOTrainer](https://discuss.huggingface.co/t/finetune-llama-with-ppotrainer/47671) [🤗Transformers](https://discuss.huggingface.co/c/transformers/9) | [2](https://discuss.huggingface.co/t/finetune-llama-with-ppotrainer/47671/1) | 952 | [Sep 2023](https://discuss.huggingface.co/t/finetune-llama-with-ppotrainer/47671/3) |

 Invalid date  Invalid date