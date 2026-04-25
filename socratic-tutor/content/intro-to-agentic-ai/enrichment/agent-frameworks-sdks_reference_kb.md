## Core Definitions

**LangGraph** — As LangChain’s docs describe it, **LangGraph is a low-level orchestration framework and runtime for building, managing, and deploying long-running, stateful agents**, focused on “underlying capabilities important for agent orchestration” such as **durable execution, streaming, human-in-the-loop, and memory**. It is intentionally low-level and “does not abstract prompts or architecture.” Source: LangGraph introduction/tutorials. https://langchain-ai.github.io/langgraph/tutorials/introduction/

**OpenAI Agents SDK** — OpenAI defines the **OpenAI Agents SDK** as a lightweight, production-ready package (an upgrade from Swarm) with a small set of primitives: **Agents** (LLMs with instructions + tools), **Agents as tools / Handoffs** (delegation to other agents), and **Guardrails** (validation of agent inputs/outputs). It includes a **built-in agent loop** for tool invocation and continuation until completion, plus **sessions** (persistent memory) and **built-in tracing**. Source: OpenAI Agents SDK docs. https://openai.github.io/openai-agents-python/

**CrewAI** — From the CrewAI repo/docs entrypoints: CrewAI provides primitives to create **Agents**, **Tasks**, and a **Crew** that orchestrates agents over tasks, with process modes like **sequential** and **hierarchical** (hierarchical assigns a manager for planning/delegation/validation). It also supports **Flows** for event-driven control using decorators like `@start`, `@listen`, and `@router`. Source: CrewAI repo card. https://github.com/crewAIInc/crewAI

**AutoGen** — AutoGen’s paper and docs describe it as an open-source framework for building LLM applications via **multiple agents that can converse with each other**; agents are customizable and can combine **LLMs, tools, and human inputs**. In AutoGen 0.2 reference docs, an **agent** is an entity that can **send messages, receive messages, and generate a reply** using models/tools/human inputs or mixtures. Sources: AutoGen paper abstract + AutoGen 0.2 reference. https://arxiv.org/abs/2308.08155 and https://microsoft.github.io/autogen/0.2/docs/reference/

**Agent orchestration** — In the OpenAI production guide, orchestration is the design of how an agent (or multiple agents) **controls workflow execution**, including **tool selection**, **completion detection**, and escalation/hand-off patterns (e.g., **manager delegates to specialist agents as tools** vs **decentralized handoffs**). Source: OpenAI “Practical guide to building agents” PDF. https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf

**State management (for agents)** — In LangGraph, “stateful agents” are first-class: you build graphs over a state object (e.g., `MessagesState`) and LangGraph emphasizes **durable execution** (persist/resume), **memory**, and **human-in-the-loop** state inspection/modification. In AutoGen GroupChat, state includes the shared `messages` list and manager metadata like `last_speaker`. Sources: LangGraph intro; AutoGen GroupChat reference. https://langchain-ai.github.io/langgraph/tutorials/introduction/ and https://microsoft.github.io/autogen/0.2/docs/reference/agentchat/groupchat/


## Key Formulas & Empirical Results

### Multi-tool agent objective (cost-aware)
From the multi-tool orchestration explainer, a generic objective trades off success vs cost:
\[
\max_\theta\ \mathbb{E}_{\tau\sim \pi_\theta}\big[ R(\tau)-\lambda\, C(\tau)\big]
\]
- \(\pi_\theta\): agent policy over actions (tool calls or terminate)
- \(\tau\): trajectory (history + memory) up to horizon \(T\)
- \(R(\tau)\): success/utility
- \(C(\tau)\): cost (e.g., number of tool calls, latency, API fees, risk)
- \(\lambda\): tradeoff weight  
Supports: why orchestration frameworks often add caching/routing/parallelism controls to manage cost/latency vs reliability. Source: https://arxiv.org/html/2603.22862v2

