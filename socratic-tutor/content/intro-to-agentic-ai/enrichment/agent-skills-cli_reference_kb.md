## Core Definitions

**Agent skill** — A reusable, composable agent behavior that packages a multi-step workflow (often “plan → act with tools → verify → iterate”) so it can be invoked consistently across tasks. Weng frames agent behavior as an LLM “brain” orchestrating **planning**, **memory**, and **tool use**; a “skill” is best understood as a repeatable unit built on top of that tool-using loop (Weng, 2023: planning/memory/tools decomposition) https://lilianweng.github.io/posts/2023-06-23-agent/

**Skill composition** — Combining multiple skills into a larger workflow where outputs of one skill become inputs/constraints for the next (e.g., “localize files → implement patch → run tests → open PR”). This aligns with the ReAct-style interleaving of reasoning and acting: the agent alternates between internal reasoning/planning and external actions/observations, which naturally supports chaining subroutines (Yao et al., 2022 ReAct) https://arxiv.org/abs/2210.03629

**Skill discovery** — The process by which an agent identifies which skills/tools to use for a task, typically by inspecting available tool/skill descriptions and selecting a minimal set before interacting with untrusted data. AgentDojo’s “tool filter” defense highlights why discovery/selection matters: pre-selecting minimal tools can reduce prompt-injection success (AgentDojo, Sec. 4.3) https://arxiv.org/abs/2406.13352

**Skill registry** — A structured catalog of skills (names, descriptions, parameters, permissions) that an agent can consult at runtime. In Claude Code, analogous “startup-discovered” capabilities include hooks/skills/plugins/MCP/CLAUDE.md unless `--bare` is used, which disables that auto-discovery (Claude Code CLI reference: `--bare`) https://docs.anthropic.com/en/docs/claude-code/cli-reference.md

**CLI agent** — A tool-using agent that leverages the terminal (shell commands, test runners, linters, git/gh, etc.) as a universal interface for software work. Claude Code is an example: it can run Bash, read/edit files, manage sessions, and iterate with verification (Claude Code best practices; CLI reference) https://code.claude.com/docs/en/best-practices and https://docs.anthropic.com/en/docs/claude-code/cli-reference.md

**Cursor (as a coding-agent environment)** — Not defined in the provided sources; treat as an IDE context where agent skills may be surfaced as reusable workflows. (No Cursor-specific primary source included in the curated set.)

**Claude Code** — Anthropic’s CLI-based coding agent. Key operational features in the sources include: interactive vs print mode invocation, session resume/forking, permission modes (including Plan Mode), tool allow/deny lists, and “bare” minimal startup mode (Claude Code CLI reference; common workflows) https://docs.anthropic.com/en/docs/claude-code/cli-reference.md and https://code.claude.com/docs/en/common-workflows

---

## Key Formulas & Empirical Results

### Prompt-injection robustness metrics (AgentDojo)
- **Benign Utility** = fraction of user tasks solved with no attack.  
- **Utility Under Attack** = fraction of security cases where the user task is solved **without adversarial side effects**.  
- **Targeted ASR** = fraction of security cases where attacker goal is achieved.  
(AgentDojo, Sec. 3.4) https://arxiv.org/abs/2406.13352

**Scale / difficulty numbers (AgentDojo):**
- 4 environments; **74 tools** total; **97** user tasks; **629** security test cases; up to **18 tool calls**; contexts up to ~**7,000** tokens data + ~**4,000** tokens tool descriptions. (AgentDojo) https://arxiv.org/abs/2406.13352  
**Defense result:** “tool filter” lowers targeted ASR to **7.5%** (AgentDojo Sec. 4.3) https://arxiv.org/abs/2406.13352  
**Detector add-on:** targeted ASR drops to ~**8%** with a secondary prompt-injection detector (AgentDojo abstract) https://arxiv.org/abs/2406.13352

### False-positive compounding for layered guardrails (Premai guardrails comparison)
If each guard has accuracy \(a\) and you chain \(n\) guards:
- \(P(\text{all correct}) = a^n\)  
- \(P(\ge 1 \text{ false positive}) = 1 - a^n\)  
Example given: \(a=0.9, n=5 \Rightarrow 1-0.9^5=0.41\) (41% flagged). (Premai blog) https://blog.premai.io/production-llm-guardrails-nemo-guardrails-ai-llama-guard-compared/

