# Card: vLLM Engine Args (Long-Context & KV/Attention-Relevant Flags)
**Source:** https://docs.vllm.ai/en/v0.6.1/models/engine_args.html  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Authoritative CLI/API parameter names + defaults for vLLM serving settings that affect long-context behavior, KV cache, and performance.

## Key Content
- **Context length control**
  - `--max-model-len`: *Model context length*; if unset, **auto-derived from model config**.
  - `--disable-sliding-window`: disables sliding window behavior (caps to sliding window size otherwise).
- **RoPE / context extension knobs**
  - `--rope-scaling`: RoPE scaling JSON, e.g. `{"type":"dynamic","factor":2.0}` (factor scales context).
  - `--rope-theta`: RoPE theta; used with `rope_scaling` and can improve performance of scaled models.
- **KV cache memory/accuracy tradeoffs**
  - `--kv-cache-dtype {auto, fp8, fp8_e5m2, fp8_e4m3}`; default **auto** (= model dtype). CUDA 11.8+ supports FP8; ROCm supports `fp8_e4m3`.
  - `--quantization-param-path`: JSON scaling factors for KV cache (generally needed for FP8 KV); otherwise scaling defaults to **1.0** (may hurt accuracy).
- **Batching/scheduling limits impacting long prompts**
  - `--max-num-batched-tokens`: max batched tokens per iteration (throughput/latency tradeoff).
  - `--max-num-seqs`: default **256** sequences per iteration.
  - `--enable-chunked-prefill`: chunk prefill based on `max_num_batched_tokens` (helps very long prompts).
- **CUDA graphs vs eager fallback (long seq performance)**
  - `--max-seq-len-to-capture`: default **8192**; sequences longer fall back to eager mode.
  - `--enforce-eager`: always eager-mode PyTorch (disables CUDA-graph hybrid).
- **Memory provisioning**
  - `--gpu-memory-utilization`: default **0.9** fraction of GPU memory for executor.
  - `--swap-space`: default **4 GiB per GPU**.
  - `--cpu-offload-gb`: default **0**; “virtual GPU memory” via CPU offload (requires fast interconnect).
- **KV block granularity**
  - `--block-size {8,16,32}`; default **16** (token block size for contiguous chunks).

## When to surface
Use when students ask how to configure vLLM for **longer context**, **RoPE scaling**, **KV cache dtype/FP8**, **chunked prefill**, or why long sequences may **fall back from CUDA graphs** (e.g., >8192).