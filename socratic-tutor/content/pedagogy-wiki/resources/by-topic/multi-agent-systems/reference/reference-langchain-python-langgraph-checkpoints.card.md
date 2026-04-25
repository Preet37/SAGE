# Card: LangGraph Checkpointing (Threads, Checkpoints, Replay)
**Source:** https://reference.langchain.com/python/langgraph/checkpoints/  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** checkpointing API surface (checkpointer interfaces/classes), persistence semantics, replay/resume configuration

## Key Content
- **Core requirement (config):** to persist/resume, pass `thread_id` in config:  
  `config = {"configurable": {"thread_id": "my-thread"}}`; `graph.invoke(inputs, config)`  
  `thread_id` is the **primary key** for storing/retrieving checkpoints; without it no save/resume/time-travel.
- **Checkpoint metadata (TypedDict):**  
  `source: Literal["input","loop","update","fork"]` (origin of checkpoint)  
  `step: int` with conventions: `-1` = first `"input"` checkpoint; `0` = first `"loop"` checkpoint; increasing thereafter.
- **Checkpoint (TypedDict) fields:**  
  `id: str` (unique, **monotonically increasing**; sortable)  
  `channel_values: dict[str, Any]` (deserialized channel snapshots)  
  `channel_versions: {channel -> version}` (monotonic version strings)  
  `versions_seen: {node_id -> {channel -> version}}` (drives which nodes execute next).
- **BaseCheckpointSaver API (sync + async):** `get`, `get_tuple`, `list`, `put`, `put_writes`, `delete_thread`; async: `aget`, `aget_tuple`, `alist`, `aput`, `aput_writes`, `adelete_thread`; plus `get_next_version(current)->V` (must be monotonically increasing; can be float).
- **Super-step semantics:** checkpoint saved at each **super-step boundary** (“tick” where scheduled nodes run). Resume/replay only from checkpoints.
- **StateSnapshot key fields (for `graph.get_state*`):** `values`, `next: tuple[str,...]`, `config` (includes `thread_id`, `checkpoint_ns`, `checkpoint_id`), `metadata` (includes `source`, `writes`, `step`), `created_at`, `parent_config`, `tasks`.
- **Checkpoint namespace (`checkpoint_ns`):** `""` for root graph; `"node_name:uuid"` for subgraph; nested joined by `|`.
- **Empirical example:** sequential `START->A->B->END` yields **4 checkpoints**: empty/START-next; input/next=A; after A/next=B; after B/next=().
- **Replay rule:** invoke with prior `checkpoint_id` to re-run **after** it; steps **before** are skipped (replayed from saved results). LLM/tool calls/interrupts **after** checkpoint are re-triggered.

## When to surface
Use when students ask how LangGraph persists state across turns, how to configure `thread_id`/`checkpoint_id`, what gets stored per checkpoint, or how replay/time-travel and super-step boundaries work.