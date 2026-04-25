# Card: PyTorch `nn.LSTM` essentials (defaults, equations, dropout)
**Source:** https://docs.pytorch.org/docs/stable/generated/torch.nn.LSTM.html  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Exact parameter defaults/behaviors; formal gate equations; dropout semantics (between stacked layers, not last)

## Key Content
- **Module signature + defaults:** `torch.nn.LSTM(input_size, hidden_size, num_layers=1, bias=True, batch_first=False, dropout=0.0, bidirectional=False, proj_size=0, device=None, dtype=None)`
- **LSTM gate equations (Eq. 1, per time step t, per layer):**  
  Let input \(x_t\), previous hidden \(h_{t-1}\), previous cell \(c_{t-1}\). Gates: input \(i_t\), forget \(f_t\), cell candidate \(g_t\), output \(o_t\).  
  \[
  i_t=\sigma(W_{ii}x_t+b_{ii}+W_{hi}h_{t-1}+b_{hi})
  \]
  \[
  f_t=\sigma(W_{if}x_t+b_{if}+W_{hf}h_{t-1}+b_{hf})
  \]
  \[
  g_t=\tanh(W_{ig}x_t+b_{ig}+W_{hg}h_{t-1}+b_{hg})
  \]
  \[
  o_t=\sigma(W_{io}x_t+b_{io}+W_{ho}h_{t-1}+b_{ho})
  \]
  \[
  c_t=f_t\odot c_{t-1}+i_t\odot g_t,\quad h_t=o_t\odot\tanh(c_t)
  \]
  where \(\sigma\)=sigmoid, \(\odot\)=Hadamard product.
- **Dropout semantics (stacked LSTMs):** In multilayer LSTM, input to layer \(l\) is previous layer’s hidden state multiplied by dropout mask; PyTorch applies dropout **on outputs of each layer except the last**, with probability=`dropout` (default `0.0`).
- **Bidirectionality:** `bidirectional=False` by default; if `True`, outputs concatenate forward+reverse states. Note: for bidirectional LSTMs, `h_n` ≠ last element of `output`.
- **Shapes & batching:** `batch_first=True` uses `(batch, seq, feature)` for input/output; **does not** change hidden/cell state layout.
- **Projections:** `proj_size>0` enables LSTM with projections; hidden output dimension becomes `proj_size` and each layer output is multiplied by learnable projection matrix.

## When to surface
Use when students ask how LSTM gates work mathematically, what PyTorch’s `nn.LSTM` defaults are, or why dropout in stacked LSTMs doesn’t affect the last layer (common in seq2seq encoder/decoder bottleneck discussions).