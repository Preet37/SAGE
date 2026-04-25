# Card: EnCodec Residual Vector Quantization (RVQ) + Loss Objective
**Source:** https://arxiv.org/pdf/2210.13438.pdf  
**Role:** paper | **Need:** FORMULA_SOURCE  
**Anchor:** RVQ formulation (residual recursion, codebook summation) + commitment loss + full generator objective

## Key Content
- **RVQ procedure (Section 3.2):** Quantize encoder latent with multiple codebooks sequentially by **quantizing residuals**. Output latent from encoder has shape **z ∈ ℝ[B, D, T]**. RVQ produces discrete indices **i ∈ [B, Nq, T]** where **Nq** = number of codebooks used (bandwidth-dependent). To reconstruct a quantized latent vector before the decoder, **sum selected codebook entries across codebooks** (one entry per codebook per time step).
- **Training mechanics (Section 3.2):**
  - **Straight-through estimator** for encoder gradients (treat quantization as identity in backward pass).
  - Codebook entries updated by **EMA** with **decay 0.99**; unused entries **replaced** with candidates sampled from current batch.
  - **Variable-bandwidth training:** randomly select **Nq as a multiple of 4** (24 kHz supports **1.5/3/6/12/24 kbps**).
  - Typical config: up to **32 codebooks** (24 kHz) or **16** (48 kHz), each with **1024 entries** (= **10 bits/codebook**).
- **Commitment loss (Eq. 3, Section 3.4):** for residual steps **c = 1..C** (C depends on bandwidth), with residual **z_c** and nearest codebook vector **q_c(z_c)**:  
  \[
  \ell_w = \sum_{c=1}^{C} \|z_c - q_c(z_c)\|_2^2
  \]
  Gradient is computed **only w.r.t. z_c** (not the quantized vector).
- **Full generator loss (Eq. 4):**  
  \[
  L_G=\lambda_t\ell_t+\lambda_f\ell_f+\lambda_g\ell_g+\lambda_{feat}\ell_{feat}+\lambda_w\ell_w
  \]
  where **time L1**: \(\ell_t(x,\hat x)=\|x-\hat x\|_1\); **multi-scale mel loss** \(\ell_f\) (Eq. 1); adversarial + feature matching (Eq. 2).
- **Key empirical bandwidth result (Table 1):** EnCodec **3.0 kbps** becomes **1.9 kbps** with entropy coding; **6.0→4.1 kbps**, **12.0→8.9 kbps**.

## When to surface
Use when students ask how **residual vector quantization** works (residual recursion, combining codebooks), or what **loss terms** (especially commitment/codebook losses) are used to train EnCodec-style discrete audio tokenizers.