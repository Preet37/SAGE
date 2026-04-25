## Core Definitions

**Multi-agent system**: A multi-agent system is an agentic architecture where multiple LLM-powered agents coordinate to solve a task, typically to reduce prompt/tool overload, enable specialization, and/or run work in parallel. OpenAI’s practical guide frames the motivation operationally: start single-agent, and “consider creating multiple agents” when you have **complex logic** or **tool overload** (especially overlapping tools) that makes a single agent unreliable. (OpenAI, *A practical guide to building agents*, “When to consider creating multiple agents”)

**Agent**: “Agents are systems that independently accomplish tasks on your behalf.” Key characteristics include: (1) the **LLM controls workflow execution** (decides what to do, recognizes completion, can correct, can halt/transfer control), and (2) **tool access** with **dynamic tool selection** inside guardrails. (OpenAI, *A practical guide to building agents*, “What is an agent?”)

**Supervisor / manager agent (agents-as-tools pattern)**: A supervisor (manager) is a controlling agent that **retains the main conversation/workflow control** and delegates subtasks to specialist agents by invoking them as **tools**. OpenAI describes this as the **Manager (agents as tools)** pattern: “one manager delegates via tool calls; best when one agent should control workflow + user interaction.” (OpenAI, *A practical guide to building agents*, “Multi-agent systems”)

**Agent delegation / handoff**: Delegation is transferring work to another agent. In the OpenAI Agents SDK, a **handoff** is a typed mechanism that lets one agent **transfer control** to another agent, optionally filtering or nesting the history passed along. Handoffs are represented to the model as tools, and can include a small structured payload via JSON schema. (OpenAI Agents SDK, *Typed Handoffs* reference; OpenAI Agents JS, *Handoffs*)

**Agents as tools (orchestration tool)**: An orchestration approach where an agent is exposed as a callable tool to another agent (often a supervisor). OpenAI’s guide explicitly includes **orchestration tools (agents as tools)** in its tool taxonomy. (OpenAI, *A practical guide to building agents*, “Defining tools”)

**Subgraph**: In LangGraph, “a subgraph is a graph that is used as a node in another graph.” Subgraphs are used for **building multi-agent systems**, **reusing** a set of nodes across graphs, and **distributing development** across teams as long as the subgraph interface (input/output schemas) is respected. (LangGraph docs, “Subgraphs”)

**Subgraph composition**: Composing systems by packaging a multi-step workflow (often a multi-agent collaboration) as a subgraph and then embedding it as a node in a parent graph—either by (a) calling it inside a wrapper node when schemas differ, or (b) adding it directly as a node when state keys are shared. (LangGraph docs, “Subgraphs”)

**Parallel agent execution**: Running multiple agents (or graph nodes/operators) concurrently to reduce wall-clock latency and/or increase coverage (e.g., fan-out research). This is a core motivation for multi-agent systems in practice (parallel work) and is formalized in orchestration research as layered parallel execution where latency is governed by the **critical path** (max per layer). (YouTube transcript “Multi-Agent Systems with LangGraph”; LAMaS paper arXiv:2601.10560)

---

## Key Formulas & Empirical Results

### When multi-agent architectures help: tool/context overload signals
- OpenAI’s production guidance: move from single-agent to multi-agent when you have:
  - **Complex logic** (many if/then branches)
  - **Tool overload** due to overlapping/similar tools  
  It notes some agents succeed with **>15 distinct tools**, while others struggle with **<10 overlapping** tools. (OpenAI, *A practical guide to building agents*, “When to consider creating multiple agents”)

### Benchmark: orchestration patterns trade off accuracy, cost, latency (SEC filings)
From *Multi-agent orchestration benchmark (SEC filing extraction)* (arXiv:2603.22651):
- Architectures compared: **Sequential**, **Parallel fan-out + merge**, **Hierarchical supervisor-worker**, **Reflexive self-correcting loop**.
- Dataset: **10,000** SEC filings; 10-K avg **187,340 tokens**, 10-Q avg **82,150**, 8-K avg **14,820**; **25 fields**. (Sec. IV-A)
- Defaults: temperature **0.0** for extraction calls; **0.3** for supervisor/critique. (Sec. IV-C)
- Primary results (Claude 3.5 Sonnet, Table III):
  - Sequential: **F1 0.903**, cost **$0.187**, latency **38.7s**
  - Parallel: **F1 0.914**, cost **$0.221**, latency **21.3s**
  - Hierarchical: **F1 0.929**, cost **$0.261**, latency **46.2s**
  - Reflexive: **F1 0.943**, cost **$0.430**, latency **74.1s**
