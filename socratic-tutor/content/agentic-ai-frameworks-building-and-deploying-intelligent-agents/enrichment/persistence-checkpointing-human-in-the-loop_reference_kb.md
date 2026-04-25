## Core Definitions

**Checkpointing (LangGraph)**: When you compile a LangGraph with a checkpointer, the runtime saves a **checkpoint (a `StateSnapshot`) at every super-step boundary**, organized into **threads**; this enables resuming, replaying, human-in-the-loop, and fault tolerance. (LangGraph persistence docs: https://docs.langchain.com/oss/javascript/langgraph/persistence, https://docs.langchain.com/oss/python/langgraph/persistence; LangGraph v0.2 blog: https://blog.langchain.com/langgraph-v0-2/)

**State persistence**: Persisting graph execution state means storing the graph’s **serialized channel values**, **channel versions**, and **which versions each node has seen**, so execution can be restored later (even on another machine) and continue from a safe boundary. (LangGraph discussion #2290: https://github.com/langchain-ai/langgraph/discussions/2290; Python checkpoints reference: https://reference.langchain.com/python/langgraph/checkpoints/)

**Durable execution**: “Durable execution is a technique in which a process or workflow saves its progress at key points, allowing it to pause and later resume exactly where it left off,” especially for long-running tasks and human-in-the-loop; in LangGraph, enabling a checkpointer + `thread_id` gives durable execution. (Durable execution docs: https://docs.langchain.com/oss/python/langgraph/durable-execution)

**Thread (LangGraph persistence)**: A **thread** is a unique identifier (`thread_id`) that groups a sequence of checkpoints and accumulated state across runs; the checkpointer uses `thread_id` as the **primary key** to store/retrieve checkpoints, and you must pass it in `configurable` to persist/resume. (Persistence docs: https://docs.langchain.com/oss/python/langgraph/persistence; Threads concept: https://langchain-ai.github.io/langgraph/cloud/concepts/threads/)

**Checkpoint (LangGraph)**: A **checkpoint** is the state of a thread at a particular point in time (a super-step boundary), represented as a `StateSnapshot` (for `get_state*`) and backed by stored channel values/versions/versions-seen (for the checkpointer). (JS persistence docs: https://docs.langchain.com/oss/javascript/langgraph/persistence; Python checkpoints reference: https://reference.langchain.com/python/langgraph/checkpoints/)

**Super-step**: A **super-step** is a single “tick” of the graph where all nodes scheduled for that step execute (potentially in parallel), and then their updates are applied deterministically; LangGraph creates a checkpoint at each super-step boundary. (JS persistence docs: https://docs.langchain.com/oss/javascript/langgraph/persistence; discussion #2290: https://github.com/langchain-ai/langgraph/discussions/2290)

**Human-in-the-loop (HITL) via interrupts**: Interrupts allow you to pause graph execution at specific points and wait for external input; calling `interrupt(value)` inside a node suspends execution, surfaces `value` to the caller, and later resuming with `Command(resume=...)` makes that resume value become the return value of `interrupt()` inside the node. Requires checkpointing. (Interrupts docs: https://docs.langchain.com/oss/python/langgraph/interrupts; types reference: https://reference.langchain.com/python/langgraph/types/)

**Workflow interruption**: In LangGraph, interruption is implemented by `interrupt()` raising a `GraphInterrupt` on first call, after which the graph is suspended with persisted state; resuming re-executes the node from the start and replays until it reaches the interrupt point. (Types reference: https://reference.langchain.com/python/langgraph/types/; HITL overview: https://docs.langchain.com/oss/python/langgraph/human-in-the-loop)

**Resumable agents**: An agent workflow is “resumable” when it can be restarted after a pause/failure and continue from the last checkpointed super-step using the same `thread_id` (and optionally a specific `checkpoint_id`). (Persistence docs: https://docs.langchain.com/oss/python/langgraph/persistence; Python checkpoints reference: https://reference.langchain.com/python/langgraph/checkpoints/)

**Approval workflows (graph-native)**: Approval workflows are HITL patterns where the graph pauses at an approval gate (often via `interrupt()` or configured interrupts before/after nodes), a human inspects/edits state, and execution resumes from the persisted checkpoint. (HITL docs: https://docs.langchain.com/oss/python/langgraph/interrupts; CompiledStateGraph JS reference: https://reference.langchain.com/javascript/classes/_langchain_langgraph.index.CompiledStateGraph.html)

---

## Key Formulas & Empirical Results

**Checkpoint write-rate sizing (production IOPS heuristic)**  
Formula (Aerospike blog):  
- **writes/sec = steps_per_request × requests/sec**  
Variables:  
- `steps_per_request`: number of super-steps per request (checkpoint per super-step)  
- `requests/sec`: throughput  
Claim supported: checkpoint storage load scales with **steps**, not wall-clock time.  
Example given: **12 steps/request** and **2,000 req/s ⇒ 24,000 writes/s**. (https://aerospike.com/blog/langgraph-production-latency-replay-scale)

**Sequential graph checkpoint count (concrete semantics)**  
Claim: For sequential `START -> A -> B -> END`, a single invoke yields **exactly 4 checkpoints**: (1) empty/START-next, (2) input saved/A-next, (3) after A/B-next, (4) after B/complete. (https://docs.langchain.com/oss/javascript/langgraph/persistence; also echoed in Python checkpoints reference: https://reference.langchain.com/python/langgraph/checkpoints/)

**RetryPolicy defaults (LangGraph Python types)**  
Defaults (v0.2.24 per types ref):  
- `initial_interval=0.5s`, `backoff_factor=2.0`, `max_interval=128.0s`, `max_attempts=3`, `jitter=True`. (https://reference.langchain.com/python/langgraph/types/)

**Streaming defaults (LangGraph.js compiled graph)**  
- `streamMode` defaults to `["values"]`. (https://reference.langchain.com/javascript/classes/_langchain_langgraph.index.CompiledStateGraph.html)

**DynamoDBSaver storage threshold (AWS checkpointing)**  
- Checkpoints **< 350 KB** stored directly in DynamoDB; **≥ 350 KB** stored in S3 with DynamoDB pointer. (https://aws.amazon.com/blogs/database/build-durable-ai-agents-with-langgraph-and-amazon-dynamodb/)

**Benchmark datapoints (MCP Server + LangGraph)**  
Methodology: GCP n2-standard-4, Gemini 2.0 Flash, k6 load, 5 min runs.  
Selected results:  
- Simple Agent (MCP+LangGraph Cloud Run): **142 req/s**, p50 **245ms**, p95 **890ms**, error **0.02%**.  
- Complex 5-node conditional graph (MCP+LangGraph): **32 req/s**, p50 **2800ms**, p95 **6500ms**, error **0.15%**, Redis checkpointing + retries. (https://mcp-server-langgraph.mintlify.app/comparisons/benchmarks)

---

## How It Works

### A. LangGraph execution model (super-steps + deterministic update application)
Mechanics (discussion #2290; #938):
1. **Channels/state** hold named values; each channel has a **version** that monotonically increases when updated. (https://github.com/langchain-ai/langgraph/discussions/2290)
2. Nodes subscribe to channels; a node becomes runnable when subscribed channel versions change relative to what it last saw. (https://github.com/langchain-ai/langgraph/discussions/2290)
3. Each iteration (“super-step”):
   1) Select runnable nodes by comparing channel versions vs node’s `versions_seen`.  
   2) Execute selected nodes (potentially in parallel) with **isolated copies** of state.  
   3) Nodes emit **partial updates** (dict of key→value).  
   4) Apply updates to channels in a **deterministic order**, bumping channel versions. (https://github.com/langchain-ai/langgraph/discussions/2290)
4. Halt when all nodes are inactive and no messages are in transit. (https://github.com/langchain-ai/langgraph/discussions/938)

### B. Reducers: how node updates merge into state
Reducer rule (discussions #4730, #938, #3459, #3810):
- Each state key/channel has an independent reducer:
  - If **no reducer**: update **overwrites** prior value. (https://github.com/langchain-ai/langgraph/discussions/4730)
  - If reducer exists: `new_value = reducer(old_value, update_value)`. (https://github.com/langchain-ai/langgraph/discussions/3459)
- Common example: `messages` with `add_messages` appends rather than overwrites. (https://github.com/langchain-ai/langgraph/discussions/4730; issue #1568 context: https://github.com/langchain-ai/langgraph/issues/1568)
- Important nuance: append reducers can duplicate content under replay/retry unless updates are idempotent or replacement reducers are used. (https://github.com/langchain-ai/langgraph/discussions/3810)

### C. Persistence: what gets checkpointed and when
Checkpoint semantics (JS persistence docs; Python checkpoints ref; discussion #2290):
1. Compile with a checkpointer (e.g., `MemorySaver`, `SqliteSaver`, Postgres, Redis, etc.). (https://docs.langchain.com/oss/javascript/langgraph/persistence; https://blog.langchain.com/langgraph-v0-2/)
2. Invoke/stream with config containing **`configurable.thread_id`**; without it, the checkpointer cannot key storage and cannot resume. (https://docs.langchain.com/oss/python/langgraph/persistence)
3. At each **super-step boundary**, the runtime writes a checkpoint containing:
   - serialized channel values,
   - channel versions,
   - versions seen per node (so it knows what’s runnable next). (https://github.com/langchain-ai/langgraph/discussions/2290; https://reference.langchain.com/python/langgraph/checkpoints/)
4. `graph.getState(config)` returns a `StateSnapshot` (values + `next` nodes + config/metadata/tasks); `getStateHistory` iterates snapshots (requires checkpointer). (JS compiled graph ref: https://reference.langchain.com/javascript/classes/_langchain_langgraph.index.CompiledStateGraph.html)

### D. Resume, replay, and “time travel”
Replay rule (JS persistence docs; Python checkpoints ref):
1. To resume a thread, invoke again with the same `thread_id`; the runtime loads latest checkpoint and continues. (https://docs.langchain.com/oss/python/langgraph/persistence)
2. To replay from a specific point, pass `checkpoint_id` in config; execution re-runs **after** that checkpoint; steps before are skipped. (https://reference.langchain.com/python/langgraph/checkpoints/)
3. During replay, LLM calls/tool calls/interrupts **after** the checkpoint are re-triggered. (https://docs.langchain.com/oss/javascript/langgraph/persistence)

### E. Fault tolerance: pending writes
Pending writes semantics (JS persistence docs; BaseCheckpointSaver.list ref):
- If a node fails mid-super-step, LangGraph stores **pending checkpoint writes** from nodes that already succeeded in that super-step; on resume from that super-step, successful nodes are not re-run. (https://docs.langchain.com/oss/javascript/langgraph/persistence; https://reference.langchain.com/javascript/langchain-langgraph-checkpoint/BaseCheckpointSaver/list)

### F. Human-in-the-loop via `interrupt()` (dynamic pause/resume)
Mechanics (types ref; HITL docs; discussion #938):
1. Inside a node, call `approved = interrupt(payload)` where payload is JSON-serializable. (https://docs.langchain.com/oss/python/langgraph/interrupts)
2. On first call, `interrupt()` **raises `GraphInterrupt`**, suspending execution and surfacing the payload to the client. (https://reference.langchain.com/python/langgraph/types/)
3. The graph is checkpointed; it can wait indefinitely. (https://docs.langchain.com/oss/python/langgraph/interrupts)
4. Resume by invoking with `Command(resume=...)`; the node is **re-executed from the start**, and the resume value becomes the return value of `interrupt()`. (https://reference.langchain.com/python/langgraph/types/)
5. Multiple `interrupt()` calls in one node: resume values are matched by **call order**, scoped per task. (https://reference.langchain.com/python/langgraph/types/)

### G. Static interrupts (breakpoints) around nodes
Compiled graph interrupt controls (JS compiled graph ref; Python compile ref):
- Configure `interrupt_before` / `interrupt_after` at compile time:
  - `"*"` or `"__start__"` or list of node names. (JS: https://reference.langchain.com/javascript/classes/_langchain_langgraph.index.CompiledStateGraph.html; Python compile: https://reference.langchain.com/python/langgraph/graph/state/StateGraph/compile)

---

## Teaching Approaches

### Intuitive (no math)
- “A checkpointer turns your graph into a save-game system: after every ‘tick’ it saves the whole game state. A `thread_id` is the save slot. Interrupts are like pausing the game and asking a human to choose what happens next.”

### Technical (with runtime mechanics)
- “LangGraph runs in super-steps: it schedules runnable nodes based on channel version changes, executes them in parallel, then applies updates deterministically. With a checkpointer, it persists channel values/versions and versions-seen at each super-step boundary. Resume loads that snapshot and continues; replay from `checkpoint_id` re-executes subsequent steps.”

### Analogy-based
- **Database transaction log analogy**: “Each super-step is like a committed transaction boundary. Checkpoints are commits; replay is restoring from a commit and re-running later transactions. Pending writes are like partial commits from successful participants in a distributed step.”

---

## Common Misconceptions

1. **“I annotated `messages` with `add_messages`, so my chat history should persist across separate user inputs automatically.”**  
   Why wrong: Reducers only define **how updates merge within a run**; without a checkpointer + `thread_id`, each new `invoke/stream` starts from an empty state, so you only see the current input. (Issue #1568 fix: add checkpointer + thread config: https://github.com/langchain-ai/langgraph/issues/1568)  
   Correct model: **Persistence is opt-in**: compile with a checkpointer and pass `configurable.thread_id` to accumulate state across calls. (https://docs.langchain.com/oss/python/langgraph/persistence)

2. **“`interrupt()` resumes from the exact line after the interrupt, like a normal program pause.”**  
   Why wrong: On resume, LangGraph **re-executes the node from the start**; the resume value is injected as the return value of `interrupt()`. (https://reference.langchain.com/python/langgraph/types/)  
   Correct model: Interrupts are implemented via checkpoint + replay; design nodes so re-execution is safe/idempotent.

3. **“Checkpointing saves after every node function call, so I can resume from any line inside a node.”**  
   Why wrong: Checkpoints are created at **super-step boundaries**, not arbitrary lines; you can only resume from a checkpoint boundary. (https://docs.langchain.com/oss/javascript/langgraph/persistence)  
   Correct model: If you need finer-grained durability, split work into more nodes/tasks so boundaries occur where you need them.

4. **“Replay won’t re-trigger tool calls/LLM calls because the checkpoint has the final state.”**  
   Why wrong: Replay from a `checkpoint_id` re-executes steps **after** that checkpoint; LLM/tool calls/interrupts after that point are re-triggered. (https://docs.langchain.com/oss/javascript/langgraph/persistence; https://reference.langchain.com/python/langgraph/checkpoints/)  
   Correct model: Treat post-checkpoint side effects as potentially repeated unless protected by durable task semantics/idempotency guidance. (Durable execution docs: https://docs.langchain.com/oss/python/langgraph/durable-execution)

5. **“If a super-step has multiple nodes and one fails, I must re-run all nodes in that step.”**  
   Why wrong: LangGraph stores **pending writes** from nodes that succeeded in the super-step; resuming from that super-step avoids re-running successful nodes. (https://docs.langchain.com/oss/javascript/langgraph/persistence; BaseCheckpointSaver.list ref: https://reference.langchain.com/javascript/langchain-langgraph-checkpoint/BaseCheckpointSaver/list)  
   Correct model: The runtime can recover mid-step using pending writes to preserve completed work.

---

## Worked Examples

### Example 1 (Python): Conversation memory across turns requires checkpointer + `thread_id`
This is the exact failure mode from issue #1568: messages appear overwritten because each loop iteration is a fresh run.

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
    # Printing state shows accumulated messages only if persistence is enabled + same thread_id
    print("STATE IN NODE:", state)
    return {"messages": [model.invoke(state["messages"])]}

builder = StateGraph(State)
builder.add_node("chatbot", chatbot)
builder.add_edge(START, "chatbot")
builder.add_edge("chatbot", END)

# Key fix: compile with checkpointer
graph = builder.compile(checkpointer=MemorySaver())

# Key fix: pass thread_id each turn
thread_config = {"configurable": {"thread_id": "1"}}

while True:
    user_input = input("User: ")
    if user_input.lower() in ["quit", "exit", "q"]:
        break

    for event in graph.stream({"messages": ("user", user_input)}, thread_config):
        for value in event.values():
            print("Assistant:", value["messages"][-1].content)
```

Tutor notes (what to point out live):
- `add_messages` controls merge behavior, but **does not persist across separate invocations** without checkpointing. (https://github.com/langchain-ai/langgraph/issues/1568)
- `thread_id` is the “persistent cursor”; reuse it to continue the same conversation. (https://docs.langchain.com/oss/python/langgraph/persistence)

### Example 2 (Python): Approval gate with `interrupt()` + resume
Minimal approval node pattern from docs/types:

```python
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.types import interrupt, Command
from langgraph.checkpoint.memory import MemorySaver

class State(TypedDict):
    approved: bool

def approval_node(state: State):
    approved = interrupt("Do you approve this action?")
    return {"approved": approved}

builder = StateGraph(State)
builder.add_node("approval", approval_node)
builder.add_edge(START, "approval")
builder.add_edge("approval", END)

app = builder.compile(checkpointer=MemorySaver())
config = {"configurable": {"thread_id": "approval-thread"}}

# 1) First invoke interrupts
try:
    app.invoke({}, config)
except Exception as e:
    # In real usage you'd read the interrupt payload from streaming / client response
    pass

# 2) Resume with a decision; node re-executes and interrupt() returns True
result = app.invoke(Command(resume=True), config)
print(result)  # {"approved": True}
```

Tutor notes:
- Requires checkpointing; `interrupt()` relies on persisted state. (https://reference.langchain.com/python/langgraph/types/)
- Resume re-executes node from start; keep side effects out of the node body or make them idempotent. (https://docs.langchain.com/oss/python/langgraph/durable-execution)

### Example 3 (JS): Inspect and update state for HITL (compiled graph surface)
Key runtime affordances (JS compiled graph reference):
- `getState()` / `getStateHistory()` require a checkpointer.
- `updateState()` creates a new checkpoint and is used for HITL edits/breakpoints. (https://reference.langchain.com/javascript/classes/_langchain_langgraph.index.CompiledStateGraph.html)

Pseudo-usage sketch (API surface emphasis, not full app):
```ts
// compiled graph: app
await app.invoke(input, { configurable: { thread_id: "t1" } });

const snapshot = await app.getState({ configurable: { thread_id: "t1" } });
// snapshot.values, snapshot.next, snapshot.metadata...

await app.updateState(
  { configurable: { thread_id: "t1" } },
  { someKey: "human-edited-value" }
);

await app.invoke(nextInput, { configurable: { thread_id: "t1" } });
```

---

## Comparisons & Trade-offs

| Choice | What you get | What you risk / pay | When to choose | Sources |
|---|---|---|---|---|
| **No checkpointer** | Simple local execution | No resume, no HITL, no `getState*`, no durable recovery | Toy demos, single-shot runs | Compiled graph requires checkpointer for state/history/update: https://reference.langchain.com/javascript/classes/_langchain_langgraph.index.CompiledStateGraph.html |
| **MemorySaver (in-memory)** | Fast, easy | State lost on process restart; not shared across machines | Local dev, tests | v0.2 blog mentions MemorySaver: https://blog.langchain.com/langgraph-v0-2/ |
| **DB-backed checkpointer (SQLite/Postgres/Redis/Mongo/DynamoDB)** | Durable across restarts; multi-worker capable | Operational overhead; storage/IOPS sizing | Production, long-running HITL | Persistence docs list options: https://docs.langchain.com/oss/javascript/langgraph/persistence; DynamoDBSaver details: https://aws.amazon.com/blogs/database/build-durable-ai-agents-with-langgraph-and-amazon-dynamodb/ |
| **LangGraph interrupts (`interrupt()`)** | Dynamic pause anywhere in node code | Node re-executes on resume; must design for replay safety | Conditional approvals, interactive review | Interrupts docs: https://docs.langchain.com/oss/python/langgraph/interrupts; types: https://reference.langchain.com/python/langgraph/types/ |
| **Static breakpoints (`interrupt_before/after`)** | Pause around nodes without editing node code | Less flexible than `interrupt()` | Debugging, consistent approval gates at node boundaries | JS compiled graph ref; Python compile ref: https://reference.langchain.com/javascript/classes/_langchain_langgraph.index.CompiledStateGraph.html, https://reference.langchain.com/python/langgraph/graph/state/StateGraph/compile |
| **Temporal Signals + wait_condition (comparison pattern)** | Durable waits without compute; signals/queries; deterministic replay | Requires Temporal infra + determinism constraints | Very long waits (days/weeks), enterprise workflow orchestration | Temporal tutorial: https://learn.temporal.io/tutorials/ai/building-durable-ai-applications-human-in-the-loop/; blog: https://danielfridljand.de/post/temporal-human-in-the-loop |

---

## Prerequisite Connections

- **Reducers / state merging**: Understanding overwrite vs append reducers is necessary to reason about what “state persistence” actually stores and why replay can duplicate messages. (Reducers discussions: https://github.com/langchain-ai/langgraph/discussions/4730, https://github.com/langchain-ai/langgraph/discussions/3810)
- **Graph execution (nodes/edges/super-steps)**: Super-step boundaries define checkpoint boundaries; without this, “resume from checkpoint” feels arbitrary. (https://github.com/langchain-ai/langgraph/discussions/2290; https://docs.langchain.com/oss/javascript/langgraph/persistence)
- **Idempotency & side effects**: Durable execution implies replay; students need the idea that side effects must be isolated or made safe. (https://docs.langchain.com/oss/python/langgraph/durable-execution; Aerospike blog replay/idempotency framing: https://aerospike.com/blog/langgraph-production-latency-replay-scale)
- **Config scoping (`thread_id`, `checkpoint_id`)**: Threading is the key to “memory between turns” and HITL resumption. (https://docs.langchain.com/oss/python/langgraph/persistence; https://reference.langchain.com/python/langgraph/checkpoints/)

---

## Socratic Question Bank

1. **If you run the same graph twice with the same input but without a checkpointer, what state do you expect on the second run—and why?**  
   Good answer: It restarts from empty; reducers don’t persist across invocations without checkpointing/threading.

2. **Where are the “safe resume points” in LangGraph: after each node line, after each node, or after each super-step? What’s the practical implication?**  
   Good answer: Super-step boundaries; split work into nodes/tasks to create boundaries where needed.

3. **Suppose a node appends to `messages` and the run is replayed. What duplication risk exists, and what are two ways to mitigate it?**  
   Good answer: Append reducer duplicates; mitigate via idempotent updates/replacement reducer or isolating side effects.

4. **What does `thread_id` represent operationally: a user, a session, a run, or a storage key? Can it be reused?**  
   Good answer: Storage key grouping checkpoints; reuse resumes same thread; new value starts new thread.

5. **When an interrupt resumes, does execution continue from the next line, or does the node re-run? How does that affect where you put API calls?**  
   Good answer: Node re-runs; keep side effects in tasks/nodes designed for replay safety.

6. **If two nodes run in parallel in a super-step and one fails, what work can be preserved and how?**  
   Good answer: Pending writes from successful nodes are stored; resume avoids re-running them.

7. **If you “time travel” to an earlier checkpoint and re-run, which operations are guaranteed not to re-run, and which might re-run?**  
   Good answer: Steps before checkpoint won’t re-run; after checkpoint tool/LLM/interrupts re-trigger.

8. **What information must a checkpoint store to know what nodes are runnable next?**  
   Good answer: Channel versions and versions-seen per node (plus channel values).

---

## Likely Student Questions

**Q: Why are my messages not appending even though I used `add_messages`?**  
→ **A:** Without a checkpointer, each `invoke/stream` starts a fresh run, so you only see the current input; compile with a checkpointer (e.g., `MemorySaver`) and pass `{"configurable": {"thread_id": "1"}}` each turn to persist/accumulate state. (Issue #1568: https://github.com/langchain-ai/langgraph/issues/1568; persistence requirement: https://docs.langchain.com/oss/python/langgraph/persistence)

**Q: What exactly is stored in a checkpoint?**  
→ **A:** The checkpointer stores serialized **channel values**, **channel version strings**, and **which versions each node has seen**; `get_state()` surfaces a `StateSnapshot` with `values`, `next`, `config` (incl. `thread_id`, `checkpoint_id`, `checkpoint_ns`), `metadata`, and `tasks`. (Discussion #2290: https://github.com/langchain-ai/langgraph/discussions/2290; Python checkpoints ref: https://reference.langchain.com/python/langgraph/checkpoints/; JS persistence docs: https://docs.langchain.com/oss/javascript/langgraph/persistence)

**Q: When does LangGraph create checkpoints?**  
→ **A:** At every **super-step boundary** (a tick where all scheduled nodes execute, potentially in parallel). For `START -> A -> B -> END`, one invoke yields **4 checkpoints** (empty/start-next, input/A-next, after A/B-next, after B/complete). (https://docs.langchain.com/oss/javascript/langgraph/persistence; https://reference.langchain.com/python/langgraph/checkpoints/)

**Q: How do I resume from a specific point in history?**  
→ **A:** Invoke with the same `thread_id` and include `checkpoint_id` in `configurable` to replay from that checkpoint; execution re-runs **after** that checkpoint and may re-trigger LLM/tool calls after it. (Python checkpoints ref: https://reference.langchain.com/python/langgraph/checkpoints/; JS persistence docs replay note: https://docs.langchain.com/oss/javascript/langgraph/persistence)

**Q: Does `interrupt()` require checkpointing?**  
→ **A:** Yes—`interrupt()` relies on persisted state; on first call it raises `GraphInterrupt` and suspends execution, and you resume by invoking with `Command(resume=...)`. (Types ref: https://reference.langchain.com/python/langgraph/types/; interrupts docs: https://docs.langchain.com/oss/python/langgraph/interrupts)

**Q: If I resume after an interrupt, will the node run again?**  
→ **A:** Yes—the node is **re-executed from the start**; the resume value becomes the return value of `interrupt()`. (https://reference.langchain.com/python/langgraph/types/)

**Q: How can I list all checkpoints for a thread (for debugging/time travel UI)?**  
→ **A:** Use `BaseCheckpointSaver.list/alist` scoped by `configurable.thread_id`, optionally filter by metadata and paginate with `before` and `limit`; it returns `CheckpointTuple` items. (https://reference.langchain.com/javascript/langchain-langgraph-checkpoint/BaseCheckpointSaver/list)

**Q: What happens if one node fails in a parallel super-step—do I lose the whole step?**  
→ **A:** LangGraph stores **pending writes** from nodes that completed successfully in that super-step; resuming from that super-step avoids re-running successful nodes. (JS persistence docs: https://docs.langchain.com/oss/javascript/langgraph/persistence; BaseCheckpointSaver.list rationale: https://reference.langchain.com/javascript/langchain-langgraph-checkpoint/BaseCheckpointSaver/list)

---

## Available Resources

### Videos
- [Intro to Large Language Models](https://youtube.com/watch?v=zjkBMFhNj_g) — Surface when: student needs broader context for “agents need memory + tools + control flow,” before diving into checkpointing/HITL.
- [Multi-Agent Systems with LangGraph](https://youtube.com/watch?v=Mi5wOpAgixw) — Surface when: student asks how persistence/interrupts scale to multi-agent graphs and long-running workflows.

### Articles & Tutorials
- [Lilian Weng — LLM Powered Autonomous Agents](https://lilianweng.github.io/posts/2023-06-23-agent/) — Surface when: student asks why agents need orchestration primitives like memory and human escalation.
- [LangGraph agentic concepts](https://langchain-ai.github.io/langgraph/concepts/agentic_concepts/) — Surface when: student asks for broader orchestration patterns beyond a single approval gate.
- [ReAct (Yao et al., 2022)](https://arxiv.org/abs/2210.03629) — Surface when: student asks how tool-using loops relate to graph nodes/edges.
- [OpenAI Agents SDK (Python)](https://openai.github.io/openai-agents-python/) — Surface when: student asks for alternative HITL patterns/examples outside LangGraph.
- [LangChain — LangGraph multi-agent workflows](https://blog.langchain.dev/langgraph-multi-agent-workflows) — Surface when: student wants practical orchestration patterns that benefit from checkpointing.

---

## Visual Aids

![Checkpointing saves state snapshots for resuming runs (LangChain LangGraph docs).](/api/wiki-images/agent-workflows/images/docs-langchain-oss-python-langgraph-persistence_001.jpg)  
Show when: student asks “what is a checkpoint / how does resume work conceptually?”

![Update persisted state to continue or branch a run (LangChain LangGraph docs).](/api/wiki-images/agent-workflows/images/docs-langchain-oss-python-langgraph-persistence_004.jpg)  
Show when: student asks “how do humans intervene/edit state and then continue?”

![LangGraph in-memory checkpointing with InMemorySaver (AWS Database Blog).](/api/wiki-images/agent-workflows/images/aws-amazon-blogs-database-build-durable-ai-agents-with-langgraph-and-amazon-dyna_001.png)  
Show when: student asks why in-memory persistence fails in production (restarts, multi-worker) and why DB-backed savers matter.

---

## Key Sources

- [Memory store (Persistence) — LangGraph Docs](https://docs.langchain.com/oss/python/langgraph/persistence) — Canonical definitions: threads, checkpoints, why persistence is required for HITL/memory/time travel/fault tolerance.
- [Interrupts — LangGraph Docs](https://docs.langchain.com/oss/python/langgraph/interrupts) — Canonical HITL mechanism and resume contract.
- [LangGraph Checkpointing — Python Reference](https://reference.langchain.com/python/langgraph/checkpoints/) — Precise checkpoint fields (`channel_versions`, `versions_seen`, metadata conventions, namespaces).
- [LangGraph discussion #2290](https://github.com/langchain-ai/langgraph/discussions/2290) — Deep mechanical explanation: Pregel/BSP execution, deterministic update application, what must be stored to resume anywhere.
- [LangGraph v0.2 blog (checkpointers)](https://blog.langchain.com/langgraph-v0-2/) — Maintainer rationale and ecosystem of standardized checkpointer implementations.