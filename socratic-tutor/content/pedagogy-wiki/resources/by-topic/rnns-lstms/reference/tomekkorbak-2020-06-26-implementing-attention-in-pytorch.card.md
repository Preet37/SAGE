# Card: Additive (Bahdanau) vs Multiplicative (Luong) Attention — PyTorch
**Source:** https://tomekkorbak.com/2020/06/26/implementing-attention-in-pytorch/  
**Role:** explainer | **Need:** COMPARISON_DATA  
**Anchor:** Side-by-side additive (MLP) vs multiplicative (bilinear/dot) implementations, parameterization, and scaling tied to hidden sizes.

## Key Content
- **Context vector as weighted average (Eq. 1):**  
  \[
  \mathbf{c}_i=\sum_j a_{ij}\mathbf{s}_j
  \]
  where \(\mathbf{s}_j\) = encoder hidden state \(j\), \(\mathbf{c}_i\) = context at decoder step \(i\), \(a_{ij}\) = attention weight.
- **Weights from score + softmax (Eq. 2):**  
  \[
  \mathbf{a}_i=\text{softmax}(f_{\text{att}}(\mathbf{h}_i,\mathbf{s}_j))
  \]
  where \(\mathbf{h}_i\) = decoder hidden state (query), \(\mathbf{s}_j\) = encoder states (values). Softmax yields categorical distribution \(p(\mathbf{s}_j\mid \mathbf{h}_i)\).
- **Additive/Bahdanau score (Eq. 3):**  
  \[
  f_{\text{att}}(\mathbf{h}_i,\mathbf{s}_j)=\mathbf{v}_a^\top \tanh(\mathbf{W}_1\mathbf{h}_i+\mathbf{W}_2\mathbf{s}_j)
  \]
  Params: \(\mathbf{W}_1:\text{decoder\_dim}\to\text{decoder\_dim}\), \(\mathbf{W}_2:\text{encoder\_dim}\to\text{decoder\_dim}\), \(\mathbf{v}_a\in\mathbb{R}^{\text{decoder\_dim}}\). Vectorized PyTorch: repeat query to `[seq_len, decoder_dim]`, compute `tanh(W1(query)+W2(values)) @ v`.
- **Multiplicative/Luong score (Eq. 4):**  
  \[
  f_{\text{att}}(\mathbf{h}_i,\mathbf{s}_j)=\mathbf{h}_i^\top \mathbf{W}\mathbf{s}_j
  \]
  with \(\mathbf{W}\in\mathbb{R}^{\text{decoder\_dim}\times \text{encoder\_dim}}\). Vectorized: `query @ W @ values.T` → `[seq_len]`.
- **Scaling rationale (Eq. 5):** divide multiplicative scores by \(\sqrt{\text{decoder\_dim}}\) (per Vaswani et al.) to control magnitude: `weights / sqrt(decoder_dim)`.
- **Defaults shown:** parameter init uniform \([-0.1,0.1]\); example dims `encoder_dim=100`, `decoder_dim=50`; example loop: at each decoding step compute `context_vector = attention(h, encoder_hidden_states)` then feed to `LSTMCell`.

## When to surface
Use when students ask how Bahdanau vs Luong attention scores are computed, how to implement them in PyTorch with correct tensor shapes, or why scaled dot/bilinear attention divides by \(\sqrt{d}\).