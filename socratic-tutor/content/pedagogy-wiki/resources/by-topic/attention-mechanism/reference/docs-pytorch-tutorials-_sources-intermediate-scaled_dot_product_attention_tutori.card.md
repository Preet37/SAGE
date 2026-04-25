# Card: PyTorch Scaled Dot Product Attention (SDPA) usage + masking
**Source:** https://docs.pytorch.org/tutorials/_sources/intermediate/scaled_dot_product_attention_tutorial.rst.txt  
**Role:** explainer | **Need:** API_REFERENCE  
**Anchor:** Concrete invocation patterns for `F.scaled_dot_product_attention`, backend dispatch control, causal masking (`is_causal` vs bias tensors), and training vs inference knobs (`dropout_p`).

## Key Content
- **SDPA call signature (usage pattern):**  
  `torch.nn.functional.scaled_dot_product_attention(query, key, value, attn_mask=None, dropout_p=..., is_causal=...)`  
  Example (dense): `F.scaled_dot_product_attention(q, k, v)` where `q,k,v` shaped like `(B, ..., L, D)`; tutorial uses `(2,3,8)` and multihead `(B, H, L, D)`.
- **Backend dispatch (CUDA):** chooses among **FlashAttention**, **Memory-Efficient Attention**, or **C++ math** implementation.  
  Explicit control via context manager:  
  `from torch.nn.attention import SDPBackend, sdpa_kernel` then `with sdpa_kernel(SDPBackend.FLASH_ATTENTION): ...` (also `MATH`, `EFFICIENT_ATTENTION`).
- **Benchmark setup + empirical timings (example):**  
  `B=32, L=1024, H=32, D=32, dtype=float16`.  
  Reported: default **2333.687 µs**, math **87407.322 µs**, flash **2316.913 µs**, efficient **4577.936 µs**.
- **Causal self-attention module procedure:** project `x` with `Linear(embed_dim, 3*embed_dim)`, `chunk(3)` into `q,k,v`, reshape to `(B,H,L,head_dim)` via `.view(...).transpose(1,2)`, then SDPA.  
  **Training vs eval knobs:** if `self.training`: `dropout_p=self.dropout`, `is_causal=self.is_causal`; else `dropout_p=0.0`, `is_causal=False`.
- **Causal bias tensors (PyTorch ≥2.3):**  
  `from torch.nn.attention.bias import causal_upper_left, causal_lower_right`  
  `is_causal=True` is equivalent to `causal_upper_left(Lq, Lkv)`; differs from `causal_lower_right` when attention score matrix is non-square (common in decoding).
- **NestedTensor note:** SDPA supports NestedTensor + dense; fused implementations currently don’t support NestedTensor **for training**; example eval benchmark: Random NT **599.388 µs** vs Random Dense **964.192 µs** (flash backend).

## When to surface
Use when students ask how to *call SDPA in PyTorch*, how to *force/compare Flash vs efficient vs math backends*, or how to *implement causal masking correctly for training vs inference/decoding (including non-square Q/KV lengths).*