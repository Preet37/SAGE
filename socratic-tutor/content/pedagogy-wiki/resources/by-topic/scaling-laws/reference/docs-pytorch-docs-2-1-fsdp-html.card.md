# Card: PyTorch FSDP constructor + core knobs
**Source:** https://docs.pytorch.org/docs/2.1/fsdp.html  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Authoritative constructor signature, parameter semantics, and defaults (sharding_strategy, backward_prefetch, mixed_precision, cpu_offload, limit_all_gathers, use_orig_params)

## Key Content
- **Constructor signature (PyTorch 2.1):**  
  `torch.distributed.fsdp.FullyShardedDataParallel(module, process_group=None, sharding_strategy=None, cpu_offload=None, auto_wrap_policy=None, backward_prefetch=BackwardPrefetch.BACKWARD_PRE, mixed_precision=None, ignored_modules=None, param_init_fn=None, device_id=None, sync_module_states=False, forward_prefetch=False, limit_all_gathers=True, use_orig_params=False, ignored_states=None)`
- **Core procedure (minimal training loop):** wrap module → **init optimizer after wrapping** → forward → loss → backward → step. Optimizer must be created after wrapping to avoid stale param references.
- **Device placement rule:** compute device is destination CUDA device; ensure module already on that device, or call `torch.cuda.set_device(dev_id)`, or pass `device_id=...`. `sync_module_states=True` requires GPU comms (module on GPU or `device_id` set).
- **ShardingStrategy (behavioral definitions):**
  - `FULL_SHARD` (default): shard params+grads+optim state; all-gather before fwd, reshard after fwd; all-gather before bwd, reshard after bwd; grads reduce-scatter after bwd.
  - `SHARD_GRAD_OP`: params sharded outside compute; unshard before fwd, **do not reshard after fwd**, reshard after bwd; inside `no_sync()` params not resharded after bwd.
  - `NO_SHARD`: replicate like DDP; grads all-reduce after bwd.
  - `HYBRID_SHARD`: `FULL_SHARD` intra-node + inter-node replication. `_HYBRID_SHARD_ZERO2`: `SHARD_GRAD_OP` intra-node + inter-node replication.
- **BackwardPrefetch default:** `BACKWARD_PRE` (more overlap, more memory). `BACKWARD_POST` (less overlap, less memory). `None` disables overlap.
- **MixedPrecision fields:** `param_dtype`, `reduce_dtype` (defaults to `param_dtype` if unset), `buffer_dtype`, `keep_low_precision_grads=False`, `cast_forward_inputs=False`, `cast_root_forward_inputs=True`.
- **CPUOffload:** `CPUOffload(offload_params=False)`; if `True`, offloads params and grads; optimizer step runs on CPU. Gradient accumulation outside `no_sync()` unsupported with CPU offload.
- **Rate limiter:** `limit_all_gathers=True` (default) synchronizes CPU thread to cap GPU memory to ~two consecutive FSDP instances’ all-gathers; set `False` only for CPU-bound + low memory pressure.
- **`use_orig_params`:** default `False`; `True` exposes original parameters (enables per-parameter hyperparams) and is **required for `torch.compile()`**.

## When to surface
Use when students ask how to configure PyTorch FSDP (sharding modes, overlap/prefetch, mixed precision, CPU offload), what defaults mean, or why optimizer/device/state-sync ordering matters in distributed pretraining.