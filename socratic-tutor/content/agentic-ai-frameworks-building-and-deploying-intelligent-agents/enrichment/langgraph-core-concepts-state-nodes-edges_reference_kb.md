## Core Definitions

**StateGraph**: “A graph whose nodes communicate by reading and writing to a shared state.” Each node has signature **`State -> Partial<State>`**, and each state key can optionally be annotated with a reducer **`(Value, Value) -> Value`** to aggregate updates from multiple nodes. `StateGraph` is a **builder** and “cannot be used directly for execution”; you must call **`.compile()`** to get an executable graph. (LangChain reference: StateGraph docs: https://reference.langchain.com/python/langgraph/graph/state/StateGraph)

**State (graph state / shared state)**: A shared data structure representing the “current snapshot” of the application, typically defined via a schema (e.g., `TypedDict`, Pydantic model, or dataclass). Nodes read from this snapshot and return partial updates that are merged into it. (Graph API overview: https://docs.langchain.com/oss/python/langgraph/graph-api ; “Use Graph API” guide: https://docs.langchain.com/oss/python/langgraph/use-graph-api)

**Typed state schema**: A Python type (commonly `TypedDict`) that defines the keys (“channels”) in state and optionally attaches per-key reducer behavior via `typing_extensions.Annotated`. This schema also typically defines the graph’s input/output schema unless separate input/output schemas are provided. (Use Graph API: https://docs.langchain.com/oss/python/langgraph/use-graph-api ; StateGraph reference: https://reference.langchain.com/python/langgraph/graph/state/StateGraph)

**Node function (StateGraph node)**: A function that “encodes the logic” of a step. Mechanically, it receives the current `state` (and optionally runtime/config context) and returns a **dict of updates** (a “partial state”) containing only the keys it wants to write. Core contract: **`node(state) -> dict`** merged into shared state. (StateGraph compile reference: https://reference.langchain.com/python/langgraph/graph/state/StateGraph/compile ; Graph API overview: https://docs.langchain.com/oss/python/langgraph/graph-api)

**Edge (directed edge)**: A directed control-flow connection that determines which node(s) execute next. Edges can be fixed transitions (`add_edge`) or conditional transitions (`add_conditional_edges`). If a node has multiple outgoing edges, all destinations can be scheduled to run (potentially in parallel) in the next super-step. (Graph API overview: https://docs.langchain.com/oss/python/langgraph/graph-api ; Discussion on execution model: https://github.com/langchain-ai/langgraph/discussions/938)

**Conditional edge (router / dynamic routing)**: A control-flow edge where, after a node runs, a **routing function** is evaluated and returns a label (e.g., `"tools"` or `END`) that is mapped to the next node via `add_conditional_edges(from_node, router, mapping)`. Mapping can be identity if omitted; the router output can be `END` to terminate. (Conditional semantics explainer: https://github.com/langchain-ai/langgraph/discussions/3346 ; Router tutorial example: https://datmt.com/python/lesson-3-1-the-router-conditional-edges/)

**Graph compilation (`StateGraph.compile`)**: The step that turns the builder specification (nodes/edges/state schema) into a runnable program. Compilation performs structural checks and is where runtime options like checkpointers and interrupts are configured. The result is a `CompiledStateGraph` that implements the Runnable interface (`invoke`, `stream`, async variants). (Compile reference: https://reference.langchain.com/python/langgraph/graph/state/StateGraph/compile ; Graph API overview: https://docs.langchain.com/oss/python/langgraph/graph-api)

**Message passing & super-steps (execution model)**: LangGraph’s underlying algorithm uses message passing inspired by Pregel; execution proceeds in discrete **super-steps**. Nodes become active when they receive a message (state) on an incoming edge/channel, run, emit updates/messages, and recipients run in the next super-step. Execution terminates when all nodes are inactive and no messages are in transit. (Graph API overview: https://docs.langchain.com/oss/python/langgraph/graph-api ; Discussion: https://github.com/langchain-ai/langgraph/discussions/938)

**State reducers (per-key reducers)**: Per-state-key functions that define how a node’s update is merged into the existing value for that key. Default behavior (no reducer) is overwrite/replace. Reducer signature: **`new_value = reducer(old_value, update_value)`** i.e., `(Value, Value) -> Value`. (Compile reference: https://reference.langchain.com/python/langgraph/graph/state/StateGraph/compile ; Reducers discussion: https://github.com/langchain-ai/langgraph/discussions/3459)

**`add_messages` reducer (messages state reducer)**: A specialized reducer for message lists that appends/merges messages using **message IDs** (replace-by-id), supports deletion via `RemoveMessage`, and can clear history via a sentinel `__remove_all__`. It also coerces various message-like inputs into LangChain `BaseMessage` objects and assigns UUIDs to missing IDs. (Implementation: https://github.com/langchain-ai/langgraph/blob/main/libs/langgraph/langgraph/graph/message.py ; Reducer rationale: https://github.com/langchain-ai/langgraph/discussions/3459)

**Checkpointing / persistence (checkpointer)**: When compiling with a checkpointer, LangGraph saves a snapshot of graph state at every super-step boundary, organized into **threads** keyed by `thread_id`. Persistence enables human-in-the-loop interrupts/resume, time travel debugging, and fault tolerance. (JS checkpointer reference: https://reference.langchain.com/javascript/langchain-langgraph/index/CompiledStateGraph/checkpointer ; AWS durability explainer: https://aws.amazon.com/blogs/database/build-durable-ai-agents-with-langgraph-and-amazon-dynamodb/)

**Interrupts (`interrupt`)**: A dynamic pause mechanism for HITL. `interrupt(value)` first raises `GraphInterrupt` and surfaces `value` to the client; later resuming with `Command(resume=...)` re-executes the node from the start, and the resume value becomes the return value of `interrupt()`. Requires checkpointing enabled. Multiple interrupts in one node match resume values by call order, scoped per task. (Types reference: https://reference.langchain.com/python/langgraph/types/ ; HITL docs: https://docs.langchain.com/oss/python/langgraph/human-in-the-loop)

**Overwrite (reducer bypass)**: `Overwrite(value=...)` bypasses a reducer (e.g., to reset accumulated state). Multiple `Overwrite` updates to the same channel in one super-step cause `InvalidUpdateError`. (Types reference: https://reference.langchain.com/python/langgraph/types/ ; Use Graph API mentions bypass: https://docs.langchain.com/oss/python/langgraph/use-graph-api)

**Dynamic fan-out (`Send`)**: `Send(node: str, arg: Any)` can be returned/used in conditional edges to invoke a node in the next step with custom per-send state (map-reduce style). (Types reference: https://reference.langchain.com/python/langgraph/types/ ; Use Graph API mentions Send: https://docs.langchain.com/oss/python/langgraph/use-graph-api)

---

## Key Formulas & Empirical Results

**Reducer merge rule (per key)**  
- **Claim supported**: how LangGraph merges node updates into state.  
- **Formula**: reducer signature **`(Value, Value) -> Value`** where left/current is the existing state value and right/update is the node’s returned update for that key. (Compile reference: https://reference.langchain.com/python/langgraph/graph/state/StateGraph/compile ; StateGraph reference: https://reference.langchain.com/python/langgraph/graph/state/StateGraph)

**`StateGraph.compile()` signature (Python)**  
- **Claim supported**: what compile configures and defaults.  
- **Signature** (verbatim from reference):
```python
compile(
  checkpointer: Checkpointer = None,
  *,
  cache: BaseCache | None = None,
  store: BaseStore | None = None,
  interrupt_before: All | list[str] | None = None,
  interrupt_after: All | list[str] | None = None,
  debug: bool = False,
  name: str | None = None,
) -> CompiledStateGraph[StateT, ContextT, InputT, OutputT]
```
Defaults: `checkpointer=None`, `cache=None`, `store=None`, `interrupt_before=None`, `interrupt_after=None`, `debug=False`, `name=None`. (Compile reference: https://reference.langchain.com/python/langgraph/graph/state/StateGraph/compile)

**Streaming modes (Python runtime types)**  
- **Claim supported**: what stream modes exist and what they emit.  
- `StreamMode = Literal["values","updates","checkpoints","tasks","debug","messages","custom"]` with semantics:
  - `"values"` full state after each step
  - `"updates"` node/task names + returned updates (each update separately if multiple in a step)
  - `"messages"` token-by-token LLM messages + metadata
  - `"checkpoints"` when checkpoint created (format like `get_state()`)
  - `"tasks"` task lifecycle
  - `"debug"` includes checkpoints + tasks
  - `"custom"` via `StreamWriter` (no-op unless `stream_mode="custom"`)  
(Types reference: https://reference.langchain.com/python/langgraph/types/)

**Retry defaults (`RetryPolicy`, v0.2.24)**  
- **Claim supported**: default retry behavior students often ask about.  
- Defaults: `initial_interval=0.5s`, `backoff_factor=2.0`, `max_interval=128.0s`, `max_attempts=3`, `jitter=True`. (Types reference: https://reference.langchain.com/python/langgraph/types/)

**Checkpointing super-step boundary**  
- **Claim supported**: when checkpoints are created.  
- LangGraph creates a checkpoint at each **super-step** boundary; for sequential `START -> A -> B -> END`, there are separate super-steps for input, A, and B, producing a checkpoint after each. (JS checkpointer reference: https://reference.langchain.com/javascript/langchain-langgraph/index/CompiledStateGraph/checkpointer)

---

## How It Works

### A. Build-time: specifying a StateGraph
1. **Define a state schema** (often `TypedDict`). Optionally attach reducers per key using `Annotated[..., reducer]`. (Use Graph API: https://docs.langchain.com/oss/python/langgraph/use-graph-api)
2. **Add nodes** with `add_node(name, fn)` where `fn(state) -> dict` returns partial updates. (StateGraph reference: https://reference.langchain.com/python/langgraph/graph/state/StateGraph)
3. **Add edges**:
   - Fixed: `add_edge("A", "B")` means B runs after A completes.
   - Conditional: `add_conditional_edges("A", router_fn, path_map)` means after A runs, evaluate `router_fn` and choose next node via `path_map` (or identity mapping). (Conditional semantics: https://github.com/langchain-ai/langgraph/discussions/3346)
4. **Compile**: `app = graph.compile(...)` to validate structure and attach runtime options (checkpointer, interrupts, debug). (Graph API overview: https://docs.langchain.com/oss/python/langgraph/graph-api ; compile reference: https://reference.langchain.com/python/langgraph/graph/state/StateGraph/compile)

### B. Run-time: super-steps, message passing, and state merging
1. **Initial activation**: execution begins with nodes scheduled from `START` (or entry point). Nodes are initially inactive and become active when they receive a message/state on an incoming edge/channel. (Graph API overview: https://docs.langchain.com/oss/python/langgraph/graph-api)
2. **Execute active nodes (within a super-step)**: all nodes scheduled for the current super-step run (potentially in parallel). Each node:
   - reads the current state snapshot
   - returns a dict of updates (partial state). (StateGraph compile reference: https://reference.langchain.com/python/langgraph/graph/state/StateGraph/compile)
3. **Merge updates into state** (per key):
   - If a key has a reducer: apply `reducer(old, update)` (and if multiple updates arrive for the same key in the same step, reducer aggregates them).
   - If no reducer: update overwrites the prior value. (Reducers discussion: https://github.com/langchain-ai/langgraph/discussions/3459)
4. **Route to next nodes**:
   - For fixed edges: schedule all downstream nodes.
   - For conditional edges: evaluate router function and map its output to the next node (or `END`). (Conditional semantics: https://github.com/langchain-ai/langgraph/discussions/3346)
5. **Checkpoint boundary (if enabled)**: at the end of each super-step, persist a `StateSnapshot` (values + next nodes + metadata) into the thread identified by `thread_id`. (JS checkpointer reference: https://reference.langchain.com/javascript/langchain-langgraph/index/CompiledStateGraph/checkpointer)
6. **Halting**: nodes with no incoming messages “vote to halt” (become inactive). Execution terminates when all nodes are inactive and no messages are in transit. (Graph API overview: https://docs.langchain.com/oss/python/langgraph/graph-api ; discussion: https://github.com/langchain-ai/langgraph/discussions/938)

### C. Conditional edges: exact routing semantics (what to quote)
Runtime procedure (as described in LangGraph discussion #3346):
1. Execute node `"chatbot"` to produce updates (e.g., `{"messages": [new_msg]}`).
2. Evaluate routing function on the current input (either a messages list or a state dict containing `"messages"`).
3. Router returns a label like `"tools"` or `END`.
4. `add_conditional_edges(from_node, router, mapping)` interprets router outputs via optional mapping dict (defaults to identity). (https://github.com/langchain-ai/langgraph/discussions/3346)

### D. Persistence across turns: threads and “why my state reset?”
1. If you compile **without** a checkpointer, each `invoke/stream` run starts from the provided input state; nothing is persisted across calls.
2. If you compile **with** a checkpointer, you must pass `configurable.thread_id` so the runtime can load/save checkpoints for that thread; reusing the same `thread_id` resumes accumulated state. (Issue #1568 resolution: https://github.com/langchain-ai/langgraph/issues/1568 ; JS checkpointer reference: https://reference.langchain.com/javascript/langchain-langgraph/index/CompiledStateGraph/checkpointer)

### E. Interrupt/resume mechanics (HITL)
1. Inside a node, call `interrupt(payload)`.
2. First call raises `GraphInterrupt` and surfaces payload to client; graph pauses.
3. Later, resume by invoking with `Command(resume=...)`.
4. On resume, the node is **re-executed from the start**, and the resume value becomes the return value of `interrupt()`. Requires checkpointing enabled. (Types reference: https://reference.langchain.com/python/langgraph/types/ ; HITL docs: https://docs.langchain.com/oss/python/langgraph/human-in-the-loop)

---

## Teaching Approaches

### Intuitive (no math)
- **State** is the shared “scratchpad” for the whole workflow.
- **Nodes** are steps that read the scratchpad and write back small changes.
- **Edges** are the arrows that decide which step runs next.
- **Reducers** are the “merge rules” for each scratchpad field (append vs overwrite).
- **Compile** is “turn my diagram into a runnable app,” plus attach runtime features like persistence and interrupts. (Graph API overview: https://docs.langchain.com/oss/python/langgraph/graph-api)

### Technical (with precise mechanics)
- Model the program as Pregel-like super-steps: active nodes run, emit partial updates, reducers merge updates into channels, edges schedule next active set, halt when no messages in transit. (Graph API overview: https://docs.langchain.com/oss/python/langgraph/graph-api)
- Node contract: `State -> Partial<State>`; reducer contract: `(Value, Value) -> Value`. (Compile reference: https://reference.langchain.com/python/langgraph/graph/state/StateGraph/compile)

### Analogy-based
- **Rail network**:
  - `add_edge` is a fixed track: the train must go there.
  - `add_conditional_edges` is a junction: after arriving, you look at the state and choose the next track. (Router tutorial: https://datmt.com/python/lesson-3-1-the-router-conditional-edges/)
- **Git commits**:
  - Each node returns a “diff” (partial update).
  - Reducers define how diffs apply (overwrite vs append/merge).
  - Checkpoints are saved snapshots you can resume from. (Checkpointing concepts in JS ref: https://reference.langchain.com/javascript/langchain-langgraph/index/CompiledStateGraph/checkpointer)

---

## Common Misconceptions

1. **“My node returns a full new state object; LangGraph replaces everything.”**  
   - **Why wrong**: Node functions return a **partial update dict**; only returned keys are merged into existing state. (Compile reference: https://reference.langchain.com/python/langgraph/graph/state/StateGraph/compile)  
   - **Correct model**: Treat node output as a patch: `State -> Partial<State>`, merged per key (with reducers if present).

2. **“If I annotate `messages` with `add_messages`, printing `state` inside the node should show the entire conversation across turns automatically.”**  
   - **Why wrong**: Without a **checkpointer + thread_id**, each run restarts from the provided input; nothing persists across invocations. This is exactly the issue in langgraph #1568; the fix is compiling with a checkpointer and passing `thread_id`. (Issue: https://github.com/langchain-ai/langgraph/issues/1568)  
   - **Correct model**: `add_messages` controls *merge within a run / within persisted state*, but persistence across turns requires checkpointing and a stable thread.

3. **“Reducers only matter when nodes run sequentially.”**  
   - **Why wrong**: Reducers are specifically important when **multiple updates** to the same key occur (often due to parallelism in a super-step). (StateGraph definition: https://reference.langchain.com/python/langgraph/graph/state/StateGraph ; discussion: https://github.com/langchain-ai/langgraph/discussions/938)  
   - **Correct model**: Reducers define how to aggregate concurrent updates to a channel; default is overwrite.

4. **“A conditional edge is just an if-statement inside the node.”**  
   - **Why wrong**: Conditional routing is evaluated by the graph runtime after node execution; the router returns a label that is mapped to next nodes via `add_conditional_edges`. (Conditional semantics: https://github.com/langchain-ai/langgraph/discussions/3346)  
   - **Correct model**: Node computes updates; router decides next node(s) based on current state/messages.

5. **“Interrupt resumes from the exact line after `interrupt()` without re-running earlier code.”**  
   - **Why wrong**: `interrupt()` pauses execution, and on resume the node is **re-executed from the start**; resume values are matched by interrupt call order. (Types reference: https://reference.langchain.com/python/langgraph/types/)  
   - **Correct model**: Write interrupting nodes to be safe under re-execution (idempotent or guarded), and rely on checkpointed state + resume values.

---

## Worked Examples

### Example 1 — Minimal StateGraph with reducer + conditional loop (Python)

```python
from typing_extensions import TypedDict, Annotated, Literal
from langgraph.graph import StateGraph, START, END

# Reducer: append ints to a list (matches reducer signature (Value, Value)->Value)
def append_list(old: list[int], update: int | None) -> list[int]:
    if update is None:
        return old
    return old + [update]

class State(TypedDict):
    x: Annotated[list[int], append_list]
    n: int

def increment(state: State) -> dict:
    # read last x, append next
    last = state["x"][-1]
    return {"x": last + 1}

def should_continue(state: State) -> Literal["increment", "__end__"]:
    # route based on current state
    if state["x"][-1] < state["n"]:
        return "increment"
    return END

builder = StateGraph(State)
builder.add_node("increment", increment)
builder.add_edge(START, "increment")
builder.add_conditional_edges("increment", should_continue, {"increment": "increment", END: END})

app = builder.compile()
out = app.invoke({"x": [0], "n": 3})
print(out)  # expected x accumulates via reducer
```

**What to point out while tutoring**
- Node returns only `{"x": ...}` (partial update), not full state. (Compile reference: https://reference.langchain.com/python/langgraph/graph/state/StateGraph/compile)
- Reducer controls accumulation for `x`. (StateGraph definition: https://reference.langchain.com/python/langgraph/graph/state/StateGraph)
- Conditional edge chooses whether to loop or end. (Conditional semantics: https://github.com/langchain-ai/langgraph/discussions/3346)

### Example 2 — “Why didn’t my messages append?” (checkpointing + thread_id)

This is the core fix from langgraph issue #1568: without a checkpointer, each run restarts.

```python
from typing_extensions import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver

class State(TypedDict):
    messages: Annotated[list, add_messages]

def echo(state: State) -> dict:
    # append an assistant message (placeholder)
    return {"messages": [("assistant", f"got: {state['messages'][-1].content if hasattr(state['messages'][-1], 'content') else state['messages'][-1]}")]}

builder = StateGraph(State)
builder.add_node("echo", echo)
builder.add_edge(START, "echo")
builder.add_edge("echo", END)

# Key: enable persistence
app = builder.compile(checkpointer=MemorySaver())

thread_config = {"configurable": {"thread_id": "1"}}

# Turn 1
app.invoke({"messages": ("user", "hi")}, thread_config)
# Turn 2 (same thread_id => state is loaded and add_messages can append)
app.invoke({"messages": ("user", "again")}, thread_config)
```

**Tutor notes**
- The issue’s resolution explicitly: “Insert a checkpoint, Otherwise, your graph will restart after each run.” plus pass `thread_id`. (https://github.com/langchain-ai/langgraph/issues/1568)
- This example is also a good moment to distinguish:
  - reducer behavior (`add_messages`) vs
  - persistence across invocations (checkpointer + thread). (JS checkpointer concepts: https://reference.langchain.com/javascript/langchain-langgraph/index/CompiledStateGraph/checkpointer)

---

## Comparisons & Trade-offs

| Concept | What it controls | Default behavior | When to choose |
|---|---|---|---|
| **No reducer on a state key** | How updates merge for that key | **Overwrite/replace** prior value | When the latest value should win (e.g., `status`, `final_answer`) (Reducers discussion: https://github.com/langchain-ai/langgraph/discussions/3459) |
| **Custom reducer** | Aggregation/merge semantics | Whatever you implement `(old, update)->new` | When you need accumulation (lists, counters) or conflict resolution across parallel updates (StateGraph definition: https://reference.langchain.com/python/langgraph/graph/state/StateGraph) |
| **`add_messages` reducer** | Message-list merging | ID-aware append/replace/delete | When managing chat history; supports edits and deletions better than naive concat (Implementation: https://github.com/langchain-ai/langgraph/blob/main/libs/langgraph/langgraph/graph/message.py ; rationale: https://github.com/langchain-ai/langgraph/discussions/3459) |
| **Reducer bypass `Overwrite(...)`** | Force set value ignoring reducer | Direct set | When you must reset/replace accumulated state (Types: https://reference.langchain.com/python/langgraph/types/) |
| **No checkpointer** | Persistence across runs | None | Stateless runs; simplest; cannot interrupt/resume (Issue #1568: https://github.com/langchain-ai/langgraph/issues/1568) |
| **Checkpointer + `thread_id`** | Durable state + resume | Checkpoint each super-step | Multi-turn memory, HITL interrupts, time travel, fault tolerance (JS checkpointer ref: https://reference.langchain.com/javascript/langchain-langgraph/index/CompiledStateGraph/checkpointer) |

---

## Prerequisite Connections

- **Python typing (`TypedDict`, `Annotated`)**: Needed to understand how state schemas are declared and how reducers are attached to keys. (Use Graph API: https://docs.langchain.com/oss/python/langgraph/use-graph-api)
- **Pure functions vs side effects**: Nodes can do side effects, but the graph’s correctness depends on understanding that nodes return partial updates merged into state. (Graph API overview: https://docs.langchain.com/oss/python/langgraph/graph-api)
- **Basic directed graphs (nodes/edges, branching, cycles)**: Needed to reason about execution order, loops, and conditional routing. (Graph API overview: https://docs.langchain.com/oss/python/langgraph/graph-api)
- **Event-driven / step-based execution**: Helps with the “super-step” model and why parallel nodes run in the same tick. (Graph API overview: https://docs.langchain.com/oss/python/langgraph/graph-api)

---

## Socratic Question Bank

1. **If a node returns `{"foo": 2}` and doesn’t mention `bar`, what should happen to `bar` in state—and why?**  
   *Good answer*: `bar` stays as-is because node outputs are partial updates merged into existing state. (Compile reference)

2. **Suppose two nodes run in the same super-step and both update `state["items"]`. What determines whether you get both updates or only one?**  
   *Good answer*: the reducer for `items`; default overwrite would lose one update, reducer can aggregate. (StateGraph definition)

3. **What exactly does a conditional router return: a node function, a boolean, or something else? How does that become the next node?**  
   *Good answer*: returns a label (often a string or `END`) mapped via `add_conditional_edges` path map. (Discussion #3346)

4. **Why might `add_messages` appear to “not work” across chat turns even if it’s correctly annotated?**  
   *Good answer*: without checkpointing + `thread_id`, each run restarts; nothing to append to. (Issue #1568)

5. **If you call `interrupt()` inside a node and then resume, what parts of the node run again? What does that imply for side effects?**  
   *Good answer*: node re-executes from the start; side effects must be guarded/idempotent. (Types reference)

6. **In the super-step model, when do downstream nodes run relative to the node that sent them updates? Same step or next step?**  
   *Good answer*: recipients run in the next super-step. (Graph API overview)

7. **When would you use `Overwrite(...)` instead of changing your reducer?**  
   *Good answer*: when you want a one-off reset/replace while keeping reducer behavior generally. (Types reference)

8. **What does compiling add beyond “turning it on”? Name one structural check and one runtime feature configured at compile time.**  
   *Good answer*: checks like no orphaned nodes; runtime options like checkpointer/interrupts/debug. (Graph API overview + compile reference)

---

## Likely Student Questions

**Q: What is the exact contract for a LangGraph node function?** → **A:** Nodes follow **`State -> Partial<State>`**: they receive the current state and return a dict of updates merged into state. (https://reference.langchain.com/python/langgraph/graph/state/StateGraph/compile)

**Q: How does LangGraph merge updates if multiple nodes write the same key?** → **A:** Each state key can have a reducer with signature **`(Value, Value) -> Value`** used to aggregate updates; if no reducer is specified, updates overwrite the prior value. (https://reference.langchain.com/python/langgraph/graph/state/StateGraph/compile ; https://github.com/langchain-ai/langgraph/discussions/3459)

**Q: What does `add_conditional_edges` expect my router to return?** → **A:** A label (e.g., `"tools"` or `END`) that is interpreted via an optional mapping dict (defaults to identity). (https://github.com/langchain-ai/langgraph/discussions/3346)

**Q: Why does my conversation history not persist between turns even with `add_messages`?** → **A:** Without a checkpointer, the graph restarts each run; to persist, compile with a checkpointer (e.g., `MemorySaver`) and pass `configurable.thread_id` on each call. (https://github.com/langchain-ai/langgraph/issues/1568)

**Q: What are the parameters to `StateGraph.compile()` and what does it return?** → **A:** `compile(checkpointer=None, *, cache=None, store=None, interrupt_before=None, interrupt_after=None, debug=False, name=None)` returns a `CompiledStateGraph` implementing Runnable methods like `invoke()` and `stream()`. (https://reference.langchain.com/python/langgraph/graph/state/StateGraph/compile)

**Q: How do interrupts work—does execution resume mid-node?** → **A:** `interrupt(value)` raises `GraphInterrupt` and pauses; resuming via `Command(resume=...)` re-executes the node from the start, and the resume value becomes the return value of `interrupt()`. Requires checkpointing. (https://reference.langchain.com/python/langgraph/types/)

**Q: What stream modes exist and what do they emit?** → **A:** `StreamMode` includes `"values"`, `"updates"`, `"checkpoints"`, `"tasks"`, `"debug"`, `"messages"`, `"custom"` with the semantics defined in the runtime types reference. (https://reference.langchain.com/python/langgraph/types/)

**Q: How can I force a state key to reset even if it has an append reducer?** → **A:** Wrap the returned value in `Overwrite(value=...)` to bypass the reducer; note multiple overwrites to the same channel in one super-step cause `InvalidUpdateError`. (https://reference.langchain.com/python/langgraph/types/)

---

## Available Resources

### Videos
- [Multi-Agent Systems with LangGraph](https://youtube.com/watch?v=Mi5wOpAgixw) — Surface when: the student asks for a high-level walkthrough of building graphs with nodes/edges/conditional routing and how this scales to multi-agent setups.
- [Intro to Large Language Models](https://youtube.com/watch?v=zjkBMFhNj_g) — Surface when: the student is missing broader agent context (why tool use + memory loops exist) and needs conceptual grounding before graph mechanics.

### Articles & Tutorials
- [Graph API overview - Docs by LangChain](https://docs.langchain.com/oss/python/langgraph/graph-api) — Surface when: the student asks “what is a node/edge/state in LangGraph?” or “what are super-steps?”
- [Use Graph API (LangGraph)](https://docs.langchain.com/oss/python/langgraph/use-graph-api) — Surface when: the student asks how to define state schemas, reducers, Send/Command, or overwrite behavior.
- [Human-in-the-loop overview (LangGraph)](https://docs.langchain.com/oss/python/langgraph/human-in-the-loop) — Surface when: the student asks how `interrupt()` works, why checkpointing is required, or how to resume.
- [Lesson 3.1: The Router (Conditional Edges)](https://datmt.com/python/lesson-3-1-the-router-conditional-edges/) — Surface when: the student needs a simple conditional routing example with a router function returning node names.
- [LangGraph agentic concepts](https://langchain-ai.github.io/langgraph/concepts/agentic_concepts/) — Surface when: the student asks how these primitives compose into real agent/workflow patterns (loops, tool routing, etc.).
- [LangGraph: Build Stateful, Multi-Agent Workflows (LangChain blog)](https://blog.langchain.dev/langgraph-multi-agent-workflows) — Surface when: the student asks for practical orchestration patterns beyond the minimal API.

---

## Visual Aids

![LLM agent architecture: planning, memory, and tool use components. (Weng, 2023)](/api/wiki-images/agent-fundamentals/images/lilianweng-posts-2023-06-23-agent_001.png)  
Show when: the student confuses “LangGraph state” with “LLM memory” or needs to see where stateful orchestration fits into the broader agent architecture (planning/memory/tools).

---

## Key Sources

- [StateGraph | langgraph - LangChain Reference Docs](https://reference.langchain.com/python/langgraph/graph/state/StateGraph) — Canonical definition of StateGraph, node signature, reducer signature, and “builder vs executable” warning.
- [`StateGraph.compile()` (LangGraph Python)](https://reference.langchain.com/python/langgraph/graph/state/StateGraph/compile) — Exact compile signature, reducer merge rule, and compiled graph runnable surface.
- [Graph API overview - Docs by LangChain](https://docs.langchain.com/oss/python/langgraph/graph-api) — Most explicit description of super-steps/message passing execution model.
- [LangGraph Runtime Types](https://reference.langchain.com/python/langgraph/types/) — Authoritative details on interrupts, streaming modes, Send, Overwrite, retry defaults.
- [Conditional Edges & Dynamic Routing Semantics (Discussion #3346)](https://github.com/langchain-ai/langgraph/discussions/3346) — Concrete runtime semantics for routers and `add_conditional_edges` mapping behavior.