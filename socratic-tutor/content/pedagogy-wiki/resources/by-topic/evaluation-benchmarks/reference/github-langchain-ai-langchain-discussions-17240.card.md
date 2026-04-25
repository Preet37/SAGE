# Card: FastAPI wiring for LangChain/LangGraph event streaming (index)
**Source:** https://github.com/langchain-ai/langchain/discussions/17240  
**Role:** reference_doc | **Need:** [WORKING_EXAMPLE] End-to-end runnable examples combining token streaming + step/event streaming + intermediate state inspection  
**Anchor:** Community discussion hub pointing to FastAPI + “events stream API” plumbing patterns and related official how-to guides (stream runnables, debug apps, inspect runnables, stream events from tools), plus LangSmith for tracing/observability.

## Key Content
- **Primary use:** A navigation/index-style discussion page for *streaming + observability* topics across LangChain/LangGraph/LangSmith.
- **Relevant procedures (as linked how-to areas):**
  - **Streaming runnables (LCEL/Runnable protocol):** guidance on streaming outputs back to clients (token streaming) and runtime configuration of runnable behavior.
  - **Inspecting/debugging:** “How to: inspect runnables” and “How to: debug your LLM apps” (intermediate state inspection / debugging workflow).
  - **Tool event streaming:** “How to: stream events from a tool” (step/event streaming hooks).
  - **Async/callback environments:** “How to: use callbacks in async environments” and “dispatch custom callback events” (observability/event emission patterns).
- **Observability rationale:** Recommends **LangSmith** as the platform to *trace, monitor, evaluate, and deploy* agents; emphasizes tracing as vital for diagnosing issues and inspecting step-level execution.
- **No equations / no numeric benchmarks / no explicit default hyperparameters** are provided in the captured text; it functions as a pointer to the concrete implementations elsewhere.

## When to surface
Use when a student asks how to wire **FastAPI HTTP streaming** for LangChain/LangGraph **event streams** (tokens + step events) and how to add **debugging/tracing/observability** (callbacks, runnable inspection, LangSmith tracing).