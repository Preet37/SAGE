## Core Definitions

**ReAct loop (Reason + Act; thought–action–observation).**  
ReAct is a prompting/agent pattern where an LLM interleaves **reasoning traces (“Thought”)** with **environment/tool actions (“Action”)** and then incorporates **feedback (“Observation”)** before deciding the next step; thoughts update the model’s internal context but do not affect the environment, while actions do and yield observations. This is presented as trajectories formatted **Thought → Action → Observation → …** until a terminal answer/action. (Yao et al., 2022: https://arxiv.org/abs/2210.03629; Google Research blog summary: https://research.google/blog/react-synergizing-reasoning-and-acting-in-language-models/)

**Thought–Action–Observation (TAO) loop.**  
A single iteration of ReAct: the model produces a **Thought** (internal reasoning), selects an **Action** (e.g., a tool call), receives an **Observation** (tool result), and repeats until it emits a final response without further tool calls. (https://arxiv.org/abs/2210.03629; https://research.google/blog/react-synergizing-reasoning-and-acting-in-language-models/)

**LangGraph StateGraph (shared-state graph).**  
LangGraph’s core abstraction is a **StateGraph** where nodes communicate via a shared **state**; each node has the signature **State → Partial\<State\>** and returns only the keys it updates. State keys can be annotated with **reducers** that merge multiple writes into one value. (LangGraph reference: https://reference.langchain.com/python/langgraph/graphs/)

**Reducer (state merge function).**  
A reducer is a function used to aggregate multiple updates to the same state key: **reducer(current_value, update_value) → new_value**. LangGraph supports annotating state keys with reducers (e.g., list-append reducers) to accumulate messages/steps across iterations. (https://reference.langchain.com/python/langgraph/graphs/)

**Tool calling (function calling).**  
Tool calling is a multi-step interaction where the model emits a **structured request** to call a tool (function name + arguments), the application executes the tool, then sends the **tool output** back to the model; the model may then produce a final response or request more tool calls. (OpenAI function calling guide: https://platform.openai.com/docs/guides/function-calling; OpenAI tools guide: https://platform.openai.com/docs/guides/tools)

**Tool execution node (in a LangGraph ReAct agent).**  
In a minimal LangGraph ReAct implementation, a dedicated node executes the tool(s) requested by the model and appends the resulting **observations** back into state, enabling the next reasoning step to condition on tool results. This matches the general tool-use loop where the model never executes tools itself; the app does. (Tool loop: https://platform.openai.com/docs/guides/function-calling; LangGraph state semantics: https://reference.langchain.com/python/langgraph/graphs/)

**Conditional routing (LangGraph).**  
A StateGraph can route execution based on a function that inspects state and returns a route key; `add_conditional_edges(source, path, path_map?)` can route to another node or to **END** to stop the graph. (https://reference.langchain.com/python/langgraph/graphs/)

**Iterative agent execution (stop condition).**  
An agent loop continues until a stop condition is met—commonly: the model returns a response **without tool calls**, or an iteration limit is reached. This is explicitly described in LangGraph agent docs (“runs until a stop condition is met”) and in OpenAI’s production agent guidance (loop ends when model stops calling tools / emits final output). (LangGraph agents ref: https://reference.langchain.com/python/langgraph/agents/; OpenAI practical agents guide PDF: https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)

---

## Key Formulas & Empirical Results

**ReAct context/policy formalism (paper definition).**  
Yao et al. define the agent context and policy as:  
\[
c_t = (o_1, a_1, \ldots, o_{t-1}, a_{t-1}, o_t), \quad \pi(a_t \mid c_t)
\]  
where \(o_t\) is the observation at time \(t\), \(a_t\) is the action, and \(c_t\) is the history-conditioned context used to choose the next action. ReAct augments the action space with language “thoughts” that don’t affect the environment. (https://arxiv.org/abs/2210.03629)

**LangGraph reducer example (list append) + numeric worked result.**  
LangGraph shows a list-append reducer pattern and a worked “logistic map step” example:  
- Equation: `next_value = x * r * (1 - x)` with `x = state["x"][-1]` and `r = runtime.context["r"]`.  
- With input `{"x": 0.5}` and `context={"r": 3.0}`, output becomes `{'x': [0.5, 0.75]}` using a list reducer.  
Supports the claim: reducers accumulate iterative updates across node executions. (https://reference.langchain.com/python/langgraph/graphs/)

**LangGraph compile/runtime knobs (names + defaults).**  
`StateGraph.compile(checkpointer=None, interrupt_before=None, interrupt_after=None, debug=False, name=None) -> CompiledStateGraph`. Compiled graphs support `invoke/stream/ainvoke/astream` and accept `context` (immutable run-scoped data). (https://reference.langchain.com/python/langgraph/graph/state/StateGraph/compile)

**Tool-calling reliability default (temperature).**  
Databricks’ function-calling eval analysis reports that tool-calling accuracy can vary by ~10% depending on decoding and that **temperature 0.0 is usually best** for programmatic tool calling. (https://www.databricks.com/blog/unpacking-function-calling-eval)

**ReAct benchmark deltas (original ReAct results).**  
Reported prompting results for PaLM-540B include:  
- ALFWorld success: Act-only 45% vs **ReAct 71%** (2-shot).  
- WebShop success: Act-only 30.1% vs **ReAct 40%** (1-shot).  
- FEVER accuracy: Act-only 58.9 vs **ReAct 60.9** (3-shot).  
(https://arxiv.org/abs/2210.03629; also summarized at https://research.google/blog/react-synergizing-reasoning-and-acting-in-language-models/)

---

## How It Works

### A. Minimal ReAct loop as a LangGraph cycle (mechanics)

**Goal:** implement the TAO loop as a graph that alternates:
1) a **reasoning/model node** that may request tool calls, and  
2) a **tool execution node** that runs those tools and appends observations,  
until the model stops calling tools (route to END).

#### 1) Define state schema (messages + optional scratch)
Use a state that accumulates conversation turns and tool observations. In LangGraph, nodes return **partial state updates**; reducers can append to lists.

Key LangGraph contract to keep in mind: each node is **State → Partial\<State\>**; reducers merge updates. (https://reference.langchain.com/python/langgraph/graphs/)

#### 2) Reasoning node (model call)
- Input: current `state` (typically includes `messages`).
- Action: call an LLM that supports tool calling (OpenAI/Anthropic/Gemini all follow the same conceptual loop: model emits tool call(s), app executes, returns results).  
  (OpenAI: https://platform.openai.com/docs/guides/function-calling; Anthropic tool use: https://docs.anthropic.com/en/docs/build-with-claude/tool-use; Gemini function calling: https://ai.google.dev/gemini-api/docs/function-calling)
- Output: append the model’s message to `state["messages"]`.

#### 3) Router (conditional edge) decides whether to run tools or stop
- Inspect the last model message for tool calls.
- If tool calls exist → route to tool node.
- Else → route to `END`.

LangGraph supports this with `add_conditional_edges(source, path, path_map?)`; if `path` returns **END**, graph stops. (https://reference.langchain.com/python/langgraph/graphs/)

#### 4) Tool execution node
- Read tool call requests from the last model message.
- Execute each tool in application code (the model never executes tools itself). (https://platform.openai.com/docs/guides/function-calling)
- Append tool outputs as “observations” back into `state["messages"]` (or a dedicated `observations` key).
- Return partial state update.

#### 5) Edge back to reasoning node
- After tool execution, route back to the reasoning node so the model can incorporate observations and decide next action.

#### 6) Compile + run
- `graph.compile(...)` produces a `CompiledStateGraph` runnable; you then `invoke()` or `stream()`. (https://reference.langchain.com/python/langgraph/graph/state/StateGraph/compile)
- Runtime controls you can use while tutoring/debugging:
  - `stream_mode="values"` vs `"updates"` to see full state vs incremental updates. (https://reference.langchain.com/python/langgraph/graphs/)
  - `interrupt_before` / `interrupt_after` to pause around nodes for inspection. (https://reference.langchain.com/python/langgraph/graphs/)
  - `context={...}` for immutable run-scoped data (e.g., user_id, db handle). (https://reference.langchain.com/python/langgraph/graphs/)

---

### B. Tool calling loop (provider-agnostic contract)

This is the same loop LangGraph is orchestrating:

1) Send model a request with **tool definitions** enabled.  
2) Model returns either normal text or a **structured tool call** (name + args).  
3) Application executes the tool.  
4) Application sends tool result back to model as the next turn.  
5) Model returns final response or more tool calls.  
(OpenAI: https://platform.openai.com/docs/guides/function-calling; Gemini 4-step loop: https://ai.google.dev/gemini-api/docs/function-calling)

Provider-specific detail worth remembering when students mix ecosystems:
- Gemini includes a unique `id` per functionCall and requires returning a functionResponse with the same `id` (supports parallel calls; results can be returned in any order because of `id`). (https://ai.google.dev/gemini-api/docs/function-calling)

---

## Teaching Approaches

### Intuitive (no math)
- “We’re turning the agent into a **two-step loop**: the model *thinks and asks for tools*, then code *runs tools and shows results*, and we repeat until the model stops asking.”
- Emphasize debuggability: each loop iteration produces an explicit artifact: model output → tool calls → tool results → next model output.

### Technical (with formal contracts)
- ReAct defines a history-conditioned policy \(\pi(a_t \mid c_t)\) where \(c_t\) is the observation/action history; ReAct adds language “thoughts” that shape the next action distribution without changing the environment. (https://arxiv.org/abs/2210.03629)
- LangGraph implements this as a StateGraph where each node is **State → Partial\<State\>**, and reducers define how iterative updates (like message lists) accumulate. (https://reference.langchain.com/python/langgraph/graphs/)

### Analogy-based
- “Reasoning node = **brain** deciding what to do next; tool node = **hands** doing it; state = **notebook** where we write down what happened; conditional routing = **decision rule**: ‘do we need to use our hands again, or are we done?’”

---

## Common Misconceptions

1) **“The model executes the tool when it calls it.”**  
- Why wrong: tool calling is explicitly a multi-step conversation; the model emits a structured request, but **your application executes** the tool and returns outputs. (https://platform.openai.com/docs/guides/function-calling)  
- Correct model: model proposes tool calls; tool node/app runs them; results become observations.

2) **“In LangGraph, nodes mutate state in place.”**  
- Why wrong: LangGraph nodes return **Partial\<State\>** updates; the runtime merges them (optionally via reducers). (https://reference.langchain.com/python/langgraph/graphs/)  
- Correct model: treat nodes as pure-ish functions that *return updates*; reducers define accumulation.

3) **“Conditional edges are like if-statements that run immediately inside the node.”**  
- Why wrong: routing is part of the graph execution semantics: `add_conditional_edges` uses a separate `path` function to choose the next node or END. (https://reference.langchain.com/python/langgraph/graphs/)  
- Correct model: node computes updates; router inspects resulting state and chooses next step.

4) **“ReAct means the model must alternate Thought/Action every turn.”**  
- Why wrong: ReAct prompting can be dense alternation for reasoning-heavy tasks, but for decision-making tasks thoughts can be sparse and placed asynchronously. (https://arxiv.org/abs/2210.03629; https://research.google/blog/react-synergizing-reasoning-and-acting-in-language-models/)  
- Correct model: TAO is the conceptual loop; the exact density of “thought” tokens is a prompting choice.

5) **“If tool calling is unreliable, the fix is just ‘add more tools’ or ‘increase temperature’.”**  
- Why wrong: function-calling accuracy is sensitive to decoding; empirical guidance suggests **temperature 0.0** is usually best for programmatic tool calling, and reliability can vary ~10% with decoding choices. (https://www.databricks.com/blog/unpacking-function-calling-eval)  
- Correct model: reduce randomness, tighten schemas/descriptions, and add validation/retries at the orchestration layer.

---

## Worked Examples

### Example 1: Minimal LangGraph ReAct cycle (reason → tools → reason … until END)

This is a **skeleton** showing the key wiring (state, reducers, conditional routing, cycle). It focuses on LangGraph mechanics (state updates + routing), aligned with the StateGraph contract. (https://reference.langchain.com/python/langgraph/graphs/)

```python
from typing import Annotated, TypedDict, List, Dict, Any
from langgraph.graph import StateGraph, START, END

# --- Reducer: append updates onto an existing list (LangGraph reducer pattern) ---
def append_list(left: list, right: list | None) -> list:
    return left + (right or [])

class AgentState(TypedDict):
    # Accumulate messages across iterations
    messages: Annotated[List[Dict[str, Any]], append_list]

# --- Node 1: "reasoning" (model call) ---
def reason_node(state: AgentState) -> dict:
    """
    In a real agent, call an LLM with tool calling enabled and return its message.
    Here we assume it returns a dict like {"role": "assistant", ...}
    """
    assistant_msg = fake_llm_call(state["messages"])  # placeholder
    return {"messages": [assistant_msg]}

# --- Router: decide whether to call tools or stop ---
def route_after_reason(state: AgentState):
    last = state["messages"][-1]
    tool_calls = last.get("tool_calls", [])
    if tool_calls:
        return "tools"
    return END

# --- Node 2: tool execution ---
def tools_node(state: AgentState) -> dict:
    last = state["messages"][-1]
    tool_calls = last.get("tool_calls", [])

    tool_results = []
    for call in tool_calls:
        name = call["name"]
        args = call.get("arguments", {})
        result = execute_tool(name, args)  # your code
        # Append as an "observation" message
        tool_results.append({
            "role": "tool",
            "name": name,
            "content": str(result),
        })

    return {"messages": tool_results}

# --- Build graph ---
g = StateGraph(AgentState)
g.add_node("reason", reason_node)
g.add_node("tools", tools_node)

g.add_edge(START, "reason")
g.add_conditional_edges("reason", route_after_reason, {"tools": "tools", END: END})
g.add_edge("tools", "reason")  # cycle

agent = g.compile()
final_state = agent.invoke({"messages": [{"role": "user", "content": "..." }]})
```

**Tutor notes (what to point at mid-conversation):**
- The *only* way the loop continues is the edge `"tools" -> "reason"` plus the router returning `"tools"`.  
- Stopping is explicit: router returns `END`. (https://reference.langchain.com/python/langgraph/graphs/)
- The reducer is what makes `messages` accumulate across iterations rather than being overwritten. (https://reference.langchain.com/python/langgraph/graphs/)

---

### Example 2: Using LangGraph runtime `context` for immutable run-scoped data

LangGraph supports passing immutable run-scoped context at invoke time; nodes can read it via `runtime.context`. (https://reference.langchain.com/python/langgraph/graphs/)

Pattern to emulate (from LangGraph logistic-map example):
- `compiled.invoke(input, context={...})`
- Node reads `runtime.context[...]`

Use this when a student asks “where do I put API keys/db handles/user_id without stuffing it into messages?”

---

## Comparisons & Trade-offs

| Design choice | What you gain | What you lose | Source anchor |
|---|---|---|---|
| **LangGraph minimal ReAct loop (custom StateGraph)** | Maximum debuggability/control; explicit state + routing; easy to add interrupts/streaming | You must implement tool parsing/execution + stop conditions yourself | LangGraph graph semantics + runtime knobs (https://reference.langchain.com/python/langgraph/graphs/) |
| **Production-ready `create_agent` (LangGraph Agents)** | Built-in agent loop, tool execution, retries/error handling patterns | Less “from-scratch” transparency; more framework defaults | LangGraph agents reference (https://reference.langchain.com/python/langgraph/agents/) |
| **Higher temperature vs temperature 0 for tool calling** | More diverse language generation | Worse schema adherence / tool-call accuracy; eval sensitivity ~10% | Databricks function-calling eval (https://www.databricks.com/blog/unpacking-function-calling-eval) |

---

## Prerequisite Connections

- **Tool calling basics (schemas, tool call → execute → tool result).** Needed because the LangGraph tool node is just an implementation of this provider-agnostic loop. (https://platform.openai.com/docs/guides/function-calling)
- **Graph execution model (nodes, edges, END, conditional routing).** Needed to understand how the ReAct loop becomes a cycle with a stop condition. (https://reference.langchain.com/python/langgraph/graphs/)
- **State + reducers.** Needed to understand how messages/observations accumulate across iterations without manual concatenation. (https://reference.langchain.com/python/langgraph/graphs/)

---

## Socratic Question Bank

1) **If the model outputs a tool call, where does the tool actually run, and what must happen before the model can use the result?**  
Good answer: tool runs in app/tool node; result must be sent back as an observation/next-turn input. (OpenAI tool loop)

2) **In your graph, what exact condition causes the loop to stop? Where is that encoded?**  
Good answer: conditional edge/router returns `END` when no tool calls in last assistant message. (LangGraph conditional edges)

3) **Why do we need a reducer on `messages` (or an equivalent accumulation strategy)? What breaks without it?**  
Good answer: without reducer, later node writes overwrite earlier messages; you lose history needed for ReAct context. (LangGraph reducers)

4) **What’s the difference between “Thought” and “Action” in ReAct in terms of effects on the environment?**  
Good answer: thought is internal/context only; action changes environment and yields observation. (ReAct paper/blog)

5) **If a tool returns an error, where should that error live so the model can react to it next step?**  
Good answer: in state as an observation/tool message; then reasoning node can decide retry/alternate tool. (Tool loop + state accumulation)

6) **How would you debug a single iteration in LangGraph without running the whole loop?**  
Good answer: use `interrupt_before/after` or streaming modes to inspect intermediate state. (LangGraph runtime knobs)

7) **Why might lowering temperature improve tool calling?**  
Good answer: decoding sensitivity; empirical note that T=0.0 usually best for programmatic tool calling. (Databricks eval)

8) **What’s the minimal set of nodes you need for a ReAct agent in LangGraph, and why?**  
Good answer: reasoning node + tool execution node + conditional router; that’s the TAO loop. (ReAct + LangGraph semantics)

---

## Likely Student Questions

**Q: What does a LangGraph node return—does it return the whole state?**  
→ **A:** Nodes return **Partial\<State\>** (only updated keys). LangGraph merges updates into shared state; keys can use reducers to aggregate multiple writes. (https://reference.langchain.com/python/langgraph/graphs/)

**Q: How do I stop the LangGraph ReAct loop?**  
→ **A:** Use `add_conditional_edges(...)` so a router function returns **END** when the model emits a message **without tool calls**; returning END stops execution. (https://reference.langchain.com/python/langgraph/graphs/)

**Q: What does `StateGraph.compile()` do?**  
→ **A:** `compile()` turns the builder into an executable `CompiledStateGraph` (Runnable) that supports `invoke/stream` and binds state schema + reducers into runtime semantics. (https://reference.langchain.com/python/langgraph/graph/state/StateGraph/compile)

**Q: Where do tool results go in the loop?**  
→ **A:** Tool results must be appended back into the conversation/state as **observations** (e.g., tool messages). Tool calling is a multi-step flow: model requests tool → app executes → app sends tool output back → model continues. (https://platform.openai.com/docs/guides/function-calling)

**Q: Can the model call multiple tools at once? How does that affect the tool node?**  
→ **A:** Yes—some APIs support multiple/parallel tool calls in one model turn; your tool node should iterate over all tool calls and append each result. Gemini explicitly supports parallel calls and uses per-call `id` mapping. (Gemini: https://ai.google.dev/gemini-api/docs/function-calling)

**Q: How do I pass immutable runtime data (like user_id or a DB handle) into LangGraph?**  
→ **A:** LangGraph supports run-scoped immutable `context` passed at invoke time (`compiled.invoke(input, context={...})`); nodes can read it via `runtime.context`. (https://reference.langchain.com/python/langgraph/graphs/)

**Q: What temperature should I use for reliable tool calling?**  
→ **A:** Databricks’ function-calling eval writeup reports tool-call accuracy can vary by ~10% with decoding and that **temperature 0.0 is usually best** for programmatic tool calling. (https://www.databricks.com/blog/unpacking-function-calling-eval)

**Q: How can I observe/debug each step of the loop?**  
→ **A:** Use `stream/astream` with `stream_mode` like `"values"` or `"updates"`, and/or `interrupt_before` / `interrupt_after` to pause around nodes; LangGraph also supports debug streaming modes. (https://reference.langchain.com/python/langgraph/graphs/)

---

## Available Resources

### Videos
- [OpenAI Function Calling - Full Beginner Walkthrough](https://youtube.com/watch?v=aqdWSYWC_LI) — Surface when: the student is stuck on what a “tool call” looks like (schema, arguments) before wiring it into LangGraph.
- [Intro to Large Language Models](https://youtube.com/watch?v=zjkBMFhNj_g) — Surface when: the student needs broader mental model of LLMs as the “cognitive core” before discussing agent loops.

### Articles & Tutorials
- [LangGraph Conceptual Documentation: Agentic Concepts](https://langchain-ai.github.io/langgraph/concepts/agentic_concepts/) — Surface when: the student asks “why graphs for agents?” or wants patterns beyond the minimal loop.
- [OpenAI — Function Calling Guide](https://platform.openai.com/docs/guides/function-calling) — Surface when: the student needs exact tool-calling lifecycle and message sequencing.
- [Yao et al., 2022 — ReAct](https://arxiv.org/abs/2210.03629) — Surface when: the student asks for the original definition, formalism, or benchmark evidence for ReAct.

---

## Visual Aids

![LLM agent architecture: planning, memory, and tool use components. (Weng, 2023)](/api/wiki-images/agent-fundamentals/images/lilianweng-posts-2023-06-23-agent_001.png)  
Show when: the student confuses “ReAct loop” with the broader agent architecture (planning/memory/tools) and needs the big-picture block diagram before returning to LangGraph wiring.

---

## Key Sources

- [LangGraph StateGraph + runtime controls](https://reference.langchain.com/python/langgraph/graphs/) — Authoritative for StateGraph semantics (State → Partial\<State\>, reducers, conditional routing, invoke/stream/interrupt/context).
- [StateGraph.compile reference](https://reference.langchain.com/python/langgraph/graph/state/StateGraph/compile) — Precise runtime contract for compiled graphs and invocation parameters.
- [OpenAI Function Calling Guide](https://platform.openai.com/docs/guides/function-calling) — Canonical tool-calling loop definition (model emits call; app executes; return tool output; repeat).
- [ReAct paper (Yao et al., 2022)](https://arxiv.org/abs/2210.03629) — Original TAO loop definition + formalism + benchmark results motivating ReAct.