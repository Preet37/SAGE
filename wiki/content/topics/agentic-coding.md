---
title: "Agentic Coding"
subject: "Agents & Reasoning"
date: 2026-04-09
tags:
  - "subject/agents-and-reasoning"
  - "level/intermediate"
  - "educator/andrej-karpathy"
  - "educator/simon-willison"
  - "educator/anthropic"
  - "resource/video"
  - "resource/blog"
  - "resource/deep-dive"
  - "resource/paper"
  - "resource/code"
educators:
  - "Andrej Karpathy"
  - "Simon Willison"
  - "Anthropic"
levels:
  - "intermediate"
resources:
  - "video"
  - "blog"
  - "deep-dive"
  - "paper"
  - "code"
---

# Agentic Coding

## Video (best)
- **Andrej Karpathy** — "Software Is Changing (Again)"
- **Watch:** [YouTube](https://www.youtube.com/watch?v=LCEmiRjPEtQ)
- Why: Clear, high-level framing of LLM-driven software development and the shift toward more autonomous/agentic tooling; good conceptual grounding before diving into specific coding agents and workflows.
- Level: Beginner → Intermediate

## Blog / Written explainer (best)
- **Simon Willison** — "Prompt injection explained"
- **Link:** [https://simonwillison.net/2023/Nov/27/prompt-injection-explained/](https://simonwillison.net/2023/Nov/27/prompt-injection-explained/)
- Why: Essential security and workflow context for agentic coding (tool use, untrusted context, and how “instructions” can be subverted), which directly impacts rules files, context management, and agent-human collaboration.
- Level: Intermediate

## Deep dive
- **Anthropic** — "Building effective agents" [VERIFY]
- url: https://www.anthropic.com/research/building-effective-agents [VERIFY]
- Why: Practical patterns for agent design (task decomposition, tool use, feedback loops) that map well to agentic workflows like iterative debugging, multi-step prompt-to-code, and context management.
- Level: Intermediate → Advanced

## Original paper
- **Yao et al. (2022)** — "ReAct: Synergizing Reasoning and Acting in Language Models"
- **Link:** [https://arxiv.org/abs/2210.03629](https://arxiv.org/abs/2210.03629)
- Why: Foundational approach for agentic behavior (interleaving reasoning and tool actions) that underpins many modern coding-agent workflows.
- Level: Intermediate → Advanced

## Code walkthrough
- **OpenAI Cookbook** — "Function calling" examples
- **Link:** [https://cookbook.openai.com/](https://cookbook.openai.com/)
- Why: Concrete, runnable patterns for tool/function calling that are directly applicable to coding agents (planning → tool invocation → result integration), and a good base for building prompt-to-code and iterative debugging loops.
- Level: Intermediate

## Coverage notes
- Strong: High-level motivation for agentic coding; foundational agent pattern (ReAct); practical tool-calling patterns; security considerations relevant to context/rules.
- Weak: Specific IDE agent products (Claude Code, Cursor, Windsurf, GitHub Copilot) and their exact feature sets change rapidly and are not covered deeply by the above evergreen resources.
- Gap: A stable, vendor-neutral “agents.md / rules files” best-practices spec and a canonical, long-lived multi-file refactor walkthrough using a modern coding agent in a real repo.

---

## Additional Resources for Tutor Depth

> **9 sources** — papers, official docs, working code, benchmarks, and deep explainers that give the AI tutor precision on this topic.

### 📄 Toolformer — self-supervised tool/API call insertion via likelihood filtering
**Paper** · [source](https://arxiv.org/abs/2302.04761)

*Toolformer’s self-supervised procedure: generate candidate API calls, execute, filter by future-token loss improvement, finetune on augmented text.*

<details>
<summary>Key content</summary>

- **Goal (Section 1–2):** Train LM \(M\) to decide **which API**, **when**, **arguments**, and **how to use results** in next-token prediction; requires only a **handful of demonstrations per API**.
- **Pipeline (Figure 2, Section 2):**
  1) **Sample API calls**: prompt \(P(\mathbf{x})\) to annotate plain text \(\mathbf{x}=x_{1:n}\) with candidate calls at position \(i\).  
  2) **Execute** calls to obtain results \(r_i\).  
  3) **Filter** calls by whether they improve predicting future tokens; **merge** surviving calls across tools; **finetune** on augmented corpus \(\mathcal{C}^*\).
- **Filtering objective (Section 2):** Weighted cross-entropy loss over future tokens:
  \[
  L_i(\mathbf{z})=-\sum_{j=i}^{n} w_{j-i}\log p_M(x_j\mid \mathbf{z},x_{1:j-1})
  \]
  Define:
  \[
  L_i^{+}=L_i(e(c_i,r_i)),\quad
  L_i^{-}=\min\big(L_i(\varepsilon),\,L_i(e(c_i,\varepsilon))\big)
  \]
  **Keep call** if:
  \[
  L_i^{-}-L_i^{+}\ge \tau_f
  \]
  where \(e(\cdot)\) inserts call+result text; \(\varepsilon\)=empty; \(\tau_f\)=tool-specific threshold.
- **Weighting (Section 4.1):** \(\tilde w_t=\max(0,1-0.2t)\), \(w_t=\tilde w_t/\sum_s \tilde w_s\) (encourages calls near where useful).
- **Finetuning (Section 4.1):** batch size **128**, LR **\(1\times10^{-5}\)**, **linear warmup 10%**.
- **Tools (Section 3):** QA (Atlas), Wikipedia search, calculator, calendar (current date), translation (NLLB 600M + fastText language ID).
- **Empirical highlights (Section 4.2):**
  - **LAMA:** Toolformer improves over best same-size baseline by **+11.7 / +5.2 / +18.6** points (SQuAD / Google-RE / T-REx subsets); uses QA tool **98.1%** of cases.
  - **Math (ASDiv/SVAMP/MAWPS):** enabling API calls **more than doubles** performance; calculator used **97.9%** of examples.
  - **Scaling (Section 4.4):** effective tool use emerges around **775M** parameters (GPT-2 family); smaller models show little gain.

</details>

### 📊 RACE-bench (Reasoning-Augmented Repo-Level Code Agent Eval)
**Benchmark** · [source](https://arxiv.org/html/2603.26337v1)

*Repository-level agent evaluation protocol for feature addition with dual-track (patch + reasoning) metrics*

<details>
<summary>Key content</summary>

- **Benchmark scope/design (Sec. 2.1):** RACE-bench = **528** real-world **feature addition** instances from **12** OSS Python repos. Each instance includes: **Task Context** (issue text + env setup + optional hints), **Reasoning Ground Truth** (4 stages / **5 modules**), and **Verification** (tests + gold/test patches).
- **Verification protocol (Sec. 2.1, 2.2.2):** Uses **Fail-to-Pass (FTP)** tests (fail on base commit, pass after gold patch) + **Pass-to-Pass (PTP)** tests (regression preservation). Patches applied via `git apply`; tests run with **pytest** in per-instance Docker.
- **Reasoning Ground Truth construction (Sec. 2.2.3):**
  - Issue Understanding: DeepSeek generates **Concept Explanations** + **Goal Expectation** (behavior-only; no code details).
  - File Localization: derive from gold/test patches; **ablation** per modified file—remove file’s changes, rerun tests → label **Necessary Code File** if tests fail; else **Other File**; test patch files = **Test Files**.
  - Issue Implementation: static parse gold patch to extract changed **functions/methods** (classes treated as containers); annotate purpose + **is_necessary** using FTP tests.
  - Step Decomposition: minimal ordered steps from closed taxonomy: *introduce new capability; reuse existing semantics; change existing semantics; deprecate/replace behavior; enforce constraints/edge cases*.
- **Dual-track evaluation (Sec. 2.3–2.4):**
  - Patch metrics: **Resolved Rate** = % instances passing **FTP+PTP** on **first attempt**; **Patch Apply Rate** = % patches that apply cleanly.
  - Reasoning metrics (Table 1): Recall/OverPrediction for files/tasks/steps; **Score@GoalExpectation** (10-pt LLM judge); concept recall/accuracy.
- **Key empirical results (Sec. 4.1 Table 2):**
  - AutoCodeRover: **Apply 96.21% (508/528)**, **Resolved 28.79% (152/528)**
  - TraeAgent: **Apply 78.98% (417/528)**, **Resolved 52.65% (278/528)**
  - mini-SWE-Agent: **Apply 95.83% (506/528)**, **Resolved 70.08% (370/528)**
- **Reasoning findings (Sec. 4.2):** High intent understanding (**Score@Goal ~9.2–9.6/10**) but “waterfall” drop from file→task→step recall (e.g., mini-SWE-Agent **Recall@Files 0.890 → Recall@Tasks 0.751 → Recall@Steps 0.445**). Apply-success/test-fail cases: **35.7% recall decrease** and **94.1% over-prediction increase** vs successes.
- **Defaults/params (Sec. 3.2):** single run per instance; **temperature=0**, **top_p=1**; max tokens **4096** (agent) / **8192** (summarizer).

</details>

### 📊 RepoBench — repository-level code completion benchmark
**Benchmark** · [source](https://proceedings.iclr.cc/paper_files/paper/2024/file/d191ba4c8923ed8fd8935b7c98658b5f-Paper-Conference.pdf)

*RepoBench task suite (RepoBench-R retrieval, RepoBench-C completion, RepoBench-P pipeline) + multi-file evaluation protocol*

<details>
<summary>Key content</summary>

- **Motivation (Sec. 1):** Prior benchmarks are mostly single-file; RepoBench targets **repository-level** (multi-file) auto-completion with explicit cross-file context.
- **Data (Sec. 3.1–3.2):**
  - Train source: `github-code` (cutoff **Mar 16, 2022**); select repos with **32–128** Python/Java files.
  - Test source: newly crawled non-fork GitHub repos created **Feb 9, 2023–Aug 3, 2023** (to reduce leakage).
  - Parsed with **tree-sitter** focusing on **import statements** → identify cross-file modules, “cross-file lines,” and defining snippets.
  - Sizes: training repos **10,345 Python / 14,956 Java**; test repos **1,075 Python / 594 Java**.
- **Task settings (Sec. 3.3):**  
  - **XF-F:** mask *first* cross-file line (hardest). **XF-R:** mask random non-first cross-file line. **IF:** mask in-file line (no cross-file module).
- **Prompt construction (Fig. 1, App. A):** cross-file snippets (commented, with path) + in-file context (path + imports + preceding lines). Default in RepoBench-C: **max 30 preceding lines**.
- **RepoBench-R retrieval (Sec. 3.3, 4.1):**
  - Retrieval objective: top‑k by similarity  
    \[
    \arg\max_{i\in\{1..n\}}^{k} f(C[-m:], S_i)
    \]
    where \(C\)=in-file code, \(S_i\)=candidate snippet, \(n\)=#candidates, \(m\)=kept preceding lines (**baseline m=3**), \(f\)=similarity.
  - Candidates: Easy **5–9**, Hard **≥10**. Metric: **acc@k** (Easy: @1,@3; Hard: @1,@3,@5).
  - Key results (Table 2, Hard/Python acc@1): **InstructOR 19.10**, **UniXcoder 18.48**, **Jaccard 10.47**, Random **6.43**. (Easy/Python acc@1: InstructOR **28.22**, UniXcoder **27.09**.)
- **RepoBench-C completion (Sec. 3.3, 4.2):**
  - Autoregressive next-line probability (Eq. 1):  
    \[
    P(Y)=\prod_{i=1}^{n} P(y_i \mid y_{<i}, C_x, C_{in})
    \]
    \(C_x\)=cross-file context, \(C_{in}\)=in-file context.
  - Subsets: **2k** prompts ≤ **1,925 tokens** (for 2,048 limit); **8k** prompts ≤ **7,685 tokens**.
  - Metrics: **Exact Match (EM)**, **Edit Similarity**, **CodeBLEU**.
  - Key results (Table 3, 2k/Python EM): **CodeLlama‑34B 37.40** (best); Codex **31.31**. (2k/Java EM: Codex **42.47** best; CodeLlama‑34B **39.41**.)
- **RepoBench-P pipeline (Sec. 4.3):**
  - Pipeline probability (Eq. 2):  
    \[
    P(Y)=\prod_{i=1}^{n} P(y_i \mid y_{<i}, S_1..S_k, C_{in})
    \]
  - Constraints: minimum prompt tokens **12k (Python)** / **24k (Java)**; retrieval requires **≥10 candidates**.
  - Codex baseline config: reserve **1,600 tokens** for in-file; crop **60** preceding lines; fill to **6,400 tokens** with cross-file snippets.
  - Key result (Table 4, Python EM): in-file-only baseline **33.15** vs **Jaccard 36.46** vs **UniXcoder-L2H 37.11**; even **Random 34.94** improves → cross-file context helps; snippet **ordering matters** (higher-similarity nearer completion helps).

</details>

### 📊 SWE-bench Verified (human-validated SWE-bench subset)
**Benchmark** · [source](https://openai.com/index/introducing-swe-bench-verified/)

*Defines SWE-bench Verified (500 human-filtered SWE-bench instances) and reports verified performance comparisons + rationale for filtering.*

<details>
<summary>Key content</summary>

- **What SWE-bench evaluates (workflow):**
  - Input to agent: **GitHub issue text (“problem statement”) + repository codebase**; **tests are hidden**.
  - Output: a **patch** (multi-file edits allowed) intended to fix the issue.
  - Scoring requires **both**:
    - `FAIL_TO_PASS` tests: **fail before** PR solution, **pass after**; passing implies the issue is solved.
    - `PASS_TO_PASS` tests: pass before/after; passing implies no regressions.
- **Why Verified was created (design rationale):** Original SWE-bench can **systematically underestimate** capability due to:
  1) overly specific / unrelated unit tests rejecting valid solutions,  
  2) underspecified issue descriptions,  
  3) unreliable environment setup causing failures independent of solution.
- **SWE-bench Verified definition & construction (procedure):**
  - Human annotation campaign: **93 Python-experienced developers**.
  - Annotated **1,699 random SWE-bench test samples**; **each sample labeled 3×**.
  - Two main criteria labeled on **severity scale {0,1,2,3}**: underspecification; unfair `FAIL_TO_PASS` tests.
  - **Ensembling rule:** take **max severity** across 3 annotators.
  - **Filter rule:** discard any sample where either criterion has **ensemble ≥ 2**, or “other major issues” flagged.
  - Final dataset: **500 non-problematic samples**; includes difficulty slicing from released annotations: **easy = 196 (<15 min)**, **hard = 45 (>1 hr)**.
- **Key empirical results:**
  - **68.3%** of SWE-bench samples filtered out (underspecification, unfair tests, or other issues).
  - Flag rates: **38.3%** underspecified problem statements; **61.1%** unfair unit tests.
  - Difficulty estimate (original SWE-bench, from 1,699-sample estimate): **77.8%** of samples **< 1 hour**.
  - Performance: **GPT‑4o = 33.2%** solve rate on **SWE-bench Verified** (model `gpt-4o-2024-05-13`); vs **16%** on original SWE-bench (best scaffold reported).  
  - Scaffold sensitivity example (SWE-bench Lite): **GPT‑4 ranges 2.7% → 28.3%** depending on scaffold (early RAG vs CodeR).
- **Evaluation reliability improvement:** new **Docker/containerized harness** for easier, more reliable evaluation.

</details>

### 📖 Claude Code Best Practices (Agentic Coding Loop)
**Reference Doc** · [source](https://code.claude.com/docs/en/best-practices)

*Actionable agent loop guidance: task decomposition, iterative verification (tests/linters), safe tool use patterns, and prompt templates*

<details>
<summary>Key content</summary>

- **Core constraint (Context Window):** Claude’s context includes *entire conversation + every file read + every command output*; it “fills up fast” (debugging/exploration can consume **tens of thousands of tokens**) and **performance degrades** as it fills (forgetting earlier instructions, more mistakes). Track via **custom status line**; reduce via token-usage strategies.
- **Verification loop (must-have):** Claude performs “dramatically better” when it can **verify its own work** (run **tests**, **linters**, Bash checks, compare screenshots/UI). Without success criteria, the human becomes the only feedback loop. Prefer: *write failing test → fix → rerun tests*.
- **Recommended workflow (4 phases):**  
  1) **Explore** in **Plan Mode** (read files, answer questions; no changes).  
  2) **Plan**: produce detailed implementation plan; **Ctrl+G** opens plan in editor for human edits.  
  3) **Implement** in Normal Mode; verify against plan.  
  4) Iterate with verification.  
  **Skip planning** for tiny diffs (“describe the diff in one sentence”: typo/log/rename).