### Tool execution interface (formalization)
\[
\text{Exec}(t, x)\rightarrow (y, s')
\]
- \(t\): tool
- \(x\): tool arguments (must match schema)
- \(y\): tool feedback (JSON/text/error)
- \(s'\): post-call environment state  
Supports: why “state management” matters—tool calls mutate state and produce feedback that must be fed back into the loop. Source: https://arxiv.org/html/2603.22862v2

### OpenAI Agents SDK run-loop exit conditions (production guide)
The OpenAI production guide states `Runner.run()` loops until either:
1) a **final-output tool** is invoked (specific output type), or  
2) the model returns a response **without tool calls**.  
Supports: what “agent loop” means operationally. Source: https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf

### Multi-agent orchestration benchmark (SEC extraction) — concrete tradeoffs
From the SEC filing extraction benchmark (Claude 3.5 Sonnet, Table III):
- **Sequential**: F1 **0.903**, cost **$0.187**, latency **38.7s**
- **Parallel**: F1 **0.914**, cost **$0.221**, latency **21.3s**
- **Hierarchical**: F1 **0.929**, cost **$0.261**, latency **46.2s**
- **Reflexive**: F1 **0.943**, cost **$0.430**, latency **74.1s**  
Supports: choosing orchestration pattern based on accuracy–cost–latency. Source: https://arxiv.org/pdf/2603.22651.pdf

Scaling note (Table IX): reflexive degrades fastest at high throughput (queueing/timeouts truncate correction loops); sequential most resilient. Source: https://arxiv.org/pdf/2603.22651.pdf

### CrewAI installation/runtime defaults + telemetry control
- Python requirement: **Python >= 3.10 and < 3.14**
- Install: `uv pip install crewai` (optional extras: `'crewai[tools]'`, `'crewai[embeddings]'`)
- Default model connection: **OpenAI API by default** (set `OPENAI_API_KEY`)
- Disable anonymous telemetry: `OTEL_SDK_DISABLED=true`  
Supports: common “why is it sending telemetry / what versions supported” questions. Source: https://github.com/crewAIInc/crewAI

### AutoGen 0.2 key defaults/knobs (agent autonomy + termination)
From `ConversableAgent` reference:
- `human_input_mode="TERMINATE"` default; `"NEVER"` for fully autonomous
- `code_execution_config=False` default (code execution off)
- `llm_config=None` uses `DEFAULT_CONFIG` (defaults to `False`); `llm_config=False` disables LLM-based auto reply
- Auto-reply limit: if `max_consecutive_auto_reply=0` ⇒ **no auto reply**; if `None` uses class `MAX_CONSECUTIVE_AUTO_REPLY`  
Supports: how AutoGen agents stop / ask humans / execute code. Source: https://microsoft.github.io/autogen/0.2/docs/reference/agentchat/conversable_agent/

From GroupChat reference:
- `admin_name="Admin"` default
- `func_call_filter=True` default (function-call suggestion constrains next speaker)
- `speaker_selection_method="auto"` default; retries default **2**  
Source: https://microsoft.github.io/autogen/0.2/docs/reference/agentchat/groupchat/


## How It Works

### What “framework handles boilerplate” typically means (cross-framework)
1) **Define tools** (Python functions or external tool servers) with schemas/validation.
2) **Register tools** with an agent runtime so the model can call them.
3) **Run an agent loop**:
   - model produces either (a) a final response or (b) tool calls
   - runtime executes tool calls (`Exec(t,x) -> (y,s')`) and appends results to state/history
   - loop continues until an exit condition (e.g., no tool calls; final-output tool)
4) **Manage state**:
   - store conversation messages + intermediate artifacts
   - optionally persist state for resuming (durable execution) or sessions (memory)
5) **Orchestrate multiple agents**:
   - manager delegates to specialists (agents as tools) or peers hand off control
   - enforce turn limits / speaker selection / termination conditions
6) **Trace/observe**:
   - capture tool calls, state transitions, and outputs for debugging/evals

