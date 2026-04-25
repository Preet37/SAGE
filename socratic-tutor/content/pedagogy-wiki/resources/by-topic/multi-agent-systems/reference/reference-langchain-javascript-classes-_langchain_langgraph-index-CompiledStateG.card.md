# Card: CompiledStateGraph runtime surface (JS)
**Source:** https://reference.langchain.com/javascript/classes/_langchain_langgraph.index.CompiledStateGraph.html  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Methods/properties on the compiled graph artifact (invoke/stream/batch/state/checkpointing/interrupts/config)

## Key Content
- **What it is:** `CompiledStateGraph` is the **final result** of building + compiling a `StateGraph`; **do not instantiate directly**—create via `StateGraph.compile()`. (Since v0.3; docs shown for v1.2.8)
- **Core execution methods**
  - `invoke(): Promise<ExtractStateType<O, O>>` — run graph once with input + config; returns **final output state** (per `outputChannels`).
  - `batch(): Promise<OperationResults<Op>>` — execute multiple operations in one batch (more efficient than individual runs).
  - `stream(): Promise<IterableReadableStream<StreamOutputMap<...>>>` — primary real-time observation API; emits per enabled `streamMode`.
  - `streamEvents(): IterableReadableStream<StreamEvent>` — stream runnable events.
- **Streaming defaults & modes**
  - `streamMode: StreamMode[]` **defaults to `["values"]`**.
  - Supported modes listed: `"values"` (full state each step), `"updates"` (state changes), `"messages"`, `"custom"`, `"tools"` (tool lifecycle events), `"debug"` (execution tracing). (`stream()` docs also mention `"checkpoints"` and `"tasks"` as streamable event types.)
  - `streamChannels` optional; **if not specified, all channels are streamed**.
- **State persistence / HITL**
  - `checkpointer: boolean | BaseCheckpointSaver<number>` — when provided, **saves a checkpoint at every superstep**; when `false/undefined`, checkpointing disabled and graph **cannot save/restore**.
  - `getState(): Promise<StateSnapshot>` and `getStateHistory(): AsyncIterableIterator<StateSnapshot>` **require a checkpointer**.
  - `updateState(): Promise<RunnableConfig<...>>` — update graph state (requires checkpointer); used for **human-in-the-loop**, breakpoints, external inputs.
  - Interrupt controls: `interruptBefore` / `interruptAfter`: `"*"` or `"__start__"` or `N[]` (node names) to interrupt around nodes.
- **Validation/config defaults**
  - `autoValidate: boolean` **defaults to `true`** (validate structure at compile).
  - `debug: boolean` **defaults to `false`**.
  - `withConfig(...)` returns a **new instance** (immutable merge pattern).
  - `validate(): this` checks: **no orphaned nodes**, valid input/output channels, valid interrupt configs.
- **Graph introspection**
  - `getGraph()` / `getGraphAsync()` return a **drawable** `Graph`.
  - `getSubgraphsAsync()` yields nested Pregel subgraphs (also deprecated sync `getSubgraphs()`).

## When to surface
Use when students ask how to **run** a compiled LangGraph (single/batch/stream), how **streaming modes** work and their defaults, or how to enable **checkpointing, state inspection/history, interrupts, and HITL state updates**.