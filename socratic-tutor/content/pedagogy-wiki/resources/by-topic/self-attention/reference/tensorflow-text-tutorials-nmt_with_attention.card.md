# Card: TF Seq2Seq NMT w/ Attention (Encoder–Decoder + CrossAttention)
**Source:** https://www.tensorflow.org/text/tutorials/nmt_with_attention  
**Role:** code | **Need:** WORKING_EXAMPLE  
**Anchor:** Runnable end-to-end NMT pipeline (Spanish→English) with explicit encoder/decoder + attention computation, training, inference, plotting, and export.

## Key Content
- **Text preprocessing (inside model for SavedModel export):**
  - Standardize (Unicode NFKD) + lowercase + regex cleanup: keep `[^ a-z.?!,¿]`, space punctuation, add `[START] ... [END]`.
  - `TextVectorization(max_tokens=5000, ragged=True)` for both context/target; then `.to_tensor()` for 0-padding.
  - Training pair transform: `((context, targ_in), targ_out)` where `targ_in = target[:, :-1]`, `targ_out = target[:, 1:]`.
- **Model architecture + defaults:**
  - `UNITS = 256`, `BATCH_SIZE = 64`, train split ≈ 80%.
  - **Encoder:** `Embedding(vocab_size, units, mask_zero=True)` → `Bidirectional(GRU(units, return_sequences=True), merge_mode='sum')` → outputs `context` with shape `(batch, s, units)`.
  - **Attention (CrossAttention):** `MultiHeadAttention(num_heads=1, key_dim=units)` with `query=x` (decoder sequence), `value=context`; returns `attn_output` and `attn_scores` shaped `(batch, heads, t, s)` then averaged over heads → `(batch, t, s)`; residual add + `LayerNormalization`.
  - **Decoder:** `Embedding` → `GRU(units, return_sequences=True, return_state=True)` → `CrossAttention` → `Dense(vocab_size)` logits.
- **Training objective (Eq. 1 masked CE):**
  - Per-token loss: `CE(y_true, y_pred)` (SparseCategoricalCrossentropy, `from_logits=True`, `reduction='none'`).
  - Mask padding: `mask = 1[y_true != 0]`; final `loss = sum(CE*mask)/sum(mask)`.
  - Accuracy similarly masked after `argmax`.
  - Compile: `optimizer='adam'`, metrics `[masked_acc, masked_loss]`.
  - Expected initial metrics for uniform logits: `loss ≈ log(vocab_size)`, `acc ≈ 1/vocab_size`.
- **Inference loop (greedy or sampling):**
  - Initialize with `[START]`; step: run decoder on last token + state → logits.
  - If `temperature==0`: `next_token = argmax(logits)` else sample `categorical(logits/temperature)`.
  - Stop when `next_token == [END]`; force padding token `0` after done.
  - Cache attention weights each step for plotting.
- **Export + performance:**
  - Wrap `translate` in `@tf.function(input_signature=[TensorSpec(tf.string,[None])])`, save via `tf.saved_model.save`.
  - Dynamic loop variant uses `for t in tf.range(max_length)` + `TensorArray` to avoid static unrolling and allow early `break`.

## When to surface
Use when students ask how to implement/train/infer an RNN seq2seq translator with attention in TensorFlow, including masking, teacher forcing shift, attention weight shapes, and SavedModel export with a dynamic decoding loop.