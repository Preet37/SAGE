# Card: PyTorch `F.scaled_dot_product_attention` API contract
**Source:** https://docs.pytorch.org/docs/stable/generated/torch.nn.functional.scaled_dot_product_attention.html  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Mask (`attn_mask`) + `is_causal` semantics/shapes, default scaling, kernel selection + numerical/determinism notes.

## Key Content
- **Signature:** `scaled_dot_product_attention(query, key, value, attn_mask=None, dropout_p=0.0, is_causal=False, scale=None, enable_gqa=False) -> Tensor` (beta).
- **Eq. 1 (core computation):**  
  Let `L = query.size(-2)`, `S = key.size(-2)`, `d_k = query.size(-1)`.  
  `scale_factor = 1/sqrt(d_k)` if `scale is None`, else `scale`.  
  `attn_weight = softmax((query @ key.transpose(-2,-1)) * scale_factor + attn_bias, dim=-1)`  
  `attn_weight = dropout(attn_weight, dropout_p, train=True)` (always uses `dropout_p`)  
  `output = attn_weight @ value`
- **Masking / bias (`attn_bias`) construction (Eq. 2):**
  - If `is_causal=True`: `attn_mask` must be `None`; uses lower-triangular causal mask; for non-square masks uses “upper-left causal bias” alignment.
  - If `attn_mask` provided: must be **broadcastable** to attention weights shape `(..., L, S)`.
    - **Bool mask:** `True` = participates in attention; `False` masked to `-inf` (note: inverse of `MultiheadAttention.key_padding_mask` semantics).
    - **Float mask:** same dtype as `query/key/value`; **added** to attention scores.
- **Kernel/backends:** auto-select among FlashAttention-2, memory-efficient, and PyTorch C++ “math” implementation; control via `torch.nn.attention.sdpa_kernel()` / `torch.backends.cuda.enable_*_sdp()`. Outputs may differ across kernels due to fused ops; C++ supports `float64`. For math backend, intermediates are `float` when inputs are `half`/`bfloat16`.
- **Determinism:** on CUDA+cuDNN may choose nondeterministic algorithm; set `torch.backends.cudnn.deterministic=True` to prefer determinism.
- **GQA (`enable_gqa=True`):** repeats `key/value` heads via `repeat_interleave`; constraints: `heads_q % heads_kv == 0` and `heads_key == heads_value`; works only for FlashAttention and math kernel on CUDA; no NestedTensor.

## When to surface
Use when students ask how PyTorch SDPA handles `attn_mask` vs `is_causal`, mask truth semantics/broadcasting, default scaling (`1/sqrt(d_k)`), dropout behavior, or why outputs/determinism differ across fused attention kernels and dtypes.