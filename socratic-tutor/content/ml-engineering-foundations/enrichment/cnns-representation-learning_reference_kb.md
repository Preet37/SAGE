## Core Definitions

**Convolution (in CNNs)**  
As CS231n describes, a convolutional layer applies a small learnable filter (kernel) across spatial positions of an input volume, computing local dot-products (more precisely, the operation used in common deep learning libraries is cross-correlation) to produce an output activation volume; the key architectural constraint is *local connectivity* (receptive fields) and *parameter sharing* across positions, which drastically reduces parameters compared to fully-connected layers for images. (CS231n; PyTorch `Conv2d` notes cross-correlation)

**Feature map (activation map)**  
In CS231n’s terminology, a CNN layer outputs a 3D activation volume (height × width × depth/channels). Each channel can be viewed as a *feature map*: a spatial grid of responses indicating where a learned feature (e.g., an edge/texture/part) is detected across the input. (CS231n)

**Pooling (max pooling)**  
Pooling is a downsampling operation applied independently per channel that aggregates local neighborhoods (e.g., 2×2 windows) into a smaller spatial map; in max pooling, each output is the maximum value in the window. PyTorch defines MaxPool2d as taking the maximum over each sliding window (with stride/padding/dilation controlling window placement). (PyTorch `MaxPool2d`; CS231n)

**Residual connections (skip connections)**  
He et al. define residual learning by rewriting a desired mapping \(H(x)\) as \(H(x)=F(x)+x\), implemented as a shortcut/identity connection that adds the input \(x\) to the output of a residual function \(F\). The residual block output is \(y = F(x,\{W_i\}) + x\) (or with a projection \(W_s x\) when dimensions differ). The motivation is optimization: if identity is optimal, it is easier to drive \(F(x)\to 0\) than to force stacked nonlinear layers to approximate identity. (ResNet, He et al. 2015)

**ImageNet (ILSVRC classification benchmark)**  
ImageNet/ILSVRC is a large-scale image classification benchmark used to compare CNN architectures. AlexNet reports training on 1.3M images into 1000 classes and reports top-1 and top-5 error; later architectures (VGG, GoogLeNet/Inception, ResNet) report top-5 error as a primary metric for ILSVRC. (AlexNet abstract; VGG; Inception v1; ResNet)

---

## Key Formulas & Empirical Results

### Convolution / pooling output-size arithmetic (Dumoulin & Visin “conv arithmetic”)
For one spatial axis (apply independently to height and width): input size \(i\), kernel/window \(k\), stride \(s\), padding \(p\).

- **General convolution output size**:  
  \[
  o=\left\lfloor\frac{i+2p-k}{s}\right\rfloor+1
  \]
  Supports “what is the output shape?” questions. (conv arithmetic, Rel. 6)

- **Stride-1, “same” padding (odd \(k\))**: \(p=\lfloor k/2\rfloor \Rightarrow o=i\). (Rel. 3)

- **Pooling output size (no padding)**:  
  \[
  o=\left\lfloor\frac{i-k}{s}\right\rfloor+1
  \]
  (Rel. 7)

- **Dilated conv effective kernel**: \(\hat{k}=k+(k-1)(d-1)\) and  
  \[
  o=\left\lfloor\frac{i+2p-k-(k-1)(d-1)}{s}\right\rfloor+1
  \]
  (Rel. 15)

### PyTorch layer semantics (for precise quoting)
- **`torch.nn.Conv2d`**: implements valid 2D **cross-correlation**; supports `stride`, `padding` (including strings `'valid'`, `'same'` with stride=1), `dilation`, `groups` (depthwise when `groups==in_channels`). (PyTorch `Conv2d`)
- **`torch.nn.MaxPool2d`**:  
  \[
  out(N_i,C_j,h,w)=\max_{m=0..k_H-1}\max_{n=0..k_W-1} input(N_i,C_j, stride[0]\cdot h+m, stride[1]\cdot w+n)
  \]
  Padding is implicit **\(-\infty\)** for max pooling. (PyTorch `MaxPool2d`)

### Residual learning equations (ResNet)
- **Identity shortcut**: \(y = F(x,\{W_i\}) + x\). (Eq. 1)  
- **Projection shortcut (dimension match)**: \(y = F(x,\{W_i\}) + W_s x\), typically \(W_s\) is a 1×1 conv. (Eq. 2) (He et al.)

