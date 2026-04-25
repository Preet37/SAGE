# Card: Accelerate essentials for distributed training knobs
**Source:** https://huggingface.co/docs/accelerate/index  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Distributed training configuration knobs (mixed precision, gradient accumulation, FSDP/DeepSpeed integration points)

## Key Content
- **Minimal integration pattern (core workflow)**
  1) `from accelerate import Accelerator`  
  2) `accelerator = Accelerator(...)` (auto-detects hardware/distributed setup)  
  3) Wrap objects: `model, optimizer, train_dl, eval_dl = accelerator.prepare(model, optimizer, train_dl, eval_dl)`  
  4) Replace backprop: `accelerator.backward(loss)` (instead of `loss.backward()`)  
  5) Launch: `accelerate launch script.py`
- **Key configuration knobs (constructor / config file)**
  - `mixed_precision`: supports `fp16`, `bf16`, `fp8` (hardware-dependent; fp8 noted for Hopper/H100-class GPUs).
  - `gradient_accumulation_steps`: increases effective batch size without increasing per-device batch.
  - Distributed strategy selectable via config: DDP / DP, **FSDP** (parameter/grad/optimizer-state sharding), **DeepSpeed** (ZeRO stages, accumulation, mixed precision).
- **Design rationale**
  - Reduces PyTorch DDP boilerplate (process group init, device placement, distributed samplers, DDP wrapping) while keeping the *same* user-defined training loop structure.
  - `prepare()` centralizes: device placement, wrapping model with backend (e.g., DDP/FSDP), enabling mixed precision, and sharding dataloaders per process.
- **Distributed data sharding rule (BatchSamplerShard)**
  - Each process yields batches where: **(Eq. 1)** `idx % num_processes == process_index`  
    - `idx`: batch index from original sampler; `num_processes`: world size; `process_index`: rank.
  - `split_batches` (bool) controls whether batches are split across processes vs. each process taking whole batches.

## When to surface
Use when students ask how to configure/implement multi-GPU training for RLHF/SFT (DDP/FSDP/DeepSpeed), how mixed precision or gradient accumulation is wired in Accelerate, or why dataloaders/models behave differently under distributed launch.