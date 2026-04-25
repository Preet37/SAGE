## Core Definitions

**Agentic framework**: A software framework for building “agents,” i.e., systems that “independently accomplish tasks on your behalf,” characterized by (1) the LLM controlling workflow execution (including deciding completion and potentially handing control back to a user) and (2) tool access for gathering context and taking actions within guardrails. (OpenAI, *A practical guide to building agents* https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)

**Control flow (in agent systems)**: The “native shape” of how an agent system decides what happens next—e.g., explicit node/edge graphs, multi-agent turn-taking conversation, role-based task delegation, or a managed tool-calling loop with sessions and guardrails. (Synthesized from: LangGraph graph model discussions; AutoGen AgentChat orchestration entry points; CrewAI Flow/Crew model; OpenAI agent loop description in the practical guide.)

**LangGraph**: A low-level orchestration framework and runtime for building long-running, stateful agents/workflows using explicit graphs (nodes + edges) with built-in persistence (checkpointing), streaming, and human-in-the-loop support. It is “inspired by Pregel and Apache Beam.” (LangGraph repo + docs: https://github.com/langchain-ai/langgraph ; https://langchain-ai.github.io/langgraph/)

**State (LangGraph)**: A shared snapshot passed to nodes, defined by a schema (e.g., `TypedDict`/Pydantic in Python or `Annotation.Root` in JS/TS) where each key can have a reducer that specifies how node updates merge into the accumulated state. (LangGraph discussions #4730, #938, #3459)

**Reducer (LangGraph)**: Per-state-key merge logic applied when a node returns a partial update. If no reducer is specified, updates overwrite prior values; with a reducer, the new value is computed as `reducer(old_value, update_value)`. (LangGraph discussions #3459, #3810)

**Node (LangGraph)**: A function that reads current state and returns a partial state update (a dict of keys → values). Nodes may run in parallel in a super-step depending on graph routing. (LangGraph discussions #938, #3346)

**Edge / conditional edge (LangGraph)**: Routing logic that determines which node(s) execute next. Conditional edges evaluate a router function after a node runs; the router returns a label that maps to a next node or `END`. (LangGraph discussion #3346)

**Super-step (LangGraph)**: A discrete “tick” of execution where all scheduled nodes for that step execute (potentially in parallel), then their updates are applied deterministically; checkpoints are created at super-step boundaries when persistence is enabled. (LangGraph persistence docs + discussions #2290, #938; JS persistence reference: https://docs.langchain.com/oss/javascript/langgraph/persistence)

**Checkpoint (LangGraph)**: A snapshot of a thread’s graph state at a super-step boundary (a `StateSnapshot`), including state values, which nodes are next, config (thread/checkpoint IDs), metadata, and task info (errors/interrupts). Enables memory, time travel, fault tolerance, and human-in-the-loop. (LangGraph JS persistence doc: https://docs.langchain.com/oss/javascript/langgraph/persistence ; LangGraph persistence concept pages: https://docs.langchain.com/oss/python/langgraph/persistence)

**Thread (LangGraph)**: A unique identifier (`thread_id`) grouping a sequence of checkpoints; used as the primary key for storing/retrieving checkpoints so runs can resume and accumulate state across invocations. (LangGraph persistence docs: https://docs.langchain.com/oss/python/langgraph/persistence ; AWS DynamoDBSaver blog)

**Durable execution (LangGraph)**: Saving progress at key points (super-steps) so a workflow can pause and later resume from the last recorded state, supporting long-running tasks, failures, and human-in-the-loop. If you compile with a checkpointer and pass a `thread_id`, durable execution is enabled. (LangGraph durable execution doc: https://docs.langchain.com/oss/python/langgraph/durable-execution)

**Interrupt / resume (LangGraph HITL)**: A mechanism to pause execution inside a node (e.g., `interrupt(...)`) and later resume from a persisted checkpoint with human input; designed to avoid redoing completed work and to support long waits without holding a process. (LangGraph discussions #2290, #938, #4730)

**AutoGen (AgentChat / v0.2)**: A framework for multi-agent AI applications where agents send/receive messages and generate replies using models/tools/human inputs; orchestration is commonly expressed as agent-to-agent conversation (e.g., `initiate_chat`) with turn limits and termination logic. (AutoGen v0.2 reference: https://microsoft.github.io/autogen/0.2/docs/reference/ ; ConversableAgent reference)

**ConversableAgent (AutoGen v0.2)**: A baseline AutoGen agent that auto-replies to messages unless termination conditions are met; supports configurable LLM, tool calls, code execution, and human input modes (`ALWAYS`, `TERMINATE`, `NEVER`) with an auto-reply limit. (AutoGen ConversableAgent reference: https://microsoft.github.io/autogen/0.2/docs/reference/agentchat/conversable_agent/)

**CrewAI**: An open-source framework for orchestrating multi-agent systems using (1) **Flows** as the event-driven, stateful orchestration backbone and (2) **Crews** as teams of role-playing agents that collaborate on tasks within a Flow. (CrewAI docs intro: https://docs.crewai.com/en/introduction ; CrewAI repo: https://github.com/crewAIInc/crewAI)

**Process mode (CrewAI)**: A Crew execution strategy such as `Process.sequential` or `Process.hierarchical` (hierarchical assigns a manager for planning/delegation/validation). (CrewAI repo: https://github.com/crewAIInc/crewAI)

**OpenAI agent loop / run exit conditions (Agents SDK framing)**: A run loop (e.g., `Runner.run()`) continues until either a final-output tool is invoked or the model returns a response without tool calls. (OpenAI practical guide PDF)

**Human-in-the-loop (HITL)**: A design where humans inspect, validate, approve, or modify an agent’s state/actions mid-execution; often triggered by high-risk actions or failure thresholds and implemented via interrupts/checkpoints (LangGraph) or signals/waits (Temporal). (OpenAI practical guide PDF; LangGraph persistence/durable execution docs; Temporal HITL tutorial)

---

## Key Formulas & Empirical Results

### LangGraph checkpoint sizing / throughput math
- **Checkpoint write rate sizing**:  
  **writes/sec = steps_per_request × requests/sec**  
  Example given: **12 steps/request** and **2,000 req/s ⇒ 24,000 writes/s**.  
  Supports: planning storage/IOPS for step-level checkpointing in production. (Aerospike LangGraph production blog: https://aerospike.com/blog/langgraph-production-latency-replay-scale)

### LangGraph checkpoint storage split (DynamoDBSaver)
- **Small checkpoint threshold**: `< 350 KB` stored directly in DynamoDB; `≥ 350 KB` stored in S3 with DynamoDB pointer.  
  Supports: understanding durability architecture and cost/perf knobs. (AWS DynamoDBSaver blog: https://aws.amazon.com/blogs/database/build-durable-ai-agents-with-langgraph-and-amazon-dynamodb/)

### LangGraph “sequential graph” checkpoint count
- For `START -> A -> B -> END`, a single invoke yields **exactly 4 checkpoints** (START/empty, after input, after A, after B/END).  
  Supports: explaining super-step boundaries and time travel granularity. (LangGraph JS persistence doc: https://docs.langchain.com/oss/javascript/langgraph/persistence ; AWS blog echoes similar)

### AutoGen v0.2 defaults/knobs (selected)
- `code_execution_config=False` (code execution off in examples; default off). (AutoGen reference: https://microsoft.github.io/autogen/0.2/docs/reference/)
- `human_input_mode="TERMINATE"` default for `ConversableAgent.__init__`. (ConversableAgent reference)
- `max_turns` used to cap multi-agent chat (example: `max_turns=2`). (AutoGen reference)

### Benchmarks (MCP Server + LangGraph comparisons)
Empirical results under stated methodology (GCP n2-standard-4; Gemini 2.0 Flash; k6 load; 5 min runs; avg of 3):
- **Simple Agent (MCP+LangGraph, Cloud Run self-hosted)**: **142 req/s**, p50 **245ms**, p95 **890ms**, p99 **1210ms**, error **0.02%**.  
- **Multi-Agent 3-step (MCP+LangGraph on GKE)**: **48 req/s**, p50 **1850ms**, p95 **4200ms**, p99 **6100ms**, error **0.08%**.  
- **Multi-Agent (CrewAI self-hosted)**: **52 req/s**, p50 **1650ms**, p95 **3800ms**, p99 **5400ms**, error **0.12%**.  
- **Complex 5-node conditional graph (MCP+LangGraph)**: **32 req/s**, p50 **2800ms**, p95 **6500ms**, p99 **9200ms**, error **0.15%**.  
Supports: “orchestration overhead” and tradeoffs across frameworks for certain shapes (sequential multi-agent vs conditional graph). (Benchmarks page: https://mcp-server-langgraph.mintlify.app/comparisons/benchmarks)

### CrewAI repo claim (treat as vendor claim)
- Repo states: CrewAI Flows reported **5.76× faster** than LangGraph in a QA task example (linked notebook).  
Supports: discussing that performance claims vary by workload and measurement. (CrewAI repo: https://github.com/crewAIInc/crewAI)

---

## How It Works

### LangGraph execution mechanics (Pregel/BSP-style super-steps)
(From LangGraph discussions #2290, #938; JS persistence docs)

1. **Define State schema** with per-key reducers (or defaults to overwrite).
2. **Add nodes**: each node is `node(state) -> dict` returning partial updates.
3. **Add edges**: fixed edges or conditional edges (router function).
4. **Compile** the graph; optionally attach a **checkpointer** for persistence.
5. **Invoke** with input mapped into channels/state.
6. Runtime repeats per **super-step**:
   1) Determine **runnable nodes** (based on which subscribed channels changed / messages in transit).  
   2) Execute runnable nodes **in parallel** with isolated copies of state.  
   3) Collect node updates locally.  
   4) **Apply updates deterministically** to shared channels/state (prevents data races), bump channel versions.
7. **Stop condition**: no nodes runnable (all inactive) and no messages in transit, or an iteration/recursion limit is reached.

**Checkpointing hook** (when enabled): after each super-step boundary, persist a `StateSnapshot` (values, next nodes, config IDs, metadata, tasks).

### LangGraph reducers: overwrite vs append vs “atomic replace”
(From discussions #3459, #3810, #4730)

- Default: if a key has **no reducer**, node updates **overwrite** prior value.
- With reducer: `new_value = reducer(old_value, update_value)`.
- Common pattern: `messages` uses an append-style reducer (e.g., `add_messages` / `messagesStateReducer`) so nodes can return `{"messages": [new_msg]}` and history accumulates.
- If you need to **replace** a list atomically (avoid duplication on replay), define a replacement reducer that returns `right` as the new value. (Discussion #3810)

### LangGraph conditional routing (tool loop pattern)
(From discussion #3346)

1. Node (e.g., `chatbot`) runs and appends an AI message.
2. Router inspects the last message:
   - If it contains `tool_calls` and `len(tool_calls) > 0`, route to `"tools"`.
   - Else route to `END`.
3. Tool node executes tool calls, writes results to state.
4. Edge `"tools" -> "chatbot"` loops back so the LLM can decide next step.

### LangGraph persistence: thread_id + checkpoints + resume/replay
(From JS persistence docs; AWS DynamoDBSaver blog; issue #1568)

**Persist across invocations**
1. Compile with a checkpointer, e.g. `MemorySaver()` (in-memory) or DB-backed saver.
2. Invoke/stream with config containing:  
   `{"configurable": {"thread_id": "<id>"}}`
3. State is saved after each super-step; later calls with the same `thread_id` load the latest checkpoint and continue accumulating state.

**Resume from a specific checkpoint**
- Provide `checkpoint_id` in config to resume/replay after that checkpoint. (JS persistence docs)

**Pending writes**
- If a node fails mid-super-step, successful nodes’ writes are stored as **pending writes** so resuming doesn’t re-run successful nodes. (JS persistence docs; BaseCheckpointSaver.list reference)

**Common gotcha (messages not accumulating)**
- If you don’t use a checkpointer + thread_id, each run starts fresh, so `add_messages` won’t accumulate across separate invocations. (LangGraph issue #1568)

### Human-in-the-loop (LangGraph interrupt/resume)
(From discussions #2290, #938, #4730)

1. Inside a node, call `interrupt(payload)` to pause.
2. A checkpoint is available for inspection/editing.
3. Resume later by invoking with a resume command/input (e.g., `Command(resume=...)` in the Python example in #938).
4. Design note: when interrupts are possible, avoid parallel tool calling that could cause repeated tool invocations on resume; example asserts `len(message.tool_calls) <= 1`. (#4730, #3346)

### AutoGen v0.2 orchestration mechanics (AgentChat)
(From AutoGen reference + ConversableAgent reference)

- **Single-turn**: `generate_reply(messages=[...])`.
- **Multi-turn**: `initiate_chat(other_agent, message=..., max_turns=...)`.
- **Stopping/autonomy controls**:
  - `human_input_mode`: `ALWAYS`, `TERMINATE` (default), `NEVER`.
  - `max_consecutive_auto_reply` / `MAX_CONSECUTIVE_AUTO_REPLY` limit.
- **Reply chain order** (ConversableAgent): termination/human → tool calls → code execution → LLM reply.

### CrewAI mechanics (Flow + Crew)
(From CrewAI docs intro + repo)

1. **Flow** defines event-driven steps, state, branching/conditions (`@start`, `@listen`, `@router`, `or_`, `and_`).
2. A Flow step can invoke a **Crew** (team of agents) to complete a complex task.
3. **Crew** is configured with agents + tasks and a process mode (`sequential` or `hierarchical` manager pattern).
4. Run via `Crew.kickoff(inputs={...})` to fill task templates.

### Temporal HITL (useful comparison for “durable waits”)
(From Temporal tutorial: https://learn.temporal.io/tutorials/ai/building-durable-ai-applications/human-in-the-loop/)

1. Workflow does work (LLM activity), stores intermediate result.
2. Workflow calls `workflow.wait_condition(...)` to pause without consuming CPU.
3. External UI/service sends a **signal** with decision data.
4. Workflow resumes, either continues, loops with edits, or times out.

---

## Teaching Approaches

### Intuitive (no math): “Pick the framework whose default shape matches your app”
- **LangGraph**: you want a *diagram* (nodes/edges) you can reason about, pause, resume, and replay.
- **AutoGen**: you want *a conversation* among agents; orchestration is “who says what next.”
- **CrewAI**: you want *a team with roles* and a manager mode; a Flow coordinates when the team runs.
- **OpenAI Assistants/Agents SDK framing**: you want a managed tool-calling loop with clear stop conditions and guardrails (final tool or no tool calls).

### Technical: “Control-flow model determines persistence + determinism constraints”
- Graph/super-step runtimes (LangGraph) naturally define checkpoint boundaries and deterministic application of updates; reducers define merge semantics.
- Conversation runtimes (AutoGen) center on message passing and termination/turn limits; persistence is not the primary primitive in the cited v0.2 references.
- Flow/team runtimes (CrewAI) separate orchestration (Flow) from collaboration (Crew), with explicit process modes.
- Managed run loops (OpenAI practical guide) define exit conditions and encourage guardrails/human escalation triggers.

### Analogy-based
- **LangGraph** = a *state machine / workflow engine* with save points every “tick.”
- **AutoGen** = a *group chat* with rules for when to stop and when to ask a human.
- **CrewAI** = a *project manager (Flow)* who hires a *task force (Crew)* to deliver artifacts.
- **Temporal (comparison)** = a *durable business process engine* where “waiting for approval” is a first-class, crash-proof state.

---

## Common Misconceptions

1. **“If I use `add_messages`, my chat history will persist automatically.”**  
   - Why wrong: `add_messages` only defines *how updates merge within a run/thread*; without a checkpointer + `thread_id`, each invocation starts from scratch.  
   - Correct model: persistence requires compiling with a checkpointer and invoking with `{"configurable": {"thread_id": ...}}`. (LangGraph issue #1568; persistence docs)

2. **“A LangGraph node returning `{'messages': [...]}` overwrites the message list.”**  
   - Why wrong: if `messages` has an append reducer (common), returning `messages` appends; overwrite happens only when no reducer exists or you define a replacement reducer.  
   - Correct model: reducer semantics control append vs replace; to replace atomically, use a replacement reducer. (Discussions #4730, #3810)

3. **“Replay/resume means the code continues from the exact line where it stopped.”**  
   - Why wrong: LangGraph durable execution notes that on resume it replays from an appropriate starting point; side effects must be isolated to avoid duplication.  
   - Correct model: design for determinism/idempotency; wrap side effects/non-determinism in tasks/nodes so results can be retrieved from persistence rather than re-executed. (Durable execution doc; Aerospike blog)

4. **“Multi-agent is always better than single-agent; it’s just more powerful.”**  
   - Why wrong: OpenAI guidance emphasizes starting single-agent and moving to multi-agent when complexity/tool overload demands it; multi-agent adds coordination overhead and failure modes.  
   - Correct model: use multi-agent when you need specialization, reduced tool overload, or distinct interaction patterns (manager-as-tools vs decentralized handoffs). (OpenAI practical guide PDF)

5. **“Interrupts are just like tool calls; I can parallelize tool calls freely and still resume safely.”**  
   - Why wrong: LangGraph HITL examples caution against parallel tool calling when interrupts can occur, to avoid repeated tool invocations on resume; example asserts only one tool call.  
   - Correct model: when HITL interrupts are possible, constrain tool-call concurrency or design idempotent tool steps. (LangGraph discussion #4730; conditional routing #3346)

---

## Worked Examples

### Example 1 (LangGraph): messages “not accumulating” until you add a checkpointer + thread_id
This mirrors the exact failure mode in LangGraph issue #1568.

```python
from typing import Annotated
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver

from langchain_openai import ChatOpenAI

class State(TypedDict):
    messages: Annotated[list, add_messages]

model = ChatOpenAI(temperature=0.1, model_name="gpt-3.5-turbo")

def chatbot(state: State):
    # Prints the accumulated state for this thread
    print("STATE:", state)
    return {"messages": [model.invoke(state["messages"])]}

builder = StateGraph(State)
builder.add_node("chatbot", chatbot)
builder.add_edge(START, "chatbot")
builder.add_edge("chatbot", END)

# Key fix: compile with a checkpointer
graph = builder.compile(checkpointer=MemorySaver())

thread_config = {"configurable": {"thread_id": "1"}}

while True:
    user_input = input("User: ")
    if user_input.lower() in ["quit", "exit", "q"]:
        break

    # Key fix: pass thread_id each time
    for event in graph.stream({"messages": ("user", user_input)}, thread_config):
        for value in event.values():
            print("Assistant:", value["messages"][-1].content)
```

**Tutor notes (what to point out live):**
- Without `checkpointer=MemorySaver()` and `thread_id`, each loop iteration is a fresh run; state prints only the latest user message (issue #1568).
- With them, state prints the growing message list for thread `"1"`.

### Example 2 (LangGraph): conditional edge tool loop router (core semantics)
Router logic from discussion #3346 (simplified):

```python
from langgraph.graph import END

def route_tools(state):
    # state can be list-of-messages or dict with "messages"
    messages = state if isinstance(state, list) else state.get("messages", [])
    if not messages:
        raise ValueError("No messages found")

    last = messages[-1]
    if getattr(last, "tool_calls", None) and len(last.tool_calls) > 0:
        return "tools"
    return END
```

**Tutor notes:**
- The router returns a *label*; `add_conditional_edges(..., mapping=...)` maps that label to a node name or `END`.
- This is the canonical “LLM decides whether to call tools” loop.

### Example 3 (AutoGen v0.2): cap a multi-agent chat with `max_turns`
From AutoGen reference patterns:

```python
# Pseudocode sketch based on AutoGen v0.2 docs
assistant.initiate_chat(other_agent, message="Draft a plan", max_turns=2)
```

**Tutor notes:**
- Use `max_turns` to prevent runaway conversations.
- Combine with `human_input_mode` and auto-reply limits for HITL control (ConversableAgent reference).

---

## Comparisons & Trade-offs

| Framework | “Native shape” of control flow | Strengths (from sources) | Typical pain points / watchouts (from sources) | Best fit signals |
|---|---|---|---|---|
| **LangGraph** | Explicit **graph** (nodes/edges), **super-steps**, reducers; durable checkpoints per step | Durable execution, HITL interrupts, time travel, fault tolerance via checkpointers; deterministic update application (Pregel-style) (docs/discussions) | Must design for determinism/idempotency; replay can re-trigger side effects unless isolated; reducers can duplicate on replay if append-only; need `thread_id` for persistence (durable exec docs; #3810; #1568) | You need explicit branching/loops, resumability, auditability, long-running workflows |
| **AutoGen (v0.2)** | **Multi-agent conversation** with termination/turn limits | Simple agent-to-agent orchestration via chat; configurable human input modes; optional code execution (refs) | Project is in maintenance mode per repo; orchestration is message-centric (may be less explicit than graphs for complex branching) (repo notice; refs) | You want conversational multi-agent patterns and quick prototyping of agent dialogues |
| **CrewAI** | **Flow** (orchestration backbone) + **Crew** (role-based team) | Clear separation: Flow manages state/control; Crews handle collaborative work; process modes sequential/hierarchical (docs/repo) | Performance claims vary by workload (repo claim vs other benchmarks); need to choose process mode and manage telemetry settings (repo) | You want role/task abstractions and a “team” metaphor with a coordinating Flow |
| **OpenAI Assistants/Agents SDK (conceptual from practical guide)** | Managed **tool-calling loop** with run exit conditions | Clear run loop stop conditions; strong emphasis on guardrails, risk-rating tools, and escalation triggers; guidance on when to go multi-agent (practical guide) | Tool overload can reduce accuracy; need guardrails and evals; multi-agent adds overhead (practical guide) | You want a managed loop + guardrails-first production guidance; start single-agent then scale |

**Selection heuristic to use in tutoring** (grounded in sources):
- If the student keeps asking “how do I pause, resume, and not lose state?” → LangGraph persistence/checkpointers/threads (LangGraph persistence docs; AWS blog).
- If they ask “how do I get multiple specialists to talk and stop after N turns?” → AutoGen `initiate_chat(..., max_turns=...)` + termination/human_input_mode (AutoGen refs).
- If they ask “how do I model a team with roles and a manager?” → CrewAI Crews + hierarchical process; Flow as backbone (CrewAI docs/repo).
- If they ask “how do I ship safely with guardrails and escalation?” → OpenAI practical guide guardrails + risk-rated tools + human triggers.

---

## Prerequisite Connections

- **Tool calling / function calling**: Needed to understand tool-loop routing (LangGraph conditional edges; OpenAI agent loop). (LangGraph #3346; OpenAI practical guide)
- **State + immutability/merging**: Needed to reason about reducers, overwrites vs appends, and replay duplication. (LangGraph #3459, #3810)
- **Determinism & idempotency**: Needed to understand durable execution and why side effects must be isolated. (LangGraph durable execution doc; Aerospike blog; Temporal replay concepts)
- **Basic concurrency intuition**: Helpful for super-steps, parallel node execution, and deterministic update application. (LangGraph #2290)

---

## Socratic Question Bank

1. **“If your agent crashes after calling an external ‘charge credit card’ tool, what guarantees do you need so resume doesn’t double-charge?”**  
   Good answer: isolate side effects into tasks/nodes; design idempotency; rely on checkpoints/pending writes; understand replay can re-trigger calls. (LangGraph durable execution doc; Aerospike blog)

2. **“In LangGraph, if two nodes both update `bar` in the same step, how do those updates combine?”**  
   Good answer: reducer defines merge; updates applied deterministically at super-step boundary; without reducer last write overwrites. (LangGraph #2290, #3459)

3. **“What’s the difference between ‘messages not accumulating’ and ‘messages accumulating but duplicating’?”**  
   Good answer: not accumulating = no persistence/thread; duplicating = append reducer + replay/retry re-executions; fix with replacement reducer or idempotent logic. (#1568; #3810)

4. **“When would you choose a conversation-based multi-agent orchestration over an explicit graph?”**  
   Good answer: when the coordination is naturally turn-taking and bounded by turns/termination; less need for explicit branching/checkpoint semantics. (AutoGen refs vs LangGraph model)

5. **“What does it mean that checkpoints happen at super-step boundaries—what can’t you do because of that?”**  
   Good answer: you can only resume/time-travel from those boundaries, not arbitrary lines inside a node. (LangGraph persistence docs)

6. **“If you add 25 tools to a single agent and accuracy drops, what architecture change does OpenAI suggest considering?”**  
   Good answer: move to multi-agent when tool overload/complex logic; manager-as-tools or decentralized handoffs. (OpenAI practical guide)

7. **“In CrewAI, what’s the conceptual difference between a Flow and a Crew?”**  
   Good answer: Flow is orchestration backbone (state/control/events); Crew is the collaborating team that executes tasks. (CrewAI docs intro)

8. **“How does AutoGen decide when to ask a human for input?”**  
   Good answer: `human_input_mode` rules + termination messages + auto-reply limit `N`. (ConversableAgent reference)

---

## Likely Student Questions

**Q: “Why is my LangGraph `add_messages` not appending across turns?”**  
→ **A:** Because without a checkpointer + `thread_id`, each invocation restarts the graph. Compile with a checkpointer (e.g., `MemorySaver()`) and pass `{"configurable": {"thread_id": "1"}}` on each call to persist and reload state. (LangGraph issue #1568; persistence docs)

**Q: “What exactly is stored in a LangGraph checkpoint?”**  
→ **A:** A `StateSnapshot` including `values` (state channel values), `next` (next nodes), `config` (`thread_id`, `checkpoint_id`, `checkpoint_ns`), `metadata` (source/writes/step), timestamps, and `tasks` (errors/interrupts; may include subgraph state). (LangGraph JS persistence doc)

**Q: “How many checkpoints should I expect for a simple sequential graph?”**  
→ **A:** For `START -> A -> B -> END`, one invoke yields **4 checkpoints**: START/empty, after input, after A, after B/END. (LangGraph JS persistence doc; AWS blog)

**Q: “How does LangGraph decide which node runs next in a tool loop?”**  
→ **A:** Use `add_conditional_edges` with a router that inspects the last AI message; if it has `tool_calls`, route to the tools node; otherwise route to `END`. Then add a normal edge from tools back to chatbot to loop. (LangGraph discussion #3346)

**Q: “What’s the core difference between overwrite and append in LangGraph state updates?”**  
→ **A:** Keys without reducers overwrite prior values; keys with reducers merge via `new_value = reducer(old_value, update_value)`. Messages commonly use an append reducer; to replace atomically, define a replacement reducer. (LangGraph #3459, #3810)

**Q: “How do I cap an AutoGen multi-agent conversation so it doesn’t run forever?”**  
→ **A:** Use `initiate_chat(..., max_turns=...)` (example shows `max_turns=2`) and/or set `max_consecutive_auto_reply` / `MAX_CONSECUTIVE_AUTO_REPLY`. (AutoGen reference; ConversableAgent reference)

**Q: “What are CrewAI’s main building blocks?”**  
→ **A:** **Flows** are the orchestration backbone (stateful, event-driven control flow); **Crews** are teams of role-playing agents that collaborate on tasks inside a Flow. (CrewAI docs intro)

**Q: “How do I estimate checkpoint storage load for a LangGraph deployment?”**  
→ **A:** Use **writes/sec = steps_per_request × requests/sec**; e.g., 12 steps/request at 2,000 req/s implies 24,000 writes/s. (Aerospike LangGraph production blog)

---

## Available Resources

### Videos
- [Intro to Large Language Models](https://youtube.com/watch?v=zjkBMFhNj_g) — Surface when: student lacks grounding on what an “agent loop” is (model + tools + memory) before comparing frameworks.
- [OpenAI Function Calling - Full Beginner Walkthrough](https://youtube.com/watch?v=aqdWSYWC_LI) — Surface when: student is confused about tool calls vs normal responses (needed for tool-loop routing discussions).
- [Multi-Agent Systems with LangGraph](https://youtube.com/watch?v=Mi5wOpAgixw) — Surface when: student wants to see explicit graph-based multi-agent orchestration patterns.

### Articles & Tutorials
- [Lilian Weng — LLM Powered Autonomous Agents](https://lilianweng.github.io/posts/2023-06-23-agent/) — Surface when: student needs the canonical conceptual pillars (planning, memory, tools, action) before framework tradeoffs.
- [LangGraph agentic concepts](https://langchain-ai.github.io/langgraph/concepts/agentic_concepts/) — Surface when: student asks for orchestration patterns (supervisor/hierarchical) in graph form.
- [ReAct (Yao et al., 2022)](https://arxiv.org/abs/2210.03629) — Surface when: student asks where the “reason → act → observe” loop comes from.
- [OpenAI Agents SDK (Python)](https://openai.github.io/openai-agents-python/) — Surface when: student wants implementation details beyond the practical guide’s conceptual run loop.
- [LangGraph multi-agent workflows blog](https://blog.langchain.dev/langgraph-multi-agent-workflows) — Surface when: student wants examples of multi-agent orchestration in LangGraph.

---

## Visual Aids

![CrewAI Flows: orchestration backbone for multi-agent tasks (CrewAI Docs).](/api/wiki-images/agent-workflows/images/docs-crewai-en-introduction_001.png)  
Show when: student confuses “agents” with “orchestration” in CrewAI; use to point to Flow as backbone vs Crew as team.

![LangGraph in-memory checkpointing with InMemorySaver (AWS Database Blog).](/api/wiki-images/agent-workflows/images/aws-amazon-blogs-database-build-durable-ai-agents-with-langgraph-and-amazon-dyna_001.png)  
Show when: student asks why state disappears after restart or why `thread_id` matters; use to visualize checkpointing.

![Durable LangGraph checkpoints using DynamoDBSaver and Amazon DynamoDB (AWS Database Blog).](/api/wiki-images/agent-workflows/images/aws-amazon-blogs-database-build-durable-ai-agents-with-langgraph-and-amazon-dyna_002.png)  
Show when: student asks “how do I make this production-durable across workers?”; highlight DynamoDB/S3 split and durability.

![Update persisted state to continue or branch a run (LangChain LangGraph docs).](/api/wiki-images/agent-workflows/images/docs-langchain-oss-python-langgraph-persistence_004.jpg)  
Show when: student asks about human-in-the-loop edits or “time travel” branching from checkpoints.

![Update persisted state to continue or branch a run (LangChain LangGraph docs).](/api/wiki-images/agent-workflows/images/docs-langchain-oss-python-langgraph-persistence_008.jpg)  
Show when: student asks for another view of state patching/resume; reinforces that edits create new checkpoints.

---

## Key Sources

- [A practical guide to building agents (OpenAI)](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf) — Defines agents, run loop exit conditions, multi-agent patterns, and guardrails/HITL triggers.
- [LangGraph Persistence (JS docs)](https://docs.langchain.com/oss/javascript/langgraph/persistence) — Most concrete description of threads/checkpoints/StateSnapshot fields, replay semantics, and pending writes.
- [LangGraph durable execution (Python docs)](https://docs.langchain.com/oss/python/langgraph/durable-execution) — Determinism/idempotency requirements and how resume/replay behaves.
- [AutoGen v0.2 AgentChat reference](https://microsoft.github.io/autogen/0.2/docs/reference/) and [ConversableAgent reference](https://microsoft.github.io/autogen/0.2/docs/reference/agentchat/conversable_agent/) — Core knobs for multi-agent conversation orchestration, human input modes, and termination limits.
- [CrewAI introduction](https://docs.crewai.com/en/introduction) — Authoritative description of Flow vs Crew architecture and when to use each.