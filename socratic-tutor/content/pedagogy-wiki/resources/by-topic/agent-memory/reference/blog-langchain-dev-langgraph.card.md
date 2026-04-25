# Card: LangGraph = explicit cyclical state-machine graphs for agents
**Source:** https://blog.langchain.dev/langgraph/  
**Role:** explainer | **Need:** CONCEPT_EXPLAINER  
**Anchor:** Rationale + mechanics for building reliable cyclical agent runtimes via nodes + shared state (vs linear DAG chains)

## Key Content
- **Design rationale (Motivation):**
  - Traditional LangChain “chains” are effectively **DAGs**; they lack an easy way to introduce **cycles**.
  - Many production agents need an **LLM-in-a-loop** (“for-loop”) to reason about next actions (e.g., refine retrieval queries when initial RAG retrieval is poor).
  - Pure agent loops (LLM decides everything) often need **more control** in production: force specific tools first, control tool calling, vary prompts by state → treated as **state machines**.
  - **LangGraph** provides a way to specify these state machines **as graphs** with explicit control flow and termination.

- **Core abstraction: `StateGraph(State)`**
  - **State** is a central typed key-value object updated over time by nodes.
  - **State update modes:**
    - **Override**: node returns a new value for a key.
    - **Accumulate (Eq. 1):** `state[key] ← state[key] + delta` for list-like fields via `Annotated[..., operator.add]`.
      - Example: `all_actions: Annotated[List[str], operator.add]`.

- **Nodes**
  - `graph.add_node(name, runnable_or_fn)`; node input/output are dicts shaped like **State**; output dict specifies state updates.
  - Special terminal node: `END` (cycles must eventually reach END).

- **Edges / control flow**
  1. **Entry point:** `graph.set_entry_point("model")`
  2. **Normal edge:** always follow: `graph.add_edge("tools","model")`
  3. **Conditional edge (Procedure 1):**
     - `graph.add_conditional_edge(upstream, router_fn, mapping)`
     - `router_fn → str`; mapping routes e.g. `{ "end": END, "continue": "tools" }`.

- **Compilation**
  - `app = graph.compile()` → runnable supporting LangChain runnable methods (`.invoke`, `.stream`, `.astream_log`, etc.).

- **Agent state defaults (AgentExecutor recreation)**
  - `input`, `chat_history`, `agent_outcome` (`AgentAction|AgentFinish|None`), `intermediate_steps: Annotated[list[tuple[AgentAction,str]], operator.add]`.
  - Chat-style variant: `messages: Annotated[Sequence[BaseMessage], operator.add]` (nodes append messages; supports tool/function calling patterns).

## When to surface
Use when students ask why LangGraph uses **explicit graphs + shared state** for agents, how to implement **agent loops with conditional routing**, or how **state accumulation vs override** enables reliable, modifiable runtimes.