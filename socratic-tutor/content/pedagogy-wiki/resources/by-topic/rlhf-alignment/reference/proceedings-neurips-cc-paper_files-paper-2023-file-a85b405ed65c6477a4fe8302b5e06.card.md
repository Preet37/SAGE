# Card: Direct Preference Optimization (DPO) objective & link to KL-RLHF
**Source:** https://proceedings.neurips.cc/paper_files/paper/2023/file/a85b405ed65c6477a4fe8302b5e06ce7-Paper-Conference.pdf  
**Role:** paper | **Need:** FORMULA_SOURCE  
**Anchor:** Closed-form DPO objective/derivation (logistic loss on preference pairs), explicit connection to KL-regularized RL and the role of the reference policy π_ref.

## Key Content
- **Preference model (Bradley–Terry)** (Eq. 1):  
  \(p^*(y_1 \succ y_2 \mid x)=\frac{\exp(r^*(x,y_1))}{\exp(r^*(x,y_1))+\exp(r^*(x,y_2))}=\sigma(r^*(x,y_1)-r^*(x,y_2))\).  
  Dataset \(D=\{(x^{(i)},y_w^{(i)},y_l^{(i)})\}_{i=1}^N\).
- **Reward-model loss** (Eq. 2):  
  \(L_R(r_\phi,D)=-\mathbb{E}_{(x,y_w,y_l)\sim D}\big[\log \sigma(r_\phi(x,y_w)-r_\phi(x,y_l))\big]\).
- **KL-regularized RLHF objective** (Eq. 3):  
  \(\max_{\pi_\theta}\ \mathbb{E}_{x\sim D,\,y\sim\pi_\theta(\cdot|x)}[r_\phi(x,y)]-\beta\,D_{KL}(\pi_\theta(\cdot|x)\|\pi_{ref}(\cdot|x))\).  
  Typically \(\pi_{ref}=\pi_{SFT}\); \(\beta\) controls deviation.
- **Optimal policy under KL constraint** (Eq. 4):  
  \(\pi_r(y|x)=\frac{1}{Z(x)}\pi_{ref}(y|x)\exp(\tfrac{1}{\beta}r(x,y))\).
- **Reward–policy reparameterization** (Eq. 5):  
  \(r(x,y)=\beta\log\frac{\pi_r(y|x)}{\pi_{ref}(y|x)}+\beta\log Z(x)\).  
  In BT differences, \(\log Z(x)\) cancels → preferences depend only on log-ratios.
- **DPO loss (closed form)** (Eq. 7):  
  \(L_{DPO}(\pi_\theta;\pi_{ref})=-\mathbb{E}_{(x,y_w,y_l)\sim D}\Big[\log \sigma\big(\beta\log\frac{\pi_\theta(y_w|x)}{\pi_{ref}(y_w|x)}-\beta\log\frac{\pi_\theta(y_l|x)}{\pi_{ref}(y_l|x)}\big)\Big]\).  
  Implicit reward: \(\hat r_\theta(x,y)=\beta\log\frac{\pi_\theta(y|x)}{\pi_{ref}(y|x)}\).
- **Procedure** (Section 4): (1) sample pairs from \(\pi_{ref}\), label preferences → \(D\); (2) optimize \(\pi_\theta\) by minimizing \(L_{DPO}\). If no SFT: set \(\pi_{ref}=\arg\max_\pi \mathbb{E}_{(x,y_w)\sim D}[\log \pi(y_w|x)]\).
- **Empirical numbers:** TL;DR summarization win rate vs reference summaries: **DPO ~61% (temp 0.0)** vs **PPO ~57% (temp 0.0)**; DPO more robust to sampling temperature. OOD CNN/DailyMail win vs ground-truth summaries (Table 1): **DPO 0.36 (temp 0)** vs **PPO 0.26 (temp 0)**.
- **Hyperparameter sweeps reported:** DPO \(\beta\in\{0.05,0.1,1,5\}\); PPO target KL \(\in\{3,6,9,12\}\).

## When to surface
Use when students ask for the *exact DPO objective*, how it derives from *KL-regularized RLHF*, why \(\pi_{ref}\) appears, or for concrete win-rate comparisons between DPO and PPO.