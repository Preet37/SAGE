# Source: https://docs.temporal.io/activity-operations
# Title: Activity Operations | Temporal Platform Documentation
# Fetched via: browser
# Date: 2026-04-10

This page discusses the following:

Pause
Unpause
Reset
Update Options
Observability

Activity Operations are deliberate actions you perform on a specific Activity Execution, as opposed to lifecycle behaviors like retries and timeouts which happen automatically.

You can perform Activity Operations through the CLI, the UI, or directly via the gRPC API. Not all operations are available in all interfaces yet - see the summary table for current support. Activity Operations don't apply to Local Activities or Standalone Activities.

PUBLIC PREVIEW

Activity Operations are in Public Preview. Pause, Unpause, and Reset are available in Server v1.28.0+. Self-hosted UI requires v2.47.0+.

Activity Operations aren't available as SDK client methods. They're operational controls designed for the CLI, UI, and gRPC API - not for programmatic use in Workflow or Activity code.

Operations summary​
Operation	What it does	CLI
Pause	Stops retries. In-flight execution continues unless the Activity uses Heartbeat.	temporal activity pause
Unpause	Resumes a Paused Activity. The next execution starts immediately.	temporal activity unpause
Reset	Clears retry state (attempts, backoff) and schedules a new execution.	temporal activity reset
Update Options	Changes timeouts, Retry Policy, or Task Queue without restarting the Activity.	temporal activity update-options
Pause​

Pause stops the Temporal Service from scheduling new retries of an Activity Execution.

When to Pause​
An Activity is calling an external service that's experiencing issues, and you want to stop retries until the service recovers.
You need to inspect or change configuration before the Activity retries.
You're rolling out a new Worker version and want to hold specific Activities until the deploy is complete.
What happens when you Pause an Activity​
Pausing an Activity doesn't affect the parent Workflow. The Workflow continues Running, and Signals, Queries, and Updates on the parent Workflow are unaffected.
No further retries are scheduled. The Temporal Service stops scheduling retries. This is enforced server-side, not by the SDK.
Workflow code has no visibility into Activity Operations. Pause doesn't produce an Event History event, so the Workflow can't detect or react to it. See Observability.
Heartbeating determines whether the in-flight execution is interrupted:
Activities with Heartbeat are interrupted on their next Heartbeat. The SDK raises a Pause-specific error, and the Activity can catch this to clean up resources before exiting.
Activities without Heartbeat continue running to completion. If the execution succeeds, the result is delivered to the Workflow normally. If it fails, no retry is scheduled. Pause takes effect after the in-flight execution ends.
Pause is idempotent. Pausing an already-Paused Activity has no effect. Pausing a completed Activity returns an error.
CLI usage​
temporal activity pause \
  --workflow-id my-workflow \
  --activity-id my-activity \
  --reason "Downstream API is down, pausing until recovery"


See the CLI reference for temporal activity pause for all options, including --activity-type for targeting by type.

Detect Pause in Activity code​

Activities with Heartbeat can detect that an interruption was caused by Pause rather than a timeout or Workflow Cancellation. A Paused Activity resumes later. A Cancelled Activity doesn't. Your Activity code may need to handle these cases differently, for example releasing held resources on Pause while preserving them on Cancellation, or vice versa.

SDK	Version	How to detect Pause
Go	v1.34.0+	Catch activity.ErrActivityPaused
Java	v1.29.0+	Catch ActivityPausedException
TypeScript	v1.12.3+	Check cancellationDetails.paused === true
Python	v1.12.0+	Check cancellation_details().paused on asyncio.CancelledError
.NET	v1.7.0+	Check CancellationDetails.IsPaused on OperationCanceledException
Interaction with Workflow Pause​

Workflow Pause and Activity Pause are independent. Both stop Activity retries, but they must be Unpaused separately.

Workflow Pause blocks retries but doesn't interrupt in-flight executions via Heartbeat. Activity Pause does.
If both are active, both must be Unpaused before the Activity resumes.
Important considerations​
A Paused Activity can still time out. Pause doesn't stop or extend the Schedule-To-Close Timeout. Use update-options to adjust the timeout if needed.
Pause won't interrupt an Activity that doesn't Heartbeat. The current execution runs to completion, which could take up to the full Start-To-Close Timeout.
Pausing by --activity-type doesn't prevent new Activities of that type from running. The command Pauses Activities that are pending when it runs. Activities that start afterward are unaffected.
Limitations​
Pause doesn't support bulk operations. Unlike Unpause, Reset, and Update Options, there's no --query flag. You can only Pause Activities within a single Workflow, by Activity Id or by Activity type.
No Namespace-wide query for Paused Activities. You must know the Workflow Id. See Observability.
Unpause​

Unpause resumes a Paused Activity Execution.