(Each step above is explicitly supported in at least one of: OpenAI Agents SDK docs, LangGraph docs, AutoGen reference, or the multi-tool formalization.)

### LangGraph: minimal “graph over state” mechanics
Hello-world from LangGraph intro:
```python
from langgraph.graph import StateGraph, MessagesState, START, END

def mock_llm(state: MessagesState):
    return {"messages": [{"role": "ai", "content": "hello world"}]}

graph = StateGraph(MessagesState)
graph.add_node(mock_llm)
graph.add_edge(START, "mock_llm")
graph.add_edge("mock_llm", END)
graph = graph.compile()

graph.invoke({"messages": [{"role": "user", "content": "hi!"}]})
```
Mechanics:
1) Choose a **state schema** (here `MessagesState`).
2) Add **nodes** (functions that map state → partial state update).
3) Add **edges** (control flow).
4) `compile()` builds an executable graph.
5) `invoke()` runs from `START` to `END`, passing and updating state.  
Source: https://langchain-ai.github.io/langgraph/tutorials/introduction/

### OpenAI Agents SDK: minimal “agent loop” mechanics
Hello-world from SDK docs:
```python
from agents import Agent, Runner

agent = Agent(name="Assistant", instructions="You are a helpful assistant")
result = Runner.run_sync(agent, "Write a haiku about recursion in programming.")
print(result.final_output)
```
Mechanics (per SDK docs + production guide):
1) Create an `Agent` with instructions and tools (tools optional).
2) `Runner.run_sync` executes the built-in loop: model → tool calls (if any) → tool execution → model … until completion.
3) Termination occurs when the model returns **no tool calls** or a **final-output tool** is invoked (production guide).  
Sources: https://openai.github.io/openai-agents-python/ and https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf

### CrewAI: Agents + Tasks + Crew kickoff (and Flows)
Core orchestration surfaces (repo examples):
- `Crew(agents=[...], tasks=[...], process=Process.sequential, verbose=True)`
- `Task(description="... {var} ...", expected_output="...", agent=..., output_file="report.md")`
- `Crew.kickoff(inputs={...})` injects template variables into task descriptions.

Flow control surfaces:
- decorators: `@start`, `@listen`, `@router`
- combinators: `or_(...)`, `and_(...)`  
Source: https://github.com/crewAIInc/crewAI

### AutoGen 0.2: agent-to-agent chat + group chat speaker selection
Single agent reply:
- `generate_reply(messages=[{"role":"user","content":...}])`

Two-agent chat:
- `initiate_chat(other_agent, message=..., max_turns=2)` caps dialogue length.

GroupChat speaker selection (auto):
1) Create nested two-agent chat: **speaker selector** + **speaker validator**
2) Selector proposes next agent name based on group messages
3) Validator checks; if invalid, retry up to `max_retries_for_selecting_speaker` (default 2)
4) If still unresolved, fallback to next agent in list  
Sources: AutoGen reference + GroupChat reference:
https://microsoft.github.io/autogen/0.2/docs/reference/ and https://microsoft.github.io/autogen/0.2/docs/reference/agentchat/groupchat/


## Teaching Approaches

### Intuitive (no math)
- **Frameworks are “agent runtimes.”** They run the repetitive loop: ask model → if tool call, execute tool → feed result back → repeat until done.
- The value is not “smarter reasoning,” but **reliability and engineering leverage**: consistent tool schemas, state persistence, multi-agent coordination, and tracing.

### Technical (with math)
- Model the agent as a policy \(\pi_\theta(a_t \mid h_t, m_t)\) over actions \(a_t\) (tool call or terminate), with tool execution `Exec(t,x)->(y,s')` and an objective \(\mathbb{E}[R(\tau)-\lambda C(\tau)]\).  
- Orchestration frameworks implement the machinery to maintain \(h_t, m_t\), execute `Exec`, and enforce termination/constraints—so you can focus on shaping \(\pi_\theta\) via prompts, toolsets, and routing.

