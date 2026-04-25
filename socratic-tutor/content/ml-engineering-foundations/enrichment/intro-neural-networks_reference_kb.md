## Core Definitions

**Neuron**  
A neuron is a computational unit that takes an input vector, forms a weighted sum (a dot product) plus a bias, and then applies a nonlinearity. CS231n describes a neuron as computing “a dot product following a non-linearity,” and neural networks as arranging these neurons into layers to form a score function via “a sequence of linear mappings with interwoven non-linearities” (CS231n). LayerNorm’s paper writes the pre-activation (“summed inputs”) for unit \(i\) in layer \(l\) as \(a_i^{l}=(w_i^{l})^\top h^{l}\) and then applies a nonlinearity after adding bias (Ba et al., 2016).

**Layer**  
A layer is a collection of neurons that apply the same kind of transformation to an input representation to produce a new representation. Olah frames this as each layer transforming the data into a new representation, where “each dimension corresponds to the firing of a neuron in the layer,” and deeper layers can make the final separation easier (Olah, 2014).

**Activation function**  
An activation function is the elementwise nonlinearity applied to a neuron’s pre-activation (weighted sum plus bias). Glorot & Bengio emphasize that saturating nonlinearities (e.g., sigmoid/tanh) can cause training difficulties in deep networks due to saturation and vanishing gradients, motivating alternative nonlinearities and careful initialization (Glorot & Bengio, 2010). He et al. define PReLU as a rectifier with a learnable negative slope (He et al., 2015).

**Forward pass**  
The forward pass is the computation that maps inputs to outputs by applying each layer’s transformation in sequence (linear map + nonlinearity, and possibly normalization). BatchNorm is explicitly defined as a forward-pass normalization using mini-batch statistics during training, with different behavior at inference using population (running) estimates (Ioffe & Szegedy, 2015; PyTorch BatchNorm2d docs).

---

## Key Formulas & Empirical Results

### Layer computation + LayerNorm (Ba et al., 2016)
- **Pre-activation and activation (Eq. 1):**  
  \[
  a_i^{l} = (w_i^{l})^\top h^{l},\quad h_{i}^{l+1}=f(a_i^{l}+b_i^{l})
  \]
  - \(h^{l}\): input to layer \(l\) (vector of hidden activations)  
  - \(w_i^{l}\): weights into unit \(i\) (row of \(W^l\))  
  - \(b_i^{l}\): bias; \(f\): elementwise nonlinearity  
  **Supports:** precise “neuron/layer” mechanics used in forward pass.

- **LayerNorm statistics (per example, across features) (Eq. 3):**  
  \[
  \mu^{l}=\frac{1}{H}\sum_{i=1}^{H} a_i^{l},\quad
  \sigma^{l}=\sqrt{\frac{1}{H}\sum_{i=1}^{H}(a_i^{l}-\mu^{l})^{2}}
  \]
  - \(H\): number of hidden units/features in the layer  
  **Supports:** LN normalizes within a single example (no batch dependence).

- **LayerNorm transform with affine parameters (vector form, Supp. Eqs. 15–16):**  
  \[
  \mathrm{LN}(z;\alpha,\beta)=\alpha\odot\frac{z-\mu}{\sigma}+\beta
  \]
  **Supports:** LN includes learnable scale/shift after normalization.

### BatchNorm forward pass + train vs eval (Ioffe & Szegedy, 2015; PyTorch docs)
- **BatchNorm transform (PyTorch docs):**  
  \[
  y=\frac{x-\mathbb{E}[x]}{\sqrt{\mathrm{Var}[x]+\epsilon}}\cdot \gamma+\beta
  \]
  - \(\mathbb{E}[x]\), \(\mathrm{Var}[x]\): computed per-dimension over the mini-batch (for BatchNorm2d, over \((N,H,W)\) for each channel \(C\))  
  - \(\epsilon\): numerical stability term added inside the square root denominator  
  - \(\gamma,\beta\): learnable affine parameters (default \(\gamma=1,\beta=0\))  
  **Supports:** exact forward equation students often ask to “write down.”

