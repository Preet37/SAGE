# Card: PyTorch AMP canonical training-loop order (GradScaler/autocast)
**Source:** https://docs.pytorch.org/docs/stable/notes/amp_examples.html  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Correct AMP training recipes incl. gradient accumulation/clipping + multi-optimizer ordering

## Key Content
- **Core AMP components**
  - Use `torch.autocast(device_type='cuda', dtype=torch.float16)` for forward/loss regions.
  - Use `torch.amp.GradScaler()` once at start to scale losses and manage inf/NaN checks + dynamic scale updates.
  - Rationale: scaling mitigates **float16 gradient underflow**; autocast chooses op precision for speed while maintaining accuracy.

- **Canonical step ordering (Typical Mixed Precision Training)**
  1. `optimizer.zero_grad()`
  2. `with autocast(...): output = model(input); loss = loss_fn(output, target)`
  3. `scaler.scale(loss).backward()`  
     - Note: **Backward under autocast not recommended**; backward ops run in dtype chosen for corresponding forward ops.
  4. `scaler.step(optimizer)`  
     - Internally **unscales** grads for optimizer params; if grads contain **inf/NaN**, `optimizer.step()` is **skipped**.
  5. `scaler.update()` (updates scale for next iteration)

- **Unscaled-gradient operations (e.g., clipping)**
  - Must unscale before inspecting/modifying `.grad` (else thresholds are effectively scaled).
  - Procedure: after backward → `scaler.unscale_(optimizer)` → `torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm)` → `scaler.step(optimizer)` → `scaler.update()`.
  - Constraint: `unscale_` **only once per optimizer per step**, and **only after all grads are accumulated**; calling twice triggers `RuntimeError`.

- **Gradient accumulation (effective batch)**
  - Effective batch size: **Eq. 1** `B_eff = batch_per_iter * iters_to_accumulate * num_procs` (if distributed).
  - Loss scaling for accumulation: **Eq. 2** `loss = loss / iters_to_accumulate`.
  - Keep grads **scaled** and scale factor **constant** across accumulation; call `step/update/zero_grad` only when `(i+1) % iters_to_accumulate == 0`. Unscale (for clipping) **just before** `step`.

- **Multiple losses/optimizers**
  - Call `scaler.scale(loss_k)` **for each loss**.
  - Call `scaler.step(optimizer_j)` **for each optimizer**; call `scaler.update()` **once after all steps**.
  - Each optimizer independently skips step on inf/NaN.

## When to surface
Use when students ask “What’s the correct AMP training loop order?” or how to combine AMP with **gradient clipping**, **gradient accumulation**, or **multiple optimizers/losses** without breaking scaling.