# Card: LangGraph Cloud (LangSmith Deployment) — scaling & reliability rationale
**Source:** https://blog.langchain.dev/langgraph-cloud/  
**Role:** explainer | **Need:** DEPLOYMENT_CASE  
**Anchor:** System-design rationale for scaling/reliability (deployment model, operational concerns, and what the platform adds beyond local execution)

## Key Content
- **LangGraph v0.1 design rationale (control vs. agency):**
  - Legacy high-level abstractions (e.g., LangChain `AgentExecutor`) can “hide too many details,” reducing developer control and hurting reliability on complex, domain-specific workflows.
  - LangGraph provides **low-level control** over **code flow, prompts, and LLM calls**, supporting **conditional branching and looping** for single- or multi-agent architectures (hierarchical/sequential patterns).
  - Enables **moderation/quality checks** as explicit gates before continuing, reducing chances an agent gets stuck on an unrecoverable path.
  - **Human-in-the-loop via persistence layer:** design workflows to (1) wait for human approval before executing and resuming, (2) edit actions before execution, (3) “time travel” to inspect/rewire/edit/resume execution.
  - Supports **streaming intermediate steps** and **token-by-token streaming** for responsiveness in long-running tasks.
- **LangGraph Cloud (beta) deployment model & operational additions:**
  - Purpose-built infra for **scalable, fault-tolerant** agent deployment; addresses overload from **uneven task distribution** that can cause slowdowns/downtime.
  - Manages **horizontally-scaling task queues and servers** plus a **robust Postgres checkpointer** to store large **states/threads** and handle many concurrent users.
  - Adds real-world interaction patterns:
    - **Double-texting** on currently-running threads with 4 strategies: **reject, queue, interrupt, rollback**.
    - **Async background jobs** for long tasks; completion via **polling or webhook**.
    - **Cron jobs** for scheduled tasks.
  - Integrated dev/ops: **LangGraph Studio** for visualizing trajectories, debugging failure modes, adding breakpoints, interruption/state editing/resumption/time travel; sharing for stakeholder feedback.
  - **Deployment workflow:** select LangGraph GitHub repo → **one-click deploy** (no infra expertise). Integrated with **LangSmith** for monitoring **usage, errors, performance, costs**.
- **Naming note:** As of **Oct 2025**, “LangGraph Platform” renamed to **LangSmith Deployment**.

## When to surface
Use when students ask how to move a LangGraph agent from local runs to production: scaling, fault tolerance, persistence/checkpointing, handling concurrent inputs (“double-texting”), background/cron jobs, and monitoring/debugging workflows.