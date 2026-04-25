## Core Definitions

**Scaling laws (for LMs).** Kaplan et al. (2020) report that language-model cross-entropy loss *L* follows empirical **power laws** in model size (*N* parameters), dataset size (*D* tokens), and training compute (*C* FLOPs), over many orders of magnitude, enabling predictions of how loss changes when scaling these factors and how to allocate a fixed compute budget. Source: https://arxiv.org/pdf/2001.08361.pdf

**Chinchilla / compute-optimal training (tokens vs parameters).** Hoffmann et al. (2022) define compute-optimal training as choosing parameter count **N** and training tokens **D** that **minimize final loss under a compute budget C**, using a compute model \(\text{FLOPs}(N,D)\approx 6ND\) and a fitted loss model \(\hat L(N,D)=E + A N^{\alpha} + B D^{\beta}\); their fitted exponents imply **tokens and parameters should scale roughly equally** (doubling N ⇒ ~doubling D) on the compute-optimal frontier. Source: https://arxiv.org/pdf/2203.15556.pdf

**Grouped-Query Attention (GQA).** (Not defined in the provided sources.) Use only as a high-level label in conversation unless the student provides an external reference; do not quote a formal definition from this packet.

**Mixture of Experts (MoE).** Shazeer et al. (2017) define an MoE layer as a set of expert networks \(E_i(\cdot)\) whose outputs are combined by a (typically sparse) gating function \(G(x)\), producing \(y=\sum_{i=1}^{n} G(x)_i E_i(x)\); in modern sparse MoE, only top‑k experts per token are active (conditional computation). Source: https://arxiv.org/abs/1701.06538

**Top‑k sparse routing (MoE).** In sparsely-gated MoE (Shazeer et al., 2017), a mask \(M(\cdot)\) (e.g., TopK) zeros out all but the top‑k gate entries and then renormalizes, yielding sparse gate weights \(G(x)\) so only k experts are evaluated per input. Source: https://arxiv.org/abs/1701.06538

**Top‑2 routing with capacity (GShard-style).** Lepikhin et al. (2020) describe routing each token to up to **two experts** chosen by top‑2 gate probabilities, subject to a **per-expert capacity**; overflowed tokens are not dispatched (gate becomes zero) and a residual path carries the representation. They add an auxiliary loss to encourage balanced expert usage. Source: https://arxiv.org/pdf/2006.16668.pdf

**FlashAttention.** Dao et al. (2022) define FlashAttention as an **exact attention** algorithm that is **IO-aware**: it tiles attention computation and **fuses** matmul→softmax(+mask/dropout)→matmul in a single kernel, avoiding materializing the \(N\times N\) attention matrix in HBM; it stores only output and softmax statistics for backward recomputation. Source: https://proceedings.neurips.cc/paper_files/paper/2022/file/67d57c32e20fd0a7a302cb81d36e40d5-Paper-Conference.pdf

**KV cache.** In autoregressive decoding, keys and values from prior tokens are cached per layer to avoid recomputing them each step; vLLM quantify the memory cost (e.g., OPT‑13B KV cache per token ≈ 800 KB in FP16) and show that allocation strategy can dominate serving throughput. Source: https://arxiv.org/abs/2309.06180


## Key Formulas & Empirical Results

### Kaplan et al. (2020): loss vs N/D/compute + compute model
- **Training compute (non-embedding params):**
  \[
  C \approx 6 N B S
  \]
  where \(N\)=non-embedding parameter count, \(B\)=batch size (tokens), \(S\)=optimizer steps. Source: https://arxiv.org/pdf/2001.08361.pdf

- **Single-factor scaling (converged / early-stopped):**
  - Model-limited (large D): \(L(N)=(N_c/N)^{\alpha_N}\), with \(\alpha_N\approx 0.076\), \(N_c\approx 8.8\times 10^{13}\).
  - Data-limited (large N): \(L(D)=(D_c/D)^{\alpha_D}\), with \(\alpha_D\approx 0.095\), \(D_c\approx 5.4\times 10^{13}\) tokens.  
  Source: https://arxiv.org/pdf/2001.08361.pdf

