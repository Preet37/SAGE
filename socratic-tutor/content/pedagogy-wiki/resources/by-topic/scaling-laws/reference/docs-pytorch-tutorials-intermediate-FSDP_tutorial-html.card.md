# Card: PyTorch FSDP2 (fully_shard) essentials
**Source:** https://docs.pytorch.org/tutorials/intermediate/FSDP_tutorial.html  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** FSDP2-specific behavior + recommended configuration patterns (wrapping, init, state dicts) vs FSDP1

## Key Content
- **Core algorithm (FSDP vs DDP):** FSDP shards **parameters, gradients, optimizer states** across ranks to cut memory. Runtime pattern:  
  1) **Before fwd/bwd:** all-gather sharded params → unsharded params  
  2) **During bwd:** local unsharded grads → **reduce-scatter** → sharded grads  
  3) **Optimizer:** updates sharded params; optimizer state remains sharded  
  (FSDP ≈ DDP all-reduce decomposed into **all-gather + reduce-scatter**.)
- **Wrapping procedure (recommended):** apply `fully_shard()` to **submodules AND root**. Example: shard each Transformer block first, then `fully_shard(model)`. This keeps non-active layers sharded during a layer’s compute (lower peak memory).
- **Parameter representation/defaults:** `fully_shard` converts `model.parameters()` from `torch.Tensor` → **DTensor**, default placement **`Shard(dim=0)`**. Inspect local shard via `param.to_local()`. Build optimizer **after** sharding: `optim = Adam(model.parameters(), ...)`.
- **Prefetching:**  
  - **Implicit (default):** CPU issues all-gather for layer *i* before compute; queued on separate CUDA stream; overlaps with compute for non-CPU-bound workloads.  
  - **Explicit:** control schedules with `set_modules_to_forward_prefetch(...)`, `set_modules_to_backward_prefetch(...)`; can prefetch **2+ layers** (higher memory, potentially faster). Trigger first all-gather earlier via `model.unshard()`.
- **Mixed precision policy:** `MixedPrecisionPolicy(param_dtype=bfloat16, reduce_dtype=float32)`; params are **float32 when sharded**, **bfloat16 when unsharded**; gradient reduce-scatter in **float32** for numerics.
- **Checkpointing/state dict workflows:**  
  - **DTensor API:** load full tensors → `distribute_tensor(full_tensor, device_mesh, placements)`; `load_state_dict(..., assign=True)` (meta tensors). Save by `DTensor.full_tensor()` (all-gather) and rank0 `cpu()` offload.  
  - **DCP API:** `set_model_state_dict(..., StateDictOptions(full_state_dict=True, broadcast_from_rank0=True))`; save via `get_model_state_dict(..., full_state_dict=True, cpu_offload=True)`.
- **Migration highlights (FSDP1→FSDP2):** no `param_init_fn`; shard under `meta`, then `model.to_empty(device="cuda"); model.reset_parameters()`. `use_orig_params` always; `buffer_dtype` omitted (buffers not sharded). `no_sync()` → `set_requires_gradient_sync`.

## When to surface
Use when students ask how to *configure or migrate to FSDP2*, how `fully_shard` differs from FSDP1/DDP, how DTensor affects optimizers/checkpointing, or how to set prefetching/mixed precision correctly.