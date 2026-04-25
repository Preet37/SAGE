# Card: Luong (2015) Global vs. Local (Multiplicative) Attention
**Source:** https://aclanthology.org/D15-1166/  
**Role:** paper | **Need:** FORMULA_SOURCE  
**Anchor:** Exact Luong et al. (2015) equations for global/local attention: score functions (dot/general/concat), local predicted position \(p_t\), Gaussian windowing.

## Key Content
- **Global attention (Section 3; Eq. for context):**  
  Given decoder state \(h_t\) and encoder states \(\{\bar h_s\}_{s=1}^S\):  
  \[
  a_t(s)=\mathrm{softmax}(\mathrm{score}(h_t,\bar h_s)),\quad
  c_t=\sum_{s=1}^S a_t(s)\,\bar h_s
  \]
  where \(a_t(s)\) are alignment weights, \(c_t\) is the context vector.
- **Score functions (multiplicative vs. concat):**
  - **dot:** \(\mathrm{score}(h_t,\bar h_s)=h_t^\top \bar h_s\)
  - **general (bilinear):** \(\mathrm{score}(h_t,\bar h_s)=h_t^\top W_a \bar h_s\)
  - **concat (additive-style):** \(\mathrm{score}(h_t,\bar h_s)=v_a^\top \tanh(W_a [h_t;\bar h_s])\)  
  Parameters: \(W_a\) (matrix), \(v_a\) (vector), \([\,;\,]\) concatenation.
- **Local attention (Section 3.1; predicted position + window):**
  - Predict aligned source position:
    \[
    p_t = S \cdot \sigma(v_p^\top \tanh(W_p h_t))
    \]
    where \(S\)=source length, \(\sigma\)=sigmoid, \(W_p, v_p\)=learned.
  - Attend only to a window around \(p_t\) (size \(2D+1\)); apply Gaussian bias:
    \[
    a_t(s)\propto \exp(\mathrm{score}(h_t,\bar h_s))\cdot
    \exp\!\left(-\frac{(s-p_t)^2}{2\sigma^2}\right)
    \]
    with \(\sigma = D/2\) (paper default), then normalize over \(s\in[p_t-D,\,p_t+D]\).
- **Design rationale:** global = full soft alignment (more compute); local = restrict to neighborhood for **computational efficiency** while keeping differentiable soft attention via Gaussian weighting.

## When to surface
Use when students ask for the *exact Luong attention equations*, differences between **global vs. local attention**, or how **dot/general/concat** scoring and **local \(p_t\)+Gaussian windowing** are defined.