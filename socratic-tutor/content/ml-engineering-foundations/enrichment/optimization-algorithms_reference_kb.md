## Core Definitions

**Stochastic Gradient Descent (SGD)**  
As Ruder explains, gradient descent minimizes an objective \(J(\theta)\) by updating parameters \(\theta\) in the opposite direction of the gradient \(\nabla_\theta J(\theta)\); in *stochastic* settings the gradient is estimated from a minibatch, trading gradient accuracy for faster updates. The **learning rate** \(\eta\) sets the step size of each update and strongly affects convergence behavior. (Ruder, “An overview of gradient descent optimization algorithms”)

**Momentum (SGD with momentum)**  
Momentum is an SGD variant that maintains a running “velocity” (an exponentially decayed accumulation of past gradients) so updates have inertia: it tends to accelerate progress along consistent directions and damp oscillations in directions where gradients change sign frequently. (Ruder)

**Adam (Adaptive Moment Estimation)**  
Kingma & Ba define Adam as a first-order stochastic optimization method that uses adaptive estimates of **lower-order moments** of the gradients—specifically running estimates of the **first moment** (mean) and **second moment** (uncentered variance)—to produce per-parameter adaptive step sizes. They emphasize it is computationally efficient, has little memory overhead, is invariant to diagonal rescaling of gradients, and is well-suited to large data/parameter problems and noisy/sparse gradients. (Kingma & Ba, 2014; also echoed in TensorFlow/Keras Adam docs)

**AMSGrad (Adam variant)**  
Keras exposes `amsgrad` as a boolean option for Adam/AdamW; it refers to the AMSGrad variant (Reddi et al., 2018 is cited in the Keras AdamW card) intended to address convergence issues by modifying how the second-moment estimate is used. (TensorFlow/Keras Adam & AdamW API docs)

**Weight decay**  
Weight decay is a regularization mechanism that shrinks weights during optimization. In PyTorch Adam, `weight_decay` is described as an L2 penalty parameter, and PyTorch additionally offers `decoupled_weight_decay=True` to make Adam behave like AdamW (so weight decay does not accumulate in the momentum/variance). In Keras, Adam has `weight_decay=None` (optional), while AdamW is explicitly “Adam + decoupled weight decay.” (PyTorch Adam docs; TensorFlow/Keras Adam & AdamW docs)

**AdamW (Adam with decoupled weight decay)**  
TensorFlow/Keras describes AdamW as Adam (adaptive first/second moment estimates) plus **decoupled weight decay** per “Decoupled Weight Decay Regularization” (Loshchilov & Hutter, 2019 as cited in the Keras AdamW card). “Decoupled” means the decay is applied separately from the gradient-based update, rather than being folded into the gradient statistics. (TensorFlow/Keras AdamW docs)

**Learning rate schedule (warmup + cosine decay as common examples)**  
A learning rate schedule changes the learning rate over training. In the provided sources, two concrete production-style examples are: (1) Megatron-LM uses **3k warmup iterations** then **single-cycle cosine decay** (to a minimum LR) for the remaining iterations; (2) PyTorch’s Llama2-7B FSDP example warms up to a peak LR then cosine decays to a lower final LR over the token budget. (Megatron-LM paper; PyTorch “Maximizing Training” blog)

---

## Key Formulas & Empirical Results

### Adam / AdamW implementation defaults (TensorFlow/Keras v2.16.1)

**Keras Adam constructor + defaults** (exact signature)  
`tf.keras.optimizers.Adam(learning_rate=0.001, beta_1=0.9, beta_2=0.999, epsilon=1e-07, amsgrad=False, weight_decay=None, clipnorm=None, clipvalue=None, global_clipnorm=None, use_ema=False, ema_momentum=0.99, ema_overwrite_frequency=None, loss_scale_factor=None, gradient_accumulation_steps=None, name='adam', **kwargs)`  
Supports: gradient clipping (`clipnorm`, `clipvalue`, `global_clipnorm`), EMA of weights, loss scaling, gradient accumulation. (TensorFlow/Keras Adam API card)

