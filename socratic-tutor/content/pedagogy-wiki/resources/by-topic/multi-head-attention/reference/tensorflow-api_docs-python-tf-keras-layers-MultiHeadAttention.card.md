# Card: tf.keras.layers.MultiHeadAttention — constructor, call semantics, masks
**Source:** https://www.tensorflow.org/api_docs/python/tf/keras/layers/MultiHeadAttention  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Constructor/forward argument semantics and defaults (num_heads, key_dim/value_dim, attention_axes, dropout, use_bias) plus mask handling and returned attention scores

## Key Content
- **Purpose/definition:** Implements multi-head attention (Vaswani et al., 2017). If `query`, `key`, `value` are the same tensor ⇒ **self-attention**; otherwise can be used for **cross-attention**.
- **Core computation (Eq. 1: scaled dot-product attention per head):**  
  - Project inputs into heads:  
    - `Q`: shape `(B, <query dims>, key_dim)`  
    - `K`: shape `(B, <key/value dims>, key_dim)`  
    - `V`: shape `(B, <key/value dims>, value_dim)`  
    (effectively a list of `num_heads` tensors)  
  - Scores: `scores = (Q · K^T) / sqrt(key_dim)`  
  - Probabilities: `P = softmax(scores)`  
  - Head output: `O_head = P · V`  
  - Concatenate heads, then optional final linear projection.
- **Constructor args + defaults:**  
  - `num_heads` (required): number of attention heads  
  - `key_dim` (required): size per head for query/key  
  - `value_dim=None`: size per head for value  
  - `dropout=0.0`: dropout probability (applied in training)  
  - `use_bias=True`: whether dense projections use bias  
  - `output_shape=None`: if `None`, output projects back to **query last-dim**; else projects to `output_shape`  
  - `attention_axes=None`: axes to apply attention over; `None` ⇒ all axes except batch, heads, features
- **Call signature + shapes:**  
  - `query`: `(B, T, dim)`; `value`: `(B, S, dim)`; `key` optional `(B, S, dim)`; if `key` omitted ⇒ `key=value`  
  - `attention_mask`: boolean `(B, T, S)`; `1` allow attention, `0` block; broadcasting allowed over missing batch dims and head dim  
  - `use_causal_mask`: boolean to prevent attending to future tokens  
  - `return_attention_scores=False`: if `True` returns `(attention_output, attention_scores)`
- **Returns:**  
  - `attention_output`: `(B, T, E)` where `E` is query last-dim if `output_shape=None`, else `output_shape`  
  - `attention_scores` (optional): multi-head attention coefficients over attention axes

## When to surface
Use when students ask how to configure `MultiHeadAttention` (dims, heads, dropout, output shape), how masks/causal masking work, or what shapes/outputs (including attention scores) to expect.