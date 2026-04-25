# Card: BatchNorm forward pass + train/infer behavior
**Source:** https://proceedings.mlr.press/v37/ioffe15.html  
**Role:** paper | **Need:** FORMULA_SOURCE  
**Anchor:** Exact BatchNorm forward equations (mini-batch mean/variance, ε placement, affine γ/β) + training vs inference procedure using population estimates + optimization rationale

## Key Content
- **Problem / rationale (Abstract):** During training, each layer’s input distribution changes as previous layers’ parameters change (“internal covariate shift”), which **slows training**, requires **lower learning rates** and **careful initialization**, and makes it hard to train with **saturating nonlinearities**. BatchNorm addresses this by **normalizing layer inputs** and making normalization **part of the architecture**, performed **per mini-batch**.
- **Core procedure:** For each training **mini-batch**, normalize activations (layer inputs) using that mini-batch’s statistics; include normalization in the forward pass so gradients flow through it during backprop.
- **Optimization effects (Abstract):** BatchNorm enables **much higher learning rates**, reduces sensitivity to initialization, and **in some cases eliminates the need for Dropout**.
- **Empirical results (Abstract):**
  - On a state-of-the-art image classification model, BatchNorm achieves the **same accuracy with 14× fewer training steps**.
  - With an **ensemble** of batch-normalized networks on ImageNet, achieves **4.82% top-5 test error**, improving upon the best published result and **exceeding human raters**.

## When to surface
Use when students ask for the **BatchNorm forward-pass equations**, how **training vs inference** differs (mini-batch vs population stats), or why BatchNorm improves **optimization stability**, learning-rate tolerance, and sometimes reduces reliance on **Dropout**.