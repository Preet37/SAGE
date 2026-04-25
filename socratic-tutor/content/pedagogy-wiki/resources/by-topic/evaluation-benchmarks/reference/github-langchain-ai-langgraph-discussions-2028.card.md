# Card: LangGraph streaming + state inspection patterns (SSE/WebSocket-adaptable)
**Source:** https://github.com/langchain-ai/langgraph/discussions/2028  
**Role:** code | **Need:** WORKING_EXAMPLE  
**Anchor:** Concrete end-to-end patterns for streaming agent execution + inspecting intermediate state (checkpoint snapshots), suitable for adapting to SSE/WebSocket event streams.

## Key Content
- **Graph “hello world” (JS/TS) procedure**
  - Define state schema with `messages: MessagesValue`.
  - Node returns state update: `return { messages: [{ role: "ai", content: "hello world" }] };`
  - Build graph: `new StateGraph(State).addNode("mock_llm", mockLlm).addEdge(START,"mock_llm").addEdge("mock_llm",END).compile();`
  - Invoke: `await graph.invoke({ messages: [{ role:"user", content:"hi!" }] });`
- **Tool-calling loop (Python) procedure**
  - State: `messages: Annotated[list, add_messages]` (reducer appends, not overwrites).
  - Bind tools: `llm_with_tools = llm.bind_tools(tools)`
  - Nodes:
    - `chatbot(state) -> {"messages":[llm_with_tools.invoke(state["messages"])]}`
    - `ToolNode(tools=[...])`
  - Control flow:
    - `add_conditional_edges("chatbot", tools_condition)` routes to tools when tool calls exist.
    - `add_edge("tools","chatbot")` returns to LLM after tool execution.
    - `add_edge(START,"chatbot")`
- **Checkpointing + intermediate state inspection**
  - Compile with checkpointer: `graph.compile(checkpointer=MemorySaver())`
  - Provide `thread_id` in `configurable` to persist/restore across calls.
  - Inspect via `StateSnapshot(...)` containing:
    - `values` (full state, incl. message history)
    - `next` (empty when at `END`)
    - `config.configurable.thread_id`, `checkpoint_id`, `checkpoint_ns`
    - `metadata.step` (example shows `step: 4`)
- **Human-in-the-loop (HIL) interrupt rationale + default constraint**
  - Tool uses `interrupt({"query": query})` and returns `human_response["data"]`.
  - **Rationale:** disable parallel tool calling to avoid repeated tool invocations on resume.
  - Enforced by: `assert len(message.tool_calls) <= 1`.

## When to surface
Use when students ask how to (a) stream/observe LangGraph execution step-by-step, (b) persist and inspect intermediate state via checkpoints/snapshots, or (c) implement resumable human-in-the-loop interrupts safely.