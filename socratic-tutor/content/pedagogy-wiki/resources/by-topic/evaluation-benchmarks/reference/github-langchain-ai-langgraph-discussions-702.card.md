# Card: LangGraph streaming + runtime config + persistence (thread_id)
**Source:** https://github.com/langchain-ai/langgraph/discussions/702  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Concrete config placement patterns + `stream_mode="events"` usage context; thread-level persistence/checkpointing patterns

## Key Content
- **Minimal StateGraph compile/invoke pattern (hello world):**
  ```py
  from langgraph.graph import StateGraph, MessagesState, START, END

  def mock_llm(state: MessagesState):
      return {"messages": [{"role": "ai", "content": "hello world"}]}

  graph = StateGraph(MessagesState)
  graph.add_node(mock_llm)
  graph.add_edge(START, "mock_llm")
  graph.add_edge("mock_llm", END)
  graph = graph.compile()

  graph.invoke({"messages": [{"role": "user", "content": "hi!"}]})
  ```
  - **Procedure:** define node(s) → connect edges `START → node → END` → `compile()` → `invoke(input_state)`.
- **Prebuilt agent invocation pattern (ReAct-style):**
  ```py
  from langgraph.prebuilt import create_react_agent

  def get_weather(city: str) -> str:
      return f"It's always sunny in {city}!"

  agent = create_react_agent(
      model="anthropic:claude-3-7-sonnet-latest",
      tools=[get_weather],
      prompt="You are a helpful assistant",
  )

  agent.invoke({"messages": [{"role": "user", "content": "what is the weather in sf"}]})
  ```
  - **Defaults/parameters shown:** `model="anthropic:claude-3-7-sonnet-latest"`, `tools=[...]`, `prompt=...`.
- **State update rule for message history (`add_messages` reducer):**
  - Merges `left` (existing messages) and `right` (new messages).
  - **If IDs match:** message in `right` **replaces** the one in `left`.
  - **Else:** messages from `right` are **appended** (append-only history).
- **Design rationale (observability/streaming):** LangGraph emphasizes durable execution + streaming + debugging/observability (LangSmith) for tracing execution paths and state transitions.

## When to surface
Use when students ask how to structure a minimal LangGraph graph/agent invocation, how message state is merged over time, or how to think about streaming/observability and thread-scoped persistence patterns (e.g., `thread_id`/checkpointing) in LangGraph.