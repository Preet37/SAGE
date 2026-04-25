## Core Definitions

**Transformer block**  
Vaswani et al. (2017) introduce the Transformer as a stack of repeated layers built around attention mechanisms rather than recurrence or convolutions (“Attention Is All You Need,” https://arxiv.org/abs/1706.03762). In the common encoder-style block shown in Weng’s and Alammar’s diagrams, each layer has (at least) two sublayers—(1) self-attention and (2) a position-wise feed-forward network—each wrapped with a residual (“skip”) connection and a normalization step (“Add & Norm”). PyTorch’s `torch.nn.TransformerEncoderLayer` summarizes this as “made up of self-attn and feedforward network” and exposes a switch `norm_first` to choose whether normalization is applied before or after each sublayer (PyTorch docs: https://docs.pytorch.org/docs/stable/generated/torch.nn.TransformerEncoderLayer.html).

**Residual connections (skip connections)**  
In the canonical Transformer encoder diagrams (e.g., Alammar’s “Residual connection and layer normalization in a Transformer encoder layer”), each sublayer output is added back to the sublayer input (“Add”) before normalization (“Norm”). Mechanically, this implements the pattern “output = x + sublayer(x)” (with normalization either before or after depending on architecture), ensuring an identity path exists through the network even if the sublayer learns small updates. (Visual references: Alammar/Weng/UvA diagrams listed in “Visual Aids.”)

**Layer normalization (LayerNorm)**  
RMSNorm paper (Zhang & Sennrich, 2019) quotes LayerNorm as normalizing a vector by subtracting its mean and dividing by its standard deviation, then applying a learnable per-dimension gain (and optionally bias) (https://arxiv.org/abs/1910.07467). In Transformer blocks, LayerNorm is used in the “Add & Norm” step to stabilize activations/gradients across depth; PyTorch exposes `layer_norm_eps` and `bias` for the LayerNorm modules in `TransformerEncoderLayer` (PyTorch docs link above).

**RMSNorm (Root Mean Square Layer Normalization)**  
Zhang & Sennrich (2019) define RMSNorm as a LayerNorm variant that *removes mean-centering* and normalizes only by the root-mean-square (RMS) magnitude of the vector, then applies a learnable gain (https://arxiv.org/abs/1910.07467). The paper’s motivation is that LayerNorm’s *re-scaling invariance* is the key benefit, while *re-centering invariance* may be unnecessary; RMSNorm reduces compute overhead and is reported to speed up Transformer training/inference while maintaining comparable quality.

**Feed-forward network (FFN; position-wise MLP)**  
Vaswani-style Transformer layers include a position-wise feed-forward network applied independently to each token position after attention (as depicted in Weng/Alammar/UvA encoder block diagrams). Shazeer (2020) formalizes the baseline Transformer FFN as two linear projections with an elementwise nonlinearity in between: \(\phi(xW_1+b_1)W_2+b_2\) (https://arxiv.org/abs/2002.05202). “Position-wise” means the same FFN weights are used at every sequence position.

**SwiGLU (a GLU-family FFN variant)**  
Shazeer (2020) defines SwiGLU as a gated linear unit variant for Transformer FFNs: \(\mathrm{Swish}(xW+b)\odot(xV+c)\), where \(\mathrm{Swish}(z)=z\cdot\sigma(\beta z)\) (typically \(\beta=1\)) (https://arxiv.org/abs/2002.05202). Compared to a standard 2-matrix FFN, GLU-family FFNs use (approximately) 3 matrices, so the paper recommends reducing the hidden width by a factor \(2/3\) to match parameter/compute budgets.

---

## Key Formulas & Empirical Results

### LayerNorm (as quoted in RMSNorm paper)
From Zhang & Sennrich (2019), for pre-activation/summed inputs \(a\in\mathbb{R}^n\):  
\[
\bar a_i=\frac{a_i-\mu}{\sigma}\, g_i,\quad y=f(\bar a + b)
\]
\[
\mu=\frac{1}{n}\sum_{i=1}^n a_i,\quad \sigma=\sqrt{\frac{1}{n}\sum_{i=1}^n (a_i-\mu)^2}
\]
- \(g\in\mathbb{R}^n\): learnable gain (init to 1 in the paper’s description)  
- \(b\): bias  
- \(f(\cdot)\): elementwise nonlinearity  
**Supports:** exact definition to contrast with RMSNorm.  
Source: https://arxiv.org/abs/1910.07467

### RMSNorm (exact equation)
\[
\bar a_i=\frac{a_i}{\mathrm{RMS}(a)}\, g_i,\quad \mathrm{RMS}(a)=\sqrt{\frac{1}{n}\sum_{i=1}^n a_i^2}
\]
Paper note: if \(\mu=0\), RMSNorm equals LayerNorm.  
**Supports:** “RMS-only normalization; no mean-centering.”  
Source: https://arxiv.org/abs/1910.07467

### RMSNorm invariance to rescaling
Key property used in the paper: \(\mathrm{RMS}(\alpha x)=\alpha\,\mathrm{RMS}(x)\), implying invariance to global rescaling of weights/inputs (e.g., scaling \(W\) by \(\delta\) can leave normalized output unchanged).  
**Supports:** why RMSNorm can stabilize training similarly to LayerNorm while being cheaper.  
Source: https://arxiv.org/abs/1910.07467

### RMSNorm speedups (reported)
Zhang & Sennrich (2019) report RMSNorm reduces running time vs LayerNorm by **7%–64%** across models/tasks; for Transformer specifically **~7%–9%** speedup with comparable BLEU (paper Section 6/Table 4 as summarized in the card).  
**Supports:** “why use RMSNorm in Transformers?” (efficiency).  
Source: https://arxiv.org/abs/1910.07467

### Pre-LN vs Post-LN vs Peri-LN (exact layer equations)
From the Peri-LN analysis paper (https://arxiv.org/html/2502.02732v1):
- **Post-LN:** \(x_{l+1}=\mathrm{LN}(x_l+F_l(x_l))\)  
- **Pre-LN:** \(x_{l+1}=x_l+F_l(\mathrm{LN}(x_l))\)  
- **Peri-LN (described):** \(u_l=\mathrm{LN}(x_l)\), \(y_l=F_l(u_l)\), \(v_l=\mathrm{LN}(y_l)\), \(x_{l+1}=x_l+v_l\)  
Where \(F_l\) is an Attention or MLP sublayer; LN can be LayerNorm or RMSNorm.  
**Supports:** precise “where does normalization go?” discussion.

### Peri-LN empirical benchmark numbers (Table 2 excerpt)
Peri-LN results reported (trained on 30B tokens; 5 seeds; RMSNorm primarily; Megatron-LM pipeline per card summary):
- **125M:** Avg **51.57**, Loss **3.34**  
- **350M:** Avg **56.55**, Loss **3.18**  
- **1.3B:** Avg **58.56**, Loss **3.11**  
(With task breakdowns in the card.)  
**Supports:** empirical evidence that adding output normalization can improve stability/quality.  
Source: https://arxiv.org/html/2502.02732v1

### Baseline FFN and GLU-family FFN formulas + width scaling
From Shazeer (2020) (https://arxiv.org/abs/2002.05202):
- Baseline FFN: \(\mathrm{FFN}(x)=\phi(xW_1+b_1)W_2+b_2\)  
- GLU: \(\sigma(xW+b)\odot(xV+c)\)  
- **SwiGLU:** \(\mathrm{Swish}(xW+b)\odot(xV+c)\), \(\mathrm{Swish}(z)=z\cdot\sigma(\beta z)\)  
- Parameter matching: baseline \(\approx 2d_{\text{model}}d_{\text{ff}}\); GLU-FFN \(\approx 3d_{\text{model}}d_{\text{ff}}\). To match budget:  
  \[
  d_{\text{ff,GLU}}=\tfrac{2}{3}d_{\text{ff,base}}
  \]
**Supports:** “what is SwiGLU exactly?” and “why is FFN width different?”

### Stable softmax trick (numerical stability)
Jarbus shows stable softmax computed as:
- subtract max: `x - np.max(x)` before exponentiating  
**Supports:** why attention implementations subtract max (esp. float16) to avoid overflow.  
Source: https://jarbus.net/blog/numerical-stability-in-flash-attention/

### PyTorch `TransformerEncoderLayer` implementation defaults (API-level)
PyTorch docs list constructor signature and key defaults (2.11 page; similar in 2.8/2.9):
- `dim_feedforward=2048`, `dropout=0.1`, `activation=relu`, `layer_norm_eps=1e-5`, `batch_first=False`, `norm_first=False`, `bias=True`  
**Supports:** quick “what are the defaults?” questions; also `norm_first` toggles pre-norm vs post-norm behavior.  
Source: https://docs.pytorch.org/docs/stable/generated/torch.nn.TransformerEncoderLayer.html

---

## How It Works

### A single encoder-style Transformer block (mechanical sequence)
Use this when a student asks “walk me through one block.”

1. **Input hidden states**  
   Start with \(x\) shaped like `(batch, seq, d_model)` (or `(seq, batch, d_model)` depending on framework; PyTorch has `batch_first`).

2. **(Optional) Normalize before sublayer (Pre-LN / `norm_first=True`)**  
   Compute \(x_{\text{norm}}=\mathrm{LN}(x)\) (LayerNorm or RMSNorm depending on architecture).  
   - Pre-LN equation form (from https://arxiv.org/html/2502.02732v1):  
     \(x_{l+1}=x_l+F_l(\mathrm{LN}(x_l))\)

3. **Self-attention sublayer**  
   Compute self-attention output \(a = \text{SelfAttn}(x_{\text{norm}})\) (or \(\text{SelfAttn}(x)\) in Post-LN).  
   - Internally, attention uses softmax; stable implementations subtract the max logit before exponentiation (jarbus softmax note).

4. **Residual add**  
   Add the sublayer output back: \(x \leftarrow x + a\).  
   (This is the “Add” in “Add & Norm” shown in Alammar/Weng diagrams.)

5. **(Optional) Normalize after sublayer (Post-LN / `norm_first=False`)**  
   Post-LN equation form (from https://arxiv.org/html/2502.02732v1):  
   \(x_{l+1}=\mathrm{LN}(x_l+F_l(x_l))\)

6. **Feed-forward (position-wise MLP) sublayer**  
   Apply the same FFN to each token position independently. Baseline formula (Shazeer 2020):  
   \(\mathrm{FFN}(x)=\phi(xW_1+b_1)W_2+b_2\)

7. **Residual add (again)**  
   \(x \leftarrow x + \mathrm{FFN}(\cdot)\) (with normalization before/after depending on Pre-LN/Post-LN).

8. **Repeat for many layers**  
   Stacking these blocks yields the deep Transformer encoder/decoder stacks shown in Weng/Alammar.

### SwiGLU FFN inside a Transformer block (drop-in replacement)
When the FFN is SwiGLU (Shazeer 2020):
1. Compute two projections: \(u=xW+b\), \(v=xV+c\)  
2. Gate with Swish: \(\mathrm{Swish}(u)\odot v\)  
3. (In practice, a final projection back to \(d_{\text{model}}\) is used in Transformer FFNs; the paper’s key definitional piece is the gated product form.)  
4. If matching baseline FFN compute/params, set \(d_{\text{ff}}\) to \(\tfrac{2}{3}\) of the baseline FFN hidden size.

### Normalization placement variants (what changes mechanically)
From https://arxiv.org/html/2502.02732v1:
- **Post-LN:** normalize *after* residual addition; tends to keep activation variance stable but can weaken gradients in deep nets (paper’s stated rationale).  
- **Pre-LN:** normalize *before* the sublayer; improves gradient flow early but can allow unnormalized residual updates to accumulate (variance growth).  
- **Peri-LN:** normalize both the input to the sublayer and the sublayer output before adding to residual:  
  \(u_l=\mathrm{LN}(x_l)\), \(y_l=F_l(u_l)\), \(v_l=\mathrm{LN}(y_l)\), \(x_{l+1}=x_l+v_l\)

---

## Teaching Approaches

### Intuitive (no math)
- **Block as “two skills + stabilizers”:** each layer has (1) attention to mix information across tokens and (2) an MLP to transform each token’s features; residual connections keep an “identity highway” so the model can refine rather than rewrite; normalization keeps the scale of activations well-behaved across depth.  
- **Norm placement as “where you clean the signal”:** Pre-LN cleans inputs before each operation; Post-LN cleans after you add the update; Peri-LN cleans both before and after to prevent residual spikes (per the Peri-LN paper’s motivation).

### Technical (with math)
- Quote exact Pre-LN/Post-LN equations from https://arxiv.org/html/2502.02732v1 and ask the student to identify where gradients can flow unchanged (the residual path) and where normalization sits relative to \(F_l\).  
- For RMSNorm vs LayerNorm, quote the exact equations from https://arxiv.org/abs/1910.07467 and highlight “mean-centering removed” + RMS scaling invariance.

### Analogy-based
- **Residuals as “version control”:** each sublayer proposes a diff/patch; the residual add applies the patch to the current representation rather than replacing it.  
- **Normalization as “automatic volume control”:** it prevents any layer from turning the signal too loud/quiet; RMSNorm is like controlling volume by overall energy (RMS) without shifting the baseline (mean).

---

## Common Misconceptions

1. **“A Transformer block is just attention; the FFN is optional fluff.”**  
   **Why wrong:** Source diagrams (Weng/Alammar/UvA) and PyTorch’s `TransformerEncoderLayer` explicitly define the layer as *self-attn + feedforward network*. Shazeer (2020) treats FFN choice (ReLU/GELU/GLU variants) as a major modeling decision with measurable perplexity differences.  
   **Correct model:** A standard block has *two* core compute sublayers: attention (token mixing) and FFN (per-token feature transformation), each wrapped with residual + norm.

2. **“LayerNorm and RMSNorm are basically the same; both subtract the mean.”**  
   **Why wrong:** RMSNorm explicitly *removes mean-centering*; it divides by RMS only (https://arxiv.org/abs/1910.07467).  
   **Correct model:** LayerNorm uses mean and variance; RMSNorm uses only RMS magnitude. They coincide only under special conditions (paper notes: if \(\mu=0\)).

3. **“Pre-LN vs Post-LN is just a coding style choice; it doesn’t affect training.”**  
   **Why wrong:** The Peri-LN paper (https://arxiv.org/html/2502.02732v1) analyzes variance/gradient stability differences: Post-LN can weaken gradients in deep nets; Pre-LN can allow variance to accumulate and lead to “massive activations”; Peri-LN adds output normalization to damp spikes.  
   **Correct model:** Norm placement changes the statistics of residual updates and gradient flow; it can materially affect stability and convergence.

4. **“SwiGLU is just ‘GELU but renamed’; it doesn’t change the FFN structure.”**  
   **Why wrong:** Shazeer (2020) defines SwiGLU as a *gated* structure with two projections and an elementwise product, not a single nonlinearity in a 2-layer MLP (https://arxiv.org/abs/2002.05202).  
   **Correct model:** SwiGLU changes the FFN from “nonlinearity then projection” to “(nonlinear gate) ⊙ (linear values),” increasing matrix count and affecting width/compute trade-offs.

5. **“Softmax overflow/NaNs are rare; subtracting max is unnecessary.”**  
   **Why wrong:** Jarbus demonstrates float16 overflow in naive softmax where `exp(15)` can produce NaNs, while subtracting `max(x)` avoids exponentiating large numbers (https://jarbus.net/blog/numerical-stability-in-flash-attention/).  
   **Correct model:** Stable softmax (subtract max) is a standard numerical stability technique, especially important in low precision.

---

## Worked Examples

### Example 1 — Stable vs unstable softmax (float16 overflow)
Use when a student asks “why do we subtract max in attention softmax?”

```python
import numpy as np

def unstable_softmax(x):
    fx = np.exp(x)
    return fx / np.sum(fx)

def stable_softmax(x):
    z = x - np.max(x)
    ez = np.exp(z)
    return ez / np.sum(ez)

a16 = np.array([6.0, -3.0, 15.0], dtype=np.float16)

print("unstable:", unstable_softmax(a16))
print("stable:  ", stable_softmax(a16))
```

**What to point out (per jarbus):**
- Unstable version can produce `nan` in float16 due to overflow in `exp(15)`.
- Stable version avoids exponentiating large values by shifting logits by their maximum; the softmax result is unchanged mathematically because the same shift appears in numerator and denominator.

### Example 2 — PyTorch `TransformerEncoderLayer` norm placement toggle
Use when a student asks “what does `norm_first` do?” or “is this pre-norm or post-norm?”

```python
import torch
import torch.nn as nn

x = torch.rand(32, 10, 512)  # (batch, seq, d_model)

post_ln = nn.TransformerEncoderLayer(d_model=512, nhead=8, batch_first=True, norm_first=False)
pre_ln  = nn.TransformerEncoderLayer(d_model=512, nhead=8, batch_first=True, norm_first=True)

y_post = post_ln(x)
y_pre  = pre_ln(x)

print(y_post.shape, y_pre.shape)
```

**Tutor notes (source: PyTorch docs):**
- `norm_first=False` corresponds to “layer norm is done after” attention/FFN (post-norm behavior).
- `norm_first=True` corresponds to “layer norm is done prior to” attention/FFN (pre-norm behavior).
- Defaults include `dim_feedforward=2048`, `dropout=0.1`, `activation=relu`, `layer_norm_eps=1e-5`, `bias=True` (https://docs.pytorch.org/docs/stable/generated/torch.nn.TransformerEncoderLayer.html).

---

## Comparisons & Trade-offs

| Choice | Definition (sourced) | Pros (sourced) | Cons / Risks (sourced) | When to choose |
|---|---|---|---|---|
| **LayerNorm** | Mean-center + variance normalize; learnable gain (and bias) (https://arxiv.org/abs/1910.07467) | Standard, widely used; provides re-centering + re-scaling invariances (RMSNorm paper framing) | More compute than RMSNorm (RMSNorm paper reports runtime reductions with RMSNorm) | When matching classic implementations or when mean-centering is desired |
| **RMSNorm** | Normalize by RMS only; no mean-centering; learnable gain (https://arxiv.org/abs/1910.07467) | Reported runtime reduction **7%–64%** across tasks; **~7%–9%** on Transformer with comparable BLEU; keeps rescaling invariance | Removes re-centering invariance (paper argues it may be dispensable) | When efficiency matters and RMSNorm is known to work in the target architecture |
| **Post-LN** | \(x_{l+1}=\mathrm{LN}(x_l+F_l(x_l))\) (https://arxiv.org/html/2502.02732v1) | Paper notes it keeps activation variance ~constant | Paper notes it can weaken gradients in deep nets → slow convergence/vanishing | Shallow models or when following original “Add & Norm” style |
| **Pre-LN** | \(x_{l+1}=x_l+F_l(\mathrm{LN}(x_l))\) (https://arxiv.org/html/2502.02732v1) | Paper notes improved early gradient flow | Paper reports variance can accumulate and become exponential (“massive activations”) | Common modern default; watch for stability at scale |
| **Peri-LN** | LN on both module input and output before residual add (https://arxiv.org/html/2502.02732v1) | Fewer gradient-norm spikes; moderates variance growth; reported benchmark/loss numbers in Table 2 excerpt | Extra normalization ops (implied overhead) | When training instability (spikes/blow-ups) is a recurring issue |

---

## Prerequisite Connections

- **Softmax and numerical stability** → needed to understand why attention implementations subtract max logits (jarbus stable softmax).  
- **Vector normalization (mean/variance vs RMS)** → needed to distinguish LayerNorm vs RMSNorm equations (https://arxiv.org/abs/1910.07467).  
- **Basic MLP structure (two linear layers + activation)** → needed to parse baseline FFN and why GLU-family adds a gate (https://arxiv.org/abs/2002.05202).  
- **Residual/skip connections concept** → needed to interpret “Add & Norm” diagrams and why stacking blocks works (Alammar/Weng/UvA diagrams).

---

## Socratic Question Bank

1. **If you remove the FFN sublayer but keep attention, what capability does the layer lose?**  
   *Good answer:* attention mixes information across tokens, but FFN provides per-token feature transformation; standard blocks include both (PyTorch layer definition; Shazeer FFN formulas).

2. **In the Pre-LN equation \(x_{l+1}=x_l+F_l(\mathrm{LN}(x_l))\), where is the “identity path,” and why might that help gradients?**  
   *Good answer:* the residual add provides a direct path from \(x_l\) to \(x_{l+1}\); normalization is inside \(F_l\), so gradients can flow around \(F_l\).

3. **What exact operation does RMSNorm remove compared to LayerNorm?**  
   *Good answer:* mean subtraction; RMSNorm divides by RMS only (quote Eq. 4 vs Eq. 2–3 from RMSNorm paper).

4. **Why does subtracting \(\max(x)\) not change softmax outputs?**  
   *Good answer:* the same constant shift appears in numerator and denominator and cancels; it prevents overflow (jarbus).

5. **SwiGLU uses two projections and an elementwise product. What does that imply about parameter count vs a baseline FFN?**  
   *Good answer:* ~3 matrices vs ~2; to match compute/params, reduce hidden size by factor \(2/3\) (Shazeer 2020).

6. **If a model shows gradient-norm spikes during training, which norm placement variant is explicitly proposed to reduce spikes in the provided sources? Why?**  
   *Good answer:* Peri-LN; output LN damps residual spikes and keeps gradients more bounded (Peri-LN paper observations).

7. **Given PyTorch’s `TransformerEncoderLayer`, which flag would you toggle to switch between pre-norm and post-norm behavior?**  
   *Good answer:* `norm_first` (PyTorch docs).

8. **When might RMSNorm equal LayerNorm according to the RMSNorm paper?**  
   *Good answer:* when the mean \(\mu=0\) (paper statement).

---

## Likely Student Questions

**Q: What’s the exact RMSNorm equation, and how is it different from LayerNorm?**  
→ **A:** RMSNorm (Zhang & Sennrich, 2019) is \(\bar a_i=\frac{a_i}{\mathrm{RMS}(a)}g_i\) with \(\mathrm{RMS}(a)=\sqrt{\frac{1}{n}\sum_i a_i^2}\); it *does not subtract the mean*. LayerNorm uses \(\bar a_i=\frac{a_i-\mu}{\sigma}g_i\) with \(\mu=\frac{1}{n}\sum_i a_i\) and \(\sigma=\sqrt{\frac{1}{n}\sum_i(a_i-\mu)^2}\). Source: https://arxiv.org/abs/1910.07467

**Q: Why do many Transformers use RMSNorm instead of LayerNorm? Any concrete speed numbers?**  
→ **A:** The RMSNorm paper reports reduced running time vs LayerNorm by **7%–64%** across models/tasks, and for Transformer specifically **~7%–9%** speedup with comparable BLEU (as summarized from Section 6/Table 4). Source: https://arxiv.org/abs/1910.07467

**Q: What’s the difference between Pre-LN and Post-LN in one equation?**  
→ **A:** Post-LN: \(x_{l+1}=\mathrm{LN}(x_l+F_l(x_l))\). Pre-LN: \(x_{l+1}=x_l+F_l(\mathrm{LN}(x_l))\). Source: https://arxiv.org/html/2502.02732v1

**Q: What is Peri-LN exactly (step-by-step)?**  
→ **A:** Peri-LN applies normalization to both the sublayer input and the sublayer output: \(u_l=\mathrm{LN}(x_l)\), \(y_l=F_l(u_l)\), \(v_l=\mathrm{LN}(y_l)\), \(x_{l+1}=x_l+v_l\). Source: https://arxiv.org/html/2502.02732v1

**Q: What are PyTorch `TransformerEncoderLayer` defaults, and how do I switch pre-norm vs post-norm?**  
→ **A:** Defaults include `dim_feedforward=2048`, `dropout=0.1`, `activation=relu`, `layer_norm_eps=1e-5`, `norm_first=False` (post-norm), `bias=True`. Set `norm_first=True` for pre-norm behavior. Source: https://docs.pytorch.org/docs/stable/generated/torch.nn.TransformerEncoderLayer.html

**Q: What is SwiGLU (exact formula), and why does it change FFN width?**  
→ **A:** SwiGLU (Shazeer, 2020) is \(\mathrm{Swish}(xW+b)\odot(xV+c)\) with \(\mathrm{Swish}(z)=z\cdot\sigma(\beta z)\) (typically \(\beta=1\)). GLU-family FFNs use ~3 matrices vs ~2 in baseline FFN, so to match parameter/compute budget the paper recommends \(d_{\text{ff,GLU}}=\tfrac{2}{3}d_{\text{ff,base}}\). Source: https://arxiv.org/abs/2002.05202

**Q: Why do attention implementations subtract the max before softmax?**  
→ **A:** For numerical stability: naive `exp` can overflow in low precision (jarbus shows float16 can yield NaNs), while computing softmax on `x - max(x)` avoids exponentiating large numbers without changing the result. Source: https://jarbus.net/blog/numerical-stability-in-flash-attention/

---

## Available Resources

### Videos
- [Let’s build GPT: from scratch, in code, spelled out.](https://youtube.com/watch?v=kCc8FmEb1nY) — **Surface when:** the student wants implementation-level understanding of a full Transformer block (attention + FFN + residuals + norm) and how it looks in code.
- [Video (wjZofJX0v4M)](https://youtube.com/watch?v=wjZofJX0v4M) — **Surface when:** the student needs a visual, conceptual walkthrough of “what flows where” inside a Transformer.

### Articles & Tutorials
- [The Illustrated Transformer (Jay Alammar)](https://jalammar.github.io/illustrated-transformer/) — **Surface when:** the student is confused about “Add & Norm,” residual paths, or how blocks stack.
- [Attention? Attention! (Lilian Weng)](https://lilianweng.github.io/posts/2018-06-24-attention/) — **Surface when:** the student asks for a more rigorous attention/Transformer reference and wants the encoder block diagram context.
- [Attention Is All You Need (Vaswani et al., 2017)](https://arxiv.org/abs/1706.03762) — **Surface when:** the student asks what the original Transformer proposed at a high level (encoder/decoder stacks; attention-centric design).
- [nanoGPT (Karpathy repo)](https://github.com/karpathy/nanoGPT) — **Surface when:** the student wants a compact reference codebase for GPT-style Transformer blocks.

---

## Visual Aids

![Transformer encoder: self-attention + feed-forward layers with residuals. (Vaswani et al., 2017)](/api/wiki-images/transformer-architecture/images/lilianweng-posts-2018-06-24-attention_014.png)  
**Show when:** the student asks “what are the parts of one encoder layer?” or “where do residuals/norm sit relative to attention and FFN?”

![Residual connection and layer normalization in a Transformer encoder layer. (Alammar)](/api/wiki-images/transformer-architecture/images/jalammar-illustrated-transformer_026.png)  
**Show when:** the student is mixing up residual add vs normalization, or asks “what does Add & Norm mean?”

![2-layer Transformer stack with residual connections and layer norm shown. (Alammar)](/api/wiki-images/transformer-architecture/images/jalammar-illustrated-transformer_027.png)  
**Show when:** the student understands one block but can’t visualize stacking many layers.

![Self-attention sub-layer with residual connection and layer normalization. (Alammar)](/api/wiki-images/transformer-architecture/images/jalammar-illustrated-transformer_028.png)  
**Show when:** the student asks for a close-up of the attention sublayer wrapper (residual + norm).

![Transformer encoder block with self-attention and FFN (UvA DLC).](/api/wiki-images/transformer-architecture/images/uvadlc-notebooks-readthedocs-en-latest-tutorial_notebooks-tutorial6-Transformers_004.svg)  
**Show when:** the student wants a clean schematic of the encoder block to map onto code (e.g., PyTorch `TransformerEncoderLayer`).

---

## Key Sources

- [RMSNorm: Root Mean Square Layer Normalization](https://arxiv.org/abs/1910.07467) — authoritative equations for LayerNorm vs RMSNorm and reported runtime speedups/invariances.
- [GLU Variants Improve Transformer (SwiGLU/GEGLU/ReGLU)](https://arxiv.org/abs/2002.05202) — definitive formulas for SwiGLU and the \(2/3\) width rule to match compute/params.
- [Peri-LN vs Pre-LN vs Post-LN](https://arxiv.org/html/2502.02732v1) — exact normalization-placement equations plus stability rationale and benchmark/loss numbers.
- [PyTorch `TransformerEncoderLayer` docs](https://docs.pytorch.org/docs/stable/generated/torch.nn.TransformerEncoderLayer.html) — practical API defaults and the `norm_first` switch mapping to pre/post norm behavior.
- [Numerical Stability in Flash Attention (softmax)](https://jarbus.net/blog/numerical-stability-in-flash-attention/) — concrete demonstration of float16 softmax overflow and the stable “subtract max” fix.