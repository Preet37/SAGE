# Card: Temporal Activity Operations (Pause/Unpause/Reset/Update Options)
**Source:** https://docs.temporal.io/activity-operations  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Operational controls for Activity Executions + effects on retries/timeouts/heartbeats + observability limits

## Key Content
- **Scope/availability**
  - Applies to **Activity Executions** (not lifecycle behaviors). **Not for Local or Standalone Activities**.
  - **Public Preview**; available in **Server v1.28.0+**; self-hosted UI requires **v2.47.0+**.
  - **Not available as SDK client methods**; use **CLI/UI/gRPC**.
- **Pause (`temporal activity pause`)**
  - **Stops server-side scheduling of new retries**; parent Workflow keeps running (Signals/Queries/Updates unaffected).
  - **Heartbeat semantics:** with Heartbeat → interrupted on next Heartbeat (SDK raises pause-specific error); without Heartbeat → continues to completion; if it fails, **no retry scheduled**.
  - **Does not stop/extend Schedule-To-Close timeout**; may still time out → use **update-options** to adjust.
  - **Idempotent**; pausing completed Activity errors.
- **Unpause (`temporal activity unpause`)**
  - Reschedules **immediately**; **discard remaining retry backoff**.
  - **Attempts + Heartbeat data preserved by default**; optional `--reset-attempts`, `--reset-heartbeats`.
  - Doesn’t override **Workflow Pause**; both must be unpaused.
- **Reset (`temporal activity reset`)**
  - Clears retry state: **attempt resets to 1**, **backoff discarded**, rescheduled immediately.
  - If paused, Reset **also unpauses** unless `--keep-paused`.
  - Heartbeat: with Heartbeat → interrupted on next Heartbeat (reset-specific error); without Heartbeat → no interruption/concurrent run; if attempt>1, service **rejects current result** due to attempt mismatch; new execution after **Start-To-Close** expires.
  - `--restore-original-options` reverts timeouts/Retry Policy/Task Queue to original.
- **Update Options (`temporal activity update-options`)**
  - Change **timeouts** (Schedule-To-Close, Start-To-Close, Schedule-To-Start, Heartbeat), **Retry Policy** (initial interval, max interval, backoff coefficient, max attempts), **Task Queue**.
  - If waiting to retry → takes effect immediately (retry timer regenerated). If running → stored for **next execution**. If paused → stored; applies on unpause.
  - `--restore-original-options` works **only with `--query`** (batch); ignored in single-workflow mode.
- **Observability/audit**
  - Operations **do not create Workflow Event History events**; Workflow code/replay/tools reading history can’t detect them.
  - Check state via `temporal workflow describe` (paused flag, attempt, last failure) or UI (who/when/why). No namespace-wide query for paused activities; must know Workflow Id.

## When to surface
Use when students ask how Temporal operationally controls Activities (pause/unpause/reset/update), how Heartbeats affect interruption, how retries/backoff/attempts/timeouts behave, or why these actions aren’t visible in Workflow history.