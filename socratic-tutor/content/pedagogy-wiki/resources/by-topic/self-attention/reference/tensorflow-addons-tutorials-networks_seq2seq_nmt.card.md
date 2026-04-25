# Card: Seq2Seq NMT pipeline (tokenization → encoder-decoder → decoding)
**Source:** https://www.tensorflow.org/addons/tutorials/networks_seq2seq_nmt  
**Role:** explainer | **Need:** WORKING_EXAMPLE  
**Anchor:** End-to-end NMT workflow with concrete dataset formatting, masking rationale, shapes, training loop, and greedy decoding.

## Key Content
- **Task/data:** English→Spanish sentence pairs (Anki dataset). Split: **118,964** total; **83,276** train; **17,844** val; **17,844** test.
- **Hyperparameters/defaults:** `BATCH_SIZE=64`, `EPOCHS=1` (note: “≥10 for convergence”), `MAX_SEQUENCE_LENGTH=40`, `ENG_VOCAB_SIZE=15000`, `SPA_VOCAB_SIZE=15000`, `EMBED_DIM=256`, `INTERMEDIATE_DIM=2048`, `NUM_HEADS=8`.
- **Special tokens:** `["[PAD]","[UNK]","[START]","[END]"]`. Spanish sequences get `[START]` and `[END]`; padding uses `[PAD]`.
- **Training data alignment (teacher forcing):**
  - Inputs dict: `encoder_inputs` = tokenized/padded English; `decoder_inputs` = Spanish tokens **excluding last** (`spa[:, :-1]`).
  - Targets: Spanish tokens **shifted left** (`spa[:, 1:]`).
  - Observed shapes for one batch: `encoder_inputs (64,40)`, `decoder_inputs (64,40)`, `targets (64,40)`.
- **Model procedure:**
  - Encoder: `TokenAndPositionEmbedding(vocab=15000, seq_len=40, dim=256)` → `TransformerEncoder(intermediate_dim=2048, num_heads=8)`.
  - Decoder: `TokenAndPositionEmbedding(...)` → `TransformerDecoder(intermediate_dim=2048, num_heads=8)` with **causal masking enabled by default** (prevents using future target tokens) → `Dropout(0.5)` → `Dense(15000, softmax)`.
- **Training setup/results:** `optimizer="rmsprop"`, `loss="sparse_categorical_crossentropy"`, metric `accuracy`. After **1 epoch**: train **accuracy 0.8385**, **loss 1.1014**; val **accuracy 0.8661**, **loss 0.8040**. Total params **14,449,304**.
- **Greedy decoding algorithm:** Start prompt = `[START]` + `[PAD]` to length 40; iteratively sample next token via `logits = transformer([encoder_input_tokens, prompt])[:, index-1, :]` until `[END]`.
- **Quant eval (ROUGE on 30 tests):** ROUGE-1 **P 0.3267 / R 0.3378 / F1 0.3207**; ROUGE-2 **P 0.0940 / R 0.1051 / F1 0.0966**. After **10 epochs**: ROUGE-1 **F1 0.579**, ROUGE-2 **F1 0.381**.

## When to surface
Use when students ask how to format seq2seq datasets (shifted decoder inputs/targets), why causal masking is needed, what shapes to expect, or how to implement greedy decoding and basic training metrics for NMT.