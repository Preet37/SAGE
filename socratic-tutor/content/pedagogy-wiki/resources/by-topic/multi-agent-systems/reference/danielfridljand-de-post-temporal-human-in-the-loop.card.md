# Source: https://danielfridljand.de/post/temporal-human-in-the-loop
# Author: Daniel Fridljand
# Author Slug: daniel-fridljand
# Title: Temporal for Human-in-the-Loop: When You Don't Know How Long ...
# Fetched via: trafilatura
# Date: 2026-04-10

Temporal for Human-in-the-Loop: When You Don't Know How Long to Wait
Orchestrating workflows that depend on human input is tricky: you don’t know whether someone will respond in minutes or in days. Polling in a loop burns resources; fire-and-forget callbacks don’t survive restarts. In a recent project I used [Temporal](https://temporal.io/) to run such workflows reliably. This post summarizes why Temporal fits this problem and the patterns that worked well—without any project-specific details.
[Why Temporal Fits Human-in-the-Loop](#why-temporal-fits-human-in-the-loop)
Human-in-the-loop (HITL) here means: the workflow does some work, then waits for a human decision (e.g. approve/reject), and only then continues. The hard part is the wait: it can be seconds or weeks, and the process might be restarted in between.
Temporal gives you:
- Durable waits — The workflow can
await
a condition for hours or days without holding a thread or a DB connection. The workflow is persisted; when the condition is satisfied (e.g. via a signal), execution resumes. - Signals — External actors (e.g. your approval UI) send decisions into the workflow as signals. The workflow reacts when the signal arrives; no polling from inside the workflow.
- Queries — Read-only views of workflow state so UIs can show “waiting for approval” or “approved by X” without affecting execution.
- Deterministic replay — After a crash or deploy, Temporal replays the workflow from history. So you keep a single source of truth (workflow state) and avoid duplicate side effects.
Together, that means you can model “do work → wait for human → continue” as a single workflow that survives restarts and doesn’t guess how long the human will take.
[Patterns That Worked](#patterns-that-worked)
[1. Signal + wait condition for approval](#1-signal--wait-condition-for-approval)
The workflow sets a status (e.g. AWAITING_APPROVAL
) and then waits until a signal sets the decision:
@workflow.signal
async def approve(self, reviewer_id: str) -> None:
if self._status != Status.AWAITING_APPROVAL or self._decision is not None:
return # Idempotent: ignore if already decided
self._decision = "approved"
self._approved_by = reviewer_id
@workflow.run
async def run(self, timeout_days: int) -> dict:
# ... do work, then wait for human ...
self._status = Status.AWAITING_APPROVAL
try:
await workflow.wait_condition(
lambda: self._decision is not None,
timeout=timedelta(days=timeout_days),
)
except TimeoutError:
self._status = Status.REJECTED
return {"status": "timeout"}
# Continue with approved path...
The UI (or another service) queries workflow state to show the right screen and sends approve
or reject
via the Temporal client. No polling inside the workflow.
[2. Timeouts so workflows don’t hang forever](#2-timeouts-so-workflows-dont-hang-forever)
Without a timeout, a workflow could wait indefinitely if the human never responds. Using wait_condition(..., timeout=...)
gives you a clear outcome: either a decision arrives (signal) or the workflow times out and you can mark it rejected or escalate. That makes the system predictable and operable.
[3. Polling external systems with unknown completion time](#3-polling-external-systems-with-unknown-completion-time)
Sometimes the “human” part is actually an external API that completes asynchronously (e.g. a job queue). You don’t know how long it will take. A robust pattern is: run an activity that starts the job, then in the workflow loop—check status via an activity, break if done or failed, otherwise workflow.sleep(interval)
and retry, with an overall time budget. All sleep and branching is deterministic, so replays are safe.
# Conceptual: poll until done or timeout
while True:
if status in ("completed", "failed"):
break
if (workflow.now() - start).total_seconds() > max_wait_seconds:
break
await workflow.sleep(timedelta(seconds=poll_interval))
[4. Idempotent signals](#4-idempotent-signals)
Humans (or UIs) may send the same signal more than once. Making the signal handler idempotent—e.g. “if we already have a decision, return”—avoids race conditions and duplicate side effects when the workflow is replayed or the client retries.
[Engineering Takeaways](#engineering-takeaways)
- Reliability under failure — Workflows can wait for long, unpredictable human response times without holding resources, and they recover deterministically after restarts.
- Clear boundaries — Workflow code only orchestrates and waits; non-deterministic or external actions live in activities. That keeps replay correct and keeps I/O and business rules in one place.
- Operability — Explicit states (e.g.
AWAITING_APPROVAL
) and timeouts make it easier to reason about stuck workflows, set SLAs, and build dashboards.
If you’re designing systems where humans (or slow external systems) are in the loop and the wait time is unknown, Temporal’s model of durable waits and signals is a good fit. I found it much easier to reason about than ad-hoc queues and callbacks, and the replay guarantee made debugging and evolution safer.