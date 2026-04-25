## Core Definitions

**Self-attention**  
Vaswani et al. define attention as mapping a query and a set of key–value pairs to an output, where the output is a weighted sum of the values and the weights come from a compatibility function of query with each key (“scaled dot-product attention” in the Transformer) ([Attention Is All You Need](https://arxiv.org/html/1706.03762v7)). In *self*-attention, the queries, keys, and values are all derived from the same sequence, so each token computes an input-dependent mixture of information from all tokens (including itself).

**Queries, Keys, Values (Q/K/V)**  
Brenndörfer motivates Q/K/V as a “separation of concerns”: a token uses a **query** to express what it needs, a **key** to advertise what it offers, and a **value** to provide the content that will be aggregated; attention weights are computed by matching queries to keys, then used to combine values ([Query, Key, Value: The Foundation of Transformer Attention](https://mbrenndoerfer.com/writing/query-key-value-attention-mechanism)).

**Scaled dot-product attention**  
Vaswani et al.’s scaled dot-product attention computes scores via dot products between queries and keys, scales by \(1/\sqrt{d_k}\), applies softmax to obtain attention weights, then uses those weights to form a weighted sum of values ([Attention Is All You Need](https://arxiv.org/html/1706.03762v7)). APXML explains the scaling motivation: if query/key components are roughly zero-mean unit-variance, the dot-product variance grows with \(d_k\), pushing softmax into saturation (small gradients); dividing by \(\sqrt{d_k}\) stabilizes magnitudes and training ([Scaled Dot-Product Attention Explained](https://apxml.com/courses/foundations-transformers-architecture/chapter-2-attention-mechanism-core-concepts/scaled-dot-product-attention)).

**Causal masking (decoder self-attention)**  
TensorFlow’s attention layer documentation describes a causal mask as preventing position \(i\) from attending to positions \(j>i\), “prevent[ing] the flow of information from the future towards the past,” and notes it is used for decoder self-attention (`use_causal_mask=True`) ([tfa.seq2seq.LuongAttention / tf.keras.layers.Attention docs](https://www.tensorflow.org/addons/api_docs/python/tfa/seq2seq/LuongAttention)).

**Attention weights**  
Attention weights are the softmax-normalized scores over keys for each query; they form a distribution (per query position) indicating how strongly each key position contributes to the output representation. APXML’s attention-map visualization notes that these weights are computed from scaled dot products followed by softmax, and can be retrieved from framework modules (e.g., PyTorch `nn.MultiheadAttention` returning averaged weights) ([Attention Map Visualization](https://apxml.com/courses/how-to-build-a-large-language-model/chapter-23-analyzing-model-behavior/attention-map-visualization)).

---

## Key Formulas & Empirical Results

### Scaled dot-product attention (Transformer)
From Vaswani et al., the canonical matrix form is:
\[
\mathrm{Attention}(Q,K,V)=\mathrm{softmax}\left(\frac{QK^\top}{\sqrt{d_k}}\right)V
\]
- \(Q\): queries matrix (packed queries)  
- \(K\): keys matrix (packed keys)  
- \(V\): values matrix (packed values)  
- \(d_k\): key (and query) dimensionality  
**Claim supported:** scaling by \(\sqrt{d_k}\) is part of the Transformer’s attention definition and is used before softmax ([Attention Is All You Need](https://arxiv.org/html/1706.03762v7)).

APXML’s justification: if components are independent with zero mean and unit variance, dot-product variance is \(d_k\); large magnitudes saturate softmax and reduce gradients; dividing by \(\sqrt{d_k}\) moderates magnitudes and stabilizes training ([Scaled Dot-Product Attention Explained](https://apxml.com/courses/foundations-transformers-architecture/chapter-2-attention-mechanism-core-concepts/scaled-dot-product-attention)).

### Dot-product attention layer (TensorFlow `tf.keras.layers.Attention`)
The TF Addons page describes the computation steps:
1. compute attention scores from query and key → shape `(batch_size, Tq, Tv)`
2. softmax over scores → shape `(batch_size, Tq, Tv)`
3. weighted combination of values → output shape `(batch_size, Tq, dim)`  
It also documents optional causal masking: `use_causal_mask=True` prevents attending to future positions \(j>i\) ([tfa.seq2seq.LuongAttention / tf.keras.layers.Attention docs](https://www.tensorflow.org/addons/api_docs/python/tfa/seq2seq/LuongAttention)).

### Luong “global” attention (multiplicative attention; seq2seq origin)
Luong et al. define global alignment weights:
\[
a_t(s)=\frac{\exp(\mathrm{score}(h_t,\bar h_s))}{\sum_{s'}\exp(\mathrm{score}(h_t,\bar h_{s'}))}
\]
and context:
\[
c_t=\sum_s a_t(s)\bar h_s
\]
Score functions (as listed in the paper summary cards):
- **dot:** \(h_t^\top \bar h_s\)  
- **general (bilinear):** \(h_t^\top W_a \bar h_s\)  
- **concat:** \(v_a^\top \tanh(W_a[h_t;\bar h_s])\)  
([Luong 2015 PDF](https://arxiv.org/pdf/1508.04025.pdf); also summarized at [ACL Anthology D15-1166](https://aclanthology.org/D15-1166/))  
**Claim supported:** Transformer dot-product attention descends from multiplicative attention; these are concrete alternative score functions students often confuse with scaled dot-product attention.

### Empirical results (Luong 2015, WMT’14 En→De)
From the benchmark card (tokenized BLEU newstest2014):
- baseline 11.3  
- +global attention (location) 16.8  
- +input-feeding 18.1  
- +local-p (general) + input-feeding 19.0  
- +unk replace 20.9  
- ensemble(8)+unk 23.0  
([ACL Anthology PDF D15-1166](https://aclanthology.org/anthology-files/pdf/D/D15/D15-1166.pdf))  
**Claim supported:** attention mechanisms materially improved seq2seq translation quality; “global vs local” is a compute/quality trade-off.

### Concrete implementation defaults (TensorFlow NMT tutorials)
**TF Text NMT with attention (GRU + CrossAttention)**
- `UNITS = 256`, `BATCH_SIZE = 64`  
- Encoder: `Embedding(mask_zero=True)` → `Bidirectional(GRU(..., return_sequences=True), merge_mode='sum')` producing `context` shape `(batch, s, units)`  
- CrossAttention: `MultiHeadAttention(num_heads=1, key_dim=units)` returning `attn_scores` shape `(batch, heads, t, s)` then averaged to `(batch, t, s)`  
- Loss: masked sparse CE with `from_logits=True`, `reduction='none'`, mask padding tokens (`y_true != 0`)  
([TF Text tutorial](https://www.tensorflow.org/text/tutorials/nmt_with_attention))

**TF Addons Transformer NMT tutorial**
- `BATCH_SIZE=64`, `MAX_SEQUENCE_LENGTH=40`, `VOCAB_SIZE=15000`, `EMBED_DIM=256`, `INTERMEDIATE_DIM=2048`, `NUM_HEADS=8`  
- Decoder uses causal masking “enabled by default” in their `TransformerDecoder` description  
- After 1 epoch: train accuracy 0.8385, loss 1.1014; val accuracy 0.8661, loss 0.8040; params 14,449,304  
([TF Addons seq2seq NMT tutorial](https://www.tensorflow.org/addons/tutorials/networks_seq2seq_nmt))

---

## How It Works

### Self-attention (single head) — mechanical steps with shapes
Assume:
- input token representations \(X\) shape `(B, T, d_model)`
- projection matrices \(W_Q, W_K, W_V\) map `d_model → d_k` (and `d_model → d_v`)

1. **Project to Q/K/V**
   - \(Q = XW_Q\) shape `(B, T, d_k)`
   - \(K = XW_K\) shape `(B, T, d_k)`
   - \(V = XW_V\) shape `(B, T, d_v)`  
   (Q/K/V role motivation: [Brenndörfer](https://mbrenndoerfer.com/writing/query-key-value-attention-mechanism))

2. **Compute raw attention scores**
   - \(S = QK^\top\) per batch → shape `(B, T, T)`  
   (dot-product scoring is the “Luong-style” / multiplicative family; see [Luong 2015](https://arxiv.org/pdf/1508.04025.pdf))

3. **Scale scores**
   - \(S \leftarrow S / \sqrt{d_k}\)  
   (definition: [Vaswani et al.](https://arxiv.org/html/1706.03762v7); motivation: [APXML scaling explanation](https://apxml.com/courses/foundations-transformers-architecture/chapter-2-attention-mechanism-core-concepts/scaled-dot-product-attention))

4. **Apply masks (if any)**
   - **Padding mask:** ensure padded key positions do not contribute (TF `value_mask` concept) ([TF Attention docs](https://www.tensorflow.org/addons/api_docs/python/tfa/seq2seq/LuongAttention))
   - **Causal mask (decoder):** set scores for future positions \(j>i\) to a large negative value so softmax gives ~0 probability; TF documents this as `use_causal_mask=True` ([TF Attention docs](https://www.tensorflow.org/addons/api_docs/python/tfa/seq2seq/LuongAttention))

5. **Softmax to get attention weights**
   - \(A = \mathrm{softmax}(S)\) over the last dimension → shape `(B, T, T)`  
   (weights definition and retrieval: [APXML attention map visualization](https://apxml.com/courses/how-to-build-a-large-language-model/chapter-23-analyzing-model-behavior/attention-map-visualization))

6. **Weighted sum of values**
   - Output \(O = AV\) → shape `(B, T, d_v)`  
   (matches TF Attention doc: softmax distribution used to create a linear combination of values, output `(batch, Tq, dim)` ([TF Attention docs](https://www.tensorflow.org/addons/api_docs/python/tfa/seq2seq/LuongAttention)))

### Causal masking — what the tutor should be able to state precisely
- For decoder self-attention, add a mask “such that position \(i\) cannot attend to positions \(j>i\)” to prevent future-to-past information flow ([TF Attention docs](https://www.tensorflow.org/addons/api_docs/python/tfa/seq2seq/LuongAttention)).
- In practice: before softmax, set disallowed logits to `-inf` (or a very negative number), so softmax assigns probability ~0.

### Retrieving attention weights in practice (PyTorch example pattern)
APXML notes that PyTorch `nn.MultiheadAttention` can return attention weights when `need_weights=True`, typically averaged over heads to shape `(batch, seq_len, seq_len)` ([Attention Map Visualization](https://apxml.com/courses/how-to-build-a-large-language-model/chapter-23-analyzing-model-behavior/attention-map-visualization)).

---

## Teaching Approaches

### Intuitive (no math)
- Self-attention lets each token decide “who to listen to” in the same sequence, producing a new representation that is a mixture of other tokens’ information.
- Q/K/V: a token uses one representation to *ask* (query), one to *be matched* (key), and one to *contribute content* (value). This avoids the limitation of “similarity = relevance,” e.g., pronouns (“it”) may need to attend to antecedents that aren’t embedding-similar ([Brenndörfer](https://mbrenndoerfer.com/writing/query-key-value-attention-mechanism)).

### Technical (with math)
- Use Vaswani’s single equation as the anchor:
  \[
  \mathrm{softmax}\left(\frac{QK^\top}{\sqrt{d_k}}\right)V
  \]
- Emphasize what changes per token: each row of \(Q\) produces a different distribution over all keys (rows of \(K\)), yielding different weighted sums of \(V\) ([Attention Is All You Need](https://arxiv.org/html/1706.03762v7)).

### Analogy-based
- Database/library analogy: query is your search request, keys are metadata used for matching, values are the content returned; attention weights are the match strengths used to combine returned content ([Brenndörfer](https://mbrenndoerfer.com/writing/query-key-value-attention-mechanism)).

---

## Common Misconceptions

1. **“Attention weights are the same thing as the output representation.”**  
   **Why wrong:** weights are just the softmax distribution over keys; the output is the *weighted sum of values* using those weights. TF’s attention doc explicitly separates “scores → softmax distribution” from “linear combination of value” ([TF Attention docs](https://www.tensorflow.org/addons/api_docs/python/tfa/seq2seq/LuongAttention)).  
   **Correct model:** weights \(A\) tell *how much* each value contributes; output \(O=AV\) is the new token representation.

2. **“Self-attention is just dot products of embeddings; Q/K/V are optional decoration.”**  
   **Why wrong:** Brenndörfer’s motivation is that raw embedding similarity answers “what is similar to me,” not “what is relevant to me” (e.g., pronoun resolution). Q/K/V projections let the model learn task-specific matching and content channels ([Brenndörfer](https://mbrenndoerfer.com/writing/query-key-value-attention-mechanism)).  
   **Correct model:** Q/K/V are learned projections that create specialized spaces for matching (Q·K) and content aggregation (V).

3. **“The \(\sqrt{d_k}\) scaling is arbitrary; it doesn’t matter.”**  
   **Why wrong:** APXML explains that dot-product variance grows with \(d_k\), which can saturate softmax and shrink gradients; scaling keeps logits in a healthier range for learning ([Scaled Dot-Product Attention Explained](https://apxml.com/courses/foundations-transformers-architecture/chapter-2-attention-mechanism-core-concepts/scaled-dot-product-attention)).  
   **Correct model:** scaling is a training-stability device tied to how dot-product magnitudes grow with dimension.

4. **“Causal masking means the model can’t use earlier tokens either (it ‘blocks context’).”**  
   **Why wrong:** TF defines causal masking as only blocking attention to *future* positions \(j>i\), not past positions ([TF Attention docs](https://www.tensorflow.org/addons/api_docs/python/tfa/seq2seq/LuongAttention)).  
   **Correct model:** causal mask enforces autoregressive directionality: token \(i\) can attend to tokens \(\le i\).

5. **“If I can plot attention maps, I’ve explained the model’s decision.”**  
   **Why wrong (nuanced):** Abnar & Zuidema argue that information gets mixed across layers, making raw attention weights unreliable as explanations; they propose attention rollout/flow as post-hoc methods to better approximate input-token relevance ([Quantifying Attention Flow in Transformers](https://arxiv.org/abs/2005.00928)).  
   **Correct model:** attention weights are internal routing signals; interpretability requires care, especially across multiple layers.

---

## Worked Examples

### Example 1 — Minimal scaled dot-product self-attention (NumPy; includes causal mask)
Runnable reference implementation the tutor can paste into a scratchpad.

```python
import numpy as np

def softmax(x, axis=-1):
    x = x - np.max(x, axis=axis, keepdims=True)  # stability
    ex = np.exp(x)
    return ex / np.sum(ex, axis=axis, keepdims=True)

def scaled_dot_product_attention(Q, K, V, causal=False):
    # Q,K,V: (T, d_k), (T, d_k), (T, d_v)
    d_k = Q.shape[-1]
    scores = (Q @ K.T) / np.sqrt(d_k)  # Vaswani et al.

    if causal:
        T = scores.shape[0]
        # mask out j > i
        mask = np.triu(np.ones((T, T), dtype=bool), k=1)
        scores = scores.copy()
        scores[mask] = -1e9  # approximate -inf

    A = softmax(scores, axis=-1)  # attention weights
    O = A @ V                     # weighted sum of values
    return O, A

# Toy data: 3 tokens, d_k=2, d_v=2
Q = np.array([[1., 0.],
              [0., 1.],
              [1., 1.]])
K = np.array([[1., 0.],
              [1., 1.],
              [0., 1.]])
V = np.array([[10., 0.],
              [0., 10.],
              [5., 5.]])

O_full, A_full = scaled_dot_product_attention(Q, K, V, causal=False)
O_causal, A_causal = scaled_dot_product_attention(Q, K, V, causal=True)

print("A_full:\n", np.round(A_full, 3))
print("O_full:\n", np.round(O_full, 3))
print("A_causal:\n", np.round(A_causal, 3))
print("O_causal:\n", np.round(O_causal, 3))
```

**Tutor prompts while stepping through**
- “What is the shape of `scores` and why?” (should be `(T,T)` because each query compares to each key)
- “Where does \(\sqrt{d_k}\) appear and what is it doing?” (scaling before softmax per Vaswani; stability per APXML)
- “What changes when `causal=True`?” (future logits set very negative so weights ~0; matches TF causal mask definition)

### Example 2 — Getting attention weights from PyTorch `nn.MultiheadAttention` (shape check)
APXML notes `need_weights=True` returns averaged attention weights across heads ([Attention Map Visualization](https://apxml.com/courses/how-to-build-a-large-language-model/chapter-23-analyzing-model-behavior/attention-map-visualization)).

```python
import torch
import torch.nn as nn

seq_len, embed_dim, num_heads, batch_size = 5, 8, 2, 1
mha = nn.MultiheadAttention(embed_dim, num_heads, batch_first=True)

x = torch.randn(batch_size, seq_len, embed_dim)
out, w = mha(x, x, x, need_weights=True, average_attn_weights=True)

print(out.shape)  # (1, 5, 8)
print(w.shape)    # (1, 5, 5) averaged over heads
```

---

## Comparisons & Trade-offs

| Mechanism | Q comes from | K/V come from | Typical use | Masking note | Source |
|---|---|---|---|---|---|
| **Self-attention** | same sequence | same sequence | encode context within a sequence | causal mask for autoregressive decoding | Vaswani et al. ([paper](https://arxiv.org/html/1706.03762v7)); TF causal mask doc ([TF](https://www.tensorflow.org/addons/api_docs/python/tfa/seq2seq/LuongAttention)) |
| **Cross-attention** | decoder states | encoder outputs (“memory”) | seq2seq: decoder attends to encoder | typically not causal over encoder positions; decoder side still autoregressive | TF Text NMT tutorial uses `query=x`, `value=context` ([TF Text](https://www.tensorflow.org/text/tutorials/nmt_with_attention)) |
| **Luong global attention (seq2seq)** | decoder state \(h_t\) | encoder states \(\bar h_s\) | classic RNN encoder–decoder attention | softmax over all source positions | Luong 2015 ([PDF](https://arxiv.org/pdf/1508.04025.pdf)) |
| **Luong local attention** | decoder state \(h_t\) | encoder states in a window | cheaper attention via windowing | restrict to \([p_t-D,p_t+D]\) with Gaussian bias | Luong 2015 ([PDF](https://arxiv.org/pdf/1508.04025.pdf)) |

**When to choose what (tutor framing)**
- Use **self-attention** when you need token-to-token interactions within the same sequence (Transformer encoder; decoder self-attn with causal mask).  
- Use **cross-attention** when a decoder must condition on an encoded source (TF Text NMT tutorial’s `query=x`, `value=context`) ([TF Text](https://www.tensorflow.org/text/tutorials/nmt_with_attention)).  
- Use **local attention** (Luong) when compute is a concern and alignments are roughly monotonic/local; Luong reports strong BLEU gains with local-p + input-feeding (19.0 vs 16.8 for global location in their progression) ([ACL PDF](https://aclanthology.org/anthology-files/pdf/D/D15/D15-1166.pdf)).

---

## Prerequisite Connections

- **Matrix multiplication & transpose**: needed to understand why \(QK^\top\) yields all pairwise query–key scores (Vaswani equation).  
- **Softmax as normalization**: needed to interpret attention weights as a distribution over keys (TF attention steps; Vaswani formula).  
- **Masking with \(-\infty\) logits**: needed to understand padding masks and causal masks before softmax (TF causal mask definition).  
- **Dot product as similarity/compatibility**: needed to interpret multiplicative scoring (Luong dot/general; Transformer dot-product attention).

---

## Socratic Question Bank

1. **If \(Q,K,V\) all come from the same \(X\), what makes self-attention “dynamic” rather than a fixed convolution-like mixing?**  
   *Good answer:* weights depend on \(QK^\top\), which depends on the current input representations, so mixing changes per example/token.

2. **Why do we apply softmax to scores—what property do we gain that raw dot products don’t have?**  
   *Good answer:* normalized, comparable weights per query (sum to 1), enabling a weighted average of values.

3. **What exactly breaks in training if we remove the \(1/\sqrt{d_k}\) scaling as \(d_k\) grows?**  
   *Good answer:* logits get large variance, softmax saturates, gradients shrink (APXML explanation).

4. **In causal masking, which entries of the attention matrix are forced near zero, and why?**  
   *Good answer:* positions \(j>i\) for each query \(i\), preventing future leakage (TF definition).

5. **If attention weights for token \(i\) put 0.9 on token \(j\), what does that imply about the output vector at \(i\)?**  
   *Good answer:* output at \(i\) is close to \(V_j\) plus small contributions from others; weights act on values.

6. **How would you explain the difference between “dot” vs “general” scoring in Luong attention?**  
   *Good answer:* dot is \(h_t^\top \bar h_s\); general inserts a learned matrix \(W_a\): \(h_t^\top W_a \bar h_s\) (Luong).

7. **In TF Text NMT tutorial cross-attention, what are the query and value tensors conceptually?**  
   *Good answer:* query is decoder sequence state; value (and keys) come from encoder context (`value=context`) ([TF Text](https://www.tensorflow.org/text/tutorials/nmt_with_attention)).

8. **Why might raw attention maps be a shaky explanation across many layers?**  
   *Good answer:* representations mix across layers; Abnar & Zuidema propose rollout/flow to better approximate input relevance ([arXiv:2005.00928](https://arxiv.org/abs/2005.00928)).

---

## Likely Student Questions

**Q: What is the exact self-attention formula I should memorize?**  
→ **A:** Vaswani et al.’s scaled dot-product attention: \(\mathrm{Attention}(Q,K,V)=\mathrm{softmax}(QK^\top/\sqrt{d_k})V\) ([Attention Is All You Need](https://arxiv.org/html/1706.03762v7)).

**Q: Why do we divide by \(\sqrt{d_k}\) before softmax?**  
→ **A:** APXML explains dot-product variance grows with \(d_k\), producing large-magnitude logits that saturate softmax and yield tiny gradients; scaling by \(1/\sqrt{d_k}\) moderates magnitudes and stabilizes training ([Scaled Dot-Product Attention Explained](https://apxml.com/courses/foundations-transformers-architecture/chapter-2-attention-mechanism-core-concepts/scaled-dot-product-attention)).

**Q: What does “causal mask” mean precisely?**  
→ **A:** TF’s attention docs: it “adds a mask such that position \(i\) cannot attend to positions \(j>i\),” preventing information flow from future to past; used for decoder self-attention (`use_causal_mask=True`) ([TF Attention docs](https://www.tensorflow.org/addons/api_docs/python/tfa/seq2seq/LuongAttention)).

**Q: What shapes should attention scores and outputs have?**  
→ **A:** TF docs: scores shape `(batch_size, Tq, Tv)`, softmax distribution same shape, output `(batch_size, Tq, dim)` ([TF Attention docs](https://www.tensorflow.org/addons/api_docs/python/tfa/seq2seq/LuongAttention)).

**Q: In cross-attention for translation, what are Q/K/V?**  
→ **A:** In the TF Text NMT tutorial, cross-attention uses `query=x` (decoder sequence) and `value=context` (encoder outputs); attention scores are shaped `(batch, heads, t, s)` before averaging heads ([TF Text](https://www.tensorflow.org/text/tutorials/nmt_with_attention)).

**Q: How do I get attention weights out of PyTorch MultiheadAttention?**  
→ **A:** APXML notes using `need_weights=True` returns attention weights (often averaged over heads) in addition to the output; typical averaged shape is `(batch, seq_len, seq_len)` ([Attention Map Visualization](https://apxml.com/courses/how-to-build-a-large-language-model/chapter-23-analyzing-model-behavior/attention-map-visualization)).

**Q: What are Luong’s score functions (dot/general/concat)?**  
→ **A:** Luong 2015: dot \(h_t^\top \bar h_s\); general \(h_t^\top W_a \bar h_s\); concat \(v_a^\top \tanh(W_a[h_t;\bar h_s])\) ([Luong 2015 PDF](https://arxiv.org/pdf/1508.04025.pdf)).

**Q: Do attention maps directly explain model decisions?**  
→ **A:** Abnar & Zuidema argue raw attention weights can be unreliable as explanations because information mixes across layers; they propose attention rollout and attention flow as post-hoc methods to better approximate attention to input tokens ([Quantifying Attention Flow in Transformers](https://arxiv.org/abs/2005.00928)).

---

## Available Resources

### Videos
- [Attention in transformers, visually explained | 3Blue1Brown](https://youtube.com/watch?v=eMlx5fFNoYc) — Surface when: student is stuck on Q/K/V intuition or what attention weights “mean” geometrically.  
- [Let’s build GPT: from scratch, in code, spelled out](https://youtube.com/watch?v=kCc8FmEb1nY) — Surface when: student wants an end-to-end “implement it” walkthrough including causal masking in an autoregressive model.

### Articles & Tutorials
- [The Illustrated Transformer (Jay Alammar)](https://jalammar.github.io/illustrated-transformer/) — Surface when: student needs a step-by-step visual of Q/K/V matrices, score computation, scaling, softmax, and the final matrix equation.  
- [Attention? Attention! (Lilian Weng)](https://lilianweng.github.io/posts/2018-06-24-attention/) — Surface when: student asks how attention evolved from seq2seq to self-attention and wants broader context/variants.  
- [Attention Is All You Need (Vaswani et al.)](https://arxiv.org/abs/1706.03762) — Surface when: student asks for the authoritative definition/equation of scaled dot-product attention and Transformer components.

---

## Visual Aids

![Self-attention links 'it' to 'animal', visualizing learned word relationships. (Alammar)](/api/wiki-images/self-attention/images/jalammar-illustrated-transformer_009.png)  
**Show when:** motivating why self-attention helps with relationships like coreference before introducing Q/K/V math.

![Step 2: Raw attention scores via dot product of query and key vectors. (Alammar)](/api/wiki-images/self-attention/images/jalammar-illustrated-transformer_011.png)  
**Show when:** student asks “what are the scores?” or confuses dot products with softmax weights.

![Steps 3–4: Scale scores by √d_k, then apply softmax to normalize. (Alammar)](/api/wiki-images/self-attention/images/jalammar-illustrated-transformer_012.png)  
**Show when:** student asks why scaling exists or where it appears in the pipeline.

![Full self-attention formula: softmax(QK^T/√d_k)V in matrix form. (Alammar)](/api/wiki-images/self-attention/images/jalammar-illustrated-transformer_015.png)  
**Show when:** student wants to connect the step-by-step procedure to the single compact equation.

![All attention heads combined for 'it' — hard to interpret. (Alammar, The Illustrated Transformer)](/api/wiki-images/self-attention/images/jalammar-illustrated-transformer_021.png)  
**Show when:** discussing interpretability limits of multi-head attention or why averaged maps can be confusing.

---

## Key Sources

- [Attention Is All You Need (Vaswani et al.)](https://arxiv.org/abs/1706.03762) — canonical definition and equation of scaled dot-product attention used in Transformers.  
- [Scaled Dot-Product Attention Explained (APXML)](https://apxml.com/courses/foundations-transformers-architecture/chapter-2-attention-mechanism-core-concepts/scaled-dot-product-attention) — clear variance/softmax-saturation motivation for the \(\sqrt{d_k}\) scaling.  
- [tfa.seq2seq.LuongAttention / tf.keras.layers.Attention docs](https://www.tensorflow.org/addons/api_docs/python/tfa/seq2seq/LuongAttention) — precise, implementation-facing shapes, masking semantics, and causal mask definition.  
- [Luong et al. 2015 (PDF)](https://arxiv.org/pdf/1508.04025.pdf) — exact global/local attention equations and score functions (dot/general/concat) that contextualize dot-product attention.  
- [Quantifying Attention Flow in Transformers (Abnar & Zuidema)](https://arxiv.org/abs/2005.00928) — cautions about interpreting raw attention weights; introduces rollout/flow as alternatives.