(From: https://arxiv.org/html/2603.22862v2)

### Analogy-based
- **LangGraph**: like building a **state machine / workflow graph** where nodes are “steps” and edges are “what happens next,” but designed for LLM + tool loops and long-running state.
- **OpenAI Agents SDK**: like a **minimal web framework** for agents—few primitives, batteries included (loop, tools, guardrails, tracing).
- **AutoGen**: like a **chatroom with rules**—agents message each other; a manager decides who speaks next; optional code execution/human input.
- **CrewAI**: like a **project team**—agents have roles, tasks have expected outputs, and a crew runs sequentially or with a manager.


## Common Misconceptions

1) **“If I use an agent framework, the agent becomes more capable automatically.”**  
Why wrong: Frameworks mainly provide **orchestration infrastructure** (looping, tool invocation, state, tracing). They don’t inherently improve the underlying model’s reasoning.  
Correct model: Capability gains come from **better tools, better prompts/instructions, better decomposition/orchestration patterns**, and evaluation/iteration; the framework reduces boilerplate and improves reliability/observability (LangGraph + OpenAI SDK positioning). Sources: LangGraph intro; OpenAI Agents SDK overview.

2) **“LangGraph is just LangChain agents with a different name.”**  
Why wrong: LangGraph explicitly positions itself as **low-level orchestration** and says it “does not abstract prompts or architecture,” and recommends higher-level LangChain agents if you want prebuilt architectures.  
Correct model: LangGraph is a **graph runtime** for stateful workflows/agents; LangChain agents are higher-level prebuilt loops built on top. Source: https://langchain-ai.github.io/langgraph/tutorials/introduction/

3) **“Multi-agent always beats single-agent.”**  
Why wrong: The OpenAI production guide recommends starting **single-agent** and moving to multi-agent only when complexity/tool overload warrants it; the SEC benchmark shows multi-agent patterns trade off **accuracy vs cost vs latency** (e.g., reflexive highest F1 but much higher cost/latency).  
Correct model: Choose orchestration pattern based on constraints; multi-agent adds coordination overhead and can increase latency/cost. Sources: OpenAI production guide PDF; SEC benchmark paper.

4) **“AutoGen code execution is on by default.”**  
Why wrong: AutoGen reference explicitly shows `code_execution_config=False` (default off).  
Correct model: You must enable code execution via configuration and choose an executor (Local or Docker). Source: https://microsoft.github.io/autogen/0.2/docs/reference/

5) **“CrewAI hierarchical just means ‘run tasks in order’.”**  
Why wrong: CrewAI distinguishes **sequential** vs **hierarchical**, where hierarchical “assigns a manager” for planning/delegation/validation.  
Correct model: Hierarchical implies a **manager-style orchestration** layer, not merely ordering. Source: https://github.com/crewAIInc/crewAI


## Worked Examples

### 1) LangGraph “hello world” (state graph)
Use when student asks: “What does a LangGraph graph actually look like?”
```python
from langgraph.graph import StateGraph, MessagesState, START, END

def mock_llm(state: MessagesState):
    # returns a partial state update: new messages
    return {"messages": [{"role": "ai", "content": "hello world"}]}

graph = StateGraph(MessagesState)
graph.add_node(mock_llm)
graph.add_edge(START, "mock_llm")
graph.add_edge("mock_llm", END)
graph = graph.compile()

out = graph.invoke({"messages": [{"role": "user", "content": "hi!"}]})
print(out)
```
Step-through:
1) Input state contains one user message.
2) Node `mock_llm` runs and returns an update with an AI message.
3) Graph reaches `END`; output state includes the appended AI message.  
Source: https://langchain-ai.github.io/langgraph/tutorials/introduction/

