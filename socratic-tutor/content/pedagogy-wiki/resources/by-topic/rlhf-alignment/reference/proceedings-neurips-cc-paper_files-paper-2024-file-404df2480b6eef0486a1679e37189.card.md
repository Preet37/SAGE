# Card: PPO vs DPO in Preference Learning (NeurIPS 2024)
**Source:** https://proceedings.neurips.cc/paper_files/paper/2024/file/404df2480b6eef0486a1679e371894b0-Paper-Conference.pdf  
**Role:** benchmark | **Need:** EMPIRICAL_DATA  
**Anchor:** Head-to-head PPO vs DPO results + ablations (data quality, RM scaling, prompts) + explicit KL-regularized objective

## Key Content
- **PPO objective (Eq. 2, KL-regularized):**  
  \[
  \max_{\pi_\theta}\ \mathbb{E}_{x\sim D_\pi,\ y\sim \pi_\theta(\cdot|x)}[R_\psi(x,y)]\ -\ \beta\, D_{KL}(\pi_\theta\ \|\ \pi_{ref})
  \]  
  - \(D_\pi\): policy-training prompts (unlabeled); \(R_\psi\): reward model; \(\pi_{ref}\): reference policy (usually SFT init); \(\beta\): KL penalty coefficient (tuned; important).
- **Reward model training loss (Eq. 1):**  
  \[
  L_R(\psi)=-\mathbb{E}_{(x,y_c,y_r)\sim D_R}\big[\log \sigma(R_\psi(x,y_c)-R_\psi(x,y_r))\big]
  \]  
  - \(D_R\): preference pairs; \(y_c\) chosen, \(y_r\) rejected.
- **DPO loss (Eq. 3):**  
  \[
  L_{DPO}(\theta)=-\mathbb{E}\Big[\log \sigma\big(\beta\log\frac{\pi_\theta(y_c|x)}{\pi_{ref}(y_c|x)}-\beta\log\frac{\pi_\theta(y_r|x)}{\pi_{ref}(y_r|x)}\big)\Big]
  \]
- **Empirical: PPO > DPO (Table 2, 13B; same data, subsampled to 60,908 ex; p<0.05).** Avg ∆ (PPO−DPO): **Reasoning +1.3**, **Coding +2.9**, **Safety +2.3**, **Truthfulness −2.5**, **Overall +0.7**.  
  UltraFeedback(FG): **DPO avg 61.0 vs PPO avg 62.2**.
- **Preference data quality dominates (Sec. 3.1/Table 1):** UltraFeedback fine-grained **avg 61.0** vs SFT **56.8**; biggest gains in **instruction following & truthfulness (up to +8 pts)**; factuality ~flat (~1 pt spread).
- **Reward model scaling (Table 3):** 70B UltraF RM boosts **GSM 58.0 vs 53.0** (13B UltraF RM) and **avg 62.8 vs 62.2** (small overall gain); RM improvements on RewardBench/BoN often **don’t translate** broadly downstream.
- **Policy prompts (Sec. 3.4/Fig. 3/Table 4):** In-domain GSM prompts + strong (70B) RM can raise GSM **46%→62%** (+16); “mixed” prompt remix **does not improve** generalist overall performance.

## When to surface
Use when students ask: “Is DPO as good as PPO?”, “What objective does PPO optimize in RLHF?”, “Do bigger reward models or better preference datasets matter more?”, or “Do targeted prompts help alignment training?”