- **Joint overfitting law:**
  \[
  L(N,D)=\Big[(N_c/N)^{\alpha_N/\alpha_D}+D_c/D\Big]^{\alpha_D}
  \]
  Implies to avoid overfitting penalty: \(D \propto N^{\alpha_N/\alpha_D}\approx N^{0.74}\). Source: https://arxiv.org/pdf/2001.08361.pdf

- **Compute-efficient frontier (empirical):** \(N \propto C_{\min}^{0.73}\), \(B \propto C_{\min}^{0.24}\), \(S \propto C_{\min}^{0.03}\). Source: https://arxiv.org/pdf/2001.08361.pdf

### Hoffmann et al. (2022): Chinchilla compute-optimal frontier
- **Optimization objective (Eq. 1):**
  \[
  (N_{\text{opt}}(C),D_{\text{opt}}(C))=\arg\min_{N,D\ \text{s.t.}\ \text{FLOPs}(N,D)=C} L(N,D)
  \]
  Source: https://arxiv.org/pdf/2203.15556.pdf

- **Compute model:** \(\text{FLOPs}(N,D)\approx 6ND\). Source: https://arxiv.org/pdf/2203.15556.pdf

- **Loss model (Eq. 2):**
  \[
  \hat L(N,D)=E + A N^{\alpha} + B D^{\beta}
  \]
  Source: https://arxiv.org/pdf/2203.15556.pdf

- **Closed-form compute-optimal allocations (Eq. 4):**
  \[
  N_{\text{opt}}(C)=G\left(\frac{C}{6}\right)^a,\quad D_{\text{opt}}(C)=G^{-1}\left(\frac{C}{6}\right)^b
  \]
  where \(G=\left(\frac{\alpha A}{\beta B}\right)^{\frac{1}{\alpha+\beta}},\ a=\frac{\beta}{\alpha+\beta},\ b=\frac{\alpha}{\alpha+\beta}\). Source: https://arxiv.org/pdf/2203.15556.pdf

- **Empirical exponents (Table 2):** \(a\approx 0.46\text{–}0.50\), \(b\approx 0.50\text{–}0.54\). **Contrast:** Kaplan et al. (2020) \(a=0.73,b=0.27\). Source: https://arxiv.org/pdf/2203.15556.pdf

- **Concrete compute-optimal comparison:** At Gopher compute \(C=5.76\times10^{23}\) FLOPs, predicted optimal model size ~40–70B; Chinchilla trains **70B on 1.4T tokens** vs Gopher **280B on 300B tokens** at similar compute. Source: https://arxiv.org/pdf/2203.15556.pdf

### FlashAttention (Dao et al., 2022): exact speed/memory numbers
- **Standard attention (materializes \(N\times N\) scores/probs):**  
  \(S=QK^\top\), \(P=\mathrm{softmax}(S)\), \(O=PV\). Source: https://proceedings.neurips.cc/paper_files/paper/2022/file/67d57c32e20fd0a7a302cb81d36e40d5-Paper-Conference.pdf

- **Benchmark (A100; \(N{=}1024,d{=}64\), 16 heads, batch 64; fwd+bwd):**
  - Standard: **35.3 GB HBM R/W**, **35.1 ms**
  - FlashAttention: **4.4 GB HBM R/W**, **11.7 ms**  
  Source: https://proceedings.neurips.cc/paper_files/paper/2022/file/67d57c32e20fd0a7a302cb81d36e40d5-Paper-Conference.pdf

- **Memory scaling claim:** FlashAttention memory footprint is **linear in sequence length N**; reported up to **20×** more memory-efficient than exact attention baselines (Fig. 3 right). Source: same as above.

