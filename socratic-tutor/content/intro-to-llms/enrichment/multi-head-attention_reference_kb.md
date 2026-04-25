## Core Definitions

**Multi-head attention (MHA).** Vaswani et al. (as reflected in TensorFlow’s `tf.keras.layers.MultiHeadAttention` and PyTorch’s `nn.MultiheadAttention` docs) implement multi-head attention as multiple scaled dot-product attention operations run in parallel on different learned linear projections of the same inputs; the per-head outputs are concatenated and then linearly projected to produce the final attention output. If `query`, `key`, and `value` are the same tensor, this is **self-attention**; otherwise it can be used for **cross-attention** (TensorFlow API doc).

**Attention head.** In multi-head attention, each head is one independent scaled dot-product attention computation with its own learned projection parameters for \(Q,K,V\) (and typically a shared final output projection after concatenation). PyTorch describes this as splitting `embed_dim` across `num_heads` so each head attends in a subspace (PyTorch `nn.MultiheadAttention` doc).

**Positional encoding (general).** Positional encodings are mechanisms that inject token order information into a Transformer, since attention alone is permutation-invariant over the set of tokens. In the original Transformer, positional information is added to token embeddings (as shown in Alammar’s positional encoding visualizations of the Vaswani et al. method).

**Sinusoidal positional encoding.** The original Transformer positional encoding uses fixed sine/cosine patterns across embedding dimensions (visualized in Alammar’s “positional encoding values” heatmaps), producing deterministic position-dependent vectors that are added to token embeddings (Alammar; derived from Vaswani et al. positional encoding depiction).

**RoPE (Rotary Position Embedding).** Su et al. define RoPE as applying position-dependent **2D rotations** to the query and key vectors (pairing even/odd dimensions into 2D subspaces) so that the dot product between rotated \(Q\) and \(K\) becomes a function of **relative position** \(m-n\) (RoPE paper Eq. 11–16).

**ALiBi (Attention with Linear Biases).** Press et al. define ALiBi as adding a **head-specific linear bias** to the attention logits (pre-softmax) proportional to relative distance, rather than adding positional embeddings to token representations; the bias penalizes attention to more distant tokens in causal self-attention (ALiBi paper, Section 3).

---

## Key Formulas & Empirical Results

### Scaled dot-product attention (per head) + MHA structure (API-grounded)
From TensorFlow `tf.keras.layers.MultiHeadAttention` (and consistent with PyTorch’s conceptual equation):

- Per head:
  \[
  \text{scores} = \frac{QK^\top}{\sqrt{d_k}},\quad P=\text{softmax}(\text{scores}),\quad O_{\text{head}} = PV
  \]
  where \(d_k=\) `key_dim` (TF) / per-head key dimension.

- MHA output: concatenate head outputs, then optional final linear projection (TF API doc; PyTorch doc describes `Concat(head₁,…,head_h) W^O`).

**What it supports:** why multiple heads can attend to different patterns simultaneously; what the \(\sqrt{d_k}\) scaling is doing (stabilizing logits magnitude).

### RoPE: rotation-based relative position in dot products (Su et al., Eq. 11–16)
Goal (relative-only dependence):
\[
\langle f_q(x_m,m), f_k(x_n,n)\rangle = g(x_m,x_n,m-n)
\]
RoPE construction (even \(d\), pair dims into 2D blocks):
\[
f_{\{q,k\}}(x_m,m)=R^d_{\Theta,m}W_{\{q,k\}}x_m
\]
with block-diagonal rotation matrix \(R^d_{\Theta,m}\) using angles \(m\theta_i\), and
\[
\theta_i = 10000^{-2(i-1)/d}
\]
Key identity (relative position emerges):
\[
(R_{\Theta,m}W_qx_m)^\top(R_{\Theta,n}W_kx_n)=(W_qx_m)^\top R_{\Theta,n-m}(W_kx_n)
\]
and \(R\) is orthogonal (norm-preserving) (RoPE paper).

