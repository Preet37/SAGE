# Card: LangGraph StateGraph + runtime controls (invoke/stream/interrupt/durability)
**Source:** https://reference.langchain.com/python/langgraph/graphs/  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Graph execution semantics + runtime knobs (invoke/stream/interrupt/durability/context); StateGraph structure for iterative agent loops

## Key Content
- **Core abstraction (StateGraph):** Nodes communicate via shared **state**. Each node signature: **State → Partial\<State\>** (returns only updated keys). State keys may be `Annotated[..., reducer]` where reducer aggregates multiple node writes: **reducer(Value_left, Value_right) → Value**.
- **Reducer example (list append):**  
  `def reducer(a: list, b: int | None) -> list: return a + [b] if b is not None else a`
- **Context (immutable runtime data):** Provide via `context_schema` and pass at run time: `compiled.invoke(input, context={...})`. Node can accept `runtime: Runtime[Context]` and read `runtime.context.get("r", 1.0)`.
- **Worked numeric example (logistic map step):**  
  **Eq. 1:** `next_value = x * r * (1 - x)` where `x = state["x"][-1]`, `r = runtime.context["r"]`.  
  With input `{"x": 0.5}` and `context={"r": 3.0}`, output becomes `{'x': [0.5, 0.75]}` (since 0.5·3·0.5 = 0.75) using list reducer.
- **Graph construction procedures:**
  - `add_node(name?, fn)` (if name omitted, inferred from callable name).
  - `add_edge(start_key | [start_keys], end_key)`; multiple start keys = wait for **ALL** to complete.
  - `add_conditional_edges(source, path, path_map?)`; if `path` returns **END**, graph stops.
  - `compile(checkpointer=None, interrupt_before=None, interrupt_after=None, debug=False, name=None) → CompiledStateGraph`.
- **Run-time knobs (CompiledStateGraph):**
  - `invoke/ainvoke(..., stream_mode="values", output_keys=None, interrupt_before=None, interrupt_after=None, durability=None)`
  - `stream/astream(..., stream_mode=None)` modes: `"values"`, `"updates"`, `"custom"`, `"messages"` (token stream as `(token, metadata)`), `"checkpoints"`, `"tasks"`, plus `"debug"` in `astream`.
  - `durability` options: `"sync"`, `"async"` (default), `"exit"`.

## When to surface
Use when students ask how to build/compile a LangGraph StateGraph for an iterative ReAct loop, how conditional routing/END works, or how to control execution via `context`, `stream_mode`, `interrupt_before/after`, and `durability`.