# Card: TF `MultiHeadAttention` (v2.13.1) — signatures + mask/dropout semantics
**Source:** https://www.tensorflow.org/versions/r2.13.1/api_docs/python/tf/keras/layers/MultiHeadAttention  
**Role:** reference_doc | **Need:** COMPARISON_DATA  
**Anchor:** Exact constructor/call signature; `attention_mask` shape/broadcast rules; training vs inference dropout; causal masking flag.

## Key Content
- **Constructor (TF 2.13.1):**  
  `tf.keras.layers.MultiHeadAttention(num_heads, key_dim, value_dim=None, dropout=0.0, use_bias=True, output_shape=None, attention_axes=None, kernel_initializer='glorot_uniform', bias_initializer='zeros', kernel_regularizer=None, bias_regularizer=None, activity_regularizer=None, kernel_constraint=None, bias_constraint=None, **kwargs)`
- **Core computation (Scaled Dot-Product Attention, described):**  
  Project `query`, `key`, `value` into per-head tensors, then **dot-product + scale → softmax → weighted sum**.  
  Shapes after projection (per head):  
  - `Q`: `(B, <query dims>, key_dim)`  
  - `K`: `(B, <key/value dims>, key_dim)`  
  - `V`: `(B, <key/value dims>, value_dim)`  
  Then concatenate heads and (optionally) output-project.
- **Call signature + tensor shapes:**  
  `layer(query, value, key=None, attention_mask=None, return_attention_scores=False, training=None, use_causal_mask=False)`  
  - `query`: `(B, T, dim)` (target length `T`)  
  - `value`: `(B, S, dim)` (source length `S`)  
  - `key`: optional `(B, S, dim)`; if omitted, `key=value` (common case; self-attn when `query=key=value`)
- **`attention_mask` semantics (boolean):** shape `(B, T, S)`; **1 = can attend**, **0 = blocked**. Broadcasting may occur for **missing batch dims** and the **head dimension**.
- **Dropout behavior:** `dropout` is a probability; `training=True` enables dropout, `training=False` disables it (inference). If `training` not passed, uses parent layer/model mode or defaults to inference if none.
- **Outputs:**  
  - `attention_output`: `(B, T, E)` where `E` = query last-dim if `output_shape=None`, else projected to `output_shape`.  
  - Optional `attention_scores` if `return_attention_scores=True`.

## When to surface
Use when students ask how TF/Keras MHA expects mask shapes/values, how broadcasting works, what `use_causal_mask` does, or why dropout differs between training and inference in `MultiHeadAttention`.