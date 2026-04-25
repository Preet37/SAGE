# Source: https://docs.temporal.io/workflows#workflow-timeouts
# Title: Temporal Docs — Workflow timeouts (Execution/Run/Task timeouts) and semantics
# Fetched via: search
# Date: 2026-04-10

## Workflow timeouts ​
Each Workflow timeout controls the maximum duration of a different aspect of a Workflow Execution.
Before we continue, we want to note that we generally do not recommend setting Workflow Timeouts, because Workflows are designed to be long-running and resilient.
Instead, setting a Timeout can limit its ability to handle unexpected delays or long-running processes.
If you need to perform an action inside your Workflow after a specific period of time, we recommend using a Timer.
Workflow timeouts are set when starting the Workflow Execution.
- **Workflow Execution Timeout** - restricts the maximum amount of time that a single Workflow Execution can be executed.
- **Workflow Run Timeout:** restricts the maximum amount of time that a single Workflow Run can last.
- **Workflow Task Timeout:** restricts the maximum amount of time that a Worker can execute a Workflow Task.
Set the timeout to either the `start_workflow()` or `execute_workflow()` asynchronous methods.
Available timeouts are:
- `execution_timeout`
- `run_timeout`
- `task_timeout`
View the source code
in the context of the rest of the application code.
```
# ...
result = await client.execute_workflow(
YourWorkflow.run,
"your timeout argument",
id="your-workflow-id",
task_queue="your-task-queue",
# Set Workflow Timeout duration
execution_timeout=timedelta(seconds=2),
# run_timeout=timedelta(seconds=2),
# task_timeout=timedelta(seconds=2),
)
```
## Workflow retries ​
...
A Retry Policy can work in cooperation with the timeouts to provide fine controls to optimize the execution experience.
Use a Retry Policy to retry a Workflow Execution in the event of a failure.
Workflow Executions do not retry by default, and Retry Policies should be used with Workflow Executions only in certain situations.
Set the Retry Policy to either the `start_workflow()` or `execute_workflow()` asynchronous methods.
View the source code
in the context of the rest of the application code.
```
# ...
handle = await client.execute_workflow(
YourWorkflow.run,
"your retry policy argument",
id="your-workflow-id",
task_queue="your-task-queue",
retry_policy=RetryPolicy(maximum_interval=timedelta(seconds=2)),
)
```

Each Workflow Timeout controls the maximum duration of a different aspect of a Workflow Execution.
Workflow Timeouts are set when starting the Workflow Execution.
Before we continue, we want to note that we generally do not recommend setting Workflow Timeouts, because Workflows are designed to be long-running and resilient.
Instead, setting a Timeout can limit its ability to handle unexpected delays or long-running processes.
If you need to perform an action inside your Workflow after a specific period of time, we recommend using a Timer.
- Workflow Execution Timeout
- Workflow Run Timeout
- Workflow Task Timeout
## Workflow Execution Timeout ​
**What is a Workflow Execution Timeout in Temporal?**
A Workflow Execution Timeout is the maximum time that a Workflow Execution can be executing (have an Open status) including retries and any usage of Continue As New.
Workflow Execution Timeout period
**The default value is ∞ (infinite).** If this timeout is reached, the Workflow Execution changes to a Timed Out status.
This timeout is different from the Workflow Run Timeout.
This timeout is most commonly used for stopping the execution of a Temporal Cron Job after a certain amount of time has passed.
## Workflow Run Timeout ​
**What is a Workflow Run Timeout in Temporal?**
A Workflow Run is the instance of a specific Workflow Execution.
Due to the potential for Workflow Retries or Continue-as-New, a Workflow Execution may have multiple Workflow runs.
For example, if a Workflow that specifies a Retry Policy initially fails and then succeeds during the next retry attempt, there is a single Workflow Execution that spans two Workflow Runs.
Both runs will share the same Workflow ID but have a unique Run ID to distinguish them.
A Workflow Run Timeout restricts the maximum duration of a single Workflow Run.
If the Workflow Run Timeout is reached, the Workflow Execution will be Timed Out.
Because this Timeout only applies to an individual Workflow Run, this does not include retries or Continue-As-New.
Workflow Run Timeout period
**The default is set to the same value as the Workflow Execution Timeout.** This timeout is most commonly used to limit the execution time of a single Temporal Cron Job Execution.
If the Workflow Run Timeout is reached, the Workflow Execution will be Timed Out.
## Workflow Task Timeout ​
**What is a Workflow Task Timeout in Temporal?**
A Workflow Task Timeout is the maximum amount of time allowed for a Worker to execute a Workflow Task after the Worker has pulled that Workflow Task from the Task Queue.
This Timeout is primarily available to recognize whether a Worker has gone down so that the Workflow Execution can be recovered on a different Worker.
Workflow Task Timeout period
**The default value is 10 seconds.** This timeout is primarily available to recognize whether a Worker has gone down so that the Workflow Execution can be recovered on a different Worker.
The main reason for increasing the default value is to accommodate a Workflow Execution that has an extensive Workflow Execution History, requiring more than 10 seconds for the Worker to load.
It's worth mentioning that although you can extend the timeout up to the maximum value of 120 seconds, it's not recommended to move beyond the default value.
## Detecting Workflow Task Failures ​
Use the `TemporalReportedProblems` Search Attribute to detect Workflows with failed Workflow Tasks.
A failed Workflow Task does not cause the Workflow to fail.
Some Tasks within a Workflow may be intended to fail.
For example, a Workflow Task may check a remote data source for new messages.
...
However, if your Workflow has a Task that fails and the failure is not handled, the Workflow will continue to run, but will not complete.
Detecting Workflows in this state is a common troubleshooting issue.
To identify Workflows with Task failures, you can use the Temporal Web UI.
See Task Failures View for more details.
You can also detect Workflows with Task failures by searching for the `TemporalReportedProblems` search attribute with your observability tools.
Activating Workflow Task Failure
To enable the Task Failures View for a Namespace, you need to update the Dynamic Config for that Namespace.
See Activating Task Failures View.

