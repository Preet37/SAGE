# Source: https://lilianweng.github.io/posts/2023-01-17-rlhf/
# Author: Lilian Weng
# Author Slug: lilian-weng
# Fetched via: search fallback (Perplexity)
# Downloaded: 2026-04-06
# Words: 1946
Reinforcement Learning from Human Feedback (RLHF) is a popular technique used to align AI systems with human preferences by training them using feedback from people, rather than relying solely on predefined reward functions. Instead of coding every desirable behavior manually (which is often infeasible in complex tasks) RLHF allows models, especially large language models (LLMs), to learn from examples of what humans consider good or bad outputs.
This approach is particularly important for tasks where success is subjective or hard to quantify, such as generating helpful and safe text responses. RLHF has become a cornerstone in building more aligned and controllable AI systems, making it essential for developing AI that behaves in ways humans intend.
This blog dives into the full training pipeline of the RLHF framework. We will explore every stage — from data generation and reward model inference, to the final training of an LLM. Our goal is to ensure that everything is fully reproducible by providing all the necessary code and the exact specifications of the environments used. By the end of this post, you should know the general pipeline to train any model with any instruction dataset using the RLHF algorithm of your choice!

…

- **Dataset:** UltraFeedback, a well-curated dataset consisting of general chat prompts. (While UltraFeedback also contains LLM-generated responses to the prompts, we won’t be using these.)
- **Base Model:** Llama-3-8B-it, a state-of-the-art instruction-tuned LLM. This is the model we will fine-tune.
- **Reward Model:** Armo, a robust reward model optimized for evaluating the generated outputs. We will use Armo to assign scalar reward values to candidate responses, indicating how “good” or “aligned” a response is.
- **Training Algorithm:** REBEL, a state-of-the-art algorithm tailored for efficient RLHF optimization.

…

We use two separate environments for different stages of the pipeline:

- `vllm`: Handles data generation, leveraging the efficient vllm library.
- `rebel`: Used for training the RLHF model.

You can install both environments using the provided YAML files:

…

## Part 1: Data Generation

The first step in the RLHF pipeline is generating samples from the policy to receive feedback on. Concretely, in this section, we will load the base model using `vllm` for fast inference, prepare the dataset, and generate multiple responses for each prompt in the dataset. The complete code for this part is available here.

…

First, load the base model and tokenizer using `vllm`:
```
from transformers import AutoTokenizer
from vllm import LLM
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Meta-Llama-3-8B-Instruct")
llm = LLM(
    model="meta-llama/Meta-Llama-3-8B-Instruct",
    tensor_parallel_size=8,
)
```
Here, `tensor_parallel_size` specifies the number of GPUs to use.

Next, load the UltraFeedback dataset:
```
from datasets import load_dataset
dataset = load_dataset("allenai/ultrafeedback_binarized_cleaned_train", split='train')
```

…

Alternatively, you can split the dataset into chunks using `dataset.shard` for implementations like SPPO where each iteration only trains on one of the chunks.

Now, let’s prepare the dataset for generation. The Llama model uses special tokens to distinguish prompts and responses. For example:

…

```
def get_message(instruction):
    message = [
        {"role": "user", "content": instruction},
    ]
    return message
prompts = [tokenizer.apply_chat_template(get_message(row['prompt']), tokenize=False, add_generation_prompt=True) for row in dataset]
```
- `get_message` transforms the plain-text prompt into a dictionary indicating it is from the user.
- `tokenizer.apply_chat_template` adds the required special tokens and appends the response tokens (<|start_header_id|>assistant<|end_header_id|>\n\n} at the end with `add_generation_prompt=True`.
Finally, we can generate the responses using `vllm` with the prompts we just formatted. We are going to generate 5 responses per prompt:
```
import torch
import random
import numpy as np
from vllm import SamplingParams

def set_seed(seed=5775709):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)

for p in range(5):
    set_seed(p * 50)
    sampling_params = SamplingParams(
        temperature=0.8,
        top_p=0.9,
        max_tokens=2048,
        seed=p * 50,
    )
    response = llm.generate(prompts, sampling_params)
    output = list(map(lambda x: x.outputs[0].text, response))
    dataset = dataset.add_column(f"response_{p}", output)
```
- `temperature=0.8, top_p=0.9` are common settings to control diversity in generation.
- `set_seed` is used to ensure reproducibility and sets a different seed for each response.
- `llm.generate` generates the response, and the results are added to the dataset with `dataset.add_column`.

…

## Part 2: Reward Model Inference

The second step in the RLHF pipeline is querying the reward model to tell us how good a generated sample was. Concretely, in this part, we will calculate reward scores for the responses generated in Part 1 what are later used for training. The complete code for this part is available here.

