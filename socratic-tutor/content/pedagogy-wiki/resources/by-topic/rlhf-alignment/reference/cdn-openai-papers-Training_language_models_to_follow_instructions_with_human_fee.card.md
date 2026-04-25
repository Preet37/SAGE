# Card: InstructGPT RLHF pipeline (SFT → RM → PPO w/ KL + pretraining mix)
**Source:** https://cdn.openai.com/papers/Training_language_models_to_follow_instructions_with_human_feedback.pdf  
**Role:** paper | **Need:** DEPLOYMENT_CASE  
**Anchor:** Operational RLHF details (labelers, data, RM, PPO+KL, PPO-ptx) + deployment-relevant outcomes

## Key Content
- **3-step RLHF workflow (Sec. 3.1):**  
  1) **SFT** on labeler demonstrations; 2) **Reward Model (RM)** trained on labeler rankings; 3) **PPO** to optimize RM reward, with **per-token KL penalty** to SFT policy; iterate steps 2–3 with new comparisons.
- **Human data ops (Sec. 3.4):** ~**40 contractors** (Upwork/ScaleAI) selected via **screening test**; onboarding + detailed instructions + shared chat. Inter-annotator agreement: **72.6±1.5%** (training labelers) vs **77.3±1.3%** (held-out).
- **Prompt sourcing & filtering (Sec. 3.2):** prompts mainly from **API Playground** (not production); **dedupe** by long common prefix; **≤200 prompts/user**; splits by **user ID**; **PII filtered** from training prompts. Dataset sizes: **SFT 13k**, **RM 33k**, **PPO 31k** prompts.
- **RM loss (Eq. 1):** for prompt \(x\), preferred completion \(y_w\), less-preferred \(y_l\):  
  \[
  \text{loss}(\theta)= -\frac{1}{\binom{K}{2}}\;\mathbb{E}_{(x,y_w,y_l)\sim D}\left[\log \sigma(r_\theta(x,y_w)-r_\theta(x,y_l))\right]
  \]
  with **K=4..9** ranked responses; train all \(\binom{K}{2}\) comparisons **as one batch element** to reduce overfitting; RM rewards **normalized** so demonstrations have mean **0** pre-RL.
- **PPO-ptx objective (Eq. 2):**  
  \[
  \mathbb{E}_{(x,y)\sim D_{\pi^\phi_{RL}}}\!\left[r_\theta(x,y)-\beta\log\frac{\pi^\phi_{RL}(y|x)}{\pi_{SFT}(y|x)}\right]+\gamma\,\mathbb{E}_{x\sim D_{pretrain}}[\log \pi^\phi_{RL}(x)]
  \]
  \(\beta\)=KL coef; \(\gamma\)=pretraining-mix coef (**PPO:** \(\gamma=0\)).
- **SFT defaults (Sec. 3.5):** **16 epochs**, cosine LR decay, **residual dropout 0.2**; select checkpoint by **RM score**.
- **Key empirical outcomes (Sec. 4.1):** On held-out API prompts, **1.3B InstructGPT preferred over 175B GPT-3**; **175B InstructGPT preferred over 175B GPT-3 85±3%**, and over **few-shot prompted GPT-3 71±4%**. **Held-out labelers** show similar preferences.
- **Alignment tax mitigation (Sec. 1, 4.2):** PPO can regress on SQuAD/DROP/HellaSwag/WMT; **PPO-ptx** (pretraining mix) greatly reduces regressions **without hurting preference**.

## When to surface
Use for questions about **how RLHF is implemented in practice** (data collection, RM ranking setup, PPO+KL, PPO-ptx) and for **specific quantitative evidence** that RLHF improves instruction-following vs larger base models.