When to Unpause​
The downstream service or dependency that caused you to Pause has recovered.
A code deploy or configuration change is complete and the Activity is safe to retry.
You Paused an Activity for investigation and are ready to let it proceed.
What happens when you Unpause an Activity​
The Activity is rescheduled immediately. Any remaining retry backoff is discarded. The next execution starts right away.
Attempt count and Heartbeat data are preserved by default. The Activity resumes from where it left off. Use --reset-attempts or --reset-heartbeats on the CLI to clear these, or use Reset to restart from attempt 1.

Unpause is idempotent. Unpausing an Activity that isn't Paused has no effect. Unpausing an Activity that has already completed returns an error.

CLI usage​
temporal activity unpause \
  --workflow-id my-workflow \
  --activity-id my-activity


See the CLI reference for temporal activity unpause for all options, including --reset-attempts and --reset-heartbeats to clear state on resume.

Important considerations​
Unpausing many Activities at once can overwhelm downstream services. If you Paused multiple Activities because a service was down, Unpausing them all at the same time sends all retries simultaneously. Consider Unpausing in batches to avoid overwhelming a recovering service.
Unpausing doesn't override Workflow Pause. If the parent Workflow is also Paused, Unpausing the Activity alone isn't enough. Both must be Unpaused before the Activity resumes. See Interaction with Workflow Pause.
Unpausing doesn't reset the attempt count. The Activity retries from its current attempt number. Use Reset to restart from attempt 1.
A Paused Activity can time out before you Unpause it. The Schedule-To-Close Timeout isn't stopped or extended while Paused. Use update-options to extend the timeout before Unpausing if needed.
Unpause doesn't interrupt or duplicate an in-flight execution. If an Activity without Heartbeat is still running when you Unpause, it continues to completion. The Temporal Service doesn't schedule a concurrent execution. If the in-flight execution fails, the next retry proceeds normally.
Reset​

Reset clears an Activity's retry state and schedules a fresh execution.

When to Reset​
An Activity has exhausted most of its retries, and you want to give it a fresh set after fixing the underlying issue.
A Paused Activity needs to start clean after a configuration change or code deploy.
You want to clear accumulated retry backoff and retry immediately instead of waiting for the next backoff interval.
A batch of Activities failed due to a transient issue and you want to restart them all with staggered jitter.
What happens when you Reset an Activity​
The attempt count resets to 1. The Activity gets a full set of retry attempts regardless of how many it had used.
Retry backoff is discarded. If the Activity was in a backoff wait, it's rescheduled to run immediately.
If the Activity is Paused, Reset also Unpauses it. Use --keep-paused to Reset the attempt count without resuming execution. With --keep-paused, the attempt count and Heartbeat data (if --reset-heartbeats) are reset, but the Activity stays Paused. No retry is scheduled until you Unpause separately.
Resetting an Activity doesn't affect the parent Workflow. The Workflow continues Running, and Signals, Queries, and Updates on the parent Workflow are unaffected.
Workflow code has no visibility into Activity Operations. Reset doesn't produce an Event History event, so the Workflow can't detect or react to it. See Observability.
Heartbeating determines whether an in-flight execution is interrupted:
Activities with Heartbeat are interrupted on their next Heartbeat. The SDK may raise a Reset-specific error so the Activity can clean up before exiting. The next execution starts at attempt 1.
Activities without Heartbeat continue running to completion. Reset doesn't cancel, interrupt, or schedule a concurrent execution. If the Activity was already retrying, the Temporal Service rejects the current execution's result because Reset changed the expected attempt number, and a fresh execution is scheduled after the Start-To-Close Timeout expires. If it was on its first execution, a successful result is still delivered to the Workflow normally.
Reset is idempotent. Resetting an Activity that's already at attempt 1 with no backoff has no effect. Resetting a completed Activity returns an error.
CLI usage​
temporal activity reset \
  --workflow-id my-workflow \
  --activity-id my-activity

# Reset retry state but don't resume yet
temporal activity reset \
  --workflow-id my-workflow \
  --activity-id my-activity \
  --keep-paused


See the CLI reference for temporal activity reset for all options, including --reset-heartbeats and bulk mode via --query.

Detect Reset in Activity code​

Activities with Heartbeat can detect that an interruption was caused by Reset rather than a timeout or Workflow Cancellation. A Reset Activity is retried from attempt 1. A Cancelled Activity isn't. Your Activity code may need to handle these cases differently, for example saving partial progress on Reset while discarding it on Cancellation.

