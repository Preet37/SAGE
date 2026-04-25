# Card: `stream_mode="updates"` can miss tool messages when tools return `Command`
**Source:** https://github.com/langchain-ai/langgraph/issues/2831  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Edge-case semantics for `stream_mode="updates"` with multi-tool calls + tools returning `Command(update=...)`

## Key Content
- **Repro setup (LangGraph ReAct agent):**
  - Build tools `add` and `sub`; create agent via `create_react_agent(model, tools=tools, checkpointer=MemorySaver())`.
  - Stream with:
    - `agent.stream(input={"messages":[("user","add(1,1), add(1,2), add(1,3) at once")]}, config={"configurable":{"thread_id":"1"}}, stream_mode="updates")`
- **Tool return patterns compared:**
  - `add` tool returns a **Command**:
    - **Eq. 1 (Command update):**  
      `Command(update={"messages":[ToolMessage(f"add result: {result}", tool_call_id=tool_call_id)]})`  
      where `result = a + b`, and `tool_call_id` is injected via `Annotated[str, InjectedToolCallId]`.
  - `sub` tool returns a **plain string**: `return f"sub result: {result}"` (note: code shows `result = a + b` even though tool is named `sub`).
- **Observed streaming behavior (empirical):**
  - When the LLM issues **multiple tool calls at once** (3 `add` calls), `stream_mode="updates"` emits:
    - an `agent` update containing **3 tool_calls**,
    - then a `tools` update containing **only 1 ToolMessage**: `add result: 4` (the last call’s message),
    - then final `agent` response.
  - For `sub` (string return), the `tools` update contains **all 3 ToolMessages** in one chunk: `sub result: 2`, `sub result: 3`, `sub result: 4`.
- **State vs stream discrepancy:**
  - `agent.get_state(config).values["messages"]` shows **all ToolMessages** for `add` (2, 3, 4) even though streaming only showed the last one.

## When to surface
Use when students ask why `stream_mode="updates"` doesn’t show all tool outputs, especially with **parallel/multi tool_calls** and tools that return `Command(update=...)`, and how to verify via `get_state()`.