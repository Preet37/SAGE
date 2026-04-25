# Card: Azure Durable Functions — Stateful serverless workflows (overview)
**Source:** https://learn.microsoft.com/en-us/azure/azure-functions/durable/durable-functions-overview  
**Role:** reference_doc | **Need:** [API_REFERENCE] / [COMPARISON_DATA]  
**Anchor:** Deterministic replay model context + orchestrator/activity/entity concepts; pointers to orchestrator constraints, storage providers, and monitoring.

## Key Content
- **What Durable Functions is (definition):** An extension of **Azure Functions** for building **stateful workflows** in a **serverless** environment by writing **orchestrator**, **activity**, and **entity** functions in code. Runtime manages **state**, **checkpoints**, **retries**, and **recovery** so workflows can run reliably for **long periods**.
- **Core workflow structure (conceptual procedure):**
  - Orchestrator function coordinates execution.
  - Activity functions perform work steps.
  - Entity functions model stateful entities (for durable state patterns).
- **Getting started procedure (numbered steps from doc):**
  1. Create a new Azure Functions app using a language quickstart.
  2. Add an **orchestrator** function and **one or more activity** functions.
  3. Choose/configure a backend via **Durable Functions storage providers**; **recommended:** **Durable Task Scheduler**.
  4. Run/test locally with **Azure Functions Core Tools**.
  5. Deploy to Azure and **monitor orchestration instances**.
- **Supported languages (table facts):** Durable Functions support listed as **Supported** for **.NET (C#), JavaScript, TypeScript, Python, PowerShell, Java** (each has a “Create your first durable function” quickstart link).
- **Design rationale (explicit):** Runtime-managed state/checkpointing/retries/recovery enables **reliable long-running** workflows without manual state management.
- **Key follow-up topics to consult next (links):** **Task hubs**, **HTTP features**, and **orchestrator code constraints** (deterministic/replay constraints are referenced via link).

## When to surface
Use when students ask whether Durable Functions fits a **long-running/stateful workflow** need, what components to implement (orchestrator/activity/entity), what languages are supported, or what the **setup steps** and **recommended backend (Durable Task Scheduler)** are.