### KV cache + serving (vLLM / PagedAttention)
- **Autoregressive factorization (Eq. 1):**
  \[
  P(x_{n+1:n+T}\mid x_{1:n})=\prod_{t=1}^{T} P(x_{n+t}\mid x_{1:n+t-1})
  \]
  Source: https://arxiv.org/abs/2309.06180

- **KV cache size example:** OPT‑13B KV cache per token ≈ **800 KB** (FP16), computed as \(2\) (K,V) × \(5120\) (hidden) × \(40\) (layers) × \(2\) bytes. Source: https://arxiv.org/abs/2309.06180

- **Throughput headline:** vLLM improves throughput by **2–4×** at similar latency vs FasterTransformer and Orca (abstract). Source: https://arxiv.org/abs/2309.06180

### MoE core equations + balancing losses
- **Sparsely-gated MoE output (Eq. 1):**
  \[
  y=\sum_{i=1}^{n} G(x)_i\,E_i(x)
  \]
  Source: https://arxiv.org/abs/1701.06538

- **Sparse gating via mask + renorm (Eq. 3):**
  \[
  G(x)_i=\frac{G_\sigma(x)_i\,M(G_\sigma(x))_i}{\sum_{j=1}^{n}G_\sigma(x)_j\,M(G_\sigma(x))_j}
  \]
  Source: https://arxiv.org/abs/1701.06538

- **Importance (Eq. 6) + CV importance loss (Eq. 7):**
  \[
  \text{Importance}(X)=\sum_{x\in X} G(x),\quad
  L_{\text{importance}}(X)=w_{\text{importance}}\cdot \mathrm{CV}(\text{Importance}(X))^2
  \]
  Source: https://arxiv.org/abs/1701.06538

- **GShard auxiliary load-balancing loss (Algorithm 1):**  
  \(m_e=\frac{1}{S}\sum_{s=1}^S g_{s,e}\), and
  \[
  \ell_{\text{aux}}=\frac{1}{E}\sum_{e=1}^E \left(\frac{c_e}{S}\right)m_e,\quad
  L=\ell_{\text{nll}}+k\,\ell_{\text{aux}}
  \]
  where \(c_e\) is (capacity-limited) token count for expert \(e\) in the group. Source: https://arxiv.org/pdf/2006.16668.pdf

