# Card: Merging state after parallel nodes (reducers + ordering)
**Source:** https://github.com/langchain-ai/langgraph/discussions/3914  
**Role:** explainer | **Need:** CONCEPT_EXPLAINER  
**Anchor:** How LangGraph combines state updates from parallel branches; reducer requirements; what ordering/determinism to expect.

## Key Content
- **Execution/merge model (parallel branches):**
  - When multiple nodes run “in parallel” and each returns a partial state update (a dict), LangGraph **merges updates field-by-field** using the state schema’s **reducers**.
  - **Reducer signature (Eq. 1):** `reducer(existing_value, new_value) -> updated_value`
- **Reducer annotation in typed state (procedure):**
  - Define a `TypedDict` state and annotate merge behavior with `typing.Annotated[field_type, reducer]`.
  - Example (code pattern):
    - `count: Annotated[int, operator.add]`  → updates **accumulate** (`count += delta`)
    - `data: Annotated[dict, merge_dicts]` where `merge_dicts(existing, new) = {**existing, **new}`
    - `messages: Annotated[list, add_messages]` → appends messages; `add_messages` is the recommended reducer for chat history (handles duplicates by message ID).
- **Default behavior (important):**
  - **Without a reducer**, a field update **overwrites** the existing value (last write wins), so parallel branches can appear to “not merge.”
- **Built-in reducers / common choices:**
  - `operator.add`: sums numbers / concatenates lists.
  - `operator.or_`: merges dicts (with overwrite on key conflicts).
  - Custom reducers for policies like max: `keep_max(existing, new) = max(existing, new)`.
- **Ordering expectation (design rationale):**
  - For parallel updates, **do not rely on branch completion order** for correctness; instead, make merges deterministic by using appropriate reducers (especially for lists/messages).

## When to surface
Use when students ask why outputs from two parallel nodes don’t both appear in state (especially `messages`), how LangGraph decides overwrite vs merge, or how to make parallel merges deterministic via reducers.