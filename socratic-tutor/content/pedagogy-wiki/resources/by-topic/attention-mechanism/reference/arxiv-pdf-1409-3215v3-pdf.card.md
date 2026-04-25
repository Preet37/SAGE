# Card: Seq2Seq LSTM (fixed context) + MLE objective + reversing trick
**Source:** https://arxiv.org/pdf/1409.3215v3.pdf  
**Role:** paper | **Need:** FORMULA_SOURCE  
**Anchor:** MLE training objective for seq2seq with decoder factorization; fixed-length context vector as final encoder state; RNN/LSTM update + teacher-forcing setup; reversing-source rationale/results.

## Key Content
- **Vanilla RNN equations (Sec. 2):** for inputs \(x_{1:T}\):  
  \[
  h_t=\sigma(W_{hx}x_t + W_{hh}h_{t-1}),\quad y_t=W_{yh}h_t
  \]
- **Seq2seq conditional factorization (Eq. 1, Sec. 2):** encode input \(x_{1:T}\) into fixed vector \(v\) (last hidden state; “context”), then decode:  
  \[
  p(y_{1:T'}\mid x_{1:T})=\prod_{t=1}^{T'} p(y_t\mid v, y_{1:t-1})
  \]
  Each \(p(\cdot)\) is a **softmax over target vocabulary**. Use special **\<EOS\>** token so model defines distribution over variable-length outputs.
- **Training objective (Sec. 3.2):** maximize average log-likelihood over dataset \(\mathcal{S}\):  
  \[
  \frac{1}{|\mathcal{S}|}\sum_{(T,S)\in\mathcal{S}} \log p(T\mid S)
  \]
  (Teacher forcing implied by conditioning on gold prefix \(y_{1:t-1}\) in Eq. 1.)
- **Decoding (Sec. 3.2):** approximate \(\hat T=\arg\max_T p(T\mid S)\) (Eq. 2) via **left-to-right beam search**; keep top \(B\) partial hypotheses; completed when \<EOS\>.
- **Design rationale: reverse source (Sec. 3.3):** reversing source words reduces “minimal time lag,” creating more short-term dependencies → easier optimization/credit assignment.
- **Key empirical results (Sec. 3.3, Table 1):** reversing source improved **test perplexity 5.8→4.7** and **BLEU 25.9→30.6** (single model). Ensemble of 5 reversed LSTMs, beam 12: **BLEU 34.81** vs SMT baseline **33.30**.
- **Defaults/hyperparams (Sec. 3.4):** 4-layer LSTMs; 1000 cells/layer; 1000-d embeddings; vocab: source 160k, target 80k; init U[-0.08,0.08]; SGD lr=0.7, after 5 epochs halve every 0.5 epoch; batch=128; gradient clip: if \(\|g\|_2>5\), set \(g\leftarrow 5g/\|g\|_2\); bucket by length (~2× speedup).

## When to surface
Use when students ask how classic seq2seq defines \(p(y\mid x)\), how MLE/teacher forcing works, what the fixed context vector bottleneck is, or why reversing the source helped early seq2seq LSTMs (with concrete perplexity/BLEU gains).