- **Training vs inference behavior (PyTorch docs):**
  - Train: uses batch statistics; variance for forward uses **biased** estimator (`torch.var(..., correction=0)`).
  - Running stats: stored using **unbiased** estimator (`correction=1`).
  - Eval: by default uses running mean/var; if `track_running_stats=False`, uses batch stats even in eval.
  - Running update rule (PyTorch docs):  
    \[
    \hat x_{\text{new}}=(1-\text{momentum})\hat x+\text{momentum}\,x_t
    \]
  **Supports:** concrete “what changes at inference?” and “what does momentum mean here?”

- **Optimization rationale (Ioffe & Szegedy, 2015):** BatchNorm addresses “internal covariate shift” and enables higher learning rates, less sensitivity to initialization, and can reduce need for Dropout in some cases (paper abstract).  
  **Supports:** why normalization is part of forward pass design.

### Initialization + saturation/vanishing gradients (Glorot & Bengio, 2010; He et al., 2015)
- **Variance-preserving compromise (Glorot & Bengio, 2010, Eq. 12):**  
  \[
  \mathrm{Var}[W_i]=\frac{2}{n_i+n_{i+1}}
  \]
  - \(n_i\): fan-in; \(n_{i+1}\): fan-out  
  **Supports:** why Xavier uses fan-in and fan-out.

- **Xavier/Glorot uniform init (Eq. 16):**  
  \[
  W\sim U\left[-\frac{\sqrt{6}}{\sqrt{n_j+n_{j+1}}},\frac{\sqrt{6}}{\sqrt{n_j+n_{j+1}}}\right]
  \]
  **Supports:** exact bounds students ask for.

- **Empirical saturation behavior (Glorot & Bengio, 2010):**
  - Sigmoid nets: top hidden layer can saturate near 0; depth-5 may never escape saturation (Sec. 3.1).
  - Reported test errors (Table 1, 5 hidden layers): e.g., MNIST sigmoid 2.21 vs tanh 1.76; tanh+norm 1.64.  
  **Supports:** “activation choice matters” with concrete numbers.

- **He/Kaiming init (He et al., 2015):** rectifier-aware scaling often expressed as \(\text{std}=\sqrt{2/\hat n_l}\) (fan-in).  
  **Supports:** why ReLU-family often uses He init.

- **PReLU definition (He et al., 2015, Eq. 1):**  
  \[
  f(y_i)=\begin{cases}
  y_i,& y_i>0\\
  a_i y_i,& y_i\le 0
  \end{cases}
  \]
  **Supports:** precise activation function variant.

---

## How It Works

### Forward pass through a basic feedforward network (MLP)
1. **Input representation**: start with input vector \(h^{0}=x\).
2. **Linear map per layer**: compute pre-activations \(a^{l}=W^{l}h^{l}+b^{l}\). (LayerNorm paper gives the per-unit form \(a_i^{l}=(w_i^{l})^\top h^{l}\).)
3. **(Optional) normalization inside the forward pass**:
   - **BatchNorm (training)**: compute batch mean/variance for each feature/channel; normalize; apply affine \(\gamma,\beta\) (PyTorch BatchNorm2d; Ioffe & Szegedy).
   - **LayerNorm**: compute per-example mean/variance across features; normalize; apply affine \(\alpha,\beta\) (Ba et al.).
4. **Nonlinearity**: apply activation function elementwise, e.g. \(h^{l+1}=f(a^{l})\) (Ba et al. Eq. 1 shows nonlinearity after adding bias).
5. **Repeat** for each layer until output layer produces scores/logits (CS231n framing: sequence of linear maps with interwoven nonlinearities).

### BatchNorm forward mechanics (what to say when asked “what exactly happens?”)
- **Train mode** (default behavior in PyTorch):
  1. For each channel/feature, compute batch mean \(\mathbb{E}[x]\) and variance \(\mathrm{Var}[x]\) over the mini-batch (for BatchNorm2d: over \((N,H,W)\) slices per channel \(C\)).
  2. Normalize: \((x-\mathbb{E}[x])/\sqrt{\mathrm{Var}[x]+\epsilon}\).
  3. Affine: multiply by \(\gamma\), add \(\beta\).
  4. Update running estimates using \(\hat x_{\text{new}}=(1-\text{momentum})\hat x+\text{momentum}\,x_t\) (PyTorch docs).
