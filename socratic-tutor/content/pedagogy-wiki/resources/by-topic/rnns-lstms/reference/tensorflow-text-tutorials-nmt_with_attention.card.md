# Card: TensorFlow/Keras Cross-Attention Wiring (Seq2Seq NMT)
**Source:** https://www.tensorflow.org/text/tutorials/nmt_with_attention  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Concrete TensorFlow/Keras attention wiring with explicit tensor shapes, masking behavior, and layer-call semantics (query/value, softmax location, context combination)

## Key Content
- **Pipeline (data → training pairs):**
  - Standardize text: Unicode NFKD normalize → lowercase → regex keep `[^ a-z.?!,¿]` removed → space around punctuation → strip → add `[START] ... [END]`.
  - `TextVectorization(..., max_tokens=5000, ragged=True)` for context/target; convert to dense with `.to_tensor()` (0-padding).
  - Training pair transform: `targ_in = target[:, :-1]`, `targ_out = target[:, 1:]`; model inputs `((context, targ_in), targ_out)`.

- **Encoder (shapes):**
  - Embedding: `Embedding(vocab_size, units, mask_zero=True)`.
  - BiGRU: `Bidirectional(GRU(units, return_sequences=True), merge_mode='sum')`.
  - Input `(batch, s)` → output context `(batch, s, units)`. Default `UNITS=256`.

- **Cross-attention layer (Section “The attention layer”):**
  - Uses `tf.keras.layers.MultiHeadAttention(key_dim=units, num_heads=1)`.
  - Call: `attn_output, attn_scores = mha(query=x, value=context, return_attention_scores=True)`.
  - Shapes: query `x: (batch, t, units)`, value/context `(batch, s, units)`, scores `(batch, heads, t, s)` → mean over heads → `(batch, t, s)`.
  - **Softmax happens inside `MultiHeadAttention`**; attention weights sum to 1 over `s` for each `t`.
  - Residual + norm: `x = LayerNorm(x + attn_output)`; caches `last_attention_weights`.

- **Decoder (training call):**
  - Embedding → GRU (`return_sequences=True, return_state=True`) → attention with **RNN output as query** → Dense to logits.
  - Logits shape `(batch, t, target_vocab_size)`; loss uses `SparseCategoricalCrossentropy(from_logits=True)`.

- **Masking & metrics:**
  - Padding token id `0`; masked loss/accuracy multiply by `mask = (y_true != 0)` and normalize by `sum(mask)`.
  - Model deletes `logits._keras_mask` to prevent Keras scaling loss/accuracy.

- **Inference loop:**
  - Start token `[START]`; iterative `get_next_token` with optional `temperature` (0 → argmax; else sample).
  - `done` when `[END]`; once done, force next tokens to `0` padding.
  - Efficient graph mode: dynamic `for t in tf.range(max_length)` + `tf.TensorArray`.

## When to surface
Use when students ask how to implement Bahdanau-style cross-attention in Keras with correct tensor shapes/masks, or where softmax/weights live in `MultiHeadAttention`, and how to combine attention output with decoder state during training/inference.