SDK	How to detect Reset
Go	activity.GetCancellationDetails(ctx).Cause() returns activity.ErrActivityReset
Java	Catch ActivityResetException
TypeScript	Catch ApplicationFailure with error.type === "ActivityReset"
Python	Check cancellation_details().reset on asyncio.CancelledError
.NET	Check CancellationDetails.IsReset on OperationCanceledException
Important considerations​
A Reset Activity can still time out. Reset doesn't restart the Schedule-To-Close Timeout. The deadline is calculated from when the Activity was originally scheduled. Use update-options to extend the timeout before or after Reset.
Heartbeat details are preserved by default. If your Activity uses Heartbeat details for progress tracking and you want a clean restart, pass --reset-heartbeats.
Reset won't interrupt an Activity that doesn't Heartbeat. The current execution runs to completion, which could take up to the full Start-To-Close Timeout. If the Activity had already retried (attempt > 1), the Temporal Service rejects the current execution's result because Reset changed the expected attempt number. The Activity waits for its Start-To-Close Timeout to expire before a new execution is scheduled.
--restore-original-options restores the Activity's original configuration. It reverts timeouts, Retry Policy, and Task Queue to the values from when the Activity was first scheduled.
Resetting by --activity-type or --match-all doesn't affect new Activities of that type. The command Resets Activities that are pending when it runs. Activities that start afterward are unaffected.
Bulk Reset can overwhelm downstream services. When using --query to Reset Activities across many Workflows, use --jitter to stagger the restart times.
Update Options​

Update Options changes an Activity's runtime configuration without restarting it.

When to Update Options​
The Schedule-To-Close Timeout is about to expire on a Paused Activity, and you need to extend it before Unpausing.
An Activity's Retry Policy needs tuning based on observed failure patterns (for example, increasing the backoff interval or maximum attempts).
You want to move an Activity to a different Task Queue to route it to a specific set of Workers.
You need to restore an Activity's original configuration after a temporary override.
What happens when you Update an Activity's Options​

You can change timeouts (Schedule-To-Close, Start-To-Close, Schedule-To-Start, Heartbeat), Retry Policy (initial interval, maximum interval, backoff coefficient, maximum attempts), and Task Queue. Only the fields you specify are changed. All other options remain unchanged.

If the Activity is waiting for retry (scheduled), the new options take effect immediately. Any pending retry timer is regenerated with the updated configuration.
If the Activity is currently running, the new options are stored but take effect on the next execution. The in-flight execution isn't interrupted.
If the Activity is Paused, the new options are stored immediately. They take effect when the Activity is Unpaused and the next execution starts.
Workflow code has no visibility into Activity Operations. Update Options doesn't produce an Event History event, so the Workflow can't detect or react to it. See Observability.

Update Options is idempotent. Updating an Activity with the same values it already has produces no change. Updating options on an Activity that has already completed returns an error.

CLI usage​
temporal activity update-options \
  --workflow-id my-workflow \
  --activity-id my-activity \
  --schedule-to-close-timeout 24h


See the CLI reference for temporal activity update-options for all options, including Retry Policy, Task Queue, and bulk mode via --query.

Important considerations​
Changes to a running Activity take effect on the next execution, not the current one. If you need the change to apply immediately, the Activity must finish or fail its current execution first.
Updating by --activity-type or --match-all doesn't affect new Activities of that type. The command updates Activities that are pending when it runs. Activities that start afterward are unaffected.
--restore-original-options is batch-only. This flag only works with --query. It's silently ignored in single-workflow mode. It can't be combined with other option changes in the same command.
Limitations​
Update Options is CLI and gRPC only. It's not available in the UI.
Observability​

Activity Operations have a limited audit trail because they are not recorded in a Workflow's Event History. However, you can use the CLI and the UI to check Activity state and find Paused Activities for running Workflows.

Check Activity state​

temporal workflow describe shows the current state of each pending Activity, including whether it's Paused, its current attempt count, and last failure. The UI shows who performed an operation, when, and why (if a --reason was provided).

Find Paused Activities​

The TemporalPauseInfo Search Attribute is filterable by Activity type within a Workflow.

There's no Namespace-wide query to find all Paused Activities across Workflows. You must know the Workflow Id.

Audit trail​

Activity Operations don't produce Event History events. There is no record of a Pause, Reset, or option change in the Workflow's Event History. Nothing that reads the Event History - Workflow code, Replays, or external tooling - will see that an Operation occurred.

Evidence of an Operation is gone when the Activity completes or the Workflow closes. There's no persistent record that an Activity was Paused, Reset, or had its options changed.

The only way to confirm the current state of an Activity is temporal workflow describe or the UI.

Operations summary
Pause
When to Pause
What happens when you Pause an Activity
CLI usage
Detect Pause in Activity code
Interaction with Workflow Pause
Important considerations
Limitations
Unpause
When to Unpause
What happens when you Unpause an Activity
CLI usage
Important considerations
Reset
When to Reset
What happens when you Reset an Activity
CLI usage
Detect Reset in Activity code
Important considerations
Update Options
When to Update Options
What happens when you Update an Activity's Options
CLI usage
Important considerations
Limitations
Observability
Check Activity state
Find Paused Activities
Audit trail