Activate the `rebel` environment:

…

```
def get_message(instruction, response):
    return [{"role": "user", "content": instruction}, {"role": "assistant", "content": response}]

rewards = {}
for i in range(5):
    rewards[f"response_{i}_reward"] = []
    for row in dataset:
        reward = rm(get_message(row['prompt'], row[f'response_{i}']))
        rewards[f"response_{i}_reward"].append(reward)
for k, v in rewards.items():
    dataset = dataset.add_column(k, v)
```
- `get_message` formats the user prompt and assistant response into a list of dictionaries.
- `rm` computes a reward score for each response in the dataset.

You can run the complete scipt with:

…

## Part 3: Filter and Tokenize

While the preceding two parts are all we need in theory to do RLHF, it is often advisable in practice to perform a filtering process to ensure training runs smoothly. Concretely, in this part, we’ll walk through the process of preparing a dataset for training by filtering excessively long prompts and responses to prevent out-of-memory (OOM) issues, selecting the best and worst responses for training, and removing duplicate responses. The complete code for this part is available here.

…

These two different tokenizers allow us to pad the prompt from left and the response from the right such that they meet in the middle. By combining left-padded prompts with right-padded responses, we ensure that:

- Prompts and responses meet at a consistent position.
- Relative position embeddings remain correct for model training.

…

Note that we skip the first five tokens of responses when counting lengths to exclude special tokens (e.g. <|begin_of_text|><|start_header_id|>assistant<|end_header_id|>\n\n) and only count the actual length of the response plus the EOS token (<|eot_id|>) at the end.

…

```
llama_prompt_tokens = []
for row in dataset:
    llama_prompt_token = tokenizer_left.apply_chat_template(
            get_message(row['prompt']),
            add_generation_prompt=True,
            tokenize=True,
            padding='max_length',
            max_length=1024,
    )
    assert len(llama_prompt_token) == 1024
    assert (llama_prompt_token[0] == 128000 or llama_prompt_token[0] == 128256) and llama_prompt_token[-1] == 271
    llama_prompt_tokens.append(llama_prompt_token)
dataset = dataset.add_column("llama_prompt_tokens", llama_prompt_tokens)
```
The assertions are used to ensure that the length is always 1,024 and the tokenized prompt either starts with `[pad]` token or `<|begin_of_text|>` token and ends with `\n\n` token.

Then, we select the responses with the highest and lowest rewards for each prompt as the chosen and reject responses, and tokenize them with right padding:
```
chosen, reject, llama_chosen_tokens, llama_reject_tokens, chosen_reward, reject_reward = [], [], [], [], [], []

for row in dataset:

    all_rewards = [row[f"response_{i}_reward"] for i in range(5)]
    chosen_idx, reject_idx = np.argmax(all_rewards), np.argmin(all_rewards)

    chosen.append(row[f"response_{chosen_idx}"])
    reject.append(row[f"response_{reject_idx}"])

    llama_chosen_token = tokenizer.apply_chat_template(
            get_message(response=row[f"response_{chosen_idx}"]),
            add_generation_prompt=False,
            tokenize=True,
            padding='max_length',
            max_length=2048+5,
    )[5:]
    llama_chosen_tokens.append(llama_chosen_token)
    chosen_reward.append(row[f"response_{chosen_idx}_reward"])
    assert len(llama_chosen_token) == 2048
    assert llama_chosen_token[-1] == 128009 or llama_chosen_token[-1] == 128256

    llama_reject_token = tokenizer.apply_chat_template(
            get_message(response=row[f"response_{reject_idx}"]),
            add_generation_prompt=False,
            tokenize=True,
            padding='max_length',
            max_length=2048+5,
    )[5:]
    llama_reject_tokens.append(llama_reject_token)
    reject_reward.append(row[f"response_{reject_idx}_reward"])
    assert len(llama_reject_token) == 2048
    assert llama_reject_token[-1] == 128009 or llama_reject_token[-1] == 128256

dataset = dataset.add_column("chosen", chosen)
dataset = dataset.add_column("chosen_reward", chosen_reward)
dataset = dataset.add_column("llama_chosen_tokens", llama_chosen_tokens)
dataset = dataset.add_column("reject", reject)
dataset = dataset.add_column("reject_reward", reject_reward)
dataset = dataset.add_column("llama_reject_tokens", llama_reject_tokens)
```
Again the assertions are used to ensure that the lengths of the tokenized responses are always 2,048 and the tokenized responses either end with `[pad]` token or `<|eot_id|>` token.

Finally, we filter out rows where the chosen and reject responses are the same:

…

## Part 4: Training with REBEL

Finally, we’re now ready to update the parameters of our model using an RLHF algorithm! We will now use our curated dataset and the REBEL algorithm to fine-tune our base model.

