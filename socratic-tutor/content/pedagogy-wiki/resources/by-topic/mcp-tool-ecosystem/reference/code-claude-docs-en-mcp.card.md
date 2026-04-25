# Card: Claude Code ↔ MCP integration & deployment patterns
**Source:** https://code.claude.com/docs/en/mcp  
**Role:** reference_doc | **Need:** DEPLOYMENT_CASE  
**Anchor:** Real integration topology + configuration/ops constraints for connecting Claude Code (MCP client) to MCP servers (HTTP/SSE/stdio), incl. auth, scopes, governance, and output/tool-search limits.

## Key Content
- **MCP server transport options (recommended order):**
  - **Remote HTTP** (recommended for remote/cloud services; most widely supported)
  - **Remote SSE**
  - **Local stdio** (runs local process; best for direct system access/custom scripts)
- **CLI ordering rule (critical):** options `--transport`, `--env`, `--scope`, `--header` **must come before** the server name; use `--` to separate server name from command/args passed to server.  
  - Example: `claude mcp add --transport stdio myserver -- npx server`  
  - Example: `claude mcp add --transport stdio --env KEY=value myserver -- python server.py --port 8080`
- **Dynamic capability refresh:** supports `list_changed` notifications → tools/prompts/resources refresh without reconnect.
- **Channels (push into session):** server declares `claude/channel`; client opts in with `--channels` at startup.
- **Scopes & precedence:** local (default, private; stored in `~/.claude.json` under project path) vs **project** (team-shared `.mcp.json` at repo root) vs **user** (`~/.claude.json`, cross-project). **Precedence:** local > project > user. Local overrides Claude.ai connector entries.
- **`.mcp.json` env expansion:** `${VAR}` and `${VAR:-default}` supported in `command`, `args`, `env`, `url`, `headers`.
- **OAuth specifics:** default callback uses random port; fix with `--callback-port` for pre-registered redirect `http://localhost:PORT/callback`. If no Dynamic Client Registration, use `--client-id` + `--client-secret` (masked prompt). Override discovery via `oauth.authServerMetadataUrl` (requires Claude Code **v2.1.64+**).
- **Custom auth headers:** `headersHelper` runs shell command (10s timeout) returning JSON headers; dynamic overrides static. Env vars: `CLAUDE_CODE_MCP_SERVER_NAME`, `CLAUDE_CODE_MCP_SERVER_URL`. Runs only after workspace trust (project/local scope).
- **Output limits:** warn at **10,000 tokens**; default max **25,000 tokens**; configurable via `MAX_MCP_OUTPUT_TOKENS`. Per-tool override via `_meta["anthropic/maxResultSizeChars"]` up to **500,000 chars**.
- **Tool Search:** enabled by default (defer schemas; load on demand). If `ANTHROPIC_BASE_URL` is non-first-party, tool search disabled by default unless `ENABLE_TOOL_SEARCH` set. Values: unset / `true` / `auto` / `auto:<N>` (0–100%) / `false`. Requires models supporting `tool_reference` (Sonnet 4+, Opus 4+; Haiku unsupported).
- **Org governance:** exclusive `managed-mcp.json` (system paths: macOS `/Library/Application Support/ClaudeCode/managed-mcp.json`; Linux/WSL `/etc/claude-code/managed-mcp.json`; Windows `C:\Program Files\ClaudeCode\managed-mcp.json`). Or allow/deny lists (`allowedMcpServers`, `deniedMcpServers`) matching by `serverName`, exact `serverCommand` array, or wildcard `serverUrl` patterns; **denylist overrides allowlist**.

## When to surface
Use for questions about configuring/operating MCP servers in Claude Code: transport choice, CLI syntax, scopes/precedence, OAuth/auth headers, output/tool-search limits, channels, and enterprise-managed policies.