## Overview
This is a six part series focused on Temporal fundamentals.
It represents, in my words, what I have learned along the way and what I would’ve like to know on day one.
...
- Temporal Fundamentals Part II: Concepts
- Temporal Fundamentals Part III: Timeouts
- Temporal Fundamentals Part IV: Workflows
...
## Workflow Timeouts
There are several timeouts that can be configured for Temporal workflows.
The timers for these timeouts are handled by the Temporal service and as such are not visible to the workers.
### Workflow Execution Timeout
Total workflow execution timeout, including retries and any invocations of continue-as-new which generates a new run-id.
The default for this timeout is unlimited.
It is not recommended to use workflow execution timeout for business logic.
If for example, you need to timeout a workflow after X minutes, it would be recommended to use a timer instead.
The reason is that the workflow execution timeout cannot be caught in workflow code, the execution will be terminated instead from the service and workers will not be notified, meaning cancellation or cleanup is also not possible.
Use cases where it is recommended to use workflow execution timeout is when duration of workflow retries needs to be limited, with cron to limit duration of execution or with continue-as-new and finally possibly for integration or load testing.
### Workflow Run Timeout
Timeout for a single workflow execution or run.
Cannot be greater than workflow execution timeout.
The default is unlimited and again it is not recommended to change or set this timeout for same reasons as with workflow execution timeout.
The use cases of when to use this timeout is also similar to that of the workflow execution timeout.
The only difference being we are limiting a specific run or execution.
### Workflow Task Timeout
Timeout of a single workflow task.
Workflow execution is a coordination between workers and the Temporal service to progress a workflow to completion.
Workflow tasks are responsible for progressing your workflow code.
When a workflow is started, a workflow task is scheduled and picked up by a worker.
Workflow code is executed by a workflow task until it reaches a Temporal primitive (such as ExecuteActivity) where it returns next steps to the Temporal service for coordination.
The workflow task timeout, is the time from when a worker picks up a workflow task, until it responds with completion.
The default for the workflow task timeout is 10 seconds and the maximum time is two minutes.
It is critical that any code which can fail, happens inside an Activity and not workflow code which is coordinated through workflow tasks.
In addition workflow code should never block as that could result in a loop causing a stuck workflow that never progresses.
It is not recommended to change this timeout unless there is a very specific use case.
## Activity Timeouts
In Temporal, any code that can fail should be executed inside an activity.
Activities have granular retry policies but also several important timeouts that affect execution.
Activities have three possible states: scheduled, started and completed.
It is required that an Activity set either Start-to-Close or Schedule-to-Close timeout.
### Start-to-Close Timeout
This timeout is the length of time from when the activity was started to when it is completed.
This timeout should be set to just slightly longer than what we expect activity to run for.
### Schedule-to-Close Timeout
This timeout is the length of time from when the activity was scheduled to when it is completed.
As with Start-to-Close timeout, it should be set to just slightly longer than what we expect activity to run for.
If there are no workers or workers are busy, activity will sit on queue and remain scheduled so if that is possibility, it should also be taken into account.
### Schedule-to-Start Timeout
This timeout is the length of time from when the activity was scheduled to when it started.
This timeout should only be used in special cases, for example re-routing activity to a different task queue, if it is stuck on the queue and in a scheduled state.
Since Temporal workers can be scaled horizontally however, it is better to go with scaling approach (if possible) and simply scale up workers on task queue, as opposed to re-routing Activities to other queues.
### Heartbeat Timeout
This timeout measures the amount of time since the last heartbeat sent from an activity.
This timeout is useful for long-running activities, where it is important to reschedule activity, if there is a worker issue well in advance of Start-to-Close or Schedule-to-Close, which could be set to hours or even days.
Heartbeat timeout lets Temporal service reschedule activity quickly, in the event of some worker or infrastructure failure causing activity to not be completed.
If setting heartbeat timeout, it is critical to also heartbeat from the activity, otherwise timeout is ignored.
Activity should heartbeat more frequently that the StartToClose timeout.
SDK throttles heartbeats at 80 percent.
## Local Activity Timeouts
Local activities run inside of workflow tasks.
They are used for short lived read/write operations, for example persisting to a database.
They do not support heartbeats and are not suited for longer running activities.
Due to retries extending workflow task, local activities can cause delayed delivery of signals and even timeout query requests.
If using signals or queries with local activities it is important to consider the possible impact.
### Start-To-Close
This timeout is the length of time from when the local activity was started to when it is completed.
If local activity runs longer than the workflow task timeout, which defaults to 10 seconds, timers will be used to extend workflow task.
Again it is strongly recommended to avoid going beyond the 10 seconds and extending workflow task timeout.
As such, we should consider limiting retries of local activities.
### Schedule-To-Close
This timeout is the length of time from when the local activity was scheduled to when it is completed.
Same as with normal activity timeout, it should be set to just slightly longer than we expect Activity to run and as mentioned above, we want to be careful about extending workflow task timeout beyond the default 10 seconds.
## Summary
In this article we discussed Temporal timeouts.
There are two categories of timeouts, those that can be configured on the workflow and those that can be configure on the activity.
When configuring workflow timeouts, it is important to understand they are not visible to the worker and as such catching them and handling cancellation is not possible.
When configuring activity timeouts it is important to understand the difference between activities and local activities.
Appropriate configuration of timeouts, according to requirements is critical for proper function of Temporal workflows.