**What it supports:** RoPE encodes relative positions directly in attention dot-products without adding position vectors to embeddings.

### ALiBi: linear distance bias added to logits (Press et al., Section 3)
For causal self-attention at query position \(i\), modify logits:
\[
\text{softmax}\Big(q_iK^\top \;+\; m\cdot [-(i-1),\ldots,-2,-1,0]\Big)
\]
- \(m\): fixed, **head-specific slope** (non-learned).
- Bias is added **pre-softmax** to logits; paper notes it is **not multiplied by** the usual \(\sqrt{d_k}\) scaling factor (ALiBi footnote 10).

**Slope defaults (paper):**
- 8 heads: \(2^{-1},2^{-2},\ldots,2^{-8}\).
- 16 heads: interpolate via geometric averaging consecutive pairs of the 8-head slopes (ALiBi paper).

**Empirical claims (paper):**
- A 1.3B model trained with context 1024 extrapolates to 2048 with perplexity matching a sinusoidal model trained on 2048, while being **11% faster** and using **11% less memory** (ALiBi abstract/results).
- WikiText-103 example: trained on 512 tokens gets **19.73** ppl at \(L_{valid}=512\), improves to **18.40** at \(L_{valid}=3072\) (ALiBi paper).

### Head redundancy/pruning evidence (Michel et al., NeurIPS 2019)
- WMT14 En→Fr Transformer-Large (6 layers, 16 heads/layer, BLEU 36.05): only **8/96** encoder self-attn heads cause significant BLEU change when individually removed (p<0.01); about half of those increases BLEU (paper).
- Many layers can be reduced to **1 head** with minimal loss, but encoder-decoder attention can be highly sensitive (e.g., Enc-Dec layer 6 single-head causes **−13.56 BLEU**) (paper).
- Pruning ~50% of BERT heads yields up to **+17.5%** inference speed at larger batch sizes (batch 64: 124.7→146.6 ex/s) (paper).

**What it supports:** “more heads” is not automatically better; some heads are redundant, but some (especially cross-attention) can be critical.

### Implementation defaults & mask semantics (TensorFlow + PyTorch APIs)

**TensorFlow `tf.keras.layers.MultiHeadAttention` constructor defaults (TF API doc):**
- `value_dim=None`, `dropout=0.0`, `use_bias=True`, `output_shape=None`, `attention_axes=None`.

**TensorFlow call/mask semantics (TF API doc):**
- `attention_mask`: boolean shape `(B, T, S)`; 1 allow, 0 block; broadcasting allowed.
- `use_causal_mask`: boolean to prevent attending to future tokens.
- `return_attention_scores=True` returns `(attention_output, attention_scores)`.

**PyTorch `nn.MultiheadAttention` constructor defaults (PyTorch doc):**
- `dropout=0.0`, `bias=True`, `kdim=None` ⇒ `kdim=embed_dim`, `vdim=None` ⇒ `vdim=embed_dim`, `batch_first=False`.

**PyTorch masks (PyTorch doc):**
- `key_padding_mask` shape `(N,S)`: True ⇒ ignore key position; float mask is added to scores.
- `attn_mask` shape `(L,S)` or `(N,L,S)`: True ⇒ disallow; float mask is added.
- If both masks are given, their **types must match**.
- `need_weights=False` enables optimized `scaled_dot_product_attention()` path for performance (PyTorch doc).

---

## How It Works

### Multi-head attention: mechanical steps (self-attention case)
1. **Inputs and shapes.**
   - Sequence hidden states \(X\) shaped like `(B, T, d_model)` (TF call signature; PyTorch uses `(L,N,E)` unless `batch_first=True`).
2. **Linear projections into Q, K, V per head.**
   - For each head \(h\), project \(X\) into \(Q^h, K^h, V^h\) with learned matrices (TF API describes per-head `key_dim`/`value_dim`; Michel et al. list head-specific \(W_q^h,W_k^h,W_v^h\)).
