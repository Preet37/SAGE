# Card: Choosing llama.cpp GGUF quantization (Llama-3.1-8B-Instruct)
**Source:** https://arxiv.org/pdf/2601.14277.pdf  
**Role:** paper | **Need:** COMPARISON_DATA  
**Anchor:** Unified downstream + throughput evaluation of llama.cpp GGUF quantization choices; GGML/GGUF block-wise (and K-quant hierarchical) quantized-tensor storage concepts.

## Key Content
- **Quantization math (Section 2.1):**
  - **Eq. (1) affine quantizer:** \(w \approx s\,(q - z)\) where \(w\)=real weight, \(q\)=integer code, \(s\)=scale, \(z\)=zero-point/offset. In GGML-style PTQ, \(s,z\) are stored **per block** (not per tensor).
  - **Eq. (2) Q4_1-style dequant:** \(w \approx s\,q + m\) where \(m\)=stored per-block offset/min (asymmetric/affine).
  - **Eq. (3) high-resolution error model:** for symmetric \(b\)-bit uniform quantizer, step \(\Delta\) implies quantization error variance \(\approx \Delta^2/12\); +1 bit \(\Rightarrow\) ~4× lower modeled variance (subject to clipping/heavy tails).
- **Format design (Section 2.2):**
  - Legacy: Q4_0 (symmetric), Q4_1 (affine), Q5_0/Q5_1, Q8_0 (symmetric 8-bit).
  - **K-quants:** hierarchical **super-blocks of 256 weights**, split into sub-blocks with additional (often quantized) scale/min metadata; suffixes _S/_M/_L trade compression vs fidelity.
- **Procedure (Section 3):**
  - Quantize from the same FP16 GGUF via: `./llama-quantize <f16.gguf> <out.gguf> <SCHEME>`.
  - Benchmarks: GSM8K (5-shot), HellaSwag (0-shot), IFEval (0-shot), MMLU (0-shot), TruthfulQA (0-shot), plus WikiText-2 perplexity.
  - Throughput measured with **pp=512** (prefill) and **tg=128** (decode).
- **Key empirical results (Table 2, Llama-3.1-8B-Instruct):**
  - **F16:** Avg 69.47, PPL 7.32.
  - **Q5_0:** size reduction **65.19%**, Avg **69.92** (highest), PPL **7.43**.
  - **Q4_K_S:** reduction **70.83%**, Avg **69.17**, PPL **7.62**.
  - **Q3_K_S (most compressed):** reduction **77.23%**, Avg **65.49**, PPL **8.96**; GSM8K drops **77.63 → 68.31**.
- **Throughput (Table 3, tokens/s):**
  - **F16:** pp512 79.57, tg128 2.83.
  - **Q3_K_S:** pp512 57.39, tg128 **9.91** (fastest decode).
  - **Q4_K_S:** pp512 92.52, tg128 4.65.
  - **Q5_0:** pp512 61.44, tg128 6.66.
- **Pareto guidance (Section 4.3):** Non-dominated set highlighted: **Q5_0** (best AvgLoss with strong compression), then **Q4_K_S**, then **Q3_K_L / Q3_K_M**, with **Q3_K_S** only when footprint dominates.

## When to surface
Use when students ask “Which GGUF quantization should I pick in llama.cpp?” or need concrete quality–size–throughput trade-offs (3–8 bit, K-quants vs legacy) for CPU/local inference.