# Card: Seq2Seq w/ Attention — Teacher Forcing, Training Loop, Decoding
**Source:** https://docs.pytorch.org/tutorials/intermediate/seq2seq_translation_tutorial.html  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Explicit `teacher_forcing` behavior in decoder forward + end-to-end training/eval code path.

## Key Content
- **Seq2Seq core (Encoder→Decoder):** Encoder GRU reads input tokens → outputs `encoder_outputs` and final `encoder_hidden` (context). Decoder starts with `SOS_token` and initial hidden = `encoder_hidden`.
- **Teacher forcing decision (Decoder forward loop):** For each timestep `i` up to `MAX_LENGTH`:
  - If `target_tensor is not None`: **teacher forcing** input is gold previous token  
    `decoder_input = target_tensor[:, i].unsqueeze(1)`
  - Else: **free-running** input is model prediction  
    `_, topi = decoder_output.topk(1)`; `decoder_input = topi.squeeze(-1).detach()`
- **Output distribution:** Decoder concatenates per-step logits → `F.log_softmax(decoder_outputs, dim=-1)`; training uses `nn.NLLLoss`.
- **Loss equation (flattened):**  
  **Eq. 1:** `loss = NLLLoss(decoder_outputs.view(-1, V), target_tensor.view(-1))`  
  where `V = decoder_outputs.size(-1)` (vocab size), flattening batch×time.
- **Training epoch procedure:** For each batch: zero grads → `encoder(input_tensor)` → `decoder(encoder_outputs, encoder_hidden, target_tensor)` → compute Eq.1 → `loss.backward()` → `optimizer.step()` for both encoder/decoder.
- **Evaluation decoding:** No targets; decoder runs autoregressively. After `decoder(...)`, take `topk(1)` over vocab, iterate predicted ids until `EOS_token`, map via `output_lang.index2word`.
- **Defaults/params:** `SOS_token=0`, `EOS_token=1`, `MAX_LENGTH=10`; Adam lr `0.001`; `hidden_size=128`, `batch_size=32`; dropout default `0.1`.
- **Empirical training trace (example):** After 80 epochs, avg loss drops to ~`0.0284` (printed at epoch 80).

## When to surface
Use when students ask how teacher forcing is implemented (exactly when gold tokens vs predictions are fed), how the seq2seq training loop computes loss/backprop, or how decoding stops at EOS during evaluation.