# Card: Glorot & Bengio 2010 — Why deep nets fail + Xavier init
**Source:** https://proceedings.mlr.press/v9/glorot10a.html  
**Role:** paper | **Need:** EMPIRICAL_DATA  
**Anchor:** Variance-preserving (Xavier/Glorot) initialization analysis + empirical evidence of saturation/vanishing gradients in deep sigmoid/tanh nets

## Key Content
- **Problem diagnosed (Abstract):** Standard gradient descent from random initialization performs poorly for deep feedforward nets; successful deep training (post-2006) relied on **new initialization/training mechanisms**.
- **Activation-function effect (Abstract):**
  - **Logistic sigmoid** is **unsuited for deep networks with random initialization** because its **non-zero mean** can push (especially) the **top hidden layer into saturation**.
  - **Saturated units can move out of saturation** on their own **slowly**, explaining **training plateaus** sometimes observed.
  - A **new non-linearity that saturates less** can be beneficial (motivates choosing less-saturating activations vs sigmoid).
- **Gradient/conditioning rationale (Abstract):**
  - Training becomes difficult when **singular values of the layer Jacobian** are **far from 1** (implies exploding/vanishing gradients through the chain rule).
  - Authors study how **activations and gradients vary across layers and during training** to connect saturation/vanishing gradients to Jacobian conditioning.
- **Procedure/design outcome (Abstract):**
  - Propose a **new initialization scheme** aimed at keeping signal/gradients well-scaled across depth (i.e., Jacobian singular values closer to 1), yielding **substantially faster convergence**.

## When to surface
Use when students ask why deep sigmoid/tanh networks get stuck (plateaus), why gradients vanish/explode with depth (Jacobian singular values), or what initialization principles (Xavier/Glorot) address these issues.