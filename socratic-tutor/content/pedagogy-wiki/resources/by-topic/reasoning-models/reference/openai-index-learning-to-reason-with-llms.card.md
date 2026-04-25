# Card: o1 reasoning via large-scale RL + test-time compute scaling (Safety & CoT)
**Source:** https://openai.com/index/learning-to-reason-with-llms/  
**Role:** explainer | **Need:** CONCEPT_EXPLAINER  
**Anchor:** Primary-source description of o1-style approach: large-scale RL for reasoning, trading inference-time compute for performance, and rationale for “thinking longer” before answering.

## Key Content
- **Training approach (Reasoning RL):** “Large-scale reinforcement learning algorithm” trains the model to “think productively” using **chain-of-thought** in a **highly data-efficient** process. RL teaches the model to: recognize/correct mistakes, break down tricky steps, and try alternate approaches when stuck (Chain of Thought section).
- **Compute scaling claim:** o1 performance **consistently improves** with:
  - **More RL** = more **train-time compute**
  - **More time spent thinking** = more **test-time compute**  
  (Stated explicitly; figure caption: “smoothly improves with both train-time and test-time compute.”)
- **Test-time selection/verification workflow (Coding/IOI):**
  - Sample many candidate submissions; **submit 50** chosen via a **test-time selection strategy** using: IOI public tests + model-generated tests + a learned scoring function.
  - With **10,000 submissions/problem**, score **362.14** (above gold threshold) even **without** selection strategy.
- **Empirical results (selected):**
  - **AIME 2024:** GPT‑4o **12% (1.8/15)** avg; o1 **74% (11.1/15)** single-sample; **83% (12.5/15)** with **consensus@64**; **93% (13.9/15)** when **re-ranking 1000 samples** with learned scoring.
  - **GPQA diamond:** o1 surpasses recruited PhD experts; **pass@1 77.3**, **cons@64 78.0** (Appendix A).
  - **Safety table (harmful prompts):** Challenging jailbreak/edge cases safe completions: GPT‑4o **0.714** vs o1‑preview **0.934**; StrongREJECT Goodness@0.1: **0.220 → 0.840**; Human-sourced jailbreak eval: **0.770 → 0.960**.
- **Design rationale (Hiding CoT):** Raw chains-of-thought not shown to users; instead show a **model-generated summary**. Rationale: preserve potential for **monitoring** (“read the mind”) while avoiding training user-preference/policy compliance onto the hidden trace and avoiding exposing unaligned thoughts.

## When to surface
Use when students ask how o1-style models are trained to “think longer,” why more inference-time compute helps, how verification/selection at test time boosts performance, or how chain-of-thought relates to safety/jailbreak robustness.