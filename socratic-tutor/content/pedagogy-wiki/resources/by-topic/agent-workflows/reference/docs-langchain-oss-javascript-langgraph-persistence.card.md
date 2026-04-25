# Card: LangGraph Persistence & Checkpoint Semantics
**Source:** https://docs.langchain.com/oss/javascript/langgraph/persistence  
**Role:** reference_doc | **Need:** DEPLOYMENT_CASE  
**Anchor:** Concrete checkpoint/persistence semantics (checkpointer configuration, what state is stored, resume/replay behavior) and canonical durable-execution pattern in LangGraph.

## Key Content
- **Persistence model:** Compile a LangGraph with a **checkpointer** to save a **checkpoint (StateSnapshot)** at **every super-step** (a “tick” where all scheduled nodes run, potentially in parallel). Enables **HITL**, **memory**, **time travel**, **fault tolerance**.
- **Required config (threading):** Must pass `thread_id` in config to persist/resume:  
  **Config formula:** `config = { configurable: { thread_id: "<id>" } }`  
  Checkpointer uses `thread_id` as the **primary key**; without it, it cannot save state or resume after interrupts.
- **Checkpoint contents (StateSnapshot fields):**
  - `values`: state channel values at checkpoint
  - `next`: node names to execute next (`[]` means complete)
  - `config`: includes `thread_id`, `checkpoint_ns`, `checkpoint_id`
  - `metadata`: `source` ∈ {"input","loop","update"}, `writes` (node outputs), `step` (super-step counter)
  - `createdAt`, `parentConfig`, `tasks` (task id/name/error/interrupts; may include subgraph state)
- **Empirical checkpoint count example:** For sequential `START -> A -> B -> END`, invoking once yields **exactly 4 checkpoints**: (1) empty/START next, (2) input saved/nodeA next, (3) nodeA outputs/nodeB next, (4) nodeB outputs/complete. Reducers accumulate (e.g., `bar` becomes `['a','b']`).
- **Replay semantics:** Invoke with prior `checkpoint_id` to re-execute **after** that checkpoint; earlier nodes skipped. **LLM calls/API requests/interrupts are re-triggered** during replay.
- **Fault tolerance + pending writes:** If a node fails mid super-step, LangGraph stores **pending writes** from successful nodes; on resume you **don’t re-run** successful nodes.
- **Namespaces:** `checkpoint_ns=""` for root; subgraph checkpoints use `"node_name:uuid"`; nested join with `|`. Accessible via `config.configurable.checkpoint_ns`.
- **APIs:** `graph.getState(config)` (latest or specific `checkpoint_id`), `graph.getStateHistory(config)` (most recent first), `graph.updateState()` creates a **new** checkpoint; reducer channels **accumulate**.
- **Defaults/infra:** Agent Server / LangGraph API handle checkpointing (and stores) automatically. Checkpointer libs: `MemorySaver` (in-memory), `SqliteSaver`, `PostgresSaver`, `MongoDBSaver`, `RedisSaver`. Base interface methods: `.put`, `.putWrites`, `.getTuple`, `.list`.

## When to surface
Use when students ask how LangGraph achieves **durable execution**, **resume/replay**, **HITL interrupts**, or what exactly is stored per step (threads, checkpoints, super-steps, pending writes, namespaces).