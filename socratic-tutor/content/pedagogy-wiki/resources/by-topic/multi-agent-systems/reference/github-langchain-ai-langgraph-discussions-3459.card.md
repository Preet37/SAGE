# Card: Custom state reducers beyond `add_messages`
**Source:** https://github.com/langchain-ai/langgraph/discussions/3459  
**Role:** explainer | **Need:** CONCEPT_EXPLAINER  
**Anchor:** Concrete guidance and pointers on custom reducers beyond `add_messages`, incl. official “Reducers” concept section + state-reducers how-to.

## Key Content
- **Reducer definition (per-state-key):** Each key/channel in LangGraph `State` has an **independent reducer** that merges a node’s *update* into the prior state value.  
  - **Default reducer (override):** if no reducer specified, updates **replace** the prior value.
- **Reducer function form (Eq. 1):**  
  `new_value = reducer(old_value, update_value)`  
  - `old_value`: current state value for that key  
  - `update_value`: partial update returned by a node for that key
- **Procedure: define reducers in state schema**
  - **JS/TS (Annotation):**
    ```ts
    const State = Annotation.Root({
      bar: Annotation<string[]>({
        reducer: (state, update) => state.concat(update),
        default: () => [],
      }),
    });
    ```
  - **Python (conceptual parallel):** define a typed state schema and attach reducer logic per field (messages commonly use a prebuilt reducer).
- **Concrete behavior examples**
  - **Example A (no reducers):** input `{foo:1, bar:["hi"]}`; node returns `{foo:2}` ⇒ state `{foo:2, bar:["hi"]}`; later `{bar:["bye"]}` ⇒ `{foo:2, bar:["bye"]}` (overwrite).
  - **Example B (custom reducer for `bar`):** with `concat` reducer + default `[]`; input `{foo:1, bar:["hi"]}`; later update `{bar:["bye"]}` ⇒ `{foo:1, bar:["hi","bye"]}`.
- **Design rationale for messages reducer:** naive `concat` breaks **manual edits** (e.g., human-in-the-loop) because it always appends; `messagesStateReducer` handles **message IDs** (overwrite existing) and **deserializes** OpenAI-style `{role, content}` into LangChain `BaseMessage`.
- **Prebuilt state:** `MessagesAnnotation` / `MessagesState` provides `messages: BaseMessage[]` with `messagesStateReducer`; can be extended via `...MessagesAnnotation.spec`.

## When to surface
Use when students ask how to accumulate/merge non-message state (arrays, counters, docs) across nodes, or why messages use a special reducer instead of simple concatenation.