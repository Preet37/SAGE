# Source: https://code.claude.com/docs/en/common-workflows
# Title: Common workflows - Claude Code Docs
# Fetched via: trafilatura
# Date: 2026-04-09

[Best practices](/docs/en/best-practices).
Understand new codebases
Get a quick codebase overview
Suppose you’ve just joined a new project and need to understand its structure quickly.Find relevant code
Suppose you need to locate code related to a specific feature or functionality.Fix bugs efficiently
Suppose you’ve encountered an error message and need to find and fix its source.Refactor code
Suppose you need to update old code to use modern patterns and practices.Use specialized subagents
Suppose you want to use specialized AI subagents to handle specific tasks more effectively.Use subagents automatically
Claude Code automatically delegates appropriate tasks to specialized subagents:
Create custom subagents for your workflow
- A unique identifier that describes the subagent’s purpose (for example,
code-reviewer
,api-designer
). - When Claude should use this agent
- Which tools it can access
- A system prompt describing the agent’s role and behavior
Use Plan Mode for safe code analysis
Plan Mode instructs Claude to create a plan by analyzing the codebase with read-only operations, perfect for exploring codebases, planning complex changes, or reviewing code safely. In Plan Mode, Claude uses[to gather requirements and clarify your goals before proposing a plan.](/docs/en/tools-reference)
AskUserQuestion
When to use Plan Mode
- Multi-step implementation: When your feature requires making edits to many files
- Code exploration: When you want to research the codebase thoroughly before changing anything
- Interactive development: When you want to iterate on the direction with Claude
How to use Plan Mode
Turn on Plan Mode during a session You can switch into Plan Mode during a session using Shift+Tab to cycle through permission modes. If you are in Normal Mode, Shift+Tab first switches into Auto-Accept Mode, indicated by⏵⏵ accept edits on
at the bottom of the terminal. A subsequent Shift+Tab will switch into Plan Mode, indicated by ⏸ plan mode on
.
Start a new session in Plan Mode
To start a new session in Plan Mode, use the --permission-mode plan
flag:
-p
(that is, in [“headless mode”](/docs/en/headless)):
Example: Planning a complex refactor
--name
or /rename
, accepting a plan won’t overwrite it.
Configure Plan Mode as default
[settings documentation](/docs/en/settings#available-settings)for more configuration options.
Work with tests
Suppose you need to add tests for uncovered code. Claude can generate tests that follow your project’s existing patterns and conventions. When asking for tests, be specific about what behavior you want to verify. Claude examines your existing test files to match the style, frameworks, and assertion patterns already in use. For comprehensive coverage, ask Claude to identify edge cases you might have missed. Claude can analyze your code paths and suggest tests for error conditions, boundary values, and unexpected inputs that are easy to overlook.Create pull requests
You can create pull requests by asking Claude directly (“create a pr for my changes”), or guide Claude through it step-by-step: When you create a PR usinggh pr create
, the session is automatically linked to that PR. You can resume it later with claude --from-pr <number>
.
Handle documentation
Suppose you need to add or update documentation for your code.Work with images
Suppose you need to work with images in your codebase, and you want Claude’s help analyzing image content.Add an image to the conversation
You can use any of these methods:
- Drag and drop an image into the Claude Code window
- Copy an image and paste it into the CLI with ctrl+v (Do not use cmd+v)
- Provide an image path to Claude. E.g., “Analyze this image: /path/to/your/image.png”
Reference files and directories
Use @ to quickly include files or directories without waiting for Claude to read them.Reference MCP resources
[MCP resources](/docs/en/mcp#use-mcp-resources)for details.
Use extended thinking (thinking mode)
[Extended thinking](https://platform.claude.com/docs/en/build-with-claude/extended-thinking)is enabled by default, giving Claude space to reason through complex problems step-by-step before responding. This reasoning is visible in verbose mode, which you can toggle on with
Ctrl+O
.
Additionally, Opus 4.6 and Sonnet 4.6 support adaptive reasoning: instead of a fixed thinking token budget, the model dynamically allocates thinking based on your [effort level](/docs/en/model-config#adjust-effort-level)setting. Extended thinking and adaptive reasoning work together to give you control over how deeply Claude reasons before responding. Extended thinking is particularly valuable for complex architectural decisions, challenging bugs, multi-step implementation planning, and evaluating tradeoffs between different approaches.
Phrases like “think”, “think hard”, and “think more” are interpreted as regular prompt instructions and don’t allocate thinking tokens.
Configure thinking mode
Thinking is enabled by default, but you can adjust or disable it.| Scope | How to configure | Details |
|---|---|---|
| Effort level | Run /effort , adjust in /model , or set
CLAUDE_CODE_EFFORT_LEVEL | Control thinking depth for Opus 4.6 and Sonnet 4.6. See
|
ultrathink
keywordOption+T
(macOS) or Alt+T
(Windows/Linux)[terminal configuration](/docs/en/terminal-config)to enable Option key shortcuts/config
to toggle thinking modeSaved as
alwaysThinkingEnabled
in ~/.claude/settings.json
[environment variable](/docs/en/env-vars)MAX_THINKING_TOKENS
0
applies unless adaptive reasoning is disabled. Example: export MAX_THINKING_TOKENS=10000
Ctrl+O
to toggle verbose mode and see the internal reasoning displayed as gray italic text.
How extended thinking works
Extended thinking controls how much internal reasoning Claude performs before responding. More thinking provides more space to explore solutions, analyze edge cases, and self-correct mistakes. With Opus 4.6 and Sonnet 4.6, thinking uses adaptive reasoning: the model dynamically allocates thinking tokens based on the[effort level](/docs/en/model-config#adjust-effort-level)you select. This is the recommended way to tune the tradeoff between speed and reasoning depth. With older models, thinking uses a fixed token budget drawn from your output allocation. The budget varies by model; see
[for per-model ceilings. You can limit the budget with that environment variable, or disable thinking entirely via](/docs/en/env-vars)
MAX_THINKING_TOKENS
/config
or the Option+T
/Alt+T
toggle.
On Opus 4.6 and Sonnet 4.6, [adaptive reasoning](/docs/en/model-config#adjust-effort-level)controls thinking depth, so
MAX_THINKING_TOKENS
only applies when set to 0
to disable thinking, or when CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING=1
reverts these models to the fixed budget. See [environment variables](/docs/en/env-vars).
Resume previous conversations
When starting Claude Code, you can resume a previous session:claude --continue
continues the most recent conversation in the current directoryclaude --resume
opens a conversation picker or resumes by nameclaude --from-pr 123
resumes sessions linked to a specific pull request
/resume
to switch to a different conversation.
Sessions are stored per project directory. The /resume
picker shows interactive sessions from the same git repository, including worktrees. When you select a session from another worktree of the same repository, Claude Code resumes it directly without requiring you to switch directories first. Sessions created by claude -p
or SDK invocations do not appear in the picker, but you can still resume one by passing its session ID directly to claude --resume <session-id>
.
Name your sessions
Give sessions descriptive names to find them later. This is a best practice when working on multiple tasks or features.Name the session
Name a session at startup with Or use You can also rename any session from the picker: run
-n
:/rename
during a session, which also shows the name on the prompt bar:/resume
, navigate to a session, and press R
.Use the session picker
The/resume
command (or claude --resume
without arguments) opens an interactive session picker with these features:
Keyboard shortcuts in the picker:
| Shortcut | Action |
|---|---|
↑ / ↓ | Navigate between sessions |
→ / ← | Expand or collapse grouped sessions |
Enter | Select and resume the highlighted session |
P | Preview the session content |
R | Rename the highlighted session |
/ | Search to filter sessions |
A | Toggle between current directory and all projects |
B | Filter to sessions from your current git branch |
Esc | Exit the picker or search mode |
- Session name or initial prompt
- Time elapsed since last activity
- Message count
- Git branch (if applicable)
/branch
, /rewind
, or --fork-session
) are grouped together under their root session, making it easier to find related conversations.
Run parallel Claude Code sessions with Git worktrees
When working on multiple tasks at once, you need each Claude session to have its own copy of the codebase so changes don’t collide. Git worktrees solve this by creating separate working directories that each have their own files and branch, while sharing the same repository history and remote connections. This means you can have Claude working on a feature in one worktree while fixing a bug in another, without either session interfering with the other. Use the--worktree
(-w
) flag to create an isolated worktree and start Claude in it. The value you pass becomes the worktree directory name and branch name:
<repo>/.claude/worktrees/<name>
and branch from the default remote branch, which is where origin/HEAD
points. The worktree branch is named worktree-<name>
.
The base branch is not configurable through a Claude Code flag or setting. origin/HEAD
is a reference stored in your local .git
directory that Git set once when you cloned. If the repository’s default branch later changes on GitHub or GitLab, your local origin/HEAD
keeps pointing at the old one, and worktrees will branch from there. To re-sync your local reference with whatever the remote currently considers its default:
.git
directory. Nothing on the remote server changes. If you want worktrees to base off a specific branch rather than the remote’s default, set it explicitly with git remote set-head origin your-branch-name
.
For full control over how worktrees are created, including choosing a different base per invocation, configure a [WorktreeCreate hook](/docs/en/hooks#worktreecreate). The hook replaces Claude Code’s default
git worktree
logic entirely, so you can fetch and branch from whatever ref you need.
You can also ask Claude to “work in a worktree” or “start a worktree” during a session, and it will create one automatically.
Subagent worktrees
Subagents can also use worktree isolation to work in parallel without conflicts. Ask Claude to “use worktrees for your agents” or configure it in a[custom subagent](/docs/en/sub-agents#supported-frontmatter-fields)by adding
isolation: worktree
to the agent’s frontmatter. Each subagent gets its own worktree that is automatically cleaned up when the subagent finishes without changes.
Worktree cleanup
When you exit a worktree session, Claude handles cleanup based on whether you made changes:- No changes: the worktree and its branch are removed automatically
- Changes or commits exist: Claude prompts you to keep or remove the worktree. Keeping preserves the directory and branch so you can return later. Removing deletes the worktree directory and its branch, discarding all uncommitted changes and commits
[setting, provided they have no uncommitted changes, no untracked files, and no unpushed commits. Worktrees you create with](/docs/en/settings#available-settings)
cleanupPeriodDays
--worktree
are never removed by this sweep.
To clean up worktrees outside of a Claude session, use [manual worktree management](#manage-worktrees-manually).
Copy gitignored files to worktrees
Git worktrees are fresh checkouts, so they don’t include untracked files like.env
or .env.local
from your main repository. To automatically copy these files when Claude creates a worktree, add a .worktreeinclude
file to your project root.
The file uses .gitignore
syntax to list which files to copy. Only files that match a pattern and are also gitignored get copied, so tracked files are never duplicated.
.worktreeinclude
--worktree
, subagent worktrees, and parallel sessions in the [desktop app](/docs/en/desktop#work-in-parallel-with-sessions).
Manage worktrees manually
For more control over worktree location and branch configuration, create worktrees with Git directly. This is useful when you need to check out a specific existing branch or place the worktree outside the repository.[official Git worktree documentation](https://git-scm.com/docs/git-worktree).
Non-git version control
Worktree isolation works with git by default. For other version control systems like SVN, Perforce, or Mercurial, configure[WorktreeCreate and WorktreeRemove hooks](/docs/en/hooks#worktreecreate)to provide custom worktree creation and cleanup logic. When configured, these hooks replace the default git behavior when you use
--worktree
, so [is not processed. Copy any local configuration files inside your hook script instead. For automated coordination of parallel sessions with shared tasks and messaging, see](#copy-gitignored-files-to-worktrees)
.worktreeinclude
[agent teams](/docs/en/agent-teams).
Get notified when Claude needs your attention
When you kick off a long-running task and switch to another window, you can set up desktop notifications so you know when Claude finishes or needs your input. This uses theNotification
[hook event](/docs/en/hooks-guide#get-notified-when-claude-needs-input), which fires whenever Claude is waiting for permission, idle and ready for a new prompt, or completing authentication.
Add the hook to your settings
Open If your settings file already has a
~/.claude/settings.json
and add a Notification
hook that calls your platform’s native notification command:- macOS
- Linux
- Windows
hooks
key, merge the Notification
entry into it rather than overwriting. You can also ask Claude to write the hook for you by describing what you want in the CLI.Optionally narrow the matcher
By default the hook fires on all notification types. To fire only for specific events, set the
matcher
field to one of these values:| Matcher | Fires when |
|---|---|
permission_prompt | Claude needs you to approve a tool use |
idle_prompt | Claude is done and waiting for your next prompt |
auth_success | Authentication completes |
elicitation_dialog | Claude is asking you a question |
[Notification reference](/docs/en/hooks#notification).
Use Claude as a unix-style utility
Add Claude to your verification process
Suppose you want to use Claude Code as a linter or code reviewer. Add Claude to your build script:Pipe in, pipe out
Suppose you want to pipe data into Claude, and get back data in a structured format. Pipe data through Claude:Control output format
Suppose you need Claude’s output in a specific format, especially when integrating Claude Code into scripts or other tools.Run Claude on a schedule
Suppose you want Claude to handle a task automatically on a recurring basis, like reviewing open PRs every morning, auditing dependencies weekly, or checking for CI failures overnight. Pick a scheduling option based on where you want the task to run:| Option | Where it runs | Best for |
|---|---|---|
|
[claude.ai/code](https://claude.ai/code).[Desktop scheduled tasks](/docs/en/desktop-scheduled-tasks)[GitHub Actions](/docs/en/github-actions)/loop
Ask Claude about its capabilities
Claude has built-in access to its documentation and can answer questions about its own features and limitations.Example questions
Claude provides documentation-based answers to these questions. For hands-on demonstrations, run
/powerup
for interactive lessons with animated demos, or refer to the specific workflow sections above.Next steps
Best practices
Patterns for getting the most out of Claude Code
How Claude Code works
Understand the agentic loop and context management
Extend Claude Code
Add skills, hooks, MCP, subagents, and plugins
Reference implementation
Clone the development container reference implementation