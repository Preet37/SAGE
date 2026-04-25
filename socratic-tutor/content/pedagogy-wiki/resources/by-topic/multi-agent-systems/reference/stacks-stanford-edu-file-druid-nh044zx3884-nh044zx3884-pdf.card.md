# Card: Blackboard System Architecture & Control Cycle
**Source:** https://stacks.stanford.edu/file/druid:nh044zx3884/nh044zx3884.pdf  
**Role:** explainer | **Need:** CONCEPT_EXPLAINER  
**Anchor:** Architecture-level decomposition (blackboard, knowledge sources, control) + event-driven control/message flow for opportunistic problem solving.

## Key Content
- **Core components (Basic Blackboard Architecture, Summary sections):**
  - **Blackboard** = *global database containing ALL solution-state data*; organized into **levels** (often matching a solution decomposition / abstraction hierarchy) and **nodes** (attribute–value structures). Nodes can be **created/deleted dynamically**; nodes across levels can be **linked** (inter-node relations).
  - **Knowledge Sources (KSs)** = event-triggered specialist modules (“demons”) containing rules/procedures/tables; **only KSs may modify the blackboard**; KSs are **procedurally independent** (no KS references another KS directly).
  - **Control component** = event-based scheduling: selects focus of attention (context), selects events, selects and invokes triggered KS instances.

- **KS protocol / structure (Knowledge Sources summary):**
  - **Condition part** often split into **trigger** (event tokens) + **precondition** (executability test) + other filters.
  - **Action part** performs blackboard modifications, I/O, and **posts events**.

- **Primitive knowledge application cycle (Control III):**
  1) **Select an event**  
  2) **Select KS(s) triggered** by that event (in the event’s context)  
  3) **Execute KS instance** → **creates new events** (repeat)

- **Event-driven control loop with multiple event lists (Control Design Choices / Control Flow):**
  - Loop: **Select event list → select event(s) → determine triggered KSs → invoke KS(s)**.
  - Supports **clocked events** (activate when evaluation-time ≤ current time) and **periodic events** (repost with time incremented by Δt).
  - Scheduling alternatives: round-robin vs fixed priority vs dynamic utility weights; FIFO/LIFO/priority by token or time&token; execute one vs all triggered KSs.

- **Concrete example numbers (PROTEAN/881 state example):** Agenda shows **Executable: 98, 94, 86** (rated KSARs), illustrating rating-based scheduling.

## When to surface
Use when students ask how blackboard systems coordinate multiple agents/experts via shared state, how opportunistic control works (events→KS triggers→agenda/scheduler), or how to structure shared-state multi-agent workflows with conflict resolution via scheduling.