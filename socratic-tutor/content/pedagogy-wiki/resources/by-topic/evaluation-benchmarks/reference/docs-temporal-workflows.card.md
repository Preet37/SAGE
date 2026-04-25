# Card: Temporal Workflow timeouts (Execution/Run/Task) — definitions, defaults, API params
**Source:** https://docs.temporal.io/workflows#workflow-timeouts  
**Role:** reference_doc | **Need:** [COMPARISON_DATA] / [API_REFERENCE]  
**Anchor:** Workflow-level timeout semantics + parameter names; contrast with Activity timeouts

## Key Content
- **General guidance (design rationale):**
  - Temporal **generally does not recommend setting Workflow Timeouts** because Workflows are **long-running/resilient**; timeouts can **limit ability to handle delays**.
  - For “do something after X time” **inside** a Workflow, prefer a **Timer** (durable sleep managed by Temporal service), not Workflow timeouts.

- **Where configured (procedure/API):**
  - Set at Workflow start via `client.start_workflow()` or `client.execute_workflow()`.
  - Timeout parameter names: `execution_timeout`, `run_timeout`, `task_timeout`.
  - Example (Python):  
    `await client.execute_workflow(..., execution_timeout=timedelta(seconds=2), run_timeout=..., task_timeout=...)`

- **Workflow timeout types (definitions + defaults):**
  - **Workflow Execution Timeout**: max time a Workflow Execution can be **Open**, **including retries and Continue-As-New**.  
    - **Default:** `∞` (infinite).  
    - On reach: Execution becomes **Timed Out**.  
    - Common use: limit total duration of a **Temporal Cron Job** over time.
  - **Workflow Run Timeout**: max duration of a **single Run** (one Run ID) within an Execution; **excludes retries/Continue-As-New**.  
    - **Default:** same as **Execution Timeout**.  
    - On reach: Execution becomes **Timed Out**.  
    - Constraint: **cannot be greater than** Execution Timeout.
  - **Workflow Task Timeout**: max time a Worker may execute a **Workflow Task** after pulling from Task Queue (detect Worker down / recovery).  
    - **Default:** **10s**; **max:** **120s**.  
    - Increase only if large history load needs >10s; not recommended beyond default.

- **Observability/troubleshooting:**
  - Use Search Attribute **`TemporalReportedProblems`** to find Workflows with **failed Workflow Tasks**; a failed Workflow Task **does not fail** the Workflow but can prevent completion if unhandled.

## When to surface
Use when students ask how Temporal’s **execution vs run vs task** timeouts differ, what the **default values/limits** are, or which **API parameters** to set at Workflow start (and why Timers are preferred for business logic time bounds).