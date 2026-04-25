## Core Definitions

**Recurrent Neural Network (RNN)**  
As Olah explains, an RNN is a neural network “with loops in them, allowing information to persist”; equivalently, it can be viewed as the same module applied repeatedly across time, passing a hidden state forward at each step (Olah, 2015). Jurafsky & Martin formalize the core recurrence as a hidden state update that depends on the previous hidden state and current input: \(h_t = g(Uh_{t-1} + Wx_t)\), with outputs computed from \(h_t\) (Jurafsky & Martin, 2019 draft).

**Hidden state (\(h_t\))**  
The hidden state is the RNN’s per-timestep vector summary of the sequence processed so far; it is updated recurrently and passed to the next timestep, enabling sequential dependence (Olah, 2015; Jurafsky & Martin, 2019 draft). In encoder–decoder setups, the encoder produces a sequence of hidden states (or annotations) that represent the input at each position (Bahdanau et al., 2015).

**Vanishing gradients (in RNN training)**  
Olah motivates LSTMs by the “problem of long-term dependencies,” where standard RNNs struggle to learn dependencies across many timesteps; a key practical symptom is that gradients propagated through many recurrent steps can become extremely small, making learning long-range effects difficult (Olah, 2015). (Use this definition operationally: “gradients shrink across many timesteps, so early tokens get little learning signal.”)

**Long Short-Term Memory (LSTM)**  
Olah describes LSTMs as a special kind of RNN module with a “cell state” and gating mechanisms that regulate what information is forgotten, written, and exposed as output at each timestep, enabling learning of longer-range dependencies than a “standard RNN repeating module” (Olah, 2015). Jurafsky & Martin note that in practice gated networks like LSTMs/GRUs are commonly used in place of simple RNNs (Jurafsky & Martin, 2019 draft).

**Gating mechanisms (LSTM/GRU gates)**  
In Olah’s framing, gates are sigmoid-controlled, elementwise “filters” that decide what information passes through; in LSTMs, multiple gates interact to control updates to the cell state and the hidden/output state (Olah, 2015). (Tutor shorthand: “sigmoid gates produce values in \([0,1]\) that scale information flow.”)

**Sequence-to-sequence (encoder–decoder) model**  
Jurafsky & Martin define encoder–decoder (seq2seq) networks as models that transform an input sequence into an output sequence of arbitrary length using an encoder that creates a contextual representation and a decoder that generates the output sequence (Jurafsky & Martin, 2019 draft). D2L emphasizes that encoder and decoder are often both RNNs; the decoder predicts tokens autoregressively, conditioned on the input representation and previously generated tokens (D2L, §10.7).

**Context vector bottleneck (classic seq2seq)**  
APXML highlights a limitation of early encoder–decoder RNNs: compressing the entire input sequence into a single fixed-size context vector creates an information bottleneck, especially for long sequences; earlier information can be overwritten/diluted as the encoder processes later tokens (APXML “Motivation: Overcoming Fixed-Length Context Vectors”). Alammar visualizes this as a single vector bridging encoder and decoder (Alammar).

**Attention mechanism (encoder–decoder attention)**  
Bahdanau et al. define attention (soft alignment) as computing, at each decoder step \(i\), a distribution \(\alpha_{ij}\) over encoder states \(h_j\) from alignment scores \(e_{ij}\), then forming a context vector \(c_i=\sum_j \alpha_{ij} h_j\) used by the decoder to predict the next token (Bahdanau et al., 2015). Vaswani et al. generalize attention as mapping queries and key–value pairs to an output that is a weighted sum of values, with weights from a compatibility function between query and keys (Vaswani et al., 2017).

**Bidirectional RNN (BiRNN)**  
APXML defines a BiRNN as two independent recurrent layers: a forward pass that summarizes past context and a backward pass that summarizes future context; their states are typically concatenated (or otherwise combined) to produce a representation that uses both left and right context (APXML “Understanding Bidirectional RNNs”). Bahdanau et al. use a bidirectional RNN encoder to produce annotations \(h_1,\dots,h_{T_x}\) (Bahdanau et al., 2015).

---

## Key Formulas & Empirical Results

