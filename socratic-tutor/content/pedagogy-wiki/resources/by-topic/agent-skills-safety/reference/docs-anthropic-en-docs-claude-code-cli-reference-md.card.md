# Card: Claude Code CLI command/flag reference
**Source:** https://docs.anthropic.com/en/docs/claude-code/cli-reference.md  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Complete Claude Code CLI commands + flags (exact behaviors/defaults)

## Key Content
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

## When to surface
Use when students ask how to invoke Claude Code non-interactively, resume sessions, enforce least-privilege tool access/permission modes, control cost/turn limits, or customize/optimize system prompts and startup latency.