# Card: `pack_padded_sequence` (masking variable-length RNN inputs)
**Source:** https://pytorch.org/docs/stable/generated/torch.nn.utils.rnn.pack_padded_sequence.html  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Exact signature/defaults, required shapes, and the official workflow for variable-length sequence batching for RNN/LSTM/GRU.

## Key Content
- **API (PyTorch stable)**
  - **Signature (Eq. 1):**  
    `torch.nn.utils.rnn.pack_padded_sequence(input, lengths, batch_first=False, enforce_sorted=True)`  
    - `batch_first` **default = False**  
    - `enforce_sorted` **default = True**
- **Purpose / rationale**
  - Packs a padded batch of variable-length sequences into a `PackedSequence` so RNN modules skip computation on padding timesteps (efficient + avoids padding influencing hidden states).
- **Required input shapes**
  - If `batch_first=False` (default): `input` shape **(T, B, *)**  
  - If `batch_first=True`: `input` shape **(B, T, *)**  
  - `T` = max sequence length in batch, `B` = batch size, `*` = any number of feature dims (e.g., embedding size).
- **Lengths argument**
  - `lengths`: 1D tensor/list of sequence lengths for each batch element (size `B`).
- **Sorting constraint**
  - With `enforce_sorted=True`, sequences **must be sorted by length in decreasing order** (required for ONNX export per docs).  
  - If not sorted, set `enforce_sorted=False` (PyTorch will handle sorting internally).
- **Canonical procedure (workflow)**
  1. Pad sequences to common `T` (and optionally sort by length desc).
  2. Call `pack_padded_sequence(...)` to create a `PackedSequence`.
  3. Feed packed input to `nn.RNN` / `nn.GRU` / `nn.LSTM`.
  4. (If needed) convert outputs back with `pad_packed_sequence` for attention/decoding.

## When to surface
Use when students ask how to batch variable-length sequences for an encoder RNN/LSTM without letting padding affect computation, or when debugging shape/sorting errors involving `PackedSequence` and `enforce_sorted`.