### Core RNN recurrence (language modeling / generation framing)
Jurafsky & Martin (2019 draft) give:
\[
h_t = g(Uh_{t-1} + Wx_t), \quad y_t = f(Vh_t)
\]
- \(x_t\): input at timestep \(t\) (e.g., embedding)  
- \(h_t\): hidden state  
- \(U,W,V\): learned matrices  
- \(g\): nonlinearity (e.g., tanh/ReLU)  
- \(f\): output function (often softmax for classification)  
**Supports:** precise statement of what “hidden state update” means in a vanilla RNN.

### Bahdanau (additive) attention (scores → softmax → context)
Bahdanau et al. (2015):
\[
e_{ij} = a(s_{i-1}, h_j), \quad
\alpha_{ij} = \frac{\exp(e_{ij})}{\sum_{k=1}^{T_x}\exp(e_{ik})}, \quad
c_i = \sum_{j=1}^{T_x}\alpha_{ij} h_j
\]
- \(s_{i-1}\): decoder hidden state before emitting \(y_i\)  
- \(h_j\): encoder annotation at source position \(j\)  
- \(a(\cdot)\): feedforward network (“alignment model”)  
- \(c_i\): context vector for decoder step \(i\)  
**Supports:** why attention avoids a single fixed context vector; decoder “searches” source each step.

TensorFlow tutorial (additive attention) gives explicit implementation form and shapes (TF NMT tutorial):
- Score:
  `score = V(tanh(W1(query_with_time_axis) + W2(values)))`
- Softmax axis: `softmax(score, axis=1)` because axis 1 is `max_len` (alignment dimension).
- Context:
  `context_vector = sum(attention_weights * values, axis=1)`

### Luong attention: global vs local + scoring functions
Luong et al. (2015) / Stanford EMNLP’15 PDF:
- Global attention weights:
\[
a_t(s)=\frac{\exp(\text{score}(h_t,\bar h_s))}{\sum_{s'}\exp(\text{score}(h_t,\bar h_{s'}))}
\]
Score options:
- dot: \(h_t^\top \bar h_s\)
- general: \(h_t^\top W_a \bar h_s\)
- concat: \(v_a^\top \tanh(W_a [h_t;\bar h_s])\)

Local attention (predictive center):
\[
p_t = S\cdot\sigma(v_p^\top\tanh(W_p h_t))
\]
Gaussian bias (with \(\sigma=D/2\)):
\[
\exp\left(-\frac{(s-p_t)^2}{2\sigma^2}\right)
\]
Defaults from the paper notes: window \(D=10\) (Stanford EMNLP’15 PDF).

**Supports:** computational tradeoff (local attends to a window) and different compatibility functions.

### Scaled dot-product attention (Transformer)
Vaswani et al. (2017):
\[
\text{Attention}(Q,K,V)=\text{softmax}\left(\frac{QK^\top}{\sqrt{d_k}}\right)V
\]
- Scaling rationale: if components are i.i.d. mean 0 var 1, \(\mathrm{Var}(q\cdot k)=d_k\); large dot products push softmax into small-gradient regions → divide by \(\sqrt{d_k}\) (Vaswani et al., 2017).

### Empirical benchmarks (Luong et al. 2015, WMT)
From Luong et al. (2015) benchmark tables (WMT’14 En→De tokenized BLEU):
- Base+rev+dropout: **14.0**
- +global attention (location): **16.8** (+2.8)
- +input-feeding: **18.1** (+1.3)
- +local-p (general) + feed: **19.0** (+0.9)
- +unk replace: **20.9** (+1.9)
- Ensemble 8 + unk: **23.0**

Training defaults (Luong et al., 2015):
- 4-layer LSTM, 1000 cells/layer, 1000-d embeddings  
- Vocab 50K each; filter length > 50  
- SGD 10 epochs (LR=1; halve after epoch 5); batch 128  
- Gradient clip norm 5; init uniform \([-0.1,0.1]\)  
- Dropout \(p=0.2\) (dropout variant trains 12 epochs; halve after epoch 8)  
- Speed: ~1K target words/sec on Tesla K40; 7–10 days/model

**Supports:** attention improves BLEU; input-feeding helps; concrete hyperparameters students often ask for.

### Working implementation defaults (tutorials)
PyTorch seq2seq+attention tutorial (GRU-based):
- Filtered dataset: `MAX_LENGTH=10`; sentence-prefix filtering; pairs reduced `135842 → 11445`
- Vocab sizes: French `4601`, English `2991`; `SOS=0`, `EOS=1`
- Example hyperparams: `hidden_size=128`, `batch_size=32`, train `80` epochs; Adam lr `0.001`
- Attention shapes: `keys=[B,T,H]`, `query=[B,1,H]`, `weights=[B,1,T]`, `context=[B,1,H]`

