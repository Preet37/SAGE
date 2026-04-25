# Source: https://huggingface.co/docs/transformers/main_classes/text_generation
# Author: Hugging Face
# Author Slug: hugging-face
# Title: Hugging Face Transformers — Text generation API (Generation)
# Fetched via: trafilatura
# Date: 2026-04-11

Transformers documentation
Generation
Generation
Each framework has a generate method for text generation implemented in their respective GenerationMixin
class:
- PyTorch
[generate()](/docs/transformers/v5.5.3/en/main_classes/text_generation#transformers.GenerationMixin.generate)is implemented in[GenerationMixin](/docs/transformers/v5.5.3/en/main_classes/text_generation#transformers.GenerationMixin).
You can parameterize the generate method with a [GenerationConfig](/docs/transformers/v5.5.3/en/main_classes/text_generation#transformers.GenerationConfig) class instance. Please refer to this class for the complete list of generation parameters, which control the behavior of the generation method.
To learn how to inspect a model’s generation configuration, what are the defaults, how to change the parameters ad hoc,
and how to create and save a customized generation configuration, refer to the
[text generation strategies guide](../generation_strategies). The guide also explains how to use related features,
like token streaming.
GenerationConfig
class transformers.GenerationConfig
[< source >](https://github.com/huggingface/transformers/blob/v5.5.3/src/transformers/generation/configuration_utils.py#L83)
( **kwargs )
Parameters that control the length of the output
[max_length (](#transformers.GenerationConfig.max_length)int
, optional) —max_new_tokens
is recommended for controlling how many tokens the model generates.max_length
remains for backward compatibility.[max_new_tokens (](#transformers.GenerationConfig.max_new_tokens)int
, optional) — The maximum numbers of tokens to generate, ignoring the number of tokens in the prompt.[min_length (](#transformers.GenerationConfig.min_length)int
, optional) — The minimum length of the sequence to be generated. Corresponds to the length of the input prompt +min_new_tokens
. Its effect is overridden bymin_new_tokens
, if also set.[min_new_tokens (](#transformers.GenerationConfig.min_new_tokens)int
, optional) — The minimum numbers of tokens to generate, ignoring the number of tokens in the prompt.[early_stopping (](#transformers.GenerationConfig.early_stopping)bool
orstr
, optional) — Controls the stopping condition for beam-based methods, like beam-search. It accepts the following values:True
, where the generation stops as soon as there arenum_beams
complete candidates;False
, where an heuristic is applied and the generation stops when is it very unlikely to find better candidates;"never"
, where the beam search procedure only stops when there cannot be better candidates (canonical beam search algorithm).[max_time (](#transformers.GenerationConfig.max_time)float
, optional) — The maximum amount of time you allow the computation to run for in seconds. generation will still finish the current pass after allocated time has been passed.[stop_strings (](#transformers.GenerationConfig.stop_strings)str or list[str]
, optional) — A string or a list of strings that should terminate generation if the model outputs them.
Parameters that control the generation strategy used
[do_sample (](#transformers.GenerationConfig.do_sample)bool
) — Whether or not to use sampling ; use greedy decoding otherwise.[num_beams (](#transformers.GenerationConfig.num_beams)int
, optional) — Number of beams for beam search. 1 means no beam search.
Parameters that control the cache
[use_cache (](#transformers.GenerationConfig.use_cache)bool
) — Whether or not the model should use the past last key/values attentions (if applicable to the model) to speed up decoding.[cache_implementation (](#transformers.GenerationConfig.cache_implementation)str
, optional) — Name of the cache class that will be instantiated ingenerate
, for faster decoding. Possible values are:"dynamic"
:[DynamicCache](/docs/transformers/v5.5.3/en/internal/generation_utils#transformers.DynamicCache)"static"
:[StaticCache](/docs/transformers/v5.5.3/en/internal/generation_utils#transformers.StaticCache)"offloaded"
:DynamicCache(offloaded=True)
"offloaded_static"
:StaticCache(offloaded=True)
"quantized"
:[QuantizedCache](/docs/transformers/v5.5.3/en/internal/generation_utils#transformers.QuantizedCache)
If none is specified, we will use the default cache for the model (which is often
[DynamicCache](/docs/transformers/v5.5.3/en/internal/generation_utils#transformers.DynamicCache)). See our[cache documentation](https://huggingface.co/docs/transformers/en/kv_cache)for further information.[cache_config (](#transformers.GenerationConfig.cache_config)dict
, optional, default toNone
) — Arguments used in the key-value cache class can be passed incache_config
.
Parameters for manipulation of the model output logits
[temperature (](#transformers.GenerationConfig.temperature)float
, optional) — The value used to module the next token probabilities. This value is set in a model’sgeneration_config.json
file. If it isn’t set, the default value is 1.0[top_k (](#transformers.GenerationConfig.top_k)int
, optional) — The number of highest probability vocabulary tokens to keep for top-k-filtering. This value is set in a model’sgeneration_config.json
file. If it isn’t set, the default value is 50.[top_p (](#transformers.GenerationConfig.top_p)float
, optional) — If set to float < 1, only the smallest set of most probable tokens with probabilities that add up totop_p
or higher are kept for generation. This value is set in a model’sgeneration_config.json
file. If it isn’t set, the default value is 1.0[min_p (](#transformers.GenerationConfig.min_p)float
, optional) — Minimum token probability, which will be scaled by the probability of the most likely token. It must be a value between 0 and 1. Typical values are in the 0.01-0.2 range, comparably selective as settingtop_p
in the 0.99-0.8 range (use the opposite of normaltop_p
values).[top_h (](#transformers.GenerationConfig.top_h)float
, optional) — Entropy budget scaling factor, which controls how much of the distribution’s entropy is preserved when sampling. Must be a value between 0 and 1. At each step, tokens are sorted by probability, and the smallest prefix of tokens is kept whose renormalized entropy is less than or equal totop_h
times the entropy of the full distribution. Smaller values (e.g., 0.2–0.5) lead to more focused, deterministic outputs, while values closer to 1.0 allow more randomness and diversity. Typical values are in the 0.3–0.6 range.[typical_p (](#transformers.GenerationConfig.typical_p)float
, optional) — Local typicality measures how similar the conditional probability of predicting a target token next is to the expected conditional probability of predicting a random token next, given the partial text already generated. If set to float < 1, the smallest set of the most locally typical tokens with probabilities that add up totypical_p
or higher are kept for generation. See[this paper](https://huggingface.co/papers/2202.00666)for more details.[epsilon_cutoff (](#transformers.GenerationConfig.epsilon_cutoff)float
, optional) — If set to float strictly between 0 and 1, only tokens with a conditional probability greater thanepsilon_cutoff
will be sampled. In the paper, suggested values range from 3e-4 to 9e-4, depending on the size of the model. See[Truncation Sampling as Language Model Desmoothing](https://huggingface.co/papers/2210.15191)for more details.[eta_cutoff (](#transformers.GenerationConfig.eta_cutoff)float
, optional) — Eta sampling is a hybrid of locally typical sampling and epsilon sampling. If set to float strictly between 0 and 1, a token is only considered if it is greater than eithereta_cutoff
orsqrt(eta_cutoff) * exp(-entropy(softmax(next_token_logits)))
. The latter term is intuitively the expected next token probability, scaled bysqrt(eta_cutoff)
. In the paper, suggested values range from 3e-4 to 2e-3, depending on the size of the model. See[Truncation Sampling as Language Model Desmoothing](https://huggingface.co/papers/2210.15191)for more details.[repetition_penalty (](#transformers.GenerationConfig.repetition_penalty)float
, optional) — The parameter for repetition penalty. 1.0 means no penalty. See[this paper](https://huggingface.co/papers/1909.05858)for more details.[encoder_repetition_penalty (](#transformers.GenerationConfig.encoder_repetition_penalty)float
, optional) — The parameter for encoder_repetition_penalty. An exponential penalty on sequences that are not in the original input. 1.0 means no penalty.[length_penalty (](#transformers.GenerationConfig.length_penalty)float
, optional) — Exponential penalty to the length that is used with beam-based generation. It is applied as an exponent to the sequence length, which in turn is used to divide the score of the sequence. Since the score is the log likelihood of the sequence (i.e. negative),length_penalty
> 0.0 promotes longer sequences, whilelength_penalty
< 0.0 encourages shorter sequences.[no_repeat_ngram_size (](#transformers.GenerationConfig.no_repeat_ngram_size)int
, optional) — If set to int > 0, all ngrams of that size can only occur once.[bad_words_ids (](#transformers.GenerationConfig.bad_words_ids)list[list[int]]
, optional) — List of list of token ids that are not allowed to be generated. Check[NoBadWordsLogitsProcessor](/docs/transformers/v5.5.3/en/internal/generation_utils#transformers.NoBadWordsLogitsProcessor)for further documentation and examples.[renormalize_logits (](#transformers.GenerationConfig.renormalize_logits)bool
) — Whether to renormalize the logits after applying all the logits processors (including the custom ones). It’s highly recommended to set this flag toTrue
as the search algorithms suppose the score logits are normalized but some logit processors break the normalization.[forced_bos_token_id (](#transformers.GenerationConfig.forced_bos_token_id)int
, optional, defaults tomodel.config.forced_bos_token_id
) — The id of the token to force as the first generated token after thedecoder_start_token_id
. Useful for multilingual models like[mBART](../model_doc/mbart)where the first generated token needs to be the target language token.[forced_eos_token_id (](#transformers.GenerationConfig.forced_eos_token_id)int
or list[int], *optional*, defaults to
model.config.forced_eos_token_id) -- The id of the token to force as the last generated token when
max_length` is reached. Optionally, use a list to set multiple end-of-sequence tokens.[remove_invalid_values (](#transformers.GenerationConfig.remove_invalid_values)bool
) — Whether to remove possible nan and inf outputs of the model to prevent the generation method to crash. Note that usingremove_invalid_values
can slow down generation.[exponential_decay_length_penalty (](#transformers.GenerationConfig.exponential_decay_length_penalty)tuple(int, float)
, optional) — This Tuple adds an exponentially increasing length penalty, after a certain amount of tokens have been generated. The tuple shall consist of:(start_index, decay_factor)
wherestart_index
indicates where penalty starts anddecay_factor
represents the factor of exponential decay[suppress_tokens (](#transformers.GenerationConfig.suppress_tokens)list[int]
, optional) — A list of tokens that will be suppressed at generation. TheSuppressTokens
logit processor will set their log probs to-inf
so that they are not sampled.[begin_suppress_tokens (](#transformers.GenerationConfig.begin_suppress_tokens)list[int]
, optional) — A list of tokens that will be suppressed at the beginning of the generation. TheSuppressBeginTokens
logit processor will set their log probs to-inf
so that they are not sampled.[sequence_bias (](#transformers.GenerationConfig.sequence_bias)dict[tuple[int], float]
, optional)) — Dictionary that maps a sequence of tokens to its bias term. Positive biases increase the odds of the sequence being selected, while negative biases do the opposite. Check[SequenceBiasLogitsProcessor](/docs/transformers/v5.5.3/en/internal/generation_utils#transformers.SequenceBiasLogitsProcessor)for further documentation and examples.[token_healing (](#transformers.GenerationConfig.token_healing)bool
) — Heal tail tokens of prompts by replacing them with their appropriate extensions. This enhances the quality of completions for prompts affected by greedy tokenization bias.[guidance_scale (](#transformers.GenerationConfig.guidance_scale)float
, optional) — The guidance scale for classifier free guidance (CFG). CFG is enabled by settingguidance_scale > 1
. Higher guidance scale encourages the model to generate samples that are more closely linked to the input prompt, usually at the expense of poorer quality.[watermarking_config (](#transformers.GenerationConfig.watermarking_config)BaseWatermarkingConfig
ordict
, optional) — Arguments used to watermark the model outputs by adding a small bias to randomly selected set of “green” tokens. See the docs of[SynthIDTextWatermarkingConfig](/docs/transformers/v5.5.3/en/internal/generation_utils#transformers.SynthIDTextWatermarkingConfig)and[WatermarkingConfig](/docs/transformers/v5.5.3/en/internal/generation_utils#transformers.WatermarkingConfig)for more details. If passed asDict
, it will be converted to aWatermarkingConfig
internally.
Parameters that define the output variables of generate
[num_return_sequences (](#transformers.GenerationConfig.num_return_sequences)int
, optional) — The number of independently computed returned sequences for each element in the batch.[output_attentions (](#transformers.GenerationConfig.output_attentions)bool
) — Whether or not to return the attentions tensors of all attention layers. Seeattentions
under returned tensors for more details.[output_hidden_states (](#transformers.GenerationConfig.output_hidden_states)bool
) — Whether or not to return the hidden states of all layers. Seehidden_states
under returned tensors for more details.[output_scores (](#transformers.GenerationConfig.output_scores)bool
) — Whether or not to return the prediction scores. Seescores
under returned tensors for more details.[output_logits (](#transformers.GenerationConfig.output_logits)bool
) — Whether or not to return the unprocessed prediction logit scores. Seelogits
under returned tensors for more details.[return_dict_in_generate (](#transformers.GenerationConfig.return_dict_in_generate)bool
) — Whether or not to return a[ModelOutput](/docs/transformers/v5.5.3/en/main_classes/output#transformers.utils.ModelOutput), as opposed to returning exclusively the generated sequence. This flag must be set toTrue
to return the generation cache (whenuse_cache
isTrue
) or optional outputs (see flags starting withoutput_
)
Special tokens that can be used at generation time
[pad_token_id (](#transformers.GenerationConfig.pad_token_id)int
, optional) — The id of the padding token.[bos_token_id (](#transformers.GenerationConfig.bos_token_id)int
, optional) — The id of the beginning-of-sequence token.[eos_token_id (](#transformers.GenerationConfig.eos_token_id)Union[int, list[int]]
, optional) — The id of the end-of-sequence token. Optionally, use a list to set multiple end-of-sequence tokens.
Generation parameters exclusive to encoder-decoder models
[encoder_no_repeat_ngram_size (](#transformers.GenerationConfig.encoder_no_repeat_ngram_size)int
, optional) — If set to int > 0, all ngrams of that size that occur in theencoder_input_ids
cannot occur in thedecoder_input_ids
.[decoder_start_token_id (](#transformers.GenerationConfig.decoder_start_token_id)int
orlist[int]
, optional) — If an encoder-decoder model starts decoding with a different token than bos, the id of that token or a list of lengthbatch_size
. Indicating a list enables different start ids for each element in the batch (e.g. multilingual models with different target languages in one batch)
Generation parameters exclusive to assistant generation
[is_assistant (](#transformers.GenerationConfig.is_assistant)bool
) — Whether the model is an assistant (draft) model.[num_assistant_tokens (](#transformers.GenerationConfig.num_assistant_tokens)int
, optional) — Defines the number of speculative tokens that shall be generated by the assistant model before being checked by the target model at each iteration. Higher values fornum_assistant_tokens
make the generation more speculative : If the assistant model is performant larger speed-ups can be reached, if the assistant model requires lots of corrections, lower speed-ups are reached.[num_assistant_tokens_schedule (](#transformers.GenerationConfig.num_assistant_tokens_schedule)str
, optional) — Defines the schedule at which max assistant tokens shall be changed during inference."heuristic"
: When all speculative tokens are correct, increasenum_assistant_tokens
by 2 else reduce by 1.num_assistant_tokens
value is persistent over multiple generation calls with the same assistant model."heuristic_transient"
: Same as"heuristic"
butnum_assistant_tokens
is reset to its initial value after each generation call."constant"
:num_assistant_tokens
stays unchanged during generation
[assistant_confidence_threshold (](#transformers.GenerationConfig.assistant_confidence_threshold)float
, optional) — The confidence threshold for the assistant model. If the assistant model’s confidence in its prediction for the current token is lower than this threshold, the assistant model stops the current token generation iteration, even if the number of speculative tokens (defined bynum_assistant_tokens
) is not yet reached. The assistant’s confidence threshold is adjusted throughout the speculative iterations to reduce the number of unnecessary draft and target forward passes, biased towards avoiding false negatives.assistant_confidence_threshold
value is persistent over multiple generation calls with the same assistant model. It is an unsupervised version of the dynamic speculation lookahead from Dynamic Speculation Lookahead Accelerates Speculative Decoding of Large Language Models[https://huggingface.co/papers/2405.04304](https://huggingface.co/papers/2405.04304).[prompt_lookup_num_tokens (](#transformers.GenerationConfig.prompt_lookup_num_tokens)int
, optional) — The number of tokens to be output as candidate tokens.[max_matching_ngram_size (](#transformers.GenerationConfig.max_matching_ngram_size)int
, optional) — The maximum ngram size to be considered for matching in the prompt. Default to 2 if not provided.[assistant_early_exit(](#transformers.GenerationConfig.assistant_early_exit(int,)int
, optional) — If set to a positive integer, early exit of the model will be used as an assistant. Can only be used with models that support early exit (i.e. models where logits from intermediate layers can be interpreted by the LM head).[assistant_lookbehind(](#transformers.GenerationConfig.assistant_lookbehind(int,)int
, optional) — If set to a positive integer, the re-encodeing process will additionally consider the lastassistant_lookbehind
assistant tokens to correctly align tokens. Can only be used with different tokenizers in speculative decoding. See this[blog](https://huggingface.co/blog/universal_assisted_generation)for more details.[target_lookbehind(](#transformers.GenerationConfig.target_lookbehind(int,)int
, optional) — If set to a positive integer, the re-encodeing process will additionally consider the lasttarget_lookbehind
target tokens to correctly align tokens. Can only be used with different tokenizers in speculative decoding. See this[blog](https://huggingface.co/blog/universal_assisted_generation)for more details.
Parameters related to performances and compilation
[compile_config (CompileConfig, optional) — If using a compilable cache, this controls how](#transformers.GenerationConfig.compile_config)generate
willcompile
the forward pass for faster inference.[disable_compile (](#transformers.GenerationConfig.disable_compile)bool
) — Whether to disable the automatic compilation of the forward pass. Automatic compilation happens when specific criteria are met, including using a compilable cache. Please open an issue if you find the need to use this flag.
Class that holds a configuration for a generation task. A generate
call supports the following generation methods
for text-decoder, text-to-text, speech-to-text, and vision-to-text models:
- greedy decoding if
num_beams=1
anddo_sample=False
- multinomial sampling if
num_beams=1
anddo_sample=True
- beam-search decoding if
num_beams>1
anddo_sample=False
- beam-search multinomial sampling if
num_beams>1
anddo_sample=True
- assisted decoding if
assistant_model
orprompt_lookup_num_tokens
is passed to.generate()
To learn more about decoding strategies refer to the [text generation strategies guide](../generation_strategies).
A large number of these flags control the logits or the stopping criteria of the generation. Make sure you check the
[generate-related classes]for a full description of the possible manipulations, as well as examples of their usage.
Note: the configuration fields that are still None
will be overridden by GenerationConfig._get_default_generation_params()
during the generation loop. If you want to use different values for these fields, make sure to explicitly set them in the
generation config.
from_pretrained
[< source >](https://github.com/huggingface/transformers/blob/v5.5.3/src/transformers/generation/configuration_utils.py#L827)
( pretrained_model_name: str | os.PathLike config_file_name: str | os.PathLike | None = None cache_dir: str | os.PathLike | None = None force_download: bool = False local_files_only: bool = False token: str | bool | None = None revision: str = 'main' **kwargs ) → [GenerationConfig](/docs/transformers/v5.5.3/en/main_classes/text_generation#transformers.GenerationConfig)
Parameters
[pretrained_model_name (](#transformers.GenerationConfig.from_pretrained.pretrained_model_name)str
oros.PathLike
) — This can be either:- a string, the model id of a pretrained model configuration hosted inside a model repo on huggingface.co.
- a path to a directory containing a configuration file saved using the
[save_pretrained()](/docs/transformers/v5.5.3/en/main_classes/text_generation#transformers.GenerationConfig.save_pretrained)method, e.g.,./my_model_directory/
.
[config_file_name (](#transformers.GenerationConfig.from_pretrained.config_file_name)str
oros.PathLike
, optional, defaults to"generation_config.json"
) — Name of the generation configuration JSON file to be loaded frompretrained_model_name
.[cache_dir (](#transformers.GenerationConfig.from_pretrained.cache_dir)str
oros.PathLike
, optional) — Path to a directory in which a downloaded pretrained model configuration should be cached if the standard cache should not be used.[force_download (](#transformers.GenerationConfig.from_pretrained.force_download)bool
, optional, defaults toFalse
) — Whether or not to force to (re-)download the configuration files and override the cached versions if they exist.[proxies (](#transformers.GenerationConfig.from_pretrained.proxies)dict[str, str]
, optional) — A dictionary of proxy servers to use by protocol or endpoint, e.g.,{'http': 'foo.bar:3128', 'http://hostname': 'foo.bar:4012'}.
The proxies are used on each request.[token (](#transformers.GenerationConfig.from_pretrained.token)str
orbool
, optional) — The token to use as HTTP bearer authorization for remote files. IfTrue
, or not specified, will use the token generated when runninghf auth login
(stored in~/.huggingface
).[revision (](#transformers.GenerationConfig.from_pretrained.revision)str
, optional, defaults to"main"
) — The specific model version to use. It can be a branch name, a tag name, or a commit id, since we use a git-based system for storing models and other artifacts on huggingface.co, sorevision
can be any identifier allowed by git.To test a pull request you made on the Hub, you can pass
revision="refs/pr/<pr_number>"
.[return_unused_kwargs (](#transformers.GenerationConfig.from_pretrained.return_unused_kwargs)bool
, optional, defaults toFalse
) — IfFalse
, then this function returns just the final configuration object.If
True
, then this functions returns aTuple(config, unused_kwargs)
where unused_kwargs is a dictionary consisting of the key/value pairs whose keys are not configuration attributes: i.e., the part ofkwargs
which has not been used to updateconfig
and is otherwise ignored.[subfolder (](#transformers.GenerationConfig.from_pretrained.subfolder)str
, optional, defaults to""
) — In case the relevant files are located inside a subfolder of the model repo on huggingface.co, you can specify the folder name here.[kwargs (](#transformers.GenerationConfig.from_pretrained.kwargs)dict[str, Any]
, optional) — The values in kwargs of any keys which are configuration attributes will be used to override the loaded values. Behavior concerning key/value pairs whose keys are not configuration attributes is controlled by thereturn_unused_kwargs
keyword parameter.
Returns
The configuration object instantiated from this pretrained model.
Instantiate a [GenerationConfig](/docs/transformers/v5.5.3/en/main_classes/text_generation#transformers.GenerationConfig) from a generation configuration file.
Examples:
>>> from transformers import GenerationConfig
>>> # Download configuration from huggingface.co and cache.
>>> generation_config = GenerationConfig.from_pretrained("openai-community/gpt2")
>>> # E.g. config was saved using *save_pretrained('./test/saved_model/')*
>>> generation_config.save_pretrained("./test/saved_model/")
>>> generation_config = GenerationConfig.from_pretrained("./test/saved_model/")
>>> # You can also specify configuration names to your generation configuration file
>>> generation_config.save_pretrained("./test/saved_model/", config_file_name="my_configuration.json")
>>> generation_config = GenerationConfig.from_pretrained("./test/saved_model/", "my_configuration.json")
>>> # If you'd like to try a minor variation to an existing configuration, you can also pass generation
>>> # arguments to `.from_pretrained()`. Be mindful that typos and unused arguments will be ignored
>>> generation_config, unused_kwargs = GenerationConfig.from_pretrained(
... "openai-community/gpt2", top_k=1, foo=False, do_sample=True, return_unused_kwargs=True
... )
>>> generation_config.top_k
1
>>> unused_kwargs
{'foo': False}
from_model_config
[< source >](https://github.com/huggingface/transformers/blob/v5.5.3/src/transformers/generation/configuration_utils.py#L1159)
( model_config: typing.Union[ForwardRef('PreTrainedConfig'), dict] ) → [GenerationConfig](/docs/transformers/v5.5.3/en/main_classes/text_generation#transformers.GenerationConfig)
Instantiates a [GenerationConfig](/docs/transformers/v5.5.3/en/main_classes/text_generation#transformers.GenerationConfig) from a [PreTrainedConfig](/docs/transformers/v5.5.3/en/main_classes/configuration#transformers.PreTrainedConfig). This function is useful to convert legacy
[PreTrainedConfig](/docs/transformers/v5.5.3/en/main_classes/configuration#transformers.PreTrainedConfig) objects, which may contain generation parameters, into a stand-alone [GenerationConfig](/docs/transformers/v5.5.3/en/main_classes/text_generation#transformers.GenerationConfig).
save_pretrained
[< source >](https://github.com/huggingface/transformers/blob/v5.5.3/src/transformers/generation/configuration_utils.py#L768)
( save_directory: str | os.PathLike config_file_name: str | os.PathLike | None = None push_to_hub: bool = False **kwargs )
Parameters
[save_directory (](#transformers.GenerationConfig.save_pretrained.save_directory)str
oros.PathLike
) — Directory where the configuration JSON file will be saved (will be created if it does not exist).[config_file_name (](#transformers.GenerationConfig.save_pretrained.config_file_name)str
oros.PathLike
, optional, defaults to"generation_config.json"
) — Name of the generation configuration JSON file to be saved insave_directory
.[push_to_hub (](#transformers.GenerationConfig.save_pretrained.push_to_hub)bool
, optional, defaults toFalse
) — Whether or not to push your model to the Hugging Face model hub after saving it. You can specify the repository you want to push to withrepo_id
(will default to the name ofsave_directory
in your namespace).[kwargs (](#transformers.GenerationConfig.save_pretrained.kwargs)dict[str, Any]
, optional) — Additional key word arguments passed along to the[push_to_hub()](/docs/transformers/v5.5.3/en/main_classes/model#transformers.utils.PushToHubMixin.push_to_hub)method.
Save a generation configuration object to the directory save_directory
, so that it can be re-loaded using the
[from_pretrained()](/docs/transformers/v5.5.3/en/main_classes/text_generation#transformers.GenerationConfig.from_pretrained) class method.
update
[< source >](https://github.com/huggingface/transformers/blob/v5.5.3/src/transformers/generation/configuration_utils.py#L1209)
( defaults_only = False allow_custom_entries = False **kwargs ) → dict[str, Any]
Parameters
[defaults_only (](#transformers.GenerationConfig.update.defaults_only)bool
, optional, defaults toFalse
) — Whether to update all keys in config withkwargs
or only those that are set toNone
(i.e. default value).[allow_custom_entries (](#transformers.GenerationConfig.update.allow_custom_entries)bool
, optional, defaults toFalse
) — Whether to allow updating custom entries into the config withkwargs
if not present in the current config.[kwargs (](#transformers.GenerationConfig.update.kwargs)dict[str, Any]
) — Dictionary of attributes to tentatively update this class.
Returns
dict[str, Any]
Dictionary containing all the key-value pairs that were not used to update the instance.
Updates attributes of this class instance with attributes from kwargs
if they match existing attributes,
returning all the unused kwargs.
validate
[< source >](https://github.com/huggingface/transformers/blob/v5.5.3/src/transformers/generation/configuration_utils.py#L590)
( strict = False )
Validates the values of the attributes of the [GenerationConfig](/docs/transformers/v5.5.3/en/main_classes/text_generation#transformers.GenerationConfig) instance. Raises exceptions in the presence
of parameterization that can be detected as incorrect from the configuration instance alone.
Note that some parameters not validated here are best validated at generate runtime, as they may depend on other inputs and/or the model, such as parameters related to the generation length.
get_generation_mode
[< source >](https://github.com/huggingface/transformers/blob/v5.5.3/src/transformers/generation/configuration_utils.py#L485)
( assistant_model: typing.Optional[ForwardRef('PreTrainedModel')] = None ) → GenerationMode
Returns the generation mode triggered by the [GenerationConfig](/docs/transformers/v5.5.3/en/main_classes/text_generation#transformers.GenerationConfig) instance.
GenerationMixin
A class containing all functions for auto-regressive text generation, to be used as a mixin in model classes.
Inheriting from this class causes the model to have special generation-related behavior, such as loading a
GenerationConfig
at initialization time or ensuring generate
-related tests are run in transformers
CI.
A model class should inherit from GenerationMixin
to enable calling methods like generate
, or when it
has defined a custom generate
method that relies on GenerationMixin
, directly or indirectly, which
approximately shares the same interface to public methods like generate
. Three examples:
LlamaForCausalLM
should inherit fromGenerationMixin
to enable callinggenerate
and other public methods in the mixin;BlipForQuestionAnswering
has a customgenerate
method that approximately shares the same interface asGenerationMixin.generate
(it has a few extra arguments, and the same output). That function also callsGenerationMixin.generate
indirectly, through an inner model. As such,BlipForQuestionAnswering
should inherit fromGenerationMixin
to benefit from all generation-related automation in our codebase;BarkModel
has a customgenerate
method and one of its inner models callsGenerationMixin.generate
. However, itsgenerate
does not share the same interface asGenerationMixin.generate
. In this case,BarkModel
should NOT inherit fromGenerationMixin
, as it breaks thegenerate
interface.
The class exposes [generate()](/docs/transformers/v5.5.3/en/main_classes/text_generation#transformers.GenerationMixin.generate), which can be used for:
- greedy decoding if
num_beams=1
anddo_sample=False
- multinomial sampling if
num_beams=1
anddo_sample=True
- beam-search decoding if
num_beams>1
anddo_sample=False
- beam-search multinomial sampling if
num_beams>1
anddo_sample=True
- assisted decoding if
assistant_model
orprompt_lookup_num_tokens
is passed to.generate()
To learn more about decoding strategies refer to the [text generation strategies guide](../generation_strategies).
generate
[< source >](https://github.com/huggingface/transformers/blob/v5.5.3/src/transformers/generation/utils.py#L2130)
( inputs: torch.Tensor | None = None generation_config: transformers.generation.configuration_utils.GenerationConfig | None = None logits_processor: transformers.generation.logits_process.LogitsProcessorList | None = None stopping_criteria: transformers.generation.stopping_criteria.StoppingCriteriaList | None = None prefix_allowed_tokens_fn: collections.abc.Callable[[int, torch.Tensor], list[int]] | None = None synced_gpus: bool | None = None assistant_model: typing.Optional[ForwardRef('PreTrainedModel')] = None streamer: typing.Optional[ForwardRef('BaseStreamer')] = None negative_prompt_ids: torch.Tensor | None = None negative_prompt_attention_mask: torch.Tensor | None = None custom_generate: str | collections.abc.Callable | None = None **kwargs ) → [ModelOutput](/docs/transformers/v5.5.3/en/main_classes/output#transformers.utils.ModelOutput) or torch.LongTensor
Parameters
[inputs (](#transformers.GenerationMixin.generate.inputs)torch.Tensor
of varying shape depending on the modality, optional) — The sequence used as a prompt for the generation or as model inputs to the encoder. IfNone
the method initializes it withbos_token_id
and a batch size of 1. For decoder-only modelsinputs
should be in the format ofinput_ids
. For encoder-decoder models inputs can represent any ofinput_ids
,input_values
,input_features
, orpixel_values
.[generation_config (](#transformers.GenerationMixin.generate.generation_config)[GenerationConfig](/docs/transformers/v5.5.3/en/main_classes/text_generation#transformers.GenerationConfig), optional) — The generation configuration to be used as base parametrization for the generation call.**kwargs
passed to generate matching the attributes ofgeneration_config
will override them. Ifgeneration_config
is not provided, the default will be used, which has the following loading priority: 1) from thegeneration_config.json
model file, if it exists; 2) from the model configuration. Please note that unspecified parameters will inherit[GenerationConfig](/docs/transformers/v5.5.3/en/main_classes/text_generation#transformers.GenerationConfig)’s default values, whose documentation should be checked to parameterize generation.[logits_processor (](#transformers.GenerationMixin.generate.logits_processor)LogitsProcessorList
, optional) — Custom logits processors that complement the default logits processors built from arguments and generation config. If a logit processor is passed that is already created with the arguments or a generation config an error is thrown. This feature is intended for advanced users.[stopping_criteria (](#transformers.GenerationMixin.generate.stopping_criteria)StoppingCriteriaList
, optional) — Custom stopping criteria that complements the default stopping criteria built from arguments and a generation config. If a stopping criteria is passed that is already created with the arguments or a generation config an error is thrown. If your stopping criteria depends on thescores
input, make sure you passreturn_dict_in_generate=True, output_scores=True
togenerate
. This feature is intended for advanced users.[prefix_allowed_tokens_fn (](#transformers.GenerationMixin.generate.prefix_allowed_tokens_fn)Callable[[int, torch.Tensor], list[int]]
, optional) — If provided, this function constraints the beam search to allowed tokens only at each step. If not provided no constraint is applied. This function takes 2 arguments: the batch IDbatch_id
andinput_ids
. It has to return a list with the allowed tokens for the next generation step conditioned on the batch IDbatch_id
and the previously generated tokensinputs_ids
. This argument is useful for constrained generation conditioned on the prefix, as described in[Autoregressive Entity Retrieval](https://huggingface.co/papers/2010.00904).[synced_gpus (](#transformers.GenerationMixin.generate.synced_gpus)bool
, optional) — Whether to continue running the while loop until max_length. Unless overridden, this flag will be set toTrue
if usingFullyShardedDataParallel
or DeepSpeed ZeRO Stage 3 with multiple GPUs to avoid deadlocking if one GPU finishes generating before other GPUs. Otherwise, defaults toFalse
.[assistant_model (](#transformers.GenerationMixin.generate.assistant_model)PreTrainedModel
, optional) — An assistant model that can be used to accelerate generation. The assistant model must have the exact same tokenizer. The acceleration is achieved when forecasting candidate tokens with the assistant model is much faster than running generation with the model you’re calling generate from. As such, the assistant model should be much smaller.[streamer (](#transformers.GenerationMixin.generate.streamer)BaseStreamer
, optional) — Streamer object that will be used to stream the generated sequences. Generated tokens are passed throughstreamer.put(token_ids)
and the streamer is responsible for any further processing.[negative_prompt_ids (](#transformers.GenerationMixin.generate.negative_prompt_ids)torch.LongTensor
of shape(batch_size, sequence_length)
, optional) — The negative prompt needed for some processors such as CFG. The batch size must match the input batch size. This is an experimental feature, subject to breaking API changes in future versions.[negative_prompt_attention_mask (](#transformers.GenerationMixin.generate.negative_prompt_attention_mask)torch.LongTensor
of shape(batch_size, sequence_length)
, optional) — Attention_mask fornegative_prompt_ids
.[custom_generate (](#transformers.GenerationMixin.generate.custom_generate)str
orCallable
, optional) — One of the following:str
(Hugging Face Hub repository name): runs the customgenerate
function defined atcustom_generate/generate.py
in that repository instead of the standardgenerate
method. The repository fully replaces the generation logic, and the return type may differ.str
(local repository path): same as above but from a local path,trust_remote_code
not required.Callable
:generate
will perform the usual input preparation steps, then call the provided callable to run the decoding loop. For more information, see[the docs](../../generation_strategies#custom-generation-methods).
[kwargs (](#transformers.GenerationMixin.generate.kwargs)dict[str, Any]
, optional) — Ad hoc parametrization ofgeneration_config
and/or additional model-specific kwargs that will be forwarded to theforward
function of the model. If the model is an encoder-decoder model, encoder specific kwargs should not be prefixed and decoder specific kwargs should be prefixed with decoder_.
Returns
[ModelOutput](/docs/transformers/v5.5.3/en/main_classes/output#transformers.utils.ModelOutput) or torch.LongTensor
A [ModelOutput](/docs/transformers/v5.5.3/en/main_classes/output#transformers.utils.ModelOutput) (if return_dict_in_generate=True
or when config.return_dict_in_generate=True
) or a torch.LongTensor
.
If the model is not an encoder-decoder model (model.config.is_encoder_decoder=False
), the possible
[ModelOutput](/docs/transformers/v5.5.3/en/main_classes/output#transformers.utils.ModelOutput) types are:
If the model is an encoder-decoder model (model.config.is_encoder_decoder=True
), the possible
[ModelOutput](/docs/transformers/v5.5.3/en/main_classes/output#transformers.utils.ModelOutput) types are:
Generates sequences of token ids for models with a language modeling head.
Most generation-controlling parameters are set in
generation_config
which, if not passed, will be set to the model’s default generation configuration. You can override anygeneration_config
by passing the corresponding parameters to generate(), e.g..generate(inputs, num_beams=4, do_sample=True)
.For an overview of generation strategies and code examples, check out the
[following guide].
compute_transition_scores
[< source >](https://github.com/huggingface/transformers/blob/v5.5.3/src/transformers/generation/utils.py#L1335)
( sequences: Tensor scores: tuple beam_indices: torch.Tensor | None = None normalize_logits: bool = False ) → torch.Tensor
Parameters
[sequences (](#transformers.GenerationMixin.compute_transition_scores.sequences)torch.LongTensor
) — The generated sequences. The second dimension (sequence_length) is either equal tomax_length
or shorter if all batches finished early due to theeos_token_id
.[scores (](#transformers.GenerationMixin.compute_transition_scores.scores)tuple(torch.FloatTensor)
) — Transition scores for each vocabulary token at each generation step. Beam transition scores consisting of log probabilities of tokens conditioned on log softmax of previously generated tokens in this beam. Tuple oftorch.FloatTensor
with up tomax_new_tokens
elements (one element for each generated token), with each tensor of shape(batch_size*num_beams, config.vocab_size)
.[beam_indices (](#transformers.GenerationMixin.compute_transition_scores.beam_indices)torch.LongTensor
, optional) — Beam indices of generated token id at each generation step.torch.LongTensor
of shape(batch_size*num_return_sequences, sequence_length)
. Only required if anum_beams>1
at generate-time.[normalize_logits (](#transformers.GenerationMixin.compute_transition_scores.normalize_logits)bool
, optional, defaults toFalse
) — Whether to normalize the logits (which, for legacy reasons, may be unnormalized).
Returns
torch.Tensor
A torch.Tensor
of shape (batch_size*num_return_sequences, sequence_length)
containing
the transition scores (logits)
Computes the transition scores of sequences given the generation scores (and beam indices, if beam search was used). This is a convenient method to quickly obtain the scores of the selected tokens at generation time.
Examples:
>>> from transformers import GPT2Tokenizer, AutoModelForCausalLM
>>> import numpy as np
>>> tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
>>> model = AutoModelForCausalLM.from_pretrained("openai-community/gpt2")
>>> tokenizer.pad_token_id = tokenizer.eos_token_id
>>> inputs = tokenizer(["Today is"], return_tensors="pt")
>>> # Example 1: Print the scores for each token generated with Greedy Search
>>> outputs = model.generate(**inputs, max_new_tokens=5, return_dict_in_generate=True, output_scores=True)
>>> transition_scores = model.compute_transition_scores(
... outputs.sequences, outputs.scores, normalize_logits=True
... )
>>> # input_length is the length of the input prompt for decoder-only models, like the GPT family, and 1 for
>>> # encoder-decoder models, like BART or T5.
>>> input_length = 1 if model.config.is_encoder_decoder else inputs.input_ids.shape[1]
>>> generated_tokens = outputs.sequences[:, input_length:]
>>> for tok, score in zip(generated_tokens[0], transition_scores[0]):
... # | token | token string | log probability | probability
... print(f"| {tok:5d} | {tokenizer.decode(tok):8s} | {score.numpy():.3f} | {np.exp(score.numpy()):.2%}")
| 262 | the | -1.414 | 24.33%
| 1110 | day | -2.609 | 7.36%
| 618 | when | -2.010 | 13.40%
| 356 | we | -1.859 | 15.58%
| 460 | can | -2.508 | 8.14%
>>> # Example 2: Reconstruct the sequence scores from Beam Search
>>> outputs = model.generate(
... **inputs,
... max_new_tokens=5,
... num_beams=4,
... num_return_sequences=4,
... return_dict_in_generate=True,
... output_scores=True,
... )
>>> transition_scores = model.compute_transition_scores(
... outputs.sequences, outputs.scores, outputs.beam_indices, normalize_logits=False
... )
>>> # If you sum the generated tokens' scores and apply the length penalty, you'll get the sequence scores.
>>> # Tip 1: recomputing the scores is only guaranteed to match with `normalize_logits=False`. Depending on the
>>> # use case, you might want to recompute it with `normalize_logits=True`.
>>> # Tip 2: the output length does NOT include the input length
>>> output_length = np.sum(transition_scores.numpy() < 0, axis=1)
>>> length_penalty = model.generation_config.length_penalty
>>> reconstructed_scores = transition_scores.sum(axis=1) / (output_length**length_penalty)
>>> print(np.allclose(outputs.sequences_scores, reconstructed_scores))
True
ContinuousMixin
Mixin class for models to add continuous batching capabilities. Continuous batching has three entry points:
init_continuous_batching
, which is the actual entry point for continuous batchingcontinuous_batching_context_manager
, which itself is a wrapper aroundinit_continuous_batching
generate_batch
, which is really a wrapper aroundcontinuous_batching_context_manager
They are defined in this order. Any change made to any of those three entry points should be reflected in the other two.
continuous_batching_context_manager
[< source >](https://github.com/huggingface/transformers/blob/v5.5.3/src/transformers/generation/continuous_batching/continuous_api.py#L1178)
( generation_config: transformers.generation.configuration_utils.GenerationConfig | None = None block: bool = True timeout: float | None = None continuous_batching_config: transformers.generation.configuration_utils.ContinuousBatchingConfig | None = None persistent_manager: bool = False warmup_requests: int | None = 0 **deprecated_kwargs )
A context manager to safely use the continuous batching manager. Arguments are similar to the ones of
init_continuous_batching
, except for:
- block: whether to block the thread when stopping the manager. Default is True.
- timeout: maximum time to wait for the thread to stop. Default is None (no timeout).
- warmup_query_tokens: the number of expected requests for which to warmup. 0 is auto, None is no warmup.
Destroy the cached continuous batching manager and free GPU resources.
generate_batch
[< source >](https://github.com/huggingface/transformers/blob/v5.5.3/src/transformers/generation/continuous_batching/continuous_api.py#L1216)
( inputs: list generation_config: transformers.generation.configuration_utils.GenerationConfig | None = None continuous_batching_config: transformers.generation.configuration_utils.ContinuousBatchingConfig | None = None record_timestamps: bool = False progress_bar: bool = True persistent_manager: bool = False warmup: bool = True **kwargs ) → dict[str, GenerationOutput]
Parameters
[inputs — List of input token sequences (prompts)](#transformers.ContinuousMixin.generate_batch.inputs)[generation_config — Optional generation configuration](#transformers.ContinuousMixin.generate_batch.generation_config)[continuous_batching_config — Optional continuous batching configuration](#transformers.ContinuousMixin.generate_batch.continuous_batching_config)[record_timestamps — If set to true, the requests will have a timestamp for each token generated](#transformers.ContinuousMixin.generate_batch.record_timestamps)[progress_bar — If set to true, a progress bar will be displayed](#transformers.ContinuousMixin.generate_batch.progress_bar)[persistent_manager — whether to persist the manager after the generation is finished. Default is False.](#transformers.ContinuousMixin.generate_batch.persistent_manager)[warmup — whether to pre-capture CUDA graphs before processing requests. Default is True.](#transformers.ContinuousMixin.generate_batch.warmup)[**kwargs — Additional generation parameters. Only max_new_tokens is used, but other deprecated arguments are extracted and passed to the continuous_batching_config object.](#transformers.ContinuousMixin.generate_batch.*kwargs)
Returns
dict[str, GenerationOutput]
a dictionary of request ids to GenerationOutput objects
Generate sequences for a batch of prompts using continuous batching.
init_continuous_batching
[< source >](https://github.com/huggingface/transformers/blob/v5.5.3/src/transformers/generation/continuous_batching/continuous_api.py#L1118)
( generation_config: transformers.generation.configuration_utils.GenerationConfig | None = None continuous_batching_config: transformers.generation.configuration_utils.ContinuousBatchingConfig | None = None **deprecated_kwargs ) → ContinuousBatchingManager
Parameters
[generation_config — An optional generation configuration, which may contain a CompileConfig object](#transformers.ContinuousMixin.init_continuous_batching.generation_config)[continuous_batching_config — An optional continuous batching configuration](#transformers.ContinuousMixin.init_continuous_batching.continuous_batching_config)[**deprecated_kwargs — Deprecated arguments that are now passed in the continuous_batching_config. Those are: max_queue_size, q_padding_interval_size, kv_padding_interval_size, allow_block_sharing, use_async_batching, max_cached_graphs](#transformers.ContinuousMixin.init_continuous_batching.*deprecated_kwargs)
Returns
ContinuousBatchingManager
The manager instance to add requests and retrieve results.
Initialize a manager for continuous batching inference.
ContinuousBatchingManager
class transformers.ContinuousBatchingManager
[< source >](https://github.com/huggingface/transformers/blob/v5.5.3/src/transformers/generation/continuous_batching/continuous_api.py#L711)
( model: ProtoPretrainedModel generation_config: GenerationConfig continuous_batching_config: ContinuousBatchingConfig )
Manager for handling continuous batching of generation requests. It provides a user interface for submitting
generation requests, retrieving results, and managing the background generation thread. This class should not be
created directly, but through one of the following entry points (all methods of the ContinuousMixin
mixin):
init_continuous_batching
continuous_batching_context_manager
generate_batch
add_request
[< source >](https://github.com/huggingface/transformers/blob/v5.5.3/src/transformers/generation/continuous_batching/continuous_api.py#L853)
( input_ids: list request_id: str | None = None max_new_tokens: int | None = None streaming: bool = False record_timestamps: bool = False eos_token_id: int | list[int] | None = None ) → str
Add a new generation request to the queue.
cancel_request
[< source >](https://github.com/huggingface/transformers/blob/v5.5.3/src/transformers/generation/continuous_batching/continuous_api.py#L920)
( request_id: str )
Cancel a request by its ID.
get_result
[< source >](https://github.com/huggingface/transformers/blob/v5.5.3/src/transformers/generation/continuous_batching/continuous_api.py#L930)
( request_id: str | None = None timeout: float | None = None ) → Optional[GenerationOutput]
Retrieve one result from the output queue.
Check if the background generation thread is running.
join
[< source >](https://github.com/huggingface/transformers/blob/v5.5.3/src/transformers/generation/continuous_batching/continuous_api.py#L838)
( stop_trigger_time: float timeout: float | None = None )
Wait for the background thread to finish.
register_result_handler
[< source >](https://github.com/huggingface/transformers/blob/v5.5.3/src/transformers/generation/continuous_batching/continuous_api.py#L971)
( request_id: str callback: Callable )
Register a callback for result delivery (streaming or non-streaming).
The callback is invoked on the event loop via call_soon_threadsafe
each time a result is produced for this request. For streaming requests,
this happens on every token; for non-streaming, only on completion.
The handler is automatically cleaned up when the request finishes.
Iterate over results matching a specific request id (blocking).
Uses the shared output queue with requeue. For high-concurrency serving,
use register_result_handler
instead.
Start the background generation thread.
stop
[< source >](https://github.com/huggingface/transformers/blob/v5.5.3/src/transformers/generation/continuous_batching/continuous_api.py#L798)
( block: bool = True timeout: float | None = None keep_for_next_session: bool = False )
Signal the background thread to stop.
Pre-capture CUDA graphs for varlen and decode paths by running dummy batches. Initializes the batch processor if not already done.
Scheduler
Abstract base class for scheduling requests in the continuous batch processor. Schedulers manage the lifecycle of requests from when they are added to the waiting queue to when they are scheduled for processing. Different schedulers implement different strategies for prioritizing and batching requests.
Adds a request to the waiting list.
Remove all cancelled requests from active and waiting queues.
Completes processing of a request and frees its allocated cache blocks. This method is called when a request has finished generation or encountered an error.
Gets generated tokens for an active request.
Checks if there are requests ready to be processed.
Checks if a request has been cancelled or removed.
Reset scheduler state for a new generation loop.
Schedules requests for the next batch based on available token and cache budgets. This method selects which requests should be processed in the current batch, considering the budgets and the scheduler’s prioritization rules. The token_budget is the maximum number of tokens that can be processed in a batch, and the cache_budget is the maximum number of KV cache entries that can be read in a batch. Returns the list of scheduled requests in their “FutureRequestState” form, a boolean indicating if the decode fast path can be used, the total number of query tokens and the maximum number of kv tokens read.
Marks a request for cancellation.
FIFOScheduler
class transformers.generation.FIFOScheduler
[< source >](https://github.com/huggingface/transformers/blob/v5.5.3/src/transformers/generation/continuous_batching/scheduler.py#L292)
( cache: PagedAttentionCache safety_margin: float = 0.2 )
This scheduler processes requests in the order they arrive, meaning decoding requests has priority over prefilling requests. Additionally, it includes a safety margin mechanism to prevent cache exhaustion. By default, when 80% of the cache is full, new requests will not be scheduled to prioritize decoding active requests.
PrefillFirstScheduler
Scheduler that prioritizes split prefill requests over decoding requests. This scheduler ensures that split prefill requests (which are continuations of partially processed prompts) are completed before processing new decoding requests.
[Update on GitHub](https://github.com/huggingface/transformers/blob/main/docs/source/en/main_classes/text_generation.md)