## Core Definitions

**Seq2seq bottleneck**: In a vanilla RNN encoder–decoder, the encoder must compress a variable-length input sequence into a *single fixed-dimensional* vector (often the final hidden state), and the decoder must generate the entire output sequence from that vector; this becomes infeasible for long sequences because the fixed-size representation cannot store all relevant information. *D2L* describes the encoder state as treated like a “sufficient statistic” of the input, which breaks down for long inputs, motivating attention. (https://d2l.ai/chapter_attention-mechanisms-and-transformers/bahdanau-attention.html)

**Attention mechanism**: Vaswani et al. define attention as mapping a **query** and a set of **key–value pairs** to an output, where the output is a weighted sum of the values and the weights come from a compatibility function between the query and keys. (https://proceedings.neurips.cc/paper_files/paper/2017/file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf)

**Encoder–decoder (cross-)attention**: A mechanism in which the decoder uses its current state (query) to compute weights over *all encoder hidden states* (keys/values) and forms a context vector as their weighted sum; this lets the decoder “look back” at the entire source sequence at each output step rather than relying on a single encoder summary. This is the core change introduced in Bahdanau et al.’s “soft alignment” model. (https://iclr.cc/archive/www/lib/exe/fetch.php%3Fmedia=iclr2015:bahdanau-iclr2015.pdf)

**Alignment scores / energies**: In Bahdanau attention, the decoder computes a scalar “energy” \(e_{ij}\) for each source position \(j\) when producing target token \(i\), using a learned function \(a(s_{i-1}, h_j)\) of the previous decoder state and the encoder annotation; these energies are normalized with softmax to produce attention weights \(\alpha_{ij}\). (https://iclr.cc/archive/www/lib/exe/fetch.php%3Fmedia=iclr2015:bahdanau-iclr2015.pdf)

**Bahdanau (additive) attention**: A differentiable “soft-search” alignment mechanism where the compatibility between decoder state and encoder states is computed by a small feedforward network (additive form), then softmaxed to produce weights used to compute a context vector as a weighted sum of encoder annotations; introduced to remove the fixed-length context bottleneck and improve long-sentence translation. (https://iclr.cc/archive/www/lib/exe/fetch.php%3Fmedia=iclr2015:bahdanau-iclr2015.pdf)

---

## Key Formulas & Empirical Results

### Bahdanau attention (paper equations)
From Bahdanau et al.:
- **Energy / score**: \[
e_{ij} = a(s_{i-1}, h_j)
\]
- **Attention weights**: \[
\alpha_{ij} = \frac{\exp(e_{ij})}{\sum_{k=1}^{T_x}\exp(e_{ik})}
\]
- **Context vector**: \[
c_i = \sum_{j=1}^{T_x}\alpha_{ij} h_j
\]
**Variables**: \(s_{i-1}\)=decoder hidden state before emitting \(y_i\); \(h_j\)=encoder annotation at source position \(j\); \(T_x\)=source length; \(c_i\)=context used for predicting \(y_i\).  
**Claim supported**: decoder can “soft-search” over all encoder states each step, avoiding a single fixed context vector. (https://iclr.cc/archive/www/lib/exe/fetch.php%3Fmedia=iclr2015:bahdanau-iclr2015.pdf)

### Additive attention (TensorFlow tutorial exact computation + shapes)
TensorFlow NMT tutorial implements additive attention as:
- **Score**: `score = V(tanh(W1(query_with_time_axis) + W2(values)))`
- **Weights**: `attention_weights = softmax(score, axis=1)`
- **Context**: `context_vector = sum(attention_weights * values, axis=1)`

**Shapes (TF tutorial)**:
- `query` (decoder hidden): `(batch, hidden)`
- `query_with_time_axis = expand_dims(query, 1)`: `(batch, 1, hidden)`
- `values` (encoder outputs): `(batch, max_len, hidden)`
- `score`: `(batch, max_len, 1)`
- `attention_weights`: `(batch, max_len, 1)` (softmax over `axis=1`, the source-length axis)
- `context_vector`: `(batch, hidden)` (sum over source positions)

**Claim supported**: attention distribution is normalized over encoder time steps; context is a weighted sum of encoder outputs. (https://www.tensorflow.org/tutorials/text/nmt_with_attention?hl=ko)

### Additive attention (PyTorch tutorial shapes)
PyTorch seq2seq tutorial uses:
- \( \text{score} = V_a(\tanh(W_a(\text{query}) + U_a(\text{keys}))) \)
- `weights = softmax(score, dim=-1)`
- `context = bmm(weights, keys)`

**Shapes (PyTorch tutorial)**:
- `query`: `[B,1,H]`
- `keys` (=encoder outputs): `[B,T,H]`
- `weights`: `[B,1,T]`
- `context`: `[B,1,H]`  
(https://docs.pytorch.org/tutorials/intermediate/seq2seq_translation_tutorial.html)

### Transformer scaled dot-product attention (contrast point)
Vaswani et al.:
\[
\text{Attention}(Q,K,V)=\text{softmax}\left(\frac{QK^\top}{\sqrt{d_k}}\right)V
\]
**Rationale for scaling**: if \(q,k\) components are i.i.d. mean 0 var 1, then \(\mathrm{Var}(q\cdot k)=d_k\); large dot products push softmax into small-gradient regions, so scale by \(1/\sqrt{d_k}\).  
**Claim supported**: dot-product attention is efficient via matrix multiplies; scaling stabilizes softmax. (https://proceedings.neurips.cc/paper_files/paper/2017/file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf)

### Implementation defaults students ask about (from tutorials)

**TensorFlow NMT with attention (selected defaults)**:
- `BATCH_SIZE=64`
- Example input shape `(64,16)`, target `(64,11)`
- `embedding_dim=256`, `units=1024`
- Encoder outputs: `enc_output (batch,max_len,units)` e.g. `(64,16,1024)`; `enc_hidden (batch,units)` e.g. `(64,1024)`
- Loss: `SparseCategoricalCrossentropy(from_logits=True, reduction='none')` with padding mask `real != 0`, then `reduce_mean`  
(https://www.tensorflow.org/tutorials/text/nmt_with_attention?hl=ko)

**PyTorch seq2seq translation tutorial (selected defaults/results)**:
- Filter `MAX_LENGTH=10`; after filtering `135842 → 11445` pairs
- Example hyperparams: `hidden_size=128`, `batch_size=32`, train `80` epochs; sample loss ~`0.0293` by epoch 80 (run-dependent)  
(https://docs.pytorch.org/tutorials/intermediate/seq2seq_translation_tutorial.html)

---

## How It Works

### A. What changes from vanilla seq2seq to Bahdanau attention (mechanically)
1. **Encode the source into a sequence of states**: run (often bidirectional) RNN over source tokens to produce annotations \(h_1,\dots,h_{T_x}\). (Bahdanau paper)  
2. **At each decoder step \(i\)**, instead of using a single fixed context:
   1) take the decoder’s previous hidden state \(s_{i-1}\) as the **query**  
   2) compute a score \(e_{ij}\) for *every* encoder state \(h_j\)  
   3) softmax over \(j\) to get weights \(\alpha_{ij}\) (a distribution over source positions)  
   4) compute context \(c_i=\sum_j \alpha_{ij} h_j\)  
   5) use \(c_i\) in the decoder update / output distribution \(p(y_i\mid y_{<i},x)=g(y_{i-1}, s_i, c_i)\) (Bahdanau paper)  
(https://iclr.cc/archive/www/lib/exe/fetch.php%3Fmedia=iclr2015:bahdanau-iclr2015.pdf)

### B. Additive attention step (TensorFlow tutorial: exact tensor operations)
Given:
- `values = enc_output` with shape `(B, S, H)` (S = source length)
- `query = dec_hidden` with shape `(B, H)`

Per decoding step:
1. `query_with_time_axis = expand_dims(query, 1)` → `(B,1,H)`
2. `score = V(tanh(W1(query_with_time_axis) + W2(values)))` → `(B,S,1)`
3. `attention_weights = softmax(score, axis=1)` → `(B,S,1)` (normalize across source positions)
4. `context_vector = sum(attention_weights * values, axis=1)` → `(B,H)`
5. Concatenate context with embedded decoder input token:
   - embed token `x` → `(B,1,E)`
   - `concat([expand_dims(context,1), x], axis=-1)` → `(B,1,E+H)`
6. Feed to GRU, project to vocab logits.  
(https://www.tensorflow.org/tutorials/text/nmt_with_attention?hl=ko)

### C. Additive attention step (PyTorch tutorial: exact order)
Per time step in the attention decoder:
1) embed input token (with dropout)  
2) compute `context, attn_weights` from `(query=hidden, encoder_outputs)`  
3) concat `embedded` and `context` → `[B,1,2H]`  
4) GRU step → output hidden  
5) linear → vocab distribution (tutorial uses `log_softmax`)  
(https://docs.pytorch.org/tutorials/intermediate/seq2seq_translation_tutorial.html)

---

## Teaching Approaches

### Intuitive (no math)
- Emphasize the *bottleneck*: vanilla seq2seq forces “everything about the source sentence” into one vector; attention replaces that with a per-output-step “glance” at the whole source sequence.  
- The decoder asks: “Which source words matter *right now*?” and forms a weighted average of encoder states to get a context vector for this step.  
Grounding: D2L’s description of fixed context failing on long sequences + Bahdanau’s “soft-search” motivation. (https://d2l.ai/chapter_attention-mechanisms-and-transformers/bahdanau-attention.html, https://iclr.cc/archive/www/lib/exe/fetch.php%3Fmedia=iclr2015:bahdanau-iclr2015.pdf)

### Technical (with math)
- Present the three-line core:
  1) \(e_{ij}=a(s_{i-1},h_j)\)  
  2) \(\alpha_{ij}=\text{softmax}_j(e_{ij})\)  
  3) \(c_i=\sum_j \alpha_{ij}h_j\)  
- Then connect to implementation: TF’s `softmax(score, axis=1)` because axis 1 is the source-length dimension; context is `sum(weights * values, axis=1)`.  
(https://iclr.cc/archive/www/lib/exe/fetch.php%3Fmedia=iclr2015:bahdanau-iclr2015.pdf, https://www.tensorflow.org/tutorials/text/nmt_with_attention?hl=ko)

### Analogy-based
- “Soft alignment” as a differentiable version of word alignment: for each target word, the model produces a probability distribution over source positions (not a single hard pointer), then blends the corresponding encoder states.  
- Use the term “soft alignment” explicitly (Bahdanau) to distinguish from hard/latent alignment.  
(https://iclr.cc/archive/www/lib/exe/fetch.php%3Fmedia=iclr2015:bahdanau-iclr2015.pdf)

---

## Common Misconceptions

1) **“Attention just picks one source token (like argmax), so it’s discrete.”**  
   - **Why wrong**: Bahdanau attention uses a **softmax distribution** \(\alpha_{ij}\) over *all* source positions and forms a **weighted sum** \(c_i=\sum_j \alpha_{ij}h_j\), explicitly designed to be differentiable (“soft alignment”).  
   - **Correct model**: attention is a *soft* mixture over encoder states; it can be peaked but is not inherently discrete.  
   (https://iclr.cc/archive/www/lib/exe/fetch.php%3Fmedia=iclr2015:bahdanau-iclr2015.pdf)

2) **“The encoder still only passes its last hidden state; attention is just extra features.”**  
   - **Why wrong**: the defining architectural change is that the decoder has access to **all encoder outputs** (`values` / `encoder_outputs`) and computes weights over the source-length dimension each step. TF tutorial: `values` has shape `(batch, max_len, units)` and softmax is over `axis=1` (max_len).  
   - **Correct model**: attention removes the single-vector bottleneck by exposing the full sequence of encoder states to the decoder.  
   (https://www.tensorflow.org/tutorials/text/nmt_with_attention?hl=ko)

3) **“Alignment scores are already probabilities; softmax is optional.”**  
   - **Why wrong**: Bahdanau defines energies \(e_{ij}\) and then *normalizes* them into \(\alpha_{ij}\) via softmax; without softmax, weights won’t sum to 1 and won’t behave like a distribution over source positions.  
   - **Correct model**: scores/energies are unnormalized compatibilities; softmax produces attention weights.  
   (https://iclr.cc/archive/www/lib/exe/fetch.php%3Fmedia=iclr2015:bahdanau-iclr2015.pdf)

4) **“Bahdanau attention is the same as Transformer attention.”**  
   - **Why wrong**: Bahdanau uses an **additive** compatibility function (a small feedforward network) \(a(s_{i-1},h_j)\). Transformers use **scaled dot-product** \(\text{softmax}(QK^\top/\sqrt{d_k})V\) and often multi-head projections.  
   - **Correct model**: both are “weighted sum of values,” but differ in the compatibility function and typical architecture (RNN encoder–decoder vs Transformer blocks).  
   (https://iclr.cc/archive/www/lib/exe/fetch.php%3Fmedia=iclr2015:bahdanau-iclr2015.pdf, https://proceedings.neurips.cc/paper_files/paper/2017/file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf)

5) **“Softmax axis doesn’t matter; it’s just normalization.”**  
   - **Why wrong**: In TF tutorial, softmax must be over the **source time dimension** (`axis=1` where `max_len` lives). Softmax over the wrong axis would normalize across batches or features, breaking the interpretation “weights over source positions.”  
   - **Correct model**: normalize across the alignment dimension (source positions \(j\)) for each decoder step.  
   (https://www.tensorflow.org/tutorials/text/nmt_with_attention?hl=ko)

---

## Worked Examples

### 1) Minimal additive (Bahdanau-style) attention in PyTorch (single step, runnable)
This mirrors the TF/PyTorch tutorial equations: score → softmax over source length → weighted sum.

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

torch.manual_seed(0)

B, S, H = 2, 5, 8  # batch, source length, hidden size

# "values" = encoder outputs (B, S, H)
values = torch.randn(B, S, H)

# "query" = decoder hidden state at current step (B, H)
query = torch.randn(B, H)

# Additive attention parameters (as in: v^T tanh(W1 q + W2 v))
W1 = nn.Linear(H, H, bias=False)
W2 = nn.Linear(H, H, bias=False)
V  = nn.Linear(H, 1, bias=False)

# 1) expand query to (B, 1, H) so it can broadcast across S
q = query.unsqueeze(1)  # (B,1,H)

# 2) score: (B,S,1)
score = V(torch.tanh(W1(q) + W2(values)))

# 3) weights over source positions: softmax across S
attn_weights = F.softmax(score, dim=1)  # (B,S,1)

# 4) context: weighted sum of values across S -> (B,H)
context = torch.sum(attn_weights * values, dim=1)

print("score:", score.shape)
print("attn_weights:", attn_weights.shape, "sum over S:", attn_weights.sum(dim=1).squeeze(-1))
print("context:", context.shape)
```

**What to point out while tutoring**
- `softmax(..., dim=1)` corresponds to TF tutorial’s `axis=1` (source length).  
- `attn_weights.sum(dim=1)` should be ~1 for each batch item (distribution over source positions).  
Grounding: TF tutorial shapes/axis choice; PyTorch tutorial’s score→softmax→context pattern. (https://www.tensorflow.org/tutorials/text/nmt_with_attention?hl=ko, https://docs.pytorch.org/tutorials/intermediate/seq2seq_translation_tutorial.html)

### 2) Decoder-step wiring (TensorFlow tutorial pattern, conceptual checklist)
When a student’s bug is “where does context go?” use this exact sequence from TF tutorial:
1. compute `context_vector` from `(dec_hidden, enc_output)`  
2. embed current input token  
3. concatenate `[context, embedded_token]` along feature dim  
4. feed to GRU → logits  
(https://www.tensorflow.org/tutorials/text/nmt_with_attention?hl=ko)

---

## Comparisons & Trade-offs

| Mechanism | Compatibility / score | Typical setting in sources | Pros | Cons / Notes |
|---|---|---|---|---|
| **Bahdanau (additive) attention** | \(e_{ij}=a(s_{i-1},h_j)\) via FFN; TF: `V(tanh(W1 q + W2 v))` | RNN encoder–decoder (NMT) | Addresses fixed-length bottleneck; works naturally with RNN hidden states | Less matrix-multiply-friendly than dot-product in Transformer context (contrast in Vaswani) |
| **Scaled dot-product attention (Transformer)** | \(\text{softmax}(QK^\top/\sqrt{d_k})V\) | Transformer encoder/decoder blocks | Fast and space-efficient via matmuls; scaling stabilizes softmax gradients | Different parameterization than additive; usually paired with multi-head projections |
| **Luong-style multiplicative variants (benchmark reference)** | dot / general / concat scoring (Luong et al.) | Attention-based NMT variants | Simpler scoring options; includes global vs local attention | Different placement/variants; details in Luong paper (not the focus here) |

**When to choose (within this lesson’s scope)**  
- Use **Bahdanau/additive** when explaining the historical breakthrough: it directly targets the seq2seq fixed-vector bottleneck and introduces soft alignment. (Bahdanau; D2L)  
- Use **scaled dot-product** when connecting “this idea became Transformers”: same weighted-sum pattern, different compatibility function and scaling rationale. (Vaswani)  
(https://iclr.cc/archive/www/lib/exe/fetch.php%3Fmedia=iclr2015:bahdanau-iclr2015.pdf, https://d2l.ai/chapter_attention-mechanisms-and-transformers/bahdanau-attention.html, https://proceedings.neurips.cc/paper_files/paper/2017/file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf)

---

## Prerequisite Connections

- **RNN encoder–decoder (seq2seq)**: needed to understand what the “fixed-length context vector” is and why it becomes a bottleneck. (D2L seq2seq + Bahdanau attention chapter context) (https://d2l.ai/chapter_recurrent-modern/seq2seq.html, https://d2l.ai/chapter_attention-mechanisms-and-transformers/bahdanau-attention.html)  
- **Softmax as normalization**: needed to interpret attention weights \(\alpha_{ij}\) as a distribution over source positions. (Bahdanau equations; TF tutorial softmax axis) (https://iclr.cc/archive/www/lib/exe/fetch.php%3Fmedia=iclr2015:bahdanau-iclr2015.pdf, https://www.tensorflow.org/tutorials/text/nmt_with_attention?hl=ko)  
- **Vector/matrix shapes & broadcasting**: needed to follow why `expand_dims(query,1)` is used and why softmax axis is the source-length dimension. (TF tutorial shapes) (https://www.tensorflow.org/tutorials/text/nmt_with_attention?hl=ko)  
- **Query/Key/Value framing**: needed to connect Bahdanau cross-attention to Transformer attention definition. (Vaswani definition) (https://proceedings.neurips.cc/paper_files/paper/2017/file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf)

---

## Socratic Question Bank

1) **If the encoder already produced a final hidden state, why isn’t that enough for long sentences?**  
Good answer: fixed-size vector bottleneck; information loss grows with length; attention avoids compressing everything into one vector. (D2L)

2) **At decoder step \(i\), what are we taking as the “query,” and what are the “values”?**  
Good answer: query is decoder hidden state (often \(s_{i-1}\) / current decoder state); values are encoder outputs \(h_j\). (Bahdanau; TF tutorial)

3) **What dimension must softmax normalize over to make attention weights meaningful, and why?**  
Good answer: over source positions \(j\) (TF: `axis=1` where `max_len` is), so weights sum to 1 across encoder time steps. (TF tutorial)

4) **What would break if we softmaxed over the hidden dimension instead of the source-length dimension?**  
Good answer: you’d normalize features, not positions; weights wouldn’t represent “which source token to attend to.” (TF tutorial shapes)

5) **What makes Bahdanau attention “additive”? Where is the nonlinearity?**  
Good answer: score uses FFN with tanh combining transformed query and value: `V(tanh(W1 q + W2 v))`. (TF tutorial; Bahdanau)

6) **How is Transformer attention’s compatibility function different, and why is there a \(\sqrt{d_k}\) term?**  
Good answer: dot-product \(QK^\top\) scaled by \(1/\sqrt{d_k}\) to prevent large magnitudes saturating softmax gradients. (Vaswani)

7) **Is attention a hard alignment? How does the model stay differentiable?**  
Good answer: softmax weights and weighted sum; “soft alignment” enables backprop. (Bahdanau)

8) **Where does the context vector go in the decoder computation in the TF tutorial?**  
Good answer: concatenated with embedded input token before GRU step. (TF tutorial)

---

## Likely Student Questions

**Q: What are the exact equations for Bahdanau attention?**  
→ **A:** Bahdanau defines \(e_{ij}=a(s_{i-1},h_j)\), \(\alpha_{ij}=\exp(e_{ij})/\sum_{k=1}^{T_x}\exp(e_{ik})\), and \(c_i=\sum_{j=1}^{T_x}\alpha_{ij}h_j\). (https://iclr.cc/archive/www/lib/exe/fetch.php%3Fmedia=iclr2015:bahdanau-iclr2015.pdf)

**Q: In TensorFlow’s additive attention tutorial, why is softmax applied with `axis=1`?**  
→ **A:** Because `axis=1` is the encoder time dimension `max_len` in `score` shaped `(batch, max_len, 1)`, so softmax normalizes across source positions to produce alignment weights. (https://www.tensorflow.org/tutorials/text/nmt_with_attention?hl=ko)

**Q: What are the tensor shapes for query/values/score/context in the TF tutorial?**  
→ **A:** `query` `(batch, hidden)`; `values` `(batch, max_len, hidden)`; `score` `(batch, max_len, 1)`; `attention_weights` `(batch, max_len, 1)`; `context_vector` `(batch, hidden)`. (https://www.tensorflow.org/tutorials/text/nmt_with_attention?hl=ko)

**Q: How does the decoder use the context vector in the TF tutorial?**  
→ **A:** It embeds the current input token `x` to `(batch,1,embed)`, expands context to `(batch,1,hidden)`, concatenates to `(batch,1,embed+hidden)`, then feeds that into the GRU before projecting to vocab logits. (https://www.tensorflow.org/tutorials/text/nmt_with_attention?hl=ko)

**Q: What’s the Transformer attention equation, and why the \(\sqrt{d_k}\) scaling?**  
→ **A:** \(\text{Attention}(Q,K,V)=\text{softmax}(QK^\top/\sqrt{d_k})V\). Vaswani et al. motivate scaling because \(\mathrm{Var}(q\cdot k)=d_k\) under i.i.d. assumptions; large dot products saturate softmax and shrink gradients. (https://proceedings.neurips.cc/paper_files/paper/2017/file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf)

**Q: What loss masking does the TF NMT tutorial use with padding?**  
→ **A:** `SparseCategoricalCrossentropy(from_logits=True, reduction='none')`; create mask `real != 0` (0 is padding), multiply per-token loss by mask, then `reduce_mean`. (https://www.tensorflow.org/tutorials/text/nmt_with_attention?hl=ko)

**Q: In the PyTorch seq2seq attention tutorial, what are the attention shapes?**  
→ **A:** `query` `[B,1,H]`, `keys` `[B,T,H]`, `weights` `[B,1,T]`, `context` `[B,1,H]` using `bmm(weights, keys)`. (https://docs.pytorch.org/tutorials/intermediate/seq2seq_translation_tutorial.html)

---

## Available Resources

### Videos
- [Attention in transformers, visually explained | Chapter 6, Deep Learning](https://youtube.com/watch?v=eMlx5fFNoYc) — Surface when: the student can’t picture what “weights over tokens” means or how Q/K/V produce a weighted sum.
- [The spelled-out intro to language modeling: building makemore](https://youtube.com/watch?v=PaCmpygFfXo) — Surface when: the student is shaky on RNN hidden states / why seq2seq uses an encoder and decoder.
- [Let’s build GPT: from scratch, in code, spelled out.](https://youtube.com/watch?v=kCc8FmEb1nY) — Surface when: the student wants the bridge from “attention idea” to modern Transformer implementation.

### Articles & Tutorials
- [Jay Alammar — The Illustrated Transformer](https://jalammar.github.io/illustrated-transformer/) — Surface when: the student needs a clear diagrammatic bridge from encoder–decoder attention to Transformer attention blocks.
- [Lilian Weng — “Attention? Attention!”](https://lilianweng.github.io/posts/2018-06-24-attention/) — Surface when: the student asks for taxonomy (additive vs dot-product, global vs local, self-attention) and historical progression.
- [Vaswani et al., 2017 — Attention Is All You Need](https://arxiv.org/abs/1706.03762) — Surface when: the student asks for the canonical Transformer equations/architecture reference.

---

## Visual Aids

![Attention: encoder passes all hidden states to decoder, not just the last. — Jay Alammar](/api/wiki-images/attention-mechanism/images/jalammar-visualizing-neural-machine-translation-mechanics-of-seq2seq-models-with_003.png)  
**Show when:** “What exactly changes in the architecture when we add attention?” or “What does it mean that the decoder can look at all encoder states?”

![Bahdanau additive attention: dynamic context from all encoder hidden states. (Bahdanau et al., 2015)](/api/wiki-images/attention-mechanism/images/lilianweng-posts-2018-06-24-attention_004.png)  
**Show when:** “Can you walk me through score → softmax → context vector?” step-by-step.

![Attention alignment matrix: French-to-English word correspondences learned automatically. (Bahdanau et al., 2015)](/api/wiki-images/attention-mechanism/images/lilianweng-posts-2018-06-24-attention_005.png)  
**Show when:** “Does attention learn interpretable alignments?” or “How does it handle reordering between languages?”

![AdditiveAttention output for 20-dim queries and 2-dim keys. (D2L.ai)](/api/wiki-images/attention-mechanism/images/d2l-ai-chapter_attention-mechanisms-and-transformers-attention-scoring-functions_006.svg)  
**Show when:** “Why use additive attention instead of dot product?” especially to emphasize it can handle differing query/key dimensions (as presented in D2L’s additive attention discussion).

---

## Key Sources

- [Neural Machine Translation by Jointly Learning to Align and Translate (Bahdanau et al., ICLR 2015)](https://iclr.cc/archive/www/lib/exe/fetch.php%3Fmedia=iclr2015:bahdanau-iclr2015.pdf) — Original additive attention / soft alignment equations and motivation (seq2seq bottleneck).
- [TensorFlow Tutorial: NMT with Attention](https://www.tensorflow.org/tutorials/text/nmt_with_attention?hl=ko) — Precise additive attention computation, tensor shapes, and masking/loss implementation details.
- [PyTorch Seq2Seq Translation Tutorial (with attention)](https://docs.pytorch.org/tutorials/intermediate/seq2seq_translation_tutorial.html) — End-to-end working attention seq2seq code with explicit step order and shapes.
- [Attention Is All You Need (Vaswani et al., 2017 PDF)](https://proceedings.neurips.cc/paper_files/paper/2017/file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf) — Canonical attention definition, scaled dot-product equation, and scaling rationale for the Transformer connection.
- [D2L: The Bahdanau Attention Mechanism](https://d2l.ai/chapter_attention-mechanisms-and-transformers/bahdanau-attention.html) — Clear statement of the fixed-length context bottleneck and why attention resolves it for long sequences.