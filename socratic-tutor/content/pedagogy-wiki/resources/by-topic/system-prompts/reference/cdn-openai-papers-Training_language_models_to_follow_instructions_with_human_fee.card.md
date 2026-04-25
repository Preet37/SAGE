# Card: InstructGPT RLHF pipeline (SFT → RM → PPO/PPO-ptx)
**Source:** https://cdn.openai.com/papers/Training_language_models_to_follow_instructions_with_human_feedback.pdf  
**Role:** paper | **Need:** CONCEPT_EXPLAINER  
**Anchor:** Step-by-step InstructGPT pipeline + datasets + evaluation numbers + key equations (RM loss, PPO-ptx objective)

## Key Content
- **3-step training pipeline (Section 3.1, Fig. 2):**
  1) **Supervised fine-tuning (SFT):** collect labeler demonstrations on prompts; fine-tune GPT-3.  
  2) **Reward model (RM):** collect **rankings** of multiple model outputs per prompt; train RM to predict preferences.  
  3) **RLHF via PPO:** optimize SFT policy against RM reward with **KL penalty** to SFT; variant **PPO-ptx** mixes in pretraining gradients to reduce “alignment tax”.
- **Datasets (Section 3.2):** SFT ~**13k** training prompts; RM **33k**; PPO **31k** (API-only). Prompts deduped by long common prefix; cap **200 prompts/user**; splits by **user ID**; training prompts filtered for **PII**.
- **SFT hyperparams (Section 3.5):** **16 epochs**, cosine LR decay, residual dropout **0.2**; select checkpoint by **RM score** (not val loss).
- **RM loss (Eq. 1):**  
  \[
  \text{loss}(\theta)= -\frac{1}{\binom{K}{2}}\; \mathbb{E}_{(x,y_w,y_l)\sim D}\left[\log \sigma(r_\theta(x,y_w)-r_\theta(x,y_l))\right]
  \]  
  where \(x\)=prompt, \(y_w\)=preferred completion, \(y_l\)=less-preferred, \(r_\theta\)=scalar RM output, \(K\)=#responses ranked (**4–9**). Train all \(\binom{K}{2}\) comparisons per prompt as one batch element to reduce overfitting.
- **PPO-ptx objective (Eq. 2):**  
  \[
  \mathbb{E}_{(x,y)\sim D_{\pi^\text{RL}_\phi}}\!\left[r_\theta(x,y)-\beta \log\frac{\pi^\text{RL}_\phi(y|x)}{\pi^\text{SFT}(y|x)}\right] + \gamma \mathbb{E}_{x\sim D_\text{pretrain}}[\log \pi^\text{RL}_\phi(x)]
  \]  
  \(\beta\)=KL coef; \(\gamma\)=pretraining-mix coef (**PPO: \(\gamma=0\)**).
- **Key empirical results (Abstract/Section 4):**
  - **1.3B InstructGPT preferred over 175B GPT-3** (human eval).  
  - **175B InstructGPT preferred over 175B GPT-3: 85±3%**; over **few-shot prompted GPT-3: 71±4%**.  
  - Closed-domain hallucination rate: **21% (InstructGPT) vs 41% (GPT-3)**.  
  - Held-out labelers: similar preferences; RM cross-group accuracy **69.6±0.9%** vs **72.4±0.4%** in-group.

## When to surface
Use when students ask how RLHF/InstructGPT is trained (SFT→RM→PPO), why PPO-ptx mixes pretraining, or want concrete equations/metrics for preference-based reward modeling and KL-regularized PPO.