### 2) OpenAI Agents SDK “hello world” (built-in loop)
Use when student asks: “What’s the minimal code to run an agent loop?”
```python
from agents import Agent, Runner

agent = Agent(name="Assistant", instructions="You are a helpful assistant")
result = Runner.run_sync(agent, "Write a haiku about recursion in programming.")
print(result.final_output)
```
Step-through:
1) `Agent(...)` defines the LLM + instructions (tools optional).
2) `Runner.run_sync(...)` runs the SDK’s loop until completion.
3) `final_output` is the terminal response.  
Source: https://openai.github.io/openai-agents-python/

### 3) CrewAI: scaffold + kickoff inputs (project workflow)
Use when student asks: “How do I actually run a CrewAI project and pass variables?”
Commands (from repo docs):
- Create scaffold:
  - `crewai create crew <project_name>`
- Run:
  - `crewai run` (or `python src/<project>/main.py`)

Core runtime pattern:
- Define `Task(description="... {var} ...", ...)`
- Call `Crew.kickoff(inputs={...})` to fill `{var}` placeholders.  
Source: https://github.com/crewAIInc/crewAI

### 4) AutoGen: cap multi-turn agent-to-agent chat
Use when student asks: “How do I prevent infinite back-and-forth?”
- Use `initiate_chat(..., max_turns=2)` to cap turns.  
Source: https://microsoft.github.io/autogen/0.2/docs/reference/


## Comparisons & Trade-offs

| Framework | Primary abstraction | Strengths (per sources) | Typical “choose it when…” | Notable defaults/knobs (sourced) |
|---|---|---|---|---|
| LangGraph | **StateGraph** over explicit state | Low-level orchestration for **long-running, stateful** agents; **durable execution**, **human-in-the-loop**, memory, streaming; doesn’t abstract prompts/architecture | You want explicit control of state + control flow; production statefulness/resume | Install: `uv pip install -U langgraph`; uses `StateGraph`, `MessagesState`, `START/END` (LangGraph intro) |
| OpenAI Agents SDK | **Agent + Runner** loop; handoffs; guardrails | Few primitives; built-in **agent loop**, **guardrails**, **sessions**, **tracing**; “Python-first” orchestration | You want a minimal SDK with production features and easy delegation/guardrails | Hello world uses `Runner.run_sync`; docs emphasize handoffs + guardrails + sessions (SDK docs) |
| CrewAI | **Agents/Tasks/Crew** (+ Flows) | Quick scaffolding; process modes **sequential/hierarchical**; Flows for event-driven routing; telemetry controls | You want “team + tasks” ergonomics and CLI scaffolding | Python 3.10–<3.14; `Crew.kickoff(inputs=...)`; disable telemetry `OTEL_SDK_DISABLED=true` (CrewAI repo) |
| AutoGen (0.2 / stable) | **Conversational agents** + group chat manager | Multi-agent conversation patterns; configurable autonomy/human input; group speaker selection; optional code execution via executors | You want explicit multi-agent chat patterns, speaker selection, and code execution utilities | `code_execution_config=False` default; `human_input_mode` defaults; GroupChat `speaker_selection_method="auto"`, retries=2 (AutoGen refs) |

When to choose multi-agent orchestration patterns (production + benchmark):
- OpenAI guide: start single-agent; go multi-agent when logic becomes complex or tool overload occurs; manager vs decentralized handoffs are common patterns.  
- SEC benchmark: sequential/parallel/hierarchical/reflexive show measurable accuracy–cost–latency tradeoffs; reflexive highest F1 but highest cost/latency; hierarchical near-reflexive accuracy at lower cost.  
Sources: OpenAI production guide PDF; https://arxiv.org/pdf/2603.22651.pdf


## Prerequisite Connections