### ImageNet benchmark anchor numbers (architecture milestones)
- **AlexNet (ILSVRC-2012 style result)**: top-1 error **39.7%**, top-5 error **18.9%**; **60M parameters**; 5 conv layers + max-pooling + 2 FC + softmax. (AlexNet abstract)
- **VGG (best single network reported)**: **25.9% top-1 / 8.0% top-5** error (with scale jittering); 3×3 conv stacks; 11/13/16/19-layer variants; 5 max-pool layers (2×2, stride 2). (VGG)
- **GoogLeNet / Inception v1 (ILSVRC14)**: designed for ~**1.5B multiply-adds** inference budget; **~12× fewer parameters** than AlexNet while more accurate; final submission **6.67% top-5 error** (7-model ensemble, 144 crops). (Inception v1)
- **ResNet (ILSVRC15)**: addresses “degradation” (deeper plain nets can have higher *training* error); **152-layer** single-model top-5 val error **4.49%**; ensemble top-5 test error **3.57%**; ResNet-50 ~**3.8B FLOPs**, ResNet-152 ~**11.3B FLOPs** (still less than VGG-16/19 **15.3/19.6B**). (ResNet)

### VGG’s kernel-stacking parameter comparison (why 3×3 stacks)
For channel width \(C\) (in/out):
- 3-layer 3×3 stack: \(3\cdot 3^2\cdot C^2 = 27C^2\) weights  
- single 7×7: \(7^2\cdot C^2 = 49C^2\) weights (**81% more**)  
Also yields more nonlinearities (3 ReLUs vs 1). (VGG Sec. 2.3)

### Inception v1 module design facts (for “why these branches?”)
- Parallel branches: **1×1**, **3×3**, **5×5**, and **3×3 max-pool**, then **concatenate along channels**.  
- **1×1 conv used for dimension reduction** before expensive 3×3/5×5 (“reduce” layers) and as “pool projection” after pooling.  
- **Auxiliary classifiers** during training: loss weight **0.3**, discarded at inference. (Inception v1)

---

## How It Works

### A. Convolution layer forward pass (mechanics)
1. **Input tensor**: typically \((N, C_{in}, H, W)\) in PyTorch conventions. (PyTorch `Conv2d`)
2. **Choose kernel size** \(k_H\times k_W\), stride, padding, dilation, groups.
3. **For each output channel** \(c_{out}\), slide the kernel over spatial positions \((h,w)\).
4. **At each position**, take the local input patch (across \(C_{in}\) channels, respecting `groups`) and compute a dot-product with the learned weights (cross-correlation per PyTorch docs), producing one scalar.
5. **Stack outputs** over all positions → one feature map per output channel; stack channels → output volume \((N, C_{out}, H_{out}, W_{out})\).
6. **Nonlinearity** (e.g., ReLU) is typically applied after conv in classic CNNs (VGG uses ReLU throughout; Inception uses ReLU throughout). (VGG; Inception v1)

### B. Max pooling forward pass (mechanics)
1. For each channel independently, define a window \(k_H\times k_W\) and stride.
2. For each output location \((h,w)\), take the maximum over the corresponding input window as in PyTorch’s formula. (PyTorch `MaxPool2d`)
3. Output shape follows the same arithmetic as strided conv (conv arithmetic Rel. 7).

### C. Residual block forward pass (ResNet)
1. Compute residual branch: \(F(x,\{W_i\})\) (a small stack of conv/BN/ReLU; deeper nets often use bottleneck 1×1,3×3,1×1). (ResNet)
2. Compute shortcut branch:
   - If shapes match: identity \(x\).
   - If shapes differ: projection \(W_s x\) (often 1×1 conv) to match dimensions. (ResNet Eq. 2)
3. Add: \(y = F(x)+x\) (or \(F(x)+W_sx\)).
4. Continue to next block; empirically this improves optimization and avoids the “degradation problem” seen in plain deep nets. (ResNet Fig. 4 discussion)

### D. Inception v1 module (multi-branch + bottlenecks)
1. Take input activation volume.
2. Run **parallel** transforms:
   - 1×1 conv
   - 1×1 reduce → 3×3 conv
   - 1×1 reduce → 5×5 conv
   - 3×3 max-pool → 1×1 “pool projection”