## Workflow Event History
A Workflow is comprised of a series of tasks.
Workflow tasks execute Workflow code and Activity tasks execute Activity code.
All of these tasks and their states (Scheduled, Started, Completed) are stored in the Workflow event history.
A single Workflow event history has limits on number of events (50,000) and size (50 MB).
**Recommendations**
- Ensure Workflow limits are not reached, otherwise Workflow will be terminated.
...
## Workflow Timeouts
Workflow tasks have a timeout of 10 seconds by default.
In addition, the SDK has a deadlock detector which is 1 second.
Workflow execution and run timeouts default to infinite.
**Recommendations**
- Do not change defaults unless you have a very specific reason.
- It is very important to not block Workflow code due to these important timeouts, as that will block and potentially cause stuck Workflows.
## Workflow Failure
Workflow code that throws a non-Temporal failure will cause Workflow task failure.
By default Workflow task will be retried every 10 seconds, infinity until it succeeds.
**Recommendations**
- Properly catch and throw exceptions.
...
A Timer in Temporal is a durable sleep, maintained by the Temporal service.
Timers are used to delay execution within a Workflow, or make business logic decisions based on time.
For example, failing a Workflow that doesn’t complete in X time, or cancelling an Activity that doesn’t complete in Y time.
**Recommendations**
- Never use the programming language sleep in Workflow, instead use Workflow.timer to sleep Workflow.
- When using timers for business logic decisions, if timer doesn’t fire it should be properly cancelled so it is reflected in event history.
- Use timers to cancel and fail Workflows that run too long, instead of Workflow timeout.
### Continue-As-New
The Continue-As-New primitive in Temporal allows for continuing Workflow, with a fresh or new event history.
This is useful for long-running Workflows to prevent reaching event history limits.
Continue-As-New allows for passing Workflow state from current runId/execution to a new one.
As such, it can also be used for Workflow migration, as well as, other such use cases where passing Workflow state, and continuing in a new Workflow is advantageous.

## CodeGPT
##### Mar 15, 2025
Download 1M+ code from https://codegive.com/4cb6491 
 okay, let's dive into the world of timeouts in temporal.  timeouts are a critical aspect of robust workflow design in temporal, allowing you to handle situations where activities or even entire workflows take longer than expected. temporal provides a variety of timeouts that you can configure at different levels, enabling you to control execution duration and prevent indefinite hangs. we'll cover the four primary types of timeouts, along with practical code examples in go (which is the language temporal is built in and most examples are in):
