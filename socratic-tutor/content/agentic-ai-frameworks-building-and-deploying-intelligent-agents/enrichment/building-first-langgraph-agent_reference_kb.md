## Core Definitions

**LangGraph state** — In LangGraph’s Graph API, a graph is defined by **State + Nodes + Edges**: nodes “do work” by reading the current state and returning **partial state updates**, and edges determine which node runs next. Execution proceeds in discrete **super-steps** (Pregel-style): nodes become active when they receive messages; the run halts when all nodes are inactive and no messages are in transit. (LangGraph Graph API essentials: https://docs.langchain.com/oss/python/langgraph/graph-api.md)

**State schema (TypedDict / dataclass / Pydantic)** — A LangGraph `StateGraph` is parameterized by a typed state object (commonly a `TypedDict`). Each node has the contract **State → Partial<State>** (returns only updated keys). State keys can be annotated with reducers to define how multiple updates merge. (Graph API essentials: https://docs.langchain.com/oss/python/langgraph/graph-api.md; StateGraph runtime reference: https://reference.langchain.com/python/langgraph/graphs/)

**Reducer (state update rule)** — Each state key has an independent reducer that merges the “current value” (left) with an “update value” (right). Default behavior is **overwrite**. With `Annotated[T, reducer]`, updates combine via the reducer (e.g., `operator.add` for list concatenation). (Graph API essentials: https://docs.langchain.com/oss/python/langgraph/graph-api.md; compile/runtime contract: https://reference.langchain.com/python/langgraph/graph/state/StateGraph/compile)

**`add_messages` reducer** — LangGraph’s recommended reducer for a `messages` channel. It appends new messages and can overwrite by message ID on updates; it also deserializes inputs like `{"messages":[{"type":"human","content":"..."}]}` into LangChain Message objects (read via `.content`). (Graph API essentials: https://docs.langchain.com/oss/python/langgraph/graph-api.md)

**`MessagesState`** — A prebuilt state schema provided by LangGraph: `messages: Annotated[list[AnyMessage], add_messages]`. It’s the standard state for chat/tool agents because it accumulates conversation history across node executions. (Graph API essentials: https://docs.langchain.com/oss/python/langgraph/graph-api.md; tracing how-to shows the same pattern: https://docs.langchain.com/oss/python/langgraph/how-tos/trace-langgraph-applications/)

**Tool calling (function calling)** — A multi-step interaction where the model emits a structured request to call a tool (with arguments), the application executes the tool, then returns the tool output to the model so it can continue (possibly calling more tools) or produce a final answer. OpenAI describes a 5-step loop: request with tools → receive tool call(s) → execute → send tool outputs → receive final response (or more calls). (OpenAI function calling guide: https://platform.openai.com/docs/guides/function-calling)

**ToolNode** — A LangGraph prebuilt node that executes tool calls found in the latest AI message, supports parallel execution of multiple tool calls, robust error handling, and injection of runtime/state/store into tools. Tool outputs are written back as tool messages (or `Command` updates for advanced control). (ToolNode implementation reference: https://github.com/langchain-ai/langgraph/blob/main/libs/prebuilt/langgraph/prebuilt/tool_node.py; many-tools how-to: https://langchain-ai.github.io/langgraph/how-tos/many-tools/)

**Conditional routing / conditional edges** — A graph control-flow mechanism: `add_conditional_edges(upstream_node, routing_fn, path_map?)`. The routing function inspects state and returns an outcome (often a string) that maps to the next node (or `END` to stop). This is the core of the “agent loop” (LLM decides whether to call tools; router sends to tools or ends). (Graph API essentials: https://docs.langchain.com/oss/python/langgraph/graph-api.md; many-tools how-to: https://langchain-ai.github.io/langgraph/how-tos/many-tools/)

**Graph compilation** — `StateGraph` is a builder and cannot execute until you call `.compile()`, which produces a `CompiledStateGraph` (a LangChain Runnable) supporting `.invoke()`, `.stream()`, async variants, and (with a checkpointer) state history operations. Compilation also performs structure checks and binds runtime options like checkpointers/interrupts/debug. (Compile reference: https://reference.langchain.com/python/langgraph/graph/state/StateGraph/compile; Graph API essentials: https://docs.langchain.com/oss/python/langgraph/graph-api.md)

**Agent loop (in LangGraph)** — A cyclical state machine where an LLM node appends an AI message (possibly containing tool calls), a conditional edge routes either to a tool execution node or to `END`, and tool results are appended as tool messages before looping back to the LLM node. LangGraph’s motivation is to make these cycles explicit and controllable (vs. linear DAG “chains”). (LangGraph rationale blog: https://blog.langchain.dev/langgraph/; many-tools how-to: https://langchain-ai.github.io/langgraph/how-tos/many-tools/)

**`Command`** — A LangGraph primitive that can combine state updates with dynamic routing: `Command(update=..., goto=..., graph=..., resume=...)`. Nodes/tools can return `Command` to mutate state and/or choose the next node. For interrupts, `invoke/stream` accepts `Command(resume=...)` only; to continue normally, pass a plain dict input (not `Command(update=...)`). (Graph API essentials: https://docs.langchain.com/oss/python/langgraph/graph-api.md)

**LangChain integration (Runnable interface)** — A compiled LangGraph app is a LangChain Runnable: it supports `.invoke`, `.stream`, `.ainvoke`, `.astream`, etc. This is why you can treat the graph like any other LangChain component in pipelines and tracing. (LangGraph rationale blog: https://blog.langchain.dev/langgraph/; compile reference: https://reference.langchain.com/python/langgraph/graph/state/StateGraph/compile)

---

## Key Formulas & Empirical Results

**Recursion limit (super-step cap)** — LangGraph has a default recursion limit of **1000 super-steps** (v1.0.6+). You can set it per run via:
```python
graph.invoke(inputs, config={"recursion_limit": 5})
```
The current step counter is available at `config["metadata"]["langgraph_step"]`. (Graph API essentials: https://docs.langchain.com/oss/python/langgraph/graph-api.md)

**Tool calling reliability default (temperature)** — In function-calling evaluations, Databricks reports tool-call accuracy can vary by ~**10%** depending on decoding, and **temperature 0.0** is usually best for programmatic tool calling. (Databricks function-calling evals: https://www.databricks.com/blog/unpacking-function-calling-eval)

**Tool inventory size heuristic** — Gemini docs recommend keeping active tools around **10–20** for best results. OpenAI’s function calling guide notes tool definitions count as input tokens and suggests keeping initial tools small (soft suggestion: **<20**) or using tool search (gpt-5.4+). (Gemini function calling: https://ai.google.dev/gemini-api/docs/function-calling; OpenAI function calling: https://platform.openai.com/docs/guides/function-calling)

**ToolNode default error templates (exact strings)** — ToolNode defines default error message templates, e.g. invalid tool name:
> `"Error: {requested_tool} is not a valid tool, try one of [{available_tools}]."`
and execution error:
> `"Error executing tool '{tool_name}' with kwargs {tool_kwargs} with error:\n {error}\n Please fix the error and try again."`
(ToolNode source: https://github.com/langchain-ai/langgraph/blob/main/libs/prebuilt/langgraph/prebuilt/tool_node.py)

---

## How It Works

### A. Minimal “first agent” control flow (LLM ↔ tools loop)

1) **Define tools** (LangChain `@tool`)
   - Type hints are required to define the input schema; docstring becomes description by default.
   - Prefer snake_case tool names for provider compatibility. (Many-tools how-to: https://langchain-ai.github.io/langgraph/how-tos/many-tools/)

2) **Bind tools to the chat model**
   - In LangChain, you typically do `model.bind_tools(tools)` so the model can emit tool calls in its response. (Call-tools quickstart: https://docs.langchain.com/oss/python/langgraph/call-tools)

3) **Define state**
   - Use `MessagesState` (prebuilt) or define your own `TypedDict` with:
     - `messages: Annotated[list[AnyMessage], add_messages]` (or `operator.add` in some quickstarts)
   - The reducer ensures messages accumulate across steps. (Graph API essentials: https://docs.langchain.com/oss/python/langgraph/graph-api.md; quickstart: https://docs.langchain.com/oss/python/langgraph/quickstart)

4) **Create a `StateGraph(State)` builder**
   ```python
   builder = StateGraph(MessagesState)
   ```
   (Many-tools how-to: https://langchain-ai.github.io/langgraph/how-tos/many-tools/)

5) **Add nodes**
   - **LLM node**: reads `state["messages"]`, calls the model, returns `{"messages": [ai_msg]}` (and any other counters you track).
   - **Tool node**: either:
     - Use `ToolNode(tools)` (recommended), or
     - Write your own node that iterates `state["messages"][-1].tool_calls` and returns `ToolMessage`s. (Many-tools how-to; call-tools quickstart)

6) **Add edges**
   - `START -> "llm"`
   - Conditional edges out of `"llm"`:
     - If the last AI message contains tool calls, route to `"tools"`
     - Else route to `END`
   - `"tools" -> "llm"` to continue the loop. (Many-tools how-to: https://langchain-ai.github.io/langgraph/how-tos/many-tools/)

7) **Compile**
   ```python
   graph = builder.compile()
   ```
   Compilation is required to execute; it returns a Runnable. (Compile reference: https://reference.langchain.com/python/langgraph/graph/state/StateGraph/compile)

8) **Invoke**
   - Provide initial messages as input:
     ```python
     graph.invoke({"messages": [{"role": "user", "content": "..." }]})
     ```
   - `add_messages` will deserialize dicts into message objects. (Graph API essentials; tracing how-to)

---

### B. What ToolNode does mechanically (high-level)

When the `"tools"` node runs (ToolNode):

1) It inspects the latest AI message for tool calls (`ToolCall` objects).
2) For each tool call:
   - Finds the matching tool by name.
   - Builds a `ToolRuntime` containing `state`, `context`, `config`, `stream_writer`, `tool_call_id`, and optionally `store`.
   - Injects runtime/state/store into tool parameters when the tool signature/schema requests it (ToolNode supports injected args detection). (ToolNode source)
3) Executes tool calls (supports parallel execution).
4) Writes results back as `ToolMessage`s (or uses `Command(update=...)` if the tool returns a `Command`). (ToolNode source; many-tools how-to)

---

### C. Conditional routing mechanics

- `add_conditional_edges(node, routing_fn, path_map?)`:
  - `routing_fn(state) -> outcome`
  - If `path_map` is provided, LangGraph maps `outcome` to a destination node.
  - If the outcome is `END`, the graph stops. (Graph API essentials; graphs runtime reference)

This is the key “agent behavior is explicit control flow” insight: the LLM doesn’t magically loop—**you** define the loop edge and the stop condition.

---

## Teaching Approaches

### Intuitive (no math)
An “agent” here is just:
- a shared notebook (`state`) where we keep the conversation (`messages`), and
- a flowchart (`graph`) that says:
  1) ask the model what to do next,
  2) if it asked for a tool, run the tool and write the result into the notebook,
  3) repeat until the model stops asking for tools.

This matches LangGraph’s motivation: production agents need explicit, inspectable loops rather than hidden behavior. (https://blog.langchain.dev/langgraph/)

### Technical (with precise runtime terms)
LangGraph executes a `StateGraph` in super-steps. Each node is a function `State → Partial<State>`. State keys merge via reducers (default overwrite; `add_messages` for message accumulation). Conditional edges implement a state-machine transition function. The standard agent loop is a cycle between an LLM node and a ToolNode, with a conditional edge from the LLM node to either ToolNode or `END`. (Graph API essentials; many-tools how-to)

### Analogy-based
Think of the LLM as a “manager” who can either:
- answer directly (end the workflow), or
- write a work order (“tool call”) for a specialist.
ToolNode is the dispatch desk that reads the work orders, calls the specialists, and files the results back into the shared case folder (`messages`). The conditional edge is the rule: “If there’s a work order, dispatch; otherwise close the case.” (Many-tools how-to; OpenAI tool calling loop)

---

## Common Misconceptions

1) **“LangGraph agents are just LangChain agents with a different name; the loop is implicit.”**  
   - **Why wrong:** LangGraph’s core design is explicit control flow: you define nodes and edges (including cycles) and a termination route to `END`. The loop exists only if you add the cycle (`tools -> llm`) and conditional routing. (https://blog.langchain.dev/langgraph/; https://langchain-ai.github.io/langgraph/how-tos/many-tools/)  
   - **Correct model:** “Agent behavior” = explicit state-machine transitions over shared state.

2) **“If my node returns `{'messages': [...]}`, it replaces the whole message history.”**  
   - **Why wrong:** With `messages: Annotated[..., add_messages]` (or `operator.add` in some examples), message updates are **appended/merged**, not overwritten. (Graph API essentials; tracing how-to)  
   - **Correct model:** Reducers define merge semantics per key; `add_messages` accumulates conversation.

3) **“I can run a `StateGraph` without compiling it.”**  
   - **Why wrong:** `StateGraph` is a builder; you must call `.compile()` to get a `CompiledStateGraph` that supports `.invoke()`/`.stream()`. (https://reference.langchain.com/python/langgraph/graph/state/StateGraph/compile)  
   - **Correct model:** Build (structure) → compile (validate + bind runtime) → invoke/stream (execute).

4) **“Tool calling means the model executes my Python function.”**  
   - **Why wrong:** Tool calling is a protocol: the model emits a structured tool call; **your application** executes it and returns the output. OpenAI explicitly describes this multi-step exchange. (https://platform.openai.com/docs/guides/function-calling)  
   - **Correct model:** Model proposes actions; the runtime executes actions; results are fed back as messages.

5) **“If I hit an infinite loop, it will just run forever.”**  
   - **Why wrong:** LangGraph enforces a recursion limit (default 1000 super-steps) and you can lower it via `config={"recursion_limit": ...}`. (Graph API essentials)  
   - **Correct model:** Cycles must be designed to reach `END`; recursion limit is a safety backstop.

---

## Worked Examples

### Example 1 — Standard LLM ↔ ToolNode agent loop (official pattern)

This mirrors the official “many-tools” pattern: `MessagesState` + `"llm"` node + `ToolNode` + `tools_condition` routing. (https://langchain-ai.github.io/langgraph/how-tos/many-tools/)

```python
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import MessagesState
from langgraph.prebuilt import ToolNode, tools_condition

from langchain.chat_models import init_chat_model
from langchain.tools import tool

# 1) Tools
@tool
def add(a: int, b: int) -> int:
    """Add two integers."""
    return a + b

@tool
def multiply(a: int, b: int) -> int:
    """Multiply two integers."""
    return a * b

tools = [add, multiply]

# 2) Model with tools
model = init_chat_model("claude-sonnet-4-6", temperature=0)
model_with_tools = model.bind_tools(tools)

# 3) Nodes
def llm_node(state: MessagesState):
    # state["messages"] is a list of LangChain message objects
    msg = model_with_tools.invoke(state["messages"])
    return {"messages": [msg]}

tool_node = ToolNode(tools)

# 4) Graph
builder = StateGraph(MessagesState)
builder.add_node("llm", llm_node)
builder.add_node("tools", tool_node)

builder.add_edge(START, "llm")
builder.add_conditional_edges("llm", tools_condition)  # routes to "tools" or END
builder.add_edge("tools", "llm")

graph = builder.compile()

# 5) Run
result = graph.invoke({"messages": [{"role": "user", "content": "What is 2 * (3 + 4)?"}]})
print(result["messages"][-1].content)
```

**Tutor notes (what to point at mid-conversation):**
- The loop is created by the explicit edge `"tools" -> "llm"`.
- Termination is created by the conditional edge returning `END` when no tool calls are present. (Many-tools how-to)
- `MessagesState` ensures messages accumulate via `add_messages`. (Graph API essentials)

---

### Example 2 — Manual tool node (from quickstart pattern) to demystify ToolNode

This is useful when a student asks “what is ToolNode doing?” The quickstart shows a manual tool node that reads `tool_calls` and returns `ToolMessage`s. (https://docs.langchain.com/oss/python/langgraph/call-tools)

```python
from typing_extensions import TypedDict, Annotated
import operator
from langchain.messages import AnyMessage, ToolMessage, SystemMessage
from langgraph.graph import StateGraph, START, END

# State (quickstart uses operator.add; Graph API recommends add_messages)
class State(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    llm_calls: int

def llm_call(state: State):
    msg = model_with_tools.invoke(
        [SystemMessage(content="You are a helpful assistant tasked with arithmetic.")]
        + state["messages"]
    )
    return {"messages": [msg], "llm_calls": state.get("llm_calls", 0) + 1}

tools_by_name = {t.name: t for t in tools}

def tool_node(state: State):
    result = []
    for tool_call in state["messages"][-1].tool_calls:
        tool = tools_by_name[tool_call["name"]]
        observation = tool.invoke(tool_call["args"])
        result.append(ToolMessage(content=observation, tool_call_id=tool_call["id"]))
    return {"messages": result}

def should_continue(state: State):
    last = state["messages"][-1]
    if getattr(last, "tool_calls", None):
        return "tool_node"
    return END

builder = StateGraph(State)
builder.add_node("llm_call", llm_call)
builder.add_node("tool_node", tool_node)
builder.add_edge(START, "llm_call")
builder.add_conditional_edges("llm_call", should_continue, {"tool_node": "tool_node", END: END})
builder.add_edge("tool_node", "llm_call")
graph = builder.compile()
```

**Tutor notes:**
- This makes the “tool calling protocol” concrete: tool calls are data in the AI message; tool results are ToolMessages appended back into `messages`. (OpenAI function calling guide; LangGraph quickstart)

---

## Comparisons & Trade-offs

| Choice | What it buys you | What it costs / risks | Source |
|---|---|---|---|
| **ToolNode** vs **manual tool execution node** | ToolNode provides parallel tool execution, error handling options, and injection of runtime/state/store; less boilerplate | Less transparent unless you inspect ToolNode behavior; manual node can be easier for learning | ToolNode source: https://github.com/langchain-ai/langgraph/blob/main/libs/prebuilt/langgraph/prebuilt/tool_node.py; quickstart manual node: https://docs.langchain.com/oss/python/langgraph/call-tools |
| **`add_messages`** vs **`operator.add`** for `messages` | `add_messages` appends and can overwrite by message ID; also deserializes dict inputs into message objects | Slightly more “LangGraph-specific” concept to learn | Graph API essentials: https://docs.langchain.com/oss/python/langgraph/graph-api.md |
| **Graph API (StateGraph)** vs **Functional API** | Graph API makes control flow explicit (nodes/edges/cycles), easier to inspect/extend/interrupt | More upfront structure than writing a single function | Call-tools page notes both options: https://docs.langchain.com/oss/python/langgraph/call-tools |
| **Explicit orchestration (LangGraph)** vs **implicit “LLM decides everything”** | Production control: force tools first, branch by state, add guardrails, debug/trace steps | More engineering; you must define termination and routing | LangGraph rationale: https://blog.langchain.dev/langgraph/ |

---

## Prerequisite Connections

- **Python typing (`TypedDict`, `Annotated`)** — Needed to understand state schemas and reducers (`Annotated[..., reducer]`) used for message accumulation. (Graph API essentials)
- **LangChain message objects** — Needed to interpret `state["messages"]` and fields like `.content` and `.tool_calls`. (Graph API essentials; quickstart)
- **Tool/function calling concept** — Needed to understand why the agent alternates between model calls and tool execution, and why tool execution happens outside the model. (OpenAI function calling guide)
- **Basic control flow (state machines / routing)** — Needed to reason about conditional edges and termination at `END`. (LangGraph rationale; Graph API essentials)

---

## Socratic Question Bank

1) **If you removed the edge `"tools" -> "llm"`, what behavior would your “agent” have?**  
   *Good answer:* It would do at most one tool execution pass (or none) and then stop; the loop is created by that explicit edge.

2) **What exactly is stored in `state["messages"]` after one tool call round-trip?**  
   *Good answer:* User message(s) + AI message containing tool call(s) + ToolMessage(s) with tool outputs + next AI message, all accumulated by the messages reducer.

3) **Why do we need a reducer on `messages` at all? What breaks if it overwrites?**  
   *Good answer:* You’d lose conversation/tool history each step; the model wouldn’t see prior tool outputs, so it can’t incorporate observations.

4) **What condition should your router check to decide between `"tools"` and `END`?**  
   *Good answer:* Whether the last AI message contains tool calls (e.g., `last_message.tool_calls` non-empty).

5) **Where does tool execution happen, and how does the model learn the result?**  
   *Good answer:* Execution happens in the application/runtime (ToolNode or your node); the result is returned as tool output messages that are appended to state and then shown to the model next call.

6) **If your agent loops forever, what are two fixes you can apply in LangGraph?**  
   *Good answer:* Fix routing/termination logic to reach `END`; also set a lower `recursion_limit` to fail fast while debugging. (Graph API essentials)

7) **What does `.compile()` change about your graph?**  
   *Good answer:* It turns the builder into an executable Runnable (`CompiledStateGraph`), validates structure, and binds runtime options like checkpointers/interrupts. (Compile reference)

8) **When would you prefer ToolNode over a manual tool node?**  
   *Good answer:* When you want parallel tool calls, standardized error handling, and runtime/state/store injection without writing boilerplate. (ToolNode source)

