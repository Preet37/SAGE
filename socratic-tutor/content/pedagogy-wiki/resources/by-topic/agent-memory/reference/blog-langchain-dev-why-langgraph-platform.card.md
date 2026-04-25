# Card: Deployment requirements LangGraph Platform (LangSmith Deployment)
**Source:** https://blog.langchain.dev/why-langgraph-platform/  
**Role:** explainer | **Need:** DEPLOYMENT_CASE  
**Anchor:** Explicit deployment requirements (retries, persistence/checkpointing, observability/streaming, scaling) + how LangGraph Platform addresses them

## Key Content
- **Renaming (timeline):** As of **Oct 2025**, “LangGraph Platform” renamed to **LangSmith Deployment**.
- **When you *don’t* need it:** **Stateless**, **quick**, **low-volume** agents can be deployed simply (e.g., “run them as a lambda”).
- **When deployment gets hard:** Agents that are **long-running**, **stateful**, or **bursty**.

- **Long-running agents: requirements → platform features**
  - Avoid holding open connections for hours: **launch runs in background** + **polling endpoints**, **streaming endpoints**, **webhooks** for status.
  - Handle timeouts/disruptions: **heartbeat signals** to prevent connection closure; **stream endpoints can be rejoined** after drops; (planned) **buffer events** during disconnect.
  - Reliability via retries + persistence: on failure, **retry configurable number of times**, and **each retry resumes from most recent successful checkpoint** (checkpoint-based recovery). Workers use **isolated event loops/background threads** to reduce exceptions.
  - Observability/user feedback: multiple streaming modes—**intermediate results**, **token-by-token LLM messages**, and **custom payloads** emitted by nodes; **multiple consumers** can attach to the same stream; streams **re-establishable**.

- **Bursty agents: requirements → platform features**
  - Load spikes: built-in **task queue**; **horizontal scaling** of server + queue; servers are **stateless**; queue shares runs **fairly** and **never executes the same run more than once**.
  - “Double texting” (multiple user messages before prior response completes): **four built-in strategies** to manage.

- **Stateful agents: requirements → platform features**
  - Supports complex state (beyond message lists), **short/long-term memory**, **human-in-the-loop** pauses, and **human-on-the-loop (“time travel”)** resume-from-prior-state.
  - Provides **optimized checkpointers** + **memory store**; **specialized endpoints** for human-in-the-loop.
  - Storage control: attach **TTLs** to **conversation threads** and **long-term memory entries** for automatic expiry.

## When to surface
Use when students ask what extra infrastructure is needed to deploy agents beyond “just host an API,” especially for **retries/checkpointing**, **streaming/monitoring**, **bursty scaling/queues**, **double-text handling**, and **stateful memory + HITL/time-travel**.