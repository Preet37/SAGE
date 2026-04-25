# Source: https://huggingface.co/docs/transformers/model_doc/layoutlm
# Downloaded: 2026-04-09
# Words: 8586
# Author: Hugging Face
# Author Slug: hugging-face
Transformers documentation
LayoutLM
This model was released on 2019-12-31 and added to Hugging Face Transformers on 2020-11-16.
LayoutLM
[LayoutLM](https://huggingface.co/papers/1912.13318) jointly learns text and the document layout rather than focusing only on text. It incorporates positional layout information and visual features of words from the document images.
You can find all the original LayoutLM checkpoints under the [LayoutLM](https://huggingface.co/collections/microsoft/layoutlm-6564539601de72cb631d0902) collection.
Click on the LayoutLM models in the right sidebar for more examples of how to apply LayoutLM to different vision and language tasks.
The example below demonstrates question answering with the [AutoModel](/docs/transformers/v5.5.3/en/model_doc/auto#transformers.AutoModel) class.
import torch
from datasets import load_dataset
from transformers import AutoTokenizer, LayoutLMForQuestionAnswering
tokenizer = AutoTokenizer.from_pretrained("impira/layoutlm-document-qa", add_prefix_space=True)
model = LayoutLMForQuestionAnswering.from_pretrained("impira/layoutlm-document-qa", dtype=torch.float16)
dataset = load_dataset("nielsr/funsd", split="train")
example = dataset[0]
question = "what's his name?"
words = example["words"]
boxes = example["bboxes"]
encoding = tokenizer(
question.split(),
words,
is_split_into_words=True,
return_token_type_ids=True,
return_tensors="pt"
)
bbox = []
for i, s, w in zip(encoding.input_ids[0], encoding.sequence_ids(0), encoding.word_ids(0)):
if s == 1:
bbox.append(boxes[w])
elif i == tokenizer.sep_token_id:
bbox.append([1000] * 4)
else:
bbox.append([0] * 4)
encoding["bbox"] = torch.tensor([bbox])
word_ids = encoding.word_ids(0)
outputs = model(**encoding)
loss = outputs.loss
start_scores = outputs.start_logits
end_scores = outputs.end_logits
start, end = word_ids[start_scores.argmax(-1)], word_ids[end_scores.argmax(-1)]
print(" ".join(words[start : end + 1]))
Notes
The original LayoutLM was not designed with a unified processing workflow. Instead, it expects preprocessed text (
words
) and bounding boxes (boxes
) from an external OCR engine (like[Pytesseract](https://pypi.org/project/pytesseract/)) and provide them as additional inputs to the tokenizer.The
[forward()](/docs/transformers/v5.5.3/en/model_doc/layoutlm#transformers.LayoutLMModel.forward)method expects the inputbbox
(bounding boxes of the input tokens). Each bounding box should be in the format(x0, y0, x1, y1)
.(x0, y0)
corresponds to the upper left corner of the bounding box and{x1, y1)
corresponds to the lower right corner. The bounding boxes need to be normalized on a 0-1000 scale as shown below.
def normalize_bbox(bbox, width, height):
return [
int(1000 * (bbox[0] / width)),
int(1000 * (bbox[1] / height)),
int(1000 * (bbox[2] / width)),
int(1000 * (bbox[3] / height)),
]
width
andheight
correspond to the width and height of the original document in which the token occurs. These values can be obtained as shown below.
from PIL import Image
# Document can be a png, jpg, etc. PDFs must be converted to images.
image = Image.open(name_of_your_document).convert("RGB")
width, height = image.size
Resources
A list of official Hugging Face and community (indicated by 🌎) resources to help you get started with LayoutLM. If you’re interested in submitting a resource to be included here, please feel free to open a Pull Request and we’ll review it! The resource should ideally demonstrate something new instead of duplicating an existing resource.
- Read
[fine-tuning LayoutLM for document-understanding using Keras & Hugging Face Transformers](https://www.philschmid.de/fine-tuning-layoutlm-keras)to learn more. - Read
[fine-tune LayoutLM for document-understanding using only Hugging Face Transformers](https://www.philschmid.de/fine-tuning-layoutlm)for more information. - Refer to this
[notebook](https://colab.research.google.com/github/NielsRogge/Transformers-Tutorials/blob/master/LayoutLM/Add_image_embeddings_to_LayoutLM.ipynb)for a practical example of how to fine-tune LayoutLM. - Refer to this
[notebook](https://colab.research.google.com/github/NielsRogge/Transformers-Tutorials/blob/master/LayoutLM/Fine_tuning_LayoutLMForSequenceClassification_on_RVL_CDIP.ipynb)for an example of how to fine-tune LayoutLM for sequence classification. - Refer to this
[notebook](https://github.com/NielsRogge/Transformers-Tutorials/blob/master/LayoutLM/Fine_tuning_LayoutLMForTokenClassification_on_FUNSD.ipynb)for an example of how to fine-tune LayoutLM for token classification. - Read
[Deploy LayoutLM with Hugging Face Inference Endpoints](https://www.philschmid.de/inference-endpoints-layoutlm)to learn how to deploy LayoutLM.
LayoutLMConfig
class transformers.LayoutLMConfig
[< source >](https://github.com/huggingface/transformers/blob/v5.5.3/src/transformers/models/layoutlm/configuration_layoutlm.py#L24)
( transformers_version: str | None = None architectures: list[str] | None = None output_hidden_states: bool | None = False return_dict: bool | None = True dtype: typing.Union[str, ForwardRef('torch.dtype'), NoneType] = None chunk_size_feed_forward: int = 0 is_encoder_decoder: bool = False id2label: dict[int, str] | dict[str, str] | None = None label2id: dict[str, int] | dict[str, str] | None = None problem_type: typing.Optional[typing.Literal['regression', 'single_label_classification', 'multi_label_classification']] = None vocab_size: int = 30522 hidden_size: int = 768 num_hidden_layers: int = 12 num_attention_heads: int = 12 intermediate_size: int = 3072 hidden_act: str = 'gelu' hidden_dropout_prob: float | int = 0.1 attention_probs_dropout_prob: float | int = 0.1 max_position_embeddings: int = 512 type_vocab_size: int = 2 initializer_range: float = 0.02 layer_norm_eps: float = 1e-12 pad_token_id: int | None = 0 eos_token_id: int | list[int] | None = None bos_token_id: int | None = None use_cache: bool = True max_2d_position_embeddings: int = 1024 tie_word_embeddings: bool = True )
Parameters
[vocab_size (](#transformers.LayoutLMConfig.vocab_size)int
, optional, defaults to30522
) — Vocabulary size of the model. Defines the number of different tokens that can be represented by theinput_ids
.[hidden_size (](#transformers.LayoutLMConfig.hidden_size)int
, optional, defaults to768
) — Dimension of the hidden representations.[num_hidden_layers (](#transformers.LayoutLMConfig.num_hidden_layers)int
, optional, defaults to12
) — Number of hidden layers in the Transformer decoder.[num_attention_heads (](#transformers.LayoutLMConfig.num_attention_heads)int
, optional, defaults to12
) — Number of attention heads for each attention layer in the Transformer decoder.[intermediate_size (](#transformers.LayoutLMConfig.intermediate_size)int
, optional, defaults to3072
) — Dimension of the MLP representations.[hidden_act (](#transformers.LayoutLMConfig.hidden_act)str
, optional, defaults togelu
) — The non-linear activation function (function or string) in the decoder. For example,"gelu"
,"relu"
,"silu"
, etc.[hidden_dropout_prob (](#transformers.LayoutLMConfig.hidden_dropout_prob)Union[float, int]
, optional, defaults to0.1
) — The dropout probability for all fully connected layers in the embeddings, encoder, and pooler.[attention_probs_dropout_prob (](#transformers.LayoutLMConfig.attention_probs_dropout_prob)Union[float, int]
, optional, defaults to0.1
) — The dropout ratio for the attention probabilities.[max_position_embeddings (](#transformers.LayoutLMConfig.max_position_embeddings)int
, optional, defaults to512
) — The maximum sequence length that this model might ever be used with.[type_vocab_size (](#transformers.LayoutLMConfig.type_vocab_size)int
, optional, defaults to2
) — The vocabulary size of thetoken_type_ids
.[initializer_range (](#transformers.LayoutLMConfig.initializer_range)float
, optional, defaults to0.02
) — The standard deviation of the truncated_normal_initializer for initializing all weight matrices.[layer_norm_eps (](#transformers.LayoutLMConfig.layer_norm_eps)float
, optional, defaults to1e-12
) — The epsilon used by the layer normalization layers.[pad_token_id (](#transformers.LayoutLMConfig.pad_token_id)int
, optional, defaults to0
) — Token id used for padding in the vocabulary.[eos_token_id (](#transformers.LayoutLMConfig.eos_token_id)Union[int, list[int]]
, optional) — Token id used for end-of-stream in the vocabulary.[bos_token_id (](#transformers.LayoutLMConfig.bos_token_id)int
, optional) — Token id used for beginning-of-stream in the vocabulary.[use_cache (](#transformers.LayoutLMConfig.use_cache)bool
, optional, defaults toTrue
) — Whether or not the model should return the last key/values attentions (not used by all models). Only relevant ifconfig.is_decoder=True
or when the model is a decoder-only generative model.[max_2d_position_embeddings (](#transformers.LayoutLMConfig.max_2d_position_embeddings)int
, optional, defaults to 1024) — The maximum value that the 2D position embedding might ever used. Typically set this to something large just in case (e.g., 1024).[tie_word_embeddings (](#transformers.LayoutLMConfig.tie_word_embeddings)bool
, optional, defaults toTrue
) — Whether to tie weight embeddings according to model’stied_weights_keys
mapping.
This is the configuration class to store the configuration of a LayoutLMModel. It is used to instantiate a Layoutlm
model according to the specified arguments, defining the model architecture. Instantiating a configuration with the
defaults will yield a similar configuration to that of the [microsoft/layoutlm-base-uncased](https://huggingface.co/microsoft/layoutlm-base-uncased)
Configuration objects inherit from [PreTrainedConfig](/docs/transformers/v5.5.3/en/main_classes/configuration#transformers.PreTrainedConfig) and can be used to control the model outputs. Read the
documentation from [PreTrainedConfig](/docs/transformers/v5.5.3/en/main_classes/configuration#transformers.PreTrainedConfig) for more information.
Examples:
>>> from transformers import LayoutLMConfig, LayoutLMModel
>>> # Initializing a LayoutLM configuration
>>> configuration = LayoutLMConfig()
>>> # Initializing a model (with random weights) from the configuration
>>> model = LayoutLMModel(configuration)
>>> # Accessing the model configuration
>>> configuration = model.config
LayoutLMTokenizer
class transformers.BertTokenizer
[< source >](https://github.com/huggingface/transformers/blob/v5.5.3/src/transformers/models/bert/tokenization_bert.py#L41)
( vocab: str | dict[str, int] | None = None do_lower_case: bool = True unk_token: str = '[UNK]' sep_token: str = '[SEP]' pad_token: str = '[PAD]' cls_token: str = '[CLS]' mask_token: str = '[MASK]' tokenize_chinese_chars: bool = True strip_accents: bool | None = None **kwargs )
Parameters
[vocab (](#transformers.BertTokenizer.vocab)str
ordict[str, int]
, optional) — Custom vocabulary dictionary. If not provided, vocabulary is loaded fromvocab_file
.[do_lower_case (](#transformers.BertTokenizer.do_lower_case)bool
, optional, defaults toTrue
) — Whether or not to lowercase the input when tokenizing.[unk_token (](#transformers.BertTokenizer.unk_token)str
, optional, defaults to"[UNK]"
) — The unknown token. A token that is not in the vocabulary cannot be converted to an ID and is set to be this token instead.[sep_token (](#transformers.BertTokenizer.sep_token)str
, optional, defaults to"[SEP]"
) — The separator token, which is used when building a sequence from multiple sequences, e.g. two sequences for sequence classification or for a text and a question for question answering. It is also used as the last token of a sequence built with special tokens.[pad_token (](#transformers.BertTokenizer.pad_token)str
, optional, defaults to"[PAD]"
) — The token used for padding, for example when batching sequences of different lengths.[cls_token (](#transformers.BertTokenizer.cls_token)str
, optional, defaults to"[CLS]"
) — The classifier token which is used when doing sequence classification (classification of the whole sequence instead of per-token classification). It is the first token of the sequence when built with special tokens.[mask_token (](#transformers.BertTokenizer.mask_token)str
, optional, defaults to"[MASK]"
) — The token used for masking values. This is the token used when training this model with masked language modeling. This is the token which the model will try to predict.[tokenize_chinese_chars (](#transformers.BertTokenizer.tokenize_chinese_chars)bool
, optional, defaults toTrue
) — Whether or not to tokenize Chinese characters.[strip_accents (](#transformers.BertTokenizer.strip_accents)bool
, optional) — Whether or not to strip all accents. If this option is not specified, then it will be determined by the value forlowercase
(as in the original BERT).
Construct a BERT tokenizer (backed by HuggingFace’s tokenizers library). Based on WordPiece.
This tokenizer inherits from [TokenizersBackend](/docs/transformers/v5.5.3/en/main_classes/tokenizer#transformers.TokenizersBackend) which contains most of the main methods. Users should refer to
this superclass for more information regarding those methods.
__call__
[< source >](https://github.com/huggingface/transformers/blob/v5.5.3/src/transformers/tokenization_utils_base.py#L2403)
( text: TextInput | PreTokenizedInput | list[TextInput] | list[PreTokenizedInput] | None = None text_pair: TextInput | PreTokenizedInput | list[TextInput] | list[PreTokenizedInput] | None = None text_target: TextInput | PreTokenizedInput | list[TextInput] | list[PreTokenizedInput] | None = None text_pair_target: TextInput | PreTokenizedInput | list[TextInput] | list[PreTokenizedInput] | None = None add_special_tokens: bool = True padding: bool | str | PaddingStrategy = False truncation: bool | str | TruncationStrategy | None = None max_length: int | None = None stride: int = 0 is_split_into_words: bool = False pad_to_multiple_of: int | None = None padding_side: str | None = None return_tensors: str | TensorType | None = None return_token_type_ids: bool | None = None return_attention_mask: bool | None = None return_overflowing_tokens: bool = False return_special_tokens_mask: bool = False return_offsets_mapping: bool = False return_length: bool = False verbose: bool = True tokenizer_kwargs: dict[str, Any] | None = None **kwargs ) → [BatchEncoding](/docs/transformers/v5.5.3/en/main_classes/tokenizer#transformers.BatchEncoding)
Parameters
[text (](#transformers.BertTokenizer.__call__.text)str
,list[str]
,list[list[str]]
, optional) — The sequence or batch of sequences to be encoded. Each sequence can be a string or a list of strings (pretokenized string). If the sequences are provided as list of strings (pretokenized), you must setis_split_into_words=True
(to lift the ambiguity with a batch of sequences).[text_pair (](#transformers.BertTokenizer.__call__.text_pair)str
,list[str]
,list[list[str]]
, optional) — The sequence or batch of sequences to be encoded. Each sequence can be a string or a list of strings (pretokenized string). If the sequences are provided as list of strings (pretokenized), you must setis_split_into_words=True
(to lift the ambiguity with a batch of sequences).[text_target (](#transformers.BertTokenizer.__call__.text_target)str
,list[str]
,list[list[str]]
, optional) — The sequence or batch of sequences to be encoded as target texts. Each sequence can be a string or a list of strings (pretokenized string). If the sequences are provided as list of strings (pretokenized), you must setis_split_into_words=True
(to lift the ambiguity with a batch of sequences).[text_pair_target (](#transformers.BertTokenizer.__call__.text_pair_target)str
,list[str]
,list[list[str]]
, optional) — The sequence or batch of sequences to be encoded as target texts. Each sequence can be a string or a list of strings (pretokenized string). If the sequences are provided as list of strings (pretokenized), you must setis_split_into_words=True
(to lift the ambiguity with a batch of sequences).[tokenizer_kwargs (](#transformers.BertTokenizer.__call__.tokenizer_kwargs)dict[str, Any]
, optional) — Additional kwargs to pass to the tokenizer. These will be merged with the explicit parameters and other kwargs, with explicit parameters taking precedence.[add_special_tokens (](#transformers.BertTokenizer.__call__.add_special_tokens)bool
, optional, defaults toTrue
) — Whether or not to add special tokens when encoding the sequences. This will use the underlyingPretrainedTokenizerBase.build_inputs_with_special_tokens
function, which defines which tokens are automatically added to the input ids. This is useful if you want to addbos
oreos
tokens automatically.[padding (](#transformers.BertTokenizer.__call__.padding)bool
,str
or[PaddingStrategy](/docs/transformers/v5.5.3/en/internal/file_utils#transformers.utils.PaddingStrategy), optional, defaults toFalse
) — Activates and controls padding. Accepts the following values:True
or'longest'
: Pad to the longest sequence in the batch (or no padding if only a single sequence is provided).'max_length'
: Pad to a maximum length specified with the argumentmax_length
or to the maximum acceptable input length for the model if that argument is not provided.False
or'do_not_pad'
(default): No padding (i.e., can output a batch with sequences of different lengths).
[truncation (](#transformers.BertTokenizer.__call__.truncation)bool
,str
or[TruncationStrategy](/docs/transformers/v5.5.3/en/internal/tokenization_utils#transformers.tokenization_utils_base.TruncationStrategy), optional, defaults toFalse
) — Activates and controls truncation. Accepts the following values:True
or'longest_first'
: Truncate to a maximum length specified with the argumentmax_length
or to the maximum acceptable input length for the model if that argument is not provided. This will truncate token by token, removing a token from the longest sequence in the pair if a pair of sequences (or a batch of pairs) is provided.'only_first'
: Truncate to a maximum length specified with the argumentmax_length
or to the maximum acceptable input length for the model if that argument is not provided. This will only truncate the first sequence of a pair if a pair of sequences (or a batch of pairs) is provided.'only_second'
: Truncate to a maximum length specified with the argumentmax_length
or to the maximum acceptable input length for the model if that argument is not provided. This will only truncate the second sequence of a pair if a pair of sequences (or a batch of pairs) is provided.False
or'do_not_truncate'
(default): No truncation (i.e., can output batch with sequence lengths greater than the model maximum admissible input size).
[max_length (](#transformers.BertTokenizer.__call__.max_length)int
, optional) — Controls the maximum length to use by one of the truncation/padding parameters.If left unset or set to
None
, this will use the predefined model maximum length if a maximum length is required by one of the truncation/padding parameters. If the model has no specific maximum input length (like XLNet) truncation/padding to a maximum length will be deactivated.[stride (](#transformers.BertTokenizer.__call__.stride)int
, optional, defaults to 0) — If set to a number along withmax_length
, the overflowing tokens returned whenreturn_overflowing_tokens=True
will contain some tokens from the end of the truncated sequence returned to provide some overlap between truncated and overflowing sequences. The value of this argument defines the number of overlapping tokens.[is_split_into_words (](#transformers.BertTokenizer.__call__.is_split_into_words)bool
, optional, defaults toFalse
) — Whether or not the input is already pre-tokenized (e.g., split into words). If set toTrue
, the tokenizer assumes the input is already split into words (for instance, by splitting it on whitespace) which it will tokenize. This is useful for NER or token classification.[pad_to_multiple_of (](#transformers.BertTokenizer.__call__.pad_to_multiple_of)int
, optional) — If set will pad the sequence to a multiple of the provided value. Requirespadding
to be activated. This is especially useful to enable the use of Tensor Cores on NVIDIA hardware with compute capability>= 7.5
(Volta).[padding_side (](#transformers.BertTokenizer.__call__.padding_side)str
, optional) — The side on which the model should have padding applied. Should be selected between [‘right’, ‘left’]. Default value is picked from the class attribute of the same name.[return_tensors (](#transformers.BertTokenizer.__call__.return_tensors)str
or[TensorType](/docs/transformers/v5.5.3/en/internal/file_utils#transformers.TensorType), optional) — If set, will return tensors instead of list of python integers. Acceptable values are:'pt'
: Return PyTorchtorch.Tensor
objects.'np'
: Return Numpynp.ndarray
objects.
[return_token_type_ids (](#transformers.BertTokenizer.__call__.return_token_type_ids)bool
, optional) — Whether to return token type IDs. If left to the default, will return the token type IDs according to the specific tokenizer’s default, defined by thereturn_outputs
attribute.[return_attention_mask (](#transformers.BertTokenizer.__call__.return_attention_mask)bool
, optional) — Whether to return the attention mask. If left to the default, will return the attention mask according to the specific tokenizer’s default, defined by thereturn_outputs
attribute.[return_overflowing_tokens (](#transformers.BertTokenizer.__call__.return_overflowing_tokens)bool
, optional, defaults toFalse
) — Whether or not to return overflowing token sequences. If a pair of sequences of input ids (or a batch of pairs) is provided withtruncation_strategy = longest_first
orTrue
, an error is raised instead of returning overflowing tokens.[return_special_tokens_mask (](#transformers.BertTokenizer.__call__.return_special_tokens_mask)bool
, optional, defaults toFalse
) — Whether or not to return special tokens mask information.[return_offsets_mapping (](#transformers.BertTokenizer.__call__.return_offsets_mapping)bool
, optional, defaults toFalse
) — Whether or not to return(char_start, char_end)
for each token.This is only available on fast tokenizers inheriting from
[PreTrainedTokenizerFast](/docs/transformers/v5.5.3/en/main_classes/tokenizer#transformers.TokenizersBackend), if using Python’s tokenizer, this method will raiseNotImplementedError
.[return_length (](#transformers.BertTokenizer.__call__.return_length)bool
, optional, defaults toFalse
) — Whether or not to return the lengths of the encoded inputs.[verbose (](#transformers.BertTokenizer.__call__.verbose)bool
, optional, defaults toTrue
) — Whether or not to print more information and warnings.[**kwargs — passed to the](#transformers.BertTokenizer.__call__.*kwargs)self.tokenize()
method
Returns
A [BatchEncoding](/docs/transformers/v5.5.3/en/main_classes/tokenizer#transformers.BatchEncoding) with the following fields:
-
input_ids — List of token ids to be fed to a model.
-
token_type_ids — List of token type ids to be fed to a model (when
return_token_type_ids=True
or if “token_type_ids” is inself.model_input_names
). -
attention_mask — List of indices specifying which tokens should be attended to by the model (when
return_attention_mask=True
or if “attention_mask” is inself.model_input_names
). -
overflowing_tokens — List of overflowing tokens sequences (when a
max_length
is specified andreturn_overflowing_tokens=True
). -
num_truncated_tokens — Number of tokens truncated (when a
max_length
is specified andreturn_overflowing_tokens=True
). -
special_tokens_mask — List of 0s and 1s, with 1 specifying added special tokens and 0 specifying regular sequence tokens (when
add_special_tokens=True
andreturn_special_tokens_mask=True
). -
length — The length of the inputs (when
return_length=True
)
Main method to tokenize and prepare for the model one or several sequence(s) or one or several pair(s) of sequences.
LayoutLMTokenizerFast
class transformers.BertTokenizer
[< source >](https://github.com/huggingface/transformers/blob/v5.5.3/src/transformers/models/bert/tokenization_bert.py#L41)
( vocab: str | dict[str, int] | None = None do_lower_case: bool = True unk_token: str = '[UNK]' sep_token: str = '[SEP]' pad_token: str = '[PAD]' cls_token: str = '[CLS]' mask_token: str = '[MASK]' tokenize_chinese_chars: bool = True strip_accents: bool | None = None **kwargs )
Parameters
[vocab (](#transformers.BertTokenizer.vocab)str
ordict[str, int]
, optional) — Custom vocabulary dictionary. If not provided, vocabulary is loaded fromvocab_file
.[do_lower_case (](#transformers.BertTokenizer.do_lower_case)bool
, optional, defaults toTrue
) — Whether or not to lowercase the input when tokenizing.[unk_token (](#transformers.BertTokenizer.unk_token)str
, optional, defaults to"[UNK]"
) — The unknown token. A token that is not in the vocabulary cannot be converted to an ID and is set to be this token instead.[sep_token (](#transformers.BertTokenizer.sep_token)str
, optional, defaults to"[SEP]"
) — The separator token, which is used when building a sequence from multiple sequences, e.g. two sequences for sequence classification or for a text and a question for question answering. It is also used as the last token of a sequence built with special tokens.[pad_token (](#transformers.BertTokenizer.pad_token)str
, optional, defaults to"[PAD]"
) — The token used for padding, for example when batching sequences of different lengths.[cls_token (](#transformers.BertTokenizer.cls_token)str
, optional, defaults to"[CLS]"
) — The classifier token which is used when doing sequence classification (classification of the whole sequence instead of per-token classification). It is the first token of the sequence when built with special tokens.[mask_token (](#transformers.BertTokenizer.mask_token)str
, optional, defaults to"[MASK]"
) — The token used for masking values. This is the token used when training this model with masked language modeling. This is the token which the model will try to predict.[tokenize_chinese_chars (](#transformers.BertTokenizer.tokenize_chinese_chars)bool
, optional, defaults toTrue
) — Whether or not to tokenize Chinese characters.[strip_accents (](#transformers.BertTokenizer.strip_accents)bool
, optional) — Whether or not to strip all accents. If this option is not specified, then it will be determined by the value forlowercase
(as in the original BERT).
Construct a BERT tokenizer (backed by HuggingFace’s tokenizers library). Based on WordPiece.
This tokenizer inherits from [TokenizersBackend](/docs/transformers/v5.5.3/en/main_classes/tokenizer#transformers.TokenizersBackend) which contains most of the main methods. Users should refer to
this superclass for more information regarding those methods.
__call__
[< source >](https://github.com/huggingface/transformers/blob/v5.5.3/src/transformers/tokenization_utils_base.py#L2403)
( text: TextInput | PreTokenizedInput | list[TextInput] | list[PreTokenizedInput] | None = None text_pair: TextInput | PreTokenizedInput | list[TextInput] | list[PreTokenizedInput] | None = None text_target: TextInput | PreTokenizedInput | list[TextInput] | list[PreTokenizedInput] | None = None text_pair_target: TextInput | PreTokenizedInput | list[TextInput] | list[PreTokenizedInput] | None = None add_special_tokens: bool = True padding: bool | str | PaddingStrategy = False truncation: bool | str | TruncationStrategy | None = None max_length: int | None = None stride: int = 0 is_split_into_words: bool = False pad_to_multiple_of: int | None = None padding_side: str | None = None return_tensors: str | TensorType | None = None return_token_type_ids: bool | None = None return_attention_mask: bool | None = None return_overflowing_tokens: bool = False return_special_tokens_mask: bool = False return_offsets_mapping: bool = False return_length: bool = False verbose: bool = True tokenizer_kwargs: dict[str, Any] | None = None **kwargs ) → [BatchEncoding](/docs/transformers/v5.5.3/en/main_classes/tokenizer#transformers.BatchEncoding)
Parameters
[text (](#transformers.BertTokenizer.__call__.text)str
,list[str]
,list[list[str]]
, optional) — The sequence or batch of sequences to be encoded. Each sequence can be a string or a list of strings (pretokenized string). If the sequences are provided as list of strings (pretokenized), you must setis_split_into_words=True
(to lift the ambiguity with a batch of sequences).[text_pair (](#transformers.BertTokenizer.__call__.text_pair)str
,list[str]
,list[list[str]]
, optional) — The sequence or batch of sequences to be encoded. Each sequence can be a string or a list of strings (pretokenized string). If the sequences are provided as list of strings (pretokenized), you must setis_split_into_words=True
(to lift the ambiguity with a batch of sequences).[text_target (](#transformers.BertTokenizer.__call__.text_target)str
,list[str]
,list[list[str]]
, optional) — The sequence or batch of sequences to be encoded as target texts. Each sequence can be a string or a list of strings (pretokenized string). If the sequences are provided as list of strings (pretokenized), you must setis_split_into_words=True
(to lift the ambiguity with a batch of sequences).[text_pair_target (](#transformers.BertTokenizer.__call__.text_pair_target)str
,list[str]
,list[list[str]]
, optional) — The sequence or batch of sequences to be encoded as target texts. Each sequence can be a string or a list of strings (pretokenized string). If the sequences are provided as list of strings (pretokenized), you must setis_split_into_words=True
(to lift the ambiguity with a batch of sequences).[tokenizer_kwargs (](#transformers.BertTokenizer.__call__.tokenizer_kwargs)dict[str, Any]
, optional) — Additional kwargs to pass to the tokenizer. These will be merged with the explicit parameters and other kwargs, with explicit parameters taking precedence.[add_special_tokens (](#transformers.BertTokenizer.__call__.add_special_tokens)bool
, optional, defaults toTrue
) — Whether or not to add special tokens when encoding the sequences. This will use the underlyingPretrainedTokenizerBase.build_inputs_with_special_tokens
function, which defines which tokens are automatically added to the input ids. This is useful if you want to addbos
oreos
tokens automatically.[padding (](#transformers.BertTokenizer.__call__.padding)bool
,str
or[PaddingStrategy](/docs/transformers/v5.5.3/en/internal/file_utils#transformers.utils.PaddingStrategy), optional, defaults toFalse
) — Activates and controls padding. Accepts the following values:True
or'longest'
: Pad to the longest sequence in the batch (or no padding if only a single sequence is provided).'max_length'
: Pad to a maximum length specified with the argumentmax_length
or to the maximum acceptable input length for the model if that argument is not provided.False
or'do_not_pad'
(default): No padding (i.e., can output a batch with sequences of different lengths).
[truncation (](#transformers.BertTokenizer.__call__.truncation)bool
,str
or[TruncationStrategy](/docs/transformers/v5.5.3/en/internal/tokenization_utils#transformers.tokenization_utils_base.TruncationStrategy), optional, defaults toFalse
) — Activates and controls truncation. Accepts the following values:True
or'longest_first'
: Truncate to a maximum length specified with the argumentmax_length
or to the maximum acceptable input length for the model if that argument is not provided. This will truncate token by token, removing a token from the longest sequence in the pair if a pair of sequences (or a batch of pairs) is provided.'only_first'
: Truncate to a maximum length specified with the argumentmax_length
or to the maximum acceptable input length for the model if that argument is not provided. This will only truncate the first sequence of a pair if a pair of sequences (or a batch of pairs) is provided.'only_second'
: Truncate to a maximum length specified with the argumentmax_length
or to the maximum acceptable input length for the model if that argument is not provided. This will only truncate the second sequence of a pair if a pair of sequences (or a batch of pairs) is provided.False
or'do_not_truncate'
(default): No truncation (i.e., can output batch with sequence lengths greater than the model maximum admissible input size).
[max_length (](#transformers.BertTokenizer.__call__.max_length)int
, optional) — Controls the maximum length to use by one of the truncation/padding parameters.If left unset or set to
None
, this will use the predefined model maximum length if a maximum length is required by one of the truncation/padding parameters. If the model has no specific maximum input length (like XLNet) truncation/padding to a maximum length will be deactivated.[stride (](#transformers.BertTokenizer.__call__.stride)int
, optional, defaults to 0) — If set to a number along withmax_length
, the overflowing tokens returned whenreturn_overflowing_tokens=True
will contain some tokens from the end of the truncated sequence returned to provide some overlap between truncated and overflowing sequences. The value of this argument defines the number of overlapping tokens.[is_split_into_words (](#transformers.BertTokenizer.__call__.is_split_into_words)bool
, optional, defaults toFalse
) — Whether or not the input is already pre-tokenized (e.g., split into words). If set toTrue
, the tokenizer assumes the input is already split into words (for instance, by splitting it on whitespace) which it will tokenize. This is useful for NER or token classification.[pad_to_multiple_of (](#transformers.BertTokenizer.__call__.pad_to_multiple_of)int
, optional) — If set will pad the sequence to a multiple of the provided value. Requirespadding
to be activated. This is especially useful to enable the use of Tensor Cores on NVIDIA hardware with compute capability>= 7.5
(Volta).[padding_side (](#transformers.BertTokenizer.__call__.padding_side)str
, optional) — The side on which the model should have padding applied. Should be selected between [‘right’, ‘left’]. Default value is picked from the class attribute of the same name.[return_tensors (](#transformers.BertTokenizer.__call__.return_tensors)str
or[TensorType](/docs/transformers/v5.5.3/en/internal/file_utils#transformers.TensorType), optional) — If set, will return tensors instead of list of python integers. Acceptable values are:'pt'
: Return PyTorchtorch.Tensor
objects.'np'
: Return Numpynp.ndarray
objects.
[return_token_type_ids (](#transformers.BertTokenizer.__call__.return_token_type_ids)bool
, optional) — Whether to return token type IDs. If left to the default, will return the token type IDs according to the specific tokenizer’s default, defined by thereturn_outputs
attribute.[return_attention_mask (](#transformers.BertTokenizer.__call__.return_attention_mask)bool
, optional) — Whether to return the attention mask. If left to the default, will return the attention mask according to the specific tokenizer’s default, defined by thereturn_outputs
attribute.[return_overflowing_tokens (](#transformers.BertTokenizer.__call__.return_overflowing_tokens)bool
, optional, defaults toFalse
) — Whether or not to return overflowing token sequences. If a pair of sequences of input ids (or a batch of pairs) is provided withtruncation_strategy = longest_first
orTrue
, an error is raised instead of returning overflowing tokens.[return_special_tokens_mask (](#transformers.BertTokenizer.__call__.return_special_tokens_mask)bool
, optional, defaults toFalse
) — Whether or not to return special tokens mask information.[return_offsets_mapping (](#transformers.BertTokenizer.__call__.return_offsets_mapping)bool
, optional, defaults toFalse
) — Whether or not to return(char_start, char_end)
for each token.This is only available on fast tokenizers inheriting from
[PreTrainedTokenizerFast](/docs/transformers/v5.5.3/en/main_classes/tokenizer#transformers.TokenizersBackend), if using Python’s tokenizer, this method will raiseNotImplementedError
.[return_length (](#transformers.BertTokenizer.__call__.return_length)bool
, optional, defaults toFalse
) — Whether or not to return the lengths of the encoded inputs.[verbose (](#transformers.BertTokenizer.__call__.verbose)bool
, optional, defaults toTrue
) — Whether or not to print more information and warnings.[**kwargs — passed to the](#transformers.BertTokenizer.__call__.*kwargs)self.tokenize()
method
Returns
A [BatchEncoding](/docs/transformers/v5.5.3/en/main_classes/tokenizer#transformers.BatchEncoding) with the following fields:
-
input_ids — List of token ids to be fed to a model.
-
token_type_ids — List of token type ids to be fed to a model (when
return_token_type_ids=True
or if “token_type_ids” is inself.model_input_names
). -
attention_mask — List of indices specifying which tokens should be attended to by the model (when
return_attention_mask=True
or if “attention_mask” is inself.model_input_names
). -
overflowing_tokens — List of overflowing tokens sequences (when a
max_length
is specified andreturn_overflowing_tokens=True
). -
num_truncated_tokens — Number of tokens truncated (when a
max_length
is specified andreturn_overflowing_tokens=True
). -
special_tokens_mask — List of 0s and 1s, with 1 specifying added special tokens and 0 specifying regular sequence tokens (when
add_special_tokens=True
andreturn_special_tokens_mask=True
). -
length — The length of the inputs (when
return_length=True
)
Main method to tokenize and prepare for the model one or several sequence(s) or one or several pair(s) of sequences.
LayoutLMModel
class transformers.LayoutLMModel
[< source >](https://github.com/huggingface/transformers/blob/v5.5.3/src/transformers/models/layoutlm/modeling_layoutlm.py#L414)
( config )
Parameters
[config (](#transformers.LayoutLMModel.config)[LayoutLMModel](/docs/transformers/v5.5.3/en/model_doc/layoutlm#transformers.LayoutLMModel)) — Model configuration class with all the parameters of the model. Initializing with a config file does not load the weights associated with the model, only the configuration. Check out the[from_pretrained()](/docs/transformers/v5.5.3/en/main_classes/model#transformers.PreTrainedModel.from_pretrained)method to load the model weights.
The bare Layoutlm Model outputting raw hidden-states without any specific head on top.
This model inherits from [PreTrainedModel](/docs/transformers/v5.5.3/en/main_classes/model#transformers.PreTrainedModel). Check the superclass documentation for the generic methods the
library implements for all its model (such as downloading or saving, resizing the input embeddings, pruning heads
etc.)
This model is also a PyTorch [torch.nn.Module](https://pytorch.org/docs/stable/nn.html#torch.nn.Module) subclass.
Use it as a regular PyTorch Module and refer to the PyTorch documentation for all matter related to general usage
and behavior.
forward
[< source >](https://github.com/huggingface/transformers/blob/v5.5.3/src/transformers/models/layoutlm/modeling_layoutlm.py#L432)
( input_ids: torch.LongTensor | None = None bbox: torch.LongTensor | None = None attention_mask: torch.FloatTensor | None = None token_type_ids: torch.LongTensor | None = None position_ids: torch.LongTensor | None = None inputs_embeds: torch.FloatTensor | None = None **kwargs: typing_extensions.Unpack[transformers.utils.generic.TransformersKwargs] ) → [BaseModelOutputWithPooling](/docs/transformers/v5.5.3/en/main_classes/output#transformers.modeling_outputs.BaseModelOutputWithPooling) or tuple(torch.FloatTensor)
Parameters
[input_ids (](#transformers.LayoutLMModel.forward.input_ids)torch.LongTensor
of shape(batch_size, sequence_length)
, optional) — Indices of input sequence tokens in the vocabulary. Padding will be ignored by default.Indices can be obtained using
[AutoTokenizer](/docs/transformers/v5.5.3/en/model_doc/auto#transformers.AutoTokenizer). See[PreTrainedTokenizer.encode()](/docs/transformers/v5.5.3/en/internal/tokenization_utils#transformers.PreTrainedTokenizerBase.encode)and[PreTrainedTokenizer.call()](/docs/transformers/v5.5.3/en/internal/tokenization_utils#transformers.PreTrainedTokenizerBase.__call__)for details.[bbox (](#transformers.LayoutLMModel.forward.bbox)torch.LongTensor
of shape(batch_size, sequence_length, 4)
, optional) — Bounding boxes of each input sequence tokens. Selected in the range[0, config.max_2d_position_embeddings-1]
. Each bounding box should be a normalized version in (x0, y0, x1, y1) format, where (x0, y0) corresponds to the position of the upper left corner in the bounding box, and (x1, y1) represents the position of the lower right corner. See[Overview](#Overview)for normalization.[attention_mask (](#transformers.LayoutLMModel.forward.attention_mask)torch.FloatTensor
of shape(batch_size, sequence_length)
, optional) — Mask to avoid performing attention on padding token indices. Mask values selected in[0, 1]
:- 1 for tokens that are not masked,
- 0 for tokens that are masked.
[token_type_ids (](#transformers.LayoutLMModel.forward.token_type_ids)torch.LongTensor
of shape(batch_size, sequence_length)
, optional) — Segment token indices to indicate first and second portions of the inputs. Indices are selected in[0, 1]
:- 0 corresponds to a sentence A token,
- 1 corresponds to a sentence B token.
[position_ids (](#transformers.LayoutLMModel.forward.position_ids)torch.LongTensor
of shape(batch_size, sequence_length)
, optional) — Indices of positions of each input sequence tokens in the position embeddings. Selected in the range[0, config.n_positions - 1]
.[inputs_embeds (](#transformers.LayoutLMModel.forward.inputs_embeds)torch.FloatTensor
of shape(batch_size, sequence_length, hidden_size)
, optional) — Optionally, instead of passinginput_ids
you can choose to directly pass an embedded representation. This is useful if you want more control over how to convertinput_ids
indices into associated vectors than the model’s internal embedding lookup matrix.
Returns
[BaseModelOutputWithPooling](/docs/transformers/v5.5.3/en/main_classes/output#transformers.modeling_outputs.BaseModelOutputWithPooling) or tuple(torch.FloatTensor)
A [BaseModelOutputWithPooling](/docs/transformers/v5.5.3/en/main_classes/output#transformers.modeling_outputs.BaseModelOutputWithPooling) or a tuple of
torch.FloatTensor
(if return_dict=False
is passed or when config.return_dict=False
) comprising various
elements depending on the configuration ([LayoutLMConfig](/docs/transformers/v5.5.3/en/model_doc/layoutlm#transformers.LayoutLMConfig)) and inputs.
The [LayoutLMModel](/docs/transformers/v5.5.3/en/model_doc/layoutlm#transformers.LayoutLMModel) forward method, overrides the __call__
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
Examples:
>>> from transformers import AutoTokenizer, LayoutLMModel
>>> import torch
>>> tokenizer = AutoTokenizer.from_pretrained("microsoft/layoutlm-base-uncased")
>>> model = LayoutLMModel.from_pretrained("microsoft/layoutlm-base-uncased")
>>> words = ["Hello", "world"]
>>> normalized_word_boxes = [637, 773, 693, 782], [698, 773, 733, 782]
>>> token_boxes = []
>>> for word, box in zip(words, normalized_word_boxes):
... word_tokens = tokenizer.tokenize(word)
... token_boxes.extend([box] * len(word_tokens))
>>> # add bounding boxes of cls + sep tokens
>>> token_boxes = [[0, 0, 0, 0]] + token_boxes + [[1000, 1000, 1000, 1000]]
>>> encoding = tokenizer(" ".join(words), return_tensors="pt")
>>> input_ids = encoding["input_ids"]
>>> attention_mask = encoding["attention_mask"]
>>> token_type_ids = encoding["token_type_ids"]
>>> bbox = torch.tensor([token_boxes])
>>> outputs = model(
... input_ids=input_ids, bbox=bbox, attention_mask=attention_mask, token_type_ids=token_type_ids
... )
>>> last_hidden_states = outputs.last_hidden_state
LayoutLMForMaskedLM
class transformers.LayoutLMForMaskedLM
[< source >](https://github.com/huggingface/transformers/blob/v5.5.3/src/transformers/models/layoutlm/modeling_layoutlm.py#L530)
( config )
Parameters
[config (](#transformers.LayoutLMForMaskedLM.config)[LayoutLMForMaskedLM](/docs/transformers/v5.5.3/en/model_doc/layoutlm#transformers.LayoutLMForMaskedLM)) — Model configuration class with all the parameters of the model. Initializing with a config file does not load the weights associated with the model, only the configuration. Check out the[from_pretrained()](/docs/transformers/v5.5.3/en/main_classes/model#transformers.PreTrainedModel.from_pretrained)method to load the model weights.
The Layoutlm Model with a language modeling
head on top.”
This model inherits from [PreTrainedModel](/docs/transformers/v5.5.3/en/main_classes/model#transformers.PreTrainedModel). Check the superclass documentation for the generic methods the
library implements for all its model (such as downloading or saving, resizing the input embeddings, pruning heads
etc.)
This model is also a PyTorch [torch.nn.Module](https://pytorch.org/docs/stable/nn.html#torch.nn.Module) subclass.
Use it as a regular PyTorch Module and refer to the PyTorch documentation for all matter related to general usage
and behavior.
forward
[< source >](https://github.com/huggingface/transformers/blob/v5.5.3/src/transformers/models/layoutlm/modeling_layoutlm.py#L555)
( input_ids: torch.LongTensor | None = None bbox: torch.LongTensor | None = None attention_mask: torch.FloatTensor | None = None token_type_ids: torch.LongTensor | None = None position_ids: torch.LongTensor | None = None inputs_embeds: torch.FloatTensor | None = None labels: torch.LongTensor | None = None **kwargs: typing_extensions.Unpack[transformers.utils.generic.TransformersKwargs] ) → [MaskedLMOutput](/docs/transformers/v5.5.3/en/main_classes/output#transformers.modeling_outputs.MaskedLMOutput) or tuple(torch.FloatTensor)
Parameters
[input_ids (](#transformers.LayoutLMForMaskedLM.forward.input_ids)torch.LongTensor
of shape(batch_size, sequence_length)
, optional) — Indices of input sequence tokens in the vocabulary. Padding will be ignored by default.Indices can be obtained using
[AutoTokenizer](/docs/transformers/v5.5.3/en/model_doc/auto#transformers.AutoTokenizer). See[PreTrainedTokenizer.encode()](/docs/transformers/v5.5.3/en/internal/tokenization_utils#transformers.PreTrainedTokenizerBase.encode)and[PreTrainedTokenizer.call()](/docs/transformers/v5.5.3/en/internal/tokenization_utils#transformers.PreTrainedTokenizerBase.__call__)for details.[bbox (](#transformers.LayoutLMForMaskedLM.forward.bbox)torch.LongTensor
of shape(batch_size, sequence_length, 4)
, optional) — Bounding boxes of each input sequence tokens. Selected in the range[0, config.max_2d_position_embeddings-1]
. Each bounding box should be a normalized version in (x0, y0, x1, y1) format, where (x0, y0) corresponds to the position of the upper left corner in the bounding box, and (x1, y1) represents the position of the lower right corner. See[Overview](#Overview)for normalization.[attention_mask (](#transformers.LayoutLMForMaskedLM.forward.attention_mask)torch.FloatTensor
of shape(batch_size, sequence_length)
, optional) — Mask to avoid performing attention on padding token indices. Mask values selected in[0, 1]
:- 1 for tokens that are not masked,
- 0 for tokens that are masked.
[token_type_ids (](#transformers.LayoutLMForMaskedLM.forward.token_type_ids)torch.LongTensor
of shape(batch_size, sequence_length)
, optional) — Segment token indices to indicate first and second portions of the inputs. Indices are selected in[0, 1]
:- 0 corresponds to a sentence A token,
- 1 corresponds to a sentence B token.
[position_ids (](#transformers.LayoutLMForMaskedLM.forward.position_ids)torch.LongTensor
of shape(batch_size, sequence_length)
, optional) — Indices of positions of each input sequence tokens in the position embeddings. Selected in the range[0, config.n_positions - 1]
.[inputs_embeds (](#transformers.LayoutLMForMaskedLM.forward.inputs_embeds)torch.FloatTensor
of shape(batch_size, sequence_length, hidden_size)
, optional) — Optionally, instead of passinginput_ids
you can choose to directly pass an embedded representation. This is useful if you want more control over how to convertinput_ids
indices into associated vectors than the model’s internal embedding lookup matrix.[labels (](#transformers.LayoutLMForMaskedLM.forward.labels)torch.LongTensor
of shape(batch_size, sequence_length)
, optional) — Labels for computing the masked language modeling loss. Indices should be in[-100, 0, ..., config.vocab_size]
(seeinput_ids
docstring) Tokens with indices set to-100
are ignored (masked), the loss is only computed for the tokens with labels in[0, ..., config.vocab_size]
Returns
[MaskedLMOutput](/docs/transformers/v5.5.3/en/main_classes/output#transformers.modeling_outputs.MaskedLMOutput) or tuple(torch.FloatTensor)
A [MaskedLMOutput](/docs/transformers/v5.5.3/en/main_classes/output#transformers.modeling_outputs.MaskedLMOutput) or a tuple of
torch.FloatTensor
(if return_dict=False
is passed or when config.return_dict=False
) comprising various
elements depending on the configuration ([LayoutLMConfig](/docs/transformers/v5.5.3/en/model_doc/layoutlm#transformers.LayoutLMConfig)) and inputs.
The [LayoutLMForMaskedLM](/docs/transformers/v5.5.3/en/model_doc/layoutlm#transformers.LayoutLMForMaskedLM) forward method, overrides the __call__
special method.
Although the recipe for forward pass needs to be defined within this function, one should call the
Module
instance afterwards instead of this since the former takes care of running the pre and post processing steps while the latter silently ignores them.
loss (
torch.FloatTensor
of shape(1,)
, optional, returned whenlabels
is provided) — Masked language modeling (MLM) loss.logits (
torch.FloatTensor
of shape(batch_size, sequence_length, config.vocab_size)
) — Prediction scores of the language modeling head (scores for each vocabulary token before SoftMax).hidden_states (
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
>>> from transformers import AutoTokenizer, LayoutLMForMaskedLM
>>> import torch
>>> tokenizer = AutoTokenizer.from_pretrained("microsoft/layoutlm-base-uncased")
>>> model = LayoutLMForMaskedLM.from_pretrained("microsoft/layoutlm-base-uncased")
>>> words = ["Hello", "[MASK]"]
>>> normalized_word_boxes = [637, 773, 693, 782], [698, 773, 733, 782]
>>> token_boxes = []
>>> for word, box in zip(words, normalized_word_boxes):
... word_tokens = tokenizer.tokenize(word)
... token_boxes.extend([box] * len(word_tokens))
>>> # add bounding boxes of cls + sep tokens
>>> token_boxes = [[0, 0, 0, 0]] + token_boxes + [[1000, 1000, 1000, 1000]]
>>> encoding = tokenizer(" ".join(words), return_tensors="pt")
>>> input_ids = encoding["input_ids"]
>>> attention_mask = encoding["attention_mask"]
>>> token_type_ids = encoding["token_type_ids"]
>>> bbox = torch.tensor([token_boxes])
>>> labels = tokenizer("Hello world", return_tensors="pt")["input_ids"]
>>> outputs = model(
... input_ids=input_ids,
... bbox=bbox,
... attention_mask=attention_mask,
... token_type_ids=token_type_ids,
... labels=labels,
... )
>>> loss = outputs.loss
LayoutLMForSequenceClassification
class transformers.LayoutLMForSequenceClassification
[< source >](https://github.com/huggingface/transformers/blob/v5.5.3/src/transformers/models/layoutlm/modeling_layoutlm.py#L651)
( config )
Parameters
[config (](#transformers.LayoutLMForSequenceClassification.config)[LayoutLMForSequenceClassification](/docs/transformers/v5.5.3/en/model_doc/layoutlm#transformers.LayoutLMForSequenceClassification)) — Model configuration class with all the parameters of the model. Initializing with a config file does not load the weights associated with the model, only the configuration. Check out the[from_pretrained()](/docs/transformers/v5.5.3/en/main_classes/model#transformers.PreTrainedModel.from_pretrained)method to load the model weights.
LayoutLM Model with a sequence classification head on top (a linear layer on top of the pooled output) e.g. for
document image classification tasks such as the [RVL-CDIP](https://www.cs.cmu.edu/~aharley/rvl-cdip/) dataset.
This model inherits from [PreTrainedModel](/docs/transformers/v5.5.3/en/main_classes/model#transformers.PreTrainedModel). Check the superclass documentation for the generic methods the
library implements for all its model (such as downloading or saving, resizing the input embeddings, pruning heads
etc.)
This model is also a PyTorch [torch.nn.Module](https://pytorch.org/docs/stable/nn.html#torch.nn.Module) subclass.
Use it as a regular PyTorch Module and refer to the PyTorch documentation for all matter related to general usage
and behavior.
forward
[< source >](https://github.com/huggingface/transformers/blob/v5.5.3/src/transformers/models/layoutlm/modeling_layoutlm.py#L665)
( input_ids: torch.LongTensor | None = None bbox: torch.LongTensor | None = None attention_mask: torch.FloatTensor | None = None token_type_ids: torch.LongTensor | None = None position_ids: torch.LongTensor | None = None inputs_embeds: torch.FloatTensor | None = None labels: torch.LongTensor | None = None **kwargs: typing_extensions.Unpack[transformers.utils.generic.TransformersKwargs] ) → [SequenceClassifierOutput](/docs/transformers/v5.5.3/en/main_classes/output#transformers.modeling_outputs.SequenceClassifierOutput) or tuple(torch.FloatTensor)
Parameters
[input_ids (](#transformers.LayoutLMForSequenceClassification.forward.input_ids)torch.LongTensor
of shape(batch_size, sequence_length)
, optional) — Indices of input sequence tokens in the vocabulary. Padding will be ignored by default.Indices can be obtained using
[AutoTokenizer](/docs/transformers/v5.5.3/en/model_doc/auto#transformers.AutoTokenizer). See[PreTrainedTokenizer.encode()](/docs/transformers/v5.5.3/en/internal/tokenization_utils#transformers.PreTrainedTokenizerBase.encode)and[PreTrainedTokenizer.call()](/docs/transformers/v5.5.3/en/internal/tokenization_utils#transformers.PreTrainedTokenizerBase.__call__)for details.[bbox (](#transformers.LayoutLMForSequenceClassification.forward.bbox)torch.LongTensor
of shape(batch_size, sequence_length, 4)
, optional) — Bounding boxes of each input sequence tokens. Selected in the range[0, config.max_2d_position_embeddings-1]
. Each bounding box should be a normalized version in (x0, y0, x1, y1) format, where (x0, y0) corresponds to the position of the upper left corner in the bounding box, and (x1, y1) represents the position of the lower right corner. See[Overview](#Overview)for normalization.[attention_mask (](#transformers.LayoutLMForSequenceClassification.forward.attention_mask)torch.FloatTensor
of shape(batch_size, sequence_length)
, optional) — Mask to avoid performing attention on padding token indices. Mask values selected in[0, 1]
:- 1 for tokens that are not masked,
- 0 for tokens that are masked.
[token_type_ids (](#transformers.LayoutLMForSequenceClassification.forward.token_type_ids)torch.LongTensor
of shape(batch_size, sequence_length)
, optional) — Segment token indices to indicate first and second portions of the inputs. Indices are selected in[0, 1]
:- 0 corresponds to a sentence A token,
- 1 corresponds to a sentence B token.
[position_ids (](#transformers.LayoutLMForSequenceClassification.forward.position_ids)torch.LongTensor
of shape(batch_size, sequence_length)
, optional) — Indices of positions of each input sequence tokens in the position embeddings. Selected in the range[0, config.n_positions - 1]
.[inputs_embeds (](#transformers.LayoutLMForSequenceClassification.forward.inputs_embeds)torch.FloatTensor
of shape(batch_size, sequence_length, hidden_size)
, optional) — Optionally, instead of passinginput_ids
you can choose to directly pass an embedded representation. This is useful if you want more control over how to convertinput_ids
indices into associated vectors than the model’s internal embedding lookup matrix.[labels (](#transformers.LayoutLMForSequenceClassification.forward.labels)torch.LongTensor
of shape(batch_size,)
, optional) — Labels for computing the sequence classification/regression loss. Indices should be in[0, ..., config.num_labels - 1]
. Ifconfig.num_labels == 1
a regression loss is computed (Mean-Square loss), Ifconfig.num_labels > 1
a classification loss is computed (Cross-Entropy).
Returns
[SequenceClassifierOutput](/docs/transformers/v5.5.3/en/main_classes/output#transformers.modeling_outputs.SequenceClassifierOutput) or tuple(torch.FloatTensor)
A [SequenceClassifierOutput](/docs/transformers/v5.5.3/en/main_classes/output#transformers.modeling_outputs.SequenceClassifierOutput) or a tuple of
torch.FloatTensor
(if return_dict=False
is passed or when config.return_dict=False
) comprising various
elements depending on the configuration ([LayoutLMConfig](/docs/transformers/v5.5.3/en/model_doc/layoutlm#transformers.LayoutLMConfig)) and inputs.
The [LayoutLMForSequenceClassification](/docs/transformers/v5.5.3/en/model_doc/layoutlm#transformers.LayoutLMForSequenceClassification) forward method, overrides the __call__
special method.
Although the recipe for forward pass needs to be defined within this function, one should call the
Module
instance afterwards instead of this since the former takes care of running the pre and post processing steps while the latter silently ignores them.
loss (
torch.FloatTensor
of shape(1,)
, optional, returned whenlabels
is provided) — Classification (or regression if config.num_labels==1) loss.logits (
torch.FloatTensor
of shape(batch_size, config.num_labels)
) — Classification (or regression if config.num_labels==1) scores (before SoftMax).hidden_states (
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
>>> from transformers import AutoTokenizer, LayoutLMForSequenceClassification
>>> import torch
>>> tokenizer = AutoTokenizer.from_pretrained("microsoft/layoutlm-base-uncased")
>>> model = LayoutLMForSequenceClassification.from_pretrained("microsoft/layoutlm-base-uncased")
>>> words = ["Hello", "world"]
>>> normalized_word_boxes = [637, 773, 693, 782], [698, 773, 733, 782]
>>> token_boxes = []
>>> for word, box in zip(words, normalized_word_boxes):
... word_tokens = tokenizer.tokenize(word)
... token_boxes.extend([box] * len(word_tokens))
>>> # add bounding boxes of cls + sep tokens
>>> token_boxes = [[0, 0, 0, 0]] + token_boxes + [[1000, 1000, 1000, 1000]]
>>> encoding = tokenizer(" ".join(words), return_tensors="pt")
>>> input_ids = encoding["input_ids"]
>>> attention_mask = encoding["attention_mask"]
>>> token_type_ids = encoding["token_type_ids"]
>>> bbox = torch.tensor([token_boxes])
>>> sequence_label = torch.tensor([1])
>>> outputs = model(
... input_ids=input_ids,
... bbox=bbox,
... attention_mask=attention_mask,
... token_type_ids=token_type_ids,
... labels=sequence_label,
... )
>>> loss = outputs.loss
>>> logits = outputs.logits
LayoutLMForTokenClassification
class transformers.LayoutLMForTokenClassification
[< source >](https://github.com/huggingface/transformers/blob/v5.5.3/src/transformers/models/layoutlm/modeling_layoutlm.py#L779)
( config )
Parameters
[config (](#transformers.LayoutLMForTokenClassification.config)[LayoutLMForTokenClassification](/docs/transformers/v5.5.3/en/model_doc/layoutlm#transformers.LayoutLMForTokenClassification)) — Model configuration class with all the parameters of the model. Initializing with a config file does not load the weights associated with the model, only the configuration. Check out the[from_pretrained()](/docs/transformers/v5.5.3/en/main_classes/model#transformers.PreTrainedModel.from_pretrained)method to load the model weights.
LayoutLM Model with a token classification head on top (a linear layer on top of the hidden-states output) e.g. for
sequence labeling (information extraction) tasks such as the [FUNSD](https://guillaumejaume.github.io/FUNSD/)
dataset and the [SROIE](https://rrc.cvc.uab.es/?ch=13) dataset.
This model inherits from [PreTrainedModel](/docs/transformers/v5.5.3/en/main_classes/model#transformers.PreTrainedModel). Check the superclass documentation for the generic methods the
library implements for all its model (such as downloading or saving, resizing the input embeddings, pruning heads
etc.)
This model is also a PyTorch [torch.nn.Module](https://pytorch.org/docs/stable/nn.html#torch.nn.Module) subclass.
Use it as a regular PyTorch Module and refer to the PyTorch documentation for all matter related to general usage
and behavior.
forward
[< source >](https://github.com/huggingface/transformers/blob/v5.5.3/src/transformers/models/layoutlm/modeling_layoutlm.py#L793)
( input_ids: torch.LongTensor | None = None bbox: torch.LongTensor | None = None attention_mask: torch.FloatTensor | None = None token_type_ids: torch.LongTensor | None = None position_ids: torch.LongTensor | None = None inputs_embeds: torch.FloatTensor | None = None labels: torch.LongTensor | None = None **kwargs: typing_extensions.Unpack[transformers.utils.generic.TransformersKwargs] ) → [TokenClassifierOutput](/docs/transformers/v5.5.3/en/main_classes/output#transformers.modeling_outputs.TokenClassifierOutput) or tuple(torch.FloatTensor)
Parameters
[input_ids (](#transformers.LayoutLMForTokenClassification.forward.input_ids)torch.LongTensor
of shape(batch_size, sequence_length)
, optional) — Indices of input sequence tokens in the vocabulary. Padding will be ignored by default.Indices can be obtained using
[AutoTokenizer](/docs/transformers/v5.5.3/en/model_doc/auto#transformers.AutoTokenizer). See[PreTrainedTokenizer.encode()](/docs/transformers/v5.5.3/en/internal/tokenization_utils#transformers.PreTrainedTokenizerBase.encode)and[PreTrainedTokenizer.call()](/docs/transformers/v5.5.3/en/internal/tokenization_utils#transformers.PreTrainedTokenizerBase.__call__)for details.[bbox (](#transformers.LayoutLMForTokenClassification.forward.bbox)torch.LongTensor
of shape(batch_size, sequence_length, 4)
, optional) — Bounding boxes of each input sequence tokens. Selected in the range[0, config.max_2d_position_embeddings-1]
. Each bounding box should be a normalized version in (x0, y0, x1, y1) format, where (x0, y0) corresponds to the position of the upper left corner in the bounding box, and (x1, y1) represents the position of the lower right corner. See[Overview](#Overview)for normalization.[attention_mask (](#transformers.LayoutLMForTokenClassification.forward.attention_mask)torch.FloatTensor
of shape(batch_size, sequence_length)
, optional) — Mask to avoid performing attention on padding token indices. Mask values selected in[0, 1]
:- 1 for tokens that are not masked,
- 0 for tokens that are masked.
[token_type_ids (](#transformers.LayoutLMForTokenClassification.forward.token_type_ids)torch.LongTensor
of shape(batch_size, sequence_length)
, optional) — Segment token indices to indicate first and second portions of the inputs. Indices are selected in[0, 1]
:- 0 corresponds to a sentence A token,
- 1 corresponds to a sentence B token.
[position_ids (](#transformers.LayoutLMForTokenClassification.forward.position_ids)torch.LongTensor
of shape(batch_size, sequence_length)
, optional) — Indices of positions of each input sequence tokens in the position embeddings. Selected in the range[0, config.n_positions - 1]
.[inputs_embeds (](#transformers.LayoutLMForTokenClassification.forward.inputs_embeds)torch.FloatTensor
of shape(batch_size, sequence_length, hidden_size)
, optional) — Optionally, instead of passinginput_ids
you can choose to directly pass an embedded representation. This is useful if you want more control over how to convertinput_ids
indices into associated vectors than the model’s internal embedding lookup matrix.[labels (](#transformers.LayoutLMForTokenClassification.forward.labels)torch.LongTensor
of shape(batch_size, sequence_length)
, optional) — Labels for computing the token classification loss. Indices should be in[0, ..., config.num_labels - 1]
.
Returns
[TokenClassifierOutput](/docs/transformers/v5.5.3/en/main_classes/output#transformers.modeling_outputs.TokenClassifierOutput) or tuple(torch.FloatTensor)
A [TokenClassifierOutput](/docs/transformers/v5.5.3/en/main_classes/output#transformers.modeling_outputs.TokenClassifierOutput) or a tuple of
torch.FloatTensor
(if return_dict=False
is passed or when config.return_dict=False
) comprising various
elements depending on the configuration ([LayoutLMConfig](/docs/transformers/v5.5.3/en/model_doc/layoutlm#transformers.LayoutLMConfig)) and inputs.
The [LayoutLMForTokenClassification](/docs/transformers/v5.5.3/en/model_doc/layoutlm#transformers.LayoutLMForTokenClassification) forward method, overrides the __call__
special method.
Although the recipe for forward pass needs to be defined within this function, one should call the
Module
instance afterwards instead of this since the former takes care of running the pre and post processing steps while the latter silently ignores them.
loss (
torch.FloatTensor
of shape(1,)
, optional, returned whenlabels
is provided) — Classification loss.logits (
torch.FloatTensor
of shape(batch_size, sequence_length, config.num_labels)
) — Classification scores (before SoftMax).hidden_states (
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
>>> from transformers import AutoTokenizer, LayoutLMForTokenClassification
>>> import torch
>>> tokenizer = AutoTokenizer.from_pretrained("microsoft/layoutlm-base-uncased")
>>> model = LayoutLMForTokenClassification.from_pretrained("microsoft/layoutlm-base-uncased")
>>> words = ["Hello", "world"]
>>> normalized_word_boxes = [637, 773, 693, 782], [698, 773, 733, 782]
>>> token_boxes = []
>>> for word, box in zip(words, normalized_word_boxes):
... word_tokens = tokenizer.tokenize(word)
... token_boxes.extend([box] * len(word_tokens))
>>> # add bounding boxes of cls + sep tokens
>>> token_boxes = [[0, 0, 0, 0]] + token_boxes + [[1000, 1000, 1000, 1000]]
>>> encoding = tokenizer(" ".join(words), return_tensors="pt")
>>> input_ids = encoding["input_ids"]
>>> attention_mask = encoding["attention_mask"]
>>> token_type_ids = encoding["token_type_ids"]
>>> bbox = torch.tensor([token_boxes])
>>> token_labels = torch.tensor([1, 1, 0, 0]).unsqueeze(0) # batch size of 1
>>> outputs = model(
... input_ids=input_ids,
... bbox=bbox,
... attention_mask=attention_mask,
... token_type_ids=token_type_ids,
... labels=token_labels,
... )
>>> loss = outputs.loss
>>> logits = outputs.logits
LayoutLMForQuestionAnswering
class transformers.LayoutLMForQuestionAnswering
[< source >](https://github.com/huggingface/transformers/blob/v5.5.3/src/transformers/models/layoutlm/modeling_layoutlm.py#L881)
( config has_visual_segment_embedding = True )
Parameters
[config (](#transformers.LayoutLMForQuestionAnswering.config)[LayoutLMForQuestionAnswering](/docs/transformers/v5.5.3/en/model_doc/layoutlm#transformers.LayoutLMForQuestionAnswering)) — Model configuration class with all the parameters of the model. Initializing with a config file does not load the weights associated with the model, only the configuration. Check out the[from_pretrained()](/docs/transformers/v5.5.3/en/main_classes/model#transformers.PreTrainedModel.from_pretrained)method to load the model weights.[has_visual_segment_embedding (](#transformers.LayoutLMForQuestionAnswering.has_visual_segment_embedding)bool
, optional, defaults toTrue
) — Whether or not to add visual segment embeddings.
The Layoutlm transformer with a span classification head on top for extractive question-answering tasks like
SQuAD (a linear layer on top of the hidden-states output to compute span start logits
and span end logits
).
This model inherits from [PreTrainedModel](/docs/transformers/v5.5.3/en/main_classes/model#transformers.PreTrainedModel). Check the superclass documentation for the generic methods the
library implements for all its model (such as downloading or saving, resizing the input embeddings, pruning heads
etc.)
This model is also a PyTorch [torch.nn.Module](https://pytorch.org/docs/stable/nn.html#torch.nn.Module) subclass.
Use it as a regular PyTorch Module and refer to the PyTorch documentation for all matter related to general usage
and behavior.
forward
[< source >](https://github.com/huggingface/transformers/blob/v5.5.3/src/transformers/models/layoutlm/modeling_layoutlm.py#L899)
( input_ids: torch.LongTensor | None = None bbox: torch.LongTensor | None = None attention_mask: torch.FloatTensor | None = None token_type_ids: torch.LongTensor | None = None position_ids: torch.LongTensor | None = None inputs_embeds: torch.FloatTensor | None = None start_positions: torch.LongTensor | None = None end_positions: torch.LongTensor | None = None **kwargs: typing_extensions.Unpack[transformers.utils.generic.TransformersKwargs] ) → [QuestionAnsweringModelOutput](/docs/transformers/v5.5.3/en/main_classes/output#transformers.modeling_outputs.QuestionAnsweringModelOutput) or tuple(torch.FloatTensor)
Parameters
[input_ids (](#transformers.LayoutLMForQuestionAnswering.forward.input_ids)torch.LongTensor
of shape(batch_size, sequence_length)
, optional) — Indices of input sequence tokens in the vocabulary. Padding will be ignored by default.Indices can be obtained using
[AutoTokenizer](/docs/transformers/v5.5.3/en/model_doc/auto#transformers.AutoTokenizer). See[PreTrainedTokenizer.encode()](/docs/transformers/v5.5.3/en/internal/tokenization_utils#transformers.PreTrainedTokenizerBase.encode)and[PreTrainedTokenizer.call()](/docs/transformers/v5.5.3/en/internal/tokenization_utils#transformers.PreTrainedTokenizerBase.__call__)for details.[bbox (](#transformers.LayoutLMForQuestionAnswering.forward.bbox)torch.LongTensor
of shape(batch_size, sequence_length, 4)
, optional) — Bounding boxes of each input sequence tokens. Selected in the range[0, config.max_2d_position_embeddings-1]
. Each bounding box should be a normalized version in (x0, y0, x1, y1) format, where (x0, y0) corresponds to the position of the upper left corner in the bounding box, and (x1, y1) represents the position of the lower right corner. See[Overview](#Overview)for normalization.[attention_mask (](#transformers.LayoutLMForQuestionAnswering.forward.attention_mask)torch.FloatTensor
of shape(batch_size, sequence_length)
, optional) — Mask to avoid performing attention on padding token indices. Mask values selected in[0, 1]
:- 1 for tokens that are not masked,
- 0 for tokens that are masked.
[token_type_ids (](#transformers.LayoutLMForQuestionAnswering.forward.token_type_ids)torch.LongTensor
of shape(batch_size, sequence_length)
, optional) — Segment token indices to indicate first and second portions of the inputs. Indices are selected in[0, 1]
:- 0 corresponds to a sentence A token,
- 1 corresponds to a sentence B token.
[position_ids (](#transformers.LayoutLMForQuestionAnswering.forward.position_ids)torch.LongTensor
of shape(batch_size, sequence_length)
, optional) — Indices of positions of each input sequence tokens in the position embeddings. Selected in the range[0, config.n_positions - 1]
.[inputs_embeds (](#transformers.LayoutLMForQuestionAnswering.forward.inputs_embeds)torch.FloatTensor
of shape(batch_size, sequence_length, hidden_size)
, optional) — Optionally, instead of passinginput_ids
you can choose to directly pass an embedded representation. This is useful if you want more control over how to convertinput_ids
indices into associated vectors than the model’s internal embedding lookup matrix.[start_positions (](#transformers.LayoutLMForQuestionAnswering.forward.start_positions)torch.LongTensor
of shape(batch_size,)
, optional) — Labels for position (index) of the start of the labelled span for computing the token classification loss. Positions are clamped to the length of the sequence (sequence_length
). Position outside of the sequence are not taken into account for computing the loss.[end_positions (](#transformers.LayoutLMForQuestionAnswering.forward.end_positions)torch.LongTensor
of shape(batch_size,)
, optional) — Labels for position (index) of the end of the labelled span for computing the token classification loss. Positions are clamped to the length of the sequence (sequence_length
). Position outside of the sequence are not taken into account for computing the loss.
Returns
[QuestionAnsweringModelOutput](/docs/transformers/v5.5.3/en/main_classes/output#transformers.modeling_outputs.QuestionAnsweringModelOutput) or tuple(torch.FloatTensor)
A [QuestionAnsweringModelOutput](/docs/transformers/v5.5.3/en/main_classes/output#transformers.modeling_outputs.QuestionAnsweringModelOutput) or a tuple of
torch.FloatTensor
(if return_dict=False
is passed or when config.return_dict=False
) comprising various
elements depending on the configuration ([LayoutLMConfig](/docs/transformers/v5.5.3/en/model_doc/layoutlm#transformers.LayoutLMConfig)) and inputs.
The [LayoutLMForQuestionAnswering](/docs/transformers/v5.5.3/en/model_doc/layoutlm#transformers.LayoutLMForQuestionAnswering) forward method, overrides the __call__
special method.
Although the recipe for forward pass needs to be defined within this function, one should call the
Module
instance afterwards instead of this since the former takes care of running the pre and post processing steps while the latter silently ignores them.
loss (
torch.FloatTensor
of shape(1,)
, optional, returned whenlabels
is provided) — Total span extraction loss is the sum of a Cross-Entropy for the start and end positions.start_logits (
torch.FloatTensor
of shape(batch_size, sequence_length)
) — Span-start scores (before SoftMax).end_logits (
torch.FloatTensor
of shape(batch_size, sequence_length)
) — Span-end scores (before SoftMax).hidden_states (
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
Example:
In the example below, we prepare a question + context pair for the LayoutLM model. It will give us a prediction of what it thinks the answer is (the span of the answer within the texts parsed from the image).
>>> from transformers import AutoTokenizer, LayoutLMForQuestionAnswering
>>> from datasets import load_dataset
>>> import torch
>>> tokenizer = AutoTokenizer.from_pretrained("impira/layoutlm-document-qa", add_prefix_space=True)
>>> model = LayoutLMForQuestionAnswering.from_pretrained("impira/layoutlm-document-qa", revision="1e3ebac")
>>> dataset = load_dataset("nielsr/funsd", split="train")
>>> example = dataset[0]
>>> question = "what's his name?"
>>> words = example["words"]
>>> boxes = example["bboxes"]
>>> encoding = tokenizer(
... question.split(), words, is_split_into_words=True, return_token_type_ids=True, return_tensors="pt"
... )
>>> bbox = []
>>> for i, s, w in zip(encoding.input_ids[0], encoding.sequence_ids(0), encoding.word_ids(0)):
... if s == 1:
... bbox.append(boxes[w])
... elif i == tokenizer.sep_token_id:
... bbox.append([1000] * 4)
... else:
... bbox.append([0] * 4)
>>> encoding["bbox"] = torch.tensor([bbox])
>>> word_ids = encoding.word_ids(0)
>>> outputs = model(**encoding)
>>> loss = outputs.loss
>>> start_scores = outputs.start_logits
>>> end_scores = outputs.end_logits
>>> start, end = word_ids[start_scores.argmax(-1)], word_ids[end_scores.argmax(-1)]
>>> print(" ".join(words[start : end + 1]))
M. Hamann P. Harper, P. Martinez
[Update on GitHub](https://github.com/huggingface/transformers/blob/main/docs/source/en/model_doc/layoutlm.md)