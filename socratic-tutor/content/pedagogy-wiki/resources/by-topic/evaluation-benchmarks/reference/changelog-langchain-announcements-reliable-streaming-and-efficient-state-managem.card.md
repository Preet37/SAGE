# Card: Reliable streaming + efficient state management (LangGraph)
**Source:** https://changelog.langchain.com/announcements/reliable-streaming-and-efficient-state-management-in-langgraph  
**Role:** reference_doc | **Need:** DEPLOYMENT_CASE  
**Anchor:** Release-level guarantees/behavior changes for “reliable streaming” + “efficient state management”; recommended streaming/state patterns.

## Key Content
- **Release guarantees / behavior changes (LangGraph API/Cloud):**
  - Streaming runs now use the **same job queue as background runs** → **greater reliability** while keeping **low-latency real-time output**.
  - New streaming endpoint: `GET /threads/{thread_id}/runs/{run_id}/stream` and SDK: `client.runs.join_stream()` → stream output from **any run**, including **background runs** (supports UX where user leaves/returns and streaming continues).
  - Final state retrieval now reliable: `GET /threads/{thread_id}/runs/{run_id}/join` and SDK: `client.runs.join()` → **reliably returns final state values** whether run is ongoing or finished.
  - Thread status expanded: `GET /threads/{id}` / `client.threads.get()` now includes **`error`** and **`interrupted`** (in addition to existing **`idle`**, **`busy`**).
  - Streamlined state retrieval: `GET /threads/{id}` and `GET /threads` now include **latest state values** (fewer API calls; no separate “get state”).
  - Advanced search: `POST /threads/search` / `client.threads.search()` can filter by **thread state values** + status (enables “agent inbox” UIs).
- **Streaming procedures (graph runtime):**
  - Use `graph.stream(...)` / `graph.astream(...)` with `stream_mode` and **`version="v2"`** for unified StreamPart format.
  - Stream modes (table):  
    - `values`: full state snapshot after each step  
    - `updates`: only changed keys; **multiple updates in same step streamed separately**  
    - `messages`: `(message_chunk, metadata)` from LLM calls (**emitted even if model invoked via `.invoke`**)  
    - `custom`: arbitrary events via `get_stream_writer()` / injected `writer` arg  
    - `checkpoints`: checkpoint events (same format as `get_state()`; **requires checkpointer**)  
    - `debug`: “as much info as possible” incl. node name + full state
  - Subgraph streaming: pass `subgraphs=True`; streamed parts include `ns` namespace to distinguish root vs subgraph.

## When to surface
Use when students ask how LangGraph streaming became more reliable in production, how to stream/join runs via Threads/Runs endpoints, or how to choose stream modes for tokens, step updates, checkpoints, debugging, and observability.