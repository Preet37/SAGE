# Card: ImitKD = DAgger-style distillation to fix exposure bias
**Source:** https://aclanthology.org/2020.emnlp-main.494.pdf  
**Role:** paper | **Need:** FORMULA_SOURCE  
**Anchor:** Formal mapping from exposure bias → imitation learning; DAgger-style mixture state distributions + objectives for seq2seq distillation

## Key Content
- **Autoregressive model factorization (Eq. 1):**  
  \[
  \pi(y)=\prod_{t=1}^{T}\pi(y_t\mid y_{<t})
  \]
  with source conditioning \(x\) implicit in later equations.
- **General distillation objective (Eq. 2):**  
  \[
  L(\pi)=\mathbb{E}_{y|x\sim D}\Big[\sum_{t=1}^{T}\ell_{\pi^*}(y_{<t},x;\pi)\Big]
  \]
  where \(D\) is the training state/trajectory distribution; \(\ell_{\pi^*}\) measures teacher–student next-token discrepancy.
- **SeqKD as behavioral cloning (Eq. 3):** teacher generates mode \(y^*=\arg\max_{y'}\pi^*(y'|x)\) (beam search), train student by NLL:  
  \[
  L_{\text{SeqKD}}(\pi)=\mathbb{E}_{y^*|x\sim D^*}\Big[\sum_{t}-\log \pi(y_t^*\mid y_{<t}^*,x)\Big]
  \]
  Exposure bias: trained on teacher states \(D^*\), tested on student-induced states; behavioral cloning regret scales **quadratically in horizon \(T\)** (Ross & Bagnell 2010, cited).
- **ImitKD objective (Eq. 4):** train on **mixture** \(\tilde D\) of initial data \(D\) and student rollouts \(D_\pi\):  
  \[
  L_{\text{ImitKD}}(\pi)=\mathbb{E}_{y|x\sim \tilde D}\Big[\sum_{t}\ell_{\pi^*}(y_{<t},x;\pi)\Big]
  \]
  Loss options: **optimal-token** (Eq. 5) with \(v^*=\arg\max_v \pi^*(v|y_{<t},x)\): \(-\log \pi(v^*|y_{<t},x)\); or **full dist. cross-entropy** (Eq. 6): \(-\sum_v \pi^*(v|\cdot)\log \pi(v|\cdot)\).
- **Algorithm 1 (ImitKD, batch “replacement”):** for each minibatch, sample \(e=y|x\sim D\); with prob \(1-\beta_i\) replace \(y\) by student generation \(\hat y\sim \pi_i(\cdot|x)\); compute teacher-based loss on resulting \(\tilde D_i\); SGD update \(\pi_{i+1}\leftarrow \pi_i-\alpha_i\nabla L_{\text{ImitKD}}\). **Anneal** \(\beta_i\) via exponential decay: \(\beta_i=r^{i/I}\) (final mixing rate \(r\)).
- **DAgger reference (Appendix A.1, Alg. 2):** mixture policy \(\tilde\pi_i=\beta_i\pi^*+(1-\beta_i)\pi_i\); aggregate states over iterations; yields **linear regret in \(T\)** under strong convexity (Ross et al. 2011, cited).
- **Key empirical numbers (IWSLT14 De→En, Table 3):** Teacher 8-layer Transformer BLEU1 **34.4**. Student SRU(2-layer): Vanilla BLEU1 **29.5**, SeqKD **32.0**, **ImitKD 33.3**, **ImitKD+Full 33.7**. SRU(3-layer) ImitKD+Full BLEU1 **34.8** (slightly > teacher).  
  Exposure-bias effect: improvements largest for **longer sequences** (Figure 1).
- **Defaults/params (Appendix A.2):** IWSLT: final mixing rate **r=0.005**, top-K sampling **K=5**, pool refresh **M=4**. SeqKD beam size **5**. CNN/DM: r=**0.1**, greedy during training.

## When to surface
Use when students ask why **teacher forcing/SeqKD causes exposure bias**, how to formalize seq2seq generation as **imitation learning**, or how **DAgger-style mixture training** changes the objective/state distribution and reduces error compounding.