# Card: LangGraph human-in-the-loop via checkpointed interrupts (Pregel runtime)
**Source:** https://github.com/langchain-ai/langgraph/discussions/2290  
**Role:** code | **Need:** WORKING_EXAMPLE  
**Anchor:** Concrete pattern for pausing/resuming execution (human input) using checkpointing + deterministic graph runtime.

## Key Content
- **Design rationale (production agents):** LangGraph prioritizes **control + durability** over “easy start.” Agents differ from classic software mainly due to **latency (seconds→minutes→hours)** and need for: **Parallelization, Streaming, Task queue, Checkpointing, Human-in-the-loop, Tracing** (six-feature shortlist).
- **Why structured graphs (not one big while-loop):** Splitting into discrete nodes enables **checkpointing + human-in-the-loop**; execution state of arbitrary subroutines can’t be portably saved/resumed across machines.
- **Execution algorithm (Pregel/BSP) procedure (Section “Execution algorithm”):**
  - **Channels**: named data containers with **version** = monotonically increasing string.
  - **Nodes**: functions subscribing to channels; run when subscribed channel versions change.
  - **Input mapping**: initial input written to input channels triggers subscribed nodes.
  - **Output mapping**: agent returns values of output channels when execution halts.
  - **Per-iteration loop**:
    1) Select runnable nodes by comparing channel versions vs last-seen versions.  
    2) Execute selected nodes **in parallel** with **isolated copies** of state.  
    3) Nodes write updates locally.  
    4) Apply updates to channels in a **deterministic order** (prevents data races), bump versions.
  - Stop when no nodes runnable or **iteration limit** reached (developer-set constant).
- **Checkpointing details:** Save **serialized channel values** (default **MsgPack**, optionally encrypted), channel version strings, and “which versions each node has seen.” Enables resume **on any machine**, arbitrarily later.
- **Human-in-the-loop mechanism:** Add `interrupt()` inside a node to **pause**; later **resume from checkpoint** with human input (scales better than keeping processes waiting).

## When to surface
Use when students ask how LangGraph implements **durable execution**, **interrupt/resume human approval**, or why LangGraph uses **Pregel-style deterministic concurrency + checkpointing** instead of a simple loop.