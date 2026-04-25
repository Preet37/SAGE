# Card: OpenAI Safety Evaluations Hub (public eval categories + metrics)
**Source:** https://openai.com/safety/evaluations-hub/  
**Role:** reference_doc | **Need:** DEPLOYMENT_CASE  
**Anchor:** Publicly described safety evaluation categories + downloadable evaluation data (disallowed content, jailbreaks, hallucinations/factuality, instruction hierarchy)

## Key Content
- **Purpose & usage:** OpenAI runs evaluations to measure model **safety and performance**, publishes results **ongoing** (not just at launch). Results are used **internally** as *one input* to safety/deployment decisions and are also included in **system cards**.
- **Scope (text-based) evaluation categories (4):**
  1. **Disallowed content:** checks model **does not comply** with requests violating policy (e.g., hateful content, illicit advice).
  2. **Jailbreaks:** adversarial prompts intended to **circumvent safety training** and induce harmful output.
  3. **Hallucinations:** measures **factual errors**.
  4. **Instruction hierarchy:** measures adherence to instruction priority: **system > developer > user**.
- **Disallowed content / overrefusal scoring (autograder):**
  - **Metric 1: `not_unsafe`** = output is not unsafe per OpenAI policy/model spec.
  - **Metric 2: `not_overrefuse`** = model does not refuse a benign/good request.
  - Includes **disaggregated sub-metrics** for higher-severity categories; has **Standard** and harder **“Challenge”** test sets.
- **Jailbreak evaluation sets:** includes **StrongReject** (academic jailbreak benchmark) + **human-sourced jailbreaks** (from human red teaming).
- **Empirical ranges reported (hub summary article):**
  - Disallowed content refusal effectiveness near **0.99** for many models; benign-handling (`not_overrefuse`) top around **0.80**, others **0.65–0.79**.
  - StrongReject robustness **0.23–0.85**; human jailbreak robustness **0.90–1.00**.
  - Hallucination benchmarks: **SimpleQA accuracy 0.09–0.59**, hallucination rate **0.41–0.86**; **PersonQA accuracy 0.17–0.70**, hallucination rate **0.13–0.52**.
  - Instruction hierarchy: system-vs-user **0.50–0.85**; developer-vs-user **0.15–0.77**; system-vs-developer **0.55–0.93**.
- **Design rationale:** evaluation methods are updated as older tests **saturate** (stop differentiating models) and to address **new modalities/emerging risks**.

## When to surface
Use when students ask how OpenAI *measures* safety (jailbreak resistance, disallowed content compliance, hallucinations, instruction-following hierarchy) or want concrete metric names/ranges and what “autograder/not_unsafe/not_overrefuse/StrongReject” mean.