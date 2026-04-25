# Card: PyTorch `nn.MultiheadAttention` (API shapes + masks)
**Source:** https://docs.pytorch.org/docs/stable/generated/torch.nn.MultiheadAttention.html  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Exact `forward()` tensor shapes, `attn_mask` vs `key_padding_mask`, constructor defaults

## Key Content
- **Module purpose (Eq. 1: Multi-Head Attention):** Implements “Attention Is All You Need” multi-head attention; conceptually  
  **MultiHead(Q,K,V) = Concat(head₁,…,head_h) Wᴼ**, where each head attends in a subspace; **embed_dim** is split across **num_heads** (per-head dim = `embed_dim // num_heads`).
- **Constructor signature + defaults:**  
  `MultiheadAttention(embed_dim, num_heads, dropout=0.0, bias=True, add_bias_kv=False, add_zero_attn=False, kdim=None, vdim=None, batch_first=False, ...)`  
  - `kdim=None` ⇒ `kdim=embed_dim`; `vdim=None` ⇒ `vdim=embed_dim`  
  - `dropout` applies to `attn_output_weights` (default **0.0**).
- **Forward signature:**  
  `forward(query, key, value, key_padding_mask=None, need_weights=True, attn_mask=None, average_attn_weights=True, is_causal=False)`
- **Input shapes (batched):**
  - If `batch_first=False` (default): `query (L,N,E)`, `key/value (S,N,Ek/Ev)`
  - If `batch_first=True`: `query (N,L,E)`, `key/value (N,S,Ek/Ev)`
  - Unbatched: `query (L,E)`, `key/value (S,Ek/Ev)`; `batch_first` ignored.
- **Masks:**
  - `key_padding_mask`: shape `(N,S)` (or `(S)` unbatched). **True** (binary) ⇒ ignore that key position; float mask is **added** to corresponding key scores.
  - `attn_mask`: 2D `(L,S)` broadcast across batch, or 3D `(N,L,S)` per batch entry. **True** (binary) ⇒ disallow attending; float mask is **added** to attention weights. If both masks given, their **types must match**.
  - `is_causal=True` applies a causal mask (hint that `attn_mask` is causal).
- **Outputs:**
  - `attn_output`: `(L,N,E)` or `(N,L,E)` (or `(L,E)` unbatched).
  - `attn_output_weights` (if `need_weights=True`):  
    - averaged heads (`average_attn_weights=True`): `(N,L,S)` (or `(L,S)` unbatched)  
    - per-head (`average_attn_weights=False`): `(N,num_heads,L,S)` (or `(num_heads,L,S)` unbatched).
- **Performance note:** Set `need_weights=False` to use optimized `scaled_dot_product_attention()` for best performance.

## When to surface
Use when students ask about PyTorch MHA tensor dimensions, how to build/shape `attn_mask` vs `key_padding_mask`, default parameter values, or why `need_weights=False` can be faster.