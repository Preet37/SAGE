---
title: "Long Context Models"
subject: "Large Language Models"
date: 2026-04-09
tags:
  - "subject/large-language-models"
  - "level/intermediate"
  - "level/advanced"
  - "educator/andrej-karpathy"
  - "educator/jay-alammar"
  - "educator/lilian-weng"
  - "resource/video"
  - "resource/blog"
  - "resource/deep-dive"
  - "resource/paper"
  - "resource/code"
educators:
  - "Andrej Karpathy"
  - "Jay Alammar"
  - "Lilian Weng"
levels:
  - "intermediate"
  - "advanced"
resources:
  - "video"
  - "blog"
  - "deep-dive"
  - "paper"
  - "code"
---

# Long Context

## Video (best)
- **Andrej Karpathy** — "Let's build GPT: from scratch, in code, spelled out."
- **Watch:** [YouTube](https://www.youtube.com/watch?v=kCc8FmEb1nY)
- Why: Clear, practical explanation of Transformer attention and why context length matters; good foundation before diving into long-context extensions.
- Level: Beginner → Intermediate

## Blog / Written explainer (best)
- **Lil'Log (Lilian Weng)** — "Attention? Attention!"
- **Link:** [https://lilianweng.github.io/posts/2018-06-24-attention/](https://lilianweng.github.io/posts/2018-06-24-attention/)
- Why: Strong conceptual grounding in attention mechanisms; useful for understanding efficient attention and context utilization issues.
- Level: Beginner → Intermediate

## Deep dive
- **Jay Alammar** — "The Illustrated Transformer"
- **Link:** [https://jalammar.github.io/illustrated-transformer/](https://jalammar.github.io/illustrated-transformer/)
- Why: Visual, intuitive walkthrough of self-attention and positional information; helpful context for rope scaling, interpolation, and long-context behavior.
- Level: Beginner → Intermediate
- **Lilian Weng** — "Transformer Family"
- **Link:** [https://lilianweng.github.io/posts/2020-04-07-the-transformer-family/](https://lilianweng.github.io/posts/2020-04-07-the-transformer-family/)
- Why: Surveys Transformer variants, including efficiency-oriented ideas that connect to long-context evaluation and efficient attention.
- Level: Intermediate

## Original paper
- **Su et al.** — "RoFormer: Enhanced Transformer with Rotary Position Embedding"
- **Link:** [https://arxiv.org/abs/2104.09864](https://arxiv.org/abs/2104.09864)
- Why: Primary reference for RoPE (rotary position embeddings), a key building block behind many modern long-context extension techniques (and later rope scaling variants).
- Level: Intermediate → Advanced
- **Beltagy, Peters, Cohan** — "Longformer: The Long-Document Transformer"
- **Link:** [https://arxiv.org/abs/2004.05150](https://arxiv.org/abs/2004.05150)
- Why: Canonical efficient-attention approach (sparse attention) for longer sequences; useful contrast vs “just increase context”.
- Level: Intermediate → Advanced
- **Dao et al.** — "FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness"
- **Link:** [https://arxiv.org/abs/2205.14135](https://arxiv.org/abs/2205.14135)
- Why: Widely used exact-attention implementation enabling longer contexts in practice by reducing memory/compute overhead.
- Level: Advanced

## Code walkthrough
- **Andrej Karpathy** — "nanoGPT"
- **Link:** [https://github.com/karpathy/nanoGPT](https://github.com/karpathy/nanoGPT)
- Why: Readable reference implementation of GPT-style training/inference; good base for experimenting with context length, attention cost, and positional embeddings.
- Level: Intermediate

## Coverage notes
- Strong: Transformer attention fundamentals; positional embeddings (incl. RoPE); efficient attention (Longformer) and practical attention optimization (FlashAttention).
- Weak: Direct, practitioner-focused guides on **rope scaling**, **yarn**, and **position interpolation** as used in modern long-context LLMs (few stable, canonical explainers).
- Gap: A single authoritative explainer that cleanly compares **retrieval vs long context**, addresses **lost-in-the-middle** and **context utilization**, and ties them to **needle-in-a-haystack** evaluation and **context compression** techniques.

---

## Additional Resources for Tutor Depth

> **10 sources** — papers, official docs, working code, benchmarks, and deep explainers that give the AI tutor precision on this topic.

### 📄 Position Interpolation (PI) for RoPE context extension
**Paper** · [source](https://arxiv.org/abs/2306.15595)

*Defines Position Interpolation (PI) for RoPE by rescaling positions (e.g., \(p' = p/s\)) and specifies how to apply it at inference and during continued training, including the exact modification point in RoPE computation.*

<details>
<summary>Key content</summary>

- **RoPE definition (Eq. 1–2):** RoPE applies a complex rotation to each head-dim pair using position \(p\). Attention score depends on relative position via trig functions after applying RoPE to **both** queries \(q\) and keys \(k\) at each layer.
- **Problem with direct extrapolation (Sec. 2.2):** Using RoPE beyond the trained max length can cause **catastrophically high attention scores** and perplexity comparable to untrained models; even evidence at distance 2900 may fail when querying at position 3000 if trained max is 2048.
- **Position Interpolation (PI) (Eq. 4):** For extending context from original \(L\) to longer \(L'\), **down-scale position indices before RoPE**:  
  \[
  p' = p/s,\quad s = L'/L
  \]
  i.e., replace RoPE\((p)\) with RoPE\((p/s)\). This aligns max relative distance back to the pretrained range (reduces from \(L'\) to \(L\)).
- **Stability rationale (Theorem 2.1, Eq. 5–7 vs Eq. 8):** Interpolated attention scores are bounded by a linear interpolation of nearby “well-behaved” grid points; interpolation bound is **at least smaller** than RoPE’s extrapolation bound (numerically \(B(s)\ge 1\), often much larger).
- **Fine-tuning procedure (Sec. 3.1):** Next-token prediction on **Pile**; AdamW \((\beta_1,\beta_2)=(0.9,0.95)\); weight decay 0; warmup 20 steps from 0 to max LR. LR: \(2\!\times\!10^{-5}\) (7B/13B), \(1\!\times\!10^{-5}\) (33B/65B). PI fine-tune typically **1000 steps** (direct FT baseline: 10000).
- **Empirical: effective context via passkey retrieval (Table 4):** PI reaches target window after **200 steps** (e.g., 7B: 8192/16384/32768 all achieved; 33B: 8192/16384 achieved). Direct FT barely improves: ~2048→2560 even after 10000 steps.
- **Empirical: perplexity improves with longer windows (Table 1):** LLaMA-7B extended to 32768 with PI: PG19 ppl **7.23→6.77** (2048→32768). Direct FT to 8192 worsens at long windows (e.g., 7B: 7.21@2048 → 7.69@8192).

</details>

### 📄 YaRN RoPE extension (NTK-by-parts + attention scaling)
**Paper** · [source](https://arxiv.org/abs/2309.00071)

*Piecewise/ramped RoPE frequency scaling (low/high-frequency treatment) + YaRN attention temperature/rescaling to preserve short-range behavior while extending max context.*

<details>
<summary>Key content</summary>

- **Goal/notation (Section 2.2):** pretrained max context \(L\); target \(L'\); **scale factor** \(s=L'/L\). **RoPE wavelength** for dim \(i\): \(\lambda_i=\frac{2\pi}{\theta_i}\) (Eq. 8). **Rotation count ratio** over pretrained window: \(r_i=\frac{L}{\lambda_i}\) (Eq. 10).
- **Position Interpolation (PI):** scale positions by \(1/s\): \(m(t)=t/s\) (Eq. 9; also Eq. 16 uses \(t\cdot L/L'\)).
- **NTK-by-parts (piecewise ramp) (Section 3.2, Def. 1):** choose thresholds \(\alpha,\beta\). If \(r_i\le \alpha\): interpolate like PI (avoid extrapolation). If \(r_i\ge \beta\): **no interpolation** (preserve local relative distances). Between: linear **ramp** (Eq. 11) to blend. Implemented via RoPE modification of form Eq. 7 with functions \(m(\cdot)\), \(n(\cdot)\) given in Eqs. 12–13. **Recommended for LLaMA:** \(\alpha=1,\ \beta=32\).
- **YaRN attention scaling (Section 3.3):** modify attention softmax temperature:  
  \(\text{Attn}(Q,K,V)=\text{softmax}\!\left(\frac{QK^\top}{\tau}\right)V\) (Eq. 14). Implement via “length scaling” by scaling both \(Q\) and \(K\) through scaled complex RoPE embeddings (no attention-code change; cached RoPE ⇒ zero overhead).
- **Recommended YaRN params (Def. 2):** set \(\alpha=1,\beta=32\) and choose \(\tau\) by fit vs extension factor (Eq. 15; used across LLaMA/Llama2).
- **Dynamic Scaling (Section 3.4):** during inference, set scale factor per forward pass to current sequence length (vs fixed \(s\)); with KV-cache, cache K/V **before** applying RoPE because RoPE changes when \(s\) changes.
- **Key empirical results:**  
  - Llama 2 7B YaRN fine-tuned: **4k→64k (×16)** perplexity on Proof-pile: 8k 3.51; 16k 2.99; 32k 2.65; 64k 2.42 (Table 1).  
  - Llama 2 7B YaRN: **4k→128k (×32)** (trained on 64k data, +200 steps) perplexity: 8k 3.56; 16k 3.04; 32k 2.70; 64k 2.45; 128k 2.37 (Table 1).  
  - Passkey retrieval @128k: YaRN 7B **99.4%**, 13B **99.4%** (Table B.5).  
  - Training recipe for 128k models (Section 4.1): PG19, chunked **64k** with BOS/EOS; AdamW, lr \(2\times10^{-5}\), warmup 20 steps, no weight decay; 7B trained **400 steps** (then +200 for 128k extrapolation).

</details>

### 📊 LaRA — RAG vs Long-Context Routing Has No Universal Winner
**Benchmark** · [source](https://arxiv.org/abs/2502.09977)

*Structured benchmark + measured outcomes on when Retrieval-Augmented Generation (RAG) vs Long-Context (LC) input wins/loses, including routing criteria and failure modes.*

<details>
<summary>Key content</summary>

- **Benchmark design (Section 1, 3):** LaRA has **2326 test cases** across **4 QA task types** (Location, Reasoning, Comparison, Hallucination detection) and **3 natural long-context types**: **novels, academic papers, financial statements**. Contexts chosen to be **near 32k and 128k tokens** (avoid truncation; reduce leakage via recency + entity replacement in novels).
- **Task definitions (Section 3.2):**
  - **Location:** answer in one sentence/paragraph; paraphrase allowed (not verbatim “needle”).
  - **Reasoning:** inference/calculation from context.
  - **Comparison:** synthesize info from multiple distant parts.
  - **Hallucination detection:** correct response is refusal: **“XXX is not mentioned in the provided context.”**
- **RAG pipeline defaults (Section 4.1):** **chunk size 600 tokens**, **overlap 100**, **5 chunks per document**; embeddings **GTE-large-en-v1.5**; **hybrid retrieval = embedding similarity + BM25**.
- **Evaluation procedure (Section 3.4):** **GPT-4o as judge** given (query, ground-truth, prediction); validated with **Cohen’s Kappa** vs humans.
- **Key empirical results (Abstract + Section 4.3/Table 2):**
  - **Model strength:** RAG helps weaker models more; at **128k**, RAG beats LC by **+6.48%** (Llama-3.2-3B) and **+38.12%** (Mistral-Nemo-12B).
  - **Context length flip:** at **32k**, LC averages **+2.40%** over RAG; at **128k**, RAG averages **+3.68%** over LC.
  - **Task routing:** RAG ≈ LC on **single-location**; **RAG best for hallucination detection**; **LC best for reasoning + comparison**. Comparison shows largest LC advantage: avg gap **+15.22% (32k)** and **+14.30% (128k)** (LC over RAG).
  - **Lost-in-the-middle (Section 4.6):** LC accuracy drops when answers are near context center; **RAG shows no clear position correlation**.

</details>

### 📊 Lost-in-the-Middle (Liu et al., 2023/2024)
**Benchmark** · [source](https://arxiv.org/abs/2307.03172)

*Canonical “lost-in-the-middle” U-shaped curves + task definitions (multi-doc QA, key–value retrieval) + evaluation protocol knobs (context length, answer position, baselines)*

<details>
<summary>Key content</summary>

- **Core phenomenon (Fig. 1, Fig. 5, Fig. 7):** Performance vs. position of relevant info is **U-shaped**: best when relevant content is at **start (primacy)** or **end (recency)**; **worst in the middle**, even for long-context models.
- **Multi-document QA task (Sec. 2 / 3.1):**
  - Input = **question + k documents**, with **exactly 1 answer-containing doc** and **k−1 distractors**.
  - **Manipulations:** (i) increase context length by increasing **k**; (ii) change **position** of the answer doc by **reordering documents** (beginning/middle/end; finer-grained positions in plots).
  - **Metric:** **Accuracy** = whether **any annotated correct answer string** (NaturalQuestions annotations) appears in model output (string match).
  - **Baselines:** **closed-book** (no docs; parametric memory) and **oracle** (only the answer doc).
  - **Concrete result:** For **GPT-3.5-Turbo**, when the answer doc is **in the middle**, open-book accuracy can be **lower than closed-book**; closed-book reported as **56.1%**.
  - **Extended-context not necessarily better:** When both models’ windows fit the same inputs (e.g., **10- and 20-doc** settings), **GPT-3.5-Turbo vs GPT-3.5-Turbo (16K)** curves are nearly **superimposed** (Fig. 5).
- **Synthetic key–value retrieval (Sec. 3):**
  - Context contains **75 / 140 / 300 key–value pairs**; **500 examples each**.
  - Query asks for the value of a key; **metric:** output contains the **correct value**.
  - Same U-shaped degradation with key–value position (Fig. 7); **query-aware contextualization** (placing query **before and after** data) yields **near-perfect** key–value performance but **minimal change** for multi-doc QA trends (Sec. 4.2).
- **Architecture probe (Sec. 4.1):** Encoder–decoder models (Flan-T5-XXL, Flan-UL2) are **robust within training-time lengths**, but show U-shape when evaluated **beyond** (e.g., encoder training max noted as **2048 tokens** for UL2).

</details>

### 📊 Lost-in-the-Middle (Long-Context Utilization Curves)
**Benchmark** · [source](https://cs.stanford.edu/~nfliu/papers/lost-in-the-middle.arxiv2023.pdf)

*Canonical “lost-in-the-middle” U-shaped accuracy curves vs. position of relevant evidence in long contexts; setups for multi-doc QA + synthetic key–value retrieval.*

<details>
<summary>Key content</summary>

- **Core finding (Fig. 1, Fig. 5, Fig. 7):** Accuracy is **highest when relevant info is at the beginning (primacy) or end (recency)** of the context and **drops in the middle** (U-shaped “lost-in-the-middle” curve), even for explicitly long-context models.
- **Multi-document QA task (Sec. 2.1):**
  - Input: question + **k documents**, with **exactly 1 answer-containing doc** and **k−1 distractors**.
  - Data: **NaturalQuestions-Open**, **2655** queries where long answer is a paragraph.
  - Docs: Wikipedia chunks **≤100 tokens**. Distractors retrieved by **Contriever (MS-MARCO fine-tuned)**; presented in **decreasing relevance**.
  - Controls: vary **context length** by changing total docs (**10/20/30**; ~**2K/4K/6K tokens**), and vary **answer-doc position** by reordering docs.
  - Metric: **accuracy** = any gold answer string appears in output.
- **Closed-book vs oracle baselines (Table 1, multi-doc QA accuracy):**
  - LongChat-13B (16K): **35.0%** closed-book, **83.4%** oracle
  - MPT-30B-Instruct: **31.5%**, **81.9%**
  - GPT-3.5-Turbo: **56.1%**, **88.3%**
  - GPT-3.5-Turbo (16K): **56.0%**, **88.6%**
  - Claude-1.3: **48.3%**, **76.1%**
  - Claude-1.3 (100K): **48.2%**, **76.4%**
  - Notable comparison (Sec. 2.3): GPT-3.5-Turbo **worst-case (middle)** in 20/30-doc settings can be **< closed-book 56.1%**.
- **Extended context ≠ better utilization (Sec. 2.3):** When prompts fit both windows, **GPT-3.5 (4K) vs GPT-3.5 (16K)** curves are **nearly identical** (Fig. 5); similarly **Claude-1.3 vs Claude-1.3-100K**.
- **Synthetic key–value retrieval (Sec. 3):**
  - Input: JSON with **k UUID→UUID pairs** + query key; output associated value (Fig. 6).
  - k tested: **75/140/300 pairs** (~**4K/8K/16K tokens**), **500 examples each**.
  - Result: some models (notably **Claude-1.3 / 100K**) near-perfect; others show **middle-position degradation** (Fig. 7).
- **Query-aware contextualization (Sec. 4.2):**
  - Put query **before and after** data.
  - Effect: **dramatically improves key–value retrieval** (e.g., GPT-3.5-Turbo-16K becomes **perfect** at **300 pairs**; without it, **worst-case 45.6%**), but **minimal improvement** for multi-doc QA (Fig. 9).
- **Architecture effect (Sec. 4.1):** Encoder–decoder (Flan-UL2, Flan-T5-XXL) is **robust within training-time lengths** (Flan-UL2: **1.9%** best–worst gap within **2048 tokens**), but shows U-shape **beyond** training lengths (Fig. 8).
- **More retrieved docs saturate (Sec. 5, Fig. 11):** In open-domain QA, reader accuracy saturates well before retriever recall; using **50 vs 20 docs** yields only **~+1.5% (GPT-3.5)** and **~+1% (Claude-1.3)**.

</details>

### 📊 MMNeedle (Multimodal Needle-in-a-Haystack) long-context benchmark
**Benchmark** · [source](https://arxiv.org/abs/2406.11230)

*Concrete NIAH-style multimodal evaluation design + reported accuracy drops as visual context (images × stitched sub-images) grows; includes negative-sample hallucination.*

<details>
<summary>Key content</summary>

- **Task (Sec. 3.1):** Given an **image haystack** (sequence of images; each may be a stitched grid of sub-images) + a **caption query** describing one sub-image, model must output the needle location.
- **Context-length construction (Sec. 3.2):**
  - Vary **#input images** \(N \in \{1,10\}\) (10 chosen because GPT-4V/4o max images/request).
  - **Image stitching:** stitch \(s \times s\) sub-images into one image; \(s \in \{1,2,4,8\}\). Total sub-images in context = \(N \cdot s^2\) (e.g., \(N{=}10,s{=}8 \Rightarrow 640\) sub-images).
  - Sub-image resize: **256×256** px; stitched resolutions: \(s{=}2\Rightarrow512^2\), \(4\Rightarrow1024^2\), \(8\Rightarrow2048^2\). 2048 chosen due to API image-size limits (GPT-4 long side ~2000 px; Claude max 8000×8000).
- **Dataset sampling (Sec. 3.3):** MS COCO 2014 val; **5000 positive + 5000 negative** per \((N,s,\#needles)\) setting. Steps: build stitched images → sample 10-image haystacks → pick needle sub-image inside haystack (positive) or outside (negative) → use COCO caption(s) as query.
- **Metrics (Sec. 3.4):**
  - Output format (positive): “\(i,r,c\)” where \(i\)=image index (1..N), \(r,c\)=row/col (1..s). Negative: “-1”.
  - **ExistenceAcc**, **IndexAcc**, **ExactAcc** with relation: **ExactAcc ≤ IndexAcc ≤ ExistenceAcc**.
- **Key empirical results (Tables 2–3):**
  - **Single image (N=1):** GPT-4o ExactAcc **94.60% (s=1)**, **83.00% (s=2)**, **19.00% (s=4)**; Gemini 1.5 best at **s=4: 29.81%**.
  - **Multi-image (N=10):** GPT-4o ExactAcc **97.00% (s=1)** → **81.80% (s=2)** → **26.90% (s=4)** → **1.00% (s=8)**; IndexAcc drops **97.0% → 87.2% → 45.0% → 17.8%**.
  - Open-source models: near-zero ExactAcc in multi-image settings (e.g., LLaVA-Llama-3 ExactAcc **0.00%** across \(s=1,2,4,8\) for \(N=10\)).
- **Negative samples (Sec. 4.3):** Strong retrievers (e.g., GPT-4o) show worse **existence accuracy** in harder negative settings → hallucination: predicting a needle exists when it doesn’t.
- **Statistical significance (Sec. 4.4):** ExactAcc stabilizes after ~**500 samples**; standard error decreases markedly from **100→1000** samples.

</details>

### 📊 NoLiMa — Long-context eval without literal-match shortcuts
**Benchmark** · [source](https://arxiv.org/html/2502.05167v2)

*Needle-in-a-haystack-style long-context evaluation where questions/needles have *minimal lexical overlap*, forcing latent association retrieval; reports degradation across long context lengths + ablations (distractors, hops, CoT).*

<details>
<summary>Key content</summary>

- **Core task design (Section 3):** Hide a single **needle** (fact about a unique character) inside a long irrelevant **haystack** (book snippets). Ask a question whose keyword **q** is *associatively linked* to needle keyword **k** (world knowledge/commonsense), with minimal literal overlap.  
  - Example: Needle “Yuki lives next to the **Semper Opera House** (k)” + Question “Which character has been to **Dresden** (q)?” (association: Semper Opera House → Dresden).  
  - **Latent hops:** 1-hop vs 2-hop (e.g., Dresden → Saxony).
  - **Fact order variants:** **Default** (character name before k) vs **Inverted** (name after k); inverted harder due to causal attention backtracing limits.
- **Haystack construction + filtering (Section 3.1):**
  - Build haystacks by concatenating random **<250-token** snippets from **10 open-licensed books** until **>2K lines / >60K tokens**.
  - **Distractor filtering:** Contriever embeddings; inspect **top-20** similar words to question keywords; remove sentences containing flagged words.
  - **Conflicting-info filtering:** scan chunks (**1000 chars**, **800-char stride** ≈ **250 tokens**); instruction-tuned LLM flags potential false answers; manual review.
- **Evaluation setup (Section 4):**
  - **58** question–needle pairs; **5** haystacks; each needle placed **26** times at equal intervals per context length ⇒ **7,540 tests per length**.
  - Lengths tested: **250, 500, 1K, 2K, 4K, 8K, 16K, 32K**.
  - **Base score:** for each example, take **max** accuracy over {250,500,1K} (avg over 5 haystacks), then average across examples.
  - **Effective length:** largest tested length with score ≥ **0.85 × base_score**.
- **Key empirical results (Table 3): strong short-context, sharp long-context drop**
  - **GPT-4o:** base **99.3**; **8K 89.2**, **16K 81.6**, **32K 69.7**; effective length **8K** (claimed 128K).
  - **Gemini 1.5 Pro:** base **92.6**; **32K 48.2**; effective length **2K** (claimed 2M).
  - **Llama 3.3 70B:** base **97.3**; **32K 42.7**; effective length **2K**.
  - At **32K**, **10/12** models fall to **≤50% of base**; at **32K** “10 models drop below 50% of strong short-length baselines.”
- **CoT prompting gains but doesn’t fix long contexts (Table 4):**
  - **One-hop:** 32K **56.2 → 60.6** with CoT.
  - **Two-hop:** 32K **25.9 → 34.3** with CoT (bigger relative gains; still poor ≥16K).
- **Literal-match ablations (Section 4.4.4, Table 6):**
  - **Direct (literal overlap like vanilla NIAH):** **~98.3–98.5** at **8K/16K/32K** (near-saturated).
  - **Multiple-choice adding literal matches:** One-hop **32K 93.1**; Two-hop **32K 87.2** (vs non-literal one-hop **56.2**, two-hop **25.9**).
  - **Distracting literal matches** (irrelevant overlap inserted) severely hurt: GPT-4o effective length drops to **1K** (base also drops: GPT-4o **93.8**, Llama 3.3 70B **84.4**).
- **Needle position findings (Section 4.4.2):**
  - “Lost-in-the-middle” dip at **32K**.
  - In **two-hop**, performance depends more on **context length** than needle position; aligning placements in the **last 2K tokens** shows drops not explained by RoPE distance (relative distance constant), implicating attention limits without surface cues.

</details>

### 📖 vLLM Engine Args (Long-Context & KV/Attention-Relevant Flags)
**Reference Doc** · [source](https://docs.vllm.ai/en/v0.6.1/models/engine_args.html)

*Authoritative CLI/API parameter names + defaults for vLLM serving settings that affect long-context behavior, KV cache, and performance.*

<details>
<summary>Key content</summary>

- **Context length control**
  - `--max-model-len`: *Model context length*; if unset, **auto-derived from model config**.
  - `--disable-sliding-window`: disables sliding window behavior (caps to sliding window size otherwise).
- **RoPE / context extension knobs**
  - `--rope-scaling`: RoPE scaling JSON, e.g. `{"type":"dynamic","factor":2.0}` (factor scales context).
  - `--rope-theta`: RoPE theta; used with `rope_scaling` and can improve performance of scaled models.
- **KV cache memory/accuracy tradeoffs**
  - `--kv-cache-dtype {auto, fp8, fp8_e5m2, fp8_e4m3}`; default **auto** (= model dtype). CUDA 11.8+ supports FP8; ROCm supports `fp8_e4m3`.
  - `--quantization-param-path`: JSON scaling factors for KV cache (generally needed for FP8 KV); otherwise scaling defaults to **1.0** (may hurt accuracy).
- **Batching/scheduling limits impacting long prompts**
  - `--max-num-batched-tokens`: max batched tokens per iteration (throughput/latency tradeoff).
  - `--max-num-seqs`: default **256** sequences per iteration.
  - `--enable-chunked-prefill`: chunk prefill based on `max_num_batched_tokens` (helps very long prompts).
- **CUDA graphs vs eager fallback (long seq performance)**
  - `--max-seq-len-to-capture`: default **8192**; sequences longer fall back to eager mode.
  - `--enforce-eager`: always eager-mode PyTorch (disables CUDA-graph hybrid).
- **Memory provisioning**
  - `--gpu-memory-utilization`: default **0.9** fraction of GPU memory for executor.
  - `--swap-space`: default **4 GiB per GPU**.
  - `--cpu-offload-gb`: default **0**; “virtual GPU memory” via CPU offload (requires fast interconnect).
- **KV block granularity**
  - `--block-size {8,16,32}`; default **16** (token block size for contiguous chunks).

</details>

### 📋 # Source: https://aclanthology.org/2024.tacl-1.9/
**Source** · 

### 📋 YaRN (RoPE context extension + dynamic scaling)
**Code** · [source](https://arxiv.org/html/2309.00071v3)

*End-to-end YaRN method + concrete training/eval settings and released 64k/128k Llama 2 variants; shows how scaling schedules are applied.*

<details>
<summary>Key content</summary>

- **Goal/notation (Sec. 2.2):** pretrained max context \(L\); extend to \(L'\). **Scale factor** \(s=L'/L\). **RoPE wavelength** for dim \(i\): \(\lambda_i = 2\pi/\theta_i\) (Eq. 8 conceptually; used to reason about “high vs low frequency” dims).
- **Position Interpolation (PI) (Eq. 9 / App. A.1 Eq. 16):** modify RoPE by scaling positions: \(m(t)=t/s\) (i.e., interpolate indices into pretrained range).
- **YaRN attention “length scaling” (Sec. 3.3):** modify attention softmax temperature:  
  \(\text{Attn}(q,k)=\text{softmax}\!\left(\frac{qk^\top}{\tau}\right)\) (Eq. 14). Implemented by scaling rotary embeddings (no attention-kernel code change; cached RoPE ⇒ **zero overhead**).
- **Dynamic Scaling (Sec. 3.4):** during inference, set scale factor per forward pass to current sequence length (vs fixed max). **KV-cache caveat:** cache K/V **before** applying RoPE because RoPE changes when scale changes.
- **Recommended YaRN params for LLaMA/Llama 2 (Def. 2, Eq. 15):** provides fitted defaults for \(\beta\) (temperature/length scaling) as a function of extension factor; authors report it transfers across LLaMA 7B–65B and Llama 2 7B–70B.
- **Training pipeline (Sec. 4.1):** Llama 2 7B/13B to **128k**: PG19, chunked **64k** segments with BOS/EOS; AdamW, **lr \(2\times10^{-5}\)**, **no weight decay**, **20-step warmup**, \(\beta_1=0.9,\beta_2=0.95\); FSDP + FlashAttention2. Steps: **400** (64k model), then **+200** more to reach 128k.
- **Key results (Sec. 4.2 Table 1):** Llama 2 7B YaRN (4k→64k, 400 steps) perplexity on Proof-pile: **8k 3.51; 16k 2.99; 32k 2.65; 64k 2.42**. 7B YaRN (4k→128k, 400+200): **8k 3.56; 16k 3.04; 32k 2.70; 64k 2.45; 128k 2.37** (“train short, test long” extrapolation).
- **Passkey retrieval (App. B.5):** YaRN 7B @128k: **99.4%**; YaRN 13B @128k: **99.4%**.

</details>

---

## Related Topics

- [[topics/rag-retrieval|RAG & Retrieval]]
- [[topics/inference-optimization|Inference Optimization]]
- [[topics/transformer-architecture|Transformer Architecture]]
- [[topics/scaling-laws|Scaling Laws]]