**Keras AdamW constructor + defaults** (exact signature)  
`tf.keras.optimizers.AdamW(learning_rate=0.001, weight_decay=0.004, beta_1=0.9, beta_2=0.999, epsilon=1e-07, amsgrad=False, clipnorm=None, clipvalue=None, global_clipnorm=None, use_ema=False, ema_momentum=0.99, ema_overwrite_frequency=None, loss_scale_factor=None, gradient_accumulation_steps=None, name='adamw', **kwargs)`  
Also supports excluding variables from weight decay via `exclude_from_weight_decay(var_list=None, var_names=None)` (call before `build()`). (TensorFlow/Keras AdamW API card)

### EMA (Exponential Moving Average) of weights (Keras)

**EMA update equation (Keras docs)**  
`new_average = ema_momentum * old_average + (1 - ema_momentum) * current_variable_value`  
- Default `ema_momentum=0.99`.  
- `ema_overwrite_frequency`: overwrite model variables with EMA every N steps; if `None`, no mid-training overwrite; call `optimizer.finalize_variable_values()` at end (Keras `fit()` does this automatically after last epoch). (TensorFlow/Keras Adam & AdamW API cards)

### Gradient accumulation (Keras)

If `gradient_accumulation_steps=N`, Keras updates model/optimizer variables **every N steps** using the **average gradient** since the last update. (TensorFlow/Keras Adam & AdamW API cards)

### PyTorch Adam defaults (PyTorch 2.11)

`torch.optim.Adam(params, lr=0.001, betas=(0.9, 0.999), eps=1e-08, weight_decay=0, amsgrad=False, ..., decoupled_weight_decay=False)`  
- `decoupled_weight_decay=True` makes it equivalent to AdamW (and “will not accumulate weight decay in the momentum nor variance”). (PyTorch Adam docs)

### Mixed precision loss scaling (FP16) — key numeric limits + procedure

From the mixed precision paper (Micikevicius et al., 2018):  
- FP16 max normalized: **65,504**; min normalized: **\(2^{-14}\approx 6.10\times 10^{-5}\)**; min denormal: **\(2^{-24}\approx 5.96\times 10^{-8}\)**.  
- Loss scaling: scale loss by \(S\): \(L' = S\cdot L\); gradients scale by \(S\); **unscale before update**: \(g = g'/S\).  
- Dynamic scaling: if Inf/NaN in grads → reduce \(S\) and skip update; if no overflow for \(N\) iterations (example \(N=2000\)) → increase \(S\). (arXiv:1710.03740)

### BFLOAT16 vs FP32 parity (empirical)

BF16 keeps FP32-like exponent range (Table 1 in BF16 paper), often avoiding FP16-style loss scaling. Empirical parity examples:  
- ResNet-50 ImageNet: FP32 **74.7/92.0** top1/top5 vs BF16 **74.7/92.0**.  
- GNMT DE→EN BLEU: **29.3 vs 29.3** (FP32 vs BF16). (arXiv:1905.12322 / PDF card)

### Concrete LR schedule + AdamW hyperparams from large-scale training examples

**Megatron-LM (GPT-2-like) hyperparams**  
- Optimizer: **AdamW**, weight decay \(\lambda=0.01\)  
- LR: **1.5e-4**, **3k warmup** iterations, **single-cycle cosine decay** over remaining **297k** iterations to min LR **1e-5**. (arXiv:1909.08053 card)

**PyTorch production FSDP (Llama2-7B) hyperparams**  
- Optimizer: **AdamW (32-bit)**, \(\beta_1=0.9\), \(\beta_2=0.95\), weight decay **0.1**  
- LR schedule: warmup to **3e-4**, cosine decay to **3e-5** over **2T tokens** (ending LR **3e-5**). (PyTorch “Maximizing Training” blog card)

---

## How It Works

### SGD (mechanics the tutor can walk through)
1. Choose minibatch \(B\); compute loss \(J(\theta;B)\).
2. Compute gradient estimate \(g=\nabla_\theta J(\theta;B)\).
3. Update parameters: \(\theta \leftarrow \theta - \eta g\).  
   - \(\eta\) is the learning rate controlling step size. (Ruder)

### Momentum (high-level mechanics)
1. Maintain a velocity-like accumulator of gradients (exponentially decayed).
2. Update parameters using this accumulator rather than raw gradient, which smooths noise and accelerates along consistent directions. (Ruder)

### Adam / AdamW in practice (what happens each step)
Use this when a student asks “what does Adam actually store and do per parameter?”

