# Card: Constitutional AI (CAI) pipeline: critique→revision + RLAIF
**Source:** https://arxiv.org/pdf/2212.08073.pdf  
**Role:** paper | **Need:** CONCEPT_EXPLAINER  
**Anchor:** Step-by-step critique→revision supervised phase and the RLAIF preference-data generation + RL phase (how constitutional principles are applied; how preference models are trained/used)

## Key Content
- **Overall goal:** Train a *helpful, harmless, non-evasive* assistant **without human harmfulness labels**; human input is a short natural-language **“constitution”** (≈ **16 principles** used in experiments).
- **Stage 1 (Supervised / SL-CAI; Section 3): Critique → Revision → SFT**
  - For each red-teaming prompt, sample an initial response from a helpful RLHF model.
  - Append a **critique request** tied to a sampled constitutional principle; sample critique.
  - Append a **revision request**; sample revised response. Repeat multiple times with **randomly sampled principles each step** (e.g., up to **4 revisions per prompt**).
  - **Training data:** red-team prompts **42,496 human-written + 140,335 model-generated = 182,831**; sample **4 critique-revision pairs per prompt**. Helpfulness prompts: **135,296**; sample **2 responses per prompt**.
  - **SFT hyperparams:** **1 epoch**, constant LR **0.5× pretraining LR**, batch size **1024 sequences**, sampling temperature **T=1**.
  - **Empirical:** revisions improve harmlessness monotonically by human-trained PM scores (Fig. 5); critiques help vs direct revision especially for smaller models (Fig. 7).
- **Stage 2 (RL / RL-CAI; Section 4): AI comparisons → Preference Model (PM) → RL (RLAIF)**
  - Generate **pairs of responses** from SL-CAI policy for harmful prompts.
  - A separate **feedback model** answers a **multiple-choice**: choose (A) vs (B) per a sampled principle; label uses **normalized log-probabilities** as **soft targets** (better than hard 0/1).
  - Train a **PM** on mixed data: **135,296 human helpfulness comparisons + 182,831 AI-labeled harmlessness comparisons**; then do RL using PM as reward (standard RLHF pipeline).
  - **CoT labeling variant:** prompt “Let’s think step-by-step”; CoT makes probabilities extreme → **clamp to 40–60%** (best reported) to reduce brittleness/overreaction.
  - **Design choices:** ensembling over **16 principles** improves robustness; SL stage reduces RL exploration problems; penalize evasiveness by instructing evaluators to prefer *thoughtful non-evasive* harmless answers.
- **Key results (crowdworker Elo):** RL-CAI models become **significantly more harmless** than RLHF/SL-CAI with small helpfulness cost (Figs. 2–3, 8). Label calibration shown as “reasonably well-calibrated” (Fig. 9). Overtraining can cause **Goodharting** (boilerplate “you are valued…”).

## When to surface
Use when students ask how **Constitutional AI differs from RLHF**, how **AI-generated preference labels** are produced (multiple-choice + principles + soft probs/CoT clamping), or how the **critique→revision SFT stage** bootstraps safer behavior before RL.