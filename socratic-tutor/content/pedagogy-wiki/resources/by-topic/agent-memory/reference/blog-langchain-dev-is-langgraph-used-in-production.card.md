# Card: LangGraph in Production — reliability/observability/control
**Source:** https://blog.langchain.dev/is-langgraph-used-in-production/  
**Role:** explainer | **Need:** DEPLOYMENT_CASE  
**Anchor:** Production-oriented discussion of reliability/observability/control requirements and how LangGraph + LangSmith address them (with named company examples).

## Key Content
- **Production adoption examples (named):**
  - **LinkedIn:** Built an AI-powered recruiter using a **hierarchical agent system** on LangGraph to automate candidate sourcing, matching, and messaging; freed human recruiters for higher-level strategy.
  - **AppFolio:** Copilot for property managers; **saved 10+ hours/week**, **cut app latency**, and **2× decision accuracy** (as attributed to LangGraph’s impact).
  - **Replit:** Multi-agent software-building copilot; LangGraph enables **human-in-the-loop** transparency so users can see agent actions (e.g., package installs, file creation).
  - **Uber:** Used LangGraph to streamline **large-scale code migrations**; structured specialized agents for unit test generation steps “with precision.”
  - **Elastic:** Orchestrated a network of agents for **real-time threat detection**, improving speed/effectiveness of security response.
- **Why production is hard (key hurdles):**
  - **Unpredictability of LLMs:** dynamic generation + free-form user input makes correctness/context hard to guarantee.
  - **Complex orchestration:** coordinating multiple agents, dependencies, error recovery, and communication.
  - **Observability/debugging limits:** hard to diagnose “why” behind bad agent decisions without tracing/monitoring.
- **What LangGraph is (design rationale):** a **controllable agent framework designed for production use**, emphasizing:
  - **Low-level, customizable primitives** (fully descriptive; intended to scale beyond prototyping).
  - **Reliability controls:** moderation checks, human-in-the-loop, persisted context for long-running workflows.
  - **Observability:** integrates with **LangSmith** for visibility into interactions, performance monitoring, debugging.
- **Historical note:** Built in **early 2024**; positioned as default framework for many production agentic apps; tradeoff: **steeper learning curve** for scalability.

## When to surface
Use when students ask whether LangGraph is used in real production, what production requirements (reliability/observability/control) look like for agents, or why LangGraph + LangSmith are chosen over higher-level “black-box” agent frameworks.