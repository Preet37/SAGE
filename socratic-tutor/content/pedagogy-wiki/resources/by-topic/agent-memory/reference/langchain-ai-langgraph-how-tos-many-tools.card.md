# Card: LangGraph many-tools (ToolNode + conditional routing)
**Source:** https://langchain-ai.github.io/langgraph/how-tos/many-tools/  
**Role:** reference_doc | **Need:** WORKING_EXAMPLE  
**Anchor:** End-to-end official pattern for scaling tool selection/routing (ToolNode + tools_condition) with runnable code structure

## Key Content
- **Tool definition (LangChain `@tool`)**
  - Type hints **required** (define input schema). Docstring becomes tool description by default.
  - Prefer **snake_case** tool names; avoid spaces/special chars for provider compatibility.
  - Customize:
    - Name: `@tool("web_search")`
    - Description: `@tool("calculator", description="...")`
  - **Reserved argument names:** `config`, `runtime` (cannot be tool args). Use `ToolRuntime` parameter instead.
- **Advanced tool schemas**
  - Use **Pydantic** via `@tool(args_schema=WeatherInput)` with fields + descriptions (e.g., `units: Literal["celsius","fahrenheit"]`, `include_forecast: bool=False`).
- **Runtime access inside tools (`ToolRuntime`)**
  - `runtime.state` (short-term state, incl. `messages`)
  - `runtime.context` (immutable invocation config; e.g., `user_id`)
  - `runtime.store` (long-term memory; namespace/key pattern like `store.get(("users",), user_id)`)
  - `runtime.stream_writer` (emit progress updates)
  - `runtime.execution_info` (thread/run IDs, attempt number)
  - `runtime.server_info` (assistant/graph/auth user when on LangGraph Server)
- **Tool return patterns**
  - Return **string** → becomes `ToolMessage`.
  - Return **object/dict** → serialized structured output.
  - Return **`Command(update=...)`** to mutate state; can include `ToolMessage(..., tool_call_id=runtime.tool_call_id)` (example sets `preferred_language`).
- **ToolNode + agent loop (core workflow)**
  - Create: `tool_node = ToolNode([search, calculator])`
  - Graph pattern:
    1. `builder = StateGraph(MessagesState)`
    2. Nodes: `"llm"`, `"tools"=ToolNode(tools)`
    3. Edges: `START -> "llm"`
    4. Conditional: `builder.add_conditional_edges("llm", tools_condition)` (routes to `"tools"` or `END`)
    5. Loop: `"tools" -> "llm"`
    6. `graph = builder.compile()`
- **ToolNode error handling defaults/options**
  - Default: catch invocation errors, re-raise execution errors.
  - `handle_tool_errors=True` (return error to LLM), string message, callable handler, or tuple of exception types.

## When to surface
Use when students ask how to (a) define many tools with schemas, (b) execute tools in LangGraph via `ToolNode`, and (c) implement the standard LLM↔tools loop using `tools_condition` conditional routing.