- **Tool calling + schemas**: Needed to understand what “tool registration” and `Exec(t,x)->(y,s')` mean in agent runtimes (multi-tool formalization).
- **Stateful vs stateless execution**: Needed to understand why LangGraph emphasizes durable execution and memory (LangGraph intro).
- **Multi-agent patterns (manager vs handoff)**: Needed to reason about orchestration choices (OpenAI production guide; AutoGen paper/docs).
- **Cost/latency vs reliability tradeoffs**: Needed to interpret benchmark tables and why orchestration adds caching/routing/parallelism (SEC benchmark; multi-tool objective).


## Socratic Question Bank

1) **If your agent can call tools, what exactly must be stored in “state” to make the next step possible?**  
Good answer: history of messages/tool calls + tool outputs; any intermediate artifacts; possibly environment state \(s'\) or summaries.

2) **What’s a concrete condition that should stop an agent loop? How does that differ across SDKs?**  
Good answer: “no tool calls” or “final-output tool invoked” (OpenAI guide); max turns (AutoGen); graph reaches END (LangGraph).

3) **When would adding a second agent reduce errors, and when would it just add cost/latency?**  
Good answer: helps when tool overload/complex branching; hurts when coordination overhead dominates; cite benchmark tradeoffs.

4) **In AutoGen GroupChat, why might `func_call_filter=True` change who speaks next?**  
Good answer: function-call suggestion constrains next speaker to an agent that has that function in its `function_map`.

5) **What’s the difference between “sequential” and “hierarchical” in CrewAI in terms of control?**  
Good answer: hierarchical introduces a manager for planning/delegation/validation; sequential is fixed order.

6) **If you needed to resume an agent run after a crash, which framework feature would you look for?**  
Good answer: LangGraph “durable execution” / persistence; OpenAI SDK sessions (memory) depending on need.

7) **Given the objective \(E[R(\tau)-\lambda C(\tau)]\), name two things that increase \(C(\tau)\) in real deployments.**  
Good answer: more tool calls, higher latency, API fees, risky write actions.

8) **What’s one reason parallel tool/agent execution can be dangerous?**  
Good answer: race conditions/state inconsistency for write-tools; need dependency-aware scheduling/rollback ideas (multi-tool explainer).


## Likely Student Questions

**Q: What does LangGraph actually provide, beyond “calling an LLM”?**  
→ **A:** LangGraph positions itself as low-level orchestration for long-running, stateful agents, emphasizing **durable execution**, **human-in-the-loop**, **memory**, **streaming**, and debugging/observability (via LangSmith). Source: https://langchain-ai.github.io/langgraph/tutorials/introduction/

**Q: What are the core primitives in the OpenAI Agents SDK?**  
→ **A:** The SDK has a small set of primitives: **Agents** (LLMs with instructions/tools), **Agents as tools / Handoffs** (delegation), and **Guardrails** (validate inputs/outputs). It also includes a built-in agent loop, sessions (persistent memory), and tracing. Source: https://openai.github.io/openai-agents-python/

**Q: When does the OpenAI Agents SDK stop looping?**  
→ **A:** The production guide states `Runner.run()` loops until either (1) a **final-output tool** is invoked, or (2) the model returns a response **without tool calls**. Source: https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf

**Q: How do I cap or terminate AutoGen multi-agent back-and-forth?**  
→ **A:** Use `initiate_chat(..., max_turns=2)` to cap turns (example in reference). Also, `ConversableAgent` has `max_consecutive_auto_reply` and `human_input_mode` rules that can stop auto replies. Sources: https://microsoft.github.io/autogen/0.2/docs/reference/ and https://microsoft.github.io/autogen/0.2/docs/reference/agentchat/conversable_agent/

**Q: Is AutoGen code execution enabled by default?**  
→ **A:** No. The reference shows `code_execution_config=False` (default off). You enable it by providing a config (and optionally an executor like `LocalCommandLineCodeExecutor` or `DockerCommandLineCodeExecutor`). Source: https://microsoft.github.io/autogen/0.2/docs/reference/

**Q: In CrewAI, how do I pass runtime variables into tasks?**  
→ **A:** Use templated variables in `Task(description="... {var} ...")` and pass values via `Crew.kickoff(inputs={...})`. Source: https://github.com/crewAIInc/crewAI

