# Card: Accurate low-latency streaming ASR + joint EOS via CTC
**Source:** https://aclanthology.org/2023.acl-industry.26.pdf  
**Role:** paper | **Need:** DEPLOYMENT_CASE  
**Anchor:** Concrete streaming ASR architecture (chunking/streaming, endpointing, batching/beam) with latency+WER and operational choices

## Key Content
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

## When to surface
Use for questions about **how to build/deploy streaming ASR** with concrete **lookahead/latency tradeoffs**, **chunk/beam decoding**, and **joint end-of-speech detection** using a CTC model (thresholding with \(\alpha,\beta\)) plus real WER/latency numbers.