1. **State per parameter**: Adam maintains running estimates of gradient mean (1st moment) and gradient-square mean (2nd moment). (Kingma & Ba; Keras Adam description)
2. **Compute gradient** \(g_t\) on current minibatch.
3. **Update moment estimates** (conceptually):  
   - 1st moment tracks average direction; 2nd moment tracks typical magnitude/variance. (Kingma & Ba)
4. **Compute per-parameter adaptive step**: parameters with consistently large gradient magnitudes get smaller effective steps; small/sparse gradients get relatively larger steps. (Kingma & Ba; Ruder)
5. **Apply update** with global `learning_rate` and numerical stabilizer `epsilon`.  
   - Keras exposes `beta_1`, `beta_2`, `epsilon`. (Keras Adam API)
6. **Weight decay**:
   - **Adam (Keras)**: optional `weight_decay` (if set). (Keras Adam API)
   - **AdamW**: apply **decoupled** weight decay (separate from gradient moments). (Keras AdamW; PyTorch `decoupled_weight_decay=True`)

### Keras extras often confused with “Adam itself”
**EMA of weights (`use_ema=True`)**  
- Every step, update EMA shadow weights using:  
  `new_average = ema_momentum * old_average + (1 - ema_momentum) * current_variable_value`  
- Optionally overwrite live weights every `ema_overwrite_frequency` steps; otherwise finalize at end. (Keras Adam/AdamW)

**Gradient accumulation (`gradient_accumulation_steps=N`)**  
- Accumulate gradients for N steps; apply update every N steps using the **average** gradient. (Keras Adam/AdamW)

**Loss scaling (`loss_scale_factor`)**  
- Multiply loss by factor before gradient computation; multiply gradients by inverse factor before applying updates. (Keras Adam API)

### PyTorch AMP (canonical order; common debugging hotspot)
When using `torch.autocast` + `GradScaler` (PyTorch AMP examples):
1. `optimizer.zero_grad()`
2. `with autocast(...): output = model(input); loss = loss_fn(output, target)`
3. `scaler.scale(loss).backward()`
4. (Optional) `scaler.unscale_(optimizer)` then clip grads
5. `scaler.step(optimizer)` (skips step if inf/NaN)
6. `scaler.update()` (PyTorch AMP examples + AMP docs)

---

## Teaching Approaches

### Intuitive (no math): “Why Adam feels faster than SGD”
- SGD uses one global step size for everything; if some parameters have tiny gradients and others have huge gradients, one learning rate is a compromise.
- Adam keeps a memory of (a) the typical direction (momentum-like) and (b) the typical scale of gradients per parameter, then automatically adjusts step sizes so each parameter moves at a more appropriate rate. (Kingma & Ba; Ruder)

### Technical (with math emphasis, but keep it source-grounded)
- Adam uses adaptive estimates of **first and second moments** of gradients (Kingma & Ba).  
- The tutor can frame it as: “track mean and variance of gradients per parameter; normalize updates by the second-moment estimate; stabilize with \(\epsilon\); use \(\beta_1,\beta_2\) to control smoothing.” (Keras Adam parameters; Kingma & Ba abstract-level description)

### Analogy-based: “Cruise control + traction control”
- Momentum is like cruise control: it keeps you moving in a consistent direction even if the road (minibatch noise) is bumpy.
- Adam adds traction control: if a wheel (parameter) is slipping (large, noisy gradients), it reduces power (effective step); if it’s barely moving (small gradients), it gives it more. (Ruder + Adam moment intuition from Kingma & Ba)

---

## Common Misconceptions (required)

1. **“Adam automatically finds the best learning rate, so I don’t need to tune LR.”**  
   - **Why wrong:** Adam adapts *relative* step sizes per parameter using moment estimates, but still multiplies by a global `learning_rate` (e.g., Keras default `learning_rate=0.001`; PyTorch default `lr=1e-3`).  
   - **Correct model:** Adam reduces sensitivity to LR, but LR remains a primary knob; schedules (warmup/cosine) are still used in large-scale training (Megatron-LM; PyTorch FSDP blog).

