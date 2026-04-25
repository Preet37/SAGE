# Card: Glorot/Bengio 2010 — Saturation, vanishing gradients, Xavier init
**Source:** https://proceedings.mlr.press/v9/glorot10a/glorot10a.pdf  
**Role:** benchmark | **Need:** EMPIRICAL_DATA  
**Anchor:** Empirical/analytic evidence of vanishing gradients with sigmoid/tanh and motivation for variance-preserving (Xavier/Glorot) initialization tied to saturation & signal propagation.

## Key Content
- **Training setup (Section 2.3):** Feedforward nets with **1–5 hidden layers**, **1000 units/layer**, **softmax** output; loss **negative log-likelihood** \(-\log P(y|x)\). **SGD minibatch size 10**, learning rate \(\epsilon\) tuned via validation after **5 million updates**. **Biases initialized to 0**.
- **Standard init (Eq. 1):** \(W_{ij}\sim U\left[-\frac{1}{\sqrt{n}},\frac{1}{\sqrt{n}}\right]\), \(n=\) fan-in (prev layer size).
- **Sigmoid saturation (Section 3.1, Fig. 2):** With random init + sigmoid, **top hidden layer quickly saturates near 0**, causing slow learning/plateaus; in a 4-hidden-layer net it **slowly desaturates ~epoch 100**; depth-5 may **never escape** saturation. Rationale: sigmoid’s **non-zero mean** pushes top activations toward 0 where sigmoid is saturated → gradients blocked.
- **Tanh vs softsign (Section 3.2–3.3, Fig. 3–4):** tanh shows **sequential saturation** starting at layer 1 upward; **softsign** saturates less and keeps activations near “knees” (≈0.6–0.8) where nonlinearity + gradient flow coexist.
- **Gradient/variance analysis (Section 4.2):** With \(s_i=z_iW_i+b_i,\ z_{i+1}=f(s_i)\):  
  \(\frac{\partial C}{\partial s_i^k}=f'(s_i^k)\, W_{i+1}^{k,\bullet}\frac{\partial C}{\partial s_{i+1}}\) (Eq. 2) and \(\frac{\partial C}{\partial w_i^{l,k}}=z_i^l\frac{\partial C}{\partial s_i^k}\) (Eq. 3).  
  To preserve forward/backward variance: want \(n_i\mathrm{Var}[W_i]\approx 1\) (Eq. 10) and \(n_{i+1}\mathrm{Var}[W_i]\approx 1\) (Eq. 11) ⇒ compromise \(\mathrm{Var}[W_i]=\frac{2}{n_i+n_{i+1}}\) (Eq. 12).
- **Normalized/Xavier init (Eq. 16):** \(W\sim U\left[-\frac{\sqrt{6}}{\sqrt{n_j+n_{j+1}}},\frac{\sqrt{6}}{\sqrt{n_j+n_{j+1}}}\right]\). Empirically, average Jacobian singular value ratio ≈ **0.8** vs **0.5** with standard init (Section 4.2.2).
- **Empirical test errors (Table 1, 5 hidden layers):**  
  - **Shapeset:** Sigmoid **82.61**; Tanh **27.15**; **Tanh+Norm 15.60**; Softsign **16.27**; Softsign+Norm **16.06**  
  - **MNIST:** Sigmoid **2.21**; Tanh **1.76**; **Tanh+Norm 1.64**; Softsign **1.64**  
  - **CIFAR-10:** Sigmoid **57.28**; Tanh **55.9**; **Tanh+Norm 52.92**; Softsign+Norm **53.8**  
  - **Small-ImageNet:** Sigmoid **70.66**; Tanh **70.58**; **Tanh+Norm 68.57**; Softsign+Norm **68.13**
- **Design rationale:** Keep layer Jacobians near 1 so **activations and gradients “flow”**; avoid sigmoid with small random init due to **top-layer saturation**; cross-entropy/log-likelihood shows **fewer plateaus** than quadratic loss (Section 4.1, Fig. 5).

## When to surface
Use when students ask why deep sigmoid/tanh nets get vanishing gradients/saturation, why Xavier/Glorot initialization uses fan-in+fan-out scaling, or what empirical gains normalized initialization provides across datasets.