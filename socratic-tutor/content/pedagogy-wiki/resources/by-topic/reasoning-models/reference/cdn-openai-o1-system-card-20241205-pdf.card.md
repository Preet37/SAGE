# Card: o1 System Card — Safety, CoT visibility, evals & mitigations
**Source:** https://cdn.openai.com/o1-system-card-20241205.pdf  
**Role:** reference_doc | **Need:** CONCEPT_EXPLAINER  
**Anchor:** Safety/faithfulness constraints, what CoT is shown vs hidden (summaries), evaluation methodology, and risk mitigations for o1.

## Key Content
- **Training & alignment (Sections 1–2, 5.3):**
  - o1 family trained with **large-scale reinforcement learning to reason using chain-of-thought**; includes **deliberative alignment**: teaches models to explicitly reason through safety specs before answering.
  - Data pipeline: diverse public + proprietary partnerships + in-house datasets; **filtering** to reduce **PII**; Moderation API + safety classifiers to exclude harmful/sensitive content (incl. CSAM).
- **Deployment decision: CoT surfaced as summaries (Section 4.3.2):**
  - ChatGPT surfaces **CoT summaries** (not full CoT). For o1 launch, same summarizer as o1-preview/mini; **no summaries for image-input results** (at time of writing).
  - Summarizer safety eval: summary introduced disallowed content when answer didn’t in **0.06%** of completions; **no regurgitation** found in summaries on regurgitation evals.
- **Instruction hierarchy to prevent developer-message jailbreaks (Section 4.2):**
  - Priority: **system > developer > user**; supervised on conflicts.
  - Tutor jailbreak eval pass rates: **o1 0.95** (system message) and **0.92** (developer message) vs **GPT-4o 0.33 / 0.58**.
- **Key safety eval numbers (Section 4.1):**
  - Challenging refusal (not_unsafe): **GPT-4o 0.713 vs o1 0.92**.
  - Hallucinations: SimpleQA accuracy **0.47 (o1) vs 0.38 (GPT-4o)**; hallucination rate **0.44 vs 0.61**. PersonQA hallucination rate **0.20 vs 0.30**.
- **External red teaming findings (Section 4.4):**
  - Pairwise safety: o1 rated safer **59.75%** vs GPT-4o **28.48%** (tie **11.76%**).
  - Gray Swan Arena ASR: harmful text **6% (o1) vs ~3.5% (4o)**; harmful image-text **5% vs 4%**; malicious code **5% vs 6%** (o1’s longer detail increased severity once jailbroken).
- **Preparedness Framework (Section 5):**
  - Deployment rule: only **post-mitigation “medium” or below** can be deployed.
  - o1 risk ratings: **Medium** (CBRN, persuasion), **Low** (cybersecurity, autonomy). Preparedness evals are a **lower bound**; more scaffolding/rollouts can elicit more.

## When to surface
Use when students ask about **o1’s reasoning traces (hidden vs summarized)**, **why models may not show full CoT**, or how **safety is evaluated/mitigated** (jailbreaks, hallucinations, instruction hierarchy, preparedness risk levels).