3. Concatenate outputs along channel dimension.
4. (Training only) optionally attach auxiliary classifier heads at intermediate modules (loss weight 0.3) to help gradient propagation/regularization; discard at inference. (Inception v1)

---

## Teaching Approaches

### Intuitive (no math): “stencils + heatmaps”
- Convolution filters are like small stencils you slide over an image; each filter produces a “heatmap” (feature map) showing where that pattern appears.
- Pooling shrinks the heatmap by summarizing neighborhoods (max = “keep the strongest evidence”).
- Residual connections let information flow around a block so deeper stacks don’t become harder to train; the block only needs to learn a *correction* to the identity. (CS231n intuition; ResNet rationale)

### Technical (with math): “shape arithmetic + residual reformulation”
- Use conv arithmetic \(o=\lfloor (i+2p-k)/s\rfloor+1\) to compute spatial sizes; emphasize per-axis independence. (conv arithmetic)
- Quote ResNet equations \(y=F(x)+x\) and \(F(x)=H(x)-x\) to explain why learning residuals can be easier than learning \(H\) directly. (ResNet)

### Analogy-based: “feature pipeline + multi-scale committee”
- VGG: repeated 3×3 layers act like building larger receptive fields via multiple small steps (two 3×3 ≈ 5×5 RF; three 3×3 ≈ 7×7 RF) with fewer parameters and more nonlinearities. (VGG)
- Inception: a “committee” of branches looks at multiple scales (1×1, 3×3, 5×5, pooling) and then votes by concatenation; 1×1 bottlenecks keep the committee cheap. (Inception v1)

---

## Common Misconceptions

1. **“Convolution layers are just fully-connected layers applied to images.”**  
   - **Why wrong:** FC layers connect every input pixel to every neuron; CNNs enforce *local receptive fields* and *weight sharing* across spatial positions, which is the core parameter-efficiency and inductive bias for images. (CS231n; Olah)  
   - **Correct model:** A conv filter is reused at every location; the same parameters detect the same pattern anywhere.

2. **“PyTorch `Conv2d` computes mathematical convolution (with kernel flipped).”**  
   - **Why wrong:** PyTorch explicitly states it applies valid 2D **cross-correlation**. (PyTorch `Conv2d`)  
   - **Correct model:** The learned kernel is applied without the mathematical convolution flip; in deep learning practice this distinction is absorbed into learned weights.

3. **“Pooling is required for translation invariance, and without pooling CNNs can’t work.”**  
   - **Why wrong:** Pooling is one common downsampling/aggregation method, but the sources here only justify pooling as a standard architectural component (e.g., VGG uses 2×2 stride-2 max-pool; Inception uses pooling branches). It’s not a logical requirement for CNNs to function. (VGG; Inception v1; CS231n)  
   - **Correct model:** Pooling is a design choice for spatial downsampling and robustness; strided convolutions can also downsample (shape arithmetic treats them similarly).

4. **“If a deeper network performs worse, it’s just overfitting.”**  
   - **Why wrong:** ResNet documents the **degradation problem**: deeper *plain* nets can have **higher training error**, indicating an optimization issue, not just generalization. (ResNet Intro/Fig.4)  
   - **Correct model:** Depth can make optimization harder; residual connections change the optimization landscape by making identity mappings easy.

5. **“Inception’s 1×1 convolutions are only for adding nonlinearity.”**  
   - **Why wrong:** Inception v1 emphasizes 1×1 convs as **dimension reduction** before expensive 3×3/5×5 convs and as **pool projection** to control compute/parameter growth. (Inception v1)  
   - **Correct model:** 1×1 convs are primarily a *bottleneck/projection* tool in Inception v1’s efficiency design.

---

## Worked Examples

### 1) Output shape arithmetic (conv + pool) with concrete numbers
**Task:** Student asks “What is the output size after this conv/pool?”

**Example A (conv):** input \(H=W=32\), kernel \(k=5\), stride \(s=1\), padding \(p=2\).  
Using \(o=\left\lfloor\frac{i+2p-k}{s}\right\rfloor+1\):  
\[
o=\left\lfloor\frac{32+4-5}{1}\right\rfloor+1 = 32
\]
So spatial size stays 32×32 (“same” behavior for odd kernel with \(p=\lfloor k/2\rfloor\)). (conv arithmetic Rel. 6 + Rel. 3)