### CAPTURE guardrail evaluation (FNR/FPR)
- Metrics: **False Negative Rate (FNR%)** on MALICIOUS-GEN; **False Positive Rate (FPR%)** on SAFE-GEN.  
- Reported results include: **PromptGuard FNR 0%** but **FPR ~100%** in many domains; **GPT-4o baseline** low FNR (~7–16%) and low FPR (~2–13%); **CaptureGuard** near-zero errors (FNR **0.00–0.15%**, FPR **0.00–2.05%** on tested domains). (CAPTURE paper) https://aclanthology.org/2025.llmsec-1.13.pdf

### Claude Code operational defaults / flags (CLI reference)
- `--max-turns <n>`: **no limit by default** (print mode).  
- `--max-budget-usd <amount>`: stop after spending that USD (print mode).  
- `--permission-mode {default,acceptEdits,plan,auto,dontAsk,bypassPermissions}`.  
- `--dangerously-skip-permissions` ≡ `--permission-mode bypassPermissions`.  
- `--bare`: disables auto-discovery (hooks/skills/plugins/MCP/auto memory/CLAUDE.md).  
(Claude Code CLI reference) https://docs.anthropic.com/en/docs/claude-code/cli-reference.md

---

## How It Works

### A. “Skillful” agent loop for coding in a CLI agent (Claude Code best practices)
Use this as the mechanical template for a reusable coding skill.

1) **Explore (Plan Mode / read-only)**  
   - Read relevant files; ask clarifying questions; avoid edits.  
   - Claude Code supports Plan Mode explicitly; it forces read-only operations while the agent proposes a plan. (Common workflows) https://code.claude.com/docs/en/common-workflows

2) **Plan (explicit implementation plan)**  
   - Produce a detailed plan; in Claude Code, the plan can be opened for human edits (best practices mention Ctrl+G to open plan in editor).  
   - Planning can be skipped for tiny diffs (“describe the diff in one sentence”). (Best practices) https://code.claude.com/docs/en/best-practices

3) **Implement (Normal Mode)**  
   - Make code changes according to the plan; keep changes scoped.

4) **Verify (tight feedback loop)**  
   - Run tests/linters/shell checks; iterate until success criteria are met.  
   - Best practices: Claude performs “dramatically better” when it can verify its own work (tests/linters). (Best practices) https://code.claude.com/docs/en/best-practices

5) **Context management (to keep the skill reliable over time)**  
   - Claude Code context includes entire conversation + every file read + every command output; it fills quickly and performance degrades.  
   - Use `/clear` between unrelated tasks; `/compact <instructions>`; `/rewind` or Esc+Esc to restore/summarize; stop mid-action with Esc. (Best practices) https://code.claude.com/docs/en/best-practices

### B. Skill discovery/selection as a security control (AgentDojo “tool filter”)
A practical “skill discovery” procedure that doubles as a guardrail:

1) **Before reading untrusted content** (web pages, tool outputs, user-provided docs), decide which tools/skills are necessary.  
2) **Restrict tool availability** to that minimal set (conceptually; in Claude Code you can restrict tools via `--tools`, `--allowedTools`, `--disallowedTools`). (CLI reference) https://docs.anthropic.com/en/docs/claude-code/cli-reference.md  
3) Execute the task with reduced tool surface area.  
AgentDojo reports this “tool filter” defense reduces targeted ASR to **7.5%** but can fail when the same tools needed for the user task also enable the attack (17% of cases). (AgentDojo Sec. 4.3) https://arxiv.org/abs/2406.13352

### C. Session + workflow mechanics in Claude Code (common workflows + CLI reference)

**Start modes**
- Interactive: `claude` or `claude "query"`  
- Print/headless: `claude -p "query"`; can pipe input: `cat file | claude -p "query"`  
(CLI reference) https://docs.anthropic.com/en/docs/claude-code/cli-reference.md

**Resume / branch sessions**
- Continue most recent in dir: `claude --continue`  
- Resume by ID/name: `claude --resume <session>`  
- Fork on resume: `--fork-session`  
(CLI reference) https://docs.anthropic.com/en/docs/claude-code/cli-reference.md

