# Card: DeepSpeed CIFAR-10 training scaffold (MoE flags + ZeRO + dtype)
**Source:** https://github.com/deepspeedai/DeepSpeedExamples/blob/master/training/cifar/cifar10_deepspeed.py  
**Role:** code | **Need:** WORKING_EXAMPLE  
**Anchor:** End-to-end runnable DeepSpeed entrypoint showing how MoE is enabled/configured via CLI flags and how to initialize DeepSpeed (model/optimizer/dataloader) with ZeRO + fp16/bf16.

## Key Content
- **CLI switches (MoE + training):**
  - `--epochs` default **30**
  - `--dtype` ∈ {`bf16`,`fp16`,`fp32`} default **fp16**
  - `--stage` (ZeRO) ∈ {0,1,2,3} default **0**
  - `--moe` (bool) enable Mixture-of-Experts path
  - `--ep-world-size` default **1** (expert-parallel world size)
  - `--num-experts` list default **[1]**
  - `--mlp-type` default **"standard"** (when `num-experts > 1`, accepts `standard` or `residual`)
  - `--top-k` default **1** (top-1 or top-2 gating supported)
  - `--min-capacity` default **0** (minimum tokens per expert regardless of capacity factor)
  - `--noisy-gate-policy` default **None** (top-1 only; valid: `RSample`, `Jitter`)
  - `--moe-param-group` (bool) create separate MoE param groups (required when using ZeRO with MoE)
- **MoE optimizer param grouping procedure:**
  - Build a single param dict: `{"params": [p for p in model.parameters()], "name": "parameters"}`
  - Call `split_params_into_different_moe_groups_for_optimizer(parameters)` to separate expert params for optimizer/ZeRO.
- **DeepSpeed config defaults (numbers):**
  - `train_batch_size: 16`, `steps_per_print: 2000`
  - Optimizer Adam: `lr=0.001`, `betas=[0.8,0.999]`, `eps=1e-8`, `weight_decay=3e-7`
  - WarmupLR: `warmup_min_lr=0`, `warmup_max_lr=0.001`, `warmup_num_steps=1000`
  - `gradient_clipping: 1.0`, `prescale_gradients: False`
  - ZeRO: `stage=args.stage`, `allgather_bucket_size=5e7`, `reduce_bucket_size=5e7`, `overlap_comm=True`, `contiguous_gradients=True`, `cpu_offload=False`
- **Training loop workflow:**
  1. `deepspeed.initialize(args, model, model_parameters, training_data, config)`
  2. Determine device via `get_accelerator().device_name(local_rank)`; set `target_dtype` to bf16/fp16 if enabled.
  3. Forward: `outputs = model_engine(inputs)`; loss: `CrossEntropyLoss`.
  4. Backprop/step: `model_engine.backward(loss)` then `model_engine.step()`.
  5. Log every `--log-interval` (default **2000**) minibatches on rank 0.

## When to surface
Use when students ask how to *wire up DeepSpeed training end-to-end* (initialize, dtype, ZeRO) and how MoE-related knobs (top-k, ep-world-size, num-experts, min-capacity, noisy gating, MoE param groups) are exposed and used in a runnable script.