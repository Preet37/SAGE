# Card: Spotify “Honk” Background Coding Agent (Part 1) — Deployment Pattern
**Source:** https://engineering.atspotify.com/2025/11/spotifys-background-coding-agent-part-1  
**Role:** explainer | **Need:** DEPLOYMENT_CASE  
**Anchor:** System-level architecture narrative for a background coding agent: how work is scoped/queued, PRs produced, and operational constraints (human review, reliability, cost).

## Key Content
- **Baseline platform (Fleet Management):** Runs **source-to-source transformations as jobs** in a **containerized environment**, then **automatically opens PRs** against target repos. Historically strong for:
  - Dependency bumps (e.g., Maven **pom.xml**)
  - Config updates (deployment manifests)
  - Simple refactors (replace deprecated calls)
- **Scale/impact metrics:**
  - Since **mid-2024**, **~50% of Spotify PRs** have been automated by Fleet Management.
  - AI agents have generated **1,500+ PRs merged** into production.
  - Reported **60–90% total time savings** vs writing changes by hand (for complex migrations).
- **Why agents (design rationale):**
  - Deterministic transformation scripts become extremely complex (example: Maven dependency updater grew to **20,000+ LOC** to handle corner cases).
  - Goal: let engineers define fleet-wide changes in **natural language**, lowering expertise barrier.
- **Architecture choice:** Replace only the **transformation declaration** with an agent; keep surrounding infra unchanged (**repo targeting → PR opening → review → merge**).
- **Internal CLI (pluggable agent runner):**
  - Delegates prompt execution to an agent
  - Runs formatting/linting via **local MCP (Model Context Protocol)**
  - Uses **LLMs-as-judge** to evaluate diffs
  - Uploads logs to **GCP**
  - Captures traces in **MLflow**
  - Rationale: enables **swapping agents/LLMs** without changing user workflow.
- **Background agent workflow (Slack/GitHub):**
  1. User interacts with an **interactive agent** to gather task info
  2. Interaction produces a **prompt**
  3. Prompt handed to coding agent → **PR produced**
  - Used for ADR drafting from Slack threads; PM-proposed simple changes.
- **Operational constraints called out:** long runtimes, unpredictable outputs → need validation/quality control; plus safety, sandboxing, and cost/LLM quota management.

## When to surface
Use when students ask how to deploy coding agents in production to generate PRs safely (workflow, tooling, observability), or want concrete adoption metrics (PR counts, time savings, automation share).