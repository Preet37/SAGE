# Card: Trace LangGraph applications (observability + debugging hooks)
**Source:** https://docs.langchain.com/oss/python/langgraph/how-tos/trace-langgraph-applications/  
**Role:** reference_doc | **Need:** DEPLOYMENT_CASE  
**Anchor:** Concrete tracing/observability workflow for LangGraph runs (node-level execution, state transitions) via LangSmith; supports production debugging/reliability claims.

## Key Content
- **Install (CLI):**
  - `pip install -U langgraph`
- **Minimal “hello world” graph (run structure):**
  - Build a `StateGraph(MessagesState)` with explicit `START -> node -> END` edges, then `compile()` to a runnable graph.
  - Example node signature: `def mock_llm(state: MessagesState): return {"messages": [{"role":"ai","content":"hello world"}]}`
  - Invoke with message input: `graph.invoke({"messages": [{"role":"user","content":"hi!"}]})`
- **State schema pattern (message accumulation):**
  - Define state as `TypedDict` with `messages: Annotated[list, add_messages]`
  - **Rationale:** `add_messages()` appends to the message list rather than overwriting, preserving conversation history across node executions.
- **Streaming execution (debugging/UX):**
  - Iterate events: `for event in graph.stream({"messages":[("user", user_input)]}): ...`
  - Print latest assistant message from streamed state updates: `value["messages"][-1].content`
- **Persistence/checkpointing for reliability (durable execution):**
  - SQLite checkpointer:  
    - `from langgraph.checkpoint.sqlite import SqliteSaver`  
    - `memory = SqliteSaver.from_conn_string(":memory:")`  
    - `graph = graph_builder.compile(checkpointer=memory)`
  - **Rationale:** durable execution + resume-from-failure via persisted state.
- **Conditional routing (control-flow debugging):**
  - Conditional edges require: (1) upstream node, (2) decision function returning a string outcome, (3) mapping from outcomes to next nodes.

## When to surface
Use when students ask how to **trace/debug LangGraph execution**, interpret **runs as node/edge steps with state updates**, enable **streaming visibility**, or add **checkpointing for production reliability/resume**.