3. **Scaled dot-product attention per head.**
   - Compute logits \(\frac{Q^h (K^h)^\top}{\sqrt{d_k}}\) (TF API).
4. **Apply masks (if any).**
   - **Padding mask**: block attention to padded key positions (`key_padding_mask` in PyTorch; `attention_mask` in TF).
   - **Causal mask**: prevent attending to future tokens (`use_causal_mask` in TF; `is_causal=True` in PyTorch).
   - In PyTorch, boolean masks disallow positions; float masks are **added** to attention weights/logits (PyTorch doc).
5. **Softmax to get attention probabilities.**
   - \(P^h=\text{softmax}(\text{logits})\) (TF API).
6. **Weighted sum of values.**
   - \(O^h = P^h V^h\) (TF API).
7. **Concatenate head outputs.**
   - `Concat(O^1,…,O^H)` (PyTorch conceptual equation).
8. **Final output projection.**
   - Multiply by output projection \(W^O\) (PyTorch doc) / TF’s optional final linear projection; TF `output_shape=None` means project back to query last-dim.

### Where positional methods plug in (three common patterns from sources)
- **Sinusoidal positional encoding:** add position vector to token embedding/hidden state before attention (Alammar’s depiction of Vaswani et al. method).
- **RoPE:** apply position-dependent rotations to **Q and K** before computing \(QK^\top\) (RoPE paper).
- **ALiBi:** add distance-dependent bias directly to **attention logits** \(QK^\top\) before softmax (ALiBi paper).

### Minimal RoPE implementation sketch (conceptual, equation-faithful)
Given projected \(Q,K\) with last-dim \(d\) even:
1. Pair dims into \((0,1),(2,3),\dots\).
2. For each pair, rotate by angle \(m\theta_i\) at position \(m\) (RoPE Eq. 12–16).
3. Use rotated \(Q',K'\) in logits \(Q'(K')^\top\).

(Keep this as a tutor “where it goes” reminder; the exact rotation matrix is in RoPE Eq. 12–16.)

---

## Teaching Approaches

### Intuitive (no math)
- **Multi-head attention:** “One attention layer is like asking one kind of question about the sequence (e.g., ‘what matches this token?’). Multi-head means asking several different kinds of questions in parallel, then combining the answers.”
- **Positional methods:** “Attention alone doesn’t know order. Positional encoding is how we tell the model ‘this token is earlier/later’—either by adding position patterns to embeddings (sinusoidal), rotating Q/K based on position (RoPE), or biasing attention toward nearby tokens (ALiBi).”

### Technical (with math)
- Use the TF equation: scores \(=\frac{QK^\top}{\sqrt{d_k}}\), softmax, then multiply by \(V\).
- Explain that heads differ because they use different learned projections \(W_q^h,W_k^h,W_v^h\) (Michel et al.).
- For RoPE, emphasize the identity:
  \[
  (R_m q)^\top (R_n k) = q^\top R_{n-m} k
  \]
  so dot-products depend on relative offset \(n-m\) (RoPE Eq. 14–16).
- For ALiBi, emphasize “add bias to logits pre-softmax” and head-specific slopes (ALiBi Section 3).

### Analogy-based
- **Heads as “lenses”:** each head is a different lens/filter over the same sentence; concatenation is stacking multiple feature maps.
- **RoPE as “rotating coordinate frames”:** each position rotates the query/key vectors; comparing two rotated vectors reveals their relative rotation (relative position).
- **ALiBi as “distance toll”:** every step back in the past costs a little more (more negative bias), with different heads charging different toll rates (different slopes).

---

## Common Misconceptions

