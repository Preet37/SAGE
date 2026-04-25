---
title: "Video Understanding"
subject: "Multimodal AI"
date: 2026-04-09
tags:
  - "subject/multimodal-ai"
  - "level/beginner"
  - "level/intermediate"
  - "level/advanced"
  - "educator/andrej-karpathy"
  - "educator/hugging-face"
  - "resource/video"
  - "resource/blog"
  - "resource/deep-dive"
  - "resource/paper"
  - "resource/code"
educators:
  - "Andrej Karpathy"
  - "Hugging Face"
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

# Video Understanding

## Video (best)
- **Andrej Karpathy** — "Deep Dive into LLMs like ChatGPT" (context for multimodal/video LLMs; not video-specific)
- youtube_id: "None identified"
- Why: Clear mental models for transformer-based language models that underpin modern video-language models (Video-LLMs).
- Level: Intermediate

## Blog / Written explainer (best)
- **Lilian Weng (OpenAI)** — "Prompt Engineering"
- **Link:** [https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/](https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/)
- Why: Practical prompting patterns that transfer directly to video QA/captioning workflows when using video-capable models (e.g., Gemini, GPT-4o).
- Level: Beginner–Intermediate

## Deep dive
- **OpenAI** — "GPT-4o" (system card / announcement + technical overview)
- Why: Primary-source description of a natively multimodal model family relevant to video understanding applications and evaluation framing.
- Level: Intermediate  
- **Link:** [https://openai.com/blog/hello-gpt-4o](https://openai.com/blog/hello-gpt-4o)
- **Google DeepMind** — "Gemini 1.5" (long-context multimodal; relevant to long-form video understanding)
- Why: Primary-source overview of long-context multimodal modeling, a key enabler for long-form video comprehension.
- Level: Intermediate  
- **Link:** [https://deepmind.google/technologies/gemini/](https://deepmind.google/technologies/gemini/)
## Original paper
- **A. Vaswani et al.** — "Attention Is All You Need"
- Why: Foundational transformer architecture used by modern video-language models and many video understanding systems.
- Level: Intermediate–Advanced  
- **Link:** [https://arxiv.org/abs/1706.03762](https://arxiv.org/abs/1706.03762)
- **A. Radford et al. (OpenAI)** — "Learning Transferable Visual Models From Natural Language Supervision" (CLIP)
- Why: Core vision-language pretraining approach widely used as a component in video retrieval/search and as a building block for video-language systems.
- Level: Intermediate  
- **Link:** [https://arxiv.org/abs/2103.00020](https://arxiv.org/abs/2103.00020)
## Code walkthrough
- **Hugging Face** — Transformers documentation (multimodal + video-related model support varies by release)
- Why: Most common practical entry point for running and adapting open multimodal models; useful for implementing video captioning/QA pipelines when supported.
- Level: Intermediate  
- **Link:** [https://huggingface.co/docs/transformers/index](https://huggingface.co/docs/transformers/index)
- **OpenAI** — API docs (multimodal usage patterns; video support depends on current API capabilities)
- Why: Canonical reference for building video understanding applications with OpenAI models where available.
- Level: Intermediate  
- **Link:** [https://platform.openai.com/docs](https://platform.openai.com/docs)
## Coverage notes
- Strong: Transformer foundations; general multimodal model overviews (GPT-4o, Gemini); practical tooling entry points (HF Transformers).
- Weak: Single, educator-grade “Video Understanding 101” video that cleanly covers video QA, captioning, long-form understanding, and evaluation end-to-end.
- Gap: High-confidence, stable, video-specific deep-dive resources (especially for Video-LLMs, long-form video benchmarks, and action recognition) with clearly identifiable canonical videos/IDs.

---

## Additional Resources for Tutor Depth

> **8 sources** — papers, official docs, working code, benchmarks, and deep explainers that give the AI tutor precision on this topic.

### 📄 Text-Conditioned Resampler (TCR) for long-video VLMs
**Paper** · [source](https://arxiv.org/abs/2312.11897)

*Mechanism to handle long videos under frame/token budgets via text-conditioned cross-attention resampling into fixed #visual tokens for an LLM.*

<details>
<summary>Key content</summary>

- **Problem:** VLM memory scales ~quadratically with input tokens; typical video-VLMs ingest **4–32 frames**. TCR enables **>100 frames (up to ~180)** in one pass by bottlenecking visual tokens into a fixed-length query set (Sec. 2.1).
- **Architecture (Sec. 2.1):**
  - Frozen **ViT-g** visual encoder → per-frame patch embeddings + **temporal embeddings**.
  - Conditioning sequence: **[ST][task prompt][learnable queries]**, where [ST] is a learned task token: **[CPN] captioning, [TRG] temporal grounding, [QA] question answering, [STG] spatio-temporal grounding**.
  - Transformer-decoder TCR: **4 blocks**, **8 heads**, **hidden dim=512**; **cross-attention in blocks 0 & 2**; output is fixed-length transformed queries → concatenated with optional text prompt → frozen **Flan-T5** LLM.
  - **Design rationale:** (i) queries interact with video only via **cross-attention** (avoids full self-attn over all frame tokens); (ii) fixed #output queries keeps LLM input small regardless of video length.
- **Differences vs Q-former/Flamingo resampler:** video-first training; **lower dim 512** (vs 768/1536) and **~69M params** (vs **188M**); separates cross-attn (to video) then self-attn (text+queries) for cheaper layers.
- **Training pipeline (Sec. 2.2):** only **TCR trained**; ViT-g + Flan-T5 frozen.
  1) **Init (no LLM):** BLIP2-style **contrastive** + **video-text matching** objectives.  
  2) **Pre-train (with LLM, YTT-1B):** generative loss on 3 tasks: (i) retrieve **when** a sentence occurred; (ii) caption segment given timestep; (iii) text **denoising/correction**.  
  3) **Fine-tune** per downstream dataset (only TCR + vocab).
- **Key empirical numbers (NextQA ablations, Table 6):**
  - Text conditioning: **yes 64.9 acc** vs **none 61.1**; adversarial corrupt prompt **55.3**.
  - #frames: **32→64.4**, **92→66.2 (best)**, **124→65.9** (videos ~44s; 124≈2.5fps).
  - #queries to LLM: **32→62.7**, **64→65.8**, **128→66.2 (best)**, **256→64.3**.
- **Efficiency trick (Sec. 2.3):** to reduce memory, for **every other frame drop random 50% patches** (reported as minimal perf loss in prior work).
- **Time tokenization (Appx):** half-second increments; supports up to **~17 minutes** with 0.5s precision; frame timestep passed through **1-layer MLP** to form temporal embedding.

</details>

### 📄 VideoCLIP pre-training pipeline (overlap positives + retrieval hard negatives)
**Paper** · [source](https://arxiv.org/pdf/2109.14084.pdf)

*Training pipeline details for video-text contrastive pretraining: overlapped positives, retrieval-mined hard negatives, InfoNCE objective, key hyperparams/results.*

<details>
<summary>Key content</summary>

- **Encoders (Sec. 3.1):**
  - Video tokens: \(x^v = f_{\theta_{\text{MLP}}}(\text{stopgrad}(f_{\theta_{\text{CNN}}}(c^v)))\) (Eq. 1). CNN is **frozen**.
  - Transformers: \(h^v=f_{\theta_v}(x^v),\; h^t=f_{\theta_t}(x^t)\) (Eq. 2).
  - Global clip embeddings via **average pooling**: \(z^v=\text{AvgPool}(h^v),\; z^t=\text{AvgPool}(h^t)\) (Eq. 3). Rationale: encourages token-level reps (helps localization/segmentation); [CLS] pooling hurts (Table 7).
- **Contrastive objective (Sec. 3.2):**
  - Symmetric InfoNCE (Eq. 4):  
    \(\mathcal{L}=-\sum_{(v,t)\in B}\big(\log \text{NCE}(z^v,z^t)+\log \text{NCE}(z^t,z^v)\big)\).
  - Video→Text NCE (Eq. 5):  
    \(\text{NCE}(z^v,z^t)=\dfrac{\exp(z^v\cdot z_t^+/\tau)}{\sum_{z\in\{z_t^+,z_t^-\}}\exp(z^v\cdot z/\tau)}\). Negatives \(z_t^-\) are **other texts in batch**; symmetric for text→video.
- **Positive pair construction = temporal overlap (Sec. 3.3):**
  1) sample a **text clip first**; 2) sample a timestamp within it as video center; 3) grow a **random-duration** video clip (up to ~32s). Rationale: strict start/end alignment often low semantic relevance.
- **Hard negatives via retrieval-augmented batching (Sec. 3.4, Alg. 1):**
  - Each epoch: compute per-video global feature \(z_V=\frac{1}{2|B_V|}\sum_{(v,t)\in B_V}(z^v+z^t)\); build FAISS index; for random video \(V\), retrieve **2k-NN**, then **sample k videos** to form a cluster/batch so clips from different but similar videos become hard negatives.
- **Defaults / hyperparams (Sec. 5.3):**
  - Video encoder: S3D pretrained on HowTo100M; 30fps; **1 token/sec**, dim 512 → MLP to 768; max **32 video tokens** (3–32s).
  - Text: 8–61 tokens (plus [CLS],[SEP]); avg ASR ~2.4 tokens/sec.
  - Batch: **k=32 videos**, **16 pairs/video** ⇒ \(|B|=512\). Temperature \(\tau=1.0\).
  - Init: BERT-base uncased; **6 layers** for video, **12** for text.
  - Train: 8×V100 32GB, fp16, **25 epochs**; Adam lr 5e-5, warmup 1000, poly decay, betas (0.9,0.98), grad clip 2.0.
- **Key empirical deltas (Table 7, Youcook2 zero-shot R@1):**
  - Full VideoCLIP: **22.7** (R@5 50.4, R@10 63.1)
  - w/o retrieval: **18.5**; w/o retrieval + w/o overlap: **12.4**
  - MIL-NCE clips+loss: **16.1**; use [CLS]: **22.1**; retrieve k directly: **22.5**; use first 32s for retrieval: **20.1**
- **Headline zero-shot results:**
  - Youcook2 retrieval: **22.7 R@1** (Table 1); COIN action segmentation: **58.9%** frame acc (Table 4); MSR-VTT VideoQA: **73.9%** (Table 3).

</details>

### 📊 EgoSchema (Very Long-form VideoQA + Temporal Certificates)
**Benchmark** · [source](https://proceedings.neurips.cc/paper_files/paper/2023/file/90ce332aff156b910b002ce4e6880dec-Paper-Datasets_and_Benchmarks.pdf)

*Dataset/task spec + “temporal certificate” metric + zero-shot baselines/human results diagnosing long-horizon video reasoning failures.*

<details>
<summary>Key content</summary>

- **Dataset spec (Abstract, Fig. 1, Datasheet):**
  - **5063 instances**; each instance = **3-minute** egocentric clip + **1 question** + **5 answer options** (label **1–5** indicates correct option).
  - Sourced from **Ego4D**; total coverage **>250 hours** of real video.
  - Raw video: **mp4**, **30 fps**, high resolution.
- **Filtering defaults (Stage I, §3.1.1):**
  - Extract **non-overlapping 3-minute clips** with **≥30 timestamped human narrations** per clip.
- **QA generation defaults (Stage II, §3.1.2):**
  - Generate **N = 3** questions per clip; **M = 4** wrong answers per question (5-way MCQ total).
  - Preferred prompting chain: **Q(AW)-shot** (2 LLM calls): generate N questions jointly, then generate all correct+wrong answers conditioned on questions.
  - LLMs found to yield good Q/A/W quality: **GPT-4, Bard, Claude**.
- **Filtering & curation (Stage III–IV, §3.1.3–§3.1.4):**
  - Rule-based keyword/format filtering.
  - **Blind filtering baseline:** LLM guesses answer from **question only**; if it can answer “blindly,” discard (precision-over-recall).
  - Human curation round 1 verifies: (A) Q well-formed & A correct, (B) all distractors wrong, (C) **temporal certificate length ≥30s**; reduces admissible Qs by **~4–5×**. Round 2: **>97%** of round-1 pass also pass.
- **Key definition (Temporal certificate, §3.2):**
  - **Temporal certificate set** = *minimum set of subclips* **necessary and sufficient** for a human to verify the annotation without watching the rest.
  - **Certificate length** = **sum of durations** of subclips in the certificate set.
  - Conventions: min subclip **0.1s**; merge certificates if gap **<5s**.
- **Empirical results (Fig. 3, Table 6–7):**
  - EgoSchema **median certificate length ~100s**; **5.7×** longer than next closest dataset; **10×–100×** longer than most others.
  - **Zero-shot model accuracy <33%** (random **20%**); **human ~76%**.
  - Table 6 examples: FrozenBiLM **26.4% (10 frames)** / **26.9% (90)**; InternVideo **31.4% (10)** / **32.0% (90)**; mPLUG-Owl peaks **30.2% (5 frames)** (non-monotonic).
  - Human settings (Table 7): **67.2% @ 1 fps (180 frames)**; **67.0% <1 min**; **68.0% <3 min**; **75.1% no constraint**; **76.2% Video→Text**.

</details>

### 📊 OVQA — Open-vocabulary VideoQA benchmark (long-tail + unseen answers)
**Benchmark** · [source](https://arxiv.org/pdf/2308.09363.pdf)

*Benchmark definition + category-wise tables measuring generalization to rare/unseen answers (distribution shift) in open-ended VideoQA.*

<details>
<summary>Key content</summary>

- **Problem (Sec.1–2):** “Open-ended” VideoQA is often implemented as **closed-vocabulary classification** over top-k frequent answers (e.g., top-1000), causing near-zero performance on **out-of-vocabulary (unseen)** answers. Example stat: in MSRVTT-QA, **top-1000 answers = 17.8% of unique answers but 90.2% of samples** (Fig.1).
- **OVQA answer categories (Sec.2.1, Table 1):** based on training frequency: **Base (≥101), Common (11–100), Rare (1–10), Unseen (0)**. Unique-answer counts:  
  - MSVD-QA: Base 41 / Common 333 / Rare 1,478 / Unseen 391 (Total 2,243)  
  - MSRVTT-QA: 205 / 937 / 2,858 / 1,632 (Total 5,632)  
  - TGIF-QA: 38 / 210 / 1,292 / 206 (Total 1,746)  
  - ActivityNet-QA: 26 / 275 / 1,353 / 1,378 (Total 3,032)
- **Task definition (Sec.2.2):** replace MLP-over-classes with **similarity between [MASK] feature** \(m\in\mathbb{R}^D\) and **answer embeddings**; report **Total acc** plus per-category (B/C/R/U) and **mAcc** = mean accuracy over unique answers.
- **GNN soft verbalizer (Sec.3, Eq.1/5–8):** message passing  
  \(h_i^{(l)}=\sigma\!\left(W^{(l)}\cdot \text{AGG}(\{h_j^{(l-1)}:j\in N_i\})\right)\) (Eq.1); GAT attention \(\alpha_{ij}^{(l)}\) (Eq.5), aggregate \(\sum_{j\in N_i}\alpha_{ij}^{(l)}h_j^{(l-1)}\) (Eq.6). Convex combine: \(\hat H=\varepsilon V+(1-\varepsilon)H\) (Eq.7). Train with CE: \(L=\text{CE}(a_{GT},\text{Softmax}(\hat H m))\) (Eq.8). Defaults: **K=2 hops**, **L=2 layers**, search \(\varepsilon\in\{0.5,0.6,0.7,0.8,0.9\}\); answer encoder frozen; use **GloVe** neighbors.
- **Key empirical results (Table 2):** CVQA models often have **U=0.0** and tiny mAcc. Example MSRVTT-QA: **VIOLET (CVQA)** T=40.9, **U=0.0**, **mAcc=1.4**. **FrozenBiLM → FrozenBiLM+ (OVQA)** improves unseen and mAcc:  
  - MSRVTT-QA: U **0.0→6.6**, mAcc **6.7→12.4**, T **46.6→47.0**  
  - TGIF-QA: U **0.0→21.3**, mAcc **23.5→30.2**, T **68.6→69.0**
- **GNN gain (Table 3):** FrozenBiLM+ w/ GNN improves unseen: MSVD **13.7→16.1**, ActivityNet **4.2→5.8**, TGIF **18.7→21.3**, MSRVTT **5.8→6.6**.

</details>

### 📖 GPT‑4o multimodal (incl. video) capability anchor
**Reference Doc** · [source](https://openai.com/index/gpt-4o/)

*Official top-level statements on GPT‑4o modality handling (text/audio/image/video), rollout status, and latency/cost/rate-limit comparisons.*

<details>
<summary>Key content</summary>

- **Multimodal I/O claim (core spec):** GPT‑4o (“omni”) *“accepts as input any combination of text, audio, image, and video and generates any combination of text, audio, and image outputs.”* (Video is explicitly listed as **input**; outputs listed: text/audio/image.)
- **Latency (audio):** Responds to audio inputs in **as little as 232 ms**, **avg 320 ms** (human-like conversational timing).
- **Prior Voice Mode pipeline (procedure):** 3-model chain:  
  1) audio→text transcription model → 2) GPT‑3.5/GPT‑4 text-in/text-out → 3) text→audio model.  
  **Rationale:** This pipeline loses information (can’t directly observe **tone**, **multiple speakers**, **background noises**) and can’t output **laughter/singing/emotion**.
- **GPT‑4o design change (procedure/rationale):** Trained **end-to-end** as a **single neural network** across **text, vision, audio** so all inputs/outputs are processed by the same network (preserves paralinguistic/audio context).
- **API availability + rollout status:** Developers can access GPT‑4o in the API **as a text and vision model**; OpenAI planned to launch **audio and video** API support to a **small group of trusted partners** “in the coming weeks” (from May 13, 2024 post).
- **Cost/speed/rate limits (empirical comparisons):** **2× faster**, **50% cheaper**, and **5× higher rate limits** vs **GPT‑4 Turbo** (API).

</details>

### 📖 OpenAI Responses API — request schema quickstart (multimodal entry point)
**Reference Doc** · [source](https://platform.openai.com/docs)

*Platform docs index + canonical “Responses API” entry point and quickstart request/response pattern (used for multimodal inputs via `input`).*

<details>
<summary>Key content</summary>

- **Primary endpoint (procedure):** Create model outputs via **Responses API**  
  - HTTP: `POST https://api.openai.com/v1/responses`  
  - Headers:  
    - `Content-Type: application/json`  
    - `Authorization: Bearer $OPENAI_API_KEY`
- **Minimal request schema (defaults shown by example):**  
  - JSON body fields used in docs quickstart:  
    - `model` (string): example `"gpt-5.4"`  
    - `input` (string): example `"Write a short bedtime story about a unicorn."`
- **SDK procedure (JavaScript):**
  1. `import OpenAI from "openai"; const client = new OpenAI();`
  2. `await client.responses.create({ model: "gpt-5.4", input: "..." })`
  3. Read text via `response.output_text`
- **SDK procedure (Python):**
  1. `from openai import OpenAI; client = OpenAI()`
  2. `client.responses.create(model="gpt-5.4", input="...")`
  3. Read text via `response.output_text`
- **SDK procedure (C#):**
  - `new OpenAIResponseClient(model: "gpt-5.4", apiKey: envVar)` then `CreateResponse("...")`, read via `GetOutputText()`.
- **Model selection guidance (design rationale):**
  - Use **`gpt-5.4`** for “complex reasoning and coding”; **`gpt-5.4-mini`** / **`gpt-5.4-nano`** for “lower-latency, lower-cost workloads.”

</details>

### 📋 # Source: https://deepmind.google/technologies/gemini/
**Source** · 

### 🔍 Vid-LLM taxonomy + training paradigms
**Explainer** · [source](https://arxiv.org/html/2312.17432v5)

*Survey taxonomy of video understanding methods and comparative discussion of Vid-LLM architectures/training across tasks.*

<details>
<summary>Key content</summary>

- **Video understanding evolution (Section I-A):**  
  1) Conventional: handcrafted features (SIFT, SURF, HOG), motion (optical flow, IDT), temporal models (HMM), classifiers (SVM/DT/RF), PCA/clustering.  
  2) Early neural: two-stream nets; LSTM/TSN for long-form; 3D CNNs (C3D, I3D); efficiency variants (S3D/ECO/P3D); long-temporal (Non-local, etc.); ViT-based video models (TimeSformer, ViViT, MViT).  
  3) Self-supervised pretraining: VideoBERT tokenizes video via hierarchical k-means; “pretrain→finetune” for downstream action classification/captioning; MAE-style video pretraining (VideoMAE, etc.).  
  4) Vid-LLMs: promptable/in-context, instruction-following; can call tools/APIs.
- **LLM core equations (Section II-B):**  
  **Eq. (1)** chain rule: \(p(x_{1:T})=\prod_{t=1}^{T} p(x_t \mid x_{<t})\), where \(T\)=sequence length.  
  **Eq. (2)** autoregressive generation: \(x_t \sim p(\cdot \mid x_{<t}; \text{LLM})\).  
  **Eq. (3)** greedy decoding: \(x_t=\arg\max_{v\in V} p(v \mid x_{<t})\), \(V\)=vocabulary (incl. SOS/EOS/PAD).
- **Vid-LLM taxonomy (Section III-A):**
  - **Video Analyzer LLM:** video→text analysis (captions, dense captions+timestamps, tracking boxes/IDs, ASR/OCR). LLM roles: **Summarizer** (unidirectional flow) vs **Manager** (LLM orchestrates analyzers, multi-round/tool-calling).
  - **Video Embedder LLM:** video encoder (ViT/CLIP; audio encoders like CLAP)→embeddings; requires **adapter** to map vision space→LLM token space. LLM roles: **Text Decoder**, **Regressor** (timestamps/boxes as continuous values), **Hidden Layer** (task head attached).
  - **(Analyzer+Embedder) LLM:** uses both text analysis + embeddings jointly (rarer).
- **Training strategies (Section III-B):**
  - **Training-free:** common for Analyzer-based systems (video parsed to text ⇒ becomes NLP).  
  - **Fine-tuning (mostly Embedder-based):**  
    1) **Full LLM fine-tune** (updates all params; higher compute; may reduce zero-shot/ICL).  
    2) **Connective adapter** (freeze embedder+LLM; train external MLP/Linear/Q-former for modality alignment).  
    3) **Insertive adapter** (e.g., LoRA inside LLM; changes behavior; common for regressor/hidden-layer).  
    4) **Hybrid adapters:** often 2-stage (align connective first, then freeze it and train insertive on target task).

</details>

---

## Related Topics

- [[topics/vision-language-models|Vision Language Models]]
- [[topics/text-to-video|Text-to-Video]]
- [[topics/multimodal-fundamentals|Multimodal Fundamentals]]
- [[topics/audio-speech-models|Audio & Speech Models]]
