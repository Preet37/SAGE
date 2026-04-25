# Card: `torch.nn.Transformer` API essentials (shapes, masks, defaults)
**Source:** https://docs.pytorch.org/docs/stable/generated/torch.nn.Transformer.html  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Parameter defaults + `forward()` signature, tensor shapes, mask semantics

## Key Content
- **Constructor (defaults):**  
  `torch.nn.Transformer(d_model=512, nhead=8, num_encoder_layers=6, num_decoder_layers=6, dim_feedforward=2048, dropout=0.1, activation="relu", layer_norm_eps=1e-5, batch_first=False, norm_first=False, bias=True, custom_encoder=None, custom_decoder=None, device=None, dtype=None)`  
  - `d_model`: feature size **E** expected for encoder/decoder inputs.  
  - `batch_first=False`: tensors are `(S, N, E)` / `(T, N, E)`; if `True`: `(N, S, E)` / `(N, T, E)`.  
  - `norm_first=False`: LayerNorm **after** attention/FFN; if `True`, **before**.
- **Forward signature:**  
  `forward(src, tgt, src_mask=None, tgt_mask=None, memory_mask=None, src_key_padding_mask=None, tgt_key_padding_mask=None, memory_key_padding_mask=None, src_is_causal=None, tgt_is_causal=None, memory_is_causal=False)`
- **Shape formulas (Eq. 1):**  
  Let **S**=source length, **T**=target length, **N**=batch size, **E**=`d_model`.  
  - `src`: unbatched `(S, E)`; batched `(S, N, E)` if `batch_first=False`, else `(N, S, E)`  
  - `tgt`: unbatched `(T, E)`; batched `(T, N, E)` if `batch_first=False`, else `(N, T, E)`  
  - **Output**: same length as decoder input: `(T, N, E)` or `(N, T, E)` (Eq. 2).
- **Mask semantics (critical):**
  - For `[src/tgt/memory]_mask`: if **BoolTensor**, `True` = **not allowed to attend**; `False` = unchanged. If **FloatTensor**, values are **added** to attention weights.
  - For `[src/tgt/memory]_key_padding_mask`: if **BoolTensor**, `True` positions in keys are **ignored**.
  - `src_is_causal` / `tgt_is_causal` / `memory_is_causal`: hints to treat corresponding mask as **causal**; incorrect hints can cause incorrect execution.
- **Example shapes:** `src = (10, 32, 512)`, `tgt = (20, 32, 512)` → `out = transformer_model(src, tgt)`.

## When to surface
Use when students ask how to wire an encoder–decoder Transformer in PyTorch: required `src/tgt` shapes, what `batch_first` changes, why output length matches target length, and how boolean vs float masks/key-padding masks behave.