**the four key timeout types in temporal:**
1.  **workflow execution timeout:** the maximum allowed duration for the entire workflow execution. if the workflow doesn't complete within this time, it's automatically terminated.

2.  **workflow run timeout:** (also sometimes called workflow execution run timeout) limits the duration for a single execution of a workflow instance.

3.  **activity timeout:** the maximum allowed duration for a single activity execution (including retries if retries are configured).
4.  **heartbeat timeout:** a specialized timeout for activities that can take a very long time. it defines how frequently an activity must "heartbeat" (report its progress) to temporal.  if a heartbeat isn't received within this interval, temporal considers the activity to be stuck and can retry it.

**understanding the importance of timeouts:**
*   **preventing resource leaks:** timeouts ensure that workflows and activities don't run indefinitely, consuming resources and potentially causing system instability.

*   **handling errors and failures:**  timeouts are often used in conjunction with retry policies to gracefully handle transient errors or unexpected delays.  if an activity or workflow times out, it can be retried automatically (subject to retry policy limits), or the workflow can take alternative actions.

…

### Transcript
{ts:0.12} download this code from codeg give.com Link in the description below. okay let's dive into the world of timeouts in temporal timeouts are a critical aspect of robust workflow design in temporal allowing you to handle situations where activities or even entire workflows take longer than expected temporal provides a variety of
timeouts that you can configure at different levels enabling you to control execution duration and prevent definite hangs we'll cover the four primary types of timeouts along with practical code examples in go which is the language temporal is built in and most examples are in the four key timeout types in temporal asterisk one workflow execution timeout asterisk the maximum allowed duration
{ts:51.28} for the entire workflow execution if the workflow doesn't complete within this time it's automatically terminated two workflow run timeout asterisk also sometimes called workflow execution run timeout limits the duration for a single execution of a workflow instance three activity timeout asterisk the maximum allowed duration for a single activity execution including retries if retries are configured for heartbeat timeout asterisk A specialized timeout for activities that can take a very long time it defines finds how frequently an activity must heartbeat report its progress to temporal if a heartbeat isn't received within this interval temporal considers
the activity to be stuck and can retry {ts:103.759} it understanding the importance of timeouts asterisk asterisk preventing resource leaks asterisk timeouts ensure that workflows and activities don't run indefinitely consuming resources and potentially causing system instability asterisk handling errors and failures asterisk timeouts are often used in conjunction with retry policies to gracefully handle transient errors or unexpected delays if an activity or workflow times out it can be retried automatically subject to retry policy limits or the workflow can take alternative actions asterisk defining service level agreements sla's timeouts can be used to enforce slas
for example you can set a workflow execution timeout to guarantee that a {ts:155.879} particular business process completes within a certain time frame asterisk debugging and monitoring asterisk timeouts provide valuable information for debugging and monitoring workflows when a timeout occurs temporal records the event in its history which you can ED to diagnose the problem let's explore each timeout type with code examples as risk one workflow execution timeout this timeout applies to the entire lifetime of a workflow execution from its start to its completion or termination if the workflow doesn't finish within this time temporal automatically terminates it regardless of what the workflow is currently doing
asterisk use case asterisk to limit the total amount of time a workflow is allowed to run in ensuring that long {ts:210.72} running processes eventually terminate asterisk configuration asterisk specified when starting the workflow asterisk example go asterisk explanation asterisk asterisk we Define a long running activity that simulates a 15-second operation asterisk the timeout workflow calls this activity asterisk when starting the workflow c. execute workflow we set workflow execution time out to 5 Seconds since the activity takes 15 seconds to complete the entire workflow will exceed its time out and temporal will terminate it asterisk in the main
function we try to retrieve the workflow result but since the workflow is terminated we will see an error indicating that the timeout was exceeded {ts:266.0} asterisk we also specify schedule to close timeout and start to close timeout for the activity note that these apply to individual attempts of the activity since the activity takes longer
than these timeouts the activity execution will time out asterisk important asterisk the workflow execution timeout is a hard limit once it's reached the workflow is terminated and any ongoing activities are also cancelled this is different from other timeouts that may trigger retries two workflow run timeout asterisk use case asterisk to limit the total amount of time an
individual run of workflow is allowed to execute this is very similar to the above workflow execution timeout but will only be for a specific run of the workflow asterisk configuration asterisk {ts:323.0} specified when starting the workflow asterisk example go asterisk explanation asterisk almost identical to the workflow execution timeout example but we are using workflow run timeout in practice for most use cases they are interchangeable three activity timeout activity timeouts are the most common type of timeout you'll use in temporal workflows they control how long an individual activity execution is allowed to run there are two primary ways to configure activity
timeouts asterisk schedule to close timeout this is the maximum time from when the activity is scheduled to when it completes if the activity doesn't complete within this time it's {ts:375.08} considered a timeout this is typically the one you want to use asterisk start to close timeout this is the maximum time from when the activity starts executing to when it completes this time amount doesn't include the time spent waiting in the task Q asterisk use case asterisk prevent activities from running indefinitely even if the workflow itself has a longer time out this is crucial for handling network issues unresponsive services or buggy activity code asterisk
configuration asterisk configured within the activity options of the workflow asterisk example go asterisk EXP explanation asterisk asterisk the slow activity simulates an activity that takes 8 seconds to complete asterisk we {ts:428.639} configure the activity options with schedule to close time outs set to 5 Seconds since the
activity takes longer than 5 Seconds it will time out asterisk we also Define a retry policy with maximum attempts two this means that temporal will retry the Activity one time after the the initial timeout even with the retry the activity will likely still time out since it always takes 8 seconds asterisk the workflow will handle the activity timeout error and
either retry the activity if a retry policy is configured or proceed to a different branch of logic asterisk choosing between schedule to close timeout and start to close timeout asterisk asterisk generally schedule to close timeout is preferred it provides a more {ts:483.28} comprehensive timeout because it includes the time the activity spends in
the task Q waiting to be picked up by a worker this is important to ensure that the entire endtoend operation scheduling to completion stays within your expected bounds asterisk start to close timeout can be useful in specific scenarios where you only want to limit the actual execution time of the activity and don't want to factor in queuing delays four heartbeat
timeout heartbeat timeouts are specifically designed for activities that are expected to run for a very long time potentially hours or even days they allow the activity to Signal its progress to temporal periodically if temporal doesn't receive a heartbeat within the configured heartbeat time out it assumes the {ts:535.839} activity is stuck or unhealthy and can take action to typically retry the activity asterisk use case asterisk long running activities that perform operations like database backups data migrations or batch processing asterisk configuration asterisk configured within the activity options of the workflow the activity must explicitly call workflow. getet logger
CTX doino within its code to Signal the heartbeat asterisk example go asterisk explanation asterisk asterisk the heartbeat activity simulates a long running activity that iterates 10 times pausing for 2 seconds in each iteration asterisk inside the loop the activity calls workflow. getet activity info {ts:589.16} CTX heartbeat FN nil to send a heartbeat signal to temporal asterisk the activity options are configured with heartbeat timeout three asterisk time. second this means that the activity must send a heartbeat at least every 3 seconds since the activity is sending a heartbeat every 2 seconds it will not time out due to the

