# Card: LangGraph `streamMode` (CompiledStateGraph) — modes & semantics
**Source:** https://reference.langchain.com/javascript/langchain-langgraph/index/CompiledStateGraph/streamMode  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Enumerated stream modes, what each yields, and defaults

## Key Content
- **Default:** `CompiledStateGraph.streamMode: StreamMode[]` **defaults to `["values"]`**.
- **Supported stream modes (pass to `graph.stream()` / `graph.astream()` via `streamMode`):**
  - **`"values"` → `ValuesStreamPart`:** streams the **full state snapshot after each step**.
  - **`"updates"` → `UpdatesStreamPart`:** streams **state updates after each step**; **multiple updates in the same step are streamed separately**. Output includes **node name → update** mapping.
  - **`"messages"` → `MessagesStreamPart`:** streams **2-tuples `(LLM token/messageChunk, metadata)`** from LLM calls. (Docs note message events can be emitted even when the LLM is run with `.invoke` rather than `.stream`.)
  - **`"custom"` → `CustomStreamPart`:** streams **arbitrary custom data** emitted from nodes via `config.writer(...)` / `get_stream_writer`.
  - **`"checkpoints"` → `CheckpointStreamPart`:** streams **checkpoint events** (same format as `get_state()`).
  - **`"tools"`:** streams tool-call lifecycle events: `on_tool_start`, `on_tool_event`, `on_tool_end`, `on_tool_error`.
  - **`"debug"`:** streams **all available execution info** (node name + full state; “as much information as possible”).
- **Multiple modes at once:** set `streamMode: ["updates","custom", ...]`. Stream yields **tuples `[mode, chunk]`** (mode name + that mode’s data).
- **Unified StreamPart format:** examples use `version="v2"` where each yielded item has `{ type, data, ... }`.
- **Subgraphs:** `subgraphs: true` streams outputs from nested subgraphs; chunks may include a namespace field (e.g., `ns`) to distinguish subgraph vs root.

## When to surface
Use when students ask “What does `streamMode` do?”, “What does each mode yield?”, “What’s the default?”, “How do I stream tokens/state/custom events/checkpoints/tools/debug?”, or “How do I stream multiple modes/subgraphs?”