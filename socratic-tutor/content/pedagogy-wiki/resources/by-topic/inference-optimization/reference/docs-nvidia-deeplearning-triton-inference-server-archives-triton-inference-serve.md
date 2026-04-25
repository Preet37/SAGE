# Source: https://docs.nvidia.com/deeplearning/triton-inference-server/archives/triton-inference-server-2540/user-guide/docs/tensorrtllm_backend/docs/model_config.html
# Title: Model Configuration#
# Fetched via: trafilatura
# Date: 2026-04-09

Model Configuration[#](#model-configuration)
Model Parameters[#](#model-parameters)
The following tables show the parameters in the config.pbtxt
of the models in
[all_models/inflight_batcher_llm](https://github.com/triton-inference-server/tensorrtllm_backend/blob/main/all_models/inflight_batcher_llm).
that can be modified before deployment. For optimal performance or custom
parameters, please refer to
[perf_best_practices](https://github.com/NVIDIA/TensorRT-LLM/blob/main/docs/source/performance/perf-best-practices.md).
The names of the parameters listed below are the values in the config.pbtxt
that can be modified using the
[ fill_template.py](https://github.com/triton-inference-server/tensorrtllm_backend/blob/main/tools/fill_template.py) script.
NOTE For fields that have comma as the value (e.g. gpu_device_ids
,
participant_ids
), you need to escape the comma with
a backslash. For example, if you want to set gpu_device_ids
to 0,1
you need
to run python3 fill_template.py -i config.pbtxt "gpu_device_ids:0\,1".
The mandatory parameters must be set for the model to run. The optional parameters are not required but can be set to customize the model.
ensemble model[#](#ensemble-model)
See
[here](../../user_guide/architecture.html#ensemble-models)
to learn more about ensemble models.
Mandatory parameters
Name |
Description |
|---|---|
|
The maximum batch size that the Triton model instance will run with. Note that for the |
|
The data type for context and generation logits. |
preprocessing model[#](#preprocessing-model)
Mandatory parameters
Name |
Description |
|---|---|
|
The maximum batch size that Triton should use with the model. |
|
The path to the tokenizer for the model. |
|
The number of instances of the model to run. |
Optional parameters
Name |
Description |
|---|---|
|
The |
|
The vision engine path used in multimodal workflow. |
|
The path to the engine for the model. This parameter is only needed for multimodal processing to extract the |
postprocessing model[#](#postprocessing-model)
Mandatory parameters
Name |
Description |
|---|---|
|
The maximum batch size that Triton should use with the model. |
|
The path to the tokenizer for the model. |
|
The number of instances of the model to run. |
Optional parameters
Name |
Description |
|---|---|
|
The |
tensorrt_llm model[#](#tensorrt-llm-model)
The majority of the tensorrt_llm
model parameters and input/output tensors
can be mapped to parameters in the TRT-LLM C++ runtime API defined in
[ executor.h](https://github.com/NVIDIA/TensorRT-LLM/blob/main/cpp/include/tensorrt_llm/executor/executor.h).
Please refer to the Doxygen comments in
executor.h
for a more detailed
description of the parameters below.Mandatory parameters
Name |
Description |
|---|---|
|
The backend to use for the model. Set to |
|
The maximum batch size that the Triton model instance will run with. Note that for the |
|
Whether to use decoupled mode. Must be set to |
|
The maximum queue delay in microseconds. Setting this parameter to a value greater than 0 can improve the chances that two requests arriving within |
|
The maximum number of requests allowed in the TRT-LLM queue before rejecting new requests. |
|
The path to the engine for the model. |
|
The batching strategy to use. Set to |
|
The dtype for the input tensor |
|
The data type for context and generation logits. |
Optional parameters
General
Name |
Description |
|---|---|
|
When running encoder-decoder models, this is the path to the folder that contains the model configuration and engine for the encoder model. |
|
When using techniques like sliding window attention, the maximum number of tokens that are attended to generate one token. Defaults attends to all tokens in sequence. (default=max_sequence_length) |
|
Number of sink tokens to always keep in attention window. |
|
Set to |
|
The time for cancellation check thread to sleep before doing the next check. It checks if any of the current active requests are cancelled through triton and prevent further execution of them. (default=100) |
|
The time for the statistics reporting thread to sleep before doing the next check. (default=100) |
|
The time for the receiving thread in orchestrator mode to sleep before doing the next check. (default=0) |
|
The maximum number of iterations for which to keep statistics. (default=ExecutorConfig::kDefaultIterStatsMaxIterations) |
|
The maximum number of iterations for which to keep per-request statistics. (default=executor::kDefaultRequestStatsMaxIterations) |
|
Controls if log probabilities should be normalized or not. Set to |
|
Comma-separated list of GPU IDs to use for this model. Use semicolons to separate multiple instances of the model. If not provided, the model will use all visible GPUs. (default=unspecified) |
|
Comma-separated list of MPI ranks to use for this model. Mandatory when using orchestrator mode with -disable-spawn-process (default=unspecified) |
|
Set to a number between 0.0 and 1.0 to specify the percentage of weights that reside on GPU instead of CPU and streaming load during runtime. Values less than 1.0 are only supported for an engine built with |
KV cache
Note that the parameter enable_trt_overlap
has been removed from the
config.pbtxt. This option allowed to overlap execution of two micro-batches to
hide CPU overhead. Optimization work has been done to reduce the CPU overhead
and it was found that the overlapping of micro-batches did not provide
additional benefits.
Name |
Description |
|---|---|
|
The maximum size of the KV cache in number of tokens. If unspecified, value is interpreted as ‘infinite’. KV cache allocation is the min of max_tokens_in_paged_kv_cache and value derived from kv_cache_free_gpu_mem_fraction below. (default=unspecified) |
|
Set to a number between 0 and 1 to indicate the maximum fraction of GPU memory (after loading the model) that may be used for KV cache. (default=0.9) |
|
Set to a number between 0 and 1 to indicate the maximum fraction of KV cache that may be used for cross attention, and the rest will be used for self attention. Optional param and should be set for encoder-decoder models ONLY. (default=0.5) |
|
Enable offloading to host memory for the given byte size. |
|
Set to |
LoRA cache
Name |
Description |
|---|---|
|
Optimal adapter size used to size cache pages. Typically optimally sized adapters will fix exactly into 1 cache page. (default=8) |
|
Used to set the minimum size of a cache page. Pages must be at least large enough to fit a single module, single later adapter_size |
|
Fraction of GPU memory used for LoRA cache. Computed as a fraction of left over memory after engine load, and after KV cache is loaded. (default=0.05) |
|
Size of host LoRA cache in bytes. (default=1G) |
Decoding mode
Name |
Description |
|---|---|
|
The beam width value of requests that will be sent to the executor. (default=1) |
|
Set to one of the following: |
Optimization
Name |
Description |
|---|---|
|
Set to |
|
Set to |
|
Set to |
|
Set to |
|
Sets the size of the CUDA graph cache, in numbers of CUDA graphs. (default=0) |
Scheduling
Name |
Description |
|---|---|
|
Set to |
Medusa
Name |
Description |
|---|---|
|
To specify Medusa choices tree in the format of e.g. “{0, 0, 0}, {0, 1}”. By default, |
Eagle
Name |
Description |
|---|---|
|
To specify default per-server Eagle choices tree in the format of e.g. “{0, 0, 0}, {0, 1}”. By default, |
tensorrt_llm_bls model[#](#tensorrt-llm-bls-model)
See
[here](../../python_backend/README.html#business-logic-scripting)
to learn more about BLS models.
Mandatory parameters
Name |
Description |
|---|---|
|
The maximum batch size that the model can handle. |
|
Whether to use decoupled mode. |
|
The number of instances of the model to run. When using the BLS model instead of the ensemble, you should set the number of model instances to the maximum batch size supported by the TRT engine to allow concurrent request execution. |
|
The data type for context and generation logits. |
Optional parameters
General
Name |
Description |
|---|---|
|
Used in the streaming mode to call the postprocessing model with all accumulated tokens, instead of only one token. This might be necessary for certain tokenizers. |
Speculative decoding
The BLS model supports speculative decoding. Target and draft triton models are set with the parameters tensorrt_llm_model_name
tensorrt_llm_draft_model_name
. Speculative decodingis performed by setting num_draft_tokens
in the request. use_draft_logits
may be set to use logits comparison speculative decoding. Note that return_generation_logits
and return_context_logits
are not supported when using speculative decoding. Also note that requests with batch size greater than 1 is not supported with speculative decoding right now.
Name |
Description |
|---|---|
|
The name of the TensorRT-LLM model to use. |
|
The name of the TensorRT-LLM draft model to use. |
Model Input and Output[#](#model-input-and-output)
Below is the lists of input and output tensors for the tensorrt_llm
and
tensorrt_llm_bls
models.
Common Inputs[#](#common-inputs)
Name |
Shape |
Type |
Description |
|---|---|---|---|
|
[1] |
|
End token ID. If not specified, defaults to -1 |
|
[1] |
|
Padding token ID |
|
[1] |
|
Sampling Config param: |
|
[1] |
|
Sampling Config param: |
|
[1] |
|
Sampling Config param: |
|
[1] |
|
Sampling Config param: |
|
[1] |
|
Sampling Config param: |
|
[1] |
|
Sampling Config param: |
|
[1] |
|
When |
|
[1] |
|
When |
|
[1] |
|
When |
|
[1] |
|
Number of generated sequences per request. (Default=1) |
|
[1] |
|
Beam width for this request; set to 1 for greedy sampling (Default=1) |
|
[1] |
|
P-tuning prompt embedding table |
|
[1] |
|
P-tuning prompt vocab size |
|
[1] |
|
When |
The following inputs for lora are for both tensorrt_llm
and tensorrt_llm_bls
models. The inputs are passed through the tensorrt_llm
model and the
tensorrt_llm_bls
model will refer to the inputs from the tensorrt_llm
model.
Name |
Shape |
Type |
Description |
|---|---|---|---|
|
[1] |
|
The unique task ID for the given LoRA. To perform inference with a specific LoRA for the first time, |
|
[ num_lora_modules_layers, D x Hi + Ho x D ] |
|
Weights for a LoRA adapter. See the config file for more details. |
|
[ num_lora_modules_layers, 3] |
|
Module identifier. See the config file for more details. |
Common Outputs[#](#common-outputs)
Name |
Shape |
Type |
Description |
|---|---|---|---|
|
[-1] |
|
Cumulative probabilities for each output |
|
[beam_width, -1] |
|
Log probabilities for each output |
|
[-1, vocab_size] |
|
Context logits for input |
|
[beam_width, seq_len, vocab_size] |
|
Generation logits for each output |
|
[1] |
|
Batch index |
|
[1] |
|
KV cache reuse metrics. Number of newly allocated blocks per request. Set the optional input |
|
[1] |
|
KV cache reuse metrics. Number of reused blocks per request. Set the optional input |
|
[1] |
|
KV cache reuse metrics. Number of total allocated blocks per request. Set the optional input |
Unique Inputs for tensorrt_llm model[#](#unique-inputs-for-tensorrt-llm-model)
Name |
Shape |
Type |
Description |
|---|---|---|---|
|
[-1] |
|
Input token IDs |
|
[1] |
|
Input lengths |
|
[1] |
|
Requested output length |
|
[-1] |
|
Draft input IDs |
|
[-1] |
|
Decoder input IDs |
|
[1] |
|
Decoder input lengths |
|
[-1, -1] |
|
Draft logits |
|
[1] |
|
Draft acceptance threshold |
|
[2, -1] |
|
List of stop words |
|
[2, -1] |
|
List of bad words |
|
[-1] |
|
Embedding bias words |
|
[1] |
|
Top-k value for runtime top-k sampling |
|
[1] |
|
Top-p value for runtime top-p sampling |
|
[1] |
|
Minimum value for runtime top-p sampling |
|
[1] |
|
Decay value for runtime top-p sampling |
|
[1] |
|
Reset IDs for runtime top-p sampling |
|
[1] |
|
Controls how to penalize longer sequences in beam search (Default=0.f) |
|
[1] |
|
Enable early stopping |
|
[1] |
|
Beam search diversity rate |
|
[1] |
|
Stop flag |
|
[1] |
|
Enable streaming |
Unique Outputs for tensorrt_llm model[#](#unique-outputs-for-tensorrt-llm-model)
Name |
Shape |
Type |
Description |
|---|---|---|---|
|
[-1, -1] |
|
Output token IDs |
|
[-1] |
|
Sequence length |
Unique Inputs for tensorrt_llm_bls model[#](#unique-inputs-for-tensorrt-llm-bls-model)
Name |
Shape |
Type |
Description |
|---|---|---|---|
|
[-1] |
|
Prompt text |
|
[1] |
|
Decoder input text |
|
[3, 224, 224] |
|
Input image |
|
[-1] |
|
Number of tokens to generate |
|
[2, num_bad_words] |
|
Bad words list |
|
[2, num_stop_words] |
|
Stop words list |
|
[1] |
|
Sampling Config param: |
|
[1] |
|
Sampling Config param: |
|
[1] |
|
Sampling Config param: |
|
[1] |
|
When |
|
[-1] |
|
Embedding bias words |
|
[-1] |
|
Embedding bias weights |
|
[1] |
|
Number of tokens to get from draft model during speculative decoding |
|
[1] |
|
Use logit comparison during speculative decoding |
Unique Outputs for tensorrt_llm_bls model[#](#unique-outputs-for-tensorrt-llm-bls-model)
Name |
Shape |
Type |
Description |
|---|---|---|---|
|
[-1] |
|
Text output |
Some tips for model configuration[#](#some-tips-for-model-configuration)
Below are some tips for configuring models for optimal performance. These
recommendations are based on our experiments and may not apply to all use cases.
For guidance on other parameters, please refer to the
[perf_best_practices](https://github.com/NVIDIA/TensorRT-LLM/blob/main/docs/source/performance/perf-best-practices.md).
Setting the
instance_count
for models to better utilize inflight batchingThe
instance_count
parameter in the config.pbtxt file specifies the number of instances of the model to run. Ideally, this should be set to match the maximum batch size supported by the TRT engine, as this allows for concurrent request execution and reduces performance bottlenecks. However, it will also consume more CPU memory resources. While the optimal value isn’t something we can determine in advance, it generally shouldn’t be set to a very small value, such as 1. For most use cases, we have found that settinginstance_count
to 5 works well across a variety of workloads in our experiments.Adjusting
max_batch_size
andmax_num_tokens
to optimize inflight batchingmax_batch_size
andmax_num_tokens
are important parameters for optimizing inflight batching. You can modifymax_batch_size
in the model configuration file, whilemax_num_tokens
is set during the conversion to a TRT-LLM engine using thetrtllm-build
command. Tuning these parameters is necessary for different scenarios, and experimentation is currently the best approach to finding optimal values. Generally, the total number of requests should be lower thanmax_batch_size
, and the total tokens should be less thanmax_num_tokens
.