- Noted tradeoff: hierarchical achieves **98.5%** of reflexive F1 at **60.7%** of cost. (Paper summary)

### Parallelism: latency is the critical path, cost adds
From *Latency-aware orchestration via critical path (LAMaS)* (arXiv:2601.10560):
- **Latency (critical path)**:
  \[
  L=\sum_{l\in \mathcal{L}} \max_{o\in \mathcal{O}_l} t(o)
  \]
  where \(\mathcal{O}_l\) are operators in layer \(l\), \(t(o)\) is operator time. (Sec. 3.1–3.3)
- **Cost**:
  \[
  C=\sum_{l\in \mathcal{L}}\sum_{o\in \mathcal{O}_l} c(o)
  \]
  (Sec. 3.1–3.3)
- Key claim supported: under parallel execution, **token/tool cost accumulates across all parallel branches**, but **latency is dominated by the slowest branch per layer** (critical path).

### Event-sourced orchestration: parallel agents, sequential commit
From ESAA (arXiv:2602.23193):
- Concurrency model: agents can run **in parallel**, but results are **validated and appended sequentially** to preserve a total order in an append-only log. (Sec. 3.4)

---

## How It Works

### A. Supervisor pattern (manager delegates specialists as tools)
Mechanics grounded in OpenAI’s “Manager (agents as tools)” pattern + Responses API tool controls.

1. **Supervisor receives user goal** and decides whether it can answer directly or should delegate.
2. **Supervisor selects a specialist** (conceptually: “agent as tool”) based on task type (e.g., research, extraction, coding, policy).
3. **Supervisor invokes the specialist via tool calling**:
   - In OpenAI Responses API, tool calling is controlled by `tool_choice`:
     - `"auto"`: model may call tools or respond normally.
     - `"required"`: model must call ≥1 tool.
     - `"none"`: model cannot call tools. (Responses API reference)
4. **Specialist runs with a smaller, focused context**:
   - Often receives only the relevant slice of history or a nested summary (see “handoff filtering/nesting” below).
5. **Specialist returns structured output** (ideally schema-validated).
6. **Supervisor merges results**:
   - Resolve conflicts, apply business rules, decide next delegation, or produce final user response.
7. **Exit conditions**:
   - In OpenAI Agents SDK, the run loop continues until either:
     1) a **final-output tool** is invoked, or
     2) the model returns a response **without tool calls**. (OpenAI practical guide, “Single-agent systems”)

Where parallelism fits:
- Supervisor can **fan out** to multiple specialists concurrently (e.g., multiple extractors or researchers) and then run a merge/synthesis step. This corresponds to the “Parallel fan-out + merge” architecture in the SEC benchmark. (arXiv:2603.22651)

### B. Delegation via typed handoffs (OpenAI Agents SDK)
Handoffs are the SDK’s explicit “transfer control” mechanism.

1. **Define a handoff** (tool exposed to the model) that points to a destination agent.
2. Optionally define:
   - `input_json_schema` / `strict_json_schema=True` to make the model produce correct structured arguments.
   - `input_filter` to remove irrelevant history/tool chatter.
   - `nest_handoff_history` to summarize prior transcript into a compact message for the next agent. (OpenAI Agents SDK, *Typed Handoffs*)
3. When the model triggers the handoff tool:
   - `on_invoke_handoff(run_context, json_args_str)` returns the next agent to run. (Typed Handoffs reference)
4. The next agent runs with the filtered/nested input history and continues the conversation/work until completion.

Key implementation detail (what gets passed):
- `HandoffInputData` includes `input_history`, `pre_handoff_items`, `new_items`, and optionally `input_items` (to override what becomes model input while keeping full history in session). (Typed Handoffs reference)

### C. Subgraphs in LangGraph (packaging multi-step collaborations)
LangGraph subgraphs let you package a workflow as a reusable module.

Two composition modes (LangGraph “Subgraphs”):

