# Card: Seq2Seq Translation w/ Bahdanau (Additive) Attention (PyTorch)
**Source:** https://docs.pytorch.org/tutorials/intermediate/seq2seq_translation_tutorial.html  
**Role:** code | **Need:** WORKING_EXAMPLE  
**Anchor:** End-to-end seq2seq+attention training loop w/ teacher forcing; explicit attention step order + tensor-shape-aware PyTorch code.

## Key Content
- **Data + preprocessing defaults**
  - Normalize: Unicode→ASCII, lowercase, trim punctuation; keep letters + `!?`.
  - Filter: `MAX_LENGTH = 10` tokens; keep English targets starting with prefixes: `"i am "`, `"he is"`, `"she is"`, `"you are"`, `"we are"`, `"they are"` (incl. contractions).
  - After filtering: `135842 → 11445` sentence pairs. Vocab sizes: French `4601`, English `2991`. Tokens: `SOS=0`, `EOS=1`.
- **Encoder (GRU, batch_first)**
  - `Embedding(input_size, hidden_size)` → `GRU(hidden_size, hidden_size, batch_first=True)` with dropout `p=0.1`.
  - Outputs: `encoder_outputs` shape `[B, T, H]`, `encoder_hidden` `[1, B, H]`.
- **Bahdanau attention (Eq. 1–3)**
  - (Eq.1) `score = Va(tanh(Wa(query) + Ua(keys)))`
  - (Eq.2) `weights = softmax(score, dim=-1)`
  - (Eq.3) `context = bmm(weights, keys)`
  - Shapes in code: `query = hidden.permute(1,0,2)` → `[B,1,H]`; `keys=encoder_outputs` `[B,T,H]`; `weights` `[B,1,T]`; `context` `[B,1,H]`.
- **Attention decoder step order (per time step)**
  1) embed input token (dropout)  
  2) compute `context, attn_weights` from `(query, encoder_outputs)`  
  3) concat `input_gru = cat(embedded, context)` → `[B,1,2H]`  
  4) GRU: `GRU(2H→H)`  
  5) linear to vocab; collect outputs; final `log_softmax(dim=-1)`.
- **Training loop (teacher forcing via target_tensor)**
  - `encoder_outputs, encoder_hidden = encoder(input_tensor)`
  - `decoder_outputs = decoder(..., target_tensor)` (teacher forcing each step: `decoder_input = target_tensor[:, i].unsqueeze(1)`)
  - Loss: `NLLLoss` on flattened tensors: `decoder_outputs.view(-1,V)` vs `target_tensor.view(-1)`.
  - Optimizers: Adam(lr=`0.001`) for encoder+decoder.
- **Example run hyperparams/results**
  - `hidden_size=128`, `batch_size=32`, train `80` epochs; sample loss drops to ~`0.0293` by epoch 80; runtime shown ~`8m 28s` (environment-dependent).

## When to surface
Use when students ask how additive (Bahdanau) attention is computed in code (scores→softmax→context) or how to implement/train an end-to-end seq2seq+attention model with teacher forcing and correct tensor shapes in PyTorch.