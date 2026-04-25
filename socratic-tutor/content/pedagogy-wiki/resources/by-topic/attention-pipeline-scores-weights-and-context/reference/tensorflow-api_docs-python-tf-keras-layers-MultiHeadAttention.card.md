# Card: tf.keras.layers.MultiHeadAttention — mask semantics & call signature
**Source:** https://www.tensorflow.org/api_docs/python/tf/keras/layers/MultiHeadAttention  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Official definitions of `attention_mask` semantics (boolean), shape expectations/broadcasting, and the layer call signature (incl. causal masking)

## Key Content
- **Core computation (scaled dot-product attention, per head)**  
  - Project inputs into heads:  
    - Query head shape: `(B, <T dims>, key_dim)`  
    - Key head shape: `(B, <S dims>, key_dim)`  
    - Value head shape: `(B, <S dims>, value_dim)`  
  - Attention logits: **Eq. 1** `L = (Q · Kᵀ) * scale` (docs state “dot-producted and scaled”; standard scale is `1/sqrt(key_dim)`), then `softmax(L)` → attention probabilities; probabilities weight `V`; heads concatenated; optional final linear projection.
- **Call signature (what masking applies to):**  
  `call(query, value, key=None, attention_mask=None, return_attention_scores=False, training=None, use_causal_mask=False)`
- **Input/Output shapes:**  
  - `query`: `(B, T, dim)`; `value`: `(B, S, dim)`; `key` optional `(B, S, dim)`; if `key` not given, **uses `value` for both key and value** (common self-attention case).  
  - Returns `attention_output`: `(B, T, E)` where `E = query last dim` if `output_shape=None`, else projected to `output_shape`.  
  - If `return_attention_scores=True`, returns `(attention_output, attention_scores)` (scores are multi-head coefficients over attention axes).
- **`attention_mask` semantics (boolean, not additive):**  
  - Shape: `(B, T, S)`; **1 = can attend**, **0 = cannot attend**.  
  - **Broadcasting** may occur for missing batch dimensions **and the head dimension**.
- **Causal masking:**  
  - `use_causal_mask=True` applies a causal mask to prevent attending to future tokens (decoder-style).
- **Key defaults/params:** `dropout=0.0`, `use_bias=True`, `attention_axes=None` (attend over all axes except batch/heads/features), `output_shape=None`.

## When to surface
Use when students ask how to build padding/causal masks for Keras MHA, what mask values mean (0/1), what shapes are required/broadcastable, or what `call()` arguments control masking and returned attention scores.