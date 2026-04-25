# Card: Switch Transformer MoE Routing (Top‑1) + Load Balancing + Stability
**Source:** https://arxiv.org/pdf/2101.03961.pdf  
**Role:** paper | **Need:** CONCEPT_EXPLAINER  
**Anchor:** Authoritative Switch (top‑1) MoE routing, capacity, auxiliary loss, and training stability defaults

## Key Content
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

## When to surface
Use when students ask how Switch/MoE routing works (top‑1 vs top‑k), how capacity factor/token dropping is defined, what the exact load-balancing loss is, or what concrete stability defaults (α, selective fp32 router, init scale, expert dropout) are recommended.