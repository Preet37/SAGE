---
title: "Reasoning Models"
subject: "Large Language Models"
date: 2026-04-09
tags:
  - "subject/large-language-models"
  - "level/intermediate"
  - "level/advanced"
  - "educator/andrej-karpathy"
  - "resource/video"
  - "resource/blog"
  - "resource/deep-dive"
  - "resource/paper"
  - "resource/code"
educators:
  - "Andrej Karpathy"
levels:
  - "intermediate"
  - "advanced"
resources:
  - "video"
  - "blog"
  - "deep-dive"
  - "paper"
  - "code"
---

# Reasoning Models

## Video (best)
- **Andrej Karpathy** — "Deep Dive into LLMs like ChatGPT"
- Why: Clear, high-signal overview of how modern LLMs are trained and used, including RLHF and inference-time behavior that connects to “reasoning” and test-time compute ideas.
- Level: Intermediate

## Blog / Written explainer (best)
- **Lilian Weng (OpenAI)** — "LLM Powered Autonomous Agents"
- **Link:** [https://lilianweng.github.io/posts/2023-06-23-agent/](https://lilianweng.github.io/posts/2023-06-23-agent/)
- Why: Strong conceptual grounding for reasoning-like behaviors in LLM systems (planning, reflection, tool use), and how inference-time scaffolding changes capabilities.
- Level: Intermediate

## Deep dive
- **Lilian Weng (OpenAI)** — "Reinforcement Learning with Human Feedback"
- **Link:** [https://lilianweng.github.io/posts/2024-11-28-reward-hacking/](https://lilianweng.github.io/posts/2024-11-28-reward-hacking/)
- Why: One of the clearest end-to-end explainers of RLHF-style training loops and reward modeling; useful background for “reinforcement learning for reasoning,” outcome vs process supervision, and reward model design.
- Level: Intermediate–Advanced
- **OpenAI** — "Learning to summarize with human feedback"
- **Link:** [https://openai.com/research/learning-to-summarize-with-human-feedback](https://openai.com/research/learning-to-summarize-with-human-feedback)
- Why: Canonical, readable RLHF case study (reward modeling + policy optimization) that transfers directly to reasoning-focused RL setups.
- Level: Intermediate

## Original paper
- **Ouyang et al. (OpenAI, 2022)** — "Training language models to follow instructions with human feedback" (InstructGPT)
- **Link:** [https://arxiv.org/abs/2203.02155](https://arxiv.org/abs/2203.02155)
- Why: Foundational paper for reward modeling + RL fine-tuning; core prerequisite for understanding later “reasoning model” training recipes.
- Level: Advanced
- **Cobbe et al. (OpenAI, 2021)** — "Training Verifiers to Solve Math Word Problems"
- **Link:** [https://arxiv.org/abs/2110.14168](https://arxiv.org/abs/2110.14168)
- Why: Directly targets verification at test time (verifier/reranker) and connects to test-time compute scaling via sampling + selection.
- Level: Advanced

## Code walkthrough
- **Hugging Face TRL** — "TRL (Transformer Reinforcement Learning)"
- **Link:** [https://github.com/huggingface/trl](https://github.com/huggingface/trl)
- Why: Widely used, practical RLHF/RLAIF tooling (PPO/DPO-style training, reward modeling utilities) suitable for implementing outcome-reward training pipelines.
- Level: Intermediate–Advanced
- **CarperAI** — "trlx"
- **Link:** [https://github.com/CarperAI/trlx](https://github.com/CarperAI/trlx)
- Why: Another established RLHF training codebase; useful for seeing end-to-end reward model + policy optimization in practice.
- Level: Advanced

## Coverage notes
- Strong: RLHF fundamentals; reward modeling; verifier-based selection; practical RL tooling (TRL/trlx).
- Weak: Specific “reasoning-architectures” branding (o1, o3, deepseek-r1) and their proprietary details; “thinking tokens” as an explicit mechanism.
- Gap: High-confidence, primary sources that explicitly define/standardize “process reward models” vs “outcome reward models” for reasoning, and authoritative public docs for o1/o3/deepseek-r1 and “reasoning traces” policies.

---

## Additional Resources for Tutor Depth

> **13 sources** — papers, official docs, working code, benchmarks, and deep explainers that give the AI tutor precision on this topic.

### 📄 DeepSeek-R1 training recipe + benchmark comparisons (o1-level)
**Paper** · [source](https://arxiv.org/html/2501.12948v1)

*DeepSeek-R1 technical report: RL/distillation pipeline, benchmark tables vs OpenAI o1, reasoning-trace formatting/rewards, test-time compute scaling.*

<details>
<summary>Key content</summary>

- **Models & goal (Abstract/§1):** DeepSeek-R1-Zero = *pure RL* on DeepSeek-V3-Base (no SFT). DeepSeek-R1 = multi-stage pipeline with cold-start SFT + RL + SFT + RL; reported “comparable to OpenAI-o1-1217” on reasoning tasks.
- **RL algorithm (GRPO, §2.2.1 Eq. 1–3):** Group Relative Policy Optimization optimizes policy using **group-sampled outputs**; baseline estimated from **group scores** (no critic model). Uses advantage \(A_i\) computed from rewards within each sampled group (Eq. 3). (Hyperparameters \(\epsilon,\beta\) appear in objective Eq. 1–2.)
- **Reward design (rule-based, §2.2.2):**
  - **Accuracy reward:** verifiable correctness (e.g., boxed math answer; compiler + tests for LeetCode).
  - **Format reward:** enforce reasoning between `<think>...</think>` tags.
  - **Rationale:** avoid neural outcome/process reward models due to **reward hacking** risk and added complexity/resources.
- **DeepSeek-R1 4-stage pipeline (§2.3):**
  1) **Cold-start SFT:** “thousands” of long-CoT samples; readable format `|special_token|<reasoning_process>|special_token|<summary>`.  
  2) **Reasoning RL:** add **language consistency reward** (proportion of target-language words in CoT); final reward = accuracy + language consistency.  
  3) **Rejection sampling → SFT:** ~**600k** reasoning samples + ~**200k** non-reasoning (writing/QA/etc.) = **~800k**; SFT **2 epochs**.  
  4) **RL all scenarios:** rule-based rewards for reasoning; preference reward models for general data; helpfulness judged on **final summary**, harmlessness on **entire response**.
- **Test-time compute scaling (§2.2.4/§3):** long CoTs (hundreds–thousands tokens); benchmark outputs capped at **32,768 tokens**.
- **Key empirical results:**
  - **R1-Zero AIME 2024:** pass@1 **15.6% → 71.0%** after RL; **cons@64 86.7%** (matches/exceeds o1-0912).  
  - **R1-Zero vs o1-0912 (Table §2.2.4):** AIME pass@1 **71.0 vs 74.4**; MATH-500 pass@1 **86.7 vs 83.3**; GPQA pass@1 **73.3 vs 77.3**; Codeforces rating **1444 vs 1843**.
  - **DeepSeek-R1 vs OpenAI-o1-1217 (Table §3.1):** AIME 2024 pass@1 **79.8 vs 79.2**; MATH-500 **97.3 vs 96.4**; GPQA Diamond **71.5 vs 75.7**; LiveCodeBench **65.9 vs 63.4**; Codeforces rating **2029 vs 2061**.
  - **Distillation (Table §3.2):** Distill-Qwen-32B AIME **72.6**, MATH-500 **83.3**, GPQA **94.3**, LiveCodeBench **62.1**, Codeforces **1691**.
  - **Distill vs RL-on-small (Table §4.1):** RL-trained Qwen-32B (R1-Zero-Qwen-32B) AIME **47.0** vs Distill-Qwen-32B **72.6** → distillation > RL on small base at similar scale.

</details>

### 📄 Inference-time compute ↔ adversarial robustness (o1)
**Paper** · [source](https://cdn.openai.com/papers/trading-inference-time-compute-for-adversarial-robustness-20250121_1.pdf)

*Quantitative evidence that increasing inference-time compute improves robustness/performance; methods + metrics (e.g., StrongREJECT goodness@0.1), attack/defense scaling curves, and human red-teaming table.*

<details>
<summary>Key content</summary>

- **Adversarial training objective (context, Intro):**  
  \[
  \min_f \mathbb{E}_{(x,y)\sim D}\left[\max_{t\in T} L(f(t(x)),y)\right]
  \]
  where \(T\) is allowed perturbations; contrasted with this paper’s approach: **no adversarial training**, only **more inference-time compute** (“thinking time”).
- **Core measurement protocol (Sec. 2):** For each prompt \(x\), sample multiple model outputs at varying **defender inference-time compute**; compute **attack success probability** vs (a) attacker resources and (b) defender compute. Models: **o1-preview, o1-mini** (plus **o1-v** for vision).
- **Tasks + attacker goals (Table 1):**
  - Math (2-digit add/mult; MATH): force output **42**, **correct+1**, or **correct×7**.
  - Safety: **StrongREJECT** (60 filtered policy-violating prompts; 35 jailbreaks), **Misuse Prompts**, **Rule Following** (unambiguous internal spec subset).
  - Agentic: **AdvSimpleQA** prompt injection; adversary wants output **“COMPROMISED”**.
  - Vision: ImageNet-A; Attack-Bard (transfer, \(\epsilon=16/255\), \(L_\infty\)); plus Attack-Bard-clean.
- **StrongREJECT metric (Sec. 3.2, Fig. 7):** **goodness@0.1** = for each misuse prompt, apply all jailbreaks; score responses with StrongREJECT grader; take **worst 10%** average; then average over prompts. Robustness **increases nearly monotonically** with compute.
- **Key empirical patterns (Figs. 2,3,12–15):**
  - For **unambiguous tasks** (math, AdvSimpleQA), for fixed attacker resources, attack success **tends toward 0** as compute increases.
  - **Soft-token attack procedure (Sec. 3.4):** optimize soft embeddings on train split to maximize logprob of sampled CoT + adversary answer; evaluate on held-out test; unconstrained norms can grow **>1000×** typical embedding norm → use **norm-capped** projection to average embedding norm every few steps.
- **Human red-teaming (Sec. 3.7, Table 2; o1-preview; 40 red-teamers; 5 compute levels):**
  - Avg attempts needed for success (↑ better): **11.0, 16.8, 15.6, 15.9, 22.6** (levels 1→5).
  - Transfer success on 80 prompts (↓ better): **36%, 30%, 21%, 20%, 19%**.
- **New compute-targeting attacks:** “**Think Less**” reduces model compute (Sec. 3.8); “**Nerd sniping**” shows top **5%** longest-compute traces can have **higher** attack success than median (Sec. 3.9, Fig. 18).

</details>

### 📄 PRM for reflective (long-CoT) math reasoning
**Paper** · [source](https://aclanthology.org/2025.findings-emnlp.253.pdf)

*Formal PRM training objective + reflective-step labeling rules (Error Propagation/Cessation) + evaluation procedures (BoN vs step-search) with concrete results.*

<details>
<summary>Key content</summary>

- **PRM vs ORM (Section 2):**  
  - **ORM** scores whole solutions via final answer.  
  - **PRM** scores **individual steps** to provide granular intermediate feedback for search/RL.
- **Reflective long-CoT labeling problem (Section 1, 3):** Traditional PRM datasets truncate incorrect solutions at the **first error**, assuming all later steps wrong—fails when models **self-correct** after mistakes.
- **New step-label rules (Section 4.2):**  
  - **Error Propagation:** if earlier steps are incorrect and current step **builds on** them without correction/new approach ⇒ label **incorrect**.  
  - **Error Cessation:** if earlier steps are incorrect but current step **corrects** them or starts a **new error-free approach** ⇒ label **correct**.
- **LLM judge annotation (Section 4.3, Appx B/E):** Incorporate the above rules into a judge prompt; reported step-annotation accuracy: **o1 = 0.963**, **claude-3.5-sonnet = 0.726**, **gpt-4o-2024-08-06 = 0.668** (Table 8).
- **PRM training objective (Eq. 1):** binary step classification with cross-entropy over steps  
  \[
  L_{\text{PRM}}=\sum_{i=0}^{K}\hat y_i\log y_i+(1-\hat y_i)\log(1-y_i)
  \]
  where \(K\)=#steps; \(y_i\)=gold label for step \(s_i\); \(\hat y_i=\text{PRM}(\text{prompt}, s_{\le i})\)=predicted probability/score for step \(s_i\).
- **Evaluation metrics (Section 5.1.3):**  
  - **PRM@N (Best-of-N):** pick best among N candidates using **final-step score**.  
  - **PRM@N-step (Online search):** at each step sample N continuations, choose top-scoring step to continue.
- **Key results (Table 2):** “Ours” PRM: **MATH500 PRM@64 = 0.816**, **PRM@8-step = 0.750**; **AIME2024 PRM@64 = 0.267**, **PRM@8-step = 0.167**; step-level **F1 = 0.828** (Precision 0.850, Recall 0.806).
- **Hyperparameters:** Generator SFT: lr **1e-5**, epochs **3**, batch **24**, max len **16384** (Table 6). PRM training: lr **1e-6**, epochs **1**, batch **256**, max len **10240** (Table 7).

</details>

### 📄 Self-Consistency (SC) for Chain-of-Thought Decoding
**Paper** · [source](https://arxiv.org/abs/2203.11171)

*Empirical accuracy gains from test-time sampling + majority/consistency selection over multiple CoT reasoning paths; ablations on number of sampled paths.*

<details>
<summary>Key content</summary>

- **Core idea (Self-Consistency decoding):** Replace **greedy decoding** in Chain-of-Thought (CoT) prompting with **sampling multiple reasoning paths** and selecting the **most consistent final answer** by marginalizing out the reasoning traces (Figure 1; Section 2).
- **Procedure (Figure 1 / Section 2):**
  1. Prompt LM with CoT exemplars (or zero-shot “let’s think step by step”).
  2. **Sample** a diverse set of outputs from the decoder to obtain pairs \((r_i, a_i)\), where \(r_i\) is the reasoning path (tokens) and \(a_i\) is the final answer.
  3. **Aggregate** by choosing the answer with highest agreement across samples (majority vote / “most consistent answer”).
- **Design rationale:** Complex reasoning problems admit **multiple valid reasoning paths** leading to a **unique correct answer**; correct paths tend to **agree more** on the final answer than incorrect ones. SC avoids greedy decoding’s **local optimality/repetitiveness** and reduces variance vs a single sampled decode.
- **Defaults / parameters (Section 3.2):** Results averaged over **10 runs**; each run samples **40 outputs** (“40 reasoning paths”).
- **Key empirical gains (Abstract / Tables 2–3):** SC boosts CoT accuracy by:
  - **GSM8K:** **+17.9%**
  - **SVAMP:** **+11.0%**
  - **AQuA:** **+12.2%**
  - **StrategyQA:** **+6.4%**
  - **ARC-Challenge:** **+3.9%**
- **Sampling ablation (Figure 2):** Increasing sampled paths improves accuracy; **~40 paths** consistently better than fewer.
- **Model coverage:** Demonstrated across **UL2-20B, LaMDA-137B, PaLM-540B, GPT-3 175B**; gains often larger at larger scale.

</details>

### 📄 Step-level PRM for inference-time reasoning search (HGS-PRM)
**Paper** · [source](https://arxiv.org/abs/2310.10080)

*Step-level (process) reward modeling objective + using PRM feedback to guide multi-step reasoning at inference time*

<details>
<summary>Key content</summary>

- **Core distinction (PRM vs ORM):**
  - **Outcome Reward Model (ORM):** provides a *single* reward for the final answer/trajectory outcome (sparse terminal feedback).
  - **Process-Supervised Reward Model (PRM):** provides **step-by-step feedback** over a multi-step reasoning trace (dense intermediate feedback), trained to predict correctness/quality of intermediate steps (process supervision).
- **Inference-time use (main contribution):** PRM is not only for training (e.g., PPO / reject sampling), but can be used **during decoding** to **discern better solution paths** for multi-step tasks (math, code).
- **Algorithmic procedure (HGS-PRM):**
  - A **heuristic greedy search** that uses **step-level PRM scores** to guide which next reasoning step/path to expand, aiming to optimize the explored reasoning pathway (search guided by per-step reward signals rather than only final correctness).
- **Empirical comparisons (as stated in source excerpt):**
  - The PRM-guided inference method **improves over Chain-of-Thought (CoT)** on **GSM8K** and **MATH** benchmarks (math reasoning).
  - Similar improvements reported for **code generation**, using an automatically generated step-level reward dataset.
- **Data generation for code PRM (workflow):**
  - Construct step-level reward data for coding tasks via **automatic code mutation** plus **unit tests** to label/score intermediate steps.

</details>

### 📖 Reasoning best practices (doc index only)
**Reference Doc** · [source](https://platform.openai.com/docs/guides/reasoning/best-practices)

*Entry point for OpenAI “Reasoning best practices” guidance; includes related navigation targets for controlling reasoning behavior (effort/latency/cost) and handling reasoning traces.*

<details>
<summary>Key content</summary>

- The fetched page content is a **404 “Page not found”** response; no best-practice guidance, equations, empirical results, or parameter defaults are present in the retrieved text.
- The document shell exposes **adjacent/related doc endpoints** via navigation and search suggestions (useful as pointers during tutoring):
  - Reasoning section links:
    - **Reasoning models:** https://platform.openai.com/api/docs/guides/reasoning  
    - **Reasoning best practices:** https://platform.openai.com/api/docs/guides/reasoning-best-practices
  - Search suggestions shown on the page (as keywords students may ask about):
    - **responses create**, **reasoning_effort**, **realtime**, **prompt caching**
- The broader docs IA (information architecture) visible here indicates where operational controls likely live:
  - **Responses API** migration guide: https://platform.openai.com/api/docs/guides/migrate-to-responses
  - **Streaming responses:** https://platform.openai.com/api/docs/guides/streaming-responses
  - **Latency optimization** and **Cost optimization** sections (for managing reasoning latency/cost tradeoffs).

</details>

### 📖 Reasoning models via Responses API (effort, tokens, summaries)
**Reference Doc** · [source](https://platform.openai.com/docs/guides/reasoning)

*How to use reasoning models with the Responses API; parameters to control reasoning behavior and how to request/suppress reasoning outputs.*

<details>
<summary>Key content</summary>

- **Model guidance (selection):** Start with `gpt-5.4` for most reasoning workloads; use `gpt-5.4-pro` for highest intelligence (more latency); `gpt-5-mini` / `gpt-5-nano` for lower cost/latency. Reasoning models “work better” with **Responses API** vs Chat Completions.
- **Core control knob:** `reasoning: {"effort": <level>}` guides how many **reasoning tokens** are generated before visible output. Supported values (model-dependent): `none`, `minimal`, `low`, `medium`, `high`, `xhigh`.  
  - Table (start here when…):  
    - `none`: lowest latency for extraction/routing/simple transforms  
    - `low`: small extra thinking improves reliability  
    - `medium`/`high`: planning, coding, synthesis, harder reasoning  
    - `xhigh`: only if evals justify extra latency/cost  
  - Defaults are model-dependent: `gpt-5.4` defaults to `none`; older GPT‑5 models default to `medium`.
- **Token accounting & context:** Reasoning tokens are **discarded from context after** the response, but still **consume context window** and are **billed as output tokens**. Usage shows reasoning tokens at:  
  `usage.output_tokens_details.reasoning_tokens` (example: `reasoning_tokens: 1024`).
- **Cost/length limit:** `max_output_tokens` caps **(reasoning + final output)** tokens.
- **Incomplete handling:** If context limit or `max_output_tokens` hit → `status: "incomplete"` and `incomplete_details.reason: "max_output_tokens"`. Can happen **before any visible output** (cost incurred for input + reasoning).
- **Practical buffer:** Recommend reserving **≥ 25,000 tokens** for reasoning+outputs when experimenting.
- **Function calling continuity:** Pass back **reasoning items** (plus tool call + tool outputs) across turns; easiest via `previous_response_id` or replaying prior `output` items.
- **Stateless/ZDR:** Include `"reasoning.encrypted_content"` in `include` to receive encrypted reasoning items for reuse.
- **Reasoning summaries (not raw traces):** Opt-in via `reasoning.summary` (e.g., `"auto"`). Summary appears in an output item of type `"reasoning"` under `summary[]`.

</details>

### 📖 o1 System Card — Safety, CoT visibility, evals & mitigations
**Reference Doc** · [source](https://cdn.openai.com/o1-system-card-20241205.pdf)

*Safety/faithfulness constraints, what CoT is shown vs hidden (summaries), evaluation methodology, and risk mitigations for o1.*

<details>
<summary>Key content</summary>

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

</details>

### 📋 # Source: https://openai.com/index/o3-o4-mini-system-card/
**Source** · 

### 📋 # Source: https://platform.openai.com/docs/api-reference/responses-streaming/response/reasoning
**Source** · 

### 🔍 o1 reasoning via large-scale RL + test-time compute scaling (Safety & CoT)
**Explainer** · [source](https://openai.com/index/learning-to-reason-with-llms/)

*Primary-source description of o1-style approach: large-scale RL for reasoning, trading inference-time compute for performance, and rationale for “thinking longer” before answering.*

<details>
<summary>Key content</summary>

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

</details>

### 🔍 o3-mini empirical evals + compute/latency tradeoffs (benchmarks)
**Explainer** · [source](https://cdn.openai.com/o3-mini-system-card-feb10.pdf)

*o3-mini-specific benchmark tables; reasoning behavior vs latency/cost via tool scaffolds + test-time attempts*

<details>
<summary>Key content</summary>

- **Reasoning model training (Section 2):** o-series trained with **large-scale reinforcement learning** to “think before answering” (chain-of-thought), learning to refine strategies and recognize mistakes; includes **deliberative alignment** (explicitly reason through safety specs before answering).
- **Evaluation defaults / test-time compute:**
  - **CTF eval (Sec. 5.3):** headless Kali Linux; **up to 60 rounds of tool use per attempt**; **12 attempts per task**. Results (post-mitigation): **61%** high-school, **21%** collegiate, **21%** professional CTFs.
  - **SWE-bench Verified N=477 (Sec. 5.7.2):**
    - *Agentless 1.0 scaffold:* **5 tries** to generate patch; metric **pass@1** computed by averaging per-instance pass rates over valid patches.
    - *o3-mini (tools) internal scaffold:* efficient iterative editing/debugging; **4 tries per instance**; **pass@1 = 61%** (non-final checkpoint).
    - *o3-mini launch candidate (Agentless):* **39%**; **o1: 48%**. (Shows tool scaffold/test-time procedure materially changes performance.)
- **Safety/jailbreak robustness (Sec. 4):**
  - StrongReject goodness@0.1: **GPT-4o 0.37**, **o1-mini 0.72**, **o3-mini 0.73**.
  - Gray Swan Arena attack success rate: **o3-mini 3.6%**, **o1-mini 3.7%**, **gpt-4o 4.0%**, **o1 1.9%**.
- **Hallucination (PersonQA, Table 3):** accuracy **o3-mini 21.7%**; hallucination rate **14.8%** (vs **GPT-4o-mini 52.4%**, **o1-mini 27.4%**).
- **Model autonomy indicator (Sec. 5.7):** interview coding **92% pass@1**; multiple-choice matches o1 (cons@32).

</details>

### 🔍 o3/o4-mini — test-time compute, long rollouts, and benchmark evidence
**Explainer** · [source](https://cdn.openai.com/pdf/2221c875-02dc-4789-800b-e7758f3722c1/o3-and-o4-mini-system-card.pdf)

*Citable PDF tables/figures quantifying reasoning/tool-use gains from longer rollouts (“test-time compute”) + evaluation methodology/metrics.*

<details>
<summary>Key content</summary>

- **Training / design (Sections 1–2):**
  - o3 and o4-mini are **reasoning models trained with large-scale reinforcement learning on chains of thought**; trained to “think before they answer,” trying strategies and recognizing mistakes.
  - Models can **use tools inside their chain-of-thought** (web browsing, Python, image/file analysis, etc.) to augment reasoning.
- **Test-time compute / long rollouts evidence (Cybersecurity CTF; Section 4.3.1, Fig. 7):**
  - Evaluation uses **16 rollouts per CTF**, reports **pass@12** (“best set of rollouts”).
  - With 12 attempts: **o3** solves **89% high-school**, **68% collegiate**, **59% professional** CTFs; **o4-mini** solves **80%**, **55%**, **41%** respectively.
  - Authors attribute gains vs prior o-series models to **improved tool use + ability to make use of long rollouts**.
  - **No-browsing results plotted** to avoid answer lookup contamination.
- **Agentic cyber range workflow + compute settings (Section 4.3.2):**
  - Two scenarios; run configs: **Normal**, **With Hints**, **With Solver Code**.
  - Trials: online-retailer scenario **30 trials/config**; priv-esc scenario **16 trials/config**.
  - Metrics: **pass@12** (Normal/With Hints), **pass@1** (With Solver Code).
  - Key result: **no model solves either scenario unaided or with hints**; **o3/o4-mini solve with reasonably high accuracy when given solver code**.
- **Evaluation methodology note (Section 4.1):**
  - Evals are **lower bounds**; longer rollouts/scaffolding can elicit more capability.
  - **95% CI for pass@1 via bootstrap** over attempts per problem.

</details>

---

## Related Topics

- [[topics/chain-of-thought|Chain-of-Thought]]
- [[topics/rlhf-alignment|RLHF & Alignment]]
- [[topics/evaluation-benchmarks|Evaluation Benchmarks]]
- [[topics/reinforcement-learning|Reinforcement Learning]]
- [[topics/synthetic-data|Synthetic Data & Self-Improvement]]
