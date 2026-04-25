# Card: Switch Transformer top‑1 routing + load balancing
**Source:** https://jmlr.org/papers/volume23/21-0998/21-0998.pdf  
**Role:** paper | **Need:** CONCEPT_EXPLAINER  
**Anchor:** Step-by-step Switch Transformer routing (top‑1 gating, expert capacity, dispatch/combination, load-balancing loss)

## Key Content
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

## When to surface
Use when students ask how **Mixture-of-Experts routing works in Switch Transformers**, how **capacity/dropped tokens** are handled, or how the **load-balancing auxiliary loss** is defined and tuned.