2. **“Weight decay in Adam is always the same as L2 regularization.”**  
   - **Why wrong:** PyTorch explicitly distinguishes classic `weight_decay` (L2 penalty) from **decoupled weight decay** (`decoupled_weight_decay=True`, AdamW behavior), which “will not accumulate weight decay in the momentum nor variance.” Keras similarly separates Adam vs AdamW.  
   - **Correct model:** If you want AdamW-style behavior, use AdamW (Keras) or `decoupled_weight_decay=True` (PyTorch Adam) so decay is applied separately from Adam’s moment tracking. (PyTorch Adam docs; Keras AdamW docs)

3. **“Momentum in BatchNorm is the same as optimizer momentum.”**  
   - **Why wrong:** PyTorch BatchNorm2d warns its `momentum` is for running-stat updates and uses: \(\hat x^{new}=(1-\text{momentum})\hat x + \text{momentum} \, x_t\), which is not the optimizer’s momentum concept.  
   - **Correct model:** Optimizer momentum accumulates gradients to shape parameter updates; BatchNorm momentum controls exponential averaging of running mean/variance buffers. (PyTorch BatchNorm2d docs)

4. **“Mixed precision just works; loss scaling is optional and doesn’t affect anything.”**  
   - **Why wrong:** FP16 has limited range; gradients can underflow to 0. The mixed precision paper gives FP16 numeric limits and shows some models (e.g., SSD) “does not train” without scaling but trains with scaling (e.g., \(S=8\)).  
   - **Correct model:** With FP16, use loss scaling (often dynamic via `GradScaler`) and unscale before clipping/step. BF16 often avoids this due to FP32-like exponent range. (arXiv:1710.03740; arXiv:1905.12322; PyTorch AMP docs)

5. **“Gradient accumulation is the same as increasing batch size with no side effects.”**  
   - **Why wrong:** Accumulation changes *when* optimizer state updates happen (e.g., Keras updates every N steps using average gradient). This interacts with schedules (step-based warmup/decay) and any per-step behaviors (EMA overwrite frequency, etc.).  
   - **Correct model:** Accumulation approximates a larger batch gradient but keeps optimizer updates less frequent; treat “step” carefully in schedules and EMA settings. (Keras gradient accumulation; PyTorch AMP accumulation notes)

---

## Worked Examples

### Example 1 — Keras: Adam vs AdamW + excluding biases from weight decay
```python
import tensorflow as tf

model = tf.keras.Sequential([
    tf.keras.layers.Dense(64, activation="relu"),
    tf.keras.layers.Dense(10)
])

# Adam defaults (TF 2.16.1): lr=1e-3, beta_1=0.9, beta_2=0.999, epsilon=1e-7
opt_adam = tf.keras.optimizers.Adam()

# AdamW defaults (TF 2.16.1): lr=1e-3, weight_decay=0.004, beta_1=0.9, beta_2=0.999, epsilon=1e-7
opt_adamw = tf.keras.optimizers.AdamW()

# Exclude biases (and commonly norm params) from weight decay by name substring
opt_adamw.exclude_from_weight_decay(var_names=["bias"])

model.compile(optimizer=opt_adamw,
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True))
```
Tutor notes:
- Quote defaults directly from the Keras Adam/AdamW signatures.
- Emphasize `exclude_from_weight_decay(...)` must be called **before** optimizer `build()` (Keras AdamW card).

### Example 2 — PyTorch: Adam configured as AdamW + AMP-safe step order
```python
import torch
from torch import nn

model = nn.Sequential(nn.Linear(100, 64), nn.ReLU(), nn.Linear(64, 10)).cuda()
optimizer = torch.optim.Adam(
    model.parameters(),
    lr=1e-3,                 # PyTorch Adam default
    betas=(0.9, 0.999),       # default
    eps=1e-8,                 # default
    weight_decay=0.1,
    decoupled_weight_decay=True  # makes it equivalent to AdamW per docs
)

scaler = torch.amp.GradScaler("cuda")

for x, y in loader:
    x, y = x.cuda(), y.cuda()
    optimizer.zero_grad(set_to_none=True)

    with torch.autocast("cuda", dtype=torch.float16):
        logits = model(x)
        loss = nn.CrossEntropyLoss()(logits, y)

    scaler.scale(loss).backward()

    # If you clip, unscale first (AMP examples)
    scaler.unscale_(optimizer)
    torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)

    scaler.step(optimizer)
    scaler.update()
```
Tutor notes:
- `decoupled_weight_decay=True` is the precise PyTorch switch that makes Adam behave like AdamW. (PyTorch Adam docs)
- The unscale→clip→step ordering is from PyTorch AMP examples. (AMP examples card)

