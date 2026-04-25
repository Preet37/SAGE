# Card: Bahdanau (Additive) Attention in TF NMT Tutorial
**Source:** https://www.tensorflow.org/tutorials/text/nmt_with_attention?hl=ko  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Official TensorFlow tutorial semantics for additive attention equations, tensor shapes, softmax axis choice, and masking in loss.

## Key Content
- **Data preprocessing pipeline**
  - Normalize to ASCII, lowercase/strip; pad punctuation with spaces via regex; remove non `[a-zA-Z?.!,¿]`; add tokens: `"<start> ... <end>"`.
  - Tokenize with `tf.keras.preprocessing.text.Tokenizer(filters='')`; pad sequences `padding='post'`.
- **Dataset / batching defaults**
  - `num_examples=30000`; train/val split `test_size=0.2` → `24000` train, `6000` val.
  - `BATCH_SIZE=64`; example shapes: input `(64,16)`, target `(64,11)`.
  - Hyperparams: `embedding_dim=256`, `units=1024`; `steps_per_epoch=len(train)//64`.
- **Encoder (GRU) outputs**
  - Encoder returns `enc_output` shape `(batch, max_len, units)` and `enc_hidden` shape `(batch, units)`; example `(64,16,1024)` and `(64,1024)`.
- **Bahdanau attention (Eq. 1–3) with shapes**
  - **Eq. 1 (score):**  
    `score = V(tanh(W1(query_with_time_axis) + W2(values)))`  
    where `query` = decoder hidden state `(batch, hidden)`, `query_with_time_axis=expand_dims(query,1)` → `(batch,1,hidden)`, `values` = encoder outputs `(batch,max_len,hidden)`.  
    `score` shape `(batch,max_len,1)`.
  - **Eq. 2 (weights):** `attention_weights = softmax(score, axis=1)` (axis=1 because `max_len` is the alignment dimension).
  - **Eq. 3 (context):** `context_vector = sum(attention_weights * values, axis=1)` → `(batch, hidden)`.
- **Decoder step**
  - Embed input token `x` → `(batch,1,embed)`; concat with context: `concat([expand_dims(context,1), x], axis=-1)` → `(batch,1,embed+hidden)`; GRU; reshape output to `(batch, hidden)`; final logits via Dense to vocab. Example decoder output `(64, vocab_tar)` = `(64,4935)`.
- **Training procedure**
  - Teacher forcing loop over target timesteps; initial `dec_input` is `<start>` token repeated `BATCH_SIZE`.
  - Loss: `SparseCategoricalCrossentropy(from_logits=True, reduction='none')` with **padding mask** `real != 0`; multiply loss by mask; `reduce_mean`.
  - Optimizer: Adam; checkpoints every 2 epochs.
- **Inference**
  - No teacher forcing; stop when predicted token is `<end>`; store attention weights each step for plotting.

## When to surface
Use when students ask how additive (Bahdanau) attention is computed (equations + tensor shapes), why softmax uses `axis=1`, or how masking/teacher forcing is implemented in TF seq2seq NMT.