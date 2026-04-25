## Key Facts & Specifications

- **Scaled dot-product attention (Transformer) definition**
  - \(\mathrm{Attention}(Q,K,V)=\mathrm{softmax}\left(\frac{QK^{T}}{\sqrt{d_{k}}}\right)V\) where queries and keys have dimension \(d_k\) and values have dimension \(d_v\). (Vaswani et al., 2017, §3.2.1, Eq. 1: https://arxiv.org/html/1706.03762v7)

- **Why divide by \(\sqrt{d_k}\) (variance / gradient rationale)**
  - Vaswani et al. state that for large \(d_k\), dot products grow large in magnitude, pushing softmax into regions with “extremely small gradients,” and therefore they scale by \(1/\sqrt{d_k}\). They illustrate: if components of \(q\) and \(k\) are i.i.d. with mean 0 and variance 1, then \(q\cdot k=\sum_{i=1}^{d_k} q_i k_i\) has mean 0 and variance \(d_k\). (Vaswani et al., 2017, §3.2.1 and footnote: https://arxiv.org/html/1706.03762v7)
  - ApX ML repeats the same assumption and states the variance of the dot product is \(d_k\), and scaling keeps softmax inputs in a regime with larger gradients. (ApX Machine Learning, “Scaled Dot-Product Attention Explained”: https://apxml.com/courses/foundations-transformers-architecture/chapter-2-attention-mechanism-core-concepts/scaled-dot-product-attention)

- **Multi-head attention head dimensions used in the Transformer paper**
  - “For each of these we use \(d_k=d_v=d_{\text{model}}/h=64\).” (Vaswani et al., 2017, §3.2.2: https://arxiv.org/html/1706.03762v7)
  - Wikipedia notes \(d_k\) was “initially set to 64 within the paper.” (Wikipedia, “Attention Is All You Need”: https://en.wikipedia.org/wiki/Attention_Is_All_You_Need)

- **Masking for autoregressive decoding**
  - In the Transformer decoder, self-attention allows each position to attend to positions “up to and including that position,” and illegal connections are masked by “setting to \(-\infty\)” the softmax inputs for those connections. (Vaswani et al., 2017: https://arxiv.org/html/1706.03762v7)

- **PyTorch `nn.MultiheadAttention` key interface facts (shapes, masks, outputs)**
  - Constructor signature includes `embed_dim`, `num_heads`, `dropout`, `batch_first=False`, etc. (PyTorch docs: https://docs.pytorch.org/docs/stable/generated/torch.nn.MultiheadAttention.html)
  - Input shapes:
    - `query`: unbatched \((L,E_q)\); batched \((L,N,E_q)\) if `batch_first=False` or \((N,L,E_q)\) if `batch_first=True`. (PyTorch docs URL above)
    - `key`/`value`: unbatched \((S,E_k/E_v)\); batched \((S,N,E_k/E_v)\) or \((N,S,E_k/E_v)\) depending on `batch_first`. (PyTorch docs URL above)
  - `key_padding_mask` shape: \((N,S)\) (or \((S)\) unbatched) indicating which `key` elements to ignore as padding. (PyTorch docs URL above)
  - `attn_mask` shape: \((L,S)\) or \((N\cdot \text{num\_heads},L,S)\). (PyTorch docs URL above)
  - Mask semantics in `nn.MultiheadAttention`:
    - “Binary and float masks are supported. For a binary mask, a `True` value indicates that the corresponding `key` value will be ignored.” For float masks, values are “directly added” to attention scores. (PyTorch docs URL above)
  - Returned attention weights shapes:
    - If `average_attn_weights=True`: \((N,L,S)\) (batched) or \((L,S)\) (unbatched).
    - If `average_attn_weights=False`: \((N,\text{num\_heads},L,S)\) (batched) or \((\text{num\_heads},L,S)\) (unbatched). (PyTorch docs URL above)
  - Performance note: “Set `need_weights=False` to use the optimized `scaled_dot_product_attention` and achieve the best performance.” (PyTorch docs URL above)

- **PyTorch `F.scaled_dot_product_attention` reference implementation and dropout behavior**
  - The docs provide an “efficient implementation equivalent” pseudocode that:
    - builds `attn_bias`,
    - applies causal masking via a lower-triangular boolean mask and `masked_fill_(..., -inf)`,
    - applies boolean `attn_mask` by masking with `-inf` (note: in this function, boolean `True` indicates the element *should take part in attention*; it masks where `logical_not()` is true),
    - adds float masks directly,
    - computes `softmax` and then `torch.dropout(..., train=True)`. (PyTorch docs: https://docs.pytorch.org/docs/stable/generated/torch.nn.functional.scaled_dot_product_attention.html)
  - Dropout warning: this function “always applies dropout according to the specified `dropout_p` argument”; to disable dropout in eval, pass `0.0` when not training. (PyTorch docs URL above)
  - Constraint: error if both `attn_mask` and `is_causal` are set. (PyTorch docs URL above)

- **Sinusoidal positional encoding formula**
  - \(PE_{(pos,2i)}=\sin\left(\frac{pos}{10000^{2i/d_{model}}}\right)\), \(PE_{(pos,2i+1)}=\cos\left(\frac{pos}{10000^{2i/d_{model}}}\right)\). (ApX Machine Learning: https://apxml.com/courses/foundations-transformers-architecture/chapter-4-positional-encoding-embedding-layer/sinusoidal-encoding-formulation; also GeeksforGeeks: https://www.geeksforgeeks.org/nlp/positional-encoding-in-transformers/)
  - The original paper’s stated motivation (quoted in a secondary source): they hypothesized it would let the model learn relative positions because \(PE_{pos+k}\) can be represented as a linear function of \(PE_{pos}\) for fixed offset \(k\). (Kemal Erdem blog quoting the paper: https://erdem.pl/2021/05/understanding-positional-encoding-in-transformers/)

- **FlashAttention: exact attention with reduced memory traffic; reported speed/quality numbers**
  - FlashAttention is “IO-aware exact attention” using tiling to reduce HBM↔SRAM reads/writes; standard attention time and memory are quadratic in sequence length. (Dao et al., 2022: https://arxiv.org/abs/2205.14135)
  - Reported benchmarks in the abstract:
    - **15%** end-to-end wall-clock speedup on **BERT-large** (seq length **512**) vs MLPerf 1.1 training speed record.
    - **3×** speedup on **GPT-2** (seq length **1K**).
    - **2.4×** speedup on Long Range Arena (seq length **1K–4K**).
    - Enables Path-X (seq length **16K**) **61.4%** accuracy and Path-256 (seq length **64K**) **63.1%** accuracy.
    - “0.7 better perplexity on GPT-2” and “6.4 points of lift on long-document classification.” (Dao et al., 2022 abstract: https://arxiv.org/abs/2205.14135)
  - Aman’s primer (secondary) states standard attention uses \(O(N^2\cdot d)\) operations and \(O(N^2)\) memory for the attention matrix, while FlashAttention achieves **linear memory growth** in \(N\) by not materializing the \(N\times N\) matrix, and reports additional metrics (e.g., FlashAttention-2 throughput/utilization). (Aman.ai primer: https://aman.ai/primers/ai/flashattention/)  
    - Note: these performance/utilization numbers are not from the original paper; treat as secondary reporting.

- **Longformer sliding-window attention complexity and example hyperparameters (secondary notes)**
  - Sliding window attention complexity \(O(n\cdot w)\) (linear in sequence length \(n\) for fixed window \(w\)). (Naoki Shibuya blog summary: https://naokishibuya.github.io/blog/2022-11-27-longformer-2020/index.html; Kripner notes: https://www.kripner.com/2004.05150-Longformer/)
  - Kripner notes “Best results were achieved when \(w\) is increasing from … 32 to 512” and dilation factor increasing “from 0 to 3.” (Kripner notes URL above)  
    - These are secondary notes about the Longformer paper; the search results do not include the original Longformer paper text.

- **NVIDIA cuDNN Frontend SDPA (FlashAttention-2) interface facts**
  - cuDNN “Scaled Dot Product Attention FP16/BF16 Forward” computes \(\text{softmax}(QK^T/\sqrt{d})V\) “using the FlashAttention-2 algorithm.” (NVIDIA cuDNN Frontend docs: https://docs.nvidia.com/deeplearning/cudnn/frontend/v1.11.0/operations/Attention.html)
  - Configurable options include:
    - `attn_scale` (default **1.0**) to scale scores before softmax.
    - Bias mask (additive), ALiBi mask (additive), padding mask via per-batch sequence lengths, causal mask that fills upper triangular with negative infinity. (NVIDIA docs URL above)
  - Tensor shapes (examples):
    - \(Q: (B, H_q, S_q, D_{qk})\), \(K: (B, H_k, S_{kv}, D_{qk})\), \(V: (B, H_v, S_{kv}, D_v)\) for FP16/BF16. (NVIDIA docs URL above)

---

## Technical Details & Procedures

- **Transformer scaled dot-product attention computation (matrix form)**
  - Pack queries, keys, values into matrices \(Q,K,V\); compute:
    1. Scores: \(QK^T\)
    2. Scale: divide by \(\sqrt{d_k}\)
    3. Softmax over key dimension to get weights
    4. Output: weights \(\times V\) (Vaswani et al., 2017, §3.2.1: https://arxiv.org/html/1706.03762v7)

- **Decoder causal masking procedure (paper)**
  - Implement inside scaled dot-product attention by “masking out (setting to \(-\infty\)) all values in the input of the softmax which correspond to illegal connections.” (Vaswani et al., 2017: https://arxiv.org/html/1706.03762v7)

- **PyTorch: `nn.MultiheadAttention` usage and exact parameter names**
  - Instantiate:
    ```python
    torch.nn.MultiheadAttention(
        embed_dim, num_heads, dropout=0.0, bias=True,
        add_bias_kv=False, add_zero_attn=False,
        kdim=None, vdim=None, batch_first=False,
        device=None, dtype=None
    )
    ```
    (PyTorch docs: https://docs.pytorch.org/docs/stable/generated/torch.nn.MultiheadAttention.html)
  - Forward:
    ```python
    attn_output, attn_output_weights = mha(
        query, key, value,
        key_padding_mask=None,
        need_weights=True,
        attn_mask=None,
        average_attn_weights=True,
        is_causal=False
    )
    ```
    (PyTorch docs URL above)
  - Mask shapes and meanings:
    - `key_padding_mask`: shape \((N,S)\); `True` indicates ignore (padding). (PyTorch docs URL above)
    - `attn_mask`: shape \((L,S)\) or \((N*num_heads,L,S)\). (PyTorch docs URL above)
    - If both masks are supplied, “their types should match.” (PyTorch docs URL above)
  - Performance procedure:
    - Set `need_weights=False` to use optimized `scaled_dot_product_attention` “and achieve the best performance.” (PyTorch docs URL above)

- **PyTorch: `F.scaled_dot_product_attention` exact call signature and key behaviors**
  - Signature:
    ```python
    torch.nn.functional.scaled_dot_product_attention(
        query, key, value,
        attn_mask=None,
        dropout_p=0.0,
        is_causal=False,
        scale=None,
        enable_gqa=False
    )
    ```
    (PyTorch docs: https://docs.pytorch.org/docs/stable/generated/torch.nn.functional.scaled_dot_product_attention.html)
  - Causal masking:
    - If `is_causal=True`, it asserts `attn_mask is None` and applies a lower-triangular mask by filling non-allowed positions with `-inf` in `attn_bias`. (PyTorch docs URL above)
  - Boolean vs float `attn_mask` semantics (important nuance):
    - In this function, boolean mask: `True` indicates the element *should take part in attention*; it masks where `logical_not()` is true. (PyTorch docs URL above)
    - Float mask: added to attention scores. (PyTorch docs URL above)
  - Dropout procedure:
    - The reference code applies `torch.dropout(attn_weight, dropout_p, train=True)` unconditionally; docs warn dropout is always applied according to `dropout_p`, so callers must pass `0.0` when not training. (PyTorch docs URL above)

- **cuDNN Frontend SDPA configuration knobs (names and defaults)**
  - `attn_scale`: default **1.0**; can be set to \(1/\sqrt{d}\). (NVIDIA cuDNN Frontend docs: https://docs.nvidia.com/deeplearning/cudnn/frontend/v1.11.0/operations/Attention.html)
  - Causal mask configuration described as filling upper triangular with \(-\infty\); can be set via:
    - `set_diagonal_band_right_bound(0)` and `set_diagonal_alignment(DiagonalAlignment_t::TOP_LEFT)` (NVIDIA docs URL above)

- **Masked softmax with valid lengths (D2L implementation)**
  - D2L masks beyond valid lengths by setting them to a “very large negative value” **-1e6** before softmax. (D2L, “Attention Scoring Functions”: https://d2l.ai/chapter_attention-mechanisms-and-transformers/attention-scoring-functions.html)

---

## Comparisons & Trade-offs

- **Additive vs dot-product attention (Transformer paper)**
  - Two commonly used functions: additive attention and dot-product attention. (Vaswani et al., 2017: https://arxiv.org/html/1706.03762v7)
  - Complexity: “similar in theoretical complexity,” but dot-product attention is “much faster and more space-efficient in practice” because it can use optimized matrix multiplication. (Vaswani et al., 2017: https://arxiv.org/html/1706.03762v7)
  - Performance vs dimension:
    - For small \(d_k\): similar.
    - Additive attention “outperforms dot product attention without scaling for larger values of \(d_k\).” (Vaswani et al., 2017: https://arxiv.org/html/1706.03762v7)
  - Scaled dot-product attention adds \(1/\sqrt{d_k}\) to address softmax small-gradient issues at large \(d_k\). (Vaswani et al., 2017: https://arxiv.org/html/1706.03762v7)

- **Dense attention vs FlashAttention (exactness, memory, speed)**
  - Dense attention materializes \(N\times N\) attention matrices; time and memory are quadratic in sequence length. (Dao et al., 2022: https://arxiv.org/abs/2205.14135)
  - FlashAttention is **exact** attention but IO-aware; reduces HBM traffic via tiling and kernel fusion. (Dao et al., 2022: https://arxiv.org/abs/2205.14135)
  - Reported speedups (paper abstract):
    - 15% end-to-end on BERT-large (512), 3× on GPT-2 (1K), 2.4× on LRA (1K–4K). (Dao et al., 2022: https://arxiv.org/abs/2205.14135)

- **Full attention \(O(n^2)\) vs sliding-window attention \(O(nw)\) (Longformer summaries)**
  - Sliding window reduces complexity from \(O(n^2)\) to \(O(n\cdot w)\) for window size \(w\). (Naoki Shibuya blog summary: https://naokishibuya.github.io/blog/2022-11-27-longformer-2020/index.html; Kripner notes: https://www.kripner.com/2004.05150-Longformer/)
  - Trade-off described in a video summary: small window may require many layers to achieve global receptive field; dilated windows increase receptive field. (YouTube explainer transcript: https://www.youtube.com/watch?v=it0iZ93aLs4)  
    - Note: this is a secondary explanation, not the paper.

- **Mask semantics mismatch: `nn.MultiheadAttention` vs `F.scaled_dot_product_attention`**
  - `nn.MultiheadAttention`: boolean mask `True` means “ignored.” (PyTorch docs: https://docs.pytorch.org/docs/stable/generated/torch.nn.MultiheadAttention.html)
  - `F.scaled_dot_product_attention`: boolean mask `True` means “should take part in attention.” (PyTorch docs: https://docs.pytorch.org/docs/stable/generated/torch.nn.functional.scaled_dot_product_attention.html)
  - Trade-off: mixing these APIs without adapting mask polarity can silently produce incorrect behavior.

- **Float masks in PyTorch fast path: potential regression**
  - A PyTorch GitHub issue reports that in some inference fast-path scenario, passing a float `attn_mask` to `nn.MultiheadAttention` produced `nan` attention scores, while a bool mask worked. (PyTorch issue #107084: https://github.com/pytorch/pytorch/issues/107084)  
    - This is a bug report; treat as an implementation caveat rather than a guaranteed behavior.

---

## Architecture & Design Rationale

- **Attention as query-to-key compatibility + weighted sum of values**
  - The Transformer paper defines attention as mapping a query and a set of key-value pairs to an output, computed as a weighted sum of values; weights come from a compatibility function between query and key. (Vaswani et al., 2017, §3.2: https://arxiv.org/html/1706.03762v7)

- **Why scaling is tied to \(d_k\)**
  - Under the i.i.d. assumption (mean 0, variance 1), dot-product variance grows with \(d_k\); scaling by \(1/\sqrt{d_k}\) counteracts this so softmax doesn’t saturate into tiny-gradient regimes. (Vaswani et al., 2017: https://arxiv.org/html/1706.03762v7; ApX ML: https://apxml.com/courses/foundations-transformers-architecture/chapter-2-attention-mechanism-core-concepts/scaled-dot-product-attention)

- **Why multi-head uses smaller per-head dimensions**
  - The paper sets \(d_k=d_v=d_{model}/h\) (example value 64) and notes reduced per-head dimension keeps total computational cost similar to single-head attention with full dimensionality (quoted in a DeepLearning.AI forum answer referencing the paper). (Vaswani et al., 2017: https://arxiv.org/html/1706.03762v7; DeepLearning.AI community thread: https://community.deeplearning.ai/t/multiheaded-attention-number-of-heads-and-dim-of-heads/317195)

- **Why dot-product attention is favored in practice**
  - Dot-product attention can be implemented with highly optimized matrix multiplication, making it faster and more space-efficient than additive attention in practice, despite similar theoretical complexity. (Vaswani et al., 2017: https://arxiv.org/html/1706.03762v7)

- **Why IO-awareness matters for long-context attention**
  - FlashAttention argues many approximate methods reduce compute complexity but “often do not achieve wall-clock speedup”; the missing principle is IO-awareness (HBM↔SRAM traffic). (Dao et al., 2022: https://arxiv.org/abs/2205.14135)

- **RoPE design intent (relative position via rotations)**
  - EleutherAI’s RoPE blog explains the intuition: represent embeddings as complex numbers and positions as rotations applied to queries and keys; shifting both by the same amount preserves relative angles and thus dot products depend on relative position. (EleutherAI blog: https://blog.eleuther.ai/rotary-embeddings/)
  - RoFormer paper abstract states RoPE encodes absolute position with a rotation matrix while incorporating explicit relative position dependency in self-attention, and claims properties including “flexibility of sequence length” and ability to equip linear self-attention with relative position encoding. (Su et al., 2021: https://arxiv.org/abs/2104.09864)

---

## Common Questions & Answers

- **Q: What exactly is “scaled dot-product attention”?**
  - A: It computes \(\mathrm{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V\), where \(Q,K\) have dimension \(d_k\) and \(V\) has dimension \(d_v\). (Vaswani et al., 2017: https://arxiv.org/html/1706.03762v7)

- **Q: Why do we divide by \(\sqrt{d_k}\) and not \(d_k\)?**
  - A: The paper’s illustration assumes components of \(q\) and \(k\) are i.i.d. with mean 0 and variance 1; then \(q\cdot k\) has variance \(d_k\). Scaling by \(1/\sqrt{d_k}\) counteracts the growth in magnitude that would push softmax into very small-gradient regions. (Vaswani et al., 2017: https://arxiv.org/html/1706.03762v7)

- **Q: How does the Transformer prevent the decoder from “seeing the future”?**
  - A: It masks illegal connections in decoder self-attention by setting corresponding softmax inputs to \(-\infty\), so each position can attend only to earlier positions (and itself). (Vaswani et al., 2017: https://arxiv.org/html/1706.03762v7)

- **Q: In PyTorch `nn.MultiheadAttention`, what shapes should my tensors have?**
  - A: With `batch_first=False` (default), `query` is \((L,N,E_q)\), `key`/`value` are \((S,N,E_k/E_v)\). With `batch_first=True`, they are \((N,L,E_q)\) and \((N,S,E_k/E_v)\). (PyTorch docs: https://docs.pytorch.org/docs/stable/generated/torch.nn.MultiheadAttention.html)

- **Q: In PyTorch `nn.MultiheadAttention`, what does `key_padding_mask` do and what shape is it?**
  - A: It is a mask of shape \((N,S)\) indicating which `key` positions to ignore as padding. For a binary mask, `True` means the corresponding key value is ignored. (PyTorch docs: https://docs.pytorch.org/docs/stable/generated/torch.nn.MultiheadAttention.html)

- **Q: What’s the difference between `attn_mask` and `key_padding_mask` in PyTorch MHA?**
  - A: `attn_mask` prevents attention to certain positions and must be shape \((L,S)\) or \((N\cdot \text{num\_heads},L,S)\). `key_padding_mask` is shape \((N,S)\) and masks padding tokens in the key. (PyTorch docs: https://docs.pytorch.org/docs/stable/generated/torch.nn.MultiheadAttention.html)

- **Q: Why do my boolean masks behave differently between `nn.MultiheadAttention` and `F.scaled_dot_product_attention`?**
  - A: The documented semantics differ:
    - `nn.MultiheadAttention`: boolean `True` means “ignored.” (PyTorch MHA docs: https://docs.pytorch.org/docs/stable/generated/torch.nn.MultiheadAttention.html)
    - `F.scaled_dot_product_attention`: boolean `True` means the element “should take part in attention.” (PyTorch SDPA docs: https://docs.pytorch.org/docs/stable/generated/torch.nn.functional.scaled_dot_product_attention.html)

- **Q: How do I ensure SDPA dropout is disabled at evaluation time?**
  - A: PyTorch warns SDPA “always applies dropout” according to `dropout_p`; to disable in eval, pass `dropout_p=0.0` when `self.training` is false (example provided in docs). (PyTorch SDPA docs: https://docs.pytorch.org/docs/stable/generated/torch.nn.functional.scaled_dot_product_attention.html)

- **Q: What is the sinusoidal positional encoding formula?**
  - A: \(PE_{(pos,2i)}=\sin\left(\frac{pos}{10000^{2i/d_{model}}}\right)\), \(PE_{(pos,2i+1)}=\cos\left(\frac{pos}{10000^{2i/d_{model}}}\right)\). (ApX Machine Learning: https://apxml.com/courses/foundations-transformers-architecture/chapter-4-positional-encoding-embedding-layer/sinusoidal-encoding-formulation)

- **Q: What does FlashAttention change—does it approximate attention?**
  - A: The FlashAttention paper describes it as an “IO-aware exact attention algorithm” that reduces HBM↔SRAM memory reads/writes via tiling; it reports speedups (e.g., 3× on GPT-2 at seq length 1K) while computing exact attention. (Dao et al., 2022: https://arxiv.org/abs/2205.14135)

- **Q: How does sliding-window attention reduce complexity compared to full attention?**
  - A: In Longformer summaries, each token attends only within a window of size \(w\), giving complexity \(O(n\cdot w)\) instead of \(O(n^2)\). (Naoki Shibuya blog summary: https://naokishibuya.github.io/blog/2022-11-27-longformer-2020/index.html; Kripner notes: https://www.kripner.com/2004.05150-Longformer/)