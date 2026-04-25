# Card: InstructGPT instruction-following via RLHF (key results & pipeline)
**Source:** https://openai.com/index/instruction-following/  
**Role:** explainer | **Need:** EMPIRICAL_DATA  
**Anchor:** Human-evaluation preference results + comparisons across SFT vs RLHF variants (InstructGPT vs GPT‑3; safety metrics; alignment-tax mitigation)

## Key Content
- **Core empirical preference result:** Human labelers **prefer outputs from the 1.3B InstructGPT model over outputs from 175B GPT‑3**, despite **>100× fewer parameters** (API prompt distribution).
- **Preference robustness:** InstructGPT is **significantly preferred** over GPT‑3 on prompts submitted to **both** InstructGPT and GPT‑3 models on the API; holds even when GPT‑3 prompts are prefixed to induce an “instruction-following mode.”
- **Safety/quality metrics (directional, named benchmarks):**
  - **Fewer imitative falsehoods** vs GPT‑3 on **TruthfulQA**.
  - **Less toxic** vs GPT‑3 on **RealToxicityPrompts**.
  - Human eval on API prompts: **hallucinates less often** and produces **more appropriate outputs**.
  - Other harms on API distribution (sexual/violent content, denigrating protected class, encouraging abuse): **no significant improvement**; incidence **equally low** for both.
- **Comparative generalization:** On customer prompt distribution, InstructGPT outputs are **preferred over FLAN and T0**, suggesting academic instruction datasets aren’t fully representative of deployed use.
- **Training pipeline (RLHF, PPO):**
  1) Collect **human-written demonstrations** on API prompts → **supervised fine-tuning (SFT) baseline**.  
  2) Collect **human rankings** of multiple model outputs on more API prompts.  
  3) Train a **reward model (RM)** to predict labeler preference.  
  4) **RL fine-tune** the policy to maximize RM reward using **PPO**.
- **Design rationale / compute note:** Fine-tuning uses **<2%** of pretraining compute+data; mainly **elicits/unlocks** pretrained capabilities rather than teaching many new ones.
- **Alignment tax mitigation:** During RL fine-tuning, **mix a small fraction of original GPT‑3 pretraining data** and train with **log-likelihood maximization**; found **more effective than increasing the KL coefficient**; maintains safety/preferences while reducing academic-task regressions.

## When to surface
Use when students ask for concrete evidence that RLHF improves instruction-following (including “smaller beats bigger”), how RLHF is implemented step-by-step (SFT→RM→PPO), or what “alignment tax” is and how mixing pretraining data mitigates it.