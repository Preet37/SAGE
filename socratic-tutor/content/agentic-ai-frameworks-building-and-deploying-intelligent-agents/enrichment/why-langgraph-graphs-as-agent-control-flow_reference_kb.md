## Core Definitions

**LangGraph**: LangGraph is “a low-level orchestration framework and runtime for building, managing, and deploying long-running, stateful agents,” focused on orchestration capabilities like durable execution, streaming, and human-in-the-loop workflows rather than prescribing prompts or a single agent architecture (LangGraph README: https://github.com/langchain-ai/langgraph; Intro tutorial: https://langchain-ai.github.io/langgraph/tutorials/introduction/).

**Graph-based orchestration (graphs as control flow)**: In LangGraph, an agent/workflow is modeled as a graph where **nodes do the work** and **edges determine what runs next**; this explicit control-flow graph supports branching, merging, and looping (including cyclic graphs) beyond linear chains (Graph API overview: https://docs.langchain.com/oss/python/langgraph/graph-api; AWS DynamoDB blog: https://aws.amazon.com/blogs/database/build-durable-ai-agents-with-langgraph-and-amazon-dynamodb/).

**State (agent state / shared state)**: State is the shared data structure representing the current snapshot of the application; nodes read the current state and return partial updates that are merged into the shared state (Graph API overview: https://docs.langchain.com/oss/python/langgraph/graph-api). In LangGraph discussions, state is described as a shared snapshot passed to nodes, typically defined via `TypedDict`/Pydantic plus **reducers** that specify how updates apply (Discussion #4730: https://github.com/langchain-ai/langgraph/discussions/4730; Discussion #938: https://github.com/langchain-ai/langgraph/discussions/938).

**Nodes**: Nodes are functions that encode the logic of a step/actor. They receive the current state as input and return a **partial state update** (a dict of keys → values) that will be merged into the shared state (Graph API overview: https://docs.langchain.com/oss/python/langgraph/graph-api; StateGraph signature reference: https://www.langgraphcn.org/reference/graphs/).

**Edges (fixed and conditional)**: Edges define control flow: fixed transitions always go to the same next node; conditional edges run a routing function on the current state and map its output to the next node(s) or `END` (Discussion #3346: https://github.com/langchain-ai/langgraph/discussions/3346; Graph API overview: https://docs.langchain.com/oss/python/langgraph/graph-api).

**Reducers (state update rules)**: Reducers are per-state-key merge functions that define how a node’s update is combined with the existing value. If a key has no reducer, updates overwrite the previous value; if it has a reducer, updates are combined using `new_value = reducer(old_value, update_value)` (Discussion #3459: https://github.com/langchain-ai/langgraph/discussions/3459; Discussion #3914: https://github.com/langchain-ai/langgraph/discussions/3914; Graph API “reducers” section: https://docs.langchain.com/oss/python/langgraph/use-graph-api).

**Cyclic graphs (loops)**: LangGraph graphs can be cyclic: edges can route back to earlier nodes (e.g., tool loop `chatbot -> tools -> chatbot`) enabling iterative agent behavior rather than one-pass pipelines (AWS DynamoDB blog: https://aws.amazon.com/blogs/database/build-durable-ai-agents-with-langgraph-and-amazon-dynamodb/; Discussion #3346: https://github.com/langchain-ai/langgraph/discussions/3346).

**Super-step**: LangGraph execution proceeds in discrete “super-steps” (Pregel-inspired). In a super-step, all nodes scheduled for that step execute (potentially in parallel), then their updates are applied; checkpoints (if enabled) are created at super-step boundaries (Graph API overview: https://docs.langchain.com/oss/python/langgraph/graph-api; JS persistence reference: https://docs.langchain.com/oss/javascript/langgraph/persistence; Aerospike blog: https://aerospike.com/blog/langgraph-production-latency-replay-scale).

**Checkpoint**: A checkpoint is a snapshot of graph state saved at each super-step, represented as a `StateSnapshot` containing state values, next nodes, config (including `thread_id` and `checkpoint_id`), metadata, and task info (AWS DynamoDB blog: https://aws.amazon.com/blogs/database/build-durable-ai-agents-with-langgraph-and-amazon-dynamodb/; JS checkpointer reference: https://reference.langchain.com/javascript/langchain-langgraph/index/CompiledStateGraph/checkpointer; Python checkpoints reference: https://reference.langchain.com/python/langgraph/checkpoints/).

**Thread (`thread_id`)**: A thread is the unique identifier grouping a sequence of checkpoints (accumulated state across runs). When invoking a graph with a checkpointer, you must pass `configurable.thread_id`; the checkpointer uses it as the primary key to store/retrieve checkpoints and to resume after interrupts (LangGraph persistence docs: https://docs.langchain.com/oss/python/langgraph/persistence; AWS DynamoDB blog: https://aws.amazon.com/blogs/database/build-durable-ai-agents-with-langgraph-and-amazon-dynamodb/; Python checkpoints reference: https://reference.langchain.com/python/langgraph/checkpoints/).

**Durable execution (persistence)**: Durable execution is LangGraph’s ability to persist state at step boundaries so runs can resume after failures, support human-in-the-loop pauses, enable time-travel debugging, and provide fault tolerance (LangGraph v0.2 blog: https://blog.langchain.com/langgraph-v0-2/; persistence docs: https://docs.langchain.com/oss/python/langgraph/persistence; AWS DynamoDB blog: https://aws.amazon.com/blogs/database/build-durable-ai-agents-with-langgraph-and-amazon-dynamodb/).

**Interrupt / human-in-the-loop (HITL)**: `interrupt(value)` pauses execution by raising a `GraphInterrupt` and surfacing `value` to the client; later the graph resumes via `Command(resume=...)` and re-executes the node from the start. Interrupts require checkpointing (Python types reference: https://reference.langchain.com/python/langgraph/types/; Discussion #2290: https://github.com/langchain-ai/langgraph/discussions/2290).

---

## Key Formulas & Empirical Results

### Checkpoint write-rate sizing (production IOPS)
**Formula (Aerospike blog)**:  
**writes/sec = steps_per_request × requests/sec** (https://aerospike.com/blog/langgraph-production-latency-replay-scale)  
- **Supports**: sizing persistence infrastructure; super-step checkpointing means write volume scales with number of steps, not wall-clock time.  
- **Example from source**: 12 steps/request and 2,000 req/s ⇒ 24,000 writes/s.

### Checkpoint count for a simple sequential graph
For `START -> A -> B -> END`, a single invocation yields **exactly 4 checkpoints**: empty at `START`, after input (before `A`), after `A` (before `B`), and final after `B` at `END` (AWS DynamoDB blog: https://aws.amazon.com/blogs/database/build-durable-ai-agents-with-langgraph-and-amazon-dynamodb/; JS persistence reference: https://docs.langchain.com/oss/javascript/langgraph/persistence; Python checkpoints reference: https://reference.langchain.com/python/langgraph/checkpoints/).

### DynamoDBSaver storage threshold
**Rule (AWS DynamoDB blog)**: checkpoints **< 350 KB** stored directly in DynamoDB; **≥ 350 KB** stored in S3 with a DynamoDB pointer (https://aws.amazon.com/blogs/database/build-durable-ai-agents-with-langgraph-and-amazon-dynamodb/).  
- **Supports**: practical durability design for large state payloads.

### RetryPolicy defaults (LangGraph runtime)
From the Python runtime types reference (v0.2.24 defaults):  
`initial_interval=0.5s`, `backoff_factor=2.0`, `max_interval=128.0s`, `max_attempts=3`, `jitter=True` (https://reference.langchain.com/python/langgraph/types/).  
- **Supports**: answering “what are the default retries?” during debugging/production hardening.

### Streaming default (JS)
`CompiledStateGraph.streamMode` defaults to `["values"]` (JS reference: https://reference.langchain.com/javascript/langchain-langgraph/index/CompiledStateGraph/streamMode; CompiledStateGraph class reference: https://reference.langchain.com/javascript/classes/_langchain_langgraph.index.CompiledStateGraph.html).

### Benchmarks (MCP Server + LangGraph)
From MCP server benchmark page (Gemini 2.0 Flash; 5-min runs; avg of 3):  
- Simple Agent (Cloud Run self-hosted): **142 req/s**, p50 **245ms**, p95 **890ms**, error **0.02%**  
- Complex 5-node conditional graph: **32 req/s**, p50 **2800ms**, p95 **6500ms**, error **0.15%** (https://mcp-server-langgraph.mintlify.app/comparisons/benchmarks).  
- **Supports**: quantitative discussion of orchestration + persistence overhead under load.

---

## How It Works

### 1) Build-time: define state, nodes, edges
1. **Define a state schema** (often `TypedDict` / Pydantic).  
   - Each key can optionally define a **reducer**; otherwise it overwrites (Graph API overview: https://docs.langchain.com/oss/python/langgraph/graph-api; reducers guide: https://docs.langchain.com/oss/python/langgraph/use-graph-api).
2. **Add nodes**: each node is a function `node(state) -> dict` returning partial updates (Graph API overview).
3. **Add edges**:
   - Fixed: `START -> node -> END`
   - Conditional: `add_conditional_edges(from_node, router_fn, mapping)` (Discussion #3346).
4. **Compile** the graph:
   - Compilation validates structure (e.g., no orphaned nodes) and is where you configure runtime features like checkpointers and interrupts (Graph API overview; `StateGraph.compile()` reference: https://reference.langchain.com/python/langgraph/graph/state/StateGraph/compile).

### 2) Run-time: Pregel-style super-steps (deterministic message passing)
LangGraph’s Graph API describes a Pregel-inspired execution model (https://docs.langchain.com/oss/python/langgraph/graph-api), elaborated in discussions (e.g., #2290, #938):

1. **Initialization**: all nodes start inactive.
2. **Activation**: a node becomes active when it receives a message/state update on an incoming edge/channel.
3. **Super-step loop**:
   1) Determine which nodes are runnable (based on incoming messages / channel version changes).  
   2) Execute runnable nodes (potentially in parallel).  
   3) Collect each node’s returned partial updates.  
   4) **Apply updates** to shared state using reducers, in a deterministic way (Discussion #2290 describes deterministic ordering to prevent races).
4. **Halting**: nodes with no incoming messages “vote to halt” (become inactive). Execution ends when all nodes are inactive and no messages are in transit (Graph API overview).

### 3) State merging: reducers decide overwrite vs accumulate
When multiple nodes write the same key in the same super-step, LangGraph merges field-by-field using reducers (Discussion #3914):
- **No reducer** ⇒ overwrite (last write wins).
- **Reducer present** ⇒ `reducer(existing, update)` combines values (e.g., append messages, add counters).

**Messages reducer (`add_messages`) specifics** (source code: https://github.com/langchain-ai/langgraph/blob/main/libs/langgraph/langgraph/graph/message.py):
- Coerces inputs to lists of `BaseMessage`.
- Assigns missing message IDs.
- Merges by message ID: if an incoming message has an existing ID, it replaces that message; supports deletions via `RemoveMessage` and a `__remove_all__` sentinel.

### 4) Conditional routing: how “next node” is chosen
From Discussion #3346 (https://github.com/langchain-ai/langgraph/discussions/3346):
1. Execute node `A` and merge its updates into state.
2. Run router function on the current state (or messages list).
3. Router returns a label (e.g., `"tools"` or `END`).
4. Mapping dict translates label → node name (or identity if omitted).
5. The chosen node(s) are scheduled for the next super-step.

### 5) Persistence: checkpoints, threads, resume/replay
When compiled with a **checkpointer**, LangGraph saves a checkpoint at every super-step (JS checkpointer reference: https://reference.langchain.com/javascript/langchain-langgraph/index/CompiledStateGraph/checkpointer; Python persistence docs: https://docs.langchain.com/oss/python/langgraph/persistence).

**Mechanics**:
1. Compile with a checkpointer (e.g., `MemorySaver`, DB-backed saver).
2. Invoke with config containing `{"configurable": {"thread_id": "<id>"}}`.
3. After each super-step, a `StateSnapshot` is persisted.
4. Later invocations with the same `thread_id` load the latest checkpoint and continue.

**Replay**:
- You can invoke with a prior `checkpoint_id` to replay from that point; steps after that checkpoint are re-executed, including LLM/tool calls and interrupts (JS persistence reference: https://docs.langchain.com/oss/javascript/langgraph/persistence; Python checkpoints reference: https://reference.langchain.com/python/langgraph/checkpoints/).

**Pending writes / fault tolerance**:
- If a node fails mid super-step, LangGraph stores pending writes from successful nodes; on resume you don’t re-run successful nodes (persistence docs: https://docs.langchain.com/oss/python/langgraph/persistence; JS persistence reference).

### 6) Human-in-the-loop: interrupt and resume
From Python types reference (https://reference.langchain.com/python/langgraph/types/) and discussions (#2290, #4730):
1. Inside a node, call `interrupt(payload)`.
2. First call raises `GraphInterrupt` and surfaces payload to client; graph pauses.
3. Client resumes by invoking with `Command(resume=...)`.
4. Node is re-executed from the start; resume values are provided in call order.
5. **Requires checkpointing**; otherwise there is no durable pause/resume point.

---

## Teaching Approaches

### Intuitive (no math)
“LangGraph is a *workflow engine* for agents. Instead of writing one big `while True:` loop, you draw the loop as a graph: each node is a step (think, call tool, summarize, ask human), and edges decide what happens next. Because the runtime knows the structure, it can pause, resume, branch, and keep state reliably.”

### Technical (with execution model)
“LangGraph runs a Pregel-style bulk-synchronous parallel (BSP) loop: in each super-step it executes all runnable nodes (possibly in parallel), then applies their partial state updates using per-key reducers. Checkpointing persists a `StateSnapshot` at each super-step boundary keyed by `thread_id`, enabling deterministic resume/replay and HITL interrupts.”

### Analogy-based
- **Finite state machine / statechart**: nodes are states/handlers; edges are transitions; state is the extended state.  
- **Database transaction log**: checkpoints are like commit points; you can replay from a commit; interrupts are like waiting for an external approval event, but you can restart the process and continue because the “log” (checkpoints) is persisted.

---

## Common Misconceptions (required)

1) **“A LangGraph node returns the whole new state.”**  
   - **Why wrong**: The node contract is `State -> Partial<State>`; nodes return only the keys they want to update, and LangGraph merges them into shared state (Graph API overview: https://docs.langchain.com/oss/python/langgraph/graph-api; StateGraph signature: https://www.langgraphcn.org/reference/graphs/).  
   - **Correct model**: Nodes emit *patches*; reducers decide how patches combine with existing values.

2) **“My `messages` should append automatically because I used `add_messages`—but it keeps overwriting.”**  
   - **Why wrong (common root cause)**: Without checkpointing + consistent `thread_id`, each run starts from fresh state, so you only see the current turn’s messages even if the reducer is correct. This exact confusion appears in issue #1568; the fix is to compile with a checkpointer and pass `thread_id` (Issue #1568: https://github.com/langchain-ai/langgraph/issues/1568; persistence docs: https://docs.langchain.com/oss/python/langgraph/persistence).  
   - **Correct model**: Reducers merge *within a run’s state evolution*; persistence + `thread_id` is what makes state accumulate across separate invocations.

3) **“Conditional edges pick exactly one path, so downstream nodes will run exactly once.”**  
   - **Why wrong**: LangGraph’s parallel/super-step semantics can make convergence behavior non-obvious when branches reconverge; a PR introduces `workflow_mode=True` to enforce “execute exactly once” workflow expectations in some conditional-branch shapes (PR #3345: https://github.com/langchain-ai/langgraph/pull/3345).  
   - **Correct model**: Default mode is message-passing + parallel scheduling; if you need strict workflow semantics for dynamic branching/convergence, consider `workflow_mode=True` (with required `path_map` or `Literal` coverage per PR).

4) **“Interrupts are just like `input()`—I can pause without persistence.”**  
   - **Why wrong**: `interrupt()` raises `GraphInterrupt` and requires checkpointing to resume later; otherwise there’s no saved super-step boundary to restart from (Python types reference: https://reference.langchain.com/python/langgraph/types/; persistence docs: https://docs.langchain.com/oss/python/langgraph/persistence).  
   - **Correct model**: Interrupts are a durable pause/resume mechanism built on checkpoints + threads.

5) **“Parallel branches will ‘just merge’ their outputs.”**  
   - **Why wrong**: Without reducers, updates overwrite; parallel writes to the same key can appear to drop data (Discussion #3914: https://github.com/langchain-ai/langgraph/discussions/3914).  
   - **Correct model**: If multiple nodes may write the same key in the same super-step, define a reducer for that key (e.g., `operator.add`, dict merge, `add_messages`).

---

## Worked Examples

### Example 1 (Python): Minimal graph + durable conversation memory (fixing the “messages overwrite” confusion)

This example mirrors the pattern referenced in issue #1568: compile with a checkpointer and pass `thread_id` so `add_messages` can accumulate across turns.

```python
from typing import Annotated
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver

# 1) Define state with a reducer for messages
class State(TypedDict):
    messages: Annotated[list, add_messages]

# 2) Define a node that appends an AI message (mocked here)
def chatbot(state: State):
    # In a real app you'd call a chat model with state["messages"]
    return {"messages": [{"role": "ai", "content": f"Echo: {state['messages'][-1]['content']}"}]}

# 3) Build graph
builder = StateGraph(State)
builder.add_node("chatbot", chatbot)
builder.add_edge(START, "chatbot")
builder.add_edge("chatbot", END)

# 4) Compile with a checkpointer (durability)
app = builder.compile(checkpointer=MemorySaver())

# 5) Use a stable thread_id across turns
config = {"configurable": {"thread_id": "thread-1"}}

# Turn 1
out1 = app.invoke({"messages": [{"role": "user", "content": "hi"}]}, config)
# Turn 2 (same thread_id => state resumes)
out2 = app.invoke({"messages": [{"role": "user", "content": "again"}]}, config)

print([m["content"] for m in out2["messages"]])
```

**What to point out while tutoring**
- The reducer `add_messages` defines *how* to merge message updates (append/ID-merge), but persistence + `thread_id` defines *whether the previous messages exist at all* across invocations (Issue #1568; persistence docs).
- With checkpointing, each invoke resumes from the latest checkpoint in that thread (persistence docs: https://docs.langchain.com/oss/python/langgraph/persistence).

### Example 2 (Conceptual): Tool loop as a cycle with conditional edges
From Discussion #3346, the canonical loop is:
- `chatbot` node produces an AI message.
- Router checks if last AI message has `tool_calls`.
- If yes: go to `tools`; else: `END`.
- After `tools`, edge back to `chatbot`.

This is the “graphs as agent control flow” core: the loop is explicit in edges, not hidden in a `while` loop (Discussion #3346: https://github.com/langchain-ai/langgraph/discussions/3346).

---

## Comparisons & Trade-offs

| Approach | Control flow representation | Branching/loops | Durability / resume | Debuggability | When it’s a good fit | Sources |
|---|---|---:|---:|---:|---|---|
| “One big while-loop” agent | Implicit in code | Yes, but ad hoc | Hard to checkpoint arbitrary stack | Harder to inspect step boundaries | Quick prototypes; single-process experiments | LangGraph discussion argues structured nodes enable checkpointing/HITL (https://github.com/langchain-ai/langgraph/discussions/2290) |
| LangGraph StateGraph | Explicit nodes + edges over shared state | Native (conditional edges, cycles) | Built-in checkpointers; threads/checkpoints | Step-level state snapshots; replay/time travel | Production workflows needing HITL, fault tolerance, long-running runs | Graph API overview (https://docs.langchain.com/oss/python/langgraph/graph-api), persistence docs (https://docs.langchain.com/oss/python/langgraph/persistence) |
| Temporal HITL workflow (comparison) | Workflow code + durable event history | Yes | Strong durability via workflow history; waits/signals | Deterministic replay model | When you want a general workflow engine with durable waits/signals | Temporal tutorial (https://learn.temporal.io/tutorials/ai/building-durable-ai-applications/human-in-the-loop/) |

**Trade-off note (from sources)**: LangGraph persistence enables replay/resume, but replay can re-trigger LLM/tool calls after the checkpoint; production designs should isolate side-effectful operations and design for determinism/idempotency (Aerospike blog: https://aerospike.com/blog/langgraph-production-latency-replay-scale; JS/Python persistence references on replay semantics).

---

## Prerequisite Connections

- **State + immutability/merging mindset**: Students need to be comfortable with “functions return updates that get merged,” not “mutate global variables,” because LangGraph nodes return partial updates merged via reducers (Graph API overview; reducers docs).
- **Basic graph concepts (nodes/edges, cycles)**: Understanding branching and loops as edges helps students see why LangGraph is more than a linear chain (AWS DynamoDB blog; Discussion #3346).
- **Concurrency intuition**: Super-steps can run nodes in parallel; reducers are required for deterministic merges (Graph API overview; Discussion #3914).
- **Persistence basics (IDs, snapshots)**: `thread_id` and checkpoints are key-value persistence concepts; without them, HITL and memory across turns won’t work (persistence docs; checkpoints reference).

---

## Socratic Question Bank

1) **If two nodes run in the same super-step and both write `messages`, what determines whether you see both updates?**  
   *Good answer*: reducers; without a reducer it overwrites; with `add_messages` it merges/append-by-ID (Discussion #3914; `add_messages` code).

2) **Why does LangGraph talk about “super-steps” instead of just “calling nodes one after another”?**  
   *Good answer*: nodes can run in parallel in a step; updates apply at step boundary; checkpoints align to these boundaries (Graph API overview; persistence references).

3) **What’s the difference between “state accumulates within a run” and “state persists across runs”?**  
   *Good answer*: reducers handle within-run merging; checkpointer + `thread_id` enables cross-invocation continuity (Issue #1568; persistence docs).

4) **If you replay from an earlier checkpoint, what kinds of operations might happen again?**  
   *Good answer*: LLM calls/tool calls/interrupts after that checkpoint are re-triggered (JS persistence reference; Python checkpoints reference).

5) **What does `interrupt()` actually do at runtime, and what must be true for resume to work?**  
   *Good answer*: raises `GraphInterrupt`, requires checkpointing; resume via `Command(resume=...)` and node re-executes (Python types reference).

6) **In a tool-using agent loop, where is the “loop” represented in LangGraph?**  
   *Good answer*: as an explicit cycle in edges (e.g., `tools -> chatbot`) plus conditional routing (Discussion #3346).

7) **What is `thread_id` conceptually: a user ID, a conversation ID, or something else?**  
   *Good answer*: it’s the primary key for a sequence of checkpoints (a thread of execution/state), often aligned with a conversation/session but technically an execution thread (persistence docs; AWS blog).

8) **Why might someone enable `workflow_mode=True` for conditional edges?**  
   *Good answer*: to enforce workflow-like “execute once” semantics in dynamic branching/convergence cases (PR #3345).

---

## Likely Student Questions

**Q: Why does LangGraph use a graph instead of a chain?**  
→ **A:** Because nodes + edges make control flow explicit and naturally support branching, merging, and loops (including cyclic graphs), enabling complex stateful workflows beyond linear chains (Graph API overview: https://docs.langchain.com/oss/python/langgraph/graph-api; AWS blog: https://aws.amazon.com/blogs/database/build-durable-ai-agents-with-langgraph-and-amazon-dynamodb/).

**Q: What exactly is a “super-step,” and why does it matter?**  
→ **A:** A super-step is a discrete “tick” where all scheduled nodes execute (potentially in parallel) and then updates are applied; checkpoints are created at super-step boundaries, and you can only resume/replay from those boundaries (Graph API overview; JS persistence reference: https://docs.langchain.com/oss/javascript/langgraph/persistence).

**Q: Why do I have to pass `thread_id`?**  
→ **A:** With a checkpointer, `thread_id` is the primary key used to store and retrieve checkpoints; without it, the checkpointer can’t persist state or resume after an interrupt (persistence docs: https://docs.langchain.com/oss/python/langgraph/persistence; Python checkpoints reference: https://reference.langchain.com/python/langgraph/checkpoints/).

**Q: I used `add_messages` but my messages still don’t accumulate across turns—why?**  
→ **A:** If you don’t compile with a checkpointer and reuse the same `thread_id`, each invocation starts fresh, so you’ll only see the current turn’s messages. This is the resolution in issue #1568: compile with `MemorySaver()` (or another saver) and pass `{"configurable": {"thread_id": "1"}}` on each call (Issue #1568: https://github.com/langchain-ai/langgraph/issues/1568).

**Q: What’s inside a checkpoint / StateSnapshot?**  
→ **A:** A checkpoint stores state values plus execution metadata: `values` (channel values), `next` (next nodes), `config` (includes `thread_id`, `checkpoint_id`), `metadata` (e.g., source/step/writes), timestamps, and task info (AWS blog; JS persistence reference; Python checkpoints reference).

**Q: If I replay from a checkpoint, will it call tools/LLMs again?**  
→ **A:** Yes—replay re-executes after that checkpoint, so LLM calls, API requests, and interrupts after that point are re-triggered (JS persistence reference: https://docs.langchain.com/oss/javascript/langgraph/persistence; Python checkpoints reference).

**Q: How does DynamoDBSaver store large checkpoints?**  
→ **A:** It stores checkpoints < 350 KB directly in DynamoDB; for ≥ 350 KB it stores state in S3 and keeps an S3 pointer in DynamoDB (AWS blog: https://aws.amazon.com/blogs/database/build-durable-ai-agents-with-langgraph-and-amazon-dynamodb/).

**Q: What are LangGraph’s default retry settings?**  
→ **A:** The runtime `RetryPolicy` defaults (v0.2.24) are `initial_interval=0.5s`, `backoff_factor=2.0`, `max_interval=128.0s`, `max_attempts=3`, `jitter=True` (Python types reference: https://reference.langchain.com/python/langgraph/types/).

---

## Available Resources

### Videos
- [Intro to Large Language Models](https://youtube.com/watch?v=zjkBMFhNj_g) — Surface when: student needs broader agent foundations (tool use, memory, loops) before “why graphs?”.
- [Multi-Agent Systems with LangGraph](https://youtube.com/watch?v=Mi5wOpAgixw) — Surface when: student asks how LangGraph structures multi-agent collaboration or supervisor patterns.

### Articles & Tutorials
- [Lilian Weng — LLM Powered Autonomous Agents](https://lilianweng.github.io/posts/2023-06-23-agent/) — Surface when: student asks how agent loops (plan/act/reflect/memory) relate to orchestration frameworks.
- [LangGraph: Multi-Agent Workflows (LangChain blog)](https://blog.langchain.dev/langgraph-multi-agent-workflows) — Surface when: student wants patterns/examples beyond a single tool loop.
- [ReAct paper](https://arxiv.org/abs/2210.03629) — Surface when: student asks how the classic reason→act→observe loop maps onto nodes/edges.
- [OpenAI Agents SDK (Python)](https://openai.github.io/openai-agents-python/) — Surface when: student asks how LangGraph compares to other agent SDKs (conceptual comparison; not a LangGraph source).
- [LangGraph conceptual docs: agentic concepts](https://langchain-ai.github.io/langgraph/concepts/agentic_concepts/) — Surface when: student asks for canonical LangGraph agent patterns and terminology.

---

## Visual Aids

![LangGraph in-memory checkpointing with InMemorySaver (AWS Database Blog).](/api/wiki-images/agent-workflows/images/aws-amazon-blogs-database-build-durable-ai-agents-with-langgraph-and-amazon-dyna_001.png)  
**Show when:** student asks “why is my state lost on restart?” or “what does checkpointing look like conceptually?”

![Durable LangGraph checkpoints using DynamoDBSaver and Amazon DynamoDB (AWS Database Blog).](/api/wiki-images/agent-workflows/images/aws-amazon-blogs-database-build-durable-ai-agents-with-langgraph-and-amazon-dyna_002.png)  
**Show when:** student asks “how do I make this production-durable?” or “how does DynamoDB/S3 storage work for checkpoints?”

![CrewAI Flows: orchestration backbone for multi-agent tasks (CrewAI Docs).](/api/wiki-images/agent-workflows/images/docs-crewai-en-introduction_001.png)  
**Show when:** student is comparing orchestration frameworks (e.g., “is LangGraph like CrewAI Flows?”) and needs a control-flow mental model comparison.

---

## Key Sources

- [Graph API overview - Docs by LangChain](https://docs.langchain.com/oss/python/langgraph/graph-api) — Authoritative description of nodes/edges/state and Pregel-inspired super-step execution/halting.
- [Persistence - Docs by LangChain (LangGraph)](https://docs.langchain.com/oss/python/langgraph/persistence) — Canonical explanation of threads, checkpoints, and why persistence enables HITL/time travel/fault tolerance.
- [LangGraph Checkpointing (Python reference)](https://reference.langchain.com/python/langgraph/checkpoints/) — Precise checkpoint fields (`checkpoint_id`, metadata `source/step`, namespaces) and replay semantics.
- [AWS Database Blog: Build durable AI agents with LangGraph and DynamoDB](https://aws.amazon.com/blogs/database/build-durable-ai-agents-with-langgraph-and-amazon-dynamodb/) — Concrete production durability architecture; 350 KB DynamoDB/S3 threshold; checkpoint count example.
- [LangGraph types (Python reference)](https://reference.langchain.com/python/langgraph/types/) — Exact interrupt/resume semantics (`GraphInterrupt`, `Command(resume=...)`), stream modes, retry defaults, and reducer bypass (`Overwrite`).