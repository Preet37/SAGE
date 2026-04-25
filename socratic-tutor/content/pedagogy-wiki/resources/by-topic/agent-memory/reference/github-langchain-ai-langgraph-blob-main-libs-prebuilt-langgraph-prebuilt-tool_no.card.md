# Card: ToolNode (LangGraph prebuilt tool execution + injection)
**Source:** https://github.com/langchain-ai/langgraph/blob/main/libs/prebuilt/langgraph/prebuilt/tool_node.py  
**Role:** code | **Need:** WORKING_EXAMPLE  
**Anchor:** Reference implementation of `ToolNode` (tool execution loop, tool-call parsing/dispatch, and how tool outputs are written back into graph state/messages).

## Key Content
- **Purpose/design patterns implemented** (module docstring):
  - Parallel execution of multiple tool calls (efficiency).
  - Robust error handling with customizable error messages.
  - **State injection** for tools needing graph state.
  - **Store injection** for tools needing persistent storage.
  - **Command-based state updates** for advanced control flow.
- **Core types referenced for tool calling loop**
  - Messages: `AIMessage`, `ToolCall`, `ToolMessage`, `RemoveMessage`, `convert_to_messages`.
  - Graph update primitives: `Command`, `Send`, `StreamWriter`.
  - Runtime context: `ToolRuntime` bundles `state`, `context`, `config`, `stream_writer`, `tool_call_id`, `store`.
- **Default error templates (string constants)**
  - Invalid tool name:  
    `INVALID_TOOL_NAME_ERROR_TEMPLATE = "Error: {requested_tool} is not a valid tool, try one of [{available_tools}]."`
  - Tool call error:  
    `TOOL_CALL_ERROR_TEMPLATE = "Error: {error}\n Please fix your mistakes."`
  - Execution error:  
    `TOOL_EXECUTION_ERROR_TEMPLATE = "Error executing tool '{tool_name}' with kwargs {tool_kwargs} with error:\n {error}\n Please fix the error and try again."`
  - Invocation error:  
    `TOOL_INVOCATION_ERROR_TEMPLATE = "Error invoking tool '{tool_name}' with kwargs {tool_kwargs} with error:\n {error}\n Please fix the error and try again."`
- **Tool call interception request object**
  - `ToolCallRequest` dataclass fields: `tool_call: ToolCall`, `tool: BaseTool | None`, `runtime: ToolRuntime`.
  - Direct attribute assignment is deprecated; use `ToolCallRequest.override()` (enforced via `__setattr__` warning).
- **Injected-argument detection algorithm** (`_get_all_injected_args(tool)`)
  - Collect annotations from **both** tool input schema (`tool.get_input_schema()` + `get_all_basemodel_annotations`) and function signature (`get_type_hints(..., include_extras=True)`), preferring schema annotations.
  - Detect injected keys via `_is_injected_arg_type`.
  - Runtime injection if param name is `"runtime"` **or** annotated with `ToolRuntime`.
  - Store injection if annotated with `InjectedStore`.

## When to surface
Use when students ask how LangGraph agents execute tool calls, how tool outputs/errors are formatted into messages/state, or how `InjectedState`/`InjectedStore`/`ToolRuntime` parameters are detected and injected.