---
title: "Tokenization"
subject: "Foundational AI"
date: 2025-04-06
tags:
  - "subject/foundational-ai"
  - "level/beginner"
  - "level/intermediate"
  - "level/advanced"
  - "educator/andrej-karpathy"
  - "educator/lilian-weng"
  - "resource/video"
  - "resource/blog"
  - "resource/deep-dive"
  - "resource/paper"
  - "resource/code"
educators:
  - "Andrej Karpathy"
  - "Lilian Weng"
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

# Tokenization

## Video (best)
- **Andrej Karpathy** — "Let's build the GPT Tokenizer"
- **Watch:** [YouTube](https://www.youtube.com/watch?v=zduSFxRajkE)
- Why: Karpathy builds a BPE tokenizer from scratch, covering byte-level encoding, vocabulary construction, special tokens, and the quirks that cause LLM failures. It's the most thorough hands-on treatment of tokenization available on YouTube — 2+ hours of dense, practical content that bridges theory and implementation seamlessly. Already validated in the existing curation.
- Level: intermediate

## Blog / Written explainer (best)
- **Hugging Face / NLP Course** — "Tokenizers (Chapter 6: Building a Tokenizer, Block by Block)"
- **Link:** [https://huggingface.co/learn/nlp-course/chapter6/1](https://huggingface.co/learn/nlp-course/chapter6/1)
- Why: The HF NLP course chapter on tokenizers is the most pedagogically complete written resource: it covers BPE, WordPiece, Unigram, and SentencePiece with clear diagrams, worked examples, and runnable code. It directly addresses subword tokens, vocabulary size trade-offs, and special tokens — all the related concepts listed for this topic.
- Level: beginner–intermediate

## Deep dive
- **Lilian Weng** — "Reducing the Cost of LLM Training: Tokenization and Vocabulary"
- url: https://lilianweng.github.io/posts/2023-01-27-the-transformer-family-v2/ [VERIFY — this is the Transformer Family v2 post, not a tokenization deep-dive; a dedicated tokenization post URL needs identification]
- Why: Weng's writing is the gold standard for comprehensive technical surveys. Her posts synthesize original papers, implementation details, and empirical findings in one place.
- Level: advanced

> ⚠️ **Note:** I am not fully confident in the exact URL above. A more reliably verifiable deep-dive alternative is:
- **HuggingFace Tokenizers documentation / conceptual guide**
- **Link:** [https://huggingface.co/docs/tokenizers/conceptual/algorithm](https://huggingface.co/docs/tokenizers/conceptual/algorithm)
- Why: Covers BPE, Unigram, and WordPiece algorithms with pseudocode and complexity analysis. Authoritative, maintained, and technically precise.
- Level: intermediate–advanced

## Original paper
- **Sennrich et al. (2016)** — "Neural Machine Translation of Rare Words with Subword Units" (the BPE tokenization paper)
- **Link:** [https://arxiv.org/abs/1508.07909](https://arxiv.org/abs/1508.07909)
- Why: This is the seminal paper that introduced Byte Pair Encoding to NLP tokenization. It is short (~9 pages), clearly written, and directly motivated the subword tokenization approach used in virtually every modern LLM. The most important single paper for this topic.
- Level: intermediate

## Code walkthrough
- **Andrej Karpathy** — "Let's build the GPT Tokenizer" (same video, but the accompanying repo is the code walkthrough)
- **Link:** [https://github.com/karpathy/minbpe](https://github.com/karpathy/minbpe)
- Why: The `minbpe` repository implements a minimal, readable BPE tokenizer in ~200 lines of Python. It is the clearest available code reference for understanding how tokenization actually works, with tests and a training script. Directly accompanies the video above, making it ideal for paired study.
- Level: intermediate

## Coverage notes
- **Strong:** BPE algorithm, subword tokens, vocabulary size trade-offs, special tokens, GPT-style tokenization — all excellently covered by Karpathy's video + minbpe + HF NLP course.
- **Weak:** Speech tokenization (EnCodec, Residual Vector Quantization) — the resources above focus on text tokenization. The multimodal/audio tokenization angle is underserved by the curated resources.
- **Gap:** No single excellent YouTube video exists specifically for **speech tokenization / EnCodec / RVQ** as used in audio LLMs (e.g., AudioLM, MusicGen). The intro-to-multimodal course will need a dedicated resource for this sub-topic. The EnCodec paper itself (arxiv.org/abs/2210.13438) is the best available reference, but no strong pedagogical explainer video has been identified.

## Cross-validation
This topic appears in 2 courses: **intro-to-llms** (text tokenization focus: BPE, vocabulary, special tokens) and **intro-to-multimodal** (speech tokenization focus: EnCodec, RVQ). The existing curated videos (all `zduSFxRajkE`, duplicated 5×) cover the LLM side well but leave the multimodal/speech side without a dedicated resource. Deduplication of the five identical entries is recommended.

---

## Additional Resources for Tutor Depth

> **7 sources** — papers, official docs, working code, benchmarks, and deep explainers that give the AI tutor precision on this topic.

### 📄 EnCodec Residual Vector Quantization (RVQ) + Loss Objective
**Paper** · [source](https://arxiv.org/pdf/2210.13438.pdf)

*RVQ formulation (residual recursion, codebook summation) + commitment loss + full generator objective*

<details>
<summary>Key content</summary>

- **RVQ procedure (Section 3.2):** Quantize encoder latent with multiple codebooks sequentially by **quantizing residuals**. Output latent from encoder has shape **z ∈ ℝ[B, D, T]**. RVQ produces discrete indices **i ∈ [B, Nq, T]** where **Nq** = number of codebooks used (bandwidth-dependent). To reconstruct a quantized latent vector before the decoder, **sum selected codebook entries across codebooks** (one entry per codebook per time step).
- **Training mechanics (Section 3.2):**
  - **Straight-through estimator** for encoder gradients (treat quantization as identity in backward pass).
  - Codebook entries updated by **EMA** with **decay 0.99**; unused entries **replaced** with candidates sampled from current batch.
  - **Variable-bandwidth training:** randomly select **Nq as a multiple of 4** (24 kHz supports **1.5/3/6/12/24 kbps**).
  - Typical config: up to **32 codebooks** (24 kHz) or **16** (48 kHz), each with **1024 entries** (= **10 bits/codebook**).
- **Commitment loss (Eq. 3, Section 3.4):** for residual steps **c = 1..C** (C depends on bandwidth), with residual **z_c** and nearest codebook vector **q_c(z_c)**:  
  \[
  \ell_w = \sum_{c=1}^{C} \|z_c - q_c(z_c)\|_2^2
  \]
  Gradient is computed **only w.r.t. z_c** (not the quantized vector).
- **Full generator loss (Eq. 4):**  
  \[
  L_G=\lambda_t\ell_t+\lambda_f\ell_f+\lambda_g\ell_g+\lambda_{feat}\ell_{feat}+\lambda_w\ell_w
  \]
  where **time L1**: \(\ell_t(x,\hat x)=\|x-\hat x\|_1\); **multi-scale mel loss** \(\ell_f\) (Eq. 1); adversarial + feature matching (Eq. 2).
- **Key empirical bandwidth result (Table 1):** EnCodec **3.0 kbps** becomes **1.9 kbps** with entropy coding; **6.0→4.1 kbps**, **12.0→8.9 kbps**.

</details>

### 📄 EnCodec end-to-end neural audio tokenization (streaming + RVQ + bitrate control)
**Paper** · [source](https://arxiv.org/abs/2210.13438)

*EnCodec pipeline: streaming encoder/decoder, residual vector quantizer stack producing discrete codes, and bitrate control rationale.*

<details>
<summary>Key content</summary>

- **Pipeline (Section 3):** audio \(x\) → encoder \(E\) outputs latent \(z\) → quantizer \(Q\) outputs quantized latent \(z_q\) → decoder \(G\) reconstructs \(\hat{x}\). Trained end-to-end with reconstruction + adversarial losses; RVQ commitment loss applies to encoder.
- **Streaming encoder/decoder (Section 3.1):**
  - Encoder: 1D conv (kernel 7, \(C\) channels) → \(B\) conv blocks (residual unit + strided conv downsampling; strided conv kernel \(K=2S\); channels double after downsampling) → 2-layer LSTM → final 1D conv (kernel 7, \(D\) channels).
  - Decoder mirrors encoder with transposed convolutions.
  - **Latency:** streamable padding enables output of **320 samples (13 ms)** once first 320 samples received.
  - **Latent rate:** at **24 kHz: 75 latent steps/s**; at **48 kHz: 150 steps/s**.
  - Streaming uses **weight normalization** (layer norm ill-suited for streaming).
- **Residual Vector Quantization (Section 3.2):**
  - Iterative quantization of residuals; codebooks updated by EMA (decay **0.99**); unused entries replaced from current batch.
  - Straight-through estimator for encoder gradients; **commitment loss** = MSE between quantizer input/output (grad only w.r.t. input).
  - **Bitrate control:** train with **variable number of residual steps** so one model supports multiple bandwidths.
- **Losses (Section 3.4):**
  - Time loss: \(\ell_t(x,\hat{x})=\|x-\hat{x}\|_1\).
  - Freq loss (Eq. 1): \(\ell_f=\sum_i \|S_i(x)-S_i(\hat{x})\|_1+\alpha_i\|S_i(x)-S_i(\hat{x})\|_2\), with \(S_i\)=64-bin mel-spec; window \(2^i\), hop \(2^i/4\), \(i\in\{5,\dots,11\}\), \(\alpha_i=1\).
  - Generator objective (Eq. 4): \(L_G=\lambda_t\ell_t+\lambda_f\ell_f+\lambda_g\ell_g+\lambda_{feat}\ell_{feat}+\lambda_w\ell_w\).
  - **Balancer:** sets \(\lambda_i\) as fraction of total gradient; uses EMA of gradient norms with \(R=1\), \(\beta=0.999\). (Commitment loss excluded.)
  - Example weights: 24 kHz \(\lambda_t=0.1,\lambda_f=1,\lambda_g=3,\lambda_{feat}=3\); 48 kHz \(\lambda_g=4,\lambda_{feat}=4\).
- **Optional entropy coding (Section 3.3):** lightweight causal Transformer predicts per-codebook distributions (e.g., **1024** entries); causal receptive field **3.5 s**; can reduce bandwidth **up to 40%** while faster than real time.

</details>

### 📄 Residual Vector Quantization (RQ) & QINCo objectives
**Paper** · [source](https://arxiv.org/pdf/2401.14732.pdf)

*Clear RQ/RVQ recursion + training objectives (Eqs. 2–3) and “implicit neural codebooks” conditioning on partial reconstruction.*

<details>
<summary>Key content</summary>

- **Conventional Residual Quantization (RQ) recursion (Sec. 3):**  
  Quantize vectors \(x\in\mathbb{R}^d\) over \(M\) steps with codebooks \(C_m\in\mathbb{R}^{d\times K}\) (columns are centroids \(c_{m,k}\)).  
  Initialize reconstruction \(\hat x_0=0\). Residual at step \(m\): \(r_m = x-\hat x_{m-1}\).  
  Encode by nearest centroid: \(k_m=\arg\min_k \|r_m - c_{m,k}\|^2\), choose \(q_m=c_{m,k_m}\).  
  Decode/add: \(\hat x_m=\hat x_{m-1}+q_m\). Final \(\hat x=\hat x_M\). Indices \((k_1,\dots,k_M)\) stored (bits \(\approx M\log_2 K\)).
- **QINCo: implicit neural codebooks (Sec. 3.1):** fixed per-step codebook is suboptimal because residual distribution depends on previous choices. QINCo generates a *specialized* codebook per step conditioned on partial reconstruction:  
  \(C_m(\hat x_{m-1}) = f_{\theta_m}(\hat x_{m-1},\, C_m^{\text{base}})\) (residual-style MLP blocks; base codebooks initialized from pretrained RQ; base codebooks also trainable).
- **Training objective (Sec. 3.2):** per-step “elementary” loss (Eq. 2) is MSE between residual and selected centroid; total loss sums across steps (Eq. 3):  
  \(L=\sum_{m=1}^M \|r_m - q_m\|^2\). Gradients from later steps backprop to earlier steps because \(r_m,\ q_m\) depend on \(\theta\).
- **Sequential decoding in QINCo (Sec. 3.2):** must reconstruct step-by-step since codebook generation needs \(\hat x_{m-1}\).
- **Empirical compression/search (Tab. 1):** BigANN1M R@1: **QINCo 45.2** vs RQ 27.9 (8 bytes); **QINCo 71.9** vs RQ 49.0 (16 bytes). Deep1M R@1: **36.3** vs 21.4 (8B); **59.8** vs 43.0 (16B). MSE also substantially lower (e.g., BigANN1M 8B: **1.12** vs 2.49).
- **Defaults noted:** common setting \(K=256\) (8 bits/step); “8 bytes” \(\Rightarrow M=8\), “16 bytes” \(\Rightarrow M=16\). QINCo trained with Adam, effective batch size 1024, LR decay ×10 on val plateau (10 epochs), early stop after 50 epochs no improvement (App. A.3).

</details>

### 📊 SoundStream RVQ tokenization & bitrate–quality benchmarks
**Benchmark** · [source](https://arxiv.org/pdf/2107.03312.pdf)

*Bitrate ↔ perceptual/objective quality curves; RVQ ablations (Nq, codebook size); comparisons vs Opus/EVS/Lyra; scalable (dropout) vs bitrate-specific.*

<details>
<summary>Key content</summary>

- **Encoder frame rate / bitrate math (Sec. III-A, III-C):** With sampling rate \(f_s=24\,\text{kHz}\) and total stride \(M\), frames/sec \(S=f_s/M\). Default strides \((2,4,5,8)\Rightarrow M=320\Rightarrow S=75\) frames/sec (13.3 ms/frame). Bits/frame \(r=R/S\). Example \(R=6000\) bps ⇒ \(r=80\) bits/frame.
- **Plain VQ infeasible (Sec. III-C):** single codebook size \(N=2^r\). At \(r=80\), \(N=2^{80}\) vectors (infeasible).
- **Residual Vector Quantization algorithm (Alg. 1):** For quantizers \(Q_i\), \(i=1..N_q\):  
  init \(\hat y=0\), residual \(=y=\text{enc}(x)\); loop: \(\hat y \mathrel{+}=Q_i(\text{residual})\); residual \(\mathrel{-}=Q_i(\text{residual})\). Output \(\hat y\).  
  Rate split: \(r_i=r/N_q=\log_2 N\) (uniform); total bits/frame \(=N_q\log_2 N\).
- **Bitrate scalability via quantizer dropout (Sec. III-C):** sample \(n_q\sim\text{Uniform}\{1..N_q\}\) per example; use only \(Q_1..Q_{n_q}\). At inference choose \(n_q\) for desired bitrate; embedding dimensionality unchanged (additive refinement).
- **Training objective (Eq. 1–6):** hinge GAN discriminator loss \(L_D\) (Eq.1), generator adversarial \(L_G^{adv}\) (Eq.2), feature loss \(L_G^{feat}\) (Eq.3), multi-scale mel-spectrogram recon \(L_G^{rec}\) (Eq.4–5). Weights: \(\lambda_{adv}=1,\lambda_{feat}=100,\lambda_{rec}=1\) (Eq.6).
- **Subjective benchmark (Fig. 5):** SoundStream **3 kbps** significantly > Opus **6 kbps** and EVS **5.9 kbps**; to match SoundStream quality: **EVS ≥9.6 kbps**, **Opus ≥12 kbps** (≈3.2×–4× more bits). SoundStream @3 kbps > Lyra @3 kbps.
- **Objective metric:** ViSQOL used; at **3 kbps** ViSQOL ≈ **3.76**; at **6 kbps** ≈ **3.96**; quality remains > **3.7** even at lowest bitrate (Fig.7a).
- **Ablation—learned encoder matters (Sec. V-D):** replacing encoder with fixed mel-filterbank drops ViSQOL **3.96 → 3.33** at 6 kbps.
- **RVQ depth vs codebook (Table II, 6 kbps):**  
  \(N_q=8,N=1024\): ViSQOL **4.01±0.03**; \(N_q=16,N=32\): **3.98±0.03**; \(N_q=80,N=2\): **3.92±0.03**.
- **Latency trade-off (Table III, 6 kbps):** strides \((1,4,5,8)\) latency **7.5 ms**, \(N_q=4\), ViSQOL **4.01±0.02**; default \((2,4,5,8)\) **13 ms**, \(N_q=8\), **4.01±0.03**; \((4,4,5,8)\) **26 ms**, \(N_q=16\), **4.01±0.03**.

</details>

### 📊 Subword tokenizers (BPE vs WordPiece vs SentencePiece/Unigram) — comparison metrics & scaling
**Benchmark** · [source](https://arxiv.org/html/2411.17669v1)

*Structured comparison criteria across BPE, WordPiece, SentencePiece(Unigram): vocab-size effects, efficiency (fertility), contextual specialization, domain-boundary alignment, linguistic-law framing.*

<details>
<summary>Key content</summary>

- **Tokenizers compared (Section II/IV):**
  - **BPE:** start with all symbols; iteratively **merge most frequent pair** until target vocab size.
  - **WordPiece:** like BPE but merges based on **likelihood improvement** of training data after adding token.
  - **SentencePiece (Unigram LM):** treats input as **raw stream** (space is a character); uses **Unigram** approach (start large, **iteratively discard tokens** to reach target vocab).
- **Training/data pipeline (Section III/IV):**
  - Protein: **UniRef50**; train tokenizers on **15M sequences** (train split). Evaluate on **validation+test = 11,957 sequences**; discard **14** test sequences **>3k residues**.
  - Natural-language baseline: **WikiText**; train **BPE** on **4.2M sentences**; evaluate on **validation+test = 19,720 sentences**.
  - **Vocabulary sizes:** **400, 800, 1600, 3200, 6400** for each protein tokenizer.
- **Shared-token overlap vs vocab size (Section IV-A):**
  - At **400**: BPE–WordPiece overlap **0.98**; BPE–SentencePiece **0.83**; WordPiece–SentencePiece **0.84**.
  - At **6400**: BPE–WordPiece **0.72**; SentencePiece overlap with each **0.47**.
- **Token length & efficiency (fertility) (Section IV-B):**
  - In **training vocab**, BPE learns **longest avg tokens**, then WordPiece; SentencePiece shortest.
  - In **test data**, trend reverses: **BPE shortest**, WordPiece next, **SentencePiece longest**.
  - **Fertility = #tokens needed to encode a sequence**: BPE higher fertility; SentencePiece lower; WordPiece in-between.
- **Contextual exponence (Section IV-C):** measured as **# unique neighbors per token** in test data; for vocab **800–3200**, beyond ~first **100 tokens**, **BPE has lower distinct-neighbor counts** → more contextually consistent/specialized tokens. At **6400**, SentencePiece plot flattens; WordPiece becomes more BPE-like after ~**300 tokens**.
- **Protein domain boundary alignment (Section IV-D):**
  - Domains from **PROSITE**: **4,646 domains** in **3,377** test sequences.
  - A domain is a **hit** if **domain start aligns with token start AND domain end aligns with token end**.
  - **BPE best**, but **performance declines as vocab increases** (longer tokens). Boundary alignment correlates with **shorter token lengths**; overall accuracy “relatively low” even at small vocabs → NLP tokenizers don’t capture true protein subunits well.
- **Heaps’ Law equation (Eq. 1 / Section IV-G):**  
  - \( V(N) = K \, N^{\beta} \)  
  - \(V\): estimated vocabulary size; \(N\): total token count; \(K\) typically **10–100**; \(\beta\) typically **0.4–0.6**. All tokenizers follow closely; SentencePiece saturates slightly faster.

</details>

### 📋 # Source: https://docs.pytorch.org/audio/stable/generated/torchaudio.save_with_torchcodec.html
**Source** · 

### 📋 # Source: https://docs.pytorch.org/torchcodec/0.5/_downloads/11ef1d93158a89ea05a303d1d7c2cc02/audio_encoding.ipynb
**Source** ·

---

## Related Topics

- [[topics/word-embeddings|Word Embeddings]]
- [[topics/transformer-architecture|Transformer Architecture]]
- [[topics/pre-training|Pre-Training]]
- [[topics/audio-speech-models|Audio & Speech Models]]