**Q: What’s the difference between sequential, parallel, hierarchical, and reflexive orchestration in practice?**  
→ **A:** In the SEC extraction benchmark (Claude 3.5 Sonnet), sequential had F1 **0.903** (cost **$0.187**, latency **38.7s**), parallel F1 **0.914** (cost **$0.221**, latency **21.3s**), hierarchical F1 **0.929** (cost **$0.261**, latency **46.2s**), reflexive F1 **0.943** (cost **$0.430**, latency **74.1s**). Source: https://arxiv.org/pdf/2603.22651.pdf

**Q: How do I disable CrewAI telemetry?**  
→ **A:** Set environment variable `OTEL_SDK_DISABLED=true`. Source: https://github.com/crewAIInc/crewAI


## Available Resources

### Videos
- [Multi-Agent Systems with LangGraph](https://youtube.com/watch?v=Mi5wOpAgixw) — Surface when: student asks “why multi-agent?” or “what are common multi-agent architectures and when do they help?”
- [Intro to Large Language Models](https://youtube.com/watch?v=zjkBMFhNj_g) — Surface when: student is missing fundamentals about what an LLM is and why “agent = LLM + tools + loop” is a useful framing.

### Articles & Tutorials
- [LangGraph Introduction](https://langchain-ai.github.io/langgraph/tutorials/introduction/) — Surface when: student wants the minimal LangGraph mental model + hello world code.
- [LangGraph Agentic Concepts](https://langchain-ai.github.io/langgraph/concepts/agentic_concepts/) — Surface when: student asks about patterns (workflow vs agent), state, tool binding, and orchestration design.
- [OpenAI Agents SDK Docs](https://openai.github.io/openai-agents-python/) — Surface when: student asks “what primitives exist?” or “how do I do handoffs/guardrails/sessions/tracing?”
- [Practical Guide to Building Agents (OpenAI PDF)](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf) — Surface when: student asks production questions (single vs multi-agent, guardrails, model selection, exit conditions).
- [AutoGen Stable Docs](https://microsoft.github.io/autogen/stable/index.html) — Surface when: student asks about AutoGen’s current direction (event-driven scalable multi-agent systems) and install/run entrypoint.
- [AutoGen 0.2 Reference](https://microsoft.github.io/autogen/0.2/docs/reference/) — Surface when: student asks for exact knobs/defaults (human_input_mode, code execution, group chat).
- [CrewAI Repo](https://github.com/crewAIInc/crewAI) — Surface when: student asks about CrewAI CLI scaffolding, process modes, kickoff inputs, or telemetry.


## Visual Aids

![LLM agent architecture: planning, memory, and tool use components. (Weng, 2023)](/api/wiki-images/agent-fundamentals/images/lilianweng-posts-2023-06-23-agent_001.png)  
Show when: student is confused about what parts an “agent framework” is responsible for (loop/orchestration/state) vs what the model/prompt/tools provide.


## Key Sources

- [LangGraph Introduction](https://langchain-ai.github.io/langgraph/tutorials/introduction/) — Authoritative positioning + minimal code for LangGraph as low-level orchestration for stateful agents.
- [OpenAI Agents SDK Docs](https://openai.github.io/openai-agents-python/) — Canonical primitives (agents, handoffs, guardrails) and minimal Runner-based loop.
- [CrewAI Repository](https://github.com/crewAIInc/crewAI) — Concrete API surfaces for Agents/Tasks/Crew/Flows, process modes, CLI scaffolding, telemetry controls.
- [AutoGen 0.2 Reference](https://microsoft.github.io/autogen/0.2/docs/reference/) — Exact defaults/knobs for autonomy, code execution, and multi-agent chat orchestration.
- [Practical Guide to Building Agents (OpenAI PDF)](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf) — Production-oriented orchestration patterns, guardrails, and run-loop termination conditions.