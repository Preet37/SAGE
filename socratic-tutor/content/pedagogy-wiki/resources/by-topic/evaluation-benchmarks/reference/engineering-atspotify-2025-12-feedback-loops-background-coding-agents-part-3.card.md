# Card: Predictable background coding agents via verification loops
**Source:** https://engineering.atspotify.com/2025/12/feedback-loops-background-coding-agents-part-3  
**Role:** explainer | **Need:** DEPLOYMENT_CASE  
**Anchor:** Concrete production pattern: iterative verification/feedback loops (agent unaware of verifier details) to improve PR success predictability.

## Key Content
- **Primary failure modes (production agent at scale):**
  1) Agent fails to produce a PR (minor; manual fallback).  
  2) PR produced but **fails CI** (frustrating; leaves half-broken code).  
  3) PR **passes CI but is functionally incorrect** (most serious; erodes trust; hard to spot across thousands of components).
- **Core procedure: “verification loop” (inner loop)**
  - Implement **strong verification loops** so the agent can **incrementally confirm** it’s on track **before committing/opening a PR**.
  - **Design principle:** agent **doesn’t know** what verification does/how; it only knows it can/must call a verification tool.
  - Loop consists of **one or more independent verifiers** that **auto-activate** based on repo contents (e.g., **Maven verifier** triggers if `pom.xml` exists at repo root).
  - Verifiers are exposed via an abstraction layer (e.g., **MCP tool definition**); **individual verifiers are not exposed directly** to the agent.
  - Verifiers run formatting/build/test and **parse noisy outputs** (often via **regex**) to return **short, relevant error messages** or a short success message.
  - System runs **all relevant verifiers before opening a PR**; in Claude Code implemented via a **stop hook**. If any verifier fails → **PR not opened**; user gets error.
- **Additional safeguard: LLM “Judge” (post-verifier)**
  - Inputs: **diff of proposed change + original prompt**; evaluated by an LLM.
  - Purpose: prevent “ambitious” out-of-scope changes (refactors, disabling flaky tests).
  - Empirics: across **thousands of agent sessions**, judge **vetoes ~25%**; when vetoed, agent **course-corrects ~50%** of the time.
- **Design rationale for predictability/security**
  - Keep agent narrowly scoped: see codebase, edit files, run verifiers only.
  - Surrounding infra handles pushing code, Slack interaction, prompt authoring.
  - Run agent **highly sandboxed** (container, limited permissions, few binaries, minimal system access).

## When to surface
Use when students ask how to deploy code-writing agents safely/reliably in production, how to structure feedback/verification loops, or how to prevent out-of-scope agent changes while keeping PRs predictable.