- **Eval mode**:
  - Use running mean/variance (unless `track_running_stats=False`, in which case batch stats are used even in eval).

### LayerNorm forward mechanics (contrast point)
1. For a single example at a layer, compute \(\mu=\frac{1}{D}\sum_i z_i\) and \(\sigma=\sqrt{\frac{1}{D}\sum_i(z_i-\mu)^2}\) across features (Ba et al.).
2. Normalize and apply affine: \(\alpha\odot\frac{z-\mu}{\sigma}+\beta\).
3. Same computation at training and test (Ba et al. emphasize no running averages and no batch dependence).

---

## Teaching Approaches

### Intuitive (no math)
- **Neurons as “feature detectors”**: each neuron looks at the input and “fires” based on a weighted combination of input features; layers stack these detectors so later layers operate on learned features rather than raw inputs (Olah’s “new representation each layer” framing).
- **Forward pass as “progressive rewriting”**: each layer rewrites the data into a representation where the task is easier (Olah: layers transform data; final layer can separate with a simple boundary).

### Technical (with math)
- Use Ba et al.’s layer equations: \(a^l=W^l h^l\), \(h^{l+1}=f(a^l+b^l)\). Emphasize that without \(f\), the whole network collapses to a single linear map (CS231n’s “sequence of linear mappings with interwoven non-linearities” implies the nonlinearity is what prevents collapse).
- For normalization questions, quote exact transforms:
  - BatchNorm: \(y=\frac{x-\mathbb{E}[x]}{\sqrt{\mathrm{Var}[x]+\epsilon}}\gamma+\beta\) (PyTorch docs).
  - LayerNorm: \(\mathrm{LN}(z;\alpha,\beta)=\alpha\odot\frac{z-\mu}{\sigma}+\beta\) (Ba et al.).

### Analogy-based
- **Assembly line**: each layer is a station that transforms the product (representation). Early stations do simple shaping; later stations do fine adjustments so the final station can do an easy “yes/no” check (Olah’s “untangling” intuition).
- **Normalization as “auto-leveling audio”**: BatchNorm/LayerNorm keep signal levels in a stable range so later processing doesn’t clip or go silent; BatchNorm uses the batch as its reference level (train vs eval differences), LayerNorm uses each example’s own reference (Ba et al.; PyTorch docs).

---

## Common Misconceptions

1. **“A neural network is just a bunch of if-statements / rules.”**  
   - **Why wrong:** In the forward pass, neurons compute continuous weighted sums and apply smooth/continuous nonlinearities; learning adjusts weights to minimize error (Rumelhart, Hinton & Williams describe backprop as repeatedly adjusting weights to minimize output error).  
   - **Correct model:** A neural net is a parameterized computation graph (layers of dot products + nonlinearities) whose parameters are optimized from data.

2. **“More layers just means more linear transformations; it’s still linear overall.”**  
   - **Why wrong:** Without nonlinearities, compositions of linear maps collapse to one linear map; CS231n explicitly frames networks as linear mappings *interwoven with non-linearities*.  
   - **Correct model:** Depth matters because nonlinearities between linear maps create a richer class of functions; layers create new representations (Olah).

3. **“BatchNorm does the same thing at training and inference.”**  
   - **Why wrong:** PyTorch BatchNorm uses batch statistics during training and running (population) estimates during evaluation by default; it even documents different variance estimators for forward vs stored running stats.  
   - **Correct model:** BatchNorm has **mode-dependent** behavior: batch stats in train; running stats in eval (unless `track_running_stats=False`).

4. **“Sigmoid/tanh are always fine; vanishing gradients is just about learning rate.”**  
   - **Why wrong:** Glorot & Bengio show deep sigmoid/tanh nets can saturate (especially top layers), causing plateaus and slow escape from saturation; this is tied to signal/gradient propagation and Jacobian conditioning, not just LR.  
   - **Correct model:** Activation choice + initialization affect whether activations/gradients stay in a healthy range across depth (Glorot & Bengio; He et al.).

