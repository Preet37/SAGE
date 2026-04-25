# Card: Bahdanau (Additive) Attention: Align + Translate
**Source:** https://iclr.cc/archive/www/lib/exe/fetch.php%3Fmedia=iclr2015:bahdanau-iclr2015.pdf  
**Role:** paper | **Need:** FORMULA_SOURCE  
**Anchor:** Additive alignment model + context integration into decoder (RNNsearch)

## Key Content
- **Problem / rationale (Intro, Sec. 1):** Fixed-length encoder context vector is a bottleneck, especially for long sentences. Solution: let decoder **soft-search** relevant source positions per target step via differentiable alignment (“soft alignment” enables backprop; alignment not treated as latent variable).
- **Encoder (Sec. 3.2):** **Bidirectional RNN** produces a sequence of annotations \(h_1,\dots,h_{T_x}\), where each \(h_j\) summarizes source token \(x_j\) with left+right context.
- **Alignment / attention (Sec. 3.1):**
  - **Score (alignment energy):**  
    \[
    e_{ij} = a(s_{i-1}, h_j)
    \]
    where \(s_{i-1}\) is decoder hidden state before emitting \(y_i\), \(h_j\) is encoder annotation, and \(a(\cdot)\) is a **feedforward NN** (additive attention; tanh nonlinearity emphasized as crucial in slides).
  - **Attention weights (softmax):**  
    \[
    \alpha_{ij} = \frac{\exp(e_{ij})}{\sum_{k=1}^{T_x}\exp(e_{ik})}
    \]
  - **Context vector:**  
    \[
    c_i = \sum_{j=1}^{T_x}\alpha_{ij} h_j
    \]
- **Decoder conditional generation (Sec. 3.1):** Predict next token using previous tokens + context:  
  \[
  p(y_i \mid y_{<i}, x) = g(y_{i-1}, s_i, c_i)
  \]
  with decoder state updated using \(c_i\) (decoder “searches” source each step).
- **Training objective (Sec. 4 / slides):** maximize (equivalently minimize negative) mean log-likelihood \(\log p(y\mid x;\theta)\); fully differentiable → standard gradient methods.
- **Empirical setup (slides):** English→French WMT’14; **RNNsearch** and baseline **RNN Encoder-Decoder** both with **1000 units**; vocab **30,000 + UNK** for neural models; Moses SMT uses full vocab. Key qualitative claim: **no performance drop on long sentences** for attention model; RNNsearch outperforms baseline and is comparable to SMT (BLEU table referenced in paper).

## When to surface
Use when students ask how **Bahdanau/additive attention** is computed (scores → softmax → context) and how it plugs into the **seq2seq decoder probability/state update**, or why attention helps with **long sentences** vs fixed-length context.