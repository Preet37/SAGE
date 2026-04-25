---
title: "Neural Networks"
subject: "Foundational AI"
date: 2025-01-01
tags:
  - "subject/foundational-ai"
  - "level/beginner"
  - "level/intermediate"
  - "level/advanced"
  - "educator/3blue1brown"
  - "educator/christopher-olah"
  - "educator/lilian-weng"
  - "educator/andrej-karpathy"
  - "resource/video"
  - "resource/blog"
  - "resource/deep-dive"
  - "resource/paper"
  - "resource/code"
educators:
  - "3Blue1Brown"
  - "Christopher Olah"
  - "Lilian Weng"
  - "Andrej Karpathy"
levels:
  - "beginner"
  - "intermediate"
  - "advanced"
resources:
  - "video"
  - "blog"
  - "deep-dive"
  - "paper"
  - "code"
---

# Neural Networks

## Video (best)
- **3Blue1Brown** — "But what is a neural network?"
- **Watch:** [YouTube](https://www.youtube.com/watch?v=aircAruvnKk)
- Why: Exceptional visual intuition for neurons, layers, weights, and activations. Grant Sanderson's animation-driven pedagogy makes abstract concepts concrete without sacrificing mathematical honesty. The best entry point for understanding *what* a neural network is before diving into training mechanics.
- Level: beginner

---

## Blog / Written explainer (best)
- **Christopher Olah** — "Neural Networks, Manifolds, and Topology"
- **Link:** [https://colah.github.io/posts/2014-03-NN-Manifolds-Topology/](https://colah.github.io/posts/2014-03-NN-Manifolds-Topology/)
- Why: Olah builds geometric intuition for *why* neural networks work — how layers progressively untangle data manifolds. Uniquely insightful for understanding depth and activation functions conceptually, not just mechanically. Complements formula-heavy resources by answering the "why does this architecture work?" question.
- Level: intermediate

> **Note:** For a more introductory written explainer, Olah's "Understanding LSTM Networks" (https://colah.github.io/posts/2015-08-Understanding-LSTMs/) is also excellent, though more specific. For the general feedforward case, his manifolds post is the strongest pedagogical choice.

---

## Deep dive
- **Lilian Weng** — "A Peek into the Basics of Neural Networks" / General ML foundations posts
- url: https://lilianweng.github.io/posts/2017-06-21-overview/ [NOT VERIFIED]
- Why: Weng's posts are exhaustively referenced, mathematically rigorous, and cover the full stack — forward pass, loss functions, backpropagation, regularization (dropout, weight decay, batch normalization), and optimization. Serves as a reliable technical reference that bridges intuition and implementation.
- Level: intermediate–advanced

---

## Original paper
- **Rumelhart, Hinton & Williams (1986)** — "Learning representations by back-propagating errors"
- **Link:** [https://www.nature.com/articles/323533a0](https://www.nature.com/articles/323533a0)
- Why: The seminal paper that established backpropagation as a practical training algorithm for multi-layer networks. Remarkably readable for its age and historically essential. Most modern neural network training traces directly to this work.
- Level: advanced

> **Note:** Because this predates arXiv, no arxiv URL exists. A freely accessible scan is often found at http://www.cs.toronto.edu/~hinton/absps/naturebp.pdf

---

## Code walkthrough
- **Andrej Karpathy** — "The spelled-out intro to neural networks and backpropagation: building micrograd"
- **Watch:** [YouTube](https://www.youtube.com/watch?v=VMj-3S1tku0)
- Why: Karpathy builds a scalar-valued autograd engine and a neural network from absolute scratch in pure Python (~150 lines). Every concept — neurons, layers, forward pass, loss, backpropagation via chain rule, gradient descent — is implemented explicitly with no framework magic. The best existing resource for understanding *how* these pieces connect in code. Pairs perfectly with the 3Blue1Brown video above.
- **Link:** [https://github.com/karpathy/micrograd](https://github.com/karpathy/micrograd)
- Level: beginner–intermediate

---

## Coverage notes
- **Strong:** Forward pass mechanics, neuron/layer abstraction, backpropagation intuition, visual explanations (3B1B), from-scratch implementation (Karpathy/micrograd)
- **Weak:** Batch normalization and dropout as standalone topics are underserved by the resources above — they appear as supporting concepts but rarely as the *focus* of a dedicated best-in-class explainer
- **Gap:** No single resource above gives deep, dedicated treatment to **batch normalization** specifically. Ioffe & Szegedy's original paper (https://arxiv.org/abs/1502.03167) is the best available reference for that sub-topic. Similarly, **data augmentation** as a neural network regularization strategy has no outstanding standalone explainer in the preferred educator list — most coverage is framework-specific (PyTorch/TF docs) rather than conceptual.
- **Duplicate alert:** The existing curated list contains 4 duplicate entries each for `aircAruvnKk` and `Ilg3gGewQ5U` — deduplication is strongly recommended before publishing.

---

---

## Additional Resources for Tutor Depth

> **9 sources** — papers, official docs, working code, benchmarks, and deep explainers that give the AI tutor precision on this topic.

### 📄 BatchNorm forward pass + train/infer behavior
**Paper** · [source](https://proceedings.mlr.press/v37/ioffe15.html)

*Exact BatchNorm forward equations (mini-batch mean/variance, ε placement, affine γ/β) + training vs inference procedure using population estimates + optimization rationale*

<details>
<summary>Key content</summary>

- **Problem / rationale (Abstract):** During training, each layer’s input distribution changes as previous layers’ parameters change (“internal covariate shift”), which **slows training**, requires **lower learning rates** and **careful initialization**, and makes it hard to train with **saturating nonlinearities**. BatchNorm addresses this by **normalizing layer inputs** and making normalization **part of the architecture**, performed **per mini-batch**.
- **Core procedure:** For each training **mini-batch**, normalize activations (layer inputs) using that mini-batch’s statistics; include normalization in the forward pass so gradients flow through it during backprop.
- **Optimization effects (Abstract):** BatchNorm enables **much higher learning rates**, reduces sensitivity to initialization, and **in some cases eliminates the need for Dropout**.
- **Empirical results (Abstract):**
  - On a state-of-the-art image classification model, BatchNorm achieves the **same accuracy with 14× fewer training steps**.
  - With an **ensemble** of batch-normalized networks on ImageNet, achieves **4.82% top-5 test error**, improving upon the best published result and **exceeding human raters**.

</details>

### 📄 Glorot & Bengio 2010 — Why deep nets fail + Xavier init
**Paper** · [source](https://proceedings.mlr.press/v9/glorot10a.html)

*Variance-preserving (Xavier/Glorot) initialization analysis + empirical evidence of saturation/vanishing gradients in deep sigmoid/tanh nets*

<details>
<summary>Key content</summary>

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

</details>

### 📄 LayerNorm (per-example, per-layer normalization)
**Paper** · [source](https://arxiv.org/abs/1607.06450)

*LayerNorm definition (mean/variance over features per example), affine parameters, and training/inference invariance vs BatchNorm*

<details>
<summary>Key content</summary>

- **Feed-forward pre-activation (“summed inputs”)** (Eq. 1): for layer \(l\), unit \(i\)  
  \[
  a_i^{l} = (w_i^{l})^\top h^{l},\quad h_{i}^{l+1}=f(a_i^{l}+b_i^{l})
  \]
  where \(h^{l}\)=input to layer \(l\), \(W^{l}\)=weight matrix (rows \(w_i^{l}\)), \(b_i^{l}\)=bias, \(f\)=elementwise nonlinearity.
- **LayerNorm statistics (per training case, across hidden units/features)** (Section 3, Eq. 3): for \(H\) hidden units in layer \(l\)  
  \[
  \mu^{l}=\frac{1}{H}\sum_{i=1}^{H} a_i^{l},\quad
  \sigma^{l}=\sqrt{\frac{1}{H}\sum_{i=1}^{H}(a_i^{l}-\mu^{l})^{2}}
  \]
- **Apply learned affine gain/bias after normalization, before nonlinearity** (Eq. 5 / Supplement Eq. 15):  
  \[
  h_i = f\!\left(\frac{g_i}{\sigma}(a_i-\mu)+b_i\right)
  \]
  Vector form: \(\mathrm{LN}(z;\alpha,\beta)=\alpha\odot\frac{z-\mu}{\sigma}+\beta\), with \(\mu=\frac{1}{D}\sum_{i=1}^D z_i\), \(\sigma=\sqrt{\frac{1}{D}\sum_{i=1}^D(z_i-\mu)^2}\) (Eqs. 15–16).
- **RNN form (per time step)** (Eq. 4): \(a^{t}=W_{hh}h^{t-1}+W_{xh}x^{t}\) then  
  \[
  h^{t}=f\!\left(\frac{g}{\sigma^{t}}\odot(a^{t}-\mu^{t})+b\right),\ 
  \mu^{t}=\tfrac{1}{H}\sum_i a_i^{t},\ 
  \sigma^{t}=\sqrt{\tfrac{1}{H}\sum_i(a_i^{t}-\mu^{t})^{2}}
  \]
- **Key rationale/contrast with BatchNorm:** LN uses **no mini-batch statistics** (works with batch size 1) and performs **the same computation at training and test** (no running averages). It introduces **no dependencies between training cases** (Abstract/Section 3).
- **Invariance result:** LN is invariant to **re-scaling individual training cases** (Eq. 7): if \(x'=\delta x\), prediction unchanged because \(\mu,\sigma\) scale by \(\delta\).

</details>

### 📊 Glorot/Bengio 2010 — Saturation, vanishing gradients, Xavier init
**Benchmark** · [source](https://proceedings.mlr.press/v9/glorot10a/glorot10a.pdf)

*Empirical/analytic evidence of vanishing gradients with sigmoid/tanh and motivation for variance-preserving (Xavier/Glorot) initialization tied to saturation & signal propagation.*

<details>
<summary>Key content</summary>

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

</details>

### 📊 He Initialization + PReLU (Rectifiers on ImageNet)
**Benchmark** · [source](https://arxiv.org/abs/1502.01852)

*PReLU activation + rectifier-aware (“He/Kaiming”) initialization; ablations/benchmarks on convergence and ImageNet accuracy.*

<details>
<summary>Key content</summary>

- **PReLU definition (Eq. 1, Sec. 2.1):**  
  \[
  f(y_i)=\begin{cases}
  y_i,& y_i>0\\
  a_i y_i,& y_i\le 0
  \end{cases}
  \quad\text{equiv. } f(y_i)=\max(0,y_i)+a_i\min(0,y_i)
  \]
  - \(a_i\) learnable slope for negative inputs (channel-wise) or shared per layer (channel-shared).
- **PReLU optimization (Sec. 2.1, Eq. 4):** momentum update  
  \[
  \Delta a_i := \mu \Delta a_i + \epsilon \frac{\partial E}{\partial a_i}
  \]
  - Initialize \(a_i=0.25\). **No weight decay on \(a_i\)** (L2 would bias toward ReLU by pushing \(a_i\to 0\)). Learned \(a_i\) rarely > 1.
- **Empirical PReLU vs ReLU (Table 2, 14-layer model, 10-view test, 75 epochs):**
  - ReLU: **top-1 33.82%**, **top-5 13.34%**
  - PReLU (channel-shared): **top-1 32.71%**, **top-5 12.87%**
  - PReLU (channel-wise): **top-1 32.64%**, **top-5 12.75%** (≈ **1.2%** top-1 gain vs ReLU)
- **Rectifier-aware initialization (Sec. 2.2):** derives variance scaling for rectifiers; commonly used as **He init**  
  - Weight std often expressed as \(\text{std}=\sqrt{2/\hat n_l}\) (fan-in \(\hat n_l\)); improves signal/gradient scaling across depth.
  - **Convergence:** 30-layer rectified net converges with this init; **“Xavier” stalls** (Fig. 3). For 22-layer, both converge but He init reduces error earlier.
- **ImageNet headline results (Abstract):**
  - Single-model **top-5 5.71%**
  - Multi-model **top-5 4.94%** (vs GoogLeNet 6.66%); surpasses reported human 5.1%.
- **Training defaults mentioned (Sec. 3):** weight decay **0.0005**, momentum **0.9**, dropout **50%** in first two FC layers, batch size **128**, LR schedule **1e-2 → 1e-3 → 1e-4** when plateau, ~**80 epochs**.

</details>

### 📖 tf.keras.optimizers.Adam (TensorFlow/Keras v2.16.1)
**Reference Doc** · [source](https://www.tensorflow.org/api_docs/python/tf/keras/optimizers/Adam)

*Exact Adam constructor parameters + defaults (lr, betas, epsilon, amsgrad, weight_decay, clipping, EMA, loss scaling, grad accumulation)*

<details>
<summary>Key content</summary>

- **What Adam is (per Kingma et al., 2014):** SGD method using adaptive estimates of **1st and 2nd moments**; described as computationally efficient, low memory, invariant to diagonal rescaling of gradients, suited to large data/parameter problems.
- **Constructor + defaults (TensorFlow 2.16.1):**  
  `tf.keras.optimizers.Adam(learning_rate=0.001, beta_1=0.9, beta_2=0.999, epsilon=1e-07, amsgrad=False, weight_decay=None, clipnorm=None, clipvalue=None, global_clipnorm=None, use_ema=False, ema_momentum=0.99, ema_overwrite_frequency=None, loss_scale_factor=None, gradient_accumulation_steps=None, name='adam', **kwargs)`
- **EMA procedure (when `use_ema=True`):**  
  **Eq. 1 (EMA update):** `new_average = ema_momentum * old_average + (1 - ema_momentum) * current_variable_value`  
  - `ema_overwrite_frequency`: every N steps, overwrite model variables with moving average.  
  - If `None`: no mid-training overwrite; call `optimizer.finalize_variable_values()` at end (built-in `fit()` does this automatically after last epoch).
- **Gradient accumulation (when `gradient_accumulation_steps=int`):** update model/optimizer variables **every N steps** using the **average gradient** since last update (reduces gradient noise for very small batch sizes).
- **Loss scaling (mixed precision):** if `loss_scale_factor` is float: multiply loss by factor before gradients; multiply gradients by inverse factor before applying updates.

</details>

### 📖 tf.keras.optimizers.AdamW (TensorFlow/Keras v2.16.1)
**Reference Doc** · [source](https://www.tensorflow.org/api_docs/python/tf/keras/optimizers/AdamW)

*Exact defaults + parameter semantics for AdamW (decoupled weight decay), incl. clipping, EMA, loss scaling, gradient accumulation, and excluding vars from weight decay.*

<details>
<summary>Key content</summary>

- **Constructor + defaults (API signature):**  
  `tf.keras.optimizers.AdamW(learning_rate=0.001, weight_decay=0.004, beta_1=0.9, beta_2=0.999, epsilon=1e-07, amsgrad=False, clipnorm=None, clipvalue=None, global_clipnorm=None, use_ema=False, ema_momentum=0.99, ema_overwrite_frequency=None, loss_scale_factor=None, gradient_accumulation_steps=None, name='adamw', **kwargs)`
- **Algorithm identity / rationale:** AdamW = Adam (adaptive first/second moment estimates) **plus decoupled weight decay** per *Decoupled Weight Decay Regularization* (Loshchilov & Hutter et al., 2019). Adam described as computationally efficient, low memory, invariant to diagonal rescaling of gradients, suited to large data/parameter problems (Kingma et al., 2014).
- **EMA procedure (when `use_ema=True`):** maintains moving average of model weights:  
  **Eq. (EMA-1)** `new_average = ema_momentum * old_average + (1 - ema_momentum) * current_variable_value`  
  Defaults: `ema_momentum=0.99`.  
  `ema_overwrite_frequency`: every N steps overwrite model vars with moving average; if `None`, no mid-training overwrite; call `optimizer.finalize_variable_values()` at end (built-in `fit()` does this automatically after last epoch).
- **Gradient accumulation (`gradient_accumulation_steps=int`):** update model/optimizer variables every N steps using the **average** gradient since last update.
- **Mixed precision support (`loss_scale_factor`):** if float, multiply loss by factor before gradients; multiply gradients by inverse factor before updating.
- **Weight decay exclusions:** call `exclude_from_weight_decay(var_list=None, var_names=None)` **before** optimizer `build()`. `var_names` matches substrings (e.g., `['bias']` excludes all bias variables).
- **AMSGrad toggle:** `amsgrad=False` by default (Reddi et al., 2018 reference).

</details>

### 📋 # Source: https://docs.pytorch.org/docs/stable/generated/torch.nn.BatchNorm2d.html
**Source** · 

### 🔍 Tail-utilization optimizations for ads model inference (Meta)
**Explainer** · [source](https://engineering.fb.com/2024/07/10/production-engineering/tail-utilization-ads-inference-meta/)

*Production metrics: timeout failures ↓ ~2/3, same resources → ~35% more work, p99 latency ↓ ~1/2 via tail-utilization optimizations.*

<details>
<summary>Key content</summary>

- **Definition (tail utilization):** utilization level of the **top 5% of servers** when ranked by utilization (i.e., 95th-percentile server utilization across fleet).
- **Empirical results (fleet-level):**
  - **Timeout error rate reduced by ~two-thirds**.
  - **Compute footprint delivered ~35% more work** with **no additional resources** (absorbed up to **35% load increase**).
  - **p99 latency cut by ~half**.
- **System context/workflow:**
  - Client request → ads core services → **model inference service**; one client request often triggers **multiple model inferences** (experiments/page type/ad attributes).
  - Service is **sharded**: each **model = shard**; multiple models can be hosted on one job host.
  - Uses **ServiceRouter** (service discovery + load balancing) and **Shard Manager** (shard scaling + placement across heterogeneous hardware).
- **Load balancing approaches:**
  - **Routing LB:** balance across replicas of a model (ServiceRouter).
  - **Placement LB:** move replicas across hosts to tighten utilization distribution (Shard Manager tuning: **load bands, thresholds, balancing frequency**).
- **Key procedures/algorithms & rationale:**
  - **Power of Two Choices** randomized LB using **polling** for fresh load (extra hop negligible for inference requests **>10s of ms**); avoids stale-load randomness from load-header.
  - **Per-model load counter** (instead of host-level outstanding requests) to align assumptions of **ReplicaEstimator + Shard Manager** (replicas should see similar load); tightened replica load distribution.
  - Preferred load counter: **“Outstanding examples CPU”** = estimated total CPU time of active requests, **normalized by #cores**.
  - **Memory bandwidth-aware placement:** memory latency rises **exponentially at ~65–70% utilization** → CPU “spikes” were stalls; treat memory bandwidth as a placement resource.
  - **Snapshot transition budget:** only transition to new model snapshot when utilization below threshold; trade-off: snapshot staleness vs failures; **fast scale-down old snapshots** to reduce staleness overhead.
  - **Cross-tier balancing:** route by **compute capacity** (not host count) + feedback controller to adjust traffic % across hardware tiers/pools.
  - **Predictive replica estimation:** forecast resource usage up to **2 hours ahead** to reduce peak-period failures vs reactive scaling.

</details>

---

## Related Topics

- [[topics/word-embeddings|Word Embeddings]]
- [[topics/optimization-algorithms|Optimization Algorithms]]
- [[topics/cnns|CNNs]]
