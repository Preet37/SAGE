## Core Definitions

**Whisper (speech-to-text Transformer)**  
Whisper is a general-purpose speech recognition system implemented as a Transformer encoder–decoder trained on multiple speech tasks (multilingual ASR, speech translation, language ID, and voice activity detection) using a unified token-prediction format with special prompt tokens that specify language and task. It operates on 30-second audio segments represented as log-Mel spectrogram features, and can optionally predict timestamp tokens interleaved with text. (OpenAI Whisper paper: https://cdn.openai.com/papers/whisper.pdf; repo overview: https://github.com/openai/whisper)

**Speech tokenization (neural codec tokens)**  
Speech tokenization is the conversion of a waveform into a sequence (often multi-stream) of *discrete* symbols produced by a neural audio codec. These discrete codes can be modeled like “tokens” by language-model-style architectures, enabling generation and conditioning in token space rather than regressing continuous spectrograms. (EnCodec: https://arxiv.org/abs/2210.13438; VALL‑E: https://arxiv.org/abs/2301.02111)

**EnCodec (neural audio codec / tokenizer)**  
EnCodec is an end-to-end neural audio compression system that encodes audio into a low-rate latent sequence and then applies residual vector quantization (RVQ) to produce discrete code indices; a decoder reconstructs the waveform from the quantized latents. It is designed to be streamable (low algorithmic latency) and supports variable bitrates by varying the number of RVQ codebooks used. (EnCodec paper: https://arxiv.org/abs/2210.13438; code: https://github.com/facebookresearch/encodec)

**Residual Vector Quantization (RVQ / residual quantization)**  
Residual vector quantization is a multi-stage quantization method that approximates a vector by iteratively quantizing the residual error: each stage selects a codebook entry to add to the reconstruction, then updates the residual. The final representation is a tuple of codebook indices; bits scale roughly with (number of stages) × log2(codebook size). (SoundStream RVQ formulation: https://arxiv.org/pdf/2107.03312.pdf; EnCodec RVQ details: https://arxiv.org/pdf/2210.13438.pdf; formal RQ recursion: https://arxiv.org/pdf/2401.14732.pdf)

**Text-to-speech (TTS) as codec language modeling (VALL‑E)**  
VALL‑E formulates TTS as *conditional language modeling over discrete neural codec tokens* (rather than predicting continuous mel spectrograms). Given text (phonemes) and an acoustic prompt (a short enrolled recording encoded into codec tokens), it generates the target codec token sequence autoregressively (and/or with auxiliary non-autoregressive stages) and then decodes tokens back to waveform using the codec decoder. (VALL‑E: https://arxiv.org/abs/2301.02111; VALL‑E 2: http://arxiv.org/pdf/2406.05370.pdf)

**Speech-to-speech (S2S) via token space (conceptual)**  
Speech-to-speech systems can be built by (1) tokenizing input speech into discrete codec tokens, (2) transforming/conditioning/generating new codec tokens (potentially with a language-model objective), and (3) decoding tokens back to waveform with the codec decoder—avoiding direct waveform regression. This “token-in/token-out” pattern is exemplified by codec-LM TTS pipelines (VALL‑E) and relies on neural codecs like EnCodec. (VALL‑E: https://arxiv.org/abs/2301.02111; EnCodec: https://arxiv.org/abs/2210.13438)

---

## Key Formulas & Empirical Results

### Whisper: feature defaults, prompting tokens, and decoding heuristics
- **Input features** (Whisper paper, Sec. 2.2): audio resampled to **16 kHz**; **80-channel log-Mel**, **25 ms window**, **10 ms stride**; global scaling to ~**[-1, 1]**. (https://cdn.openai.com/papers/whisper.pdf)
- **Segmentation**: trained on **30 s segments**. (https://cdn.openai.com/papers/whisper.pdf)
- **Prompt tokens** (multitask format): `<|startoftranscript|>`, language token (99 total), `<|nospeech|>`, task token `<|transcribe|>`/`<|translate|>`, `<|notimestamps|>`; timestamps quantized to **20 ms** and interleaved. (https://cdn.openai.com/papers/whisper.pdf)
- **Long-form decoding defaults** (Sec. 4.5): **beam=5**; temperature fallback **0→1.0 step 0.2** if avg logprob < **−1** or gzip compression rate > **2.4**; previous-text conditioning when temp < **0.5**; VAD: `<|nospeech|>` prob > **0.6** plus avg logprob < **−1**; constrain initial timestamp to **0.0–1.0 s**. (https://cdn.openai.com/papers/whisper.pdf)
- **Empirical robustness snapshot** (Table 2): Whisper Large V2 vs wav2vec2 Large (no LM): LibriSpeech Clean **2.7 WER** (similar), but much better OOD (e.g., CHiME6 **25.5 vs 65.8**; Common Voice **9.0 vs 29.9**); average WER **12.8 vs 29.3** (55.2% relative reduction). (https://cdn.openai.com/papers/whisper.pdf)

### SoundStream / EnCodec: RVQ bitrate math and recursion
- **Stride-to-frame-rate example** (SoundStream, Sec. III-A): strides (2,4,5,8) ⇒ downsampling factor \(M=320\) samples; at 24 kHz ⇒ **75 Hz** latent steps (≈ **13.3 ms** per frame). (https://arxiv.org/pdf/2107.03312.pdf)
- **RVQ recursion (algorithmic form)** (SoundStream, Alg. 1): initialize \(\hat{y}=0\), \(r=y\). For \(i=1..N_q\): \(\hat{y} \mathrel{+}= Q_i(r)\); \(r \mathrel{-}= Q_i(r)\). (https://arxiv.org/pdf/2107.03312.pdf)
- **Bits per frame** (SoundStream, Sec. III-C): \(r = N_q \log_2 N\) where \(N\) is codebook size per quantizer. Example: 6 kbps at 75 fps ⇒ 80 bits/frame; with \(N_q=8\) ⇒ \(N=2^{80/8}=1024\). (https://arxiv.org/pdf/2107.03312.pdf)
- **EnCodec commitment loss** (Eq. 3): \(\ell_w = \sum_{c=1}^{C} \|z_c - q_c(z_c)\|_2^2\) (grad only w.r.t. \(z_c\)). (https://arxiv.org/pdf/2210.13438.pdf)
- **EnCodec generator loss** (Eq. 4): \(L_G=\lambda_t\ell_t+\lambda_f\ell_f+\lambda_g\ell_g+\lambda_{feat}\ell_{feat}+\lambda_w\ell_w\). (https://arxiv.org/pdf/2210.13438.pdf)
- **Entropy coding bandwidth reduction** (EnCodec): 3.0→**1.9 kbps**, 6.0→**4.1 kbps**, 12.0→**8.9 kbps**. (https://arxiv.org/pdf/2210.13438.pdf)

### VALL‑E: codec token shapes and modeling choices
- **Tokenization config** (VALL‑E, Sec. 4; EnCodec @ 6 kbps): audio **24 kHz**; encoder embeddings at **75 Hz**; RVQ with **8 quantizers**, each **1024 entries**; codes \(C \in \mathbb{N}^{T \times 8}\). (https://arxiv.org/abs/2301.02111)
- **Zero-shot objective**: maximize \(p(C \mid x, \tilde{C})\) where \(x\) is phoneme sequence and \(\tilde{C}\) is an acoustic prompt encoded by the same codec (e.g., **3 s**). (https://arxiv.org/abs/2301.02111)
- **Decoding structure**: AR Transformer generates first code stream; NAR Transformer predicts remaining streams 2–8 conditioned on text/prompt and previously generated streams. (https://arxiv.org/abs/2301.02111)

### VALL‑E 2: grouped codec LM + repetition-aware sampling
- **Grouped codec LM NLL** (Eq. 1–2): minimize \(-\log p(\tilde{c}\mid x)= -\sum_i \log p(\tilde{c}_i \mid \tilde{c}_{<i}, x)\), where grouping reduces sequence length by factor \(g\). (http://arxiv.org/pdf/2406.05370.pdf)
- **Repetition-aware sampling** (Alg. 1): nucleus sampling (top‑\(p\)); if repetition ratio in window \(w\) exceeds \(\tau\), replace with random sampling. Eval hyperparams: **\(w=50\)**, **\(\tau=0.1\)**; top‑\(p\) searched **0.0–1.0** in 0.1 steps. (http://arxiv.org/pdf/2406.05370.pdf)
- **LibriSpeech test-clean snapshot** (Table 1, 3s prefix prompt): VALL‑E WER **2.3**; VALL‑E 2 (g=2) WER **1.5**; SIM and DNSMOS also reported. (http://arxiv.org/pdf/2406.05370.pdf)

---

## How It Works

### A. Whisper (speech → text) mechanics
1. **Resample & featurize**: audio → 16 kHz → 80-channel log-Mel spectrogram (25 ms window, 10 ms hop). (Whisper paper)
2. **Chunking**: process in **30 s** segments. (Whisper paper)
3. **Encoder**: Transformer encoder consumes the spectrogram frames and produces hidden states.
4. **Decoder prompt**: prepend special tokens specifying:
   - start-of-transcript,
   - language token,
   - task token (transcribe/translate),
   - optional timestamp mode (`<|notimestamps|>`), etc. (Whisper paper)
5. **Autoregressive decoding**: decoder predicts next token (text tokens and possibly timestamp tokens).
6. **Long-form stitching (heuristics)**: beam search + temperature fallback; `<|nospeech|>`-based VAD; timestamp constraints; optional conditioning on previous text depending on temperature. (Whisper paper)

### B. EnCodec (waveform → discrete tokens → waveform) mechanics
1. **Encoder** \(E\): waveform \(x\) → latent sequence \(z\) at a reduced frame rate (e.g., 24 kHz → 75 steps/s). (EnCodec paper)
2. **RVQ quantization** \(Q\):
   - For each time step, apply multiple quantizers sequentially to the residual (RVQ).
   - Output is a stack of discrete indices: one index per codebook per time step. (EnCodec paper; SoundStream algorithm)
3. **(Optional) entropy coding**: a lightweight causal Transformer predicts code distributions to reduce bitrate up to ~40% (EnCodec paper).
4. **Decoder** \(G\): quantized latents → reconstructed waveform \(\hat{x}\). (EnCodec paper)
5. **Variable bitrate**: choose how many RVQ codebooks \(N_q\) to use at inference; EnCodec trains with variable \(N_q\) so one model supports multiple bandwidths. (EnCodec paper)

### C. VALL‑E (text + prompt speech → speech) mechanics
1. **Text to phonemes**: training uses phoneme sequences \(x\) (with alignments via Kaldi in the paper’s pipeline). (VALL‑E)
2. **Prompt tokenization**: take a short enrolled recording (e.g., 3 s), encode with EnCodec → prompt codes \(\tilde{C}\). (VALL‑E)
3. **Target tokenization**: encode target speech waveform \(y\) with EnCodec → target code matrix \(C \in \mathbb{N}^{T\times 8}\). (VALL‑E)
4. **Codec-LM training objective**: learn \(p(C \mid x, \tilde{C})\). (VALL‑E)
5. **Generation**:
   - **AR** model generates the first code stream over time.
   - **NAR** model fills in remaining streams 2–8 conditioned on text + prompt + generated streams. (VALL‑E)
6. **Decode to waveform**: EnCodec decoder reconstructs waveform from generated codes. (VALL‑E)

---

## Teaching Approaches

### Intuitive (no math): “specialized ears vs shared alphabet”
- Whisper: a model with a **speech-specific front end** (log-Mel + encoder) that turns audio into a representation the decoder can “read” to output text.
- Codec-token models: instead of a speech-specific continuous representation, you convert audio into a **discrete alphabet** (codec tokens). Then a language model can generate “audio sentences” in that alphabet, and a codec decoder turns them back into sound.

### Technical (with math): “conditional LM over discrete audio codes”
- Whisper is seq2seq over text tokens conditioned on acoustic encoder states.
- VALL‑E explicitly models \(p(C \mid x, \tilde{C})\) where \(C\) is a matrix of RVQ code indices (8 streams per frame at 6 kbps EnCodec setting). (VALL‑E)
- RVQ explains why codebooks can be small (e.g., 1024 entries) while total bits/frame are large: bits/frame \(=N_q\log_2 N\). (SoundStream)

### Analogy-based: “MP3-like compression + autocomplete”
- EnCodec is like a learned, low-bitrate “MP3” that outputs **symbols** instead of bytes.
- VALL‑E is like **autocomplete** over those symbols, conditioned on text and a short “voice sample” prompt.
- Whisper is like a **captioning model** for audio: it listens and writes.

---

## Common Misconceptions

1. **“Whisper tokenizes raw audio into tokens like an LLM tokenizer.”**  
   *Why wrong:* Whisper’s input is **continuous log-Mel features**, not discrete codec tokens; its “tokens” are output-side text/timestamp tokens. (Whisper paper)  
   *Correct model:* Whisper = speech feature encoder + text-token decoder; codec tokenization (EnCodec) is a separate approach.

2. **“RVQ is just one big codebook lookup repeated; codebooks don’t interact.”**  
   *Why wrong:* RVQ quantizes the **residual** after previous steps; later codebooks depend on earlier reconstruction. (SoundStream Alg. 1; RQ recursion in QINCo paper)  
   *Correct model:* reconstruction is additive across stages; each stage refines what earlier stages missed.

3. **“VALL‑E directly predicts waveforms or mel spectrograms.”**  
   *Why wrong:* VALL‑E predicts **discrete codec code indices** and uses the codec decoder to synthesize waveform. (VALL‑E)  
   *Correct model:* TTS as conditional LM over codec tokens.

4. **“More codebooks always means a different model architecture.”**  
   *Why wrong:* EnCodec trains with **variable number of residual steps** so the same model can run at multiple bitrates by selecting how many codebooks to use. (EnCodec paper)  
   *Correct model:* bitrate is a runtime knob (within the trained bandwidth set).

5. **“If a codec LM repeats, it’s because the model is ‘stuck’ and there’s no fix besides retraining.”**  
   *Why wrong:* VALL‑E 2 introduces **repetition-aware sampling** that detects repetition in a window and forces alternative sampling. (VALL‑E 2)  
   *Correct model:* decoding strategy can materially affect looping/repetition without changing weights.

---

## Worked Examples

### 1) Compute codec token rate and bitrate (EnCodec/VALL‑E settings)
**Goal:** help student connect 24 kHz audio, 75 Hz frames, 8 RVQ streams, 1024 entries to bits/sec.

Given (from VALL‑E / EnCodec @ 6 kbps setting):  
- sample rate = 24,000 samples/s  
- latent frame rate = 75 frames/s (i.e., downsample factor 320) (SoundStream; VALL‑E mentions 75 Hz)  
- RVQ streams \(N_q = 8\)  
- codebook size \(N = 1024\) ⇒ \(\log_2 1024 = 10\) bits per stream per frame

Then:
- **bits per frame** \(= N_q \log_2 N = 8 \times 10 = 80\) bits/frame (SoundStream)
- **bits per second** \(= 80 \times 75 = 6000\) bps = **6 kbps**

This is exactly the “6 kbps” configuration described in VALL‑E/VALL‑E 2 using EnCodec. (VALL‑E; VALL‑E 2)

### 2) RVQ pseudocode (quantize residuals)
Use this when a student asks “what does residual quantization actually do?”

```python
# Based on SoundStream Alg. 1 (RVQ)
y_hat = 0
r = y
for i in range(Nq):
    q = Qi(r)      # nearest codebook vector in codebook i
    y_hat = y_hat + q
    r = r - q
return y_hat, indices
```

Key point to probe: later quantizers see the *residual* \(r\), not the original \(y\). (https://arxiv.org/pdf/2107.03312.pdf)

---

## Comparisons & Trade-offs

| Approach | Representation | Typical objective | Strengths | Weaknesses / gotchas | Sources |
|---|---|---|---|---|---|
| Whisper-style ASR | Continuous log-Mel features in encoder; text/timestamp tokens out | Seq2seq decoding with prompt tokens | Strong robustness OOD/noise; unified ASR/translate/LID/VAD via tokens | Not a unified “audio token” interface for generation; input not discrete | https://cdn.openai.com/papers/whisper.pdf |
| Codec tokenization (EnCodec) | Discrete RVQ code indices (multi-stream) | Codec reconstruction + adversarial/perceptual losses; optional entropy model | Enables treating audio as tokens; streamable; variable bitrate | Token sequences can be long; quality depends on bitrate/codecs | https://arxiv.org/abs/2210.13438 |
| Codec-LM TTS (VALL‑E) | LM over codec tokens conditioned on text + prompt codes | Maximize \(p(C\mid x,\tilde{C})\) | Zero-shot voice prompting; avoids mel regression/vocoder training | Multi-stream generation complexity; repetition/looping issues | https://arxiv.org/abs/2301.02111 |
| Grouped codec LM + repetition-aware sampling (VALL‑E 2) | Grouped codec tokens (shorter sequence) | NLL over grouped tokens; repetition-aware sampling | Faster inference; mitigates long-context errors; reduces looping | Adds grouping design choice + sampling hyperparams | http://arxiv.org/pdf/2406.05370.pdf |

When to choose:
- Choose **Whisper** when the task is **speech → text** with robustness and timestamps.  
- Choose **EnCodec-style tokenization** when you need a **discrete audio interface** for generation/editing/LM-style modeling.  
- Choose **VALL‑E-style codec LM** when you need **prompted/zero-shot TTS** and can operate in codec-token space.

---

## Prerequisite Connections

- **Transformer encoder–decoder basics**: needed to understand Whisper’s architecture and why prompt tokens steer tasks. (Whisper paper; general Transformer background in listed resources)
- **Tokenization concept (text)**: helps transfer intuition to *speech tokenization* (discrete symbols + embeddings), even though the algorithms differ. (Tokenizer resources listed)
- **Quantization / codebooks**: needed to understand RVQ and bitrate math (bits/frame). (SoundStream; EnCodec)
- **Autoregressive vs non-autoregressive decoding**: needed to understand VALL‑E’s AR first-stream + NAR remaining streams design. (VALL‑E; VALL‑E 2)

---

## Socratic Question Bank

1. **If Whisper doesn’t use codec tokens, what exactly is “tokenized” in Whisper—and where?**  
   *Good answer:* audio → continuous log-Mel features; decoder outputs discrete text/timestamp tokens; special prompt tokens specify task/language.

2. **Why does RVQ let you use small codebooks (e.g., 1024 entries) instead of one astronomically large codebook?**  
   *Good answer:* bits/frame add across stages; residual refinement means each stage only needs to cover remaining error; formula \(N_q\log_2 N\).

3. **Given 75 frames/s and 8 streams with 1024 entries, can you derive the kbps?**  
   *Good answer:* 10 bits/stream × 8 = 80 bits/frame; ×75 = 6000 bps.

4. **In VALL‑E, what information is carried by the acoustic prompt \(\tilde{C}\) that text alone doesn’t provide?**  
   *Good answer:* speaker identity + acoustic environment characteristics retained in codec tokens (VALL‑E rationale).

5. **Why might grouping codec tokens (VALL‑E 2) help long-form generation?**  
   *Good answer:* reduces sequence length by factor \(g\), lowering long-context error accumulation and speeding inference.

6. **What’s a concrete symptom of repetition/looping in codec LMs, and how does VALL‑E 2 address it?**  
   *Good answer:* repeated token patterns; repetition-aware sampling checks repetition ratio in a window and forces alternative sampling.

7. **What’s the role of the codec decoder in VALL‑E, and why is it useful?**  
   *Good answer:* converts discrete codes back to waveform; avoids training a separate vocoder and leverages codec fidelity.

8. **How do Whisper’s long-form heuristics decide to increase temperature?**  
   *Good answer:* fallback if avg logprob < −1 or gzip compression rate > 2.4; temperature steps 0→1.0 by 0.2.

---

## Likely Student Questions

**Q: What are Whisper’s exact audio feature settings?** → **A:** 16 kHz audio; 80-channel log-Mel spectrogram; 25 ms window; 10 ms stride; global scaling to ~[-1,1]. (https://cdn.openai.com/papers/whisper.pdf)

**Q: How does Whisper represent timestamps?** → **A:** timestamps are discrete tokens quantized to **20 ms** and interleaved with text (start token before caption text, end token after). (https://cdn.openai.com/papers/whisper.pdf)

**Q: In VALL‑E, what do the codec tokens look like (shape/rate)?** → **A:** using EnCodec @ 24 kHz, embeddings at **75 Hz**; RVQ with **8 quantizers** × **1024 entries**; codes form \(C \in \mathbb{N}^{T \times 8}\). (https://arxiv.org/abs/2301.02111)

**Q: How do you compute 6 kbps from RVQ settings?** → **A:** with 75 frames/s, 8 quantizers, 1024 entries: bits/frame \(=8\cdot \log_2(1024)=8\cdot10=80\); bps \(=80\cdot75=6000\) = 6 kbps. (https://arxiv.org/pdf/2107.03312.pdf; VALL‑E uses this config)

**Q: What is the RVQ algorithm in one sentence?** → **A:** iteratively quantize the residual: each stage picks a codebook vector for the current residual, adds it to the reconstruction, and updates the residual by subtraction. (https://arxiv.org/pdf/2107.03312.pdf)

**Q: What’s VALL‑E’s training objective for zero-shot TTS?** → **A:** maximize \(p(C\mid x,\tilde{C})\) where \(C\) are target codec codes, \(x\) is the phoneme sequence, and \(\tilde{C}\) are codec codes from a short acoustic prompt (e.g., 3 s). (https://arxiv.org/abs/2301.02111)

**Q: How does VALL‑E 2 reduce repetition/looping during sampling?** → **A:** repetition-aware sampling: start with top‑p sampling; compute repetition ratio in a history window \(w\); if ratio \(>\tau\), replace with random sampling. Reported eval hyperparams: \(w=50\), \(\tau=0.1\). (http://arxiv.org/pdf/2406.05370.pdf)

**Q: What are Whisper’s long-form decoding defaults (beam/temperature fallback)?** → **A:** beam=5; temperature fallback 0→1.0 in 0.2 steps if avg logprob < −1 or gzip compression rate > 2.4; previous-text conditioning when temp < 0.5. (https://cdn.openai.com/papers/whisper.pdf)

---

## Available Resources

### Videos
- [Let’s build GPT: from scratch, in code, spelled out.](https://youtube.com/watch?v=kCc8FmEb1nY) — Surface when: student needs a refresher on Transformer decoding/autoregression to map onto codec-LM generation.
- [Let’s build the GPT Tokenizer](https://youtube.com/watch?v=zduSFxRajkE) — Surface when: student is confused about “what tokenization means” and you want to transfer the concept to audio tokens (while noting Whisper uses log-Mels, not codec tokens).
- [Sora - OpenAI’s Text-to-Video Model (Paper Explained)](https://youtube.com/watch?v=_gCqFBFd_Ls) — Surface when: student asks about “tokenizing” other modalities (patch tokens) and you want a cross-modal analogy to speech tokens.

### Articles & Tutorials
- [The Illustrated Transformer (Jay Alammar)](https://jalammar.github.io/illustrated-transformer/) — Surface when: student needs a fast mental model of encoder–decoder attention (relevant to Whisper).
- [Whisper repository (OpenAI)](https://github.com/openai/whisper) — Surface when: student asks “where do I see the end-to-end inference pipeline?”
- [AudioCraft (Meta)](https://github.com/facebookresearch/audiocraft) — Surface when: student asks about practical tooling around EnCodec and audio generation stacks.
- [Robust Speech Recognition via Large-Scale Weak Supervision (Whisper paper)](https://arxiv.org/abs/2212.04356) — Surface when: student asks for canonical training/eval details and robustness claims.
- [High Fidelity Neural Audio Compression (EnCodec paper)](https://arxiv.org/abs/2210.13438) — Surface when: student asks “how do audio tokens actually get produced?”

---

## Key Sources

- [Whisper: Robust Speech Recognition via Large-Scale Weak Supervision](https://cdn.openai.com/papers/whisper.pdf) — primary source for Whisper architecture, feature defaults, prompting tokens, and decoding heuristics/benchmarks.
- [EnCodec: High Fidelity Neural Audio Compression](https://arxiv.org/abs/2210.13438) — primary source for neural audio tokenization, RVQ training, streaming/latency, and bitrate control.
- [VALL‑E: End-to-end codec language model for zero-shot TTS](https://arxiv.org/abs/2301.02111) — primary source for “TTS as conditional LM over codec tokens” and AR/NAR multi-stream generation.
- [SoundStream (RVQ + bitrate math)](https://arxiv.org/pdf/2107.03312.pdf) — clean RVQ algorithm and bitrate derivations used widely in neural codecs.
- [VALL‑E 2](http://arxiv.org/pdf/2406.05370.pdf) — grouped codec LM formulation and repetition-aware sampling details/hyperparameters.