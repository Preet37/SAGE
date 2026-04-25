# Card: Unpacking PackedSequence with `pad_packed_sequence`
**Source:** https://pytorch.org/docs/stable/generated/torch.nn.utils.rnn.pad_packed_sequence.html  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Exact unpacking behavior, output shapes, and `total_length` handling for recovering padded encoder outputs (e.g., for attention).

## Key Content
- **Purpose:** Inverse of `pack_padded_sequence`. Converts a `PackedSequence` back to a padded tensor plus the true lengths.
- **Signature (PyTorch):**  
  `pad_packed_sequence(sequence, batch_first=False, padding_value=0.0, total_length=None)`  
  - `sequence`: a `PackedSequence` (typically RNN output).  
  - `batch_first`: if `False` (default), time dimension first. If `True`, batch dimension first.  
  - `padding_value`: value used to pad shorter sequences (default `0.0`).  
  - `total_length`: if set, pads output to this fixed time length.
- **Returns:** `(padded_sequence, lengths)`  
  - `lengths`: tensor of original sequence lengths (after any sorting used during packing).
- **Output shapes (Eq. 1):** Let `T` = max sequence length in batch (or `total_length` if provided), `B` = batch size, `*` = remaining feature dims (e.g., hidden size).  
  - If `batch_first=False`: `padded_sequence.shape = (T, B, *)`  
  - If `batch_first=True`: `padded_sequence.shape = (B, T, *)`
- **`total_length` behavior (Eq. 2):** If `total_length` is specified, output is padded so that `T = total_length` (useful to match a known max length for attention masks / batching consistency).

## When to surface
Use when a student asks how to recover padded encoder/RNN outputs from a `PackedSequence`, what tensor shape to expect (`T,B,*` vs `B,T,*`), or how/why to use `total_length` to force a fixed time dimension for attention.