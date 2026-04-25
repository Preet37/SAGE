# Card: Claude Code CLI surface (commands + flags)
**Source:** https://docs.anthropic.com/en/docs/claude-code/cli-reference.md  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Complete Claude Code CLI command/flag surface (sessions `-c`/`-r`, MCP via `claude mcp`, print mode `-p`, etc.)

## Key Content
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

## When to surface
Use when students ask “which Claude Code CLI flag/command do I use for X?”—especially session continuation/resume, print-mode scripting, permission/tool restrictions, MCP/plugin configuration, or system-prompt customization.