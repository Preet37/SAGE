# Card: PyTorch DistributedDataParallel (DDP) constructor semantics & key knobs
**Source:** https://docs.pytorch.org/docs/stable/generated/torch.nn.parallel.DistributedDataParallel.html  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** DDP defaults/semantics: bucket sizing, buffer/param sync, unused params, bucket views, static graph, mixed precision surface

## Key Content
- **What DDP does (core procedure):** Wraps a `torch.nn.Module` to do *data parallelism* by **all-reducing gradients** across replicas in a `process_group` (default: world). **Does not shard inputs**; user must shard (e.g., `DistributedSampler`). Requires `torch.distributed.init_process_group()` before construction.
- **Process/GPU setup (single-node N GPUs):** Spawn **N processes**, each bound to one GPU (`torch.cuda.set_device(i)` or `torch.accelerator.set_device_index(i)`), then `DDP(model, device_ids=[i], output_device=i)`. Alternative init: `torch.distributed.init_process_group(device_id=i)`.
- **Sync semantics & rationale:**
  - **Parameters are never broadcast each iteration**; DDP assumes optimizers update params identically on all ranks after gradient all-reduce.
  - **Buffers** (e.g., BatchNorm stats) are **broadcast from rank 0 each iteration** if `broadcast_buffers=True` (default).
  - `init_sync=True` (default) **verifies param shapes and broadcasts parameters and buffers at init**; if `False`, user must ensure identical weights across ranks.
- **Gradient bucketing (overlap comm/compute):** DDP buckets params so bucket all-reduce can overlap backward compute. `bucket_cap_mb` controls bucket size in **MiB**; default **25 MiB** when `None`.
- **Unused params handling:** `find_unused_parameters=False` (default). If `True`, DDP traverses autograd graph from `forward` outputs; params not receiving grads are pre-marked “ready” for reduction.
- **Memory/perf knobs:**
  - `gradient_as_bucket_view=False` (default). If `True`, `.grad` becomes a **view into all-reduce buckets**, saving peak memory ≈ **total gradient size** and avoiding copies; cannot call `detach_()` on grads.
  - `static_graph=False` (default). If `True`, graph/used-params set is constant; enables reentrant backwards, multiple checkpointing, unused params with checkpointing, params outside `forward`, and avoids per-iter unused-param search. Check via `ddp._get_ddp_logging_data()["can_set_static_graph"]`.
- **Uneven inputs workflow:** Use `with model.join(...):` to prevent hangs when ranks exhaust data at different times. `divide_by_initial_world_size=True` (default) vs divide by effective world size.
- **Gradient accumulation:** `with ddp.no_sync(): ...` disables sync inside context; sync occurs on first backward after exiting.
- **Mixed precision:** DDP supports mixed parameter dtypes (e.g., fp16/fp32); constructor includes `mixed_precision=` argument.

## When to surface
Use when students ask how to configure/optimize PyTorch DDP (bucket sizes, buffer/param sync, unused parameters, static graphs, gradient accumulation, uneven dataloaders, or mixed-precision behavior).