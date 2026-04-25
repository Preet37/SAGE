# Card: `StateGraph.compile()` (LangGraph Python)
**Source:** https://reference.langchain.com/python/langgraph/graph/state/StateGraph/compile  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Exact `StateGraph.compile()` signature/params + compiled graph is a `Runnable` (`invoke/stream/batch/async`)

## Key Content
- **Core model (StateGraph):**
  - Nodes communicate via **shared state**.
  - **Node signature:** `State -> Partial<State>` (returns an update dict merged into existing state).
  - **Optional reducers per state key:** annotate a key with a reducer to aggregate multiple updates.
    - **Reducer signature (Eq. 1):** `(Value, Value) -> Value` (left/current, right/update).
- **Must compile to execute:** `StateGraph` is a **builder**; call `.compile()` to get an executable graph supporting `invoke()`, `stream()`, `ainvoke()`, `astream()`.
- **`compile()` signature (Python):**
  ```python
  compile(
    checkpointer: Checkpointer = None,
    *,
    cache: BaseCache | None = None,
    store: BaseStore | None = None,
    interrupt_before: All | list[str] | None = None,
    interrupt_after: All | list[str] | None = None,
    debug: bool = False,
    name: str | None = None,
  ) -> CompiledStateGraph[StateT, ContextT, InputT, OutputT]
  ```
  - **Defaults:** `checkpointer=None`, `cache=None`, `store=None`, `interrupt_before=None`, `interrupt_after=None`, `debug=False`, `name=None`.
  - **Return:** `CompiledStateGraph` implementing **Runnable** (invokable, streamable, batchable, async).
- **Execution flow procedure (Quickstart):**
  1. Define `State` schema (e.g., `TypedDict`).
  2. Write node functions returning partial updates.
  3. Add nodes + edges (`START` → …).
  4. `app = graph.compile()` then `app.invoke(initial_state)`.
- **Conditional looping example:** `add_conditional_edges("increment", should_continue)` where `should_continue` returns `"increment"` until `count < 3`, else `END`; result reaches `count: 3`.

## When to surface
Use when students ask how to **run** a `StateGraph`, what `.compile()` accepts/returns, how **reducers** merge state updates, or how to configure **interrupts/debug/checkpointing** for execution.