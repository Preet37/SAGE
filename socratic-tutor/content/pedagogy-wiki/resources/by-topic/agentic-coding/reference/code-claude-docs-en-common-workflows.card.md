# Card: Claude Code Common Workflows (Plan Mode, tests, PRs, sessions, worktrees)
**Source:** https://code.claude.com/docs/en/common-workflows  
**Role:** reference_doc | **Need:** WORKING_EXAMPLE  
**Anchor:** End-to-end agentic coding workflows + concrete prompt/session management patterns

## Key Content
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

## When to surface
Use when students ask how to safely explore/refactor with an agent (Plan Mode), add tests/edge cases, create/resume PR-linked sessions, or run parallel agent work without file conflicts (worktrees).