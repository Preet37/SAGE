# Source: https://huggingface.co/docs/trl/main/en/dpo_trainer
# Author: Hugging Face
# Author Slug: hugging-face
# Title: TRL Documentation: DPOTrainer
# Fetched via: trafilatura
# Date: 2026-04-09

TRL documentation
DPO Trainer
[installation from source](/docs/trl/installation#source). If you'd like regular pip install, checkout the latest stable version (
[v1.0.0](/docs/trl/v1.0.0/dpo_trainer)).
DPO Trainer
Overview
TRL supports the Direct Preference Optimization (DPO) Trainer for training language models, as described in the paper [Direct Preference Optimization: Your Language Model is Secretly a Reward Model](https://huggingface.co/papers/2305.18290) by [Rafael Rafailov](https://huggingface.co/rmrafailov), Archit Sharma, Eric Mitchell, [Stefano Ermon](https://huggingface.co/ermonste), [Christopher D. Manning](https://huggingface.co/manning), [Chelsea Finn](https://huggingface.co/cbfinn).
The abstract from the paper is the following:
While large-scale unsupervised language models (LMs) learn broad world knowledge and some reasoning skills, achieving precise control of their behavior is difficult due to the completely unsupervised nature of their training. Existing methods for gaining such steerability collect human labels of the relative quality of model generations and fine-tune the unsupervised LM to align with these preferences, often with reinforcement learning from human feedback (RLHF). However, RLHF is a complex and often unstable procedure, first fitting a reward model that reflects the human preferences, and then fine-tuning the large unsupervised LM using reinforcement learning to maximize this estimated reward without drifting too far from the original model. In this paper we introduce a new parameterization of the reward model in RLHF that enables extraction of the corresponding optimal policy in closed form, allowing us to solve the standard RLHF problem with only a simple classification loss. The resulting algorithm, which we call Direct Preference Optimization (DPO), is stable, performant, and computationally lightweight, eliminating the need for sampling from the LM during fine-tuning or performing significant hyperparameter tuning. Our experiments show that DPO can fine-tune LMs to align with human preferences as well as or better than existing methods. Notably, fine-tuning with DPO exceeds PPO-based RLHF in ability to control sentiment of generations, and matches or improves response quality in summarization and single-turn dialogue while being substantially simpler to implement and train.
This post-training method was contributed by [Kashif Rasul](https://huggingface.co/kashif) and later refactored by [Quentin Gallouédec](https://huggingface.co/qgallouedec).
Quick start
This example demonstrates how to train a language model using the [DPOTrainer](/docs/trl/main/en/bema_for_reference_model#trl.DPOTrainer) from TRL. We train a [Qwen 3 0.6B](https://huggingface.co/Qwen/Qwen3-0.6B) model on the [UltraFeedback dataset](https://huggingface.co/datasets/openbmb/UltraFeedback).
from trl import DPOTrainer
from datasets import load_dataset
trainer = DPOTrainer(
model="Qwen/Qwen3-0.6B",
train_dataset=load_dataset("trl-lib/ultrafeedback_binarized", split="train"),
)
trainer.train()
Expected dataset type and format
DPO requires a [preference](dataset_formats#preference) dataset. The [DPOTrainer](/docs/trl/main/en/bema_for_reference_model#trl.DPOTrainer) is compatible with both [standard](dataset_formats#standard) and [conversational](dataset_formats#conversational) dataset formats. When provided with a conversational dataset, the trainer will automatically apply the chat template to the dataset.
# Standard format
## Explicit prompt (recommended)
preference_example = {"prompt": "The sky is", "chosen": " blue.", "rejected": " green."}
# Implicit prompt
preference_example = {"chosen": "The sky is blue.", "rejected": "The sky is green."}
# Conversational format
## Explicit prompt (recommended)
preference_example = {"prompt": [{"role": "user", "content": "What color is the sky?"}],
"chosen": [{"role": "assistant", "content": "It is blue."}],
"rejected": [{"role": "assistant", "content": "It is green."}]}
## Implicit prompt
preference_example = {"chosen": [{"role": "user", "content": "What color is the sky?"},
{"role": "assistant", "content": "It is blue."}],
"rejected": [{"role": "user", "content": "What color is the sky?"},
{"role": "assistant", "content": "It is green."}]}
If your dataset is not in one of these formats, you can preprocess it to convert it into the expected format. Here is an example with the [Vezora/Code-Preference-Pairs](https://huggingface.co/datasets/Vezora/Code-Preference-Pairs) dataset:
from datasets import load_dataset
dataset = load_dataset("Vezora/Code-Preference-Pairs")
def preprocess_function(example):
return {
"prompt": [{"role": "user", "content": example["input"]}],
"chosen": [{"role": "assistant", "content": example["accepted"]}],
"rejected": [{"role": "assistant", "content": example["rejected"]}],
}
dataset = dataset.map(preprocess_function, remove_columns=["instruction", "input", "accepted", "ID"])
print(next(iter(dataset["train"])))
{
"prompt": [{"role": "user", "content": "Create a nested loop to print every combination of numbers [...]"}],
"chosen": [{"role": "assistant", "content": "Here is an example of a nested loop in Python [...]"}],
"rejected": [{"role": "assistant", "content": "Here is an example of a nested loop in Python [...]"}],
}
Looking deeper into the DPO method
Direct Preference Optimization (DPO) is a training method designed to align a language model with preference data. Instead of supervised input–output pairs, the model is trained on pairs of completions to the same prompt, where one completion is preferred over the other. The objective directly optimizes the model to widen the margin between the log-likelihoods of preferred and dispreferred completions, relative to a reference model, without requiring an explicit reward model. In practice, this is typically achieved by suppressing the likelihood of dispreferred completions rather than by increasing the likelihood of preferred ones.
This section breaks down how DPO works in practice, covering the key steps: preprocessing and loss computation.
Preprocessing and tokenization
During training, each example is expected to contain a prompt along with a preferred (chosen
) and a dispreferred (rejected
) completion. For more details on the expected formats, see [Dataset formats](dataset_formats).
The [DPOTrainer](/docs/trl/main/en/bema_for_reference_model#trl.DPOTrainer) tokenizes each input using the model’s tokenizer.
Computing the loss
The loss used in DPO is defined as follows:
where is the prompt, is the preferred completion and is the dispreferred completion. is the policy model being trained, is the reference model, is the sigmoid function, and is a hyperparameter that controls the strength of the preference signal.
Loss Types
Several formulations of the objective have been proposed in the literature. Initially, the objective of DPO was defined as presented above.
loss_type= | Description |
|---|---|
"sigmoid" (default) | Given the preference data, we can fit a binary classifier according to the Bradley-Terry model and in fact the
logsigmoid to fit a logistic regression. |
"hinge"
[RSO](https://huggingface.co/papers/2309.06657)authors propose to use a hinge loss on the normalized likelihood from the[SLiC](https://huggingface.co/papers/2305.10425)paper. In this case, thebeta
is the reciprocal of the margin."ipo"
[IPO](https://huggingface.co/papers/2310.12036)authors argue the logit transform can overfit and propose the identity transform to optimize preferences directly; TRL exposes this asloss_type="ipo"
."exo_pair"
[EXO](https://huggingface.co/papers/2402.00856)authors propose reverse-KL preference optimization.label_smoothing
must be strictly greater than 0.0
; a recommended value is 1e-3
(see Eq. 16 for the simplified pairwise variant). The full method uses K>2
SFT completions and approaches PPO as K
grows."nca_pair"
[NCA](https://huggingface.co/papers/2402.05369)authors shows that NCA optimizes the absolute likelihood for each response rather than the relative likelihood."robust"
[Robust DPO](https://huggingface.co/papers/2403.00409)authors propose an unbiased DPO loss under noisy preferences. Uselabel_smoothing
in [DPOConfig](/docs/trl/main/en/dpo_trainer#trl.DPOConfig)to model label-flip probability; valid values are in the range[0.0, 0.5)
."bco_pair"
[BCO](https://huggingface.co/papers/2404.04656)authors train a binary classifier whose logit serves as a reward so that the classifier maps {prompt, chosen completion} pairs to 1 and {prompt, rejected completion} pairs to 0. For unpaired data, we recommend the dedicated[experimental.bco.BCOTrainer](/docs/trl/main/en/bco_trainer#trl.experimental.bco.BCOTrainer)."sppo_hard"
[SPPO](https://huggingface.co/papers/2405.00675)authors claim that SPPO is capable of solving the Nash equilibrium iteratively by pushing the chosen rewards to be as large as 1/2 and the rejected rewards to be as small as -1/2 and can alleviate data sparsity issues. The implementation approximates this algorithm by employing hard label probabilities, assigning 1 to the winner and 0 to the loser."aot"
or loss_type="aot_unpaired"
[AOT](https://huggingface.co/papers/2406.05882)authors propose Distributional Preference Alignment via Optimal Transport.loss_type="aot"
is for paired data; loss_type="aot_unpaired"
is for unpaired data. Both enforce stochastic dominance via sorted quantiles; larger per-GPU batch sizes help."apo_zero"
or loss_type="apo_down"
[APO](https://huggingface.co/papers/2408.06266)method introduces an anchored objective.apo_zero
boosts winners and downweights losers (useful when the model underperforms the winners). apo_down
downweights both, with stronger pressure on losers (useful when the model already outperforms winners)."discopop"
[DiscoPOP](https://huggingface.co/papers/2406.08414)paper uses LLMs to discover more efficient offline preference optimization losses. In the paper the proposed DiscoPOP loss (which is a log-ratio modulated loss) outperformed other optimization losses on different tasks (IMDb positive text generation, Reddit TLDR summarization, and Alpaca Eval 2.0)."sft"
Logged metrics
While training and evaluating we record the following reward metrics:
global_step
: The total number of optimizer steps taken so far.epoch
: The current epoch number, based on dataset iteration.num_tokens
: The total number of tokens processed so far.loss
: The average cross-entropy loss computed over non-masked tokens in the current logging interval.entropy
: The average entropy of the model’s predicted token distribution over non-masked tokens.mean_token_accuracy
: The proportion of non-masked tokens for which the model’s top-1 prediction matches the token from the chosen completion.learning_rate
: The current learning rate, which may change dynamically if a scheduler is used.grad_norm
: The L2 norm of the gradients, computed before gradient clipping.logits/chosen
: The average logit values assigned by the model to the tokens in the chosen completion.logits/rejected
: The average logit values assigned by the model to the tokens in the rejected completion.logps/chosen
: The average log-probability assigned by the model to the tokens in the chosen completion.logps/rejected
: The average log-probability assigned by the model to the tokens in the rejected completion.rewards/chosen
: The average implicit reward computed for the chosen completion, computed as .rewards/rejected
: The average implicit reward computed for the rejected completion, computed as .rewards/margins
: The average implicit reward margin between the chosen and rejected completions.rewards/accuracies
: The proportion of examples where the implicit reward for the chosen completion is higher than that for the rejected completion.
Customization
Compatibility and constraints
Some argument combinations are intentionally restricted in the current [DPOTrainer](/docs/trl/main/en/bema_for_reference_model#trl.DPOTrainer) implementation:
use_weighting=True
is not supported withloss_type="aot"
orloss_type="aot_unpaired"
.- With
use_liger_kernel=True
:- only a single
loss_type
is supported, compute_metrics
is not supported,precompute_ref_log_probs=True
is not supported.
- only a single
sync_ref_model=True
is not supported when training with PEFT models that do not keep a standaloneref_model
.sync_ref_model=True
cannot be combined withprecompute_ref_log_probs=True
.precompute_ref_log_probs=True
is not supported withIterableDataset
(train or eval).
Multi-loss combinations
The DPO trainer supports combining multiple loss functions with different weights, enabling more sophisticated optimization strategies. This is particularly useful for implementing algorithms like MPO (Mixed Preference Optimization). MPO is a training approach that combines multiple optimization objectives, as described in the paper [Enhancing the Reasoning Ability of Multimodal Large Language Models via Mixed Preference Optimization](https://huggingface.co/papers/2411.10442).
To combine multiple losses, specify the loss types and corresponding weights as lists:
# MPO: Combines DPO (sigmoid) for preference and BCO (bco_pair) for quality
training_args = DPOConfig(
loss_type=["sigmoid", "bco_pair", "sft"], # loss types to combine
loss_weights=[0.8, 0.2, 1.0] # corresponding weights, as used in the MPO paper
)
Model initialization
You can directly pass the kwargs of the from_pretrained()
method to the [DPOConfig](/docs/trl/main/en/dpo_trainer#trl.DPOConfig). For example, if you want to load a model in a different precision, analogous to
model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen3-0.6B", dtype=torch.bfloat16)
you can do so by passing the model_init_kwargs={"dtype": torch.bfloat16}
argument to the [DPOConfig](/docs/trl/main/en/dpo_trainer#trl.DPOConfig).
from trl import DPOConfig
training_args = DPOConfig(
model_init_kwargs={"dtype": torch.bfloat16},
)
Note that all keyword arguments of from_pretrained()
are supported.
Train adapters with PEFT
We support tight integration with 🤗 PEFT library, allowing any user to conveniently train adapters and share them on the Hub, rather than training the entire model.
from datasets import load_dataset
from trl import DPOTrainer
from peft import LoraConfig
dataset = load_dataset("trl-lib/ultrafeedback_binarized", split="train")
trainer = DPOTrainer(
"Qwen/Qwen3-0.6B",
train_dataset=dataset,
peft_config=LoraConfig(),
)
trainer.train()
You can also continue training your [PeftModel](https://huggingface.co/docs/peft/main/en/package_reference/peft_model#peft.PeftModel). For that, first load a PeftModel
outside [DPOTrainer](/docs/trl/main/en/bema_for_reference_model#trl.DPOTrainer) and pass it directly to the trainer without the peft_config
argument being passed.
from datasets import load_dataset
from trl import DPOTrainer
from peft import AutoPeftModelForCausalLM
model = AutoPeftModelForCausalLM.from_pretrained("trl-lib/Qwen3-4B-LoRA", is_trainable=True)
dataset = load_dataset("trl-lib/ultrafeedback_binarized", split="train")
trainer = DPOTrainer(
model=model,
train_dataset=dataset,
)
trainer.train()
When training adapters, you typically use a higher learning rate (≈1e‑5) than full fine-tuning since only new parameters are being learned.
DPOConfig(learning_rate=1e-5, ...)
Train with Liger Kernel
Liger Kernel is a collection of Triton kernels for LLM training that boosts multi-GPU throughput by 20%, cuts memory use by 60% (enabling up to 4× longer context), and works seamlessly with tools like FlashAttention, PyTorch FSDP, and DeepSpeed. For more information, see [Liger Kernel Integration](liger_kernel_integration).
Rapid Experimentation for DPO
RapidFire AI is an open-source experimentation engine that sits on top of TRL and lets you launch multiple DPO configurations at once, even on a single GPU. Instead of trying configurations sequentially, RapidFire lets you see all their learning curves earlier, stop underperforming runs, and clone promising ones with new settings in flight without restarting. For more information, see [RapidFire AI Integration](rapidfire_integration).
Train with Unsloth
Unsloth is an open‑source framework for fine‑tuning and reinforcement learning that trains LLMs (like Llama, Mistral, Gemma, DeepSeek, and more) up to 2× faster with up to 70% less VRAM, while providing a streamlined, Hugging Face–compatible workflow for training, evaluation, and deployment. For more information, see [Unsloth Integration](unsloth_integration).
Tool Calling with DPO
The [DPOTrainer](/docs/trl/main/en/bema_for_reference_model#trl.DPOTrainer) fully supports fine-tuning models with tool calling capabilities. In this case, each dataset example should include:
- The conversation messages (prompt, chosen and rejected), including any tool calls (
tool_calls
) and tool responses (tool
role messages) - The list of available tools in the
tools
column, typically provided as JSON schemas
For details on the expected dataset structure, see the [Dataset Format — Tool Calling](dataset_formats#tool-calling) section.
Training Vision Language Models
[DPOTrainer](/docs/trl/main/en/bema_for_reference_model#trl.DPOTrainer) fully supports training Vision-Language Models (VLMs). To train a VLM, provide a dataset with either an image
column (single image per sample) or an images
column (list of images per sample). For more information on the expected dataset structure, see the [Dataset Format — Vision Dataset](dataset_formats#vision-dataset) section.
An example of such a dataset is the [RLAIF-V Dataset](https://huggingface.co/datasets/HuggingFaceH4/rlaif-v_formatted) dataset.
from trl import DPOConfig, DPOTrainer
from datasets import load_dataset
trainer = DPOTrainer(
model="Qwen/Qwen2.5-VL-3B-Instruct",
args=DPOConfig(max_length=None),
train_dataset=load_dataset("HuggingFaceH4/rlaif-v_formatted", split="train"),
)
trainer.train()
For VLMs, truncating may remove image tokens, leading to errors during training. To avoid this, set
max_length=None
in the[DPOConfig]. This allows the model to process the full sequence length without truncating image tokens.DPOConfig(max_length=None, ...)
Only use
max_length
when you’ve verified that truncation won’t remove image tokens for the entire dataset.
DPOTrainer
class trl.DPOTrainer
[< source >](https://github.com/huggingface/trl/blob/main/trl/trainer/dpo_trainer.py#L406)
( model: str | PreTrainedModel | PeftModel ref_model: transformers.modeling_utils.PreTrainedModel | None = None args: trl.trainer.dpo_config.DPOConfig | None = None data_collator: collections.abc.Callable[[list[typing.Any]], dict[str, typing.Any]] | None = None train_dataset: datasets.arrow_dataset.Dataset | datasets.iterable_dataset.IterableDataset | None = None eval_dataset: datasets.arrow_dataset.Dataset | datasets.iterable_dataset.IterableDataset | dict[str, datasets.arrow_dataset.Dataset | datasets.iterable_dataset.IterableDataset] | None = None processing_class: transformers.tokenization_utils_base.PreTrainedTokenizerBase | transformers.processing_utils.ProcessorMixin | None = None compute_metrics: collections.abc.Callable[[transformers.trainer_utils.EvalPrediction], dict] | None = None callbacks: list[transformers.trainer_callback.TrainerCallback] | None = None optimizers: tuple = (None, None) peft_config: PeftConfig | None = None )
Parameters
[model (](#trl.DPOTrainer.model)str
or[PreTrainedModel](https://huggingface.co/docs/transformers/main/en/main_classes/model#transformers.PreTrainedModel)or[PeftModel](https://huggingface.co/docs/peft/main/en/package_reference/peft_model#peft.PeftModel)) — Model to be trained. Can be either:- A string, being the model id of a pretrained model hosted inside a model repo on huggingface.co, or a
path to a directory containing model weights saved using
[save_pretrained](https://huggingface.co/docs/transformers/main/en/main_classes/model#transformers.PreTrainedModel.save_pretrained), e.g.,'./my_model_directory/'
. The model is loaded using<ModelArchitecture>.from_pretrained
(where<ModelArchitecture>
is derived from the model config) with the keyword arguments inargs.model_init_kwargs
. - A
[PreTrainedModel](https://huggingface.co/docs/transformers/main/en/main_classes/model#transformers.PreTrainedModel)object. Only causal language models are supported. - A
[PeftModel](https://huggingface.co/docs/peft/main/en/package_reference/peft_model#peft.PeftModel)object. Only causal language models are supported.
- A string, being the model id of a pretrained model hosted inside a model repo on huggingface.co, or a
path to a directory containing model weights saved using
[ref_model (](#trl.DPOTrainer.ref_model)PreTrainedModel
, optional) — Reference model used to compute the reference log probabilities.- If provided, this model is used directly as the reference policy.
- If
None
, the trainer will automatically use the initial policy corresponding tomodel
, i.e. the model state before DPO training starts.
[args (](#trl.DPOTrainer.args)[DPOConfig](/docs/trl/main/en/dpo_trainer#trl.DPOConfig), optional) — Configuration for this trainer. IfNone
, a default configuration is used.[data_collator (](#trl.DPOTrainer.data_collator)DataCollator
, optional) — Function to use to form a batch from a list of elements of the processedtrain_dataset
oreval_dataset
. Will default toDataCollatorForPreference
if the model is a language model andDataCollatorForVisionPreference
if the model is a vision-language model. Custom collators must truncate sequences before padding; the trainer does not apply post-collation truncation.[train_dataset (](#trl.DPOTrainer.train_dataset)[Dataset](https://huggingface.co/docs/datasets/main/en/package_reference/main_classes#datasets.Dataset)or[IterableDataset](https://huggingface.co/docs/datasets/main/en/package_reference/main_classes#datasets.IterableDataset)) — Dataset to use for training. This trainer supports both[language modeling](#language-modeling)type and[prompt-completion](#prompt-completion)type. The format of the samples can be either:[Standard](dataset_formats#standard): Each sample contains plain text.[Conversational](dataset_formats#conversational): Each sample contains structured messages (e.g., role and content).
[eval_dataset (](#trl.DPOTrainer.eval_dataset)[Dataset](https://huggingface.co/docs/datasets/main/en/package_reference/main_classes#datasets.Dataset),[IterableDataset](https://huggingface.co/docs/datasets/main/en/package_reference/main_classes#datasets.IterableDataset)ordict[str, Dataset | IterableDataset]
) — Dataset to use for evaluation. It must meet the same requirements astrain_dataset
.[processing_class (](#trl.DPOTrainer.processing_class)[PreTrainedTokenizerBase](https://huggingface.co/docs/transformers/main/en/internal/tokenization_utils#transformers.PreTrainedTokenizerBase),[ProcessorMixin](https://huggingface.co/docs/transformers/main/en/main_classes/processors#transformers.ProcessorMixin), optional) — Processing class used to process the data. The padding side must be set to “left”. IfNone
, the processing class is loaded from the model’s name with[from_pretrained](https://huggingface.co/docs/transformers/main/en/model_doc/auto#transformers.AutoProcessor.from_pretrained). A padding token,tokenizer.pad_token
, must be set. If the processing class has not set a padding token,tokenizer.eos_token
will be used as the default.[compute_metrics (](#trl.DPOTrainer.compute_metrics)Callable[[EvalPrediction], dict]
, optional) — The function that will be used to compute metrics at evaluation. Must take a[EvalPrediction](https://huggingface.co/docs/transformers/main/en/internal/trainer_utils#transformers.EvalPrediction)and return a dictionary string to metric values. When passing[SFTConfig](/docs/trl/main/en/sft_trainer#trl.SFTConfig)withbatch_eval_metrics
set toTrue
, yourcompute_metrics
function must take a booleancompute_result
argument. This will be triggered after the last eval batch to signal that the function needs to calculate and return the global summary statistics rather than accumulating the batch-level statistics.[callbacks (list of](#trl.DPOTrainer.callbacks)[TrainerCallback](https://huggingface.co/docs/transformers/main/en/main_classes/callback#transformers.TrainerCallback), optional) — List of callbacks to customize the training loop. Will add those to the list of default callbacks detailed in[here](https://huggingface.co/docs/transformers/main_classes/callback).If you want to remove one of the default callbacks used, use the
[remove_callback](https://huggingface.co/docs/transformers/main/en/main_classes/trainer#transformers.Trainer.remove_callback)method.[optimizers (](#trl.DPOTrainer.optimizers)tuple[torch.optim.Optimizer | None, torch.optim.lr_scheduler.LambdaLR | None]
, optional, defaults to(None, None)
) — A tuple containing the optimizer and the scheduler to use. Will default to an instance ofAdamW
on your model and a scheduler given by[get_linear_schedule_with_warmup](https://huggingface.co/docs/transformers/main/en/main_classes/optimizer_schedules#transformers.get_linear_schedule_with_warmup)controlled byargs
.[peft_config (](#trl.DPOTrainer.peft_config)[PeftConfig](https://huggingface.co/docs/peft/main/en/package_reference/config#peft.PeftConfig), optional) — PEFT configuration used to wrap the model. IfNone
, the model is not wrapped.
Trainer for Direct Preference Optimization (DPO) method. This algorithm was initially proposed in the paper [Direct
Preference Optimization: Your Language Model is Secretly a Reward Model](https://huggingface.co/papers/2305.18290).
This class is a wrapper around the [Trainer](https://huggingface.co/docs/transformers/main/en/main_classes/trainer#transformers.Trainer) class and inherits all of its attributes and methods.
Example:
from trl import DPOTrainer
from datasets import load_dataset
dataset = load_dataset("trl-lib/ultrafeedback_binarized", split="train")
trainer = DPOTrainer(
model="Qwen/Qwen2.5-0.5B-Instruct",
train_dataset=dataset,
)
trainer.train()
train
[< source >](https://github.com/huggingface/trl/blob/main/transformers/trainer.py#L1322)
( resume_from_checkpoint: str | bool | None = None trial: optuna.Trial | dict[str, Any] | None = None ignore_keys_for_eval: list[str] | None = None ) → ~trainer_utils.TrainOutput
Parameters
[resume_from_checkpoint (](#trl.DPOTrainer.train.resume_from_checkpoint)str
orbool
, optional) — If astr
, local path to a saved checkpoint as saved by a previous instance ofTrainer
. If abool
and equalsTrue
, load the last checkpoint in args.output_dir as saved by a previous instance ofTrainer
. If present, training will resume from the model/optimizer/scheduler states loaded here.[trial (](#trl.DPOTrainer.train.trial)optuna.Trial
ordict[str, Any]
, optional) — The trial run or the hyperparameter dictionary for hyperparameter search.[ignore_keys_for_eval (](#trl.DPOTrainer.train.ignore_keys_for_eval)list[str]
, optional) — A list of keys in the output of your model (if it is a dictionary) that should be ignored when gathering predictions for evaluation during the training.
Returns
~trainer_utils.TrainOutput
Object containing the global step count, training loss, and metrics.
Main training entry point.
Will save the model, so you can reload it using from_pretrained()
.
Will only save from the main process.
push_to_hub
[< source >](https://github.com/huggingface/trl/blob/main/transformers/trainer.py#L3992)
( commit_message: str | None = 'End of training' blocking: bool = True token: str | None = None revision: str | None = None **kwargs )
Parameters
[commit_message (](#trl.DPOTrainer.push_to_hub.commit_message)str
, optional, defaults to"End of training"
) — Message to commit while pushing.[blocking (](#trl.DPOTrainer.push_to_hub.blocking)bool
, optional, defaults toTrue
) — Whether the function should return only when thegit push
has finished.[token (](#trl.DPOTrainer.push_to_hub.token)str
, optional, defaults toNone
) — Token with write permission to overwrite Trainer’s original args.[revision (](#trl.DPOTrainer.push_to_hub.revision)str
, optional) — The git revision to commit from. Defaults to the head of the “main” branch.[kwargs (](#trl.DPOTrainer.push_to_hub.kwargs)dict[str, Any]
, optional) — Additional keyword arguments passed along to~Trainer.create_model_card
.
Upload self.model
and self.processing_class
to the 🤗 model hub on the repo self.args.hub_model_id
.
DPOConfig
class trl.DPOConfig
[< source >](https://github.com/huggingface/trl/blob/main/trl/trainer/dpo_config.py#L23)
( output_dir: str | None = None per_device_train_batch_size: int = 8 num_train_epochs: float = 3.0 max_steps: int = -1 learning_rate: float = 1e-06 lr_scheduler_type: transformers.trainer_utils.SchedulerType | str = 'linear' lr_scheduler_kwargs: dict | str | None = None warmup_steps: float = 0 optim: transformers.training_args.OptimizerNames | str = 'adamw_torch_fused' optim_args: str | None = None weight_decay: float = 0.0 adam_beta1: float = 0.9 adam_beta2: float = 0.999 adam_epsilon: float = 1e-08 optim_target_modules: None | str | list[str] = None gradient_accumulation_steps: int = 1 average_tokens_across_devices: bool = True max_grad_norm: float = 1.0 label_smoothing_factor: float = 0.0 bf16: bool | None = None fp16: bool = False bf16_full_eval: bool = False fp16_full_eval: bool = False tf32: bool | None = None gradient_checkpointing: bool = True gradient_checkpointing_kwargs: dict[str, typing.Any] | str | None = None torch_compile: bool = False torch_compile_backend: str | None = None torch_compile_mode: str | None = None use_liger_kernel: bool = False liger_kernel_config: dict[str, bool] | None = None use_cache: bool = False neftune_noise_alpha: float | None = None torch_empty_cache_steps: int | None = None auto_find_batch_size: bool = False logging_strategy: transformers.trainer_utils.IntervalStrategy | str = 'steps' logging_steps: float = 10 logging_first_step: bool = False log_on_each_node: bool = True logging_nan_inf_filter: bool = True include_num_input_tokens_seen: str | bool = 'no' log_level: str = 'passive' log_level_replica: str = 'warning' disable_tqdm: bool | None = None report_to: None | str | list[str] = 'none' run_name: str | None = None project: str = 'huggingface' trackio_space_id: str | None = 'trackio' eval_strategy: transformers.trainer_utils.IntervalStrategy | str = 'no' eval_steps: float | None = None eval_delay: float = 0 per_device_eval_batch_size: int = 8 prediction_loss_only: bool = False eval_on_start: bool = False eval_do_concat_batches: bool = True eval_use_gather_object: bool = False eval_accumulation_steps: int | None = None include_for_metrics: list = <factory> batch_eval_metrics: bool = False save_only_model: bool = False save_strategy: transformers.trainer_utils.SaveStrategy | str = 'steps' save_steps: float = 500 save_on_each_node: bool = False save_total_limit: int | None = None enable_jit_checkpoint: bool = False push_to_hub: bool = False hub_token: str | None = None hub_private_repo: bool | None = None hub_model_id: str | None = None hub_strategy: transformers.trainer_utils.HubStrategy | str = 'every_save' hub_always_push: bool = False hub_revision: str | None = None load_best_model_at_end: bool = False metric_for_best_model: str | None = None greater_is_better: bool | None = None ignore_data_skip: bool = False restore_callback_states_from_checkpoint: bool = False full_determinism: bool = False seed: int = 42 data_seed: int | None = None use_cpu: bool = False accelerator_config: dict | str | None = None parallelism_config: accelerate.parallelism_config.ParallelismConfig | None = None dataloader_drop_last: bool = False dataloader_num_workers: int = 0 dataloader_pin_memory: bool = True dataloader_persistent_workers: bool = False dataloader_prefetch_factor: int | None = None remove_unused_columns: bool = True label_names: list[str] | None = None train_sampling_strategy: str = 'random' length_column_name: str = 'length' ddp_find_unused_parameters: bool | None = None ddp_bucket_cap_mb: int | None = None ddp_broadcast_buffers: bool | None = None ddp_backend: str | None = None ddp_timeout: int = 1800 fsdp: list[transformers.trainer_utils.FSDPOption] | str | None = None fsdp_config: dict[str, typing.Any] | str | None = None deepspeed: dict | str | None = None debug: str | list[transformers.debug_utils.DebugOption] = '' skip_memory_metrics: bool = True do_train: bool = False do_eval: bool = False do_predict: bool = False resume_from_checkpoint: str | None = None warmup_ratio: float | None = None logging_dir: str | None = None local_rank: int = -1 model_init_kwargs: dict[str, typing.Any] | str | None = None disable_dropout: bool = True dataset_num_proc: int | None = None max_length: int | None = 1024 truncation_mode: str = 'keep_start' padding_free: bool = False pad_to_multiple_of: int | None = None precompute_ref_log_probs: bool = False precompute_ref_batch_size: int | None = None loss_type: list = <factory> loss_weights: list[float] | None = None ld_alpha: float | None = None f_divergence_type: str = 'reverse_kl' f_alpha_divergence_coef: float = 0.5 label_smoothing: float = 0.0 beta: float = 0.1 use_weighting: bool = False discopop_tau: float = 0.05 activation_offloading: bool = False sync_ref_model: bool = False ref_model_mixup_alpha: float = 0.6 ref_model_sync_steps: int = 512 pad_token: str | None = None )
Parameters that control the model
[model_init_kwargs (](#trl.DPOConfig.model_init_kwargs)dict[str, Any]
, optional) — Keyword arguments for[from_pretrained](https://huggingface.co/docs/transformers/main/en/model_doc/auto#transformers.AutoModelForCausalLM.from_pretrained), used when themodel
argument of the[DPOTrainer](/docs/trl/main/en/bema_for_reference_model#trl.DPOTrainer)is provided as a string.[disable_dropout (](#trl.DPOConfig.disable_dropout)bool
, optional, defaults toTrue
) — Whether to disable dropout in the model and reference model.
Parameters that control the data preprocessing
[dataset_num_proc (](#trl.DPOConfig.dataset_num_proc)int
, optional) — Number of processes to use for processing the dataset.[max_length (](#trl.DPOConfig.max_length)int
orNone
, optional, defaults to1024
) — Maximum length of the tokenized sequence. Sequences longer thanmax_length
are truncated from the left or right depending on thetruncation_mode
. IfNone
, no truncation is applied.[truncation_mode (](#trl.DPOConfig.truncation_mode)str
, optional, defaults to"keep_start"
) — Truncation mode to use when the sequence exceedsmax_length
. The only supported value is"keep_start"
. The"keep_end"
value is deprecated and will be removed in v2.0.0.[padding_free (](#trl.DPOConfig.padding_free)bool
, optional, defaults toFalse
) — Whether to perform forward passes without padding by flattening all sequences in the batch into a single continuous sequence. This reduces memory usage by eliminating padding overhead. Currently, this is only supported with the FlashAttention 2 or 3, which can efficiently handle the flattened batch structure.[pad_to_multiple_of (](#trl.DPOConfig.pad_to_multiple_of)int
, optional) — If set, the sequences will be padded to a multiple of this value.[precompute_ref_log_probs (](#trl.DPOConfig.precompute_ref_log_probs)bool
, optional, defaults toFalse
) — Whether to precompute the reference model log probabilities for the entire training dataset before training. This allows to save memory during training, as the reference model does not need to be kept in memory.[precompute_ref_batch_size (](#trl.DPOConfig.precompute_ref_batch_size)int
, optional) — Batch size to use when precomputing reference model log probabilities. This can be set higher than the training batch size to speed up preprocessing. IfNone
, defaults toper_device_train_batch_size
for training andper_device_eval_batch_size
for evaluation.
Parameters that control the training
[loss_type (](#trl.DPOConfig.loss_type)list[str]
, optional, defaults to["sigmoid"]
) — Type of loss to use. Possible values are:'sigmoid'
,'hinge'
,'ipo'
,'exo_pair'
,'nca_pair'
,'robust'
,'bco_pair'
,'sppo_hard'
,'aot'
,'aot_unpaired'
,'apo_zero'
,'apo_down'
,'discopop'
,'sft'
. If multiple loss types are provided, they will be combined using the weights specified inloss_weights
.[loss_weights (](#trl.DPOConfig.loss_weights)list[float]
, optional) — List of loss weights for multi-loss combinations. Used when combining multiple loss types. Example:[0.8, 0.2, 1.0]
for MPO. If not provided, defaults to equal weights (1.0
) for all loss types.[ld_alpha (](#trl.DPOConfig.ld_alpha)float
, optional) — α parameter from the LD-DPO paper, which controls the weighting of the verbose token log-probabilities in responses. IfNone
, no weighting is applied to the verbose part, and the loss is equivalent to the standard DPO loss. Must be in [0.0, 1.0]:ld_alpha=1.0
applies no weighting, andld_alpha=0.0
masks tokens beyond shared lengths.[f_divergence_type (](#trl.DPOConfig.f_divergence_type)str
, optional, defaults to"reverse_kl"
) — f-divergence regularizer between policy and reference (f-DPO paper). Possible values are:reverse_kl
(default),forward_kl
,js_divergence
,alpha_divergence
.[f_alpha_divergence_coef (](#trl.DPOConfig.f_alpha_divergence_coef)float
, optional, defaults to0.5
) — α coefficient for the α-divergence u^-α regularizer, used only whenf_divergence_type='alpha_divergence'
.[label_smoothing (](#trl.DPOConfig.label_smoothing)float
, optional, defaults to0.0
) — Label smoothing parameter used in Robust DPO and EXO. In Robust DPO, it is interpreted as the probability that a preference label is flipped and must lie in [0.0, 0.5); a typical value recommended by the Robust DPO paper is 0.1. In EXO, it corresponds to the ε label smoothing parameter, for which the paper recommends a typical value of 1e-3.[beta (](#trl.DPOConfig.beta)float
, optional, defaults to0.1
) — Parameter controlling the deviation from the reference model. Higher β means less deviation from the reference model. For the IPO loss (loss_type='ipo'
), this value is the regularization parameter denoted by τ in the[paper](https://huggingface.co/papers/2310.12036).[use_weighting (](#trl.DPOConfig.use_weighting)bool
, optional, defaults toFalse
) — Whether to apply WPO-style weighting ([https://huggingface.co/papers/2406.11827](https://huggingface.co/papers/2406.11827)) to preference pairs using the policy’s length-normalized sequence probabilities.[discopop_tau (](#trl.DPOConfig.discopop_tau)float
, optional, defaults to0.05
) — τ/temperature parameter from the DiscoPOP paper, which controls the shape of the log-ratio modulated loss when usingloss_type='discopop'
. The paper recommends the default valuediscopop_tau=0.05
.[activation_offloading (](#trl.DPOConfig.activation_offloading)bool
, optional, defaults toFalse
) — Whether to offload the activations to the CPU.[sync_ref_model (](#trl.DPOConfig.sync_ref_model)bool
, optional, defaults toFalse
) — Whether to synchronize the reference model with the active model everyref_model_sync_steps
steps, using theref_model_mixup_alpha
parameter. This synchronization originates from the[TR-DPO](https://huggingface.co/papers/2404.09656)paper.sync_ref_model=True
is not yet compatible with PEFT orprecompute_ref_log_probs=True
.[ref_model_mixup_alpha (](#trl.DPOConfig.ref_model_mixup_alpha)float
, optional, defaults to0.6
) — α parameter from the TR-DPO paper, which controls the mix between the current policy and the previous reference policy during updates. The reference policy is updated according to the equation:π_ref = α * π_θ + (1 - α) * π_ref_prev
. To use this parameter, you must setsync_ref_model=True
.[ref_model_sync_steps (](#trl.DPOConfig.ref_model_sync_steps)int
, optional, defaults to512
) — τ parameter from the TR-DPO paper, which determines how frequently the current policy is synchronized with the reference policy. To use this parameter, you must setsync_ref_model=True
.
Deprecated parameters
Configuration class for the [DPOTrainer](/docs/trl/main/en/bema_for_reference_model#trl.DPOTrainer).
This class includes only the parameters that are specific to DPO training. For a full list of training arguments,
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
: Defaults to1e-6
instead of5e-5
.
[Update on GitHub](https://github.com/huggingface/trl/blob/main/docs/source/dpo_trainer.md)