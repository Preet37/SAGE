# Card: LangGraph v0.2 — Checkpointers, durability, replay/resume
**Source:** https://blog.langchain.com/langgraph-v0-2/  
**Role:** explainer | **Need:** CONCEPT_EXPLAINER  
**Anchor:** Maintainer rationale for standardizing checkpointer interfaces; how persistence enables durable, replayable graph/state execution.

## Key Content
- **Core design pillar:** LangGraph includes a built-in **persistence layer** via **checkpointers**. A checkpointer **saves a checkpoint of graph state at each step** (step-level durability).
- **Capabilities enabled by step checkpoints:**
  - **Session memory:** store checkpoint history of user interactions; **resume** from a saved checkpoint in follow-up interactions.
  - **Error recovery:** **continue from last successful step checkpoint** after failures.
  - **Human-in-the-loop:** tool approval, wait for human input, edit agent actions.
  - **Time travel / forking:** edit graph state at any point in execution history and create an alternative execution from that point (“fork the thread”).
- **Rationale for v0.2 changes:** community demand for DB-specific checkpointers (Postgres/Redis/MongoDB) existed, but **no clear blueprint** for custom implementations; v0.2 introduces **standardized interfaces + dedicated libraries** to simplify creation/customization and foster a community ecosystem.
- **New checkpointer library ecosystem (interchangeable implementations):**
  - `langgraph_checkpoint`: base interfaces **`BaseCheckpointSaver`**, **`SerializationProtocol`**; includes **`MemorySaver`** (in-memory).
  - `langgraph_checkpoint_sqlite`: **SQLite** implementation (local/experimentation).
  - `langgraph_checkpoint_postgres`: production-grade **Postgres** implementation (open-sourced from LangGraph Cloud).
- **Postgres checkpointer optimizations:**
  - Write-side: **Postgres pipeline mode** to reduce roundtrips; store **each channel value separately and versioned** so each checkpoint stores **only changed values**.
  - Read-side: **cursor** for list endpoint to efficiently fetch long thread histories.
- **Imports / installs (namespace packages):**
  - `from langgraph.checkpoint.base import BaseCheckpointSaver`
  - `from langgraph.checkpoint.memory import MemorySaver`
  - `from langgraph.checkpoint.sqlite import SqliteSaver` (requires `pip install langgraph-checkpoint-sqlite`)
  - `from langgraph.checkpoint.postgres import PostgresSaver` (requires `pip install langgraph-checkpoint-postgres`)
- **Versioning:** checkpointer libs follow **semantic versioning starting at 1.0**; breaking changes in main interfaces → **major bump** (e.g., `langgraph_checkpoint` 2.0 implies implementations update to 2.0).
- **Breaking rename:** `thread_ts` → `checkpoint_id`; `parent_ts` → `parent_checkpoint_id` (still recognized if passed via config).

## When to surface
Use when students ask why LangGraph emphasizes persistence, how replay/resume/error recovery/HITL work in graph execution, or what changed in v0.2 regarding checkpointer interfaces and DB-backed durability.