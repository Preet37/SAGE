# Card: PyTorch AMP (autocast + GradScaler) essentials
**Source:** https://docs.pytorch.org/docs/stable/amp.html  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Exact semantics/defaults for `torch.amp.autocast` + gradient scaling; fp16 vs bf16 behavior and device defaults

## Key Content
- **Mixed precision goal/rationale:** Run some ops in `float32` (range/stability, e.g., reductions) and others in lower precision (`lower_precision_fp`: `float16` or `bfloat16`) for speed (e.g., linear/conv).
- **Autocast API:** `torch.autocast(device_type, dtype=None, enabled=True, cache_enabled=None)`
  - **Defaults:** `enabled=True`, `cache_enabled=True`.
  - **dtype default if `None`:** from `get_autocast_dtype()` → **CUDA:** `torch.float16`; **CPU:** `torch.bfloat16`.
  - **Procedure:** Wrap **only forward + loss** in autocast; **do not** run backward under autocast (“Backward passes under autocast are not recommended”; backward runs in same dtype used by corresponding forward ops).
  - **Do not manually call** `.half()` / `.bfloat16()` on model/inputs when using autocast.
  - **Nesting:** `autocast(enabled=False)` subregions allowed; cast incoming tensors (e.g., `e_float16.float()`) to force `float32` execution.
  - **Thread-local state:** must enable autocast per thread; impacts multi-GPU per process (e.g., `DataParallel`, `DistributedDataParallel`).
- **Gradient scaling rationale:** fp16 backward can underflow (small grads flush to 0). Scale loss to amplify grads, then **unscale before optimizer step**.
  - **Equation (Eq. 1):** `L_scaled = s * L`; backprop on `L_scaled`; before update use `g = (∂L_scaled/∂w) / s`.
  - **Important note:** AMP/fp16 may fail for bf16-pretrained models due to fp16 max **65504** → overflow/NaNs; `GradScaler` scale may decrease **below 1** (not guaranteed >1).
- **Deprecations:** `torch.cuda.amp.autocast` / `torch.cpu.amp.autocast` and corresponding `GradScaler` are deprecated → use `torch.amp.autocast("cuda"/"cpu", ...)`, `torch.amp.GradScaler("cuda"/"cpu", ...)`.
- **Loss function pitfall:** `binary_cross_entropy` / `BCELoss` error under autocast; prefer `binary_cross_entropy_with_logits` / `BCEWithLogitsLoss` (safe).

## When to surface
Use when students ask how to correctly implement AMP training/inference in PyTorch, what autocast/GradScaler do (and their defaults), or why fp16 can underflow/overflow (esp. bf16-pretrained models, BCE vs BCEWithLogits).