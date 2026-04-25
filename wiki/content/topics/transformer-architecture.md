---
title: "Transformer Architecture"
subject: "Sequence Models & Attention"
date: 2026-04-06
tags:
  - "subject/sequence-models-and-attention"
  - "level/beginner"
  - "level/intermediate"
  - "level/advanced"
  - "educator/andrej-karpathy"
  - "educator/jay-alammar"
  - "educator/lilian-weng"
  - "resource/video"
  - "resource/blog"
  - "resource/deep-dive"
  - "resource/paper"
  - "resource/code"
educators:
  - "Andrej Karpathy"
  - "Jay Alammar"
  - "Lilian Weng"
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

# Transformer Architecture

## Video (best)
- **Andrej Karpathy** — "Let's build GPT: from scratch, in code, spelled out."
- **Watch:** [YouTube](https://www.youtube.com/watch?v=kCc8FmEb1nY)
- Why: Karpathy builds a transformer from scratch in ~2 hours, covering every architectural component (attention, FFN, residual connections, layer norm) with live coding. The ground-up construction forces genuine understanding rather than hand-waving. Uniquely bridges conceptual and implementation levels in a single session.
- Level: intermediate

> **Note on existing curation:** The 3Blue1Brown video (`wjZofJX0v4M`) is excellent for visual intuition and is correctly curated — it is the best *purely visual/conceptual* intro. Karpathy's video is recommended here as the single best overall because it covers more of the related concepts (residual connections, layer norm, the full transformer block) at implementation depth. Both are worth including; the 3B1B video appears to be duplicated 6× in the existing list — **deduplication is needed.**

---

## Blog / Written explainer (best)
- **Jay Alammar** — "The Illustrated Transformer"
- **Link:** [https://jalammar.github.io/illustrated-transformer/](https://jalammar.github.io/illustrated-transformer/)
- Why: The definitive visual walkthrough of the transformer architecture. Alammar's step-by-step diagrams of multi-head attention, positional encoding, and the encoder-decoder stack are unmatched for building correct mental models. Widely used as a first reading in university ML courses. Covers most related concepts (positional encoding, FFN, residual connections, layer norm) in one coherent narrative.
- Level: beginner–intermediate

---

## Deep dive
- **Lilian Weng** — "Attention? Attention!"
- **Link:** [https://lilianweng.github.io/posts/2018-06-24-attention/](https://lilianweng.github.io/posts/2018-06-24-attention/)
- Why: Weng's post situates the transformer within the broader history of attention mechanisms, covers the mathematical formulation rigorously, and connects to related variants. Her writing is precise and densely referenced, making it the best single technical reference for understanding *why* each design choice was made. Complements Alammar's visual approach with mathematical depth.
- Level: intermediate–advanced

---

## Original paper
- **Vaswani et al., 2017** — "Attention Is All You Need"
- **Link:** [https://arxiv.org/abs/1706.03762](https://arxiv.org/abs/1706.03762)
- Why: The seminal paper introducing the transformer architecture. Unusually readable for a foundational ML paper — the architecture section is concise, the diagrams are clear, and the ablations justify design choices (number of heads, model depth, positional encoding). Essential primary source for all related concepts in this topic.
- Level: intermediate–advanced

---

## Code walkthrough
- **Andrej Karpathy** — "nanoGPT" (repository)
- **Link:** [https://github.com/karpathy/nanoGPT](https://github.com/karpathy/nanoGPT)
- Why: The cleanest, most pedagogically intentional transformer implementation available. The `model.py` file is ~300 lines and implements a full GPT-style transformer (transformer block, multi-head attention, FFN, layer norm, residual connections, positional encoding) with no unnecessary abstraction. Directly paired with the video above. Widely used in courses and bootcamps as the reference implementation.
- Level: intermediate

---

## Coverage notes
- **Strong:** Core transformer block, multi-head attention, residual connections, layer normalization, sinusoidal positional encoding, feed-forward network — all covered excellently by the resources above.
- **Weak:** RoPE (RoPE), ALiBi, RMSNorm, SwiGLU — these are post-2020 architectural refinements not covered in the classic resources. The Karpathy video touches on some but not all.
- **Gap:** No single excellent beginner-friendly video exists specifically for **RoPE vs. ALiBi vs. sinusoidal encoding** as a comparative topic. No excellent standalone explainer for **Mixture of Experts** at the transformer-architecture level (MoE deserves its own curated resource). **Diffusion Transformers (DiT)** are not covered by any of the above — a separate resource (e.g., the DiT paper or a multimodal-focused video) should be curated under `intro-to-multimodal`. **SwiGLU** has no dedicated high-quality explainer video; the best available is the original PaLM/GLU Variants paper.

---

## Cross-validation
This topic appears in **3 courses**: `intro-to-llms`, `intro-to-multimodal`, `ml-engineering-foundations`

| Resource | intro-to-llms | intro-to-multimodal | ml-engineering-foundations |
|---|---|---|---|
| Karpathy video | ✅ core | ⚠️ partial (no DiT) | ✅ core |
| Illustrated Transformer | ✅ core | ✅ background | ✅ core |
| Weng deep dive | ✅ advanced | ✅ advanced | ✅ core |
| Attention Is All You Need | ✅ primary source | ✅ background | ✅ reference |
| nanoGPT | ✅ core | ⚠️ partial | ✅ core |

**Recommendation:** `intro-to-multimodal` needs an additional resource specifically covering **Diffusion Transformers** (DiT — Peebles & Xie, 2023, arxiv.org/abs/2212.09748). `ml-engineering-foundations` may benefit from a systems-level resource covering efficient transformer implementations (e.g., Flash Attention).

---

## Deduplication alert
The existing curation contains `youtube_id=wjZofJX0v4M` listed **6 times** for the same lesson (`intro-to-llms/transformer-block`). This should be reduced to a single entry.

---

---

## Additional Resources for Tutor Depth

> **9 sources** — papers, official docs, working code, benchmarks, and deep explainers that give the AI tutor precision on this topic.

### 📄 GLU-family FFNs (ReGLU/GEGLU/SwiGLU) + width scaling
**Paper** · [source](https://arxiv.org/abs/2002.05202)

*GLU-family feed-forward formulas (incl. SwiGLU) and how to choose hidden size to keep params/compute constant.*

<details>
<summary>Key content</summary>

- **Baseline Transformer FFN (position-wise)**  
  **Eq. (FFN-ReLU):**  \[
  \mathrm{FFN}(x)=\phi(xW_1+b_1)W_2+b_2
  \]
  where \(x\in\mathbb{R}^{d_{\text{model}}}\), \(W_1\in\mathbb{R}^{d_{\text{model}}\times d_{\text{ff}}}\), \(W_2\in\mathbb{R}^{d_{\text{ff}}\times d_{\text{model}}}\), \(\phi\) typically ReLU or GELU.

- **Original GLU (Dauphin et al.)**  
  **Eq. (GLU):** \[
  \mathrm{GLU}(x)=\sigma(xW+b)\odot(xV+c)
  \]
  \(\sigma\)=sigmoid, \(\odot\)=elementwise product; \(W,V\in\mathbb{R}^{d_{\text{model}}\times d_{\text{ff}}}\).

- **GLU variants tested in Transformer FFN** (gate nonlinearity swapped):  
  **ReGLU:** \(\mathrm{ReLU}(xW+b)\odot(xV+c)\)  
  **GEGLU:** \(\mathrm{GELU}(xW+b)\odot(xV+c)\)  
  **SwiGLU:** \(\mathrm{Swish}(xW+b)\odot(xV+c)\), with \(\mathrm{Swish}(z)=z\cdot\sigma(\beta z)\) (typically \(\beta=1\)).

- **Parameter/compute matching rationale (3 matrices vs 2):**  
  Baseline FFN params \(\approx 2\,d_{\text{model}}d_{\text{ff}}\).  
  GLU-FFN params \(\approx 3\,d_{\text{model}}d_{\text{ff}}\).  
  **To match baseline budget:** reduce GLU hidden size by **factor \(2/3\)**: \(d_{\text{ff,GLU}}=\tfrac{2}{3}d_{\text{ff,base}}\).

- **Empirical results (T5/C4 span-filling pretrain):** log-perplexity: **ReLU 1.677**, **GEGLU 1.633**, **SwiGLU 1.636** (best among reported).

</details>

### 📄 GShard MoE Transformer—conditional compute + automatic SPMD sharding
**Paper** · [source](https://arxiv.org/pdf/2006.16668v1.pdf)

*System + training pipeline details for large-scale MoE Transformers (top-2 gating, capacity, group dispatch, XLA SPMD sharding/collectives)*

<details>
<summary>Key content</summary>

- **MoE layer equations (Section 2.2, Eq. 1–3):** For token input \(x_s\), gating \(G_{s,E}=\text{GATE}(x_s)\). Expert FFN: \(\text{FFN}_e(x_s)=w^o_e\cdot \text{ReLU}(w^i_e\cdot x_s)\). Output: \(y_s=\sum_{e=1}^{E} G_{s,e}\,\text{FFN}_e(x_s)\). Each token routed to **≤2 experts** (top-2).
- **Top-2 gating procedure (Alg. 1):**  
  - Compute gates \(g_{s,E}=\text{softmax}(w_g x_s)\); mean gates \(m_e=\frac{1}{S}\sum_s g_{s,e}\).  
  - **Capacity constraint:** per-group expert capacity \(C \approx 2N/(G\cdot E)\) (overall \(O(N/E)\)); overflow tokens get zero gate and pass via residual.  
  - **Local group dispatch:** split batch tokens into \(G\) groups of size \(S=N/G\), processed independently in parallel.  
  - **Aux loss:** \(\ell_{\text{aux}}=\frac{1}{E}\sum_e (c_e/S)\, m_e\) where \(c_e\) is (non-diff) token count routed to expert \(e\).  
  - **Random routing:** dispatch to 2nd expert with probability \(\propto 2g_2\) (after normalization).
- **Linear-algebra MoE forward (Alg. 2):** uses einsums with tensors: `combine_weights` shape \([G,S,E,C]\); `dispatch_mask` binary; dispatch via einsum `"GSEC,GSM->EGCM"`, FFN via two einsums + ReLU, combine via `"GSEC,GECM->GSM"`.
- **Sharding workflow (Section 3.2–3.3):** annotate tensors with `replicate`, `split`, `shard`; compiler infers others and inserts collectives. Key reshard uses **AllToAll** (e.g., split inputs on **G** then reshard dispatched inputs on **E**). Other primitives: **AllGather**, **AllReduce**, **CollectivePermute**. Uses **SPMD** to keep compilation ~O(1) vs device count.
- **Empirical scaling/results:**  
  - **600B** MoE trained on **2048 TPU v3 cores** in **4 days** (≈**22 TPU v3 core-years**); scaling 37.5B→600B (16× params) cost **6→22 core-years** (3.6×).  
  - Quality table (Fig. 6): MoE(2048E,36L) **600B** achieves **BLEU 44.3**, **avg ΔBLEU 13.5**; dense T(96L) **2.3B** has **ΔBLEU 6.1** and took **6 weeks** on 2048 cores (**235.5 core-years**).

</details>

### 📄 Peri-LN vs Pre-LN vs Post-LN (variance/gradient stability)
**Paper** · [source](https://arxiv.org/html/2502.02732v1)

*Comparative analysis + concrete results on normalization placement (Pre-LN, Post-LN, Peri-LN), focusing on variance growth, gradient stability, and convergence.*

<details>
<summary>Key content</summary>

- **Architectures / equations (Section 3.1–3.3):**
  - **Post-LN (Eq. 1):** \(x_{l+1}=\mathrm{LN}(x_l+F_l(x_l))\).  
  - **Pre-LN (Eq. 2):** \(x_{l+1}=x_l+F_l(\mathrm{LN}(x_l))\). (Often plus a final LN at model output, e.g., Llama-style.)
  - **Peri-LN (Section 3.3):** LN on **both** module input and module output (plus embedding input LN and final embedding LN). Per-layer idea:  
    \(u_l=\mathrm{LN}(x_l)\), \(y_l=F_l(u_l)\), \(v_l=\mathrm{LN}(y_l)\), \(x_{l+1}=x_l+v_l\).
  - Variables: \(x_l\)=hidden state at layer \(l\); \(F_l\)=Attention or MLP sublayer; LN = LayerNorm/RMSNorm.
- **Design rationale (Sections 3.2–3.4):**
  - **Post-LN:** keeps activation variance ~constant but can **weaken gradients** in deep nets → vanishing/slow convergence.
  - **Pre-LN:** improves early gradient flow but leaves module outputs unnormalized → variance can **accumulate exponentially** during training (“massive activations”).
  - **Peri-LN:** output LN damps residual spikes; aims for **linear/sub-exponential** growth and more uniform gradients.
- **Gradient stability theory (Prop. 3.1, informal):**
  - Pre-LN: massive activations can yield **exploding gradients**.
  - Peri-LN: output LN introduces a **damping factor** keeping gradient norm **bounded** (“self-regularizing”).
  - Post-LN: LN on main path can overly suppress gradients → **vanishing**.
- **Empirical training pipeline (Section 4.1):**
  - Model sizes: **125M, 350M, 1.3B** params (excluding embeddings); trained on **30B tokens**; **5 seeds**; Adam + cosine LR; RMSNorm primarily; Megatron-LM; DCLM-baseline dataset; TikToken “clk_base”; weight decay **0.1**; LR sweep **1e-5 to 3e-4**; seq length and batch size fixed (values not shown in excerpt).
- **Concrete benchmark numbers (Table 2; Peri-LN rows):**
  - **125M Peri-LN:** ARC-E 57.51, HellaSwag 37.46, PIQA 69.48, SIQA 40.64, WinoGrande 52.74, **Avg 51.57**, **Loss 3.34**, SFT Avg 51.96.
  - **350M Peri-LN:** ARC-E 66.17, HellaSwag 43.94, PIQA 73.63, SIQA 42.34, WinoGrande 56.64, **Avg 56.55**, **Loss 3.18**, SFT Avg 56.94.
  - **1.3B Peri-LN:** ARC-E 68.73, HellaSwag 46.99, PIQA 74.31, SIQA 43.00, WinoGrande 59.76, **Avg 58.56**, **Loss 3.11**, SFT Avg 59.02.
- **Stability observations (Section 4.2, 4.4):**
  - Gradient-norm spikes: **Pre-LN and Post-LN show many spikes across seeds; Peri-LN shows relatively few**.
  - Hidden-state variance over training: Pre-LN goes from ~linear at init to **exponential blow-up**; Peri-LN remains **moderate**; Post-LN stays **stable**.

</details>

### 📄 RMSNorm (Root Mean Square Layer Normalization)
**Paper** · [source](https://arxiv.org/abs/1910.07467)

*Exact RMSNorm equation (RMS-only normalization; no mean-centering) + comparison to LayerNorm (mean/variance), incl. scale parameter and invariances.*

<details>
<summary>Key content</summary>

- **LayerNorm definition (Eq. 2–3):** for pre-activation/summed inputs \(a\in\mathbb{R}^n\)  
  \[
  \bar a_i=\frac{a_i-\mu}{\sigma}\, g_i,\quad y=f(\bar a + b)
  \]
  \[
  \mu=\frac{1}{n}\sum_{i=1}^n a_i,\quad \sigma=\sqrt{\frac{1}{n}\sum_{i=1}^n (a_i-\mu)^2}
  \]
  where \(g\in\mathbb{R}^n\) is a learnable gain (init to 1), \(b\) bias, \(f(\cdot)\) elementwise nonlinearity.
- **RMSNorm definition (Eq. 4):** removes mean-centering; normalizes by RMS only  
  \[
  \bar a_i=\frac{a_i}{\mathrm{RMS}(a)}\, g_i,\quad \mathrm{RMS}(a)=\sqrt{\frac{1}{n}\sum_{i=1}^n a_i^2}
  \]
  If \(\mu=0\), RMSNorm equals LayerNorm (paper statement).
- **General RMSNorm layer form (Eq. 5):**  
  \[
  y=f\!\left(\frac{Wx}{\mathrm{RMS}(a)}\odot g + b\right),\ \ a=Wx
  \]
- **Key property (Eq. 6–7):** linearity \(\mathrm{RMS}(\alpha x)=\alpha\,\mathrm{RMS}(x)\) ⇒ invariance to global rescaling of weights/inputs (e.g., \(W'=\delta W\) leaves output unchanged).
- **Design rationale:** authors hypothesize LayerNorm’s **re-centering invariance** is dispensable; **re-scaling invariance** is the core benefit; RMSNorm reduces compute overhead.
- **Empirical speedups:** RMSNorm reduces running time vs LayerNorm by **7%–64%** across models/tasks; for Transformer specifically **~7%–9%** speedup with comparable BLEU (Section 6; Table 4 mention).
- **Partial RMSNorm (pRMSNorm):** estimate RMS from only first **p%** of components; reported competitive at **p=6.25%** (Section 1/4).

</details>

### 📄 Switch Transformer MoE Routing (Top‑1) + Load Balancing + Stability
**Paper** · [source](https://arxiv.org/pdf/2101.03961.pdf)

*Authoritative Switch (top‑1) MoE routing, capacity, auxiliary loss, and training stability defaults*

<details>
<summary>Key content</summary>

- **Router / gating (Eq. 1):** for token representation \(x\), router logits \(h(x)=W_r x\). Softmax gate for expert \(i\):  
  \[
  p_i(x)=\frac{e^{h(x)_i}}{\sum_{j=1}^N e^{h(x)_j}}
  \]
  \(N\)=#experts.
- **MoE output (Eq. 2):** for selected expert set \(T\) (top‑k),  
  \[
  y=\sum_{i\in T} p_i(x)E_i(x)
  \]
  **Switch uses \(k=1\)** (route each token to single best expert) for simpler routing, lower compute/comm, and smaller required expert capacity.
- **Expert capacity (Eq. 3, Section 2.2):** static per-expert token budget  
  \[
  C=\Big(\frac{\text{tokens per batch}}{\text{\#experts}}\Big)\times \text{capacity factor}
  \]
  If an expert overflows, **dropped tokens skip expert compute** and pass via residual connection. Empirically dropped tokens typically **<1%** with adequate aux loss.
- **Aux load-balancing loss (Eq. 4–6):** per Switch layer, add to training loss  
  \[
  L_{\text{aux}}=\alpha\cdot N\sum_{i=1}^N f_i P_i
  \]
  \(f_i=\frac{1}{T}\sum_{x\in B}\mathbf{1}\{\arg\max p(x)=i\}\) (fraction dispatched),  
  \(P_i=\frac{1}{T}\sum_{x\in B} p_i(x)\) (mean prob mass), \(T\)=#tokens in batch \(B\). Multiply by \(N\) to keep scale constant as \(N\) varies. **Default \(\alpha=10^{-2}\)** (swept \(10^{-1}\) to \(10^{-5}\)).
- **Stability tricks (Section 2.4):**
  - **Selective precision:** cast router input/ops to **float32**, then recast dispatch/combine tensors to **bfloat16** → stable and fast. Example (Table 2): Switch‑Base **float32** \(-1.718\) @ **1160 ex/s**; **bfloat16 diverged**; **selective precision** \(-1.716\) @ **1390 ex/s**.
  - **Smaller init scale:** truncated normal with \(\sigma=\sqrt{s/n}\) (fan-in \(n\)); reduce \(s\) from **1.0 to 0.1** improves stability (Table 3): **0.1x-init** \(-2.72\pm0.01\) vs **1.0x-init** \(-3.60\pm0.68\) at 3.5k steps.
  - **Fine-tuning regularization:** use **dropout 0.1** non-expert layers + **expert dropout 0.4** inside experts (Table 4 best row).
- **Speed/quality benchmark (Table 1, 128 experts):** Switch‑Base capacity factor **1.0** reaches threshold faster (**62.8h**) and faster throughput (**1000 ex/s**) than MoE‑Base (**80.1h**, **860 ex/s**).

</details>

### 📄 Switch Transformer top‑1 routing + load balancing
**Paper** · [source](https://jmlr.org/papers/volume23/21-0998/21-0998.pdf)

*Step-by-step Switch Transformer routing (top‑1 gating, expert capacity, dispatch/combination, load-balancing loss)*

<details>
<summary>Key content</summary>

- **Router / gating (Eq. 1):** For token representation \(x\), router logits \(h(x)=W_r x\). Gate prob for expert \(i\):  
  \[
  p_i(x)=\frac{e^{h(x)_i}}{\sum_{j=1}^N e^{h(x)_j}}
  \]
- **MoE output (Eq. 2):** For selected top‑\(k\) experts \(T\):  
  \[
  y=\sum_{i\in T} p_i(x)E_i(x)
  \]
  **Switch = top‑1** (\(k=1\)): route each token to a single expert; still differentiable via \(p_i(x)\). Rationale: less router compute, **expert capacity can be ~halved**, simpler implementation + lower communication.
- **Expert capacity (Eq. 3):**  
  \[
  C=\Big(\frac{\text{tokens per batch}}{\text{\#experts}}\Big)\times \text{capacity factor}
  \]
  If an expert overflows, **dropped tokens skip expert compute** and pass via residual connection. Larger capacity factor reduces drops but wastes compute/memory.
- **Aux load-balancing loss (Eq. 4–6):** For batch \(B\) with \(T\) tokens, \(N\) experts:  
  \[
  \mathcal{L}_{aux}=\alpha\cdot N\sum_{i=1}^N f_i P_i
  \]
  \(f_i=\frac{1}{T}\sum_{x\in B}\mathbf{1}\{\arg\max p(x)=i\}\) (fraction dispatched),  
  \(P_i=\frac{1}{T}\sum_{x\in B} p_i(x)\) (avg prob mass). Multiply by \(N\) keeps scale constant under uniform routing. Default **\(\alpha=10^{-2}\)** (swept \(10^{-1}\) to \(10^{-5}\)).
- **Empirics (Table 1):** 128 experts, experts every other FFN. Switch-Base vs T5-Base: **~7× pretrain speedup** (Fig. 5). Examples/sec at capacity factor 1.0: **Switch 1000 vs MoE 860**.
- **Stability:** Selective precision: cast router ops to **float32**; rest bfloat16 (Table 2: bfloat16 diverged; selective precision stable at **-1.716** neg log perp, **1390 ex/s**). Initialization scale: reduce by **10×** improves stability (Table 3).

</details>

### 📋 # Source: https://docs.pytorch.org/docs/2.8/generated/torch.nn.TransformerEncoderLayer.html
**Source** · 

### 📋 # Source: https://docs.pytorch.org/docs/2.9/generated/torch.nn.TransformerEncoderLayer.html
**Source** · 

### 📋 # Source: https://docs.pytorch.org/docs/stable/generated/torch.nn.TransformerEncoderLayer.html
**Source** ·

---

## Related Topics

- [[topics/attention-mechanism|Attention Mechanism]]
- [[topics/self-attention|Self-Attention]]
- [[topics/multi-head-attention|Multi-Head Attention]]
- [[topics/pre-training|Pre-Training]]
- [[topics/tokenization|Tokenization]]
- [[topics/mixture-of-experts|Mixture of Experts]]
