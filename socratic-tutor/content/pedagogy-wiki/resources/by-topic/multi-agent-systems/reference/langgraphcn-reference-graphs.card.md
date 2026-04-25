# Card: LangGraph StateGraph node signature + reducers
**Source:** https://www.langgraphcn.org/reference/graphs/  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Explicit node signature `State -> Partial<State>` and per-key reducer annotation semantics

## Key Content
- **Core abstraction (StateGraph):** Nodes communicate by **reading/writing a shared state**.
- **Node signature (Eq. 1):**  
  **`node: State -> Partial<State>`**  
  Meaning: each node receives the full current `State` and returns a **dict of updates** (a “partial” state) containing only keys it wants to write.
- **Per-key reducers (Eq. 2):**  
  Each state key may be annotated with a **reducer** used to aggregate multiple node updates to that key in the same step.  
  **Reducer signature:** **`reducer: (Value, Value) -> Value`**  
  Used when multiple nodes emit updates for the same key; reducer combines them into one value.
- **Reducer annotation mechanism:** Use `typing_extensions.Annotated` in a `TypedDict` state schema, e.g.  
  `x: Annotated[list, reducer]` (state key `x` is a list aggregated via `reducer`).
- **Edge execution rule:** `add_edge(start_key: str | list[str], end_key: str)`  
  - Single `start_key`: downstream runs after that node completes.  
  - Multiple `start_key` list: downstream waits for **ALL** listed start nodes to complete.
- **Compilation result:** `compile()` returns `CompiledStateGraph` implementing `Runnable` with methods like `invoke`, `stream`, `ainvoke`, `astream`.
- **Streaming modes (enumeration):** `StreamMode ∈ {"values","updates","debug","messages","custom"}`  
  - `"values"`: emit full state after each step  
  - `"updates"`: emit per-node updates/events

## When to surface
Use when students ask: “What should a LangGraph node return?”, “How does LangGraph merge concurrent updates to the same state key?”, or “What happens when an edge has multiple start nodes / how does execution order work?”