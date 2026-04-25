# Card: Whisper benchmarks + decoding/eval defaults
**Source:** https://cdn.openai.com/papers/whisper.pdf  
**Role:** benchmark | **Need:** EMPIRICAL_DATA  
**Anchor:** Benchmark WER/BLEU tables across datasets + model sizes; decoding/evaluation setup (normalization, long-form heuristics)

## Key Content
- **Training data & tasks (Sec. 2.1–2.3):** 680,000 hours weakly supervised audio-text; includes **117k hours / 96 non-English languages** and **125k hours X→en translation**. Audio split into **30s segments**. Multitask decoder prompt tokens: `<|startoftranscript|>`, **language token (99 total)**, `<|nospeech|>` (VAD), task token `<|transcribe|>`/`<|translate|>`, `<|notimestamps|>`; timestamps quantized to **20 ms** and interleaved (start token before caption text, end token after).
- **Audio/features (Sec. 2.2):** resample **16 kHz**; **80-channel log-Mel**, **25 ms window**, **10 ms stride**; global scaling to **[-1, 1]** ~zero mean.
- **Model family (Table 1):** Transformer encoder-decoder. Params: **Tiny 39M**, **Base 74M**, **Small 244M (12L, 768w, 12h)**, **Medium 769M (24L, 1024w, 16h)**, **Large 1550M (32L, 1280w, 20h)**. Large **V2** trained longer (+SpecAugment, Stochastic Depth, BPE dropout).
- **Optimization defaults (Sec. 2.4):** AdamW, FP16, grad-norm clipping; **batch 256 segments**; LR warmup **2048 updates**, linear decay to 0; train **2^20 updates** (~2–3 epochs).
- **WER evaluation (Sec. 3.2):** extensive **text normalization** before WER; can reduce WER up to **50%** on some datasets.
- **Key English robustness result (Table 2):** vs wav2vec2 Large (no LM), Whisper Large V2 matches LibriSpeech Clean **2.7 WER** but is far better OOD: e.g., **CHiME6 25.5 vs 65.8**, **Common Voice 9.0 vs 29.9**, **TED-LIUM 4.0 vs 10.5**; **Average WER 12.8 vs 29.3** (**55.2% relative error reduction**).
- **Multilingual/translation benchmarks:** MLS/VoxPopuli (Table 3): Whisper zero-shot **7.3 WER (MLS)**, **13.6 (VoxPopuli)**. CoVoST2 X→en (Table 4): Whisper **29.1 BLEU** (High/Mid/Low: **36.2/32.6/25.2**).
- **Noise robustness (Sec. 3.7):** under **pub noise**, Whisper outperforms all compared models when **SNR < 10 dB**.
- **Long-form decoding heuristics (Sec. 4.5, Table 7):** **beam=5**; temperature fallback **0→1.0 step 0.2** if avg logprob < **−1** or gzip compression rate > **2.4**; previous-text conditioning when temp < **0.5**; VAD: `<|nospeech|>` prob > **0.6** plus avg logprob < **−1**; constrain initial timestamp to **0.0–1.0 s**. Average WER improves **11.0 → 10.0** across long-form sets with full heuristics.

## When to surface
Use for questions about **Whisper’s reported WER/BLEU on specific datasets**, **how evaluation/normalization affects WER**, or **default decoding settings for long-form transcription and robustness (noise, OOD)**.