TensorFlow NMT tutorial:
- `embedding_dim=256`, `units=1024`, `BATCH_SIZE=64`
- Loss masking: multiply per-token loss by mask `(real != 0)` then mean

---

## How It Works

### A. Vanilla RNN forward pass (mechanics)
1. **Embed/prepare input** \(x_t\) (e.g., word embedding).
2. **Update hidden state** using recurrence (Jurafsky & Martin):
   \[
   h_t = g(Uh_{t-1} + Wx_t)
   \]
3. **Compute output** (e.g., logits then softmax):
   \[
   y_t = f(Vh_t)
   \]
4. Repeat for \(t=1\ldots T\). Unrolling the loop yields a chain of repeated modules sharing parameters (Olah).

### B. Seq2seq (encoder–decoder) with RNNs (no attention)
(Use D2L + Jurafsky & Martin framing.)
1. **Encoder** reads input tokens sequentially, producing hidden states; classic design often uses the **final** encoder hidden state as a fixed-size “context vector” passed to the decoder (APXML motivation; Alammar visualization).
2. **Decoder** generates output tokens autoregressively: at each step, predict next token conditioned on previous outputs and the encoder-provided context (D2L; Jurafsky & Martin).
3. **Training** commonly uses **teacher forcing**: feed the ground-truth previous target token as the next decoder input (D2L; TF and PyTorch tutorials show explicit loops).

### C. Seq2seq with additive (Bahdanau) attention (per decoding step)
At decoder step \(i\) (Bahdanau et al.; TF/PyTorch tutorials):
1. **Query** = current/previous decoder hidden state (TF: `query` shape `(batch, hidden)`; PyTorch: `query` `(B,1,H)`).
2. **Keys/values** = all encoder outputs (TF: `values` `(batch, max_len, hidden)`; PyTorch: `keys` `[B,T,H]`).
3. **Compute scores** (additive):
   - TF form: `score = V(tanh(W1(query) + W2(values)))` producing `(batch, max_len, 1)`.
4. **Normalize** with softmax over source positions:
   - TF: `softmax(score, axis=1)` (axis is the source-length dimension).
5. **Context vector** = weighted sum of encoder outputs:
   - TF: `sum(attention_weights * values, axis=1)` → `(batch, hidden)`
   - PyTorch: `context = bmm(weights, keys)` → `[B,1,H]`
6. **Combine context with decoder input/state**:
   - TF tutorial: concatenate context with embedded decoder input token before GRU step.
   - PyTorch tutorial: concat `embedded` and `context` → feed to GRU.
7. **Project to vocab** to get logits/probabilities for next token.

### D. Luong attention variants (global vs local) in decoding
1. Compute alignment weights over **all** source states (global) or a **window** around a predicted center \(p_t\) (local) (Luong et al., 2015).
2. Score function choices: dot/general/concat (Luong et al., Eq. 7–8).
3. Context \(c_t\) is weighted sum of encoder states; attentional hidden state:
   \[
   \tilde h_t=\tanh(W_c[c_t;h_t])
   \]
   then softmax over vocab (Luong et al., Eq. 5–6).
4. Optional **input-feeding**: feed \(\tilde h_t\) into the next timestep input (Luong et al., Section 3.3).

---

## Teaching Approaches

### Intuitive (no math): “state as memory; attention as looking back”
- RNN: a running “summary” (hidden state) that updates as you read tokens (Olah; Alammar).
- Problem: forcing the whole input into one summary vector is a bottleneck for long sequences (APXML motivation).
- Attention: instead of relying on one summary, the decoder can “look back” at all encoder states and pick what matters right now (Bahdanau; APXML).

### Technical (with math): “compatibility → softmax distribution → weighted sum”
- Define encoder states \(h_j\), decoder state \(s_{i-1}\).
- Compute energies \(e_{ij}=a(s_{i-1},h_j)\), normalize to \(\alpha_{ij}\), compute \(c_i=\sum_j \alpha_{ij}h_j\) (Bahdanau).
- Emphasize softmax axis: normalize across source positions (TF tutorial: `axis=1`).

