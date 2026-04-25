# Card: LangGraph execution + state editing (super-steps, reducers, checkpoints)
**Source:** https://github.com/langchain-ai/langgraph/discussions/938  
**Role:** explainer | **Need:** CONCEPT_EXPLAINER  
**Anchor:** End-to-end execution model (state representation, manual edits, update semantics) + how it relates to checkpoints/threads

## Key Content
- **Graph primitives (definition):**  
  - **State** = shared snapshot (schema + per-key **reducers**).  
  - **Nodes** = functions that take current `state` (optionally `config`, `runtime`) and **return partial updates** (dict of keys→values).  
  - **Edges** = routing logic (fixed or conditional) selecting next node(s).
- **Execution model (Pregel-like “super-steps”):**  
  - Nodes start **inactive**; become **active** when they receive a message (state) on an incoming edge/channel.  
  - Active nodes run, emit updates/messages; recipients run in the **next super-step**.  
  - Nodes with no incoming messages “vote to halt” (become inactive).  
  - **Termination condition:** all nodes inactive **and** no messages in transit.
- **Reducers (per state key):**  
  - Default reducer = **overwrite** (latest update replaces prior value).  
  - Example reducer for chat history: `add_messages` appends to `messages` and handles message IDs + deserialization.
- **Parallelism rule:** if a node has **multiple outgoing edges**, **all** destination nodes execute **in parallel** in the next super-step.
- **Schema filtering + write-anywhere rule:** nodes may **write to any channel** in the graph’s *internal* state union, even if their **input schema** is a subset (input/output schemas can filter external I/O).
- **Checkpointing/thread config:** state snapshots include `values`, `next`, and `config` with `thread_id` + `checkpoint_id`; using the same `thread_id` reloads saved state for multi-turn continuity.
- **Human-in-the-loop procedure:** `interrupt(prompt_or_payload)` pauses; resume via `graph.invoke(Command(resume=...))`. Example: first call pauses; second call resumes with `"yes"`.

## When to surface
Use when students ask how LangGraph *actually runs* (super-steps, parallel nodes, halting), how state updates are merged (reducers), or how pausing/resuming and checkpointed threads relate to inspecting/modifying state mid-run.