### MoE inference bottlenecks (MoE-Inference-Bench)
- **Throughput definition (Eq. 2):**
  \[
  \text{Throughput}=\frac{\#\text{input tokens}+\#\text{output tokens}}{\text{end-to-end latency (s)}}
  \]
  Source: https://www.arxiv.org/pdf/2508.17467.pdf

- **Top‑k/active experts effect:** For DeepSeek‑V2‑Lite, active experts **1→32** drops throughput **~15–20%** at large batches (64/128) vs **~5–8%** at small batches (1/16). Source: https://www.arxiv.org/pdf/2508.17467.pdf

- **FP8 vs FP16:** FP8 gives **~20–25%** throughput gain across lengths; up to **~25–30%** at highest batch size. Source: https://www.arxiv.org/pdf/2508.17467.pdf

### DeepSpeed MoE API defaults (implementation knobs students ask about)
- **Layer signature + defaults:**  
  `MoE(hidden_size, expert, num_experts=1, ep_size=1, k=1, capacity_factor=1.0, eval_capacity_factor=1.0, min_capacity=4, use_residual=False, noisy_gate_policy=None, drop_tokens=True, use_rts=True, use_tutel=False, enable_expert_tensor_parallelism=False, top2_2nd_expert_sampling=True)`  
  Notes: `k` supports **only 1 or 2**; `drop_tokens=False` is “equivalent to infinite capacity”. Source: https://deepspeed.readthedocs.io/en/latest/moe.html


## How It Works

### A. Using scaling laws to pick N and D under compute budget (Chinchilla-style)
1. **Assume compute budget \(C\)** and compute model \(\text{FLOPs}(N,D)\approx 6ND\). (Hoffmann et al., 2022)
2. **Assume a separable loss model** \(\hat L(N,D)=E + A N^{\alpha} + B D^{\beta}\) fitted from experiments. (Hoffmann et al., 2022)
3. **Solve constrained optimization**: minimize \(\hat L(N,D)\) subject to \(6ND=C\). (Eq. 1)
4. **Use closed-form frontier**:
   - \(N_{\text{opt}}(C)=G(C/6)^a\)
   - \(D_{\text{opt}}(C)=G^{-1}(C/6)^b\)  
   with \(a=\beta/(\alpha+\beta)\), \(b=\alpha/(\alpha+\beta)\). (Eq. 4)
5. **Interpretation:** with fitted \(a\approx b\approx 0.5\), compute-optimal training scales **tokens roughly proportionally with parameters**. (Table 2)

### B. FlashAttention mechanics (what changes vs “standard attention”)
1. **Standard attention** computes \(S=QK^\top\), then \(P=\mathrm{softmax}(S)\), then \(O=PV\), typically **writing \(S\) and/or \(P\) to HBM**, costing \(O(N^2)\) memory traffic. (Dao et al., 2022)
2. **FlashAttention**:
   - **Tiles** Q/K/V into blocks that fit in SRAM.
   - **Fuses** matmul→softmax(+mask/dropout)→matmul in one kernel.
   - **Avoids materializing** the full \(N\times N\) attention matrix in HBM.
   - Stores only output \(O\) and softmax stats \((m,\ell)\) to enable exact backward via recomputation. (Alg. 1 / Sec. 3.1)

### C. MoE forward pass (sparse top‑k routing)
(Use this when a student asks “what happens to a token in an MoE layer?”)

1. **Compute gate scores** for each token \(x\): dense scores \(G_\sigma(x)\) over experts. (Shazeer et al., 2017)
2. **Apply TopK mask** \(M(\cdot)\) to keep only k experts; zero others.
3. **Renormalize** masked scores to get sparse gate weights \(G(x)\) (Eq. 3).
4. **Dispatch token** to selected experts; compute expert outputs \(E_i(x)\) only for active experts.
5. **Combine outputs**: \(y=\sum_i G(x)_i E_i(x)\) (Eq. 1).
6. **Add balancing loss** (optional but common): e.g., importance/CV loss (Shazeer et al., 2017) or GShard auxiliary loss (Lepikhin et al., 2020).

### D. KV cache + PagedAttention (why serving systems care)
1. **Autoregressive decoding** generates one token at a time (vLLM Eq. 1).
2. Each step needs attention over all previous tokens; **keys/values for previous tokens are cached** per layer to avoid recomputation.
3. KV cache is large (e.g., OPT‑13B ≈ **800 KB per token** in FP16), so **allocation strategy** affects batch size and throughput. (vLLM Sec. 3)
4. **PagedAttention** stores KV in fixed-size blocks, allocates on demand, and uses a block table mapping logical→physical blocks; waste is bounded to ≤1 block/request and enables sharing + copy-on-write. (vLLM Sec. 4)


## Teaching Approaches

### Intuitive (no math): “Budget allocation”
- Scaling laws are like a rule-of-thumb map: if you have a fixed training budget, you can spend it on **more parameters** (bigger model) or **more tokens** (train longer / more data).  
- Chinchilla’s key message (Hoffmann et al., 2022): many big models were **undertrained**—they had lots of parameters but not enough tokens—so smaller models trained on more tokens can win at the same compute.

### Technical (with math): “Constrained optimization”
- Start from Hoffmann et al. objective: minimize \(L(N,D)\) subject to \(6ND=C\).  
- With \(\hat L(N,D)=E + A N^{\alpha} + B D^{\beta}\), the optimum yields power-law allocations \(N_{\text{opt}}(C)\propto (C/6)^a\), \(D_{\text{opt}}(C)\propto (C/6)^b\).  
- The fitted exponents \(a\approx b\approx 0.5\) imply **balanced scaling** of N and D.

### Analogy-based: “Restaurant kitchen”
- **Parameters** = number of chefs; **tokens** = number of meals cooked in training.  
- If you hire many chefs (huge model) but only cook a few meals (few tokens), the team never learns the menu well (undertrained). Chinchilla says: for best results at fixed budget, scale chefs and meals together.


## Common Misconceptions

1. **“Compute-optimal means ‘largest model possible’.”**  
   - Why wrong: Hoffmann et al. explicitly optimize **loss under fixed compute** with \(6ND=C\); the optimum can be **smaller N with larger D** than “max N”.  
   - Correct model: compute-optimal is a **trade-off curve** \(N_{\text{opt}}(C), D_{\text{opt}}(C)\), not “maximize parameters”. (https://arxiv.org/pdf/2203.15556.pdf)

2. **“Chinchilla says ‘always use 20 tokens per parameter’ as a universal constant.”**  
   - Why wrong: the paper provides a **compute-optimal frontier** with fitted exponents and constants; the “tokens/param” ratio is a *derived implication* that depends on the fitted regime and compute budget, not a universal law stated as a single constant in the equations.  
   - Correct model: use the **frontier equations** (Eq. 4) and fitted exponents \(a,b\) to reason about scaling; the key qualitative takeaway is **tokens scale roughly proportionally with parameters**. (https://arxiv.org/pdf/2203.15556.pdf)

3. **“FlashAttention is an approximation like linear attention.”**  
   - Why wrong: Dao et al. present FlashAttention as **exact attention**; it changes IO/memory behavior by tiling and recomputation, not the mathematical result.  
   - Correct model: same \(O= \mathrm{softmax}(QK^\top)V\), but computed without materializing \(N\times N\) in HBM. (https://proceedings.neurips.cc/paper_files/paper/2022/file/67d57c32e20fd0a7a302cb81d36e40d5-Paper-Conference.pdf)

4. **“MoE makes inference cheaper because the model has fewer parameters.”**  
   - Why wrong: MoE often has **more total parameters**; savings come from **sparse activation** (only top‑k experts used per token).  
   - Correct model: distinguish **total params** vs **active params per token**; routing/dispatch and load balance can become bottlenecks (see MoE-Inference-Bench throughput drops as active experts increase). (https://www.arxiv.org/pdf/2508.17467.pdf, https://arxiv.org/abs/1701.06538)

5. **“KV cache is a small constant overhead.”**  
   - Why wrong: vLLM shows KV cache can be enormous (OPT‑13B ≈ **800 KB/token**) and naive allocation can waste memory via fragmentation, limiting batching/throughput.  
   - Correct model: KV cache is often the **dominant memory term** in long-context serving; systems like PagedAttention exist to manage it. (https://arxiv.org/abs/2309.06180)


## Worked Examples

### 1) Compute-optimal scaling: plug-and-play frontier (symbolic)
Goal: show the *mechanics* of using Chinchilla Eq. 4 without inventing constants.

Given compute budget \(C\) and fitted constants \((A,B,E,\alpha,\beta)\):
1. Compute:
   \[
   G=\left(\frac{\alpha A}{\beta B}\right)^{\frac{1}{\alpha+\beta}},\quad
   a=\frac{\beta}{\alpha+\beta},\quad
   b=\frac{\alpha}{\alpha+\beta}
   \]
2. Then:
   \[
   N_{\text{opt}}(C)=G\left(\frac{C}{6}\right)^a,\quad
   D_{\text{opt}}(C)=G^{-1}\left(\frac{C}{6}\right)^b
   \]
Source: Hoffmann et al. (Eq. 4) https://arxiv.org/pdf/2203.15556.pdf

Tutor move: ask the student what happens to \(N_{\text{opt}}\) and \(D_{\text{opt}}\) if compute \(C\) increases by 16×, using \(a\approx b\approx 0.5\) (Table 2) → both scale by about \(16^{0.5}=4\).

### 2) FlashAttention: interpret a benchmark table entry
Use the A100 benchmark point (Fig. 2 left) to ground “why it’s faster”:
- Standard attention: **35.3 GB** HBM R/W, **35.1 ms** (fwd+bwd)
- FlashAttention: **4.4 GB** HBM R/W, **11.7 ms**  
Source: Dao et al. (2022) https://proceedings.neurips.cc/paper_files/paper/2022/file/67d57c32e20fd0a7a302cb81d36e40d5-Paper-Conference.pdf

Tutor move: ask the student to compute the memory-traffic ratio \(35.3/4.4\approx 8\times\) and time ratio \(35.1/11.7\approx 3\times\), then connect to “IO-bound vs compute-bound”.

### 3) KV cache sizing sanity check (vLLM OPT-13B)
Reproduce the given calculation:
- 2 (K,V) × 5120 (hidden) × 40 (layers) × 2 bytes (FP16)  
= \(2\times5120\times40\times2 = 819{,}200\) bytes ≈ **800 KB per token**.  
Source: vLLM https://arxiv.org/abs/2309.06180

Tutor move: ask what happens at 2,000 cached tokens → ~1.6 GB per sequence (order-of-magnitude reasoning), motivating paging.


## Comparisons & Trade-offs

| Topic | Option | What you gain | What you pay | Source anchor |
|---|---|---|---|---|
| Compute-optimal scaling | Kaplan (2020) allocation trend | Predictive power laws; compute-efficient frontier | Empirically led to “train very large models on modest data” regime | https://arxiv.org/pdf/2001.08361.pdf |
| Compute-optimal scaling | Chinchilla (2022) allocation trend | Better loss at same compute by training on more tokens; “undertrained” diagnosis | Requires much more data sourcing/cleaning | https://arxiv.org/pdf/2203.15556.pdf |
| Attention implementation | Standard exact attention | Simple; widely available | Materializes \(N\times N\) → high HBM traffic/memory | https://proceedings.neurips.cc/paper_files/paper/2022/file/67d57c32e20fd0a7a302cb81d36e40d5-Paper-Conference.pdf |
| Attention implementation | FlashAttention (exact) | Much lower HBM traffic; faster; memory ~linear in N | More complex kernel; relies on tiling/recompute | same |
| Model architecture | Dense Transformer | Predictable compute; no routing overhead | Scaling capacity requires scaling compute | MoE contrast sources below |
| Model architecture | Sparse MoE (top‑k) | Higher total capacity at similar active compute | Routing, load balance, capacity overflow, comm overhead; throughput drops as active experts increase | https://arxiv.org/abs/1701.06538, https://arxiv.org/pdf/2006.16668.pdf, https://www.arxiv.org/pdf/2508.17467.pdf |
| Serving memory | Naive KV allocation | Simple | Fragmentation + wasted memory; limits batching | https://arxiv.org/abs/2309.06180 |
| Serving memory | PagedAttention (vLLM) | Bounded waste (≤1 block/request), sharing + COW, swap to CPU | More complex allocator + block tables | https://arxiv.org/abs/2309.06180 |


## Prerequisite Connections

- **Cross-entropy / next-token prediction loss:** scaling laws are stated in terms of cross-entropy loss (Kaplan et al.).  
- **FLOPs accounting:** both Kaplan and Chinchilla use approximate compute models (e.g., \(6ND\), \(6NBS\)).  
- **Transformer attention math (Q,K,V; softmax):** needed to understand what FlashAttention accelerates (standard attention equations).  
- **Autoregressive decoding:** needed to understand why KV cache exists and why it grows with sequence length (vLLM Eq. 1).


## Socratic Question Bank

1. **If you fix compute \(C\approx 6ND\), what happens to tokens \(D\) if you double parameters \(N\)?**  
   *Good answer:* \(D\) must halve to keep compute fixed; then discuss why Chinchilla suggests that’s often suboptimal for loss.

2. **Chinchilla’s fitted exponents give \(a\approx b\approx 0.5\). What does that imply about how \(N_{\text{opt}}\) and \(D_{\text{opt}}\) scale with compute?**  
   *Good answer:* both scale roughly as \(\sqrt{C}\); tokens and parameters grow similarly with compute.

3. **Why can FlashAttention be faster even though it computes the same exact attention output?**  
   *Good answer:* reduces HBM reads/writes by not materializing \(N\times N\); IO-bound speedup.

4. **In MoE, what’s the difference between “total parameters” and “active parameters”? Why does it matter for throughput?**  
   *Good answer:* total params can be huge, but only top‑k experts are evaluated; throughput still depends on routing/dispatch and number of active experts (bench shows throughput drops as active experts increase).

5. **What failure mode do MoE balancing losses address?**  
   *Good answer:* expert collapse/imbalance where a few experts get most tokens; balancing losses encourage uniform utilization (importance/CV or GShard aux loss).

6. **Why does KV cache often dominate memory at long context? Use the OPT‑13B per-token number to justify.**  
   *Good answer:* 800 KB/token × thousands of tokens becomes GBs per sequence; limits batch size.

7. **What does PagedAttention change about KV cache allocation, and what problem is it solving?**  
   *Good answer:* block-based paging reduces fragmentation/reservation waste; enables sharing and swapping.


## Likely Student Questions

**Q: What’s the actual Chinchilla compute-optimal formula for \(N_{\text{opt}}(C)\) and \(D_{\text{opt}}(C)\)?**  
→ **A:** Hoffmann et al. give (Eq. 4)  
\(N_{\text{opt}}(C)=G(C/6)^a,\ D_{\text{opt}}(C)=G^{-1}(C/6)^b\), with \(G=(\alpha A/\beta B)^{1/(\alpha+\beta)}\), \(a=\beta/(\alpha+\beta)\), \(b=\alpha/(\alpha+\beta)\). Source: https://arxiv.org/pdf/2203.15556.pdf

**Q: What compute model do Kaplan and Chinchilla use?**  
→ **A:** Kaplan uses \(C\approx 6NBS\) FLOPs (non-embedding), while Chinchilla uses \(\text{FLOPs}(N,D)\approx 6ND\). Sources: https://arxiv.org/pdf/2001.08361.pdf and https://arxiv.org/pdf/2203.15556.pdf

**Q: What’s the key empirical difference between Kaplan vs Chinchilla allocations?**  
→ **A:** Chinchilla’s fitted exponents are \(a\approx 0.46\text{–}0.50\), \(b\approx 0.50\text{–}0.54\) (tokens scale about as fast as params), whereas Kaplan reported \(a=0.73,b=0.27\) (params scale faster than tokens). Source: https://arxiv.org/pdf/2203.15556.pdf (Table 2 contrast)

**Q: Is FlashAttention approximate? What exactly does it compute?**  
→ **A:** It computes **exact** attention \(O=\mathrm{softmax}(QK^\top)V\) but avoids writing the \(N\times N\) attention matrix to HBM by tiling and fusing kernels; it stores softmax stats for backward recomputation. Source: https://proceedings.neurips.cc/paper_files/paper/2022/file/67d57c32e20fd0a7a302cb81d36e40d5-Paper-Conference.pdf

**Q: What are concrete FlashAttention speed/memory numbers?**  
→ **A:** On A100 with \(N=1024,d=64\), 16 heads, batch 64 (fwd+bwd): standard attention **35.3 GB** HBM R/W and **35.1 ms** vs FlashAttention **4.4 GB** and **11.7 ms**. Source: same as above.

**Q: How big is the KV cache in practice?**  
→ **A:** vLLM reports OPT‑13B KV cache per token ≈ **800 KB** in FP16, computed as \(2\times5120\times40\times2\) bytes. Source: https://arxiv.org/abs/2309.06180

**Q: What’s the canonical MoE equation and how is top‑k enforced?**  
→ **A:** Shazeer et al.: \(y=\sum_i G(x)_iE_i(x)\). Top‑k is enforced by masking all but top‑k gate entries and renormalizing (Eq. 3). Source: https://arxiv.org/abs/1701.06538

**Q: How does increasing top‑k (more active experts) affect inference throughput?**  
→ **A:** MoE-Inference-Bench shows throughput decreases as active experts increase; e.g., DeepSeek‑V2‑Lite active experts 1→32 drops throughput ~15–20% at large batches (64/128). Source: https://www.arxiv.org/pdf/2508.17467.pdf


## Available Resources

### Videos
- [Switch Transformer (Mixture of Experts) - Paper Explained](https://youtube.com/watch?v=ccBMRryxGog) — Surface when: student asks “how does routing/top‑k work?” or “what’s the load-balancing objective in Switch/MoE?”
- [Let's build GPT: from scratch, in code, spelled out.](https://www.youtube.com/watch?v=kCc8FmEb1nY) — Surface when: student needs grounding in autoregressive generation/Transformer basics before scaling/architecture efficiency.

### Articles & Tutorials
- [Mixture-of-Experts (MoE) — Lilian Weng](https://lilianweng.github.io/posts/2021-09-25-train-large/) — Surface when: student wants a conceptual + practical MoE overview (routing, collapse, balancing).
- [Switch Transformers (paper)](https://arxiv.org/abs/2101.03961) — Surface when: student asks “what did Switch change vs earlier MoE?” (top‑1 simplification; high-level from abstract in this packet).
- [Hugging Face Transformers: Switch Transformers docs](https://huggingface.co/docs/transformers/model_doc/switch_transformers) — Surface when: student asks “how do I use a Switch model in code / what objects exist (router, experts)?”
- [The Transformer Family v2 — Lilian Weng](https://lilianweng.github.io/posts/2023-01-27-the-transformer-family-v2/) — Surface when: student needs broader Transformer architecture context (attention notation, variants) before FlashAttention/MoE discussion.


## Visual Aids

![Chinchilla scaling laws show LLMs are undertrained; tokens matter as much as parameters. (Hoffmann et al., 2022)](/api/wiki-images/scaling-laws/images/magazine-sebastianraschka-p-understanding-large-language-models_015.png)  
Show when: student says “isn’t bigger always better?” or asks for the core Chinchilla takeaway about undertraining and tokens-vs-parameters.

![Language models generate text token-by-token via next-token prediction. (Huyenchip.com)](/api/wiki-images/scaling-laws/images/huyenchip-2023-05-02-rlhf-html_002.gif)  
Show when: student is confused why KV cache exists or why decoding is sequential and memory-heavy.


## Key Sources

- [Scaling Laws for Neural Language Models (Kaplan et al., 2020)](https://arxiv.org/pdf/2001.08361.pdf) — Primary source for loss scaling forms and compute-efficient frontier.
- [Training Compute-Optimal Large Language Models (Hoffmann et al., 2022)](https://arxiv.org/pdf/2203.15556.pdf) — Primary source for Chinchilla compute-optimal \(N,D\) frontier and exponents.
- [FlashAttention (Dao et al., 2022 NeurIPS)](https://proceedings.neurips.cc/paper_files/paper/2022/file/67d57c32e20fd0a7a302cb81d36e40d5-Paper-Conference.pdf) — Authoritative algorithm + benchmark numbers for IO-aware exact attention.
- [Outrageously Large Neural Networks: The Sparsely-Gated MoE Layer (Shazeer et al., 2017)](https://arxiv.org/abs/1701.06538) — Canonical MoE equations and classic load-balancing losses.
- [Efficient Memory Management for LLM Serving with PagedAttention (vLLM)](https://arxiv.org/abs/2309.06180) — Concrete KV-cache sizing and paging-based serving design with throughput claims.