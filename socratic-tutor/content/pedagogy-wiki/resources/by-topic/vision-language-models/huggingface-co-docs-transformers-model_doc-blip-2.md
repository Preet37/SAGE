# Source: https://huggingface.co/docs/transformers/model_doc/blip-2
# Author: Hugging Face
# Author Slug: hugging-face
# Downloaded: 2026-04-06
# Words: 8100
Transformers documentation
BLIP-2
This model was released on 2023-01-30 and added to Hugging Face Transformers on 2023-02-09.
BLIP-2
Overview
The BLIP-2 model was proposed in [BLIP-2: Bootstrapping Language-Image Pre-training with Frozen Image Encoders and Large Language Models](https://huggingface.co/papers/2301.12597) by
Junnan Li, Dongxu Li, Silvio Savarese, Steven Hoi. BLIP-2 leverages frozen pre-trained image encoders and large language models (LLMs) by training a lightweight, 12-layer Transformer
encoder in between them, achieving state-of-the-art performance on various vision-language tasks. Most notably, BLIP-2 improves upon [Flamingo](https://huggingface.co/papers/2204.14198), an 80 billion parameter model, by 8.7%
on zero-shot VQAv2 with 54x fewer trainable parameters.
The abstract from the paper is the following:
The cost of vision-and-language pre-training has become increasingly prohibitive due to end-to-end training of large-scale models. This paper proposes BLIP-2, a generic and efficient pre-training strategy that bootstraps vision-language pre-training from off-the-shelf frozen pre-trained image encoders and frozen large language models. BLIP-2 bridges the modality gap with a lightweight Querying Transformer, which is pre-trained in two stages. The first stage bootstraps vision-language representation learning from a frozen image encoder. The second stage bootstraps vision-to-language generative learning from a frozen language model. BLIP-2 achieves state-of-the-art performance on various vision-language tasks, despite having significantly fewer trainable parameters than existing methods. For example, our model outperforms Flamingo80B by 8.7% on zero-shot VQAv2 with 54x fewer trainable parameters. We also demonstrate the model’s emerging capabilities of zero-shot image-to-text generation that can follow natural language instructions.
BLIP-2 architecture. Taken from the[original paper.](https://huggingface.co/papers/2301.12597)
This model was contributed by [nielsr](https://huggingface.co/nielsr).
The original code can be found [here](https://github.com/salesforce/LAVIS/tree/5ee63d688ba4cebff63acee04adaef2dee9af207).
Usage tips
- BLIP-2 can be used for conditional text generation given an image and an optional text prompt. At inference time, it’s recommended to use the
generate
method. - One can use
[Blip2Processor](/docs/transformers/v5.5.0/en/model_doc/blip-2#transformers.Blip2Processor)to prepare images for the model, and decode the predicted tokens ID’s back to text.
BLIP models after release v4.46 will raise warnings about adding
processor.num_query_tokens = {{num_query_tokens}}
and expand model embeddings layer to add special<image>
token. It is strongly recommended to add the attributes to the processor if you own the model checkpoint, or open a PR if it is not owned by you. Adding these attributes means that BLIP will add the number of query tokens required per image and expand the text with as many<image>
placeholders as there will be query tokens. Usually it is around 500 tokens per image, so make sure that the text is not truncated as otherwise there will be failure when merging the embeddings. The attributes can be obtained from model config, asmodel.config.num_query_tokens
and model embeddings expansion can be done by following[this link].
Resources
A list of official Hugging Face and community (indicated by 🌎) resources to help you get started with BLIP-2.
- Demo notebooks for BLIP-2 for image captioning, visual question answering (VQA) and chat-like conversations can be found
[here](https://github.com/NielsRogge/Transformers-Tutorials/tree/master/BLIP-2).
If you’re interested in submitting a resource to be included here, please feel free to open a Pull Request and we’ll review it! The resource should ideally demonstrate something new instead of duplicating an existing resource.
Blip2Config
class transformers.Blip2Config
[< source >](https://github.com/huggingface/transformers/blob/v5.5.0/src/transformers/models/blip_2/configuration_blip_2.py#L107)
( transformers_version: str | None = None architectures: list[str] | None = None output_hidden_states: bool | None = False return_dict: bool | None = True dtype: typing.Union[str, ForwardRef('torch.dtype'), NoneType] = None chunk_size_feed_forward: int = 0 is_encoder_decoder: bool = False id2label: dict[int, str] | dict[str, str] | None = None label2id: dict[str, int] | dict[str, str] | None = None problem_type: typing.Optional[typing.Literal['regression', 'single_label_classification', 'multi_label_classification']] = None vision_config: dict | transformers.configuration_utils.PreTrainedConfig | None = None qformer_config: dict | transformers.configuration_utils.PreTrainedConfig | None = None text_config: dict | transformers.configuration_utils.PreTrainedConfig | None = None num_query_tokens: int = 32 image_text_hidden_size: int = 256 image_token_index: int | None = None initializer_factor: float = 1.0 initializer_range: float = 0.02 )
Parameters
[vision_config (](#transformers.Blip2Config.vision_config)Union[dict, ~configuration_utils.PreTrainedConfig]
, optional) — The config object or dictionary of the vision backbone.[qformer_config (](#transformers.Blip2Config.qformer_config)dict
, optional) — Dictionary of configuration options used to initialize[Blip2QFormerConfig](/docs/transformers/v5.5.0/en/model_doc/blip-2#transformers.Blip2QFormerConfig).[text_config (](#transformers.Blip2Config.text_config)Union[dict, ~configuration_utils.PreTrainedConfig]
, optional) — The config object or dictionary of the text backbone.[num_query_tokens (](#transformers.Blip2Config.num_query_tokens)int
, optional, defaults to 32) — The number of query tokens passed through the Transformer.[image_text_hidden_size (](#transformers.Blip2Config.image_text_hidden_size)int
, optional, defaults to 256) — Dimensionality of the hidden state of the image-text fusion layer.[image_token_index (](#transformers.Blip2Config.image_token_index)int
, optional) — The image token index used as a placeholder for input images.[initializer_factor (](#transformers.Blip2Config.initializer_factor)float
, optional, defaults to1.0
) — A factor for initializing all weight matrices (should be kept to 1, used internally for initialization testing).[initializer_range (](#transformers.Blip2Config.initializer_range)float
, optional, defaults to0.02
) — The standard deviation of the truncated_normal_initializer for initializing all weight matrices.
This is the configuration class to store the configuration of a Blip 2Model. It is used to instantiate a Blip 2
model according to the specified arguments, defining the model architecture. Instantiating a configuration with the
defaults will yield a similar configuration to that of the [Salesforce/blip2-opt-2.7b](https://huggingface.co/Salesforce/blip2-opt-2.7b)
Configuration objects inherit from [PreTrainedConfig](/docs/transformers/v5.5.0/en/main_classes/configuration#transformers.PreTrainedConfig) and can be used to control the model outputs. Read the
documentation from [PreTrainedConfig](/docs/transformers/v5.5.0/en/main_classes/configuration#transformers.PreTrainedConfig) for more information.
Example:
>>> from transformers import (
... Blip2VisionConfig,
... Blip2QFormerConfig,
... OPTConfig,
... Blip2Config,
... Blip2ForConditionalGeneration,
... )
>>> # Initializing a Blip2Config with Salesforce/blip2-opt-2.7b style configuration
>>> configuration = Blip2Config()
>>> # Initializing a Blip2ForConditionalGeneration (with random weights) from the Salesforce/blip2-opt-2.7b style configuration
>>> model = Blip2ForConditionalGeneration(configuration)
>>> # Accessing the model configuration
>>> configuration = model.config
>>> # We can also initialize a Blip2Config from a Blip2VisionConfig, Blip2QFormerConfig and any PreTrainedConfig
>>> # Initializing BLIP-2 vision, BLIP-2 Q-Former and language model configurations
>>> vision_config = Blip2VisionConfig()
>>> qformer_config = Blip2QFormerConfig()
>>> text_config = OPTConfig()
>>> config = Blip2Config(vision_config=vision_config, qformer_config=qformer_config, text_config=text_config)
Blip2VisionConfig
class transformers.Blip2VisionConfig
[< source >](https://github.com/huggingface/transformers/blob/v5.5.0/src/transformers/models/blip_2/configuration_blip_2.py#L29)
( transformers_version: str | None = None architectures: list[str] | None = None output_hidden_states: bool | None = False return_dict: bool | None = True dtype: typing.Union[str, ForwardRef('torch.dtype'), NoneType] = None chunk_size_feed_forward: int = 0 is_encoder_decoder: bool = False id2label: dict[int, str] | dict[str, str] | None = None label2id: dict[str, int] | dict[str, str] | None = None problem_type: typing.Optional[typing.Literal['regression', 'single_label_classification', 'multi_label_classification']] = None hidden_size: int = 1408 intermediate_size: int = 6144 num_hidden_layers: int = 39 num_attention_heads: int = 16 image_size: int | list[int] | tuple[int, int] = 224 patch_size: int | list[int] | tuple[int, int] = 14 hidden_act: str = 'gelu' layer_norm_eps: float = 1e-06 attention_dropout: float | int = 0.0 initializer_range: float = 1e-10 qkv_bias: bool = True )
Parameters
[hidden_size (](#transformers.Blip2VisionConfig.hidden_size)int
, optional, defaults to1408
) — Dimension of the hidden representations.[intermediate_size (](#transformers.Blip2VisionConfig.intermediate_size)int
, optional, defaults to6144
) — Dimension of the MLP representations.[num_hidden_layers (](#transformers.Blip2VisionConfig.num_hidden_layers)int
, optional, defaults to39
) — Number of hidden layers in the Transformer decoder.[num_attention_heads (](#transformers.Blip2VisionConfig.num_attention_heads)int
, optional, defaults to16
) — Number of attention heads for each attention layer in the Transformer decoder.[image_size (](#transformers.Blip2VisionConfig.image_size)Union[int, list[int], tuple[int, int]]
, optional, defaults to224
) — The size (resolution) of each image.[patch_size (](#transformers.Blip2VisionConfig.patch_size)Union[int, list[int], tuple[int, int]]
, optional, defaults to14
) — The size (resolution) of each patch.[hidden_act (](#transformers.Blip2VisionConfig.hidden_act)str
, optional, defaults togelu
) — The non-linear activation function (function or string) in the decoder. For example,"gelu"
,"relu"
,"silu"
, etc.[layer_norm_eps (](#transformers.Blip2VisionConfig.layer_norm_eps)float
, optional, defaults to1e-06
) — The epsilon used by the layer normalization layers.[attention_dropout (](#transformers.Blip2VisionConfig.attention_dropout)Union[float, int]
, optional, defaults to0.0
) — The dropout ratio for the attention probabilities.[initializer_range (](#transformers.Blip2VisionConfig.initializer_range)float
, optional, defaults to1e-10
) — The standard deviation of the truncated_normal_initializer for initializing all weight matrices.[qkv_bias (](#transformers.Blip2VisionConfig.qkv_bias)bool
, optional, defaults toTrue
) — Whether to add a bias to the queries, keys and values.
This is the configuration class to store the configuration of a Blip 2Model. It is used to instantiate a Blip 2
model according to the specified arguments, defining the model architecture. Instantiating a configuration with the
defaults will yield a similar configuration to that of the [Salesforce/blip2-opt-2.7b](https://huggingface.co/Salesforce/blip2-opt-2.7b)
Configuration objects inherit from [PreTrainedConfig](/docs/transformers/v5.5.0/en/main_classes/configuration#transformers.PreTrainedConfig) and can be used to control the model outputs. Read the
documentation from [PreTrainedConfig](/docs/transformers/v5.5.0/en/main_classes/configuration#transformers.PreTrainedConfig) for more information.
Example:
>>> from transformers import Blip2VisionConfig, Blip2VisionModel
>>> # Initializing a Blip2VisionConfig with Salesforce/blip2-opt-2.7b style configuration
>>> configuration = Blip2VisionConfig()
>>> # Initializing a Blip2VisionModel (with random weights) from the Salesforce/blip2-opt-2.7b style configuration
>>> model = Blip2VisionModel(configuration)
>>> # Accessing the model configuration
>>> configuration = model.config
Blip2QFormerConfig
class transformers.Blip2QFormerConfig
[< source >](https://github.com/huggingface/transformers/blob/v5.5.0/src/transformers/models/blip_2/configuration_blip_2.py#L64)
( transformers_version: str | None = None architectures: list[str] | None = None output_hidden_states: bool | None = False return_dict: bool | None = True dtype: typing.Union[str, ForwardRef('torch.dtype'), NoneType] = None chunk_size_feed_forward: int = 0 is_encoder_decoder: bool = False id2label: dict[int, str] | dict[str, str] | None = None label2id: dict[str, int] | dict[str, str] | None = None problem_type: typing.Optional[typing.Literal['regression', 'single_label_classification', 'multi_label_classification']] = None vocab_size: int = 30522 hidden_size: int = 768 num_hidden_layers: int = 12 num_attention_heads: int = 12 intermediate_size: int = 3072 hidden_act: str = 'gelu' hidden_dropout_prob: float | int = 0.1 attention_probs_dropout_prob: float | int = 0.1 max_position_embeddings: int = 512 initializer_range: float = 0.02 layer_norm_eps: float = 1e-12 pad_token_id: int | None = 0 cross_attention_frequency: int = 2 encoder_hidden_size: int = 1408 use_qformer_text_input: bool = False )
Parameters
[vocab_size (](#transformers.Blip2QFormerConfig.vocab_size)int
, optional, defaults to30522
) — Vocabulary size of the model. Defines the number of different tokens that can be represented by theinput_ids
.[hidden_size (](#transformers.Blip2QFormerConfig.hidden_size)int
, optional, defaults to768
) — Dimension of the hidden representations.[num_hidden_layers (](#transformers.Blip2QFormerConfig.num_hidden_layers)int
, optional, defaults to12
) — Number of hidden layers in the Transformer decoder.[num_attention_heads (](#transformers.Blip2QFormerConfig.num_attention_heads)int
, optional, defaults to12
) — Number of attention heads for each attention layer in the Transformer decoder.[intermediate_size (](#transformers.Blip2QFormerConfig.intermediate_size)int
, optional, defaults to3072
) — Dimension of the MLP representations.[hidden_act (](#transformers.Blip2QFormerConfig.hidden_act)str
, optional, defaults togelu
) — The non-linear activation function (function or string) in the decoder. For example,"gelu"
,"relu"
,"silu"
, etc.[hidden_dropout_prob (](#transformers.Blip2QFormerConfig.hidden_dropout_prob)Union[float, int]
, optional, defaults to0.1
) — The dropout probability for all fully connected layers in the embeddings, encoder, and pooler.[attention_probs_dropout_prob (](#transformers.Blip2QFormerConfig.attention_probs_dropout_prob)Union[float, int]
, optional, defaults to0.1
) — The dropout ratio for the attention probabilities.[max_position_embeddings (](#transformers.Blip2QFormerConfig.max_position_embeddings)int
, optional, defaults to512
) — The maximum sequence length that this model might ever be used with.[initializer_range (](#transformers.Blip2QFormerConfig.initializer_range)float
, optional, defaults to0.02
) — The standard deviation of the truncated_normal_initializer for initializing all weight matrices.[layer_norm_eps (](#transformers.Blip2QFormerConfig.layer_norm_eps)float
, optional, defaults to1e-12
) — The epsilon used by the layer normalization layers.[pad_token_id (](#transformers.Blip2QFormerConfig.pad_token_id)int
, optional, defaults to0
) — Token id used for padding in the vocabulary.[cross_attention_frequency (](#transformers.Blip2QFormerConfig.cross_attention_frequency)int
, optional, defaults to 2) — The frequency of adding cross-attention to the Transformer layers.[encoder_hidden_size (](#transformers.Blip2QFormerConfig.encoder_hidden_size)int
, optional, defaults to1408
) — Dimension of the hidden representations.[use_qformer_text_input (](#transformers.Blip2QFormerConfig.use_qformer_text_input)bool
, optional, defaults toFalse
) — Whether to use BERT-style embeddings.
This is the configuration class to store the configuration of a Blip 2Model. It is used to instantiate a Blip 2
model according to the specified arguments, defining the model architecture. Instantiating a configuration with the
defaults will yield a similar configuration to that of the [Salesforce/blip2-opt-2.7b](https://huggingface.co/Salesforce/blip2-opt-2.7b)
Configuration objects inherit from [PreTrainedConfig](/docs/transformers/v5.5.0/en/main_classes/configuration#transformers.PreTrainedConfig) and can be used to control the model outputs. Read the
documentation from [PreTrainedConfig](/docs/transformers/v5.5.0/en/main_classes/configuration#transformers.PreTrainedConfig) for more information.
Examples:
>>> from transformers import Blip2QFormerConfig, Blip2QFormerModel
>>> # Initializing a BLIP-2 Salesforce/blip2-opt-2.7b style configuration
>>> configuration = Blip2QFormerConfig()
>>> # Initializing a model (with random weights) from the Salesforce/blip2-opt-2.7b style configuration
>>> model = Blip2QFormerModel(configuration)
>>> # Accessing the model configuration
>>> configuration = model.config
Blip2Processor
class transformers.Blip2Processor
[< source >](https://github.com/huggingface/transformers/blob/v5.5.0/src/transformers/models/blip_2/processing_blip_2.py#L45)
( image_processor tokenizer num_query_tokens = None **kwargs )
Constructs a Blip2Processor which wraps a image processor and a tokenizer into a single processor.
[Blip2Processor](/docs/transformers/v5.5.0/en/model_doc/blip-2#transformers.Blip2Processor) offers all the functionalities of [BlipImageProcessor](/docs/transformers/v5.5.0/en/model_doc/blip#transformers.BlipImageProcessor) and [GPT2Tokenizer](/docs/transformers/v5.5.0/en/model_doc/gpt2#transformers.GPT2Tokenizer). See the
[~BlipImageProcessor](/docs/transformers/v5.5.0/en/model_doc/blip#transformers.BlipImageProcessor) and [~GPT2Tokenizer](/docs/transformers/v5.5.0/en/model_doc/gpt2#transformers.GPT2Tokenizer) for more information.
__call__
[< source >](https://github.com/huggingface/transformers/blob/v5.5.0/src/transformers/models/blip_2/processing_blip_2.py#L61)
( images: typing.Union[ForwardRef('PIL.Image.Image'), numpy.ndarray, ForwardRef('torch.Tensor'), list['PIL.Image.Image'], list[numpy.ndarray], list['torch.Tensor'], NoneType] = None text: str | list[str] | None = None **kwargs: typing_extensions.Unpack[transformers.models.blip_2.processing_blip_2.Blip2ProcessorKwargs] ) → ~tokenization_utils_base.BatchEncoding
Parameters
[images (](#transformers.Blip2Processor.__call__.images)Union[PIL.Image.Image, numpy.ndarray, torch.Tensor, list[PIL.Image.Image], list[numpy.ndarray], list[torch.Tensor]]
, optional) — Image to preprocess. Expects a single or batch of images with pixel values ranging from 0 to 255. If passing in images with pixel values between 0 and 1, setdo_rescale=False
.[text (](#transformers.Blip2Processor.__call__.text)Union[str, list[str]]
, optional) — The sequence or batch of sequences to be encoded. Each sequence can be a string or a list of strings (pretokenized string). If you pass a pretokenized input, setis_split_into_words=True
to avoid ambiguity with batched inputs.[return_tensors (](#transformers.Blip2Processor.__call__.return_tensors)str
or[TensorType](/docs/transformers/v5.5.0/en/internal/file_utils#transformers.TensorType), optional) — If set, will return tensors of a particular framework. Acceptable values are:'pt'
: Return PyTorchtorch.Tensor
objects.'np'
: Return NumPynp.ndarray
objects.
[**kwargs (](#transformers.Blip2Processor.__call__.*kwargs)[ProcessingKwargs](/docs/transformers/v5.5.0/en/main_classes/processors#transformers.ProcessingKwargs), optional) — Additional processing options for each modality (text, images, videos, audio). Model-specific parameters are listed above; see the TypedDict class for the complete list of supported arguments.
Returns
~tokenization_utils_base.BatchEncoding
- data (
dict
, optional) — Dictionary of lists/arrays/tensors returned by the__call__
/encode_plus
/batch_encode_plus
methods (‘input_ids’, ‘attention_mask’, etc.). - encoding (
tokenizers.Encoding
orSequence[tokenizers.Encoding]
, optional) — If the tokenizer is a fast tokenizer which outputs additional information like mapping from word/character space to token space thetokenizers.Encoding
instance or list of instance (for batches) hold this information. - tensor_type (
Union[None, str, TensorType]
, optional) — You can give a tensor_type here to convert the lists of integers in PyTorch/Numpy Tensors at initialization. - prepend_batch_axis (
bool
, optional, defaults toFalse
) — Whether or not to add a batch axis when converting to tensors (seetensor_type
above). Note that this parameter has an effect if the parametertensor_type
is set, otherwise has no effect. - n_sequences (
int
, optional) — You can give a tensor_type here to convert the lists of integers in PyTorch/Numpy Tensors at initialization.
Blip2VisionModel
class transformers.Blip2VisionModel
[< source >](https://github.com/huggingface/transformers/blob/v5.5.0/src/transformers/models/blip_2/modeling_blip_2.py#L483)
( config: Blip2VisionConfig )
Parameters
[config (](#transformers.Blip2VisionModel.config)[Blip2VisionConfig](/docs/transformers/v5.5.0/en/model_doc/blip-2#transformers.Blip2VisionConfig)) — Model configuration class with all the parameters of the model. Initializing with a config file does not load the weights associated with the model, only the configuration. Check out the[from_pretrained()](/docs/transformers/v5.5.0/en/main_classes/model#transformers.PreTrainedModel.from_pretrained)method to load the model weights.
The bare Blip 2 Model outputting raw hidden-states without any specific head on top.
This model inherits from [PreTrainedModel](/docs/transformers/v5.5.0/en/main_classes/model#transformers.PreTrainedModel). Check the superclass documentation for the generic methods the
library implements for all its model (such as downloading or saving, resizing the input embeddings, pruning heads
etc.)
This model is also a PyTorch [torch.nn.Module](https://pytorch.org/docs/stable/nn.html#torch.nn.Module) subclass.
Use it as a regular PyTorch Module and refer to the PyTorch documentation for all matter related to general usage
and behavior.
forward
[< source >](https://github.com/huggingface/transformers/blob/v5.5.0/src/transformers/models/blip_2/modeling_blip_2.py#L503)
( pixel_values: torch.FloatTensor | None = None interpolate_pos_encoding: bool = False **kwargs: typing_extensions.Unpack[transformers.utils.generic.TransformersKwargs] ) → [BaseModelOutputWithPooling](/docs/transformers/v5.5.0/en/main_classes/output#transformers.modeling_outputs.BaseModelOutputWithPooling) or tuple(torch.FloatTensor)
Parameters
[pixel_values (](#transformers.Blip2VisionModel.forward.pixel_values)torch.FloatTensor
of shape(batch_size, num_channels, image_size, image_size)
, optional) — The tensors corresponding to the input images. Pixel values can be obtained using[BlipImageProcessor](/docs/transformers/v5.5.0/en/model_doc/blip#transformers.BlipImageProcessor). SeeBlipImageProcessor.__call__()
for details ([Blip2Processor](/docs/transformers/v5.5.0/en/model_doc/blip-2#transformers.Blip2Processor)uses[BlipImageProcessor](/docs/transformers/v5.5.0/en/model_doc/blip#transformers.BlipImageProcessor)for processing images).[interpolate_pos_encoding (](#transformers.Blip2VisionModel.forward.interpolate_pos_encoding)bool
, optional, defaults toFalse
) — Whether to interpolate the pre-trained position encodings.
Returns
[BaseModelOutputWithPooling](/docs/transformers/v5.5.0/en/main_classes/output#transformers.modeling_outputs.BaseModelOutputWithPooling) or tuple(torch.FloatTensor)
A [BaseModelOutputWithPooling](/docs/transformers/v5.5.0/en/main_classes/output#transformers.modeling_outputs.BaseModelOutputWithPooling) or a tuple of
torch.FloatTensor
(if return_dict=False
is passed or when config.return_dict=False
) comprising various
elements depending on the configuration ([Blip2Config](/docs/transformers/v5.5.0/en/model_doc/blip-2#transformers.Blip2Config)) and inputs.
The [Blip2VisionModel](/docs/transformers/v5.5.0/en/model_doc/blip-2#transformers.Blip2VisionModel) forward method, overrides the __call__
special method.
Although the recipe for forward pass needs to be defined within this function, one should call the
Module
instance afterwards instead of this since the former takes care of running the pre and post processing steps while the latter silently ignores them.
last_hidden_state (
torch.FloatTensor
of shape(batch_size, sequence_length, hidden_size)
) — Sequence of hidden-states at the output of the last layer of the model.pooler_output (
torch.FloatTensor
of shape(batch_size, hidden_size)
) — Last layer hidden-state of the first token of the sequence (classification token) after further processing through the layers used for the auxiliary pretraining task. E.g. for BERT-family of models, this returns the classification token after processing through a linear layer and a tanh activation function. The linear layer weights are trained from the next sentence prediction (classification) objective during pretraining.hidden_states (
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
Blip2QFormerModel
class transformers.Blip2QFormerModel
[< source >](https://github.com/huggingface/transformers/blob/v5.5.0/src/transformers/models/blip_2/modeling_blip_2.py#L879)
( config: Blip2QFormerConfig )
Parameters
[config (](#transformers.Blip2QFormerModel.config)[Blip2QFormerConfig](/docs/transformers/v5.5.0/en/model_doc/blip-2#transformers.Blip2QFormerConfig)) — Model configuration class with all the parameters of the model. Initializing with a config file does not load the weights associated with the model, only the configuration. Check out the[from_pretrained()](/docs/transformers/v5.5.0/en/main_classes/model#transformers.PreTrainedModel.from_pretrained)method to load the model weights.
BLIP-2 Querying Transformer (Q-Former).
This model inherits from [PreTrainedModel](/docs/transformers/v5.5.0/en/main_classes/model#transformers.PreTrainedModel). Check the superclass documentation for the generic methods the
library implements for all its model (such as downloading or saving, resizing the input embeddings, pruning heads
etc.)
This model is also a PyTorch [torch.nn.Module](https://pytorch.org/docs/stable/nn.html#torch.nn.Module) subclass.
Use it as a regular PyTorch Module and refer to the PyTorch documentation for all matter related to general usage
and behavior.
forward
[< source >](https://github.com/huggingface/transformers/blob/v5.5.0/src/transformers/models/blip_2/modeling_blip_2.py#L959)
( query_embeds: FloatTensor query_length: int | None = None attention_mask: torch.FloatTensor | None = None encoder_hidden_states: torch.FloatTensor | None = None encoder_attention_mask: torch.FloatTensor | None = None **kwargs: typing_extensions.Unpack[transformers.utils.generic.TransformersKwargs] ) → [BaseModelOutputWithPoolingAndCrossAttentions](/docs/transformers/v5.5.0/en/main_classes/output#transformers.modeling_outputs.BaseModelOutputWithPoolingAndCrossAttentions) or tuple(torch.FloatTensor)
Parameters
[query_embeds (](#transformers.Blip2QFormerModel.forward.query_embeds)torch.FloatTensor
of shape(batch_size, sequence_length, hidden_size)
) — Hidden states to be used in the attention computation. If cross-attention, will be used for the query (i.e., key and value will use the encoder_hidden_states).[query_length (](#transformers.Blip2QFormerModel.forward.query_length)int
, optional) — Length of the query, usually based on the number of query tokens. If no value is provided, query_length will be inferred by the query_embeds.[attention_mask (](#transformers.Blip2QFormerModel.forward.attention_mask)torch.FloatTensor
of shape(batch_size, sequence_length)
, optional) — Mask to avoid performing attention on padding token indices. Mask values selected in[0, 1]
:- 1 for tokens that are not masked,
- 0 for tokens that are masked.
[encoder_hidden_states (](#transformers.Blip2QFormerModel.forward.encoder_hidden_states)torch.FloatTensor
of shape(batch_size, sequence_length, hidden_size)
, optional) — Sequence of hidden-states at the output of the last layer of the encoder. Used in the cross-attention if the model is configured as a decoder.[encoder_attention_mask (](#transformers.Blip2QFormerModel.forward.encoder_attention_mask)torch.FloatTensor
of shape(batch_size, sequence_length)
, optional) — Mask to avoid performing attention on the padding token indices of the encoder input. This mask is used in the cross-attention if the model is configured as a decoder. Mask values selected in[0, 1]
:- 1 for tokens that are not masked,
- 0 for tokens that are masked.
Returns
[BaseModelOutputWithPoolingAndCrossAttentions](/docs/transformers/v5.5.0/en/main_classes/output#transformers.modeling_outputs.BaseModelOutputWithPoolingAndCrossAttentions) or tuple(torch.FloatTensor)
A [BaseModelOutputWithPoolingAndCrossAttentions](/docs/transformers/v5.5.0/en/main_classes/output#transformers.modeling_outputs.BaseModelOutputWithPoolingAndCrossAttentions) or a tuple of
torch.FloatTensor
(if return_dict=False
is passed or when config.return_dict=False
) comprising various
elements depending on the configuration ([Blip2Config](/docs/transformers/v5.5.0/en/model_doc/blip-2#transformers.Blip2Config)) and inputs.
The [Blip2QFormerModel](/docs/transformers/v5.5.0/en/model_doc/blip-2#transformers.Blip2QFormerModel) forward method, overrides the __call__
special method.
Although the recipe for forward pass needs to be defined within this function, one should call the
Module
instance afterwards instead of this since the former takes care of running the pre and post processing steps while the latter silently ignores them.
last_hidden_state (
torch.FloatTensor
of shape(batch_size, sequence_length, hidden_size)
) — Sequence of hidden-states at the output of the last layer of the model.pooler_output (
torch.FloatTensor
of shape(batch_size, hidden_size)
) — Last layer hidden-state of the first token of the sequence (classification token) after further processing through the layers used for the auxiliary pretraining task. E.g. for BERT-family of models, this returns the classification token after processing through a linear layer and a tanh activation function. The linear layer weights are trained from the next sentence prediction (classification) objective during pretraining.hidden_states (
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
cross_attentions (
tuple(torch.FloatTensor)
, optional, returned whenoutput_attentions=True
andconfig.add_cross_attention=True
is passed or whenconfig.output_attentions=True
) — Tuple oftorch.FloatTensor
(one for each layer) of shape(batch_size, num_heads, sequence_length, sequence_length)
.Attentions weights of the decoder’s cross-attention layer, after the attention softmax, used to compute the weighted average in the cross-attention heads.
past_key_values (
Cache
, optional, returned whenuse_cache=True
is passed or whenconfig.use_cache=True
) — It is a[Cache](/docs/transformers/v5.5.0/en/internal/generation_utils#transformers.Cache)instance. For more details, see our[kv cache guide](https://huggingface.co/docs/transformers/en/kv_cache).Contains pre-computed hidden-states (key and values in the self-attention blocks and optionally if
config.is_encoder_decoder=True
in the cross-attention blocks) that can be used (seepast_key_values
input) to speed up sequential decoding.
Blip2Model
class transformers.Blip2Model
[< source >](https://github.com/huggingface/transformers/blob/v5.5.0/src/transformers/models/blip_2/modeling_blip_2.py#L1045)
( config: Blip2Config )
Parameters
[config (](#transformers.Blip2Model.config)[Blip2Config](/docs/transformers/v5.5.0/en/model_doc/blip-2#transformers.Blip2Config)) — Model configuration class with all the parameters of the model. Initializing with a config file does not load the weights associated with the model, only the configuration. Check out the[from_pretrained()](/docs/transformers/v5.5.0/en/main_classes/model#transformers.PreTrainedModel.from_pretrained)method to load the model weights.
BLIP-2 Model for generating text and image features. The model consists of a vision encoder, Querying Transformer (Q-Former) and a language model.
This model inherits from [PreTrainedModel](/docs/transformers/v5.5.0/en/main_classes/model#transformers.PreTrainedModel). Check the superclass documentation for the generic methods the
library implements for all its model (such as downloading or saving, resizing the input embeddings, pruning heads
etc.)
This model is also a PyTorch [torch.nn.Module](https://pytorch.org/docs/stable/nn.html#torch.nn.Module) subclass.
Use it as a regular PyTorch Module and refer to the PyTorch documentation for all matter related to general usage
and behavior.
forward
[< source >](https://github.com/huggingface/transformers/blob/v5.5.0/src/transformers/models/blip_2/modeling_blip_2.py#L1246)
( pixel_values: FloatTensor input_ids: FloatTensor attention_mask: torch.LongTensor | None = None decoder_input_ids: torch.LongTensor | None = None decoder_attention_mask: torch.LongTensor | None = None labels: torch.LongTensor | None = None interpolate_pos_encoding: bool = False **kwargs: typing_extensions.Unpack[transformers.utils.generic.TransformersKwargs] ) → Blip2ForConditionalGenerationModelOutput
or tuple(torch.FloatTensor)
Parameters
[pixel_values (](#transformers.Blip2Model.forward.pixel_values)torch.FloatTensor
of shape(batch_size, num_channels, image_size, image_size)
) — The tensors corresponding to the input images. Pixel values can be obtained using[BlipImageProcessor](/docs/transformers/v5.5.0/en/model_doc/blip#transformers.BlipImageProcessor). SeeBlipImageProcessor.__call__()
for details ([Blip2Processor](/docs/transformers/v5.5.0/en/model_doc/blip-2#transformers.Blip2Processor)uses[BlipImageProcessor](/docs/transformers/v5.5.0/en/model_doc/blip#transformers.BlipImageProcessor)for processing images).[input_ids (](#transformers.Blip2Model.forward.input_ids)torch.FloatTensor
of shape(batch_size, sequence_length)
) — Indices of input sequence tokens in the vocabulary. Padding will be ignored by default.Indices can be obtained using
[AutoTokenizer](/docs/transformers/v5.5.0/en/model_doc/auto#transformers.AutoTokenizer). See[PreTrainedTokenizer.encode()](/docs/transformers/v5.5.0/en/internal/tokenization_utils#transformers.PreTrainedTokenizerBase.encode)and[PreTrainedTokenizer.call()](/docs/transformers/v5.5.0/en/internal/tokenization_utils#transformers.PreTrainedTokenizerBase.__call__)for details.[attention_mask (](#transformers.Blip2Model.forward.attention_mask)torch.LongTensor
of shape(batch_size, sequence_length)
, optional) — Mask to avoid performing attention on padding token indices. Mask values selected in[0, 1]
:- 1 for tokens that are not masked,
- 0 for tokens that are masked.
[decoder_input_ids (](#transformers.Blip2Model.forward.decoder_input_ids)torch.LongTensor
of shape(batch_size, target_sequence_length)
, optional) — Indices of decoder input sequence tokens in the vocabulary.Indices can be obtained using
[AutoTokenizer](/docs/transformers/v5.5.0/en/model_doc/auto#transformers.AutoTokenizer). See[PreTrainedTokenizer.encode()](/docs/transformers/v5.5.0/en/internal/tokenization_utils#transformers.PreTrainedTokenizerBase.encode)and[PreTrainedTokenizer.call()](/docs/transformers/v5.5.0/en/internal/tokenization_utils#transformers.PreTrainedTokenizerBase.__call__)for details.[decoder_attention_mask (](#transformers.Blip2Model.forward.decoder_attention_mask)torch.BoolTensor
of shape(batch_size, target_sequence_length)
, optional) — Default behavior: generate a tensor that ignores pad tokens indecoder_input_ids
. Causal mask will also be used by default.Only relevant in case an encoder-decoder language model (like T5) is used.
[labels (](#transformers.Blip2Model.forward.labels)torch.LongTensor
of shape(batch_size, sequence_length)
, optional) — Labels for computing the masked language modeling loss. Indices should either be in[0, ..., config.vocab_size]
or -100 (seeinput_ids
docstring). Tokens with indices set to-100
are ignored (masked), the loss is only computed for the tokens with labels in[0, ..., config.vocab_size]
.[interpolate_pos_encoding (](#transformers.Blip2Model.forward.interpolate_pos_encoding)bool
, optional, defaults toFalse
) — Whether to interpolate the pre-trained position encodings.
Returns
Blip2ForConditionalGenerationModelOutput
or tuple(torch.FloatTensor)
A Blip2ForConditionalGenerationModelOutput
or a tuple of
torch.FloatTensor
(if return_dict=False
is passed or when config.return_dict=False
) comprising various
elements depending on the configuration ([Blip2Config](/docs/transformers/v5.5.0/en/model_doc/blip-2#transformers.Blip2Config)) and inputs.
The [Blip2Model](/docs/transformers/v5.5.0/en/model_doc/blip-2#transformers.Blip2Model) forward method, overrides the __call__
special method.
Although the recipe for forward pass needs to be defined within this function, one should call the
Module
instance afterwards instead of this since the former takes care of running the pre and post processing steps while the latter silently ignores them.
- loss (
torch.FloatTensor
, optional, returned whenlabels
is provided,torch.FloatTensor
of shape(1,)
) — Language modeling loss from the language model. - logits (
torch.FloatTensor
of shape(batch_size, sequence_length, config.vocab_size)
) — Prediction scores of the language modeling head of the language model. - vision_outputs (
~modeling_outputs.BaseModelOutputWithPooling
, optional, defaults toNone
) — Outputs of the vision encoder. - qformer_outputs (
~modeling_outputs.BaseModelOutputWithPoolingAndCrossAttentions
, optional, defaults toNone
) — Outputs of the Q-Former (Querying Transformer). - language_model_outputs (
CausalLMOutputWithPast
orSeq2SeqLMOutput
) — Outputs of the language model.
Examples:
>>> from PIL import Image
>>> import httpx
>>> from io import BytesIO
>>> from transformers import Blip2Processor, Blip2Model
>>> import torch
>>> device = "cuda" if torch.cuda.is_available() else "cpu"
>>> processor = Blip2Processor.from_pretrained("Salesforce/blip2-opt-2.7b")
>>> model = Blip2Model.from_pretrained("Salesforce/blip2-opt-2.7b", dtype=torch.float16)
>>> model.to(device)
>>> url = "http://images.cocodataset.org/val2017/000000039769.jpg"
>>> with httpx.stream("GET", url) as response:
... image = Image.open(BytesIO(response.read()))
>>> prompt = "Question: how many cats are there? Answer:"
>>> inputs = processor(images=image, text=prompt, return_tensors="pt").to(device, torch.float16)
>>> outputs = model(**inputs)
get_text_features
[< source >](https://github.com/huggingface/transformers/blob/v5.5.0/src/transformers/models/blip_2/modeling_blip_2.py#L1088)
( input_ids: Tensor attention_mask: torch.Tensor | None = None decoder_input_ids: torch.Tensor | None = None decoder_attention_mask: torch.Tensor | None = None labels: torch.Tensor | None = None **kwargs: typing_extensions.Unpack[transformers.utils.generic.TransformersKwargs] ) → [BaseModelOutputWithPooling](/docs/transformers/v5.5.0/en/main_classes/output#transformers.modeling_outputs.BaseModelOutputWithPooling) or tuple(torch.FloatTensor)
Parameters
[input_ids (](#transformers.Blip2Model.get_text_features.input_ids)torch.Tensor
of shape(batch_size, sequence_length)
) — Indices of input sequence tokens in the vocabulary. Padding will be ignored by default.Indices can be obtained using
[AutoTokenizer](/docs/transformers/v5.5.0/en/model_doc/auto#transformers.AutoTokenizer). See[PreTrainedTokenizer.encode()](/docs/transformers/v5.5.0/en/internal/tokenization_utils#transformers.PreTrainedTokenizerBase.encode)and[PreTrainedTokenizer.call()](/docs/transformers/v5.5.0/en/internal/tokenization_utils#transformers.PreTrainedTokenizerBase.__call__)for details.[attention_mask (](#transformers.Blip2Model.get_text_features.attention_mask)torch.Tensor
of shape(batch_size, sequence_length)
, optional) — Mask to avoid performing attention on padding token indices. Mask values selected in[0, 1]
:- 1 for tokens that are not masked,
- 0 for tokens that are masked.
[decoder_input_ids (](#transformers.Blip2Model.get_text_features.decoder_input_ids)torch.LongTensor
of shape(batch_size, target_sequence_length)
, optional) — Indices of decoder input sequence tokens in the vocabulary.Indices can be obtained using
[AutoTokenizer](/docs/transformers/v5.5.0/en/model_doc/auto#transformers.AutoTokenizer). See[PreTrainedTokenizer.encode()](/docs/transformers/v5.5.0/en/internal/tokenization_utils#transformers.PreTrainedTokenizerBase.encode)and[PreTrainedTokenizer.call()](/docs/transformers/v5.5.0/en/internal/tokenization_utils#transformers.PreTrainedTokenizerBase.__call__)for details.T5 uses the
pad_token_id
as the starting token fordecoder_input_ids
generation. Ifpast_key_values
is used, optionally only the lastdecoder_input_ids
have to be input (seepast_key_values
).To know more on how to prepare
decoder_input_ids
for pretraining take a look at[T5 Training](./t5#training).[decoder_attention_mask (](#transformers.Blip2Model.get_text_features.decoder_attention_mask)torch.BoolTensor
of shape(batch_size, target_sequence_length)
, optional) — Default behavior: generate a tensor that ignores pad tokens indecoder_input_ids
. Causal mask will also be used by default.[labels (](#transformers.Blip2Model.get_text_features.labels)torch.Tensor
of shape(batch_size, sequence_length)
, optional) — Labels for computing the masked language modeling loss. Indices should either be in[0, ..., config.vocab_size]
or -100 (seeinput_ids
docstring). Tokens with indices set to-100
are ignored (masked), the loss is only computed for the tokens with labels in[0, ..., config.vocab_size]
.
Returns
[BaseModelOutputWithPooling](/docs/transformers/v5.5.0/en/main_classes/output#transformers.modeling_outputs.BaseModelOutputWithPooling) or tuple(torch.FloatTensor)
A [BaseModelOutputWithPooling](/docs/transformers/v5.5.0/en/main_classes/output#transformers.modeling_outputs.BaseModelOutputWithPooling) or a tuple of
torch.FloatTensor
(if return_dict=False
is passed or when config.return_dict=False
) comprising various
elements depending on the configuration ([Blip2Config](/docs/transformers/v5.5.0/en/model_doc/blip-2#transformers.Blip2Config)) and inputs.
last_hidden_state (
torch.FloatTensor
of shape(batch_size, sequence_length, hidden_size)
) — Sequence of hidden-states at the output of the last layer of the model.pooler_output (
torch.FloatTensor
of shape(batch_size, hidden_size)
) — Last layer hidden-state of the first token of the sequence (classification token) after further processing through the layers used for the auxiliary pretraining task. E.g. for BERT-family of models, this returns the classification token after processing through a linear layer and a tanh activation function. The linear layer weights are trained from the next sentence prediction (classification) objective during pretraining.hidden_states (
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
Examples:
>>> import torch
>>> from transformers import AutoTokenizer, Blip2Model
>>> model = Blip2Model.from_pretrained("Salesforce/blip2-opt-2.7b")
>>> tokenizer = AutoTokenizer.from_pretrained("Salesforce/blip2-opt-2.7b")
>>> inputs = tokenizer(["a photo of a cat"], padding=True, return_tensors="pt")
>>> with torch.inference_mode():
... text_features = model.get_text_features(**inputs)
get_image_features
[< source >](https://github.com/huggingface/transformers/blob/v5.5.0/src/transformers/models/blip_2/modeling_blip_2.py#L1150)
( pixel_values: FloatTensor interpolate_pos_encoding: bool = False **kwargs: typing_extensions.Unpack[transformers.utils.generic.TransformersKwargs] ) → [BaseModelOutputWithPooling](/docs/transformers/v5.5.0/en/main_classes/output#transformers.modeling_outputs.BaseModelOutputWithPooling) or tuple(torch.FloatTensor)
Parameters
[pixel_values (](#transformers.Blip2Model.get_image_features.pixel_values)torch.FloatTensor
of shape(batch_size, num_channels, image_size, image_size)
) — The tensors corresponding to the input images. Pixel values can be obtained using[BlipImageProcessor](/docs/transformers/v5.5.0/en/model_doc/blip#transformers.BlipImageProcessor). SeeBlipImageProcessor.__call__()
for details ([Blip2Processor](/docs/transformers/v5.5.0/en/model_doc/blip-2#transformers.Blip2Processor)uses[BlipImageProcessor](/docs/transformers/v5.5.0/en/model_doc/blip#transformers.BlipImageProcessor)for processing images).[interpolate_pos_encoding (](#transformers.Blip2Model.get_image_features.interpolate_pos_encoding)bool
, optional, defaults toFalse
) — Whether to interpolate the pre-trained position encodings.
Returns
[BaseModelOutputWithPooling](/docs/transformers/v5.5.0/en/main_classes/output#transformers.modeling_outputs.BaseModelOutputWithPooling) or tuple(torch.FloatTensor)
A [BaseModelOutputWithPooling](/docs/transformers/v5.5.0/en/main_classes/output#transformers.modeling_outputs.BaseModelOutputWithPooling) or a tuple of
torch.FloatTensor
(if return_dict=False
is passed or when config.return_dict=False
) comprising various
elements depending on the configuration ([Blip2Config](/docs/transformers/v5.5.0/en/model_doc/blip-2#transformers.Blip2Config)) and inputs.
last_hidden_state (
torch.FloatTensor
of shape(batch_size, sequence_length, hidden_size)
) — Sequence of hidden-states at the output of the last layer of the model.pooler_output (
torch.FloatTensor
of shape(batch_size, hidden_size)
) — Last layer hidden-state of the first token of the sequence (classification token) after further processing through the layers used for the auxiliary pretraining task. E.g. for BERT-family of models, this returns the classification token after processing through a linear layer and a tanh activation function. The linear layer weights are trained from the next sentence prediction (classification) objective during pretraining.hidden_states (
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
Examples:
>>> import torch
>>> from transformers import AutoProcessor, Blip2Model
>>> from transformers.image_utils import load_image
>>> model = Blip2Model.from_pretrained("Salesforce/blip2-opt-2.7b")
>>> processor = AutoProcessor.from_pretrained("Salesforce/blip2-opt-2.7b")
>>> url = "http://images.cocodataset.org/val2017/000000039769.jpg"
>>> image = load_image(url)
>>> inputs = processor(images=image, return_tensors="pt")
>>> with torch.inference_mode():
... image_outputs = model.get_image_features(**inputs)
get_qformer_features
[< source >](https://github.com/huggingface/transformers/blob/v5.5.0/src/transformers/models/blip_2/modeling_blip_2.py#L1181)
( pixel_values: FloatTensor interpolate_pos_encoding: bool = False ) → qformer_outputs (torch.FloatTensor
)
Parameters
[pixel_values (](#transformers.Blip2Model.get_qformer_features.pixel_values)torch.FloatTensor
of shape(batch_size, num_channels, image_size, image_size)
) — The tensors corresponding to the input images. Pixel values can be obtained using[BlipImageProcessor](/docs/transformers/v5.5.0/en/model_doc/blip#transformers.BlipImageProcessor). SeeBlipImageProcessor.__call__()
for details ([Blip2Processor](/docs/transformers/v5.5.0/en/model_doc/blip-2#transformers.Blip2Processor)uses[BlipImageProcessor](/docs/transformers/v5.5.0/en/model_doc/blip#transformers.BlipImageProcessor)for processing images).[interpolate_pos_encoding (](#transformers.Blip2Model.get_qformer_features.interpolate_pos_encoding)bool
, optional, defaults toFalse
) — Whether to interpolate the pre-trained position encodings.
Returns
qformer_outputs (torch.FloatTensor
)
The Q-Former model’s last layer hidden states.
Examples:
>>> import torch
>>> from transformers import AutoProcessor, Blip2Model
>>> from transformers.image_utils import load_image
>>> processor = Blip2Processor.from_pretrained("Salesforce/blip2-opt-2.7b")
>>> model = Blip2Model.from_pretrained("Salesforce/blip2-opt-2.7b")
>>> url = "http://images.cocodataset.org/val2017/000000039769.jpg"
>>> image = load_image(url)
>>> inputs = processor(images=image, return_tensors="pt")
>>> with torch.inference_mode():
... qformer_outputs = model.get_qformer_features(**inputs)
Blip2ForConditionalGeneration
class transformers.Blip2ForConditionalGeneration
[< source >](https://github.com/huggingface/transformers/blob/v5.5.0/src/transformers/models/blip_2/modeling_blip_2.py#L1559)
( config: Blip2Config )
Parameters
[config (](#transformers.Blip2ForConditionalGeneration.config)[Blip2Config](/docs/transformers/v5.5.0/en/model_doc/blip-2#transformers.Blip2Config)) — Model configuration class with all the parameters of the model. Initializing with a config file does not load the weights associated with the model, only the configuration. Check out the[from_pretrained()](/docs/transformers/v5.5.0/en/main_classes/model#transformers.PreTrainedModel.from_pretrained)method to load the model weights.
BLIP-2 Model for generating text given an image and an optional text prompt. The model consists of a vision encoder, Querying Transformer (Q-Former) and a language model.
One can optionally pass input_ids
to the model, which serve as a text prompt, to make the language model continue
the prompt. Otherwise, the language model starts generating text from the [BOS] (beginning-of-sequence) token.
Note that Flan-T5 checkpoints cannot be cast to float16. They are pre-trained using bfloat16.
This model inherits from [PreTrainedModel](/docs/transformers/v5.5.0/en/main_classes/model#transformers.PreTrainedModel). Check the superclass documentation for the generic methods the
library implements for all its model (such as downloading or saving, resizing the input embeddings, pruning heads
etc.)
This model is also a PyTorch [torch.nn.Module](https://pytorch.org/docs/stable/nn.html#torch.nn.Module) subclass.
Use it as a regular PyTorch Module and refer to the PyTorch documentation for all matter related to general usage
and behavior.
forward
[< source >](https://github.com/huggingface/transformers/blob/v5.5.0/src/transformers/models/blip_2/modeling_blip_2.py#L1692)
( pixel_values: FloatTensor input_ids: LongTensor attention_mask: torch.LongTensor | None = None decoder_input_ids: torch.LongTensor | None = None decoder_attention_mask: torch.LongTensor | None = None inputs_embeds: torch.FloatTensor | None = None labels: torch.LongTensor | None = None interpolate_pos_encoding: bool = False **kwargs: typing_extensions.Unpack[transformers.utils.generic.TransformersKwargs] ) → Blip2ForConditionalGenerationModelOutput
or tuple(torch.FloatTensor)
Parameters
[pixel_values (](#transformers.Blip2ForConditionalGeneration.forward.pixel_values)torch.FloatTensor
of shape(batch_size, num_channels, image_size, image_size)
) — The tensors corresponding to the input images. Pixel values can be obtained using[BlipImageProcessor](/docs/transformers/v5.5.0/en/model_doc/blip#transformers.BlipImageProcessor). SeeBlipImageProcessor.__call__()
for details ([Blip2Processor](/docs/transformers/v5.5.0/en/model_doc/blip-2#transformers.Blip2Processor)uses[BlipImageProcessor](/docs/transformers/v5.5.0/en/model_doc/blip#transformers.BlipImageProcessor)for processing images).[input_ids (](#transformers.Blip2ForConditionalGeneration.forward.input_ids)torch.LongTensor
of shape(batch_size, sequence_length)
, optional) — Indices of input sequence tokens in the vocabulary of the language model. Input tokens can optionally be provided to serve as text prompt, which the language model can continue.Indices can be obtained using
[Blip2Processor](/docs/transformers/v5.5.0/en/model_doc/blip-2#transformers.Blip2Processor). See[Blip2Processor.call()](/docs/transformers/v5.5.0/en/model_doc/blip-2#transformers.Blip2Processor.__call__)for details.[attention_mask (](#transformers.Blip2ForConditionalGeneration.forward.attention_mask)torch.LongTensor
of shape(batch_size, sequence_length)
, optional) — Mask to avoid performing attention on padding token indices. Mask values selected in[0, 1]
:- 1 for tokens that are not masked,
- 0 for tokens that are masked.
[decoder_input_ids (](#transformers.Blip2ForConditionalGeneration.forward.decoder_input_ids)torch.LongTensor
of shape(batch_size, target_sequence_length)
, optional) — Indices of decoder input sequence tokens in the vocabulary.Indices can be obtained using
[AutoTokenizer](/docs/transformers/v5.5.0/en/model_doc/auto#transformers.AutoTokenizer). See[PreTrainedTokenizer.encode()](/docs/transformers/v5.5.0/en/internal/tokenization_utils#transformers.PreTrainedTokenizerBase.encode)and[PreTrainedTokenizer.call()](/docs/transformers/v5.5.0/en/internal/tokenization_utils#transformers.PreTrainedTokenizerBase.__call__)for details.[decoder_attention_mask (](#transformers.Blip2ForConditionalGeneration.forward.decoder_attention_mask)torch.BoolTensor
of shape(batch_size, target_sequence_length)
, optional) — Default behavior: generate a tensor that ignores pad tokens indecoder_input_ids
. Causal mask will also be used by default.Only relevant in case an encoder-decoder language model (like T5) is used.
[inputs_embeds (](#transformers.Blip2ForConditionalGeneration.forward.inputs_embeds)torch.FloatTensor
of shape(batch_size, sequence_length, hidden_size)
, optional) — Optionally, instead of passinginput_ids
you can choose to directly pass an embedded representation. This is useful if you want more control over how to convertinput_ids
indices into associated vectors than the model’s internal embedding lookup matrix.[labels (](#transformers.Blip2ForConditionalGeneration.forward.labels)torch.LongTensor
of shape(batch_size, sequence_length)
, optional) — Labels for computing the masked language modeling loss. Indices should either be in[0, ..., config.vocab_size]
or -100 (seeinput_ids
docstring). Tokens with indices set to-100
are ignored (masked), the loss is only computed for the tokens with labels in[0, ..., config.vocab_size]
.[interpolate_pos_encoding (](#transformers.Blip2ForConditionalGeneration.forward.interpolate_pos_encoding)bool
, optional, defaults toFalse
) — Whether to interpolate the pre-trained position encodings.
Returns
Blip2ForConditionalGenerationModelOutput
or tuple(torch.FloatTensor)
A Blip2ForConditionalGenerationModelOutput
or a tuple of
torch.FloatTensor
(if return_dict=False
is passed or when config.return_dict=False
) comprising various
elements depending on the configuration ([Blip2Config](/docs/transformers/v5.5.0/en/model_doc/blip-2#transformers.Blip2Config)) and inputs.
The [Blip2ForConditionalGeneration](/docs/transformers/v5.5.0/en/model_doc/blip-2#transformers.Blip2ForConditionalGeneration) forward method, overrides the __call__
special method.
Although the recipe for forward pass needs to be defined within this function, one should call the
Module
instance afterwards instead of this since the former takes care of running the pre and post processing steps while the latter silently ignores them.
- loss (
torch.FloatTensor
, optional, returned whenlabels
is provided,torch.FloatTensor
of shape(1,)
) — Language modeling loss from the language model. - logits (
torch.FloatTensor
of shape(batch_size, sequence_length, config.vocab_size)
) — Prediction scores of the language modeling head of the language model. - vision_outputs (
~modeling_outputs.BaseModelOutputWithPooling
, optional, defaults toNone
) — Outputs of the vision encoder. - qformer_outputs (
~modeling_outputs.BaseModelOutputWithPoolingAndCrossAttentions
, optional, defaults toNone
) — Outputs of the Q-Former (Querying Transformer). - language_model_outputs (
CausalLMOutputWithPast
orSeq2SeqLMOutput
) — Outputs of the language model.
Examples:
Prepare processor, model and image input
>>> from PIL import Image
>>> import httpx
>>> from io import BytesIO
>>> from transformers import Blip2Processor, Blip2ForConditionalGeneration
>>> import torch
>>> device = "cuda" if torch.cuda.is_available() else "cpu"
>>> processor = Blip2Processor.from_pretrained("Salesforce/blip2-opt-2.7b")
>>> model = Blip2ForConditionalGeneration.from_pretrained(
... "Salesforce/blip2-opt-2.7b", load_in_8bit=True, device_map={"": 0}, dtype=torch.float16
... ) # doctest: +IGNORE_RESULT
>>> url = "http://images.cocodataset.org/val2017/000000039769.jpg"
>>> with httpx.stream("GET", url) as response:
... image = Image.open(BytesIO(response.read()))
Image captioning (without providing a text prompt):
>>> inputs = processor(images=image, return_tensors="pt").to(device, torch.float16)
>>> generated_ids = model.generate(**inputs)
>>> generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0].strip()
>>> print(generated_text)
two cats laying on a couch
Visual question answering (prompt = question):
>>> prompt = "Question: how many cats are there? Answer:"
>>> inputs = processor(images=image, text=prompt, return_tensors="pt").to(device="cuda", dtype=torch.float16)
>>> generated_ids = model.generate(**inputs)
>>> generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0].strip()
>>> print(generated_text)
two
Note that int8 inference is also supported through [bitsandbytes](https://github.com/TimDettmers/bitsandbytes).
This greatly reduces the amount of memory used by the model while maintaining the same performance.
>>> model = Blip2ForConditionalGeneration.from_pretrained(
... "Salesforce/blip2-opt-2.7b", load_in_8bit=True, device_map={"": 0}, dtype=torch.bfloat16
... ) # doctest: +IGNORE_RESULT
>>> inputs = processor(images=image, text=prompt, return_tensors="pt").to(device="cuda", dtype=torch.bfloat16)
>>> generated_ids = model.generate(**inputs)
>>> generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0].strip()
>>> print(generated_text)
two
generate
[< source >](https://github.com/huggingface/transformers/blob/v5.5.0/src/transformers/models/blip_2/modeling_blip_2.py#L1842)
( pixel_values: FloatTensor input_ids: torch.LongTensor | None = None attention_mask: torch.LongTensor | None = None inputs_embeds: torch.FloatTensor | None = None interpolate_pos_encoding: bool = False **generate_kwargs ) → captions (list)
Parameters
[pixel_values (](#transformers.Blip2ForConditionalGeneration.generate.pixel_values)torch.FloatTensor
of shape (batch_size, num_channels, height, width)) — Input images to be processed.[input_ids (](#transformers.Blip2ForConditionalGeneration.generate.input_ids)torch.LongTensor
of shape (batch_size, sequence_length), optional) — The sequence used as a prompt for the generation.[attention_mask (](#transformers.Blip2ForConditionalGeneration.generate.attention_mask)torch.LongTensor
of shape (batch_size, sequence_length), optional) — Mask to avoid performing attention on padding token indices[inputs_embeds (](#transformers.Blip2ForConditionalGeneration.generate.inputs_embeds)torch.FloatTensor
of shape(batch_size, sequence_length, hidden_size)
) — Embedded representation of the inputs. Should be float, not int tokens.[interpolate_pos_encoding (](#transformers.Blip2ForConditionalGeneration.generate.interpolate_pos_encoding)bool
, optional, defaults toFalse
) — Whether to interpolate the positional encoding of the image embeddings.
Returns
captions (list)
A list of strings of length batch_size * num_captions.
Overrides generate
function to be able to use the model as a conditional generator.
get_image_features
[< source >](https://github.com/huggingface/transformers/blob/v5.5.0/src/transformers/models/blip_2/modeling_blip_2.py#L1624)
( pixel_values: FloatTensor interpolate_pos_encoding: bool | None = False **kwargs: typing_extensions.Unpack[transformers.utils.generic.TransformersKwargs] ) → BaseModelOutputWithVisionQformerOutputs
or tuple(torch.FloatTensor)
Parameters
[pixel_values (](#transformers.Blip2ForConditionalGeneration.get_image_features.pixel_values)torch.FloatTensor
of shape(batch_size, num_channels, image_size, image_size)
) — The tensors corresponding to the input images.[interpolate_pos_encoding (](#transformers.Blip2ForConditionalGeneration.get_image_features.interpolate_pos_encoding)bool
, optional, defaults toFalse
) — Whether to interpolate the pre-trained position encodings.
Returns
BaseModelOutputWithVisionQformerOutputs
or tuple(torch.FloatTensor)
A BaseModelOutputWithVisionQformerOutputs
or a tuple of
torch.FloatTensor
(if return_dict=False
is passed or when config.return_dict=False
) comprising various
elements depending on the configuration ([Blip2Config](/docs/transformers/v5.5.0/en/model_doc/blip-2#transformers.Blip2Config)) and inputs.
last_hidden_state (
torch.FloatTensor
of shape(batch_size, sequence_length, hidden_size)
, optional) — Sequence of hidden-states at the output of the last layer of the model.pooler_output (
torch.FloatTensor
of shape(batch_size, hidden_size)
, optional) — Last layer hidden-state after a pooling operation on the spatial dimensions.hidden_states (
tuple[torch.FloatTensor, ...]
, optional, returned whenoutput_hidden_states=True
is passed or whenconfig.output_hidden_states=True
) — Tuple oftorch.FloatTensor
(one for the output of the embeddings, if the model has an embedding layer, + one for the output of each layer) of shape(batch_size, sequence_length, hidden_size)
.Hidden-states of the model at the output of each layer plus the optional initial embedding outputs.
attentions (
tuple[torch.FloatTensor, ...]
, optional, returned whenoutput_attentions=True
is passed or whenconfig.output_attentions=True
) — Tuple oftorch.FloatTensor
(one for each layer) of shape(batch_size, num_heads, sequence_length, sequence_length)
.Attentions weights after the attention softmax, used to compute the weighted average in the self-attention heads.
vision_outputs (
~modeling_outputs.BaseModelOutputWithPooling
, optional, defaults toNone
) — Outputs of the vision encoder.qformer_outputs (
~modeling_outputs.BaseModelOutputWithPoolingAndCrossAttentions
, optional, defaults toNone
) — Outputs of the Q-Former (Querying Transformer).
Example:
>>> from PIL import Image
>>> from transformers import AutoProcessor, Blip2ForConditionalGeneration
>>> model = Blip2ForConditionalGeneration.from_pretrained("Salesforce/blip2-opt-2.7b")
>>> processor = AutoProcessor.from_pretrained("Salesforce/blip2-opt-2.7b")
>>> messages = [
... {
... "role": "user", "content": [
... {"type": "image", "url": "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/pipeline-cat-chonk.jpeg"},
... {"type": "text", "text": "Where is the cat standing?"},
... ]
... },
... ]
>>> inputs = processor.apply_chat_template(
... messages,
... tokenize=True,
... return_dict=True,
... return_tensors="pt",
... add_generation_prompt=True
... )
>>> # Generate
>>> generate_ids = model.generate(**inputs)
>>> processor.batch_decode(generate_ids, skip_special_tokens=True)[0]
Blip2ForImageTextRetrieval
class transformers.Blip2ForImageTextRetrieval
[< source >](https://github.com/huggingface/transformers/blob/v5.5.0/src/transformers/models/blip_2/modeling_blip_2.py#L1936)
( config: Blip2Config )
Parameters
[config (](#transformers.Blip2ForImageTextRetrieval.config)[Blip2Config](/docs/transformers/v5.5.0/en/model_doc/blip-2#transformers.Blip2Config)) — Model configuration class with all the parameters of the model. Initializing with a config file does not load the weights associated with the model, only the configuration. Check out the[from_pretrained()](/docs/transformers/v5.5.0/en/main_classes/model#transformers.PreTrainedModel.from_pretrained)method to load the model weights.
BLIP-2 Model with a vision and text projector, and a classification head on top. The model is used in the context of image-text retrieval. Given an image and a text, the model returns the probability of the text being relevant to the image.
This model inherits from [PreTrainedModel](/docs/transformers/v5.5.0/en/main_classes/model#transformers.PreTrainedModel). Check the superclass documentation for the generic methods the
library implements for all its model (such as downloading or saving, resizing the input embeddings, pruning heads
etc.)
This model is also a PyTorch [torch.nn.Module](https://pytorch.org/docs/stable/nn.html#torch.nn.Module) subclass.
Use it as a regular PyTorch Module and refer to the PyTorch documentation for all matter related to general usage
and behavior.
forward
[< source >](https://github.com/huggingface/transformers/blob/v5.5.0/src/transformers/models/blip_2/modeling_blip_2.py#L1970)
( pixel_values: FloatTensor input_ids: LongTensor attention_mask: torch.LongTensor | None = None use_image_text_matching_head: bool | None = False output_attentions: bool | None = None output_hidden_states: bool | None = None return_dict: bool | None = None **kwargs ) → Blip2ImageTextMatchingModelOutput
or tuple(torch.FloatTensor)
Parameters
[pixel_values (](#transformers.Blip2ForImageTextRetrieval.forward.pixel_values)torch.FloatTensor
of shape(batch_size, num_channels, image_size, image_size)
) — The tensors corresponding to the input images. Pixel values can be obtained using[BlipImageProcessor](/docs/transformers/v5.5.0/en/model_doc/blip#transformers.BlipImageProcessor). SeeBlipImageProcessor.__call__()
for details ([Blip2Processor](/docs/transformers/v5.5.0/en/model_doc/blip-2#transformers.Blip2Processor)uses[BlipImageProcessor](/docs/transformers/v5.5.0/en/model_doc/blip#transformers.BlipImageProcessor)for processing images).[input_ids (](#transformers.Blip2ForImageTextRetrieval.forward.input_ids)torch.LongTensor
of shape(batch_size, sequence_length)
, optional) — Indices of input sequence tokens in the vocabulary of the language model. Input tokens can optionally be provided to serve as text prompt, which the language model can continue.Indices can be obtained using
[Blip2Processor](/docs/transformers/v5.5.0/en/model_doc/blip-2#transformers.Blip2Processor). See[Blip2Processor.call()](/docs/transformers/v5.5.0/en/model_doc/blip-2#transformers.Blip2Processor.__call__)for details.[attention_mask (](#transformers.Blip2ForImageTextRetrieval.forward.attention_mask)torch.LongTensor
of shape(batch_size, sequence_length)
, optional) — Mask to avoid performing attention on padding token indices. Mask values selected in[0, 1]
:- 1 for tokens that are not masked,
- 0 for tokens that are masked.
[use_image_text_matching_head (](#transformers.Blip2ForImageTextRetrieval.forward.use_image_text_matching_head)bool
, optional) — Whether to return the Image-Text Matching or Contrastive scores.[output_attentions (](#transformers.Blip2ForImageTextRetrieval.forward.output_attentions)bool
, optional) — Whether or not to return the attentions tensors of all attention layers. Seeattentions
under returned tensors for more detail.[output_hidden_states (](#transformers.Blip2ForImageTextRetrieval.forward.output_hidden_states)bool
, optional) — Whether or not to return the hidden states of all layers. Seehidden_states
under returned tensors for more detail.[return_dict (](#transformers.Blip2ForImageTextRetrieval.forward.return_dict)bool
, optional) — Whether or not to return a[ModelOutput](/docs/transformers/v5.5.0/en/main_classes/output#transformers.utils.ModelOutput)instead of a plain tuple.
Returns
Blip2ImageTextMatchingModelOutput
or tuple(torch.FloatTensor)
A Blip2ImageTextMatchingModelOutput
or a tuple of
torch.FloatTensor
(if return_dict=False
is passed or when config.return_dict=False
) comprising various
elements depending on the configuration ([Blip2Config](/docs/transformers/v5.5.0/en/model_doc/blip-2#transformers.Blip2Config)) and inputs.
The [Blip2ForImageTextRetrieval](/docs/transformers/v5.5.0/en/model_doc/blip-2#transformers.Blip2ForImageTextRetrieval) forward method, overrides the __call__
special method.
Although the recipe for forward pass needs to be defined within this function, one should call the
Module
instance afterwards instead of this since the former takes care of running the pre and post processing steps while the latter silently ignores them.
- loss (
torch.FloatTensor
of shape(1,)
, optional, returned whenreturn_loss
isTrue
) — Contrastive loss for image-text similarity. - logits_per_image (
torch.FloatTensor
of shape(image_batch_size, text_batch_size)
) — The scaled dot product scores betweenimage_embeds
andtext_embeds
. This represents the image-text similarity scores. - logits_per_text (
torch.FloatTensor
of shape(text_batch_size, image_batch_size)
) — The scaled dot product scores betweentext_embeds
andimage_embeds
. This represents the text-image similarity scores. - text_embeds (
torch.FloatTensor
of shape(batch_size, output_dim
) — The text embeddings obtained by applying the projection layer to the pooled output. - image_embeds (
torch.FloatTensor
of shape(batch_size, output_dim
) — The image embeddings obtained by applying the projection layer to the pooled output. - text_model_output (
~modeling_outputs.BaseModelOutputWithPooling
, defaults toNone
) — The output of the[Blip2QFormerModel](/docs/transformers/v5.5.0/en/model_doc/blip-2#transformers.Blip2QFormerModel). - vision_model_output (
~modeling_outputs.BaseModelOutputWithPooling
, defaults toNone
) — The output of the[Blip2VisionModel](/docs/transformers/v5.5.0/en/model_doc/blip-2#transformers.Blip2VisionModel).
Examples:
>>> import torch
>>> from PIL import Image
>>> import httpx
>>> from io import BytesIO
>>> from transformers import AutoProcessor, Blip2ForImageTextRetrieval
>>> device = "cuda" if torch.cuda.is_available() else "cpu"
>>> model = Blip2ForImageTextRetrieval.from_pretrained("Salesforce/blip2-itm-vit-g", dtype=torch.float16)
>>> processor = AutoProcessor.from_pretrained("Salesforce/blip2-itm-vit-g")
>>> model.to(device)
>>> url = "http://images.cocodataset.org/val2017/000000039769.jpg"
>>> with httpx.stream("GET", url) as response:
... image = Image.open(BytesIO(response.read()))
>>> text = "two cats laying on a pink blanket"
>>> inputs = processor(images=image, text=text, return_tensors="pt").to(device, torch.float16)
>>> itm_out = model(**inputs, use_image_text_matching_head=True)
>>> logits_per_image = torch.nn.functional.softmax(itm_out.logits_per_image, dim=1)
>>> probs = logits_per_image.softmax(dim=1) # we can take the softmax to get the label probabilities
>>> print(f"{probs[0][0]:.1%} that image 0 is not '{text}'")
26.9% that image 0 is not 'two cats laying on a pink blanket'
>>> print(f"{probs[0][1]:.1%} that image 0 is '{text}'")
73.0% that image 0 is 'two cats laying on a pink blanket'
>>> texts = ["a photo of a cat", "a photo of a dog"]
>>> inputs = processor(images=image, text=texts, return_tensors="pt").to(device, torch.float16)
>>> itc_out = model(**inputs, use_image_text_matching_head=False)
>>> logits_per_image = itc_out.logits_per_image # this is the image-text similarity score
>>> probs = logits_per_image.softmax(dim=1) # we can take the softmax to get the label probabilities
>>> print(f"{probs[0][0]:.1%} that image 0 is '{texts[0]}'")
55.3% that image 0 is 'a photo of a cat'
>>> print(f"{probs[0][1]:.1%} that image 0 is '{texts[1]}'")
44.7% that image 0 is 'a photo of a dog'
Blip2TextModelWithProjection
class transformers.Blip2TextModelWithProjection
[< source >](https://github.com/huggingface/transformers/blob/v5.5.0/src/transformers/models/blip_2/modeling_blip_2.py#L1373)
( config: Blip2Config )
Parameters
[config (](#transformers.Blip2TextModelWithProjection.config)[Blip2Config](/docs/transformers/v5.5.0/en/model_doc/blip-2#transformers.Blip2Config)) — Model configuration class with all the parameters of the model. Initializing with a config file does not load the weights associated with the model, only the configuration. Check out the[from_pretrained()](/docs/transformers/v5.5.0/en/main_classes/model#transformers.PreTrainedModel.from_pretrained)method to load the model weights.
The Blip 2 Model with a projection layer on top (a linear layer on top of the pooled output).
This model inherits from [PreTrainedModel](/docs/transformers/v5.5.0/en/main_classes/model#transformers.PreTrainedModel). Check the superclass documentation for the generic methods the
library implements for all its model (such as downloading or saving, resizing the input embeddings, pruning heads
etc.)
This model is also a PyTorch [torch.nn.Module](https://pytorch.org/docs/stable/nn.html#torch.nn.Module) subclass.
Use it as a regular PyTorch Module and refer to the PyTorch documentation for all matter related to general usage
and behavior.
forward
[< source >](https://github.com/huggingface/transformers/blob/v5.5.0/src/transformers/models/blip_2/modeling_blip_2.py#L1397)
( input_ids: torch.Tensor | None = None attention_mask: torch.Tensor | None = None position_ids: torch.Tensor | None = None **kwargs: typing_extensions.Unpack[transformers.utils.generic.TransformersKwargs] ) → Blip2TextModelOutput
or tuple(torch.FloatTensor)
Parameters
[input_ids (](#transformers.Blip2TextModelWithProjection.forward.input_ids)torch.Tensor
of shape(batch_size, sequence_length)
, optional) — Indices of input sequence tokens in the vocabulary. Padding will be ignored by default.Indices can be obtained using
[AutoTokenizer](/docs/transformers/v5.5.0/en/model_doc/auto#transformers.AutoTokenizer). See[PreTrainedTokenizer.encode()](/docs/transformers/v5.5.0/en/internal/tokenization_utils#transformers.PreTrainedTokenizerBase.encode)and[PreTrainedTokenizer.call()](/docs/transformers/v5.5.0/en/internal/tokenization_utils#transformers.PreTrainedTokenizerBase.__call__)for details.[attention_mask (](#transformers.Blip2TextModelWithProjection.forward.attention_mask)torch.Tensor
of shape(batch_size, sequence_length)
, optional) — Mask to avoid performing attention on padding token indices. Mask values selected in[0, 1]
:- 1 for tokens that are not masked,
- 0 for tokens that are masked.
[position_ids (](#transformers.Blip2TextModelWithProjection.forward.position_ids)torch.Tensor
of shape(batch_size, sequence_length)
, optional) — Indices of positions of each input sequence tokens in the position embeddings. Selected in the range[0, config.n_positions - 1]
.
Returns
Blip2TextModelOutput
or tuple(torch.FloatTensor)
A Blip2TextModelOutput
or a tuple of
torch.FloatTensor
(if return_dict=False
is passed or when config.return_dict=False
) comprising various
elements depending on the configuration ([Blip2Config](/docs/transformers/v5.5.0/en/model_doc/blip-2#transformers.Blip2Config)) and inputs.
The [Blip2TextModelWithProjection](/docs/transformers/v5.5.0/en/model_doc/blip-2#transformers.Blip2TextModelWithProjection) forward method, overrides the __call__
special method.
Although the recipe for forward pass needs to be defined within this function, one should call the
Module
instance afterwards instead of this since the former takes care of running the pre and post processing steps while the latter silently ignores them.
text_embeds (
torch.FloatTensor
of shape(batch_size, output_dim)
optional returned when model is initialized withwith_projection=True
) — The text embeddings obtained by applying the projection layer to the pooler_output.last_hidden_state (
torch.FloatTensor
of shape(batch_size, sequence_length, hidden_size)
, optional, defaults toNone
) — Sequence of hidden-states at the output of the last layer of the model.hidden_states (
tuple[torch.FloatTensor, ...]
, optional, returned whenoutput_hidden_states=True
is passed or whenconfig.output_hidden_states=True
) — Tuple oftorch.FloatTensor
(one for the output of the embeddings, if the model has an embedding layer, + one for the output of each layer) of shape(batch_size, sequence_length, hidden_size)
.Hidden-states of the model at the output of each layer plus the optional initial embedding outputs.
attentions (
tuple[torch.FloatTensor, ...]
, optional, returned whenoutput_attentions=True
is passed or whenconfig.output_attentions=True
) — Tuple oftorch.FloatTensor
(one for each layer) of shape(batch_size, num_heads, sequence_length, sequence_length)
.Attentions weights after the attention softmax, used to compute the weighted average in the self-attention heads.
Examples:
>>> import torch
>>> from transformers import AutoProcessor, Blip2TextModelWithProjection
>>> device = "cuda" if torch.cuda.is_available() else "cpu"
>>> model = Blip2TextModelWithProjection.from_pretrained(
... "Salesforce/blip2-itm-vit-g", dtype=torch.float16
... )
>>> model.to(device)
>>> processor = AutoProcessor.from_pretrained("Salesforce/blip2-itm-vit-g")
>>> inputs = processor(text=["a photo of a cat", "a photo of a dog"], return_tensors="pt").to(device)
>>> outputs = model(**inputs)
>>> text_embeds = outputs.text_embeds
>>> print(text_embeds.shape)
torch.Size([2, 7, 256])
Blip2VisionModelWithProjection
class transformers.Blip2VisionModelWithProjection
[< source >](https://github.com/huggingface/transformers/blob/v5.5.0/src/transformers/models/blip_2/modeling_blip_2.py#L1458)
( config: Blip2Config )
Parameters
[config (](#transformers.Blip2VisionModelWithProjection.config)[Blip2Config](/docs/transformers/v5.5.0/en/model_doc/blip-2#transformers.Blip2Config)) — Model configuration class with all the parameters of the model. Initializing with a config file does not load the weights associated with the model, only the configuration. Check out the[from_pretrained()](/docs/transformers/v5.5.0/en/main_classes/model#transformers.PreTrainedModel.from_pretrained)method to load the model weights.
The Blip 2 Model with a projection layer on top (a linear layer on top of the pooled output).
This model inherits from [PreTrainedModel](/docs/transformers/v5.5.0/en/main_classes/model#transformers.PreTrainedModel). Check the superclass documentation for the generic methods the
library implements for all its model (such as downloading or saving, resizing the input embeddings, pruning heads
etc.)
This model is also a PyTorch [torch.nn.Module](https://pytorch.org/docs/stable/nn.html#torch.nn.Module) subclass.
Use it as a regular PyTorch Module and refer to the PyTorch documentation for all matter related to general usage
and behavior.
forward
[< source >](https://github.com/huggingface/transformers/blob/v5.5.0/src/transformers/models/blip_2/modeling_blip_2.py#L1481)
( pixel_values: torch.FloatTensor | None = None **kwargs: typing_extensions.Unpack[transformers.utils.generic.TransformersKwargs] ) → Blip2VisionModelOutput
or tuple(torch.FloatTensor)
Parameters
[pixel_values (](#transformers.Blip2VisionModelWithProjection.forward.pixel_values)torch.FloatTensor
of shape(batch_size, num_channels, image_size, image_size)
, optional) — The tensors corresponding to the input images. Pixel values can be obtained using[BlipImageProcessor](/docs/transformers/v5.5.0/en/model_doc/blip#transformers.BlipImageProcessor). SeeBlipImageProcessor.__call__()
for details ([Blip2Processor](/docs/transformers/v5.5.0/en/model_doc/blip-2#transformers.Blip2Processor)uses[BlipImageProcessor](/docs/transformers/v5.5.0/en/model_doc/blip#transformers.BlipImageProcessor)for processing images).
Returns
Blip2VisionModelOutput
or tuple(torch.FloatTensor)
A Blip2VisionModelOutput
or a tuple of
torch.FloatTensor
(if return_dict=False
is passed or when config.return_dict=False
) comprising various
elements depending on the configuration ([Blip2Config](/docs/transformers/v5.5.0/en/model_doc/blip-2#transformers.Blip2Config)) and inputs.
The [Blip2VisionModelWithProjection](/docs/transformers/v5.5.0/en/model_doc/blip-2#transformers.Blip2VisionModelWithProjection) forward method, overrides the __call__
special method.
Although the recipe for forward pass needs to be defined within this function, one should call the
Module
instance afterwards instead of this since the former takes care of running the pre and post processing steps while the latter silently ignores them.
image_embeds (
torch.FloatTensor
of shape(batch_size, output_dim)
optional returned when model is initialized withwith_projection=True
) — The image embeddings obtained by applying the projection layer to the pooler_output.last_hidden_state (
torch.FloatTensor
of shape(batch_size, sequence_length, hidden_size)
, optional, defaults toNone
) — Sequence of hidden-states at the output of the last layer of the model.hidden_states (
tuple[torch.FloatTensor, ...]
, optional, returned whenoutput_hidden_states=True
is passed or whenconfig.output_hidden_states=True
) — Tuple oftorch.FloatTensor
(one for the output of the embeddings, if the model has an embedding layer, + one for the output of each layer) of shape(batch_size, sequence_length, hidden_size)
.Hidden-states of the model at the output of each layer plus the optional initial embedding outputs.
attentions (
tuple[torch.FloatTensor, ...]
, optional, returned whenoutput_attentions=True
is passed or whenconfig.output_attentions=True
) — Tuple oftorch.FloatTensor
(one for each layer) of shape(batch_size, num_heads, sequence_length, sequence_length)
.Attentions weights after the attention softmax, used to compute the weighted average in the self-attention heads.
Examples:
>>> import torch
>>> from transformers import AutoProcessor, Blip2VisionModelWithProjection
>>> from transformers.image_utils import load_image
>>> device = "cuda" if torch.cuda.is_available() else "cpu"
>>> processor = AutoProcessor.from_pretrained("Salesforce/blip2-itm-vit-g")
>>> model = Blip2VisionModelWithProjection.from_pretrained(
... "Salesforce/blip2-itm-vit-g", dtype=torch.float16
... )
>>> model.to(device)
>>> url = "http://images.cocodataset.org/val2017/000000039769.jpg"
>>> image = load_image(url)
>>> inputs = processor(images=image, return_tensors="pt").to(device, torch.float16)
>>> with torch.inference_mode():
... outputs = model(**inputs)
>>> image_embeds = outputs.image_embeds
>>> print(image_embeds.shape)
torch.Size([1, 32, 256])
[Update on GitHub](https://github.com/huggingface/transformers/blob/main/docs/source/en/model_doc/blip-2.md)