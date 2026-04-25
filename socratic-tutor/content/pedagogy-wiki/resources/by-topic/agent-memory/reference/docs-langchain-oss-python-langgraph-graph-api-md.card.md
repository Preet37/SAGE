# Card: LangGraph Graph API (StateGraph) essentials
**Source:** https://docs.langchain.com/oss/python/langgraph/graph-api.md  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Exact Python API surface for building/compiling/invoking StateGraph; state reducers (esp. `add_messages`), conditional routing, `Command`, recursion limits, runtime context.

## Key Content
- **Core model:** Graph = **State + Nodes + Edges**. *Nodes do work; edges decide next.* Execution proceeds in discrete **super-steps** (Pregel-style message passing): nodes become **active** when receiving messages; execution halts when all nodes are **inactive** and no messages are in transit.
- **Build procedure (required):**
  1) Define **State schema** (`TypedDict`, `dataclass` for defaults, or Pydantic `BaseModel`—slower).  
  2) `builder = StateGraph(State, input_schema=..., output_schema=..., context_schema=...)`  
  3) `add_node(name, fn, cache_policy=...)`  
  4) Add edges: `add_edge(src, dst)`; entry via `add_edge(START, first)`; finish via `add_edge(node, END)`  
  5) Conditional routing: `add_conditional_edges(node, routing_fn, path_map?)`  
  6) **Must compile:** `graph = builder.compile(...)` (structure checks; set runtime args like checkpointers/breakpoints/cache).
- **Reducers (state update rule):** Each key has an independent reducer; default = **overwrite**. With `Annotated[T, reducer]`, updates combine via reducer (e.g., `operator.add` for list concatenation).
- **Messages channel best practice:** Use `add_messages` reducer to append new messages **and** overwrite by message ID on updates; also **deserializes** inputs like `{"messages":[{"type":"human","content":"..."}]}` into LangChain Message objects (access via `.content`). `MessagesState` = prebuilt state with `messages: Annotated[list[AnyMessage], add_messages]`.
- **`Command` primitive:** `Command(update=..., goto=..., graph=..., resume=...)`.
  - Return from nodes/tools to combine **state update + routing** (`goto` adds dynamic edges; static edges still run).
  - Input to `invoke/stream`: **only** `Command(resume=...)` for interrupts. To continue a thread normally, pass a **plain dict** input (not `Command(update=...)`).
- **Recursion limit:** default **1000** super-steps (v1.0.6+). Set via `graph.invoke(inputs, config={"recursion_limit": 5})` (top-level config key). Step counter available at `config["metadata"]["langgraph_step"]`. `RemainingSteps` managed value enables proactive routing before `GraphRecursionError`.
- **Runtime context:** `context_schema=...`; pass via `graph.invoke(..., context={...})`; access in nodes via `runtime: Runtime[ContextSchema]`.

## When to surface
Use when students ask how to construct a LangGraph agent loop (nodes/edges/conditional routing), how state updates merge (reducers, messages), how to compile/invoke/stream correctly (incl. `Command`), or how to handle recursion limits and runtime context.