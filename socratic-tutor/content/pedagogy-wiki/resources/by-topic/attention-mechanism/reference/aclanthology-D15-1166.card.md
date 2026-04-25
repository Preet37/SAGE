# Card: Luong Attention (Global vs Local; Dot/General/Concat)
**Source:** https://aclanthology.org/D15-1166/  
**Role:** paper | **Need:** COMPARISON_DATA  
**Anchor:** Side-by-side definitions of attention scoring functions and global vs local attention variants + per-step computation

## Key Content
- **Global attention (per decoder step *t*)** (Section 3):  
  - Alignment scores: \(e_{t,s} = \text{score}(h_t,\bar{h}_s)\) where \(h_t\)=decoder hidden state at time \(t\), \(\bar{h}_s\)=encoder hidden state at source position \(s\).  
  - Attention weights: \(\alpha_{t,s}=\text{softmax}(e_{t,s})\) over all source positions \(s\in[1,S]\).  
  - Context vector: \(c_t=\sum_{s=1}^{S}\alpha_{t,s}\bar{h}_s\).  
  - **Compute cost:** attends to **all** \(S\) source states each step.
- **Attention scoring functions** (Section 3.1):  
  - **Dot:** \(\text{score}(h_t,\bar{h}_s)=h_t^\top \bar{h}_s\). (No extra parameters; requires same dimensionality.)  
  - **General:** \(\text{score}(h_t,\bar{h}_s)=h_t^\top W_a \bar{h}_s\). (Adds matrix \(W_a\).)  
  - **Concat / additive:** \(\text{score}(h_t,\bar{h}_s)=v_a^\top \tanh(W_a [h_t;\bar{h}_s])\). (Adds \(W_a, v_a\); concatenates states.)
- **Local attention** (Section 3.2):  
  - Predict aligned position \(p_t\) and attend only to a **window** around \(p_t\): \(s\in[p_t-D,\,p_t+D]\).  
  - Uses a Gaussian bias around \(p_t\) to downweight far positions (improves efficiency vs global).  
  - **Compute cost:** \(O(2D+1)\) encoder states per step instead of \(O(S)\).
- **Design rationale:** attention mitigates the **fixed-length context bottleneck** of vanilla seq2seq by letting the decoder access encoder states dynamically; local attention trades some flexibility for speed by restricting the attended region.

## When to surface
Use when students ask “what are dot/general/additive attention formulas?”, “global vs local attention—what changes computationally?”, or “how does attention fix the seq2seq bottleneck?”