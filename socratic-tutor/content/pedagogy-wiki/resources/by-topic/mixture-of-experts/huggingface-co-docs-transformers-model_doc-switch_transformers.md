# Source: https://huggingface.co/docs/transformers/model_doc/switch_transformers
# Downloaded: 2026-04-09
# Words: 4068
# Author: Hugging Face
# Author Slug: hugging-face
Transformers documentation
Switch Transformers
This model was released on 2021-01-11 and added to Hugging Face Transformers on 2022-11-15.
Switch Transformers
[Switch Transformers](https://huggingface.co/papers/2101.03961) is a sparse T5 model where the MLP layer is replaced by a Mixture-of-Experts (MoE). A routing mechanism associates each token with an expert and each expert is a dense MLP. Sparsity enables better scaling and the routing mechanism allows the model to select relevant weights on the fly which increases model capacity.
You can find all the original Switch Transformers checkpoints under the [Switch Transformer](https://huggingface.co/collections/google/switch-transformers-release-6548c35c6507968374b56d1f) collection.
This model was contributed by
[ybelkada]and[ArthurZ].Click on the Switch Transformers models in the right sidebar for more examples of how to apply Switch Transformers to different natural language tasks.
The example below demonstrates how to predict the masked token with [Pipeline](/docs/transformers/v5.5.3/en/main_classes/pipelines#transformers.Pipeline), [AutoModel](/docs/transformers/v5.5.3/en/model_doc/auto#transformers.AutoModel), and from the command line.
import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained("google/switch-base-8")
model = AutoModelForSeq2SeqLM.from_pretrained("google/switch-base-8", device_map="auto", dtype=torch.float16)
input_text = "The capital of France is <extra_id_0>."
input_ids = tokenizer(input_text, return_tensors="pt").input_ids.to(0)
outputs = model.generate(input_ids)
print(tokenizer.decode(outputs[0]))
Quantization reduces the memory burden of large models by representing the weights in a lower precision. Refer to the [Quantization](../quantization/overview) overview for more available quantization backends.
The example below uses [bitsandbytes](../quantization/bitsandbytes/) to only quantize the weights to 8-bits.
# pip install bitsandbytes
import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, BitsAndBytesConfig
tokenizer = AutoTokenizer.from_pretrained("google/switch-base-8")
quantization_config = BitsAndBytesConfig(load_in_8bit=True)
model = AutoModelForSeq2SeqLM.from_pretrained("google/switch-base-8", device_map="auto", quantization_config=quantization_config)
input_text = "The capital of France is <extra_id_0>."
input_ids = tokenizer(input_text, return_tensors="pt").input_ids.to(0)
outputs = model.generate(input_ids)
print(tokenizer.decode(outputs[0]))
SwitchTransformersConfig
class transformers.SwitchTransformersConfig
[< source >](https://github.com/huggingface/transformers/blob/v5.5.3/src/transformers/models/switch_transformers/configuration_switch_transformers.py#L26)
( transformers_version: str | None = None architectures: list[str] | None = None output_hidden_states: bool | None = False return_dict: bool | None = True dtype: typing.Union[str, ForwardRef('torch.dtype'), NoneType] = None chunk_size_feed_forward: int = 0 id2label: dict[int, str] | dict[str, str] | None = None label2id: dict[str, int] | dict[str, str] | None = None problem_type: typing.Optional[typing.Literal['regression', 'single_label_classification', 'multi_label_classification']] = None is_encoder_decoder: bool = True vocab_size: int = 32128 d_model: int = 768 d_kv: int = 64 d_ff: int = 2048 expert_capacity: int = 64 num_layers: int = 12 num_sparse_encoder_layers: int = 3 num_decoder_layers: int | None = 12 num_sparse_decoder_layers: int = 3 num_heads: int = 12 num_experts: int = 8 router_bias: bool = False router_jitter_noise: int | float = 0.01 router_dtype: typing.Literal['float32', 'float16', 'bfloat16'] = 'float32' router_ignore_padding_tokens: bool = False relative_attention_num_buckets: int = 32 relative_attention_max_distance: int = 128 dropout_rate: float | int = 0.1 layer_norm_epsilon: float = 1e-06 router_z_loss_coef: float = 0.001 router_aux_loss_coef: float = 0.001 initializer_factor: float = 1.0 dense_act_fn: str = 'relu' add_router_probs: bool = False use_cache: bool = True pad_token_id: int | None = 0 eos_token_id: int | list[int] | None = 1 bos_token_id: int | None = None tie_word_embeddings: bool = True is_decoder: bool = False add_cross_attention: bool = False )
Parameters
[is_encoder_decoder (](#transformers.SwitchTransformersConfig.is_encoder_decoder)bool
, optional, defaults toTrue
) — Whether the model is used as an encoder/decoder or not.[vocab_size (](#transformers.SwitchTransformersConfig.vocab_size)int
, optional, defaults to32128
) — Vocabulary size of the model. Defines the number of different tokens that can be represented by theinput_ids
.[d_model (](#transformers.SwitchTransformersConfig.d_model)int
, optional, defaults to768
) — Size of the encoder layers and the pooler layer.[d_kv (](#transformers.SwitchTransformersConfig.d_kv)int
, optional, defaults to64
) — Size of the key, query, value projections per attention head. Theinner_dim
of the projection layer will be defined asnum_heads * d_kv
.[d_ff (](#transformers.SwitchTransformersConfig.d_ff)int
, optional, defaults to2048
) — Dimension of the MLP representations.[expert_capacity (](#transformers.SwitchTransformersConfig.expert_capacity)int
, optional, defaults to64
) — The number of tokens that each expert can process. IfNone
,expert_capacity
will be set to(sequence_length / num_experts) * capacity_factor
.[num_layers (](#transformers.SwitchTransformersConfig.num_layers)int
, optional, defaults to12
) — Number of hidden layers in the Transformer decoder.[num_sparse_encoder_layers (](#transformers.SwitchTransformersConfig.num_sparse_encoder_layers)int
, optional, defaults to 3) — Number of sparse (MoE) dense hidden layers in the Transformer encoder layer. Note: When set to 0 withnum_layers=1
, the current implementation may still create a sparse layer due to the sparse step calculation. This edge case is not encountered in existing checkpoints.[num_decoder_layers (](#transformers.SwitchTransformersConfig.num_decoder_layers)int
, optional, defaults to12
) — Number of hidden layers in the Transformer decoder. Will use the same value asnum_layers
if not set.[num_sparse_decoder_layers (](#transformers.SwitchTransformersConfig.num_sparse_decoder_layers)int
, optional, defaults to 3) — Number of sparse (MoE) dense hidden layers in the Transformer decoder layer. Note: When set to 0 withnum_decoder_layers=1
, the current implementation may still create a sparse layer due to the sparse step calculation. This edge case is not encountered in existing checkpoints.[num_heads (](#transformers.SwitchTransformersConfig.num_heads)int
, optional, defaults to12
) — Number of attention heads for each attention layer in the Transformer decoder.[num_experts (](#transformers.SwitchTransformersConfig.num_experts)int
, optional, defaults to8
) — Number of routed experts in MoE layers.[router_bias (](#transformers.SwitchTransformersConfig.router_bias)bool
, optional, defaults toFalse
) — Whether to add a bias to the router.[router_jitter_noise (](#transformers.SwitchTransformersConfig.router_jitter_noise)Union[int, float]
, optional, defaults to0.01
) — Amount of noise to add to the router logits during training for better load balancing.[router_dtype (](#transformers.SwitchTransformersConfig.router_dtype)str
, optional, default to"float32"
) — Thedtype
used for the routers. It is preferable to keep thedtype
to"float32"
as specified in the selective precision discussion in[the paper](https://huggingface.co/papers/2101.03961).[router_ignore_padding_tokens (](#transformers.SwitchTransformersConfig.router_ignore_padding_tokens)bool
, optional, defaults toFalse
) — Whether to ignore padding tokens when routing.[relative_attention_num_buckets (](#transformers.SwitchTransformersConfig.relative_attention_num_buckets)int
, optional, defaults to 32) — The number of buckets to use for each attention layer.[relative_attention_max_distance (](#transformers.SwitchTransformersConfig.relative_attention_max_distance)int
, optional, defaults to 128) — The maximum distance of the longer sequences for the bucket separation.[dropout_rate (](#transformers.SwitchTransformersConfig.dropout_rate)Union[float, int]
, optional, defaults to0.1
) — The ratio for all dropout layers.[layer_norm_epsilon (](#transformers.SwitchTransformersConfig.layer_norm_epsilon)float
, optional, defaults to1e-06
) — The epsilon used by the layer normalization layers.[router_z_loss_coef (](#transformers.SwitchTransformersConfig.router_z_loss_coef)float
, optional, defaults to0.001
) — Coefficient for the router z-loss, which penalizes large router logits to improve training stability.[router_aux_loss_coef (](#transformers.SwitchTransformersConfig.router_aux_loss_coef)float
, optional, defaults to0.001
) — Auxiliary load balancing loss coefficient. Used to penalize uneven expert routing in MoE models.[initializer_factor (](#transformers.SwitchTransformersConfig.initializer_factor)float
, optional, defaults to1.0
) — A factor for initializing all weight matrices (should be kept to 1, used internally for initialization testing).[dense_act_fn (](#transformers.SwitchTransformersConfig.dense_act_fn)string
, optional, defaults to"relu"
) — Type of feed forward layer to be used. Should be one of"relu"
or"gated-gelu"
. SwitchTransformersv1.1 uses the"gated-gelu"
feed forward projection. Original SwitchTransformers uses"relu"
.[add_router_probs (](#transformers.SwitchTransformersConfig.add_router_probs)bool
, optional, defaults toFalse
) — Whether to output router probabilities to compute router auxiliary loss.[use_cache (](#transformers.SwitchTransformersConfig.use_cache)bool
, optional, defaults toTrue
) — Whether or not the model should return the last key/values attentions (not used by all models). Only relevant ifconfig.is_decoder=True
or when the model is a decoder-only generative model.[pad_token_id (](#transformers.SwitchTransformersConfig.pad_token_id)int
, optional, defaults to0
) — Token id used for padding in the vocabulary.[eos_token_id (](#transformers.SwitchTransformersConfig.eos_token_id)Union[int, list[int]]
, optional, defaults to1
) — Token id used for end-of-stream in the vocabulary.[bos_token_id (](#transformers.SwitchTransformersConfig.bos_token_id)int
, optional) — Token id used for beginning-of-stream in the vocabulary.[tie_word_embeddings (](#transformers.SwitchTransformersConfig.tie_word_embeddings)bool
, optional, defaults toTrue
) — Whether to tie weight embeddings according to model’stied_weights_keys
mapping.[is_decoder (](#transformers.SwitchTransformersConfig.is_decoder)bool
, optional, defaults toFalse
) — Whether the model is used as a decoder or not. IfFalse
, the model is used as an encoder.[add_cross_attention (](#transformers.SwitchTransformersConfig.add_cross_attention)bool
, optional, defaults toFalse
) — Whether cross-attention layers should be added to the model.
This is the configuration class to store the configuration of a SwitchTransformersModel. It is used to instantiate a Switch Transformers
model according to the specified arguments, defining the model architecture. Instantiating a configuration with the
defaults will yield a similar configuration to that of the [google/switch-base-8](https://huggingface.co/google/switch-base-8)
Configuration objects inherit from [PreTrainedConfig](/docs/transformers/v5.5.3/en/main_classes/configuration#transformers.PreTrainedConfig) and can be used to control the model outputs. Read the
documentation from [PreTrainedConfig](/docs/transformers/v5.5.3/en/main_classes/configuration#transformers.PreTrainedConfig) for more information.
SwitchTransformersTop1Router
Router using tokens choose top-1 experts assignment.
This router uses the same mechanism as in Switch Transformer ([https://huggingface.co/papers/2101.03961](https://huggingface.co/papers/2101.03961)) and V-MoE
([https://huggingface.co/papers/2106.05974](https://huggingface.co/papers/2106.05974)): tokens choose their top experts. Items are sorted by router_probs and then
routed to their choice of expert until the expert’s expert_capacity is reached. There is no guarantee that each
token is processed by an expert, or that each expert receives at least one token.
forward
[< source >](https://github.com/huggingface/transformers/blob/v5.5.3/src/transformers/models/switch_transformers/modeling_switch_transformers.py#L71)
( hidden_states: Tensor ) → router_probabilities (torch.Tensor
)
Parameters
[hidden_states (](#transformers.SwitchTransformersTop1Router.forward.hidden_states)torch.Tensor
) — (batch_size, sequence_length, hidden_dim) from which router probabilities are computed.
Returns
router_probabilities (torch.Tensor
)
Tensor of shape (batch_size, sequence_length, num_experts) corresponding to the probabilities for each
token and expert. Used for routing tokens to experts.
router_logits (torch.Tensor
):
Logits tensor of shape (batch_size, sequence_length, num_experts) corresponding to raw router logits.
This is used later for computing router z-loss.
Computes router probabilities from input hidden states.
SwitchTransformersSparseMLP
SwitchTransformersModel
class transformers.SwitchTransformersModel
[< source >](https://github.com/huggingface/transformers/blob/v5.5.3/src/transformers/models/switch_transformers/modeling_switch_transformers.py#L747)
( config: SwitchTransformersConfig )
Parameters
[config (](#transformers.SwitchTransformersModel.config)[SwitchTransformersConfig](/docs/transformers/v5.5.3/en/model_doc/switch_transformers#transformers.SwitchTransformersConfig)) — Model configuration class with all the parameters of the model. Initializing with a config file does not load the weights associated with the model, only the configuration. Check out the[from_pretrained()](/docs/transformers/v5.5.3/en/main_classes/model#transformers.PreTrainedModel.from_pretrained)method to load the model weights.
The bare Switch Transformers Model outputting raw hidden-states without any specific head on top.
This model inherits from [PreTrainedModel](/docs/transformers/v5.5.3/en/main_classes/model#transformers.PreTrainedModel). Check the superclass documentation for the generic methods the
library implements for all its model (such as downloading or saving, resizing the input embeddings, pruning heads
etc.)
This model is also a PyTorch [torch.nn.Module](https://pytorch.org/docs/stable/nn.html#torch.nn.Module) subclass.
Use it as a regular PyTorch Module and refer to the PyTorch documentation for all matter related to general usage
and behavior.
forward
[< source >](https://github.com/huggingface/transformers/blob/v5.5.3/src/transformers/models/switch_transformers/modeling_switch_transformers.py#L775)
( input_ids: torch.LongTensor | None = None attention_mask: torch.FloatTensor | None = None decoder_input_ids: torch.LongTensor | None = None decoder_attention_mask: torch.BoolTensor | None = None encoder_outputs: tuple[tuple[torch.FloatTensor]] | None = None past_key_values: transformers.cache_utils.Cache | None = None inputs_embeds: torch.Tensor | None = None decoder_inputs_embeds: torch.Tensor | None = None **kwargs: typing_extensions.Unpack[transformers.utils.generic.TransformersKwargs] ) → Seq2SeqMoEModelOutput
or tuple(torch.FloatTensor)
Parameters
[input_ids (](#transformers.SwitchTransformersModel.forward.input_ids)torch.LongTensor
of shape(batch_size, sequence_length)
, optional) — Indices of input sequence tokens in the vocabulary. Padding will be ignored by default.Indices can be obtained using
[AutoTokenizer](/docs/transformers/v5.5.3/en/model_doc/auto#transformers.AutoTokenizer). See[PreTrainedTokenizer.encode()](/docs/transformers/v5.5.3/en/internal/tokenization_utils#transformers.PreTrainedTokenizerBase.encode)and[PreTrainedTokenizer.call()](/docs/transformers/v5.5.3/en/internal/tokenization_utils#transformers.PreTrainedTokenizerBase.__call__)for details.[attention_mask (](#transformers.SwitchTransformersModel.forward.attention_mask)torch.FloatTensor
of shape(batch_size, sequence_length)
, optional) — Mask to avoid performing attention on padding token indices. Mask values selected in[0, 1]
:- 1 for tokens that are not masked,
- 0 for tokens that are masked.
[decoder_input_ids (](#transformers.SwitchTransformersModel.forward.decoder_input_ids)torch.LongTensor
of shape(batch_size, target_sequence_length)
, optional) — Indices of decoder input sequence tokens in the vocabulary.Indices can be obtained using
[AutoTokenizer](/docs/transformers/v5.5.3/en/model_doc/auto#transformers.AutoTokenizer). See[PreTrainedTokenizer.encode()](/docs/transformers/v5.5.3/en/internal/tokenization_utils#transformers.PreTrainedTokenizerBase.encode)and[PreTrainedTokenizer.call()](/docs/transformers/v5.5.3/en/internal/tokenization_utils#transformers.PreTrainedTokenizerBase.__call__)for details.[decoder_attention_mask (](#transformers.SwitchTransformersModel.forward.decoder_attention_mask)torch.BoolTensor
of shape(batch_size, target_sequence_length)
, optional) — Mask to avoid performing attention on certain token indices. By default, a causal mask will be used, to make sure the model can only look at previous inputs in order to predict the future.[encoder_outputs (](#transformers.SwitchTransformersModel.forward.encoder_outputs)tuple[tuple[torch.FloatTensor]]
, optional) — Tuple consists of (last_hidden_state
, optional:hidden_states
, optional:attentions
)last_hidden_state
of shape(batch_size, sequence_length, hidden_size)
, optional) is a sequence of hidden-states at the output of the last layer of the encoder. Used in the cross-attention of the decoder.[past_key_values (](#transformers.SwitchTransformersModel.forward.past_key_values)~cache_utils.Cache
, optional) — Pre-computed hidden-states (key and values in the self-attention blocks and in the cross-attention blocks) that can be used to speed up sequential decoding. This typically consists in thepast_key_values
returned by the model at a previous stage of decoding, whenuse_cache=True
orconfig.use_cache=True
.Only
[Cache](/docs/transformers/v5.5.3/en/internal/generation_utils#transformers.Cache)instance is allowed as input, see our[kv cache guide](https://huggingface.co/docs/transformers/en/kv_cache). If nopast_key_values
are passed,[DynamicCache](/docs/transformers/v5.5.3/en/internal/generation_utils#transformers.DynamicCache)will be initialized by default.The model will output the same cache format that is fed as input.
If
past_key_values
are used, the user is expected to input only unprocessedinput_ids
(those that don’t have their past key value states given to this model) of shape(batch_size, unprocessed_length)
instead of allinput_ids
of shape(batch_size, sequence_length)
.[inputs_embeds (](#transformers.SwitchTransformersModel.forward.inputs_embeds)torch.Tensor
of shape(batch_size, sequence_length, hidden_size)
, optional) — Optionally, instead of passinginput_ids
you can choose to directly pass an embedded representation. This is useful if you want more control over how to convertinput_ids
indices into associated vectors than the model’s internal embedding lookup matrix.[decoder_inputs_embeds (](#transformers.SwitchTransformersModel.forward.decoder_inputs_embeds)torch.Tensor
of shape(batch_size, target_sequence_length, hidden_size)
, optional) — Optionally, instead of passingdecoder_input_ids
you can choose to directly pass an embedded representation. Ifpast_key_values
is used, optionally only the lastdecoder_inputs_embeds
have to be input (seepast_key_values
). This is useful if you want more control over how to convertdecoder_input_ids
indices into associated vectors than the model’s internal embedding lookup matrix.If
decoder_input_ids
anddecoder_inputs_embeds
are both unset,decoder_inputs_embeds
takes the value ofinputs_embeds
.
Returns
Seq2SeqMoEModelOutput
or tuple(torch.FloatTensor)
A Seq2SeqMoEModelOutput
or a tuple of
torch.FloatTensor
(if return_dict=False
is passed or when config.return_dict=False
) comprising various
elements depending on the configuration (None
) and inputs.
The [SwitchTransformersModel](/docs/transformers/v5.5.3/en/model_doc/switch_transformers#transformers.SwitchTransformersModel) forward method, overrides the __call__
special method.
Although the recipe for forward pass needs to be defined within this function, one should call the
Module
instance afterwards instead of this since the former takes care of running the pre and post processing steps while the latter silently ignores them.
last_hidden_state (
torch.FloatTensor
of shape(batch_size, sequence_length, hidden_size)
) — Sequence of hidden-states at the output of the last layer of the decoder of the model.If
past_key_values
is used only the last hidden-state of the sequences of shape(batch_size, 1, hidden_size)
is output.past_key_values (
EncoderDecoderCache
, optional, returned whenuse_cache=True
is passed or whenconfig.use_cache=True
) — It is a[EncoderDecoderCache](/docs/transformers/v5.5.3/en/internal/generation_utils#transformers.EncoderDecoderCache)instance. For more details, see our[kv cache guide](https://huggingface.co/docs/transformers/en/kv_cache).Contains pre-computed hidden-states (key and values in the self-attention blocks and in the cross-attention blocks) that can be used (see
past_key_values
input) to speed up sequential decoding.decoder_hidden_states (
tuple(torch.FloatTensor)
, optional, returned whenoutput_hidden_states=True
is passed or whenconfig.output_hidden_states=True
) — Tuple oftorch.FloatTensor
(one for the output of the embeddings, if the model has an embedding layer, + one for the output of each layer) of shape(batch_size, sequence_length, hidden_size)
.Hidden-states of the decoder at the output of each layer plus the optional initial embedding outputs.
decoder_attentions (
tuple(torch.FloatTensor)
, optional, returned whenoutput_attentions=True
is passed or whenconfig.output_attentions=True
) — Tuple oftorch.FloatTensor
(one for each layer) of shape(batch_size, num_heads, sequence_length, sequence_length)
.Attentions weights of the decoder, after the attention softmax, used to compute the weighted average in the self-attention heads.
decoder_router_logits (
tuple(torch.FloatTensor)
, optional, returned whenoutput_router_logits=True
is passed or whenconfig.add_router_probs=True
) — Tuple oftorch.FloatTensor
(one for each layer) of shape(batch_size, sequence_length, num_experts)
.Router logits of the decoder model, useful to compute the auxiliary loss for Mixture of Experts models.
cross_attentions (
tuple(torch.FloatTensor)
, optional, returned whenoutput_attentions=True
is passed or whenconfig.output_attentions=True
) — Tuple oftorch.FloatTensor
(one for each layer) of shape(batch_size, num_heads, sequence_length, sequence_length)
.Attentions weights of the decoder’s cross-attention layer, after the attention softmax, used to compute the weighted average in the cross-attention heads.
encoder_last_hidden_state (
torch.FloatTensor
of shape(batch_size, sequence_length, hidden_size)
, optional) — Sequence of hidden-states at the output of the last layer of the encoder of the model.encoder_hidden_states (
tuple(torch.FloatTensor)
, optional, returned whenoutput_hidden_states=True
is passed or whenconfig.output_hidden_states=True
) — Tuple oftorch.FloatTensor
(one for the output of the embeddings, if the model has an embedding layer, + one for the output of each layer) of shape(batch_size, sequence_length, hidden_size)
.Hidden-states of the encoder at the output of each layer plus the optional initial embedding outputs.
encoder_attentions (
tuple(torch.FloatTensor)
, optional, returned whenoutput_attentions=True
is passed or whenconfig.output_attentions=True
) — Tuple oftorch.FloatTensor
(one for each layer) of shape(batch_size, num_heads, sequence_length, sequence_length)
.Attentions weights of the encoder, after the attention softmax, used to compute the weighted average in the self-attention heads.
encoder_router_logits (
tuple(torch.FloatTensor)
, optional, returned whenoutput_router_logits=True
is passed or whenconfig.add_router_probs=True
) — Tuple oftorch.FloatTensor
(one for each layer) of shape(batch_size, sequence_length, num_experts)
.Router logits of the encoder model, useful to compute the auxiliary loss and the z_loss for the sparse modules.
SwitchTransformersForConditionalGeneration
class transformers.SwitchTransformersForConditionalGeneration
[< source >](https://github.com/huggingface/transformers/blob/v5.5.3/src/transformers/models/switch_transformers/modeling_switch_transformers.py#L889)
( config: SwitchTransformersConfig )
Parameters
[config (](#transformers.SwitchTransformersForConditionalGeneration.config)[SwitchTransformersConfig](/docs/transformers/v5.5.3/en/model_doc/switch_transformers#transformers.SwitchTransformersConfig)) — Model configuration class with all the parameters of the model. Initializing with a config file does not load the weights associated with the model, only the configuration. Check out the[from_pretrained()](/docs/transformers/v5.5.3/en/main_classes/model#transformers.PreTrainedModel.from_pretrained)method to load the model weights.
SWITCH_TRANSFORMERS Model with a language modeling
head on top.
This model inherits from [PreTrainedModel](/docs/transformers/v5.5.3/en/main_classes/model#transformers.PreTrainedModel). Check the superclass documentation for the generic methods the
library implements for all its model (such as downloading or saving, resizing the input embeddings, pruning heads
etc.)
This model is also a PyTorch [torch.nn.Module](https://pytorch.org/docs/stable/nn.html#torch.nn.Module) subclass.
Use it as a regular PyTorch Module and refer to the PyTorch documentation for all matter related to general usage
and behavior.
forward
[< source >](https://github.com/huggingface/transformers/blob/v5.5.3/src/transformers/models/switch_transformers/modeling_switch_transformers.py#L926)
( input_ids: torch.LongTensor | None = None attention_mask: torch.FloatTensor | None = None decoder_input_ids: torch.LongTensor | None = None decoder_attention_mask: torch.BoolTensor | None = None encoder_outputs: tuple[tuple[torch.Tensor]] | None = None past_key_values: transformers.cache_utils.Cache | None = None inputs_embeds: torch.FloatTensor | None = None decoder_inputs_embeds: torch.FloatTensor | None = None labels: torch.LongTensor | None = None output_router_logits: bool | None = False **kwargs: typing_extensions.Unpack[transformers.utils.generic.TransformersKwargs] ) → Seq2SeqMoEOutput
or tuple(torch.FloatTensor)
Parameters
[input_ids (](#transformers.SwitchTransformersForConditionalGeneration.forward.input_ids)torch.LongTensor
of shape(batch_size, sequence_length)
, optional) — Indices of input sequence tokens in the vocabulary. Padding will be ignored by default.Indices can be obtained using
[AutoTokenizer](/docs/transformers/v5.5.3/en/model_doc/auto#transformers.AutoTokenizer). See[PreTrainedTokenizer.encode()](/docs/transformers/v5.5.3/en/internal/tokenization_utils#transformers.PreTrainedTokenizerBase.encode)and[PreTrainedTokenizer.call()](/docs/transformers/v5.5.3/en/internal/tokenization_utils#transformers.PreTrainedTokenizerBase.__call__)for details.[attention_mask (](#transformers.SwitchTransformersForConditionalGeneration.forward.attention_mask)torch.FloatTensor
of shape(batch_size, sequence_length)
, optional) — Mask to avoid performing attention on padding token indices. Mask values selected in[0, 1]
:- 1 for tokens that are not masked,
- 0 for tokens that are masked.
[decoder_input_ids (](#transformers.SwitchTransformersForConditionalGeneration.forward.decoder_input_ids)torch.LongTensor
of shape(batch_size, target_sequence_length)
, optional) — Indices of decoder input sequence tokens in the vocabulary.Indices can be obtained using
[AutoTokenizer](/docs/transformers/v5.5.3/en/model_doc/auto#transformers.AutoTokenizer). See[PreTrainedTokenizer.encode()](/docs/transformers/v5.5.3/en/internal/tokenization_utils#transformers.PreTrainedTokenizerBase.encode)and[PreTrainedTokenizer.call()](/docs/transformers/v5.5.3/en/internal/tokenization_utils#transformers.PreTrainedTokenizerBase.__call__)for details.[decoder_attention_mask (](#transformers.SwitchTransformersForConditionalGeneration.forward.decoder_attention_mask)torch.BoolTensor
of shape(batch_size, target_sequence_length)
, optional) — Mask to avoid performing attention on certain token indices. By default, a causal mask will be used, to make sure the model can only look at previous inputs in order to predict the future.[encoder_outputs (](#transformers.SwitchTransformersForConditionalGeneration.forward.encoder_outputs)tuple[tuple[torch.Tensor]]
, optional) — Tuple consists of (last_hidden_state
, optional:hidden_states
, optional:attentions
)last_hidden_state
of shape(batch_size, sequence_length, hidden_size)
, optional) is a sequence of hidden-states at the output of the last layer of the encoder. Used in the cross-attention of the decoder.[past_key_values (](#transformers.SwitchTransformersForConditionalGeneration.forward.past_key_values)~cache_utils.Cache
, optional) — Pre-computed hidden-states (key and values in the self-attention blocks and in the cross-attention blocks) that can be used to speed up sequential decoding. This typically consists in thepast_key_values
returned by the model at a previous stage of decoding, whenuse_cache=True
orconfig.use_cache=True
.Only
[Cache](/docs/transformers/v5.5.3/en/internal/generation_utils#transformers.Cache)instance is allowed as input, see our[kv cache guide](https://huggingface.co/docs/transformers/en/kv_cache). If nopast_key_values
are passed,[DynamicCache](/docs/transformers/v5.5.3/en/internal/generation_utils#transformers.DynamicCache)will be initialized by default.The model will output the same cache format that is fed as input.
If
past_key_values
are used, the user is expected to input only unprocessedinput_ids
(those that don’t have their past key value states given to this model) of shape(batch_size, unprocessed_length)
instead of allinput_ids
of shape(batch_size, sequence_length)
.[inputs_embeds (](#transformers.SwitchTransformersForConditionalGeneration.forward.inputs_embeds)torch.FloatTensor
of shape(batch_size, sequence_length, hidden_size)
, optional) — Optionally, instead of passinginput_ids
you can choose to directly pass an embedded representation. This is useful if you want more control over how to convertinput_ids
indices into associated vectors than the model’s internal embedding lookup matrix.[decoder_inputs_embeds (](#transformers.SwitchTransformersForConditionalGeneration.forward.decoder_inputs_embeds)torch.FloatTensor
of shape(batch_size, target_sequence_length, hidden_size)
, optional) — Optionally, instead of passingdecoder_input_ids
you can choose to directly pass an embedded representation. Ifpast_key_values
is used, optionally only the lastdecoder_inputs_embeds
have to be input (seepast_key_values
). This is useful if you want more control over how to convertdecoder_input_ids
indices into associated vectors than the model’s internal embedding lookup matrix.If
decoder_input_ids
anddecoder_inputs_embeds
are both unset,decoder_inputs_embeds
takes the value ofinputs_embeds
.[labels (](#transformers.SwitchTransformersForConditionalGeneration.forward.labels)torch.LongTensor
of shape(batch_size, sequence_length)
, optional) — Labels for computing the masked language modeling loss. Indices should either be in[0, ..., config.vocab_size]
or -100 (seeinput_ids
docstring). Tokens with indices set to-100
are ignored (masked), the loss is only computed for the tokens with labels in[0, ..., config.vocab_size]
.[output_router_logits (](#transformers.SwitchTransformersForConditionalGeneration.forward.output_router_logits)bool
, optional, defaults toFalse
) — Whether or not to return the logits of all the routers. They are useful for computing the router loss, and should not be returned during inference.
Returns
Seq2SeqMoEOutput
or tuple(torch.FloatTensor)
A Seq2SeqMoEOutput
or a tuple of
torch.FloatTensor
(if return_dict=False
is passed or when config.return_dict=False
) comprising various
elements depending on the configuration (None
) and inputs.
The [SwitchTransformersForConditionalGeneration](/docs/transformers/v5.5.3/en/model_doc/switch_transformers#transformers.SwitchTransformersForConditionalGeneration) forward method, overrides the __call__
special method.
Although the recipe for forward pass needs to be defined within this function, one should call the
Module
instance afterwards instead of this since the former takes care of running the pre and post processing steps while the latter silently ignores them.
loss (
torch.FloatTensor
of shape(1,)
, optional, returned whenlabels
is provided) — Language modeling loss.logits (
torch.FloatTensor
of shape(batch_size, sequence_length, config.vocab_size)
) — Prediction scores of the language modeling head (scores for each vocabulary token before SoftMax).past_key_values (
EncoderDecoderCache
, optional, returned whenuse_cache=True
is passed or whenconfig.use_cache=True
) — It is a[EncoderDecoderCache](/docs/transformers/v5.5.3/en/internal/generation_utils#transformers.EncoderDecoderCache)instance. For more details, see our[kv cache guide](https://huggingface.co/docs/transformers/en/kv_cache).Contains pre-computed hidden-states (key and values in the self-attention blocks and in the cross-attention blocks) that can be used (see
past_key_values
input) to speed up sequential decoding.decoder_hidden_states (
tuple(torch.FloatTensor)
, optional, returned whenoutput_hidden_states=True
is passed or whenconfig.output_hidden_states=True
) — Tuple oftorch.FloatTensor
(one for the output of the embeddings, if the model has an embedding layer, + one for the output of each layer) of shape(batch_size, sequence_length, hidden_size)
.Hidden-states of the decoder at the output of each layer plus the initial embedding outputs.
decoder_attentions (
tuple(torch.FloatTensor)
, optional, returned whenoutput_attentions=True
is passed or whenconfig.output_attentions=True
) — Tuple oftorch.FloatTensor
(one for each layer) of shape(batch_size, num_heads, sequence_length, sequence_length)
.Attentions weights of the decoder, after the attention softmax, used to compute the weighted average in the self-attention heads.
decoder_router_logits (
tuple(torch.FloatTensor)
, optional, returned whenoutput_router_logits=True
is passed or whenconfig.add_router_probs=True
) — Tuple oftorch.FloatTensor
(one for each layer) of shape(batch_size, sequence_length, num_experts)
.Router logits of the decoder model, useful to compute the auxiliary loss for Mixture of Experts models.
cross_attentions (
tuple(torch.FloatTensor)
, optional, returned whenoutput_attentions=True
is passed or whenconfig.output_attentions=True
) — Tuple oftorch.FloatTensor
(one for each layer) of shape(batch_size, num_heads, sequence_length, sequence_length)
.Attentions weights of the decoder’s cross-attention layer, after the attention softmax, used to compute the weighted average in the cross-attention heads.
encoder_last_hidden_state (
torch.FloatTensor
of shape(batch_size, sequence_length, hidden_size)
, optional) — Sequence of hidden-states at the output of the last layer of the encoder of the model.encoder_hidden_states (
tuple(torch.FloatTensor)
, optional, returned whenoutput_hidden_states=True
is passed or whenconfig.output_hidden_states=True
) — Tuple oftorch.FloatTensor
(one for the output of the embeddings, if the model has an embedding layer, + one for the output of each layer) of shape(batch_size, sequence_length, hidden_size)
.Hidden-states of the encoder at the output of each layer plus the initial embedding outputs.
encoder_attentions (
tuple(torch.FloatTensor)
, optional, returned whenoutput_attentions=True
is passed or whenconfig.output_attentions=True
) — Tuple oftorch.FloatTensor
(one for each layer) of shape(batch_size, num_heads, sequence_length, sequence_length)
.Attentions weights of the encoder, after the attention softmax, used to compute the weighted average in the self-attention heads.
encoder_router_logits (
tuple(torch.FloatTensor)
, optional, returned whenoutput_router_logits=True
is passed or whenconfig.add_router_probs=True
) — Tuple oftorch.FloatTensor
(one for each layer) of shape(batch_size, sequence_length, num_experts)
.Router logits of the encoder model, useful to compute the auxiliary loss and z_loss for Mixture of Experts models.
SwitchTransformersEncoderModel
forward
[< source >](https://github.com/huggingface/transformers/blob/v5.5.3/src/transformers/models/switch_transformers/modeling_switch_transformers.py#L1069)
( input_ids: torch.LongTensor | None = None attention_mask: torch.FloatTensor | None = None inputs_embeds: torch.FloatTensor | None = None use_cache: bool | None = None **kwargs: typing_extensions.Unpack[transformers.utils.generic.TransformersKwargs] ) → MoEModelOutput
or tuple(torch.FloatTensor)
Parameters
[input_ids (](#transformers.SwitchTransformersEncoderModel.forward.input_ids)torch.LongTensor
of shape(batch_size, sequence_length)
, optional) — Indices of input sequence tokens in the vocabulary. Padding will be ignored by default.Indices can be obtained using
[AutoTokenizer](/docs/transformers/v5.5.3/en/model_doc/auto#transformers.AutoTokenizer). See[PreTrainedTokenizer.encode()](/docs/transformers/v5.5.3/en/internal/tokenization_utils#transformers.PreTrainedTokenizerBase.encode)and[PreTrainedTokenizer.call()](/docs/transformers/v5.5.3/en/internal/tokenization_utils#transformers.PreTrainedTokenizerBase.__call__)for details.[attention_mask (](#transformers.SwitchTransformersEncoderModel.forward.attention_mask)torch.FloatTensor
of shape(batch_size, sequence_length)
, optional) — Mask to avoid performing attention on padding token indices. Mask values selected in[0, 1]
:- 1 for tokens that are not masked,
- 0 for tokens that are masked.
[inputs_embeds (](#transformers.SwitchTransformersEncoderModel.forward.inputs_embeds)torch.FloatTensor
of shape(batch_size, sequence_length, hidden_size)
, optional) — Optionally, instead of passinginput_ids
you can choose to directly pass an embedded representation. This is useful if you want more control over how to convertinput_ids
indices into associated vectors than the model’s internal embedding lookup matrix.[use_cache (](#transformers.SwitchTransformersEncoderModel.forward.use_cache)bool
, optional) — If set toTrue
,past_key_values
key value states are returned and can be used to speed up decoding (seepast_key_values
).
Returns
MoEModelOutput
or tuple(torch.FloatTensor)
A MoEModelOutput
or a tuple of
torch.FloatTensor
(if return_dict=False
is passed or when config.return_dict=False
) comprising various
elements depending on the configuration (None
) and inputs.
The [SwitchTransformersEncoderModel](/docs/transformers/v5.5.3/en/model_doc/switch_transformers#transformers.SwitchTransformersEncoderModel) forward method, overrides the __call__
special method.
Although the recipe for forward pass needs to be defined within this function, one should call the
Module
instance afterwards instead of this since the former takes care of running the pre and post processing steps while the latter silently ignores them.
last_hidden_state (
torch.FloatTensor
of shape(batch_size, sequence_length, hidden_size)
) — Sequence of hidden-states at the output of the last layer of the model.hidden_states (
tuple(torch.FloatTensor)
, optional, returned whenoutput_hidden_states=True
is passed or whenconfig.output_hidden_states=True
) — Tuple oftorch.FloatTensor
(one for the output of the embeddings, if the model has an embedding layer, + one for the output of each layer) of shape(batch_size, sequence_length, hidden_size)
.Hidden-states of the model at the output of each layer plus the optional initial embedding outputs.
attentions (
tuple(torch.FloatTensor)
, optional, returned whenoutput_attentions=True
is passed or whenconfig.output_attentions=True
) — Tuple oftorch.FloatTensor
(one for each layer) of shape(batch_size, num_heads, sequence_length, sequence_length)
.Attentions weights after the attention softmax, used to compute the weighted average in the self-attention heads.
router_probs (
tuple(torch.FloatTensor)
, optional, returned whenoutput_router_probs=True
andconfig.add_router_probs=True
is passed or whenconfig.output_router_probs=True
) — Tuple oftorch.FloatTensor
(one for each layer) of shape(batch_size, sequence_length, num_experts)
.Raw router probabilities that are computed by MoE routers, these terms are used to compute the auxiliary loss and the z_loss for Mixture of Experts models.
[Update on GitHub](https://github.com/huggingface/transformers/blob/main/docs/source/en/model_doc/switch_transformers.md)