### Analogy-based: “compression vs retrieval”
- Classic seq2seq: compress a whole document into one fixed-size vector (APXML: bottleneck).
- Attention: keep an “index” of all intermediate notes (encoder states) and retrieve a custom summary each time you write the next word (Bahdanau; Alammar visualization).

---

## Common Misconceptions

1. **“The hidden state is the same as the output.”**  
   **Why wrong:** Jurafsky & Martin separate hidden update \(h_t\) from output \(y_t=f(Vh_t)\); hidden state is an internal representation, output is a function of it.  
   **Correct model:** \(h_t\) is the recurrent memory passed forward; \(y_t\) is what you expose (e.g., logits/softmax) derived from \(h_t\).

2. **“Seq2seq always uses a single context vector; attention is optional decoration.”**  
   **Why wrong:** APXML explicitly frames the single fixed-size context vector as a bottleneck; Bahdanau’s model replaces reliance on a single vector with per-step context \(c_i\) computed from all encoder states.  
   **Correct model:** Without attention, decoder depends heavily on a fixed summary; with attention, decoder computes a *different* context vector each step via \(\alpha_{ij}\) and \(c_i\).

3. **“Attention weights are computed once for the whole output sequence.”**  
   **Why wrong:** Bahdanau defines \(\alpha_{ij}\) per decoder step \(i\); TF tutorial stores attention weights each decoding step for plotting.  
   **Correct model:** For each output timestep \(i\), compute a fresh distribution over source positions \(j\).

4. **“Softmax axis doesn’t matter; it’s just normalization.”**  
   **Why wrong:** TF tutorial is explicit: `softmax(score, axis=1)` because axis 1 corresponds to `max_len` (source positions). Normalizing over the wrong axis changes the meaning (you’d normalize across batch or features instead of source positions).  
   **Correct model:** Normalize across the dimension representing the set you’re choosing among (source tokens for alignment).

5. **“Luong attention and Bahdanau attention are the same thing with different names.”**  
   **Why wrong:** The sources distinguish additive (Bahdanau) scoring via an MLP vs multiplicative (Luong) dot/bilinear scoring; Luong also introduces global vs local attention and input-feeding (Luong et al.; Tomek Korbak comparison card).  
   **Correct model:** They share the same *pattern* (scores → softmax → weighted sum) but differ in score parameterization and (often) decoder wiring.

---

## Worked Examples

### 1) PyTorch: one Bahdanau attention step (shape-checked, matches tutorial)
Based on the PyTorch seq2seq translation tutorial’s attention equations and shapes.

```python
import torch
import torch.nn.functional as F

B, T, H = 2, 5, 8  # batch, source length, hidden size

# Encoder outputs are keys/values: [B, T, H]
keys = torch.randn(B, T, H)

# Decoder hidden state as query: tutorial uses [1,B,H] then permutes to [B,1,H]
hidden = torch.randn(1, B, H)
query = hidden.permute(1, 0, 2)  # [B, 1, H]

# Simple additive attention parameterization (tutorial form):
Wa = torch.nn.Linear(H, H, bias=False)
Ua = torch.nn.Linear(H, H, bias=False)
Va = torch.nn.Linear(H, 1, bias=False)

# Score: Va(tanh(Wa(query) + Ua(keys))) -> [B, T, 1] then transpose to [B, 1, T]
score = Va(torch.tanh(Wa(query) + Ua(keys)))      # broadcast query over T
weights = F.softmax(score.transpose(1, 2), dim=-1)  # [B, 1, T]

# Context: bmm([B,1,T], [B,T,H]) -> [B,1,H]
context = torch.bmm(weights, keys)

print("weights", weights.shape, "context", context.shape)
```

**What to point out mid-tutoring (from the tutorial):**
- `weights` sums to 1 over `T` (source positions) because softmax is over the last dim `T`.
- `context` is a weighted average of encoder outputs; it’s what you concatenate with the embedded decoder input before the GRU step (PyTorch tutorial’s step order).

### 2) TensorFlow: why `axis=1` in additive attention softmax
From TF NMT tutorial: `score` has shape `(batch, max_len, 1)`. The alignment dimension is `max_len`, so:
- `softmax(score, axis=1)` normalizes across source positions.
- If you used `axis=-1`, you’d normalize across the trailing singleton dimension (degenerate).

---

## Comparisons & Trade-offs

