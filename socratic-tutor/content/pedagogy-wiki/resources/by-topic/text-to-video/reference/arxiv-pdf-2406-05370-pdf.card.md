# Card: VALL‑E 2 — Grouped Neural Codec LM + Repetition‑Aware Sampling
**Source:** http://arxiv.org/pdf/2406.05370.pdf  
**Role:** paper | **Need:** FORMULA_SOURCE  
**Anchor:** Neural codec tokenization + codec-language-model formulation for zero-shot TTS; decoding/sampling (repetition-aware) over discrete audio token streams.

## Key Content
- **Codec tokenization setup (Sec. 4.1.1):** Text tokenization via **BPE**. Speech tokenization via **EnCodec @ 6 kbps, 24 kHz**; waveform decoding via **Vocos**.
- **Grouped codec language modeling (Sec. 3.1, Eq. 1–4):** Audio → codec codes \(c\) of length \(T\), with \(Q\) quantizers (paper uses **8 code streams** per time step). Partition into groups of size \(g\): grouped sequence \(\tilde{c}=\{\tilde{c}_1,\dots,\tilde{c}_{T/g}\}\). Train by NLL:
  - **Eq. (1–2):** minimize \(-\log p(\tilde{c}\mid x)= -\sum_i \log p(\tilde{c}_i \mid \tilde{c}_{<i}, x)\), where \(x\) is text tokens.
  - **Inference (Eq. 3–4):** prompt with enrolled speech codes \(\tilde{c}^{(p)}\) + text (prompt transcript + target text) to generate target grouped codes \(\tilde{c}^{(t)}\), then decode to waveform.
  - **Rationale:** grouping reduces sequence length by factor \(g\) → faster inference + mitigates long-context errors.
- **Hierarchical modeling (Sec. 3.2):**
  - **AR model** generates **first code stream** (coarse) per frame/group causally.
  - **NAR model** generates remaining **code streams 2–8** conditioned on text + prompt + preceding streams (full attention); run **7 passes** with greedy decoding (Sec. 3.4.2).
- **Repetition‑Aware Sampling (Sec. 3.4.1, Alg. 1):** Start with nucleus sampling (top‑\(p\)). Compute repetition ratio of sampled token within a history window \(w\); if ratio \(>\tau\), **replace** with **random sampling** from the distribution to avoid infinite loops. Hyperparams used in eval: **\(w=50\)**, **\(\tau=0.1\)**; top‑\(p\) searched **0.0–1.0 in 0.1 steps** (Sec. 4.1.3).
- **Empirical results (LibriSpeech test-clean, Table 1):** Single-sampling robustness improves vs VALL‑E:
  - **VALL‑E:** SIM **0.773**, WER **2.3**, DNSMOS **3.942** (3s prefix prompt).
  - **VALL‑E 2 (g=1):** SIM **0.782**, WER **1.6**, DNSMOS **3.947** (3s prefix).
  - **VALL‑E 2 (g=2):** SIM **0.777**, WER **1.5**, DNSMOS **3.966** (3s prefix).
- **Multi-sample selection (Eq. 23):** For 5 samples, select by sorting on **WER if SIM>0.3 else SIM** (lexicographic argmax).

## When to surface
Use when students ask how VALL‑E/VALL‑E 2 formulates TTS as **codec-token language modeling**, how **grouping** changes sequence length/frame rate, or how **repetition-aware sampling** prevents looping and stabilizes decoding.