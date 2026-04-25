# Card: tf.keras.layers.MultiHeadAttention (Scaled Dot-Product Attention)
**Source:** https://www.tensorflow.org/api_docs/python/tf/keras/layers/MultiHeadAttention  
**Role:** API reference | **Need:** implementation details + shapes/defaults  
**Anchor:** Keras MultiHeadAttention computation steps (project → dot/scale → softmax → weighted sum → concat → output proj), masks, and call signatures.

## Key Content
- **Core procedure (multi-head attention pipeline):**  
  1) **Project inputs** with learned dense layers: `query_dense`, `key_dense`, `value_dense`.  
  2) Reshape into `num_heads` heads (effectively a list of tensors):  
     - Query head shape: **(B, <query dims>, key_dim)**  
     - Key head shape: **(B, <key/value dims>, key_dim)**  
     - Value head shape: **(B, <key/value dims>, value_dim)**  
  3) **Scaled dot-product attention (per head)**: compute dot-product of query and key, then **scale**, then **softmax** to get attention probabilities.  
     - (Eq. 1) Scores: `scores = (Q · K^T) * scale` where `Q` has last dim `key_dim`, `K` has last dim `key_dim`. (Scaling factor is applied after dot-product; exact constant not specified in this excerpt.)  
     - (Eq. 2) Probabilities: `P = softmax(scores)`  
     - (Eq. 3) Output per head: `head = P · V`
  4) **Concatenate heads** back to a single tensor; optionally apply final linear projection (`output_dense`).
- **Self-attention condition:** if `query`, `key`, `value` are the same (or `key` omitted so it defaults to `value`), the layer performs self-attention.
- **Call signature & shapes:**  
  - `query`: **(B, T, dim)** (target length `T`)  
  - `value`: **(B, S, dim)** (source length `S`)  
  - `key` (optional): **(B, S, dim)**; if not given, uses `value`  
  - `attention_mask`: boolean **(B, T, S)**; **1 = attend**, **0 = block**; can broadcast over missing batch dims and head dim  
  - `use_causal_mask`: prevents attending to future tokens (decoder-style)
- **Outputs:**  
  - `attention_output`: **(B, T, E)** where `E` = query last dim if `output_shape=None`, else projected to `output_shape`  
  - Optional `attention_scores` if `return_attention_scores=True`
- **Key parameters/defaults:** `dropout=0.0`, `use_bias=True`, `kernel_initializer='glorot_uniform'`, `bias_initializer='zeros'`, `attention_axes=None` (attend over all axes except batch/heads/features).

## When to surface
Use when students ask how scaled dot-product attention is implemented in Keras, what tensor shapes/masks mean (especially `(B,T,S)`), how self-attention is triggered, or what `num_heads`, `key_dim`, `value_dim`, `output_shape`, `dropout`, and causal masking do.