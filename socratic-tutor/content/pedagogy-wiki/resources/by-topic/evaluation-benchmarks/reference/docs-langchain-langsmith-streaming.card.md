# Card: LangSmith/LangGraph Streaming API (runs + threads)
**Source:** https://docs.langchain.com/langsmith/streaming  
**Role:** reference_doc | **Need:** [WORKING_EXAMPLE] End-to-end runnable examples combining token streaming + step/event streaming + intermediate state inspection  
**Anchor:** Official streaming primitives/modes and how streamed outputs map to runs/threads for tracing & observability

## Key Content
- **Core workflow (run streaming):**
  1) `client = get_client(url=<DEPLOYMENT_URL>, api_key=<API_KEY>)`  
  2) (Stateful) `thread = await client.threads.create()` → `thread_id = thread["thread_id"]`  
  3) Stream a run:  
     `async for chunk in client.runs.stream(thread_id, assistant_id, input=inputs, stream_mode="updates"): print(chunk.data)`
- **Stateless run:** pass `None` instead of `thread_id` to avoid persisting outputs in the checkpointer DB:  
  `client.runs.stream(None, assistant_id, input=inputs, stream_mode="updates")`
- **Stream modes (run streaming):**
  - `values`: full graph state after each **super-step** (`.stream()`/`.astream()` with `stream_mode="values"`)
  - `updates`: state **updates** after each step; if multiple updates in same step (e.g., multiple nodes), streamed separately
  - `messages-tuple`: **token-by-token** LLM output + metadata (for chat UIs)
  - `debug`: “as much information as possible” incl. node name + full state
  - `custom`: user-defined streamed data from inside graph
  - `events`: all events (incl. state); mainly for migrating large LCEL apps (`.astream_events()`)
- **Multi-mode streaming:** `stream_mode=["updates","custom"]` → outputs are tuples `(mode, chunk)`.
- **Subgraph streaming:** set `stream_subgraphs=True` to include parent + subgraph outputs.
- **Token streaming shape (`messages-tuple`):** `chunk.data == (message_chunk, metadata)`; example filters `chunk.event != "messages"`. Print `message_chunk["content"]`. Metadata includes node/LLM invocation details (e.g., `langgraph_node`).
- **Join existing run:** `client.runs.join_stream(thread_id, run_id)`; **outputs not buffered** (miss earlier output).
- **Thread streaming vs run streaming (comparison table):**
  - Methods: `client.threads.join_stream()` vs `client.runs.stream()`
  - REST: `GET /threads/{thread_id}/stream` vs `POST /threads/{thread_id}/runs/stream`
  - Scope: all runs on thread vs single run; lifetime: indefinite vs closes on completion; creates run: no vs yes.
- **Thread stream modes:** `run_modes` (default; equivalent to run stream output), `lifecycle` (only run start/end). Example: `stream_mode=["lifecycle","state_update"]`.
- **Resumability (thread streams):** use `Last-Event-ID` / `last_event_id="<LAST_EVENT_ID>"`; pass `"-"` to replay from beginning.

## When to surface
Use when students ask how to stream LangGraph executions (tokens, step updates, full state, debug/events), how to choose `stream_mode`, how to stream subgraphs, or how to monitor/resume runs/threads for observability and production debugging.