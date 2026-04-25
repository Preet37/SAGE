# Card: DeepSpeed config knobs that change memory/throughput
**Source:** https://www.deepspeed.ai/docs/config-json/  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Concrete config fields (batch sizing, ZeRO stages/offload, fp16/bf16, gradient clipping)

## Key Content
- **Batch size identity (Eq. 1):**  
  `train_batch_size = train_micro_batch_size_per_gpu * gradient_accumulation_steps * num_gpus`  
  - `train_batch_size`: effective batch per optimizer update  
  - `train_micro_batch_size_per_gpu`: per-GPU batch per fwd/bwd  
  - `gradient_accumulation_steps`: steps to accumulate before update (default **1**)  
  DeepSpeed can infer the 3rd value if you set any 2.
- **Gradient clipping:** `gradient_clipping` (float), default **1.0**.
- **Mixed precision modes (mutual exclusivity):**
  - `fp16` dict (cannot combine with `amp`): defaults include `enabled:false`, `loss_scale:0.0` (dynamic), `initial_scale_power:16` (scale=2^16), `loss_scale_window:1000`, `hysteresis:2`, `min_loss_scale:1`.
  - `bf16` dict (cannot combine with `fp16` or `amp`): `enabled:false`; options `bf16_master_weights_and_grads`, `bf16_optimizer_states`.
  - `amp` not compatible with **ZeRO** (per doc).
  - `torch_autocast`: `enabled:false`, `dtype:"bfloat16"`, `lower_precision_safe_modules` default includes Linear/Conv*.
- **ZeRO optimization (`zero_optimization.stage`):**  
  Stage **0/1/2/3** = disabled / partition optimizer states / partition optimizer+gradients / partition optimizer+gradients+parameters.  
  Common defaults: `allgather_bucket_size:5e8`, `reduce_bucket_size:5e8`, `overlap_comm:false`, `reduce_scatter:true`, `contiguous_gradients:true`.
- **Offload constraints:**
  - `offload_param` (params to **cpu|nvme**) is **stage 3 only**; defaults: `device:"cpu"`, `nvme_path:"/local_nvme"`, `buffer_count:5`, `buffer_size:1e8`, `max_in_cpu:1e9`, `pin_memory:false`.
  - `offload_optimizer` valid for **stage 1/2/3**; NVMe only with **stage 3**; defaults: `device:"cpu"`, `ratio:1`, `buffer_count:4`, `pin_memory:false`.
  - `cpu_offload` is **deprecated** (use `offload_optimizer`).

## When to surface
Use when students ask how DeepSpeed settings change effective batch size, stability (loss scaling/clipping), or memory/throughput tradeoffs (ZeRO stage, bucket sizes, CPU/NVMe offload) that can affect RLHF/PPO/DPO training dynamics.