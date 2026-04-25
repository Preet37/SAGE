---
title: "Mixture of Experts"
subject: "Large Language Models"
date: 2026-04-09
tags:
  - "subject/large-language-models"
  - "level/intermediate"
  - "level/advanced"
  - "educator/yannic-kilcher"
  - "resource/video"
  - "resource/blog"
  - "resource/deep-dive"
  - "resource/paper"
  - "resource/code"
educators:
  - "Yannic Kilcher"
levels:
  - "intermediate"
  - "advanced"
resources:
  - "video"
  - "blog"
  - "deep-dive"
  - "paper"
  - "code"
---

# Mixture Of Experts

## Video (best)
- **Yannic Kilcher** — "Switch Transformer (Mixture of Experts) - Paper Explained"
- **Watch:** [YouTube](https://www.youtube.com/watch?v=ccBMRryxGog)
- Why: Clear, paper-focused walkthrough of sparse MoE routing, top-k/top-1 gating, and the load-balancing objective used in Switch Transformer.
- Level: Intermediate

## Blog / Written explainer (best)
- **Lilian Weng (OpenAI)** — "Mixture-of-Experts (MoE)"
- **Link:** [https://lilianweng.github.io/posts/2021-09-25-train-large/](https://lilianweng.github.io/posts/2021-09-25-train-large/)
- Why: One of the most complete written explainers of MoE fundamentals (sparse routing, expert specialization, top-k routing) and training issues (load balancing, auxiliary losses, expert collapse).
- Level: Intermediate

## Deep dive
- **NVIDIA Developer Blog** — "Mixture of Experts Explained"
- **Link:** [https://developer.nvidia.com/blog/applying-mixture-of-experts-in-llm-architectures/](https://developer.nvidia.com/blog/applying-mixture-of-experts-in-llm-architectures/)
- Why: Systems-and-training oriented deep dive; useful for understanding practical MoE implementation concerns (capacity, routing, throughput) alongside conceptual grounding.
- Level: Intermediate

## Original paper
- **Fedus, Zoph, Shazeer (2021)** — "Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity"
- **Link:** [https://arxiv.org/abs/2101.03961](https://arxiv.org/abs/2101.03961)
- Why: Canonical modern sparse MoE Transformer design; introduces top-1 routing variant, capacity factor, and the auxiliary load-balancing loss widely reused in later MoE models.
- Level: Advanced

## Code walkthrough
- **Hugging Face Transformers Docs** — "SwitchTransformers"
- **Link:** [https://huggingface.co/docs/transformers/model_doc/switch_transformers](https://huggingface.co/docs/transformers/model_doc/switch_transformers)
- Why: Practical reference for how Switch Transformer is exposed in a mainstream library; helpful for mapping paper concepts (router, experts, capacity) to code-level components.
- Level: Intermediate

## Coverage notes
- Strong: MoE fundamentals (mixture of experts, sparse routing, expert specialization, top-k/top-1 routing); training mechanics (load balancing, auxiliary losses); Switch Transformer as the reference architecture.
- Weak: High-confidence, single-source deep dives specifically on **Mixtral**, **DeepSeek-V2**, and **Grok** MoE design details (beyond general MoE concepts and scattered release materials).
- Gap: A reliable, step-by-step code walkthrough for **Mixtral**-style MoE (and/or DeepSeek-V2) that explains router math, capacity management, and load-balancing losses end-to-end in one place.

---

## Additional Resources for Tutor Depth

> **10 sources** — papers, official docs, working code, benchmarks, and deep explainers that give the AI tutor precision on this topic.

### 📄 DeepSeekMoE efficiency knobs (device-limited routing, balance losses, token dropping)
**Paper** · [source](https://arxiv.org/html/2405.04434v5)

*DeepSeekMoE ablations/metrics + mechanisms for communication-bounded routing and load balance (expert/device/comm) and token dropping.*

<details>
<summary>Key content</summary>

- **MoE FFN computation (Sec. 2.2.1, Eq. 20–22):** For token hidden state \(u_t\), output is sum of **shared experts** + **top-\(K\) routed experts**:  
  \[
  y_t=\sum_{i=1}^{N_s}E^{(s)}_i(u_t)+\sum_{j\in \text{TopK}(t)} g_{t,j}\,E^{(r)}_j(u_t)
  \]
  where \(N_s\)=# shared experts, \(N_r\)=# routed experts, \(K\)=# activated routed experts, \(g_{t,j}\)=gate value; routing uses token-to-expert affinity scores vs expert centroids \(c_j\) (TopK over affinities).
- **Device-limited routing (Sec. 2.2.2):** Beyond naive top-\(K\), constrain each token’s selected experts to lie on **at most \(M\) devices** to bound all-to-all communication. Procedure: (1) pick devices with highest-affinity experts; (2) do top-\(K\) among experts on those devices. Empirically, **\(M=3\)** gives performance “roughly aligned” with unrestricted top-\(K\).
- **Three auxiliary load-balance losses (Sec. 2.2.3):** expert-level \(L_{\text{exp}}\), device-level \(L_{\text{dev}}\), communication balance \(L_{\text{comm}}\). Device-level groups experts per device; communication loss encourages each device to **receive ~\(B/D\)** hidden states (balanced exchange), while device-limited routing bounds sending.
- **Token-dropping (Sec. 2.2.4):** device-level capacity factor **=1.0**; drop lowest-affinity tokens per device until budget met; ensure tokens from **~10% of sequences are never dropped**. Train with dropping; evaluation uses **no dropping**; inference may choose to drop for efficiency while matching training.
- **Concrete training config (Sec. 3.1.2):** 60 layers, hidden 5120; MoE in all FFNs except first; each MoE layer: **2 shared + 160 routed experts**, expert FFN intermediate dim **1536**, activate **\(K=6\)** routed experts/token; experts spread across **8 devices** (\(D=8\)); device-limited routing **\(M=3\)**. Balance-loss weights: **\(L_{\text{exp}}:0.003\), \(L_{\text{dev}}:0.05\), \(L_{\text{comm}}:0.02\)**.
- **Efficiency outcomes (Sec. 3.2.3):** vs DeepSeek 67B, DeepSeek-V2 saves **42.5%** training cost (GPU hours per 1T tokens: **300.6K → 172.8K**); inference throughput **5.76×** (single node 8×H800: **>50K tok/s** generation; **>100K tok/s** prompt).

</details>

### 📄 GShard MoE top-2 routing + load-balancing loss
**Paper** · [source](https://arxiv.org/pdf/2006.16668.pdf)

*Exact sparse routing formulation (top-2 gating/dispatch) + auxiliary load-balancing loss to prevent expert imbalance*

<details>
<summary>Key content</summary>

- **MoE layer equations (Section 2.2, Eq. 1–3):** For token input \(x_s\) and \(E\) experts:  
  - Gates: \(G_{s,1:E}=\mathrm{GATE}(x_s)\) (Eq. 1), sparse (mostly zeros), dispatch to ≤2 experts.  
  - Expert FFN: \(\mathrm{FFN}_e(x_s)=w^o_e\cdot \mathrm{ReLU}(w^i_e\cdot x_s)\) (Eq. 2).  
  - Output: \(y_s=\sum_{e=1}^{E} G_{s,e}\,\mathrm{FFN}_e(x_s)\) (Eq. 3).
- **Group-level top-2 gating algorithm (Algorithm 1):**  
  - Partition batch tokens into \(G\) groups; group size \(S=N/G\).  
  - Compute per-token softmax gates: \(g_{s,e}=\mathrm{softmax}(w_g x_s)\).  
  - Pick \((e_1,e_2)=\mathrm{top2}(g_{s,:})\); normalize \(g_1\leftarrow g_1/(g_1+g_2)\).  
  - **Capacity constraint:** per-group expert capacity \(C\) (fractional capacity; overall expert capacity \(\approx O(N/E)\)). Maintain counters \(c_e\); if \(c_{e}\ge C\), token overflows (gate becomes zero; residual path carries representation).  
  - **Second expert stochastic routing:** normalize \(g_2\leftarrow g_2/(g_1+g_2)\); dispatch to \(e_2\) if \(2g_2>\mathrm{Uniform}(0,1)\) and capacity allows.
- **Auxiliary load-balancing loss (Algorithm 1, line 13):**  
  - Mean gate per expert: \(m_e=\frac{1}{S}\sum_{s=1}^S g_{s,e}\).  
  - Loss: \(\ell_{\text{aux}}=\frac{1}{E}\sum_{e=1}^E \left(\frac{c_e}{S}\right)m_e\).  
  - Total loss: \(L=\ell_{\text{nll}}+k\,\ell_{\text{aux}}\) (constant multiplier \(k\)).
- **Linear-algebra implementation (Algorithm 2):** uses tensors `combine_weights` \([G,S,E,C]\) and `dispatch_mask` to dispatch via einsums; resharding uses AllToAll.
- **Empirical scaling result (Figure 1):** scaling MoE from **37.5B→600B params (16×)** increased training cost **6→22 TPU v3 core-years (3.6×)**; **600B** trained on **2048 TPU v3 cores for 4 days**.

</details>

### 📄 Sparsely-Gated MoE (Noisy/Top‑k gating + balancing)
**Paper** · [source](https://arxiv.org/abs/1701.06538)

*Original sparsely-gated MoE equations (top‑k mask / sparse gating) + classic expert-usage balancing losses; key scaling results.*

<details>
<summary>Key content</summary>

- **MoE output (Eq. 1, Section 3):**  
  \[
  y=\sum_{i=1}^{n} G(x)_i\,E_i(x)
  \]
  where \(n\)=#experts, \(E_i(x)\)=expert output, \(G(x)\in\mathbb{R}^n\)=sparse gate weights.
- **Sparse gating via mask + renorm (Eq. 3, Section 3.1):**  
  \[
  G(x)_i=\frac{G_\sigma(x)_i\,M(G_\sigma(x))_i}{\sum_{j=1}^{n}G_\sigma(x)_j\,M(G_\sigma(x))_j}
  \]
  \(G_\sigma(x)\)=dense pre-mask gate scores; \(M(\cdot)\)=mask (e.g., TopK).
- **Top‑k routing mask (Section 3.1):** keep only the top \(k\) experts per example (others set to 0), enforcing per-example sparsity; typical \(k\) values used include **4** (many experiments) and **8** (small-model LM setting).
- **Expert imbalance problem + soft balancing (Section 4 / 3.2):**
  - **Importance per expert over batch \(X\) (Eq. 6):**  
    \[
    \text{Importance}(X)=\sum_{x\in X} G(x)
    \]
  - **Importance loss (Eq. 7):**  
    \[
    L_{\text{importance}}(X)=w_{\text{importance}}\cdot \mathrm{CV}(\text{Importance}(X))^2
    \]
    (CV = coefficient of variation across experts).
  - **Alternative balance loss (Eq. 5 in excerpt):** \(\ell_2\) loss between batch-mean gate and uniform:  
    \[
    L_{\text{balance}}(X)=\frac12\sum_{i=1}^{n}\left(\frac{1}{|X|}\sum_{x\in X}G(x)_i-\frac{1}{n}\right)^2
    \]
- **Scaling/efficiency results (LM):**
  - **1B Word benchmark:** low-compute MoE with **4096 experts** (4 active/input) achieved **24% lower test perplexity** vs compute-matched baselines; largest reported hierarchical MoE up to **32768 experts** reached **test ppl 36.8** (small-model setting).  
  - **Very large MoE:** up to **65536 experts** (~**99.994% sparsity**) maintained ~**0.72 TFLOPS/GPU**; MoE layer up to **137B parameters** reported.
- **System/training procedure (Section 4):** mitigate “shrinking batch” by **combining routed examples across data-parallel replicas** so each expert sees ~\(k b d / n\) examples (batch \(b\), devices \(d\)).

</details>

### 📊 Mixtral 8x7B inference on H100 + TensorRT-LLM (throughput/latency, FP8, batching)
**Benchmark** · [source](https://developer.nvidia.com/blog/achieving-high-mixtral-8x7b-performance-with-nvidia-h100-tensor-core-gpus-and-tensorrt-llm/)

*Production-oriented Mixtral 8x7B serving results + system optimizations (TensorRT-LLM on 2× H100 SXM), with FP16 vs FP8 comparisons.*

<details>
<summary>Key content</summary>

- **MoE routing (Mixtral 8x7B, quoted from paper):** Each layer has **8 experts (FFN blocks)**; for **every token at each layer**, a **router selects top-2 experts** and **combines outputs** (weighted).  
  - **Capacity vs active params:** token has access to **47B parameters**, but uses **13B active parameters** during inference (due to sparse top-2 routing).
- **Serving workflow / design choices:**
  - **In-flight batching:** during serving, **completed requests are replaced with new requests** to improve throughput under latency targets.
  - **Deployment tuning rationale:** choose a **response-time budget** by examining the **throughput–latency curve**; production targets often sit in a “steep” region where **small latency increases yield large throughput gains**.
- **Benchmark configuration (key defaults):**
  - **Hardware/software:** **2× NVIDIA H100 SXM**, **TensorRT-LLM v0.10**, **CUDA 12.4 (12.4.131)**.
  - **Parallelism:** **Tensor Parallel (TP)=2**.
  - **Online test lengths:** **Avg ISL=573**, **Avg OSL=50**.
  - **Offline test lengths:** **ISL=128**, **OSL=128**; batch sizes swept up to **1024**.
- **Empirical results (specific numbers):**
  - **FP8 benefit (online):** **~50% more throughput** than FP16 **within a 0.5 s response limit** (H100 FP8 vs FP16).
  - **Streaming mode point:** at **mean time/output token = 0.016 s** (~**>60 tok/s** per user), **2×H100 FP8** achieves **38.4 requests/s**.
  - **Offline peak:** at **batch size 1024**, throughput reaches **~21,000 tokens/s** with **FP8**.
- **Why FP8:** H100 **4th-gen Tensor Cores** support **FP8 at ~2× peak compute** vs FP16/BF16; FP8 also **reduces memory footprint**, enabling larger batches.

</details>

### 📊 MoE-Inference-Bench (MoE inference bottlenecks & deployment levers)
**Benchmark** · [source](https://arxiv.org/html/2508.17467v1)

*Benchmark results quantifying MoE inference bottlenecks (routing/load imbalance) + throughput/latency comparisons across MoE models & serving optimizations (H100, vLLM)*

<details>
<summary>Key content</summary>

- **Metrics & formulas (Sec. 3.4):**
  - **TTFT**: time from prompt receipt → first generated token (measured by setting max output length = 1).
  - **ITL (Eq. 1)**: average time between consecutive output tokens (per-token decode latency).
  - **Throughput (Eq. 2)**: tokens/sec computed from end-to-end latency: total tokens processed (input+output) divided by total time from submission → final token.
- **Benchmark setup defaults (Sec. 3.2–3.3):** Nvidia **H100 SXM5 80GB**, **vLLM**. Input/output lengths: **128, 256, 512, 1024, 2048** tokens. Batch sizes: **1, 16, 32, 64** (some plots also discuss up to 128).
- **Model architecture rows (Table 1):**
  - **Mixtral-8×7B:** 32 layers, d_model 4096, FFN 14336, **8 experts**, **top-2**, total **47B**, active **12.9B**.
  - **Qwen3-30B-A3B:** 48 layers, **128 experts**, **top-8**, total **30.5B**, active **3.3B**.
  - **DeepSeek-V2-Lite:** 27 layers, **64 experts**, **top-6**, total **15.7B**, active **2.4B**.
  - **OLMoE-1B-7B:** 16 layers, **64 experts**, **top-8**, total **7.2B**, active **1.3B**.
- **Empirical bottlenecks & trade-offs:**
  - **More active experts ⇒ lower throughput** (Sec. 4.2, Fig. 5): DeepSeek-V2-Lite active experts **1→32** drops throughput **~15–20%** at large batches (64/128) vs **~5–8%** at small batches (1/16). Qwen1.5-MoE shows **~12–18%** (large) vs **~4–7%** (small).
  - **Sequence length effect** (Sec. 4.3, Fig. 6): length **128** yields up to **~30% higher throughput** than **2048** at large batches; long lengths (1024–2048) can degrade throughput **>20%**.
  - **Active-expert scaling lever** (Sec. 5.4, Fig. 9): **top-1** can be **50–80% higher throughput** than **top-8**, especially at large FFN dims.
  - **FFN dim scaling** (Sec. 5.2, Fig. 7): increasing FFN dim **1792→14336** reduces throughput **~50%** on average; at FFN 14336, **top-1 vs top-8 gap ~60%** (bandwidth saturation regime).
- **Deployment optimizations (Secs. 6–7):**
  - **FP8 quantization** (Sec. 6.1, Fig. 10): Mixtral FP8 gives **~20–25%** throughput gain across lengths; up to **~25–30%** at highest batch vs FP16.
  - **Fused MoE kernel** (Sec. 7.2, Fig. 14): **~15–20%** throughput gain when scaling batch; **~12–18%** across sequence lengths.
  - **Parallelism** (Sec. 7.1, Fig. 13): **Tensor parallelism (TP)** scales best on multi-H100 (NVLink); **pipeline (PP)** and **expert parallelism (EP)** show poorer scaling due to stage imbalance + dispatch/load-balance overhead.

</details>

### 📊 MoE-Inference-Bench (MoE inference performance + routing/imbalance effects)
**Benchmark** · [source](https://www.arxiv.org/pdf/2508.17467.pdf)

*Stable benchmark figures/tables on routing (Top‑k/active experts), imbalance, and end‑to‑end inference performance (H100, vLLM)*

<details>
<summary>Key content</summary>

- **Metrics & formulas (Section 3.4):**
  - **TTFT**: time from prompt receipt to first generated token (measured by setting max output length = 1).
  - **ITL (Eq. 1)**: average time between consecutive generated tokens (per-token decode latency).
  - **Throughput (Eq. 2)**: tokens/sec computed from end-to-end latency:  
    \[
    \text{Throughput}=\frac{\text{#input tokens}+\text{#output tokens}}{\text{end-to-end latency (s)}}
    \]
  - **VLM metric:** samples/sec (image+text samples processed per second).
- **Experimental defaults (Sections 3.2–3.3):** input/output lengths ∈ {128, 256, 512, 1024, 2048}; batch sizes ∈ {1, 16, 32, 64}. Hardware: **NVIDIA H100 SXM5 80GB**, framework **vLLM**.
- **Model architecture table (Table 1 examples):**
  - **Mixtral‑8×7B:** 32 layers, d_model 4096, FFN 14336, **8 experts**, **Top‑k=2**, total params **47B**, active params **12.9B**.
  - **Qwen3‑30B‑A3B:** 48 layers, **128 experts**, **Top‑k=8**, total **30.5B**, active **3.3B**.
  - **OLMoE‑1B‑7B:** 16 layers, **64 experts**, **Top‑k=8**, total **7.2B**, active **1.3B**.
- **Empirical routing/Top‑k effects (Figure 5):** throughput **decreases as active experts increase**; for **DeepSeek‑V2‑Lite**, active experts 1→32 causes ~**15–20%** throughput drop at large batches (64/128) vs **5–8%** at small batches (1/16). **Qwen1.5‑MoE‑A2.7B**: ~**12–18%** (large) vs **4–7%** (small).
- **Sequence length effects (Figure 6):** at large batches, length **128** yields up to **~30%** higher throughput than **2048**; long lengths (1024–2048) degrade throughput **>20%** (DeepSeek‑V2‑Lite).
- **Hyperparameter scaling (Section 5):**
  - **FFN dim 1792→14336**: throughput drops **~50% avg** (Figure 7); at FFN=14336, **1 vs 8 active experts** gap ~**60%**.
  - **Active experts 1→8**: **50–80%** higher throughput for single-expert vs 8-expert configs (Figure 9), especially at large FFNs.
- **Optimization results:**
  - **FP8 vs FP16 (Figure 10):** FP8 gives **~20–25%** throughput gain across lengths; up to **~25–30%** at highest batch size.
  - **Fused MoE (Figure 14):** **~15–20%** higher throughput when scaling batch size; **~12–18%** across sequence lengths.
- **Load balancing evidence (Figure 15):** DeepSeek‑VL2 shows **uniform expert activation**; MolmoE‑1B shows skew (peaks **~1M** activations vs DeepSeek‑VL2 peak **~290K**). DeepSeek‑V2 uses an **auxiliary loss** to balance expert utilization.

</details>

### 📖 DeepSpeed MoE API + Inference/Training Defaults
**Reference Doc** · [source](https://deepspeed.readthedocs.io/en/latest/moe.html)

*Authoritative DeepSpeed MoE API surface and defaults (k, capacity_factor/eval_capacity_factor, min_capacity, noisy_gate_policy, drop_tokens, ep_size, use_rts, top2_2nd_expert_sampling)*

<details>
<summary>Key content</summary>

- **Core layer API:** `deepspeed.moe.layer.MoE(hidden_size, expert, num_experts=1, ep_size=1, k=1, capacity_factor=1.0, eval_capacity_factor=1.0, min_capacity=4, use_residual=False, noisy_gate_policy=None, drop_tokens=True, use_rts=True, use_tutel=False, enable_expert_tensor_parallelism=False, top2_2nd_expert_sampling=True)`
  - `k` = top-k routing; **only supports k=1 or k=2**.
  - `noisy_gate_policy` valid: **'Jitter', 'RSample', 'None'**.
  - `drop_tokens=False` is **equivalent to infinite capacity**.
  - `use_rts=True` enables **Random Token Selection** (RTS) by default (convergence improvement).
- **Forward signature/returns:** `forward(hidden_states, used_token=None) -> (output, l_aux, exp_counts)`
  - `used_token`: mask for only used tokens.
  - Returns: model output tensor, **gate loss** `l_aux`, and **expert counts** `exp_counts`.
- **Capacity sizing knobs (training vs eval):** `capacity_factor` (train), `eval_capacity_factor` (eval), with floor `min_capacity` per expert.
- **Expert parallelism:** `ep_size` = number of ranks in expert-parallel group; layer accepts `ep_size` directly (older `groups.initialize(ep_size=...)` is deprecated).
- **PR-MoE (Pyramid-Residual MoE):** pass `num_experts` as a **list** (e.g., `[4, 8]`) and set `use_residual=True`.
- **Inference workflow:** use `deepspeed.init_inference(model, mp_size=..., dtype=torch.half, moe_experts=..., checkpoint=..., replace_with_kernel_inject=True)`.
- **Empirical scaling/results:** DS-MoE inference reports **24%–60%** speedup vs PyTorch (generic) and **2x–3.2x** (specialized) on 8/16/32 GPUs; up to **7.3x** latency reduction; trillion-parameter MoE inference **<25 ms**; up to **4.5x faster** and **9x cheaper** vs quality-equivalent dense.
- **Example model fact:** Switch Transformer **1.6T params** with compute ~ **10B dense**.

</details>

### 📖 DeepSpeed MoE API + key defaults
**Reference Doc** · [source](https://docs.deepspeed.org.cn/en/latest/moe.html)

*DeepSpeed `deepspeed.moe.layer.MoE` parameter names + defaults; MoE parallelism + inference init knobs*

<details>
<summary>Key content</summary>

- **MoE layer signature (API + defaults):**  
  `deepspeed.moe.layer.MoE(hidden_size:int, expert:Module, num_experts:int=1, ep_size:int=1, k:int=1, capacity_factor:float=1.0, eval_capacity_factor:float=1.0, min_capacity:int=4, use_residual:bool=False, noisy_gate_policy:Optional[str]=None, drop_tokens:bool=True, use_rts:bool=True, use_tutel:bool=False, enable_expert_tensor_parallelism:bool=False, top2_2nd_expert_sampling:bool=True)`  
  - `k` supports **only 1 or 2** (top-k routing).  
  - `noisy_gate_policy` valid: **'Jitter'**, **'RSample'**, **'None'** (default `None`).  
  - `drop_tokens=False` ⇒ “equivalent to **infinite capacity**”.
- **Forward outputs:** `forward(hidden_states, used_token=None) -> (output, l_aux, exp_counts)`  
  - `l_aux`: gate loss (load-balancing auxiliary loss); `exp_counts`: per-expert token counts.
- **Capacity concept (operational):** expert capacity controlled by `capacity_factor` (train) / `eval_capacity_factor` (eval) with floor `min_capacity=4`.
- **Parallelism knobs:** `ep_size` passed per-layer (old `deepspeed.utils.groups.initialize(ep_size=...)` is **deprecated**). Ranks in an expert-parallel group of size `ep_size` **distribute** the layer’s `num_experts`.
- **Training procedure (optimizer param groups):**  
  Use `split_params_into_different_moe_groups_for_optimizer` to create MoE/non-MoE param groups before `deepspeed.initialize(...)`.
- **Inference init (key args):** `deepspeed.init_inference(moe_model, mp_size=..., dtype=torch.half, moe_experts=..., checkpoint=..., replace_with_kernel_inject=True)`
- **Empirical scaling claims:** Switch Transformer **1.6T params** at ~**10B dense compute**; DS-MoE inference reports up to **7.3×** latency/cost reduction vs baseline MoE systems and up to **4.5× faster / 9× cheaper** vs quality-equivalent dense.

</details>

### 📋 # Source: https://deepspeed.readthedocs.io/en/stable/_modules/deepspeed/moe/layer.html
**Source** · 

### 📋 DeepSpeed CIFAR-10 training scaffold (MoE flags + ZeRO + dtype)
**Code** · [source](https://github.com/deepspeedai/DeepSpeedExamples/blob/master/training/cifar/cifar10_deepspeed.py)

*End-to-end runnable DeepSpeed entrypoint showing how MoE is enabled/configured via CLI flags and how to initialize DeepSpeed (model/optimizer/dataloader) with ZeRO + fp16/bf16.*

<details>
<summary>Key content</summary>

- **CLI switches (MoE + training):**
  - `--epochs` default **30**
  - `--dtype` ∈ {`bf16`,`fp16`,`fp32`} default **fp16**
  - `--stage` (ZeRO) ∈ {0,1,2,3} default **0**
  - `--moe` (bool) enable Mixture-of-Experts path
  - `--ep-world-size` default **1** (expert-parallel world size)
  - `--num-experts` list default **[1]**
  - `--mlp-type` default **"standard"** (when `num-experts > 1`, accepts `standard` or `residual`)
  - `--top-k` default **1** (top-1 or top-2 gating supported)
  - `--min-capacity` default **0** (minimum tokens per expert regardless of capacity factor)
  - `--noisy-gate-policy` default **None** (top-1 only; valid: `RSample`, `Jitter`)
  - `--moe-param-group` (bool) create separate MoE param groups (required when using ZeRO with MoE)
- **MoE optimizer param grouping procedure:**
  - Build a single param dict: `{"params": [p for p in model.parameters()], "name": "parameters"}`
  - Call `split_params_into_different_moe_groups_for_optimizer(parameters)` to separate expert params for optimizer/ZeRO.
- **DeepSpeed config defaults (numbers):**
  - `train_batch_size: 16`, `steps_per_print: 2000`
  - Optimizer Adam: `lr=0.001`, `betas=[0.8,0.999]`, `eps=1e-8`, `weight_decay=3e-7`
  - WarmupLR: `warmup_min_lr=0`, `warmup_max_lr=0.001`, `warmup_num_steps=1000`
  - `gradient_clipping: 1.0`, `prescale_gradients: False`
  - ZeRO: `stage=args.stage`, `allgather_bucket_size=5e7`, `reduce_bucket_size=5e7`, `overlap_comm=True`, `contiguous_gradients=True`, `cpu_offload=False`
- **Training loop workflow:**
  1. `deepspeed.initialize(args, model, model_parameters, training_data, config)`
  2. Determine device via `get_accelerator().device_name(local_rank)`; set `target_dtype` to bf16/fp16 if enabled.
  3. Forward: `outputs = model_engine(inputs)`; loss: `CrossEntropyLoss`.
  4. Backprop/step: `model_engine.backward(loss)` then `model_engine.step()`.
  5. Log every `--log-interval` (default **2000**) minibatches on rank 0.

</details>

---

## Related Topics

- [[topics/scaling-laws|Scaling Laws]]
- [[topics/transformer-architecture|Transformer Architecture]]
- [[topics/inference-optimization|Inference Optimization]]
- [[topics/pre-training|Pre-Training]]
