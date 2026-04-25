# Card: InstructGPT RLHF pipeline (SFT → RM → PPO w/ KL)
**Source:** https://proceedings.neurips.cc/paper_files/paper/2022/file/b1efde53be364a73914f58805a001731-Paper-Conference.pdf  
**Role:** paper | **Need:** CONCEPT_EXPLAINER  
**Anchor:** Step-by-step InstructGPT pipeline + RM loss (ranked comparisons) + PPO w/ KL penalty + selection/early-stopping details

## Key Content
- **3-step RLHF pipeline (Fig. 2; Sec. 3.1):**
  1) **SFT:** collect **labeler demonstrations** on prompts; supervised fine-tune GPT-3.  
  2) **RM:** collect **labeler rankings** of multiple model outputs per prompt; train reward model to predict preferences.  
  3) **PPO:** optimize SFT policy against RM reward using **PPO** in a **bandit** setup; add **per-token KL penalty from SFT** to prevent reward over-optimization; value function initialized from RM. Steps 2–3 can be iterated with new data.
- **Reward model loss (Eq. 1; Sec. 3.4 RM):** labelers rank **K = 4 to 9** responses; train on all \(\binom{K}{2}\) pairs.  
  \[
  \text{loss}(\theta)= -\frac{1}{\binom{K}{2}}\;\mathbb{E}_{(x,y_w,y_l)\sim D}\left[\log \sigma\left(r_\theta(x,y_w)-r_\theta(x,y_l)\right)\right]
  \]
  - \(x\)=prompt, \(y_w\)=preferred completion, \(y_l\)=less-preferred, \(D\)=comparison dataset, \(r_\theta(x,y)\)=scalar RM output, \(\sigma\)=sigmoid.
- **Data + labelers (Sec. 3.2–3.3):** ~**40 contractors**; prompts mostly API + some labeler-written; **>96% English**; PII filtered; train sizes: **SFT 13k prompts**, **RM 33k**, **PPO 31k** (API-only).
- **SFT hyperparams + selection (Sec. 3.4):** **16 epochs**, **cosine LR decay**, **residual dropout 0.2**; select final SFT checkpoint by **RM score on validation** (not val loss).
- **RM choice rationale (Sec. 3.4):** use **6B RM** (compute savings; **175B RM training unstable**, also less suitable as value fn).
- **PPO-ptx rationale (Sec. 4.2):** mix **pretraining-distribution (ptx) gradients** into PPO to reduce regressions on public NLP tasks; performs better than simply increasing KL coefficient.
- **Key empirical results (Abstract; Sec. 4.1):**
  - **1.3B InstructGPT preferred over 175B GPT-3** on their prompt distribution.  
  - **175B InstructGPT preferred to 175B GPT-3: 85 ± 3%**; preferred to **175B GPT-3 few-shot prompted: 71 ± 4%**.
  - Closed-domain hallucination rate: **21% (InstructGPT) vs 41% (GPT-3)**.
  - Inter-annotator agreement: training labelers **72.6 ± 1.5%**; held-out labelers **77.3 ± 1.3%**.

## When to surface
Use when students ask “How does RLHF/InstructGPT work step-by-step?”, “What’s the reward model objective from ranked comparisons?”, or “Why add KL penalties / pretraining-mix (PPO-ptx) during PPO fine-tuning?”