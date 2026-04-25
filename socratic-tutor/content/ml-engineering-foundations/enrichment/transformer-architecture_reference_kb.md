## Key Facts & Specifications

### Original Transformer (Vaswani et al., 2017)
- **Layer counts**
  - Encoder: stack of **N = 6** identical layers. (Vaswani et al., 2017, https://arxiv.org/html/1706.03762v7)
  - Decoder: stack of **N = 6** identical layers. (Vaswani et al., 2017, https://arxiv.org/html/1706.03762v7)
- **Sublayers per layer**
  - Encoder layer has **2 sublayers**: (1) multi-head self-attention, (2) position-wise feed-forward network. (Vaswani et al., 2017, https://arxiv.org/html/1706.03762v7)
  - Decoder layer has **3 sublayers**: masked self-attention, encoder-decoder attention (cross-attention), and feed-forward. (Vaswani et al., 2017, https://arxiv.org/html/1706.03762v7)
- **Residual + LayerNorm placement (Post-LN in paper text)**
  - Paper states: output of each sublayer is **`LayerNorm(x + Sublayer(x))`**. (Vaswani et al., 2017, https://arxiv.org/html/1706.03762v7)
- **Model dimension constraint**
  - “To facilitate these residual connections, all sub-layers … produce outputs of dimension **d_model = 512**.” (Vaswani et al., 2017, https://arxiv.org/html/1706.03762v7)
- **Dropout**
  - “For the base model, we use a rate of **P_drop = 0.1**.” (Vaswani et al., 2017, https://arxiv.org/html/1706.03762v7)

### Pre-LN vs Post-LN discrepancy (paper figure vs code)
- A secondary source notes a mismatch: the **paper figure** suggests Post-LN, while the **“updated code implementation”** defaults to **Pre-LN**. (Raschka, “Why the original Transformer figure…”, referencing Xiong et al., 2020 and Vaswani et al., 2017: https://magazine.sebastianraschka.com/p/why-the-original-transformer-figure)
- Pre-LN and Post-LN formulas (as explicitly stated):
  - Post-LN: **`LayerNorm(x + SubLayer(x))`**
  - Pre-LN: **`x + SubLayer(LayerNorm(x))`** (ApX, “Pre-LN vs Post-LN”, https://apxml.com/courses/foundations-transformers-architecture/chapter-6-advanced-architectural-variants-analysis/pre-ln-vs-post-ln)

### PyTorch `nn.MultiheadAttention` (masking, shapes, performance knobs)
- **Input shapes**
  - `query` shape:
    - Unbatched: **(L, E_q)**
    - Batched, `batch_first=False`: **(L, N, E_q)**
    - Batched, `batch_first=True`: **(N, L, E_q)**  
  (PyTorch docs, https://docs.pytorch.org/docs/stable/generated/torch.nn.MultiheadAttention.html)
- **`key_padding_mask` shape**
  - Batched: **(N, S)**; unbatched: **(S)**. (PyTorch docs, same URL)
- **`attn_mask` shape**
  - 2D: **(L, S)** or 3D: **(N·num_heads, L, S)**. (PyTorch docs, same URL)
- **Mask type compatibility**
  - If both `attn_mask` and `key_padding_mask` are supplied, **their types should match**. (PyTorch docs, same URL)
- **Attention weights shape**
  - If `average_attn_weights=False`, per-head weights:
    - Unbatched: **(num_heads, L, S)**
    - Batched: **(N, num_heads, L, S)**  
  (PyTorch docs, same URL)
- **Performance note**
  - Set **`need_weights=False`** to use optimized **`scaled_dot_product_attention`** for best performance. (PyTorch docs, same URL)
- **Causal hint**
  - `is_causal` “provides a hint that `attn_mask` is the causal mask.” (PyTorch docs, same URL)

### PyTorch `nn.LayerNorm` defaults and math
- Constructor signature includes defaults: **`eps=1e-05`**, **`elementwise_affine=True`**, **`bias=True`**. (PyTorch docs, https://docs.pytorch.org/docs/stable/generated/torch.nn.LayerNorm.html)
- Mean/variance computed over last **D** dimensions defined by `normalized_shape`. (PyTorch docs, same URL)
- Variance uses **biased estimator**: equivalent to `torch.var(input, correction=0)`. (PyTorch docs, same URL)
- If `elementwise_affine=True`, parameters initialized:
  - `weight` initialized to **1**
  - `bias` initialized to **0**  
  (PyTorch docs, same URL)

### FFN intermediate dimension (4× example)
- A reference article states: original Transformer used **4× expansion**, with **d_model=512** and **d_ff=2048**. (Brenndoerfer, “Feed-Forward Networks in Transformers…”, https://mbrenndoerfer.com/writing/transformer-feed-forward-networks)

### BERT MLM masking rates and 80-10-10
- BERT-style MLM procedure described in a discussion referencing the original BERT paper:
  - Mask **15%** of tokens.
  - Of selected tokens: **80%** replaced with `[MASK]`, **10%** replaced with random word, **10%** unchanged. (Hugging Face forum thread, https://discuss.huggingface.co/t/bert-mlm-80-mask-10-random-words-and-10-same-word-how-does-this-work/17867)
- Research revisiting masking rate:
  - “Masking **40%** outperforms **15%** for **BERT-large** size models on **GLUE** and **SQuAD**.” (EACL 2023 paper, https://aclanthology.org/2023.eacl-main.217.pdf)
  - “Masking rate of **80%** can still preserve **95%** fine-tuning performance…” (same EACL 2023 paper)
  - The paper reports that BERT’s **80-10-10 corruption strategy** “does not perform better for most downstream tasks” and they “simply replace all the masked tokens with `[MASK]` by default.” (same EACL 2023 paper)

### Scaling laws (Kaplan 2020; Hoffmann/Chinchilla 2022)
- Kaplan et al. (2020): cross-entropy loss scales as a **power-law** with **model size**, **dataset size**, and **compute**; trends span “**more than seven orders of magnitude**.” (Kaplan et al., 2020, https://arxiv.org/abs/2001.08361)
- Chinchilla (Hoffmann et al., 2022):
  - Trained “**over 400** language models” ranging from **70M to >16B parameters**, on **5B to 500B tokens**. (Hoffmann et al., 2022 PDF, https://s10251.pcdn.co/pdf/2022-hoffman-chinchilla.pdf)
  - Compute-optimal rule: “for every **doubling** of model size the number of training tokens should also be **doubled**.” (Hoffmann et al., 2022 PDF)
  - Chinchilla verification: trained a **70B** model on **1.4 trillion tokens** (and notes it used same compute budget as Gopher). (Hoffmann et al., 2022 PDF)

### FlashAttention (Dao et al., 2022)
- FlashAttention is an **exact** attention algorithm that is **IO-aware** and uses **tiling** to reduce HBM↔SRAM reads/writes. (Dao et al., 2022, https://arxiv.org/abs/2205.14135)
- Reported speedups:
  - **15%** end-to-end wall-clock speedup on **BERT-large** (seq length **512**) vs MLPerf 1.1 training speed record.
  - **3×** speedup on **GPT-2** (seq length **1K**).
  - **2.4×** speedup on **Long Range Arena** (seq length **1K–4K**).  
  (Dao et al., 2022, https://arxiv.org/abs/2205.14135)
- Block-sparse FlashAttention:
  - “**2–4×** faster than even FlashAttention,” scaling to **sequence length 64K**. (Dao et al., 2022, ar5iv HTML mirror: https://ar5iv.labs.arxiv.org/html/2205.14135)
- Open-source code link: https://github.com/HazyResearch/flash-attention (Dao et al., 2022, ar5iv mirror)

### KV cache (Hugging Face Transformers docs)
- KV cache purpose: store KV pairs from previously processed tokens to avoid recomputation; “Caching should only be used for **inference**.” (HF docs, https://github.com/huggingface/transformers/blob/main/docs/source/en/cache_explanation.md)
- When concatenating past and current KV:
  - Attention weights shape becomes **`(new_tokens_length, past_kv_length + new_tokens_length)`**. (HF docs, same URL)
  - Attention mask should match combined length: **`(batch_size, past_kv_length + new_tokens_length)`**. (HF docs, same URL)
- Default cache class: **`DynamicCache`** is default for most models; disable with **`use_cache=False`** in `generate()`. (HF docs, https://github.com/huggingface/transformers/blob/main/docs/source/en/kv_cache.md)

### Tokenization / BPE (Sennrich-style and OpenAI tiktoken)
- BPE hyperparameter: **number of merge operations** governs vocabulary size; final vocab size equals **initial vocab size + number of merges**. (RWS blog, https://www.rws.com/language-weaver/blog/issue-121-finding-the-optimal-vocabulary-size-for-neural-machine-translation/)
- `subword-nmt`:
  - `apply_bpe.py` accepts `--vocabulary` (and other args) to prevent edge cases with multi-language BPE learning. (subword-nmt repo, https://github.com/rsennrich/subword-nmt)
  - Byte-level BPE can be enabled with `--bytes` when learning BPE; whether bytes/chars are used is stored in the first line of the BPE file. (subword-nmt repo, same URL)
  - New-style BPE files identified by first line: **`#version: 0.2`**. (subword-nmt repo, same URL)
- `tiktoken`:
  - “fast BPE tokeniser for use with OpenAI’s models.” (tiktoken GitHub, https://github.com/openai/tiktoken)
  - Performance claim: **3–6× faster** than a comparable open-source tokenizer in a benchmark described in the README. (tiktoken GitHub, same URL)
  - BPE properties listed: reversible/lossless; works on arbitrary text; “On average… each token corresponds to about **4 bytes**.” (tiktoken GitHub, same URL)
- OpenAI token counting heuristics (English rule-of-thumb):
  - **1 token ≈ 4 characters**
  - **1 token ≈ ¾ of a word**
  - **100 tokens ≈ 75 words**
  - **~1,500 words ≈ 2,048 tokens**  
  (OpenAI Help Center, https://help.openai.com/en/articles/4936856-what-are-tokens-and-how-to-count-them)

---

## Technical Details & Procedures

### Post-LN vs Pre-LN computation (explicit formulas)
- Post-LN sublayer:
  - `LayerNorm(x + SubLayer(x))` (Vaswani et al., 2017, https://arxiv.org/html/1706.03762v7; also summarized at ApX)
- Pre-LN sublayer:
  - `x + SubLayer(LayerNorm(x))` (ApX, https://apxml.com/courses/foundations-transformers-architecture/chapter-6-advanced-architectural-variants-analysis/pre-ln-vs-post-ln)

### PyTorch `nn.MultiheadAttention` forward signature and mask configuration
- Forward signature includes:
  - `forward(query, key, value, key_padding_mask=None, need_weights=True, attn_mask=None, average_attn_weights=True, is_causal=False)`  
  (PyTorch docs, https://docs.pytorch.org/docs/stable/generated/torch.nn.MultiheadAttention.html)
- Mask shapes (must match docs exactly):
  - `key_padding_mask`: (N, S) (or (S) unbatched)
  - `attn_mask`: (L, S) or (N·num_heads, L, S)  
  (PyTorch docs, same URL)
- Combining masks:
  - `merge_masks(attn_mask, key_padding_mask, query)` expands both to `(batch_size, num_heads, seq_len, seq_len)` and combines with logical `or`. (PyTorch docs, same URL)
- Performance procedure:
  - Use `need_weights=False` to enable optimized `scaled_dot_product_attention`. (PyTorch docs, same URL)

### Example causal self-attention masking (explicit code pattern)
- A decoder-only causal mask implementation (nanoGPT-style) registers a lower-triangular mask and applies it by filling masked positions with `-inf` before softmax:
  - `self.register_buffer("mask", torch.tril(torch.ones(T, T)).view(1, 1, T, T))`
  - `att = att.masked_fill(self.mask[:,:,:T,:T] == 0, float('-inf'))`
  - `att = F.softmax(att, dim=-1)`  
  (Wolfe article quoting nanoGPT code, https://cameronrwolfe.substack.com/p/decoder-only-transformers-the-workhorse)

### Hugging Face: using `past_key_values` + attention masks correctly in `forward`
- In an iterative `forward` loop with `past_key_values`, you should pass **only the new, unprocessed input ids** (example given: `input_ids = [[7]]`), while the **attention mask must cover past + present** because keys/values are concatenated. (HF GitHub issue #34835, comment, https://github.com/huggingface/transformers/issues/34835)
- Mask shapes mentioned in the issue comment:
  - 2D mask: **`[bs, 7]`**
  - or 4D mask: **`[bs, heads, 1, 7]`**  
  (HF issue #34835, same URL)
- For `generate()`, the guidance differs: pass the whole concatenated input; `generate()` “will take care of cropping already processed ids.” (HF issue #34835, same URL)

### LayerNorm configuration parameters (PyTorch)
- `torch.nn.LayerNorm(normalized_shape, eps=1e-05, elementwise_affine=True, bias=True, ...)` (PyTorch docs, https://docs.pytorch.org/docs/stable/generated/torch.nn.LayerNorm.html)
- Variance computation: `torch.var(input, correction=0)` (PyTorch docs, same URL)

### `tiktoken` basic usage (exact snippet)
- Example from README:
  ```python
  import tiktoken
  enc = tiktoken.get_encoding("o200k_base")
  assert enc.decode(enc.encode("hello world")) == "hello world"
  enc = tiktoken.encoding_for_model("gpt-4o")
  ```
  (tiktoken GitHub, https://github.com/openai/tiktoken)

### Disabling KV cache in Hugging Face `generate()`
- Example:
  ```python
  model.generate(**inputs, do_sample=False, max_new_tokens=20, use_cache=False)
  ```
  (HF docs, https://github.com/huggingface/transformers/blob/main/docs/source/en/kv_cache.md)

---

## Comparisons & Trade-offs

### Post-LN vs Pre-LN (training stability vs tuning)
- ApX comparison table claims:
  - Post-LN: “Less stable, especially in deep models”; often requires careful LR warmup.
  - Pre-LN: “More stable, facilitates deeper model training”; less sensitive to LR warmup.  
  (ApX, https://apxml.com/courses/foundations-transformers-architecture/chapter-6-advanced-architectural-variants-analysis/pre-ln-vs-post-ln)
- Another secondary source (MachineLearningMastery) similarly states:
  - Post-norm can be unstable for very deep models; pre-norm more robust; post-norm may perform better if successfully trained. (MachineLearningMastery, https://machinelearningmastery.com/skip-connections-in-transformer-models/)
- Discrepancy note:
  - Raschka article highlights ongoing debate and mismatch between paper figure and code defaults. (Raschka, https://magazine.sebastianraschka.com/p/why-the-original-transformer-figure)

### FlashAttention vs standard attention / approximate attention
- FlashAttention motivation: many approximate methods reduce FLOPs but “do not display wall-clock speedup” due to IO overhead; FlashAttention targets IO (HBM access). (Dao et al., 2022, https://ar5iv.labs.arxiv.org/html/2205.14135)
- Benchmarks (reported):
  - FlashAttention: up to **3×** faster than standard attention for sequence lengths **128–2K**, and scales to **64K**. (Dao et al., 2022, ar5iv mirror)
  - For seq length beyond **1K**, some approximate methods (e.g., Linformer) “start to become faster” (as stated in the paper), while block-sparse FlashAttention is claimed faster than approximate methods known to authors. (Dao et al., 2022, ar5iv mirror)
- End-to-end training speedups (reported): **15%** (BERT-large 512), **3×** (GPT-2 1K), **2.4×** (LRA 1K–4K). (Dao et al., 2022, https://arxiv.org/abs/2205.14135)

### MLM masking strategies: 80-10-10 vs all-[MASK]
- EACL 2023 paper reports:
  - They “simply replace all the masked tokens with `[MASK]` by default.”
  - The “80-10-10 corruption strategy does not perform better for most downstream tasks.” (EACL 2023, https://aclanthology.org/2023.eacl-main.217.pdf)
- This contrasts with the commonly cited BERT recipe (15% with 80-10-10). (HF forum thread, https://discuss.huggingface.co/t/bert-mlm-80-mask-10-random-words-and-10-same-word-how-does-this-work/17867)

### Scaling laws: Kaplan (2020) vs Chinchilla (2022)
- Kaplan (2020): emphasizes compute-optimal training can involve “training very large models on a relatively modest amount of data and stopping significantly before convergence.” (Kaplan et al., 2020, https://arxiv.org/abs/2001.08361)
- Hoffmann/Chinchilla (2022): argues many LLMs are under-trained; compute-optimal frontier suggests scaling **tokens and parameters equally** (doubling N ⇒ doubling D), and demonstrates 70B on 1.4T tokens. (Hoffmann et al., 2022 PDF, https://s10251.pcdn.co/pdf/2022-hoffman-chinchilla.pdf)
- Hoffmann et al. explicitly contrast Kaplan’s suggested scaling under 10× compute:
  - Kaplan suggestion (as quoted in Chinchilla PDF): model size **5.5×**, tokens **1.8×**.
  - Hoffmann et al.: instead scale model size and tokens in **equal proportions**. (Hoffmann et al., 2022 PDF)

### Token counting: heuristics vs exact tokenizer
- OpenAI provides heuristics (English): 1 token ≈ 4 characters, etc. (OpenAI Help Center, https://help.openai.com/en/articles/4936856-what-are-tokens-and-how-to-count-them)
- `tiktoken` provides exact BPE encoding and claims 3–6× speed vs a comparable open-source tokenizer in a specific benchmark. (tiktoken GitHub, https://github.com/openai/tiktoken)

---

## Architecture & Design Rationale

### Why residual connections + LayerNorm are used (as described in sources)
- Original Transformer: residual connection around each sublayer, followed by LayerNorm: `LayerNorm(x + Sublayer(x))`. (Vaswani et al., 2017, https://arxiv.org/html/1706.03762v7)
- Residual/skip connections rationale (secondary source):
  - Provide direct paths for gradients; mitigate vanishing gradients; “+1 term ensures gradient doesn’t diminish…” (MachineLearningMastery, https://machinelearningmastery.com/skip-connections-in-transformer-models/)
- LayerNorm rationale (secondary source):
  - Stabilizes hidden state dynamics by normalizing activations across feature dimension per position; improves gradient flow; placement affects stability. (ApX, https://apxml.com/courses/foundations-transformers-architecture/chapter-6-advanced-architectural-variants-analysis/pre-ln-vs-post-ln)

### Why FFN expands hidden dimension (4× example)
- FFN provides nonlinearity; attention outputs are weighted averages (linear/convex combination after softmax), so FFN adds expressive nonlinear transformation per token. (Brenndoerfer, https://mbrenndoerfer.com/writing/transformer-feed-forward-networks)
- Expansion rationale (as stated): wider hidden layers increase expressiveness; expand to higher-dimensional space then project back to enable richer transformations; output must return to `d_model` for residual addition. (Brenndoerfer, same URL)
- Concrete original example: `d_model=512`, `d_ff=2048` (4×). (Brenndoerfer, same URL)

### Why causal masking is implemented with `-inf` above diagonal
- Decoder-only masked self-attention: set values above diagonal of attention matrix to **negative infinity** before softmax to prevent attending to future tokens. (Wolfe article, https://cameronrwolfe.substack.com/p/decoder-only-transformers-the-workhorse)

### Encoder-decoder cross-attention as the “bridge”
- Cross-attention uses:
  - Queries from decoder state; Keys/Values from encoder outputs. (ApX cross-attention, https://apxml.com/courses/foundations-transformers-architecture/chapter-5-encoder-decoder-stacks/encoder-decoder-cross-attention; also Brenndoerfer cross-attention article)
- Placement:
  - In original architecture: masked self-attention → cross-attention → FFN within each decoder layer. (Brenndoerfer cross-attention, https://mbrenndoerfer.com/writing/cross-attention-encoder-decoder-transformers)
- Efficiency rationale:
  - Encoder output computed once and reused in every decoder layer; decoder doesn’t recompute encoder each step. (Brenndoerfer cross-attention, same URL)

### Why KV caching works for causal attention
- HF cache explanation: once a token is processed under causal masking, its representation “never changes with respect to future tokens,” so past K/V can be cached and reused. (HF docs, https://github.com/huggingface/transformers/blob/main/docs/source/en/cache_explanation.md)

### Why FlashAttention focuses on IO (HBM access)
- FlashAttention paper argues approximate methods often fail to yield wall-clock speedups because they ignore memory access overhead; FlashAttention reduces HBM reads/writes via tiling and kernel fusion. (Dao et al., 2022, https://ar5iv.labs.arxiv.org/html/2205.14135)

---

## Common Questions & Answers

### Q1: “Did the original Transformer use Pre-LN or Post-LN?”
- The **paper text** states Post-LN: **`LayerNorm(x + Sublayer(x))`**. (Vaswani et al., 2017, https://arxiv.org/html/1706.03762v7)
- A secondary source reports a **discrepancy**: the paper figure suggests Post-LN, but the “updated code implementation” defaults to **Pre-LN**. (Raschka, https://magazine.sebastianraschka.com/p/why-the-original-transformer-figure)
- Conclusion for tutoring: cite that **paper text is Post-LN**, but note **implementation variants exist** and are debated.

### Q2: “What dropout rate did the original Transformer base model use?”
- **P_drop = 0.1** for the base model. (Vaswani et al., 2017, https://arxiv.org/html/1706.03762v7)

### Q3: “What are the exact mask shapes for PyTorch `nn.MultiheadAttention`?”
- `key_padding_mask`: **(N, S)** (or **(S)** unbatched). (PyTorch docs, https://docs.pytorch.org/docs/stable/generated/torch.nn.MultiheadAttention.html)
- `attn_mask`: **(L, S)** or **(N·num_heads, L, S)**. (PyTorch docs, same URL)

### Q4: “How do I get the fastest PyTorch MultiheadAttention?”
- PyTorch docs: set **`need_weights=False`** to use optimized **`scaled_dot_product_attention`** and achieve best performance. (PyTorch docs, https://docs.pytorch.org/docs/stable/generated/torch.nn.MultiheadAttention.html)

### Q5: “When using Hugging Face `past_key_values`, why does my attention mask shape need to change?”
- HF docs: attention concatenates past and current KV, so attention weights span **past_kv_length + new_tokens_length**; mask must match combined length: **(batch_size, past_kv_length + new_tokens_length)**. (HF docs, https://github.com/huggingface/transformers/blob/main/docs/source/en/cache_explanation.md)
- HF issue guidance: in `forward` with `past_key_values`, pass only new tokens (e.g., `[[7]]`), but mask must cover total length; can be **[bs, 7]** or **[bs, heads, 1, 7]** in the example. (HF issue #34835, https://github.com/huggingface/transformers/issues/34835)

### Q6: “What are LayerNorm’s default parameters in PyTorch, and how is variance computed?”
- Defaults: `eps=1e-05`, `elementwise_affine=True`, `bias=True`. (PyTorch docs, https://docs.pytorch.org/docs/stable/generated/torch.nn.LayerNorm.html)
- Variance: biased estimator `torch.var(..., correction=0)`. (PyTorch docs, same URL)

### Q7: “What FFN size did the original Transformer use?”
- Example cited: `d_model=512`, `d_ff=2048` (4× expansion). (Brenndoerfer, https://mbrenndoerfer.com/writing/transformer-feed-forward-networks)

### Q8: “What exactly is BERT’s 80-10-10 masking rule?”
- For the 15% selected tokens: **80%** `[MASK]`, **10%** random token, **10%** unchanged. (HF forum thread referencing BERT paper, https://discuss.huggingface.co/t/bert-mlm-80-mask-10-random-words-and-10-same-word-how-does-this-work/17867)
- Note: EACL 2023 paper reports this strategy “does not perform better for most downstream tasks” and uses all `[MASK]` by default. (EACL 2023, https://aclanthology.org/2023.eacl-main.217.pdf)

### Q9: “What did Chinchilla change compared to earlier scaling recommendations?”
- Hoffmann et al. (2022) find compute-optimal training scales **tokens and parameters equally** (doubling model size ⇒ doubling tokens) and validate with **70B parameters** trained on **1.4T tokens**. (Hoffmann et al., 2022 PDF, https://s10251.pcdn.co/pdf/2022-hoffman-chinchilla.pdf)
- They explicitly contrast Kaplan et al. (2020)’s quoted 10× compute scaling suggestion (model **5.5×**, tokens **1.8×**) with their equal-scaling finding. (Hoffmann et al., 2022 PDF)

### Q10: “What concrete speedups does FlashAttention report?”
- Reported: **15%** end-to-end speedup on BERT-large (seq **512**), **3×** on GPT-2 (seq **1K**), **2.4×** on Long Range Arena (seq **1K–4K**). (Dao et al., 2022, https://arxiv.org/abs/2205.14135)
- Block-sparse FlashAttention: **2–4×** faster than FlashAttention, scaling to **64K** sequence length. (Dao et al., 2022, https://ar5iv.labs.arxiv.org/html/2205.14135)