…

In this tutorial, we demonstrate a single iteration of REBEL (\(t=0\)) using the base model \(\pi_{\theta_0}\). For multi-iteration training, you can repeat Parts 1 through 4, initializing each iteration with the model trained in the previous iteration.

The complete code for this part is available here. To enable full parameter training using 8 GPUs, we use the Accelerate library with Deepspeed Stage 3 by running:

…

- `args.world_size` is the number of GPUs we are using.
- `args.local_batch_size` is the batch size for each GPU.
- `args.batch_size` is the actual batch size for training.
- `args.rebel.num_updates` is the total number of updates to perform and `args.total_episodes` is the number of data points to train for. Typically, we set `args.total_episodes` to be the size of the training set for one epoch.

…

```
tokenizer = AutoTokenizer.from_pretrained(
                args.base_model,
                padding_side='right',
                trust_remote_code=True,
            )
tokenizer.add_special_tokens({"pad_token": "[PAD]"})
policy = AutoModelForCausalLM.from_pretrained(
            args.base_model,
            trust_remote_code=True,
            torch_dtype=torch.bfloat16,
            attn_implementation="flash_attention_2",
        )
disable_dropout_in_model(policy)
```

…

```
output = policy(
    input_ids=input_ids,
    attention_mask=attention_mask,
    return_dict=True,
    output_hidden_states=True,
)
logits = output.logits[:, args.task.maxlen_prompt - 1 : -1]
logits /= args.task.temperature + 1e-7
all_logprobs = F.log_softmax(logits, dim=-1)
logprobs = torch.gather(all_logprobs, 2, input_ids[:, args.task.maxlen_prompt:].unsqueeze(-1)).squeeze(-1)
logprobs = (logprobs * seq_mask).sum(-1)
```
- `output.logits` contains the logits of all tokens in the vocabulary for the sequence of `input_ids`.
- `output.logits[:, args.task.maxlen_prompt - 1 : -1]` is the logits of all tokens in the vocabulary for the sequence of response only. It is shifted by 1 since the logits at position \(p\) are referring to the logits at position \(p+1\).

…

## Takeaway

In this post, we outlined the pipeline for implementing RLHF, covering the entire process from data generation to the actual training phase. While we focused specifically on the REBEL algorithm, this pipeline is versatile and can be readily adapted to other methods such as DPO or SimPO. The necessary components for these methods are already included except for the specific loss formulation. There’s also a natural extension of the above pipeline to *multi-turn* RLHF where we optimize for performance over an entire conversation (rather than a single generation) — check out our follow-up paper here for more information!

Basics
Nathan Lambert
13 August 2024
Abstract
Reinforcement learning from human feedback (RLHF) has become an
important technical and storytelling tool to the deploy of the lastest ma-
chine learning systems.
In this book, we hope to give a gentle introduction
to the core methods for people with some level of quantitative background.
The book starts with the origins of RLHF – both in recent literature and
in a convergence of disparate fields of science in economics, philosophy,
and optimal control.
We then set the stage with definitions, problem for-
mulation, data collection, and other common math used in the literature.
We detail the detail the popular algorithms and future frontiers of RLHF.
Contents
1
...
Now, we pass all
...
⋯
𝑟𝑀,𝑁
...
⎦
Each reward 𝑟𝑖,𝑗is computed by passing the completion 𝑦𝑖,𝑗and its correspond-
ing prompt 𝑥𝑖through a reward model ℛ:
𝑟𝑖,𝑗= ℛ(𝑦𝑖,𝑗|𝑥𝑖)
7
…
𝑗
𝑟𝑀,𝑗]
This function 𝑆returns a vector of indices, where each index corresponds to the
column with the maximum reward for each row in 𝑅.
We can then use these
indices to select our chosen completions:
…
This 𝑅𝑓𝑙𝑎𝑡vector has length 𝑀× 𝑁, where M is the number of prompts and N
is the number of completions per prompt.
Now, we can define a selection function 𝑆𝐾that selects the indices of the K
…
• Index 0 →prompt 1, completion 1 (reward 0.7)
• Index 19 →prompt 3, completion 4 (reward 0.7)
...
tuning on the current rendition of the model.
More details can be found in
...
tempetures above zero, e.g. between 0.7 and 1.0, with other modifications
to paramters such as top-p or top-k sampling.
...
This

In machine learning, **reinforcement learning from human feedback** (**RLHF**) is a technique to align an intelligent agent with human preferences.
It involves training a reward model to represent preferences, which can then be used to train other models through reinforcement learning.
…
RLHF has applications in various domains in machine learning, including natural language processing tasks such as text summarization and conversational agents, computer vision tasks like text-to-image models, and the developme