**Plan Mode**
- In-session: Shift+Tab cycles permission modes; Plan Mode indicator “⏸ plan mode on”.  
- Start in Plan Mode: `claude --permission-mode plan`  
(Common workflows; CLI reference) https://code.claude.com/docs/en/common-workflows and https://docs.anthropic.com/en/docs/claude-code/cli-reference.md

**PR linking**
- Creating a PR via `gh pr create` links the session; later resume with `claude --from-pr <number>`. (Common workflows) https://code.claude.com/docs/en/common-workflows

**Parallel work**
- Use git worktrees via `--worktree/-w` to isolate changes into separate directories/branches. (Common workflows) https://code.claude.com/docs/en/common-workflows

---

## Teaching Approaches

### Intuitive (no math): “Skills are macros for good agent behavior”
- A skill is a “macro” that bundles: *figure out what to do → do it → check it worked*.  
- CLI agents are powerful because the terminal already exposes almost every developer action (tests, linters, git, deploy), so skills can be expressed as sequences of terminal actions plus file edits.  
Ground in Claude Code’s recommended 4-phase workflow and verification emphasis. (Best practices) https://code.claude.com/docs/en/best-practices

### Technical (with metrics): “Skills reduce error by tightening feedback loops and shrinking attack surface”
- Reliability: verification loops (tests/linters) provide deterministic feedback; without them, the human is the only feedback loop. (Best practices) https://code.claude.com/docs/en/best-practices  
- Security: selecting minimal tools/skills before exposure to untrusted content can reduce prompt-injection success; AgentDojo’s tool filter yields **7.5%** targeted ASR. (AgentDojo) https://arxiv.org/abs/2406.13352  
- Operations: layered guardrails can compound false positives: \(1-a^n\). (Premai) https://blog.premai.io/production-llm-guardrails-nemo-guardrails-ai-llama-guard-compared/

### Analogy-based: “Skills are kitchen recipes; CLI agents are a fully stocked kitchen”
- Skill = recipe card (ingredients, steps, safety notes, how to tell it’s done).  
- Skill registry = recipe box.  
- Skill composition = multi-course meal plan.  
- Plan Mode = mise en place (prep without cooking).  
- Tests/linters = tasting/thermometer (verification).  
Maps to Claude Code Plan Mode + verification loop. https://code.claude.com/docs/en/common-workflows and https://code.claude.com/docs/en/best-practices

---

## Common Misconceptions

1) **“A skill is just a single tool call (like ‘run tests’).”**  
   - Why wrong: sources emphasize multi-step loops—explore/plan/implement/verify—and ReAct-style interleaving of reasoning and acting, not one-off actions. (Claude Code best practices; ReAct)  
   - Correct model: a skill is a *workflow chunk* that may call multiple tools and includes verification criteria.

2) **“Plan Mode is just ‘the model thinks harder’; it can still safely edit if needed.”**  
   - Why wrong: Claude Code Plan Mode is explicitly described as **read-only** behavior to force analysis and planning before edits. (Common workflows)  
   - Correct model: Plan Mode is a *permission/guardrail state*—use it to explore and propose a plan, then switch to implement.

3) **“If I keep chatting longer, the agent will get more accurate because it has more context.”**  
   - Why wrong: Claude Code best practices warn the context window fills fast (conversation + file reads + command outputs) and performance **degrades** as it fills (forgetting earlier instructions, more mistakes).  
   - Correct model: treat context as a limited resource; use `/clear` and compaction strategies to maintain performance. (Best practices) https://code.claude.com/docs/en/best-practices

4) **“Prompt injection is mainly a model problem; adding delimiters or more instructions should fix it.”**  
   - Why wrong: Willison stresses prompt injection is an attack on *applications built on top of models* via concatenated/untrusted text; “prompt begging” is not a robust fix. (Willison) https://simonwillison.net/2023/May/2/prompt-injection/  
   - Correct model: use defense-in-depth: tool restriction, detectors/guardrails, and careful handling of untrusted tool outputs (AgentDojo; AWS guardrails guidance).

