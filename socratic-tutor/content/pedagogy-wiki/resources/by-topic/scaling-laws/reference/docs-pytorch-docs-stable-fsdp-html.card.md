# Card: PyTorch FSDP constructor + core knobs (2.11)
**Source:** https://docs.pytorch.org/docs/stable/fsdp.html  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** `torch.distributed.fsdp.FullyShardedDataParallel` constructor signature, defaults, and parameter semantics (sharding, mixed precision, CPU offload, auto-wrapping, prefetch/rate limiting, orig params)

## Key Content
- **Constructor (signature + key defaults):**  
  `FullyShardedDataParallel(module, process_group=None, sharding_strategy=None, cpu_offload=None, auto_wrap_policy=None, backward_prefetch=BackwardPrefetch.BACKWARD_PRE, mixed_precision=None, ignored_modules=None, param_init_fn=None, device_id=None, sync_module_states=False, forward_prefetch=False, limit_all_gathers=True, use_orig_params=False, ignored_states=None, device_mesh=None)`
- **What FSDP does:** shards **module parameters across data-parallel workers** (inspired by ZeRO-3 / Xu et al.).
- **Device placement procedure:** ensure compute device is the destination CUDA device via (1) move module to device, (2) `torch.cuda.set_device(dev_id)`, or (3) pass `device_id=dev_id`. If `sync_module_states=True`, module must be on GPU or specify `device_id` (GPU comm required). Inputs are moved to compute device automatically.
- **ShardingStrategy semantics:**
  - `FULL_SHARD`: shard params+grads+optim state; all-gather before fwd, reshard after fwd; all-gather before bwd; reduce-scatter grads after bwd.
  - `SHARD_GRAD_OP`: keep params unsharded after fwd; reshard after bwd; inside `no_sync()` params not resharded after bwd.
  - `NO_SHARD`: replicate like DDP; all-reduce grads.
  - `HYBRID_SHARD`: `FULL_SHARD` intra-node + inter-node replication.
  - `_HYBRID_SHARD_ZERO2`: `SHARD_GRAD_OP` intra-node + inter-node replication.
- **Backward prefetch default:** `BackwardPrefetch.BACKWARD_PRE` (max overlap, higher peak memory); `BACKWARD_POST` less memory; `None` disables overlap (not recommended).
- **Rate limiter default:** `limit_all_gathers=True` synchronizes CPU thread to cap memory to ~two consecutive instances’ all-gathers; set `False` only for CPU-bound + low memory pressure.
- **MixedPrecision (FSDP-native):** `MixedPrecision(param_dtype=None, reduce_dtype=None, buffer_dtype=None, keep_low_precision_grads=False, cast_forward_inputs=False, cast_root_forward_inputs=True, _module_classes_to_ignore=(_BatchNorm,))`. If `reduce_dtype is None` and `param_dtype` set, reduction uses `param_dtype`.
- **CPU offload:** `CPUOffload(offload_params=False)`; if `True`, gradients offloaded too and optimizer step runs on CPU.
- **`use_orig_params` default `False`:** `True` exposes original params to optimizer (per-parameter hparams) and is **required for `torch.compile()`**; sharded form may be size-0 on ranks with no local data.

## When to surface
Use when students ask how to configure PyTorch FSDP for large-model pretraining (memory vs throughput tradeoffs), especially defaults/meaning of `sharding_strategy`, `mixed_precision`, `cpu_offload`, `auto_wrap_policy`, `backward_prefetch`, `limit_all_gathers`, and `use_orig_params`.