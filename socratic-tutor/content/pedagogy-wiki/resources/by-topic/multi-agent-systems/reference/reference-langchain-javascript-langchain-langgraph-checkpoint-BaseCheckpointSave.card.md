# Card: BaseCheckpointSaver.list (LangGraph.js checkpoint listing)
**Source:** https://reference.langchain.com/javascript/langchain-langgraph-checkpoint/BaseCheckpointSaver/list  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Concrete semantics + parameters for listing checkpoints (filters/pagination) on `BaseCheckpointSaver`

## Key Content
- **Core concepts**
  - **Checkpoint** = snapshot of graph state at a superstep (enables “memory”, resumability, human-in-the-loop).
  - **CheckpointTuple** = `{ checkpoint, config, metadata, pendingWrites }` (checkpoint plus associated config/metadata/pending writes).
  - **Thread** = unique `thread_id` grouping a series of checkpoints (supports multi-tenant separation).
- **Required/optional run identifiers (configurable config)**
  - Always pass `thread_id`.
  - Optionally pass `checkpoint_id` to resume from a specific checkpoint within a thread.
  - Examples:
    - `{ configurable: { thread_id: "1" } }`
    - `{ configurable: { thread_id: "1", checkpoint_id: "0c62ca34-ac19-445d-bbb0-5b4984975b2a" } }`
- **Design rationale: pending writes for durable execution**
  - If a node fails mid-superstep, LangGraph stores **pending checkpoint writes** from nodes that already succeeded so resuming from that superstep avoids re-running successful nodes.
- **`BaseCheckpointSaver.list` / `alist` parameters (checkpoint retrieval semantics)**
  - `config`: base configuration used to scope listing (typically includes `configurable.thread_id`).
  - `filter`: additional filtering criteria (metadata filter).
  - `before`: list checkpoints created **before** this configuration (cursor-style pagination).
  - `limit`: maximum number of checkpoints to return.
  - Returns: `Iterator[CheckpointTuple]` (sync) / `AsyncIterator[CheckpointTuple]` (async).
- **Procedure: list checkpoints (JS example)**
  - `for await (const checkpoint of checkpointer.list(readConfig)) { console.log(checkpoint); }`

## When to surface
Use when students ask how to **enumerate checkpoints for a thread**, apply **metadata filters**, or implement **pagination** (`before`, `limit`) for resumable/human-approval workflows.