5) **“The fastest way is to give the agent full permissions (bypass prompts) all the time.”**  
   - Why wrong: Claude Code provides multiple permission modes and explicit “dangerously skip permissions”; the existence of these modes reflects real risk trade-offs. (CLI reference)  
   - Correct model: start with least privilege; selectively relax via allowlists/Auto mode/sandboxing and checkpointing (Anthropic org workflow PDF emphasizes clean git state + checkpoint commits). https://www-cdn.anthropic.com/58284b19e702b49db9302d5b6f135ad8871e7658.pdf

---

## Worked Examples

### Example 1: A reusable “Bugfix skill” loop in Claude Code (Plan → Implement → Verify)

**Goal:** demonstrate a composable skill pattern you can reuse across repos.

1) **Start a session in Plan Mode (read-only)**
```bash
claude --permission-mode plan -n "bugfix: failing test in auth"
```
(Plan Mode flag: CLI reference; Plan Mode behavior: common workflows)

2) **Prompt template (forces success criteria + verification)**
Use best-practices prompting: specify files, constraints, and definition of done.
```
We have a failing test in the auth module. Please:
1) Explore and identify the failure cause (read-only).
2) Propose a minimal fix plan.
Constraints: follow existing code patterns; avoid mocks if possible.
Definition of fixed: all tests pass via the project’s normal test command.
```
(Best practices: specify scenario/constraints/testing prefs; verification loop)

3) **Switch to implementation (Normal Mode)**
- In-session: Shift+Tab to exit Plan Mode (common workflows).

4) **Run verification**
- Ask the agent to run the repo’s test command and iterate until green.  
Best practices explicitly recommend tests/linters as the feedback loop. https://code.claude.com/docs/en/best-practices

5) **If the session drifts / gets too long**
- Use `/compact <instructions>` or `/clear` between unrelated tasks. (Best practices)

**Tutor note:** This example is intentionally tool-agnostic about the exact test command because the sources emphasize *inspecting existing test files and conventions* rather than assuming a framework. (Common workflows: tests workflow)

---

### Example 2: Headless “skill invocation” via print mode + piped input (CLI agent as a Unix tool)

**Use case:** treat Claude Code like a CLI skill that transforms input into output.

1) Pipe a file into Claude Code print mode:
```bash
cat README.md | claude -p "Extract the installation steps as a numbered list."
```
(CLI reference: `cat file | claude -p "query"`)

2) Add cost/turn limits for safety in automation:
```bash
cat logs.txt | claude -p "Summarize errors and propose next debugging commands." \
  --max-turns 6 --max-budget-usd 0.50
```
(CLI reference: `--max-turns` no default limit; `--max-budget-usd`)

---

### Example 3: Restricting tool surface area (skill discovery + least privilege)

**Goal:** show how “skill discovery” maps to concrete CLI restrictions.

- Start Claude Code with restricted tools (conceptual example; exact tool names depend on Claude Code’s tool identifiers):
```bash
claude --tools "Bash,ReadFile,EditFile" --permission-mode default
```
Then optionally auto-allow a subset:
```bash
claude --allowedTools "ReadFile" --disallowedTools "Bash"
```
(Flags exist per CLI reference; the exact allowed tool strings are environment-specific.)

**Why this matters:** AgentDojo shows tool filtering can reduce targeted ASR to **7.5%** by limiting what an injected instruction can cause the agent to do. https://arxiv.org/abs/2406.13352

---

## Comparisons & Trade-offs

| Choice point | Option A | Option B | Trade-off / when to choose |
|---|---|---|---|
| Planning vs immediate edits | **Plan Mode** (read-only exploration + plan) | **Normal Mode** (edit/execute) | Use Plan Mode for multi-step or multi-file work and when requirements are unclear; switch to Normal for implementation. (Common workflows) |
| Permissions | Default prompting | `bypassPermissions` / `--dangerously-skip-permissions` | Faster autonomy vs higher risk; org workflow suggests pairing autonomy with clean git state + frequent checkpoint commits for rollback. (CLI reference; Anthropic org PDF) |
| Interactive vs automation | `claude` interactive | `claude -p` print mode | Interactive for iterative coding; print mode for scripts/CI-like “skill calls” with budgets/turn limits. (CLI reference) |
| Defense approach to injection | Tool restriction/filtering | Detector/guardrails | AgentDojo: tool filter can reduce ASR to 7.5% but fails when task tools also enable attack; detectors can reduce ASR further (~8% with added detector). (AgentDojo) |
| Layered guardrails | Many validators chained | Fewer, higher-quality checks | Premai shows false positives compound as \(1-a^n\); layer with early exit and latency tiers to manage cost/latency/FP. (Premai) |

