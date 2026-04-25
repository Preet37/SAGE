# Card: DeepSpeed MoE API + key defaults
**Source:** https://docs.deepspeed.org.cn/en/latest/moe.html  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** DeepSpeed `deepspeed.moe.layer.MoE` parameter names + defaults; MoE parallelism + inference init knobs

## Key Content
- **MoE layer signature (API + defaults):**  
  `deepspeed.moe.layer.MoE(hidden_size:int, expert:Module, num_experts:int=1, ep_size:int=1, k:int=1, capacity_factor:float=1.0, eval_capacity_factor:float=1.0, min_capacity:int=4, use_residual:bool=False, noisy_gate_policy:Optional[str]=None, drop_tokens:bool=True, use_rts:bool=True, use_tutel:bool=False, enable_expert_tensor_parallelism:bool=False, top2_2nd_expert_sampling:bool=True)`  
  - `k` supports **only 1 or 2** (top-k routing).  
  - `noisy_gate_policy` valid: **'Jitter'**, **'RSample'**, **'None'** (default `None`).  
  - `drop_tokens=False` ⇒ “equivalent to **infinite capacity**”.
- **Forward outputs:** `forward(hidden_states, used_token=None) -> (output, l_aux, exp_counts)`  
  - `l_aux`: gate loss (load-balancing auxiliary loss); `exp_counts`: per-expert token counts.
- **Capacity concept (operational):** expert capacity controlled by `capacity_factor` (train) / `eval_capacity_factor` (eval) with floor `min_capacity=4`.
- **Parallelism knobs:** `ep_size` passed per-layer (old `deepspeed.utils.groups.initialize(ep_size=...)` is **deprecated**). Ranks in an expert-parallel group of size `ep_size` **distribute** the layer’s `num_experts`.
- **Training procedure (optimizer param groups):**  
  Use `split_params_into_different_moe_groups_for_optimizer` to create MoE/non-MoE param groups before `deepspeed.initialize(...)`.
- **Inference init (key args):** `deepspeed.init_inference(moe_model, mp_size=..., dtype=torch.half, moe_experts=..., checkpoint=..., replace_with_kernel_inject=True)`
- **Empirical scaling claims:** Switch Transformer **1.6T params** at ~**10B dense compute**; DS-MoE inference reports up to **7.3×** latency/cost reduction vs baseline MoE systems and up to **4.5× faster / 9× cheaper** vs quality-equivalent dense.

## When to surface
Use when students ask how to configure DeepSpeed MoE layers (routing `k`, capacity, token dropping, RTS/noisy gating), interpret MoE forward outputs (`l_aux`, `exp_counts`), or set `ep_size/mp_size/moe_experts` for training/inference.