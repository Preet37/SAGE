# Card: SmoothQuant (W8A8 PTQ via activation smoothing)
**Source:** https://arxiv.org/pdf/2211.10438.pdf  
**Role:** paper | **Need:** COMPARISON_DATA  
**Anchor:** Exact smoothing formulation (α) + calibration protocol + W8A8 accuracy/latency/memory tables

## Key Content
- **Uniform INT8 quantization (Eq. 1):** quantize float tensor \(x\) to INT8 \(\hat{x}\) with step size \(\Delta\): \(\hat{x}=\mathrm{round}(x/\Delta)\) (symmetric; asymmetric adds zero-point). \(\Delta\) typically set from max-abs (static via calibration or dynamic at runtime).  
- **Hardware constraint (Sec. 3, Eq. 2):** per-channel activation scaling is hard to fuse into INT8 GEMM; scaling is feasible only along outer GEMM dims and applied after matmul.
- **SmoothQuant smoothing transform (Eq. 3):** for linear \(Y=XW\), choose per-input-channel scale \(s\) and rewrite equivalently:  
  \[
  Y=(X\operatorname{diag}(s)^{-1})(\operatorname{diag}(s)W)
  \]
  Smooth activations by dividing each input channel by \(s\); compensate by scaling corresponding weight rows/cols (mathematically equivalent).
- **Choosing \(s\) with migration strength \(\alpha\) (Eq. 4):** split quantization difficulty between activations and weights:  
  \[
  s_j=\frac{\left(\max|X_j|\right)^{\alpha}}{\left(\max|W_j|\right)^{1-\alpha}}
  \]
  where \(j\) indexes input channels; \(\max|X_j|\) estimated from calibration samples; \(\alpha\in[0,1]\). Sweet spot for OPT/BLOOM: \(\alpha\approx0.5\); ablation shows good region \(\alpha\in[0.4,0.6]\). For heavier outliers (e.g., GLM-130B), use larger \(\alpha\) (e.g., 0.75).
- **Calibration protocol (Sec. 5.1):** compute smoothing factors + static quant steps once using **512 random sentences from The Pile**; reuse same quantized model for all downstream tasks. For GLM-130B static steps, **clip top 2% tokens** during calibration.
- **Accuracy (Table 3, OPT-175B avg):** FP16 **66.9%**; naive W8A8 **35.5%**; LLM.int8() **66.7%**; SmoothQuant O1/O2/O3 **66.5/66.4/66.8%** (WikiText PPL FP16 **10.99** vs SQ-O3 **11.17**; naive W8A8 **93080**).
- **Latency/memory (Table 8, decoding):** OPT-30B (1 GPU) BS1 Seq512: FP16 **422ms, 57GB** vs SQ **314ms, 30GB** (speedup **1.35×**, saving **1.91×**). OPT-175B (8 GPUs) BS16 Seq512: FP16 **2212ms, 50GB** vs SQ **1628ms, 30GB** (speedup **1.36×**, saving **1.67×**).  
- **Quantization schemes (Table 2):** SmoothQuant O1 = W per-tensor, A per-token dynamic; O2 = W per-tensor, A per-tensor dynamic; O3 = W per-tensor, A per-tensor static (coarser ⇒ lower latency).

## When to surface
Use when students ask how SmoothQuant’s **α-based smoothing** works, how to **calibrate** PTQ for W8A8, or need **specific accuracy/latency/memory comparisons** vs naive W8A8 and LLM.int8() on large models (e.g., OPT-175B).