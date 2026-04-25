# Card: StateGraph.compile → CompiledStateGraph runtime contract
**Source:** https://reference.langchain.com/python/langgraph/graph/state/StateGraph/compile  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** `StateGraph.compile()` binds state schema + reducers into an executable `CompiledStateGraph` (Runnable) exposing `invoke/stream` and accepting `config` + `context`.

## Key Content
- **StateGraph model (runtime semantics)**
  - Nodes communicate via shared state; each node signature: **State → Partial<State>**.
  - State keys may be annotated with a **reducer** to aggregate multiple updates: **(Value, Value) → Value** (left = current value, right = update value).
- **Compile requirement**
  - `StateGraph` is a **builder** and **cannot execute** directly; must call **`.compile()`** to get an executable graph supporting: `invoke()`, `stream()`, `ainvoke()`, `astream()`.
- **`compile()` signature (Python)**
  - `compile(checkpointer=None, *, cache=None, store=None, interrupt_before=None, interrupt_after=None, debug=False, name=None) -> CompiledStateGraph`
  - Key defaults: `debug=False`, `name=None`, `checkpointer=None`.
- **Compiled graph capabilities (CompiledStateGraph)**
  - Implements **Runnable** interface: can be invoked, streamed, batched, async.
  - Core methods: `invoke`, `ainvoke`, `stream`, `astream`, plus state ops: `get_state`, `get_state_history`, `update_state`, `bulk_update_state` (bulk requires a checkpointer).
- **`invoke()` signature essentials**
  - `invoke(input, config=None, *, context=None, stream_mode="values", print_mode=(), output_keys=None, interrupt_before=None, interrupt_after=None, durability=None, **kwargs)`
  - `context` is **static run-scoped context** (added in v0.6.0) for immutable data (e.g., `user_id`, `db_conn`).
- **Reducer example (logistic map)**
  - State: `x: Annotated[list, reducer]`; reducer appends new values.
  - `compiled.invoke({"x": 0.5}, context={"r": 3.0})` ⇒ `{'x': [0.5, 0.75]}` where `next = x * r * (1 - x)`.

## When to surface
Use when students ask how LangGraph state updates are merged, what `.compile()` produces, or how to run/stream a compiled graph with `config` and run-scoped `context` (common in ReAct loops and tool-execution routing).