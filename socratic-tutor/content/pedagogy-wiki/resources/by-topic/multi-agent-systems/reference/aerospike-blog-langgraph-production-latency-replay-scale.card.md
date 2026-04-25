# Card: LangGraph production metrics: latency, checkpoints, replay, scale
**Source:** https://aerospike.com/blog/langgraph-production-latency-replay-scale  
**Role:** benchmark | **Need:** DEPLOYMENT_CASE  
**Anchor:** Operational framing + concrete latency/storage math for production agent workflows (TTFT/TPOT targets, checkpointing, replay/idempotency, fan-out amplification).

## Key Content
- **Interactive latency targets (MLPerf framing):** real-time systems often target **TTFT < 1s** and **TPOT in “tens of ms”** to feel responsive; orchestration overhead must fit inside these budgets.
- **LangGraph execution model (supersteps):** each step has **3 phases**: (1) *plan* which actors/nodes to execute, (2) *execute* selected actors in parallel, (3) *apply updates*. Intermediate updates aren’t visible until the next step → clearer race-condition boundaries and replay points.
- **Eq. 1 — Checkpoint write rate sizing:**  
  **writes/sec = steps_per_request × requests/sec**  
  Example from source: **12 steps/request** and **2,000 req/s ⇒ 24,000 writes/s** (plus reads for resume/inspection).
- **Checkpoint alignment:** checkpoints persist at **superstep boundaries**; snapshot count scales with **#steps**, not wall-clock runtime.
- **Replay/resume semantics:** workflows can **pause and resume** (even **up to a week** later) by restoring state and **replaying from a safe point**. To avoid duplicated side effects (e.g., “write ticket twice”, “charge twice”), **non-deterministic/side-effectful operations must be isolated as separate tasks**; design for **determinism + idempotency**.
- **State types:** (a) **thread-local execution state** keyed by **thread_id** for checkpointing/resume; (b) **cross-thread long-term memory** with **TTL** and optional similarity search (**semantic search disabled by default; requires index + compatible store**).
- **Tool catalog default guidance:** OpenAI function calling guidance cited: keep **< 20 functions** available at once for higher accuracy; function definitions are injected into system message and billed as input tokens.
- **Empirical comparison:** external benchmark (5-agent workflow × **100 runs**) reports LangGraph **>2× faster than CrewAI**; CrewAI had ~**5s of a 9s** segment as tool-interaction gap; LangGraph passes **state deltas** vs full histories (token/latency savings).

## When to surface
Use when students ask how to set **production SLOs** (TTFT/TPOT), **size checkpoint storage IOPS**, design **replay-safe/idempotent** agent steps, or reason about **fan-out/superstep amplification** and orchestration overhead.