---

## Comparisons & Trade-offs

| Choice | What it changes | Pros | Cons / gotchas | When to choose (from sources) |
|---|---|---|---|---|
| **SGD** | Single global LR step on gradient estimate | Simple; baseline | Sensitive to LR; noisy minibatch gradients | Use as conceptual baseline (Ruder; Karpathy micrograd) |
| **Momentum** | Adds running gradient accumulator | Faster along consistent directions; less oscillation | Still one global LR; momentum hyperparam matters | When SGD is slow/oscillatory (Ruder) |
| **Adam** | Adaptive per-parameter steps via 1st/2nd moment estimates | Efficient; low memory; good for noisy/sparse gradients; less tuning | Still needs LR tuning; weight decay semantics can be confusing | Default go-to optimizer in many deep learning setups (Kingma & Ba; Keras/PyTorch defaults) |
| **AdamW** | Decoupled weight decay from Adam moments | Cleaner regularization behavior; widely used in large-scale training | Must set weight_decay appropriately; exclude biases/norm often desired | Used in Megatron-LM and PyTorch FSDP examples with warmup+cosine schedules (Megatron-LM; PyTorch blog) |

Additional note for tutors: large-scale training examples in the sources overwhelmingly pair **AdamW** with **warmup + cosine decay** schedules (Megatron-LM; PyTorch “Maximizing Training”).

---

## Prerequisite Connections

- **Gradients / backpropagation**: Optimizers update parameters using \(\nabla_\theta J(\theta)\); if a student can’t interpret “gradient,” Adam’s moment estimates won’t land. (Ruder; Karpathy micrograd context)
- **Learning rate as step size**: Adam still multiplies by a global LR; schedules are defined in terms of LR over steps/tokens. (Keras/PyTorch defaults; Megatron-LM/PyTorch schedules)
- **Regularization basics (L2 vs weight decay)**: Needed to understand why AdamW is distinct and why “decoupled” matters. (PyTorch Adam docs; Keras AdamW docs)
- **Numerical precision / overflow-underflow**: Needed when discussing AMP, loss scaling, and why BF16 differs from FP16. (arXiv:1710.03740; arXiv:1905.12322; PyTorch AMP docs)

---

## Socratic Question Bank

1. **If Adam adapts learning rates per parameter, why do we still specify a global `learning_rate`?**  
   *Good answer:* Because Adam’s per-parameter scaling is multiplied by a global LR; defaults exist (e.g., 1e-3) and schedules still matter (warmup/cosine in large runs).

2. **What information do the “first moment” and “second moment” estimates capture about gradients?**  
   *Good answer:* First moment ≈ average direction (momentum-like); second moment ≈ typical squared magnitude/variance used to normalize step sizes.

3. **How is AdamW’s weight decay different from “L2 penalty inside the loss” in Adam?**  
   *Good answer:* Decoupled weight decay is applied separately and does not get mixed into Adam’s momentum/variance statistics (PyTorch `decoupled_weight_decay` wording; Keras AdamW definition).

4. **If you turn on gradient accumulation for N steps, what changes about “one optimizer step”?**  
   *Good answer:* Updates happen every N minibatches using the average gradient; step-based schedules/EMA overwrite frequency should be interpreted accordingly (Keras accumulation semantics).

5. **In AMP training, why must you unscale gradients before clipping?**  
   *Good answer:* Clipping thresholds would be effectively scaled otherwise; PyTorch AMP examples specify `unscale_` before inspecting/modifying `.grad`.

6. **Why might BF16 not need loss scaling while FP16 often does?**  
   *Good answer:* BF16 keeps FP32-like exponent range (dynamic range), reducing underflow/overflow issues that motivate loss scaling in FP16.

7. **What does `epsilon` do in Adam implementations? Where do you see it exposed?**  
   *Good answer:* It’s a numerical stability term in the denominator; exposed as `epsilon` in Keras (default 1e-7) and `eps` in PyTorch (default 1e-8).

---

## Likely Student Questions

