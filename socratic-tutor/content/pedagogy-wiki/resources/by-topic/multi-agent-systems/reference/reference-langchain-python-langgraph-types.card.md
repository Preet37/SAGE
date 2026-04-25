# Card: LangGraph Runtime Types (interrupts, streaming, state snapshots)
**Source:** https://reference.langchain.com/python/langgraph/types/  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Canonical type definitions that constrain what nodes can return/raise and what the runner expects (interrupts, streaming, checkpointing, dynamic sends, state snapshots).

## Key Content
- **Interrupting execution (HITL)**
  - `interrupt(value: Any) -> Any`: first call **raises `GraphInterrupt`** and surfaces `value` to the client; graph later resumes via `Command(resume=...)` and **re-executes the node from the start**.
  - Multiple `interrupt()` calls in one node: resume values are matched **by call order**, scoped **per task** (not shared across tasks).
  - **Requires checkpointing enabled** (interrupt relies on persisted state).
  - Interrupt info surfaced in stream as `{'__interrupt__': (Interrupt(value=..., id=...),)}`.
- **Checkpoint configuration**
  - `Checkpointer = None | bool | BaseCheckpointSaver`
    - `True`: enable persistent checkpointing for subgraph
    - `False`: disable even if parent has one
    - `None`: inherit from parent
- **Streaming modes**
  - `StreamMode = Literal["values","updates","checkpoints","tasks","debug","messages","custom"]`
    - `"values"`: emit full state after each step (incl. interrupts)
    - `"updates"`: emit node/task names + returned updates (each update separately if multiple in a step)
    - `"messages"`: token-by-token LLM messages + metadata
    - `"checkpoints"`: emit when checkpoint created (format like `get_state()`)
    - `"tasks"`: task start/finish + results/errors
    - `"debug"`: includes `"checkpoints"` + `"tasks"`
    - `"custom"`: emit via `StreamWriter`
  - `StreamWriter = Callable[[Any], None]`: injected kwarg; **no-op unless** `stream_mode="custom"`.
- **Retry defaults (`RetryPolicy`, v0.2.24)**
  - `initial_interval=0.5s`, `backoff_factor=2.0`, `max_interval=128.0s`, `max_attempts=3`, `jitter=True`.
- **Caching (`CachePolicy`)**
  - `key_func` default: `default_cache_key` (hashes input via pickle).
- **Dynamic fan-out**
  - `Send(node: str, arg: Any)`: used in conditional edges to invoke a node next step with **custom per-send state** (map-reduce style).
- **State snapshot structure (`StateSnapshot`)**
  - `next: tuple[str,...]`, `config: RunnableConfig`, `metadata: CheckpointMetadata|None`, `parent_config: RunnableConfig|None`, `tasks: tuple[PregelTask,...]`.
- **Reducer bypass**
  - `Overwrite(value=...)`: bypass `BinaryOperatorAggregate` reducer; multiple `Overwrite` to same channel in one super-step ⇒ `InvalidUpdateError`.

## When to surface
Use when students ask what node functions may return/raise, how interrupts/resume work, how to configure streaming/checkpointing/retries, or how to fan-out tasks with `Send` / override reducers with `Overwrite`.