# Source: https://huggingface.co/docs/trl/main/en/ppo_trainer
# Author: Hugging Face
# Author Slug: hugging-face
# Title: TRL Documentation: PPOTrainer
# Fetched via: trafilatura
# Date: 2026-04-09

TRL documentation
PPO Trainer
[installation from source](/docs/trl/installation#source). If you'd like regular pip install, checkout the latest stable version (
[v1.0.0](/docs/trl/v1.0.0/ppo_trainer)).
PPO Trainer
TRL supports training LLMs with [Proximal Policy Optimization (PPO)](https://huggingface.co/papers/1707.06347).
References:
[Fine-Tuning Language Models from Human Preferences](https://github.com/openai/lm-human-preferences)[Learning to Summarize from Human Feedback](https://github.com/openai/summarize-from-feedback)[The N Implementation Details of RLHF with PPO](https://huggingface.co/blog/the_n_implementation_details_of_rlhf_with_ppo)[The N+ Implementation Details of RLHF with PPO: A Case Study on TL;DR Summarization](https://huggingface.co/papers/2403.17031)
Get started
To just run a PPO script to make sure the trainer can run, you can run the following command to train a PPO model with a dummy reward model.
python examples/scripts/ppo/ppo.py \ --dataset_name trl-internal-testing/descriptiveness-sentiment-trl-style \ --dataset_train_split descriptiveness \ --learning_rate 3e-6 \ --num_ppo_epochs 1 \ --num_mini_batches 1 \ --output_dir models/minimal/ppo \ --per_device_train_batch_size 64 \ --gradient_accumulation_steps 1 \ --total_episodes 10000 \ --model_name_or_path EleutherAI/pythia-1b-deduped \ --sft_model_path EleutherAI/pythia-1b-deduped \ --reward_model_path EleutherAI/pythia-1b-deduped \ --missing_eos_penalty 1.0
Explanation of the logged metrics
The logged metrics are as follows. Here is an example [tracked run at Weights and Biases](https://wandb.ai/huggingface/trl/runs/dd2o3g35)
eps
: Tracks the number of episodes per second.objective/kl
: The mean Kullback-Leibler (KL) divergence between the current policy and reference policy.objective/entropy
: The mean entropy of the policy, indicating the randomness of the actions chosen by the policy.objective/non_score_reward
: The mean reward from non-score-related sources, basicallybeta * kl.sum(1)
, wherebeta
is the KL penalty coefficient andkl
is the per-token KL divergence.objective/rlhf_reward
: The mean RLHF reward, which isscore - non_score_reward
.objective/scores
: The mean scores returned by the reward model / environment.policy/approxkl_avg
: The average approximate KL divergence between consecutive PPO policies. Note that this is not the same asobjective/kl
.policy/clipfrac_avg
: The average fraction of policy updates that are clipped, indicating how often the policy updates are constrained to prevent large changes.loss/policy_avg
: The average policy loss, indicating how well the policy is performing.loss/value_avg
: The average value loss, indicating the difference between the predicted value and the actual reward.val/clipfrac_avg
: The average fraction of value function updates that are clipped, similar to policy/clipfrac_avg but for the value function.policy/entropy_avg
: The average entropy of the policy during training, indicating how diverse the policy’s actions are.val/ratio
: The mean ratio of the current policy probability to the old policy probability, providing a measure of how much the policy has changed.val/ratio_var
: The variance of theval/ratio
, indicating the variability in policy changes.val/num_eos_tokens
: The number of end-of-sequence (EOS) tokens generated, which can indicate the number of complete responses.lr
: lr: The current learning rate used by the optimizer.episode
: episode: The current episode count in the training process.
Cookbook
- Debugging TIP:
objective/rlhf_reward
: this is the ultimate objective of the RLHF training. If training works as intended, this metric should keep going up. - Debugging TIP:
val/ratio
: this number should float around 1.0, and it gets clipped by--cliprange 0.2
with PPO’s surrogate loss. So if thisratio
is too high like 2.0 or 1000.0 or too small like 0.1, it means the updates between consecutive policies are too drastic. You should try understand why this is happening and try to fix it. - Memory TIP: If you are running out of memory, you can try to reduce the
--per_device_train_batch_size
or increase the--gradient_accumulation_steps
to reduce the memory footprint. - Memory TIP: If you have multiple GPUs, you can also run training with DeepSpeed stage 3 to reduce the memory footprint
accelerate launch --config_file examples/accelerate_configs/deepspeed_zero3.yaml
. - Usage TIP: We recommend to use the “EOS trick” via
--missing_eos_penalty
, which subtracts a static scalar penalty from the score of completions that do not end with an EOS token. This can help the model learn to generate more coherent completions.
What is my model doing exactly?
To help you understand what your model is doing, we periodically log some sample completions from the model. Here is an example of a completion. In an example [tracked run at Weights and Biases](https://wandb.ai/huggingface/trl/runs/dd2o3g35), it looks like the following, allowing you to see the model’s response at different stages of training. By default we generate --num_sample_generations 10
during training, but you can customize the number of generations.
In the logs the sampled generations look like
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┓ ┃ query ┃ model response ┃ score ┃ ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━┩ │ SUBREDDIT: r/AskReddit │ I'm in love with a friend, and │ 3.921875 │ │ │ I don't know how to get rid of │ │ │ TITLE: How do you get someone │ those feelings. I'm │ │ │ out of your head? │ desperate.<|endoftext|>[PAD][P… │ │ │ │ │ │ │ POST: Hi, │ │ │ │ I'm 22, and I have been with my │ │ │ │ girlfriend for 5 years now. We │ │ │ │ recently moved together. We've │ │ │ │ always loved each other │ │ │ │ intensely. │ │ │ │ │ │ │ │ Problem, I recently started to │ │ │ │ have feelings for an other │ │ │ │ person (a friend). This person │ │ │ │ has had a boyfriend for now 3 │ │ │ │ years, and has absolutely no │ │ │ │ ideas. Those feelings were so │ │ │ │ strong, it was hard to hide │ │ │ │ them. After 2 months of me │ │ │ │ being distant and really sad, │ │ │ │ my girlfriend forced me to say │ │ │ │ what was bothering me. I'm not │ │ │ │ a good liar, and now she knows. │ │ │ │ │ │ │ │ We decided to give us a week │ │ │ │ alone, I went to my parents. │ │ │ │ │ │ │ │ Now, I'm completely lost. I │ │ │ │ keep on thinking about this │ │ │ │ person, and I hate that. I │ │ │ │ would like for those feelings │ │ │ │ to go away, to leave me alone. │ │ │ │ But I can't. │ │ │ │ │ │ │ │ What do I do? It's been 3 │ │ │ │ months now, and I'm just │ │ │ │ desperate. │ │ │ │ │ │ │ │ TL;DR: │ │ │ ├─────────────────────────────────┼─────────────────────────────────┼──────────┤ │ SUBREDDIT: r/pettyrevenge │ My mom woke me up with a loud │ 6.84375 │ │ │ TV. I blasted Gangnam Style on │ │ │ TITLE: So, my mom woke me up │ repeat, with the bass cranked │ │ │ with a loud TV. │ up as high as it could │ │ │ │ go.<|endoftext|>[PAD][PAD][PAD… │ │ │ POST: She was in her living │ │ │ │ room, watching TV. This was at │ │ │ │ about 8:30 in the morning, and │ │ │ │ she was exercising. She turned │ │ │ │ the TV up extra loud to hear it │ │ │ │ over her excercycle, and woke │ │ │ │ me up. I went in there asking │ │ │ │ for her to turn it down. She │ │ │ │ said she didn't have to; I │ │ │ │ explained that I always used │ │ │ │ headphones so she didn't have │ │ │ │ to deal with my noise and that │ │ │ │ she should give me a little │ │ │ │ more respect, given that I paid │ │ │ │ rent at the time. │ │ │ │ │ │ │ │ She disagreed. I went back to │ │ │ │ my room, rather pissed off at │ │ │ │ the lack of equality. I had no │ │ │ │ lock on my door; but I had a │ │ │ │ dresser right next to it, so I │ │ │ │ pulled one of the drawers out │ │ │ │ enough so that it caused the │ │ │ │ door to not be openable. Then, │ │ │ │ I turned my speakers up really │ │ │ │ loud and blasted Gangnam Style │ │ │ │ on repeat, with the bass │ │ │ │ cranked up as high as it could │ │ │ │ go. │ │ │ │ │ │ │ │ If you hate Gangnam Style for │ │ │ │ being overplayed, you will see │ │ │ │ why I chose that particular │ │ │ │ song. I personally don't mind │ │ │ │ it. But here's the thing about │ │ │ │ my bass; it vibrates the walls, │ │ │ │ making one hell of a lot of │ │ │ │ noise. Needless to say, my mom │ │ │ │ was not pleased and shut off │ │ │ │ the internet. But it was oh so │ │ │ │ worth it. │ │ │ │ │ │ │ │ TL;DR: │ │ │ └─────────────────────────────────┴─────────────────────────────────┴──────────┘
Implementation details
This PPO implementation is based on the [The N+ Implementation Details of RLHF with PPO: A Case Study on TL;DR Summarization](https://huggingface.co/papers/2403.17031).
Benchmark experiments
To validate the PPO implementation works, we ran experiment on the 1B model. Here are the command we used to run the experiment. We take the SFT / RM models directly from [The N+ Implementation Details of RLHF with PPO: A Case Study on TL;DR Summarization](https://huggingface.co/papers/2403.17031).
accelerate launch --config_file examples/accelerate_configs/deepspeed_zero2.yaml \ examples/scripts/ppo/ppo_tldr.py \ --dataset_name trl-lib/tldr \ --dataset_test_split validation \ --output_dir models/minimal/ppo_tldr \ --learning_rate 3e-6 \ --per_device_train_batch_size 16 \ --gradient_accumulation_steps 4 \ --total_episodes 1000000 \ --model_name_or_path EleutherAI/pythia-1b-deduped \ --sft_model_path cleanrl/EleutherAI_pythia-1b-deduped__sft__tldr \ --reward_model_path cleanrl/EleutherAI_pythia-1b-deduped__reward__tldr \ --local_rollout_forward_batch_size 16 \ --missing_eos_penalty 1.0 \ --stop_token eos \ --eval_strategy steps \ --eval_steps 100
Checkpoints and experiment tracking are available at:
To evaluate, we use [vLLM](https://github.com/vllm-project/vllm) to load the checkpoints and GPT-4o mini as a judge model to evaluate the generated TL;DR against the reference TL;DR.
For more information on how to use judges, see [Judges](judges).
$ python examples/scripts/evals/judge_tldr.py --model_name_or_path cleanrl/EleutherAI_pythia-1b-deduped__sft__tldr --judge_model gpt-4o-mini --num_examples 1000 Model win rate: 33.00% $ python examples/scripts/evals/judge_tldr.py --model_name_or_path trl-lib/ppo_tldr --judge_model gpt-4o-mini --num_examples 1000 Model win rate: 64.70%
The PPO checkpoint gets a 64.7% preferred rate vs the 33.0% preference rate of the SFT checkpoint. This is a good sign that the PPO training is working as intended.
Metrics:
# pip install openrlbenchmark==0.2.1a5
# see https://github.com/openrlbenchmark/openrlbenchmark#get-started for documentation
# to use it, change `?we=huggingface&wpn=trl` to your own project and `?tag=pr-1540` to your own tag
python -m openrlbenchmark.rlops_multi_metrics \
--filters '?we=huggingface&wpn=trl&xaxis=train/episode&ceik=output_dir&cen=sft_model_path&metrics=train/objective/rlhf_reward&metrics=train/objective/scores&metrics=train/objective/kl&metrics=train/objective/non_score_reward&metrics=train/objective/entropy&metrics=train/policy/approxkl_avg&metrics=train/policy/clipfrac_avg&metrics=train/loss/policy_avg&metrics=train/loss/value_avg&metrics=train/val/clipfrac_avg&metrics=train/policy/entropy_avg&metrics=train/val/ratio&metrics=train/val/ratio_var&metrics=train/val/num_eos_tokens&metrics=train/lr&metrics=train/eps' \
"cleanrl/EleutherAI_pythia-1b-deduped__sft__tldr?tag=pr-1540" \
--env-ids models/minimal/ppo_tldr \
--pc.ncols 4 \
--pc.ncols-legend 1 \
--pc.xlabel "Episode" \
--output-filename benchmark/trl/pr-1540/ppo \
--scan-history
PPOTrainer
class trl.experimental.ppo.PPOTrainer
[< source >](https://github.com/huggingface/trl/blob/main/trl/experimental/ppo/ppo_trainer.py#L305)
( args: PPOConfig processing_class: transformers.tokenization_utils_base.PreTrainedTokenizerBase | transformers.image_processing_utils.BaseImageProcessor | transformers.feature_extraction_utils.FeatureExtractionMixin | transformers.processing_utils.ProcessorMixin model: Module ref_model: torch.nn.modules.module.Module | None reward_model: Module train_dataset: Dataset value_model: Module data_collator: transformers.data.data_collator.DataCollatorWithPadding | None = None eval_dataset: datasets.arrow_dataset.Dataset | dict[str, datasets.arrow_dataset.Dataset] | None = None optimizers: tuple = (None, None) callbacks: list[transformers.trainer_callback.TrainerCallback] | None = None peft_config: PeftConfig | None = None )
Parameters
[args (](#trl.experimental.ppo.PPOTrainer.args)[experimental.ppo.PPOConfig](/docs/trl/main/en/ppo_trainer#trl.experimental.ppo.PPOConfig)) — Training arguments.[processing_class (](#trl.experimental.ppo.PPOTrainer.processing_class)[PreTrainedTokenizerBase](https://huggingface.co/docs/transformers/main/en/internal/tokenization_utils#transformers.PreTrainedTokenizerBase),[BaseImageProcessor](https://huggingface.co/docs/transformers/main/en/main_classes/image_processor#transformers.BaseImageProcessor),[FeatureExtractionMixin](https://huggingface.co/docs/transformers/main/en/main_classes/feature_extractor#transformers.FeatureExtractionMixin)or[ProcessorMixin](https://huggingface.co/docs/transformers/main/en/main_classes/processors#transformers.ProcessorMixin)) — Class to process the data.[model (](#trl.experimental.ppo.PPOTrainer.model)torch.nn.Module
) — Model to be trained. This is the policy model.[ref_model (](#trl.experimental.ppo.PPOTrainer.ref_model)torch.nn.Module
, optional) — Reference model used to compute the KL divergence. IfNone
, a copy of the policy model is created.[reward_model (](#trl.experimental.ppo.PPOTrainer.reward_model)torch.nn.Module
) — Reward model used to compute the rewards.[train_dataset (](#trl.experimental.ppo.PPOTrainer.train_dataset)[Dataset](https://huggingface.co/docs/datasets/main/en/package_reference/main_classes#datasets.Dataset)) — Dataset for training.[value_model (](#trl.experimental.ppo.PPOTrainer.value_model)torch.nn.Module
) — Value model used to predict the value of a state.[data_collator (](#trl.experimental.ppo.PPOTrainer.data_collator)[DataCollatorWithPadding](https://huggingface.co/docs/transformers/main/en/main_classes/data_collator#transformers.DataCollatorWithPadding), optional) — Data collator to batch and pad samples from the dataset. IfNone
, a default data collator is created using theprocessing_class
.[eval_dataset (](#trl.experimental.ppo.PPOTrainer.eval_dataset)[Dataset](https://huggingface.co/docs/datasets/main/en/package_reference/main_classes#datasets.Dataset)ordict
of[Dataset](https://huggingface.co/docs/datasets/main/en/package_reference/main_classes#datasets.Dataset), optional) — Dataset for evaluation.[optimizers (](#trl.experimental.ppo.PPOTrainer.optimizers)tuple
oftorch.optim.Optimizer
andtorch.optim.lr_scheduler.LambdaLR
, optional, defaults to(None, None)
) — Tuple containing the optimizer and the learning rate scheduler to use for training. IfNone
, the optimizer and the learning rate scheduler are created using the[create_optimizer_and_scheduler](https://huggingface.co/docs/transformers/main/en/main_classes/trainer#transformers.Trainer.create_optimizer_and_scheduler)method.[callbacks (](#trl.experimental.ppo.PPOTrainer.callbacks)list
of[TrainerCallback](https://huggingface.co/docs/transformers/main/en/main_classes/callback#transformers.TrainerCallback), optional) — Callbacks to use during training.[peft_config (](#trl.experimental.ppo.PPOTrainer.peft_config)[PeftConfig](https://huggingface.co/docs/peft/main/en/package_reference/config#peft.PeftConfig), optional) — PEFT configuration to use PEFT for training. IfNone
, PEFT is not used. If provided, the policymodel
will be wrapped with the specified PEFT adapter.
Trainer for Proximal Policy Optimization (PPO).
For details on PPO, see the paper: [Proximal Policy Optimization
Algorithms](https://huggingface.co/papers/1707.06347).
push_to_hub
[< source >](https://github.com/huggingface/trl/blob/main/transformers/trainer.py#L3992)
( commit_message: str | None = 'End of training' blocking: bool = True token: str | None = None revision: str | None = None **kwargs )
Parameters
[commit_message (](#trl.experimental.ppo.PPOTrainer.push_to_hub.commit_message)str
, optional, defaults to"End of training"
) — Message to commit while pushing.[blocking (](#trl.experimental.ppo.PPOTrainer.push_to_hub.blocking)bool
, optional, defaults toTrue
) — Whether the function should return only when thegit push
has finished.[token (](#trl.experimental.ppo.PPOTrainer.push_to_hub.token)str
, optional, defaults toNone
) — Token with write permission to overwrite Trainer’s original args.[revision (](#trl.experimental.ppo.PPOTrainer.push_to_hub.revision)str
, optional) — The git revision to commit from. Defaults to the head of the “main” branch.[kwargs (](#trl.experimental.ppo.PPOTrainer.push_to_hub.kwargs)dict[str, Any]
, optional) — Additional keyword arguments passed along to~Trainer.create_model_card
.
Upload self.model
and self.processing_class
to the 🤗 model hub on the repo self.args.hub_model_id
.
PPOConfig
class trl.experimental.ppo.PPOConfig
[< source >](https://github.com/huggingface/trl/blob/main/trl/experimental/ppo/ppo_config.py#L22)
( output_dir: str | None = None per_device_train_batch_size: int = 8 num_train_epochs: float = 3.0 max_steps: int = -1 learning_rate: float = 3e-06 lr_scheduler_type: transformers.trainer_utils.SchedulerType | str = 'linear' lr_scheduler_kwargs: dict | str | None = None warmup_steps: float = 0 optim: transformers.training_args.OptimizerNames | str = 'adamw_torch_fused' optim_args: str | None = None weight_decay: float = 0.0 adam_beta1: float = 0.9 adam_beta2: float = 0.999 adam_epsilon: float = 1e-08 optim_target_modules: None | str | list[str] = None gradient_accumulation_steps: int = 1 average_tokens_across_devices: bool = True max_grad_norm: float = 1.0 label_smoothing_factor: float = 0.0 bf16: bool | None = None fp16: bool = False bf16_full_eval: bool = False fp16_full_eval: bool = False tf32: bool | None = None gradient_checkpointing: bool = True gradient_checkpointing_kwargs: dict[str, typing.Any] | str | None = None torch_compile: bool = False torch_compile_backend: str | None = None torch_compile_mode: str | None = None use_liger_kernel: bool = False liger_kernel_config: dict[str, bool] | None = None use_cache: bool = False neftune_noise_alpha: float | None = None torch_empty_cache_steps: int | None = None auto_find_batch_size: bool = False logging_strategy: transformers.trainer_utils.IntervalStrategy | str = 'steps' logging_steps: float = 10 logging_first_step: bool = False log_on_each_node: bool = True logging_nan_inf_filter: bool = True include_num_input_tokens_seen: str | bool = 'no' log_level: str = 'passive' log_level_replica: str = 'warning' disable_tqdm: bool | None = None report_to: None | str | list[str] = 'none' run_name: str | None = None project: str = 'huggingface' trackio_space_id: str | None = 'trackio' eval_strategy: transformers.trainer_utils.IntervalStrategy | str = 'no' eval_steps: float | None = None eval_delay: float = 0 per_device_eval_batch_size: int = 8 prediction_loss_only: bool = False eval_on_start: bool = False eval_do_concat_batches: bool = True eval_use_gather_object: bool = False eval_accumulation_steps: int | None = None include_for_metrics: list = <factory> batch_eval_metrics: bool = False save_only_model: bool = False save_strategy: transformers.trainer_utils.SaveStrategy | str = 'steps' save_steps: float = 500 save_on_each_node: bool = False save_total_limit: int | None = None enable_jit_checkpoint: bool = False push_to_hub: bool = False hub_token: str | None = None hub_private_repo: bool | None = None hub_model_id: str | None = None hub_strategy: transformers.trainer_utils.HubStrategy | str = 'every_save' hub_always_push: bool = False hub_revision: str | None = None load_best_model_at_end: bool = False metric_for_best_model: str | None = None greater_is_better: bool | None = None ignore_data_skip: bool = False restore_callback_states_from_checkpoint: bool = False full_determinism: bool = False seed: int = 42 data_seed: int | None = None use_cpu: bool = False accelerator_config: dict | str | None = None parallelism_config: accelerate.parallelism_config.ParallelismConfig | None = None dataloader_drop_last: bool = False dataloader_num_workers: int = 0 dataloader_pin_memory: bool = True dataloader_persistent_workers: bool = False dataloader_prefetch_factor: int | None = None remove_unused_columns: bool = True label_names: list[str] | None = None train_sampling_strategy: str = 'random' length_column_name: str = 'length' ddp_find_unused_parameters: bool | None = None ddp_bucket_cap_mb: int | None = None ddp_broadcast_buffers: bool | None = None ddp_backend: str | None = None ddp_timeout: int = 1800 fsdp: list[transformers.trainer_utils.FSDPOption] | str | None = None fsdp_config: dict[str, typing.Any] | str | None = None deepspeed: dict | str | None = None debug: str | list[transformers.debug_utils.DebugOption] = '' skip_memory_metrics: bool = True do_train: bool = False do_eval: bool = False do_predict: bool = False resume_from_checkpoint: str | None = None warmup_ratio: float | None = None logging_dir: str | None = None local_rank: int = -1 dataset_num_proc: int | None = None num_mini_batches: int = 1 total_episodes: int | None = None local_rollout_forward_batch_size: int = 64 num_sample_generations: int = 10 response_length: int = 53 stop_token: typing.Optional[typing.Literal['eos']] = None stop_token_id: int | None = None temperature: float = 0.7 missing_eos_penalty: float | None = None sft_model_path: str = 'EleutherAI/pythia-160m' world_size: int | None = None num_total_batches: int | None = None micro_batch_size: int | None = None local_batch_size: int | None = None batch_size: int | None = None local_mini_batch_size: int | None = None mini_batch_size: int | None = None reward_model_path: str = 'EleutherAI/pythia-160m' model_adapter_name: str | None = None ref_adapter_name: str | None = None num_ppo_epochs: int = 4 whiten_rewards: bool = False kl_coef: float = 0.05 kl_estimator: typing.Literal['k1', 'k3'] = 'k1' cliprange: float = 0.2 vf_coef: float = 0.1 cliprange_value: float = 0.2 gamma: float = 1.0 lam: float = 0.95 ds3_gather_for_generation: bool = True )
Parameters
[dataset_num_proc (](#trl.experimental.ppo.PPOConfig.dataset_num_proc)int
, optional) — Number of processes to use for processing the dataset.[num_mini_batches (](#trl.experimental.ppo.PPOConfig.num_mini_batches)int
, optional, defaults to1
) — Number of minibatches to split a batch into.[total_episodes (](#trl.experimental.ppo.PPOConfig.total_episodes)int
, optional) — Total number of episodes in the dataset.[local_rollout_forward_batch_size (](#trl.experimental.ppo.PPOConfig.local_rollout_forward_batch_size)int
, optional, defaults to64
) — Per rank no grad forward pass in the rollout phase.[num_sample_generations (](#trl.experimental.ppo.PPOConfig.num_sample_generations)int
, optional, defaults to10
) — Number of debugging samples generations (i.e.,generate_completions
calls) throughout training.[response_length (](#trl.experimental.ppo.PPOConfig.response_length)int
, optional, defaults to53
) — Length of the response.[stop_token (](#trl.experimental.ppo.PPOConfig.stop_token)str
, optional) — Specifies the stop token to use for text generation. This parameter is mutually exclusive withstop_token_id
.None
: No stop token is applied, unlessstop_token_id
is specified.'eos'
: Uses the tokenizer’seos_token
.
[stop_token_id (](#trl.experimental.ppo.PPOConfig.stop_token_id)int
, optional) — Specifies the ID of the stop token to use for text generation. IfNone
, no stop token ID is applied, unlessstop_token
is specified. This parameter is mutually exclusive withstop_token
.[temperature (](#trl.experimental.ppo.PPOConfig.temperature)float
, optional, defaults to0.7
) — Sampling temperature.[missing_eos_penalty (](#trl.experimental.ppo.PPOConfig.missing_eos_penalty)float
, optional) — Penalty applied to the score when the model fails to generate an EOS token. This is useful to encourage to generate completions shorter than the maximum length (max_new_tokens
). The penalty must be a positive value.[sft_model_path (](#trl.experimental.ppo.PPOConfig.sft_model_path)str
, optional, defaults to"EleutherAI/pythia-160m"
) — Path to the SFT model.[world_size (](#trl.experimental.ppo.PPOConfig.world_size)int
, optional) — Number of processes (GPUs) to use for the training.[num_total_batches (](#trl.experimental.ppo.PPOConfig.num_total_batches)int
, optional) — Number of total batches to train.[micro_batch_size (](#trl.experimental.ppo.PPOConfig.micro_batch_size)int
, optional) — Micro batch size across devices (HF’sper_device_train_batch_size
*world_size
).[local_batch_size (](#trl.experimental.ppo.PPOConfig.local_batch_size)int
, optional) — Batch size per GPU (HF’sper_device_train_batch_size
*gradient_accumulation_steps
).[batch_size (](#trl.experimental.ppo.PPOConfig.batch_size)int
, optional) — Batch size across devices (HF’sper_device_train_batch_size
world_size
gradient_accumulation_steps
).[local_mini_batch_size (](#trl.experimental.ppo.PPOConfig.local_mini_batch_size)int
, optional) — Mini batch size per GPU.[mini_batch_size (](#trl.experimental.ppo.PPOConfig.mini_batch_size)int
, optional) — Mini batch size across GPUs.[push_to_hub (](#trl.experimental.ppo.PPOConfig.push_to_hub)bool
, optional, defaults toFalse
) — Whether to push the model to the Hub after training.[reward_model_path (](#trl.experimental.ppo.PPOConfig.reward_model_path)str
, optional, defaults to"EleutherAI/pythia-160m"
) — Path to the reward model.[model_adapter_name (](#trl.experimental.ppo.PPOConfig.model_adapter_name)str
, optional) — Name of the train target PEFT adapter, when using LoRA with multiple adapters.[ref_adapter_name (](#trl.experimental.ppo.PPOConfig.ref_adapter_name)str
, optional) — Name of the reference PEFT adapter, when using LoRA with multiple adapters.[num_ppo_epochs (](#trl.experimental.ppo.PPOConfig.num_ppo_epochs)int
, optional, defaults to4
) — Number of epochs to train.[whiten_rewards (](#trl.experimental.ppo.PPOConfig.whiten_rewards)bool
, optional, defaults toFalse
) — Whether to whiten the rewards.[kl_coef (](#trl.experimental.ppo.PPOConfig.kl_coef)float
, optional, defaults to0.05
) — KL coefficient.[kl_estimator (](#trl.experimental.ppo.PPOConfig.kl_estimator)Literal["k1", "k3"]
, optional, defaults to"k1"
) — Which estimator for KL-Divergence to use from[Approximating KL Divergence](http://joschu.net/blog/kl-approx.html). Defaults to “k1”, a straightforward, unbiased estimator. Can be set to “k3”, an unbiased estimator with lower variance which “appears to be a strictly better estimator”. Cannot be set to “k2”, as it is used for logging purposes.[cliprange (](#trl.experimental.ppo.PPOConfig.cliprange)float
, optional, defaults to0.2
) — Clip range.[vf_coef (](#trl.experimental.ppo.PPOConfig.vf_coef)float
, optional, defaults to0.1
) — Value function coefficient.[cliprange_value (](#trl.experimental.ppo.PPOConfig.cliprange_value)float
, optional, defaults to0.2
) — Clip range for the value function.[gamma (](#trl.experimental.ppo.PPOConfig.gamma)float
, optional, defaults to1.0
) — Discount factor.[lam (](#trl.experimental.ppo.PPOConfig.lam)float
, optional, defaults to0.95
) — Lambda value for GAE.[ds3_gather_for_generation (](#trl.experimental.ppo.PPOConfig.ds3_gather_for_generation)bool
, optional, defaults toTrue
) — This setting applies to DeepSpeed ZeRO-3. If enabled, the policy model weights are gathered for generation, improving generation speed. However, disabling this option allows training models that exceed the VRAM capacity of a single GPU, albeit at the cost of slower generation.
Configuration class for the [experimental.ppo.PPOTrainer](/docs/trl/main/en/ppo_trainer#trl.experimental.ppo.PPOTrainer).
This class includes only the parameters that are specific to PPO training. For a full list of training arguments,
please refer to the [TrainingArguments](https://huggingface.co/docs/transformers/main/en/main_classes/trainer#transformers.TrainingArguments) documentation. Note that default values in this class may
differ from those in [TrainingArguments](https://huggingface.co/docs/transformers/main/en/main_classes/trainer#transformers.TrainingArguments).
Using [HfArgumentParser](https://huggingface.co/docs/transformers/main/en/internal/trainer_utils#transformers.HfArgumentParser) we can turn this class into
[argparse](https://docs.python.org/3/library/argparse#module-argparse) arguments that can be specified on the
command line.
These parameters have default values different from
[TrainingArguments]:
logging_steps
: Defaults to10
instead of500
.gradient_checkpointing
: Defaults toTrue
instead ofFalse
.bf16
: Defaults toTrue
iffp16
is not set, instead ofFalse
.learning_rate
: Defaults to3e-6
instead of5e-5
.
PreTrainedModelWrapper
class trl.experimental.ppo.PreTrainedModelWrapper
[< source >](https://github.com/huggingface/trl/blob/main/trl/experimental/ppo/modeling_value_head.py#L52)
( pretrained_model = None score_module = None supports_rm_adapter = False rm_adapter_name = None **kwargs )
Parameters
[pretrained_model (](#trl.experimental.ppo.PreTrainedModelWrapper.pretrained_model)[PreTrainedModel](https://huggingface.co/docs/transformers/main/en/main_classes/model#transformers.PreTrainedModel)) — The model to be wrapped.[parent_class (](#trl.experimental.ppo.PreTrainedModelWrapper.parent_class)[PreTrainedModel](https://huggingface.co/docs/transformers/main/en/main_classes/model#transformers.PreTrainedModel)) — The parent class of the model to be wrapped.[supported_args (](#trl.experimental.ppo.PreTrainedModelWrapper.supported_args)list
) — The list of arguments that are supported by the wrapper class.
Wrapper for a [PreTrainedModel](https://huggingface.co/docs/transformers/main/en/main_classes/model#transformers.PreTrainedModel) implemented as a standard PyTorch torch.nn.Module
.
This class provides a compatibility layer that preserves the key attributes and methods of the original
[PreTrainedModel](https://huggingface.co/docs/transformers/main/en/main_classes/model#transformers.PreTrainedModel), while exposing a uniform interface consistent with PyTorch modules. It enables
seamless integration of pretrained Transformer models into custom training, evaluation, or inference workflows.
add_and_load_reward_modeling_adapter
[< source >](https://github.com/huggingface/trl/blob/main/trl/experimental/ppo/modeling_value_head.py#L438)
( pretrained_model adapter_model_id adapter_name = 'reward_model_adapter' token = None )
Add and load a reward modeling adapter. This method can only be used if the model is a PeftModel
and if you
have initialized the model with the reward_modeling_adapter_id
argument, pointing to the id of the reward
modeling adapter. The latest needs also to contain the score head in order to produce the reward.
Computes the reward score for a given input. The method has first to enable the adapter and then compute the reward score. After that the model disables the reward modeling adapter and enables the default ppo adapter again.
from_pretrained
[< source >](https://github.com/huggingface/trl/blob/main/trl/experimental/ppo/modeling_value_head.py#L106)
( pretrained_model_name_or_path *model_args **kwargs )
Parameters
[pretrained_model_name_or_path (](#trl.experimental.ppo.PreTrainedModelWrapper.from_pretrained.pretrained_model_name_or_path)str
or[PreTrainedModel](https://huggingface.co/docs/transformers/main/en/main_classes/model#transformers.PreTrainedModel)) — The path to the pretrained model or its name.[*model_args (](#trl.experimental.ppo.PreTrainedModelWrapper.from_pretrained.*model_args)list
, optional) — Additional positional arguments passed along to the underlying model’sfrom_pretrained
method.[**kwargs (](#trl.experimental.ppo.PreTrainedModelWrapper.from_pretrained.*kwargs)dict
, optional) — Additional keyword arguments passed along to the underlying model’sfrom_pretrained
method. We also pre-process the kwargs to extract the arguments that are specific to the[PreTrainedModel](https://huggingface.co/docs/transformers/main/en/main_classes/model#transformers.PreTrainedModel)class and the arguments that are specific to trl models. The kwargs also supportprepare_model_for_kbit_training
arguments frompeft
library.
Instantiates a new model from a pretrained model from transformers
. The pretrained model is loaded using the
from_pretrained
method of the [PreTrainedModel](https://huggingface.co/docs/transformers/main/en/main_classes/model#transformers.PreTrainedModel) class. The arguments that are specific to the
[PreTrainedModel](https://huggingface.co/docs/transformers/main/en/main_classes/model#transformers.PreTrainedModel) class are passed along this method and filtered out from the kwargs
argument.
Post initialization method. This method is called after the model is instantiated and loaded from a checkpoint. It can be used to perform additional operations such as loading the state_dict.
push_to_hub
[< source >](https://github.com/huggingface/trl/blob/main/trl/experimental/ppo/modeling_value_head.py#L509)
( *args **kwargs )
Push the pretrained model to the hub. This method is a wrapper around
[push_to_hub](https://huggingface.co/docs/transformers/main/en/main_classes/model#transformers.PreTrainedModel.push_to_hub). Please refer to the documentation of
[push_to_hub](https://huggingface.co/docs/transformers/main/en/main_classes/model#transformers.PreTrainedModel.push_to_hub) for more information.
save_pretrained
[< source >](https://github.com/huggingface/trl/blob/main/trl/experimental/ppo/modeling_value_head.py#L523)
( *args **kwargs )
Save the pretrained model to a directory. This method is a wrapper around
[save_pretrained](https://huggingface.co/docs/transformers/main/en/main_classes/model#transformers.PreTrainedModel.save_pretrained). Please refer to the documentation of
[save_pretrained](https://huggingface.co/docs/transformers/main/en/main_classes/model#transformers.PreTrainedModel.save_pretrained) for more information.
Return the state_dict of the pretrained model.
AutoModelForCausalLMWithValueHead
class trl.experimental.ppo.AutoModelForCausalLMWithValueHead
[< source >](https://github.com/huggingface/trl/blob/main/trl/experimental/ppo/modeling_value_head.py#L634)
( pretrained_model **kwargs )
An autoregressive model with a value head in addition to the language model head. This class inherits from
[experimental.ppo.PreTrainedModelWrapper](/docs/trl/main/en/ppo_trainer#trl.experimental.ppo.PreTrainedModelWrapper) and wraps a [PreTrainedModel](https://huggingface.co/docs/transformers/main/en/main_classes/model#transformers.PreTrainedModel) class. The wrapper class
supports classic functions such as from_pretrained
, push_to_hub
and generate
. To call a method of the wrapped
model, simply manipulate the pretrained_model
attribute of this class.
Class attributes:
- transformers_parent_class (
[PreTrainedModel](https://huggingface.co/docs/transformers/main/en/main_classes/model#transformers.PreTrainedModel)) — The parent class of the wrapped model. This should be set totransformers.AutoModelForCausalLM
for this class. - supported_args (
tuple
) — A tuple of strings that are used to identify the arguments that are supported by theValueHead
class. Currently, the supported args are:- summary_dropout_prob (
float
,optional
, defaults toNone
) — The dropout probability for theValueHead
class. - v_head_initializer_range (
float
,optional
, defaults to0.2
) — The initializer range for theValueHead
if a specific initialization strategy is selected. - v_head_init_strategy (
str
,optional
, defaults toNone
) — The initialization strategy for theValueHead
. Currently, the supported strategies are:None
— Initializes the weights of theValueHead
with a random distribution. This is the default strategy.- “normal” — Initializes the weights of the
ValueHead
with a normal distribution.
- summary_dropout_prob (
__init__
[< source >](https://github.com/huggingface/trl/blob/main/trl/experimental/ppo/modeling_value_head.py#L665)
( pretrained_model **kwargs )
Parameters
[pretrained_model (](#trl.experimental.ppo.AutoModelForCausalLMWithValueHead.__init__.pretrained_model)[PreTrainedModel](https://huggingface.co/docs/transformers/main/en/main_classes/model#transformers.PreTrainedModel)) — The model to wrap. It should be a causal language model such as GPT2. or any model mapped inside theAutoModelForCausalLM
class.[kwargs (](#trl.experimental.ppo.AutoModelForCausalLMWithValueHead.__init__.kwargs)dict
,optional
) — Additional keyword arguments, that are passed to theValueHead
class.
Initializes the model.
forward
[< source >](https://github.com/huggingface/trl/blob/main/trl/experimental/ppo/modeling_value_head.py#L703)
( input_ids = None past_key_values = None attention_mask = None return_past_key_values = False **kwargs )
Parameters
[input_ids (torch.LongTensor of shape (batch_size, sequence_length)) — Indices of input sequence tokens in the vocabulary.](#trl.experimental.ppo.AutoModelForCausalLMWithValueHead.forward.input_ids)[past_key_values (tuple(tuple(torch.FloatTensor)), optional) — Contains pre-computed hidden-states (key and values in the attention blocks) as computed by the model (see past_key_values input) to speed up sequential decoding.](#trl.experimental.ppo.AutoModelForCausalLMWithValueHead.forward.past_key_values)[attention_mask (torch.FloatTensor of shape (batch_size, sequence_length), optional) — Mask to avoid performing attention on padding token indices. Mask values selected in](#trl.experimental.ppo.AutoModelForCausalLMWithValueHead.forward.attention_mask)[0, 1]
:- 1 for tokens that are not masked,
- 0 for tokens that are masked.
[return_past_key_values (bool) — A flag indicating if the computed hidden-states should be returned.](#trl.experimental.ppo.AutoModelForCausalLMWithValueHead.forward.return_past_key_values)[kwargs (dict, optional) — Additional keyword arguments, that are passed to the wrapped model.](#trl.experimental.ppo.AutoModelForCausalLMWithValueHead.forward.kwargs)
Applies a forward pass to the wrapped model and returns the logits of the value head.
generate
[< source >](https://github.com/huggingface/trl/blob/main/trl/experimental/ppo/modeling_value_head.py#L758)
( *args **kwargs )
A simple wrapper around the generate
method of the wrapped model. Please refer to the
[ generate](https://huggingface.co/docs/transformers/internal/generation_utils) method of the wrapped model
for more information about the supported arguments.
_init_weights
[< source >](https://github.com/huggingface/trl/blob/main/trl/experimental/ppo/modeling_value_head.py#L681)
( **kwargs )
Initializes the weights of the value head. The default initialization strategy is random. Users can pass a
different initialization strategy by passing the v_head_init_strategy
argument when calling
.from_pretrained
. Supported strategies are:
normal
: initializes the weights with a normal distribution.
AutoModelForSeq2SeqLMWithValueHead
class trl.experimental.ppo.AutoModelForSeq2SeqLMWithValueHead
[< source >](https://github.com/huggingface/trl/blob/main/trl/experimental/ppo/modeling_value_head.py#L838)
( pretrained_model **kwargs )
Parameters
[pretrained_model (](#trl.experimental.ppo.AutoModelForSeq2SeqLMWithValueHead.pretrained_model)[PreTrainedModel](https://huggingface.co/docs/transformers/main/en/main_classes/model#transformers.PreTrainedModel)) — The model to wrap. It should be a causal language model such as GPT2. or any model mapped inside the[AutoModelForSeq2SeqLM](https://huggingface.co/docs/transformers/main/en/model_doc/auto#transformers.AutoModelForSeq2SeqLM)class.[kwargs — Additional keyword arguments passed along to the](#trl.experimental.ppo.AutoModelForSeq2SeqLMWithValueHead.kwargs)ValueHead
class.
A seq2seq model with a value head in addition to the language model head. This class inherits from
[experimental.ppo.PreTrainedModelWrapper](/docs/trl/main/en/ppo_trainer#trl.experimental.ppo.PreTrainedModelWrapper) and wraps a [PreTrainedModel](https://huggingface.co/docs/transformers/main/en/main_classes/model#transformers.PreTrainedModel) class. The wrapper class
supports classic functions such as from_pretrained
and push_to_hub
and also provides some additional
functionalities such as generate
.
forward
[< source >](https://github.com/huggingface/trl/blob/main/trl/experimental/ppo/modeling_value_head.py#L969)
( input_ids = None past_key_values = None attention_mask = None return_past_key_values = False **kwargs )
We call generate
on the wrapped model.
We initialize the weights of the value head.
[Update on GitHub](https://github.com/huggingface/trl/blob/main/docs/source/ppo_trainer.md)