---
title: "Attention Mechanism"
subject: "Sequence Models & Attention"
date: 2026-04-08
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

# Attention Mechanism

## Video (best)
- **3Blue1Brown** — "Attention in transformers, visually explained | Chapter 6, Deep Learning"
- **Watch:** [YouTube](https://www.youtube.com/watch?v=eMlx5fFNoYc)
- Why: Exceptional visual intuition for how attention scores are computed, how queries/keys/values interact, and why the mechanism works. Grant Sanderson's geometric framing makes abstract matrix operations concrete. Part of a coherent series so learners have scaffolding.
- Level: beginner/intermediate

## Blog / Written explainer (best)
- **Jay Alammar** — "The Illustrated Transformer"
- **Link:** [https://jalammar.github.io/illustrated-transformer/](https://jalammar.github.io/illustrated-transformer/)
- Why: The gold standard written explainer for attention. Step-by-step diagrams show exactly how Q, K, V matrices are formed and combined, multi-head attention is visualized clearly, and the encoder-decoder attention is distinguished from self-attention. Widely cited in courses precisely because it bridges intuition and math without losing either.
- Level: beginner/intermediate

## Deep dive
- **Lilian Weng** — "Attention? Attention!"
- **Link:** [https://lilianweng.github.io/posts/2018-06-24-attention/](https://lilianweng.github.io/posts/2018-06-24-attention/)
- Why: Comprehensive taxonomy of attention variants (soft vs. hard, self-attention, global vs. local, additive vs. dot-product). Covers the historical progression from Bahdanau through Transformer attention with mathematical rigor. Excellent reference when learners need to understand *why* design choices were made, not just what they are.
- Level: intermediate/advanced

## Original paper
- **Vaswani et al., 2017** — "Attention Is All You Need"
- **Link:** [https://arxiv.org/abs/1706.03762](https://arxiv.org/abs/1706.03762)
- Why: The seminal paper that crystallized scaled dot-product attention and multi-head attention as the dominant paradigm. Unusually readable for a landmark paper — the architecture description is self-contained and the ablations are instructive. The clear notation has become the field's standard vocabulary.
- Level: intermediate/advanced

## Code walkthrough
- **Andrej Karpathy** — "Let's build GPT: from scratch, in code, spelled out."
- **Watch:** [YouTube](https://www.youtube.com/watch?v=kCc8FmEb1nY)
- Why: Karpathy builds self-attention from a blank Python file, deriving each line from first principles (starting from the "mathematical trick" of masked self-attention). Learners see exactly how the Q/K/V projections, scaled dot-product, softmax, and multi-head assembly translate to ~50 lines of PyTorch. The incremental build-up makes debugging intuitions explicit.
- Level: intermediate/advanced

## Coverage notes
- **Strong:** Visual/conceptual explanation (3B1B video + Jay Alammar blog form a near-perfect beginner ramp); mathematical formalism (Lilian Weng); hands-on implementation (Karpathy); seminal theory (Vaswani et al.)
- **Weak:** Attention variants beyond the Transformer (e.g., linear attention, sparse attention, cross-attention in diffusion models) are not well covered by any single beginner-friendly resource
- **Gap:** No excellent standalone resource specifically covers *cross-attention* (encoder-decoder attention) in isolation with worked code examples — most resources treat it as a footnote to self-attention. Learners building seq2seq systems may need to supplement with the original Bahdanau paper (arxiv.org/abs/1409.0473) [VERIFY current URL stability] and the older Jay Alammar post "Visualizing A Neural Machine Translation Model."

---

## Additional Resources for Tutor Depth

> **8 sources** — papers, official docs, working code, benchmarks, and deep explainers that give the AI tutor precision on this topic.

### 📄 FlashAttention-2 (exact IO-aware attention via tiling + online softmax)
**Paper** · [source](https://tridao.me/publications/flash2/flash2.pdf)

*Block/tiling scheme for exact attention; online softmax with running \((m,\ell)\) / logsumexp \(L\); recomputation to avoid materializing \(N\times N\) attention.*

<details>
<summary>Key content</summary>

- **Standard attention (Sec. 2.2):** Given \(Q,K,V\in\mathbb{R}^{N\times d}\):  
  \(S=QK^\top\in\mathbb{R}^{N\times N}\), \(P=\mathrm{softmax}(S)\) (row-wise), \(O=PV\in\mathbb{R}^{N\times d}\).  
  Backward: \(dV=P^\top dO\); \(dP=dOV^\top\); \(dS=\mathrm{dsoftmax}(dP)\); \(dQ=dSK\); \(dK=QdS^\top\).
- **FlashAttention-2 forward algorithm (Alg. 1, Sec. 3.1.1):** Tile rows/cols: \(T_r=\lceil N/B_r\rceil\), \(T_c=\lceil N/B_c\rceil\). For each row block \(Q_i\): init on-chip \(O_i^{(0)}=0\), \(\ell_i^{(0)}=0\), \(m_i^{(0)}=-\infty\). For each col block \(K_j,V_j\):  
  \(S_{ij}=Q_iK_j^\top\). Update running row-wise max and exp-sum:  
  \(m_i^{(j)}=\max(m_i^{(j-1)}, \mathrm{rowmax}(S_{ij}))\); \(\tilde P_{ij}=\exp(S_{ij}-m_i^{(j)})\);  
  \(\ell_i^{(j)}=\exp(m_i^{(j-1)}-m_i^{(j)})\ell_i^{(j-1)}+\mathrm{rowsum}(\tilde P_{ij})\).  
  Update unnormalized output: \(O_i^{(j)}=\mathrm{diag}(\exp(m_i^{(j-1)}-m_i^{(j)}))O_i^{(j-1)}+\tilde P_{ij}V_j\).  
  Final: \(O_i=\mathrm{diag}((\ell_i^{(T_c)})^{-1})O_i^{(T_c)}\); store \(L_i=m_i^{(T_c)}+\log(\ell_i^{(T_c)})\) (logsumexp).
- **Rationale (Sec. 3.1):** Reduce expensive non-matmul FLOPs (A100: 312 TFLOPs/s FP16/BF16 matmul vs 19.5 TFLOPs/s FP32 non-matmul; ~16× gap). Keep \(O\) unscaled until end; store only \(L\) (not both \(m,\ell\)).
- **Memory/compute:** Exact output (no approximation); avoids materializing \(S,P\) in HBM; **extra memory \(O(N)\)** (store \(L\)); FLOPs \(O(N^2 d)\) (Sec. 3.1.1).
- **Causal mask (Sec. 3.1.1):** Skip blocks entirely above diagonal (~half blocks) → ~**1.7–1.8×** speedup vs non-causal; per row apply mask to only ~1 block (square blocks).
- **Parallelism/work partitioning (Secs. 3.2–3.3):** Forward parallelize over row blocks (sequence length) + batch + heads; backward parallelize over column blocks; atomic adds for \(dQ\). Avoid “split-K”: FlashAttn-2 splits **Q across warps** (K,V shared) to reduce shared-memory traffic.
- **Empirical (A100 80GB, Sec. 4.1):** FlashAttention-2 **1.7–3.0×** faster than FlashAttention; **3–10×** faster than PyTorch attention; forward reaches **up to 73%** of theoretical peak; end-to-end training up to **225 TFLOPs/s per A100** (72% MFU) (Table 1).

</details>

### 📄 FlashAttention-3 (Hopper): asynchrony + FP8 attention
**Paper** · [source](https://arxiv.org/html/2407.08608v1)

*Consolidated H100 benchmarks + kernel design changes beyond FlashAttention-2 (asynchrony/pipelining, FP8)*

<details>
<summary>Key content</summary>

- **Attention formula (Sec. 2.1):** For one head with sequence length \(n\), head dim \(d\):  
  \[
  O=\mathrm{softmax}(S)V,\quad S=\alpha QK^\top,\ \alpha=\frac{1}{\sqrt d}
  \]
  Softmax applied row-wise; subtract row max from \(S\) for numerical stability.
- **Why FA-3 (Intro):** FlashAttention-2 achieves ~**35% utilization** on H100 vs **80–90%** for optimized GEMM; FA-3 redesigns for Hopper **asynchrony** (Tensor Cores + TMA) and **low precision (FP8)**.
- **3 main techniques (Intro, Sec. 3):**
  1) **Producer–consumer warp specialization**: separate warps issue **TMA loads** vs **WGMMA compute**; use **setmaxnreg** to reallocate registers to compute warps.  
  2) **Overlap softmax under async GEMMs**: 2-stage pipeline across iterations; “pingpong scheduling” uses barriers so one warpgroup does softmax while another runs GEMMs. Example gain: **570 → 620–640 TFLOPs/s** (FP16 fwd, headdim 128, seqlen 8192).  
  3) **FP8 support**: FP8 WGMMA requires **k-major** operands; FA-3 uses **in-kernel transpose** (LDSM/STSM) + register byte-permute to satisfy layout for back-to-back GEMMs.
- **Empirical performance (Abstract/Sec. 4):**
  - FP16: **1.5–2.0×** faster than FA-2 forward; up to **740 TFLOPs/s (~75% H100 peak)**. Backward: **1.5–1.75×** faster.  
  - FP8: near **1.2 PFLOPs/s**.
  - Ablation (Table 2, non-causal FP16): FA-3 **3.538 ms, 661 TFLOPs/s**; removing pipelining **4.021 ms, 582**; removing warp-specialization **4.105 ms, 570**.
- **Numerical error (Table 3):** RMSE vs FP64 reference with outlier \(Q\) (0.1% entries add \(\mathcal N(0,10)\) to \(\mathcal N(0,1)\)):  
  - Baseline FP16 **3.2e-4**; FA-2 FP16 **1.9e-4**; FA-3 FP16 **1.9e-4** (softmax intermediates kept FP32).  
  - Baseline FP8 (per-tensor scaling) **2.4e-2**; FA-3 FP8 **9.1e-3** (~**2.6×** lower error). “No incoherent processing” returns to **2.4e-2**.
- **Benchmark defaults (Sec. 4.1/C.1):** H100 80GB SXM5; CUDA 12.3, cuDNN 9.1.1.17, CUTLASS 3.5, FA2 2.5.8, Triton nightly 3.0, PyTorch 2.3; GPU clock fixed **1830 MHz**; 100 repeats avg. Seqlen 512–16k; total tokens **16k**; hidden dim **2048**; headdim **64/128/256** (32/16/8 heads). Forward FLOPs: \(4n^2d+2n^2\); causal halves FLOPs; backward ≈ **2.5×** forward.

</details>

### 📄 Multi-Query Attention (MQA) for Faster Autoregressive Decoding
**Paper** · [source](https://arxiv.org/abs/1911.02150)

*MQA rationale + incremental decoding bottleneck: KV-cache memory-bandwidth; sharing K/V across heads shrinks cache/loads.*

<details>
<summary>Key content</summary>

- **Dot-Product Attention (Sec. 2.1):**  
  Given query \(q\in\mathbb{R}^{k}\), keys \(K\in\mathbb{R}^{m\times k}\), values \(V\in\mathbb{R}^{m\times v}\):  
  \(\text{logits}= qK^\top\in\mathbb{R}^{m}\); \(\alpha=\text{softmax}(\text{logits})\); output \(y=\alpha^\top V\in\mathbb{R}^{v}\).
- **Multi-Head Attention (Sec. 2.2–2.3):**  
  For \(h\) heads, projections \(P_q\in\mathbb{R}^{h\times d\times k}\), \(P_k\in\mathbb{R}^{h\times d\times k}\), \(P_v\in\mathbb{R}^{h\times d\times v}\), \(P_o\in\mathbb{R}^{h\times d\times v}\).  
  \(Q=\text{einsum}(X,P_q)\in\mathbb{R}^{b\times h\times n\times k}\); \(K=\text{einsum}(M,P_k)\in\mathbb{R}^{b\times h\times m\times k}\); \(V=\text{einsum}(M,P_v)\in\mathbb{R}^{b\times h\times m\times v}\).  
  logits \(\in\mathbb{R}^{b\times h\times n\times m}\); \(O=\text{softmax}(\cdot)\,V\); \(Y=\text{einsum}(O,P_o)\in\mathbb{R}^{b\times n\times d}\).
- **Incremental decoding bottleneck (Sec. 2.4.1):** autoregressive inference can’t parallelize over time; repeatedly loading cached \(K,V\) dominates due to **memory bandwidth**. Cost term tied to reloading \(K,V\) of size \(\approx bhn^2\) (under simplifying assumptions \(m=n, k=v=d/h\)).
- **MQA definition (Sec. 3):** keep multi-head **queries** but **share keys/values across heads** (remove head dim from \(K,V,P_k,P_v\)):  
  \(K\in\mathbb{R}^{b\times m\times k}\), \(V\in\mathbb{R}^{b\times m\times v}\); logits \(=\text{einsum}(Q,K)\in\mathbb{R}^{b\times h\times n\times m}\).  
  **KV-cache size/load reduced by factor \(\approx h\)** vs multi-head.
- **Empirical speed (Sec. 4.3, TPUv2):** incremental greedy inference, batch 1024, src=128, tgt=128.  
  Baseline decoder: **47 ms/step ⇒ 46 µs/token**; MQA decoder: **3.9 ms/step ⇒ 3.8 µs/token** (~12× faster). Encoder: 222 ms (1.7 µs/token) baseline vs 195 ms (1.5 µs/token) MQA.
- **Training setup (Sec. 4.1):** WMT14 En-De, 6-layer encoder-decoder, \(d_{model}=1024\), \(d_{ff}=4096\) baseline, \(h=8\), \(d_k=d_v=128\), learned positional embeddings, embed/output weight sharing; 100k steps, batch 128 examples, each 256 src + 256 tgt tokens; TPUv3 32-core. MQA widens FFN to **5440** to match params (211M).

</details>

### 📄 PagedAttention & vLLM KV-cache paging for LLM serving
**Paper** · [source](https://arxiv.org/abs/2309.06180)

*PagedAttention + vLLM system design: paged KV-cache layout, block allocation/eviction to avoid fragmentation, throughput/latency under dynamic batching*

<details>
<summary>Key content</summary>

- **Problem (Sec. 1, 3): KV cache dominates serving memory + is dynamic.** Example memory split on **A100-40GB with 13B model**: ~**65% weights**, ~**30% KV cache**, small activations. KV cache grows/shrinks per request; inefficient management limits batch size → throughput.
- **KV cache size formula (Sec. 3):** For OPT-13B, **per-token KV cache ≈ 800 KB**, computed as  
  **2 (K,V) × 5120 (hidden size) × 40 (layers) × 2 bytes (FP16)**.
- **Why existing systems waste memory (Sec. 3):** contiguous pre-allocation to max length causes:
  - **Reserved slots** for future tokens (held for entire request lifetime)
  - **Internal fragmentation** (unknown output length)
  - **External fragmentation** (allocator/buddy system). Profiling: only **20–40%** of KV cache space utilized; “effective memory … as low as **20%**”.
- **PagedAttention algorithm (Sec. 4.1):** partition each sequence’s KV cache into fixed-size **KV blocks** (pages). Logical blocks are contiguous; **physical blocks can be non-contiguous**. Attention kernel uses a **block table** (logical→physical) to fetch blocks during attention.
- **Block-size tradeoff (Sec. 4.3, 7.2 mention):** larger blocks improve parallelism/utilization (lower latency) but increase fragmentation; **block size 16** “generally works well” (slides/transcript).
- **Write path optimization (Sec. 4.3):** **fused reshape + block write** per layer: split new KV into blocks, reshape to block-read-friendly layout, write to physical blocks via block table.
- **Sharing (Sec. 4.4):** block-level **copy-on-write** enables sharing prompt KV across parallel sampling/beam search; reported savings: **~30%** (parallel sampling) and **>60%** (beam search); prompt itself noted as **~12%** of total KV in one experiment.
- **Preemption/recovery (talk):** when out of blocks, either **swap to CPU** or **recompute KV**; recomputation can be faster for small blocks; vLLM uses recomputation “whenever possible”.
- **Empirical result (Abstract):** vLLM improves throughput **2–4×** vs **FasterTransformer/Orca** at similar latency; memory utilization **>96%** average (talk) and **2.5–5×** KV efficiency improvement.

</details>

### 📊 FlashAttention-2 benchmarks & efficiency claims
**Benchmark** · [source](https://arxiv.org/abs/2307.08691)

*Benchmark comparisons (throughput/latency, causal vs non-causal, training-relevant fwd+bwd) and end-to-end GPT training TFLOPs/s.*

<details>
<summary>Key content</summary>

- **Attention equations (Section 2):**  
  - Scores: \(S = QK^\top \in \mathbb{R}^{N\times N}\)  
  - Probabilities: \(P=\mathrm{softmax}(S)\) (row-wise)  
  - Output: \(O = PV \in \mathbb{R}^{N\times d}\)  
  - Variables: \(N\)=sequence length, \(d\)=head dimension; computed per head and batch in MHA.
- **Core FlashAttention idea (Section 2.3):** tile blocks of \(Q,K,V\) from HBM→SRAM, compute block attention with **online softmax rescaling**, and **avoid materializing** \(S\) and \(P\) in HBM → **memory drops from \(O(N^2)\) to \(O(N)\)** (stores row-wise logsumexp \(L\)).
- **FlashAttention-2 design rationale (Sections 3.1–3.3):**
  - Reduce **non-matmul FLOPs** because A100 peak FP16/BF16 matmul is **312 TFLOPs/s** vs **19.5 TFLOPs/s** non-matmul FP32 (~**16×** gap).  
  - Increase occupancy by parallelizing over **sequence length** (not just batch×heads).  
  - Reduce shared-memory traffic by switching warp partitioning from **split-K** (FlashAttention) to **split-Q** (FlashAttention-2), avoiding inter-warp reductions in forward pass.
- **Empirical speed/efficiency (benchmarks, Section 4 + abstract):**
  - FlashAttention-2: **~2× faster** than FlashAttention; reaches **50–73%** of theoretical max FLOPs/s on A100; up to **230 TFLOPs/s** (A100, FP16/BF16).  
  - Compared to standard PyTorch attention: up to **9× faster** (forward+backward benchmarks mentioned).
- **End-to-end GPT training throughput (table in text):**
  - GPT3-1.3B, **2k**: Baseline **142**, FA **189**, FA-2 **196** TFLOPs/s  
  - GPT3-1.3B, **8k**: Baseline **72**, FA **170**, FA-2 **220** TFLOPs/s  
  - GPT3-2.7B, **2k**: Baseline **149**, FA **189**, FA-2 **205** TFLOPs/s  
  - GPT3-2.7B, **8k**: Baseline **80**, FA **175**, FA-2 **225** TFLOPs/s (**72%** model FLOPs utilization); **~1.3×** end-to-end speedup over FlashAttention.
- **Causal masking optimization (Section 3.1.1):** skip blocks where column index > row index → **~1.7–1.8× speedup** vs non-causal (since ~half entries computed).
- **Supported configs/features:** head dim up to **256**; supports **MQA/GQA** (reduces KV-cache size, improves inference throughput).

</details>

### 📖 PyTorch `scaled_dot_product_attention` (SDPA) semantics
**Reference Doc** · [source](https://docs.pytorch.org/docs/stable/generated/torch.nn.functional.scaled_dot_product_attention.html)

*Authoritative parameter semantics/defaults, tensor shapes, mask behavior, kernel selection (Flash/MemEff/Math), GQA constraints.*

<details>
<summary>Key content</summary>

- **API + defaults:** `scaled_dot_product_attention(query, key, value, attn_mask=None, dropout_p=0.0, is_causal=False, scale=None, enable_gqa=False) -> Tensor`. `scale` is **keyword-only**.
- **Eq. 1 (scores + scaling):**  
  Let `L = query.size(-2)`, `S = key.size(-2)`, `d = query.size(-1)`.  
  `scale_factor = 1/sqrt(d)` if `scale is None` else `scale`.  
  `attn_weight = (query @ key.transpose(-2, -1)) * scale_factor` with shape `(..., L, S)`.
- **Eq. 2 (mask/bias + softmax + dropout + output):**  
  `attn_bias` initialized zeros `(L,S)`.  
  If `is_causal=True`: requires `attn_mask is None`; apply lower-triangular allow-mask, fill others with `-inf`.  
  If `attn_mask` provided (broadcastable to `(..., L, S)`):  
  - **bool mask:** `True` = participates/allowed; `False` filled with `-inf`.  
  - **float mask (same dtype as q/k/v):** added to scores (`attn_bias = attn_mask + attn_bias`).  
  Then: `softmax(dim=-1)`, `dropout(attn_weight, dropout_p, train=True)`, output `attn_weight @ value` (shape like `query`).
- **Dropout behavior:** always applied per `dropout_p`; to disable in eval, pass `0.0` when `not self.training`.
- **Mask semantics note:** SDPA bool mask is inverse of `MultiheadAttention.key_padding_mask` (MHA: `True` = masked out). Invert when migrating (`~mask` / `logical_not()`).
- **Backends:** auto-select among FlashAttention-2, Memory-Efficient, and PyTorch C++ “math”; control via `torch.nn.attention.sdpa_kernel()` (preferred) or global CUDA toggles.
- **GQA (`enable_gqa=True`) constraints:** works only for Flash + math on CUDA; no NestedTensor. Requires `num_heads_q % num_heads_kv == 0` and `heads_key == heads_value`; implemented via repeating K/V along head dim.

</details>

### 📋 # Source: https://aclanthology.org/2023.emnlp-main.298/
**Source** · 

### 🔍 PyTorch Scaled Dot Product Attention (SDPA) usage + masking
**Explainer** · [source](https://docs.pytorch.org/tutorials/_sources/intermediate/scaled_dot_product_attention_tutorial.rst.txt)

*Concrete invocation patterns for `F.scaled_dot_product_attention`, backend dispatch control, causal masking (`is_causal` vs bias tensors), and training vs inference knobs (`dropout_p`).*

<details>
<summary>Key content</summary>

- **SDPA call signature (usage pattern):**  
  `torch.nn.functional.scaled_dot_product_attention(query, key, value, attn_mask=None, dropout_p=..., is_causal=...)`  
  Example (dense): `F.scaled_dot_product_attention(q, k, v)` where `q,k,v` shaped like `(B, ..., L, D)`; tutorial uses `(2,3,8)` and multihead `(B, H, L, D)`.
- **Backend dispatch (CUDA):** chooses among **FlashAttention**, **Memory-Efficient Attention**, or **C++ math** implementation.  
  Explicit control via context manager:  
  `from torch.nn.attention import SDPBackend, sdpa_kernel` then `with sdpa_kernel(SDPBackend.FLASH_ATTENTION): ...` (also `MATH`, `EFFICIENT_ATTENTION`).
- **Benchmark setup + empirical timings (example):**  
  `B=32, L=1024, H=32, D=32, dtype=float16`.  
  Reported: default **2333.687 µs**, math **87407.322 µs**, flash **2316.913 µs**, efficient **4577.936 µs**.
- **Causal self-attention module procedure:** project `x` with `Linear(embed_dim, 3*embed_dim)`, `chunk(3)` into `q,k,v`, reshape to `(B,H,L,head_dim)` via `.view(...).transpose(1,2)`, then SDPA.  
  **Training vs eval knobs:** if `self.training`: `dropout_p=self.dropout`, `is_causal=self.is_causal`; else `dropout_p=0.0`, `is_causal=False`.
- **Causal bias tensors (PyTorch ≥2.3):**  
  `from torch.nn.attention.bias import causal_upper_left, causal_lower_right`  
  `is_causal=True` is equivalent to `causal_upper_left(Lq, Lkv)`; differs from `causal_lower_right` when attention score matrix is non-square (common in decoding).
- **NestedTensor note:** SDPA supports NestedTensor + dense; fused implementations currently don’t support NestedTensor **for training**; example eval benchmark: Random NT **599.388 µs** vs Random Dense **964.192 µs** (flash backend).

</details>

---

## Related Topics

- [[topics/self-attention|Self-Attention]]
- [[topics/multi-head-attention|Multi-Head Attention]]
- [[topics/transformer-architecture|Transformer Architecture]]
- [[topics/rnns-lstms|RNNs & LSTMs]]