1. **“Each head attends to a different token position, like head 1 looks left, head 2 looks right.”**  
   - **Why wrong:** Heads are not hard-assigned to positions; each head computes a full attention distribution over keys via softmax of \(QK^\top\) (TF/PyTorch attention definition).  
   - **Correct model:** Heads differ by **learned projections** into different subspaces (\(W_q^h,W_k^h,W_v^h\)), so they can learn different *types* of relationships, not fixed directions (Michel et al.; PyTorch conceptual description).

2. **“More heads always means better performance.”**  
   - **Why wrong:** Head pruning results show many heads are redundant; removing many heads often has little effect, and some removals can even improve BLEU (Michel et al.).  
   - **Correct model:** Heads provide capacity/diversity, but usefulness is task- and layer-dependent; some heads (notably encoder-decoder attention heads) can be critical (Michel et al.).

3. **“Positional encoding is always added to embeddings; RoPE and ALiBi are just variants of that.”**  
   - **Why wrong:** RoPE applies rotations to **Q and K** (multiplicative, not additive), and ALiBi adds bias to **logits** and explicitly “does not add positional embeddings” (RoPE paper; ALiBi paper).  
   - **Correct model:** Positional information can enter at different points: input embeddings (sinusoidal), Q/K transformation (RoPE), or logits bias (ALiBi).

4. **“Masks just delete tokens from the sequence.”**  
   - **Why wrong:** In both TF and PyTorch, masks operate on **attention scores/weights**: they block certain query-key pairs (TF `attention_mask`; PyTorch `attn_mask`/`key_padding_mask`), not necessarily removing tokens from tensors.  
   - **Correct model:** Masking changes which keys each query is allowed to attend to; the token representations still exist, but their influence can be prevented via masked logits/weights (TF/PyTorch docs).

5. **“Attention weights are always an explanation of model decisions.”**  
   - **Why wrong:** The “Attention is not not Explanation” paper argues the usefulness depends on definitions and proposes multiple tests; attention weights alone are not guaranteed to be faithful explanations in all settings (Wiegreffe & Pinter, 2019).  
   - **Correct model:** Attention maps can be informative diagnostics, but explanation claims require careful testing and context (Wiegreffe & Pinter, 2019).

---

## Worked Examples

### Example 1: PyTorch `nn.MultiheadAttention` with both masks (shapes + outputs)
```python
import torch
import torch.nn as nn

torch.manual_seed(0)

# Settings
N = 2          # batch size
L = 4          # target length (query length)
S = 6          # source length (key/value length)
E = 8          # embed_dim
H = 2          # num_heads

mha = nn.MultiheadAttention(embed_dim=E, num_heads=H, batch_first=True)  # PyTorch doc

# Fake data
query = torch.randn(N, L, E)
key   = torch.randn(N, S, E)
value = torch.randn(N, S, E)

# key_padding_mask: shape (N, S); True means "ignore this key position"
key_padding_mask = torch.tensor([
    [False, False, False, False, True,  True],
    [False, False, True,  False, False, True],
])

# attn_mask: either (L,S) or (N,L,S). Here: (L,S) broadcast across batch.
# True means "disallow attending"
attn_mask = torch.zeros(L, S, dtype=torch.bool)
attn_mask[:, 0] = True  # block attending to key position 0 for all queries

attn_output, attn_weights = mha(
    query, key, value,
    key_padding_mask=key_padding_mask,
    attn_mask=attn_mask,
    need_weights=True,
    average_attn_weights=False,  # get per-head weights (PyTorch doc)
)

print(attn_output.shape)   # (N, L, E)
print(attn_weights.shape)  # (N, H, L, S)
```

**Tutor notes (what to point out live):**
- `attn_weights` is per-head only if `average_attn_weights=False` (PyTorch doc).
- `key_padding_mask` blocks keys per batch element; `attn_mask` blocks query-key pairs (PyTorch doc).
- If a student gets a type error: PyTorch requires mask types match if both are provided (PyTorch doc).

