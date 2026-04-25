# Card: Durable execution + interrupt/resume + state updates (LangGraph #4730)
**Source:** https://github.com/langchain-ai/langgraph/discussions/4730  
**Role:** explainer | **Need:** CONCEPT_EXPLAINER  
**Anchor:** Concrete edge-case behavior context: state persistence + interrupt/resume patterns (esp. around human-in-the-loop) and how state is updated via reducers; pointers to subgraph concepts for nested graphs.

## Key Content
- **LangGraph core model (Graphs as control flow):**
  - **State** = shared snapshot passed to nodes; defined as `TypedDict`/Pydantic + **reducers** that specify how updates apply.
  - **Nodes**: functions `node(state) -> dict` emitting partial state updates.
  - **Edges**: determine next node(s); can be conditional or fixed.
  - Runtime proceeds in discrete **“super-steps”** (Pregel-inspired): nodes execute, emit messages along edges; execution halts when all nodes are inactive and no messages are in transit.
- **Reducer formula (state update rule):**
  - For key `messages` with reducer `add_messages`: **append** new messages rather than overwrite.  
    Example reducer shown: `messages: Annotated[list, lambda x, y: x + y]` where `x`=prior list, `y`=new list.
  - Keys **without** reducer annotations **overwrite** previous values.
- **Durable execution / memory procedure (checkpointing):**
  1. Compile graph with a `checkpointer` (example: `memory = MemorySaver(); graph = builder.compile(checkpointer=memory)`).
  2. Invoke with `configurable.thread_id` to persist/load state across calls.
  3. State is saved after each step; later invocations with same `thread_id` resume from saved checkpoint.
- **Human-in-the-loop procedure (interrupt/resume):**
  - Tool uses `interrupt({"query": query})` and returns `human_response["data"]`.
  - **Design rationale:** disable parallel tool calling when interrupts can occur to avoid repeating tool invocations on resume: `assert len(message.tool_calls) <= 1`.
- **Defaults/parameters shown:**
  - `TavilySearch(max_results=2)`
  - Example recursion limit usage: `graph.invoke(..., {"recursion_limit": 10})`.

## When to surface
Use when students ask how LangGraph persists state across runs, how `interrupt()` pauses/resumes execution safely, how reducers control state merging (append vs overwrite), or how to avoid duplicated tool calls after resume (parallel tool calling constraint).