5. **“Normalization layers remove the need for learnable scaling.”**  
   - **Why wrong:** Both BatchNorm and LayerNorm include learnable affine parameters (\(\gamma,\beta\) or \(\alpha,\beta\)) after normalization (PyTorch docs; Ba et al.).  
   - **Correct model:** Normalization standardizes statistics, then affine parameters let the network recover/adjust scale and shift if beneficial.

---

## Worked Examples

### Example 1: Forward pass of a tiny 2-layer MLP (NumPy-style)
Use this when a student asks “what is the forward pass concretely?”

```python
import numpy as np

# one example (D=3)
x = np.array([1.0, -2.0, 0.5])

# layer 1: 4 hidden units
W1 = np.array([
    [ 0.2, -0.1,  0.4],
    [-0.3,  0.5,  0.1],
    [ 0.7,  0.2, -0.6],
    [ 0.0, -0.4,  0.3],
])
b1 = np.array([0.0, 0.1, -0.2, 0.0])

# layer 2: 2 outputs
W2 = np.array([
    [ 0.6, -0.2, 0.1, 0.0],
    [-0.1,  0.3, 0.4, -0.5],
])
b2 = np.array([0.05, -0.05])

def relu(z): return np.maximum(0, z)

# forward pass (Ba et al. Eq. 1 in vector form)
a1 = W1 @ x + b1
h1 = relu(a1)
scores = W2 @ h1 + b2

print("a1:", a1)
print("h1:", h1)
print("scores:", scores)
```

**Step-through (what to narrate):**
- Compute **pre-activations** \(a^1=W^1x+b^1\) (LayerNorm paper’s \(a_i=(w_i)^\top h\) is the per-unit view).
- Apply **activation** \(h^1=f(a^1)\) (CS231n: nonlinearity is essential).
- Compute output scores \(W^2h^1+b^2\).

### Example 2: BatchNorm2d behavior toggles (PyTorch defaults)
Use when students ask “what changes in eval mode?” or “what does momentum mean?”

```python
import torch
import torch.nn as nn

bn = nn.BatchNorm2d(num_features=3, eps=1e-5, momentum=0.1,
                    affine=True, track_running_stats=True)

x = torch.randn(8, 3, 16, 16)  # (N,C,H,W)

bn.train()
y_train = bn(x)  # uses batch stats; updates running_mean/var

bn.eval()
y_eval = bn(x)   # uses running stats (by default)
```

**Tutor notes grounded in PyTorch docs:**
- Normalization is over \((N,H,W)\) per channel \(C\).
- Running stats update uses \(\hat x_{\text{new}}=(1-\text{momentum})\hat x+\text{momentum}x_t\).
- If `track_running_stats=False`, then eval also uses batch stats.

---

## Comparisons & Trade-offs

| Choice | What it normalizes over | Train vs eval difference | Works with batch size 1? | Source anchor |
|---|---|---|---|---|
| **BatchNorm** | Per feature/channel over the mini-batch (e.g., BatchNorm2d over \((N,H,W)\) per \(C\)) | Yes: batch stats (train) vs running stats (eval) by default | Not ideal (depends on batch stats) | Ioffe & Szegedy (2015); PyTorch BatchNorm2d docs |
| **LayerNorm** | Per example over features in a layer | No: same computation at train/test | Yes | Ba et al. (2016) |

**When to choose (as supported by sources):**
- Choose **BatchNorm** when mini-batch statistics are stable and you want the optimization benefits described by Ioffe & Szegedy (higher learning rates, less sensitivity to init).
- Choose **LayerNorm** when batch dependence is undesirable; Ba et al. emphasize LN has no dependencies between training cases and behaves the same at training and test.

---

## Prerequisite Connections

- **Dot product / linear algebra basics**: neurons compute weighted sums \(w^\top x\) (Ba et al. Eq. 1).
- **Elementwise nonlinear functions**: activation functions are applied per component; saturation matters for training dynamics (Glorot & Bengio).
- **Mean/variance**: normalization layers explicitly compute \(\mu,\sigma\) (Ba et al.; PyTorch BatchNorm docs).
- **Computation graphs idea**: forward pass is a sequence of operations; micrograd is a concrete reference implementation of forward/backward over a DAG (micrograd repo).