…

timeout should be significantly shorter than the {ts:640.88} schedule to close timeout and start to close timeout this allows temporal to detect issues with the activity more quickly asterisk the workflow. getet activity info CTX do heartbeat FN nil function is crucial for sending the heart beat signal you can also pass custom data to the heartbeat function if you want to
track the progress of the activity example the current iteration number the amount of data processed error handling and retries timeouts often result in errors that you need to handle within your workflows temporal provides retry policies to automatically retry activities or workflows that fail due to timeouts asterisk ret retry policies asterisk retry policies Define the criteria for retrying a failed activity {ts:694.92} or workflow you can configure the maximum number of attempts the back off interval between retries and the types of Errors to retry asterisk example with retry policy see the examples above the activity timeout example includes this best
practices for timeouts asterisk asterisk choose a appropriate values asterisk carefully consider the expected duration of your activities and workflows when setting timeout values don't set them too short leading to unnecessary retries or too long masking potential problems asterisk monitor timeouts asterisk use temporals monitoring and alerting capabilities to track timeout events this can help you identify activities or workflows that are {ts:747.88} consistently timing out and require optimization asterisk use heartbeats for long running activities asterisk if you have activities that are expected to run for a long time use heartbeat timeouts to ensure that they are healthy and responsive asterisk Implement error
handling asterisk gracefully handle timeout errors in your workflows by retrying activities or taking alternative actions in summary asterisk timeouts are an essential tool for building reliable and resilient temporal workflows by understanding the different types of timeouts and using them effectively you can prevent resource leaks handle errors gracefully and ensure that your workflows complete within expected time {ts:795.48} frames remember to consider the specific requirements of your workflows and activities when configuring timeouts and always monitor your system for timeout events to identify and address potential issues