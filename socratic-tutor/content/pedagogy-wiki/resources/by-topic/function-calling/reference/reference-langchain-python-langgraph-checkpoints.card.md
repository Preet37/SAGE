# Card: LangGraph Checkpointing & Persistence (threads, checkpoints, replay)
**Source:** https://reference.langchain.com/python/langgraph/checkpoints/  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Checkpointing/persistence API surface (checkpointer interfaces + attaching to compiled graph) for durable memory, resume, time-travel

## Key Content
- **Attach persistence to a graph**
  - Compile with a checkpointer: `graph = builder.compile(checkpointer=checkpointer, store=store)` (store optional; checkpointer enables threads/checkpoints).
  - **Must pass `thread_id`** on invoke/stream/batch to persist/resume:  
    `config = {"configurable": {"thread_id": "my-thread"}}`; `graph.invoke(inputs, config)`.  
    `thread_id` is the **primary key** for storing/retrieving checkpoints; without it no save/resume/time-travel.
- **Core objects**
  - **CheckpointMetadata** fields: `source ∈ {'input','loop','update','fork'}`; `step: int` where `-1` = first `"input"` checkpoint, `0` = first `"loop"` checkpoint, increasing thereafter.
  - **Checkpoint** fields: `id: str` (unique, monotonically increasing), `channel_values: dict[str, Any]`, `channel_versions`, `versions_seen` (per-node channel versions seen; drives scheduling).
  - **StateSnapshot** (returned by `graph.get_state*`): `values`, `next` (tuple of next node names; empty `()` means complete), `config` (includes `thread_id`, `checkpoint_ns`, `checkpoint_id`), `metadata` (includes `source`, `writes`, `step`), `created_at`, `parent_config`, `tasks`.
- **Super-step procedure (empirical count)**
  - Checkpoints are created at each **super-step boundary** (“tick”). Example sequential graph `START→A→B→END` yields **4 checkpoints**: empty/START-next, input/node_a-next, after A/node_b-next, after B/complete.
- **Namespaces**
  - `checkpoint_ns=""` for root graph; subgraph checkpoints use `"node_name:uuid"`; nested join with `|`. Accessible in-node via `config["configurable"]["checkpoint_ns"]`.
- **Replay/time travel**
  - Invoke with a prior `checkpoint_id` to **skip** nodes before it (replayed from saved results) and **re-execute** nodes after it (LLM/API/interrupts re-trigger).
- **Checkpointer interface (BaseCheckpointSaver)**
  - Sync: `get`, `get_tuple`, `list`, `put`, `put_writes`, `delete_thread`, `get_next_version`.
  - Async counterparts: `aget`, `aget_tuple`, `alist`, `aput`, `aput_writes`, `adelete_thread`.
  - Example implementation: `InMemorySaver`; SQLite example: `SqliteSaver.from_conn_string(":memory:")`.

## When to surface
Use when students ask how LangGraph persists state across turns, how to enable durable memory/resume/interrupts, how checkpoints are structured (thread_id, step, source), or how to replay/fork execution via checkpoint_id.