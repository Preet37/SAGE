# Card: Triton TensorRT‑LLM backend — model config essentials
**Source:** https://docs.nvidia.com/deeplearning/triton-inference-server/archives/triton-inference-server-2540/user-guide/docs/tensorrtllm_backend/docs/model_config.html  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Triton TensorRT‑LLM backend `config.pbtxt` fields, defaults, and performance-tuning notes (batching, KV cache, speculative decoding, removed fields)

## Key Content
- **Template editing procedure:** Config fields are filled via `tools/fill_template.py`. For comma-valued fields (e.g., `gpu_device_ids`, `participant_ids`), **escape commas**:  
  `python3 fill_template.py -i config.pbtxt "gpu_device_ids:0\,1"`.
- **tensorrt_llm mandatory config highlights:**  
  `backend` (set to TensorRT‑LLM backend), `max_batch_size`, `decoupled_mode` (**must be true**), `max_queue_delay_microseconds` (>0 can improve co-batching of close arrivals), `max_queue_size` (reject beyond), `engine_dir`, batching strategy (set to inflight batching), input dtype, logits dtype.
- **KV-cache parameters & defaults (KV cache section):**
  - `max_tokens_in_paged_kv_cache`: max KV tokens; if unspecified interpreted as **infinite**.  
    **Allocation rule (Eq. 1):** `KV_alloc = min(max_tokens_in_paged_kv_cache, KV_from_mem_fraction)`  
    where `KV_from_mem_fraction` is derived from `kv_cache_free_gpu_mem_fraction`.
  - `kv_cache_free_gpu_mem_fraction` default **0.9** (fraction of post-model-load GPU mem usable for KV).
  - `cross_kv_cache_fraction` default **0.5** (encoder-decoder only; rest for self-attn).
  - Note: `enable_trt_overlap` **removed**; overlapping micro-batches didn’t help after CPU overhead reductions.
- **LoRA cache defaults:** `lora_cache_optimal_adapter_size` **8**; `lora_cache_gpu_mem_fraction` **0.05** (after engine + KV cache); host LoRA cache size default **1G**.
- **Speculative decoding (tensorrt_llm_bls):** set `tensorrt_llm_model_name` (target) and `tensorrt_llm_draft_model_name` (draft); request sets `num_draft_tokens`; optional `use_draft_logits`. Not supported with `return_generation_logits`/`return_context_logits`; **batch size > 1 not supported**.
- **Empirical tuning tips (Some tips section):**
  - `instance_count` ideally ≈ engine max batch size; **5** worked well in experiments; too small (e.g., **1**) is discouraged.
  - Inflight batching: keep **#requests < max_batch_size** and **total tokens < max_num_tokens** (engine build-time via `trtllm-build`).

## When to surface
Use when students ask how to tune Triton + TensorRT‑LLM for throughput/latency (inflight batching, `instance_count`, queue delay) or how KV-cache/LoRA cache sizing and speculative decoding constraints are configured in `config.pbtxt`.