---

## Socratic Question Bank

1. **If you removed every activation function from an MLP, what kind of function would the whole network represent? Why?**  
   *Good answer:* composition of linear maps collapses to a single linear map; nonlinearities are what make depth expressive (CS231n framing).

2. **In BatchNorm2d, over which axes are mean/variance computed, and what does “per channel” mean in \((N,C,H,W)\)?**  
   *Good answer:* per channel \(C\), statistics over \((N,H,W)\) slices (PyTorch docs).

3. **Why might sigmoid networks show long plateaus early in training as depth increases?**  
   *Good answer:* saturation near 0/1 leads to tiny gradients; Glorot & Bengio describe top-layer saturation and slow desaturation.

4. **What changes when you call `model.eval()` for a network with BatchNorm layers?**  
   *Good answer:* uses running mean/var instead of batch stats by default; unless `track_running_stats=False` (PyTorch docs).

5. **LayerNorm computes \(\mu,\sigma\) across what dimension(s), and why does that make it batch-size invariant?**  
   *Good answer:* across features within a single example; no batch statistics needed (Ba et al.).

6. **What role do \(\gamma,\beta\) (or \(\alpha,\beta\)) play in normalization layers—why not just normalize and stop?**  
   *Good answer:* learnable affine parameters restore/adjust scale and shift after normalization (PyTorch docs; Ba et al.).

7. **If a student says “vanishing gradients is only a learning-rate problem,” what evidence would you cite against that?**  
   *Good answer:* Glorot & Bengio’s saturation observations and their variance/Jacobian conditioning analysis; initialization/activation matter.

8. **How would you explain “each layer creates a new representation” using a 2D classification picture?**  
   *Good answer:* Olah’s view: transform data each layer so final separation is simpler (line/hyperplane in last representation).

---

## Likely Student Questions

