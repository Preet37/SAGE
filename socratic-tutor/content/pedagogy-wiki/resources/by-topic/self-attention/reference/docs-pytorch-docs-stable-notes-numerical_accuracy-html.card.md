# Card: Numerical Accuracy Pitfalls & SDPA Precision Controls (PyTorch)
**Source:** https://docs.pytorch.org/docs/stable/notes/numerical_accuracy.html  
**Role:** Authoritative PyTorch behavior notes | **Need:** numerical stability/precision defaults & knobs  
**Anchor:** What can change floating-point results (esp. SDPA) and which backend flags control precision

## Key Content
- **Floating-point limits (IEEE 754):**  
  - fp32 has ~**7 decimal digits** precision; fp64 has ~**16 decimal digits**.  
  - **Addition/multiplication are not associative** ⇒ operation order can change results.
- **Reproducibility caveat:** PyTorch is **not guaranteed bitwise identical** across releases/commits/platforms; **CPU vs GPU** may differ even with identical inputs and controlled randomness.
- **Batching/slicing can change results (order of reductions):**  
  - For batched matmul: **(A @ B)[0]** not guaranteed bitwise equal to **A[0] @ B[0]** (even if mathematically identical).  
  - For slicing: **A.sum(-1)[0]** not guaranteed bitwise equal to **A[:, 0].sum()**.
- **Extremal values / overflow example:**  
  - `a = torch.tensor([1e20, 1e20])` (fp32) ⇒ `a.norm()` returns **inf**.  
  - `a.double().norm()` returns **1.4142e+20** (representable in fp32), showing intermediate overflow can dominate.
- **TF32 on Nvidia Ampere+:**  
  - TF32 tensor cores read only **10 mantissa bits** of inputs; can yield surprising errors (e.g., `I @ X ≠ X`).  
  - Defaults: TF32 **disabled for matmul**, **enabled for conv**.  
  - Control: `torch.backends.cuda.matmul.fp32_precision = "tf32"` to enable; disable conv TF32 via `torch.backends.cudnn.conv.fp32_precision = "ieee"`.
- **SDPA reduced-precision reductions (FP16/BF16):**  
  - **Default mitigation:** upcast FP16/BF16 inputs to **FP32**, compute in **FP32/TF32**, then downcast output to FP16/BF16 (better accuracy, more memory, possible perf regression).  
  - Speed-over-accuracy toggle: `torch.backends.cuda.allow_fp16_bf16_reduction_math_sdp(True)`.

## When to surface
Use when students ask why attention/softmax/SDPA outputs differ across devices, why FP16/BF16 attention becomes unstable, or how to choose/disable TF32 and reduced-precision reductions for numerical stability.