| Concept | Variant | Core computation | Pros | Cons / When it breaks | Source |
|---|---|---|---|---|---|
| RNN cell | Vanilla RNN | \(h_t=g(Uh_{t-1}+Wx_t)\) | Simple | Struggles with long-term dependencies (motivation for LSTM) | Jurafsky & Martin; Olah |
| Gated RNN | LSTM | Cell state + gates controlling write/forget/output | Better long-range learning in practice | More complex than vanilla | Olah; Jurafsky & Martin |
| Attention scoring | Additive (Bahdanau) | MLP: \(v^\top\tanh(W_1h + W_2s)\) | Flexible when dims differ; classic NMT | More parameters than dot | Bahdanau; Tomek Korbak; TF tutorial |
| Attention scoring | Multiplicative (Luong) | dot / bilinear \(h^\top Ws\) | Computationally simpler; matrix mult friendly | Needs scaling for large dims (Transformer note) | Luong; Tomek Korbak; Vaswani |
| Attention scope | Global | attend over all source positions | Best alignment flexibility | More compute for long sources | Luong |
| Attention scope | Local | attend over window around \(p_t\) | Cheaper; focused | Must predict center; may miss far tokens | Luong |
| Decoder wiring | Input-feeding | feed \(\tilde h_t\) into next step input | Improves BLEU in Luong results | Adds recurrence depth | Luong |

**When to choose (from sources):**
- Use **attention** when fixed-length context is a bottleneck for long sequences (APXML; Bahdanau).
- Use **local attention** when you want cheaper attention by restricting to a window (Luong).
- Use **scaled dot-product** when using dot products at larger dimensions to avoid softmax saturation (Vaswani).

---

## Prerequisite Connections

- **Vector embeddings / representing tokens as vectors**: Alammar’s seq2seq walkthrough assumes words are embedded before entering the RNN encoder.  
- **Softmax as a distribution**: Attention weights \(\alpha_{ij}\) are a softmax distribution over source positions (Bahdanau; TF tutorial).  
- **Autoregressive decoding**: Decoder predicts next token conditioned on previous tokens; teacher forcing during training (D2L; TF/PyTorch tutorials).  
- **Matrix shapes / batch dimensions**: Implementations hinge on understanding `(batch, time, hidden)` vs `(batch, hidden)` and correct softmax axis (TF tutorial; PyTorch tutorial).

---

## Socratic Question Bank

1. **If an RNN’s hidden state is a “summary,” what information might get lost as sequences get longer?**  
   *Good answer:* Mentions bottleneck/overwriting; earlier info diluted (APXML motivation).

2. **In Bahdanau attention, what set does the softmax normalize over, and why?**  
   *Good answer:* Over source positions \(j\) for a fixed decoder step \(i\); yields alignment distribution (Bahdanau; TF axis=1 note).

3. **What changes between global and local attention in Luong’s formulation?**  
   *Good answer:* Global attends over all encoder states; local attends to a window around \(p_t\) (Luong).

4. **Why might dot-product attention need scaling by \(\sqrt{d_k}\)?**  
   *Good answer:* Large dot products at high dimension saturate softmax; scaling controls variance (Vaswani).

5. **In seq2seq decoding, what’s the difference between training with teacher forcing and inference?**  
   *Good answer:* Training feeds ground-truth previous token; inference feeds model’s own previous prediction (TF tutorial; D2L).

6. **What are “keys/values” vs “queries” in encoder–decoder attention terms?**  
   *Good answer:* Encoder outputs are keys/values; decoder hidden state is query (TF tutorial; Vaswani definition).

7. **If you normalized attention scores over the hidden dimension instead of time, what would the weights represent?**  
   *Good answer:* They wouldn’t represent a distribution over source tokens; would be meaningless for alignment (TF axis discussion).

8. **What does input-feeding add conceptually?**  
   *Good answer:* Feeds attentional state \(\tilde h_t\) into next step input to encourage coverage-like behavior (Luong).

---

## Likely Student Questions

