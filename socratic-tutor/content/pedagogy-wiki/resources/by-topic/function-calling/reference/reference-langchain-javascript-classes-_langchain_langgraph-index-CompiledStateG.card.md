# Card: CompiledStateGraph runtime contract (LangGraph JS)
**Source:** https://reference.langchain.com/javascript/classes/_langchain_langgraph.index.CompiledStateGraph.html  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Compiled graph runtime contract in JS: invoke/stream signatures, config handling, and what the compiled artifact exposes

## Key Content
- **What it is:** `CompiledStateGraph` is the **final artifact** produced by `StateGraph.compile()` (should not be instantiated directly). Version **v1.2.8**, **since v0.3**.
- **Primary execution APIs**
  - `invoke(input, config?) → Promise<ExtractStateType<O, O>>`: run graph once with a single input + optional per-call config override.
  - `stream(input, config?) → Promise<IterableReadableStream<StreamOutputMap<...>>>`: real-time execution stream.
  - `streamEvents() → IterableReadableStream<StreamEvent>`: stream event objects.
- **Streaming defaults & modes**
  - `streamMode: StreamMode[]` default = `["values"]`.
  - Supported modes (doc list):  
    - `"values"` full state after each step  
    - `"updates"` state deltas after each step  
    - `"messages"` messages emitted inside nodes  
    - `"custom"` custom node events  
    - `"tools"` tool-call lifecycle events (`on_tool_start`, `on_tool_event`, `on_tool_end`, `on_tool_error`)  
    - `"debug"` execution/debug events  
    - (also mentioned under `stream`): `"checkpoints"`, `"tasks"`
  - `streamChannels` optional; if omitted, **all channels** streamed.
- **Config & immutability**
  - `config: LangGraphRunnableConfig` is the **default execution config**, overridable per invocation.
  - `withConfig(newConfig) → CompiledStateGraph`: returns a **new instance** with merged config (immutable pattern).
- **State persistence / HITL**
  - `checkpointer: boolean | BaseCheckpointSaver`: if provided, checkpoints **every superstep**; if `false/undefined`, no save/restore.
  - `getState()`, `getStateHistory()`, `updateState()` **require a checkpointer**.
  - `interruptBefore` / `interruptAfter`: `"*"` or `"__start__"` or `N[]` node names for human-in-the-loop breakpoints.
- **Other key knobs:** `autoValidate` default `true`; `debug` default `false`; `retryPolicy`; `stepTimeout` (ms per superstep); optional `cache`; optional long-term `store`.

## When to surface
Use when students ask how to **run/stream a compiled LangGraph**, choose **stream modes**, override **runtime config**, or implement **checkpointing + interrupts** for iterative ReAct/tool loops.