### Example 2: TensorFlow `MultiHeadAttention` returning attention scores
```python
import tensorflow as tf

B, T, S, D = 2, 4, 6, 8
num_heads = 2
key_dim = 4

mha = tf.keras.layers.MultiHeadAttention(
    num_heads=num_heads,
    key_dim=key_dim,
    dropout=0.0,     # default is 0.0 (TF doc)
    use_bias=True,   # default True (TF doc)
)

query = tf.random.normal((B, T, D))
value = tf.random.normal((B, S, D))

# attention_mask: (B, T, S), 1 allow, 0 block (TF doc)
attention_mask = tf.ones((B, T, S), dtype=tf.int32)
attention_mask = tf.tensor_scatter_nd_update(
    attention_mask,
    indices=[[0, 0, 5]],  # block one query-key pair
    updates=[0]
)

out, scores = mha(
    query=query,
    value=value,
    attention_mask=attention_mask,
    return_attention_scores=True,  # TF doc
    use_causal_mask=False
)

print(out.shape)    # (B, T, D) if output_shape=None (TF doc)
print(scores.shape) # multi-head attention coefficients (TF doc)
```

**Tutor notes:**
- TF mask semantics are “1 allow, 0 block” and shape `(B,T,S)` with broadcasting allowed (TF doc).
- `use_causal_mask=True` is the simplest way to enforce autoregressive behavior (TF doc).

---

## Comparisons & Trade-offs

| Method | Where position info enters | What changes mathematically | Key defaults / notes (from sources) | When to choose (source-grounded) |
|---|---|---|---|---|
| Sinusoidal positional encoding (Vaswani-style, via Alammar visuals) | Added to embeddings/hidden states | Add fixed position vector to token representation | Visualized as interleaved sine/cos patterns (Alammar images) | Baseline, simple fixed encoding; common for teaching/legacy implementations |
| RoPE (Su et al., 2021) | Applied to **Q and K** | Rotate Q/K in 2D subspaces so dot-products depend on \(m-n\) | \(\theta_i = 10000^{-2(i-1)/d}\); orthogonal rotations preserve norms (RoPE paper) | When you want explicit relative-position behavior in attention dot-products |
| ALiBi (Press et al., 2021) | Added to **attention logits** | Add head-specific linear distance bias pre-softmax | 8-head slopes \(2^{-1}\dots2^{-8}\); bias not scaled by \(\sqrt{d_k}\) (ALiBi paper) | When you want length extrapolation without positional embeddings; paper reports speed/memory gains and extrapolation results |

**Extra trade-off (heads):** Many heads can be redundant (Michel et al.), but pruning cross-attention heads can be catastrophic in some layers (Michel et al.). Use this when students ask “how many heads do I need?”

---

## Prerequisite Connections

- **Scaled dot-product attention:** Needed to understand what each head computes (\(QK^\top/\sqrt{d_k}\), softmax, then \(V\)) (TF API).
- **Linear projections / embeddings:** Heads differ via learned \(W_q^h,W_k^h,W_v^h\) projections (Michel et al.; PyTorch conceptual description).
- **Masking in attention:** Needed to reason about padding vs causal behavior (TF/PyTorch mask semantics).
- **Softmax behavior:** Needed to interpret logits biases (ALiBi) and why scaling by \(\sqrt{d_k}\) matters (TF attention equation; ALiBi note about not scaling bias).

---

## Socratic Question Bank

1. **If we removed the final output projection after concatenating heads, what capacity would we lose?**  
   *Good answer:* recognizes concatenation alone doesn’t mix head subspaces; output projection mixes/reshapes back to model dimension (PyTorch conceptual equation).

2. **What’s the difference between blocking a key with `key_padding_mask` vs blocking with `attn_mask` in PyTorch?**  
   *Good answer:* `key_padding_mask` is per-batch key position mask `(N,S)`; `attn_mask` is per query-key pair `(L,S)` or `(N,L,S)` (PyTorch doc).

