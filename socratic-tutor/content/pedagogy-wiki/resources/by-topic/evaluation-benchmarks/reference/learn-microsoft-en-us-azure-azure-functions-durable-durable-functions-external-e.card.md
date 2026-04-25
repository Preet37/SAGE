# Card: Durable Functions External Events (Wait/Raise) API + Semantics
**Source:** https://learn.microsoft.com/en-us/azure/azure-functions/durable/durable-functions-external-events  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** API surface for `WaitForExternalEvent` / `RaiseEvent` and correlation semantics

## Key Content
- **Purpose/use case:** Orchestrator functions can **wait for external events**—commonly for **human interaction** or other external triggers (human-in-the-loop signaling).
- **One-way async constraint:** External events are **one-way asynchronous**; **not suitable** when the sender needs a **synchronous response** from the orchestrator.
- **Wait API (orchestrator side):**
  - Isolated worker: `await context.WaitForExternalEventAsync<T>("EventName")`
  - In-process: `await context.WaitForExternalEvent<T>("EventName")`
  - Orchestrator declares **event name** and expected **payload type `T`**.
  - **Type conversion rule (.NET):** if payload can’t be converted to `T`, an **exception is thrown**.
- **Concurrency patterns:**
  - **Wait for any:** create multiple `WaitForExternalEvent*` tasks and `await Task.WhenAny(...)`.
  - **Wait for all:** `await Task.WhenAll(gate1, gate2, gate3)` before proceeding.
- **Indefinite wait + lifecycle/billing:**
  - Waits **indefinitely**; app/worker can be **stopped/unloaded** while waiting; instance is **awakened automatically** when event arrives.
  - **Consumption Plan:** **no billing charges** while an orchestrator is awaiting an external event task (regardless of duration).
- **Raise API (client side):**
  - `await client.RaiseEventAsync(instanceId, eventName, eventData)`
  - Event parameters: **`instanceId`**, **`eventName`**, **`eventData`** (must be **JSON-serializable**).
  - **Correlation:** `eventName` must **match** between sender and receiver.
  - **Delivery mechanics:** message is enqueued; if instance isn’t currently waiting on that `eventName`, it’s buffered (in-memory) until it starts listening.
  - **If no instance with `instanceId`:** event is **discarded**.
- **Reliability + dedup:**
  - External events have **at-least-once delivery** ⇒ duplicates possible (restarts/scaling/crashes).
  - Best practice: include a **unique ID** in events for **manual dedup** in orchestrators.
  - Storage note: **MSSQL provider** updates state transactionally ⇒ **no duplicate risk** vs **Azure Storage provider**, but unique IDs/names still recommended for portability.
- **HTTP raise-event example:**  
  `POST /runtime/webhooks/durabletask/instances/MyInstanceId/raiseEvent/Approval&code=XXX` with JSON body `"true"`.

## When to surface
Use when students ask how to implement **human approvals**, **pause/resume workflows**, or need exact semantics for **correlating**, **buffering**, **deduplicating**, and **billing behavior** of Durable Functions external events.