# Card: PyTorch `scaled_dot_product_attention` (SDPA) semantics
**Source:** https://docs.pytorch.org/docs/stable/generated/torch.nn.functional.scaled_dot_product_attention.html  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Authoritative parameter semantics/defaults, tensor shapes, mask behavior, kernel selection (Flash/MemEff/Math), GQA constraints.

## Key Content
- **API + defaults:** `scaled_dot_product_attention(query, key, value, attn_mask=None, dropout_p=0.0, is_causal=False, scale=None, enable_gqa=False) -> Tensor`. `scale` is **keyword-only**.
- **Eq. 1 (scores + scaling):**  
  Let `L = query.size(-2)`, `S = key.size(-2)`, `d = query.size(-1)`.  
  `scale_factor = 1/sqrt(d)` if `scale is None` else `scale`.  
  `attn_weight = (query @ key.transpose(-2, -1)) * scale_factor` with shape `(..., L, S)`.
- **Eq. 2 (mask/bias + softmax + dropout + output):**  
  `attn_bias` initialized zeros `(L,S)`.  
  If `is_causal=True`: requires `attn_mask is None`; apply lower-triangular allow-mask, fill others with `-inf`.  
  If `attn_mask` provided (broadcastable to `(..., L, S)`):  
  - **bool mask:** `True` = participates/allowed; `False` filled with `-inf`.  
  - **float mask (same dtype as q/k/v):** added to scores (`attn_bias = attn_mask + attn_bias`).  
  Then: `softmax(dim=-1)`, `dropout(attn_weight, dropout_p, train=True)`, output `attn_weight @ value` (shape like `query`).
- **Dropout behavior:** always applied per `dropout_p`; to disable in eval, pass `0.0` when `not self.training`.
- **Mask semantics note:** SDPA bool mask is inverse of `MultiheadAttention.key_padding_mask` (MHA: `True` = masked out). Invert when migrating (`~mask` / `logical_not()`).
- **Backends:** auto-select among FlashAttention-2, Memory-Efficient, and PyTorch C++ “math”; control via `torch.nn.attention.sdpa_kernel()` (preferred) or global CUDA toggles.
- **GQA (`enable_gqa=True`) constraints:** works only for Flash + math on CUDA; no NestedTensor. Requires `num_heads_q % num_heads_kv == 0` and `heads_key == heads_value`; implemented via repeating K/V along head dim.

## When to surface
Use when students ask about SDPA parameter defaults, causal vs explicit masks, boolean mask meaning, dropout in eval, backend/FlashAttention selection, or grouped-query attention (GQA) head-shape constraints.