- **Prompting procedures (concrete patterns):** specify **file(s)**, scenario, constraints, and testing prefs (e.g., “edge case logged out; avoid mocks”); point to sources (git history); reference existing code patterns; describe symptom + likely location + definition of fixed.
- **Persistent rules (CLAUDE.md):** loaded at start of every convo; keep **short**. Include: non-obvious Bash commands, style deviations, test runners, repo etiquette, architecture decisions, env quirks, gotchas. Exclude: things Claude can infer, long tutorials, file-by-file descriptions. Locations: `~/.claude/CLAUDE.md`, `./CLAUDE.md`, `./CLAUDE.local.md` (gitignored); parent dirs auto-included; child dirs loaded on demand.
- **Safety/automation defaults:** permissions prompt by default; reduce via **Auto mode** (classifier blocks risky actions), **allowlists**, or **sandboxing**. Use **hooks** for deterministic steps (e.g., run eslint after every edit; block writes to migrations).
- **Context management commands:** `/clear` between unrelated tasks; `/compact <instructions>`; `/rewind` or **Esc+Esc** to restore/summarize; **Esc** stops mid-action. After **two failed correction cycles**, `/clear` and rewrite prompt.

</details>

### 📖 Claude Code CLI surface (commands + flags)
**Reference Doc** · [source](https://docs.anthropic.com/en/docs/claude-code/cli-reference.md)

*Complete Claude Code CLI command/flag surface (sessions `-c`/`-r`, MCP via `claude mcp`, print mode `-p`, etc.)*

<details>
<summary>Key content</summary>

- **Doc index lookup (important):** fetch full documentation index at `https://code.claude.com/docs/llms.txt` to discover all pages.
- **Feedback endpoint:** POST `https://code.claude.com/docs/_mintlify/feedback/claude-code/agent-feedback` with JSON `{ "path": "/current-page-path", "feedback": "..." }`.
- **Core session commands**
  - Start interactive: `claude` or `claude "query"`.
  - Print/SDK then exit: `claude -p "query"`; pipe: `cat file | claude -p "query"`.
  - Continue most recent convo (cwd): `claude -c` / `claude --continue`; also `claude -c -p "query"`.
  - Resume by **ID or name**: `claude -r <id|name> "query"` or `claude --resume <id|name>` (picker if omitted).
  - Name session: `claude -n "my-feature-work"`; resume named session with `--resume`.
  - Fork on resume: `--fork-session` (with `--resume`/`--continue`).
- **Auth & updates:** `claude update`; `claude auth login [--email] [--sso] [--console]`; `claude auth status` (JSON; `--text`; exit code **0 logged in / 1 not**); `claude auth logout`; `claude setup-token` (prints long-lived OAuth token).
- **MCP / plugins / remote control**
  - MCP config: `claude mcp`; load via `--mcp-config` (JSON file/string); `--strict-mcp-config` ignores other MCP configs.
  - Plugins: `claude plugin` (alias `claude plugins`); `--plugin-dir` repeatable.
  - Remote control server: `claude remote-control`; interactive RC: `claude --remote-control` / `--rc`; name prefix flag `--remote-control-session-name-prefix` (env: `CLAUDE_REMOTE_CONTROL_SESSION_NAME_PREFIX`).
- **Permission/tooling controls**
  - Permission modes: `--permission-mode {default,acceptEdits,plan,auto,dontAsk,bypassPermissions}`; `--dangerously-skip-permissions` == bypassPermissions; `--allow-dangerously-skip-permissions` adds bypass to mode cycle.
  - Tool allow/deny: `--tools` (restrict available tools), `--allowedTools` (auto-allow patterns), `--disallowedTools` (remove tools).
- **Print-mode I/O & limits:** `--output-format {text,json,stream-json}`; `--input-format {text,stream-json}`; `--max-turns N`; `--max-budget-usd X`; `--no-session-persistence`; `--json-schema <schema>`.
- **System prompt flags (rationale):** prefer **append** to preserve built-ins.
  - Replace: `--system-prompt` XOR `--system-prompt-file`.
  - Append: `--append-system-prompt`, `--append-system-prompt-file` (can combine with replacement).
- **Other notable defaults/notes:** `claude --help` is **not exhaustive** for flags; `--bare` skips auto-discovery (hooks/skills/plugins/MCP/auto memory/CLAUDE.md) and sets env `CLAUDE_CODE_SIMPLE`.

</details>

### 📖 Claude Code Common Workflows (Plan Mode, tests, PRs, sessions, worktrees)
**Reference Doc** · [source](https://code.claude.com/docs/en/common-workflows)

*End-to-end agentic coding workflows + concrete prompt/session management patterns*

<details>
<summary>Key content</summary>

- **Plan Mode (safe analysis, read-only planning)**
  - **When to use:** multi-step implementations (many files), deep code exploration before edits, interactive iteration on direction.
  - **How to enable (in-session):** `Shift+Tab` cycles permission modes: **Normal → Auto-Accept → Plan Mode**. Plan Mode indicator: “⏸ plan mode on”.
  - **Start in Plan Mode (CLI):** `claude --permission-mode plan` (also `-p` in headless mode).
  - **Rationale:** forces read-only operations while Claude analyzes and proposes a plan; uses `AskUserQuestion` to clarify requirements before planning.
- **Tests workflow**
  - Ask for tests with **specific behaviors** to verify.
  - Claude should **inspect existing test files** to match project conventions (framework, assertion style).
  - Prompt for **edge cases**: error conditions, boundary values, unexpected inputs.
- **Pull request workflow**
  - You can ask directly: “create a pr for my changes”, or guide step-by-step using `gh pr create`.
  - **Session ↔ PR linking:** creating a PR via `gh pr create` automatically links the session; resume later with `claude --from-pr <number>`.
- **Session management (resume/organize)**
  - Resume: `claude --continue` (most recent in current dir), `claude --resume` (picker), `claude --from-pr 123`, in-session `/resume`.
  - Sessions stored **per project directory**; picker spans same git repo incl. worktrees.
  - Naming: start with `-n` or rename via `:/rename`; picker rename shortcut `R`.
- **Parallel work with Git worktrees**
  - Create isolated worktree session: `--worktree` (`-w`); creates `<repo>/.claude/worktrees/<name>` and branch `worktree-<name>` from `origin/HEAD`.
  - Update base ref if needed: `git remote set-head origin your-branch-name`.
  - Cleanup rules: **no changes → auto-remove**; **changes/commits → prompt keep/remove**.
  - Copy gitignored env/config into worktrees via `.worktreeinclude` (gitignore syntax; only matches files that are also gitignored).

</details>

### 🔍 How Anthropic teams use Claude Code — org workflows & constraints
**Explainer** · [source](https://www-cdn.anthropic.com/58284b19e702b49db9302d5b6f135ad8871e7658.pdf)

*Real organizational usage patterns + operational workflow details for Claude Code in team settings*

<details>
<summary>Key content</summary>

- **Workflow patterns (repeatable procedures)**
  - **Checkpoint-heavy autonomy loop (Product Dev/RL Eng):** start from **clean git state** → enable **auto-accept mode (Shift+Tab)** → let Claude write code/run tests/iterate → **commit checkpoints regularly** for easy rollback if it goes off track.
  - **Task classification heuristic:** use async autonomy for **peripheral/prototyping/edge features**; use synchronous supervision for **core business logic/critical fixes** (monitor architecture/style in real time).
  - **“Try one-shot, then collaborate” (RL Eng):** let Claude attempt full implementation first; if it fails, switch to guided iteration.
  - **End-of-session doc loop (Data Infra):** ask Claude to **summarize session + suggest improvements** → update **Claude.md** continuously based on real usage.
  - **Parallel instances:** run multiple Claude Code instances in different repos; each maintains context across **hours/days** for parallel workstreams.
- **Integration touchpoints**
  - **GitHub Actions:** Claude can address PR comments (e.g., formatting/renames) automatically.
  - **MCP servers (security control):** Data Infra recommends **MCP servers instead of BigQuery CLI** for sensitive data access control/logging.
  - **Screenshots/images:** used for **Kubernetes debugging** (dashboard screenshots) and **design-to-prototype** (paste mockups via **Cmd+V**).
- **Empirical results (numbers)**
  - Product Dev: **~70%** of Vim mode implementation came from autonomous Claude work.
  - Security Eng: incident code-scanning reduced **10–15 min → ~5 min**.
  - Inference: ML research time reduced by **~80%** (**~60 min → 10–20 min**).
  - Data Sci/Vis: built **~5,000-line** TypeScript app; reports **2–4×** time savings on refactors.
  - Growth Marketing: ad copy creation **2 hours → 15 min**; **10×** creative output; constraints: **30-char headlines**, **90-char descriptions**; Figma plugin generates **up to 100** variations per batch.
  - Product Design: Figma + Claude Code open **~80%** of time; execution **2–3× faster**; messaging project reduced **~1 week → two 30-min calls**.
  - RL Eng: one-shot success **~1/3** of the time.

</details>

### 🔍 Measuring GitHub Copilot’s Impact on Productivity (telemetry + survey)
**Explainer** · [source](https://cacm.acm.org/research/measuring-github-copilots-impact-on-productivity/)

*Measured productivity impacts + how Copilot usage telemetry relates to perceived productivity (ACM CACM write-up; DOI:10.1145/3633453)*

<details>
<summary>Key content</summary>

- **Study design (survey + telemetry, 2022 preview):**
  - Survey emailed to **17,420** preview users; **2,047** responses matched to IDE telemetry.
  - Focus period: **4 weeks** leading up to survey completion (most responses within first **2 days**, on/before **Feb 12, 2022**).
  - Survey built on **SPACE**; used **S, P, C, E** (excluded self-reported Activity). Aggregate productivity = **mean of 12 measures** (11 SPACE statements + “I am more productive…”), excluding skipped items.
- **Telemetry event funnel (Table 1):** `opportunity`, `shown`, `accepted`, `accepted_char`, `mostly_unchanged_X` (Levenshtein distance < **33%**) at **X ∈ {30,120,300,600}s**, `unchanged_X` at same X, and `(active) hour`.
- **Core metric formulas (Table 2; “X_per_Y” normalization):**
  - **Acceptance rate** = `accepted_per_shown` = (# accepted completions) / (# shown completions).
  - **Shown rate** = `shown_per_opportunity`.
  - **Acceptance frequency** = `accepted_per_active_hour`.
  - **Contribution speed** = `accepted_char_per_active_hour`.
  - **Persistence rate** = `unchanged_X_per_accepted`; **Fuzzy persistence** = `mostly_unchanged_X_per_accepted`.
- **Key empirical findings:**
  - **Acceptance rate is the strongest positive predictor of perceived productivity**, outperforming persistence-based metrics.
  - PLS regression: **Component 1 explains 43.2%** of variance; **Component 2 explains 21.2%**; both draw strongly from acceptance rate.
- **Controlled experiment (speed):** **95** pro developers, JS HTTP server task.
  - Completion success: **78% (Copilot)** vs **70% (control)**.
  - Time: **1h11m (Copilot)** vs **2h41m (control)** ⇒ **55% faster**; *P* = **.0017**; 95% CI **[21%, 89%]**.

</details>

---

## Related Topics

- [[topics/agent-fundamentals|Agent Fundamentals]]
- [[topics/agent-skills-safety|Agent Skills & Safety]]
- [[topics/mcp-tool-ecosystem|Model Context Protocol]]
- [[topics/prompting|Prompting]]
- [[topics/system-prompts|System Prompts]]