---

## Prerequisite Connections

- **Tool-using agent loop (reason → act → observe)**: Needed to understand why skills are multi-step and composable (ReAct) https://arxiv.org/abs/2210.03629  
- **Planning / decomposition**: Skills often encode decomposition into subgoals and ordered steps (Weng planning module) https://lilianweng.github.io/posts/2023-06-23-agent/  
- **Verification via tests/linters**: Central to reliable CLI-agent coding workflows (Claude Code best practices) https://code.claude.com/docs/en/best-practices  
- **Prompt injection basics**: Needed to reason about skill discovery/tool restriction and untrusted tool outputs (Willison; AgentDojo) https://simonwillison.net/2023/May/2/prompt-injection/ and https://arxiv.org/abs/2406.13352

---

## Socratic Question Bank

1) **“If you had to turn your approach into a reusable skill, what are the explicit inputs, outputs, and ‘definition of done’?”**  
   - Good answer: names success criteria (tests pass, lint clean), identifies artifacts (files changed, PR), and constraints.

2) **“When would Plan Mode be strictly better than starting to edit immediately?”**  
   - Good answer: multi-file changes, unclear requirements, need to inspect conventions; references read-only planning.

3) **“What’s the smallest set of tools this task truly needs—and what could go wrong if we allow more?”**  
   - Good answer: least-privilege reasoning; connects to tool filtering reducing injection risk (AgentDojo).

4) **“What verification step would catch the most likely failure here?”**  
   - Good answer: proposes tests/linters/shell checks aligned with repo conventions (Claude Code best practices/common workflows).

5) **“How would you keep the agent effective over a long debugging session?”**  
   - Good answer: context window management (/clear, /compact), avoid dumping huge logs, checkpointing.

6) **“If an untrusted tool output contains instructions, why shouldn’t the agent follow them?”**  
   - Good answer: explains prompt injection as application-layer vulnerability (Willison) and suggests guardrails/tool restriction.

7) **“What’s your rollback strategy if the agent goes off track?”**  
   - Good answer: clean git state, frequent commits/checkpoints (Anthropic org PDF).

8) **“How would you run the same ‘skill’ in CI or a script?”**  
   - Good answer: uses `claude -p`, piping, and budgets/turn limits (CLI reference).

---

## Likely Student Questions

**Q: How do I start Claude Code in a safe read-only planning mode?**  
→ **A:** Use Plan Mode: `claude --permission-mode plan` (CLI reference). In-session, Shift+Tab cycles permission modes and Plan Mode shows “⏸ plan mode on” (common workflows).  
Sources: https://docs.anthropic.com/en/docs/claude-code/cli-reference.md and https://code.claude.com/docs/en/common-workflows

**Q: What’s the difference between `claude` and `claude -p`?**  
→ **A:** `claude` starts an interactive session; `claude -p "query"` runs in print mode (non-interactive) and exits; you can pipe input like `cat file | claude -p "query"`.  
Source: https://docs.anthropic.com/en/docs/claude-code/cli-reference.md

**Q: How do I resume a previous session, and how do I fork it?**  
→ **A:** `claude --continue` loads the most recent conversation in the current directory; `claude --resume <session>` resumes by ID/name (or opens a picker). Add `--fork-session` to create a new session ID when resuming/continuing.  
Source: https://docs.anthropic.com/en/docs/claude-code/cli-reference.md

**Q: What’s the single most important practice to make a coding agent reliable?**  
→ **A:** A verification loop: run tests/linters/shell checks so the agent can verify its own work; Claude Code best practices say Claude performs “dramatically better” when it can verify its work.  
Source: https://code.claude.com/docs/en/best-practices

**Q: Why does the agent get worse in long sessions?**  
→ **A:** Claude Code context includes the entire conversation plus every file read and every command output; it “fills up fast,” and performance degrades as it fills (forgetting earlier instructions, more mistakes). Use `/clear` between unrelated tasks and compaction/rewind tools.  
Source: https://code.claude.com/docs/en/best-practices

