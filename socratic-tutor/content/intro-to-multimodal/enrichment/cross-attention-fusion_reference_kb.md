## Key Facts & Specifications

### Scaled Dot-Product Attention (core attention equation)
- Scaled dot-product attention is given by:  
  \[
  \text{Attention}(Q,K,V)=\text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V
  \]
  where \(d_k\) is the key/query dimensionality. (apxml “Scaled Dot-Product Attention Mechanism” URL: https://apxml.com/courses/introduction-to-transformer-models/chapter-2-self-attention-multi-head-attention/scaled-dot-product-attention; apxml “Softmax Function for Attention Weights” URL: https://apxml.com/courses/foundations-transformers-architecture/chapter-2-attention-mechanism-core-concepts/softmax-attention-weights)
- Softmax is applied **row-wise** to the score matrix so each query’s attention weights sum to **1**. (apxml “Softmax Function for Attention Weights” URL above)
- For a single query \(q_i\) and key \(k_j\), the scaled score is:  
  \[
  s_{ij}=\frac{q_i k_j^T}{\sqrt{d_k}}
  \]
  and the attention weight is:
  \[
  \alpha_{ij}=\frac{\exp(s_{ij})}{\sum_{l=1}^{N}\exp(s_{il})}
  \]
  where \(N\) is the key/value sequence length. (apxml “Softmax Function for Attention Weights” URL above)

### Multi-head attention definition (formal)
- Multi-head attention is defined as:  
  \[
  \text{MultiHead}(Q,K,V)=\text{Concat}(\text{head}_1,\dots,\text{head}_h)W^O
  \]
  with \(\text{head}_i=\text{Attention}(QW_i^Q,KW_i^K,VW_i^V)\). (PyTorch docs, `torch.nn.MultiheadAttention` https://docs.pytorch.org/docs/stable/generated/torch.nn.MultiheadAttention.html)

### Encoder–decoder cross-attention (what comes from where)
- In encoder–decoder cross-attention:
  - **Queries** come from the decoder state.
  - **Keys and values** come from the **output of the final encoder layer**. (apxml “Encoder-Decoder Cross-Attention” https://apxml.com/courses/foundations-transformers-architecture/chapter-5-encoder-decoder-stacks/encoder-decoder-cross-attention)

### BLIP-2 Q-Former: concrete architectural numbers
- Q-Former uses **32 queries**, each of dimension **768** (hidden dimension of Q-Former). Output query representation \(Z\) has size **32 × 768**. (Li et al., 2023 PDF https://www.nematilab.info/bmijc/assets/081823_paper.pdf)
- Example comparison of bottleneck sizes in the BLIP-2 paper:
  - Q-Former output: **32 × 768**
  - Frozen image features example: **257 × 1024** for **ViT-L/14**. (Li et al., 2023 PDF https://www.nematilab.info/bmijc/assets/081823_paper.pdf)
- Cross-attention layers in Q-Former are **inserted every other transformer block**. (Li et al., 2023 PDF https://www.nematilab.info/bmijc/assets/081823_paper.pdf)
- Q-Former initialization/training facts:
  - Q-Former is initialized with **BERTbase** pretrained weights; **cross-attention layers are randomly initialized**. (Li et al., 2023 PDF https://www.nematilab.info/bmijc/assets/081823_paper.pdf)
  - Q-Former contains **188M parameters** (queries are considered model parameters). (Li et al., 2023 PDF https://www.nematilab.info/bmijc/assets/081823_paper.pdf)

### ViT patch token counts (concrete example)
- For a **224×224** image with **16×16** patches:
  - Patch grid is **14×14**, yielding **196** patches/tokens.
  - Patch embedding matrix is **196×768**; after adding a `[cls]` token it becomes **197×768**. (A. Arora blog “ViT Explained” https://amaarora.github.io/posts/2021-01-18-ViT.html)
- Keras example also states: 224×224 with 16×16 patches gives **196 patches**. (Keras TokenLearner example https://keras.io/examples/vision/token_learner/)

### Flamingo: gated cross-attention facts and ablations (numbers)
- Flamingo conditions a frozen LM using **freshly initialized cross-attention layers** interleaved between pretrained LM layers. (Flamingo NeurIPS 2022 paper https://papers.neurips.cc/paper_files/paper/2022/file/960a172bc7fbf0177ccccbb411a7d800-Paper-Conference.pdf)
- Gated block formula (as shown in the paper):
  - \(y = y + \tanh(\alpha_{\text{xattn}})\cdot \text{attention}(q=y, kv=x)\)
  - \(y = y + \tanh(\alpha_{\text{dense}})\cdot \text{ffw}(y)\)  
  with \(\alpha\) a **learnable scalar initialized to 0**, so at initialization the model matches the pretrained LM output. (Flamingo NeurIPS 2022 paper URL above)
- Reported ablation outcomes (from course slides summarizing Flamingo):
  - Removing the “bridge” (gated cross-attention dense block) drops overall score by **4.2%** and training becomes unstable. (Group-Flamingo slides PDF https://llmsystem.github.io/llmsystem2024spring/assets/files/Group-Flamingo-98ae9c68fca94cd437716229a2cf42c1.pdf)
  - Inserting gated cross-attention dense blocks only **every 4th layer** increases computational efficiency by **66%** with **1.9%** performance loss. (Multimodal Language slides https://yumeng5.github.io/teaching/2024-spring-cs6501/multimodal.pdf; also echoed in Group-Flamingo slides PDF above)

### Llama 3.2 Vision: adapter + benchmarks + training compute (numbers)
- Llama 3.2 Vision uses a “vision adapter” consisting of a **series of cross-attention layers** feeding image encoder representations into the Llama 3.1 language model. (NVIDIA NIM overview https://docs.nvidia.com/nim/vision-language-models/1.2.0/examples/llama3-2/overview.html; Meta model card on GitHub https://github.com/meta-llama/llama-models/blob/main/models/llama3_2/MODEL_CARD_VISION.md)
- Context length: **128k** tokens. (NVIDIA NIM overview URL above; Meta model card URL above)
- Pretraining data volume: **6B image and text pairs**; knowledge cutoff **December 2023**. (NVIDIA NIM overview URL above; Meta model card URL above)
- Zero-shot benchmark numbers (base pretrained models):
  - VQAv2 (test-dev, 30k), 0-shot accuracy: **66.83** (11B) and **73.64** (90B)
  - TextVQA (val), 0-shot relaxed accuracy: **73.14** (11B) and **73.52** (90B)
  - DocVQA (val, unseen), 0-shot ANLS: **62.26** (11B) and **70.65** (90B)
  - MMMU (val), 0-shot micro avg accuracy: **41.67** (11B) and **49.33** (90B)  
  (NVIDIA NIM overview URL above)
- Training energy/computation reporting:
  - Total: **2.02M GPU hours** on **H100-80GB**, TDP **700W**. (NVIDIA NIM overview URL above; Meta model card URL above)
  - Stage breakdown examples:
    - 11B: Stage 1 pre-training **147K** hours; Stage 2 annealing **98K**; SFT **896**; RLHF **224**. (NVIDIA NIM overview URL above)
    - 90B: Stage 1 pre-training **885K**; Stage 2 annealing **885K**; SFT **3072**; RLHF **2048**. (NVIDIA NIM overview URL above)

### PyTorch `nn.MultiheadAttention`: key parameters and shapes (for cross-attention too)
- Constructor defaults:
  - `dropout=0.0`, `bias=True`, `add_bias_kv=False`, `add_zero_attn=False`, `kdim=None`, `vdim=None`, `batch_first=False`. (PyTorch 2.11 docs https://docs.pytorch.org/docs/stable/generated/torch.nn.MultiheadAttention.html)
- Forward signature:  
  `forward(query, key, value, key_padding_mask=None, need_weights=True, attn_mask=None, average_attn_weights=True, is_causal=False)` (PyTorch 2.11 docs URL above)
- Shapes (PyTorch 2.11 docs):
  - `query`: (L, Eq) unbatched; (L, N, Eq) if `batch_first=False`; (N, L, Eq) if `batch_first=True`
  - `key`: (S, Ek) unbatched; (S, N, Ek) if `batch_first=False`; (N, S, Ek) if `batch_first=True`
  - `key_padding_mask`: (N, S) (or (S) for unbatched query); `True` means ignore that key position (binary mask)
  - `attn_mask`: (L, S) or (N⋅num_heads, L, S)
  - Output `attn_output`: (L, E) unbatched; (L, N, E) or (N, L, E) depending on `batch_first`
  - Output `attn_output_weights` (if returned): averaged across heads by default; per-head if `average_attn_weights=False` (PyTorch 2.11 docs URL above)
- Performance note:
  - Setting `need_weights=False` enables using optimized `scaled_dot_product_attention` for best performance. (PyTorch 2.11 docs URL above)
- Fastpath inference conditions (self-attention only): fastpath is used iff `query`, `key`, and `value` are the same tensor plus additional constraints (batched 3D with `batch_first=True`, `.eval()`, no grad, etc.). (PyTorch 2.11 docs URL above)

### Hugging Face `past_key_values` (shapes and a discrepancy)
- In a Hugging Face issue describing `EncoderDecoderModel` outputs, `past_key_values` is described as:
  - List length `config.n_layers`, each tensor shape **(2, batch_size, num_heads, sequence_length, embed_size_per_head)**. (HF issue #7246 https://github.com/huggingface/transformers/issues/7246)
- Another discussion notes BART’s `past_key_values` is described differently:
  - Tuple of length `config.n_layers`, each tuple has **2 tuples**, each containing **2 tensors** of shape **(batch_size, num_heads, sequence_length - 1, embed_size_per_head)**. (Lightrun mirror of HF discussion https://lightrun.com/answers/huggingface-transformers-similar-usage-of-past_key_values-in-causallm-and-seq2seqlm)
- **Discrepancy note:** these two sources describe different container structures for `past_key_values` (list of tensors vs nested tuples) and slightly different sequence length conventions (sequence_length vs sequence_length-1). The search results do not reconcile them; treat as model-specific. (HF issue #7246 URL; Lightrun URL)

### MODA: quantified multimodal attention imbalance
- MODA paper reports:
  - “inconsistent attention across multiple layers” with **63% disparity** (as referenced to a figure in the paper)
  - attention score disparity across modalities can reach up to **10 times**
  - attention devoted to visual content is “significantly weaker” than textual modality
  - layer-by-layer decay can “accentuate” disparity  
  (MODA arXiv HTML https://arxiv.org/html/2507.04635v1)

---

## Technical Details & Procedures

### Implementing cross-attention with PyTorch `nn.MultiheadAttention`
- Cross-attention is performed by passing **different tensors** for `query` vs `key`/`value`:
  ```python
  multihead_attn = nn.MultiheadAttention(embed_dim, num_heads)
  attn_output, attn_output_weights = multihead_attn(query, key, value)
  ```
  (PyTorch docs https://docs.pytorch.org/docs/stable/generated/torch.nn.MultiheadAttention.html)
- Key configuration parameters (constructor):
  - `embed_dim`: total model dimension
  - `num_heads`: number of heads
  - `kdim`, `vdim`: set if key/value dims differ from `embed_dim` (default `None` → equals `embed_dim`)
  - `batch_first=True` to use (N, L, E) layout (default `False`)  
  (PyTorch docs URL above)
- Masking:
  - `key_padding_mask` shape (N, S): `True` indicates ignore that key position (padding). (PyTorch docs URL above)
  - `attn_mask` shape (L, S) or (N⋅num_heads, L, S). (PyTorch docs URL above)
- Performance procedure:
  - If you do **not** need attention weights, set `need_weights=False` to use optimized `scaled_dot_product_attention` and “achieve the best performance.” (PyTorch docs URL above)

### Encoder–decoder cross-attention placement in decoder layer (conceptual procedure)
- Decoder layer data flow: cross-attention sits **between** masked self-attention and the position-wise feed-forward sub-layer; residual connections and layer normalization are applied around it. (apxml encoder-decoder cross-attention URL: https://apxml.com/courses/foundations-transformers-architecture/chapter-5-encoder-decoder-stacks/encoder-decoder-cross-attention)

### BART decoder caching procedure (as shown in code excerpt)
- In the provided excerpt, BART decoder layer splits cached values:
  - self-attention cache uses `past_key_value[:2]`
  - cross-attention cache uses `past_key_value[-2:]`
  - then concatenates present key/values: `present_key_value = present_key_value + cross_attn_present_key_value`  
  (Lightrun BART excerpt https://lightrun.com/answers/huggingface-transformers-similar-usage-of-past_key_values-in-causallm-and-seq2seqlm)

### ViT patch embedding procedure (explicit code shown)
- Example patch embedding via Conv2d with kernel/stride equal to patch size:
  - `nn.Conv2d(3, 768, 16, 16)` on input `(1,3,224,224)` yields reshaped patch embeddings of shape **[196, 768]**. (A. Arora ViT blog https://amaarora.github.io/posts/2021-01-18-ViT.html)

---

## Comparisons & Trade-offs

### Bottlenecking visual tokens: Q-Former vs raw ViT features
- BLIP-2 Q-Former bottleneck:
  - Output is **32×768** vs frozen image features example **257×1024** (ViT-L/14). This is explicitly described as a “bottleneck architecture” with much smaller \(Z\). (Li et al., 2023 PDF https://www.nematilab.info/bmijc/assets/081823_paper.pdf)
- Trade-off implied by design:
  - Fixed number of output features “independent of input image resolution.” (BLIP-2 project page https://zhangtemplar.github.io/blip2/; Li et al., 2023 PDF https://proceedings.mlr.press/v202/li23q/li23q.pdf)

### Flamingo cross-attention insertion frequency: compute vs performance
- Inserting gated cross-attention dense blocks only **every 4th layer**:
  - **+66% computational efficiency** with **-1.9%** performance loss. (Multimodal Language slides https://yumeng5.github.io/teaching/2024-spring-cs6501/multimodal.pdf; Group-Flamingo slides PDF https://llmsystem.github.io/llmsystem2024spring/assets/files/Group-Flamingo-98ae9c68fca94cd437716229a2cf42c1.pdf)
- Removing the bridge entirely:
  - **-4.2%** overall score and training instability. (Group-Flamingo slides PDF URL above)

### LLaVA-SP: adding a small number of spatial tokens vs increasing token count
- LLaVA-SP claims it “only adds **six** spatial visual tokens” to enhance representation. (LLaVA-SP arXiv HTML https://arxiv.org/html/2507.00505v1)
- Inference speed (single A40 GPU, 7B LLMs):
  - LLaVA-SP-Cropping: **20.51 tokens/s**
  - LLaVA-SP-Pooling: **20.28 tokens/s**
  - Reported as comparable to LLaVA-1.5. (LLaVA-SP arXiv HTML https://arxiv.org/html/2507.00505v1)
- Token-count trade-off (ablation statement):
  - Best performance observed at **6 tokens**; **12 tokens** comparable but “doubles the parameters and slows down inference speed.” (LLaVA-SP arXiv HTML https://arxiv.org/html/2507.00505v1)

### Attention imbalance/failure mode evidence (MODA)
- MODA reports multimodal attention can be biased toward language and that disparity can reach **10×**, with **layer-by-layer decay** worsening it. (MODA arXiv HTML https://arxiv.org/html/2507.04635v1)
- This provides an explicit trade-off pressure: naive multimodal attention may under-utilize vision features without architectural changes. (MODA arXiv HTML URL above)

---

## Architecture & Design Rationale

### Why scale by \(\sqrt{d_k}\) in attention?
- apxml explains scaling is used because dot products can become very large when \(d_k\) is large; dividing by \(\sqrt{d_k}\) keeps variance of inputs to softmax “more controlled” and “helps stabilize the training process.” (apxml scaled dot-product attention URL: https://apxml.com/courses/introduction-to-transformer-models/chapter-2-self-attention-multi-head-attention/scaled-dot-product-attention)

### Why softmax in attention?
- Softmax converts raw alignment scores into a normalized distribution:
  - weights sum to **1** per query (normalization)
  - weights are positive (non-negativity)
  - enables probabilistic interpretation and sharp focusing when one score dominates. (apxml softmax attention weights URL: https://apxml.com/courses/foundations-transformers-architecture/chapter-2-attention-mechanism-core-concepts/softmax-attention-weights)

### Why gated cross-attention in Flamingo?
- Flamingo freezes pretrained LM blocks and inserts new gated cross-attention + dense blocks trained from scratch. (Flamingo NeurIPS 2022 paper URL)
- Rationale for tanh-gating:
  - Multiply new layer output by \(\tanh(\alpha)\) with \(\alpha\) initialized to **0** so the conditioned model initially yields the **same results as the original LM**, improving “training stability and final performance.” (Flamingo NeurIPS 2022 paper URL)
- Slide summaries reinforce:
  - `alpha_xattn` and `alpha_dense` set to **0** initially; \(\tanh(\alpha_*)=0\) initially; “LM is kept intact at initialization.” (Group-Flamingo slides PDF URL above)

### Why Q-Former in BLIP-2?
- BLIP-2 positions Q-Former as an “information bottleneck” between a frozen image encoder and frozen LLM, extracting a fixed number of features independent of image resolution. (Li et al., 2023 PMLR PDF https://proceedings.mlr.press/v202/li23q/li23q.pdf; BLIP-2 project page https://zhangtemplar.github.io/blip2/)
- Architectural rationale details:
  - Two transformer submodules share the same self-attention layers; queries interact with frozen image features via cross-attention inserted every other block. (Li et al., 2023 PDF https://www.nematilab.info/bmijc/assets/081823_paper.pdf)

### Why adapters for Llama 3.2 Vision?
- Meta states they trained “adapter weights” integrating a pretrained image encoder into the pretrained language model; adapter is “a series of cross-attention layers.” During adapter training, they did **not** update language-model parameters to keep text-only capabilities intact. (Meta blog https://ai.meta.com/blog/llama-3-2-connect-2024-vision-edge-mobile-devices/)

---

## Common Questions & Answers

### Q1: What is the exact attention equation used in Transformers?
- \(\text{Attention}(Q,K,V)=\text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V\). (apxml scaled dot-product attention URL; apxml softmax attention weights URL)

### Q2: In cross-attention, which modality provides Q vs K/V?
- In encoder–decoder cross-attention, queries come from the decoder state, while keys and values come from the encoder’s final output. (apxml encoder-decoder cross-attention URL)

### Q3: How do I implement cross-attention in PyTorch `nn.MultiheadAttention`?
- Pass decoder (or text) states as `query`, and encoder (or vision) states as `key` and `value`:
  - `attn_output, attn_weights = mha(query, key, value)` (PyTorch docs URL)
- Use `need_weights=False` for best performance via optimized `scaled_dot_product_attention`. (PyTorch docs URL)

### Q4: Why does Flamingo initialize the gate to zero?
- Flamingo uses \(\tanh(\alpha)\) gating with \(\alpha\) initialized to **0** so the model output initially matches the pretrained LM, which the paper says improves training stability and final performance. (Flamingo NeurIPS 2022 paper URL)

### Q5: How many query tokens does BLIP-2 Q-Former use, and what dimension?
- BLIP-2 uses **32** learnable queries, each of dimension **768**, producing output \(Z\) of size **32×768**. (Li et al., 2023 PDF https://www.nematilab.info/bmijc/assets/081823_paper.pdf)

### Q6: How often are cross-attention layers inserted in BLIP-2 Q-Former?
- Cross-attention layers are inserted **every other transformer block**. (Li et al., 2023 PDF https://www.nematilab.info/bmijc/assets/081823_paper.pdf)

### Q7: How many tokens does a ViT produce for a 224×224 image with 16×16 patches?
- **196** patch tokens (14×14). With a `[cls]` token, the sequence becomes **197** tokens. (A. Arora ViT blog URL; Keras TokenLearner example URL)

### Q8: What’s the compute/performance trade-off of inserting Flamingo cross-attention less frequently?
- A reported ablation: inserting gated cross-attention dense blocks only **every 4th layer** yields **66%** higher computational efficiency with **1.9%** performance loss. (Multimodal Language slides URL; Group-Flamingo slides PDF URL)

### Q9: Are `past_key_values` shapes consistent across Hugging Face models?
- Not fully, per the search results:
  - One description: list of tensors shaped **(2, batch_size, num_heads, sequence_length, embed_size_per_head)**. (HF issue #7246 URL)
  - Another (BART) description: nested tuples with tensors shaped **(batch_size, num_heads, sequence_length - 1, embed_size_per_head)**. (Lightrun URL)
- The results indicate model-specific conventions; they conflict in container structure and sequence length handling. (HF issue #7246; Lightrun)

### Q10: What evidence exists that multimodal attention can become imbalanced (language-dominant)?
- MODA reports attention scores can be biased toward language, with modality disparity reaching up to **10×**, and mentions **63% disparity** across layers (per a referenced figure). (MODA arXiv HTML https://arxiv.org/html/2507.04635v1)