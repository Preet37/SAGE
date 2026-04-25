## Core Definitions

**Regularization (general)**  
Regularization is any training-time technique that reduces overfitting by constraining effective model capacity or discouraging reliance on brittle patterns. In CS231n’s framing, regularization includes explicit penalties like L2/L1/max-norm and stochastic methods like dropout, all aimed at improving generalization rather than training loss. (CS231n: https://cs231n.github.io/neural-networks-2/#reg)

**Dropout**  
Srivastava et al. define dropout as randomly “dropping” units (and their connections) during training; this prevents units from co-adapting and can be viewed as sampling from an exponential number of “thinned” networks. At test time, the effect of averaging these thinned networks is approximated by using a single unthinned network with appropriately smaller effective weights. (Srivastava et al., 2014: https://jmlr.org/papers/v15/srivastava14a.html)

**Weight decay (L2 regularization) & decoupled weight decay (AdamW)**  
Weight decay is the practice of penalizing large weights (commonly via an L2 penalty) to bias solutions toward smaller-norm parameters; in deep learning practice it is often implemented as “weight decay” in optimizers. TensorFlow’s `AdamW` explicitly implements **decoupled weight decay** (Loshchilov & Hutter, 2019 as cited in the API doc): Adam’s adaptive moment updates plus a separate weight decay term, rather than folding L2 into the gradient. (Keras AdamW API: https://www.tensorflow.org/api_docs/python/tf/keras/optimizers/AdamW)

**Batch Normalization (BatchNorm)**  
Ioffe & Szegedy’s BatchNorm normalizes activations using **mini-batch** mean and variance during training, then uses accumulated (“population”) estimates at inference; it is integrated into the model so gradients flow through the normalization. The PyTorch `BatchNorm2d` doc states the forward form \(y = \frac{x - \mathbb{E}[x]}{\sqrt{\mathrm{Var}[x]+\epsilon}} \cdot \gamma + \beta\), with learnable \(\gamma,\beta\) per channel, and describes running-statistics behavior across train/eval. (Ioffe & Szegedy via proceedings page: https://proceedings.mlr.press/v37/ioffe15.html; PyTorch BN2d: https://docs.pytorch.org/docs/stable/generated/torch.nn.BatchNorm2d.html)

**Layer Normalization (LayerNorm)**  
Ba et al. define LayerNorm as normalizing each training case independently by computing mean and variance across the **features/hidden units** of a layer (not across the batch), then applying a learned affine transform. A key contrast to BatchNorm is that LayerNorm uses no mini-batch statistics and performs the same computation at training and test time. (LayerNorm paper: https://arxiv.org/abs/1607.06450)

**RMSNorm (common LayerNorm variant in Transformers)**  
Zhang & Sennrich define RMSNorm as a simplification of LayerNorm that removes mean-centering and normalizes only by the root-mean-square (RMS) of activations, then applies a learned gain. The paper states that if the mean is zero, RMSNorm equals LayerNorm, and highlights rescaling invariance \(\mathrm{RMS}(\alpha x)=\alpha\,\mathrm{RMS}(x)\). (RMSNorm paper: https://arxiv.org/abs/1910.07467)

**Normalization placement in Transformers (Pre-LN vs Post-LN vs Peri-LN)**  
A recent analysis defines: **Post-LN** as \(x_{l+1}=\mathrm{LN}(x_l+F_l(x_l))\); **Pre-LN** as \(x_{l+1}=x_l+F_l(\mathrm{LN}(x_l))\); and **Peri-LN** as applying LN both before and after the sublayer output before adding to the residual. The paper’s focus is variance/gradient stability and convergence behavior across these placements. (Peri-LN vs Pre/Post-LN: https://arxiv.org/html/2502.02732v1)

**Data augmentation (as regularization)**  
Data augmentation is a regularization strategy that increases effective dataset diversity by applying label-preserving transformations to inputs, reducing overfitting by making the model invariant/robust to those transformations. (This lesson includes it as a key concept; the provided sources emphasize regularization broadly but do not give a single canonical augmentation definition beyond that framing in CS231n’s “setting up data/model” context.) (CS231n context: https://cs231n.github.io/neural-networks-2/#reg)


## Key Formulas & Empirical Results

### Dropout: “thinned networks” view (qualitative claim)
- **Claim:** Dropout “samples from an exponential number of different thinned networks” during training; test-time uses a single unthinned network approximating the average prediction.  
  **Supports:** Why dropout reduces overfitting and can be seen as implicit ensembling.  
  Source: Srivastava et al., 2014 (abstract) https://jmlr.org/papers/v15/srivastava14a.html

### BatchNorm forward equation + running-statistics behavior (PyTorch)
- **Forward (PyTorch doc):**  
  \[
  y=\frac{x-\mathbb{E}[x]}{\sqrt{\mathrm{Var}[x]+\epsilon}}\cdot \gamma+\beta
  \]
  - Stats computed per-dimension over mini-batches; for `BatchNorm2d`, over \((N,H,W)\) slices for each channel \(C\).  
  - \(\gamma,\beta\) are learnable vectors of size \(C\); defaults: \(\gamma=1\), \(\beta=0\).  
  - Train-time variance uses **biased** estimator (`correction=0`), but running variance stored uses **unbiased** estimator (`correction=1`).  
  - Running-stat update (note PyTorch’s BN “momentum” meaning):  
    \[
    \hat x_{\text{new}}=(1-\text{momentum})\hat x+\text{momentum}\,x_t
    \]
  - Defaults: `eps=1e-5`, `momentum=0.1`, `affine=True`, `track_running_stats=True`.  
  Source: https://docs.pytorch.org/docs/stable/generated/torch.nn.BatchNorm2d.html

### LayerNorm equations (Ba et al.)
- Per-example, across features (hidden units) for a layer:
  \[
  \mu=\frac{1}{H}\sum_{i=1}^{H} a_i,\quad
  \sigma=\sqrt{\frac{1}{H}\sum_{i=1}^{H}(a_i-\mu)^2}
  \]
- Apply learned gain/bias after normalization:
  \[
  h_i=f\!\left(\frac{g_i}{\sigma}(a_i-\mu)+b_i\right)
  \]
  Source: https://arxiv.org/abs/1607.06450

### RMSNorm equation + invariance (Zhang & Sennrich)
- RMSNorm:
  \[
  \bar a_i=\frac{a_i}{\mathrm{RMS}(a)}\, g_i,\quad \mathrm{RMS}(a)=\sqrt{\frac{1}{n}\sum_{i=1}^n a_i^2}
  \]
- Rescaling property:
  \[
  \mathrm{RMS}(\alpha x)=\alpha\,\mathrm{RMS}(x)
  \]
  Source: https://arxiv.org/abs/1910.07467

### Pre-LN vs Post-LN vs Peri-LN definitions (explicit equations)
- **Post-LN:** \(x_{l+1}=\mathrm{LN}(x_l+F_l(x_l))\)  
- **Pre-LN:** \(x_{l+1}=x_l+F_l(\mathrm{LN}(x_l))\)  
- **Peri-LN (described):** \(u_l=\mathrm{LN}(x_l)\), \(y_l=F_l(u_l)\), \(v_l=\mathrm{LN}(y_l)\), \(x_{l+1}=x_l+v_l\)  
  Source: https://arxiv.org/html/2502.02732v1

### Empirical: BatchNorm optimization effect (paper abstract)
- **Claim:** BatchNorm can reach the same accuracy with **14× fewer training steps** on an image classification model (abstract).  
  Source: https://proceedings.mlr.press/v37/ioffe15.html

### Empirical: Peri-LN stability/quality (selected table values)
- Table 2 (Peri-LN rows), average benchmark scores and losses reported for 125M/350M/1.3B models (trained on 30B tokens; 5 seeds). Example: **1.3B Peri-LN Avg 58.56, Loss 3.11**.  
  Source: https://arxiv.org/html/2502.02732v1

### Implementation defaults frequently asked about (APIs)
- **Keras AdamW signature defaults:** `learning_rate=0.001`, `weight_decay=0.004`, `beta_1=0.9`, `beta_2=0.999`, `epsilon=1e-07`, `amsgrad=False`, plus optional clipping/EMA/loss scaling/grad accumulation.  
  Source: https://www.tensorflow.org/api_docs/python/tf/keras/optimizers/AdamW
- **Keras Adam signature defaults:** `learning_rate=0.001`, `beta_1=0.9`, `beta_2=0.999`, `epsilon=1e-07`, `amsgrad=False`, `weight_decay=None`.  
  Source: https://www.tensorflow.org/api_docs/python/tf/keras/optimizers/Adam

### TransformerEncoderLayer normalization/dropout knobs (PyTorch)
- `torch.nn.TransformerEncoderLayer(..., dropout=0.1, layer_norm_eps=1e-5, norm_first=False, ...)`  
  - `norm_first=False` means “after” (Post-LN style in that module); `norm_first=True` applies layer norm prior to attention/FFN (Pre-LN style).  
  Source: PyTorch docs (2.11): https://docs.pytorch.org/docs/stable/generated/torch.nn.TransformerEncoderLayer.html


## How It Works

### Dropout (mechanics in a forward pass)
1. **Training mode:** sample a binary mask for activations (or units) and zero out (“drop”) a random subset; the network becomes a “thinned” subnetwork for that step.  
2. **Backprop:** gradients flow only through the kept units/paths for that step.  
3. **Across steps:** training effectively averages over many thinned networks (Srivastava et al. describe this as exponential in count).  
4. **Evaluation mode:** use the full network (no dropping) as an approximation to averaging predictions of the thinned networks.  
Source for the conceptual procedure: Srivastava et al. abstract https://jmlr.org/papers/v15/srivastava14a.html

### BatchNorm2d in PyTorch (train vs eval)
1. **Input shape:** \((N,C,H,W)\).  
2. **Compute batch statistics (train):** for each channel \(c\), compute mean/variance over the \((N,H,W)\) elements.  
3. **Normalize:** \(x \mapsto (x-\mathbb{E}[x])/\sqrt{\mathrm{Var}[x]+\epsilon}\).  
4. **Affine transform (if `affine=True`):** multiply by \(\gamma_c\), add \(\beta_c\).  
5. **Update running stats (if `track_running_stats=True`):** update `running_mean` and `running_var` using the doc’s exponential moving average rule with `momentum` (PyTorch BN momentum is not optimizer momentum).  
6. **Eval mode:** use running statistics instead of batch statistics (unless `track_running_stats=False`, in which case batch stats are used even in eval).  
Source: https://docs.pytorch.org/docs/stable/generated/torch.nn.BatchNorm2d.html

### LayerNorm (per-example normalization)
1. For each example (and typically each token position in a Transformer), take the feature vector \(z\in\mathbb{R}^D\).  
2. Compute \(\mu\) and \(\sigma\) across the **D features** for that example.  
3. Normalize and apply learned affine parameters \(\alpha,\beta\): \(\mathrm{LN}(z)=\alpha\odot\frac{z-\mu}{\sigma}+\beta\).  
4. Same computation in training and inference (no running averages).  
Source: https://arxiv.org/abs/1607.06450

### RMSNorm (LayerNorm variant)
1. For each feature vector \(a\), compute \(\mathrm{RMS}(a)=\sqrt{\frac{1}{n}\sum_i a_i^2}\).  
2. Normalize by RMS (no mean subtraction), then multiply by learned gain \(g\).  
Source: https://arxiv.org/abs/1910.07467

### Transformer layer: where normalization and dropout appear (PyTorch reference)
1. A `TransformerEncoderLayer` contains self-attention + feedforward network.  
2. It includes dropout (`dropout=0.1` default) and LayerNorm with `layer_norm_eps=1e-5`.  
3. `norm_first` toggles whether LayerNorm is applied before sublayers (Pre-LN) or after residual addition (Post-LN-like in this module).  
Source: https://docs.pytorch.org/docs/stable/generated/torch.nn.TransformerEncoderLayer.html


## Teaching Approaches

### Intuitive (no math): “stability vs generalization”
- **Regularization** (dropout, weight decay, augmentation) is about *generalization*: make it harder for the model to memorize quirks of the training set.  
- **Normalization** (BatchNorm/LayerNorm/RMSNorm) is about *training dynamics*: keep activations in a well-behaved range so optimization is less fragile (BatchNorm abstract emphasizes higher learning rates and less sensitivity to initialization). (https://proceedings.mlr.press/v37/ioffe15.html)

### Technical (with math): “what statistics are used, and on which axes”
- BatchNorm uses mini-batch statistics and maintains running estimates for inference; PyTorch specifies the exact forward equation and running-stat update. (https://docs.pytorch.org/docs/stable/generated/torch.nn.BatchNorm2d.html)  
- LayerNorm uses per-example statistics across features and is identical at train/test. (https://arxiv.org/abs/1607.06450)  
- RMSNorm replaces variance-around-mean with RMS-only normalization and has a rescaling invariance property. (https://arxiv.org/abs/1910.07467)

### Analogy-based: “noise injection vs re-centering”
- **Dropout** is like training a committee where different members are randomly absent each meeting; the group can’t rely on any single specialist always being present (Srivastava et al.’s “thinned networks” view).  
- **Normalization** is like standardizing the “units” of internal signals so later layers don’t have to constantly adapt to shifting scales; BatchNorm explicitly targets shifting distributions during training (internal covariate shift motivation in the BatchNorm paper abstract). (https://proceedings.mlr.press/v37/ioffe15.html)


## Common Misconceptions

1. **“Dropout just makes the network smaller, so it must underfit.”**  
   - **Why wrong:** Dropout is not a permanent reduction in capacity; Srivastava et al. describe it as sampling many thinned networks during training and approximating their average at test time.  
   - **Correct model:** Dropout is *stochastic regularization / implicit ensembling*; it can reduce overfitting while keeping full capacity at inference.  
   Source: https://jmlr.org/papers/v15/srivastava14a.html

2. **“BatchNorm and LayerNorm are basically the same; they both normalize activations.”**  
   - **Why wrong:** They normalize over different axes and have different train/test behavior. PyTorch BN uses mini-batch stats and (by default) running estimates for eval; LayerNorm uses per-example stats and is the same at train/test.  
   - **Correct model:** BatchNorm couples examples within a batch; LayerNorm does not.  
   Sources: BN2d doc https://docs.pytorch.org/docs/stable/generated/torch.nn.BatchNorm2d.html; LayerNorm paper https://arxiv.org/abs/1607.06450

3. **“BatchNorm momentum is the same as optimizer momentum.”**  
   - **Why wrong:** PyTorch explicitly notes BN’s `momentum` is for running-stat updates and gives the update equation \(\hat x_{\text{new}}=(1-\text{momentum})\hat x+\text{momentum}x_t\).  
   - **Correct model:** BN momentum controls how quickly running mean/var track recent batches; it’s unrelated to SGD/Adam momentum.  
   Source: https://docs.pytorch.org/docs/stable/generated/torch.nn.BatchNorm2d.html

4. **“LayerNorm needs running averages at inference like BatchNorm.”**  
   - **Why wrong:** Ba et al. emphasize LN uses no mini-batch statistics and performs the same computation at training and test.  
   - **Correct model:** LN recomputes mean/variance from the current example’s features every time; no running buffers required.  
   Source: https://arxiv.org/abs/1607.06450

5. **“Pre-LN vs Post-LN is just a style choice; it doesn’t affect stability.”**  
   - **Why wrong:** The cited analysis explicitly links placement to gradient/variance behavior: Post-LN can weaken gradients in deep nets; Pre-LN can allow variance to accumulate; Peri-LN adds output normalization to damp residual spikes.  
   - **Correct model:** Norm placement changes the effective signal/gradient scaling through residual paths and can materially affect convergence stability.  
   Source: https://arxiv.org/html/2502.02732v1


## Worked Examples

### Example 1: PyTorch BatchNorm2d train vs eval behavior (running stats)
```python
import torch
import torch.nn as nn

bn = nn.BatchNorm2d(num_features=3, eps=1e-5, momentum=0.1,
                    affine=True, track_running_stats=True)

x = torch.randn(8, 3, 16, 16)

# TRAIN: uses batch stats and updates running stats
bn.train()
y_train = bn(x)
rm1 = bn.running_mean.clone()
rv1 = bn.running_var.clone()

# EVAL: uses running stats (not batch stats)
bn.eval()
y_eval = bn(x)

print("running_mean after one train forward:", rm1)
print("running_var after one train forward:", rv1)
print("train/eval outputs close?", torch.allclose(y_train, y_eval, atol=1e-4))
```

**Tutor notes (what to point out mid-conversation):**
- In `.train()`, BN uses mini-batch mean/var and updates `running_mean/var` per the doc’s EMA rule.  
- In `.eval()`, BN uses the stored running stats (unless `track_running_stats=False`).  
Source for semantics and defaults: https://docs.pytorch.org/docs/stable/generated/torch.nn.BatchNorm2d.html

### Example 2: PyTorch TransformerEncoderLayer and `norm_first` (Pre-LN vs Post-LN toggle)
```python
import torch
import torch.nn as nn

layer_post = nn.TransformerEncoderLayer(d_model=64, nhead=8, norm_first=False, dropout=0.1)
layer_pre  = nn.TransformerEncoderLayer(d_model=64, nhead=8, norm_first=True,  dropout=0.1)

src = torch.randn(10, 32, 64)  # (seq, batch, feature) default

out_post = layer_post(src)
out_pre  = layer_pre(src)

print(out_post.shape, out_pre.shape)
```

**Tutor notes:**
- Use this to concretely anchor “Pre-LN vs Post-LN” in a real API knob (`norm_first`).  
- Default `dropout=0.1`, `layer_norm_eps=1e-5` are visible in the signature.  
Source: https://docs.pytorch.org/docs/stable/generated/torch.nn.TransformerEncoderLayer.html


## Comparisons & Trade-offs

| Technique | Category | What it targets | Train vs eval difference | Typical failure mode / caveat (from sources) |
|---|---|---|---|---|
| Dropout | Regularization | Overfitting via co-adaptation | Yes (drop units only in training) | Can hurt if applied where noise is harmful; BatchNorm paper notes BN can sometimes eliminate need for dropout (contextual claim). (Ioffe15 abstract) |
| Weight decay (AdamW) | Regularization | Large weights / complexity | No (optimizer behavior during training only) | Must often exclude some variables in practice; Keras provides `exclude_from_weight_decay(...)`. |
| BatchNorm | Normalization | Optimization stability; internal distribution shift | Yes (batch stats in train; running stats in eval by default) | Sensitive to batch statistics; behavior changes with `track_running_stats`. |
| LayerNorm | Normalization | Optimization stability without batch coupling | No (same computation train/test) | Placement in residual blocks matters (Pre/Post/Peri-LN stability differences). |
| RMSNorm | Normalization | Similar to LN but RMS-only | No (same computation train/test) | Removes mean-centering; relies on RMS-only normalization properties. |

**When to choose (source-grounded cues):**
- Choose **BatchNorm** when mini-batch statistics are reliable and you want the optimization benefits described by Ioffe & Szegedy (higher learning rates, less init sensitivity). (https://proceedings.mlr.press/v37/ioffe15.html)  
- Choose **LayerNorm/RMSNorm** when you want per-example normalization with identical train/test computation (LayerNorm paper) and/or RMS-only efficiency/invariance (RMSNorm paper). (https://arxiv.org/abs/1607.06450, https://arxiv.org/abs/1910.07467)  
- In Transformers, be explicit about **norm placement**; PyTorch exposes `norm_first` and research compares Pre/Post/Peri-LN stability. (https://docs.pytorch.org/docs/stable/generated/torch.nn.TransformerEncoderLayer.html, https://arxiv.org/html/2502.02732v1)


## Prerequisite Connections

- **Overfitting vs generalization (train/dev/test split):** needed to justify why regularization helps even if training loss worsens (CS231n regularization section context). (https://cs231n.github.io/neural-networks-2/#reg)  
- **Mean/variance and normalization:** needed to parse BN/LN equations and understand what “axes” statistics are computed over. (BN2d doc; LayerNorm paper)  
- **Training vs inference modes (`train()`/`eval()`):** needed to understand BN running stats and dropout behavior differences. (BN2d doc; dropout paper abstract)  
- **Residual blocks in Transformers:** needed to understand why norm placement (Pre/Post/Peri-LN) changes stability. (Peri-LN paper; PyTorch TransformerEncoderLayer `norm_first`)


## Socratic Question Bank

1. **If BatchNorm uses batch statistics, what changes when batch size becomes very small—what would you expect to happen to the noise in the normalization?**  
   *Good answer:* recognizes batch-stat estimates become noisy; links to BN’s dependence on mini-batch stats (BN2d doc).

2. **LayerNorm and BatchNorm both compute a mean and variance—over which dimensions does each compute them in the definitions we have?**  
   *Good answer:* BN over mini-batch (and spatial dims for BN2d); LN over features per example (sources: BN2d doc; LayerNorm paper).

3. **Why does dropout reduce “co-adaptation” according to the dropout paper’s description? What does the network have to do differently during training?**  
   *Good answer:* explains reliance on any single unit is risky because it may be dropped; must distribute representations (Srivastava abstract).

4. **In PyTorch BatchNorm2d, what does `track_running_stats=False` imply for evaluation-time behavior?**  
   *Good answer:* eval uses batch stats as well; running buffers are `None` (BN2d doc).

5. **What does `norm_first=True` in `TransformerEncoderLayer` correspond to conceptually: Pre-LN or Post-LN?**  
   *Good answer:* Pre-LN (norm before attention/FFN) (PyTorch TransformerEncoderLayer doc).

6. **Peri-LN adds an extra normalization—where is it applied and what instability is it intended to damp?**  
   *Good answer:* LN on both input and output of sublayer; intended to damp residual spikes / stabilize variance and gradients (Peri-LN paper).

7. **AdamW vs Adam: what extra hyperparameter appears in AdamW’s signature by default, and what is its default value in Keras?**  
   *Good answer:* `weight_decay=0.004` in `AdamW` (Keras AdamW API).


## Likely Student Questions

**Q: What exactly is the BatchNorm2d formula in PyTorch?**  
→ **A:** PyTorch states \(y=\frac{x-\mathbb{E}[x]}{\sqrt{\mathrm{Var}[x]+\epsilon}}\cdot\gamma+\beta\), with per-channel \(\gamma,\beta\) (size \(C\)), default \(\gamma=1,\beta=0\). (https://docs.pytorch.org/docs/stable/generated/torch.nn.BatchNorm2d.html)

**Q: In PyTorch BatchNorm2d, what does `momentum=0.1` mean?**  
→ **A:** It is the EMA coefficient for running stats: \(\hat x_{\text{new}}=(1-\text{momentum})\hat x+\text{momentum}x_t\). PyTorch notes this is different from optimizer momentum. (https://docs.pytorch.org/docs/stable/generated/torch.nn.BatchNorm2d.html)

**Q: How does LayerNorm compute its mean/variance?**  
→ **A:** LayerNorm computes \(\mu=\frac{1}{H}\sum_i a_i\) and \(\sigma=\sqrt{\frac{1}{H}\sum_i(a_i-\mu)^2}\) across hidden units/features for each training case, then applies learned gain/bias. It uses no batch statistics and is the same at train/test. (https://arxiv.org/abs/1607.06450)

**Q: What is RMSNorm’s equation and how is it different from LayerNorm?**  
→ **A:** RMSNorm uses \(\bar a_i=\frac{a_i}{\mathrm{RMS}(a)}g_i\) with \(\mathrm{RMS}(a)=\sqrt{\frac{1}{n}\sum_i a_i^2}\); it removes mean-centering (no \(a_i-\mu\)). (https://arxiv.org/abs/1910.07467)

**Q: What does `norm_first` do in `torch.nn.TransformerEncoderLayer`?**  
→ **A:** `norm_first=True` applies layer norm prior to attention and feedforward operations; otherwise it’s done after (default `False`). This corresponds to Pre-LN vs Post-LN-style placement in that module. (https://docs.pytorch.org/docs/stable/generated/torch.nn.TransformerEncoderLayer.html)

**Q: What are the default dropout and LayerNorm epsilon in PyTorch’s TransformerEncoderLayer?**  
→ **A:** The signature shows `dropout=0.1` and `layer_norm_eps=1e-05`. (https://docs.pytorch.org/docs/stable/generated/torch.nn.TransformerEncoderLayer.html)

**Q: What are Keras AdamW defaults for learning rate and weight decay?**  
→ **A:** `tf.keras.optimizers.AdamW(learning_rate=0.001, weight_decay=0.004, beta_1=0.9, beta_2=0.999, epsilon=1e-07, ...)`. (https://www.tensorflow.org/api_docs/python/tf/keras/optimizers/AdamW)

**Q: What does the dropout paper claim is happening at test time?**  
→ **A:** It says test-time prediction approximates averaging predictions of many thinned networks by using a single unthinned network with smaller weights. (https://jmlr.org/papers/v15/srivastava14a.html)


## Available Resources

### Videos
- [The spelled-out intro to neural networks and backpropagation: building micrograd](https://youtube.com/watch?v=VMj-3S1tku0) — **Surface when:** student is shaky on forward/backward passes and why regularization affects gradients/updates.
- [Let’s build GPT: from scratch, in code, spelled out.](https://youtube.com/watch?v=kCc8FmEb1nY) — **Surface when:** student asks where LayerNorm/dropout live inside a Transformer block and how `train()`/`eval()` changes behavior.
- [Video (wjZofJX0v4M)](https://youtube.com/watch?v=wjZofJX0v4M) — **Surface when:** student wants a visual, high-level sense of Transformer blocks (Add & Norm) before diving into equations.
- [But what is a neural network?](https://youtube.com/watch?v=aircAruvnKk) — **Surface when:** student needs intuition for activations/neurons before discussing normalization statistics.

### Articles & Tutorials
- [Jay Alammar — The Illustrated Transformer](https://jalammar.github.io/illustrated-transformer/) — **Surface when:** student asks “where exactly is Add & Norm?” or needs a diagram of residual + layer norm in the encoder.
- [Christopher Olah — Neural Networks, Manifolds, and Topology](https://colah.github.io/posts/2014-03-NN-Manifolds-Topology/) — **Surface when:** student asks why over-parameterized nets overfit and how depth changes representation geometry.
- [Lilian Weng — Attention? Attention!](https://lilianweng.github.io/posts/2018-06-24-attention/) — **Surface when:** student asks how normalization affects attention dot products/norms (context: D2L notes norms bounded by normalization).
- [Karpathy micrograd](https://github.com/karpathy/micrograd) — **Surface when:** student wants to implement L2/weight decay or dropout-like masking from scratch to see gradient effects.


## Visual Aids

![Dropout randomly deactivates neurons during training to reduce overfitting. (cs231n)](/api/wiki-images/neural-networks/images/cs231n-neural-networks-2_004.jpeg)  
**Show when:** student confuses dropout with “removing neurons permanently” or needs the core mechanism visually.

![Residual connection and layer normalization in a Transformer encoder layer. (Alammar)](/api/wiki-images/transformer-architecture/images/jalammar-illustrated-transformer_026.png)  
**Show when:** student asks where LayerNorm sits relative to residual connections (“Add & Norm”) in Transformers.

![Transformer encoder block with self-attention and FFN (UvA DLC).](/api/wiki-images/transformer-architecture/images/uvadlc-notebooks-readthedocs-en-latest-tutorial_notebooks-tutorial6-Transformers_004.svg)  
**Show when:** student asks how many norms/dropouts exist per encoder layer and how the block is structured.


## Key Sources

- [BatchNorm2d — PyTorch documentation](https://docs.pytorch.org/docs/stable/generated/torch.nn.BatchNorm2d.html) — precise forward equation, running-stat update rule, and train/eval semantics used in practice.
- [Layer Normalization (Ba et al., 2016)](https://arxiv.org/abs/1607.06450) — authoritative definition of LayerNorm and its train/test invariance.
- [Dropout (Srivastava et al., 2014)](https://jmlr.org/papers/v15/srivastava14a.html) — canonical statement of dropout’s purpose and “thinned networks” interpretation.
- [RMSNorm (Zhang & Sennrich, 2019)](https://arxiv.org/abs/1910.07467) — exact RMSNorm equation and invariance properties.
- [TransformerEncoderLayer — PyTorch documentation](https://docs.pytorch.org/docs/stable/generated/torch.nn.TransformerEncoderLayer.html) — concrete API knobs (`dropout`, `layer_norm_eps`, `norm_first`) that map to normalization/regularization choices in Transformer blocks.