**Q: What permission modes exist, and what does “dangerously skip permissions” mean?**  
→ **A:** `--permission-mode {default,acceptEdits,plan,auto,dontAsk,bypassPermissions}`. `--dangerously-skip-permissions` is equivalent to `--permission-mode bypassPermissions`.  
Source: https://docs.anthropic.com/en/docs/claude-code/cli-reference.md

**Q: Is there evidence that restricting tools helps against prompt injection?**  
→ **A:** Yes. AgentDojo evaluates prompt injection in tool-using agents and reports a “tool filter” defense (pre-select minimal tools) achieving **7.5%** targeted ASR; it can fail when the same tools needed for the task also enable the attack (17% of cases).  
Source: https://arxiv.org/abs/2406.13352

**Q: If I add more guardrails, do I always get safer behavior?**  
→ **A:** Not necessarily—false positives can compound. A referenced formula: if each guard has accuracy \(a\) and you chain \(n\) guards, \(P(\ge 1 \text{ false positive}) = 1-a^n\). Example given: \(a=0.9, n=5\) yields 41% flagged.  
Source: https://blog.premai.io/production-llm-guardrails-nemo-guardrails-ai-llama-guard-compared/

---

## Available Resources

### Videos
- [AI Agents: Safety, Security, and Trust](https://youtube.com/watch?v=kJLiOGle3Lw) — Surface when: the student asks how to think about agent safety/guardrails beyond “just prompt it better,” especially for tool-using/CLI agents.
- [Software Is Changing (Again)](https://youtube.com/watch?v=LCEmiRjPEtQ) — Surface when: the student needs high-level motivation for agentic coding and why workflows are shifting toward more autonomous tools.

### Articles & Tutorials
- [LLM Powered Autonomous Agents (Weng, 2023)](https://lilianweng.github.io/posts/2023-06-23-agent/) — Surface when: the student needs the conceptual architecture (planning/memory/tools) to understand what “skills” are made of.
- [Prompt injection explained (Willison)](https://simonwillison.net/2023/May/2/prompt-injection/) — Surface when: the student confuses prompt injection as a “model bug” rather than an application/tooling vulnerability.
- [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/) — Surface when: the student asks for an industry taxonomy of LLM/agent risks (prompt injection, sensitive info disclosure, etc.).
- [NVIDIA NeMo Guardrails (GitHub)](https://github.com/NVIDIA/NeMo-Guardrails) — Surface when: the student asks how to implement programmable guardrails around an LLM app (topic steering, tool safety, dialog control).

---

## Visual Aids

![LLM-powered autonomous agent system overview with planning, memory, and tools. (Weng, 2023)](/api/wiki-images/agent-skills-safety/images/lilianweng-posts-2023-06-23-agent_001.png)  
Show when: the student asks “what are the components of an agent?” or “where do skills fit—planning, memory, or tools?”

![ReAct reasoning trajectories for knowledge and decision tasks. (Yao et al., 2023)](/api/wiki-images/agent-skills-safety/images/lilianweng-posts-2023-06-23-agent_002.png)  
Show when: the student asks how “reasoning + acting” interleave in practice, or why skills are naturally multi-step.

---

## Key Sources

- [Claude Code Best Practices (Agentic Coding Loop)](https://code.claude.com/docs/en/best-practices) — Primary operational guidance for planning vs implementing, verification loops, and context management in CLI coding agents.
- [Claude Code CLI reference](https://docs.anthropic.com/en/docs/claude-code/cli-reference.md) — Authoritative command/flag behaviors for sessions, permission modes, tool restrictions, and automation controls.
- [Claude Code Common Workflows](https://code.claude.com/docs/en/common-workflows) — End-to-end workflows: Plan Mode, tests, PR linking, sessions, and worktrees.
- [AgentDojo benchmark (arXiv)](https://arxiv.org/abs/2406.13352) — Concrete evaluation framework and numbers for prompt injection in tool-using agents; includes tool-filter defense results.
- [LLM Powered Autonomous Agents (Weng, 2023)](https://lilianweng.github.io/posts/2023-06-23-agent/) — Conceptual scaffolding for planning/memory/tool use that underlies “skills” and their composition.