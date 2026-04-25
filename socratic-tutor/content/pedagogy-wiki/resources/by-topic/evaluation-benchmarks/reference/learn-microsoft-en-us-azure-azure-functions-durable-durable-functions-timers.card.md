# Card: Durable Functions — Durable Timers (sleep/wait) semantics
**Source:** https://learn.microsoft.com/en-us/azure/azure-functions/durable/durable-functions-timers  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Durable timer API usage + semantics for long waits/timeouts (incl. human-approval wait patterns)

## Key Content
- **Use durable timers in orchestrators (not language `sleep`/`delay`)** to implement delays and timeouts in Durable Functions/Durable Task orchestrations.
- **Timer creation (Eq. 1: due-time form)**  
  - `dueTime = context.CurrentUtcDateTime + Δ` (e.g., `AddHours(72)`)  
  - `await context.CreateTimer(dueTime, cancellationToken)`  
  - Variables: `context.CurrentUtcDateTime` = orchestrator’s deterministic “now”; `Δ` = desired delay; `cancellationToken` controls cancellation.
- **Timer creation (Eq. 2: duration form)**  
  - `await context.CreateTimer(TimeSpan.FromHours(72), cancellationToken)`
- **Semantics:** awaiting the timer “sleeps” the orchestrator until expiration **while the orchestration can still process other incoming events** during the wait.
- **Underlying behavior:** creating a timer for time *T* enqueues a message that becomes visible at *T* (e.g., 4:30 PM UTC). If the app scales to zero, the visible timer message triggers reactivation on an appropriate VM.
- **Long-timer limits / behavior (numbers):**
  - **JavaScript, Python, PowerShell:** durable timers limited to **6 days**; workaround: loop with multiple timers to simulate longer delays.
  - **.NET and Java (up-to-date):** support **arbitrarily long** timers.
  - Some SDK/storage-provider combos may implement **≥6-day** waits as **multiple shorter timers** (e.g., **3-day** chunks); visible in logs/history but not orchestration behavior.
- **Time calculation rule:** don’t use built-in date/time APIs; always use orchestration context time (`context.CurrentUtcDateTime`, `ctx.current_utc_datetime`, `context.CurrentUtcDateTime` in JS).
- **Timeout pattern (procedure):**  
  1) Start activity task `activityTask = CallActivityAsync(...)`  
  2) Start timer `timeoutTask = CreateTimer(deadline, cts.Token)`  
  3) `winner = await Task.WhenAny(activityTask, timeoutTask)`  
  4) If activity wins: `cts.Cancel()` (cancels timer) else timeout.
- **Cancellation requirement:** if you create timers you won’t await, **cancel them**; orchestration won’t reach **“Completed”** until all outstanding tasks (incl. timers) are completed or canceled.
- **Consumption plan default:** abandoned activities still run/bill; default function timeout **5 minutes** (configurable).

## When to surface
Use when students ask how to implement long waits, human-approval delays, or timeouts in Durable Functions orchestrations, especially around determinism, scaling-to-zero behavior, timer limits (6 days), and cancellation/WhenAny patterns.