**Q: What are the default Adam hyperparameters in Keras?**  
→ **A:** `learning_rate=0.001, beta_1=0.9, beta_2=0.999, epsilon=1e-07, amsgrad=False, weight_decay=None` (plus optional clipping/EMA/loss scaling/grad accumulation args). (https://www.tensorflow.org/api_docs/python/tf/keras/optimizers/Adam)

**Q: What are the default AdamW hyperparameters in Keras?**  
→ **A:** `learning_rate=0.001, weight_decay=0.004, beta_1=0.9, beta_2=0.999, epsilon=1e-07, amsgrad=False` (plus clipping/EMA/loss scaling/grad accumulation). (https://www.tensorflow.org/api_docs/python/tf/keras/optimizers/AdamW)

**Q: How do I exclude biases from weight decay in Keras AdamW?**  
→ **A:** Call `exclude_from_weight_decay(var_names=['bias'])` (substring match) **before** optimizer `build()`. (Keras AdamW API card)

**Q: In PyTorch, how do I make `torch.optim.Adam` behave like AdamW?**  
→ **A:** Set `decoupled_weight_decay=True`; PyTorch docs state this makes it “equivalent to AdamW” and prevents weight decay from accumulating in momentum/variance. (https://pytorch.org/docs/stable/generated/torch.optim.Adam.html)

**Q: What’s the EMA update rule in Keras optimizers?**  
→ **A:** `new_average = ema_momentum * old_average + (1 - ema_momentum) * current_variable_value`; default `ema_momentum=0.99`. (Keras Adam/AdamW API cards)

**Q: What does `gradient_accumulation_steps` do in Keras Adam/AdamW?**  
→ **A:** It updates model/optimizer variables every N steps using the **average gradient** since the last update. (Keras Adam/AdamW API cards)

**Q: Why does FP16 mixed precision need loss scaling?**  
→ **A:** FP16 has limited range (max 65504; min normalized \(2^{-14}\)); small gradients can underflow to 0. Loss scaling multiplies the loss by \(S\) so gradients scale up, then unscales before the optimizer update. (https://arxiv.org/abs/1710.03740)

**Q: What LR schedules and AdamW settings are used in real large-scale training examples here?**  
→ **A:** Megatron-LM: AdamW, weight decay 0.01, LR 1.5e-4, 3k warmup iters, cosine decay to 1e-5. PyTorch FSDP Llama2-7B: AdamW (32-bit), betas (0.9, 0.95), weight decay 0.1, warmup to 3e-4 then cosine decay to 3e-5 over 2T tokens. (Megatron-LM card; PyTorch “Maximizing Training” card)

---

## Available Resources

### Videos
- [The spelled-out intro to neural networks and backpropagation: building micrograd](https://youtube.com/watch?v=VMj-3S1tku0) — Surface when: the student needs a concrete feel for SGD/momentum and “what training loops actually do” from scratch.

### Articles & Tutorials
- [An overview of gradient descent optimization algorithms (Sebastian Ruder)](https://www.ruder.io/optimizing-gradient-descent/) — Surface when: the student asks for a unified comparison of SGD, momentum, RMSProp, Adam, and schedules with intuition.
- [micrograd (Karpathy) GitHub repo](https://github.com/karpathy/micrograd) — Surface when: the student wants minimal code to inspect/modify an optimizer and see gradients flow.

---

## Key Sources

- [tf.keras.optimizers.Adam](https://www.tensorflow.org/api_docs/python/tf/keras/optimizers/Adam) — authoritative Keras defaults and knobs (epsilon/betas/EMA/clipping/accumulation).
- [tf.keras.optimizers.AdamW](https://www.tensorflow.org/api_docs/python/tf/keras/optimizers/AdamW) — authoritative decoupled weight decay defaults + exclusion mechanism.
- [torch.optim.Adam](https://pytorch.org/docs/stable/generated/torch.optim.Adam.html) — authoritative PyTorch semantics including `decoupled_weight_decay`.
- [Adam: A Method for Stochastic Optimization (Kingma & Ba, 2014)](https://arxiv.org/abs/1412.6980) — primary definition/claims for Adam (moments, efficiency, invariances).
- [Mixed Precision Training (Micikevicius et al., 2018)](https://arxiv.org/abs/1710.03740) — numeric limits + loss scaling procedure that frequently interacts with optimizer behavior.