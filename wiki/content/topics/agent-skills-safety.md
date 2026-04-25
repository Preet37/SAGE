---
title: "Agent Skills & Safety"
subject: "Agents & Reasoning"
date: 2025-01-01
tags:
  - "subject/agents-and-reasoning"
  - "level/intermediate"
  - "level/advanced"
  - "educator/lilian-weng"
  - "resource/video"
  - "resource/blog"
  - "resource/deep-dive"
  - "resource/paper"
  - "resource/code"
educators:
  - "Lilian Weng"
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

# Agent Skills Safety

## Video (best)
- **Stanford HAI** — "Agentic AI: A Progression of Language Model Applications"
- **Watch:** [YouTube](https://www.youtube.com/watch?v=kJLiOGle3Lw)
- Why: Stanford HAI panel covering agent safety, security, and trust — addresses guardrails and operational safety concerns for agentic systems.
- Level: intermediate

> ⚠️ **Coverage Gap**: No excellent video exists for this specific topic from the preferred educator list. General agentic AI videos (e.g., from LangChain or AutoGPT walkthroughs) touch on safety tangentially but do not address skill composition safety, principle of least privilege in agents, or defense-in-depth architectures for CLI/code agents.

---

## Blog / Written explainer (best)
- **Lilian Weng** — "LLM Powered Autonomous Agents"
- **Link:** [https://lilianweng.github.io/posts/2023-06-23-agent/](https://lilianweng.github.io/posts/2023-06-23-agent/)
- Why: Weng's post is the most cited and pedagogically rigorous treatment of agentic architectures available. It covers tool use, skill composition, memory, and planning — providing the conceptual scaffolding needed to understand *why* safety constraints (sandboxing, least privilege, guardrails) are necessary. The section on tool use maps directly to skill registry and skill discovery concepts. It is dense but well-structured, making it ideal for learners in both intro-to-agentic-ai and intro-to-multimodal contexts.
- Level: intermediate

---

## Deep dive
- **OWASP LLM Top 10 — LLM06: Sensitive Information Disclosure / LLM01: Prompt Injection**
- **Link:** [https://owasp.org/www-project-top-10-for-large-language-model-applications/](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- Why: The OWASP LLM Top 10 project is the most operationally grounded reference for agent security risks. It directly addresses prompt injection (critical for CLI agents and Claude Code), privilege escalation, and insecure plugin/skill design — mapping cleanly onto defense-in-depth and principle of least privilege concepts in this topic. It is practitioner-oriented and regularly updated, making it more actionable than academic papers for course designers.
- Level: intermediate/advanced

---

## Original paper
- **Perez & Ribeiro (2022)** — "Ignore Previous Prompt: Attack Techniques For Language Models"
- **Link:** [https://arxiv.org/abs/2211.09527](https://arxiv.org/abs/2211.09527)
- Why: This is the most readable seminal paper specifically on prompt injection as an attack vector — the foundational safety concern for any agent that composes skills, executes CLI commands, or processes external inputs. It is short, accessible, and directly motivates the guardrails and sandboxing concepts in this topic. More pedagogically appropriate than broader alignment papers for this specific operational safety focus.
- Level: intermediate

---

## Code walkthrough
- **NVIDIA NeMo Guardrails — Official Documentation & Colabs**
- **Link:** [https://github.com/NVIDIA/NeMo-Guardrails](https://github.com/NVIDIA/NeMo-Guardrails)
- Why: NeMo Guardrails is explicitly listed as a related concept for this topic, and the official repo contains runnable notebooks demonstrating how to implement input/output rails, topical guardrails, and dialog flow constraints on LLM agents. This is the most direct hands-on implementation resource that bridges the conceptual (guardrails, defense in depth) with working code. Learners can see how guardrails compose with agent skill calls in practice.
- Level: intermediate/advanced

---

## Coverage notes
- **Strong**: Prompt injection theory, agentic architecture concepts (Weng), NeMo Guardrails implementation, OWASP operational risk framing
- **Weak**: Skill registry design patterns, skill discovery safety, cost optimization and latency management as safety-adjacent concerns, multi-modal deployment-specific risks
- **Gap**: No high-quality video exists from preferred educators (3Blue1Brown, Karpathy, Kilcher, etc.) that addresses agent skills safety as a unified topic. Claude Code and Cursor-specific safety patterns are not well covered in public educational resources. Defense-in-depth architectures for multi-agent systems lack a canonical explainer.

---

## Cross-validation
This topic appears in 2 courses: **intro-to-agentic-ai**, **intro-to-multimodal**

- The Weng blog post and OWASP deep dive serve both courses well — agentic AI learners need the architectural grounding; multimodal learners need to understand how additional input surfaces (images, audio) expand the attack surface for prompt injection and skill misuse.
- The NeMo Guardrails code walkthrough is most relevant to intro-to-agentic-ai; multimodal courses may need supplementary resources on modality-specific safety (e.g., vision-based prompt injection).

---

---

## Additional Resources for Tutor Depth

> **9 sources** — papers, official docs, working code, benchmarks, and deep explainers that give the AI tutor precision on this topic.

### 📄 CAPTURE benchmark + robustness scoring for prompt-injection guardrails
**Paper** · [source](https://aclanthology.org/anthology-files/pdf/llmsec/2025.llmsec-1.13.pdf)

*Full evaluation protocol (context-aware test generation + scoring) and published FNR/FPR results*

<details>
<summary>Key content</summary>

- **Attack construction (Section 2):** Context-aware prompt injection uses 3-part structure from Liu et al. (2023): **Framework (F)** = normal in-domain request; **Separator (S)** = context-breaking cue to override F; **Disruptor (D)** = malicious instruction. CAPTURE systematically varies **F, S, D**.
- **Two generation modes (Figure 1):**
  - **MALICIOUS-GEN:** GPT-4o decomposes existing attacks into **S and D** (Fig. 3), then rewrites **S → S′** to be more evasive (Fig. 4), then embeds **S′ + D** into in-domain **F**. Output sizes: **1274 train**, **641 test/val** adversarial prompts.
  - **SAFE-GEN (over-defense test):** Uses trigger words from **NotInject** inside **S**, with **safe D** (Fig. 2). Output sizes: **339 train**, **171 test/val** benign prompts.
- **Domains (Section 2.1):** 6 domains: Shopping, Covid, Movies, Stock, Travel, Python Code. Base split per domain: **30 train / 15 test / 15 val**, expanded via GPT-4o to **100 examples per domain per split**.
- **Metrics (Tables 2–3):** Report **False Negative Rate (FNR%)** on MALICIOUS-GEN and **False Positive Rate (FPR%)** on SAFE-GEN.
- **Key empirical results (Tables 2–3):**
  - **PromptGuard:** **FNR 0%** across domains, but **FPR ~100%** (e.g., Stock/Movies/Travel/Covid/Shopping all **100%**, Python **24.12%**).
  - **InjecGuard:** extremely high **FNR** (e.g., Movies **100%**, Stock **99.84%**) and **FPR ~99%** (Python **0.88%** exception).
  - **Fmops:** **FNR 100%** across domains; **FPR 0%** (misleading due to total miss).
  - **GPT-4o baseline:** low FNR (**7.33–16.38%**) and low FPR (**2.64–13.15%**).
  - **CaptureGuard (trained on CAPTURE data):** near-zero on tested domains—**FNR 0.00–0.15%**, **FPR 0.00–2.05%** (Stock/Movies/Python).
- **CaptureGuard training defaults (Section 2.4, Table 5):** DeBERTaV3-base; **batch 32**, **LR 2e-5**, **max seq len 64**, **Adam**, **1 epoch**, **threshold 0.5**. Trained per-domain (Python/Movies/Stocks) on CAPTURE + InjecGuard’s **14 benign + 12 malicious** datasets.
- **External benchmark accuracies (Table 6):** CaptureGuard: **NotInject(avg) 79.04%**, **WildGuard 75.00%**, **BIPIA(Injection) 54.77%** (vs InjecGuard **87.31/76.11/68.34**, GPT-4o **86.62/84.24/66.00**).

</details>

### 📄 CAPTURE context-aware prompt-injection testing + robustness results
**Paper** · [source](https://aclanthology.org/2025.llmsec-1.13.pdf)

*Context-aware prompt-injection testing procedure (generation + evaluation) with empirical FNR/FPR results for guardrails and a trained improved detector (CaptureGuard).*

<details>
<summary>Key content</summary>

- **Attack structure (Section 2):** prompts decomposed into **Framework (F)** = normal in-domain request; **Separator (S / refined S′)** = context-break to redirect; **Disruptor (D)** = injected instruction (malicious or safe). Final prompt = embed **S′ + D** inside domain **F**.
- **Dataset generation pipeline (Fig. 1, Sec. 2):**
  - **Contextual domain data (Sec. 2.1):** 6 domains (Shopping, Covid, Movies, Stock, Travel, Python Code). Start with **30 train / 15 test / 15 val** questions per domain, expanded via **GPT-4o** to **100 examples per domain per split**.
  - **MALICIOUS-GEN (Sec. 2.2):** GPT-4o decomposes existing attacks into **S and D**; augment **D** with strategies (Table 7); refine **S → S′** to evade trigger-word detection; yields **1274 train** and **641 test/val** attacks.
  - **SAFE-GEN (Sec. 2.3):** build benign prompts to test over-defense: **S** uses trigger words from **NotInject**; **D** is safe in-domain instruction; yields **339 train** and **171 test/val** benign samples.
- **Evaluation metrics (Sec. 3):** **FNR** on MALICIOUS-GEN (missed attacks) and **FPR** on SAFE-GEN (benign flagged).
- **Empirical results (Tables 2–3):**
  - **PromptGuard:** **FNR 0%** across domains but **FPR ~100%** (e.g., Stock/Movies **100%**, Python **24.12%**).
  - **InjecGuard:** extremely high **FNR** (Stock **99.84%**, Movies **100%**, Python **35.65%**) and **FPR** (Stock/Movies **99.12%**, Python **0.88%**).
  - **Fmops:** **FNR 100%** with **FPR 0%** (fails by missing all attacks).
  - **GPT-4o detector baseline:** low FNR/FPR (e.g., Stock **16.38/5.81**, Movies **7.48/9.35**, Python **13.72/2.64**).
  - **CaptureGuard (trained on CAPTURE + InjecGuard datasets):** near-zero errors: **FNR 0.00–0.15%**, **FPR 0.00–2.05%** (Table 2).
- **CaptureGuard training defaults (Table 5):** DeBERTaV3-base; batch **32**; LR **2e-5**; max length **64**; Adam; **1 epoch**; threshold **0.5**.

</details>

### 📄 Swiss-cheese multi-layer runtime guardrails for FM web agents
**Paper** · [source](https://arxiv.org/html/2408.02205v3)

*End-to-end guardrail architecture (taxonomy + reference architecture across quality attributes/pipelines/artifacts) and concrete guardrail integration points in the agent loop*

<details>
<summary>Key content</summary>

- **Core definition (Intro):** Runtime guardrails = mechanisms integrated into an FM-agent architecture to safeguard behavior during runtime, preventing undesirable/unsafe behaviors (vs. design-time alignment).
- **Design rationale (Intro, Sec. V):** Single-layer guardrails are insufficient for autonomous, non-deterministic agents; multi-layer “Swiss Cheese Model” defense-in-depth reduces risk bypass because “holes” differ across layers.
- **Taxonomy dimensions (Sec. IV, Fig. 3):**
  - **Quality attributes to protect:** accuracy, efficiency (latency/cost), privacy, security, safety, fairness, compliance, generalizability, customizability, adaptability, traceability, portability, interoperability, interpretability.
- **Guardrail design options (Sec. IV-B):**
  - **Actions:** Block, Modify, Validate, Retry, Defer, Isolate, Evaluate.
  - **Rules:** uniform; priority-enabled; context-dependent; negotiable **soft** vs **hard** (hard = non-negotiable for legal/ethical/safety constraints).
  - **Modalities:** single-modal vs multimodal guardrails (synchronize protections across data types).
  - **Underlying techniques:** rule-based vs ML-based vs hybrid.
- **Concrete mapping of actions→targets (Sec. IV-B1/B2, Table V):**
  - **Pipeline targets:** prompts (block/filter/flag/modify/parallel calls/retry/defer/evaluate); intermediate results (flag/human intervention/evaluate); final results (block/filter/flag/modify/retry/fall back/human intervention/evaluate).
  - **Artifact targets:** goals (validate/block/flag/modify/human intervention/defer); memory (block/filter/flag/modify/retry/human intervention/isolate/evaluate); plans (block/flag/modify/validate/retry/fall back/human intervention/defer); tools (block/parallel calls/retry/fall back/human intervention/defer/evaluate); FMs (block/filter/flag/modify/parallel calls/retry/fall back/human intervention/isolate/evaluate/redundancy).
- **Reference architecture components (Sec. V, Fig. 4):** external environment + agent components (context engine; reasoning/planning; workflow execution; memory) + built-in multi-layer guardrails + AgentOps infrastructure.
- **Empirical/process numbers (Sec. III-E):** SLR search returned **1,733** papers → removed **108** duplicates/editorials → excluded **1,524** after screening → removed **80** after IC check; manual search **189** → **15** selected; final cross-check **32** papers.

</details>

### 📄 WebGuard—Action-Risk Guardrails for Web Agents
**Paper** · [source](https://arxiv.org/html/2507.14293v1)

*End-to-end guardrail construction + integration for web agents (risk schema, data curation, model design, integration points, evaluation splits/metrics/results)*

<details>
<summary>Key content</summary>

- **Risk assessment formulation (Section 3.1):** multiclass classification.  
  **Eq. (risk label):** given webpage state \(s\), proposed action \(a\), and risk schema \(\mathcal{R}\), predict label  
  \[
  y = f_\theta(s, a, \mathcal{R}) \in \{\text{SAFE}, \text{LOW}, \text{HIGH}\}
  \]
  where \(f_\theta\) is a prompted or fine-tuned LM; \(\mathcal{R}\) includes textual definitions + examples.
- **Observation/action design (Section 3.2):**
  - State \(s\): DOM/HTML, Accessibility (A11y) tree (roles/labels/hierarchy/layout), screenshot, URL.
  - Action \(a\): interaction with a specific element causing state change; grounded by **bounding box** (vision) or **A11y node index + HTML snippet/metadata** (text-only).
- **Prompted guardrail reasoning stages (Section 3.2):** (1) state understanding → (2) outcome reasoning → (3) risk classification.
- **Training pipeline (Section 2.2, 3.2):** website selection (7 domains) → 1-hour exploration per site to exhaustively record **state-changing actions** → annotate risk via Chrome-extension tool (WebOlympus-based) saving screenshots/bboxes/metadata → execute actions only when needed; allow post-outcome label revision → **3-annotator review** (label validity + snapshot integrity). Unannotated remaining actions labeled SAFE by default.
- **Integration (Section 3.3):** guardrail runs **before execution**; user sets unsafe threshold (LOW or HIGH). If exceeded: pause + user **approve / reject / revise**.
- **Evaluation splits (Section 4.1):** TestLong-Tail (hold out low-traffic sites), TestCross-Domain (hold out Social+Entertainment), TestCross-Website (new sites within domains), TestCross-Action (random 20% in-domain).
- **Metrics (Section 4.2):** 3-class Accuracy; RecallH (HIGH); RecallL (LOW); average F1.
- **Key results (Table 2):** Fine-tuned **WebGuard-VL-7B**:  
  - Long-Tail **Acc 84.6 / RecallH 86.0 / RecallL 87.1**  
  - Cross-Domain **75.2 / 66.8 / 87.5**  
  - Cross-Website **87.8 / 90.2 / 87.4**  
  - Cross-Action **86.7 / 83.2 / 91.6**  
  Smaller **WebGuard-VL-3B** still strong (e.g., Cross-Action **Acc 83.0 / RecallH 90.8 / RecallL 85.5**). Zero-shot text-only often > multimodal; after fine-tuning, multimodal becomes best.

</details>

### 📊 AgentDojo benchmark (prompt injection for tool-using agents)
**Benchmark** · [source](https://arxiv.org/abs/2406.13352)

*Benchmark construction (env/tools/tasks/injection suites) + attack/defense metrics & ablations (arXiv canonical)*

<details>
<summary>Key content</summary>

- **Benchmark structure (Section 3):**
  - 4 **stateful environments**: *Workspace, Slack, Travel Agency, e-banking* with mutable environment state + **attack placeholders** in tool outputs.
  - **Tools:** 74 total; tool outputs formatted as **YAML** by default (arbitrary formats supported).
  - **Tasks:** 97 **user tasks** + injection tasks; **629 security test cases** formed by **cross-product** of user × injection tasks per environment.
  - Each user/injection task includes (i) NL instruction, (ii) **deterministic binary** utility/security check over environment state, (iii) **ground-truth tool-call sequence** used to place injections only in tool outputs actually queried.
  - Task difficulty: contexts up to **~7,000 GPT-4 tokens** (data) + **~4,000 tokens** (tool descriptions); chaining up to **18 tool calls**.
- **Metrics (Section 3.4):**
  - **Benign Utility** = fraction of user tasks solved with no attack.
  - **Utility Under Attack** = fraction of security cases where user task solved **without adversarial side effects** (complement sometimes reported as **untargeted ASR**).
  - **Targeted ASR** = fraction of security cases where attacker goal achieved.
  - **Adaptive attacker (Max)**: attack set succeeds if **any** attack succeeds on a case.
- **Suite sizes (Table 1):** Workspace (24 tools, 40 user, 6 injection); Slack (11, 21, 5); Travel (28, 20, 7); Banking (11, 16, 9).
- **Empirical results (Intro/Section 4):**
  - Current LLMs solve **<66%** of tasks even **without attacks**.
  - Strong agents: attacks succeed **<25%** overall; with a secondary **prompt-injection detector**, ASR drops to **~8%**.
  - Slack suite: **92%** attack success (Important message attack); Travel injection task #6: **0%** success (requires 2 unrelated malicious goals).
  - Injection position: end-of-tool-response most effective; up to **~70%** ASR vs GPT-4o.
- **Attack/knowledge ablation (Section 4.2):** “Important message” baseline targeted ASR **45.8%**; wrong user **23.2%** (−22.6); wrong model **23.7%** (−22.1); both correct **47.7%** (+1.9).
- **Defense comparison (Section 4.3):** defenses tested on GPT-4o: **delimiters**, **PI detector (DeBERTa/BERT classifier)**, **prompt sandwiching**, **tool filter** (pre-select minimal tools before seeing untrusted data). **Tool filter** lowers ASR to **7.5%**; fails when tools can’t be planned in advance or when same tools suffice for attack (**17%** of cases).
- **Cost (Appendix D):** full 629-case suite on GPT-4o **~$35**; 97 benign utility cases **~$4**.

</details>

### 📊 AgentDojo — Benchmarking Prompt Injection in Tool-Calling Agents
**Benchmark** · [source](https://proceedings.neurips.cc/paper_files/paper/2024/file/97091a5177d8dc64b1da8bf3e1f6fb54-Paper-Datasets_and_Benchmarks_Track.pdf)

*AgentDojo methodology + utility/attack-success metrics for prompt-injection attacks/defenses (incl. ablations)*

<details>
<summary>Key content</summary>

- **Benchmark scale & setup (Abstract, Sec. 3, Table 1):**
  - **97** realistic **user tasks**, **27** injection targets, **629** security test cases (cross-product per environment).
  - **4 environments:** Workspace, Slack, Travel, Banking.
  - **Tools:** total **74** tools (Table 1 lists 24/11/28/11 per env; text also mentions “70 tools”).
  - Tasks can require **up to 18 tool calls**, long contexts: **~7,000 GPT-4 tokens** data + **~4,000** tokens tool descriptions.
- **Metrics (Sec. 3.4):**
  - **Benign Utility** = fraction of user tasks solved with **no attack**.
  - **Utility Under Attack** = fraction of security cases where user task solved **without adversarial side effects** (complement sometimes called **untargeted ASR**).
  - **Targeted ASR** = fraction of security cases where **attacker goal achieved**.
  - **Adaptive attacker (“Max”)** over attacks {Aᵢ}: success on a case if **any** Aᵢ succeeds.
- **Core empirical results (Abstract, Sec. 4, Fig. 8–9, Table 2):**
  - Current LLMs solve **<66%** of tasks even **without attacks** (Abstract).
  - “Important message” injection: best agents see **<25% targeted ASR** (Abstract); Slack suite can reach **92% ASR** for GPT-4o (Fig. 7).
  - **Defense effect:** with an added attack detector, targeted ASR drops to **~8%** (Abstract).
  - **Tool filter defense** (isolation-lite): targeted ASR **7.5%** (Sec. 4.3); fails when task tools suffice for attack (**17%** of cases).
  - **Attacker knowledge ablation (Table 2, targeted ASR):** baseline **45.8%**; both correct user+model **47.7%** (+1.9%); wrong user **23.2%**; wrong model **23.7%**.
  - **Attack phrasing matters:** “Important message” > prior (InjecAgent / ignore-prev / TODO); “Max” adds **~10%** ASR boost (Fig. 8).
  - **Injection position:** end-of-tool-response most effective, up to **~70%** ASR vs GPT-4o (Sec. 4.2).
- **Design rationale (Sec. 3.1):** deterministic, state-based utility/security checks (not LLM judges) to avoid evaluation being hijacked by injections.

</details>

### 📖 Claude Code CLI command/flag reference
**Reference Doc** · [source](https://docs.anthropic.com/en/docs/claude-code/cli-reference.md)

*Complete Claude Code CLI commands + flags (exact behaviors/defaults)*

<details>
<summary>Key content</summary>

- **Session start / query modes**
  - `claude` = interactive session.
  - `claude "query"` = interactive with initial prompt.
  - `claude -p "query"` = **print mode** (SDK query) then exit.
  - `cat file | claude -p "query"` = process piped content.
- **Resume/continue**
  - `claude -c/--continue` = load most recent conversation in current directory.
  - `claude -r/--resume <session>` = resume by ID/name or open picker.
  - `--fork-session` = when resuming/continuing, create **new session ID**.
  - `--session-id <uuid>` = force a specific UUID session ID.
  - `--name/-n "<display>"` = session display name; resumable via `--resume <name>`.
- **Auth / updates**
  - `claude auth status` outputs JSON; `--text` for human output; exit code **0 logged in, 1 not**.
  - `claude auth login --console` = sign in with Anthropic Console billing (API usage) vs subscription.
  - `claude update` updates to latest version.
  - `claude setup-token` prints long-lived OAuth token (CI/scripts); requires subscription.
- **Permissions / guardrails**
  - `--permission-mode {default,acceptEdits,plan,auto,dontAsk,bypassPermissions}`.
  - `--dangerously-skip-permissions` ≡ `--permission-mode bypassPermissions`.
  - `--allow-dangerously-skip-permissions` adds `bypassPermissions` to Shift+Tab cycle (not starting in it).
  - Tool control: `--tools` (restrict available tools), `--allowedTools` (auto-allow without prompting), `--disallowedTools` (remove from context).
- **Cost/latency controls (print mode)**
  - `--max-budget-usd <amount>` = stop after spending that USD.
  - `--max-turns <n>` = limit agentic turns; **no limit by default**.
  - `--fallback-model <model>` = auto fallback when default overloaded (print mode only).
- **Prompt customization (system prompt flags)**
  - Replace: `--system-prompt`, `--system-prompt-file` (**mutually exclusive**).
  - Append: `--append-system-prompt`, `--append-system-prompt-file` (can combine with replacement).
  - Rationale: **prefer append** to preserve built-in capabilities; replace only for full control.
- **Performance / reproducibility**
  - `--bare` = minimal mode; skips auto-discovery (hooks/skills/plugins/MCP/auto memory/CLAUDE.md); still has Bash/Read/Edit; sets `CLAUDE_CODE_SIMPLE`.
  - `--exclude-dynamic-system-prompt-sections` moves machine-specific sections into first user msg to improve prompt-cache reuse (ignored if custom system prompt set).

</details>

### 📋 # Source: https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-security/best-practices-input-validation.html
**Source** · 

### 🔍 Production LLM Guardrails — Tool & Latency/FP Trade-offs
**Explainer** · [source](https://blog.premai.io/production-llm-guardrails-nemo-guardrails-ai-llama-guard-compared/)

*Side-by-side comparison of NeMo Guardrails vs Guardrails AI vs Llama Guard (+ LLM Guard), with latency, deployment patterns, and production trade-offs.*

<details>
<summary>Key content</summary>

- **Guardrail stages + latency budgets (Table):** Input (prompt injection/PII/banned topics) **50–200ms**; Output (toxicity/secrets/off-topic) **100–500ms**; Retrieval (poisoned chunks/sensitive docs) **20–100ms**.
- **False-positive compounding math (Eq. 1):**  
  - \(P(\text{all correct}) = a^n\) where \(a\)=per-guard accuracy, \(n\)=#guards.  
  - \(P(\ge 1 \text{ false positive}) = 1 - a^n\).  
  - Example: \(a=0.9, n=5 \Rightarrow 1-0.9^5=0.41\) (**41%** flagged). Table: 5 guards @95% ⇒ **23%** FP; 5 @99% ⇒ **5%** FP.
- **Latency tiers:** Tier1 rules **µs–10ms**; Tier2 classifiers **20–100ms**; Tier3 LLM-judge **500ms–8s**. Rationale: **layer + early exit** to keep average latency low.
- **Tool selection matrix (key rows):**  
  - **NeMo Guardrails:** dialog/topic steering; **medium** latency; **T4** GPU; open source; adds **1 LLM call** for flow routing; rail types: **input/output/dialog/retrieval/execution** (execution wraps tool calls).  
  - **Guardrails AI:** structured output validation via **RAIL** specs; latency **20–200ms** per validator; supports **server mode** (`guardrails start ...`); `on_fail`: **REFRAIN/FIX/EXCEPTION/NOOP**.  
  - **LLM Guard:** scanner pipeline; **20–200ms**; anonymize/deanonymize with **Vault** (in-memory mappings).  
  - **Llama Guard 3-8B:** LLM classifier; **800ms P50**; needs **A100**; vision moderation; categories **S1–S13**; customizable via system prompt.
- **Empirical P50 latency (benchmarks):** Regex **<1ms**; LLM Guard toxicity **45ms** (5-guard pipeline **120ms**); Presidio PII **35ms**; Guardrails AI pipeline **300–500ms**; NeMo input check **150–400ms** (pipeline **600ms–1.2s**); Llama Guard **800ms**.
- **Accuracy (datasets):** ToxiGen F1: Llama Guard 3 **0.89** vs OpenAI Moderation **0.82**. JailbreakBench detection/FP: Regex **35%/2%**, PromptGuard(BERT) **72%/8%**, LLM Guard inj **78%/12%**, Llama Guard 3 **85%/15%**, **NeMo+Nemotron 89%/11%**.
- **Cost for 1M req/mo:** Regex **~$20**; LLM Guard **~$150**; Guardrails AI **~$200**; Llama Guard(A100) **~$800**; OpenAI Moderation **$200 API**; GPT-4 judge **$3k–10k**.
- **Deployment patterns:** **Sidecar proxy**, **middleware**, **async pipeline** (Kafka worker). Monitoring: track **P50/P95/P99**, block spikes, error rate, queue depth; graceful degradation via **timeouts + fallback** (fail open vs closed).

</details>

---

## Related Topics

- [[topics/agent-fundamentals|Agent Fundamentals]]
- [[topics/multi-agent-systems|Multi-Agent Systems]]
- [[topics/agentic-coding|Agentic Coding]]
- [[topics/mcp-tool-ecosystem|Model Context Protocol]]
