# Card: PyTorch SDPA (Scaled Dot-Product Attention) — usage, backends, causal masking
**Source:** https://docs.pytorch.org/tutorials/_sources/intermediate/scaled_dot_product_attention_tutorial.rst.txt  
**Role:** code | **Need:** WORKING_EXAMPLE  
**Anchor:** End-to-end SDPA call path + backend dispatch control + causal self-attention module example

## Key Content
- **Primitive:** `torch.nn.functional.scaled_dot_product_attention(query, key, value, attn_mask=None, dropout_p=..., is_causal=...)` (PyTorch ≥ 2.0). Incorporated into `nn.MultiheadAttention` and `nn.TransformerEncoderLayer`.
- **SDPA math (Eq. 1):**  
  \[
  \text{Attention}(Q,K,V)=\text{softmax}\left(\frac{QK^\top}{\sqrt{d_k}} + \text{mask}\right)V
  \]
  Variables: \(Q\)=query, \(K\)=key, \(V\)=value, \(d_k\)=key/query head dimension; mask implements causal or provided attention bias/mask.
- **Fused backend dispatch (CUDA):** chooses among **FlashAttention**, **Memory-Efficient Attention**, or **C++ math** implementation for performance vs naive PyTorch.
- **Explicit backend control (Procedure):**
  - Use `from torch.nn.attention import SDPBackend, sdpa_kernel`
  - Wrap calls: `with sdpa_kernel(SDPBackend.FLASH_ATTENTION): ...` (or `MATH`, `EFFICIENT_ATTENTION`) to force/disable implementations and benchmark.
- **Benchmark setup (Defaults used):** `batch_size=32`, `max_sequence_len=1024`, `num_heads=32`, `embed_dimension=32`, `dtype=torch.float16`; tensors shaped `[B, H, L, D]`.
- **Empirical timings (example output):**
  - Default: **2333.687 µs**
  - Math: **87407.322 µs**
  - FlashAttention: **2316.913 µs**
  - Memory-efficient: **4577.936 µs**
- **CausalSelfAttention module (Workflow):**
  - Linear projection `c_attn: embed_dim → 3*embed_dim`, chunk into Q/K/V, reshape to `[B, H, T, head_dim]`, call SDPA with `dropout_p=self.dropout` only in training; in eval set `dropout=0.0` and `is_causal=False`.
- **Attention bias subclasses (PyTorch 2.3):** `torch.nn.attention.bias.causal_upper_left` equals `is_causal=True`; `causal_lower_right` differs for non-square score matrices (decoding).

## When to surface
Use when students ask how to implement/benchmark scaled dot-product attention in PyTorch, how causal masking/bias works (upper-left vs lower-right), or how to force FlashAttention vs math/efficient backends for correctness/performance.