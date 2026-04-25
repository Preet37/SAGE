# Card: MIXER—Sequence-level expected reward + REINFORCE gradient + curriculum
**Source:** https://michaelauli.github.io/papers/iclr2016_mixer.pdf  
**Role:** paper | **Need:** FORMULA_SOURCE  
**Anchor:** MIXER sequence-level expected reward objective and REINFORCE-style gradient estimator for directly optimizing BLEU/ROUGE, incl. curriculum from cross-entropy to sequence-level training

## Key Content
- **RNN next-word model (Eq. 1–5):**  
  \(h_{t+1}=\phi_\theta(w_t,h_t,c_t)\) (Eq.1); \(w_{t+1}\sim p_\theta(w\mid w_t,h_{t+1})\) (Eq.2).  
  Elman: \(h_{t+1}=\sigma(M_i\mathbf{1}(w_t)+M_h h_t+M_c c_t)\) (Eq.3); \(o_{t+1}=M_o h_{t+1}\) (Eq.4); \(w_{t+1}\sim \text{softmax}(o_{t+1})\) (Eq.5).
- **Cross-entropy objective (Eq.6):**  
  \(L=-\log p(w_1,\dots,w_T)=-\sum_{t=1}^T \log p(w_t\mid w_{1:t-1})\).
- **Greedy decoding (Eq.7):** \(w^g_{t+1}=\arg\max_w p_\theta(w\mid w^g_t,h_{t+1})\). Exposure bias: train on \(w_t\) (gold), test on \(w^g_t\) (model).
- **Sequence-level expected reward (REINFORCE) (Eq.9):**  
  \(L_\theta=-\sum_{w^g_{1:T}} p_\theta(w^g_{1:T})\, r(w^g_{1:T}) = -\mathbb{E}_{w^g_{1:T}\sim p_\theta}[r]\). Reward \(r\): BLEU or ROUGE-2.
- **REINFORCE gradient signal (Eq.10–11):**  
  \(\frac{\partial L_\theta}{\partial \theta}=\sum_t \frac{\partial L_\theta}{\partial o_t}\frac{\partial o_t}{\partial \theta}\) (Eq.10), with  
  \(\frac{\partial L_\theta}{\partial o_t}=(r-\bar r_{t+1})\big(p_\theta(w_{t+1}\mid w^g_t,h_{t+1},c_t)-\mathbf{1}(w^g_{t+1})\big)\) (Eq.11). Baseline \(\bar r_t\): linear regressor on \(h_t\), trained by MSE \(\|\bar r_t-r\|^2\); no backprop into RNN.
- **MIXER procedure (Sec.3.2.2, Alg.1):**  
  1) Pretrain \(N_{\text{XENT}}\) epochs with XENT (optimal-ish policy).  
  2) For curriculum \(s=T, T-\Delta, \dots, 1\): train \(N_{\text{XE+R}}\) epochs using XENT for first \(s\) steps, then sample from model and apply REINFORCE for remaining \(T-s\) steps. Typical \(\Delta=2\) or \(3\).
- **Key results (Fig.5, greedy decoding):**  
  Summarization ROUGE-2: XENT 13.01, DAD 12.18, E2E 12.78, **MIXER 16.22**.  
  Translation BLEU-4: XENT 17.74, DAD 20.12, E2E 17.77, **MIXER 20.73**.  
  Image captioning BLEU-4: XENT 27.8, DAD 28.16, E2E 26.42, **MIXER 29.16**.
- **Best MIXER schedule params (Table 2):**  
  Summarization \(N_{\text{XENT}}=20, N_{\text{XE+R}}=5, \Delta=2\); Translation \(25,5,3\); Captioning \(20,5,2\).
- **Rationale:** REINFORCE from random fails in huge action spaces (\(|V|\sim10^4\), search \(O(W^T)\)); MIXER starts from XENT policy (perplexity ~50 vs ~10,000 random) and gradually shifts to sampling to reduce exposure bias + optimize non-differentiable metrics.

## When to surface
Use when students ask how to directly optimize BLEU/ROUGE (non-differentiable), how REINFORCE gradients look for seq2seq generation, or how MIXER’s curriculum transitions from teacher forcing (XENT) to fully sampled sequence-level training to address exposure bias.