## Core Definitions

**Backpropagation**: Rumelhart, Hinton & Williams (1986) describe back-propagation as a learning procedure that *repeatedly adjusts the weights of the connections in the network so as to minimize a measure of the difference between the actual output vector of the net and the desired output vector*; the key mechanism is propagating “errors” backward through the network to compute how each weight should change to reduce the loss. (Rumelhart et al., 1986)

**Gradient descent**: In the setup described by Rumelhart et al. (1986), learning proceeds by repeatedly adjusting weights to minimize a loss; operationally, gradient descent is the iterative optimization method that updates parameters in the direction that reduces the loss, using the gradient of the loss with respect to parameters (computed efficiently by backpropagation). (Rumelhart et al., 1986; Glorot & Bengio, 2010 training setup uses SGD)

**Chain rule (in neural nets)**: Glorot & Bengio (2010) explicitly express backpropagation through layers as repeated application of the chain rule: gradients at one layer are obtained by multiplying by the next layer’s weights and the derivative of the nonlinearity, e.g. \(\frac{\partial C}{\partial s_i^k}=f'(s_i^k)\, W_{i+1}^{k,\bullet}\frac{\partial C}{\partial s_{i+1}}\). This is the core “chain” that makes gradients shrink or grow with depth depending on Jacobians. (Glorot & Bengio, 2010)

**Loss function**: Glorot & Bengio (2010) use negative log-likelihood for classification, written as \(-\log P(y|x)\), and note that cross-entropy/log-likelihood can show fewer training plateaus than quadratic loss in deep nets. (Glorot & Bengio, 2010)

---

## Key Formulas & Empirical Results

### Backprop layerwise gradient identities (Glorot & Bengio, 2010)
**Forward notation** (their setup): \(s_i=z_iW_i+b_i,\quad z_{i+1}=f(s_i)\)

**Backprop to pre-activation** (Eq. 2):
\[
\frac{\partial C}{\partial s_i^k}=f'(s_i^k)\, W_{i+1}^{k,\bullet}\frac{\partial C}{\partial s_{i+1}}
\]
- \(C\): cost/loss  
- \(s_i^k\): pre-activation of unit \(k\) at layer \(i\)  
- \(f'\): derivative of activation function  
- \(W_{i+1}^{k,\bullet}\): row (or appropriate slice) of next layer weights mapping from layer \(i\) to \(i+1\)  
**Claim supported**: gradients propagate backward by repeated multiplication with weight matrices and activation derivatives; this is where vanishing/exploding gradients arise.

**Gradient w.r.t. weights** (Eq. 3):
\[
\frac{\partial C}{\partial w_i^{l,k}}=z_i^l\frac{\partial C}{\partial s_i^k}
\]
- \(w_i^{l,k}\): weight from unit \(l\) in layer \(i\) input \(z_i\) to unit \(k\) pre-activation \(s_i\)  
- \(z_i^l\): activation feeding into that weight  
**Claim supported**: weight gradients are “input activation × backpropagated error signal”.

### Initialization formulas tied to gradient flow (Glorot & Bengio, 2010)
**Variance compromise target** (Eqs. 10–12):
- Want both forward and backward variance preserved:
  - \(n_i\mathrm{Var}[W_i]\approx 1\)
  - \(n_{i+1}\mathrm{Var}[W_i]\approx 1\)
- Compromise:
\[
\mathrm{Var}[W_i]=\frac{2}{n_i+n_{i+1}}
\]
where \(n_i\)=fan-in, \(n_{i+1}\)=fan-out.

**Xavier/Glorot uniform init** (Eq. 16):
\[
W\sim U\left[-\frac{\sqrt{6}}{\sqrt{n_j+n_{j+1}}},\frac{\sqrt{6}}{\sqrt{n_j+n_{j+1}}}\right]
\]
**Claim supported**: keeping layer Jacobians better conditioned (singular values closer to 1) improves gradient flow and convergence.

**Empirical Jacobian conditioning**: Glorot & Bengio report average Jacobian singular value ratio ≈ **0.8** with normalized/Xavier init vs **0.5** with “standard” init (Section 4.2.2).  
**Claim supported**: normalized init improves gradient propagation.

### “Standard” baseline init used in experiments (Glorot & Bengio, 2010)
(Eq. 1):
\[
W_{ij}\sim U\left[-\frac{1}{\sqrt{n}},\frac{1}{\sqrt{n}}\right],\quad n=\text{fan-in}
\]
Biases initialized to **0** (Section 2.3).

### Training setup numbers (Glorot & Bengio, 2010)
- Depth: **1–5 hidden layers**, **1000 units/layer**, **softmax** output  
- Loss: **negative log-likelihood** \(-\log P(y|x)\)  
- Optimization: **SGD**, minibatch size **10**, learning rate tuned via validation after **5 million updates** (Section 2.3)

### Saturation/plateau observations (Glorot & Bengio, 2010)
- With sigmoid + random init, top hidden layer saturates near **0**, causing slow learning/plateaus; in a 4-hidden-layer net it slowly desaturates around **epoch 100**; depth-5 may never escape saturation (Section 3.1).

### He/Kaiming initialization for rectifiers (He et al., 2015)
- Rectifier-aware scaling commonly expressed as:
  - \(\text{std}=\sqrt{2/\hat n_l}\) (fan-in \(\hat n_l\)) (Sec. 2.2)
- Empirical convergence: **30-layer** rectified net converges with this init; **“Xavier” stalls** (Fig. 3 description).  
**Claim supported**: initialization must match activation to maintain signal/gradient scale.

### Adam / AdamW defaults (TensorFlow/Keras API)
From `tf.keras.optimizers.Adam` (v2.16.1):
- `learning_rate=0.001`, `beta_1=0.9`, `beta_2=0.999`, `epsilon=1e-07`, `amsgrad=False`, `weight_decay=None` (plus clipping/EMA/loss scaling/grad accumulation options).  
Source: https://www.tensorflow.org/api_docs/python/tf/keras/optimizers/Adam

From `tf.keras.optimizers.AdamW` (v2.16.1):
- `learning_rate=0.001`, `weight_decay=0.004`, `beta_1=0.9`, `beta_2=0.999`, `epsilon=1e-07`, `amsgrad=False` (plus clipping/EMA/loss scaling/grad accumulation; and `exclude_from_weight_decay(...)`).  
Source: https://www.tensorflow.org/api_docs/python/tf/keras/optimizers/AdamW

---

## How It Works

### Backpropagation through a feedforward network (mechanical steps)
Use Glorot & Bengio (2010) notation: \(s_i=z_iW_i+b_i,\ z_{i+1}=f(s_i)\), loss \(C\).

1. **Forward pass (cache intermediates)**  
   For each layer \(i\):
   - compute pre-activations \(s_i\)
   - compute activations \(z_{i+1}=f(s_i)\)  
   Cache \(z_i\) and \(s_i\) (needed for gradients).

2. **Initialize gradient at output (loss derivative)**  
   Compute \(\frac{\partial C}{\partial s_L}\) (or \(\frac{\partial C}{\partial z_L}\) then convert to \(\frac{\partial C}{\partial s_L}\) via \(f'\)).  
   (Exact form depends on output nonlinearity + loss; Glorot & Bengio use softmax with negative log-likelihood.)

3. **Backward recursion: propagate “error signal” to earlier layers**  
   For each layer \(i\) from last hidden toward first:
   - Apply chain rule (Glorot & Bengio Eq. 2):
     \[
     \frac{\partial C}{\partial s_i^k}=f'(s_i^k)\, W_{i+1}^{k,\bullet}\frac{\partial C}{\partial s_{i+1}}
     \]
   This is the computational heart: multiply by weights and elementwise by \(f'(s_i)\).

4. **Compute parameter gradients at each layer**  
   - Weight gradients (Eq. 3):
     \[
     \frac{\partial C}{\partial w_i^{l,k}}=z_i^l\frac{\partial C}{\partial s_i^k}
     \]
   - Bias gradients follow similarly from \(\partial s_i/\partial b_i = 1\) (not explicitly given in sources, but consistent with \(s_i=z_iW_i+b_i\); if quoting strictly, keep focus on Eq. 2–3).

5. **Optimization step (e.g., SGD)**  
   Glorot & Bengio’s experiments use SGD with minibatch size 10; update weights using the computed gradients, then repeat.

### Why depth causes vanishing/exploding gradients (what to say mid-debug)
- Glorot & Bengio (2010) connect training difficulty to **singular values of layer Jacobians** being far from 1: repeated chain-rule multiplications across layers shrink or blow up gradients.
- With sigmoid/tanh, saturation makes \(f'(s)\) small, further shrinking gradients; they empirically observe saturation and plateaus in deep sigmoid/tanh nets.

---

## Teaching Approaches

### Intuitive (no math)
- Backprop is “credit assignment”: after seeing how wrong the network is, it sends a correction signal backward telling each weight how much it contributed to the error.
- The chain rule is the bookkeeping rule that lets you translate “output error” into “how should this earlier weight change?”
- Deep nets can struggle because each layer can dampen the correction signal (especially if activations saturate), so early layers barely get updated (Glorot & Bengio’s saturation/plateau observations).

### Technical (with math)
- Use Glorot & Bengio’s two identities as the backbone:
  - error signal recursion: \(\partial C/\partial s_i = f'(s_i)\odot (W_{i+1}^\top (\partial C/\partial s_{i+1}))\) (component form is Eq. 2 in the paper)
  - parameter gradient: \(\partial C/\partial W_i = z_i^\top (\partial C/\partial s_i)\) (component form Eq. 3)
- Then connect to conditioning: if Jacobian singular values deviate from 1, repeated multiplication causes vanishing/exploding gradients; Xavier init targets variance preservation via \(\mathrm{Var}[W_i]=2/(n_i+n_{i+1})\).

### Analogy-based
- **Assembly line quality control**: the final inspector (loss) finds defects and sends notes upstream. Each station (layer) forwards the note, scaled by (a) how strongly it influences the next station (weights) and (b) whether it’s operating in a sensitive region (activation derivative). If a station is “stuck” (saturated), it barely responds, so upstream stations don’t learn (Glorot & Bengio’s saturation story).

---

## Common Misconceptions

1. **“Backprop is the same thing as gradient descent.”**  
   - **Why wrong**: Backprop is a *gradient computation method* (efficiently applying the chain rule across layers); gradient descent/SGD is the *parameter update rule* that uses those gradients. Glorot & Bengio explicitly separate gradient computation (Eqs. 2–3) from the SGD training procedure (minibatch size 10, LR tuning).  
   - **Correct model**: Backprop gives \(\nabla_\theta C\); SGD/Adam decides how to step using that gradient.

2. **“Vanishing gradients only happen because the network is ‘too deep’, not because of activations/initialization.”**  
   - **Why wrong**: Glorot & Bengio show sigmoid’s non-zero mean can push upper layers into saturation, producing plateaus; they also tie difficulty to Jacobian singular values and propose Xavier init to keep signals/gradients scaled. He et al. show Xavier can stall for deep rectifier nets while He init converges.  
   - **Correct model**: Depth amplifies whatever scaling each layer introduces; activation derivatives and weight scaling (initialization) determine whether the product shrinks/explodes.

3. **“If a sigmoid unit saturates, it can never recover.”**  
   - **Why wrong**: Glorot & Bengio report saturated units can move out of saturation *slowly*, explaining plateaus; in a 4-hidden-layer sigmoid net, the top layer desaturates around epoch ~100, while deeper nets may not escape.  
   - **Correct model**: Saturation makes gradients tiny, so recovery is possible but very slow; better initialization/nonlinearities reduce time spent saturated.

4. **“Xavier initialization is universally best.”**  
   - **Why wrong**: He et al. (2015) report that for a 30-layer rectified network, rectifier-aware (He) init converges while “Xavier” stalls (their Fig. 3 description).  
   - **Correct model**: Initialization should match activation statistics; Xavier targets tanh/sigmoid-style variance preservation, while He targets rectifiers.

5. **“AdamW is just Adam with L2 regularization.”**  
   - **Why wrong**: The Keras doc explicitly labels AdamW as Adam plus **decoupled weight decay** (Loshchilov & Hutter, 2019 as cited in the API doc).  
   - **Correct model**: AdamW applies weight decay as a separate mechanism from the gradient-based update; in Keras it’s configured via `weight_decay` (default 0.004) and can exclude variables via `exclude_from_weight_decay(...)`.

---

## Worked Examples

### Example 1: Verify backprop gradients on a small compute graph (micrograd)
**Use case**: student asks “what does backprop actually compute?” or “how do I know gradients are correct?”

From the `micrograd` README example (Karpathy’s micrograd repo), run:

```python
from micrograd.engine import Value

a = Value(-4.0)
b = Value(2.0)
c = a + b
d = a * b + b**3
c += c + 1
c += 1 + c + (-a)
d += d * 2 + (b + a).relu()
d += 3 * d + (b - a).relu()
e = c - d
f = e**2
g = f / 2.0
g += 10.0 / f

print(f'{g.data:.4f}')  # 24.7041 in the README
g.backward()
print(f'{a.grad:.4f}')  # 138.8338 in the README
print(f'{b.grad:.4f}')  # 645.5773 in the README
```

**Tutor notes (what to point out)**
- The forward pass builds a DAG of primitive ops (+, *, power, relu, /).
- `backward()` performs reverse-mode autodiff (backprop) over that DAG, accumulating gradients at each node.
- This concretely instantiates the chain rule: each op contributes a local derivative; backprop multiplies and accumulates them along paths.

### Example 2: Initialization choice affects deep training stability (what to reach for)
**Use case**: student asks “why do we care about Xavier/He init?”

- Quote Glorot & Bengio’s Xavier uniform:
  \[
  U\left[-\frac{\sqrt{6}}{\sqrt{n_j+n_{j+1}}},\frac{\sqrt{6}}{\sqrt{n_j+n_{j+1}}}\right]
  \]
  and their motivation: keep Jacobian singular values closer to 1; they report ~0.8 vs ~0.5 average singular value ratio with standard init.
- Then quote He et al.: for a **30-layer** rectified net, He init converges while “Xavier” stalls (Fig. 3 description), motivating activation-aware scaling \(\sqrt{2/\text{fan-in}}\).

(Keep this as a “worked talking example” rather than inventing unsourced training curves.)

---

## Comparisons & Trade-offs

| Topic | Option | What sources say | When to choose |
|---|---|---|---|
| Initialization | **Xavier/Glorot** | \(\mathrm{Var}[W]=2/(n_{in}+n_{out})\); uniform bounds \(\pm \sqrt{6}/\sqrt{n_{in}+n_{out}}\). Motivated by preserving forward/backward variance and better Jacobian conditioning (Glorot & Bengio, 2010). | Common default for tanh/sigmoid-style analyses; when you want variance preservation across fan-in/out per Glorot & Bengio. |
| Initialization | **He/Kaiming** | Rectifier-aware scaling, commonly \(\text{std}=\sqrt{2/\text{fan-in}}\); enables very deep rectified nets; “Xavier stalls” for 30-layer rectified net (He et al., 2015). | Deep ReLU/PReLU-style networks; when rectifiers dominate and you see stalled optimization with Xavier. |
| Optimizer | **SGD (minibatch)** | Glorot & Bengio train with SGD, minibatch size 10, LR tuned via validation after 5M updates (2010). | When teaching the canonical gradient descent loop; when you want simplest dynamics to reason about. |
| Optimizer | **Adam / AdamW** | Keras defaults: Adam lr=0.001, betas (0.9,0.999), eps=1e-7; AdamW adds decoupled weight decay with default weight_decay=0.004 (TF API docs). | When students ask about practical defaults; AdamW when you explicitly want decoupled weight decay and exclusion controls. |

---

## Prerequisite Connections

- **Derivatives & chain rule (single-variable → multistep composition)**: backprop is repeated chain rule application across a composed function (Glorot & Bengio Eq. 2–3 are explicit chain-rule instances).
- **Matrix/vector notation for layers**: understanding \(s=zW+b\) and elementwise nonlinearity \(f\) is needed to parse layerwise gradients (Glorot & Bengio setup).
- **Loss as an objective**: negative log-likelihood / cross-entropy as the scalar objective being minimized (Glorot & Bengio use \(-\log P(y|x)\)).
- **Basic optimization loop**: iterative updates (SGD/Adam) using gradients; distinguishes “compute gradient” vs “apply update” (Rumelhart et al. learning procedure; Glorot & Bengio SGD setup).

---

## Socratic Question Bank

1. **If I change one weight in an early layer, through what sequence of computations does it affect the loss?**  
   *Good answer*: describes forward dependence through \(s_i=z_iW_i+b_i\), then later layers, then loss; recognizes composition.

2. **In Glorot & Bengio’s Eq. 3, why does \(\partial C/\partial w_i^{l,k}\) include \(z_i^l\)? What does that mean intuitively?**  
   *Good answer*: weight’s effect scales with the input activation feeding it; “active inputs create larger gradient contributions.”

3. **What two factors multiply repeatedly as you backprop through many layers, and how can each cause vanishing gradients?**  
   *Good answer*: weight matrices (Jacobian) and activation derivatives \(f'(s)\); saturation makes \(f'\) small; Jacobian singular values < 1 shrink signals.

4. **Why might a deep sigmoid network show a long plateau even if it’s not at a minimum?**  
   *Good answer*: saturation near 0 in upper layers yields tiny gradients; Glorot & Bengio’s observation that saturated units escape slowly.

5. **What problem is Xavier initialization trying to solve, in one sentence tied to a measurable quantity?**  
   *Good answer*: keep forward/backward variance stable / keep Jacobian singular values closer to 1 (Glorot & Bengio).

6. **If Xavier can stall for deep rectifier nets (He et al.), what does that suggest about “one-size-fits-all” initialization?**  
   *Good answer*: initialization must match activation statistics; rectifiers need different variance scaling.

7. **How would you explain the difference between Adam and AdamW using only the Keras API docs?**  
   *Good answer*: AdamW = Adam + decoupled weight decay; Adam has `weight_decay=None` by default; AdamW has `weight_decay=0.004` default and exclusion method.

8. **If a unit is saturated, what would you expect about \(f'(s)\) and therefore \(\partial C/\partial s\)?**  
   *Good answer*: \(f'(s)\) small ⇒ backpropagated gradient shrinks at that unit.

---

## Likely Student Questions

**Q: What exact equations show how gradients propagate backward through layers?**  
→ **A:** Glorot & Bengio (2010) give (Eq. 2) \(\frac{\partial C}{\partial s_i^k}=f'(s_i^k)\, W_{i+1}^{k,\bullet}\frac{\partial C}{\partial s_{i+1}}\) and (Eq. 3) \(\frac{\partial C}{\partial w_i^{l,k}}=z_i^l\frac{\partial C}{\partial s_i^k}\). These are the chain rule in layer form. https://proceedings.mlr.press/v9/glorot10a/glorot10a.pdf

**Q: What loss function did Glorot & Bengio use in their deep net experiments?**  
→ **A:** Negative log-likelihood for softmax classification: \(-\log P(y|x)\) (Section 2.3). https://proceedings.mlr.press/v9/glorot10a/glorot10a.pdf

**Q: What is Xavier/Glorot initialization exactly (the formula)?**  
→ **A:** Glorot & Bengio’s normalized uniform init (Eq. 16) is \(W\sim U\left[-\frac{\sqrt{6}}{\sqrt{n_j+n_{j+1}}},\frac{\sqrt{6}}{\sqrt{n_j+n_{j+1}}}\right]\). https://proceedings.mlr.press/v9/glorot10a/glorot10a.pdf

**Q: Why do deep sigmoid networks get stuck on plateaus?**  
→ **A:** Glorot & Bengio (2010) report that with random init + logistic sigmoid, the top hidden layer can saturate near 0; saturated units move out of saturation only slowly, producing training plateaus; deeper (e.g., 5 hidden layers) may never escape saturation. https://proceedings.mlr.press/v9/glorot10a/glorot10a.pdf and https://proceedings.mlr.press/v9/glorot10a.html

**Q: What’s the practical difference between Xavier and He initialization?**  
→ **A:** He et al. (2015) derive rectifier-aware scaling commonly written as \(\text{std}=\sqrt{2/\text{fan-in}}\) and report that a 30-layer rectified net converges with this init while “Xavier” stalls (Fig. 3 description). https://arxiv.org/abs/1502.01852

**Q: What are the default hyperparameters for Adam in Keras?**  
→ **A:** `tf.keras.optimizers.Adam` defaults: `learning_rate=0.001`, `beta_1=0.9`, `beta_2=0.999`, `epsilon=1e-07`, `amsgrad=False`, `weight_decay=None` (plus optional clipping/EMA/loss scaling/grad accumulation). https://www.tensorflow.org/api_docs/python/tf/keras/optimizers/Adam

**Q: What are the default hyperparameters for AdamW in Keras, and how do I exclude biases from weight decay?**  
→ **A:** `tf.keras.optimizers.AdamW` defaults: `learning_rate=0.001`, `weight_decay=0.004`, `beta_1=0.9`, `beta_2=0.999`, `epsilon=1e-07`, `amsgrad=False`. To exclude variables, call `exclude_from_weight_decay(var_list=None, var_names=None)` before `build()`; `var_names` matches substrings like `['bias']`. https://www.tensorflow.org/api_docs/python/tf/keras/optimizers/AdamW

---

## Available Resources

### Videos
- [The spelled-out intro to neural networks and backpropagation: building micrograd](https://youtube.com/watch?v=VMj-3S1tku0) — Surface when: student asks “can we see backprop implemented from scratch?” or is confused about computational graphs / reverse-mode autodiff.
- [But what is a neural network?](https://youtube.com/watch?v=aircAruvnKk) — Surface when: student lacks intuition for layers/weights/activations before discussing gradients.

### Articles & Tutorials
- [Rumelhart, Hinton & Williams (1986) — Learning representations by back-propagating errors](https://www.nature.com/articles/323533a0) — Surface when: student asks “who invented backprop / what is the original idea?”
- [micrograd (Karpathy) GitHub repo](https://github.com/karpathy/micrograd) — Surface when: student wants a minimal, inspectable autograd engine to connect chain rule to code.
- [nn-zero-to-hero (Karpathy) GitHub repo](https://github.com/karpathy/nn-zero-to-hero) — Surface when: student wants exercises that manually backprop through modern components (e.g., cross-entropy, batchnorm) without autograd.
- [Glorot & Bengio (2010) — Why deep nets fail + Xavier init](https://proceedings.mlr.press/v9/glorot10a.html) — Surface when: student asks “why do gradients vanish/explode?” or “why does initialization matter?”
- [Olah — Neural Networks, Manifolds, and Topology](https://colah.github.io/posts/2014-03-NN-Manifolds-Topology/) — Surface when: student asks “what are hidden layers *doing* geometrically?” (useful motivation alongside optimization mechanics).

---

## Key Sources

- [Glorot & Bengio (2010) — Understanding the difficulty of training deep feedforward neural networks (PDF)](https://proceedings.mlr.press/v9/glorot10a/glorot10a.pdf) — Primary source for explicit backprop layer equations (Eq. 2–3), Xavier init (Eq. 16), and empirical saturation/plateau observations.
- [Rumelhart, Hinton & Williams (1986) — Learning representations by back-propagating errors](https://www.nature.com/articles/323533a0) — Seminal definition of backprop as iterative weight adjustment to minimize output error.
- [He et al. (2015) — Delving Deep into Rectifiers (PReLU + He init)](https://arxiv.org/abs/1502.01852) — Activation-aware initialization and empirical note that very deep rectifier nets converge with He init while Xavier can stall.
- [TensorFlow/Keras API — `tf.keras.optimizers.Adam`](https://www.tensorflow.org/api_docs/python/tf/keras/optimizers/Adam) — Exact optimizer defaults students ask for frequently.
- [TensorFlow/Keras API — `tf.keras.optimizers.AdamW`](https://www.tensorflow.org/api_docs/python/tf/keras/optimizers/AdamW) — Exact AdamW defaults and weight-decay exclusion mechanism.