3. **Why does RoPE rotate Q and K but not necessarily V in the core definition? What part of attention uses Q/K vs V?**  
   *Good answer:* dot-products (logits) use Q and K; V is only used after softmax as weighted sum (TF attention computation; RoPE focuses on Q/K).

4. **In ALiBi, where exactly is the bias added, and why does that matter?**  
   *Good answer:* added to logits pre-softmax \(q_iK^\top + \text{bias}\); affects probability distribution directly (ALiBi paper).

5. **If many heads are redundant, why not always use 1 head? What evidence suggests that can fail?**  
   *Good answer:* cites Michel et al. result where encoder-decoder attention layer 6 single-head causes −13.56 BLEU; sensitivity differs by component.

6. **What would happen if you forgot to apply a causal mask in an autoregressive decoder?**  
   *Good answer:* model can attend to future tokens during training/inference, breaking autoregressive constraint; relates to `use_causal_mask`/`is_causal` (TF/PyTorch docs).

7. **How can positional information be injected without changing token embeddings at all?**  
   *Good answer:* ALiBi adds bias to attention logits and explicitly does not add positional embeddings (ALiBi paper).

8. **Why might `need_weights=False` speed up PyTorch attention?**  
   *Good answer:* PyTorch doc: enables optimized `scaled_dot_product_attention()` path; avoids returning weights.

---

## Likely Student Questions

**Q: In TensorFlow `MultiHeadAttention`, what shape should `attention_mask` be and what do 1/0 mean?**  
→ **A:** TF expects a boolean mask shaped `(B, T, S)` where **1 allows attention and 0 blocks**, with broadcasting allowed over missing batch/head dims; it masks attention over the attention axes (TensorFlow `tf.keras.layers.MultiHeadAttention` doc).

**Q: In PyTorch, what’s the difference between `attn_mask` and `key_padding_mask`?**  
→ **A:** `key_padding_mask` is shape `(N,S)` and masks **key positions** per batch element (True = ignore); `attn_mask` is `(L,S)` broadcast across batch or `(N,L,S)` per batch and masks **query-key pairs** (True = disallow). Float masks are added to scores/weights; if both masks are provided their types must match (PyTorch `nn.MultiheadAttention` doc).

**Q: What exactly does ALiBi add to attention, and is it scaled by \(\sqrt{d_k}\)?**  
→ **A:** ALiBi adds a head-specific linear bias proportional to relative distance directly to the **pre-softmax logits** \(q_iK^\top\); the paper notes the bias term is **not multiplied by** the usual \(\sqrt{d_k}\) scaling factor (ALiBi paper, Section 3 and footnote 10).

**Q: What are the default ALiBi slopes for 8 heads?**  
→ **A:** The paper’s default for 8 heads is the geometric sequence \(2^{-1},2^{-2},\ldots,2^{-8}\) (ALiBi paper, Section 3).

**Q: How does RoPE make attention depend on relative position rather than absolute position?**  
→ **A:** RoPE rotates \(Q\) at position \(m\) and \(K\) at position \(n\) with rotation matrices \(R_{\Theta,m}\) and \(R_{\Theta,n}\); the dot product becomes \((W_qx_m)^\top R_{\Theta,n-m}(W_kx_n)\), which depends on \(n-m\) (RoPE paper Eq. 14–16).

**Q: Are more attention heads always better?**  
→ **A:** Not necessarily—head pruning experiments show many heads can be removed with little effect (e.g., only 8/96 encoder self-attn heads in a WMT Transformer-Large significantly affected BLEU when removed), but some heads—especially encoder-decoder attention heads—can be critical (e.g., a single-head ablation in Enc-Dec layer 6 caused −13.56 BLEU) (Michel et al., NeurIPS 2019).