**Example B (pool):** input \(i=32\), window \(k=2\), stride \(s=2\), no padding.  
\[
o=\left\lfloor\frac{32-2}{2}\right\rfloor+1 = 16
\]
So 32×32 → 16×16 after 2×2 stride-2 max pool. (conv arithmetic Rel. 7; VGG uses 2×2 stride-2 max-pool)

### 2) Minimal PyTorch snippet to verify shapes (Conv2d + MaxPool2d)
```python
import torch
import torch.nn as nn

x = torch.randn(4, 3, 32, 32)  # (N,C,H,W)

conv = nn.Conv2d(in_channels=3, out_channels=16, kernel_size=5, stride=1, padding=2)
pool = nn.MaxPool2d(kernel_size=2, stride=2)

y = conv(x)
z = pool(y)

print(x.shape)  # torch.Size([4, 3, 32, 32])
print(y.shape)  # torch.Size([4, 16, 32, 32])
print(z.shape)  # torch.Size([4, 16, 16, 16])
```
**Tutor notes:** If a student expects padding to use zeros for max-pool, quote PyTorch: max-pool padding is \(-\infty\). (PyTorch `MaxPool2d`)

### 3) Residual block “identity is easy” micro-check (conceptual)
If a residual block outputs \(y=F(x)+x\), then setting weights so \(F(x)=0\) yields \(y=x\) (identity). ResNet’s claim is that this is easier than forcing a deep plain stack to approximate identity directly. (ResNet Sec. 3.1)

---

## Comparisons & Trade-offs

| Idea | What it changes | Why it helps (per sources) | Costs / caveats | When to choose |
|---|---|---|---|---|
| **VGG-style 3×3 stacks** | Replace large kernels with multiple 3×3 convs | Same effective receptive field with fewer params (e.g., 27\(C^2\) vs 49\(C^2\) for 7×7) + more nonlinearities | Deeper stack increases layer count/compute | When you want simple, uniform design and strong ImageNet baselines (VGG) |
| **Inception v1 multi-branch** | Parallel 1×1/3×3/5×5/pool then concat | Multi-scale receptive fields; 1×1 reductions prevent compute blow-up; strong accuracy with ~1.5B MAC budget and ~12× fewer params than AlexNet | More complex module design; tuning branch widths | When compute/params are constrained but you want multi-scale features (Inception v1) |
| **Plain deep nets vs ResNets** | Add skip connections \(y=F(x)+x\) | Fixes degradation: deeper residual nets optimize better than shallower ones; enables very deep nets (152 layers) with strong ImageNet results | Slight overhead; need projection shortcuts when dims change | When depth is desired and optimization becomes difficult (ResNet) |
| **MaxPool vs strided conv (shape-wise)** | Both downsample spatially | Output-size arithmetic is the same form; pooling is explicit max aggregation | Pooling discards within-window detail; max-pool padding is \(-\infty\) in PyTorch | Use max-pool when you want explicit local max aggregation; use stride conv when you want learned downsampling (pooling/conv arithmetic sources) |

---

## Prerequisite Connections

- **Linear algebra (dot products)**: convolution/cross-correlation is repeated dot products between a kernel and local patches. (CS231n; PyTorch `Conv2d`)
- **Tensor shapes & indexing**: understanding \((N,C,H,W)\) and how stride/padding change \(H,W\) is required to reason about feature maps. (conv arithmetic; PyTorch docs)
- **Nonlinear activations (ReLU)**: VGG/Inception use ReLU throughout; stacking convs relies on nonlinearities between them. (VGG; Inception v1)
- **Optimization intuition (training vs validation error)**: needed to understand ResNet’s “degradation problem” as an optimization issue (training error increases). (ResNet)

---

## Socratic Question Bank

1. **If you replace a fully-connected first layer on a 224×224×3 image with a 3×3 conv, what structural assumption did you add?**  
   *Good answer:* locality + weight sharing; same detector applied across positions. (CS231n/Olah framing)

2. **Given \(i=32, k=3, s=2, p=1\), what is \(o\) and why is there a floor?**  
   *Good answer:* \(o=\lfloor(32+2-3)/2\rfloor+1=\lfloor31/2\rfloor+1=15+1=16\); floor because windows must fit discretely. (conv arithmetic)