**Q: What is the exact BatchNorm forward equation? Where does \(\epsilon\) go?**  
→ **A:** PyTorch documents BatchNorm as \(y=\frac{x-\mathbb{E}[x]}{\sqrt{\mathrm{Var}[x]+\epsilon}}\cdot\gamma+\beta\), with \(\epsilon\) added inside the square root in the denominator for numerical stability (https://docs.pytorch.org/docs/stable/generated/torch.nn.BatchNorm2d.html).

**Q: What’s the difference between BatchNorm at training time vs inference time?**  
→ **A:** In training, BatchNorm uses mini-batch mean/variance; by default it also tracks running estimates. In evaluation, it uses the running mean/variance for normalization. If `track_running_stats=False`, it uses batch statistics in both train and eval (PyTorch BatchNorm2d docs).

**Q: How does PyTorch’s BatchNorm “momentum” update running stats?**  
→ **A:** PyTorch defines \(\hat x_{\text{new}}=(1-\text{momentum})\hat x+\text{momentum}\,x_t\), where \(\hat x\) is the running estimate and \(x_t\) is the newly observed statistic; default momentum is 0.1 (PyTorch BatchNorm2d docs).

**Q: What is Xavier/Glorot initialization exactly?**  
→ **A:** Glorot & Bengio give \(W\sim U\left[-\frac{\sqrt{6}}{\sqrt{n_j+n_{j+1}}},\frac{\sqrt{6}}{\sqrt{n_j+n_{j+1}}}\right]\), derived from a variance compromise \(\mathrm{Var}[W]=\frac{2}{n_i+n_{i+1}}\) to help preserve signal/gradient variance across layers (https://proceedings.mlr.press/v9/glorot10a/glorot10a.pdf).

**Q: Why do deep sigmoid networks train poorly? Is there evidence?**  
→ **A:** Glorot & Bengio report that with sigmoid and random init, the top hidden layer can quickly saturate near 0, causing slow learning/plateaus; deeper nets (e.g., 5 hidden layers) may never escape saturation (Sec. 3.1 of the paper).

**Q: What is He/Kaiming initialization and when is it used?**  
→ **A:** He et al. derive rectifier-aware scaling commonly expressed as \(\text{std}=\sqrt{2/\text{fan-in}}\), and show deeper rectified nets converge with this init while “Xavier” can stall in their experiments (https://arxiv.org/abs/1502.01852).

**Q: What is PReLU, exactly?**  
→ **A:** He et al. define \(f(y)=y\) if \(y>0\), else \(f(y)=a y\) with learnable \(a\) (Eq. 1), i.e., a ReLU with a learnable negative slope (https://arxiv.org/abs/1502.01852).

**Q: How is LayerNorm defined, and why doesn’t it need running averages?**  
→ **A:** LayerNorm computes \(\mu,\sigma\) across features within a single example (e.g., \(\mu=\frac{1}{H}\sum_i a_i\), \(\sigma=\sqrt{\frac{1}{H}\sum_i(a_i-\mu)^2}\)) and applies an affine transform; Ba et al. emphasize it uses no mini-batch statistics and performs the same computation at training and test (https://arxiv.org/abs/1607.06450).

---

## Available Resources

### Videos
- [But what is a neural network? (3Blue1Brown)](https://youtube.com/watch?v=aircAruvnKk) — **Surface when:** student needs first-principles intuition for neurons/layers/activations before equations.
- [The spelled-out intro to neural networks and backpropagation: building micrograd](https://youtube.com/watch?v=VMj-3S1tku0) — **Surface when:** student asks how forward pass relates to computation graphs and gradients; good bridge to “what is a node/edge in the graph?”

### Articles & Tutorials
- [Neural Networks, Manifolds, and Topology (Christopher Olah)](https://colah.github.io/posts/2014-03-NN-Manifolds-Topology/) — **Surface when:** student asks “why do multiple layers help?” or wants geometric intuition about representations.
- [micrograd (Karpathy)](https://github.com/karpathy/micrograd) — **Surface when:** student wants a minimal, inspectable implementation of forward/backward over a DAG.
- [Learning representations by back-propagating errors (Rumelhart, Hinton & Williams, 1986)](https://www.nature.com/articles/323533a0) — **Surface when:** student asks for the historical/primary-source definition of backprop as weight adjustment to minimize output error.

---

## Visual Aids

![The Transformer encoder-decoder architecture (Vaswani et al., 2017).](/api/wiki-images/neural-networks/images/arxiv-html-1706-03762v7_001.png)  
**Show when:** student asks what a “layered neural network” looks like in a modern architecture; use as a map to point out repeated layer blocks.

![Scaled Dot-Product Attention: Q·K scaled, softmaxed, then applied to V.](/api/wiki-images/neural-networks/images/arxiv-html-1706-03762v7_002.png)  
**Show when:** student asks what a forward pass “looks like” in a non-MLP neural network block (attention as a computational graph).

---

## Key Sources

- [Batch Normalization: Accelerating Deep Network Training by Reducing Internal Covariate Shift (Ioffe & Szegedy, 2015)](https://proceedings.mlr.press/v37/ioffe15.html) — authoritative rationale + train/infer distinction for BatchNorm as part of the forward pass.
- [BatchNorm2d — PyTorch documentation](https://docs.pytorch.org/docs/stable/generated/torch.nn.BatchNorm2d.html) — exact forward equation, running-stat update rule, and default hyperparameters/behavior.
- [Understanding the difficulty of training deep feedforward neural networks (Glorot & Bengio, 2010)](https://proceedings.mlr.press/v9/glorot10a/glorot10a.pdf) — primary source for saturation/vanishing gradients evidence and Xavier initialization formula.
- [Layer Normalization (Ba et al., 2016)](https://arxiv.org/abs/1607.06450) — exact LN equations and the key contrast: same computation at train/test, no batch dependence.
- [Delving Deep into Rectifiers: Surpassing Human-Level Performance on ImageNet Classification (He et al., 2015)](https://arxiv.org/abs/1502.01852) — PReLU definition and rectifier-aware (He/Kaiming) initialization scaling.