**Q: In PyTorch, why is `need_weights=False` recommended for performance?**  
→ **A:** PyTorch notes that setting `need_weights=False` allows use of the optimized `scaled_dot_product_attention()` fast path for best performance (PyTorch `nn.MultiheadAttention` doc).

---

## Available Resources

### Videos
- [Attention in transformers, visually explained | Chapter 6, Deep Learning](https://youtube.com/watch?v=eMlx5fFNoYc) — **Surface when:** student can compute attention mechanically but lacks intuition for why multiple heads help.
- [Let’s build GPT: from scratch, in code, spelled out](https://youtube.com/watch?v=kCc8FmEb1nY) — **Surface when:** student asks “how do I implement MHA/masks end-to-end?” or wants code-level grounding.
- [Video (wjZofJX0v4M)](https://youtube.com/watch?v=wjZofJX0v4M) — **Surface when:** student needs a high-level Transformer overview before diving into MHA/positional methods.

### Articles & Tutorials
- [The Illustrated Transformer (Jay Alammar)](https://jalammar.github.io/illustrated-transformer/) — **Surface when:** student asks for visual step-by-step of Q/K/V, head splitting, and positional encoding heatmaps.
- [Attention? Attention! (Lilian Weng)](https://lilianweng.github.io/posts/2018-06-24-attention/) — **Surface when:** student wants a more formal taxonomy/history and precise attention formulations.
- [Attention Is All You Need (Vaswani et al.)](https://arxiv.org/abs/1706.03762) — **Surface when:** student wants the primary-source definition of MHA and original positional encoding motivation.

---

## Visual Aids

![Multi-head scaled dot-product attention with parallel heads and projection. (Vaswani et al., 2017)](/api/wiki-images/multi-head-attention/images/lilianweng-posts-2018-06-24-attention_013.png)  
**Show when:** student asks “what does multi-head attention *look like* structurally?” or confuses “multiple heads” with “multiple layers.”

![Actual positional encoding values for a 4-dimensional embedding. (Alammar, 2018)](/api/wiki-images/multi-head-attention/images/jalammar-illustrated-transformer_023.png)  
**Show when:** student asks “what are positional encodings numerically?” or struggles with sine/cosine patterns across dimensions.

![Positional encoding from 'Attention Is All You Need' paper (interleaved). (Alammar, 2018)](/api/wiki-images/multi-head-attention/images/jalammar-illustrated-transformer_025.png)  
**Show when:** student asks about the original paper’s sinusoidal encoding layout (interleaving sine/cosine) and how to read it.

![Full Transformer architecture: encoder-decoder with multi-head attention. (Vaswani et al., 2017)](/api/wiki-images/transformer-architecture/images/lilianweng-posts-2018-06-24-attention_016.png)  
**Show when:** student confuses self-attention vs cross-attention, or asks where positional encoding sits in the full encoder-decoder stack.

---

## Key Sources

- [tf.keras.layers.MultiHeadAttention](https://www.tensorflow.org/api_docs/python/tf/keras/layers/MultiHeadAttention) — authoritative constructor/call semantics, mask handling, and returned attention scores.
- [torch.nn.MultiheadAttention](https://docs.pytorch.org/docs/stable/generated/torch.nn.MultiheadAttention.html) — authoritative PyTorch shapes, mask types, and performance note (`need_weights=False`).
- [RoFormer: Rotary Position Embedding (RoPE)](https://arxiv.org/abs/2104-09864) — defining equations showing how rotations yield relative-position dependence in dot products.
- [Train Short, Test Long: ALiBi](https://arxiv.org/abs/2108.12409) — exact logits-bias formula, slope schedule, and extrapolation speed/memory results.
- [Are Sixteen Heads Really Better than One? (Head pruning)](https://proceedings.neurips.cc/paper_files/paper/2019/file/2c601ad9d2ff9bc8b282670cdd54f69f-Paper.pdf) — empirical evidence on head redundancy and sensitivity differences (self-attn vs encoder-decoder attention).