# Card: Two-layer agent architecture (LangGraph logic + Temporal durability)
**Source:** https://temporal.io/blog/prototype-to-prod-ready-agentic-ai-grid-dynamics  
**Role:** explainer | **Need:** COMPARISON_DATA  
**Anchor:** Pattern: keep agent logic in LangGraph-style graphs, but use Temporal for durable execution (state persistence, retries, recovery, scaling).

## Key Content
- **Use case:** “Deep research agent” for a Fortune 500 manufacturer with **100+ plants**; searches internal DBs/shared drives/repos, then expands to web if needed; **labels internal vs open-web sources** and cites sources.
- **Observed LangGraph-in-prod pain points (why migrate):**
  - Needed **robust error handling + retries** → built **custom retry/error-handling** especially for **human-in-the-loop waits**, requiring **manual state maintenance**; led to **inconsistent workflow state** and hard recovery/debugging.
  - **Redis-based state**: had to manage **lifecycle/expiration**; bugs around **expired state** were time-consuming to reproduce; caching updates could wipe common requests.
  - Scaling/exactly-once: to ensure each request processed **exactly once**, they used **Apache Kafka** + executor pool; still hit **race conditions, stale state, stuck agents**.
- **Temporal design rationale (what changed):**
  - **State becomes part of the workflow** (durably persisted in Temporal event history), not an external “baton” (Redis key). Workflow passes a **serializable state object** into each Activity; Activities return updated state.
  - **Declarative retries via `RetryPolicy`** attached to Activity execution (delete “thousands of lines” of try/catch + retry loops).
    - Example defaults shown: `initial_interval=1s`, `backoff_coefficient=2.0`, `maximum_interval=60s`, `maximum_attempts=4`; another policy `initial_interval=5s`, `backoff_coefficient=1.0`, `maximum_interval=15s`, `maximum_attempts=3`; `non_retryable_error_types` includes `ValueError` (and `TypeError` in second).
- **Scaling procedure:** run **multiple identical stateless Temporal Worker replicas** on Kubernetes polling the same task queue; Temporal handles load balancing/distribution.
- **Architectural decoupling step:** convert each LangGraph node into a **self-contained Temporal Activity** with **explicit serializable inputs/outputs**; move shared client init into Activities; optimize via **client pooling/lazy init**.

## When to surface
Use when students ask how to move an agent from prototype to production: durable state, exactly-once execution, human-in-the-loop pauses, retries/backoff policies, and horizontal scaling patterns (LangGraph vs Temporal).