**Mode 1 — Call a subgraph inside a node (schemas differ / private state):**
1. Parent node function maps parent state → subgraph input state.
2. Invoke subgraph: `subgraph.invoke(subgraph_state)`.
3. Map subgraph output → parent state updates.
4. Return updates to parent graph.

**Mode 2 — Add a subgraph as a node (shared state keys):**
1. Compile subgraph.
2. `parent_builder.add_node("name", compiled_subgraph)`
3. Subgraph reads/writes the same state channels as parent (no wrapper).

Why this matters for multi-agent:
- You can keep **private message histories per agent** by using Mode 1 (transform state), while still composing them into a larger orchestrated system. (LangGraph “Subgraphs”)

### D. Persistence/checkpointing (why your “state” may reset)
In LangGraph, persistence is provided by a **checkpointer**:
- When compiled with a checkpointer, a snapshot is saved at every **super-step** boundary, organized into **threads** (requires `thread_id`). This enables HITL, time travel, and fault tolerance. (LangGraph checkpointer reference)
- Common pitfall: without a checkpointer, a graph can “restart” each run, so message accumulation doesn’t happen across turns—highlighted in LangGraph issue #1568, where adding `MemorySaver()` and a `thread_id` fixes message merging. (LangGraph issue #1568)

---

## Teaching Approaches

### Intuitive (no math)
- A **supervisor** is like a project lead: it talks to the user, breaks the job into parts, and asks **specialists** to do each part. Each specialist only sees what it needs, so it doesn’t get overwhelmed by the entire conversation and tool list.
- A **subgraph** is like a “department playbook”: a reusable mini-workflow (maybe involving multiple specialists) that you can plug into bigger workflows.

### Technical (with math)
- Parallel orchestration changes the objective: **latency ≠ cost**.
  - Cost adds across all parallel branches: \(C=\sum_{l}\sum_{o\in \mathcal{O}_l} c(o)\).
  - Latency is the **critical path**: \(L=\sum_{l}\max_{o\in \mathcal{O}_l} t(o)\). (LAMaS, arXiv:2601.10560)
- Supervisor patterns are a practical way to choose \(\mathcal{O}_l\) (which agents/tools to run) while keeping each agent’s context bounded.

### Analogy-based
- **Supervisor + specialists**: a hospital triage doctor (supervisor) routes you to cardiology/radiology/labs (specialists). The triage doctor integrates results and decides next steps.
- **Subgraph**: a standardized “diagnostic protocol” (e.g., chest pain workup) that can be reused in many cases; it’s a module with a defined input/output interface.

---

## Common Misconceptions

1. **“If I add more agents, it’s always faster.”**  
   - Why wrong: parallelism can reduce wall-clock time, but only if tasks are independent and you can merge results efficiently. Also, some architectures (hierarchical/reflexive) increase latency due to verification/retries. The SEC benchmark shows **parallel** is faster than sequential (21.3s vs 38.7s), but **hierarchical** and **reflexive** are slower (46.2s, 74.1s). (arXiv:2603.22651)  
   - Correct model: multi-agent can trade **latency vs accuracy vs cost**; parallelism reduces latency when the critical path shrinks, but coordination/verification can add steps.

2. **“Parallel execution reduces cost because it’s faster.”**  
   - Why wrong: cost is not governed by wall-clock time; it’s the sum of all tokens/tool calls across branches. LAMaS explicitly separates **cost** (sum over all operators) from **latency** (critical path max per layer). (arXiv:2601.10560)  
   - Correct model: parallelism often **increases cost** while decreasing latency.

3. **“A handoff is the same thing as ‘agents as tools’.”**  
   - Why wrong: in OpenAI’s framing, **manager (agents as tools)** keeps the manager in control; **handoff** transfers control to another agent (useful when the specialist should take over the conversation). (OpenAI practical guide; OpenAI Agents JS “Handoffs”)  
   - Correct model: choose **agents-as-tools** for supervisor-controlled delegation; choose **handoffs** when you want the specialist to become the primary agent.

4. **“Subgraphs are just code organization; they don’t affect state or context.”**  
   - Why wrong: LangGraph subgraphs define how **state schemas** and **message histories** flow. If schemas differ, you must transform state; if shared, the subgraph directly reads/writes parent channels. This directly affects what context each agent/node sees. (LangGraph “Subgraphs”)  
   - Correct model: subgraphs are **interface-bound modules**; composition mode determines state sharing vs isolation.

