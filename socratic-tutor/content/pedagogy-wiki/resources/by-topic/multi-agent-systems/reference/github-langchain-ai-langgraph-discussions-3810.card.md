# Card: Atomic message replacement vs reducers (LangGraph StateGraph)
**Source:** https://github.com/langchain-ai/langgraph/discussions/3810  
**Role:** explainer | **Need:** API_REFERENCE  
**Anchor:** Node return-type rules + reducer semantics (replace vs append) + replay/idempotency implications

## Key Content
- **StateGraph contract (Core rule):** Each node reads **State** and returns a **Partial\<State\>** update. Returned keys are merged into shared state.
- **Reducer semantics (per-key aggregation):** A state key can be annotated with a reducer used to combine multiple updates.  
  **Reducer signature (Eq. 1):** `reducer(left: Value, right: UpdateValue) => Value`  
  - `left` = current accumulated state value  
  - `right` = node’s returned update for that key
- **Append-style messages reducer (example):**  
  `messages: Annotation<BaseMessage[]>({ reducer: (left, right) => left.concat(Array.isArray(right) ? right : [right]), default: () => [] })`  
  **Default:** `messages` starts as `[]`.
- **Implication for “replace history atomically”:** If `messages` uses an **append reducer**, returning `{"messages": [...]}` will **append**, not overwrite. To **overwrite/replace**, define `messages` with a reducer that **returns `right` as the new value** (i.e., replacement reducer) so the update is atomic at the state-key level.
- **Idempotency / replay rationale:** Durable execution + retries/replay can re-run nodes; **append reducers can duplicate messages** on re-execution. Replacement reducers (or otherwise idempotent update logic) avoid duplication by making the update deterministic for a given run.
- **Execution workflow:** Build graph (`addNode`, `addEdge(START, node)`, `addEdge(node, END)`), then **must call** `.compile()` before `.invoke()`.

## When to surface
Use when a student asks why messages are duplicating, how reducers affect state updates, or how to safely overwrite message history (especially under retries/replay/checkpointed execution).