# Card: Accurate log-sum-exp / softmax computation (numerical stability)
**Source:** https://academic.oup.com/imajna/article/41/4/2311/5893596  
**Role:** Numerical analysis reference | **Need:** Stable softmax/log-sum-exp for attention  
**Anchor:** How to compute softmax and log-sum-exp accurately (avoid overflow/underflow)

## Key Content
- **Softmax definition (vector \(x\in\mathbb{R}^n\))**:  
  \[
  \mathrm{softmax}(x)_i=\frac{e^{x_i}}{\sum_{j=1}^n e^{x_j}},\quad i=1,\dots,n
  \]
- **Log-sum-exp (LSE) definition**:  
  \[
  \mathrm{LSE}(x)=\log\left(\sum_{j=1}^n e^{x_j}\right)
  \]
- **Stabilizing shift (core procedure)**: choose  
  \[
  m=\max_j x_j
  \]
  then compute
  \[
  \mathrm{LSE}(x)= m + \log\left(\sum_{j=1}^n e^{x_j-m}\right)
  \]
  and
  \[
  \mathrm{softmax}(x)_i=\frac{e^{x_i-m}}{\sum_{j=1}^n e^{x_j-m}}
  \]
  **Variables:** \(x_i\) logits/scores; \(m\) max-logit shift; denominator is the shifted exp-sum.
- **Design rationale:** subtracting \(m\) makes all exponents \(\le 0\), preventing overflow in \(e^{x_i}\) and improving accuracy when logits have large magnitude differences (common in attention score matrices).
- **Implementation default (vectorized):** compute \(m\) per row (per query) for attention matrices; apply shift before exponentiation; reuse the same shifted exp-sum for both LSE and softmax normalization.

## When to surface
Use when students ask why attention uses “subtract max before softmax,” how to implement stable softmax/log-sum-exp, or how numerical overflow/underflow arises in scaled dot-product attention.