5. **“If my LangGraph messages aren’t accumulating, `add_messages` is broken.”**  
   - Why wrong: without a **checkpointer** and `thread_id`, the graph can restart each run, so state doesn’t persist across turns. This is the resolution in issue #1568. (LangGraph issue #1568; checkpointer reference)  
   - Correct model: message reducers append within a run; cross-run persistence requires checkpointing/threading.

---

## Worked Examples

### 1) LangGraph subgraph composition (different schemas via wrapper)
Directly adapted from LangGraph “Subgraphs” docs.

```python
from typing_extensions import TypedDict
from langgraph.graph.state import StateGraph, START

# --- Subgraph state/schema ---
class SubgraphState(TypedDict):
    bar: str

def subgraph_node_1(state: SubgraphState):
    return {"bar": "hi! " + state["bar"]}

subgraph_builder = StateGraph(SubgraphState)
subgraph_builder.add_node(subgraph_node_1)
subgraph_builder.add_edge(START, "subgraph_node_1")
subgraph = subgraph_builder.compile()

# --- Parent graph state/schema ---
class State(TypedDict):
    foo: str

def call_subgraph(state: State):
    # Map parent -> subgraph
    subgraph_output = subgraph.invoke({"bar": state["foo"]})
    # Map subgraph -> parent
    return {"foo": subgraph_output["bar"]}

builder = StateGraph(State)
builder.add_node("node_1", call_subgraph)
builder.add_edge(START, "node_1")
graph = builder.compile()

print(graph.invoke({"foo": "there"}))  # {"foo": "hi! there"}
```

Tutor notes (what to emphasize live):
- This is **Mode 1**: schemas differ (`foo` vs `bar`), so you wrap.
- This pattern is how you keep **private state** inside a subgraph (e.g., private agent message history) and only export a small result to the parent.

### 2) LangGraph persistence pitfall (messages not merging across turns)
From LangGraph issue #1568: without checkpointing, state resets each run. Fix by compiling with a checkpointer and using a `thread_id`.

```python
from langgraph.checkpoint.memory import MemorySaver

graph = graph_builder.compile(checkpointer=MemorySaver())
thread_config = {"configurable": {"thread_id": "1"}}

for event in graph.stream({"messages": ("user", user_input)}, thread_config):
    ...
```

Tutor notes:
- If a student says “my supervisor forgets prior steps,” ask whether they have **persistence** configured (checkpointer/thread).

### 3) OpenAI Responses API: forcing a supervisor to delegate (tool_choice)
Use when a student asks how to *force* delegation vs allow free-form answers.

Key control knob (Responses API):
- `tool_choice: "required"` forces ≥1 tool call.
- `tool_choice: "auto"` lets the model decide.
- `tool_choice: "none"` disables tool calls.

(Exact schema details are in the Responses API reference: `ToolChoiceOptions`.)

---

## Comparisons & Trade-offs

| Pattern / Architecture | What it is | Strengths | Weaknesses | Choose when |
|---|---|---|---|---|
| Single agent + tools | One agent selects among tools | Simple, fewer coordination failures | Tool/prompt overload; brittle with overlapping tools | Default starting point (OpenAI guidance) |
| Manager / Supervisor (agents as tools) | One agent delegates to specialists via tool calls | Centralized control, consistent UX, bounded specialist context | Manager can become bottleneck; needs good merge logic | One agent should own workflow + user interaction (OpenAI practical guide) |
| Decentralized handoffs | Peer agents transfer control | Good for triage; clear ownership per phase | Harder to maintain global plan; more transitions | Triage-style routing (OpenAI practical guide) |
| Parallel fan-out + merge (benchmark B) | Dispatcher splits work; merge agent resolves conflicts | Lower latency (21.3s) and improved F1 (0.914) vs sequential | Higher cost ($0.221 vs $0.187); merge complexity | Independent subtasks (document sections, research queries) (arXiv:2603.22651) |
| Hierarchical supervisor-worker (benchmark C) | Supervisor manages queue; reassigns low-confidence fields | Higher F1 (0.929) than parallel/sequential | Higher latency (46.2s) than parallel; higher cost | Need quality control + targeted retries (arXiv:2603.22651) |
| Reflexive self-correcting loop (benchmark D) | Verifier checks consistency/grounding; iterates corrections | Best F1 (0.943) | Highest cost ($0.430) and latency (74.1s); scales poorly at high throughput | Maximum accuracy, low throughput constraints (arXiv:2603.22651) |
| Subgraphs (LangGraph) | A graph used as a node in another graph | Reuse, modularity, team boundaries, encapsulation | Interface/schema design overhead | You want reusable multi-step modules (LangGraph “Subgraphs”) |