**Q: What’s the exact equation for Bahdanau attention?**  
→ **A:** Bahdanau et al. define \(e_{ij}=a(s_{i-1},h_j)\), \(\alpha_{ij}=\frac{\exp(e_{ij})}{\sum_k \exp(e_{ik})}\), and \(c_i=\sum_j \alpha_{ij}h_j\), where \(h_j\) are encoder annotations and \(s_{i-1}\) is the decoder state (https://iclr.cc/archive/www/lib/exe/fetch.php%3Fmedia=iclr2015:bahdanau-iclr2015.pdf).

**Q: In TensorFlow’s additive attention tutorial, why is softmax over `axis=1`?**  
→ **A:** Because `score` has shape `(batch, max_len, 1)` and `max_len` (axis 1) indexes source positions; softmax over axis 1 produces attention weights that sum to 1 across the source sequence (https://www.tensorflow.org/tutorials/text/nmt_with_attention?hl=ko).

**Q: How do Luong’s dot/general/concat scoring functions differ?**  
→ **A:** Luong et al. define score options: dot \(h_t^\top \bar h_s\), general \(h_t^\top W_a \bar h_s\), concat \(v_a^\top\tanh(W_a[h_t;\bar h_s])\) (https://nlp.stanford.edu/pubs/emnlp15_attn.pdf).

**Q: What’s the difference between global and local attention in Luong et al. (2015)?**  
→ **A:** Global attention computes weights over all source positions; local attention predicts a center \(p_t=S\cdot\sigma(v_p^\top\tanh(W_p h_t))\) and attends only to a window \([p_t-D,p_t+D]\), optionally with a Gaussian bias (https://nlp.stanford.edu/pubs/emnlp15_attn.pdf).

**Q: What is “input-feeding” and why use it?**  
→ **A:** Luong et al. feed the attentional hidden state \(\tilde h_t\) into the next timestep’s input, which they describe as encouraging coverage-like behavior and improving results in their experiments (https://nlp.stanford.edu/pubs/emnlp15_attn.pdf).

**Q: Why does Transformer attention divide by \(\sqrt{d_k}\)?**  
→ **A:** Vaswani et al. explain that dot products grow in variance with \(d_k\), pushing softmax into regions with tiny gradients; scaling by \(1/\sqrt{d_k}\) controls magnitude (https://proceedings.neurips.cc/paper_files/paper/2017/file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf).

**Q: What concrete BLEU gains did attention give in Luong et al. (2015)?**  
→ **A:** On WMT’14 En→De tokenized BLEU, Base+rev+dropout is 14.0; adding global attention (location) gives 16.8; adding input-feeding gives 18.1; local-p (general)+feed gives 19.0; unk replace gives 20.9; ensemble 8 + unk gives 23.0 (https://aclanthology.org/anthology-files/pdf/D/D15/D15-1166.pdf).

**Q: What are the key training hyperparameters in Luong et al. (2015)?**  
→ **A:** 4-layer LSTM with 1000 cells/layer, 1000-d embeddings; SGD for 10 epochs with LR=1 halved after epoch 5; batch 128; gradient clip norm 5; init U[-0.1,0.1]; dropout \(p=0.2\) in dropout variant (https://nlp.stanford.edu/pubs/emnlp15_attn.pdf).

---

## Available Resources

### Videos
- [The spelled-out intro to language modeling: building makemore (Karpathy)](https://youtube.com/watch?v=PaCmpygFfXo) — Surface when: student asks how hidden state + BPTT works in practice for language modeling, or wants a from-scratch RNN training walkthrough.

### Articles & Tutorials
- [Understanding LSTM Networks (Olah, 2015)](https://colah.github.io/posts/2015-08-Understanding-LSTMs/) — Surface when: student is confused about what gates do, or why LSTMs help with long-term dependencies.
- [Attention Is All You Need (Vaswani et al., 2017)](https://arxiv.org/html/1706.03762v7) — Surface when: student asks about scaled dot-product attention, \(\sqrt{d_k}\) scaling, or multi-head definitions.
- [Bahdanau et al. 2015 (RNNsearch)](https://iclr.cc/archive/www/lib/exe/fetch.php%3Fmedia=iclr2015:bahdanau-iclr2015.pdf) — Surface when: student wants the original additive attention equations and the “fixed-length bottleneck” motivation.
- [Luong et al. 2015 Attention (EMNLP PDF)](https://nlp.stanford.edu/pubs/emnlp15_attn.pdf) — Surface when: student asks global vs local attention, dot/general/concat scoring, or input-feeding.
- [TensorFlow NMT with attention tutorial](https://www.tensorflow.org/tutorials/text/nmt_with_attention?hl=ko) — Surface when: student asks about tensor shapes, softmax axis, masking, or teacher forcing in TF.
- [PyTorch seq2seq translation tutorial](https://docs.pytorch.org/tutorials/intermediate/seq2seq_translation_tutorial.html) — Surface when: student wants an end-to-end runnable implementation with attention and teacher forcing.
- [Visualizing NMT with attention (Alammar)](https://jalammar.github.io/visualizing-neural-machine-translation-mechanics-of-seq2seq-models-with-attention/) — Surface when: student needs an intuition for encoder/decoder roles and the context vector bottleneck.
- [D2L: Sequence-to-Sequence Learning for MT](https://d2l.ai/chapter_recurrent-modern/seq2seq.html) — Surface when: student asks about teacher forcing vs inference behavior in seq2seq.

---

## Visual Aids

![Rolled RNN: module A recurrently passes hidden state h_t. (Olah, 2015)](/api/wiki-images/rnns-lstms/images/colah-posts-2015-08-Understanding-LSTMs_001.png)  
Show when: introducing “what makes an RNN recurrent?” and what the loop carries (hidden state).

![Standard RNN repeating module: a single tanh layer per time step. (Olah, 2015)](/api/wiki-images/rnns-lstms/images/colah-posts-2015-08-Understanding-LSTMs_005.png)  
Show when: contrasting vanilla RNN cell simplicity before motivating LSTM complexity.

![LSTM chain: four interacting layers per module enable long-term memory. (Olah, 2015)](/api/wiki-images/rnns-lstms/images/colah-posts-2015-08-Understanding-LSTMs_006.png)  
Show when: student asks “what’s inside an LSTM cell?” at a high level.

![LSTM cell state update: forget old info, add new candidate values. (Olah, 2015)](/api/wiki-images/rnns-lstms/images/colah-posts-2015-08-Understanding-LSTMs_012.png)  
Show when: explaining how forget + input gates jointly update the cell state.

![LSTM output gate: sigmoid filters cell state through tanh to produce h_t. (Olah, 2015)](/api/wiki-images/rnns-lstms/images/colah-posts-2015-08-Understanding-LSTMs_013.png)  
Show when: clarifying difference between cell state and hidden/output state; “what gets passed on?”

![GRU: two gates and merged cell/hidden state simplify the LSTM. (Olah, 2015)](/api/wiki-images/rnns-lstms/images/colah-posts-2015-08-Understanding-LSTMs_016.png)  
Show when: student asks how GRU relates to LSTM (simplification; fewer gates).

![Context vector (size 4) bridges encoder and decoder in seq2seq. — Jay Alammar](/api/wiki-images/rnns-lstms/images/jalammar-visualizing-neural-machine-translation-mechanics-of-seq2seq-models-with_001.png)  
Show when: motivating attention via the fixed-length context bottleneck.

![Word embeddings feed into RNN steps, updating hidden states sequentially. — Jay Alammar](/api/wiki-images/rnns-lstms/images/jalammar-visualizing-neural-machine-translation-mechanics-of-seq2seq-models-with_002.png)  
Show when: student is shaky on how tokens become vectors and enter the encoder timestep-by-timestep.

---

## Key Sources

- [Understanding LSTM Networks (Olah, 2015)](https://colah.github.io/posts/2015-08-Understanding-LSTMs/) — clearest pedagogical reference for RNN unrolling and LSTM gating intuition/structure.
- [Bahdanau et al. 2015: Neural Machine Translation by Jointly Learning to Align and Translate](https://iclr.cc/archive/www/lib/exe/fetch.php%3Fmedia=iclr2015:bahdanau-iclr2015.pdf) — original additive attention equations (energies → softmax → context) and bottleneck motivation.
- [Luong et al. 2015 (EMNLP): Effective Approaches to Attention-based NMT](https://nlp.stanford.edu/pubs/emnlp15_attn.pdf) — global vs local attention, dot/general/concat scoring, input-feeding, and concrete WMT hyperparameters/results.
- [TensorFlow NMT with attention tutorial](https://www.tensorflow.org/tutorials/text/nmt_with_attention?hl=ko) — implementation-grounded tensor shapes, softmax axis choice, masking, and teacher forcing loop.
- [Attention Is All You Need (Vaswani et al., 2017)](https://proceedings.neurips.cc/paper_files/paper/2017/file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf) — definitive formula and rationale for scaled dot-product attention (\(/\sqrt{d_k}\)).