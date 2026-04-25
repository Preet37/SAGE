# Card: `torch.nn.utils.rnn.pad_sequence` (PyTorch)
**Source:** https://pytorch.org/docs/stable/generated/torch.nn.utils.rnn.pad_sequence.html  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Official padding utility signature/defaults (`batch_first=False`, `padding_value=0.0`) used in seq2seq batching and masking discussions.

## Key Content
- **Purpose:** Pad a list of variable-length sequences (tensors) to the same length by padding to the length of the **longest** sequence.
- **Signature (PyTorch stable):**  
  **Eq. 1:** `pad_sequence(sequences, batch_first=False, padding_value=0.0, padding_side='right') -> Tensor`
- **Inputs:**
  - `sequences`: list/tuple of tensors with shape **(L_i, *)**, where:
    - `L_i` = length of sequence *i*
    - `*` = any number of trailing dimensions (e.g., embedding dim `D`)
  - `batch_first` (bool, **default `False`**): controls output layout.
  - `padding_value` (float, **default `0.0`**): value used for padded positions.
  - `padding_side` (str, **default `'right'`**): pad on the right (end) or left (start).
- **Output shape:**
  - If `batch_first=False` (**default**): **(T, B, *)**
  - If `batch_first=True`: **(B, T, *)**
  - Where:
    - `T = max_i L_i` (max sequence length in the batch)
    - `B = len(sequences)` (batch size)
- **Typical procedure (batching variable-length seq2seq inputs):**
  1. Collect per-example tensors of shape `(L_i, *)`.
  2. Call `pad_sequence(...)` to form a single padded batch tensor.
  3. Build a mask from original lengths to ignore padded positions in loss/attention.

## When to surface
Use when students ask how to batch variable-length sequences in PyTorch, what shapes to expect (`T,B,*` vs `B,T,*`), or what the default padding value/layout is when creating masks for seq2seq models.