# Card: Scaled Dot-Product Attention (SDPA) in PyTorch: math, masks, and performance
**Source:** https://docs.pytorch.org/tutorials/intermediate/scaled_dot_product_attention_tutorial.html  
**Role:** code | **Need:** WORKING_EXAMPLE  
**Anchor:** End-to-end reference usage of `torch.nn.functional.scaled_dot_product_attention` plus multi-head causal self-attention module and backend benchmarking.

## Key Content
- **Eq. 1 (SDPA math, “Attention is All You Need”):**  
  Let \(Q,K,V\) be query/key/value. Attention weights:  
  \[
  \text{Attn}(Q,K,V)=\text{softmax}\left(\frac{QK^\top}{\sqrt{d_k}} + \text{attn\_mask}\right)V
  \]
  where \(d_k\) is per-head key dimension; `attn_mask` is additive bias/mask (e.g., causal/padding).
- **Tensor shapes used throughout (multi-head):** `query,key,value` shaped **(batch, heads, L, head_dim)**; output matches query length: **(batch, heads, L, head_dim)**. Example benchmark tensors: `(32, 32, 1024, 32)` with `dtype=torch.float16`.
- **Procedure (multi-head causal self-attention block):**
  1. Project input `x` with `Linear(embed_dim, 3*embed_dim)` to get concatenated QKV.
  2. `chunk(3, -1)` → `view(batch, seq, heads, head_dim).transpose(1,2)` to `(batch, heads, seq, head_dim)`.
  3. Call `F.scaled_dot_product_attention(query, key, value, attn_mask=None, dropout_p=dropout, is_causal=is_causal)`.
  4. Merge heads: `transpose(1,2).view(batch, seq, heads*head_dim)` then output projection + dropout.
  5. In eval: `dropout_p=0.0`, `is_causal=False` (per tutorial code).
- **Backend control workflow:** use `from torch.nn.attention import SDPBackend, sdpa_kernel` to force `MATH`, `FLASH_ATTENTION`, or `EFFICIENT_ATTENTION` for benchmarking.
- **Empirical timings (example run, microseconds):** default **2274.809**, math **87433.647**, flash **2277.896**, memory-efficient **4379.249** (batch=32, seq=1024, heads=32, head_dim=32, fp16, CUDA).
- **attn_bias utilities (PyTorch ≥2.3):** `torch.nn.attention.bias.causal_upper_left` equals `is_causal=True`; `causal_lower_right` differs when attention matrix is non-square (e.g., decoding with Lq≠Lk).

## When to surface
Use when students ask how to implement scaled dot-product attention with correct shapes/masking in PyTorch, or how SDPA backends (math/flash/mem-efficient) affect performance and how to force/benchmark them.