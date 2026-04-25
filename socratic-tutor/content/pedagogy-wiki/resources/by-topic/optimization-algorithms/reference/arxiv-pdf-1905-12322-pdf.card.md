# Card: BFLOAT16 training parity vs FP32 (empirical)
**Source:** https://arxiv.org/pdf/1905.12322.pdf  
**Role:** benchmark | **Need:** EMPIRICAL_DATA  
**Anchor:** Cross-task BF16 vs FP32 convergence/accuracy; BF16’s FP32-like exponent range often removes need for loss scaling

## Key Content
- **Numeric format (Table 1):**  
  - FP32: (sign,exp,mant) = (1,8,23); max normal **3.40e38**; min normal **1.17e−38**; min subnormal **1.40e−45**  
  - FP16: (1,5,10); max normal **6.55e4**; min normal **6.10e−5**; min subnormal **5.96e−8**  
  - **BFLOAT16:** (1,8,7); max normal **3.38e38**; min normal **1.17e−38**; **no subnormals**  
  - **Rationale (Sec. 3):** BF16 keeps FP32 exponent range ⇒ fewer over/underflows in backprop gradients; avoids FP16-style **loss scaling** hyperparameter tuning.
- **Mixed-precision workflow (Fig. 1, Sec. 3):**
  - GEMMs take **BF16 inputs** (weights/activations/gradients) and **accumulate to FP32 outputs**.
  - A **FP32 master copy of weights** is used for the optimizer update step (e.g., SGD) to preserve accuracy.
  - “Quantlib” emulation: convert FP32→BF16 by **zeroing low 16 bits** with **RNE (round-to-nearest-even)**; applied before ops intended to run in BF16.
  - Bias tensors kept **FP32**; non-GEMM ops (BN, ReLU/tanh/sigmoid) accept BF16 inputs.
- **Empirical parity (Sec. 4):**
  - **AlexNet ImageNet-1K:** FP32 **57.4/80.7** (top1/top5) vs BF16 **57.2/80.1**; global minibatch **1024**, data-parallel **16 nodes**, **88 epochs**.
  - **ResNet-50 ImageNet-1K:** FP32 **74.7/92.0** vs BF16 **74.7/92.0**; global minibatch **1024**, **32 nodes**, **SGD + Nesterov**, **90 epochs**, LR warmup **5 epochs**.
  - **GNMT BLEU (Table 2):** DE→EN **29.3 vs 29.3**; VI→EN(+attention) **17.1 vs 18.3** (FP32 vs BF16).
  - **Recsys logloss (Table 5; lower is better):** Deep&Cross **0.44372 vs 0.44372** (BF16 RND); DNN recsys **0.12520 vs 0.12520** (BF16 RND). Truncation slightly worse (e.g., **0.44393**, **0.12537**).

## When to surface
Use when students ask whether BF16 needs loss scaling/hyperparameter retuning, or want concrete convergence/accuracy comparisons of BF16 vs FP32 across CNN/RNN/recsys workloads and typical mixed-precision training steps.