---

## Prerequisite Connections

- **Tool calling & tool-choice control**: Students need to understand how models decide to call tools and how developers constrain that (`tool_choice`) to understand supervisors delegating specialists. (Responses API reference; OpenAI Tools guide)
- **State & persistence**: Subgraphs and multi-agent orchestration depend on how state is passed, summarized, and checkpointed; otherwise students misdiagnose “forgetting” as model failure. (LangGraph checkpointer; issue #1568)
- **Basic agent loop / termination**: Understanding when an agent run stops (final tool vs no tool calls) helps explain supervisor loops and delegation cycles. (OpenAI practical guide, “Single-agent systems”)
- **Latency vs cost under parallelism**: Needed to reason about why parallel agents can be faster but more expensive. (LAMaS formulas)

---

## Socratic Question Bank

1. **If you had 12 tools and the agent keeps picking the wrong one, what are two architecture changes you could try before prompt-tweaking?**  
   *Good answer:* split into specialists to reduce overlapping tools; introduce a supervisor/manager; constrain tool choice sets.

2. **In a parallel fan-out + merge design, what determines wall-clock latency: average worker time or something else?**  
   *Good answer:* critical path / slowest worker per layer (LAMaS critical-path latency).

3. **When would you prefer a handoff over “agents as tools”?**  
   *Good answer:* when the specialist should take over the conversation/control, not just return a sub-result.

4. **What’s the interface contract of a subgraph in LangGraph?**  
   *Good answer:* input/output state schemas (shared keys vs transformed via wrapper).

5. **If your LangGraph agent forgets previous turns, what’s the first thing you check?**  
   *Good answer:* checkpointer + `thread_id` configured; otherwise state resets each run.

6. **Why might a hierarchical supervisor-worker system outperform a pure parallel system on accuracy?**  
   *Good answer:* supervisor can reassign low-confidence fields and iterate (as in benchmark C with thresholds/iterations).

7. **How do you prevent a supervisor from taking a high-risk action automatically?**  
   *Good answer:* guardrails + risk rating + human intervention triggers for high-risk actions (OpenAI practical guide guardrails section).

8. **What’s one reason multi-agent systems help with “context rot” concerns?**  
   *Good answer:* each agent keeps a smaller working context; supervisor delegates rather than stuffing everything into one prompt (motivated in the multi-agent video transcript).

---

## Likely Student Questions

**Q: When should I switch from a single agent to multiple agents?**  
→ **A:** OpenAI recommends starting single-agent and moving to multi-agent when you have **complex logic** (many if/then branches) or **tool overload**, especially with overlapping tools; they note some setups work with **>15 distinct tools**, while others struggle with **<10 overlapping** tools. (https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)

**Q: What’s the difference between “manager (agents as tools)” and “handoffs”?**  
→ **A:** In OpenAI’s guide, **manager/agents-as-tools** means one manager delegates via tool calls and keeps workflow + user interaction control; **handoffs** transfer control to another agent (useful for triage or when the specialist should take over). (https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf; https://openai.github.io/openai-agents-js/guides/handoffs/)

**Q: How do I force the supervisor to call a specialist tool instead of answering directly?**  
→ **A:** In the Responses API, set `tool_choice` to `"required"` to force ≥1 tool call; `"auto"` allows tool calls; `"none"` disables them. (https://platform.openai.com/docs/api-reference/responses)

**Q: How do subgraphs work in LangGraph—do I need a wrapper?**  
→ **A:** If parent and subgraph have **different state schemas** (or you want to transform/isolate state), you **call the subgraph inside a node** and map state in/out. If they **share state keys**, you can **add the compiled subgraph directly as a node** with no wrapper. (https://docs.langchain.com/oss/python/langgraph/use-subgraphs)

**Q: Why is my LangGraph message list not appending across turns even with `add_messages`?**  
→ **A:** Without a **checkpointer** and a `thread_id`, the graph can restart each run, so messages appear overwritten. The fix shown in issue #1568 is compiling with `MemorySaver()` and passing `{"configurable": {"thread_id": "1"}}` on each call. (https://github.com/langchain-ai/langgraph/issues/1568; checkpointer reference)

**Q: What are real measured tradeoffs between sequential, parallel, hierarchical, and reflexive orchestration?**  
→ **A:** On SEC filing extraction (Claude 3.5 Sonnet): Sequential F1 **0.903** cost **$0.187** latency **38.7s**; Parallel F1 **0.914** cost **$0.221** latency **21.3s**; Hierarchical F1 **0.929** cost **$0.261** latency **46.2s**; Reflexive F1 **0.943** cost **$0.430** latency **74.1s**. (https://arxiv.org/pdf/2603.22651.pdf)

**Q: In parallel orchestration, why can latency drop while cost rises?**  
→ **A:** LAMaS formalizes that **latency** is the sum over layers of the **max** operator time per layer (critical path), while **cost** sums over **all** operators executed. Parallelism reduces the max-per-layer path but adds more total operators. (https://arxiv.org/abs/2601.10560)

---

## Available Resources

### Videos
- [Multi-Agent Systems with LangGraph](https://www.youtube.com/watch?v=Mi5wOpAgixw) — Surface when: the student asks *why* multi-agent helps with context limits/context rot, or wants a high-level taxonomy of multi-agent patterns and parallelism motivation.
- [OpenAI Function Calling - Full Beginner Walkthrough](https://youtube.com/watch?v=aqdWSYWC_LI) — Surface when: the student is stuck on tool calling mechanics that underpin “agents as tools” supervisors.
- [Intro to Large Language Models](https://youtube.com/watch?v=zjkBMFhNj_g) — Surface when: the student lacks grounding in what the LLM is doing inside an agent loop (planning/tool use/memory as system components).

### Articles & Tutorials
- [OpenAI Agents SDK (Python)](https://openai.github.io/openai-agents-python/) — Surface when: the student wants the minimal set of primitives (agents, handoffs, guardrails, sessions) and how they map to supervisor patterns.
- [LangGraph: Subgraphs](https://docs.langchain.com/oss/python/langgraph/use-subgraphs) — Surface when: the student asks how to package multi-agent collaborations into reusable modules with schema boundaries.
- [OpenAI — Tools guide](https://platform.openai.com/docs/guides/tools) — Surface when: the student asks about tool calling, parallel tool calls, or remote MCP tools in orchestration.
- [ReAct (Yao et al., 2022)](https://arxiv.org/abs/2210.03629) — Surface when: the student wants the canonical reasoning↔acting loop that many supervisors/workers implement internally.

---

## Visual Aids

![LLM agent architecture: planning, memory, and tool use components. (Weng, 2023)](/api/wiki-images/agent-fundamentals/images/lilianweng-posts-2023-06-23-agent_001.png)  
Show when: the student is mixing up “agent” vs “orchestrator” vs “tools,” and you need a single diagram to anchor planning/memory/tool-use as separable components before layering supervisors/subgraphs on top.

---

## Key Sources

- [OpenAI — *A practical guide to building agents*](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf) — Primary production-oriented definitions and when/why to adopt multi-agent supervisor patterns; concrete guardrails and tool-overload guidance.
- [OpenAI Responses API reference](https://platform.openai.com/docs/api-reference/responses) — Exact knobs (`tool_choice`, tool call events/status) that determine how supervisors delegate and control execution.
- [LangGraph — Subgraphs](https://docs.langchain.com/oss/python/langgraph/use-subgraphs) — Canonical definition and mechanics of subgraphs as composable modules with schema/interface considerations.
- [arXiv:2603.22651 (SEC orchestration benchmark)](https://arxiv.org/pdf/2603.22651.pdf) — Concrete accuracy/cost/latency numbers comparing sequential/parallel/hierarchical/reflexive orchestration.
- [arXiv:2601.10560 (LAMaS)](https://arxiv.org/abs/2601.10560) — Formalizes latency under parallelism via critical path; clarifies why cost and latency diverge in multi-agent DAGs.