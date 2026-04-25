# Card: LangGraph runtime + streaming modes (Pregel/BSP)
**Source:** https://blog.langchain.com/building-langgraph/  
**Role:** explainer | **Need:** CONCEPT_EXPLAINER  
**Anchor:** Design rationale for LangGraph’s runtime (graph execution model + why streaming exists) and concrete `graph.stream`/`graph.astream` pattern via `stream_mode` values.

## Key Content
- **Production needs driving design (6 features):** Parallelization (reduce *actual* latency), Streaming (reduce *perceived* latency), Task queue (reliable retries), Checkpointing (cheap retries), Human-in-the-loop (interrupt/resume), Tracing (visibility into agent loops).
- **Why streaming exists (latency rationale):** LLM agents run in **seconds/minutes/hours**; when you can’t reduce true latency without harming quality, stream useful intermediate info (progress/actions) up to **token-by-token** output.
- **Runtime architecture choice (Section “Execution algorithm”):** Uses **BSP/Pregel** to support **cycles/loops** and **deterministic concurrency** (avoid data races).
- **Execution model (algorithm steps):**
  - **Channels**: named data containers with **monotonically increasing version strings**.
  - **Nodes**: functions subscribing to channels; run when subscribed channel versions change.
  - **Loop per iteration:**  
    1) Select runnable nodes by comparing channel versions vs last-seen versions.  
    2) Execute selected nodes **in parallel** with **independent state copies**.  
    3) Apply node updates to channels in a **deterministic order**, bump versions.  
    4) Halt when no nodes runnable or **max iteration steps** reached (developer-set constant).
- **Streaming implementation + modes:** Engine emits stream output **inside nodes while running** and **at step boundaries** without custom developer code. Provides **6 stream modes**: `values`, `updates`, `messages`, `tasks`, `checkpoints`, `custom`. Example guidance: chatbots → `messages`; long-running agents → `updates`.
- **Checkpoint contents (for resume-anywhere):** serialized channel values (**MsgPack by default**, optionally encrypted), version strings, and record of last-seen channel versions per node.
- **Empirical scaling table (Big-O):**
  - **Planning a step:** nodes **O(1)**, edges **O(1)**, channels **O(n)**, active nodes **O(n)**, history **O(1)**, threads **O(1)**.
  - **History length is O(1)** across start/plan/run/finish (fetch latest checkpoint; no replay).

## When to surface
Use when students ask how LangGraph executes graphs with loops safely, why/what streaming provides in production agents, what `stream_mode` options mean, or how checkpointing/tracing enable debugging and observability.