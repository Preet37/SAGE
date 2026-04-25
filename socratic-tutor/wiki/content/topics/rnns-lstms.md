---
title: "RNNs & LSTMs"
subject: "Sequence Models & Attention"
date: 2026-04-06
tags:
  - "subject/sequence-models-and-attention"
  - "level/beginner"
  - "level/intermediate"
  - "level/advanced"
  - "educator/andrej-karpathy"
  - "educator/christopher-olah"
  - "educator/lilian-weng"
  - "educator/jay-alammar"
  - "resource/video"
  - "resource/blog"
  - "resource/deep-dive"
  - "resource/paper"
  - "resource/code"
educators:
  - "Andrej Karpathy"
  - "Christopher Olah"
  - "Lilian Weng"
  - "Jay Alammar"
levels:
  - "beginner"
  - "intermediate"
  - "advanced"
resources:
  - "video"
  - "blog"
  - "deep-dive"
  - "paper"
  - "code"
---

# Rnns Lstms

## Video (best)
- **Andrej Karpathy** — "The spelled-out intro to language modeling: building makemore" (covers RNNs deeply in context)
- **Watch:** [YouTube](https://www.youtube.com/watch?v=PaCmpygFfXo)
- Why: Karpathy builds RNN-based character-level language models from scratch, explaining hidden states, backpropagation through time, and vanishing gradients with hands-on code. The ground-up construction makes abstract concepts concrete. For LSTM specifically, his CS231n lecture is the canonical reference.
- Level: intermediate

> [NOT VERIFIED] — Confirm this video ID maps to the makemore/RNN episode in the series. The broader "Neural Networks: Zero to Hero" playlist is well-established.

## Blog / Written explainer (best)
- **Christopher Olah** — "Understanding LSTM Networks"
- **Link:** [https://colah.github.io/posts/2015-08-Understanding-LSTMs/](https://colah.github.io/posts/2015-08-Understanding-LSTMs/)
- Why: The single most-cited pedagogical resource on LSTMs. Olah's diagrams of cell state, forget/input/output gates, and the comparison to vanilla RNNs are exceptionally clear. Covers vanishing gradients motivation and gating mechanisms in a visually intuitive way that textbooks rarely match.
- Level: beginner/intermediate

## Deep dive
- **Lilian Weng** — "Attention? Attention!"
- **Link:** [https://lilianweng.github.io/posts/2018-06-24-attention/](https://lilianweng.github.io/posts/2018-06-24-attention/)
- Why: Covers the full arc from seq2seq bottleneck → Bahdanau attention → alignment scores → encoder-decoder attention in one comprehensive post. Includes mathematical derivations, architecture diagrams, and historical context. Bridges the LSTM/RNN foundation to the attention mechanism that superseded it, making it ideal for the full topic scope listed here.
- Level: intermediate/advanced

## Original paper
- **Hochreiter & Schmidhuber (1997)** — "Long Short-Term Memory"
- **Link:** [https://www.bioinf.jku.at/publications/older/2604.pdf](https://www.bioinf.jku.at/publications/older/2604.pdf)
- Why: The foundational LSTM paper. While dense, it remains the definitive reference for the gating mechanism design rationale and the explicit treatment of the vanishing gradient problem. For Bahdanau attention specifically, the companion paper is below.

**Companion — Bahdanau et al. (2014)** — "Neural Machine Translation by Jointly Learning to Align and Translate"
- **Link:** [https://arxiv.org/abs/1409.0473](https://arxiv.org/abs/1409.0473)
- Why: Introduces alignment scores and the attention mechanism over encoder hidden states — directly maps to the seq2seq bottleneck and encoder-decoder attention concepts in this topic. Highly readable for a research paper.

## Code walkthrough
- **Jay Alammar** — "Visualizing A Neural Machine Translation Model (Mechanics of Seq2seq Models With Attention)"
- **Link:** [https://jalammar.github.io/visualizing-neural-machine-translation-mechanics-of-seq2seq-models-with-attention/](https://jalammar.github.io/visualizing-neural-machine-translation-mechanics-of-seq2seq-models-with-attention/)
- Why: Step-by-step animated walkthrough of a seq2seq model with Bahdanau-style attention, showing exactly how encoder hidden states are queried, how alignment scores are computed, and how the context vector is formed. Pairs naturally with Olah's LSTM post as a two-part reading sequence. Includes enough implementation detail to guide coding.
- Level: intermediate

> **Note:** For a pure code implementation, the PyTorch official tutorial "NLP From Scratch: Translation with a Sequence to Sequence Network and Attention" at https://pytorch.org/tutorials/intermediate/seq2seq_translation_tutorial.html is the best hands-on complement.

## Coverage notes
- **Strong:** LSTM gating mechanisms and cell state (Olah blog is definitive), Bahdanau attention and alignment scores (Weng + Alammar are excellent), seq2seq bottleneck motivation, original papers
- **Weak:** Dedicated video covering *all* related concepts (RNN → LSTM → seq2seq → attention) in a single resource without jumping between multiple videos
- **Gap:** No single YouTube video cleanly covers the full arc from vanishing gradients → LSTM → seq2seq bottleneck → Bahdanau attention in one sitting. Karpathy's series requires watching multiple episodes. StatQuest has individual LSTM videos but does not connect through to attention. A purpose-built video for this exact topic cluster would be valuable for the ml-engineering-foundations course.

---

## Additional Resources for Tutor Depth

> **8 sources** — papers, official docs, working code, benchmarks, and deep explainers that give the AI tutor precision on this topic.

### 📄 Bahdanau (Additive) Attention: Align + Translate
**Paper** · [source](https://iclr.cc/archive/www/lib/exe/fetch.php%3Fmedia=iclr2015:bahdanau-iclr2015.pdf)

*Additive alignment model + context integration into decoder (RNNsearch)*

<details>
<summary>Key content</summary>

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

</details>

### 📄 Transformer Attention (Scaled Dot-Product vs Additive; Multi-Head)
**Paper** · [source](https://proceedings.neurips.cc/paper_files/paper/2017/file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf)

*Exact equations + architectural procedure for scaled dot-product attention and multi-head attention; contrasts with additive (Bahdanau) attention and gives rationale.*

<details>
<summary>Key content</summary>

- **Attention definition (Section 3.2):** maps **query** and **key–value pairs** to an output; output is weighted sum of values; weights from a compatibility function between query and keys.
- **Scaled Dot-Product Attention (Eq. 1, Section 3.2.1):**  
  \[
  \text{Attention}(Q,K,V)=\text{softmax}\left(\frac{QK^\top}{\sqrt{d_k}}\right)V
  \]  
  where \(Q\) (queries), \(K\) (keys) have dimension \(d_k\); \(V\) (values) has dimension \(d_v\).
- **Rationale for scaling (Section 3.2.1, footnote 4):** if components of \(q,k\) are i.i.d. mean 0 var 1, then \(\mathrm{Var}(q\cdot k)=d_k\); large dot products push softmax into tiny-gradient regions → scale by \(1/\sqrt{d_k}\).
- **Additive vs dot-product (Section 3.2.1):** additive attention uses a 1-hidden-layer FFN for compatibility; similar theoretical complexity, but dot-product is faster/more space-efficient via matrix multiplies; additive can outperform **unscaled** dot-product for large \(d_k\).
- **Multi-Head Attention (Section 3.2.2):**  
  \[
  \text{MultiHead}(Q,K,V)=\text{Concat}(\text{head}_1,\dots,\text{head}_h)W^O
  \]
  \[
  \text{head}_i=\text{Attention}(QW_i^Q,KW_i^K,VW_i^V)
  \]
  with \(W_i^Q,W_i^K\in\mathbb{R}^{d_{model}\times d_k}\), \(W_i^V\in\mathbb{R}^{d_{model}\times d_v}\), \(W^O\in\mathbb{R}^{hd_v\times d_{model}}\). Default: \(h=8\), \(d_{model}=512\), \(d_k=d_v=64\).
- **Empirical (Table 3A):** single-head \(h=1\) gives **BLEU 24.9** vs base **25.8** (EN-DE dev); too many heads also drops (e.g., \(h=32\) → **25.4**).
- **Applications (Section 3.2.3):** encoder self-attn; decoder masked self-attn (mask illegal future positions by setting softmax inputs to \(-\infty\)); encoder–decoder attention (decoder queries attend to encoder keys/values).

</details>

### 📊 Luong et al. 2015 Attention (Global vs Local) + Scoring Ablations
**Benchmark** · [source](https://nlp.stanford.edu/pubs/emnlp15_attn.pdf)

*Canonical benchmark tables/ablations (global vs local; dot/general/concat scoring) with BLEU + speed/architecture tradeoffs*

<details>
<summary>Key content</summary>

- **Seq2seq objective (Eq. 1–4):**  
  \(\log p(y|x)=\sum_{j=1}^m \log p(y_j|y_{<j}, s)\). Decoder: \(p(y_j|y_{<j},s)=\text{softmax}(g(h_j))\); \(h_j=f(h_{j-1}, s)\). Train by minimizing \(J=\sum_{(x,y)\in D}-\log p(y|x)\).
- **Attention output layer (Eq. 5–6):** context \(c_t\) + decoder state \(h_t\) → attentional state  
  \(\tilde h_t=\tanh(W_c[c_t;h_t])\); \(p(y_t|y_{<t},x)=\text{softmax}(W_s\tilde h_t)\).
- **Global attention (Section 3.1, Eq. 7–8):** alignment weights over all source states \(\bar h_s\):  
  \(a_t(s)=\frac{\exp(\text{score}(h_t,\bar h_s))}{\sum_{s'}\exp(\text{score}(h_t,\bar h_{s'}))}\).  
  Scores: **dot** \(h_t^\top \bar h_s\); **general** \(h_t^\top W_a\bar h_s\); **concat** \(v_a^\top\tanh(W_a[h_t;\bar h_s])\). Location baseline: \(a_t=\text{softmax}(W_a h_t)\).
- **Local attention (Section 3.2, Eq. 9–10):** attend to window \([p_t-D,p_t+D]\), fixed \(a_t\in\mathbb{R}^{2D+1}\). Predictive center: \(p_t=S\cdot\sigma(v_p^\top\tanh(W_p h_t))\). Reweight with Gaussian: \(a_t(s)=\text{align}(h_t,\bar h_s)\exp(-(s-p_t)^2/(2\sigma^2))\), with \(\sigma=D/2\). Default **window** \(D=10\).
- **Input-feeding (Section 3.3):** feed \(\tilde h_t\) into next step input to model coverage-like dependence.
- **Training defaults (Section 4.1):** WMT’14 4.5M pairs; vocab 50K; filter length >50; 4-layer LSTM, 1000 cells/layer, 1000-d embeddings; SGD 10 epochs (dropout models 12); LR=1 then halve after epoch 5 (dropout: after 8); batch 128; grad clip norm 5; dropout \(p=0.2\). Speed: ~1K target words/s on Tesla K40; 7–10 days/train.
- **Key empirical results (Tables 1–4):**
  - **WMT’14 En→De (tokenized BLEU):** Base 11.3 → +reverse 12.6 (+1.3) → +dropout 14.0 (+1.4) → +global attn (location) 16.8 (+2.8) → +feed 18.1 (+1.3) → +local-p (general)+feed 19.0 (+0.9) → +unk replace 20.9 (+1.9) → **ensemble 8 + unk 23.0**.
  - **WMT’15 En→De (NIST BLEU):** **25.9** (ensemble 8 + unk) vs top WMT’15 NMT+5gram rerank 24.9.
  - **WMT’15 De→En (Table 3):** Base(reverse) 16.9; +global(location) 19.1 (+2.2); +feed 20.1 (+1.0); +global(dot)+drop+feed 22.8 (+2.7); +unk 24.9 (+2.1).
  - **Ablation insight (Table 4):** global(dot) 18.6 BLEU (20.5 after unk); local-p(general) best: 19.0 (20.9 after unk). Location yields weaker unk-replace gain (+1.2).

</details>

### 📊 Luong et al. 2015 Attention Variants + Benchmarks (WMT En↔De)
**Benchmark** · [source](https://aclanthology.org/anthology-files/pdf/D/D15/D15-1166.pdf)

*Benchmark tables comparing attention variants (global/local; dot/general/concat scoring) with BLEU on WMT tasks + speed/architecture tradeoffs.*

<details>
<summary>Key content</summary>

- **NMT objective (Eq. 1–4):**  
  \(\log p(y|x)=\sum_{j=1}^m \log p(y_j|y_{<j}, s)\) (Eq.1);  
  \(p(y_j|y_{<j},s)=\text{softmax}(g(h_j))\) (Eq.2); \(h_j=f(h_{j-1},s)\) (Eq.3); training minimizes \(J=\sum_{(x,y)\in D}-\log p(y|x)\) (Eq.4).
- **Attention output layer (Eq. 5–6):**  
  \(\tilde h_t=\tanh(W_c[c_t;h_t])\) (Eq.5); \(p(y_t|y_{<t},x)=\text{softmax}(W_s\tilde h_t)\) (Eq.6).
- **Global attention (Section 3.1, Eq. 7–9):**  
  \(a_t(s)=\frac{\exp(\text{score}(h_t,\bar h_s))}{\sum_{s'}\exp(\text{score}(h_t,\bar h_{s'}))}\) (Eq.7);  
  score options (Eq.8): dot \(h_t^\top \bar h_s\); general \(h_t^\top W_a\bar h_s\); concat \(W_a[h_t;\bar h_s]\).  
  Location baseline: \(a_t=\text{softmax}(W_a h_t)\) (Eq.9). Context \(c_t=\sum_s a_t(s)\bar h_s\).
- **Local attention (Section 3.2, Eq. 10–11):** attend to window \([p_t-D,p_t+D]\), \(a_t\in\mathbb{R}^{2D+1}\).  
  local-m: \(p_t=t\). local-p: \(p_t=S\cdot\sigma(v_p^\top\tanh(W_p h_t))\) (Eq.10); Gaussian bias: multiply by \(\exp(-(s-p_t)^2/(2\sigma^2))\), with \(\sigma=D/2\) (Eq.11).
- **Input-feeding (Section 3.3):** feed \(\tilde h_t\) as part of next-step input to model coverage-like behavior; deepens network horizontally/vertically.
- **Training defaults (Section 4.1):** WMT’14 4.5M pairs; vocab 50K each; filter length >50; 4-layer LSTM, 1000 cells/layer, 1000-d embeddings; SGD 10 epochs (LR=1, halve after epoch 5); batch 128; grad clip norm 5; init U[-0.1,0.1]; dropout variant trains 12 epochs, halve after epoch 8. Speed: ~1K target words/sec on Tesla K40; 7–10 days/model.
- **Key empirical results (Tables 1–4):**
  - En→De newstest2014 tokenized BLEU: Base+rev+dropout **14.0** → +global attn(location) **16.8** (+2.8) → +feed **18.1** (+1.3) → +local-p(general)+feed **19.0** (+0.9) → +unk replace **20.9** (+1.9). Ensemble 8 + unk: **23.0**.
  - WMT’15 En→De (Table 2, NIST BLEU): prior SOTA 24.9 vs **25.9** (ensemble 8 + unk).
  - De→En newstest2015 (Table 3): Base(reverse) 16.9 → +global(location) 19.1 (+2.2) → +feed 20.1 (+1.0) → +global(dot)+drop+feed 22.8 (+2.7) → +unk 24.9 (+2.1).
  - Attention scoring comparison (Table 4): global(dot) BLEU 18.6 (20.5 after unk); local-p(general) BLEU 19.0 (20.9 after unk). Location learns weaker alignments (smaller unk-replace gain).
- **Alignment quality (Table 6):** AER: global(location) 0.39; local-m(general) 0.34; local-p(general) 0.36; ensemble 0.34; Berkeley aligner 0.32.

</details>

### 📖 Bahdanau (Additive) Attention in TF NMT Tutorial
**Reference Doc** · [source](https://www.tensorflow.org/tutorials/text/nmt_with_attention?hl=ko)

*Official TensorFlow tutorial semantics for additive attention equations, tensor shapes, softmax axis choice, and masking in loss.*

<details>
<summary>Key content</summary>

- **Data preprocessing pipeline**
  - Normalize to ASCII, lowercase/strip; pad punctuation with spaces via regex; remove non `[a-zA-Z?.!,¿]`; add tokens: `"<start> ... <end>"`.
  - Tokenize with `tf.keras.preprocessing.text.Tokenizer(filters='')`; pad sequences `padding='post'`.
- **Dataset / batching defaults**
  - `num_examples=30000`; train/val split `test_size=0.2` → `24000` train, `6000` val.
  - `BATCH_SIZE=64`; example shapes: input `(64,16)`, target `(64,11)`.
  - Hyperparams: `embedding_dim=256`, `units=1024`; `steps_per_epoch=len(train)//64`.
- **Encoder (GRU) outputs**
  - Encoder returns `enc_output` shape `(batch, max_len, units)` and `enc_hidden` shape `(batch, units)`; example `(64,16,1024)` and `(64,1024)`.
- **Bahdanau attention (Eq. 1–3) with shapes**
  - **Eq. 1 (score):**  
    `score = V(tanh(W1(query_with_time_axis) + W2(values)))`  
    where `query` = decoder hidden state `(batch, hidden)`, `query_with_time_axis=expand_dims(query,1)` → `(batch,1,hidden)`, `values` = encoder outputs `(batch,max_len,hidden)`.  
    `score` shape `(batch,max_len,1)`.
  - **Eq. 2 (weights):** `attention_weights = softmax(score, axis=1)` (axis=1 because `max_len` is the alignment dimension).
  - **Eq. 3 (context):** `context_vector = sum(attention_weights * values, axis=1)` → `(batch, hidden)`.
- **Decoder step**
  - Embed input token `x` → `(batch,1,embed)`; concat with context: `concat([expand_dims(context,1), x], axis=-1)` → `(batch,1,embed+hidden)`; GRU; reshape output to `(batch, hidden)`; final logits via Dense to vocab. Example decoder output `(64, vocab_tar)` = `(64,4935)`.
- **Training procedure**
  - Teacher forcing loop over target timesteps; initial `dec_input` is `<start>` token repeated `BATCH_SIZE`.
  - Loss: `SparseCategoricalCrossentropy(from_logits=True, reduction='none')` with **padding mask** `real != 0`; multiply loss by mask; `reduce_mean`.
  - Optimizer: Adam; checkpoints every 2 epochs.
- **Inference**
  - No teacher forcing; stop when predicted token is `<end>`; store attention weights each step for plotting.

</details>

### 📖 TensorFlow/Keras Cross-Attention Wiring (Seq2Seq NMT)
**Reference Doc** · [source](https://www.tensorflow.org/text/tutorials/nmt_with_attention)

*Concrete TensorFlow/Keras attention wiring with explicit tensor shapes, masking behavior, and layer-call semantics (query/value, softmax location, context combination)*

<details>
<summary>Key content</summary>

- **Pipeline (data → training pairs):**
  - Standardize text: Unicode NFKD normalize → lowercase → regex keep `[^ a-z.?!,¿]` removed → space around punctuation → strip → add `[START] ... [END]`.
  - `TextVectorization(..., max_tokens=5000, ragged=True)` for context/target; convert to dense with `.to_tensor()` (0-padding).
  - Training pair transform: `targ_in = target[:, :-1]`, `targ_out = target[:, 1:]`; model inputs `((context, targ_in), targ_out)`.

- **Encoder (shapes):**
  - Embedding: `Embedding(vocab_size, units, mask_zero=True)`.
  - BiGRU: `Bidirectional(GRU(units, return_sequences=True), merge_mode='sum')`.
  - Input `(batch, s)` → output context `(batch, s, units)`. Default `UNITS=256`.

- **Cross-attention layer (Section “The attention layer”):**
  - Uses `tf.keras.layers.MultiHeadAttention(key_dim=units, num_heads=1)`.
  - Call: `attn_output, attn_scores = mha(query=x, value=context, return_attention_scores=True)`.
  - Shapes: query `x: (batch, t, units)`, value/context `(batch, s, units)`, scores `(batch, heads, t, s)` → mean over heads → `(batch, t, s)`.
  - **Softmax happens inside `MultiHeadAttention`**; attention weights sum to 1 over `s` for each `t`.
  - Residual + norm: `x = LayerNorm(x + attn_output)`; caches `last_attention_weights`.

- **Decoder (training call):**
  - Embedding → GRU (`return_sequences=True, return_state=True`) → attention with **RNN output as query** → Dense to logits.
  - Logits shape `(batch, t, target_vocab_size)`; loss uses `SparseCategoricalCrossentropy(from_logits=True)`.

- **Masking & metrics:**
  - Padding token id `0`; masked loss/accuracy multiply by `mask = (y_true != 0)` and normalize by `sum(mask)`.
  - Model deletes `logits._keras_mask` to prevent Keras scaling loss/accuracy.

- **Inference loop:**
  - Start token `[START]`; iterative `get_next_token` with optional `temperature` (0 → argmax; else sample).
  - `done` when `[END]`; once done, force next tokens to `0` padding.
  - Efficient graph mode: dynamic `for t in tf.range(max_length)` + `tf.TensorArray`.

</details>

### 🔍 Additive (Bahdanau) vs Multiplicative (Luong) Attention — PyTorch
**Explainer** · [source](https://tomekkorbak.com/2020/06/26/implementing-attention-in-pytorch/)

*Side-by-side additive (MLP) vs multiplicative (bilinear/dot) implementations, parameterization, and scaling tied to hidden sizes.*

<details>
<summary>Key content</summary>

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

</details>

### 📋 Seq2Seq Translation w/ Bahdanau (Additive) Attention (PyTorch)
**Code** · [source](https://docs.pytorch.org/tutorials/intermediate/seq2seq_translation_tutorial.html)

*End-to-end seq2seq+attention training loop w/ teacher forcing; explicit attention step order + tensor-shape-aware PyTorch code.*

<details>
<summary>Key content</summary>

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

</details>

---

## Related Topics

- [[topics/attention-mechanism|Attention Mechanism]]
- [[topics/neural-networks|Neural Networks]]
- [[topics/word-embeddings|Word Embeddings]]