---

## Likely Student Questions

**Q: Why do I have to call `compile()`—why can’t I just `invoke()` the builder?**  
→ **A:** `StateGraph` is a builder and “cannot execute directly”; `.compile()` produces a `CompiledStateGraph` that implements the Runnable interface (`invoke`, `stream`, async variants). (https://reference.langchain.com/python/langgraph/graph/state/StateGraph/compile)

**Q: How does LangGraph decide whether to append or overwrite state keys?**  
→ **A:** Each key has its own reducer. Default is overwrite. If you annotate a key with `Annotated[T, reducer]`, updates merge via that reducer (e.g., list concatenation). For messages, use `add_messages`. (https://docs.langchain.com/oss/python/langgraph/graph-api.md)

**Q: What’s special about `add_messages` compared to `operator.add`?**  
→ **A:** `add_messages` appends new messages and can overwrite by message ID on updates; it also deserializes dict inputs into LangChain message objects. (https://docs.langchain.com/oss/python/langgraph/graph-api.md)

**Q: What’s the standard LangGraph pattern for tool-using agents?**  
→ **A:** Use `StateGraph(MessagesState)`, add an `"llm"` node and a `"tools"` node (`ToolNode(tools)`), route from `"llm"` with `add_conditional_edges("llm", tools_condition)` to either `"tools"` or `END`, and loop `"tools" -> "llm"`, then `compile()`. (https://langchain-ai.github.io/langgraph/how-tos/many-tools/)

**Q: Where do tool errors go—do they crash the graph?**  
→ **A:** ToolNode has configurable error handling. The many-tools guide notes defaults: it catches invocation errors and re-raises execution errors; you can set `handle_tool_errors=True` (or provide a string/callable/exception tuple) to return errors to the LLM instead. (https://langchain-ai.github.io/langgraph/how-tos/many-tools/)

**Q: How do I stop an accidental infinite loop?**  
→ **A:** Fix your conditional routing to return `END` when appropriate, and use LangGraph’s recursion limit (default 1000 super-steps) by setting `config={"recursion_limit": N}` on `invoke`. (https://docs.langchain.com/oss/python/langgraph/graph-api.md)

**Q: Does the model execute my tools?**  
→ **A:** No. In OpenAI’s tool calling flow, the model emits tool call(s), your application executes them, then you send tool outputs back; the model then produces a final response or more tool calls. (https://platform.openai.com/docs/guides/function-calling)

**Q: Why do people recommend temperature=0 for tool calling?**  
→ **A:** Databricks reports function-calling accuracy can vary by ~10% with decoding, and temperature 0.0 is usually best for programmatic tool calling reliability. (https://www.databricks.com/blog/unpacking-function-calling-eval)

---

## Available Resources

### Videos
- [Intro to Large Language Models](https://youtube.com/watch?v=zjkBMFhNj_g) — Surface when: a student is missing the big-picture “LLM as cognitive core + tools + memory + loop” framing behind why agents are built as iterative systems.
- [OpenAI Function Calling - Full Beginner Walkthrough](https://youtube.com/watch?v=aqdWSYWC_LI) — Surface when: a student is confused about the tool-calling protocol (call → execute → return output) or how tool schemas/arguments work.

### Articles & Tutorials
- [LangGraph Agentic Concepts](https://langchain-ai.github.io/langgraph/concepts/agentic_concepts/) — Surface when: student asks “workflow vs agent” or wants patterns beyond the basic loop (prompt chaining, gating, branching).
- [LangGraph Quickstart](https://docs.langchain.com/oss/python/langgraph/quickstart) — Surface when: student wants a canonical end-to-end “calculator agent” build.
- [Call tools (LangGraph)](https://docs.langchain.com/oss/python/langgraph/call-tools) — Surface when: student wants the minimal tool-calling agent loop with Graph API vs Functional API options.
- [OpenAI Function Calling Guide](https://platform.openai.com/docs/guides/function-calling) — Surface when: student asks about `tool_choice`, parallel tool calls, strict schemas, or how to parse/return tool call arguments/outputs.
- [Lilian Weng — LLM Powered Autonomous Agents](https://lilianweng.github.io/posts/2023-06-23-agent/) — Surface when: student asks how this simple loop relates to planning/memory/reflection patterns in broader agent design.

---

## Visual Aids

![Agent workflow loop for tool use (LangChain).](/api/wiki-images/agent-memory/images/langchain-ai-langgraph-concepts-tools_001.png)  
Show when: the student can write code but doesn’t “see” the loop (decide → tool → observe → decide) that the graph is implementing.

![Agent architecture: LLM with tools and state/memory (LangChain).](/api/wiki-images/agent-memory/images/langchain-ai-langgraph-concepts-tools_008.png)  
Show when: the student confuses “state” (graph-managed) with “prompt” (model input) and needs a component diagram.

![Common ways to augment an LLM: tools, retrieval, memory (LangChain).](/api/wiki-images/agent-memory/images/langchain-ai-langgraph-concepts-tools_002.png)  
Show when: the student asks “should I use tools or RAG or memory for this requirement?”

---

## Key Sources

- [LangGraph Graph API (StateGraph) essentials](https://docs.langchain.com/oss/python/langgraph/graph-api.md) — Most authoritative for StateGraph construction, reducers (`add_messages`), conditional routing, `Command`, recursion limits, and runtime context.
- [LangGraph many-tools (ToolNode + conditional routing)](https://langchain-ai.github.io/langgraph/how-tos/many-tools/) — Canonical end-to-end agent loop pattern using `ToolNode` and `tools_condition`.
- [StateGraph.compile reference](https://reference.langchain.com/python/langgraph/graph/state/StateGraph/compile) — Precise runtime contract for compilation and invocation/streaming.
- [ToolNode implementation](https://github.com/langchain-ai/langgraph/blob/main/libs/prebuilt/langgraph/prebuilt/tool_node.py) — Ground truth for how tool calls are dispatched, injected args are detected, and errors are formatted.
- [OpenAI Function Calling Guide](https://platform.openai.com/docs/guides/function-calling) — Clear definition of the tool-calling protocol and runtime responsibilities (model proposes calls; app executes; outputs returned).