# Card: Claude Code Best Practices (Agentic Coding Loop)
**Source:** https://code.claude.com/docs/en/best-practices  
**Role:** reference_doc | **Need:** WORKING_EXAMPLE  
**Anchor:** Actionable agent loop guidance: task decomposition, iterative verification (tests/linters), safe tool use patterns, and prompt templates

## Key Content
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

## When to surface
Use when students ask how to run an effective coding-agent loop (plan vs implement), how to prevent “LLM drift” from long sessions, how to structure prompts/verification, or how to configure CLAUDE.md/permissions/hooks for safe, iterative development.