3. **What does a single channel in a conv layer output represent?**  
   *Good answer:* a feature map: spatial responses of one learned filter across the image. (CS231n)

4. **Why can a deeper plain network have higher training error than a shallower one?**  
   *Good answer:* degradation/optimization difficulty, not just overfitting; ResNet shows this empirically. (ResNet)

5. **In \(y=F(x)+x\), what happens if the best mapping is identity?**  
   *Good answer:* set \(F(x)\to 0\); residual formulation makes identity easy. (ResNet)

6. **Why does Inception put 1×1 conv before 3×3/5×5?**  
   *Good answer:* dimension reduction to control compute/parameters; also pool projection. (Inception v1)

7. **What’s the difference between “same padding” in conv arithmetic and PyTorch `padding='same'`?**  
   *Good answer:* arithmetic says choose \(p=\lfloor k/2\rfloor\) for stride 1 and odd \(k\) to keep size; PyTorch notes `'same'` doesn’t support stride ≠ 1. (conv arithmetic; PyTorch `Conv2d`)

8. **MaxPool padding uses what value in PyTorch, and why does that matter?**  
   *Good answer:* \(-\infty\); ensures padded values never become maxima. (PyTorch `MaxPool2d`)

---

## Likely Student Questions

**Q: “How do I compute the output height/width of a conv layer with stride and padding?”**  
→ **A:** Use \(o=\left\lfloor\frac{i+2p-k}{s}\right\rfloor+1\) per axis (height and width separately), where \(i\)=input size, \(k\)=kernel size, \(s\)=stride, \(p\)=padding. (Dumoulin & Visin, Rel. 6)

**Q: “Does PyTorch Conv2d do convolution or cross-correlation?”**  
→ **A:** PyTorch `torch.nn.Conv2d` applies valid 2D **cross-correlation** (not the flipped-kernel mathematical convolution). (PyTorch `Conv2d`)

**Q: “What exactly is max pooling computing?”**  
→ **A:** For each output location, it takes the maximum over a \(k_H\times k_W\) window:  
\(out(N_i,C_j,h,w)=\max_{m}\max_{n} input(N_i,C_j,stride[0]\cdot h+m, stride[1]\cdot w+n)\). Padding (if any) is \(-\infty\). (PyTorch `MaxPool2d`)

**Q: “Why did VGG use stacks of 3×3 convs instead of 7×7?”**  
→ **A:** VGG argues stacked 3×3 convs achieve the same effective receptive field with fewer parameters and more nonlinearities; e.g., three 3×3 layers have \(27C^2\) weights vs \(49C^2\) for one 7×7 (81% more). (VGG Sec. 2.3)

**Q: “What problem do residual connections solve?”**  
→ **A:** ResNet identifies a **degradation problem** where deeper *plain* nets can have higher **training error** than shallower ones; residual blocks use \(y=F(x)+x\) to make optimization easier and enable very deep nets. (He et al., ResNet Intro/Fig.4/Eq.1)

**Q: “When do ResNets use a 1×1 projection in the skip path?”**  
→ **A:** When dimensions differ, ResNet uses \(y=F(x)+W_sx\) where \(W_s\) is a linear projection (typically 1×1 conv) mainly for dimension matching. (ResNet Eq. 2)

**Q: “What is an Inception module and why the parallel branches?”**  
→ **A:** Inception v1 runs parallel 1×1, 3×3, 5×5, and pooling branches and concatenates channels; it’s motivated by multi-scale processing, and uses 1×1 convs as dimension reduction before expensive convs to keep compute manageable. (Inception v1 Sec. 4)

**Q: “What are the headline ImageNet numbers for AlexNet/VGG/GoogLeNet/ResNet?”**  
→ **A:** AlexNet: top-1 error 39.7%, top-5 error 18.9%, 60M params (AlexNet abstract). VGG best single: 25.9% top-1 / 8.0% top-5 (VGG). Inception v1: 6.67% top-5 (7-model ensemble), ~1.5B multiply-adds, ~12× fewer params than AlexNet (Inception v1). ResNet: 152-layer single-model top-5 val 4.49%, ensemble top-5 test 3.57% (ResNet).

---

## Available Resources

