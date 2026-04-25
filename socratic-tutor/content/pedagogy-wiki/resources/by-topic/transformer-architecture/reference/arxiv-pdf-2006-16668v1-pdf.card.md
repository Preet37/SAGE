# Card: GShard MoE Transformer—conditional compute + automatic SPMD sharding
**Source:** https://arxiv.org/pdf/2006.16668v1.pdf  
**Role:** paper | **Need:** PROCESS/ARCHITECTURE  
**Anchor:** System + training pipeline details for large-scale MoE Transformers (top-2 gating, capacity, group dispatch, XLA SPMD sharding/collectives)

## Key Content
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

## When to surface
Use when students ask how large MoE Transformers are *trained efficiently* (capacity/group routing, aux loss), or how **automatic sharding/SPMD + collectives** implement expert-parallel MoE at thousands of devices.