## Core Definitions

**Prompt injection** — A class of security vulnerabilities where an attacker crafts input (or *untrusted retrieved/tool content*) that causes an LLM-based system to ignore intended instructions and follow the attacker’s instructions instead. OWASP lists this as **LLM01: Prompt Injection**, emphasizing that manipulation via crafted inputs can lead to unauthorized access, data breaches, and compromised decision-making. (OWASP Top 10 for LLM Applications: https://owasp.org/www-project-top-10-for-large-language-model-applications/)

**Guardrails (runtime guardrails)** — Mechanisms integrated into an FM/LLM application or agent architecture to safeguard behavior *during runtime*, preventing undesirable/unsafe behaviors (as opposed to design-time alignment). The “Swiss cheese” framing motivates multiple layers because any single layer can fail. (Swiss-cheese runtime guardrails paper: https://arxiv.org/html/2408.02205v3)

**NeMo Guardrails** — An open-source toolkit for adding *programmable guardrails* (“rails”) between application code and an LLM to control behavior (topic steering, dialog flows, style constraints, structured extraction, and protections against jailbreaks/prompt injections). It can be used via Python API or as a server layer. (NVIDIA repo: https://github.com/NVIDIA/NeMo-Guardrails)

**Sandboxing** — A containment strategy for agent tool execution: run code/tools in an isolated environment with constrained resources and access, so that even if the agent is manipulated, the blast radius is limited. (This lesson’s sources emphasize layered defenses and tool-call safety; sandboxing is a standard “isolate” action in the runtime guardrails taxonomy.) (Swiss-cheese runtime guardrails paper: https://arxiv.org/html/2408.02205v3)

**Principle of least privilege** — A permission design rule: give an agent (and its tools) only the minimum permissions needed to complete the current task, reducing damage from mistakes or compromise. In practice this often means restricting tool availability and requiring approvals for sensitive actions. (Claude Code CLI exposes explicit permission modes and tool allow/deny lists, illustrating least-privilege controls in an agentic tool runner.) (Claude Code CLI reference: https://docs.anthropic.com/en/docs/claude-code/cli-reference.md)

**Defense in depth** — A security strategy that uses multiple, diverse layers of controls (e.g., rules → classifiers → LLM-judges; input → retrieval → output → execution gates) so that if one layer fails, others still reduce risk. The runtime guardrails “Swiss cheese model” explicitly argues single-layer guardrails are insufficient for autonomous, non-deterministic agents. (Swiss-cheese runtime guardrails paper: https://arxiv.org/html/2408.02205v3; production guardrails trade-offs: https://blog.premai.io/production-llm-guardrails-nemo-guardrails-ai-llama-guard-compared/)

**Goal drift** — In agentic systems, the phenomenon where the agent’s effective objective shifts away from the user/developer intent over time or across steps (e.g., due to prompt injection in tool outputs, accumulating memory, or mis-specified intermediate goals). The runtime guardrails taxonomy explicitly includes guarding *goals* and *plans* as artifacts that can be validated/blocked/modified. (Swiss-cheese runtime guardrails paper: https://arxiv.org/html/2408.02205v3)

---

## Key Formulas & Empirical Results

### False-positive compounding across multiple guards (production guardrail pipelines)
If each guard has accuracy \(a\) and you chain \(n\) guards, then:
- \(P(\text{all correct}) = a^n\)
- \(P(\ge 1 \text{ false positive}) = 1 - a^n\)

Example from the source: \(a=0.9, n=5 \Rightarrow 1-0.9^5=0.41\) → **41%** flagged. Table examples: **5 guards @95% ⇒ 23% FP; 5 @99% ⇒ 5% FP**.  
Supports: why “add more detectors” can quickly create usability/latency problems; motivates early-exit tiers and careful calibration.  
(Source: https://blog.premai.io/production-llm-guardrails-nemo-guardrails-ai-llama-guard-compared/)

### Latency budgets by guardrail stage (production)
Typical stage budgets reported:
- **Input** checks (prompt injection/PII/banned topics): **50–200ms**
- **Output** checks (toxicity/secrets/off-topic): **100–500ms**
- **Retrieval** checks (poisoned chunks/sensitive docs): **20–100ms**

Supports: designing guardrails as a pipeline with stage-specific SLAs.  
(Source: https://blog.premai.io/production-llm-guardrails-nemo-guardrails-ai-llama-guard-compared/)

### Latency tiers (rules → classifiers → LLM-judge)
- Tier 1 rules: **µs–10ms**
- Tier 2 classifiers: **20–100ms**
- Tier 3 LLM-judge: **500ms–8s**

Supports: “layer + early exit” to keep average latency low.  
(Source: https://blog.premai.io/production-llm-guardrails-nemo-guardrails-ai-llama-guard-compared/)

### AgentDojo benchmark scale + defense effect (tool-using agents under injection)
- **97** user tasks, **74** tools, **629** security test cases across 4 environments (Workspace/Slack/Travel/Banking).
- Attacks can be extremely effective in some suites (e.g., Slack “Important message” can reach **92%** attack success in reported results).
- Adding a **prompt-injection detector** can reduce attack success to **~8%** (reported summary).
- A “tool filter” defense (pre-select minimal tools before seeing untrusted data) reduces targeted ASR to **7.5%**, but fails when the same tools suffice for the attack (**17%** of cases).

Supports: prompt injection is not just “user prompt”; tool outputs are a major injection surface; isolation/tool-minimization can be powerful.  
(Sources: arXiv: https://arxiv.org/abs/2406.13352 and NeurIPS dataset/bench paper: https://proceedings.neurips.cc/paper_files/paper/2024/file/97091a5177d8dc64b1da8bf3e1f6fb54-Paper-Datasets_and_Benchmarks_Track.pdf)

### CAPTURE benchmark: detector trade-off (over-defense vs misses)
CAPTURE evaluates prompt-injection detectors with:
- **FNR** on MALICIOUS-GEN (missed attacks)
- **FPR** on SAFE-GEN (benign flagged)

Notable results (examples reported):
- **PromptGuard:** **FNR 0%** but **FPR ~100%** in many domains.
- **GPT-4o baseline detector:** low FNR (**~7–16%**) and low FPR (**~2.6–13%**).
- **CaptureGuard (trained on CAPTURE data):** **FNR 0.00–0.15%**, **FPR 0.00–2.05%** on tested domains.

Supports: naive detectors can either block everything or miss everything; context-aware test generation is crucial.  
(Source: https://aclanthology.org/2025.llmsec-1.13.pdf)

### WebGuard: action-risk guardrail metrics (web agents)
Risk label prediction:
\[
y = f_\theta(s, a, \mathcal{R}) \in \{\text{SAFE}, \text{LOW}, \text{HIGH}\}
\]
Fine-tuned WebGuard-VL-7B results (selected):
- Long-Tail: **Acc 84.6 / RecallH 86.0 / RecallL 87.1**
- Cross-Domain: **Acc 75.2 / RecallH 66.8 / RecallL 87.5**

Supports: guardrails can be framed as *pre-execution risk classification* with HITL thresholds.  
(Source: https://arxiv.org/html/2507.14293v1)

---

## How It Works

### A. Where guardrails sit in an agent loop (runtime “Swiss cheese” placement)
Use the runtime guardrails taxonomy to place controls on both **pipelines** and **artifacts**:

1. **Before model call (prompt/input stage)**  
   - Actions: block/filter/flag/modify; retry/defer; parallel checks.  
   - Target: user input + any untrusted context being inserted.

2. **During retrieval (RAG stage)**  
   - Actions: validate/filter/flag retrieved chunks; isolate sensitive docs.  
   - Target: retrieved text that can contain injections or secrets.

3. **During planning (intermediate artifacts)**  
   - Actions: validate/flag/modify plans; defer to human; fall back.  
   - Target: the *plan* and *goals* (explicitly called out as guardable artifacts).

4. **Before tool execution (execution guardrails)**  
   - Actions: block/validate/modify tool calls; isolate tool execution; require approval.  
   - Target: tool selection + tool arguments + side-effecting actions.

5. **After tool execution (observation/tool output stage)**  
   - Actions: treat tool output as untrusted; scan for injection patterns; constrain what can be copied into the next prompt.

6. **Before final answer (output stage)**  
   - Actions: block/filter/modify; retry; fall back; human intervention.  
   - Target: user-visible output (toxicity, secrets, policy violations, off-topic).

(From the runtime guardrails mapping of actions→targets and the “Swiss cheese model” rationale: https://arxiv.org/html/2408.02205v3)

### B. Production guardrail pipeline mechanics (latency-aware layering)
A common production pattern (from the guardrails comparison source):

1. **Tier 1 (fast rules)**: regex/allowlists/format checks; early exit if clearly safe/unsafe.  
2. **Tier 2 (classifiers)**: moderate latency detectors (toxicity, PII, injection).  
3. **Tier 3 (LLM-judge)**: slow but flexible adjudication for ambiguous cases.  
4. **Timeouts + fallback**: if a guard times out, decide “fail open vs fail closed” per risk.  
5. **Monitoring**: track P50/P95/P99 latency, block spikes, error rate, queue depth; degrade gracefully.

(Source: https://blog.premai.io/production-llm-guardrails-nemo-guardrails-ai-llama-guard-compared/)

### C. Input validation best practices for agentic systems (AWS guidance)
1. Treat user inputs as the **primary attack vector** (prompt injection/manipulation).  
2. Use **multi-layered validation**: application-level sanitization + model-level guardrails.  
3. Maintain **automated prompt security test suites** (e.g., prompt injection, jailbreaking, adversarial inputs; multi-turn attacks; cross-agent propagation).  
4. Establish baseline metrics: injection detection rates, false positive thresholds, response consistency; run continuously in CI.  
5. Enable prompt logging + metrics to monitor masking/blocking trends.

(Source: AWS prescriptive guidance: https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-security/best-practices-input-validation.html)

---

## Teaching Approaches

### Intuitive (no math)
- Agents are dangerous because they **do things**, not just **say things**.  
- Any single safety layer can be bypassed (or can fail), so you stack layers: *screen inputs, constrain tools, sandbox execution, and gate risky actions with humans*.

### Technical (with metrics)
- Guardrails are a pipeline with measurable **FPR/FNR** and **latency**.  
- Adding more guards increases coverage but compounds false positives: \(1-a^n\).  
- Benchmarks like **AgentDojo** show tool-output injections can drive high ASR; adding detectors or tool filtering can reduce ASR to single digits (e.g., ~8% / 7.5% reported).

### Analogy-based
- “Swiss cheese security”: each slice has holes; stacking slices reduces the chance a straight-line attack passes through all holes. (Runtime guardrails paper explicitly uses this model: https://arxiv.org/html/2408.02205v3)

---

## Common Misconceptions

1. **“If I add delimiters around tool output / retrieved text, prompt injection is solved.”**  
   - Why wrong: injection can still be effective even when content is clearly separated; attackers exploit the model’s tendency to follow salient instructions. The AgentDojo benchmark shows injections placed in tool outputs can be highly effective, and defenses require more than formatting.  
   - Correct model: treat tool outputs as **untrusted**, apply **detectors**, and constrain **tool choice/execution** (e.g., tool filtering reduced ASR to 7.5% in AgentDojo).  
   - Sources: AgentDojo defense comparison (https://arxiv.org/abs/2406.13352); prompt injection is a core OWASP risk (https://owasp.org/www-project-top-10-for-large-language-model-applications/)

2. **“More guardrails always makes the system safer.”**  
   - Why wrong: chaining guards compounds false positives: \(P(\ge1\text{ FP})=1-a^n\). With 5 guards at 90% accuracy, **41%** of requests get flagged in the example.  
   - Correct model: use **tiering + early exit**, calibrate thresholds, and measure FPR/FNR and latency budgets per stage.  
   - Source: production guardrails compounding math + tiers (https://blog.premai.io/production-llm-guardrails-nemo-guardrails-ai-llama-guard-compared/)

3. **“Prompt injection is only about the user typing ‘ignore previous instructions’.”**  
   - Why wrong: in tool-using agents, the attacker can inject via **tool outputs** (emails, Slack messages, web pages, retrieved docs). AgentDojo explicitly places injections in tool outputs actually queried.  
   - Correct model: defend at **input, retrieval, and execution** layers; treat every external channel as an injection surface.  
   - Source: AgentDojo benchmark construction (https://arxiv.org/abs/2406.13352)

4. **“A prompt-injection detector that never misses attacks is ideal.”**  
   - Why wrong: CAPTURE shows detectors can achieve **FNR 0%** while having **FPR ~100%** (blocking benign prompts), which breaks usability.  
   - Correct model: optimize the *trade-off* using realistic benign “over-defense” tests (SAFE-GEN) and malicious tests (MALICIOUS-GEN).  
   - Source: CAPTURE results (https://aclanthology.org/2025.llmsec-1.13.pdf)

5. **“If the model is aligned (RLHF/CAI), agents don’t need runtime guardrails.”**  
   - Why wrong: runtime guardrails are explicitly motivated as necessary because agents are autonomous and non-deterministic; safety must be enforced at runtime across prompts, plans, tools, and outputs.  
   - Correct model: training-time alignment reduces risk, but runtime controls (block/validate/isolate/defer) are still required.  
   - Source: runtime guardrails definition + Swiss cheese rationale (https://arxiv.org/html/2408.02205v3)

---

## Worked Examples

### Example 1: Estimating false-positive rate when stacking guards
**Scenario:** You add 5 independent guard checks, each with 95% accuracy on benign traffic (so 5% false positive rate per guard, simplified).

Compute probability at least one flags a benign request:
\[
P(\ge1\text{ FP}) = 1 - a^n = 1 - 0.95^5 \approx 0.226
\]
So **~23%** of benign requests get flagged (matches the source’s table example).  
Use this mid-conversation to justify: “we need early-exit tiers and careful calibration.”  
(Source: https://blog.premai.io/production-llm-guardrails-nemo-guardrails-ai-llama-guard-compared/)

### Example 2: Least-privilege tool access in a CLI agent (Claude Code)
**Goal:** Demonstrate concrete knobs for restricting an agent’s capabilities.

- Restrict which tools are even available:
  - Use `--tools` to restrict available tools (source describes tool control flags).
- Auto-allow only a subset:
  - `--allowedTools` (auto-allow without prompting)
- Remove tools from context:
  - `--disallowedTools`

- Enforce permission prompting behavior:
  - `--permission-mode {default,acceptEdits,plan,auto,dontAsk,bypassPermissions}`
  - `--dangerously-skip-permissions` ≡ `--permission-mode bypassPermissions` (explicitly dangerous)

Tutor move: ask the student which mode/tool set they’d choose for (a) read-only repo analysis vs (b) production deploy.  
(Source: https://docs.anthropic.com/en/docs/claude-code/cli-reference.md)

### Example 3: Pre-execution action-risk guardrail (WebGuard pattern)
**Pattern:** Before executing a web action, classify risk:
\[
y = f_\theta(s, a, \mathcal{R}) \in \{\text{SAFE}, \text{LOW}, \text{HIGH}\}
\]
Then:
- If \(y\) exceeds a user-set threshold (LOW or HIGH), **pause** and require **approve/reject/revise**.

Use this as a worked “HITL gate” template for any side-effecting tool (payments, deletes, sending messages).  
(Source: https://arxiv.org/html/2507-14293v1)

---

## Comparisons & Trade-offs

| Approach / Tool | What it’s best at (per sources) | Typical latency / cost notes | Key trade-off / failure mode | Source |
|---|---|---|---|---|
| **NeMo Guardrails** | Dialog/topic steering; multiple rail types incl. **execution** wrapping tool calls | Adds ~1 LLM call for flow routing; “medium” latency; GPU noted (T4) | Strong for conversational control; still needs layered defenses | https://blog.premai.io/production-llm-guardrails-nemo-guardrails-ai-llama-guard-compared/ ; https://github.com/NVIDIA/NeMo-Guardrails |
| **Guardrails AI** | Structured output validation via RAIL specs; `on_fail` behaviors (REFRAIN/FIX/EXCEPTION/NOOP) | Validators ~20–200ms each; pipelines ~300–500ms reported | Great for schema/format; doesn’t solve tool-output injection alone | https://blog.premai.io/production-llm-guardrails-nemo-guardrails-ai-llama-guard-compared/ |
| **Llama Guard 3-8B** | LLM-based safety classifier; customizable categories | ~800ms P50; needs A100 (per benchmark notes) | Higher latency; still has FPR/FNR trade-offs | https://blog.premai.io/production-llm-guardrails-nemo-guardrails-ai-llama-guard-compared/ |
| **Tool filtering (AgentDojo defense)** | Reduce attack surface by selecting minimal tools before seeing untrusted data | Not given as latency; conceptually reduces exposure | Fails when task tools also enable attack (**17%** cases) | https://arxiv.org/abs/2406.13352 |
| **Prompt-injection detectors (CAPTURE/AgentDojo)** | Detect injection attempts in context | Varies; classifier tier often 20–100ms | Can over-block (FPR) or miss (FNR); needs realistic eval | https://aclanthology.org/2025.llmsec-1.13.pdf ; https://arxiv.org/abs/2406.13352 |

---

## Prerequisite Connections

- **Instruction hierarchy (system > developer > user)** — Needed to reason about what “prompt injection” is overriding; also appears as an explicit evaluation category in OpenAI’s eval hub. (https://openai.com/safety/evaluations-hub/)
- **Agent loop basics (plan → act/tool → observe → respond)** — Needed to see where to place guardrails (input/retrieval/execution/output). (Weng’s agent overview: https://lilianweng.github.io/posts/2023-06-23-agent/)
- **Basic security concepts (attack surface, least privilege, defense in depth)** — Needed to justify layered controls and permission models. (Runtime guardrails Swiss cheese model: https://arxiv.org/html/2408.02205v3)

---

## Socratic Question Bank

1. **Where can prompt injection enter an agent besides the user’s message?**  
   *Good answer:* tool outputs, retrieved docs, web pages/DOM, memory, cross-agent messages (AgentDojo places injections in tool outputs).

2. **If each guard is 95% accurate, what happens to benign traffic when you chain 5 guards?**  
   *Good answer:* \(1-0.95^5 \approx 23\%\) flagged; compounding FPs.

3. **What’s the difference between guarding “output text” and guarding “execution”?**  
   *Good answer:* output moderation prevents harmful text; execution guardrails prevent side effects (tool calls), often pre-execution.

4. **Why might a detector with FNR=0% still be unacceptable in production?**  
   *Good answer:* could have huge FPR (CAPTURE shows ~100% FPR cases), blocking benign use.

5. **What does “tool filtering” buy you, and when does it fail?**  
   *Good answer:* reduces attack surface; fails when same tools needed for task can perform attack (17% cases in AgentDojo).

6. **What’s a concrete example of least privilege for an agentic CLI tool?**  
   *Good answer:* restrict tools, require permission prompts; avoid bypassPermissions; use allow/deny lists (Claude Code flags).

7. **Where would you put a human-in-the-loop gate, and what triggers it?**  
   *Good answer:* before high-risk actions (payments/deletes/sends); trigger on risk classifier label (WebGuard SAFE/LOW/HIGH).

8. **What metrics would you monitor to detect a rising injection campaign?**  
   *Good answer:* guardrail block/mask rates, prompt-attack filter metrics, trends in sensitive-info policy triggers (AWS guidance suggests logging + metrics).

---

## Likely Student Questions

**Q: If I add more guardrails, why do I suddenly get lots of false alarms?**  
→ **A:** False positives compound: if each guard has accuracy \(a\) and you chain \(n\), \(P(\ge1\text{ FP})=1-a^n\). Example given: \(a=0.9,n=5\Rightarrow 41\%\) flagged; table shows 5 guards @95% ⇒ **23%** FP. (https://blog.premai.io/production-llm-guardrails-nemo-guardrails-ai-llama-guard-compared/)

**Q: What are typical latency budgets for input/output/retrieval guardrails?**  
→ **A:** Reported budgets: Input **50–200ms**, Output **100–500ms**, Retrieval **20–100ms**. (https://blog.premai.io/production-llm-guardrails-nemo-guardrails-ai-llama-guard-compared/)

**Q: How do we evaluate prompt injection robustness for tool-using agents?**  
→ **A:** AgentDojo provides **97** user tasks, **74** tools, **629** security test cases with deterministic checks; metrics include Benign Utility, Utility Under Attack, and Targeted ASR. (https://arxiv.org/abs/2406.13352)

**Q: Do detectors actually help against tool-output prompt injection?**  
→ **A:** In AgentDojo’s reported summary, adding a prompt-injection detector can reduce attack success to **~8%**; tool filtering reduces targeted ASR to **7.5%** (but fails in **17%** of cases). (https://arxiv.org/abs/2406.13352)

**Q: Why not just use a detector that never misses (FNR=0%)?**  
→ **A:** CAPTURE shows a detector can have **FNR 0%** but **FPR ~100%** (blocking benign prompts), which is unusable. CAPTURE explicitly measures both FNR (malicious) and FPR (benign over-defense). (https://aclanthology.org/2025.llmsec-1.13.pdf)

**Q: What does a “human-in-the-loop” action gate look like in practice?**  
→ **A:** WebGuard runs a risk classifier **before execution** and pauses if risk exceeds a threshold; user can approve/reject/revise. Risk labels are **SAFE/LOW/HIGH**. (https://arxiv.org/html/2507.14293v1)

**Q: What concrete knobs exist for least-privilege in a real agent tool runner?**  
→ **A:** Claude Code CLI supports `--permission-mode` (including dangerous bypass), plus `--tools`, `--allowedTools`, `--disallowedTools` to restrict tool access. (https://docs.anthropic.com/en/docs/claude-code/cli-reference.md)

---

## Available Resources

### Videos
- [AI Agents: Safety, Security, and Trust](https://youtube.com/watch?v=kJLiOGle3Lw) — Surface when: student asks for an end-to-end discussion of agent safety/security/trust framing.

### Articles & Tutorials
- [Lilian Weng — LLM Powered Autonomous Agents](https://lilianweng.github.io/posts/2023-06-23-agent/) — Surface when: student needs the agent loop (planning/memory/tools) to understand *where* guardrails attach.
- [OWASP Top 10 for Large Language Model Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/) — Surface when: student asks “what are the standard named risks?” esp. **LLM01 Prompt Injection** and insecure output handling.
- [NVIDIA NeMo Guardrails (GitHub)](https://github.com/NVIDIA-NeMo/Guardrails) — Surface when: student asks “what is NeMo Guardrails and what can it control?”
- [AWS Prescriptive Guidance: Input validation and guardrails for agentic AI systems](https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-security/best-practices-input-validation.html) — Surface when: student asks about operational best practices (testing suites, logging/metrics, Bedrock Guardrails).

---

## Visual Aids

![LLM-powered autonomous agent system overview with planning, memory, and tools. (Weng, 2023)](/api/wiki-images/agent-skills-safety/images/lilianweng-posts-2023-06-23-agent_001.png)  
Show when: student is confused about the agent architecture and you need to point to *where* to place input/retrieval/execution/output guardrails.

---

## Key Sources

- [Production LLM Guardrails — Tool & Latency/FP Trade-offs](https://blog.premai.io/production-llm-guardrails-nemo-guardrails-ai-llama-guard-compared/) — Concrete production numbers: latency tiers, stage budgets, FP compounding math, tool comparisons.
- [AgentDojo benchmark (arXiv)](https://arxiv.org/abs/2406.13352) — Canonical tool-using agent prompt-injection benchmark with metrics and defense ablations (detectors, tool filtering).
- [CAPTURE benchmark (LLMsec 2025)](https://aclanthology.org/2025.llmsec-1.13.pdf) — Context-aware injection test generation + explicit FNR/FPR trade-offs; shows over-defense failure modes.
- [Swiss-cheese multi-layer runtime guardrails for FM web agents](https://arxiv.org/html/2408.02205v3) — Taxonomy + reference architecture for placing guardrails across prompts, goals, plans, tools, memory, and outputs.
- [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/) — Standardized naming and framing of prompt injection as a top risk (LLM01).