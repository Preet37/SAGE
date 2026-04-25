---
title: "Audio & Speech Models"
subject: "Multimodal AI"
date: 2026-04-09
tags:
  - "subject/multimodal-ai"
  - "level/intermediate"
  - "level/advanced"
  - "educator/andrej-karpathy"
  - "educator/jay-alammar"
  - "resource/video"
  - "resource/blog"
  - "resource/deep-dive"
  - "resource/paper"
  - "resource/code"
educators:
  - "Andrej Karpathy"
  - "Jay Alammar"
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

# Audio Speech Models

## Video (best)
- **Andrej Karpathy** — "Let's build GPT: from scratch, in code, spelled out."
- **Watch:** [YouTube](https://www.youtube.com/watch?v=kCc8FmEb1nY)
- Why: Clear, practical introduction to transformer language models; transfers well to *audio language models* and *audio tokenization* concepts even though the demo is text.
- Level: Intermediate

## Blog / Written explainer (best)
- **Jay Alammar** — "The Illustrated Transformer"
- **Link:** [https://jalammar.github.io/illustrated-transformer/](https://jalammar.github.io/illustrated-transformer/)
- Why: Best high-level visual explanation of transformers; foundational for understanding Whisper-style ASR, TTS models, and audio LMs.
- Level: Beginner → Intermediate

## Deep dive
- **OpenAI** — "Whisper" (model + paper + usage)
- Why: Canonical reference for modern automatic speech recognition (speech-to-text) with a practical repo and paper.
- Level: Intermediate  
- **Link:** [https://github.com/openai/whisper](https://github.com/openai/whisper)
- **Meta AI** — "Audiocraft" (MusicGen and audio generation tooling)
- Why: Practical deep dive into *music generation* and audio generation pipelines; useful for understanding audio tokenization + generation stacks.
- Level: Intermediate  
- **Link:** [https://github.com/facebookresearch/audiocraft](https://github.com/facebookresearch/audiocraft)
## Original paper
- **Radford et al. (OpenAI)** — "Robust Speech Recognition via Large-Scale Weak Supervision" (Whisper)
- Why: Foundational ASR paper for Whisper; covers training setup, data, robustness, and evaluation.
- Level: Intermediate → Advanced  
- **Link:** [https://arxiv.org/abs/2212.04356](https://arxiv.org/abs/2212.04356)
- **Défossez et al. (Meta AI)** — "High Fidelity Neural Audio Compression" (EnCodec)
- Why: Core reference for *audio tokenization* via neural audio codecs; widely used in downstream audio language models.
- Level: Advanced  
- **Link:** [https://arxiv.org/abs/2210.13438](https://arxiv.org/abs/2210.13438)
## Code walkthrough
- **OpenAI** — Whisper repository (reference implementation)
- Why: Straightforward codebase to study end-to-end ASR inference (feature extraction, decoding, timestamps).
- Level: Intermediate  
- **Link:** [https://github.com/openai/whisper](https://github.com/openai/whisper)
- **Meta AI** — EnCodec repository
- Why: Practical implementation of neural audio compression/tokenization; useful for understanding discrete audio representations.
- Level: Advanced  
- **Link:** [https://github.com/facebookresearch/encodec](https://github.com/facebookresearch/encodec)
## Coverage notes
- Strong: Whisper / automatic speech recognition (speech-to-text); transformer foundations; EnCodec-style audio tokenization; music generation tooling (MusicGen via Audiocraft).
- Weak: Text-to-speech systems (especially VALL-E, Bark) and voice cloning—high-quality, stable, primary resources are less consistently available in canonical “teaching” formats.
- Gap: A single, educator-grade walkthrough that connects *audio tokenization → audio language model → TTS/voice cloning* end-to-end (with modern discrete codec tokens and practical training details).

---

## Additional Resources for Tutor Depth

> **6 sources** — papers, official docs, working code, benchmarks, and deep explainers that give the AI tutor precision on this topic.

### 📄 Accurate low-latency streaming ASR + joint EOS via CTC
**Paper** · [source](https://aclanthology.org/2023.acl-industry.26.pdf)

*Concrete streaming ASR architecture (chunking/streaming, endpointing, batching/beam) with latency+WER and operational choices*

<details>
<summary>Key content</summary>

- **Streaming model architecture (Sec. 3.1):** 3-level hierarchical CTC (HCTC): predict **characters (73 tokens)** → **short subwords (300)** → **long subwords (5000)**. LSTM-attention blocks per level: **N = 5, 5, 2** layers; each LSTM has **700 hidden dims**.  
- **Windowed self-attention for streaming:** Multi-head self-attention with **8 heads**, **64-d** key/query/value per head; attention restricted to **5-frame window (t±2)** to preserve streaming. Skip connections + layer norm after each layer.
- **Input features:** **80 log-mel filterbanks**, window **20 ms**, stride **10 ms**, FFT **512**. Stack **5 adjacent frames** with stride **3** → **400-d** input; receptive field **60 ms**, stride **30 ms**. Time conv after level 2: kernel **5**, stride **3** (reduces time steps to 1/3). Overall receptive field/stride becomes **780 ms / 90 ms**; **forward lookahead 390 ms** in streaming.
- **Training loss with label smoothing (Eq. in Sec. 3.1):**  
  \(L(x,y)=\sum_k\left[\text{CTC}(x,y^k)-\lambda\sum_t \text{Entropy}(P_k(\cdot|x_t))\right]\)  
  \(=\sum_k\left[-\log P(y^k|x)+\lambda\sum_{t,v}P_k(v|x)\log P_k(v|x)\right]\).  
  Variables: level \(k\in\{\text{char},s300,s5k\}\); \(P_k\) token distribution at time \(t\); \(\lambda\) weight.
- **EOS integration (Sec. 3.2):** Add token **</s>**; forced alignment uses **character-level output** (least lookahead). Fine-tune with **early-late (EL) penalties** (Li et al., 2020) to penalize predicting </s> too early/late.  
  Online EOS at time \(t\) if: (1) ≥1 word emitted; (2) **EOS peak:** \(P_t(</s>) \ge P_t(\text{any token})\); (3) \(P_t(</s>) \ge \text{threshold}_t=\alpha_1 + n_t/\beta\), where \(n_t\)=#EOS peaks before \(t\); \(\alpha\) controls aggressiveness; \(n_t/\beta\) lowers threshold after repeated peaks. Backup: small VAD + max time.
- **Decoding/rescoring (Sec. 3.3):** Per audio chunk, **prefix beam search**, **beam=1000**, decode from **subword-5000** level; EOS also from same distribution. On EOS/end: rerank **top 100** using **5-gram KenLM + HCTC loss (sum of CTC losses across levels)**; weights via grid search.
- **Data/training ops (Sec. 4):** ~**14M** audio-text pairs (~**22.5k hours**; **8M** target domain + **6M** other). Train **200k iters**, batch ≈ **55 minutes**, Adam + **cyclical LR**; **2×A100 40GB**, ~**50 hours**. EOS fine-tune: **48k iters** (~**12 hours**). Eval: ~**19k** manually transcribed (clean ~16k, noisy ~3k).
- **Key results (Table 1):**
  - Best model (no EOS): **WER 3.69%** (clean **2.95**, noisy **8.12**); mean latency reported **2858 ms** (clean **2457**, noisy **5080**).
  - With EOS detection + \(n/\beta\): **WER 4.78%** (clean **4.19**, noisy **8.32**); mean EOS latency **1525 ms** (clean **1242**, noisy **3096**).  
  - Latency reduction vs independent VAD: **1333 ms** overall (**46.64%**), clean **1215**, noisy **1985**. EOS coverage at \(\alpha=0.8,\beta=2.0\): **64.13%**.
- **Ablation (Table 2, ~5500h):** Baseline LSTM CTC **WER 7.68**. Full LSTM-attn HCTC **5.37**. Removing components worsens WER: remove skip connections → **7.68**; remove HCTC loss → **6.62**; remove HCTC rescoring → **6.19**; remove windowed MHA → **5.94**. Windowed MHA credited with **+9.6% relative** improvement; HCTC loss+rescoring **~10.28% relative**; skip connections **13.8% relative**.
- **Model comparisons (Table 4, ~5500h):** Streaming Conformer CTC **5.30** vs their streaming LSTM-attn HCTC **5.37** (similar WER; Conformer higher complexity/latency). Non-streaming BiLSTM-attn HCTC **4.65**; Transformer AED+CTC **4.37**.

</details>

### 📄 SCDiar streaming diarization via token-level SCD + representative segments
**Paper** · [source](https://arxiv.org/pdf/2501.16641.pdf)

*Streaming diarization pipeline (token-level speaker change detection, caching, label mapping) + benchmark results*

<details>
<summary>Key content</summary>

- **System blocks (Sec. II, Fig.1):** VAD → CIF-based ASR → **token-level SCD** (split transcript into homogeneous token segments) → SD network builds **segment–token similarity matrix** → **representative segment selection (optimization)** → **speaker label mapping + cache update** for streaming.
- **Token-level SCD (Sec. II-B, Eq.5–7):** Extract frame-level speaker features \(H\); align to token-level features \(Z\) via MHA using ASR token embeddings as queries; refine with BiLSTM + 1D-CNN (kernel=3); softmax gives per-token change probs; peak detection (`scipy.signal.find_peaks`) with threshold \(\tau\) (inference \(\tau=0.25\)) yields change tokens → segment timestamps (using CIF token timestamps, Eq.4). Training: freeze ASR; TPSP maps reference speaker labels onto hypothesis tokens; **focal loss** (\(\alpha=0.25,\gamma=2\)).
- **Length-aware similarity (Sec. II-C, Eq.12):** Instead of square cosine matrix, compute **rectangular** \(A\) where \(A_{t,s}\) = similarity between token \(t\) and segment \(s\) via refined token speaker embeddings; preserves **segment length/token count** for downstream selection. Training uses weighted BCE vs target matrix, weighted by token count (Eq.13).
- **Representative segment selection (Sec. II-D, Eq.14–15):** Choose binary vector \(x\) over segments (number of 1s = predicted #speakers) to minimize token overlap/miss; relax to bounded non-negative least squares (solved efficiently); threshold \(\sigma=0.3\) selects representative segments.
- **Streaming cache + label mapping (Sec. II-E):** Maintain cache centers \(C\). Steps: (1) cosine distance between new reps \(R\) and \(C\); discard too-similar reps (threshold 0.55). (2) append remaining reps as new speakers. (3) map speaker IDs to segments by cosine distance. (4) update cache center with matched embeddings weighted by token counts. Exclude segments with <10 tokens from rep selection/cache update.
- **Training strategy (Sec. II-F):** Multi-target loss \(L=L_{SD}+ \lambda L_{SCD}\) with \(\lambda=10\). **Split augmentation:** randomly split long segments into two during training to simulate SCD variability.
- **Empirical results (Sec. III-C, Table I; metrics cpWER/WDER):**
  - **AISHELL-4 (4–8 spk):** SCDiar **3.42 / 3.56** vs Core sample+VBx **10.09 / 7.84**; offline SlidingWindow+SpC **2.13 / 2.69** (SCDiar gap: +1.29 cpWER, +0.87 WDER).
  - **In-house (≥10 spk):** SCDiar **10.66 / 15.36** vs Core sample+VBx **21.65 / 19.23**; offline SlidingWindow+SpC **9.95 / 13.51**.
  - **Ablations:** w/o rep selection → AISHELL-4 **11.96 / 8.76**; In-house **13.63 / 16.29**. w/o split strategy → In-house cpWER **14.38** (worse than 10.66).
- **Latency/compute (Sec. III-B/III-C):** Max latency set by VAD max active segment length (default 15s). RTF on Xeon 6148 + V100: ASR **0.072**, SCD **0.004**, SD **0.009**. Performance degrades when streaming chunk <3s; stabilizes after ~10s.

</details>

### 📄 SoundStream RVQ + adversarial/perceptual training objective
**Paper** · [source](https://arxiv.org/pdf/2107.03312.pdf)

*Explicit RVQ formulation + end-to-end training objective (reconstruction + adversarial/feature losses), plus bitrate/latency tradeoffs*

<details>
<summary>Key content</summary>

- **Model pipeline (Section III):** waveform \(x\in\mathbb{R}^T\) → encoder \(y=\mathrm{enc}(x)\in\mathbb{R}^{S\times D}\) with \(S=T/M\) → residual vector quantizer \(Q(\cdot)\) → decoder \(\hat{x}=\mathrm{dec}(Q(y))\). Generator \(G(x)=\mathrm{dec}(Q(\mathrm{enc}(x)))\).
- **Architectural latency via strides (Sec. III-A):** causal convs; resampling ratio \(M=\prod \text{strides}\). Example strides \((2,4,5,8)\Rightarrow M=320\) samples → embeddings at \(24\text{kHz}/320=75\) Hz → **13.3 ms** per frame.
- **Residual Vector Quantization (Algorithm 1, Sec. III-C):**  
  Initialize \(\hat{y}=0\), \(r=y\). For \(i=1..N_q\): \(\hat{y}\mathrel{+}=Q_i(r)\); \(r\mathrel{-}=Q_i(r)\). Output \(\hat{y}\).  
  Per-frame bits \(r = N_q\log_2 N\). Example: target \(R=6000\) bps, \(S=75\) fps ⇒ \(r=80\) bits/frame; plain VQ needs \(N=2^{80}\) (infeasible). With \(N_q=8\): \(N=2^{80/8}=1024\).
- **Bitrate scalability via quantizer dropout (Sec. III-C):** sample \(n_q\sim\mathrm{Unif}\{1,\dots,N_q\}\) per example; use only \(Q_1..Q_{n_q}\). Inference chooses \(n_q\) for desired bitrate; embedding dimensionality unchanged (additive refinement).
- **Training objective (Sec. III-E):** multi-discriminator hinge GAN + feature + multi-scale mel losses.  
  Discriminator loss **Eq. (1)**:  
  \[
  L_D=\mathbb{E}_x\Big[\frac1K\sum_k\frac1{T_k}\sum_t \max(0,1-D_{k,t}(x))\Big]+\mathbb{E}_x\Big[\frac1K\sum_k\frac1{T_k}\sum_t \max(0,1+D_{k,t}(G(x)))\Big]
  \]
  Generator adversarial **Eq. (2)**: \(L_G^{adv}=\mathbb{E}_x[\frac1K\sum_{k,t}\frac1{T_k}\max(0,1-D_{k,t}(G(x)))]\).  
  Feature loss **Eq. (3)**: average \(\ell_1\) diff of discriminator internal activations \(D_k^{(l)}\).  
  Multi-scale spectral recon **Eq. (4–5):** 64-bin mel-spectrograms with window \(s\in\{2^6,\dots,2^{11}\}\), hop \(s/4\): \(\|S^s(x)-S^s(G(x))\|_1 + \alpha_s\|\log S^s(x)-\log S^s(G(x))\|_2\), \(\alpha_s=\sqrt{s/2}\).  
  Total **Eq. (6):** \(L_G=\lambda_{adv}L_G^{adv}+\lambda_{feat}L_G^{feat}+\lambda_{rec}L_G^{rec}\) with **\(\lambda_{adv}=1,\lambda_{feat}=100,\lambda_{rec}=1\)**.
- **Key empirical comparisons (Abstract + Sec. V-A):** subjective @24 kHz: **SoundStream 3 kbps > Opus 12 kbps**, approaches **EVS 9.6 kbps**; to match SoundStream@3 kbps, EVS needs ≥9.6 kbps and Opus ≥12 kbps (≈3.2–4× bits).
- **Latency/RTF tradeoff (Table III, 6 kbps):** strides \((1,4,5,8)\) latency **7.5 ms**, \(N_q=4\), RTF(enc) **1.6×**, RTF(dec) **1.5×**, ViSQOL **4.01**; \((2,4,5,8)\) latency **13 ms**, \(N_q=8\), RTF(enc) **2.4×**, RTF(dec) **2.3×**, ViSQOL **4.01**; \((4,4,5,8)\) latency **26 ms**, \(N_q=16\), RTF(enc) **4.1×**, RTF(dec) **4.0×**, ViSQOL **4.01**.
- **RVQ depth vs codebook size (Table II, 6 kbps):** \(N_q=8,N=1024\Rightarrow\) ViSQOL **4.01**; \(N_q=16,N=32\Rightarrow 3.98\); \(N_q=80,N=2\Rightarrow 3.92\).

</details>

### 📄 VALL-E end-to-end codec-LM zero-shot TTS
**Paper** · [source](https://arxiv.org/abs/2301.02111)

*End-to-end VALL-E pipeline: acoustic prompt conditioning, discrete neural codec tokens, AR generation of codec code sequences*

<details>
<summary>Key content</summary>

- **Core idea (Abstract, Sec. 4.1):** Treat TTS as **conditional language modeling over discrete neural codec tokens** (not continuous mel regression). Train a neural codec language model (VALL-E) on **discrete codes** from an off-the-shelf codec (EnCodec).
- **Codec/tokenization (Sec. 4; EnCodec config):**
  - Audio: **24 kHz**.
  - Encoder produces embeddings at **75 Hz** ⇒ **320×** reduction vs 24 kHz.
  - Residual Vector Quantization (RVQ): **8 quantizers**, each with **1024 entries** (≈ EnCodec **6 kbps** setting).
  - Output codes form matrix \(C \in \mathbb{N}^{T \times 8}\); waveform reconstructed by codec decoder: \(\hat{y}=\mathrm{Decodec}(C)\).
- **Problem formulation (Sec. 4.1):**
  - Dataset \(D=\{(x_i,y_i)\}\), where \(x=\{x_0,\dots,x_L\}\) is **phoneme sequence**, \(y\) is audio.
  - Encode audio to codes: \(C=\mathrm{Codec}(y)\).
  - **Zero-shot objective:** maximize \(p(C\mid x,\tilde{C})\), where \(\tilde{C}\) is an **acoustic prompt** (e.g., **3 s** enrolled recording) encoded by same codec.
- **Modeling procedure (Sec. 4.2–4.3):**
  - **AR Transformer** predicts **first codebook stream** \(c_{:,1}\) causally (token \(c_{t,1}\) attends to \((x,c_{\le t,1})\)).
  - **NAR Transformer** predicts remaining streams \(c_{:,j}, j=2..8\) conditioned on phonemes + acoustic prompt + previously generated streams; training samples stage \(i\in[2,8]\) and predicts \(c_{:,i}\).
- **Training data & pipeline (Intro, Sec. 5):**
  - Pre-train on **LibriLight 60K hours**, **>7000 speakers**; transcripts generated via ASR; phoneme alignments via **Kaldi** (30 ms frameshift).
  - Train on **16× V100 32GB**, **6k acoustic tokens/GPU**, **800k steps**, AdamW; LR warmup **32k** to **5e-4**, then linear decay.
- **Empirical results (Table snippet in text):**
  - Zero-shot baseline **YourTTS:** WER **7.7**, speaker similarity (SMOS) **0.337**.
  - **VALL-E:** WER **5.9**, SMOS **0.580**.
  - **VALL-E-continual:** WER **3.8**, SMOS **0.508**.
- **Design rationale (Intro, Sec. 3–4):**
  - Codec tokens retain **speaker identity + acoustic environment**; codec decoder avoids training a separate vocoder; discrete tokens enable **sampling-based diversity** and **prompting/in-context learning** for unseen speakers; RVQ hierarchy: early quantizers capture coarse properties (speaker), later quantizers refine details.

</details>

### 📊 Whisper benchmarks + decoding/eval defaults
**Benchmark** · [source](https://cdn.openai.com/papers/whisper.pdf)

*Benchmark WER/BLEU tables across datasets + model sizes; decoding/evaluation setup (normalization, long-form heuristics)*

<details>
<summary>Key content</summary>

- **Training data & tasks (Sec. 2.1–2.3):** 680,000 hours weakly supervised audio-text; includes **117k hours / 96 non-English languages** and **125k hours X→en translation**. Audio split into **30s segments**. Multitask decoder prompt tokens: `<|startoftranscript|>`, **language token (99 total)**, `<|nospeech|>` (VAD), task token `<|transcribe|>`/`<|translate|>`, `<|notimestamps|>`; timestamps quantized to **20 ms** and interleaved (start token before caption text, end token after).
- **Audio/features (Sec. 2.2):** resample **16 kHz**; **80-channel log-Mel**, **25 ms window**, **10 ms stride**; global scaling to **[-1, 1]** ~zero mean.
- **Model family (Table 1):** Transformer encoder-decoder. Params: **Tiny 39M**, **Base 74M**, **Small 244M (12L, 768w, 12h)**, **Medium 769M (24L, 1024w, 16h)**, **Large 1550M (32L, 1280w, 20h)**. Large **V2** trained longer (+SpecAugment, Stochastic Depth, BPE dropout).
- **Optimization defaults (Sec. 2.4):** AdamW, FP16, grad-norm clipping; **batch 256 segments**; LR warmup **2048 updates**, linear decay to 0; train **2^20 updates** (~2–3 epochs).
- **WER evaluation (Sec. 3.2):** extensive **text normalization** before WER; can reduce WER up to **50%** on some datasets.
- **Key English robustness result (Table 2):** vs wav2vec2 Large (no LM), Whisper Large V2 matches LibriSpeech Clean **2.7 WER** but is far better OOD: e.g., **CHiME6 25.5 vs 65.8**, **Common Voice 9.0 vs 29.9**, **TED-LIUM 4.0 vs 10.5**; **Average WER 12.8 vs 29.3** (**55.2% relative error reduction**).
- **Multilingual/translation benchmarks:** MLS/VoxPopuli (Table 3): Whisper zero-shot **7.3 WER (MLS)**, **13.6 (VoxPopuli)**. CoVoST2 X→en (Table 4): Whisper **29.1 BLEU** (High/Mid/Low: **36.2/32.6/25.2**).
- **Noise robustness (Sec. 3.7):** under **pub noise**, Whisper outperforms all compared models when **SNR < 10 dB**.
- **Long-form decoding heuristics (Sec. 4.5, Table 7):** **beam=5**; temperature fallback **0→1.0 step 0.2** if avg logprob < **−1** or gzip compression rate > **2.4**; previous-text conditioning when temp < **0.5**; VAD: `<|nospeech|>` prob > **0.6** plus avg logprob < **−1**; constrain initial timestamp to **0.0–1.0 s**. Average WER improves **11.0 → 10.0** across long-form sets with full heuristics.

</details>

### 📖 Azure Speech TTS SSML surface (voice, prosody, style, audio)
**Reference Doc** · [source](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/speech-synthesis-markup-voice)

*Exact SSML elements/attributes for Azure Speech TTS: required `<voice>` in `<speak>`, multi-voice docs, prosody/emphasis/style/role/lang/audio/backgroundaudio/audioduration/viseme/voiceconversion.*

<details>
<summary>Key content</summary>

- **Document rule:** Inside each `<speak ...>` root, **at least one** `<voice>` element is required; you can include **multiple** `<voice>` blocks (different voices/languages/settings).
- **`<voice>` attributes:**  
  - `name` = voice name (or **custom voice model name**).  
  - `effect` (optional): `eq_car` (car/bus enclosed auto playback compensation), `eq_telecomhp8k` (telecom narrowband; **use 8 kHz** sampling rate). Missing/invalid → ignored.
- **Multi-talker:** Use `<voice name='en-US-MultiTalker-Ava-Andrew:DragonHDLatestNeural'><mstts:dialog><mstts:turn speaker="ava|andrew">...</mstts:turn>...</mstts:dialog></voice>`.
- **Styles/roles:** `<mstts:express-as style="..." styledegree="..." role="...">`  
  - `style` required; invalid/missing → whole element ignored (neutral).  
  - `styledegree` optional **0.01–2** (default **1**).  
  - `role` optional: `Girl|Boy|YoungAdultFemale|YoungAdultMale|OlderAdultFemale|OlderAdultMale|SeniorFemale|SeniorMale`.
- **Language override (multilingual voices only):** `<lang xml:lang="locale">...</lang>`; `xml:lang` required. Non-multilingual voices don’t support `<lang>`. `<speak>` default language must be `xml:lang="en-US"` in examples.
- **Prosody:** `<prosody pitch|contour|range|rate|volume>`  
  - **Rate:** multiplier **0.5–2** or `%` or constants `x-slow/slow/medium/fast/x-fast`.  
  - **Pitch:** absolute `Hz`, relative `+/-Hz` or `+/-st`, `%`, or constants `x-low/low/medium/high/x-high` (~0.55…1.45).  
  - **Volume:** absolute **0.0–100.0** (default **100.0**), relative `+/-`, `%`, or constants `silent…x-loud`.
- **Emphasis:** `<emphasis level="reduced|none|moderate|strong">` (default **moderate**); word-level emphasis only for **en-US-GuyNeural, en-US-DavisNeural, en-US-JaneNeural**.
- **Insert audio:** `<audio src="https://...">fallback text/SSML</audio>`; formats: **mp3/wav/opus/ogg/flac/wma**; total response (text+audio) **≤600s**; HTTPS required.
- **Audio duration control:** `<mstts:audioduration value="20s|2000ms"/>` applies to enclosing `<voice>`; allowed scaling **0.5–2×** original; **max 300s** output.
- **Background audio:** `<mstts:backgroundaudio .../>` must be **first child of `<speak>`**; only **one** per SSML. `volume 0–100` (default **1**), `fadein/fadeout 0–10000 ms` (default **0**).
- **Visemes:** `<mstts:viseme type="redlips_front|FacialExpression"/>` (locale limits: redlips_front en-US; FacialExpression en-US & zh-CN).
- **Voice conversion (preview):** `<mstts:voiceconversion url="https://..."/>` input audio **<100 MB**; **ignores** SSML prosody/pronunciation and any text; target voice set by `<voice name="...">`.

</details>

---

## Related Topics

- [[topics/multimodal-fundamentals|Multimodal Fundamentals]]
- [[topics/tokenization|Tokenization]]
- [[topics/text-to-video|Text-to-Video]]
- [[topics/contrastive-learning|Contrastive Learning]]
