# Card: PyTorch `scaled_dot_product_attention` (SDPA) API + semantics
**Source:** https://docs.pytorch.org/docs/stable/generated/torch.nn.functional.scaled_dot_product_attention.html  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Exact API signature and semantics: `attn_mask` vs `is_causal`, `dropout_p` behavior, optional `scale` override (default \(1/\sqrt{d_k}\)), and `enable_gqa`.

## Key Content
- **Signature:** `scaled_dot_product_attention(query, key, value, attn_mask=None, dropout_p=0.0, is_causal=False, scale=None, enable_gqa=False) -> Tensor`  
  `scale` is **keyword-only**.
- **Eq. 1 (core computation):**  
  Let \(L=\text{query.size}(-2)\), \(S=\text{key.size}(-2)\), \(d_k=\text{query.size}(-1)\).  
  Scale factor \( \alpha = 1/\sqrt{d_k} \) if `scale is None`, else \( \alpha=\text{scale} \).  
  Scores: \(A = (QK^\top)\alpha + B\) where \(B\) is attention bias from masks.  
  Weights: \(W=\text{softmax}(A,\ \text{dim}=-1)\).  
  Dropout: \(W=\text{dropout}(W,\ p=\text{dropout_p},\ \text{train=True})\).  
  Output: \(O = WV\).
- **Mask semantics (critical):**
  - `is_causal=True` creates a **lower-triangular** causal mask (upper-left causal bias for non-square). **Error/assert** if both `attn_mask` and `is_causal` are set.
  - `attn_mask` must broadcast to attention weights shape \((..., L, S)\).
  - Boolean `attn_mask`: **True = participates in attention** (inverse of `MultiheadAttention.key_padding_mask`, where True = masked out).
  - Float `attn_mask` (same dtype as Q/K/V): **added** to attention scores.
- **Dropout behavior:** SDPA **always applies dropout** according to `dropout_p` (no automatic eval-mode disable). Use `dropout_p=(p if self.training else 0.0)`.
- **GQA (`enable_gqa=True`):** repeats K/V heads via `repeat_interleave` so that `num_heads_q % num_heads_kv == 0` and `num_heads_k == num_heads_v`. Experimental; works only for FlashAttention and math kernel on CUDA; no NestedTensor support.
- **Backends:** may select FlashAttention-2, memory-efficient, or PyTorch C++/math; controllable via `torch.nn.attention.sdpa_kernel()` / CUDA backend toggles. Outputs may differ by backend; C++ supports `float64`. CuDNN may choose nondeterministic algorithms unless `torch.backends.cudnn.deterministic=True`.

## When to surface
Use when students ask how PyTorch SDPA handles masking (`attn_mask` vs `is_causal`), scaling, dropout in eval vs train, GQA head constraints, or why outputs/perf differ across SDPA backends.