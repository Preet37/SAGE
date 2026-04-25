# Card: DeepSpeed MoE API + Inference/Training Defaults
**Source:** https://deepspeed.readthedocs.io/en/latest/moe.html  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Authoritative DeepSpeed MoE API surface and defaults (k, capacity_factor/eval_capacity_factor, min_capacity, noisy_gate_policy, drop_tokens, ep_size, use_rts, top2_2nd_expert_sampling)

## Key Content
- **Core layer API:** `deepspeed.moe.layer.MoE(hidden_size, expert, num_experts=1, ep_size=1, k=1, capacity_factor=1.0, eval_capacity_factor=1.0, min_capacity=4, use_residual=False, noisy_gate_policy=None, drop_tokens=True, use_rts=True, use_tutel=False, enable_expert_tensor_parallelism=False, top2_2nd_expert_sampling=True)`
  - `k` = top-k routing; **only supports k=1 or k=2**.
  - `noisy_gate_policy` valid: **'Jitter', 'RSample', 'None'**.
  - `drop_tokens=False` is **equivalent to infinite capacity**.
  - `use_rts=True` enables **Random Token Selection** (RTS) by default (convergence improvement).
- **Forward signature/returns:** `forward(hidden_states, used_token=None) -> (output, l_aux, exp_counts)`
  - `used_token`: mask for only used tokens.
  - Returns: model output tensor, **gate loss** `l_aux`, and **expert counts** `exp_counts`.
- **Capacity sizing knobs (training vs eval):** `capacity_factor` (train), `eval_capacity_factor` (eval), with floor `min_capacity` per expert.
- **Expert parallelism:** `ep_size` = number of ranks in expert-parallel group; layer accepts `ep_size` directly (older `groups.initialize(ep_size=...)` is deprecated).
- **PR-MoE (Pyramid-Residual MoE):** pass `num_experts` as a **list** (e.g., `[4, 8]`) and set `use_residual=True`.
- **Inference workflow:** use `deepspeed.init_inference(model, mp_size=..., dtype=torch.half, moe_experts=..., checkpoint=..., replace_with_kernel_inject=True)`.
- **Empirical scaling/results:** DS-MoE inference reports **24%–60%** speedup vs PyTorch (generic) and **2x–3.2x** (specialized) on 8/16/32 GPUs; up to **7.3x** latency reduction; trillion-parameter MoE inference **<25 ms**; up to **4.5x faster** and **9x cheaper** vs quality-equivalent dense.
- **Example model fact:** Switch Transformer **1.6T params** with compute ~ **10B dense**.

## When to surface
Use for questions about **DeepSpeed MoE layer parameters/defaults**, **top-k routing/capacity/drop-token behavior**, **what MoE forward returns (aux loss, expert counts)**, and **how to initialize/run MoE inference with DeepSpeed**.