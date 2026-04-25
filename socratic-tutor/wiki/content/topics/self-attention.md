---
title: "Self-Attention"
subject: "Sequence Models & Attention"
date: 2025-01-01
tags:
  - "subject/sequence-models-and-attention"
  - "level/beginner"
  - "level/intermediate"
  - "level/advanced"
  - "educator/3blue1brown"
  - "educator/jay-alammar"
  - "educator/lilian-weng"
  - "educator/andrej-karpathy"
  - "resource/video"
  - "resource/blog"
  - "resource/deep-dive"
  - "resource/paper"
  - "resource/code"
educators:
  - "3Blue1Brown"
  - "Jay Alammar"
  - "Lilian Weng"
  - "Andrej Karpathy"
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

# Self Attention

## Video (best)
- **3Blue1Brown** — "Attention in transformers, visually explained | 3Blue1Brown"
- **Watch:** [YouTube](https://www.youtube.com/watch?v=eMlx5fFNoYc)
- Why: Exceptional visual intuition for queries, keys, and values as geometric operations in embedding space. Builds understanding of scaled dot-product attention from first principles without assuming prior knowledge. The animation of attention weights as "which tokens attend to which" is the clearest visual treatment available for beginners.
- Level: beginner/intermediate

## Blog / Written explainer (best)
- **Jay Alammar** — "The Illustrated Transformer"
- **Link:** [https://jalammar.github.io/illustrated-transformer/](https://jalammar.github.io/illustrated-transformer/)
- Why: The definitive written explainer for self-attention. Step-by-step diagrams show exactly how Q, K, V matrices are computed, how dot products become attention weights via softmax, and how multi-head attention works. Widely used in university courses precisely because it makes the matrix math visually concrete. Covers causal masking in the decoder context.
- Level: beginner/intermediate

## Deep dive
- **Lilian Weng** — "Attention? Attention!"
- **Link:** [https://lilianweng.github.io/posts/2018-06-24-attention/](https://lilianweng.github.io/posts/2018-06-24-attention/)
- Why: Comprehensive technical survey tracing attention from its seq2seq origins through self-attention and Transformers. Covers the full mathematical formulation of scaled dot-product attention, multi-head variants, and positional encoding interactions. Ideal for readers who want to understand *why* each design choice was made, not just how to implement it.
- Level: intermediate/advanced

## Original paper
- **Vaswani et al.** — "Attention Is All You Need"
- **Link:** [https://arxiv.org/abs/1706.03762](https://arxiv.org/abs/1706.03762)
- Why: The seminal paper introducing the Transformer architecture and scaled dot-product self-attention. Section 3.2 ("Attention") is unusually readable for a research paper and directly defines the canonical Q/K/V formulation still used today. The scaling factor (1/√d_k) motivation is explained clearly in the paper itself.
- Level: intermediate/advanced

## Code walkthrough
- **Andrej Karpathy** — "Let's build GPT: from scratch, in code, spelled out"
- **Watch:** [YouTube](https://www.youtube.com/watch?v=kCc8FmEb1nY)
- Why: Karpathy implements self-attention (including causal masking) from scratch in ~100 lines of PyTorch, narrating every line. The progression from raw dot-products → scaled attention → masked attention → multi-head is the best available code-first treatment. Viewers see exactly why the triangular mask is applied and how attention weights are computed in practice. Paired with the nanoGPT repo for hands-on experimentation.
- Level: intermediate

## Coverage notes
- **Strong:** Visual/conceptual explanation of Q/K/V (3B1B video + Jay Alammar blog are both excellent and complementary). Mathematical formulation (Weng deep dive + original paper). From-scratch implementation (Karpathy).
- **Weak:** Efficient attention variants (Flash Attention, sparse attention) are not well covered by any of the above. Causal masking gets coverage in Karpathy but is underemphasized in the beginner resources.
- **Gap:** No single resource cleanly bridges the gap between the visual intuition (3B1B) and production-level implementation details (e.g., KV caching, memory layout). Advanced practitioners looking for hardware-aware attention implementations should consult the Flash Attention paper (arxiv.org/abs/2205.14135) separately.

---

## Additional Resources for Tutor Depth

> **7 sources** — papers, official docs, working code, benchmarks, and deep explainers that give the AI tutor precision on this topic.

### 📄 Luong (2015) Global vs. Local (Multiplicative) Attention
**Paper** · [source](https://aclanthology.org/D15-1166/)

*Exact Luong et al. (2015) equations for global/local attention: score functions (dot/general/concat), local predicted position \(p_t\), Gaussian windowing.*

<details>
<summary>Key content</summary>

- **Global attention (Section 3; Eq. for context):**  
  Given decoder state \(h_t\) and encoder states \(\{\bar h_s\}_{s=1}^S\):  
  \[
  a_t(s)=\mathrm{softmax}(\mathrm{score}(h_t,\bar h_s)),\quad
  c_t=\sum_{s=1}^S a_t(s)\,\bar h_s
  \]
  where \(a_t(s)\) are alignment weights, \(c_t\) is the context vector.
- **Score functions (multiplicative vs. concat):**
  - **dot:** \(\mathrm{score}(h_t,\bar h_s)=h_t^\top \bar h_s\)
  - **general (bilinear):** \(\mathrm{score}(h_t,\bar h_s)=h_t^\top W_a \bar h_s\)
  - **concat (additive-style):** \(\mathrm{score}(h_t,\bar h_s)=v_a^\top \tanh(W_a [h_t;\bar h_s])\)  
  Parameters: \(W_a\) (matrix), \(v_a\) (vector), \([\,;\,]\) concatenation.
- **Local attention (Section 3.1; predicted position + window):**
  - Predict aligned source position:
    \[
    p_t = S \cdot \sigma(v_p^\top \tanh(W_p h_t))
    \]
    where \(S\)=source length, \(\sigma\)=sigmoid, \(W_p, v_p\)=learned.
  - Attend only to a window around \(p_t\) (size \(2D+1\)); apply Gaussian bias:
    \[
    a_t(s)\propto \exp(\mathrm{score}(h_t,\bar h_s))\cdot
    \exp\!\left(-\frac{(s-p_t)^2}{2\sigma^2}\right)
    \]
    with \(\sigma = D/2\) (paper default), then normalize over \(s\in[p_t-D,\,p_t+D]\).
- **Design rationale:** global = full soft alignment (more compute); local = restrict to neighborhood for **computational efficiency** while keeping differentiable soft attention via Gaussian weighting.

</details>

### 📄 Luong (Multiplicative) Attention — Global & Local (2015)
**Paper** · [source](https://arxiv.org/pdf/1508.04025.pdf)

*Exact equations for global attention score functions + local attention (predictive \(p_t\) + Gaussian window) and training/inference details.*

<details>
<summary>Key content</summary>

- **Decoder objective (Eq. 1–4):**  
  \(\log p(\mathbf{y}|\mathbf{x})=\sum_{j=1}^m \log p(y_j|y_{<j},\mathbf{s})\) (Eq. 1);  
  \(p(y_j|y_{<j},\mathbf{s})=\text{softmax}(g(h_j))\) (Eq. 2); \(h_j=f(h_{j-1},\mathbf{s})\) (Eq. 3);  
  training loss \(J=\sum_{(x,y)\in D}-\log p(y|x)\) (Eq. 4).
- **Attention output layer (Eq. 5–6):**  
  \(\tilde h_t=\tanh(W_c[c_t;h_t])\) (Eq. 5);  
  \(p(y_t|y_{<t},x)=\text{softmax}(W_s\tilde h_t)\) (Eq. 6).
- **Global attention alignment (Eq. 7–8, Sec. 3.1):**  
  \(a_t(s)=\frac{\exp(\text{score}(h_t,\bar h_s))}{\sum_{s'}\exp(\text{score}(h_t,\bar h_{s'}))}\) (Eq. 7).  
  Score functions:  
  **dot:** \(\text{score}=h_t^\top \bar h_s\)  
  **general (bilinear):** \(\text{score}=h_t^\top W_a \bar h_s\)  
  **concat:** \(\text{score}=v_a^\top \tanh(W_a[h_t;\bar h_s])\)  
  Location baseline: \(a_t=\text{softmax}(W_a h_t)\) (Eq. 8).  
  Context: \(c_t=\sum_s a_t(s)\bar h_s\) (described after Eq. 7).
- **Local attention (Sec. 3.2):** window \([p_t-D,p_t+D]\), fixed \(a_t\in\mathbb{R}^{2D+1}\).  
  **local-m:** \(p_t=t\).  
  **local-p predictive position:** \(p_t=S\cdot \sigma(v_p^\top\tanh(W_p h_t))\) (Eq. 9), \(S=\) source length.  
  Gaussian bias: \(a_t(s)=\text{align}(h_t,\bar h_s)\exp\!\left(-\frac{(s-p_t)^2}{2\sigma^2}\right)\) (Eq. 10), with \(\sigma=D/2\).
- **Input-feeding (Sec. 3.3):** feed \(\tilde h_t\) as part of next-step input to model past alignment/coverage; if LSTM size \(n\), first-layer input becomes \(2n\).
- **Defaults / training (Sec. 4.1):** WMT’14 4.5M pairs; vocab top 50K each; filter length \(>50\); 4-layer LSTM, 1000 cells/layer, 1000-d embeddings; init \([-0.1,0.1]\); SGD 10 epochs (LR=1, halve after epoch 5); batch 128; clip/rescale grad norm \(>5\); dropout \(0.2\) (train 12 epochs, halve after epoch 8); local window \(D=10\).
- **Key results (Tables 1–4):** En→De: baseline+reverse+dropout BLEU 14.0; +global(location) 16.8; +feed 18.1; +local-p(general)+feed 19.0; +unk replace 20.9; ensemble(8)+unk 23.0 (tokenized BLEU, newstest2014). WMT’15 En→De: 25.9 NIST BLEU (Table 2). Architecture comparison (Table 4): global(dot) 18.6→20.5 after unk; local-p(general) best 19.0→20.9.

</details>

### 📊 Luong Attention (Global vs Local) + Scoring Functions (EMNLP’15)
**Benchmark** · [source](https://aclanthology.org/anthology-files/pdf/D/D15/D15-1166.pdf)

*Benchmark tables/ablations comparing global vs local attention + score functions; BLEU on WMT En↔De.*

<details>
<summary>Key content</summary>

- **Decoder with attention (Section 3):** given top-layer decoder state \(h_t\), compute context \(c_t\), then attentional state  
  \(\tilde{h}_t=\tanh(W_c[c_t;h_t])\) (Eq. 5), output \(p(y_t|y_{<t},x)=\text{softmax}(W_s\tilde{h}_t)\) (Eq. 6).
- **Global attention (Eq. 7–8):** alignment over all source states \(\bar{h}_s\):  
  \(a_t(s)=\frac{\exp(\text{score}(h_t,\bar{h}_s))}{\sum_{s'}\exp(\text{score}(h_t,\bar{h}_{s'}))}\).  
  Scores (Eq. 8): **dot** \(h_t^\top\bar{h}_s\); **general** \(h_t^\top W_a\bar{h}_s\); **concat** \(W_a[h_t;\bar{h}_s]\).  
  Location baseline: \(a_t=\text{softmax}(W_a h_t)\) (Eq. 9). Context \(c_t=\sum_s a_t(s)\bar{h}_s\).
- **Local attention (Section 3.2):** attend to window \([p_t-D,p_t+D]\), fixed \(a_t\in\mathbb{R}^{2D+1}\).  
  - **local-m:** \(p_t=t\).  
  - **local-p:** \(p_t=S\cdot\sigma(v_p^\top\tanh(W_p h_t))\) (Eq. 10); apply Gaussian bias  
    \(a_t(s)=\text{align}(h_t,\bar{h}_s)\exp(-(s-p_t)^2/(2\sigma^2))\), with \(\sigma=D/2\) (Eq. 11).
- **Input-feeding (Section 3.3):** feed \(\tilde{h}_t\) as part of next-step input to model coverage; if LSTM size \(n\), first-layer input becomes \(2n\).
- **Training defaults (Section 4.1):** WMT’14 4.5M pairs; vocab 50K each; filter length >50; 4-layer LSTM, 1000 cells/layer, 1000-d embeddings; SGD 10 epochs (dropout: 12); LR=1 then halve after epoch 5 (dropout: after 8); batch 128; grad clip norm 5; init U[-0.1,0.1].
- **Key En→De results (Table 1, tokenized BLEU newstest2014):**  
  Base 11.3; +reverse 12.6 (+1.3); +dropout 14.0 (+1.4); +global attn (location) 16.8 (+2.8); +feed 18.1 (+1.3); +local-p (general)+feed 19.0 (+0.9); +unk replace 20.9 (+1.9); ensemble(8)+unk 23.0.
- **WMT’15 En→De (Table 2, NIST BLEU newstest2015):** ensemble(8)+unk **25.9** vs prior SOTA 24.9.
- **De→En (Table 3, BLEU):** base(reverse) 16.9; +global(location) 19.1 (+2.2); +feed 20.1 (+1.0); +global(dot)+drop+feed 22.8 (+2.7); +unk 24.9 (+2.1).
- **Architecture ablation (Table 4):** global(dot) BLEU 18.6 (20.5 after unk); local-p(general) BLEU 19.0 (20.9 after unk). Location aligns poorly (smaller unk-replace gain: +1.2).
- **Alignment quality (Table 6, AER):** global(location) 0.39; local-m(general) 0.34; local-p(general) 0.36; ensemble 0.34; Berkeley aligner 0.32.

</details>

### 📋 # Source: https://www.tensorflow.org/addons/api_docs/python/tfa/seq2seq/LuongAttention
**Source** · 

### 📋 # Source: https://www.tensorflow.org/versions/r1.15/api_docs/python/tf/contrib/seq2seq/LuongMonotonicAttention
**Source** · 

### 🔍 Seq2Seq NMT pipeline (tokenization → encoder-decoder → decoding)
**Explainer** · [source](https://www.tensorflow.org/addons/tutorials/networks_seq2seq_nmt)

*End-to-end NMT workflow with concrete dataset formatting, masking rationale, shapes, training loop, and greedy decoding.*

<details>
<summary>Key content</summary>

- **Task/data:** English→Spanish sentence pairs (Anki dataset). Split: **118,964** total; **83,276** train; **17,844** val; **17,844** test.
- **Hyperparameters/defaults:** `BATCH_SIZE=64`, `EPOCHS=1` (note: “≥10 for convergence”), `MAX_SEQUENCE_LENGTH=40`, `ENG_VOCAB_SIZE=15000`, `SPA_VOCAB_SIZE=15000`, `EMBED_DIM=256`, `INTERMEDIATE_DIM=2048`, `NUM_HEADS=8`.
- **Special tokens:** `["[PAD]","[UNK]","[START]","[END]"]`. Spanish sequences get `[START]` and `[END]`; padding uses `[PAD]`.
- **Training data alignment (teacher forcing):**
  - Inputs dict: `encoder_inputs` = tokenized/padded English; `decoder_inputs` = Spanish tokens **excluding last** (`spa[:, :-1]`).
  - Targets: Spanish tokens **shifted left** (`spa[:, 1:]`).
  - Observed shapes for one batch: `encoder_inputs (64,40)`, `decoder_inputs (64,40)`, `targets (64,40)`.
- **Model procedure:**
  - Encoder: `TokenAndPositionEmbedding(vocab=15000, seq_len=40, dim=256)` → `TransformerEncoder(intermediate_dim=2048, num_heads=8)`.
  - Decoder: `TokenAndPositionEmbedding(...)` → `TransformerDecoder(intermediate_dim=2048, num_heads=8)` with **causal masking enabled by default** (prevents using future target tokens) → `Dropout(0.5)` → `Dense(15000, softmax)`.
- **Training setup/results:** `optimizer="rmsprop"`, `loss="sparse_categorical_crossentropy"`, metric `accuracy`. After **1 epoch**: train **accuracy 0.8385**, **loss 1.1014**; val **accuracy 0.8661**, **loss 0.8040**. Total params **14,449,304**.
- **Greedy decoding algorithm:** Start prompt = `[START]` + `[PAD]` to length 40; iteratively sample next token via `logits = transformer([encoder_input_tokens, prompt])[:, index-1, :]` until `[END]`.
- **Quant eval (ROUGE on 30 tests):** ROUGE-1 **P 0.3267 / R 0.3378 / F1 0.3207**; ROUGE-2 **P 0.0940 / R 0.1051 / F1 0.0966**. After **10 epochs**: ROUGE-1 **F1 0.579**, ROUGE-2 **F1 0.381**.

</details>

### 📋 TF Seq2Seq NMT w/ Attention (Encoder–Decoder + CrossAttention)
**Code** · [source](https://www.tensorflow.org/text/tutorials/nmt_with_attention)

*Runnable end-to-end NMT pipeline (Spanish→English) with explicit encoder/decoder + attention computation, training, inference, plotting, and export.*

<details>
<summary>Key content</summary>

- **Text preprocessing (inside model for SavedModel export):**
  - Standardize (Unicode NFKD) + lowercase + regex cleanup: keep `[^ a-z.?!,¿]`, space punctuation, add `[START] ... [END]`.
  - `TextVectorization(max_tokens=5000, ragged=True)` for both context/target; then `.to_tensor()` for 0-padding.
  - Training pair transform: `((context, targ_in), targ_out)` where `targ_in = target[:, :-1]`, `targ_out = target[:, 1:]`.
- **Model architecture + defaults:**
  - `UNITS = 256`, `BATCH_SIZE = 64`, train split ≈ 80%.
  - **Encoder:** `Embedding(vocab_size, units, mask_zero=True)` → `Bidirectional(GRU(units, return_sequences=True), merge_mode='sum')` → outputs `context` with shape `(batch, s, units)`.
  - **Attention (CrossAttention):** `MultiHeadAttention(num_heads=1, key_dim=units)` with `query=x` (decoder sequence), `value=context`; returns `attn_output` and `attn_scores` shaped `(batch, heads, t, s)` then averaged over heads → `(batch, t, s)`; residual add + `LayerNormalization`.
  - **Decoder:** `Embedding` → `GRU(units, return_sequences=True, return_state=True)` → `CrossAttention` → `Dense(vocab_size)` logits.
- **Training objective (Eq. 1 masked CE):**
  - Per-token loss: `CE(y_true, y_pred)` (SparseCategoricalCrossentropy, `from_logits=True`, `reduction='none'`).
  - Mask padding: `mask = 1[y_true != 0]`; final `loss = sum(CE*mask)/sum(mask)`.
  - Accuracy similarly masked after `argmax`.
  - Compile: `optimizer='adam'`, metrics `[masked_acc, masked_loss]`.
  - Expected initial metrics for uniform logits: `loss ≈ log(vocab_size)`, `acc ≈ 1/vocab_size`.
- **Inference loop (greedy or sampling):**
  - Initialize with `[START]`; step: run decoder on last token + state → logits.
  - If `temperature==0`: `next_token = argmax(logits)` else sample `categorical(logits/temperature)`.
  - Stop when `next_token == [END]`; force padding token `0` after done.
  - Cache attention weights each step for plotting.
- **Export + performance:**
  - Wrap `translate` in `@tf.function(input_signature=[TensorSpec(tf.string,[None])])`, save via `tf.saved_model.save`.
  - Dynamic loop variant uses `for t in tf.range(max_length)` + `TensorArray` to avoid static unrolling and allow early `break`.

</details>

---

## Related Topics

- [[topics/attention-mechanism|Attention Mechanism]]
- [[topics/multi-head-attention|Multi-Head Attention]]
- [[topics/transformer-architecture|Transformer Architecture]]
