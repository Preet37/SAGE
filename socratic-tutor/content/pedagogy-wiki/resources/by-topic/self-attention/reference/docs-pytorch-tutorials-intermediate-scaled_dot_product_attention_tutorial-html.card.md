# Card: PyTorch SDPA (Scaled Dot-Product Attention) — usage + performance controls
**Source:** https://docs.pytorch.org/tutorials/intermediate/scaled_dot_product_attention_tutorial.html  
**Role:** Implementation guide | **Need:** math+implementation+performance reference  
**Anchor:** How to use `torch.nn.functional.scaled_dot_product_attention` (SDPA), select backends, causal masking, NestedTensor, and profiling/compile behavior.

## Key Content
- **SDPA definition (paper reference):** computes scaled dot-product attention between **query (Q)**, **key (K)**, **value (V)** per *Attention Is All You Need*:  
  **Eq. 1:** `Attention(Q,K,V) = softmax((Q K^T) / sqrt(d_k)) V`  
  where `d_k` is key/query head dimension (scaling improves stability vs large dot products before softmax).
- **PyTorch API:** `torch.nn.functional.scaled_dot_product_attention(query, key, value, attn_mask=None, dropout_p=..., is_causal=...)`. Incorporated into `nn.MultiheadAttention` and `nn.TransformerEncoderLayer`. Requires **PyTorch ≥ 2.0**.
- **Fused CUDA backends + explicit control:** on CUDA inputs, SDPA dispatches among implementations (math / FlashAttention / memory-efficient). Force backend via:  
  `from torch.nn.attention import SDPBackend, sdpa_kernel` and `with sdpa_kernel(SDPBackend.FLASH_ATTENTION): ...`
- **Benchmark setup (defaults used in tutorial):** `batch_size=32`, `max_sequence_len=1024`, `num_heads=32`, `embed_dimension=32`, `dtype=float16`, tensors shaped `(B, H, S, D)`.
- **Empirical timings (example run):**
  - Default: **2274.809 µs**
  - Math: **87433.647 µs**
  - FlashAttention: **2277.896 µs**
  - Memory-efficient: **4379.249 µs**
- **Causal self-attention module procedure:** project `x` with `Linear(embed_dim, 3*embed_dim)` → `chunk` into Q,K,V → reshape to `(B, heads, S, head_dim)` → call SDPA with `dropout_p` only during training; `is_causal` disabled in eval.
- **Causal bias subclasses (PyTorch ≥ 2.3):** `torch.nn.attention.bias.causal_upper_left` equals `is_causal=True`; `causal_lower_right` differs for non-square score matrices (decoding).
- **NestedTensor note:** SDPA supports NestedTensor + dense; fused implementations **don’t support NestedTensor for training** (example eval benchmark: Random NT **639.435 µs** vs Random Dense **954.428 µs** under FlashAttention).
- **torch.compile behavior:** SDPA is composable with `torch.compile`; profiling showed GPU time dominated by same kernels; example report includes `aten::_scaled_dot_product_flash_attention` ~**2.821–2.825 ms** over 25 calls.

## When to surface
Use when students ask how to implement/optimize scaled dot-product attention in PyTorch, how to force FlashAttention vs math kernels, how causal masking/bias works (upper-left vs lower-right), or why `torch.compile` may not speed up already-fused attention kernels.