# Card: GShard MoE top-2 routing + load-balancing loss
**Source:** https://arxiv.org/pdf/2006.16668.pdf  
**Role:** paper | **Need:** FORMULA_SOURCE  
**Anchor:** Exact sparse routing formulation (top-2 gating/dispatch) + auxiliary load-balancing loss to prevent expert imbalance

## Key Content
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

## When to surface
Use when students ask how MoE top-2 routing is computed (capacity, grouping, stochastic 2nd expert) or how GShard’s auxiliary loss mathematically encourages balanced expert utilization / prevents expert collapse.