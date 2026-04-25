# Card: Conditional Edges & Dynamic Routing Semantics (LangGraph)
**Source:** https://github.com/langchain-ai/langgraph/discussions/3346  
**Role:** explainer | **Need:** CONCEPT_EXPLAINER  
**Anchor:** Conditional edge routing function signatures + runtime evaluation semantics (how next nodes are chosen/applied)

## Key Content
- **Node function contract (core pattern):** `node(state) -> dict` returning **partial state updates** (e.g., `{"messages": [new_msg]}`), which are merged into graph state via reducers (example uses `add_messages` to **append** rather than overwrite).
- **Conditional edge procedure (runtime routing):**
  1. Execute a node (e.g., `"chatbot"`) to produce state updates.
  2. Evaluate a **routing function** on the current input (either a messages list or a state dict containing `"messages"`).
  3. Routing function returns a **label** (e.g., `"tools"` or `END`).
  4. `add_conditional_edges(from_node, router, mapping)` interprets router outputs via an optional **mapping dict** (defaults to identity if omitted).
- **Routing function signature/semantics (example `route_tools(state)`):**
  - Accepts either:
    - `state: list` (treated as messages; uses `state[-1]`), or
    - `state: dict` with `state.get("messages", [])` (uses last message).
  - Decision rule:
    - If last AI message has attribute `tool_calls` and `len(tool_calls) > 0` ⇒ return `"tools"`
    - Else ⇒ return `END`
  - Error behavior: if no messages found ⇒ raises `ValueError("No messages found...")`.
- **Looping design rationale:** After tool execution, add a normal edge `"tools" -> "chatbot"` so the LLM can decide next step; this forms the main agent loop.
- **Default/parameter notes shown:**
  - Conditional mapping example: `{"tools": "tools", END: END}` (lets you rename targets, e.g., `"tools": "my_tools"`).
  - Human-in-the-loop tool example asserts `len(message.tool_calls) <= 1` to avoid repeated invocations on resume when interrupts/checkpointing are used.

## When to surface
Use when students ask: “How do conditional edges decide the next node?”, “What should my router return?”, “How does `add_conditional_edges` map outputs to nodes/END?”, or “How do tool-calling loops work in LangGraph?”