### Videos
- [Lecture 5: Convolutional Neural Networks](https://youtube.com/watch?v=YRhxdVk_sIs) — **Surface when:** student wants a canonical walkthrough of conv/stride/padding/pooling/feature maps and classic CNN architecture patterns (CS231n-style).
- [Let’s build GPT: from scratch, in code, spelled out.](https://youtube.com/watch?v=kCc8FmEb1nY) — **Surface when:** student asks about residual connections in modern deep learning more broadly (bridge from ResNet skips to Transformer “Add & Norm” patterns).
- [Video (wjZofJX0v4M)](https://youtube.com/watch?v=wjZofJX0v4M) — **Surface when:** student wants a high-level intuition for residual connections and deep architectures in the broader Transformer era (contextual motivation).

### Articles & Tutorials
- [Conv Nets: A Modular Perspective (Olah, 2014)](https://colah.github.io/posts/2014-07-Conv-Nets-Modular/) — **Surface when:** student is stuck on *why* convolution/weight sharing makes sense; needs intuition from “local symmetry” and modular composition.
- [CS231n: Convolutional Neural Networks](https://cs231n.github.io/convolutional-networks/) — **Surface when:** student needs a precise reference for activation volumes, layer patterns, and architecture case studies (AlexNet/VGG/GoogLeNet/ResNet).
- [ImageNet Classification with Deep Convolutional Neural Networks (AlexNet abstract)](https://papers.nips.cc/paper/2012/hash/c399862d3b9d6b76c8436e924a68c45b-Abstract.html) — **Surface when:** student asks “what changed in 2012?” or wants the original ImageNet error numbers and model scale.
- [Machine Learning with PyTorch and Scikit-Learn (code repo)](https://github.com/rasbt/machine-learning-book) — **Surface when:** student wants runnable PyTorch CNN examples and broader training/evaluation scaffolding.
- [The Illustrated Transformer (Alammar)](https://jalammar.github.io/illustrated-transformer/) — **Surface when:** student asks about residual connections as a general deep learning pattern (skip connections + normalization), to connect CNN ResNets to Transformers.

---

## Visual Aids

![ConvNet pipeline: INPUT→CONV→RELU→POOL→FC for CIFAR-10. (cs231n)](/api/wiki-images/cnns/images/cs231n-convolutional-networks_002.jpeg)  
**Show when:** student asks “what’s the standard CNN stack?” or confuses feature maps vs classifier head.

![Full 2D CNN architecture with two stacked convolutional layers. (Olah, 2014)](/api/wiki-images/cnns/images/colah-posts-2014-07-Conv-Nets-Modular_001.png)  
**Show when:** student needs a modular picture of stacked conv layers producing progressively more abstract representations.

![Neuron group A detecting local features in a 1D audio signal. (Olah, 2014)](/api/wiki-images/cnns/images/colah-posts-2014-07-Conv-Nets-Modular_003.png)  
**Show when:** student doesn’t “buy” locality/weight sharing; use 1D analogy to make translational symmetry obvious.

![AlexNet ImageNet results: correct and near-miss classifications shown. (Krizhevsky et al., 2012)](/api/wiki-images/cnns/images/colah-posts-2014-07-Conv-Nets-Modular_014.png)  
**Show when:** student asks why top-5 accuracy/error is used; illustrate “near miss” predictions.

---

## Key Sources

- [CS231n: Convolutional Neural Networks](https://cs231n.github.io/convolutional-networks/) — most comprehensive reference for CNN mechanics, activation volumes, and architecture patterns.
- [Deep Residual Learning for Image Recognition (ResNet)](https://arxiv.org/abs/1512.03385) — authoritative source for residual block equations and the degradation/optimization motivation plus ImageNet depth results.
- [Very Deep Convolutional Networks for Large-Scale Image Recognition (VGG)](https://arxiv.org/abs/1409.1556) — canonical rationale and numbers for stacking 3×3 convs; ImageNet error tables and training/testing details.
- [Going Deeper with Convolutions (Inception v1 / GoogLeNet)](https://arxiv.org/abs/1409.4842) — definitive description of Inception modules (multi-branch + 1×1 bottlenecks) and ILSVRC14 top-5 results/efficiency targets.
- [A guide to convolution arithmetic for deep learning](https://arxiv.org/pdf/1603.07285.pdf) — precise, tutor-friendly formulas for conv/pool (and dilation/transposed conv) output sizes.